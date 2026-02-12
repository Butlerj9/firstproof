"""
P04 CE-9: Intensive n=4 counterexample search for the finite free Fisher inequality.

Goal: Find p, q monic real-rooted degree-4 polynomials such that
    1/Phi_4(p box_4 q) < 1/Phi_4(p) + 1/Phi_4(q)

Strategy:
  Phase 1: Large random search (100K samples) at double precision, flag candidates
  Phase 2: Targeted search in clustered-root regimes (near-degenerate discriminant)
  Phase 3: Parametric families designed to maximize the cross-term effect
  Phase 4: scipy optimization to minimize margin
  Phase 5: High-precision (80-digit) verification of ALL candidates with margin < 1e-4
  Phase 6: If confirmed CE found, verify at 200+ digits

Key insight from CE-7: the cross-term (1/6)*a2*b2 in c4 is the obstruction.
We focus on regimes where this cross-term most distorts the inequality.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from math import factorial
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')

print("P04 CE-9: Intensive n=4 counterexample search")
print("=" * 70)

# ============================================================
# Core functions (double precision for speed)
# ============================================================

def boxplus4_centered(a2, a3, a4, b2, b3, b4):
    """Compute box_4 for centered quartics (a1=b1=0).
    c_2 = a2+b2, c_3 = a3+b3, c_4 = a4+b4+(1/6)*a2*b2
    """
    return (a2+b2, a3+b3, a4+b4+a2*b2/6.0)

def phi_from_roots_np(roots):
    """Compute Phi_n from roots (numpy). Returns inf if near-degenerate."""
    n = len(roots)
    roots = np.sort(np.real(roots))
    min_gap = np.min(np.diff(roots))
    if min_gap < 1e-12:
        return np.inf
    total = 0.0
    for i in range(n):
        s = 0.0
        for j in range(n):
            if j != i:
                s += 1.0 / (roots[i] - roots[j])
        total += s * s
    return total

def margin_from_roots(rp, rq, n=4):
    """Compute margin from root arrays. Uses exact boxplus formula."""
    # Build coefficients from roots
    pp = np.poly(rp)  # monic, descending
    pq = np.poly(rq)

    # boxplus_n
    c = np.zeros(n+1)
    for k in range(n+1):
        for i in range(k+1):
            j = k - i
            if i <= n and j <= n:
                w = factorial(n-i) * factorial(n-j) / (factorial(n) * factorial(n-k))
                c[k] += w * pp[i] * pq[j]

    rh = np.sort(np.roots(c))
    if np.any(np.abs(np.imag(rh)) > 1e-8):
        return 1e10  # complex roots
    rh = np.real(rh)

    phi_p = phi_from_roots_np(rp)
    phi_q = phi_from_roots_np(rq)
    phi_h = phi_from_roots_np(rh)

    if phi_p <= 0 or phi_q <= 0 or phi_h <= 0:
        return 1e10
    if np.isinf(phi_p) or np.isinf(phi_q) or np.isinf(phi_h):
        return 1e10

    return 1.0/phi_h - 1.0/phi_p - 1.0/phi_q

def margin_centered_coeffs(a2, a3, a4, b2, b3, b4):
    """Compute margin from centered quartic coefficients."""
    p_coeffs = np.array([1.0, 0.0, a2, a3, a4])
    q_coeffs = np.array([1.0, 0.0, b2, b3, b4])
    h2, h3, h4 = boxplus4_centered(a2, a3, a4, b2, b3, b4)
    h_coeffs = np.array([1.0, 0.0, h2, h3, h4])

    try:
        rp = np.sort(np.roots(p_coeffs))
        rq = np.sort(np.roots(q_coeffs))
        rh = np.sort(np.roots(h_coeffs))

        if np.any(np.abs(np.imag(rp)) > 1e-8): return 1e10
        if np.any(np.abs(np.imag(rq)) > 1e-8): return 1e10
        if np.any(np.abs(np.imag(rh)) > 1e-8): return 1e10

        rp, rq, rh = np.real(rp), np.real(rq), np.real(rh)

        phi_p = phi_from_roots_np(rp)
        phi_q = phi_from_roots_np(rq)
        phi_h = phi_from_roots_np(rh)

        if phi_p <= 0 or phi_q <= 0 or phi_h <= 0: return 1e10
        if np.isinf(phi_p) or np.isinf(phi_q) or np.isinf(phi_h): return 1e10

        return 1.0/phi_h - 1.0/phi_p - 1.0/phi_q
    except:
        return 1e10

# ============================================================
# Phase 1: Massive random search (root-based sampling)
# ============================================================
print("\nPhase 1: Random root-based search (200K samples)")
print("-" * 60)

candidates = []
np.random.seed(12345)

t0 = time.time()
N_PHASE1 = 200000
min_margin_p1 = 1e10
min_margin_config = None

for trial in range(N_PHASE1):
    # Sample roots directly for guaranteed real-rootedness
    rp = np.sort(np.random.randn(4) * 2.0)
    rq = np.sort(np.random.randn(4) * 2.0)

    m = margin_from_roots(rp, rq, 4)
    if m < min_margin_p1:
        min_margin_p1 = m
        min_margin_config = (rp.copy(), rq.copy())
    if m < 1e-4 and m > -1e10:
        candidates.append((m, rp.copy(), rq.copy()))

    if (trial+1) % 50000 == 0:
        elapsed = time.time() - t0
        print(f"  {trial+1}/{N_PHASE1}: min_margin = {min_margin_p1:.8e}, "
              f"candidates (margin<1e-4) = {len(candidates)}, "
              f"elapsed = {elapsed:.1f}s")

print(f"  Phase 1 done: min_margin = {min_margin_p1:.8e}, "
      f"#candidates = {len(candidates)}")

# ============================================================
# Phase 2: Clustered-root regimes
# ============================================================
print("\nPhase 2: Clustered-root regimes (50K samples)")
print("-" * 60)

min_margin_p2 = 1e10
N_PHASE2 = 50000

for trial in range(N_PHASE2):
    # Strategy: create polynomials with 2 tight clusters
    eps = 10**(-np.random.uniform(1, 8))
    strategy = trial % 5

    if strategy == 0:
        # Two pairs of near-coincident roots
        c1 = np.random.randn() * 2
        c2 = np.random.randn() * 2
        rp = np.sort([c1 - eps, c1 + eps, c2 - eps*0.5, c2 + eps*0.5])
        rq = np.sort(np.random.randn(4) * 2)
    elif strategy == 1:
        # Three clustered, one far
        c = np.random.randn()
        rp = np.sort([c - eps, c, c + eps, c + np.random.uniform(1, 5)])
        rq = np.sort([c - eps*2, c - eps, c + eps, c + np.random.uniform(1, 5)])
    elif strategy == 2:
        # Both polynomials with clusters but different patterns
        c1, c2 = np.random.randn(2)
        rp = np.sort([c1 - eps, c1 + eps, c1 + 2*eps, c1 + 3*eps])
        d = np.random.uniform(0.5, 3)
        rq = np.sort([c2, c2 + d, c2 + 2*d, c2 + 3*d])
    elif strategy == 3:
        # Large a2*b2 product: both with large spread but skewed
        spread = np.random.uniform(3, 10)
        rp = np.sort([-spread, -eps, eps, spread * 0.5])
        rq = np.sort([-spread * 0.7, -eps*2, eps*3, spread])
    else:
        # Near-degenerate: one root pair very close
        base = np.sort(np.random.randn(4) * 2)
        idx = np.random.randint(0, 3)
        base[idx+1] = base[idx] + eps
        rp = base
        rq = np.sort(np.random.randn(4) * 2)

    rp = np.sort(np.array(rp, dtype=float))
    rq = np.sort(np.array(rq, dtype=float))

    m = margin_from_roots(rp, rq, 4)
    if m < min_margin_p2:
        min_margin_p2 = m
    if m < 1e-4 and m > -1e10:
        candidates.append((m, rp.copy(), rq.copy()))

    if (trial+1) % 10000 == 0:
        print(f"  {trial+1}/{N_PHASE2}: min_margin = {min_margin_p2:.8e}, "
              f"total candidates = {len(candidates)}")

print(f"  Phase 2 done: min_margin = {min_margin_p2:.8e}")

# ============================================================
# Phase 3: Parametric families maximizing cross-term effect
# ============================================================
print("\nPhase 3: Parametric families (cross-term focus)")
print("-" * 60)

min_margin_p3 = 1e10

# The cross-term is (1/6)*a2*b2 in c4.
# Large |a2*b2| means large cross-term.
# a2 = sum_{i<j} lambda_i*lambda_j for centered polynomial.
# For centered quartic with roots {-a, -b, b, a}, a2 = -(a^2+b^2)+b*a-b*a = -(a^2+b^2)
# Actually a2 = e2(roots). For {-a,-b,b,a}: e2 = ab-ab-a^2+ab-ab-b^2 = -(a^2+b^2)

for trial in range(20000):
    # Family 1: symmetric roots {-a, -b, b, a}
    if trial % 4 == 0:
        a, b = np.random.uniform(0.1, 5, 2)
        rp = np.sort([-a, -b, b, a])
        c, d = np.random.uniform(0.1, 5, 2)
        rq = np.sort([-c, -d, d, c])
    # Family 2: asymmetric with large a2
    elif trial % 4 == 1:
        s = np.random.uniform(1, 10)
        e = np.random.uniform(0.01, 0.5)
        rp = np.sort([-s, -e, e, s])
        t = np.random.uniform(1, 10)
        f = np.random.uniform(0.01, 0.5)
        rq = np.sort([-t, -f, f, t])
    # Family 3: one polynomial tight, one spread
    elif trial % 4 == 2:
        eps = 10**(-np.random.uniform(0, 4))
        rp = np.sort([-eps, 0, eps, 2*eps])
        rp = rp - np.mean(rp)
        s = np.random.uniform(2, 10)
        rq = np.sort([-s, -1, 1, s])
    # Family 4: both with same-sign a2 (maximize product)
    else:
        # a2 < 0 for real roots typically
        rp = np.sort(np.random.uniform(-5, 5, 4))
        rp = rp - np.mean(rp)
        rq = np.sort(np.random.uniform(-5, 5, 4))
        rq = rq - np.mean(rq)

    m = margin_from_roots(rp, rq, 4)
    if m < min_margin_p3:
        min_margin_p3 = m
    if m < 1e-4 and m > -1e10:
        candidates.append((m, rp.copy(), rq.copy()))

print(f"  Phase 3 done: min_margin = {min_margin_p3:.8e}")

# ============================================================
# Phase 4: Scipy optimization (aggressive)
# ============================================================
print("\nPhase 4: Scipy optimization (500 starts + DE)")
print("-" * 60)

def objective(params):
    """Minimize margin over root space."""
    rp = np.sort(params[:4])
    rq = np.sort(params[4:])
    return margin_from_roots(rp, rq, 4)

min_margin_p4 = 1e10
best_params_p4 = None

# Local optimization from random starts
for trial in range(500):
    np.random.seed(20000 + trial)
    x0 = np.random.randn(8) * 2.0
    try:
        result = minimize(objective, x0, method='Nelder-Mead',
                         options={'maxiter': 5000, 'xatol': 1e-14, 'fatol': 1e-16})
        if result.fun < min_margin_p4:
            min_margin_p4 = result.fun
            best_params_p4 = result.x.copy()
            if result.fun < 0:
                print(f"  *** CANDIDATE at trial {trial}: margin = {result.fun:.10e} ***")
    except:
        pass
    if (trial+1) % 100 == 0:
        print(f"  After {trial+1} starts: best = {min_margin_p4:.8e}")

# Also seed from best candidates found in Phase 1-3
candidates_sorted = sorted(candidates, key=lambda x: x[0])[:20]
for idx, (m, rp, rq) in enumerate(candidates_sorted):
    x0 = np.concatenate([rp, rq])
    try:
        result = minimize(objective, x0, method='Nelder-Mead',
                         options={'maxiter': 10000, 'xatol': 1e-15, 'fatol': 1e-17})
        if result.fun < min_margin_p4:
            min_margin_p4 = result.fun
            best_params_p4 = result.x.copy()
            if result.fun < 0:
                print(f"  *** CANDIDATE from seed {idx}: margin = {result.fun:.10e} ***")
    except:
        pass

# Differential evolution
print(f"  Running differential evolution...")
try:
    bounds = [(-6, 6)] * 8
    result_de = differential_evolution(objective, bounds, seed=42,
                                       maxiter=1000, tol=1e-16, popsize=40,
                                       mutation=(0.5, 1.5), recombination=0.9)
    if result_de.fun < min_margin_p4:
        min_margin_p4 = result_de.fun
        best_params_p4 = result_de.x.copy()
    print(f"  DE result: {result_de.fun:.10e}")
except Exception as e:
    print(f"  DE failed: {e}")

print(f"  Phase 4 done: min_margin = {min_margin_p4:.8e}")
if min_margin_p4 < 0:
    rp_best = np.sort(best_params_p4[:4])
    rq_best = np.sort(best_params_p4[4:])
    print(f"  Best p roots: {rp_best}")
    print(f"  Best q roots: {rq_best}")

# Add Phase 4 results to candidates
if min_margin_p4 < 1e-3 and best_params_p4 is not None:
    rp_best = np.sort(best_params_p4[:4])
    rq_best = np.sort(best_params_p4[4:])
    candidates.append((min_margin_p4, rp_best, rq_best))

# ============================================================
# Phase 5: Coefficient-space optimization (exploit cross-term)
# ============================================================
print("\nPhase 5: Coefficient-space optimization (cross-term focus)")
print("-" * 60)

def objective_coeff(params):
    """Optimize in coefficient space to focus on cross-term effect."""
    a2, a3, a4, b2, b3, b4 = params
    return margin_centered_coeffs(a2, a3, a4, b2, b3, b4)

min_margin_p5 = 1e10
best_params_p5 = None

# Strategy: large |a2| and |b2| with same sign to maximize cross-term
for trial in range(500):
    np.random.seed(30000 + trial)

    strategy = trial % 5
    if strategy == 0:
        # Large same-sign a2, b2
        a2 = -np.random.uniform(1, 20)
        b2 = -np.random.uniform(1, 20)
        a3 = np.random.randn() * 0.5
        b3 = np.random.randn() * 0.5
        a4 = np.random.uniform(0, a2**2/4)  # try to keep real roots
        b4 = np.random.uniform(0, b2**2/4)
    elif strategy == 1:
        # Opposite sign a2, b2 (cross-term negative)
        a2 = -np.random.uniform(1, 10)
        b2 = np.random.uniform(0.1, 5)
        a3, b3 = np.random.randn(2) * 0.3
        a4, b4 = np.random.randn(2)
    elif strategy == 2:
        # Near-degenerate discriminant
        a2 = -np.random.uniform(0.1, 5)
        a3 = np.random.randn() * 0.1
        a4 = (a2**2) / 4.0 * (1 - np.random.uniform(0.001, 0.1))
        b2 = -np.random.uniform(0.1, 5)
        b3 = np.random.randn() * 0.1
        b4 = (b2**2) / 4.0 * (1 - np.random.uniform(0.001, 0.1))
    elif strategy == 3:
        # Very asymmetric
        a2 = -np.random.uniform(0.01, 0.1)
        a3 = np.random.randn() * 0.001
        a4 = np.random.uniform(0, 0.001)
        b2 = -np.random.uniform(5, 50)
        b3 = np.random.randn() * 2
        b4 = np.random.uniform(0, b2**2/3)
    else:
        # Random
        params0 = np.random.randn(6) * 3.0
        a2, a3, a4, b2, b3, b4 = params0

    x0 = np.array([a2, a3, a4, b2, b3, b4])
    try:
        result = minimize(objective_coeff, x0, method='Nelder-Mead',
                         options={'maxiter': 5000, 'xatol': 1e-14, 'fatol': 1e-16})
        if result.fun < min_margin_p5:
            min_margin_p5 = result.fun
            best_params_p5 = result.x.copy()
            if result.fun < 0:
                print(f"  *** COEFF CANDIDATE at trial {trial}: margin = {result.fun:.10e} ***")
                print(f"      params = {result.x}")
    except:
        pass

    if (trial+1) % 100 == 0:
        print(f"  After {trial+1}: best = {min_margin_p5:.8e}")

print(f"  Phase 5 done: min_margin = {min_margin_p5:.8e}")

# ============================================================
# Phase 6: High-precision verification of all candidates
# ============================================================
print("\nPhase 6: High-precision verification")
print("-" * 60)

import mpmath
mpmath.mp.dps = 80

def mp_factorial(n):
    return mpmath.factorial(n)

def finite_free_conv_mp(a, b, n):
    c = [mpmath.mpf(0)] * (n + 1)
    for k in range(n + 1):
        for i in range(k + 1):
            j = k - i
            if i <= n and j <= n:
                num = mp_factorial(n - i) * mp_factorial(n - j)
                den = mp_factorial(n) * mp_factorial(n - k)
                c[k] += (num / den) * a[i] * b[j]
    return c

def phi_mp(roots):
    n = len(roots)
    total = mpmath.mpf(0)
    for i in range(n):
        s = mpmath.mpf(0)
        for j in range(n):
            if j != i:
                if abs(roots[i] - roots[j]) < mpmath.mpf(10)**(-60):
                    return mpmath.inf
                s += 1 / (roots[i] - roots[j])
        total += s**2
    return total

def verify_hp(rp, rq, n=4, dps=80):
    """Verify margin at high precision. Returns (margin, phi_p, phi_q, phi_h)."""
    mpmath.mp.dps = dps
    rp_mp = [mpmath.mpf(str(x)) for x in rp]
    rq_mp = [mpmath.mpf(str(x)) for x in rq]

    a = [mpmath.mpf(1)]
    for r in rp_mp:
        new_a = [mpmath.mpf(0)] * (len(a) + 1)
        for i in range(len(a)):
            new_a[i] += a[i]
            new_a[i+1] -= a[i] * r
        a = new_a

    b = [mpmath.mpf(1)]
    for r in rq_mp:
        new_b = [mpmath.mpf(0)] * (len(b) + 1)
        for i in range(len(b)):
            new_b[i] += b[i]
            new_b[i+1] -= b[i] * r
        b = new_b

    c = finite_free_conv_mp(a, b, n)
    rh = sorted(mpmath.polyroots(c, maxsteps=1000, extraprec=100),
                key=lambda r: mpmath.re(r))
    rh = [mpmath.re(r) for r in rh]

    pp = phi_mp(rp_mp)
    pq = phi_mp(rq_mp)
    ph = phi_mp(rh)

    if pp == mpmath.inf or pq == mpmath.inf or ph == mpmath.inf:
        return (mpmath.mpf(0), pp, pq, ph)

    margin = 1/ph - 1/pp - 1/pq
    return (margin, pp, pq, ph)

# Collect all candidates
all_candidates = sorted(candidates, key=lambda x: x[0])[:50]

# Also add the global best from each phase
overall_min = min(min_margin_p1, min_margin_p2, min_margin_p3, min_margin_p4, min_margin_p5)
print(f"\n  Overall minimum margin (double precision): {overall_min:.10e}")
print(f"  Number of candidates with margin < 1e-4: {len([c for c in candidates if c[0] < 1e-4])}")

confirmed_ce = []
if all_candidates:
    print(f"\n  Verifying top {len(all_candidates)} candidates at 80 digits...")
    for idx, (m_dp, rp, rq) in enumerate(all_candidates[:30]):
        try:
            m_hp, pp, pq, ph = verify_hp(rp, rq, 4, dps=80)
            status = "CONFIRMED CE" if m_hp < 0 else "false alarm"
            if m_hp < 0:
                confirmed_ce.append((m_hp, rp, rq))
            if idx < 10 or m_hp < 0:
                print(f"  #{idx}: dp_margin={m_dp:.6e}, hp_margin={float(m_hp):.15e} [{status}]")
        except Exception as e:
            if idx < 5:
                print(f"  #{idx}: verification failed: {e}")
else:
    print("  No candidates found (all margins well above 0)")

# ============================================================
# Phase 7: Ultra-high precision verification of confirmed CEs
# ============================================================
if confirmed_ce:
    print(f"\n\nPhase 7: ULTRA-HIGH PRECISION verification ({len(confirmed_ce)} confirmed CEs)")
    print("=" * 70)
    mpmath.mp.dps = 200

    for idx, (m80, rp, rq) in enumerate(confirmed_ce[:5]):
        print(f"\n  CE #{idx+1}:")
        print(f"    p roots = {rp}")
        print(f"    q roots = {rq}")
        try:
            m200, pp, pq, ph = verify_hp(rp, rq, 4, dps=200)
            print(f"    200-digit margin = {mpmath.nstr(m200, 50)}")
            if m200 < 0:
                print(f"    *** COUNTEREXAMPLE CONFIRMED AT 200 DIGITS ***")
            else:
                print(f"    False alarm at 200 digits")
        except Exception as e:
            print(f"    200-digit verification failed: {e}")
else:
    print(f"\n  No confirmed counterexamples.")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("SUMMARY")
print(f"  Phase 1 (200K random): min_margin = {min_margin_p1:.8e}")
print(f"  Phase 2 (50K clustered): min_margin = {min_margin_p2:.8e}")
print(f"  Phase 3 (20K parametric): min_margin = {min_margin_p3:.8e}")
print(f"  Phase 4 (500 scipy + DE): min_margin = {min_margin_p4:.8e}")
print(f"  Phase 5 (500 coeff-space): min_margin = {min_margin_p5:.8e}")
print(f"  Overall minimum: {overall_min:.10e}")
print(f"  Candidates tested at 80 digits: {min(30, len(all_candidates))}")
print(f"  Confirmed counterexamples: {len(confirmed_ce)}")
if confirmed_ce:
    print(f"\n  *** COUNTEREXAMPLE FOUND ***")
else:
    print(f"\n  NO COUNTEREXAMPLE FOUND - inequality appears to hold for n=4")
print("DONE")
