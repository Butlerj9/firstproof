"""
P03 EXP-15g: n=4 perturbation via fast numpy modular arithmetic.
Key optimization: pre-compute A0 transformation matrix once,
then batch-solve all RHS vectors via matrix multiplication.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from itertools import permutations as perms

print("P03 EXP-15g: n=4 Fast Numpy Modular Perturbation")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)

# Prime: need N * p^2 < 2^63. With N=714: p < 1.14e8
PRIME = 99999989

# Enumerate compositions
comps = []
for a in range(weight + 1):
    for b in range(weight + 1 - a):
        for c in range(weight + 1 - a - b):
            for d in range(weight + 1 - a - b - c):
                comps.append((a, b, c, d))

van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in comps if m != leading]
N = len(unk_monoms)
print(f"N = {N}")

def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i + 1, len(nu)):
        if nu[j] >= nu[i]: count += 1
    return count

k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}

# Precompute binomial coefficients
MAX_P = weight * weight
MAX_ORDER = 25
binom_table = np.zeros((MAX_P + 1, MAX_ORDER + 1), dtype=np.int64)
binom_table[:, 0] = 1
for p_val in range(1, MAX_P + 1):
    for k_val in range(1, min(p_val + 1, MAX_ORDER + 1)):
        binom_table[p_val, k_val] = binom_table[p_val - 1, k_val - 1] + binom_table[p_val - 1, k_val]


def build_matrix_mod(order, t_mod, t_inv_mod, p):
    """Build A_order and b_order as numpy int64 arrays mod p."""
    A = np.zeros((N, N), dtype=np.int64)
    b = np.zeros(N, dtype=np.int64)
    for i, nu in enumerate(van_comps):
        k = k_stats[nu]
        for j, m in enumerate(unk_monoms):
            te = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2] + k[3]*m[3])
            dp = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2] + nu[3]*m[3]
            bn = int(binom_table[dp, order]) if dp <= MAX_P else 0
            tp = pow(int(t_mod), te, p) if te >= 0 else pow(int(t_inv_mod), -te, p)
            A[i, j] = (bn * tp) % p
        te_l = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2] + k[3]*leading[3])
        dp_l = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2] + nu[3]*leading[3]
        bn_l = int(binom_table[dp_l, order]) if dp_l <= MAX_P else 0
        tp_l = pow(int(t_mod), te_l, p) if te_l >= 0 else pow(int(t_inv_mod), -te_l, p)
        b[i] = (-bn_l * tp_l) % p
    return A, b


def gauss_rref_mod(A_in, p):
    """Compute RREF of A mod p with transformation matrix.
    Returns: pivots, T (transformation matrix such that T @ A = RREF)."""
    nrows, ncols = A_in.shape
    # Augmented: [A | I]
    aug = np.zeros((nrows, ncols + nrows), dtype=np.int64)
    aug[:, :ncols] = A_in % p
    for i in range(nrows):
        aug[i, ncols + i] = 1

    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r, col] % p != 0:
                piv = r; break
        if piv is None:
            continue
        pivots.append((ri, col))
        if piv != ri:
            aug[[ri, piv]] = aug[[piv, ri]]
        inv_pv = pow(int(aug[ri, col]), p - 2, p)
        aug[ri] = (aug[ri] * inv_pv) % p
        for r in range(nrows):
            if r != ri and aug[r, col] % p != 0:
                f = int(aug[r, col])
                aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1

    T = aug[:, ncols:]
    return pivots, T


def solve_A0_batch(T, pivots, B_matrix, p):
    """Solve A0 @ X = B for multiple RHS columns.
    T: transformation matrix (N x N), pivots from RREF.
    B_matrix: (N x k) matrix of RHS vectors.
    Returns X: (N x k) matrix of solutions (free vars = 0)."""
    # TB = T @ B gives transformed RHS
    # For non-batched: TB = T @ b, then x[pivot_col] = TB[pivot_row]
    if B_matrix.ndim == 1:
        TB = np.zeros(len(T), dtype=np.int64)
        # Manual matrix-vector product to avoid overflow
        for i in range(len(T)):
            s = np.int64(0)
            for j in range(len(B_matrix)):
                s = (s + T[i, j] * B_matrix[j]) % p
            TB[i] = s
        X = np.zeros(len(B_matrix), dtype=np.int64)
        for ri, ci in pivots:
            X[ci] = TB[ri] % p
        return X

    k = B_matrix.shape[1]
    # For batch: split into chunks to manage memory and overflow
    X = np.zeros((B_matrix.shape[0], k), dtype=np.int64)
    # Process in chunks
    chunk_size = 50
    for start in range(0, k, chunk_size):
        end = min(start + chunk_size, k)
        B_chunk = B_matrix[:, start:end]
        # Manual modular matmul for reliability
        n_rhs = end - start
        TB_chunk = np.zeros((len(T), n_rhs), dtype=np.int64)
        for row_block in range(0, len(T), 100):
            row_end = min(row_block + 100, len(T))
            for col_block in range(0, B_chunk.shape[0], 100):
                col_end = min(col_block + 100, B_chunk.shape[0])
                partial = T[row_block:row_end, col_block:col_end] @ B_chunk[col_block:col_end, :]
                TB_chunk[row_block:row_end] = (TB_chunk[row_block:row_end] + partial) % p
        for ri, ci in pivots:
            X[ci, start:end] = TB_chunk[ri] % p
    return X


def modular_matmul(A, B, p):
    """Compute (A @ B) mod p safely for int64, handling potential overflow.
    Uses chunked multiplication."""
    m, k = A.shape
    k2, n = B.shape
    assert k == k2
    C = np.zeros((m, n), dtype=np.int64)
    # Process in row/column chunks
    chunk = 100  # chunk size to limit intermediate values
    for i_start in range(0, k, chunk):
        i_end = min(i_start + chunk, k)
        partial = A[:, i_start:i_end] @ B[i_start:i_end, :]
        C = (C + partial) % p
    return C


def gauss_elim_constraint(C_mat, C_rhs, n_null, p):
    """Gaussian elimination on constraint system. Returns rank and pivots."""
    nrows = len(C_mat)
    ncols = n_null
    aug = np.zeros((nrows, ncols + 1), dtype=np.int64)
    for i in range(nrows):
        aug[i, :ncols] = np.array(C_mat[i], dtype=np.int64)
        aug[i, ncols] = C_rhs[i]
    aug = aug % p

    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r, col] % p != 0:
                piv = r; break
        if piv is None:
            continue
        pivots.append((ri, col))
        if piv != ri:
            aug[[ri, piv]] = aug[[piv, ri]]
        inv_pv = pow(int(aug[ri, col]), p - 2, p)
        aug[ri] = (aug[ri] * inv_pv) % p
        for r in range(nrows):
            if r != ri and aug[r, col] % p != 0:
                f = int(aug[r, col])
                aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1
    return len(pivots), pivots, aug


def solve_perturbation(t_num, t_den, p, max_order=MAX_ORDER):
    """Full perturbation solve mod p."""
    t_total = time.time()

    t_den_inv = pow(t_den, p - 2, p)
    t_mod = (t_num * t_den_inv) % p
    t_inv_mod = pow(t_mod, p - 2, p)

    # Build A0
    print(f"    Building A0...", end=""); sys.stdout.flush()
    t0 = time.time()
    A0, b0 = build_matrix_mod(0, t_mod, t_inv_mod, p)
    print(f" {time.time()-t0:.1f}s")

    # RREF + transformation matrix
    print(f"    RREF with transform...", end=""); sys.stdout.flush()
    t0 = time.time()
    pivots0, T0 = gauss_rref_mod(A0, p)
    rank0 = len(pivots0)
    pivot_cols0 = set(c for _, c in pivots0)
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    print(f" rank={rank0}, null={n_null} ({time.time()-t0:.1f}s)")

    # Particular solution for A0 * c0 = b0
    c0_part = solve_A0_batch(T0, pivots0, b0, p)

    # Null space basis (N x n_null)
    null_mat = np.zeros((N, n_null), dtype=np.int64)
    # From RREF: T0 @ A0 = RREF. The RREF has zeros in free columns.
    # null_vec[free_col_k] has 1 at free_cols0[k], and for each pivot (ri, ci):
    #   null_vec[ci] = -(RREF[ri, free_cols0[k]]) = -(T0 @ A0)[ri, free_cols0[k]]
    # But we need RREF directly. Let's compute it.
    RREF = modular_matmul(T0, A0, p)
    for k, fc in enumerate(free_cols0):
        null_mat[fc, k] = 1
        for ri, ci in pivots0:
            null_mat[ci, k] = (-RREF[ri, fc]) % p

    # Left null space (need left null of A0)
    print(f"    Left null space...", end=""); sys.stdout.flush()
    t0 = time.time()
    pivsT, TT = gauss_rref_mod(A0.T.copy(), p)
    pcT = set(c for _, c in pivsT)
    free_colsT = [c for c in range(N) if c not in pcT]
    n_left = len(free_colsT)

    RREFT = modular_matmul(TT, A0.T.copy(), p)
    left_mat = np.zeros((n_left, N), dtype=np.int64)
    for l, fc in enumerate(free_colsT):
        left_mat[l, fc] = 1
        for ri, ci in pivsT:
            left_mat[l, ci] = (-RREFT[ri, fc]) % p
    print(f" dim={n_left} ({time.time()-t0:.1f}s)")

    # Build remaining perturbation matrices
    print(f"    Building A1..A{max_order}...", end=""); sys.stdout.flush()
    t0 = time.time()
    A_mats = {0: A0}
    b_vecs = {0: b0}
    for order in range(1, max_order + 1):
        A_mats[order], b_vecs[order] = build_matrix_mod(order, t_mod, t_inv_mod, p)
    print(f" {time.time()-t0:.1f}s")

    # Perturbation iteration
    ck_bases = {0: c0_part}
    ck_nulls = {0: null_mat}  # N x n_null

    all_C_rows = []
    all_C_rhs = []

    for order in range(1, max_order + 1):
        t_order = time.time()

        # Constraint: L * (b_order - sum A_m c_{order-m}) = 0
        # Split c_{order-m} = base + null @ alpha
        # Constant: L * b_order - sum L * A_m * base_{order-m}
        # Linear in alpha: sum L * A_m * null_{order-m}

        L_b = modular_matmul(left_mat, b_vecs[order].reshape(-1, 1), p).flatten()  # n_left
        const = L_b.copy()
        lin = np.zeros((n_left, n_null), dtype=np.int64)

        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om not in ck_bases:
                continue
            Am = A_mats[m_idx]
            # L * Am * base_om
            Am_base = modular_matmul(Am, ck_bases[om].reshape(-1, 1), p).flatten()
            L_Am_base = modular_matmul(left_mat, Am_base.reshape(-1, 1), p).flatten()
            const = (const - L_Am_base) % p

            if om in ck_nulls:
                # L * Am * null_om: (n_left x N) @ (N x N) @ (N x n_null)
                Am_null = modular_matmul(Am, ck_nulls[om], p)  # N x n_null
                L_Am_null = modular_matmul(left_mat, Am_null, p)  # n_left x n_null
                lin = (lin + L_Am_null) % p

        # Append constraints
        for l in range(n_left):
            all_C_rows.append(lin[l].tolist())
            all_C_rhs.append(int(const[l]))

        # Check rank
        rank_cum, pvs, aug = gauss_elim_constraint(all_C_rows, all_C_rhs, n_null, p)
        elapsed = time.time() - t_order
        total = time.time() - t_total
        print(f"    Order {order}: rank={rank_cum}/{n_null} ({elapsed:.1f}s, total {total:.0f}s)")

        if rank_cum >= n_null:
            print(f"    ** CLOSED at order {order}! **")
            alpha = np.zeros(n_null, dtype=np.int64)
            for ri, ci in pvs:
                alpha[ci] = aug[ri, n_null]
            c0 = (c0_part + modular_matmul(null_mat, alpha.reshape(-1, 1), p).flatten()) % p
            return c0, time.time() - t_total

        # Compute c_{order} for next iteration
        # base: A0 * ck_base = b_order - sum A_m * base_{order-m}
        rhs_base = b_vecs[order].copy()
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_bases:
                Am_base = modular_matmul(A_mats[m_idx], ck_bases[om].reshape(-1, 1), p).flatten()
                rhs_base = (rhs_base - Am_base) % p
        ck_bases[order] = solve_A0_batch(T0, pivots0, rhs_base, p)

        # null: A0 * ck_null = -sum A_m * null_{order-m}
        rhs_null = np.zeros((N, n_null), dtype=np.int64)
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_nulls:
                Am_null = modular_matmul(A_mats[m_idx], ck_nulls[om], p)
                rhs_null = (rhs_null - Am_null) % p
        ck_nulls[order] = solve_A0_batch(T0, pivots0, rhs_null, p)
        print(f"      c{order} computed ({time.time()-t_order:.1f}s)")

    return None, None


# Run
t_num, t_den = 7, 10
print(f"\nt = {t_num}/{t_den}, p = {PRIME}")
c0, elapsed = solve_perturbation(t_num, t_den, PRIME)

if c0 is not None:
    print(f"\nTotal: {elapsed:.1f}s")

    # Symmetry check mod p
    coeff_dict = {}
    for i, m in enumerate(unk_monoms):
        coeff_dict[m] = int(c0[i]) % PRIME
    coeff_dict[leading] = 1

    broken = 0
    total = 0
    for m, val in coeff_dict.items():
        for perm in perms(m):
            if perm > m and perm in coeff_dict:
                total += 1
                if coeff_dict[perm] % PRIME != val % PRIME:
                    broken += 1

    status = "SYMMETRIC" if broken == 0 else f"BROKEN ({broken}/{total})"
    print(f"\nSymmetry check mod {PRIME}: {status}")

    if broken == 0:
        # Verify with second prime
        PRIME2 = 99999971
        print(f"\nVerifying with p2 = {PRIME2}...")
        c0_2, elapsed2 = solve_perturbation(t_num, t_den, PRIME2)
        if c0_2 is not None:
            broken2 = 0
            for i, m in enumerate(unk_monoms):
                val2 = int(c0_2[i]) % PRIME2
                for perm in perms(m):
                    if perm > m and perm in {mm: True for mm in unk_monoms}:
                        j = unk_monoms.index(perm)
                        if int(c0_2[j]) % PRIME2 != val2:
                            broken2 += 1
            if perm == leading and val2 != 1:
                broken2 += 1

            if broken2 == 0:
                print(f"SYMMETRIC mod {PRIME2}")
                print(f"\n*** SYMMETRY CONFIRMED mod TWO primes ***")
            else:
                print(f"BROKEN mod {PRIME2}: {broken2} pairs")
else:
    print(f"\nFAILED: did not close")

print(f"\n{'='*70}")
print("DONE")
