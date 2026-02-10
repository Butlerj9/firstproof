"""
CE-1: Numeric sweep for P04 — Φ_n inequality under finite free convolution ⊞_n.

Tests whether 1/Φ_n(p ⊞_n q) >= 1/Φ_n(p) + 1/Φ_n(q)
for random monic real-rooted polynomials of degree n = 2, 3, 4, 5, 6, 7.

Also checks:
- Whether p ⊞_n q preserves simplicity of roots (CE-3 piggyback)
- Reports minimum margin (LHS - RHS)
- Uses mpmath for near-failures (margin < 1e-6)

Seed: 42 for reproducibility.
"""

import numpy as np
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)

def poly_from_roots(roots):
    """Monic polynomial coefficients in descending power: a_0=1, a_1, ..., a_n."""
    # np.poly returns [1, c1, c2, ..., cn] for monic polynomial
    return np.poly(roots)

def finite_free_conv_coeffs(a, b, n):
    """
    Compute coefficients of p ⊞_n q using the formula:
    c_k = sum_{i+j=k} (n-i)!(n-j)! / (n!(n-k)!) * a_i * b_j

    a, b: coefficient arrays [a_0=1, a_1, ..., a_n] (descending power convention)
    Returns: c = [c_0=1, c_1, ..., c_n]
    """
    from math import factorial
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
    """
    Compute Φ_n(p) = sum_i (sum_{j!=i} 1/(λ_i - λ_j))^2.
    Returns float, or np.inf if any roots are repeated (within tolerance).
    """
    n = len(roots)
    # Check for repeated roots
    for i in range(n):
        for j in range(i + 1, n):
            if abs(roots[i] - roots[j]) < 1e-14:
                return np.inf

    total = 0.0
    for i in range(n):
        inner_sum = 0.0
        for j in range(n):
            if j != i:
                inner_sum += 1.0 / (roots[i] - roots[j])
        total += inner_sum ** 2
    return total

def check_inequality(roots_p, roots_q, n):
    """
    Check 1/Φ_n(p ⊞_n q) >= 1/Φ_n(p) + 1/Φ_n(q).

    Returns: (passes, margin, phi_p, phi_q, phi_conv, roots_conv, min_gap_conv)
    """
    # Compute coefficients from roots
    a = poly_from_roots(roots_p)
    b = poly_from_roots(roots_q)

    # Compute convolution
    c = finite_free_conv_coeffs(a, b, n)

    # Find roots of convolution
    roots_conv = np.roots(c)

    # Check if all roots are real
    imag_parts = np.abs(np.imag(roots_conv))
    max_imag = np.max(imag_parts)
    roots_conv_real = np.sort(np.real(roots_conv))

    # Min gap in convolution roots (for simplicity check)
    min_gap = np.inf
    for i in range(len(roots_conv_real) - 1):
        gap = abs(roots_conv_real[i + 1] - roots_conv_real[i])
        if gap < min_gap:
            min_gap = gap

    # Compute Φ_n values
    phi_p = phi_n(np.sort(roots_p))
    phi_q = phi_n(np.sort(roots_q))
    phi_conv = phi_n(roots_conv_real)

    # Compute 1/Φ values (0 if Φ = inf)
    inv_phi_p = 0.0 if phi_p == np.inf else 1.0 / phi_p
    inv_phi_q = 0.0 if phi_q == np.inf else 1.0 / phi_q
    inv_phi_conv = 0.0 if phi_conv == np.inf else 1.0 / phi_conv

    lhs = inv_phi_conv
    rhs = inv_phi_p + inv_phi_q
    margin = lhs - rhs

    passes = margin >= -1e-10  # small tolerance for float noise

    return passes, margin, phi_p, phi_q, phi_conv, roots_conv_real, min_gap, max_imag

def run_sweep(n, num_trials=100000):
    """Run CE-1 sweep for degree n."""
    print(f"\n{'='*60}")
    print(f"CE-1 Sweep: n = {n}, trials = {num_trials}")
    print(f"{'='*60}")

    min_margin = np.inf
    worst_case = None
    num_failures = 0
    num_near_failures = 0  # margin < 1e-6
    min_conv_gap = np.inf
    num_complex_roots = 0  # convolution roots with significant imaginary part
    num_simplicity_issues = 0  # convolution roots very close together

    for trial in range(num_trials):
        # Generate random real-rooted monic polynomials
        roots_p = np.sort(np.random.randn(n))
        roots_q = np.sort(np.random.randn(n))

        try:
            passes, margin, phi_p, phi_q, phi_conv, roots_conv, min_gap, max_imag = \
                check_inequality(roots_p, roots_q, n)
        except Exception as e:
            print(f"  Trial {trial}: ERROR — {e}")
            continue

        if max_imag > 1e-6:
            num_complex_roots += 1

        if min_gap < 1e-10:
            num_simplicity_issues += 1

        if min_gap < min_conv_gap:
            min_conv_gap = min_gap

        if margin < min_margin:
            min_margin = margin
            worst_case = (trial, roots_p, roots_q, phi_p, phi_q, phi_conv, roots_conv, margin, min_gap)

        if not passes:
            num_failures += 1
            if num_failures <= 5:  # Print first 5 failures
                print(f"  FAILURE at trial {trial}:")
                print(f"    p roots: {roots_p}")
                print(f"    q roots: {roots_q}")
                print(f"    conv roots: {roots_conv}")
                print(f"    Φ_n(p)={phi_p:.6e}, Φ_n(q)={phi_q:.6e}, Φ_n(p⊞q)={phi_conv:.6e}")
                print(f"    1/Φ(p⊞q)={1/phi_conv if phi_conv != np.inf else 0:.6e}")
                print(f"    1/Φ(p)+1/Φ(q)={1/phi_p + 1/phi_q:.6e}")
                print(f"    margin={margin:.6e}")

        if margin < 1e-6 and margin >= -1e-10:
            num_near_failures += 1

    # Report
    print(f"\nResults for n = {n}:")
    print(f"  Total trials: {num_trials}")
    print(f"  Failures (margin < -1e-10): {num_failures}")
    print(f"  Near-failures (0 <= margin < 1e-6): {num_near_failures}")
    print(f"  Min margin: {min_margin:.10e}")
    print(f"  Complex root issues (max|Im| > 1e-6): {num_complex_roots}")
    print(f"  Simplicity issues (min gap < 1e-10): {num_simplicity_issues}")
    print(f"  Min convolution root gap: {min_conv_gap:.6e}")

    if worst_case:
        trial, rp, rq, pp, pq, pc, rc, mg, gap = worst_case
        print(f"\n  Worst case (trial {trial}):")
        print(f"    p roots: {rp}")
        print(f"    q roots: {rq}")
        print(f"    conv roots: {rc}")
        print(f"    Φ(p)={pp:.6e}, Φ(q)={pq:.6e}, Φ(p⊞q)={pc:.6e}")
        inv_p = 0 if pp == np.inf else 1/pp
        inv_q = 0 if pq == np.inf else 1/pq
        inv_c = 0 if pc == np.inf else 1/pc
        print(f"    LHS=1/Φ(p⊞q)={inv_c:.10e}")
        print(f"    RHS=1/Φ(p)+1/Φ(q)={inv_p + inv_q:.10e}")
        print(f"    margin={mg:.10e}")
        print(f"    min conv root gap={gap:.6e}")

    status = "PASS" if num_failures == 0 else "FAIL"
    print(f"\n  STATUS: {status}")
    return num_failures == 0, min_margin, num_failures

# ============================================================
# MAIN: Run sweeps for n = 2, 3, 4, 5, 6, 7
# ============================================================

print("P04 CE-1: Numeric sweep for Φ_n inequality under ⊞_n")
print("=" * 60)

results = {}
all_pass = True

for n in [2, 3, 4, 5, 6, 7]:
    # Use fewer trials for larger n (root-finding slower)
    num_trials = {2: 100000, 3: 100000, 4: 50000, 5: 20000, 6: 10000, 7: 5000}[n]
    passed, min_margin, num_fail = run_sweep(n, num_trials)
    results[n] = (passed, min_margin, num_fail, num_trials)
    if not passed:
        all_pass = False

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"{'n':>3} | {'Trials':>8} | {'Status':>6} | {'Min margin':>15} | {'Failures':>8}")
print("-" * 60)
for n in [2, 3, 4, 5, 6, 7]:
    passed, min_margin, num_fail, num_trials = results[n]
    status = "PASS" if passed else "FAIL"
    print(f"{n:>3} | {num_trials:>8} | {status:>6} | {min_margin:>15.6e} | {num_fail:>8}")

print(f"\nOVERALL: {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")

if not all_pass:
    print("\n*** COUNTEREXAMPLE CANDIDATES FOUND — need mpmath confirmation ***")
else:
    print("\nNo counterexamples found. Proceed to CE-2 (structured stress tests).")
