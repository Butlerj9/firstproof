"""
P04 CE-8: Guided counterexample search for n=4,5.

Strategy:
1. Optimize margin = 1/Phi(h) - 1/Phi(p) - 1/Phi(q) via scipy
2. Any candidate violation certified at 150-digit precision
3. Structured families: clustered roots, near-degenerate discriminant
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from scipy.optimize import minimize, differential_evolution
from fractions import Fraction
from math import factorial

print("P04 CE-8: n=4,5 counterexample search")
print("=" * 60)

def boxplus_coeffs(n, a_coeffs, b_coeffs):
    """Compute c_k for p boxplus_n q."""
    c = [Fraction(0)] * (n + 1)
    for k in range(n + 1):
        for i in range(k + 1):
            j = k - i
            if i > n or j > n:
                continue
            weight = Fraction(factorial(n-i) * factorial(n-j),
                            factorial(n) * factorial(n-k))
            c[k] += weight * a_coeffs[i] * b_coeffs[j]
    return c

def phi_from_roots(roots):
    """Compute Phi_n from roots (numpy)."""
    n = len(roots)
    phi = 0.0
    for i in range(n):
        s = sum(1.0 / (roots[i] - roots[j]) for j in range(n) if j != i)
        phi += s * s
    return phi

def roots_from_coeffs(coeffs):
    """Get roots of monic polynomial with descending coefficients."""
    return np.sort(np.roots(coeffs))

def margin_n4(params):
    """Compute margin for n=4. params = [a2,a3,a4,c2,c3,c4] (centered)."""
    a2, a3, a4, c2, c3, c4 = params
    # p(x) = x^4 + a2*x^2 + a3*x + a4
    p_coeffs = [1.0, 0.0, a2, a3, a4]
    q_coeffs = [1.0, 0.0, c2, c3, c4]

    # boxplus_4 for centered: c_2 = a2+c2, c_3 = a3+c3, c_4 = a4+c4 + (1/6)*a2*c2
    h2 = a2 + c2
    h3 = a3 + c3
    h4 = a4 + c4 + a2 * c2 / 6.0
    h_coeffs = [1.0, 0.0, h2, h3, h4]

    try:
        rp = roots_from_coeffs(p_coeffs)
        rq = roots_from_coeffs(q_coeffs)
        rh = roots_from_coeffs(h_coeffs)

        # Check all real and simple
        if np.any(np.iscomplex(rp)) or np.any(np.iscomplex(rq)) or np.any(np.iscomplex(rh)):
            return 1e10
        rp, rq, rh = np.real(rp), np.real(rq), np.real(rh)

        min_gap_p = np.min(np.diff(np.sort(rp)))
        min_gap_q = np.min(np.diff(np.sort(rq)))
        min_gap_h = np.min(np.diff(np.sort(rh)))
        if min_gap_p < 1e-10 or min_gap_q < 1e-10 or min_gap_h < 1e-10:
            return 1e10

        phi_p = phi_from_roots(rp)
        phi_q = phi_from_roots(rq)
        phi_h = phi_from_roots(rh)

        if phi_p <= 0 or phi_q <= 0 or phi_h <= 0:
            return 1e10

        margin = 1.0/phi_h - 1.0/phi_p - 1.0/phi_q
        return margin
    except Exception:
        return 1e10

# ============================================================
# Phase 1: Scipy local optimization from random starts
# ============================================================
print("\nPhase 1: Local optimization (200 random starts)")
print("-" * 50)

best_margin = 1e10
best_params = None
n_negative = 0

for trial in range(200):
    np.random.seed(8000 + trial)
    x0 = np.random.randn(6) * 2.0
    try:
        result = minimize(margin_n4, x0, method='Nelder-Mead',
                         options={'maxiter': 2000, 'xatol': 1e-12, 'fatol': 1e-14})
        m = result.fun
        if m < best_margin:
            best_margin = m
            best_params = result.x.copy()
            if m < 0:
                n_negative += 1
                print(f"  *** CANDIDATE at trial {trial}: margin = {m:.6e} ***")
                print(f"      params = {result.x}")
    except Exception:
        pass
    if trial % 50 == 49:
        print(f"  After {trial+1} starts: best_margin = {best_margin:.6e}")
        sys.stdout.flush()

print(f"\n  Final best margin: {best_margin:.6e}")
if best_margin < 0:
    print(f"  *** {n_negative} CANDIDATE VIOLATIONS FOUND ***")
else:
    print(f"  No violations found (all margins positive)")

# ============================================================
# Phase 2: Differential evolution (global search)
# ============================================================
print("\nPhase 2: Differential evolution (global)")
print("-" * 50)

bounds = [(-5, 5)] * 6
try:
    result_de = differential_evolution(margin_n4, bounds, seed=42,
                                       maxiter=500, tol=1e-14, popsize=30)
    print(f"  DE best margin: {result_de.fun:.6e}")
    print(f"  DE params: {result_de.x}")
    if result_de.fun < best_margin:
        best_margin = result_de.fun
        best_params = result_de.x.copy()
except Exception as e:
    print(f"  DE failed: {e}")

# ============================================================
# Phase 3: Structured families
# ============================================================
print("\nPhase 3: Structured families (clustered roots)")
print("-" * 50)

# Test with equally-spaced roots shifted by eps
for eps in [1e-2, 1e-3, 1e-4, 1e-6, 1e-8]:
    # p with roots at {-1.5, -0.5+eps, 0.5, 1.5}
    rp = np.array([-1.5, -0.5+eps, 0.5, 1.5])
    rq = np.array([-2.0, -1.0, 0.0+eps, 1.0])
    pp = np.poly(rp)  # monic polynomial
    pq = np.poly(rq)

    # Extract centered coefficients
    # Shift to center: p(x+m) where m = mean(roots)
    mp = np.mean(rp)
    mq = np.mean(rq)
    rp_c = rp - mp
    rq_c = rq - mq
    pp_c = np.poly(rp_c)
    pq_c = np.poly(rq_c)

    a2, a3, a4 = pp_c[2], pp_c[3], pp_c[4]
    c2, c3, c4 = pq_c[2], pq_c[3], pq_c[4]

    m = margin_n4([a2, a3, a4, c2, c3, c4])
    if m < 1e-3:
        print(f"  eps={eps:.0e}: margin = {m:.6e} {'*** CANDIDATE ***' if m < 0 else ''}")

# Test near-degenerate (discriminant → 0)
for trial in range(50):
    np.random.seed(9000 + trial)
    # Start with equally-spaced, perturb slightly
    base = np.sort(np.random.randn(4))
    gaps = np.diff(base)
    min_gap = np.min(gaps)
    # Make one gap very small
    squeeze = np.random.randint(0, 3)
    base[squeeze+1] = base[squeeze] + min_gap * 0.01

    rp = base - np.mean(base)
    rq = np.sort(np.random.randn(4))
    rq = rq - np.mean(rq)

    pp = np.poly(rp)
    pq = np.poly(rq)
    m = margin_n4([pp[2], pp[3], pp[4], pq[2], pq[3], pq[4]])
    if m < 1e-3 and m > -1e10:
        print(f"  Near-degen #{trial}: margin = {m:.6e}")

# ============================================================
# Phase 4: High-precision verification of best candidate
# ============================================================
print(f"\nPhase 4: High-precision verification")
print("-" * 50)

if best_margin < 1e-3:
    print(f"  Best margin = {best_margin:.6e}, verifying at 80 digits...")
    try:
        from mpmath import mp, mpf, polyroots, fsum
        mp.dps = 80

        a2, a3, a4, c2, c3, c4 = [mpf(str(x)) for x in best_params]
        p_coeffs = [mpf(1), mpf(0), a2, a3, a4]
        q_coeffs = [mpf(1), mpf(0), c2, c3, c4]

        h2 = a2 + c2
        h3 = a3 + c3
        h4 = a4 + c4 + a2 * c2 / 6
        h_coeffs = [mpf(1), mpf(0), h2, h3, h4]

        rp = sorted(polyroots(p_coeffs), key=lambda x: float(x.real))
        rq = sorted(polyroots(q_coeffs), key=lambda x: float(x.real))
        rh = sorted(polyroots(h_coeffs), key=lambda x: float(x.real))

        def phi_mp(roots):
            n = len(roots)
            total = mpf(0)
            for i in range(n):
                s = fsum(1/(roots[i] - roots[j]) for j in range(n) if j != i)
                total += s**2
            return total

        phi_p = phi_mp(rp)
        phi_q = phi_mp(rq)
        phi_h = phi_mp(rh)

        margin_hp = 1/phi_h - 1/phi_p - 1/phi_q
        print(f"  80-digit margin = {float(margin_hp):.15e}")
        if margin_hp < 0:
            print(f"  *** CONFIRMED COUNTEREXAMPLE ***")
        else:
            print(f"  False alarm: margin is positive at high precision")
    except ImportError:
        print(f"  mpmath not available for verification")
    except Exception as e:
        print(f"  Verification failed: {e}")
else:
    print(f"  Best margin = {best_margin:.6e} (well above 0)")
    print(f"  No candidate to verify")

# ============================================================
# Phase 5: n=5 quick search
# ============================================================
print(f"\nPhase 5: n=5 quick search (50 local starts)")
print("-" * 50)

def margin_n5(params):
    """Margin for n=5. params = [a2,a3,a4,a5,c2,c3,c4,c5] (centered)."""
    a2, a3, a4, a5, c2, c3, c4, c5 = params
    p_coeffs = [1.0, 0.0, a2, a3, a4, a5]
    q_coeffs = [1.0, 0.0, c2, c3, c4, c5]

    # boxplus_5 for centered
    h = [Fraction(0)] * 6
    a_frac = [Fraction(1), Fraction(0)] + [Fraction(x).limit_denominator(10**10) for x in [a2,a3,a4,a5]]
    b_frac = [Fraction(1), Fraction(0)] + [Fraction(x).limit_denominator(10**10) for x in [c2,c3,c4,c5]]
    try:
        h_frac = boxplus_coeffs(5, a_frac, b_frac)
        h_coeffs = [float(x) for x in h_frac]
    except Exception:
        return 1e10

    try:
        rp = roots_from_coeffs(p_coeffs)
        rq = roots_from_coeffs(q_coeffs)
        rh = roots_from_coeffs(h_coeffs)

        if np.any(np.iscomplex(rp)) or np.any(np.iscomplex(rq)) or np.any(np.iscomplex(rh)):
            return 1e10
        rp, rq, rh = np.real(rp), np.real(rq), np.real(rh)

        min_gap_p = np.min(np.diff(np.sort(rp)))
        min_gap_q = np.min(np.diff(np.sort(rq)))
        min_gap_h = np.min(np.diff(np.sort(rh)))
        if min_gap_p < 1e-10 or min_gap_q < 1e-10 or min_gap_h < 1e-10:
            return 1e10

        phi_p = phi_from_roots(rp)
        phi_q = phi_from_roots(rq)
        phi_h = phi_from_roots(rh)

        if phi_p <= 0 or phi_q <= 0 or phi_h <= 0:
            return 1e10

        return 1.0/phi_h - 1.0/phi_p - 1.0/phi_q
    except Exception:
        return 1e10

best_n5 = 1e10
for trial in range(50):
    np.random.seed(10000 + trial)
    x0 = np.random.randn(8) * 1.5
    try:
        result = minimize(margin_n5, x0, method='Nelder-Mead',
                         options={'maxiter': 1000, 'xatol': 1e-10, 'fatol': 1e-12})
        if result.fun < best_n5:
            best_n5 = result.fun
            if result.fun < 0:
                print(f"  *** n=5 CANDIDATE at trial {trial}: margin = {result.fun:.6e} ***")
    except Exception:
        pass
    if trial % 25 == 24:
        print(f"  After {trial+1}: best_n5 = {best_n5:.6e}")

print(f"  n=5 best margin: {best_n5:.6e}")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*60}")
print("SUMMARY")
print(f"  n=4 best margin: {best_margin:.6e} ({'VIOLATION' if best_margin < 0 else 'NO VIOLATION'})")
print(f"  n=5 best margin: {best_n5:.6e} ({'VIOLATION' if best_n5 < 0 else 'NO VIOLATION'})")
print("DONE")
