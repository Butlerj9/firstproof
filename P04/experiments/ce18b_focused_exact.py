"""
ce18b_focused_exact.py — Focused exact-arithmetic test of CE-17b violations.

CE-17b reported 4 negative M values from 508,260 valid evaluations.
Min M = -4.11e-03 at (s1=0.3, s2=0.5, b1=-0.05, b2=-0.05, c1=0.04, c2=~0.0).

This script:
1. Reconstructs the exact CE-17b grid to find the 4 violation points
2. Verifies each with exact SymPy Rational arithmetic
3. Determines if violations are genuine or numerical artifacts
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import Rational, symbols, cancel, expand

SEP = "=" * 70
t0 = time.time()

# Define 1/Phi_4 symbolically
a_s, b_s, c_s = symbols("a b c")
A_f = a_s**2 + 12*c_s
B_f = 2*a_s**3 - 8*a_s*c_s + 9*b_s**2
Delta = (16*a_s**4*c_s - 4*a_s**3*b_s**2 - 128*a_s**2*c_s**2
         + 144*a_s*b_s**2*c_s - 27*b_s**4 + 256*c_s**3)

def eval_exact(sigma, bv, cpv):
    """Evaluate 1/Phi_4 and Delta at (sigma, b, cp) using exact Rationals."""
    av = -sigma
    cv = cpv + sigma**2 / 12

    d = (16*av**4*cv - 4*av**3*bv**2 - 128*av**2*cv**2
         + 144*av*bv**2*cv - 27*bv**4 + 256*cv**3)
    af = av**2 + 12*cv
    bf = 2*av**3 - 8*av*cv + 9*bv**2

    if af == 0 or bf == 0:
        return None, d
    return -d / (4 * af * bf), d

def test_margin(s1, s2, b1, b2, c1, c2):
    """Test superadditivity margin M = f(sum) - f(1) - f(2) with exact arithmetic."""
    v_sum, d_sum = eval_exact(s1+s2, b1+b2, c1+c2)
    v1, d1 = eval_exact(s1, b1, c1)
    v2, d2 = eval_exact(s2, b2, c2)

    all_valid = (d_sum > 0 and d1 > 0 and d2 > 0)
    M = None
    if v_sum is not None and v1 is not None and v2 is not None:
        M = v_sum - v1 - v2

    return M, d_sum, d1, d2, all_valid

# ============================================================
print(SEP)
print("SECTION 1: Reconstruct CE-17b grid candidates")
print(SEP)

# CE-17b grid parameters (as Rationals):
# sigma_vals = [0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
# b_vals = np.arange(-0.3, 0.31, 0.05) => 13 values
# cp_vals = np.arange(-0.05, 0.051, 0.01) => 11 values
# Min reported at approximately (0.3, 0.5, -0.05, -0.05, 0.04, 0.0)

# First, let's just test the reported approximate min point
print("\nTesting reported min point (approximate):")
candidates = [
    (Rational(3,10), Rational(1,2), Rational(-1,20), Rational(-1,20), Rational(4,100), Rational(0)),
    (Rational(3,10), Rational(1,2), Rational(-1,20), Rational(-1,20), Rational(4,100), Rational(1,100)),
    (Rational(3,10), Rational(1,2), Rational(-1,20), Rational(-1,20), Rational(4,100), Rational(-1,100)),
    (Rational(3,10), Rational(1,2), Rational(-1,20), Rational(-1,20), Rational(5,100), Rational(0)),
    (Rational(3,10), Rational(1,2), Rational(-1,20), Rational(-1,20), Rational(3,100), Rational(0)),
    # Try more b combos near min
    (Rational(3,10), Rational(1,2), Rational(0), Rational(-1,10), Rational(4,100), Rational(0)),
    (Rational(3,10), Rational(1,2), Rational(-1,10), Rational(0), Rational(4,100), Rational(0)),
    (Rational(3,10), Rational(1,2), Rational(1,20), Rational(-3,20), Rational(4,100), Rational(0)),
]

print("\n%3s  %5s %5s %6s %6s %6s %6s | %12s | %5s %5s %5s | %s" %
      ("#", "s1", "s2", "b1", "b2", "c1", "c2", "M(float)", "Ds", "D1", "D2", "Valid"))
print("-" * 100)

for i, (s1,s2,b1,b2,c1,c2) in enumerate(candidates):
    M, ds, d1, d2, valid = test_margin(s1,s2,b1,b2,c1,c2)
    mf = float(M) if M is not None else float('nan')
    print("%3d  %5s %5s %6s %6s %6s %6s | %12.6e | %5s %5s %5s | %s" %
          (i+1, s1, s2, b1, b2, c1, c2, mf,
           "+" if ds>0 else "-", "+" if d1>0 else "-", "+" if d2>0 else "-",
           "VALID" if valid else "INVALID"))
    if valid and M is not None and M < 0:
        print("  *** GENUINE VIOLATION: M = %s (exact)" % M)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Systematic search near reported min")
print(SEP)
print("Scanning small region around (s=0.3/0.5, b~-0.05, cp~0.04)...")

sigma_test = [Rational(3,10), Rational(1,2)]
b_test = [Rational(i,20) for i in range(-6, 7)]  # -0.3 to 0.3 step 0.05
cp_test = [Rational(i,100) for i in range(-5, 6)]  # -0.05 to 0.05 step 0.01

min_M = None
min_params = None
neg_count = 0
total_valid = 0

for s1 in sigma_test:
    for s2 in sigma_test:
        for b1 in b_test:
            for b2 in b_test:
                for c1 in cp_test:
                    for c2 in cp_test:
                        M, ds, d1, d2, valid = test_margin(s1,s2,b1,b2,c1,c2)
                        if not valid or M is None:
                            continue
                        total_valid += 1
                        if min_M is None or M < min_M:
                            min_M = M
                            min_params = (s1, s2, b1, b2, c1, c2)
                        if M < 0:
                            neg_count += 1

print("Valid evaluations: %d" % total_valid)
print("Negative: %d" % neg_count)
if min_M is not None:
    print("Min M: %.15e (exact: %s...)" % (float(min_M), str(min_M)[:80]))
    print("At: %s" % (min_params,))
    if min_M < 0:
        print("*** GENUINE VIOLATION with exact arithmetic!")
    else:
        print("ALL M >= 0 (no violations)")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Extend to wider sigma range")
print(SEP)

sigma_ext = [Rational(3,10), Rational(1,2), Rational(1), Rational(3,2), Rational(2)]
b_coarse = [Rational(i,10) for i in range(-3, 4)]  # step 0.1
cp_coarse = [Rational(i,50) for i in range(-2, 3)]  # step 0.02

min_M3 = None
neg3 = 0
tot3 = 0

for s1 in sigma_ext:
    for s2 in sigma_ext:
        for b1 in b_coarse:
            for b2 in b_coarse:
                for c1 in cp_coarse:
                    for c2 in cp_coarse:
                        M, ds, d1, d2, valid = test_margin(s1,s2,b1,b2,c1,c2)
                        if not valid or M is None:
                            continue
                        tot3 += 1
                        if min_M3 is None or M < min_M3:
                            min_M3 = M
                        if M < 0:
                            neg3 += 1

print("Valid evaluations: %d" % tot3)
print("Negative: %d" % neg3)
if min_M3 is not None:
    print("Min M: %.15e" % float(min_M3))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Direct boundary analysis")
print(SEP)
print("Checking if violations cluster near Delta=0 boundary...")

# Take the CE-17b min point and check Delta values
for s1,s2,b1,b2,c1,c2 in candidates[:5]:
    M, ds, d1, d2, valid = test_margin(s1,s2,b1,b2,c1,c2)
    if valid and M is not None:
        print("\n(s1=%s,s2=%s,b1=%s,b2=%s,c1=%s,c2=%s)" % (s1,s2,b1,b2,c1,c2))
        print("  M = %.10e" % float(M))
        print("  Delta_sum = %.6e" % float(ds))
        print("  Delta_1   = %.6e" % float(d1))
        print("  Delta_2   = %.6e" % float(d2))
        print("  min(Deltas) = %.6e" % min(float(ds), float(d1), float(d2)))

# ============================================================
print("\n" + SEP)
print("SECTION 5: b=0 verification (known to hold)")
print(SEP)
print("Testing superadditivity with b1=b2=0 (should all pass)...")

neg_b0 = 0
tot_b0 = 0
min_b0 = None
for s1 in [Rational(3,10), Rational(1,2), Rational(1), Rational(2), Rational(3), Rational(5)]:
    for s2 in [Rational(3,10), Rational(1,2), Rational(1), Rational(2), Rational(3), Rational(5)]:
        for c1 in [Rational(i,100) for i in range(-5, 6)]:
            for c2 in [Rational(i,100) for i in range(-5, 6)]:
                M, ds, d1, d2, valid = test_margin(s1, s2, Rational(0), Rational(0), c1, c2)
                if not valid or M is None:
                    continue
                tot_b0 += 1
                if min_b0 is None or M < min_b0:
                    min_b0 = M
                if M < 0:
                    neg_b0 += 1

print("b=0 valid: %d, negative: %d, min M: %.10e" % (tot_b0, neg_b0, float(min_b0) if min_b0 else 0))

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
print()
print("Section 2 (focused s={0.3,0.5}):")
print("  Valid: %d, Negative: %d" % (total_valid, neg_count))
if min_M is not None:
    print("  Min M: %.15e" % float(min_M))
print("Section 3 (wider sigma):")
print("  Valid: %d, Negative: %d" % (tot3, neg3))
print("Section 5 (b=0 control):")
print("  Valid: %d, Negative: %d" % (tot_b0, neg_b0))
print()
if neg_count == 0 and neg3 == 0:
    print("*** NO VIOLATIONS found with exact arithmetic.")
    print("    CE-17b violations were numerical artifacts (boundary proximity).")
elif neg_count > 0 or neg3 > 0:
    print("*** GENUINE VIOLATIONS confirmed with exact arithmetic!")
    print("    Superadditivity of 1/Phi_4 is FALSE for b != 0.")
