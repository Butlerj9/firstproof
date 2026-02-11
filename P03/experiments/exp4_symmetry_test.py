"""
P03 EXP-4: Test whether E*_{lambda^-}(q=1) is a symmetric polynomial.

KEY INSIGHT: If E*_{(0,2,3)}(q=1) is symmetric in (x1,x2,x3), then:
- s_i(E*) = E* for all i
- T_i(E*) = t * s_i(E*) + (t-1)*x_i/(x_i-x_{i+1}) * (E* - s_i(E*)) = t*E* + 0 = t*E*
- So T_i E* = t * E* (Hecke eigenvalue)
- Then f*_mu = T_{sigma_mu} E* = t^{inv(mu)} * E*
- And pi(mu) = t^{inv(mu)} / [n]_t! (Mallows distribution)

This would PROVE the Hecke eigenvalue claim for n=3 (conditional on the q->1 limit).

For n=2: E*_{(0,2)}(q=1) = (y1+y2-1-1/t)^2 IS symmetric. Verified.
For n=3: TEST whether E*_{(0,2,3)}(q~1) is approximately symmetric.

Two tests:
1. COEFFICIENT SYMMETRY: Check if coefficients of permuted monomials are equal.
2. POINT EVALUATION SYMMETRY: Check if E*(x1,x2,x3) = E*(x_sigma(1),x_sigma(2),x_sigma(3)).
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 80

import random
random.seed(42)

print("P03 EXP-4: Symmetry test for E*_{(0,2,3)}(q->1)")
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

def spectral_vector(nu, q, t):
    result = []
    for i in range(len(nu)):
        k_i = sum(1 for j in range(i) if nu[j] > nu[i]) + \
              sum(1 for j in range(i+1, len(nu)) if nu[j] >= nu[i])
        result.append(q**nu[i] * t**(-k_i))
    return result

# Monomial basis (total degree <= 5 in 3 variables)
monoms = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            monoms.append((a, b, c))

leading = (0, 2, 3)
leading_idx = monoms.index(leading)
unknown_monoms = [m for m in monoms if m != leading]
unknown_indices = [i for i, m in enumerate(monoms) if m != leading]

# Vanishing compositions
all_comps_le5 = []
for total in range(6):
    all_comps_le5.extend(list(compositions_of(total, 3)))
vanishing_comps = [nu for nu in all_comps_le5 if nu != lam_minus]

def compute_E_star(q, t):
    nrows = len(vanishing_comps)
    ncols = len(unknown_monoms)
    A = mpmath.matrix(nrows, ncols)
    b = mpmath.matrix(nrows, 1)
    for row, nu in enumerate(vanishing_comps):
        sv = spectral_vector(nu, q, t)
        for col, monom in enumerate(unknown_monoms):
            A[row, col] = sv[0]**monom[0] * sv[1]**monom[1] * sv[2]**monom[2]
        b[row] = -(sv[0]**leading[0] * sv[1]**leading[1] * sv[2]**leading[2])
    return mpmath.lu_solve(A, b)

def build_full_coeffs(E_coeffs):
    full = [mpmath.mpf(0)] * len(monoms)
    full[leading_idx] = mpmath.mpf(1)
    for i, idx in enumerate(unknown_indices):
        full[idx] = E_coeffs[i]
    return full

def eval_full(full_coeffs, xv):
    result = mpmath.mpf(0)
    for idx, monom in enumerate(monoms):
        result += full_coeffs[idx] * xv[0]**monom[0] * xv[1]**monom[1] * xv[2]**monom[2]
    return result

# ============================================================
# TEST 1: COEFFICIENT SYMMETRY
# ============================================================
print("\nTEST 1: Coefficient symmetry of E*_{(0,2,3)}")
print("-" * 60)

from itertools import permutations

t_val = mpmath.mpf('0.7')  # A generic t value

for q_label, q_val in [('0.99', mpmath.mpf('0.99')),
                         ('0.999', mpmath.mpf('0.999')),
                         ('0.9999', mpmath.mpf('0.9999')),
                         ('0.99999', mpmath.mpf('0.99999'))]:
    E_coeffs = compute_E_star(q_val, t_val)
    full_E = build_full_coeffs(E_coeffs)

    # Group monomials by their sorted exponent tuple (= partition)
    from collections import defaultdict
    groups = defaultdict(list)
    for idx, monom in enumerate(monoms):
        key = tuple(sorted(monom))
        groups[key].append((monom, float(full_E[idx])))

    # Check if coefficients in each group are approximately equal
    max_rel_dev = 0.0
    worst_group = None
    for key, entries in sorted(groups.items()):
        if len(entries) <= 1:
            continue
        coeffs = [c for _, c in entries]
        mean_c = sum(coeffs) / len(coeffs)
        if abs(mean_c) < 1e-20:
            continue
        rel_dev = max(abs(c - mean_c) / abs(mean_c) for c in coeffs)
        if rel_dev > max_rel_dev:
            max_rel_dev = rel_dev
            worst_group = (key, entries)

    print(f"  q={q_label}: max relative deviation within monomial groups = {max_rel_dev:.3e}")
    if worst_group and max_rel_dev > 1e-8:
        key, entries = worst_group
        print(f"    Worst group {key}: {[(m, f'{c:.6f}') for m, c in entries]}")

# ============================================================
# TEST 2: POINT EVALUATION SYMMETRY
# ============================================================
print(f"\nTEST 2: Point evaluation symmetry of E*_{{(0,2,3)}}")
print("-" * 60)

for q_label, q_val in [('0.99', mpmath.mpf('0.99')),
                         ('0.999', mpmath.mpf('0.999')),
                         ('0.9999', mpmath.mpf('0.9999')),
                         ('0.99999', mpmath.mpf('0.99999'))]:
    E_coeffs = compute_E_star(q_val, t_val)
    full_E = build_full_coeffs(E_coeffs)

    # Test at several points
    test_points = [
        [mpmath.mpf('1.5'), mpmath.mpf('0.8'), mpmath.mpf('1.2')],
        [mpmath.mpf('2.0'), mpmath.mpf('1.0'), mpmath.mpf('0.5')],
        [mpmath.mpf('0.7'), mpmath.mpf('1.3'), mpmath.mpf('0.9')],
    ]

    max_dev = 0.0
    for pt in test_points:
        # Evaluate at all 6 permutations
        vals = []
        for perm in permutations(range(3)):
            ppt = [pt[perm[0]], pt[perm[1]], pt[perm[2]]]
            vals.append(eval_full(full_E, ppt))
        mean_val = sum(vals) / 6
        if abs(mean_val) > 1e-20:
            rel_dev = max(abs(v - mean_val) / abs(mean_val) for v in vals)
            max_dev = max(max_dev, rel_dev)

    print(f"  q={q_label}: max relative deviation across permutations = {float(max_dev):.3e}")

# ============================================================
# TEST 3: Convergence rate of symmetry deviation
# ============================================================
print(f"\nTEST 3: Convergence rate of symmetry deviation")
print("-" * 60)
print("  If deviation ~ O(1-q), the q=1 limit should be exactly symmetric.")

pt = [mpmath.mpf('1.5'), mpmath.mpf('0.8'), mpmath.mpf('1.2')]
for q_label, q_val in [('0.9', mpmath.mpf('0.9')),
                         ('0.99', mpmath.mpf('0.99')),
                         ('0.999', mpmath.mpf('0.999')),
                         ('0.9999', mpmath.mpf('0.9999')),
                         ('0.99999', mpmath.mpf('0.99999'))]:
    E_coeffs = compute_E_star(q_val, t_val)
    full_E = build_full_coeffs(E_coeffs)

    vals = []
    for perm in permutations(range(3)):
        ppt = [pt[perm[0]], pt[perm[1]], pt[perm[2]]]
        vals.append(eval_full(full_E, ppt))
    mean_val = sum(vals) / 6
    max_dev = max(abs(v - mean_val) for v in vals)
    print(f"  q={q_label}: max |E*(x_sigma) - mean| = {float(max_dev):.6e}  (1-q = {float(1-q_val):.1e})")

# ============================================================
# TEST 4: Direct Hecke eigenvalue verification
# ============================================================
print(f"\nTEST 4: Direct Hecke eigenvalue verification T_i E* = t E*")
print("-" * 60)

q_val = mpmath.mpf('0.9999')
E_coeffs = compute_E_star(q_val, t_val)
full_E = build_full_coeffs(E_coeffs)

# Check at several points: T_i(E*)(x) vs t*E*(x)
for pos in [0, 1]:
    max_rel_err = 0.0
    for _ in range(20):
        xv = [mpmath.mpf(random.uniform(0.5, 2.5)) for _ in range(3)]
        if abs(xv[pos] - xv[pos+1]) < 0.2:
            continue

        f_val = eval_full(full_E, xv)
        xs = list(xv)
        xs[pos], xs[pos+1] = xs[pos+1], xs[pos]
        si_f_val = eval_full(full_E, xs)

        diff = f_val - si_f_val
        xi = xv[pos]
        xi1 = xv[pos+1]
        divided = diff / (xi - xi1)
        T_val = t_val * si_f_val + (t_val - 1) * xi * divided

        expected = t_val * f_val
        if abs(expected) > 1e-20:
            rel_err = abs(T_val - expected) / abs(expected)
            max_rel_err = max(max_rel_err, rel_err)

    print(f"  T_{pos} E* = t E* : max relative error = {float(max_rel_err):.3e}")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("""
If E*_{lambda^-}(q=1) is symmetric, then:
  T_i E* = t * s_i(E*) + (t-1)*x_i/(x_i-x_{i+1})*(E*-s_i(E*))
         = t * E*     + 0  [since s_i(E*) = E* for symmetric E*]
         = t * E*

This proves the Hecke eigenvalue claim and hence f*_mu(q=1) = C*t^{inv(mu)}.

The conjecture reduces to: E*_{lambda^-}(q=1) is a symmetric polynomial.
For n=2: PROVED (C = (y1+y2-1-1/t)^2 is a perfect square of a symmetric function).
For n=3: NUMERICAL EVIDENCE above.
""")
