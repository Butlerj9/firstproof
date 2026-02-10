"""
CE-2 + CE-3: Structured stress tests and simplicity preservation check for P04.

CE-2: Tests inequality on adversarial polynomial families:
  - Near-degenerate roots (clustered)
  - Extreme spread (one outlier)
  - Self-convolution (p = q)
  - Chebyshev roots
  - One polynomial with near-multiple root

CE-3: Dedicated simplicity check — tries to find (p,q) where p ⊞_n q has a multiple root
  - Minimizes discriminant of p ⊞_n q
  - Uses scipy.optimize to search for simplicity failures

Seed: 42.
"""

import numpy as np
from math import factorial
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
np.random.seed(42)


def finite_free_conv_coeffs(a, b, n):
    """Compute coefficients of p ⊞_n q."""
    c = np.zeros(n + 1)
    for k in range(n + 1):
        s = 0.0
        for i in range(k + 1):
            j = k - i
            if i <= n and j <= n:
                s += (factorial(n - i) * factorial(n - j)) / (factorial(n) * factorial(n - k)) * a[i] * b[j]
        c[k] = s
    return c


def phi_n(roots):
    """Compute Φ_n(p) from roots. Returns inf if roots are repeated."""
    n = len(roots)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(roots[i] - roots[j]) < 1e-14:
                return np.inf
    total = 0.0
    for i in range(n):
        s = sum(1.0 / (roots[i] - roots[j]) for j in range(n) if j != i)
        total += s ** 2
    return total


def check_ineq(roots_p, roots_q, n, label=""):
    """Check inequality and print result."""
    a = np.poly(roots_p)
    b = np.poly(roots_q)
    c = finite_free_conv_coeffs(a, b, n)
    roots_conv = np.sort(np.real(np.roots(c)))
    max_imag = np.max(np.abs(np.imag(np.roots(c))))

    pp = phi_n(np.sort(roots_p))
    pq = phi_n(np.sort(roots_q))
    pc = phi_n(roots_conv)

    inv_p = 0 if pp == np.inf else 1.0 / pp
    inv_q = 0 if pq == np.inf else 1.0 / pq
    inv_c = 0 if pc == np.inf else 1.0 / pc

    margin = inv_c - (inv_p + inv_q)
    status = "PASS" if margin >= -1e-10 else "FAIL"

    min_gap = min(abs(roots_conv[i+1] - roots_conv[i]) for i in range(n-1)) if n > 1 else np.inf

    print(f"  {label}: margin={margin:.6e}, min_gap={min_gap:.6e}, max|Im|={max_imag:.2e} [{status}]")

    if status == "FAIL":
        print(f"    *** COUNTEREXAMPLE: p_roots={roots_p}, q_roots={roots_q}")
        print(f"    conv_roots={roots_conv}")
        print(f"    Φ(p)={pp:.6e}, Φ(q)={pq:.6e}, Φ(p⊞q)={pc:.6e}")

    return status == "PASS", margin, min_gap


# ============================================================
# CE-2: STRUCTURED STRESS TESTS
# ============================================================
print("=" * 70)
print("CE-2: Structured stress tests")
print("=" * 70)

all_pass = True
all_margins = []

for n in [3, 4, 5, 6]:
    print(f"\n--- n = {n} ---")

    # (A) Near-degenerate roots: roots = (0, ε, 2ε, ..., (n-1)ε)
    for eps in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]:
        roots_p = np.array([i * eps for i in range(n)])
        roots_q = np.array([i * eps + 0.5 for i in range(n)])
        ok, mg, _ = check_ineq(roots_p, roots_q, n, f"clustered ε={eps:.0e}")
        all_pass &= ok
        all_margins.append(mg)

    # (B) Extreme spread: roots = (0, 0.1, 0.2, ..., 0.1*(n-2), M)
    for M in [10, 100, 1000]:
        roots_p = np.array(list(range(n-1)) + [M], dtype=float)
        roots_q = np.array(list(range(n-1)) + [M/2], dtype=float)
        ok, mg, _ = check_ineq(roots_p, roots_q, n, f"spread M={M}")
        all_pass &= ok
        all_margins.append(mg)

    # (C) Self-convolution: p = q
    roots_p = np.sort(np.random.randn(n))
    ok, mg, _ = check_ineq(roots_p, roots_p, n, "self-conv (p=q)")
    all_pass &= ok
    all_margins.append(mg)

    # (D) Chebyshev roots: cos(π(2k-1)/(2n))
    roots_cheb = np.array([np.cos(np.pi * (2*k - 1) / (2*n)) for k in range(1, n+1)])
    roots_q2 = np.sort(np.random.randn(n))
    ok, mg, _ = check_ineq(roots_cheb, roots_q2, n, "Chebyshev × random")
    all_pass &= ok
    all_margins.append(mg)

    # (E) Near-multiple root in p: roots = (0, ε, 1, 2, ..., n-2) for small ε
    for eps in [1e-2, 1e-4, 1e-6, 1e-8]:
        if n >= 3:
            roots_p = np.array([0, eps] + list(range(1, n-1)), dtype=float)
        else:
            roots_p = np.array([0, eps], dtype=float)
        roots_q = np.linspace(-1, 1, n)
        ok, mg, _ = check_ineq(roots_p, roots_q, n, f"near-multiple ε={eps:.0e}")
        all_pass &= ok
        all_margins.append(mg)

    # (F) Both near-degenerate
    for eps in [1e-2, 1e-4, 1e-6]:
        roots_p = np.array([0, eps] + list(range(1, n-1)), dtype=float)
        roots_q = np.array([0, eps/2] + list(range(1, n-1)), dtype=float) + 0.01
        ok, mg, _ = check_ineq(roots_p, roots_q, n, f"both-near-degen ε={eps:.0e}")
        all_pass &= ok
        all_margins.append(mg)

    # (G) Arithmetic progression with different spacings
    for d_p, d_q in [(1, 2), (0.1, 10), (0.01, 100)]:
        roots_p = np.array([i * d_p for i in range(n)])
        roots_q = np.array([i * d_q for i in range(n)])
        ok, mg, _ = check_ineq(roots_p, roots_q, n, f"arith d_p={d_p},d_q={d_q}")
        all_pass &= ok
        all_margins.append(mg)

print(f"\nCE-2 OVERALL: {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
print(f"Min margin across all stress tests: {min(all_margins):.6e}")

# ============================================================
# CE-3: SIMPLICITY PRESERVATION CHECK
# ============================================================
print("\n" + "=" * 70)
print("CE-3: Simplicity preservation check")
print("=" * 70)

print("\nSearching for (p, q) where p ⊞_n q has near-multiple roots...")

min_gaps_found = {}

for n in [3, 4, 5, 6]:
    print(f"\n--- n = {n}: Optimization-based search ---")

    from scipy.optimize import minimize

    def neg_min_gap(params):
        """Objective: minimize the min gap between consecutive roots of p ⊞_n q."""
        roots_p = np.sort(params[:n])
        roots_q = np.sort(params[n:])
        a = np.poly(roots_p)
        b = np.poly(roots_q)
        c = finite_free_conv_coeffs(a, b, n)
        roots_conv = np.sort(np.real(np.roots(c)))
        gaps = [abs(roots_conv[i+1] - roots_conv[i]) for i in range(n-1)]
        return min(gaps)

    best_gap = np.inf
    best_params = None

    # Multiple random starts
    for start in range(200):
        x0 = np.random.randn(2 * n)
        try:
            res = minimize(neg_min_gap, x0, method='Nelder-Mead',
                          options={'maxiter': 2000, 'xatol': 1e-12, 'fatol': 1e-14})
            if res.fun < best_gap:
                best_gap = res.fun
                best_params = res.x
        except Exception:
            continue

    min_gaps_found[n] = best_gap
    print(f"  Best min gap found: {best_gap:.10e}")

    if best_gap < 1e-8:
        roots_p = np.sort(best_params[:n])
        roots_q = np.sort(best_params[n:])
        print(f"  *** NEAR-SIMPLICITY-FAILURE ***")
        print(f"  p roots: {roots_p}")
        print(f"  q roots: {roots_q}")
        # Check the inequality too
        check_ineq(roots_p, roots_q, n, "simplicity-failure candidate")
    else:
        print(f"  No simplicity failure found (gap > 1e-8).")

print("\n" + "=" * 70)
print("CE-3 SUMMARY")
print("=" * 70)
print(f"{'n':>3} | {'Min gap found':>15}")
print("-" * 25)
for n in sorted(min_gaps_found.keys()):
    print(f"{n:>3} | {min_gaps_found[n]:>15.6e}")

simplicity_ok = all(g > 1e-8 for g in min_gaps_found.values())
print(f"\nSimplicity preservation: {'No failures found' if simplicity_ok else 'POTENTIAL FAILURES — investigate'}")

print("\n" + "=" * 70)
print("COMBINED CE-2 + CE-3 VERDICT")
print("=" * 70)
print(f"CE-2 (stress tests): {'PASS' if all_pass else 'FAIL'}")
print(f"CE-3 (simplicity): {'PASS' if simplicity_ok else 'INVESTIGATE'}")
print(f"Overall: {'ALL PASS' if (all_pass and simplicity_ok) else 'ISSUES FOUND'}")
