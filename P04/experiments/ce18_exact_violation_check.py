"""
ce18_exact_violation_check.py — Exact Fraction arithmetic verification of
CE-17b superadditivity violations.

CE-17b found min M = -4.11e-03 at (s1=0.3, s2=0.5, b1=-0.05, b2=-0.05, c1=0.04, c2~0).
This script uses SymPy Rational arithmetic to determine if M < 0 is genuine
or a numerical artifact (floating-point error near Delta=0 boundary).
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import (symbols, Rational, cancel, expand, factor, simplify,
                   Poly, sign as sp_sign)
from fractions import Fraction

SEP = "=" * 70
t0 = time.time()

# Define symbolic 1/Phi_4 in (a, b, c) coordinates
a_s, b_s, c_s = symbols("a b c", real=True)
A_f = a_s**2 + 12*c_s
B_f = 2*a_s**3 - 8*a_s*c_s + 9*b_s**2
Delta = (16*a_s**4*c_s - 4*a_s**3*b_s**2 - 128*a_s**2*c_s**2
         + 144*a_s*b_s**2*c_s - 27*b_s**4 + 256*c_s**3)
inv_Phi4 = -Delta / (4 * A_f * B_f)

def eval_exact(sigma_val, b_val, cp_val):
    """Evaluate 1/Phi_4 at given (sigma, b, cp) using exact Rationals.
    Returns (value, delta, valid) where valid = (delta > 0)."""
    s = Rational(sigma_val) if not isinstance(sigma_val, Rational) else sigma_val
    bv = Rational(b_val) if not isinstance(b_val, Rational) else b_val
    cv = Rational(cp_val) if not isinstance(cp_val, Rational) else cp_val

    a_val = -s
    c_val = cv + s**2 / 12

    d = Delta.subs([(a_s, a_val), (b_s, bv), (c_s, c_val)])
    af = A_f.subs([(a_s, a_val), (b_s, bv), (c_s, c_val)])
    bf = B_f.subs([(a_s, a_val), (b_s, bv), (c_s, c_val)])

    val = None
    if af != 0 and bf != 0:
        val = -d / (4 * af * bf)

    return val, d, (d > 0)

def superadditivity_margin(s1, s2, b1, b2, c1, c2):
    """Compute M = f(s1+s2, b1+b2, c1+c2) - f(s1,b1,c1) - f(s2,b2,c2) exactly."""
    v_sum, d_sum, ok_sum = eval_exact(s1+s2, b1+b2, c1+c2)
    v1, d1, ok1 = eval_exact(s1, b1, c1)
    v2, d2, ok2 = eval_exact(s2, b2, c2)

    return {
        'M': v_sum - v1 - v2 if (v_sum is not None and v1 is not None and v2 is not None) else None,
        'v_sum': v_sum, 'v1': v1, 'v2': v2,
        'd_sum': d_sum, 'd1': d1, 'd2': d2,
        'valid': ok_sum and ok1 and ok2,
        'ok_sum': ok_sum, 'ok1': ok1, 'ok2': ok2
    }

# ============================================================
print(SEP)
print("SECTION 1: Reproduce CE-17b violations with exact arithmetic")
print(SEP)

# CE-17b used: sigma_vals = [0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
#              b_vals = np.arange(-0.3, 0.31, 0.05)
#              cp_vals = np.arange(-0.05, 0.051, 0.01)
# Reported min at approximately (0.3, 0.5, ..., ..., ..., ...)
# Let me reconstruct the exact values using Rationals

# The CE-17b min was at: (s1=0.3, s2=0.5, b1=?, b2=?, c1=?, c2=?)
# From the output: min_p = (0.3, 0.5, -0.05, -0.05, 0.04, ~0.0)
# But let me do a focused exact sweep around that region

sigma_vals = [Rational(3,10), Rational(1,2), Rational(1,1)]
b_vals_R = [Rational(i, 20) for i in range(-6, 7)]  # -0.3 to 0.3 step 0.05
cp_vals_R = [Rational(i, 100) for i in range(-5, 6)]  # -0.05 to 0.05 step 0.01

print("Grid: %d sigma × %d b × %d cp = %d points per pair" %
      (len(sigma_vals), len(b_vals_R), len(cp_vals_R), len(b_vals_R)*len(cp_vals_R)))
print("Testing all pairs of (s1,b1,c1) x (s2,b2,c2)...")
sys.stdout.flush()

min_M = None
min_params = None
neg_count = 0
total_valid = 0
neg_list = []

for s1 in sigma_vals:
    for s2 in sigma_vals:
        for b1 in b_vals_R:
            for b2 in b_vals_R:
                for c1 in cp_vals_R:
                    for c2 in cp_vals_R:
                        r = superadditivity_margin(s1, s2, b1, b2, c1, c2)
                        if not r['valid'] or r['M'] is None:
                            continue
                        total_valid += 1
                        M = r['M']
                        if min_M is None or M < min_M:
                            min_M = M
                            min_params = (s1, s2, b1, b2, c1, c2)
                        if M < 0:
                            neg_count += 1
                            if len(neg_list) < 20:
                                neg_list.append((float(M), s1, s2, b1, b2, c1, c2))

elapsed = time.time() - t0
print("\nExact sweep complete (%.1fs)" % elapsed)
print("Valid evaluations: %d" % total_valid)
print("Negative count: %d" % neg_count)
if min_M is not None:
    print("Min M (exact rational): %s" % min_M)
    print("Min M (float): %.15e" % float(min_M))
    print("At: s1=%s, s2=%s, b1=%s, b2=%s, c1=%s, c2=%s" % min_params)
    print("Sign of min M: %s" % ("NEGATIVE => GENUINE VIOLATION" if min_M < 0 else "NON-NEGATIVE => OK"))
print("ALL M >= 0?", "YES" if neg_count == 0 else "NO (%d violations)" % neg_count)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Detail on violations (if any)")
print(SEP)

if neg_list:
    print("Listing up to 20 violations:")
    for i, (mf, s1, s2, b1, b2, c1, c2) in enumerate(neg_list):
        print("\n--- Violation %d ---" % (i+1))
        print("  s1=%s, s2=%s, b1=%s, b2=%s, c1=%s, c2=%s" % (s1,s2,b1,b2,c1,c2))
        r = superadditivity_margin(s1, s2, b1, b2, c1, c2)
        print("  M = %s = %.15e" % (r['M'], float(r['M'])))
        print("  Delta_sum = %s (>0: %s)" % (r['d_sum'], r['d_sum'] > 0))
        print("  Delta_1   = %s (>0: %s)" % (r['d1'], r['d1'] > 0))
        print("  Delta_2   = %s (>0: %s)" % (r['d2'], r['d2'] > 0))
        print("  v_sum = %s = %.10e" % (r['v_sum'], float(r['v_sum'])))
        print("  v1    = %s = %.10e" % (r['v1'], float(r['v1'])))
        print("  v2    = %s = %.10e" % (r['v2'], float(r['v2'])))
else:
    print("No violations found => superadditivity holds on this grid.")

# ============================================================
print("\n" + SEP)
print("SECTION 3: Boundary proximity check")
print(SEP)
print("For each violation, checking how close Delta values are to 0...")

if neg_list:
    for i, (mf, s1, s2, b1, b2, c1, c2) in enumerate(neg_list[:5]):
        r = superadditivity_margin(s1, s2, b1, b2, c1, c2)
        print("\nViolation %d:" % (i+1))
        for label, d in [("sum", r['d_sum']), ("1", r['d1']), ("2", r['d2'])]:
            df = float(d)
            print("  Delta_%s = %.6e (boundary proximity: %s)" %
                  (label, df, "VERY CLOSE" if abs(df) < 1e-3 else
                   "CLOSE" if abs(df) < 1e-1 else "FAR"))

# ============================================================
print("\n" + SEP)
print("SECTION 4: Extended exact sweep with finer b,cp grid")
print(SEP)
print("Widening sigma range, using Rational(1,10) step for b...")

# Larger sweep with more sigma values
sigma_ext = [Rational(3,10), Rational(1,2), Rational(1,1), Rational(3,2), Rational(2,1)]
b_fine = [Rational(i, 10) for i in range(-3, 4)]  # -0.3 to 0.3 step 0.1 (coarser but wider)
cp_fine = [Rational(i, 100) for i in range(-5, 6)]  # same cp range

min_M2 = None
neg2 = 0
tot2 = 0

for s1 in sigma_ext:
    for s2 in sigma_ext:
        for b1 in b_fine:
            for b2 in b_fine:
                for c1 in cp_fine:
                    for c2 in cp_fine:
                        r = superadditivity_margin(s1, s2, b1, b2, c1, c2)
                        if not r['valid'] or r['M'] is None:
                            continue
                        tot2 += 1
                        M = r['M']
                        if min_M2 is None or M < min_M2:
                            min_M2 = M
                        if M < 0:
                            neg2 += 1

print("Extended sweep: %d valid, %d negative" % (tot2, neg2))
if min_M2 is not None:
    print("Min M: %s = %.15e" % (min_M2, float(min_M2)))
print("ALL M >= 0?", "YES" if neg2 == 0 else "NO (%d violations)" % neg2)

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
print()
if neg_count > 0:
    print("*** CRITICAL: Exact arithmetic confirms %d GENUINE violations." % neg_count)
    print("    The superadditivity inequality 1/Phi_4(X+Y) >= 1/Phi_4(X) + 1/Phi_4(Y)")
    print("    is FALSE for general n=4 (b != 0).")
    print("    P04 answer for n=4 general case: DISPROVED.")
else:
    print("*** No violations found with exact arithmetic on this grid.")
    print("    CE-17b float violations were likely numerical artifacts.")
    print("    Superadditivity may still hold — need wider/finer sweep or proof.")
