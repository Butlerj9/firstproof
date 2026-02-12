"""
P03 EXP-15f: n=4 perturbation via numpy modular arithmetic.
Uses numpy int64 arrays for fast matrix operations mod prime.
All heavy linear algebra is vectorized.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from itertools import permutations as perms

print("P03 EXP-15f: n=4 Numpy Modular Perturbation")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)

# Use a prime that fits well in int64 but is large enough
# We need p < 2^31 to avoid overflow in matrix products (since N*p^2 must fit in int64)
# N = 714, so N * p^2 < 2^63. p^2 < 2^63 / 714 ≈ 1.29e16. p < 1.14e8.
# Use p ≈ 10^8
PRIME = 104729  # small prime for testing, will use larger later
# Actually, for N=714 matrix products, each dot product sums N terms of size up to p-1.
# The sum can be up to N*(p-1)^2. For this to fit in int64: 714*(p-1)^2 < 2^63.
# (p-1)^2 < 2^63 / 714 ≈ 1.29e16. p < ~1.14e8.
# Use p = 99999989 (prime near 10^8)
PRIME = 99999989

# For verification, second prime
PRIME2 = 99999971

print(f"Prime 1: {PRIME}")
print(f"Prime 2: {PRIME2}")

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
print(f"N = {N} unknowns")

# Precompute k-stats
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
MAX_ORDER = 20
binom_table = np.zeros((MAX_P + 1, MAX_ORDER + 1), dtype=np.int64)
binom_table[:, 0] = 1
for p_val in range(1, MAX_P + 1):
    for k_val in range(1, min(p_val + 1, MAX_ORDER + 1)):
        binom_table[p_val, k_val] = binom_table[p_val - 1, k_val - 1] + binom_table[p_val - 1, k_val]

# Precompute dot products and t-exponents (these don't change with prime)
dot_products = np.zeros((N, N), dtype=np.int64)  # dot_products[van_idx, unk_idx]
t_exponents = np.zeros((N, N), dtype=np.int64)
dot_products_lead = np.zeros(N, dtype=np.int64)
t_exponents_lead = np.zeros(N, dtype=np.int64)

for i, nu in enumerate(van_comps):
    k = k_stats[nu]
    for j, m in enumerate(unk_monoms):
        dot_products[i, j] = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2] + nu[3]*m[3]
        t_exponents[i, j] = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2] + k[3]*m[3])
    dot_products_lead[i] = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2] + nu[3]*leading[3]
    t_exponents_lead[i] = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2] + k[3]*leading[3])


def build_matrix_mod(order, t_mod, t_inv_mod, p):
    """Build perturbation matrix A_order and rhs b_order as numpy arrays mod p."""
    A = np.zeros((N, N), dtype=np.int64)
    b = np.zeros(N, dtype=np.int64)

    for i in range(N):
        for j in range(N):
            dp = int(dot_products[i, j])
            te = int(t_exponents[i, j])
            bn = int(binom_table[dp, order]) if dp <= MAX_P and order <= MAX_ORDER else 0
            if te >= 0:
                tp = pow(int(t_mod), te, p)
            else:
                tp = pow(int(t_inv_mod), -te, p)
            A[i, j] = (bn * tp) % p

        dp_l = int(dot_products_lead[i])
        te_l = int(t_exponents_lead[i])
        bn_l = int(binom_table[dp_l, order]) if dp_l <= MAX_P and order <= MAX_ORDER else 0
        if te_l >= 0:
            tp_l = pow(int(t_mod), te_l, p)
        else:
            tp_l = pow(int(t_inv_mod), -te_l, p)
        b[i] = (-bn_l * tp_l) % p

    return A, b


def gauss_elim_np(A_in, b_in, p):
    """Gaussian elimination mod p using numpy. Returns pivots, RREF augmented matrix."""
    nrows, ncols = A_in.shape
    aug = np.zeros((nrows, ncols + 1), dtype=np.int64)
    aug[:, :ncols] = A_in % p
    aug[:, ncols] = b_in % p

    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r, col] % p != 0:
                piv = r
                break
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
    return pivots, aug


def solve_perturbation_numpy(t_num, t_den, p, max_order=MAX_ORDER):
    """Solve perturbation mod p using numpy for heavy operations."""
    t0_total = time.time()

    t_den_inv = pow(t_den, p - 2, p)
    t_mod = (t_num * t_den_inv) % p
    t_inv_mod = pow(t_mod, p - 2, p)

    # Build order 0 matrix
    print(f"    Building A0...", end=""); sys.stdout.flush()
    t0 = time.time()
    A0, b0 = build_matrix_mod(0, t_mod, t_inv_mod, p)
    print(f" {time.time()-t0:.1f}s")

    # RREF of A0
    print(f"    RREF of A0...", end=""); sys.stdout.flush()
    t0 = time.time()
    pivots0, aug0 = gauss_elim_np(A0, b0, p)
    rank0 = len(pivots0)
    pivot_cols0 = set(c for _, c in pivots0)
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    print(f" rank={rank0}, null={n_null} ({time.time()-t0:.1f}s)")

    # Particular solution
    c0_part = np.zeros(N, dtype=np.int64)
    for r, c in pivots0:
        c0_part[c] = aug0[r, N]

    # Null space basis as numpy matrix (N x n_null)
    null_mat = np.zeros((N, n_null), dtype=np.int64)
    for k, fc in enumerate(free_cols0):
        null_mat[fc, k] = 1
        for r, c in pivots0:
            null_mat[c, k] = (-aug0[r, fc]) % p

    # Left null space
    print(f"    Left null space...", end=""); sys.stdout.flush()
    t0 = time.time()
    A0T = A0.T.copy()
    pivsT, augT = gauss_elim_np(A0T, np.zeros(N, dtype=np.int64), p)
    pcT = set(c for _, c in pivsT)
    free_colsT = [c for c in range(N) if c not in pcT]
    n_left = len(free_colsT)

    left_mat = np.zeros((n_left, N), dtype=np.int64)  # n_left x N
    for l, fc in enumerate(free_colsT):
        left_mat[l, fc] = 1
        for r, c in pivsT:
            left_mat[l, c] = (-augT[r, fc]) % p
    print(f" dim={n_left} ({time.time()-t0:.1f}s)")

    # Build remaining A matrices
    print(f"    Building A1..A{max_order}...", end=""); sys.stdout.flush()
    t0 = time.time()
    A_mats = {0: A0}
    b_vecs = {0: b0}
    for order in range(1, max_order + 1):
        A_mats[order], b_vecs[order] = build_matrix_mod(order, t_mod, t_inv_mod, p)
    print(f" {time.time()-t0:.1f}s")

    # Perturbation iteration
    # Store c_k as: c_k = ck_base + null_mat @ alpha_k
    # where alpha_k encodes the null space contribution
    ck_bases = {0: c0_part}
    # For null contributions, store as N-vectors for each null direction
    # ck_null_coeffs[order] is a list of n_null N-vectors
    # Actually, let's store ck as full N-vectors for base and for each null direction
    ck_null_vecs = {0: null_mat}  # N x n_null matrix

    all_constraint_rows = []  # list of n_null-vectors
    all_constraint_rhs = []   # list of scalars

    for order in range(1, max_order + 1):
        t_order = time.time()

        # Build constraint: L * (b_order - sum_{m=1}^{order} A_m * c_{order-m}) = 0
        # Decompose c_{order-m} = base + null @ alpha
        # Constant part: L * b_order - sum L * A_m * base_{order-m}
        # Linear part: - sum L * A_m * null_{order-m} @ alpha

        # Constant part: n_left vector
        const = (left_mat @ b_vecs[order]) % p  # n_left vector

        # Linear part: n_left x n_null matrix
        lin = np.zeros((n_left, n_null), dtype=np.int64)

        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om not in ck_bases:
                continue
            # L * A_m * base_om
            Am_base = (A_mats[m_idx] @ ck_bases[om]) % p  # N vector
            L_Am_base = (left_mat @ Am_base) % p  # n_left vector
            const = (const - L_Am_base) % p

            if om in ck_null_vecs:
                # L * A_m * null_om: (n_left x N) @ (N x N) @ (N x n_null)
                # = (n_left x N) @ (N x n_null)
                Am_null = (A_mats[m_idx] @ ck_null_vecs[om]) % p  # N x n_null
                L_Am_null = (left_mat @ Am_null) % p  # n_left x n_null
                lin = (lin + L_Am_null) % p

        # Append constraints
        for l in range(n_left):
            all_constraint_rows.append(lin[l].tolist())
            all_constraint_rhs.append(int(const[l]))

        # Check cumulative rank
        n_constraints = len(all_constraint_rows)
        C_mat = np.array(all_constraint_rows, dtype=np.int64)
        C_rhs = np.array(all_constraint_rhs, dtype=np.int64)
        pvs, aug_acc = gauss_elim_np(C_mat, C_rhs, p)
        rank_cum = len(pvs)
        elapsed = time.time() - t_order
        total_time = time.time() - t0_total
        print(f"    Order {order}: rank={rank_cum}/{n_null} ({elapsed:.1f}s, total {total_time:.0f}s)")

        if rank_cum >= n_null:
            print(f"    ** CLOSED at order {order}! **")
            alpha = np.zeros(n_null, dtype=np.int64)
            for r, c in pvs:
                alpha[c] = aug_acc[r, n_null]
            c0 = (c0_part + null_mat @ alpha) % p
            return c0.tolist(), time.time() - t0_total

        # Compute c_k base and null for next iteration
        # A0 * c_k = b_k - sum_{m=1}^k A_m * c_{k-m}
        # base part: A0 * ck_base = b_k - sum A_m * base_{k-m}
        rhs_base = b_vecs[order].copy()
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_bases:
                rhs_base = (rhs_base - A_mats[m_idx] @ ck_bases[om]) % p

        _, aug_base = gauss_elim_np(A0, rhs_base, p)
        ck_base = np.zeros(N, dtype=np.int64)
        for r, c in pivots0:  # use original A0 pivots structure
            pass
        # Re-solve A0 properly
        pvs_b, aug_b = gauss_elim_np(A0, rhs_base, p)
        for r, c in pvs_b:
            ck_base[c] = aug_b[r, N]
        ck_bases[order] = ck_base

        # null part: A0 * ck_null[:,j] = -sum A_m * null_{k-m}[:,j] for each j
        ck_null = np.zeros((N, n_null), dtype=np.int64)
        rhs_null = np.zeros((N, n_null), dtype=np.int64)
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_null_vecs:
                rhs_null = (rhs_null - A_mats[m_idx] @ ck_null_vecs[om]) % p

        # Solve A0 * ck_null = rhs_null column by column
        # Since A0 is the same for all columns, we could batch this
        # For now, solve each column
        for j in range(n_null):
            pvs_j, aug_j = gauss_elim_np(A0, rhs_null[:, j], p)
            for r, c in pvs_j:
                ck_null[c, j] = aug_j[r, N]
        ck_null_vecs[order] = ck_null
        print(f"      c{order} computed ({time.time()-t_order:.1f}s)")

    print(f"    ** Did not close through order {max_order} **")
    return None, None


# Run
t_num, t_den = 7, 10
print(f"\nt = {t_num}/{t_den}, prime = {PRIME}")

result = solve_perturbation_numpy(t_num, t_den, PRIME)

if result[0] is not None:
    c0_mod, elapsed = result
    print(f"\n  Total time: {elapsed:.1f}s")

    # Quick symmetry check mod p
    print(f"\n  Checking symmetry mod p...")
    coeff_dict = {}
    for i, m in enumerate(unk_monoms):
        coeff_dict[m] = c0_mod[i] % PRIME
    coeff_dict[leading] = 1

    broken = 0
    total = 0
    for m, val in coeff_dict.items():
        for perm in perms(m):
            if perm > m and perm in coeff_dict:
                total += 1
                if coeff_dict[perm] % PRIME != val % PRIME:
                    broken += 1

    if broken == 0:
        print(f"  SYMMETRIC mod {PRIME} ({total} pairs)")
        print(f"\n  Verifying with second prime {PRIME2}...")
        result2 = solve_perturbation_numpy(t_num, t_den, PRIME2)
        if result2[0] is not None:
            c0_mod2 = result2[0]
            broken2 = 0
            coeff_dict2 = {}
            for i, m in enumerate(unk_monoms):
                coeff_dict2[m] = c0_mod2[i] % PRIME2
            coeff_dict2[leading] = 1
            for m, val in coeff_dict2.items():
                for perm in perms(m):
                    if perm > m and perm in coeff_dict2:
                        if coeff_dict2[perm] % PRIME2 != val % PRIME2:
                            broken2 += 1
            if broken2 == 0:
                print(f"  SYMMETRIC mod {PRIME2}")
                print(f"\n  ** SYMMETRY CONFIRMED mod TWO independent primes **")
            else:
                print(f"  BROKEN mod {PRIME2}: {broken2} pairs differ")
    else:
        print(f"  BROKEN: {broken}/{total} pairs differ mod {PRIME}")
else:
    print(f"\n  FAILED")

print(f"\n{'='*70}")
print("DONE")
