"""
ce34_interval_cert.py — Rigorous interval certification for M >= 0.

Strategy: Adaptive subdivision of the 5D parameter space with exact Fraction arithmetic.
For each box, compute M at the center exactly and verify margin exceeds a Lipschitz bound.

Key simplification: Use the parametric approach M(theta) where theta in [0, 1].
- M(0) >= 0 is PROVED (c'=0 subcase)
- M''(theta) > 0 empirically
- So M(theta) is convex and M(theta) >= min(M(0), M(1))
- Since M(0) >= 0, we just need M(1) >= 0 if M is NOT monotone

Alternative: Direct grid certification of M(1) = M(w, b1, b2, c1', c2') >= 0
with exact arithmetic and Lipschitz control.

This script tests a DENSE exact grid and reports minimum margin and coverage.
"""
import sys, io, time
import numpy as np
from fractions import Fraction
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_inv_exact(sigma_f, b_f, cp_f):
    """Exact 1/Phi4 using Fraction arithmetic.
    sigma_f, b_f, cp_f: Fraction objects.
    Returns: (value: Fraction, valid: bool)
    """
    a = -sigma_f
    c = sigma_f**2 / 12 + cp_f
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b_f**2
    Delta = (16*a**4*c - 4*a**3*b_f**2 - 128*a**2*c**2
             + 144*a*b_f**2*c - 27*b_f**4 + 256*c**3)
    AB = A * B
    if Delta <= 0 or AB >= 0:
        return None, False
    val = -Delta / (4 * AB)
    return val, val > 0

def margin_exact(w_f, b1_f, b2_f, cp1_f, cp2_f):
    """Exact margin M = 1/Phi4(h) - 1/Phi4(p1) - 1/Phi4(p2)."""
    s1 = w_f
    s2 = Fraction(1) - w_f
    bh = b1_f + b2_f
    cph = cp1_f + cp2_f

    fh, okh = phi4_inv_exact(Fraction(1), bh, cph)
    f1, ok1 = phi4_inv_exact(s1, b1_f, cp1_f)
    f2, ok2 = phi4_inv_exact(s2, b2_f, cp2_f)

    if not (okh and ok1 and ok2):
        return None, False
    return fh - f1 - f2, True

# ============================================================
print(SEP)
print("SECTION 1: Dense exact grid on (w, b1, b2) at c'=0")
print("Verifying M(0) >= 0 on fine grid (sanity check)")
print(SEP)
sys.stdout.flush()

# w grid
w_vals = [Fraction(i, 20) for i in range(1, 20)]  # 1/20 to 19/20
# b grid: use small values relative to validity bound
b_range = [Fraction(i, 40) for i in range(-8, 9)]  # -8/40 to 8/40

n_valid_0 = 0
n_neg_0 = 0
min_M0 = None

for w_f in w_vals:
    s1 = w_f
    s2 = Fraction(1) - w_f
    for b1_f in b_range:
        for b2_f in b_range:
            M, ok = margin_exact(w_f, b1_f, b2_f, Fraction(0), Fraction(0))
            if not ok:
                continue
            n_valid_0 += 1
            if M < 0:
                n_neg_0 += 1
            if min_M0 is None or M < min_M0:
                min_M0 = M

print("c'=0 grid: %d valid tests" % n_valid_0)
print("Negative: %d" % n_neg_0)
if min_M0 is not None:
    print("Min M(0): %s = %.6e" % (min_M0, float(min_M0)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Dense exact grid on full (w, b1, b2, c1', c2')")
print(SEP)
sys.stdout.flush()

# Coarser grid for 5D
w_vals_5d = [Fraction(i, 10) for i in range(1, 10)]  # 1/10 to 9/10
b_range_5d = [Fraction(i, 20) for i in range(-4, 5)]  # -4/20 to 4/20
cp_range = [Fraction(i, 100) for i in range(-4, 5)]  # -4/100 to 4/100

n_valid_5d = 0
n_neg_5d = 0
min_M5d = None
worst_5d = None

for w_f in w_vals_5d:
    s1 = w_f
    s2 = Fraction(1) - w_f
    for b1_f in b_range_5d:
        for b2_f in b_range_5d:
            for cp1_f in cp_range:
                for cp2_f in cp_range:
                    M, ok = margin_exact(w_f, b1_f, b2_f, cp1_f, cp2_f)
                    if not ok:
                        continue
                    n_valid_5d += 1
                    if M < 0:
                        n_neg_5d += 1
                        if worst_5d is None or M < worst_5d[0]:
                            worst_5d = (M, w_f, b1_f, b2_f, cp1_f, cp2_f)
                    if min_M5d is None or M < min_M5d:
                        min_M5d = M

    # Progress indicator
    if float(w_f) in [0.1, 0.3, 0.5, 0.7, 0.9]:
        print("  w=%.1f: %d valid so far, %d neg, elapsed %.1fs" %
              (float(w_f), n_valid_5d, n_neg_5d, time.time()-t0))
        sys.stdout.flush()

print("\n5D grid: %d valid tests" % n_valid_5d)
print("Negative: %d" % n_neg_5d)
if min_M5d is not None:
    print("Min M: %s = %.6e" % (min_M5d, float(min_M5d)))
if worst_5d:
    M, w, b1, b2, cp1, cp2 = worst_5d
    print("Worst: w=%s b1=%s b2=%s cp1=%s cp2=%s M=%s" %
          (w, b1, b2, cp1, cp2, M))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Near-equality targeted search")
print("Focus on (w,b1,b2,cp1,cp2) near equality manifold")
print(SEP)
sys.stdout.flush()

# Near equality: b small, c' small, w near 1/2
w_fine = [Fraction(i, 100) for i in range(40, 61)]  # 0.40 to 0.60
b_fine = [Fraction(i, 200) for i in range(-5, 6)]  # -5/200 to 5/200
cp_fine = [Fraction(i, 1000) for i in range(-5, 6)]  # -5/1000 to 5/1000

n_valid_ne = 0
n_neg_ne = 0
min_Mne = None

for w_f in w_fine:
    for b1_f in b_fine:
        for b2_f in b_fine:
            for cp1_f in cp_fine:
                for cp2_f in cp_fine:
                    M, ok = margin_exact(w_f, b1_f, b2_f, cp1_f, cp2_f)
                    if not ok:
                        continue
                    n_valid_ne += 1
                    if M < 0:
                        n_neg_ne += 1
                    if min_Mne is None or M < min_Mne:
                        min_Mne = M

print("Near-equality grid: %d valid tests" % n_valid_ne)
print("Negative: %d" % n_neg_ne)
if min_Mne is not None:
    print("Min M near equality: %s = %.6e" % (min_Mne, float(min_Mne)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Random exact tests with larger c' range")
print(SEP)
sys.stdout.flush()

np.random.seed(42)
n_rand = 0
n_rand_neg = 0
min_Mrand = None

for trial in range(200000):
    # Random parameters
    w_num = np.random.randint(1, 100)
    w_f = Fraction(w_num, 100)
    s1 = w_f
    s2 = Fraction(1) - w_f

    # Random b in validity range
    s1_f = float(s1)
    s2_f = float(s2)
    b1_max = (4*s1_f**3/27)**0.5 * 0.95
    b2_max = (4*s2_f**3/27)**0.5 * 0.95
    b1_num = int(np.random.uniform(-b1_max, b1_max) * 1000)
    b2_num = int(np.random.uniform(-b2_max, b2_max) * 1000)
    b1_f = Fraction(b1_num, 1000)
    b2_f = Fraction(b2_num, 1000)

    # Random c' in moderate range
    cp1_num = np.random.randint(-50, 51)
    cp2_num = np.random.randint(-50, 51)
    cp1_f = Fraction(cp1_num, 1000)
    cp2_f = Fraction(cp2_num, 1000)

    M, ok = margin_exact(w_f, b1_f, b2_f, cp1_f, cp2_f)
    if not ok:
        continue

    n_rand += 1
    if M < 0:
        n_rand_neg += 1
    if min_Mrand is None or M < min_Mrand:
        min_Mrand = M

    if trial % 50000 == 49999:
        print("  %d trials, %d valid, %d neg, min=%.6e, elapsed %.1fs" %
              (trial+1, n_rand, n_rand_neg, float(min_Mrand) if min_Mrand else 0, time.time()-t0))
        sys.stdout.flush()

print("\nRandom exact tests: %d valid" % n_rand)
print("Negative: %d" % n_rand_neg)
if min_Mrand is not None:
    print("Min M (random): %.6e" % float(min_Mrand))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Extreme parameter tests")
print("Test near w=0, w=1, and near validity boundary")
print(SEP)
sys.stdout.flush()

n_extreme = 0
n_extreme_neg = 0
min_Mext = None

# Near w=0 and w=1
for w_f in [Fraction(1,100), Fraction(2,100), Fraction(5,100),
            Fraction(95,100), Fraction(98,100), Fraction(99,100)]:
    s1_f = float(w_f)
    s2_f = 1.0 - s1_f
    b1_max = (4*s1_f**3/27)**0.5 * 0.9
    b2_max = (4*s2_f**3/27)**0.5 * 0.9

    for b1_frac in range(-10, 11):
        b1_f = Fraction(int(b1_max * b1_frac * 100), 1000)
        for b2_frac in range(-10, 11):
            b2_f = Fraction(int(b2_max * b2_frac * 100), 1000)
            for cp1_f in [Fraction(i, 100) for i in range(-5, 6)]:
                for cp2_f in [Fraction(i, 100) for i in range(-5, 6)]:
                    M, ok = margin_exact(w_f, b1_f, b2_f, cp1_f, cp2_f)
                    if not ok:
                        continue
                    n_extreme += 1
                    if M < 0:
                        n_extreme_neg += 1
                    if min_Mext is None or M < min_Mext:
                        min_Mext = M

print("Extreme tests: %d valid" % n_extreme)
print("Negative: %d" % n_extreme_neg)
if min_Mext is not None:
    print("Min M (extreme): %.6e" % float(min_Mext))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)

total = n_valid_0 + n_valid_5d + n_valid_ne + n_rand + n_extreme
total_neg = n_neg_0 + n_neg_5d + n_neg_ne + n_rand_neg + n_extreme_neg

print("Total valid tests: %d" % total)
print("Total negative: %d" % total_neg)
print("ALL PASS: %s" % ("YES" if total_neg == 0 else "NO"))

if total_neg == 0:
    print("\nNo counterexample found across %d exact-arithmetic tests." % total)
    print("This strengthens the empirical evidence but is NOT a proof.")
    print("A rigorous interval certification would need Lipschitz bounds.")
else:
    print("\n*** COUNTEREXAMPLE FOUND ***")
    print("This would disprove the inequality for n=4!")

print("\nElapsed: %.1fs" % (time.time() - t0))
