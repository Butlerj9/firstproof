"""
P03 EXP-5b: Direct computation at exact q=1 via degenerate system analysis.

At q=1, many compositions share the same spectral vector.
This script:
  1. Identifies distinct spectral vectors at q=1
  2. Solves the (underdetermined) vanishing system
  3. Checks if the null space forces symmetry
  4. Investigates the t=2 anomaly from EXP-5
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 100

from itertools import permutations
from collections import defaultdict

print("P03 EXP-5b: Direct computation at exact q=1")
print("=" * 70)

n = 3
lam_minus = (0, 2, 3)

def compositions_of(total, nparts):
    if nparts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions_of(total - first, nparts - 1):
            yield (first,) + rest

def k_vector(nu):
    """Compute k-vector of composition nu."""
    result = []
    for i in range(len(nu)):
        k_i = sum(1 for j in range(i) if nu[j] > nu[i]) + \
              sum(1 for j in range(i + 1, len(nu)) if nu[j] >= nu[i])
        result.append(k_i)
    return tuple(result)

def spectral_vector_q1(nu, t):
    """Spectral vector at q=1: nu_tilde_i = t^{-k_i}."""
    kv = k_vector(nu)
    return tuple(t ** (-k) for k in kv)

# Monomial basis
monoms = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            monoms.append((a, b, c))

leading = (0, 2, 3)
leading_idx = monoms.index(leading)

# All compositions with |nu| <= 5
all_comps = []
for total in range(6):
    all_comps.extend(list(compositions_of(total, 3)))
vanishing_comps = [nu for nu in all_comps if nu != lam_minus]

# ============================================================
# PHASE 1: Identify distinct spectral vectors at q=1
# ============================================================
print("\nPHASE 1: Distinct spectral vectors at q=1")
print("-" * 60)

# Group compositions by k-vector
kv_groups = defaultdict(list)
for nu in all_comps:
    kv = k_vector(nu)
    kv_groups[kv].append(nu)

print(f"Total compositions |nu| <= 5: {len(all_comps)}")
print(f"Distinct k-vectors: {len(kv_groups)}")
print()

# Show groups with multiple compositions
for kv, comps in sorted(kv_groups.items()):
    if len(comps) > 1:
        print(f"  k-vector {kv}: {comps}")

# Count distinct spectral vectors (same k-vector => same spectral point at q=1)
vanishing_kv = set()
for nu in vanishing_comps:
    vanishing_kv.add(k_vector(nu))

# Remove the k-vector of lam_minus itself (which is (2,1,0) for (0,2,3))
lam_kv = k_vector(lam_minus)
print(f"\nk-vector of lambda^- = {lam_minus}: {lam_kv}")
vanishing_kv.discard(lam_kv)

print(f"Distinct vanishing spectral points at q=1: {len(vanishing_kv)}")
print(f"Unknowns (non-leading coefficients): {len(monoms) - 1}")
print(f"System is {'underdetermined' if len(vanishing_kv) < len(monoms) - 1 else 'determined or overdetermined'}")

# ============================================================
# PHASE 2: Solve directly at q=1
# ============================================================
print(f"\nPHASE 2: Direct solution at q=1")
print("-" * 60)

t_val = mpmath.mpf('7') / 10

# Set up the vanishing system using distinct spectral points
distinct_sv = sorted(vanishing_kv)
unknown_monoms = [m for m in monoms if m != leading]

nrows = len(distinct_sv)
ncols = len(unknown_monoms)
print(f"System: {nrows} equations x {ncols} unknowns")

A = mpmath.matrix(nrows, ncols)
b = mpmath.matrix(nrows, 1)

for row, kv in enumerate(distinct_sv):
    sv = tuple(t_val ** (-k) for k in kv)
    for col, monom in enumerate(unknown_monoms):
        A[row, col] = sv[0] ** monom[0] * sv[1] ** monom[1] * sv[2] ** monom[2]
    b[row] = -(sv[0] ** leading[0] * sv[1] ** leading[1] * sv[2] ** leading[2])

# Check rank
print(f"Computing SVD to check rank...")

# For underdetermined systems, use SVD to find minimum-norm solution
# and analyze null space
if nrows < ncols:
    print(f"System is underdetermined ({nrows} < {ncols}). Using SVD analysis.")

    # Compute A^T A for the normal equations approach
    # Or use mpmath's SVD
    # Actually, let's just check: does the minimum-norm solution give a symmetric polynomial?

    # Use the pseudoinverse: x = A^T (A A^T)^{-1} b
    AAt = A * A.T
    try:
        AAt_inv = AAt ** (-1)
        x_min = A.T * AAt_inv * b

        # Build full coefficients
        full_coeffs = [mpmath.mpf(0)] * len(monoms)
        full_coeffs[leading_idx] = mpmath.mpf(1)
        for i, idx in enumerate([j for j, m in enumerate(monoms) if m != leading]):
            full_coeffs[idx] = x_min[i]

        # Check symmetry
        groups = defaultdict(list)
        for idx, monom in enumerate(monoms):
            key = tuple(sorted(monom))
            groups[key].append((monom, full_coeffs[idx]))

        max_rd = mpmath.mpf(0)
        for key, entries in sorted(groups.items()):
            if len(entries) <= 1:
                continue
            coeffs = [c for _, c in entries]
            mean_c = sum(coeffs) / len(coeffs)
            if abs(mean_c) > mpmath.mpf('1e-50'):
                rd = max(abs(c - mean_c) / abs(mean_c) for c in coeffs)
                max_rd = max(max_rd, rd)

        print(f"Minimum-norm solution: max symmetry deviation = {mpmath.nstr(max_rd, 10)}")

        if max_rd < mpmath.mpf('1e-10'):
            print("*** Minimum-norm solution IS symmetric ***")
        else:
            print("Minimum-norm solution is NOT symmetric. Need to add limit constraints.")
    except Exception as e:
        print(f"SVD solve failed: {e}")
else:
    print(f"System is determined ({nrows} >= {ncols}). Solving directly.")
    try:
        x = mpmath.lu_solve(A, b)
        full_coeffs = [mpmath.mpf(0)] * len(monoms)
        full_coeffs[leading_idx] = mpmath.mpf(1)
        for i, idx in enumerate([j for j, m in enumerate(monoms) if m != leading]):
            full_coeffs[idx] = x[i]

        groups = defaultdict(list)
        for idx, monom in enumerate(monoms):
            key = tuple(sorted(monom))
            groups[key].append((monom, full_coeffs[idx]))

        max_rd = mpmath.mpf(0)
        for key, entries in sorted(groups.items()):
            if len(entries) <= 1:
                continue
            coeffs = [c for _, c in entries]
            mean_c = sum(coeffs) / len(coeffs)
            if abs(mean_c) > mpmath.mpf('1e-50'):
                rd = max(abs(c - mean_c) / abs(mean_c) for c in coeffs)
                max_rd = max(max_rd, rd)

        print(f"Direct solution: max symmetry deviation = {mpmath.nstr(max_rd, 10)}")
    except Exception as e:
        print(f"Direct solve failed: {e}")

# ============================================================
# PHASE 3: Null space analysis
# ============================================================
print(f"\nPHASE 3: Null space analysis at q=1")
print("-" * 60)

if nrows < ncols:
    null_dim = ncols - nrows
    print(f"Expected null space dimension: {null_dim}")
    print(f"The unique q->1 limit picks one element of the {null_dim+1}-dim affine space.")
    print(f"Key question: does the null space contain only symmetric directions?")

    # If we IMPOSE symmetry, how many unknowns remain?
    # Group unknowns by sorted monomial
    sym_groups = defaultdict(list)
    for i, m in enumerate(unknown_monoms):
        key = tuple(sorted(m))
        sym_groups[key].append(i)

    n_sym_unknowns = len(sym_groups)
    print(f"If we impose symmetry: {n_sym_unknowns} independent coefficients")
    print(f"Vanishing conditions: {nrows}")
    print(f"{'Over' if nrows > n_sym_unknowns else 'Under' if nrows < n_sym_unknowns else 'Exactly '}determined under symmetry constraint")

    # Solve with symmetry imposed: average the columns for each symmetry group
    A_sym = mpmath.matrix(nrows, n_sym_unknowns)
    sym_keys = sorted(sym_groups.keys())
    for row in range(nrows):
        for col, key in enumerate(sym_keys):
            indices = sym_groups[key]
            A_sym[row, col] = sum(A[row, i] for i in indices)

    # Also need to handle the leading monomial group
    # The leading monomial (0,2,3) has sorted key (0,2,3)
    # Under symmetry, all 6 permutations have coefficient 1
    # But we already fixed coefficient of (0,2,3) = 1
    # The OTHER 5 monomials in this group are unknowns
    # Under symmetry, they should also be 1
    # So we should remove them from the unknown list and add their contribution to b

    # Actually, let me redo this more carefully.
    # Under symmetry, all monomials with the same sorted exponents have the same coefficient.
    # The leading group (0,2,3) already has coefficient 1 for the leading monomial.
    # Under symmetry, all 6 monomials in this group have coefficient 1.
    # So the 5 non-leading monomials in this group contribute 5 * (monomial evaluations) to the system.

    # Let me rebuild the system with symmetry
    # For each row (spectral point), the equation is:
    # sum_{monom} c_{sorted(monom)} * monom(sv) = 0

    # Group ALL monomials by sorted key
    all_sym_groups = defaultdict(list)
    for idx, m in enumerate(monoms):
        key = tuple(sorted(m))
        all_sym_groups[key].append((idx, m))

    sym_keys_all = sorted(all_sym_groups.keys())
    # The leading group is (0,2,3) with coefficient 1 (fixed)
    leading_key = tuple(sorted(leading))
    free_keys = [k for k in sym_keys_all if k != leading_key]

    A_sym2 = mpmath.matrix(nrows, len(free_keys))
    b_sym2 = mpmath.matrix(nrows, 1)

    for row, kv in enumerate(distinct_sv):
        sv = tuple(t_val ** (-k) for k in kv)
        # RHS: negative of the leading group's contribution
        leading_contrib = sum(
            sv[0] ** m[0] * sv[1] ** m[1] * sv[2] ** m[2]
            for _, m in all_sym_groups[leading_key]
        )
        b_sym2[row] = -leading_contrib

        for col, key in enumerate(free_keys):
            total = mpmath.mpf(0)
            for _, m in all_sym_groups[key]:
                total += sv[0] ** m[0] * sv[1] ** m[1] * sv[2] ** m[2]
            A_sym2[row, col] = total

    print(f"\nSymmetric system: {nrows} equations x {len(free_keys)} unknowns")

    if nrows >= len(free_keys):
        try:
            x_sym = mpmath.lu_solve(A_sym2, b_sym2)
            print(f"Symmetric system solved successfully!")

            # Build the symmetric polynomial
            sym_coeffs = {}
            sym_coeffs[leading_key] = mpmath.mpf(1)
            for i, key in enumerate(free_keys):
                sym_coeffs[key] = x_sym[i]

            # Verify vanishing
            max_resid = mpmath.mpf(0)
            for kv in distinct_sv:
                sv = tuple(t_val ** (-k) for k in kv)
                val = mpmath.mpf(0)
                for key, coeff in sym_coeffs.items():
                    for _, m in all_sym_groups[key]:
                        val += coeff * sv[0] ** m[0] * sv[1] ** m[1] * sv[2] ** m[2]
                max_resid = max(max_resid, abs(val))

            print(f"Max vanishing residual: {mpmath.nstr(max_resid, 10)}")

            if max_resid < mpmath.mpf('1e-50'):
                print("\n*** A SYMMETRIC POLYNOMIAL SATISFIES ALL VANISHING CONDITIONS AT q=1 ***")
                print("*** This means E*_{lambda^-}(q=1) IS symmetric (unique solution of vanishing system) ***")
            else:
                print("Symmetric solution does NOT satisfy vanishing conditions.")

            # Print the symmetric coefficients
            print(f"\nSymmetric polynomial coefficients:")
            for key in sorted(sym_coeffs.keys()):
                val = sym_coeffs[key]
                mult = len(all_sym_groups[key])
                print(f"  m_{key} (x{mult}): {mpmath.nstr(val, 25)}")

            # Compare with Richardson extrapolation from EXP-5
            print(f"\n  (Compare these with the Richardson-extrapolated values from EXP-5)")

        except Exception as e:
            print(f"Symmetric system solve failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Symmetric system is underdetermined: {nrows} < {len(free_keys)}")
        print(f"Cannot uniquely determine the symmetric polynomial at q=1.")

# ============================================================
# PHASE 4: t=2 investigation
# ============================================================
print(f"\nPHASE 4: t=2 investigation")
print("-" * 60)

t2 = mpmath.mpf(2)

# Check spectral vector collisions at q near 1, t=2
print("Spectral vector near-collisions at t=2, q=0.9999:")
q_test = mpmath.mpf('0.9999')
sv_dict = {}
for nu in all_comps:
    sv = tuple(q_test ** nu[i] * t2 ** (-k_vector(nu)[i]) for i in range(3))
    sv_key = tuple(float(s) for s in sv)
    if sv_key in sv_dict:
        print(f"  COLLISION: {nu} and {sv_dict[sv_key]} share spectral vector {sv_key}")
    sv_dict[sv_key] = nu

# Condition number of the system at t=2
print(f"\nCondition number analysis at t=2:")
for q_label, q_val in [('0.9999', mpmath.mpf('0.9999')),
                         ('0.99999', mpmath.mpf('0.99999'))]:
    A_test = mpmath.matrix(len(vanishing_comps), len(unknown_monoms))
    for row, nu in enumerate(vanishing_comps):
        sv = tuple(q_val ** nu[i] * t2 ** (-k_vector(nu)[i]) for i in range(3))
        for col, monom in enumerate(unknown_monoms):
            A_test[row, col] = sv[0] ** monom[0] * sv[1] ** monom[1] * sv[2] ** monom[2]

    # Estimate condition number via max/min singular value ratio
    try:
        # Just compute the matrix norm as a rough indicator
        max_entry = max(abs(A_test[i, j]) for i in range(A_test.rows) for j in range(A_test.cols))
        min_nonzero = min(abs(A_test[i, j]) for i in range(A_test.rows) for j in range(A_test.cols)
                         if abs(A_test[i, j]) > mpmath.mpf('1e-50'))
        print(f"  q={q_label}: max|A| = {mpmath.nstr(max_entry, 5)}, min|A| = {mpmath.nstr(min_nonzero, 5)}, "
              f"ratio ~ {mpmath.nstr(max_entry / min_nonzero, 5)}")
    except:
        print(f"  q={q_label}: analysis failed")

# Retry t=2 with closer h values
print(f"\nRetrying Richardson extrapolation at t=2 with closer h values:")
h_close = [mpmath.power(10, -k) for k in [20, 22, 24, 26, 28, 30, 32, 34, 36, 38]]
q_close = [1 - h for h in h_close]

def compute_E_star_full(q, t):
    nrows = len(vanishing_comps)
    ncols = len(unknown_monoms)
    A = mpmath.matrix(nrows, ncols)
    b = mpmath.matrix(nrows, 1)
    for row, nu in enumerate(vanishing_comps):
        sv = tuple(q ** nu[i] * t ** (-k_vector(nu)[i]) for i in range(3))
        for col, monom in enumerate(unknown_monoms):
            A[row, col] = sv[0] ** monom[0] * sv[1] ** monom[1] * sv[2] ** monom[2]
        b[row] = -(sv[0] ** leading[0] * sv[1] ** leading[1] * sv[2] ** leading[2])
    return mpmath.lu_solve(A, b)

def build_full(E_coeffs):
    full = [mpmath.mpf(0)] * len(monoms)
    full[leading_idx] = mpmath.mpf(1)
    for i, idx in enumerate([j for j, m in enumerate(monoms) if m != leading]):
        full[idx] = E_coeffs[i]
    return full

def neville(h_vals, y_vals):
    m = len(h_vals)
    table = [[mpmath.mpf(0)] * m for _ in range(m)]
    for i in range(m):
        table[i][0] = y_vals[i]
    for j in range(1, m):
        for i in range(j, m):
            table[i][j] = ((h_vals[i - j] * table[i][j - 1] - h_vals[i] * table[i - 1][j - 1])
                           / (h_vals[i - j] - h_vals[i]))
    return table[m - 1][m - 1]

coeff_sets_t2 = []
for q_val in q_close:
    E_c = compute_E_star_full(q_val, t2)
    coeff_sets_t2.append(build_full(E_c))

ext_t2 = [mpmath.mpf(0)] * len(monoms)
for k in range(len(monoms)):
    y_v = [coeff_sets_t2[i][k] for i in range(len(q_close))]
    ext_t2[k] = neville(h_close, y_v)

# Check symmetry
groups_t2 = defaultdict(list)
for idx, monom in enumerate(monoms):
    key = tuple(sorted(monom))
    groups_t2[key].append((monom, ext_t2[idx]))

max_rd_t2 = mpmath.mpf(0)
for key, entries in groups_t2.items():
    if len(entries) <= 1:
        continue
    coeffs = [c for _, c in entries]
    mean_c = sum(coeffs) / len(coeffs)
    if abs(mean_c) > mpmath.mpf('1e-50'):
        rd = max(abs(c - mean_c) / abs(mean_c) for c in coeffs)
        max_rd_t2 = max(max_rd_t2, rd)

digits_t2 = -int(mpmath.log10(max_rd_t2)) if max_rd_t2 > 0 else 100
print(f"  t=2 with close h values: max rel dev = {mpmath.nstr(max_rd_t2, 8)} ({digits_t2}+ digits)")

print(f"\n{'='*70}")
print("CONCLUSION")
print("=" * 70)
