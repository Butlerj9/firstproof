"""
P03 EXP-13: Third-order perturbation theory for Symmetry Conjecture.

Previous results (exp10): orders 0-2 give rank 35/49, leaving 14 free params.
This experiment adds order-3 constraints to attempt full determination of c0.
If rank reaches 49, we can reconstruct c0 exactly and verify symmetry.

Stop-loss: if order 3 doesn't close, PARK P03.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from itertools import permutations

print("P03 EXP-13: Order-3 perturbation for n=3 Symmetry Conjecture")
print("=" * 70)

n = 3
leading = (0, 2, 3)

# All compositions of weight <= 5 into 3 parts
comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

monoms = list(comps)
van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in monoms if m != leading]
N = len(unk_monoms)  # 55

def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i+1, len(nu)):
        if nu[j] >= nu[i]: count += 1
    return count

k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}

def falling_fact(p, k):
    """p*(p-1)*...*(p-k+1) as Fraction."""
    r = Fraction(1)
    for i in range(k):
        r *= Fraction(p - i)
    return r

def binom_frac(p, k):
    """Generalized binomial C(p,k) = p!/(k!(p-k)!) for integer p >= 0."""
    if k < 0: return Fraction(0)
    if k == 0: return Fraction(1)
    fk = Fraction(1)
    for i in range(1, k+1):
        fk *= Fraction(i)
    return falling_fact(p, k) / fk

def build_matrices(t_val, max_order=3):
    """Build perturbation matrices A0..A_{max_order} and b0..b_{max_order}."""
    matrices = {k: [] for k in range(max_order+1)}
    rhs = {k: [] for k in range(max_order+1)}

    for nu in van_comps:
        k = k_stats[nu]
        for order in range(max_order+1):
            row = []
            for m in unk_monoms:
                t_exp = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2])
                p = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2]
                tp = t_val ** t_exp
                row.append(binom_frac(p, order) * tp)
            matrices[order].append(row)

            t_exp_l = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2])
            p_l = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2]
            tp_l = t_val ** t_exp_l
            rhs[order].append(-binom_frac(p_l, order) * tp_l)

    return matrices, rhs

def gauss_elim(mat, rhs_vec, nrows, ncols):
    """RREF of [mat | rhs]. Returns (pivots, reduced augmented matrix)."""
    aug = [mat[i][:] + [rhs_vec[i]] for i in range(nrows)]
    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r][col] != Fraction(0):
                piv = r; break
        if piv is None: continue
        pivots.append((ri, col))
        if piv != ri: aug[ri], aug[piv] = aug[piv], aug[ri]
        pv = aug[ri][col]
        for j in range(ncols+1): aug[ri][j] /= pv
        for r in range(nrows):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(ncols+1): aug[r][j] -= f * aug[ri][j]
        ri += 1
    return pivots, aug

def solve_via_rref(A0_pivots, A0_aug, rhs_vec, ncols):
    """Solve A0 x = rhs using precomputed RREF. Free vars = 0."""
    aug = [A0_aug[i][:ncols] + [rhs_vec[i]] for i in range(len(rhs_vec))]
    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, len(rhs_vec)):
            if aug[r][col] != Fraction(0):
                piv = r; break
        if piv is None: continue
        pivots.append((ri, col))
        if piv != ri: aug[ri], aug[piv] = aug[piv], aug[ri]
        pv = aug[ri][col]
        for j in range(ncols+1): aug[ri][j] /= pv
        for r in range(len(rhs_vec)):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(ncols+1): aug[r][j] -= f * aug[ri][j]
        ri += 1
    x = [Fraction(0)] * ncols
    for r, c in pivots:
        x[c] = aug[r][ncols]
    return x

def matvec(M, v):
    return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(M))]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def check_symmetry(c0):
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c0[i]
    coeffs[leading] = Fraction(1)

    max_asym = Fraction(0)
    asym_count = 0
    for m, val in coeffs.items():
        for p in permutations(m):
            if p != m and p in coeffs:
                diff = abs(coeffs[p] - val)
                if diff > Fraction(0): asym_count += 1
                if diff > max_asym: max_asym = diff

    is_sym = (max_asym == Fraction(0))
    print(f"    Symmetry: {'EXACT' if is_sym else 'BROKEN'}, max_asym={float(max_asym):.3e}, count={asym_count}")
    return is_sym

def run_perturbation(t_val):
    t0 = time.time()
    print(f"\n  t = {t_val}:")
    A, b = build_matrices(t_val, max_order=3)
    print(f"    Matrices built ({time.time()-t0:.1f}s)")

    # Order 0: RREF of A0
    pivots0, aug0 = gauss_elim(A[0], b[0], N, N)
    rank0 = len(pivots0)
    pivot_cols0 = {c for _, c in pivots0}
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    print(f"    Order 0: rank={rank0}, null_dim={n_null}")

    # Particular solution
    c0_part = [Fraction(0)] * N
    for r, c in pivots0: c0_part[c] = aug0[r][N]

    # Right null basis
    null_vecs = []
    for fc in free_cols0:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots0: v[c] = -aug0[r][fc]
        null_vecs.append(v)

    # Left null of A0 (= null of A0^T)
    A0T = [[A[0][j][i] for j in range(N)] for i in range(N)]
    pivsT, augT = gauss_elim(A0T, [Fraction(0)]*N, N, N)
    pcT = {c for _, c in pivsT}
    left_null = []
    for fc in [c for c in range(N) if c not in pcT]:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivsT: v[c] = -augT[r][fc]
        left_null.append(v)
    n_left = len(left_null)
    print(f"    Left null dim: {n_left}")

    # =============================================
    # Iterative constraint accumulation
    # =============================================
    # We accumulate constraints on alpha (coordinates in null space)
    # c0 = c0_part + sum_k alpha_k * null_vecs[k]
    # Each order gives new linear constraints on alpha.
    # We need c_1, c_2, ... as intermediate variables but we eliminate them.

    # Order 1 constraints: L * (b1 - A1*c0) = 0
    # => L*A1*N*alpha = L*(b1 - A1*c0_part)
    print(f"    Order 1...", end=""); sys.stdout.flush()
    A1N = [[dot(left_null[l], [sum(A[1][i][j]*null_vecs[k][j] for j in range(N)) for i in range(N)]) for k in range(n_null)] for l in range(n_left)]
    A1c0p = matvec(A[1], c0_part)
    d1 = [dot(left_null[l], [b[1][i] - A1c0p[i] for i in range(N)]) for l in range(n_left)]

    # Stack constraints
    all_rows = [row[:] for row in A1N]
    all_rhs = d1[:]

    pivs, aug = gauss_elim(all_rows, all_rhs, len(all_rows), n_null)
    rank_cum = len(pivs)
    print(f" rank={rank_cum}/{n_null} ({time.time()-t0:.1f}s)")

    if rank_cum >= n_null:
        print(f"    Order 1 sufficient!")
        alpha = [Fraction(0)] * n_null
        for r, c in pivs: alpha[c] = aug[r][n_null]
        c0 = [c0_part[j] + sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
        return check_symmetry(c0)

    # For orders 2+, we need c_1(alpha) = c1_base + sum_k alpha_k * c1_null_k
    # where c1(alpha) is particular solution of A0*c1 = b1 - A1*c0(alpha)
    # c1_base = A0^+(b1 - A1*c0_part)
    # c1_null_k = A0^+(-A1*null_vecs[k])

    print(f"    Computing c1...", end=""); sys.stdout.flush()
    rhs_c1_base = [b[1][i] - A1c0p[i] for i in range(N)]
    c1_base = solve_via_rref(pivots0, aug0, rhs_c1_base, N)
    c1_nulls = []
    for k in range(n_null):
        rhs_k = [-sum(A[1][i][j]*null_vecs[k][j] for j in range(N)) for i in range(N)]
        c1_nulls.append(solve_via_rref(pivots0, aug0, rhs_k, N))
    print(f" done ({time.time()-t0:.1f}s)")

    # Order 2: L*(b2 - A1*c1 - A2*c0) = 0
    # = L*(b2 - A1*(c1_base + sum alpha_k c1_nulls[k]) - A2*(c0_part + sum alpha_k null_vecs[k]))
    # Bilinear terms: A1*c1 has c1_nulls[k]*alpha_k, and A2*c0 has null_vecs[k]*alpha_k
    # Linear in alpha if we also treat null-space freedom in c1 as beta variables
    # But we set null-space freedom in c1 to 0 (particular solution)
    # Then c1 depends linearly on alpha, and order-2 constraint is LINEAR in alpha

    print(f"    Order 2...", end=""); sys.stdout.flush()
    # Constant: L*(b2 - A1*c1_base - A2*c0_part)
    A1c1b = matvec(A[1], c1_base)
    A2c0p = matvec(A[2], c0_part)
    const2 = [dot(left_null[l], [b[2][i] - A1c1b[i] - A2c0p[i] for i in range(N)]) for l in range(n_left)]

    # Linear in alpha_k: -L*(A1*c1_nulls[k] + A2*null_vecs[k])
    lin2 = []
    for l in range(n_left):
        row = []
        for k in range(n_null):
            A1c1k = matvec(A[1], c1_nulls[k])
            A2nk = matvec(A[2], null_vecs[k])
            row.append(dot(left_null[l], [A1c1k[i] + A2nk[i] for i in range(N)]))
        lin2.append(row)

    # Add to accumulated constraints
    for l in range(n_left):
        all_rows.append(lin2[l][:])
        all_rhs.append(const2[l])

    pivs, aug = gauss_elim(all_rows, all_rhs, len(all_rows), n_null)
    rank_cum = len(pivs)
    print(f" rank={rank_cum}/{n_null} ({time.time()-t0:.1f}s)")

    if rank_cum >= n_null:
        print(f"    Order 2 sufficient!")
        alpha = [Fraction(0)] * n_null
        for r, c in pivs: alpha[c] = aug[r][n_null]
        c0 = [c0_part[j] + sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
        return check_symmetry(c0)

    # For order 3: need c2(alpha) = c2_base + sum alpha_k c2_nulls[k]
    # A0*c2 = b2 - A1*c1 - A2*c0
    print(f"    Computing c2...", end=""); sys.stdout.flush()
    rhs_c2_base = [b[2][i] - A1c1b[i] - A2c0p[i] for i in range(N)]
    c2_base = solve_via_rref(pivots0, aug0, rhs_c2_base, N)
    c2_nulls = []
    for k in range(n_null):
        A1c1k = matvec(A[1], c1_nulls[k])
        A2nk = matvec(A[2], null_vecs[k])
        rhs_k = [-A1c1k[i] - A2nk[i] for i in range(N)]
        c2_nulls.append(solve_via_rref(pivots0, aug0, rhs_k, N))
    print(f" done ({time.time()-t0:.1f}s)")

    # Order 3: L*(b3 - A1*c2 - A2*c1 - A3*c0) = 0
    print(f"    Order 3...", end=""); sys.stdout.flush()
    A1c2b = matvec(A[1], c2_base)
    A2c1b = matvec(A[2], c1_base)
    A3c0p = matvec(A[3], c0_part)
    const3 = [dot(left_null[l], [b[3][i] - A1c2b[i] - A2c1b[i] - A3c0p[i] for i in range(N)]) for l in range(n_left)]

    lin3 = []
    for l in range(n_left):
        row = []
        for k in range(n_null):
            A1c2k = matvec(A[1], c2_nulls[k])
            A2c1k = matvec(A[2], c1_nulls[k])
            A3nk = matvec(A[3], null_vecs[k])
            row.append(dot(left_null[l], [A1c2k[i] + A2c1k[i] + A3nk[i] for i in range(N)]))
        lin3.append(row)

    for l in range(n_left):
        all_rows.append(lin3[l][:])
        all_rhs.append(const3[l])

    pivs, aug = gauss_elim(all_rows, all_rhs, len(all_rows), n_null)
    rank_cum = len(pivs)
    print(f" rank={rank_cum}/{n_null} ({time.time()-t0:.1f}s)")

    if rank_cum >= n_null:
        print(f"    ** Order 3 CLOSES the gap! **")
        alpha = [Fraction(0)] * n_null
        for r, c in pivs: alpha[c] = aug[r][n_null]
        c0 = [c0_part[j] + sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
        return check_symmetry(c0)
    else:
        free = n_null - rank_cum
        print(f"    Still {free} free params. Need higher orders.")
        return None

# Run at t = 7/10
result = run_perturbation(Fraction(7, 10))
if result is None:
    print("\n  ** STOP-LOSS: Order 3 insufficient. P03 gap not closable by perturbation. **")
elif result:
    # Try second t value
    result2 = run_perturbation(Fraction(1, 3))
    if result2:
        print("\n  ** EXACT SYMMETRY at t=7/10 AND t=1/3! **")

print(f"\n{'='*70}")
print("DONE")
