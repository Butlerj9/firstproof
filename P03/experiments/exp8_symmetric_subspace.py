"""
P03 EXP-8: Symmetric subspace approach for Symmetry Conjecture.

Key idea: Instead of solving in the full 49-dim null space, parameterize
c0 as a SYMMETRIC polynomial and check if first-order perturbation
constraints are consistent. If the unique symmetric solution also
satisfies ALL (non-symmetric) first-order constraints, symmetry is
algebraically forced by first-order perturbation theory.

Steps:
1. Build symmetric parameterization (15 free variables)
2. Impose vanishing condition g0(k0) = 0  (1 equation)
3. Impose first-order perturbation in symmetric subspace
4. Check if solution satisfies FULL first-order constraints
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from itertools import permutations

print("P03 EXP-8: Symmetric subspace test for n=3 symmetry")
print("=" * 70)

# Setup
n = 3
leading = (0, 2, 3)

# All compositions of weight <= 5 into 3 parts
comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

monoms = list(comps)
leading_idx = monoms.index(leading)
van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in monoms if m != leading]
N = len(unk_monoms)  # 55

def k_stat(nu, i):
    n = len(nu)
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i+1, n):
        if nu[j] >= nu[i]: count += 1
    return count

# Partitions of weight <= 5 with <= 3 parts
partitions = []
for a in range(6):
    for b in range(a+1):
        for c in range(b+1):
            if a + b + c <= 5:
                partitions.append((a, b, c))
partitions.sort(key=lambda p: (sum(p), p), reverse=True)
print(f"  Partitions: {len(partitions)}")

# Map each monomial to its partition (sorted tuple, descending)
def to_partition(m):
    return tuple(sorted(m, reverse=True))

# Build symmetry map M: maps 16 partition coefficients to 56 monomial coefficients
# For the unknown monomials (excluding leading), we need the map from
# partition coefficients to the 55 unknown monomial coefficients.

# First, identify which partition each unknown monomial belongs to
unk_partition_idx = []
for m in unk_monoms:
    p = to_partition(m)
    unk_partition_idx.append(partitions.index(p))

# The leading monomial (0,2,3) -> partition (3,2,0)
leading_part = to_partition(leading)
leading_part_idx = partitions.index(leading_part)
print(f"  Leading partition: {leading_part} (index {leading_part_idx})")

# In the symmetric parameterization:
# coefficient of partition (3,2,0) = 1 (fixed)
# coefficient of other partitions = free variables a_j
# For unknown monomials: c[i] = a[partition_of(monom[i])]
# where a[leading_part_idx] = 1 (fixed)

# Free partition indices (all except leading_part_idx)
free_parts = [i for i in range(len(partitions)) if i != leading_part_idx]
n_free = len(free_parts)  # 15
print(f"  Free symmetric variables: {n_free}")

# Build M matrix: N x n_free, where M[i][j] = 1 if unk_monoms[i] belongs to free_parts[j]
# and c_fixed: N x 1, where c_fixed[i] = 1 if unk_monoms[i] belongs to leading_part
M_mat = [[Fraction(0)] * n_free for _ in range(N)]
c_fixed = [Fraction(0)] * N

for i in range(N):
    pidx = unk_partition_idx[i]
    if pidx == leading_part_idx:
        c_fixed[i] = Fraction(1)
    else:
        j = free_parts.index(pidx)
        M_mat[i][j] = Fraction(1)

def run_test(t_val):
    t0 = time.time()

    # Compute k-statistics
    k_stats = {}
    for nu in comps:
        k_stats[nu] = tuple(k_stat(nu, i) for i in range(n))

    # Build A0 and A1
    A0 = []
    A1 = []
    b0 = []
    b1 = []

    for nu in van_comps:
        k = k_stats[nu]
        row0, row1 = [], []
        for m in unk_monoms:
            t_exp = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2])
            q_exp = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2]
            tp = t_val ** t_exp
            row0.append(tp)
            row1.append(Fraction(q_exp) * tp)
        A0.append(row0)
        A1.append(row1)

        m_lead = leading
        t_exp_l = -(k[0]*m_lead[0] + k[1]*m_lead[1] + k[2]*m_lead[2])
        q_exp_l = nu[0]*m_lead[0] + nu[1]*m_lead[1] + nu[2]*m_lead[2]
        tp_l = t_val ** t_exp_l
        b0.append(-tp_l)
        b1.append(-Fraction(q_exp_l) * tp_l)

    # Step 1: Left null space of A0
    # Row reduce A0^T to find null space
    A0T = [[A0[j][i] for j in range(N)] for i in range(N)]
    mat = [row[:] for row in A0T]

    pivots = []
    row_idx = 0
    for col in range(N):
        piv = None
        for r in range(row_idx, N):
            if mat[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: continue
        pivots.append((row_idx, col))
        if piv != row_idx:
            mat[row_idx], mat[piv] = mat[piv], mat[row_idx]
        pv = mat[row_idx][col]
        for j in range(N):
            mat[row_idx][j] /= pv
        for r in range(N):
            if r != row_idx and mat[r][col] != Fraction(0):
                f = mat[r][col]
                for j in range(N):
                    mat[r][j] -= f * mat[row_idx][j]
        row_idx += 1

    pivot_cols = {c for _, c in pivots}
    free_cols = [c for c in range(N) if c not in pivot_cols]

    null_basis = []
    for fc in free_cols:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots:
            v[c] = -mat[r][fc]
        null_basis.append(v)

    rank0 = len(pivots)
    n_left = len(null_basis)
    print(f"    A0 rank: {rank0}, left null dim: {n_left}")

    # Step 2: First-order constraint in FULL space: L * A1 * c0 = L * b1
    # where c0 = c_fixed + M * a (symmetric parameterization)
    # So: L * A1 * M * a = L * (b1 - A1 * c_fixed)

    # Compute A1 * c_fixed
    A1_cf = [sum(A1[i][j] * c_fixed[j] for j in range(N)) for i in range(N)]

    # Compute A1 * M columns
    A1_M = [[Fraction(0)] * n_free for _ in range(N)]
    for j in range(n_free):
        for i in range(N):
            A1_M[i][j] = sum(A1[i][k] * M_mat[k][j] for k in range(N))

    # Project through left null space: L * A1 * M and L * (b1 - A1*cf)
    C_sym = []  # n_left x n_free
    d_sym = []  # n_left x 1

    for v in null_basis:
        row = [sum(v[i] * A1_M[i][j] for i in range(N)) for j in range(n_free)]
        C_sym.append(row)
        rhs = sum(v[i] * (b1[i] - A1_cf[i]) for i in range(N))
        d_sym.append(rhs)

    # Step 3: Add vanishing condition g0(k0) = 0
    # k0 = (t^{-2}, t^{-1}, 1)
    k0 = (t_val ** (-2), t_val ** (-1), Fraction(1))

    # g0(k0) = sum over all monomials of coeff * k0^m
    # = k0^leading + sum_{unk} c[i] * k0^{unk_monoms[i]}
    # = k0^leading + sum_i c_fixed[i]*k0^{unk[i]} + sum_j a[j] * (sum_{i: part(i)=j} k0^{unk[i]})

    def eval_monom(m, pt):
        return pt[0]**m[0] * pt[1]**m[1] * pt[2]**m[2]

    lead_eval = eval_monom(leading, k0)
    fixed_eval = sum(c_fixed[i] * eval_monom(unk_monoms[i], k0) for i in range(N))

    van_row = [Fraction(0)] * n_free
    for i in range(N):
        pidx = unk_partition_idx[i]
        if pidx != leading_part_idx:
            j = free_parts.index(pidx)
            van_row[j] += eval_monom(unk_monoms[i], k0)

    van_rhs = -(lead_eval + fixed_eval)

    # Combined system: C_sym * a = d_sym  AND  van_row * a = van_rhs
    # Stack them
    full_C = C_sym + [van_row]
    full_d = d_sym + [van_rhs]
    n_eq = len(full_C)

    print(f"    Combined system: {n_eq} equations, {n_free} unknowns")

    # Solve by Gaussian elimination
    aug = [full_C[i][:] + [full_d[i]] for i in range(n_eq)]

    pivs = []
    ri = 0
    for col in range(n_free):
        piv = None
        for r in range(ri, n_eq):
            if aug[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: continue
        pivs.append((ri, col))
        if piv != ri:
            aug[ri], aug[piv] = aug[piv], aug[ri]
        pv = aug[ri][col]
        for j in range(n_free + 1):
            aug[ri][j] /= pv
        for r in range(n_eq):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(n_free + 1):
                    aug[r][j] -= f * aug[ri][j]
        ri += 1

    rank_sym = len(pivs)
    print(f"    Symmetric system rank: {rank_sym} / {n_free}")

    if rank_sym < n_free:
        print(f"    *** Underdetermined: {n_free - rank_sym} free parameters ***")
        return None

    # Check consistency (no contradictory rows)
    consistent = True
    for r in range(rank_sym, n_eq):
        if aug[r][n_free] != Fraction(0):
            consistent = False
            break

    if not consistent:
        print(f"    *** INCONSISTENT: symmetry assumption contradicts perturbation! ***")
        return False

    # Extract solution
    a_sol = [Fraction(0)] * n_free
    for r, c in pivs:
        a_sol[c] = aug[r][n_free]

    # Build full coefficient vector c0_sym
    c0_sym = list(c_fixed)
    for i in range(N):
        pidx = unk_partition_idx[i]
        if pidx != leading_part_idx:
            j = free_parts.index(pidx)
            c0_sym[i] += a_sol[j]

    # Step 4: CRITICAL CHECK - does c0_sym satisfy FULL first-order constraints?
    # Check L * (b1 - A1 * c0_sym) = 0 for ALL left null vectors
    residuals = []
    for v in null_basis:
        r = sum(v[i] * (b1[i] - sum(A1[i][j] * c0_sym[j] for j in range(N)) - A1_cf[i] + A1_cf[i]) for i in range(N))
        # Actually: the constraint is v . (b1 - A1*(c_fixed + c0_from_free))
        # But c0_sym already includes c_fixed. Let me recompute:
        pass

    # Recompute properly: c0_full[i] = c0_sym[i] (which includes c_fixed contribution)
    # First-order constraint: for each left null vector v:
    #   sum_i v[i] * (b1[i] - sum_j A1[i][j] * c0_full[j]) = 0

    max_resid = Fraction(0)
    n_nonzero = 0
    for v in null_basis:
        val = Fraction(0)
        for i in range(N):
            term = b1[i]
            for j in range(N):
                term -= A1[i][j] * c0_sym[j]
            val += v[i] * term
        if val != Fraction(0):
            n_nonzero += 1
        if abs(val) > max_resid:
            max_resid = abs(val)
        residuals.append(val)

    print(f"    Full first-order residual: {n_nonzero}/{n_left} nonzero, max = {float(max_resid):.6e}")

    if n_nonzero == 0:
        print(f"    *** PASS: Symmetric solution satisfies ALL first-order constraints ***")
    else:
        print(f"    *** FAIL: Symmetric solution violates {n_nonzero} first-order constraints ***")
        return False

    # Step 5: Verify symmetry of the coefficient vector
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c0_sym[i]
    coeffs[leading] = Fraction(1)

    sym_groups = {}
    for m, c in coeffs.items():
        key = tuple(sorted(m, reverse=True))
        if key not in sym_groups:
            sym_groups[key] = []
        sym_groups[key].append((m, c))

    all_sym = True
    for key, group in sorted(sym_groups.items()):
        vals = [c for _, c in group]
        if len(vals) > 1:
            for v in vals[1:]:
                if v != vals[0]:
                    all_sym = False

    print(f"    Coefficient symmetry: {'EXACT' if all_sym else 'BROKEN'}")

    # Print a few coefficients
    print(f"    Sample coefficients (partition: value):")
    for pidx in range(min(6, len(partitions))):
        p = partitions[pidx]
        if pidx == leading_part_idx:
            val = Fraction(1)
        else:
            j = free_parts.index(pidx)
            val = a_sol[j]
        print(f"      m_{p} = {val} = {float(val):.10f}")

    elapsed = time.time() - t0
    print(f"    ({elapsed:.1f}s)")
    return True

# Run at several t values
for t_val in [Fraction(7, 10), Fraction(3, 4), Fraction(1, 3), Fraction(5, 3)]:
    print(f"\n  t = {t_val}:")
    result = run_test(t_val)
    if result is True:
        print(f"    ==> Symmetry CONSISTENT with first-order perturbation")
    elif result is False:
        print(f"    ==> Symmetry INCONSISTENT")
    else:
        print(f"    ==> Underdetermined (need higher-order terms)")
    sys.stdout.flush()

print(f"\n{'='*70}")
print("DONE")
