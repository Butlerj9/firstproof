"""
P03 EXP-13b: Fourth-order perturbation to close remaining 4 free params.
Order 3 reached rank 45/49. Order 4 should close.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from itertools import permutations

print("P03 EXP-13b: Order 4 perturbation")
print("=" * 70)

n = 3
leading = (0, 2, 3)
comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

monoms = list(comps)
van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in monoms if m != leading]
N = len(unk_monoms)

def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i+1, len(nu)):
        if nu[j] >= nu[i]: count += 1
    return count

k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}

def falling_fact(p, k):
    r = Fraction(1)
    for i in range(k): r *= Fraction(p - i)
    return r

def binom_frac(p, k):
    if k < 0: return Fraction(0)
    if k == 0: return Fraction(1)
    fk = Fraction(1)
    for i in range(1, k+1): fk *= Fraction(i)
    return falling_fact(p, k) / fk

def build_matrices(t_val, max_order):
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

def solve_A0(A0, b_vec):
    pvs, ag = gauss_elim(A0, b_vec, len(b_vec), len(A0[0]))
    x = [Fraction(0)] * len(A0[0])
    for r, c in pvs: x[c] = ag[r][len(A0[0])]
    return x

def matvec(M, v):
    return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(M))]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def check_symmetry(c0):
    coeffs = {}
    for i, m in enumerate(unk_monoms): coeffs[m] = c0[i]
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
    if is_sym:
        seen = set()
        for m_key in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
            key = tuple(sorted(m_key, reverse=True))
            if key not in seen:
                seen.add(key)
                print(f"      m_{key} = {coeffs[m_key]}")
                if len(seen) >= 5: break
    return is_sym

def run(t_val):
    t0 = time.time()
    print(f"\n  t = {t_val}:")
    MAX_ORDER = 5  # try up to order 5 if needed
    A, b = build_matrices(t_val, max_order=MAX_ORDER)
    print(f"    Matrices built ({time.time()-t0:.1f}s)")

    # Order 0
    pivots0, aug0 = gauss_elim(A[0], b[0], N, N)
    rank0 = len(pivots0)
    pivot_cols0 = {c for _, c in pivots0}
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    print(f"    Order 0: rank={rank0}, null_dim={n_null}")

    c0_part = [Fraction(0)] * N
    for r, c in pivots0: c0_part[c] = aug0[r][N]

    null_vecs = []
    for fc in free_cols0:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots0: v[c] = -aug0[r][fc]
        null_vecs.append(v)

    A0T = [[A[0][j][i] for j in range(N)] for i in range(N)]
    pivsT, augT = gauss_elim(A0T, [Fraction(0)]*N, N, N)
    pcT = {c for _, c in pivsT}
    left_null = []
    for fc in [c for c in range(N) if c not in pcT]:
        v = [Fraction(0)] * N; v[fc] = Fraction(1)
        for r, c in pivsT: v[c] = -augT[r][fc]
        left_null.append(v)
    n_left = len(left_null)

    # Iteratively compute c_k and add constraints
    # c_k_base, c_k_nulls[j] such that c_k = c_k_base + sum alpha_j * c_k_nulls[j]
    ck_bases = {0: c0_part}
    ck_nullss = {0: null_vecs}

    all_rows = []
    all_rhs_vals = []

    for order in range(1, MAX_ORDER+1):
        print(f"    Order {order}...", end=""); sys.stdout.flush()

        # Constraint: L*(b_order - sum_{m=1}^{order} A_m * c_{order-m}) = 0
        # = L*b_order - sum_{m=1}^{order} L*A_m*(c_{order-m}_base + sum alpha c_{order-m}_nulls)
        # Constant part: L*(b_order - sum A_m * c_{order-m}_base)
        # Linear part: -sum_m sum_k L*A_m*c_{order-m}_nulls[k] * alpha_k

        const = [Fraction(0)] * n_left
        lin = [[Fraction(0)] * n_null for _ in range(n_left)]

        for l in range(n_left):
            val = dot(left_null[l], b[order])
            const[l] = val

        for m in range(1, order+1):
            om = order - m
            if om not in ck_bases: continue
            Am_ckb = matvec(A[m], ck_bases[om])
            for l in range(n_left):
                const[l] -= dot(left_null[l], Am_ckb)

            for k in range(n_null):
                Am_ckn = matvec(A[m], ck_nullss[om][k])
                for l in range(n_left):
                    lin[l][k] += dot(left_null[l], Am_ckn)

        for l in range(n_left):
            all_rows.append(lin[l][:])
            all_rhs_vals.append(const[l])

        pivs, aug_acc = gauss_elim(all_rows, all_rhs_vals, len(all_rows), n_null)
        rank_cum = len(pivs)
        elapsed = time.time()-t0
        print(f" rank={rank_cum}/{n_null} ({elapsed:.1f}s)")

        if rank_cum >= n_null:
            print(f"    ** Order {order} CLOSES! **")
            alpha = [Fraction(0)] * n_null
            for r, c in pivs: alpha[c] = aug_acc[r][n_null]
            c0 = [c0_part[j] + sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
            return check_symmetry(c0)

        # Compute c_{order} for next iteration
        # A0*c_order = b_order - sum_{m=1}^{order} A_m * c_{order-m}
        print(f"    Computing c{order}...", end=""); sys.stdout.flush()
        rhs_base = [b[order][i] for i in range(N)]
        for m in range(1, order+1):
            om = order - m
            if om in ck_bases:
                Am_ckb = matvec(A[m], ck_bases[om])
                for i in range(N): rhs_base[i] -= Am_ckb[i]
        ck_bases[order] = solve_A0(A[0], rhs_base)

        ck_nullss[order] = []
        for k in range(n_null):
            rhs_k = [Fraction(0)] * N
            for m in range(1, order+1):
                om = order - m
                if om in ck_nullss:
                    Am_ckn = matvec(A[m], ck_nullss[om][k])
                    for i in range(N): rhs_k[i] -= Am_ckn[i]
            ck_nullss[order].append(solve_A0(A[0], rhs_k))
        print(f" done ({time.time()-t0:.1f}s)")

    print(f"    ** Did not close through order {MAX_ORDER} **")
    return None

result = run(Fraction(7, 10))
if result is True:
    print("\n  Trying second t value...")
    result2 = run(Fraction(1, 3))
    if result2 is True:
        print("\n  ** EXACT SYMMETRY PROVED at t=7/10 AND t=1/3 (Fraction arithmetic) **")
elif result is None:
    print("\n  ** STOP-LOSS HIT **")

print(f"\n{'='*70}")
print("DONE")
