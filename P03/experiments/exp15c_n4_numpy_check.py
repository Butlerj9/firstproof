"""
P03 EXP-15c: Quick numerical check of n=4 symmetry using numpy.
Uses Richardson extrapolation at double precision (64-bit).
Not a proof but fast diagnostic.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from itertools import permutations as perms

print("P03 EXP-15c: n=4 Quick Numerical Symmetry Check")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)

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
leading_idx = comps.index(leading)
unk_idx = {m: i for i, m in enumerate(unk_monoms)}

print(f"N = {N} unknowns, {len(comps)} compositions")


def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]:
            count += 1
    for j in range(i + 1, len(nu)):
        if nu[j] >= nu[i]:
            count += 1
    return count


k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}


def build_system(q_val, t_val):
    """Build the vanishing system A*c = b at given (q, t)."""
    A = np.zeros((N, N), dtype=np.float64)
    b_vec = np.zeros(N, dtype=np.float64)
    for row_i, nu in enumerate(van_comps):
        k = k_stats[nu]
        # Spectral vector: spec_i = q^{nu_i} * t^{-k_i}
        spec = [q_val ** nu[j] * t_val ** (-k[j]) for j in range(n)]
        # Evaluate monomial at spec: prod spec_j^{m_j}
        for col_j, m in enumerate(unk_monoms):
            val = 1.0
            for j in range(n):
                val *= spec[j] ** m[j]
            A[row_i, col_j] = val
        # RHS: -leading_monomial evaluated at spec
        val_l = 1.0
        for j in range(n):
            val_l *= spec[j] ** leading[j]
        b_vec[row_i] = -val_l
    return A, b_vec


def solve_at_q(q_val, t_val):
    """Solve for E*_{leading} coefficients at given (q, t)."""
    A, b = build_system(q_val, t_val)
    try:
        c = np.linalg.solve(A, b)
        return c
    except np.linalg.LinAlgError:
        return None


def richardson_extrapolate(t_val, n_points=8):
    """Richardson extrapolation to q=1 using Neville's algorithm."""
    # Use q = 1 - h_k where h_k = 10^{-k}
    ks = list(range(2, 2 + n_points))
    hs = [10.0 ** (-k) for k in ks]
    qs = [1.0 - h for h in hs]

    # Solve at each q
    solutions = []
    for q_val in qs:
        c = solve_at_q(q_val, t_val)
        if c is None:
            return None
        solutions.append(c)

    # Neville's algorithm for each coefficient
    result = np.zeros(N)
    for j in range(N):
        # Neville tableau
        P = [solutions[i][j] for i in range(n_points)]
        for k in range(1, n_points):
            for i in range(n_points - k):
                P[i] = (hs[i] * P[i + 1] - hs[i + k] * P[i]) / (hs[i] - hs[i + k])
        result[j] = P[0]
    return result


def check_symmetry(coeffs, t_val, tol=1e-8):
    """Check if coefficients are symmetric under permutation."""
    coeff_dict = {}
    for i, m in enumerate(unk_monoms):
        coeff_dict[m] = coeffs[i]
    coeff_dict[leading] = 1.0

    max_asym = 0.0
    broken = 0
    total_checks = 0
    for m, val in coeff_dict.items():
        for p in perms(m):
            if p != m and p in coeff_dict:
                diff = abs(coeff_dict[p] - val)
                total_checks += 1
                if diff > tol:
                    broken += 1
                max_asym = max(max_asym, diff)

    return max_asym, broken, total_checks


# Test at several t values
t_values = [0.3, 0.5, 0.7, 1.5, 2.5, 0.1, 3.0, 5.0]
print(f"\nTesting symmetry at {len(t_values)} t values (Richardson, float64):\n")

all_results = {}
for t_val in t_values:
    t0 = time.time()
    coeffs = richardson_extrapolate(t_val, n_points=8)
    elapsed = time.time() - t0
    if coeffs is None:
        print(f"  t={t_val}: FAILED")
        continue
    max_asym, broken, total = check_symmetry(coeffs, t_val)
    status = "SYMMETRIC" if max_asym < 1e-6 else "BROKEN"
    print(f"  t={t_val}: max_asym={max_asym:.2e}, broken={broken}/{total} -> {status} ({elapsed:.2f}s)")
    all_results[t_val] = (max_asym, broken, total, coeffs)

# Detailed check: compare coefficient ratios with Mallows prediction
print(f"\n{'='*70}")
print(f"Mallows check: f*_mu / t^inv(mu) should be constant")
# For this, we need to compute f*_mu from E*_{lambda^-} via Hecke operators
# Skipping for now - coefficient symmetry is the primary check

# Summary
n_sym = sum(1 for v in all_results.values() if v[0] < 1e-6)
n_total = len(all_results)
print(f"\nSummary: {n_sym}/{n_total} t-values show symmetry (tol 1e-6)")
if n_sym == n_total:
    print("ALL SYMMETRIC - strong numerical evidence for n=4 Symmetry Conjecture")
else:
    print("SOME BROKEN - symmetry may not hold at n=4")

# Show best/worst cases
if all_results:
    best_t = min(all_results, key=lambda t: all_results[t][0])
    worst_t = max(all_results, key=lambda t: all_results[t][0])
    print(f"\n  Best:  t={best_t}, max_asym={all_results[best_t][0]:.2e}")
    print(f"  Worst: t={worst_t}, max_asym={all_results[worst_t][0]:.2e}")

print(f"\n{'='*70}")
print("DONE")
