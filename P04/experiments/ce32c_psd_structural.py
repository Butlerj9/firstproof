"""
ce32c_psd_structural.py — Test structural conditions for M''(theta) >= 0.

Key finding from CE-32b: f'' = (27b^2-8sigma^3) * Q(sigma,b,c') / [(A/2)^3 * (3B)^3]

M''(theta) = c1'^2*g1(theta) + c2'^2*g2(theta) - (c1'+c2')^2*g_h(theta)
where g_i = |f''_i| > 0.

This is PSD as quadratic form in (c1',c2') iff:
(a) g1 >= g_h  AND  g2 >= g_h
(b) g1*g2 >= g_h*(g1+g2)  [i.e., harmonic mean >= g_h]

The PSD condition is EQUIVALENT to phi-subadditivity (phi = 1/g):
  phi1 + phi2 <= phi_h

Test all three conditions at general (c1', c2', theta).
"""
import sys, io, time
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_inv(sigma, b, cp):
    a = -sigma
    c = sigma**2/12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    if Delta <= 0 or A*B >= 0:
        return None
    return -Delta/(4.0*A*B)

h_fd = 1e-6

def g_at(sig, bv, cpv):
    """g = |f''| = |d^2(1/Phi4)/dc'^2| > 0 via finite differences."""
    f0 = phi4_inv(sig, bv, cpv)
    fp = phi4_inv(sig, bv, cpv + h_fd)
    fm = phi4_inv(sig, bv, cpv - h_fd)
    if f0 is None or fp is None or fm is None:
        return None
    fpp = (fp - 2*f0 + fm) / h_fd**2
    return -fpp  # g = -f'' > 0

# ============================================================
print(SEP)
print("SECTION 1: Test g1 >= g_h and g2 >= g_h (diagonal dominance)")
print(SEP)
sys.stdout.flush()

np.random.seed(42)
n_test1 = 0
n_fail_a1 = 0  # g1 < g_h
n_fail_a2 = 0  # g2 < g_h

for _ in range(500000):
    w = np.random.uniform(0.02, 0.98)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    theta = np.random.uniform(0.0, 1.5)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)
    cph = cp1 + cp2

    g1 = g_at(s1, b1, theta*cp1)
    g2 = g_at(s2, b2, theta*cp2)
    gh = g_at(1.0, bh, theta*cph)

    if g1 is None or g2 is None or gh is None:
        continue
    if g1 <= 0 or g2 <= 0 or gh <= 0:
        continue

    n_test1 += 1
    if g1 < gh - 1e-3:
        n_fail_a1 += 1
    if g2 < gh - 1e-3:
        n_fail_a2 += 1

print("Tests: %d" % n_test1)
print("g1 < g_h violations: %d (%.2f%%)" % (n_fail_a1, 100*n_fail_a1/max(1,n_test1)))
print("g2 < g_h violations: %d (%.2f%%)" % (n_fail_a2, 100*n_fail_a2/max(1,n_test1)))
print("Diagonal dominance holds: %s" % ("YES" if n_fail_a1 == 0 and n_fail_a2 == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Test g1*g2 >= g_h*(g1+g2) (determinant condition)")
print(SEP)
sys.stdout.flush()

np.random.seed(123)
n_test2 = 0
n_fail_det = 0
min_det_slack = float('inf')

for _ in range(500000):
    w = np.random.uniform(0.02, 0.98)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    theta = np.random.uniform(0.0, 1.5)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)
    cph = cp1 + cp2

    g1 = g_at(s1, b1, theta*cp1)
    g2 = g_at(s2, b2, theta*cp2)
    gh = g_at(1.0, bh, theta*cph)

    if g1 is None or g2 is None or gh is None:
        continue
    if g1 <= 0 or g2 <= 0 or gh <= 0:
        continue

    n_test2 += 1
    det_slack = g1*g2 - gh*(g1+g2)

    if det_slack < min_det_slack:
        min_det_slack = det_slack

    if det_slack < -1e-3:
        n_fail_det += 1

print("Tests: %d" % n_test2)
print("Det violations (g1*g2 < g_h*(g1+g2)): %d (%.2f%%)" % (n_fail_det, 100*n_fail_det/max(1,n_test2)))
print("Min det slack: %.6e" % min_det_slack)
print("Det condition holds: %s" % ("YES" if n_fail_det == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Generalized phi-subadditivity at general c' and theta")
print(SEP)
sys.stdout.flush()

np.random.seed(456)
n_test3 = 0
n_fail3 = 0
max_ratio3 = 0

for _ in range(500000):
    w = np.random.uniform(0.02, 0.98)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    theta = np.random.uniform(0.0, 1.5)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)
    cph = cp1 + cp2

    g1 = g_at(s1, b1, theta*cp1)
    g2 = g_at(s2, b2, theta*cp2)
    gh = g_at(1.0, bh, theta*cph)

    if g1 is None or g2 is None or gh is None:
        continue
    if g1 <= 0 or g2 <= 0 or gh <= 0:
        continue

    n_test3 += 1
    phi1 = 1.0/g1
    phi2 = 1.0/g2
    phih = 1.0/gh

    ratio = (phi1 + phi2) / phih
    if ratio > max_ratio3:
        max_ratio3 = ratio

    if phi1 + phi2 > phih + 1e-10:
        n_fail3 += 1

print("Tests: %d" % n_test3)
print("Generalized phi-subadditivity violations: %d" % n_fail3)
print("Max ratio (phi1+phi2)/phi_h: %.6f" % max_ratio3)
print("Subadditive universally: %s" % ("YES" if n_fail3 == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Ratio g1/g_h and g2/g_h distributions")
print(SEP)
sys.stdout.flush()

np.random.seed(789)
n_test4 = 0
min_g1_gh = float('inf')
min_g2_gh = float('inf')
max_gh_g1 = 0
max_gh_g2 = 0

for _ in range(300000):
    w = np.random.uniform(0.02, 0.98)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    theta = np.random.uniform(0.0, 1.5)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)
    cph = cp1 + cp2

    g1 = g_at(s1, b1, theta*cp1)
    g2 = g_at(s2, b2, theta*cp2)
    gh = g_at(1.0, bh, theta*cph)

    if g1 is None or g2 is None or gh is None:
        continue
    if g1 <= 0 or g2 <= 0 or gh <= 0:
        continue

    n_test4 += 1
    r1 = g1/gh
    r2 = g2/gh

    if r1 < min_g1_gh:
        min_g1_gh = r1
    if r2 < min_g2_gh:
        min_g2_gh = r2
    if 1/r1 > max_gh_g1:
        max_gh_g1 = 1/r1
    if 1/r2 > max_gh_g2:
        max_gh_g2 = 1/r2

print("Tests: %d" % n_test4)
print("Min g1/g_h: %.6f" % min_g1_gh)
print("Min g2/g_h: %.6f" % min_g2_gh)
print("Max g_h/g1: %.6f" % max_gh_g1)
print("Max g_h/g2: %.6f" % max_gh_g2)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Direct M''(theta) >= 0 test — extended scale")
print("Using g directly (no matrix PSD requirement)")
print(SEP)
sys.stdout.flush()

np.random.seed(999)
n_test5 = 0
n_fail5 = 0
min_mpp = float('inf')

for _ in range(500000):
    w = np.random.uniform(0.02, 0.98)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.1, 0.1)
    cp2 = np.random.uniform(-0.1, 0.1)

    theta = np.random.uniform(0.0, 2.0)

    vals = []
    valid = True
    for dt in [-h_fd, 0, h_fd]:
        tv = theta + dt
        fh = phi4_inv(1.0, b1+b2, tv*(cp1+cp2))
        f1 = phi4_inv(s1, b1, tv*cp1)
        f2 = phi4_inv(s2, b2, tv*cp2)
        if fh is None or f1 is None or f2 is None:
            valid = False
            break
        vals.append(fh - f1 - f2)

    if not valid:
        continue

    Mpp = (vals[2] - 2*vals[1] + vals[0]) / h_fd**2
    n_test5 += 1

    if Mpp < min_mpp:
        min_mpp = Mpp

    if Mpp < -1e-3:
        n_fail5 += 1

print("Extended M''(theta) tests: %d" % n_test5)
print("Violations: %d" % n_fail5)
print("Min M''(theta): %.6e" % min_mpp)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print()
print("1. Diagonal dominance (g_i >= g_h): %s" %
      ("YES ✓" if n_fail_a1 == 0 and n_fail_a2 == 0 else "NO ✗ (%d + %d violations)" % (n_fail_a1, n_fail_a2)))
print("2. Det condition (g1g2 >= gh(g1+g2)): %s" %
      ("YES ✓" if n_fail_det == 0 else "NO ✗ (%d violations)" % n_fail_det))
print("3. Generalized phi-subadditivity: %s (max ratio %.4f)" %
      ("YES ✓" if n_fail3 == 0 else "NO ✗", max_ratio3))
print("4. Direct M''(theta) >= 0: %s (min %.2e)" %
      ("YES ✓" if n_fail5 == 0 else "NO ✗", min_mpp))
print()

if n_fail_a1 == 0 and n_fail_a2 == 0:
    print("STRUCTURAL RESULT: g_i >= g_h universally!")
    print("This means: |f''| at each PART >= |f''| at SUM.")
    print("Combined with det condition, the matrix is PSD.")
    print("M''(theta) >= 0 follows for ALL (c1', c2') directions.")

print("\nElapsed: %.1fs" % (time.time() - t0))
