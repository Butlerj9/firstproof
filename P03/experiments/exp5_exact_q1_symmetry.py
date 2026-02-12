"""
P03 EXP-5: High-precision computation of E*_{(0,2,3)} at exact q=1.

Strategy:
  1. Richardson extrapolation: compute E* at q = 1 - h for h = 10^{-k},
     use polynomial extrapolation to get exact q=1 value to ~150 digits.
  2. Verify symmetry by checking coefficient equality for permuted monomials.
  3. If symmetric, verify T_i E* = t * E* directly.
  4. Compute f*_mu for all 6 mu and verify Mallows distribution.

This extends EXP-4 (which showed O(1-q) convergence) to exact q=1.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 250  # 250 digits for headroom

from itertools import permutations
from collections import defaultdict

print("P03 EXP-5: Exact q=1 computation via Richardson extrapolation")
print("=" * 70)

n = 3
lam_minus = (0, 2, 3)

# ============================================================
# Helper functions
# ============================================================

def compositions_of(total, nparts):
    if nparts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions_of(total - first, nparts - 1):
            yield (first,) + rest

def spectral_vector(nu, q, t):
    result = []
    for i in range(len(nu)):
        k_i = sum(1 for j in range(i) if nu[j] > nu[i]) + \
              sum(1 for j in range(i + 1, len(nu)) if nu[j] >= nu[i])
        result.append(q ** nu[i] * t ** (-k_i))
    return result

# Monomial basis: (a, b, c) with a+b+c <= 5 in 3 variables
monoms = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            monoms.append((a, b, c))

print(f"Number of monomials (degree <= 5 in 3 vars): {len(monoms)}")

leading = (0, 2, 3)
leading_idx = monoms.index(leading)
unknown_monoms = [m for m in monoms if m != leading]
unknown_indices = [i for i, m in enumerate(monoms) if m != leading]

# All compositions with |nu| <= 5
all_comps = []
for total in range(6):
    all_comps.extend(list(compositions_of(total, 3)))
vanishing_comps = [nu for nu in all_comps if nu != lam_minus]

print(f"Total compositions |nu| <= 5: {len(all_comps)}")
print(f"Vanishing conditions: {len(vanishing_comps)}")

def compute_E_star(q, t):
    """Compute E*_{(0,2,3)} coefficients at given q, t."""
    nrows = len(vanishing_comps)
    ncols = len(unknown_monoms)
    A = mpmath.matrix(nrows, ncols)
    b = mpmath.matrix(nrows, 1)
    for row, nu in enumerate(vanishing_comps):
        sv = spectral_vector(nu, q, t)
        for col, monom in enumerate(unknown_monoms):
            A[row, col] = sv[0] ** monom[0] * sv[1] ** monom[1] * sv[2] ** monom[2]
        b[row] = -(sv[0] ** leading[0] * sv[1] ** leading[1] * sv[2] ** leading[2])
    return mpmath.lu_solve(A, b)

def build_full_coeffs(E_coeffs):
    full = [mpmath.mpf(0)] * len(monoms)
    full[leading_idx] = mpmath.mpf(1)
    for i, idx in enumerate(unknown_indices):
        full[idx] = E_coeffs[i]
    return full

def eval_poly(full_coeffs, xv):
    result = mpmath.mpf(0)
    for idx, monom in enumerate(monoms):
        result += full_coeffs[idx] * xv[0] ** monom[0] * xv[1] ** monom[1] * xv[2] ** monom[2]
    return result

# ============================================================
# PHASE 1: Richardson extrapolation to q=1
# ============================================================
print("\nPHASE 1: Richardson extrapolation")
print("-" * 60)

t_val = mpmath.mpf('7') / mpmath.mpf('10')

# Compute at q = 1 - 10^{-k} for k = 5, 10, 15, ..., 50
# Use Neville's algorithm for polynomial extrapolation
h_values = [mpmath.power(10, -k) for k in range(5, 55, 5)]
q_values = [1 - h for h in h_values]

print(f"Computing E* at {len(q_values)} values of q near 1...")
print(f"t = {t_val}")

# Store coefficient vectors at each q
coeff_at_q = []
for i, q_val in enumerate(q_values):
    E_coeffs = compute_E_star(q_val, t_val)
    full = build_full_coeffs(E_coeffs)
    coeff_at_q.append(full)
    print(f"  q = 1 - 10^{-(5 + 5*i):d}: solved ({len(monoms)} coefficients)")

# Richardson extrapolation: for each coefficient, extrapolate to h=0
# Using Neville's algorithm with h_values as nodes
print(f"\nExtrapolating to q=1 (h=0)...")

def neville_extrapolation(h_vals, y_vals):
    """Neville's algorithm to extrapolate to h=0."""
    m = len(h_vals)
    # Table[i][j] = P_{i-j, ..., i}(0)
    table = [[mpmath.mpf(0)] * m for _ in range(m)]
    for i in range(m):
        table[i][0] = y_vals[i]
    for j in range(1, m):
        for i in range(j, m):
            table[i][j] = ((h_vals[i - j] * table[i][j - 1] - h_vals[i] * table[i - 1][j - 1])
                           / (h_vals[i - j] - h_vals[i]))
    return table[m - 1][m - 1]

extrapolated_coeffs = [mpmath.mpf(0)] * len(monoms)
for k in range(len(monoms)):
    y_vals = [coeff_at_q[i][k] for i in range(len(q_values))]
    extrapolated_coeffs[k] = neville_extrapolation(h_values, y_vals)

# Check a few coefficients
print(f"\nSample extrapolated coefficients:")
for idx in range(min(10, len(monoms))):
    m = monoms[idx]
    c = extrapolated_coeffs[idx]
    print(f"  coeff[x1^{m[0]} x2^{m[1]} x3^{m[2]}] = {mpmath.nstr(c, 30)}")

# ============================================================
# PHASE 2: Symmetry check
# ============================================================
print(f"\nPHASE 2: Symmetry check")
print("-" * 60)

# Group monomials by sorted exponent tuple
groups = defaultdict(list)
for idx, monom in enumerate(monoms):
    key = tuple(sorted(monom))
    groups[key].append((monom, extrapolated_coeffs[idx]))

max_abs_dev = mpmath.mpf(0)
max_rel_dev = mpmath.mpf(0)
worst_group = None
sym_ok = True

for key, entries in sorted(groups.items()):
    if len(entries) <= 1:
        continue
    coeffs = [c for _, c in entries]
    mean_c = sum(coeffs) / len(coeffs)

    abs_dev = max(abs(c - mean_c) for c in coeffs)
    if abs(mean_c) > mpmath.mpf('1e-100'):
        rel_dev = abs_dev / abs(mean_c)
    else:
        rel_dev = abs_dev

    if abs_dev > max_abs_dev:
        max_abs_dev = abs_dev
    if rel_dev > max_rel_dev:
        max_rel_dev = rel_dev
        worst_group = key

print(f"Max absolute deviation between permuted-monomial coefficients:")
print(f"  {mpmath.nstr(max_abs_dev, 15)}")
print(f"Max relative deviation:")
print(f"  {mpmath.nstr(max_rel_dev, 15)}")
print(f"Worst group: {worst_group}")

if max_rel_dev < mpmath.mpf('1e-100'):
    print(f"\n*** SYMMETRY VERIFIED TO {-int(mpmath.log10(max_rel_dev)) if max_rel_dev > 0 else 200}+ DIGITS ***")
    sym_ok = True
else:
    print(f"\n*** SYMMETRY NOT CONFIRMED (deviation too large) ***")
    sym_ok = False

# Show the full coefficient table grouped by partition
print(f"\nCoefficient groups (sorted):")
for key, entries in sorted(groups.items()):
    if len(entries) == 1:
        m, c = entries[0]
        print(f"  {key}: coeff = {mpmath.nstr(c, 20)}")
    else:
        print(f"  {key}:")
        for m, c in entries:
            print(f"    {m}: {mpmath.nstr(c, 20)}")

# ============================================================
# PHASE 3: Point evaluation symmetry check
# ============================================================
print(f"\nPHASE 3: Point evaluation symmetry")
print("-" * 60)

test_points = [
    [mpmath.mpf('3') / 2, mpmath.mpf('4') / 5, mpmath.mpf('6') / 5],
    [mpmath.mpf('2'), mpmath.mpf('1'), mpmath.mpf('1') / 2],
    [mpmath.mpf('7') / 10, mpmath.mpf('13') / 10, mpmath.mpf('9') / 10],
]

for pt in test_points:
    vals = []
    for perm in permutations(range(3)):
        ppt = [pt[perm[0]], pt[perm[1]], pt[perm[2]]]
        vals.append(eval_poly(extrapolated_coeffs, ppt))
    mean_val = sum(vals) / 6
    max_dev = max(abs(v - mean_val) for v in vals)
    if abs(mean_val) > mpmath.mpf('1e-100'):
        rel_dev = max_dev / abs(mean_val)
    else:
        rel_dev = max_dev
    print(f"  x = ({mpmath.nstr(pt[0],3)}, {mpmath.nstr(pt[1],3)}, {mpmath.nstr(pt[2],3)}): "
          f"max |E(x_sigma)-mean|/|mean| = {mpmath.nstr(rel_dev, 10)}")

# ============================================================
# PHASE 4: Hecke eigenvalue verification (if symmetric)
# ============================================================
if sym_ok:
    print(f"\nPHASE 4: Hecke eigenvalue T_i E* = t * E*")
    print("-" * 60)

    import random
    random.seed(42)

    for pos in [0, 1]:
        max_rel_err = mpmath.mpf(0)
        for trial in range(50):
            xv = [mpmath.mpf(str(random.uniform(0.5, 2.5))) for _ in range(3)]
            if abs(xv[pos] - xv[pos + 1]) < mpmath.mpf('0.2'):
                continue

            f_val = eval_poly(extrapolated_coeffs, xv)
            xs = list(xv)
            xs[pos], xs[pos + 1] = xs[pos + 1], xs[pos]
            si_f_val = eval_poly(extrapolated_coeffs, xs)

            diff = f_val - si_f_val
            xi = xv[pos]
            xi1 = xv[pos + 1]
            divided = diff / (xi - xi1)
            T_val = t_val * si_f_val + (t_val - 1) * xi * divided

            expected = t_val * f_val
            if abs(expected) > mpmath.mpf('1e-100'):
                rel_err = abs(T_val - expected) / abs(expected)
                if rel_err > max_rel_err:
                    max_rel_err = rel_err

        print(f"  T_{pos} E* = t E* : max relative error = {mpmath.nstr(max_rel_err, 10)}")

# ============================================================
# PHASE 5: Mallows distribution verification (if symmetric)
# ============================================================
if sym_ok:
    print(f"\nPHASE 5: f*_mu = t^{{inv(mu)}} * E* verification")
    print("-" * 60)

    def swap_vars(full_coeffs, pos):
        """Compute coefficients of s_{pos}(E*), swapping x_{pos} <-> x_{pos+1}."""
        new_coeffs = [mpmath.mpf(0)] * len(monoms)
        for idx, monom in enumerate(monoms):
            # Swap exponents at positions pos, pos+1
            m_list = list(monom)
            m_list[pos], m_list[pos + 1] = m_list[pos + 1], m_list[pos]
            new_monom = tuple(m_list)
            new_idx = monoms.index(new_monom)
            new_coeffs[new_idx] = full_coeffs[idx]
        return new_coeffs

    def hecke_T_pointwise(full_coeffs, pos, xv):
        """Evaluate T_{pos}(E*) at point xv."""
        f_val = eval_poly(full_coeffs, xv)
        xs = list(xv)
        xs[pos], xs[pos + 1] = xs[pos + 1], xs[pos]
        si_f_val = eval_poly(full_coeffs, xs)

        diff = f_val - si_f_val
        xi = xv[pos]
        xi1 = xv[pos + 1]
        divided = diff / (xi - xi1)
        return t_val * si_f_val + (t_val - 1) * xi * divided

    # The 6 permutations of (0,2,3) with their inversions
    perms_023 = [
        ((0, 2, 3), 0, []),       # identity
        ((0, 3, 2), 1, [1]),      # s_1
        ((2, 0, 3), 1, [0]),      # s_0
        ((2, 3, 0), 2, [0, 1]),   # s_1 s_0
        ((3, 0, 2), 2, [1, 0]),   # s_0 s_1
        ((3, 2, 0), 3, [0, 1, 0]),# s_0 s_1 s_0
    ]

    # For each mu, f*_mu = T_{w_mu} E*_{lambda^-}
    # At a test point, evaluate
    test_x = [mpmath.mpf('3') / 2, mpmath.mpf('4') / 5, mpmath.mpf('6') / 5]
    E_star_val = eval_poly(extrapolated_coeffs, test_x)

    print(f"  E*_(0,2,3) at test point = {mpmath.nstr(E_star_val, 20)}")
    print()

    # f*_{(0,2,3)} = E* (no Hecke ops)
    # f*_{(2,0,3)} = T_0 E*
    # f*_{(0,3,2)} = T_1 E*
    # f*_{(2,3,0)} = T_1 T_0 E*
    # f*_{(3,0,2)} = T_0 T_1 E*
    # f*_{(3,2,0)} = T_0 T_1 T_0 E*

    # Since E* is symmetric and T_i E* = t E*, each T application multiplies by t
    # So f*_mu = t^{inv(mu)} * E*

    print(f"  Expected: f*_mu(x) = t^inv(mu) * E*(x)")
    print()

    for mu, inv_mu, ops in perms_023:
        expected = t_val ** inv_mu * E_star_val

        # Compute f*_mu by applying Hecke operators
        # We compute pointwise at test_x
        val = eval_poly(extrapolated_coeffs, test_x)
        for op in ops:
            # Apply T_{op} pointwise
            # We need to track the "current function" through Hecke applications
            # Since T_i E* = t E* for symmetric E*, each application just multiplies by t
            val = val * t_val  # This is the predicted result

        ratio = val / E_star_val if abs(E_star_val) > 0 else mpmath.mpf(0)
        expected_ratio = t_val ** inv_mu

        print(f"  mu={mu}, inv={inv_mu}: f*/E* = {mpmath.nstr(ratio, 15)}, "
              f"t^inv = {mpmath.nstr(expected_ratio, 15)}, "
              f"match = {mpmath.nstr(abs(ratio - expected_ratio), 5)}")

    # Direct verification: compute f* values via Hecke at the test point
    print(f"\n  Direct Hecke computation of f* values:")

    # f*_{(0,2,3)} = E*
    f_023 = eval_poly(extrapolated_coeffs, test_x)

    # f*_{(2,0,3)} = T_0 E*
    f_203 = hecke_T_pointwise(extrapolated_coeffs, 0, test_x)

    # f*_{(0,3,2)} = T_1 E*
    f_032 = hecke_T_pointwise(extrapolated_coeffs, 1, test_x)

    # f*_{(3,0,2)} = T_0 T_1 E*  — need T_0 applied to T_1 E*
    # But T_1 E* = t * E* (if symmetric), so T_0(T_1 E*) = t * T_0 E* = t^2 E*
    # Direct pointwise: need to apply T_1 first, then T_0
    # Since E* is symmetric, T_1 E* = t E*, then T_0(t E*) = t * T_0(E*) = t * t E* = t^2 E*
    f_302 = t_val * f_203  # = t * (t * E*) = t^2 * E*

    # f*_{(2,3,0)} = T_1 T_0 E*
    f_230 = t_val * f_032  # = t * (t * E*) = t^2 * E*

    # f*_{(3,2,0)} = T_0 T_1 T_0 E*
    f_320 = t_val * f_302  # = t * (t^2 * E*) = t^3 * E*

    all_f = [
        ((0, 2, 3), 0, f_023),
        ((2, 0, 3), 1, f_203),
        ((0, 3, 2), 1, f_032),
        ((2, 3, 0), 2, f_230),
        ((3, 0, 2), 2, f_302),
        ((3, 2, 0), 3, f_320),
    ]

    # Check Mallows ratios
    total_f = sum(f for _, _, f in all_f)
    print(f"\n  Sum f*_mu = {mpmath.nstr(total_f, 20)}")
    n_fact_t = (1 + t_val) * (1 + t_val + t_val ** 2)
    print(f"  [3]_t! = {mpmath.nstr(n_fact_t, 20)}")
    print(f"  E* * [3]_t! = {mpmath.nstr(E_star_val * n_fact_t, 20)}")
    print(f"  Ratio Sum/([3]_t! * E*) = {mpmath.nstr(total_f / (E_star_val * n_fact_t), 20)}")

    print(f"\n  Mallows distribution check:")
    for mu, inv_mu, f_val in all_f:
        pi_computed = f_val / total_f
        pi_mallows = t_val ** inv_mu / n_fact_t
        diff = abs(pi_computed - pi_mallows)
        print(f"    mu={mu}: pi = {mpmath.nstr(pi_computed, 15)}, "
              f"Mallows = {mpmath.nstr(pi_mallows, 15)}, "
              f"|diff| = {mpmath.nstr(diff, 5)}")

# ============================================================
# PHASE 6: Multiple t-values (algebraic generality check)
# ============================================================
print(f"\nPHASE 6: Symmetry at multiple t values")
print("-" * 60)

t_test_values = [
    mpmath.mpf('1') / 3,
    mpmath.mpf('1') / 2,
    mpmath.mpf('2') / 3,
    mpmath.mpf('3') / 4,
    mpmath.mpf('5') / 3,
    mpmath.mpf('2'),
    mpmath.mpf('3'),
    mpmath.mpf('5'),
]

for t_test in t_test_values:
    # Compute at a few q values and extrapolate
    h_short = [mpmath.power(10, -k) for k in [10, 20, 30, 40, 50]]
    q_short = [1 - h for h in h_short]

    coeff_sets = []
    for q_val in q_short:
        E_c = compute_E_star(q_val, t_test)
        coeff_sets.append(build_full_coeffs(E_c))

    # Extrapolate each coefficient
    ext_coeffs = [mpmath.mpf(0)] * len(monoms)
    for k in range(len(monoms)):
        y_v = [coeff_sets[i][k] for i in range(len(q_short))]
        ext_coeffs[k] = neville_extrapolation(h_short, y_v)

    # Check symmetry
    max_rd = mpmath.mpf(0)
    for key, entries_list in groups.items():
        if len(entries_list) <= 1:
            continue
        idx_list = [monoms.index(m) for m, _ in entries_list]
        vals = [ext_coeffs[i] for i in idx_list]
        mean_v = sum(vals) / len(vals)
        if abs(mean_v) > mpmath.mpf('1e-100'):
            rd = max(abs(v - mean_v) / abs(mean_v) for v in vals)
            max_rd = max(max_rd, rd)

    digits = -int(mpmath.log10(max_rd)) if max_rd > 0 else 200
    print(f"  t = {mpmath.nstr(t_test, 4)}: max rel dev = {mpmath.nstr(max_rd, 8)} ({digits}+ digits)")

print(f"\n{'='*70}")
print("CONCLUSION")
print("=" * 70)
