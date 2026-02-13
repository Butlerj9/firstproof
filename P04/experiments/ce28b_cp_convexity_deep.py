"""
ce28b_cp_convexity_deep.py — Deep test of parametric c' convexity.

KEY FINDING from CE-28: M(w, b1, b2, t*cp1, t*cp2) appears convex in t.
This means: starting from the PROVED c'=0 case (t=0), the margin M stays
non-negative if we can show:
  1. M is convex in t (d²M/dt² >= 0)
  2. M(0) >= 0 (PROVED, c'=0 subcase)
  3. M at boundary (t_max) >= 0 (need to verify)

Convexity + M(0) >= 0 => min is at boundary, so we need M(t_max) >= 0.
MSS guarantees h has real roots whenever p,q do, so boundary = Δ₁=0 or Δ₂=0.

This script:
  - Tests convexity thoroughly (500K+ points)
  - Tests boundary behavior
  - Computes d²M/dt² at many parameter combinations
  - Identifies if convexity holds universally
"""
import sys, io, time, random
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_formula(sigma, b, cp):
    """1/Phi4 via closed form."""
    a = -sigma
    c = sigma**2 / 12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    if Delta <= 0:
        return None, False
    if A * B >= 0:
        return None, False
    val = -Delta / (4.0 * A * B)
    if val <= 0:
        return None, False
    return val, True

def margin(w, b1, b2, cp1, cp2):
    s1, s2, sh = w, 1.0 - w, 1.0
    fh, okh = phi4_formula(sh, b1+b2, cp1+cp2)
    f1, ok1 = phi4_formula(s1, b1, cp1)
    f2, ok2 = phi4_formula(s2, b2, cp2)
    if not (okh and ok1 and ok2):
        return None, False
    return fh - f1 - f2, True

def margin_t(w, b1, b2, cp1, cp2, t):
    """Margin with c' scaled by t."""
    return margin(w, b1, b2, t*cp1, t*cp2)

# ============================================================
print(SEP)
print("SECTION 1: Massive convexity test (d²M/dt² >= 0)")
print(SEP)

h = 1e-5
random.seed(42)
n_tested = 0
n_violations = 0
min_d2 = float('inf')
worst = None

# Test many random parameters and many t values
for _ in range(100000):
    w = random.uniform(0.1, 0.9)
    b1 = random.uniform(-0.4, 0.4)
    b2 = random.uniform(-0.4, 0.4)
    cp1 = random.uniform(-0.08, 0.08)
    cp2 = random.uniform(-0.08, 0.08)

    for t_val in np.linspace(0.1, 2.0, 10):
        f0, ok0 = margin_t(w, b1, b2, cp1, cp2, t_val)
        fp, okp = margin_t(w, b1, b2, cp1, cp2, t_val + h)
        fm, okm = margin_t(w, b1, b2, cp1, cp2, t_val - h)

        if not (ok0 and okp and okm):
            continue

        n_tested += 1
        d2 = (fp - 2*f0 + fm) / h**2

        if d2 < min_d2:
            min_d2 = d2
            worst = (w, b1, b2, cp1, cp2, t_val, d2, f0)

        if d2 < -1e-3:  # conservative tolerance
            n_violations += 1

print("Total d²M/dt² tests: %d" % n_tested)
print("Violations (d² < -1e-3): %d" % n_violations)
print("Min d²M/dt²: %.6e" % min_d2)
if worst:
    w, b1, b2, cp1, cp2, tv, d2v, fv = worst
    print("Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f t=%.2f d2=%.4e M=%.4e" %
          (w, b1, b2, cp1, cp2, tv, d2v, fv))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Stress test near boundary (small sigma, large b)")
print(SEP)

random.seed(123)
n_stress = 0
n_stress_viol = 0

for _ in range(50000):
    w = random.uniform(0.05, 0.95)
    # Larger b values (closer to validity boundary)
    s1 = w
    s2 = 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = random.uniform(-b1_max, b1_max)
    b2 = random.uniform(-b2_max, b2_max)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    for t_val in np.linspace(0.1, 1.5, 8):
        f0, ok0 = margin_t(w, b1, b2, cp1, cp2, t_val)
        fp, okp = margin_t(w, b1, b2, cp1, cp2, t_val + h)
        fm, okm = margin_t(w, b1, b2, cp1, cp2, t_val - h)

        if not (ok0 and okp and okm):
            continue

        n_stress += 1
        d2 = (fp - 2*f0 + fm) / h**2

        if d2 < min_d2:
            min_d2 = d2
            worst = (w, b1, b2, cp1, cp2, t_val, d2, f0)

        if d2 < -1e-3:
            n_stress_viol += 1

print("Stress tests: %d" % n_stress)
print("Stress violations: %d" % n_stress_viol)
print("Overall min d²: %.6e" % min_d2)
if worst:
    w, b1, b2, cp1, cp2, tv, d2v, fv = worst
    print("Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f t=%.2f d2=%.4e M=%.4e" %
          (w, b1, b2, cp1, cp2, tv, d2v, fv))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Boundary behavior (as t -> t_max)")
print(SEP)

# Find t_max for each parameter set and check M there
random.seed(456)
n_boundary = 0
n_boundary_neg = 0
min_boundary_M = float('inf')

for _ in range(50000):
    w = random.uniform(0.1, 0.9)
    s1 = w
    s2 = 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = random.uniform(-b1_max, b1_max)
    b2 = random.uniform(-b2_max, b2_max)
    cp1 = random.uniform(-0.03, 0.03)
    cp2 = random.uniform(-0.03, 0.03)

    if abs(cp1) < 1e-6 and abs(cp2) < 1e-6:
        continue

    # Binary search for t_max (largest t where all three polys are valid)
    t_lo, t_hi = 0.0, 10.0
    for _ in range(50):
        t_mid = (t_lo + t_hi) / 2
        _, ok = margin_t(w, b1, b2, cp1, cp2, t_mid)
        if ok:
            t_lo = t_mid
        else:
            t_hi = t_mid

    t_max = t_lo
    if t_max < 0.5:
        continue

    # Evaluate M near the boundary
    M_bdry, ok_bdry = margin_t(w, b1, b2, cp1, cp2, t_max * 0.999)
    if not ok_bdry:
        continue

    n_boundary += 1
    if M_bdry < min_boundary_M:
        min_boundary_M = M_bdry

    if M_bdry < -1e-8:
        n_boundary_neg += 1

print("Boundary tests: %d" % n_boundary)
print("Boundary M < 0: %d" % n_boundary_neg)
print("Min boundary M: %.6e" % min_boundary_M)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: First derivative at t=0 (should be 0 by symmetry)")
print(SEP)

# M(w, b1, b2, t*cp1, t*cp2) at t=0 has value M_b (the c'=0 margin).
# Check if dM/dt = 0 at t=0 (this would mean the c'=0 point is critical).
random.seed(789)
n_deriv = 0
max_d1 = -float('inf')

for _ in range(20000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.2, 0.2)
    b2 = random.uniform(-0.2, 0.2)
    cp1 = random.uniform(-0.03, 0.03)
    cp2 = random.uniform(-0.03, 0.03)

    # First derivative at t=0+
    t_val = 0.001
    f0, ok0 = margin_t(w, b1, b2, cp1, cp2, 0)
    fp, okp = margin_t(w, b1, b2, cp1, cp2, t_val)
    # Handle t=0 specially: at t=0, we're at c'=0
    M_0, ok_0 = margin(w, b1, b2, 0, 0)
    if not (ok_0 and okp):
        continue

    n_deriv += 1
    d1 = (fp - M_0) / t_val

    if abs(d1) > abs(max_d1):
        max_d1 = d1

# M at t=0 is M_b (c'=0 margin). dM/dt at t=0 measures the effect of turning on c'.
print("Derivative tests: %d" % n_deriv)
print("Max |dM/dt| at t≈0: %.6e" % abs(max_d1))
print("Note: dM/dt at t=0 is generally NONZERO (c' enters at first order)")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Comprehensive profile M(t) along representative rays")
print(SEP)

# Pick a few representative parameter sets and trace the full M(t) profile
random.seed(321)
for trial in range(5):
    w = random.uniform(0.2, 0.8)
    s1 = w
    b1_max = (4*s1**3/27)**0.5 * 0.8
    b2_max = (4*(1-w)**3/27)**0.5 * 0.8
    b1 = random.uniform(-b1_max, b1_max)
    b2 = random.uniform(-b2_max, b2_max)
    cp1 = random.uniform(-0.02, 0.02)
    cp2 = random.uniform(-0.02, 0.02)

    print("\nRay %d: w=%.3f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f" %
          (trial+1, w, b1, b2, cp1, cp2))

    t_vals = np.linspace(0, 3.0, 100)
    M_vals = []
    for tv in t_vals:
        M_val, ok = margin_t(w, b1, b2, cp1, cp2, tv)
        if ok:
            M_vals.append((tv, M_val))
        else:
            break

    if len(M_vals) < 5:
        print("  Too few valid points (%d)" % len(M_vals))
        continue

    t_arr = [x[0] for x in M_vals]
    M_arr = [x[1] for x in M_vals]
    print("  t range: [%.3f, %.3f], %d points" % (t_arr[0], t_arr[-1], len(M_vals)))
    print("  M range: [%.6e, %.6e]" % (min(M_arr), max(M_arr)))
    print("  M(0)=%.6e, M(t_max/2)=%.6e, M(t_max)=%.6e" %
          (M_arr[0], M_arr[len(M_arr)//2], M_arr[-1]))
    print("  Min M: %.6e at t=%.3f" % (min(M_arr), t_arr[M_arr.index(min(M_arr))]))
    print("  All M >= 0: %s" % all(m >= -1e-10 for m in M_arr))

    # Check convexity along this ray
    n_conv = 0
    n_nonconv = 0
    for i in range(1, len(M_arr)-1):
        dt = t_arr[i] - t_arr[i-1]
        d2 = (M_arr[i+1] - 2*M_arr[i] + M_arr[i-1]) / dt**2
        if d2 < -1e-4:
            n_nonconv += 1
        else:
            n_conv += 1
    print("  Convex points: %d/%d" % (n_conv, n_conv + n_nonconv))

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("VERDICT")
print(SEP)

total_violations = n_violations + n_stress_viol
total_tests = n_tested + n_stress
print("Total convexity tests: %d" % total_tests)
print("Total violations: %d" % total_violations)
print("Violation rate: %.4f%%" % (100.0 * total_violations / max(1, total_tests)))

if total_violations == 0:
    print("\n=> PARAMETRIC c' CONVEXITY HOLDS (0 violations in %d tests)" % total_tests)
    print("   Combined with c'=0 subcase (CE-26), this gives:")
    print("   M(w,b,cp) >= M(w,b,0) + dM/dt|_{t=0} * t + (convex correction)")
    print("   The minimum is at t=0 (proved >= 0) or at t_max (boundary).")
    if n_boundary_neg == 0:
        print("   Boundary M >= 0 in %d tests => FULL INEQUALITY HOLDS NUMERICALLY" % n_boundary)
else:
    print("\n=> PARAMETRIC c' CONVEXITY FAILS (%d violations)" % total_violations)

print("\nElapsed: %.1fs" % (time.time() - t0))
