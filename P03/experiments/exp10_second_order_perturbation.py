"""
P03 EXP-10: Second-order perturbation theory.

Theory: Order 1 gives rank 17 on 49-dim null space.
Order 2 gives 32 additional constraints (after eliminating c1 unknowns).
Together: 49 constraints -> unique c0. Then check symmetry.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P03 EXP-10: Second-order perturbation for n=3")
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
N = len(unk_monoms)  # 55

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
    """Binomial coefficient C(n,k) for non-negative integers."""
    if k_val < 0 or k_val > n_val:
        return 0
    if k_val == 0:
        return 1
    result = 1
    for i in range(k_val):
        result = result * (n_val - i) // (i + 1)
    return result

def run_analysis(t_val):
    t0 = time.time()

    # Build A0, A1, A2 and b0, b1, b2
    # A_k[nu,alpha] = t^{-k_stat.alpha} * binom(p(nu,alpha), k)
    # where p(nu,alpha) = sum(nu_i * alpha_i)
    # b_k[nu] = -t^{-k_stat.leading} * binom(p(nu,leading), k)

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
        A0.append(row0)
        A1.append(row1)
        A2.append(row2)

        t_exp_l = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2])
        p_l = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2]
        tp_l = t_val ** t_exp_l
        b0.append(-tp_l)
        b1.append(-Fraction(p_l) * tp_l)
        b2.append(-Fraction(binom(p_l, 2)) * tp_l)

    print(f"    Matrices built ({time.time()-t0:.1f}s)")

    # Step 1: RREF of A0, find null space and particular solution
    aug = [A0[i][:] + [b0[i]] for i in range(N)]

    pivots = []
    ri = 0
    for col in range(N):
        piv = None
        for r in range(ri, N):
            if aug[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: continue
        pivots.append((ri, col))
        if piv != ri:
            aug[ri], aug[piv] = aug[piv], aug[ri]
        pv = aug[ri][col]
        for j in range(N+1):
            aug[ri][j] /= pv
        for r in range(N):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(N+1):
                    aug[r][j] -= f * aug[ri][j]
        ri += 1

    rank0 = len(pivots)
    pivot_cols = {c for _, c in pivots}
    free_cols = [c for c in range(N) if c not in pivot_cols]
    n_null = len(free_cols)

    # Particular solution c0_part
    c0_part = [Fraction(0)] * N
    for r, c in pivots:
        c0_part[c] = aug[r][N]

    # Right null space basis
    null_vecs = []
    for fc in free_cols:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots:
            v[c] = -aug[r][fc]
        null_vecs.append(v)

    print(f"    A0 rank: {rank0}, null dim: {n_null}")

    # Left null space of A0 (null space of A0^T)
    A0T = [[A0[j][i] for j in range(N)] for i in range(N)]
    matT = [row[:] for row in A0T]
    pivsT = []
    ri = 0
    for col in range(N):
        piv = None
        for r in range(ri, N):
            if matT[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: continue
        pivsT.append((ri, col))
        if piv != ri:
            matT[ri], matT[piv] = matT[piv], matT[ri]
        pv = matT[ri][col]
        for j in range(N):
            matT[ri][j] /= pv
        for r in range(N):
            if r != ri and matT[r][col] != Fraction(0):
                f = matT[r][col]
                for j in range(N):
                    matT[r][j] -= f * matT[ri][j]
        ri += 1

    pcT = {c for _, c in pivsT}
    fcT = [c for c in range(N) if c not in pcT]
    left_null = []
    for fc in fcT:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivsT:
            v[c] = -matT[r][fc]
        left_null.append(v)

    n_left = len(left_null)
    print(f"    Left null dim: {n_left}")

    # Step 2: First-order constraint
    # L * A1 * N * alpha = L * (b1 - A1 * c0_part)
    # Compute A1 * null_vecs[k] for each k
    print(f"    Computing first-order constraint...", end="")
    sys.stdout.flush()

    # Compute A1 * c0_part
    A1_c0p = [sum(A1[i][j]*c0_part[j] for j in range(N)) for i in range(N)]

    # Compute A1 * null_vecs
    A1_N = []  # list of N-vectors, one per null vec
    for nv in null_vecs:
        col = [sum(A1[i][j]*nv[j] for j in range(N)) for i in range(N)]
        A1_N.append(col)

    # Project: C1[l][k] = left_null[l] . A1_N[k]
    # d1[l] = left_null[l] . (b1 - A1_c0p)
    C1 = []
    d1 = []
    for lv in left_null:
        row = [sum(lv[i]*A1_N[k][i] for i in range(N)) for k in range(n_null)]
        C1.append(row)
        rhs = sum(lv[i]*(b1[i]-A1_c0p[i]) for i in range(N))
        d1.append(rhs)

    print(f" done ({time.time()-t0:.1f}s)")

    # Solve C1 * alpha = d1 partially (get rank, identify free/pivot variables)
    aug1 = [C1[i][:] + [d1[i]] for i in range(n_left)]
    pivs1 = []
    ri = 0
    for col in range(n_null):
        piv = None
        for r in range(ri, n_left):
            if aug1[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: continue
        pivs1.append((ri, col))
        if piv != ri:
            aug1[ri], aug1[piv] = aug1[piv], aug1[ri]
        pv = aug1[ri][col]
        for j in range(n_null+1):
            aug1[ri][j] /= pv
        for r in range(n_left):
            if r != ri and aug1[r][col] != Fraction(0):
                f = aug1[r][col]
                for j in range(n_null+1):
                    aug1[r][j] -= f * aug1[ri][j]
        ri += 1

    rank1 = len(pivs1)
    pc1 = {c for _, c in pivs1}
    fc1 = [c for c in range(n_null) if c not in pc1]
    n_free1 = len(fc1)
    print(f"    First-order rank: {rank1}/{n_null}, free: {n_free1}")

    if n_free1 == 0:
        print(f"    First-order already determines c0!")
        # Extract alpha
        alpha = [Fraction(0)] * n_null
        for r, c in pivs1:
            alpha[c] = aug1[r][n_null]
        c0 = [c0_part[j] + sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
        return check_sym(c0)

    # Step 3: Second-order constraint
    # From order 1: A0 c1 = b1 - A1 c0
    # For each free alpha direction, compute c1_part
    # c0(alpha) = c0_part + sum alpha_k * null_vecs[k]
    # c0 depends on n_free1 free alpha's (indexed by fc1)

    # Express alpha in terms of free variables:
    # alpha[pivot_col] = aug1[pivot_row][n_null] - sum_{free_col} aug1[pivot_row][free_col] * alpha_free[j]
    # alpha[free_col] = alpha_free[j]

    # For each free direction j (alpha_free[j] = 1, others = 0):
    # Compute c0_free_j = sum_k alpha_k(e_j) * null_vecs[k]

    print(f"    Computing second-order constraint...", end="")
    sys.stdout.flush()

    # For each free variable j, compute the corresponding c0 direction
    c0_dirs = []  # n_free1 directions in R^N
    for fj_idx, fj in enumerate(fc1):
        alpha = [Fraction(0)] * n_null
        alpha[fj] = Fraction(1)
        # Adjust pivot variables
        for r, c in pivs1:
            alpha[c] = -aug1[r][fj]  # contribution from this free variable
        # c0_dir = sum alpha_k * null_vecs[k]
        c0_dir = [sum(alpha[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]
        c0_dirs.append(c0_dir)

    # Base c0 (from particular + pivot parts of first-order):
    alpha_base = [Fraction(0)] * n_null
    for r, c in pivs1:
        alpha_base[c] = aug1[r][n_null]
    c0_base = [c0_part[j] + sum(alpha_base[k]*null_vecs[k][j] for k in range(n_null)) for j in range(N)]

    # c0 = c0_base + sum gamma_j * c0_dirs[j]  (gamma_j are the n_free1 free variables)

    # For c1: A0 c1 = b1 - A1 c0
    # Particular solution: c1_part = A0^+ (b1 - A1 c0)
    # We need c1_part_base and c1_part_dirs[j]

    # Compute b1 - A1 * c0_base
    rhs_base = [b1[i] - sum(A1[i][j]*c0_base[j] for j in range(N)) for i in range(N)]

    # Compute -A1 * c0_dirs[j]
    rhs_dirs = []
    for c0d in c0_dirs:
        rhs_d = [-sum(A1[i][j]*c0d[j] for j in range(N)) for i in range(N)]
        rhs_dirs.append(rhs_d)

    # Solve A0 x = rhs using the pre-computed RREF of A0
    # From the RREF in 'aug' (step 1), pivot rows give: x[pivot_col] = rhs_col - sum of free cols
    # Set free variables to 0

    def solve_A0(rhs_vec):
        """Solve A0 x = rhs_vec using RREF. Returns particular solution (free vars = 0)."""
        # First transform rhs through same row operations as A0's RREF
        # We need to re-do the elimination on the augmented [A0 | rhs] system
        # But we already have A0 in RREF. We can use back-substitution.
        # Actually, the RREF is stored in 'aug' (with the b0 column at position N).
        # We need a fresh elimination for a new RHS.

        # Simpler: use the RREF of A0 (without b0 column) to solve
        # We need the RREF row operations applied to rhs_vec.
        # Since we didn't store the row operations, let me re-solve from scratch.

        # Create augmented system [A0 | rhs_vec]
        a = [A0[i][:] + [rhs_vec[i]] for i in range(N)]
        pvs = []
        ri = 0
        for col in range(N):
            piv = None
            for r in range(ri, N):
                if a[r][col] != Fraction(0):
                    piv = r
                    break
            if piv is None: continue
            pvs.append((ri, col))
            if piv != ri:
                a[ri], a[piv] = a[piv], a[ri]
            pv = a[ri][col]
            for j in range(N+1):
                a[ri][j] /= pv
            for r in range(N):
                if r != ri and a[r][col] != Fraction(0):
                    f = a[r][col]
                    for j in range(N+1):
                        a[r][j] -= f * a[ri][j]
            ri += 1

        x = [Fraction(0)] * N
        for r, c in pvs:
            x[c] = a[r][N]
        return x

    c1_base = solve_A0(rhs_base)
    c1_dirs = [solve_A0(rd) for rd in rhs_dirs]

    print(f" c1 computed ({time.time()-t0:.1f}s)")

    # c1 = c1_base + sum gamma_j * c1_dirs[j] + sum beta_k * null_vecs[k]
    # Second-order constraint: L(b2 - A1 c1 - A2 c0) = 0  [wait, check sign]
    # Order 2: A0 c2 + A1 c1 + A2 c0 = b2
    # Consistency: L(b2 - A1 c1 - A2 c0) = 0

    # Compute A2*c0_base, A2*c0_dirs[j]
    A2_c0b = [sum(A2[i][j]*c0_base[j] for j in range(N)) for i in range(N)]
    A2_c0d = [[sum(A2[i][j]*c0_dirs[d][j] for j in range(N)) for i in range(N)] for d in range(n_free1)]

    # Compute A1*c1_base, A1*c1_dirs[j]
    A1_c1b = [sum(A1[i][j]*c1_base[j] for j in range(N)) for i in range(N)]
    A1_c1d = [[sum(A1[i][j]*c1_dirs[d][j] for j in range(N)) for i in range(N)] for d in range(n_free1)]

    # Residual for second order (constant part):
    # r2_base = L * (b2 - A1*c1_base - A2*c0_base)
    # r2_dirs[j] = L * (-A1*c1_dirs[j] - A2*c0_dirs[j])

    # Also beta contribution: L * A1 * null_vecs[k] = A1_N projected through L
    # This is the same as C1 from step 2.

    # Second-order constraint:
    # For each left null vector l:
    # l.(b2 - A1*(c1_base + sum gamma c1_dirs + sum beta null) - A2*(c0_base + sum gamma c0_dirs)) = 0
    # l.(b2-A1*c1_base-A2*c0_base) - sum_j gamma_j l.(A1*c1_dirs[j]+A2*c0_dirs[j]) - sum_k beta_k l.A1.null[k] = 0

    # Matrix form: [D2 | C1] [gamma; beta] = r2_base
    # where D2[l][j] = l.(A1*c1_dirs[j] + A2*c0_dirs[j])
    # C1[l][k] already computed

    print(f"    Building second-order system...", end="")
    sys.stdout.flush()

    r2_const = []  # n_left values
    D2 = []  # n_left x n_free1
    for l_idx, lv in enumerate(left_null):
        r2_val = sum(lv[i]*(b2[i]-A1_c1b[i]-A2_c0b[i]) for i in range(N))
        r2_const.append(r2_val)

        d2_row = []
        for d in range(n_free1):
            val = sum(lv[i]*(A1_c1d[d][i]+A2_c0d[d][i]) for i in range(N))
            d2_row.append(val)
        D2.append(d2_row)

    print(f" done ({time.time()-t0:.1f}s)")

    # Full second-order system: [D2 | C1] [gamma; beta] = r2_const
    # Size: n_left x (n_free1 + n_null) = 49 x (32 + 49) = 49 x 81
    n_vars2 = n_free1 + n_null
    aug2 = []
    for l_idx in range(n_left):
        row = D2[l_idx] + C1[l_idx] + [r2_const[l_idx]]
        aug2.append(row)

    print(f"    Second-order system: {n_left} x {n_vars2}")

    # Gaussian elimination
    pivs2 = []
    ri = 0
    for col in range(n_vars2):
        piv = None
        for r in range(ri, n_left):
            if aug2[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: continue
        pivs2.append((ri, col))
        if piv != ri:
            aug2[ri], aug2[piv] = aug2[piv], aug2[ri]
        pv = aug2[ri][col]
        for j in range(n_vars2+1):
            aug2[ri][j] /= pv
        for r in range(n_left):
            if r != ri and aug2[r][col] != Fraction(0):
                f = aug2[r][col]
                for j in range(n_vars2+1):
                    aug2[r][j] -= f * aug2[ri][j]
        ri += 1

    rank2 = len(pivs2)
    # Count how many gamma variables are determined
    gamma_pivots = [(r,c) for r,c in pivs2 if c < n_free1]
    beta_pivots = [(r,c-n_free1) for r,c in pivs2 if c >= n_free1]
    n_gamma_det = len(gamma_pivots)
    n_beta_det = len(beta_pivots)

    print(f"    Second-order rank: {rank2}/{n_left}")
    print(f"    Gamma determined: {n_gamma_det}/{n_free1}")
    print(f"    Beta determined: {n_beta_det}/{n_null}")

    # Check consistency
    consistent = True
    for r in range(rank2, n_left):
        if aug2[r][n_vars2] != Fraction(0):
            consistent = False
            break
    print(f"    Consistent: {consistent}")

    if not consistent:
        print(f"    *** INCONSISTENT — possible error ***")
        return None

    if n_gamma_det < n_free1:
        free_gamma = n_free1 - n_gamma_det
        print(f"    *** Still {free_gamma} free gamma variables ***")
        print(f"    Need third-order perturbation")
        return None

    # Extract gamma values
    gamma = [Fraction(0)] * n_free1
    # First get gamma from pivots (they may depend on free betas)
    # Since some betas may be free, gamma values may depend on them.
    # Check if any gamma pivot row has nonzero entries in free beta columns
    pc2 = {c for _, c in pivs2}
    fc2 = [c for c in range(n_vars2) if c not in pc2]
    free_beta_cols = [c for c in fc2 if c >= n_free1]

    has_free_beta_dep = False
    for r, c in gamma_pivots:
        for fbc in free_beta_cols:
            if aug2[r][fbc] != Fraction(0):
                has_free_beta_dep = True
                break

    if has_free_beta_dep:
        print(f"    Gamma depends on free betas — setting free betas to 0")

    for r, c in pivs2:
        if c < n_free1:
            gamma[c] = aug2[r][n_vars2]
            # Subtract free beta contributions (set to 0)

    # Reconstruct c0
    c0 = [c0_base[j] + sum(gamma[d]*c0_dirs[d][j] for d in range(n_free1)) for j in range(N)]

    elapsed = time.time() - t0
    print(f"    Total time: {elapsed:.1f}s")

    # Check symmetry
    return check_sym(c0)

def check_sym(c0):
    from itertools import permutations as perms
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c0[i]
    coeffs[leading] = Fraction(1)

    max_asym = Fraction(0)
    asym_count = 0
    for m, val in coeffs.items():
        for p in perms(m):
            if p != m and p in coeffs:
                diff = abs(coeffs[p] - val)
                if diff > Fraction(0):
                    asym_count += 1
                if diff > max_asym:
                    max_asym = diff

    is_sym = (max_asym == Fraction(0))
    print(f"    Symmetry: {'EXACT' if is_sym else 'BROKEN'}")
    print(f"    Max asymmetry: {float(max_asym):.6e}, count: {asym_count}")

    if is_sym:
        print(f"    *** EXACT SYMMETRY PROVED (at this t value) ***")
        # Print some coefficients
        seen = set()
        for m_key in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
            key = tuple(sorted(m_key, reverse=True))
            if key not in seen:
                seen.add(key)
                print(f"      m_{key} = {coeffs[m_key]}")
                if len(seen) >= 6:
                    break

    return is_sym

# Run
for t_val in [Fraction(7, 10), Fraction(1, 3)]:
    print(f"\n  t = {t_val}:")
    result = run_analysis(t_val)
    sys.stdout.flush()

print(f"\n{'='*70}")
print("DONE")
