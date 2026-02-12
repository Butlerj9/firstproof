"""
P03 EXP-10b: Check if partial c0 (from orders 1+2, free gammas = 0) is symmetric.

Hypothesis: The 14 free directions span the symmetric subspace. If so, the
non-symmetric part of c0 is fully determined by orders 1+2 and equals 0,
proving symmetry.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from itertools import permutations as perms

print("P03 EXP-10b: Symmetry of partial solution + free direction analysis")
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

k_stats = {}
for nu in comps:
    k_stats[nu] = tuple(k_stat(nu, i) for i in range(n))

def binom(n_val, k_val):
    if k_val < 0 or k_val > n_val: return 0
    if k_val == 0: return 1
    result = 1
    for i in range(k_val):
        result = result * (n_val - i) // (i + 1)
    return result

def to_partition(m):
    return tuple(sorted(m, reverse=True))

def is_symmetric_vec(c):
    """Check if coefficient vector gives symmetric polynomial."""
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c[i]
    coeffs[leading] = Fraction(1)

    for m, val in coeffs.items():
        for p in perms(m):
            if p in coeffs and coeffs[p] != val:
                return False
    return True

def symmetry_deviation(c):
    """Max absolute difference between permuted coefficients."""
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c[i]
    coeffs[leading] = Fraction(1)

    max_dev = Fraction(0)
    for m, val in coeffs.items():
        for p in perms(m):
            if p in coeffs:
                d = abs(coeffs[p] - val)
                if d > max_dev: max_dev = d
    return max_dev

def run(t_val):
    t0 = time.time()
    # Build A0, A1, A2
    A0, A1, A2 = [], [], []
    b0, b1, b2 = [], [], []

    for nu in van_comps:
        k = k_stats[nu]
        row0, row1, row2 = [], [], []
        for m in unk_monoms:
            t_exp = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2])
            p = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2]
            tp = t_val ** t_exp
            row0.append(tp)
            row1.append(Fraction(p) * tp)
            row2.append(Fraction(binom(p, 2)) * tp)
        A0.append(row0); A1.append(row1); A2.append(row2)
        t_exp_l = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2])
        p_l = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2]
        tp_l = t_val ** t_exp_l
        b0.append(-tp_l); b1.append(-Fraction(p_l)*tp_l); b2.append(-Fraction(binom(p_l,2))*tp_l)

    # A0 RREF
    aug = [A0[i][:] + [b0[i]] for i in range(N)]
    pivots = []
    ri = 0
    for col in range(N):
        piv = None
        for r in range(ri, N):
            if aug[r][col] != Fraction(0):
                piv = r; break
        if piv is None: continue
        pivots.append((ri, col))
        if piv != ri: aug[ri], aug[piv] = aug[piv], aug[ri]
        pv = aug[ri][col]
        for j in range(N+1): aug[ri][j] /= pv
        for r in range(N):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(N+1): aug[r][j] -= f * aug[ri][j]
        ri += 1

    pc = {c for _, c in pivots}
    fc = [c for c in range(N) if c not in pc]
    n_null = len(fc)
    c0_part = [Fraction(0)] * N
    for r, c in pivots: c0_part[c] = aug[r][N]
    null_vecs = []
    for fci in fc:
        v = [Fraction(0)] * N; v[fci] = Fraction(1)
        for r, c in pivots: v[c] = -aug[r][fci]
        null_vecs.append(v)

    # Left null space
    A0T = [[A0[j][i] for j in range(N)] for i in range(N)]
    matT = [row[:] for row in A0T]
    pivsT = []; ri = 0
    for col in range(N):
        piv = None
        for r in range(ri, N):
            if matT[r][col] != Fraction(0): piv = r; break
        if piv is None: continue
        pivsT.append((ri, col))
        if piv != ri: matT[ri], matT[piv] = matT[piv], matT[ri]
        pv = matT[ri][col]
        for j in range(N): matT[ri][j] /= pv
        for r in range(N):
            if r != ri and matT[r][col] != Fraction(0):
                f = matT[r][col]
                for j in range(N): matT[r][j] -= f * matT[ri][j]
        ri += 1
    pcT = {c for _, c in pivsT}
    fcT = [c for c in range(N) if c not in pcT]
    left_null = []
    for fci in fcT:
        v = [Fraction(0)] * N; v[fci] = Fraction(1)
        for r, c in pivsT: v[c] = -matT[r][fci]
        left_null.append(v)
    n_left = len(left_null)

    # First-order: L*A1*N*alpha = L*(b1-A1*c0_part)
    A1_c0p = [sum(A1[i][j]*c0_part[j] for j in range(N)) for i in range(N)]
    A1_N = [[sum(A1[i][j]*null_vecs[k][j] for j in range(N)) for i in range(N)] for k in range(n_null)]
    C1 = [[sum(left_null[l][i]*A1_N[k][i] for i in range(N)) for k in range(n_null)] for l in range(n_left)]
    d1 = [sum(left_null[l][i]*(b1[i]-A1_c0p[i]) for i in range(N)) for l in range(n_left)]

    aug1 = [C1[i][:]+[d1[i]] for i in range(n_left)]
    pivs1 = []; ri = 0
    for col in range(n_null):
        piv = None
        for r in range(ri, n_left):
            if aug1[r][col] != Fraction(0): piv = r; break
        if piv is None: continue
        pivs1.append((ri, col))
        if piv != ri: aug1[ri], aug1[piv] = aug1[piv], aug1[ri]
        pv = aug1[ri][col]
        for j in range(n_null+1): aug1[ri][j] /= pv
        for r in range(n_left):
            if r != ri and aug1[r][col] != Fraction(0):
                f = aug1[r][col]
                for j in range(n_null+1): aug1[r][j] -= f * aug1[ri][j]
        ri += 1

    rank1 = len(pivs1)
    pc1 = {c for _, c in pivs1}
    fc1 = [c for c in range(n_null) if c not in pc1]
    n_free1 = len(fc1)

    # Base alpha (from first-order, free alphas = 0)
    alpha_base = [Fraction(0)] * n_null
    for r, c in pivs1: alpha_base[c] = aug1[r][n_null]

    # c0 directions for free variables
    c0_dirs = []
    for fj in fc1:
        alpha = [Fraction(0)] * n_null; alpha[fj] = Fraction(1)
        for r, c in pivs1: alpha[c] = -aug1[r][fj]
        c0_dir = [sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
        c0_dirs.append(c0_dir)

    c0_base = [c0_part[j] + sum(alpha_base[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]

    # Second-order: compute c1 parts
    def solve_A0(rhs_vec):
        a = [A0[i][:]+[rhs_vec[i]] for i in range(N)]
        pvs = []; ri = 0
        for col in range(N):
            piv = None
            for r in range(ri, N):
                if a[r][col] != Fraction(0): piv = r; break
            if piv is None: continue
            pvs.append((ri, col))
            if piv != ri: a[ri], a[piv] = a[piv], a[ri]
            pv = a[ri][col]
            for j in range(N+1): a[ri][j] /= pv
            for r in range(N):
                if r != ri and a[r][col] != Fraction(0):
                    f = a[r][col]
                    for j in range(N+1): a[r][j] -= f * a[ri][j]
            ri += 1
        x = [Fraction(0)] * N
        for r, c in pvs: x[c] = a[r][N]
        return x

    rhs_base = [b1[i]-sum(A1[i][j]*c0_base[j] for j in range(N)) for i in range(N)]
    rhs_dirs = [[-sum(A1[i][j]*c0_dirs[d][j] for j in range(N)) for i in range(N)] for d in range(n_free1)]

    c1_base = solve_A0(rhs_base)
    c1_dirs = [solve_A0(rd) for rd in rhs_dirs]

    # Second-order system
    A2_c0b = [sum(A2[i][j]*c0_base[j] for j in range(N)) for i in range(N)]
    A2_c0d = [[sum(A2[i][j]*c0_dirs[d][j] for j in range(N)) for i in range(N)] for d in range(n_free1)]
    A1_c1b = [sum(A1[i][j]*c1_base[j] for j in range(N)) for i in range(N)]
    A1_c1d = [[sum(A1[i][j]*c1_dirs[d][j] for j in range(N)) for i in range(N)] for d in range(n_free1)]

    n_vars2 = n_free1 + n_null
    aug2 = []
    for l_idx, lv in enumerate(left_null):
        r2_val = sum(lv[i]*(b2[i]-A1_c1b[i]-A2_c0b[i]) for i in range(N))
        row = [sum(lv[i]*(A1_c1d[d][i]+A2_c0d[d][i]) for i in range(N)) for d in range(n_free1)]
        row += C1[l_idx]
        row.append(r2_val)
        aug2.append(row)

    pivs2 = []; ri = 0
    for col in range(n_vars2):
        piv = None
        for r in range(ri, n_left):
            if aug2[r][col] != Fraction(0): piv = r; break
        if piv is None: continue
        pivs2.append((ri, col))
        if piv != ri: aug2[ri], aug2[piv] = aug2[piv], aug2[ri]
        pv = aug2[ri][col]
        for j in range(n_vars2+1): aug2[ri][j] /= pv
        for r in range(n_left):
            if r != ri and aug2[r][col] != Fraction(0):
                f = aug2[r][col]
                for j in range(n_vars2+1): aug2[r][j] -= f * aug2[ri][j]
        ri += 1

    rank2 = len(pivs2)
    gamma_pivs = [(r,c) for r,c in pivs2 if c < n_free1]
    n_gamma_det = len(gamma_pivs)
    n_free_gamma = n_free1 - n_gamma_det

    print(f"    Rank 1+2: {rank1}+{rank2-rank1}={rank2}, free gamma: {n_free_gamma}")

    # Extract gamma (setting remaining free vars to 0)
    gamma = [Fraction(0)] * n_free1
    for r, c in pivs2:
        if c < n_free1:
            gamma[c] = aug2[r][n_vars2]

    # Reconstruct c0
    c0 = [c0_base[j] + sum(gamma[d]*c0_dirs[d][j] for d in range(n_free1)) for j in range(N)]

    # ======= KEY TEST =======
    print(f"\n    --- KEY SYMMETRY TEST ---")
    dev = symmetry_deviation(c0)
    is_sym = is_symmetric_vec(c0)
    print(f"    c0 (free gammas=0) symmetric: {is_sym}")
    print(f"    Max deviation: {float(dev):.6e}")

    # Check if free directions are symmetric
    print(f"\n    --- FREE DIRECTION ANALYSIS ---")
    for d_idx in range(min(n_free_gamma, 5)):
        # Find which gamma index is free
        det_gamma_cols = {c for _, c in gamma_pivs}
        free_gamma_cols = [c for c in range(n_free1) if c not in det_gamma_cols]
        if d_idx >= len(free_gamma_cols): break
        fgc = free_gamma_cols[d_idx]
        dir_vec = c0_dirs[fgc]
        is_dir_sym = is_symmetric_vec([dir_vec[j] for j in range(N)])
        dev_dir = symmetry_deviation(dir_vec)
        print(f"    Free direction {d_idx}: symmetric={is_dir_sym}, dev={float(dev_dir):.6e}")

    elapsed = time.time() - t0
    print(f"\n    Time: {elapsed:.1f}s")
    return is_sym

for t_val in [Fraction(7, 10), Fraction(1, 3), Fraction(3, 4)]:
    print(f"\n  t = {t_val}:")
    result = run(t_val)
    if result:
        print(f"  ==> SYMMETRY CONFIRMED at t={t_val}")
    else:
        print(f"  ==> Symmetry NOT confirmed at t={t_val}")
    sys.stdout.flush()

print(f"\n{'='*70}")
print("DONE")
