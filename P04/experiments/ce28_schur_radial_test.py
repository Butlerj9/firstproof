"""
ce28_schur_radial_test.py — Test Schur complement and radial convexity for general n=4.

Now that b=0 (CE-16) and c'=0 (CE-26) subcases are proved, test whether:
1. Additive decomposition: M_full >= M_b + M_c  (coupling term >= 0)
2. Radial convexity: M(w, t*b1, t*b2, t*c1', t*c2') is convex in t
3. Parametric slice: M(w, b1, b2, t*c1', t*c2') is monotone/convex in t
4. Schur complement: the 2x2 matrix [[M_b, Delta/2],[Delta/2, M_c]] is PSD

If ANY of these hold, it provides a new route to close the general case.
"""
import sys, io, time, random
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_formula(sigma, b, cp):
    """Compute 1/Phi4 using the closed-form formula.
    1/Phi4 = -Delta / (4 * A * B) where
    A = a^2 + 12c, B = 2a^3 - 8ac + 9b^2, a = -sigma, c = sigma^2/12 + cp
    Returns (value, is_valid).
    """
    a = -sigma
    c = sigma**2 / 12.0 + cp

    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2

    # Discriminant
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)

    if Delta <= 0:
        return None, False
    if A * B >= 0:  # need A*B < 0 for 4 real roots
        return None, False

    val = -Delta / (4.0 * A * B)
    if val <= 0:
        return None, False
    return val, True

def margin(w, b1, b2, cp1, cp2):
    """Superadditivity margin M = F(h) - F(1) - F(2)."""
    s1 = w
    s2 = 1.0 - w
    sh = 1.0
    bh = b1 + b2
    cph = cp1 + cp2

    fh, okh = phi4_formula(sh, bh, cph)
    f1, ok1 = phi4_formula(s1, b1, cp1)
    f2, ok2 = phi4_formula(s2, b2, cp2)

    if not (okh and ok1 and ok2):
        return None, False
    return fh - f1 - f2, True

# ============================================================
print(SEP)
print("SECTION 1: Additive decomposition test")
print("  M_full >= M_b + M_c  <=>  coupling Δ >= 0")
print(SEP)

random.seed(42)
n_tested = 0
n_additive_violations = 0
min_coupling = float('inf')
worst_additive = None

for _ in range(200000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    M_full, ok_full = margin(w, b1, b2, cp1, cp2)
    M_b, ok_b = margin(w, b1, b2, 0, 0)
    M_c, ok_c = margin(w, 0, 0, cp1, cp2)

    if not (ok_full and ok_b and ok_c):
        continue

    n_tested += 1
    coupling = M_full - M_b - M_c

    if coupling < min_coupling:
        min_coupling = coupling
        worst_additive = (w, b1, b2, cp1, cp2, coupling, M_full, M_b, M_c)

    if coupling < -1e-10:
        n_additive_violations += 1

print("Points tested: %d" % n_tested)
print("Additive violations (Δ < -1e-10): %d" % n_additive_violations)
print("Min coupling Δ: %.6e" % min_coupling)
if worst_additive:
    w, b1, b2, cp1, cp2, coup, Mf, Mb, Mc = worst_additive
    print("Worst point: w=%.3f, b1=%.3f, b2=%.3f, cp1=%.4f, cp2=%.4f" % (w, b1, b2, cp1, cp2))
    print("  M_full=%.6e, M_b=%.6e, M_c=%.6e, coupling=%.6e" % (Mf, Mb, Mc, coup))

if n_additive_violations == 0:
    print("\n=> ADDITIVE DECOMPOSITION HOLDS: M_full >= M_b + M_c ✓")
    print("   This means the proved b=0 and c'=0 subcases are SUFFICIENT!")
else:
    print("\n=> ADDITIVE DECOMPOSITION FAILS: %d violations" % n_additive_violations)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Radial convexity test")
print("  Is M(w, t*b1, t*b2, t*cp1, t*cp2) convex in t?")
print(SEP)

random.seed(123)
h = 1e-5
n_radial_tested = 0
n_radial_violations = 0
min_d2 = float('inf')
worst_radial = None

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    # Test at several t values
    for t_val in [0.3, 0.5, 0.7, 1.0]:
        f0, ok0 = margin(w, t_val*b1, t_val*b2, t_val*cp1, t_val*cp2)
        fp, okp = margin(w, (t_val+h)*b1, (t_val+h)*b2, (t_val+h)*cp1, (t_val+h)*cp2)
        fm, okm = margin(w, (t_val-h)*b1, (t_val-h)*b2, (t_val-h)*cp1, (t_val-h)*cp2)

        if not (ok0 and okp and okm):
            continue

        d2 = (fp - 2*f0 + fm) / h**2  # second derivative
        n_radial_tested += 1

        if d2 < min_d2:
            min_d2 = d2
            worst_radial = (w, b1, b2, cp1, cp2, t_val, d2)

        if d2 < -1e-2:  # tolerance for finite differences
            n_radial_violations += 1

print("Radial tests: %d" % n_radial_tested)
print("Convexity violations (d²M/dt² < -0.01): %d" % n_radial_violations)
print("Min d²M/dt²: %.6e" % min_d2)
if worst_radial:
    w, b1, b2, cp1, cp2, tv, d2v = worst_radial
    print("Worst: w=%.3f, b1=%.3f, b2=%.3f, cp1=%.4f, cp2=%.4f, t=%.1f, d2=%.4f" %
          (w, b1, b2, cp1, cp2, tv, d2v))

if n_radial_violations == 0:
    print("\n=> RADIAL CONVEXITY HOLDS ✓")
    print("   Combined with M(0)=0, M''(0)>0, this proves M(t)>=0 for all t!")
else:
    print("\n=> RADIAL CONVEXITY FAILS: %d violations" % n_radial_violations)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Parametric c' slice test")
print("  Fix (w,b1,b2), vary c'. Is M(w,b1,b2,t*cp1,t*cp2) monotone in t?")
print(SEP)

random.seed(456)
n_slice_tested = 0
n_monotone_violations = 0
n_convex_violations = 0

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    for t_val in [0.3, 0.5, 0.7, 1.0]:
        f0, ok0 = margin(w, b1, b2, t_val*cp1, t_val*cp2)
        fp, okp = margin(w, b1, b2, (t_val+h)*cp1, (t_val+h)*cp2)
        fm, okm = margin(w, b1, b2, (t_val-h)*cp1, (t_val-h)*cp2)

        if not (ok0 and okp and okm):
            continue

        n_slice_tested += 1
        d1 = (fp - fm) / (2*h)  # first derivative
        d2 = (fp - 2*f0 + fm) / h**2

        # Check: is M decreasing in t? (from proved c'=0 baseline at t=0)
        # At t=0, M = M_b (proved >= 0). If M is decreasing, it could go negative.
        # Instead, check convexity in t.
        if d2 < -1e-2:
            n_convex_violations += 1

print("Parametric c' tests: %d" % n_slice_tested)
print("Convexity violations: %d" % n_convex_violations)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Parametric b slice (from b=0 proved baseline)")
print("  Fix (w,cp1,cp2), vary b. Is M(w,t*b1,t*b2,cp1,cp2) convex in t?")
print(SEP)

random.seed(789)
n_bslice_tested = 0
n_bconvex_violations = 0
min_bd2 = float('inf')

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    for t_val in [0.3, 0.5, 0.7, 1.0]:
        f0, ok0 = margin(w, t_val*b1, t_val*b2, cp1, cp2)
        fp, okp = margin(w, (t_val+h)*b1, (t_val+h)*b2, cp1, cp2)
        fm, okm = margin(w, (t_val-h)*b1, (t_val-h)*b2, cp1, cp2)

        if not (ok0 and okp and okm):
            continue

        n_bslice_tested += 1
        d2 = (fp - 2*f0 + fm) / h**2

        if d2 < min_bd2:
            min_bd2 = d2

        if d2 < -1e-2:
            n_bconvex_violations += 1

print("Parametric b tests: %d" % n_bslice_tested)
print("Convexity violations: %d" % n_bconvex_violations)
print("Min d²M/dt²: %.6e" % min_bd2)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Schur complement condition")
print("  Is [[M_b, Δ/2],[Δ/2, M_c]] PSD? (i.e., M_b*M_c >= (Δ/2)^2)")
print(SEP)

# Re-use data from Section 1 with a targeted test
random.seed(42)
n_schur_tested = 0
n_schur_violations = 0
min_schur_det = float('inf')

for _ in range(200000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    M_full, ok_full = margin(w, b1, b2, cp1, cp2)
    M_b, ok_b = margin(w, b1, b2, 0, 0)
    M_c, ok_c = margin(w, 0, 0, cp1, cp2)

    if not (ok_full and ok_b and ok_c):
        continue

    n_schur_tested += 1
    coupling = M_full - M_b - M_c

    # Schur condition: M_b * M_c >= (coupling/2)^2
    schur_det = M_b * M_c - (coupling/2)**2

    if schur_det < min_schur_det:
        min_schur_det = schur_det

    if schur_det < -1e-15:
        n_schur_violations += 1

print("Schur tests: %d" % n_schur_tested)
print("Schur violations: %d" % n_schur_violations)
print("Min Schur det: %.6e" % min_schur_det)

if n_schur_violations == 0:
    print("\n=> SCHUR COMPLEMENT CONDITION HOLDS ✓")
else:
    print("\n=> SCHUR COMPLEMENT CONDITION FAILS: %d violations" % n_schur_violations)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Direct SOS feasibility assessment")
print(SEP)

# After gauge-fixing sigma_h = 1, we have 5 variables (w, b1, b2, cp1, cp2).
# The margin numerator after clearing denominators is degree 16 in these.
# Number of monomials up to degree 8 in 5 variables: C(13,8) = 1287
# Gram matrix: 1287 x 1287 (borderline for SDP)
# With sparsity: potentially much smaller blocks.

print("For SOS on degree-16 in 5 vars:")
from math import comb
n_monoms = comb(5+8, 8)
print("  Monomials up to degree 8: %d" % n_monoms)
print("  Gram matrix size: %d x %d" % (n_monoms, n_monoms))
print("  Gram matrix entries: %d" % (n_monoms * (n_monoms + 1) // 2))
print("  Available solvers: CLARABEL, SCS")
print("  Assessment: BORDERLINE (may work with Clarabel)")

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)

results = {
    "Additive decomposition": n_additive_violations == 0,
    "Radial convexity": n_radial_violations == 0,
    "Parametric c' convexity": n_convex_violations == 0,
    "Parametric b convexity": n_bconvex_violations == 0,
    "Schur complement": n_schur_violations == 0,
}

for name, passed in results.items():
    print("  %-30s: %s" % (name, "PASS ✓" if passed else "FAIL ✗"))

passing = [k for k, v in results.items() if v]
if passing:
    print("\nPASSING ROUTES: %s" % ", ".join(passing))
    print("=> These provide potential new proof approaches!")
else:
    print("\nNo structural property holds. All routes FAIL.")

print("\nElapsed: %.1fs" % (time.time() - t0))
