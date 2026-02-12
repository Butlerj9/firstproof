"""
P03 EXP-7: Algebraic perturbation theory for Symmetry Conjecture at n=3.

Strategy: Write q = 1 - eps. At q=1 the 55x55 vanishing system degenerates to rank 5
(50-dim null space). The first-order perturbation in eps provides 50 additional linear
constraints on the q=1 solution, which (if independent) uniquely determine it.

We compute A0, A1 (zeroth and first-order matrices) symbolically in t, find the
left null space of A0, project the first-order constraint through it, and solve
for c0. Then we check if c0 gives a symmetric polynomial.

Uses exact Fraction arithmetic with t as a specific rational value first,
then optionally SymPy for symbolic verification.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fractions import Fraction
import time

print("P03 EXP-7: Algebraic perturbation theory for n=3 symmetry")
print("=" * 70)

def k_stat(nu, i):
    """Compute k-statistic for composition nu at position i."""
    n = len(nu)
    count = 0
    for j in range(i):
        if nu[j] > nu[i]:
            count += 1
    for j in range(i+1, n):
        if nu[j] >= nu[i]:
            count += 1
    return count

# Setup for n=3, lambda = (3,2,0), lambda^- = (0,2,3)
n = 3
leading = (0, 2, 3)

# All compositions of weight <= 5 into 3 parts
comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

print(f"  Total compositions: {len(comps)}")

# Monomial list (same as compositions)
monoms = list(comps)
leading_idx = monoms.index(leading)

# Vanishing compositions (all except leading)
van_comps = [nu for nu in comps if nu != leading]
# Unknown monomials (all except leading, whose coeff is fixed to 1)
unk_monoms = [m for m in monoms if m != leading]
n_van = len(van_comps)
n_unk = len(unk_monoms)
print(f"  Vanishing conditions: {n_van}")
print(f"  Unknown coefficients: {n_unk}")

# ============================================================
# Phase 1: Exact computation at specific rational t
# ============================================================

def run_perturbation(t_val):
    """Run perturbation theory at a specific rational t value."""

    # Compute k-statistics for all compositions
    k_stats = {}
    for nu in comps:
        k_stats[nu] = tuple(k_stat(nu, i) for i in range(n))

    # Build A0 (q=1 matrix) and A1 (dA/dq at q=1) for the vanishing system
    # A[nu, m] = q^{sum(nu_i * m_i)} * t^{-sum(k_i * m_i)}
    # A0[nu, m] = t^{-sum(k_i(nu) * m_i)}  (q=1 term)
    # A1[nu, m] = sum(nu_i * m_i) * t^{-sum(k_i(nu) * m_i)}  (d/dq at q=1)

    A0 = []
    A1 = []
    b0 = []
    b1 = []

    for nu in van_comps:
        k = k_stats[nu]

        row0 = []
        row1 = []
        for m in unk_monoms:
            t_exp = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2])
            q_exp_deriv = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2]

            t_power = t_val ** t_exp  # This is exact for Fraction
            row0.append(t_power)
            row1.append(Fraction(q_exp_deriv) * t_power)

        A0.append(row0)
        A1.append(row1)

        # RHS: negative of the leading monomial column
        m_lead = leading
        t_exp_lead = -(k[0]*m_lead[0] + k[1]*m_lead[1] + k[2]*m_lead[2])
        q_exp_lead = nu[0]*m_lead[0] + nu[1]*m_lead[1] + nu[2]*m_lead[2]
        t_power_lead = t_val ** t_exp_lead

        b0.append(-t_power_lead)
        b1.append(-Fraction(q_exp_lead) * t_power_lead)

    # Step 1: Find rank and null space of A0
    # Gaussian elimination to find rank
    N = n_unk  # = 55
    aug0 = [A0[i][:] for i in range(N)]

    pivot_cols = []
    row_idx = 0
    for col in range(N):
        # Find pivot
        pivot = None
        for r in range(row_idx, N):
            if aug0[r][col] != Fraction(0):
                pivot = r
                break
        if pivot is None:
            continue
        pivot_cols.append(col)
        if pivot != row_idx:
            aug0[row_idx], aug0[pivot] = aug0[pivot], aug0[row_idx]
        piv_val = aug0[row_idx][col]
        # Eliminate below
        for r in range(row_idx + 1, N):
            if aug0[r][col] != Fraction(0):
                factor = Fraction(aug0[r][col], piv_val)
                for j in range(col, N):
                    aug0[r][j] -= factor * aug0[row_idx][j]
        row_idx += 1

    rank0 = len(pivot_cols)
    null_dim = N - rank0
    print(f"    Rank of A0: {rank0}, null dim: {null_dim}")

    if null_dim == 0:
        print(f"    System is full rank at q=1 — no perturbation needed")
        return None

    # Step 2: Find left null space of A0 (rows of V such that V * A0 = 0)
    # Transpose and find null space
    A0T = [[A0[j][i] for j in range(N)] for i in range(N)]

    # Row reduce A0^T
    augT = [row[:] + [Fraction(1) if i == j else Fraction(0) for j in range(N)]
            for i, row in enumerate(A0T)]

    # Gaussian elimination on A0^T to find left null space of A0
    # Actually, let's do it differently: left null space of A0 = null space of A0^T

    # Row reduce A0^T
    M = N  # rows = N (columns of original)
    pivot_cols_T = []
    row_idx = 0
    for col in range(N):
        pivot = None
        for r in range(row_idx, M):
            if augT[r][col] != Fraction(0):
                pivot = r
                break
        if pivot is None:
            continue
        pivot_cols_T.append(col)
        if pivot != row_idx:
            augT[row_idx], augT[pivot] = augT[pivot], augT[row_idx]
        piv_val = augT[row_idx][col]
        for r in range(M):
            if r != row_idx and augT[r][col] != Fraction(0):
                factor = Fraction(augT[r][col], piv_val)
                for j in range(2*N):
                    augT[r][j] -= factor * augT[row_idx][j]
        # Normalize pivot row
        for j in range(2*N):
            augT[row_idx][j] = Fraction(augT[row_idx][j], piv_val)
        row_idx += 1

    rank_T = len(pivot_cols_T)
    # The left null space vectors are the rows of augT that became zero in the first N columns
    free_rows = [i for i in range(N) if all(augT[i][j] == Fraction(0) for j in range(N))]

    # Actually this approach is getting complicated. Let me use a cleaner method.
    # Left null space of A0 = vectors v such that v^T A0 = 0, i.e. A0^T v = 0

    # Use standard null space computation for A0^T
    # Row reduce A0^T to RREF
    mat = [[A0[j][i] for j in range(N)] for i in range(N)]  # A0^T

    pivots = []
    row_idx = 0
    for col in range(N):
        pivot = None
        for r in range(row_idx, N):
            if mat[r][col] != Fraction(0):
                pivot = r
                break
        if pivot is None:
            continue
        pivots.append((row_idx, col))
        if pivot != row_idx:
            mat[row_idx], mat[pivot] = mat[pivot], mat[row_idx]
        piv_val = mat[row_idx][col]
        for j in range(N):
            mat[row_idx][j] = Fraction(mat[row_idx][j], piv_val)
        for r in range(N):
            if r != row_idx and mat[r][col] != Fraction(0):
                factor = mat[r][col]
                for j in range(N):
                    mat[r][j] -= factor * mat[row_idx][j]
        row_idx += 1

    pivot_row_cols = {r: c for r, c in pivots}
    pivot_col_set = {c for _, c in pivots}
    free_cols = [c for c in range(N) if c not in pivot_col_set]

    print(f"    Rank of A0^T: {len(pivots)}, free cols: {len(free_cols)}")

    # Build null space basis for A0^T
    null_basis = []
    for fc in free_cols:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots:
            v[c] = -mat[r][fc]
        null_basis.append(v)

    print(f"    Left null space dimension: {len(null_basis)}")

    # Verify: each null vector v satisfies A0^T v = 0
    verify_count = 0
    for v in null_basis[:3]:
        # A0^T v = 0 means sum_j A0[j][i] * v[j] = 0 for all i
        ok = True
        for i in range(N):
            s = sum(A0[j][i] * v[j] for j in range(N))
            if s != Fraction(0):
                ok = False
                break
        if ok:
            verify_count += 1
    print(f"    Null space verification (first 3): {verify_count}/3 pass")

    # Step 3: Project first-order constraint through left null space
    # For each left null vector v: v . (b1 - A1 c0) = 0
    # where c0 is the unknown coefficient vector
    # Since A0 c0 = b0, c0 is in the affine subspace b0 + null(A0)

    # First, find a particular solution c0_part to A0 c0 = b0
    # Augmented system [A0 | b0]
    aug = [A0[i][:] + [b0[i]] for i in range(N)]

    pivots2 = []
    row_idx = 0
    for col in range(N):
        pivot = None
        for r in range(row_idx, N):
            if aug[r][col] != Fraction(0):
                pivot = r
                break
        if pivot is None:
            continue
        pivots2.append((row_idx, col))
        if pivot != row_idx:
            aug[row_idx], aug[pivot] = aug[pivot], aug[row_idx]
        piv_val = aug[row_idx][col]
        for j in range(N + 1):
            aug[row_idx][j] = Fraction(aug[row_idx][j], piv_val)
        for r in range(N):
            if r != row_idx and aug[r][col] != Fraction(0):
                factor = aug[r][col]
                for j in range(N + 1):
                    aug[r][j] -= factor * aug[row_idx][j]
        row_idx += 1

    # Extract particular solution
    c0_part = [Fraction(0)] * N
    for r, c in pivots2:
        c0_part[c] = aug[r][N]

    # Null space of A0 (right null space)
    pivot_col_set2 = {c for _, c in pivots2}
    free_cols2 = [c for c in range(N) if c not in pivot_col_set2]

    null_A0 = []
    for fc in free_cols2:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots2:
            v[c] = -aug[r][fc]
        null_A0.append(v)

    print(f"    Right null space dim of A0: {len(null_A0)}")

    # c0 = c0_part + sum alpha_k * null_A0[k]
    # Constraint: for each left null vector v_j:
    #   v_j . (b1 - A1 * c0) = 0
    #   v_j . b1 - v_j . A1 . (c0_part + sum alpha_k * null_A0[k]) = 0
    #   v_j . b1 - v_j . A1 . c0_part = sum alpha_k * (v_j . A1 . null_A0[k])

    n_null = len(null_A0)
    n_left = len(null_basis)

    print(f"    Building {n_left} x {n_null} constraint system...")

    # Compute v_j . A1 . null_A0[k] for each j, k
    # And v_j . (b1 - A1 . c0_part) for each j

    # First compute A1 . c0_part and A1 . null_A0[k]
    A1_c0_part = [sum(A1[i][j] * c0_part[j] for j in range(N)) for i in range(N)]

    A1_null = []
    for null_vec in null_A0:
        col = [sum(A1[i][j] * null_vec[j] for j in range(N)) for i in range(N)]
        A1_null.append(col)

    # Build the constraint matrix C and RHS d
    # C[j][k] = v_j . A1_null[k]
    # d[j] = v_j . (b1 - A1_c0_part)

    C_mat = []
    d_vec = []

    for v in null_basis:
        row = []
        for A1n in A1_null:
            row.append(sum(v[i] * A1n[i] for i in range(N)))
        C_mat.append(row)

        rhs = sum(v[i] * (b1[i] - A1_c0_part[i]) for i in range(N))
        d_vec.append(rhs)

    print(f"    Constraint system: {n_left} x {n_null}")

    # Solve C_mat . alpha = d_vec
    # Gaussian elimination
    aug_c = [C_mat[i][:] + [d_vec[i]] for i in range(n_left)]

    pivots3 = []
    row_idx = 0
    for col in range(n_null):
        pivot = None
        for r in range(row_idx, n_left):
            if aug_c[r][col] != Fraction(0):
                pivot = r
                break
        if pivot is None:
            continue
        pivots3.append((row_idx, col))
        if pivot != row_idx:
            aug_c[row_idx], aug_c[pivot] = aug_c[pivot], aug_c[row_idx]
        piv_val = aug_c[row_idx][col]
        for j in range(n_null + 1):
            aug_c[row_idx][j] = Fraction(aug_c[row_idx][j], piv_val)
        for r in range(n_left):
            if r != row_idx and aug_c[r][col] != Fraction(0):
                factor = aug_c[r][col]
                for j in range(n_null + 1):
                    aug_c[r][j] -= factor * aug_c[row_idx][j]
        row_idx += 1

    rank_constraint = len(pivots3)
    print(f"    Constraint rank: {rank_constraint} / {n_null}")

    if rank_constraint < n_null:
        print(f"    *** First-order constraints insufficient: {rank_constraint} < {n_null} ***")
        print(f"    Need higher-order perturbation terms")
        return None

    # Extract alpha
    alpha = [Fraction(0)] * n_null
    for r, c in pivots3:
        alpha[c] = aug_c[r][n_null]

    # Compute c0 = c0_part + sum alpha_k * null_A0[k]
    c0 = list(c0_part)
    for k in range(n_null):
        for j in range(N):
            c0[j] += alpha[k] * null_A0[k][j]

    # Build full coefficient dictionary
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c0[i]
    coeffs[leading] = Fraction(1)

    # Check symmetry: group by sorted monomial
    sym_groups = {}
    for m, c in coeffs.items():
        key = tuple(sorted(m))
        if key not in sym_groups:
            sym_groups[key] = []
        sym_groups[key].append((m, c))

    all_symmetric = True
    max_asym = Fraction(0)
    asym_count = 0
    for key, group in sorted(sym_groups.items()):
        vals = [c for _, c in group]
        if len(vals) > 1:
            for i in range(1, len(vals)):
                diff = abs(vals[i] - vals[0])
                if diff > max_asym:
                    max_asym = diff
                if diff > 0:
                    all_symmetric = False
                    asym_count += 1

    return all_symmetric, max_asym, asym_count, coeffs

# Run at several t values
print(f"\n  Phase 1: First-order perturbation at specific t values")
print("-" * 60)

t_values = [Fraction(7, 10), Fraction(3, 4), Fraction(1, 3), Fraction(5, 3)]

for t_val in t_values:
    print(f"\n  t = {t_val}:")
    start = time.time()
    result = run_perturbation(t_val)
    elapsed = time.time() - start

    if result is None:
        print(f"    (computation incomplete, {elapsed:.1f}s)")
    else:
        is_sym, max_asym, asym_count, coeffs = result
        if is_sym:
            print(f"    *** EXACT SYMMETRY (first-order perturbation) ***")
            print(f"    All coefficient groups match exactly")
        else:
            print(f"    NOT symmetric: max_asym = {float(max_asym):.6e}, {asym_count} pairs")
        print(f"    ({elapsed:.1f}s)")

    sys.stdout.flush()

print(f"\n{'='*70}")
print("DONE")
