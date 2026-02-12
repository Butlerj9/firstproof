"""
ce19_corrected_validity.py — Corrected validity filter for quartic superadditivity.

CRITICAL BUG IN CE-17b: For quartics, Delta > 0 means 0 or 4 real roots.
Additional conditions needed to guarantee 4 real roots.

For x^4 + ax^2 + bx + c with all real simple roots:
  - Delta > 0 (necessary)
  - 1/Phi_4 > 0 (equivalently: A*B < 0 where A = a^2+12c, B = 2a^3-8ac+9b^2)

This is because Phi_4 = sum_i (sum_{j!=i} 1/(ri-rj))^2 >= 0 for real roots,
and 1/Phi_4 = -Delta/(4*A*B). With Delta > 0, positivity requires A*B < 0.

This script re-runs the superadditivity sweep with the CORRECT filter.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import Rational
import numpy as np

SEP = "=" * 70
t0 = time.time()

def eval_all(sigma, bv, cpv):
    """Evaluate 1/Phi_4, Delta, A, B at (sigma, b, cp) using exact Rationals.
    Returns (inv_phi, delta, A, B, valid) where valid = real-rooted with simple roots."""
    av = -sigma
    cv = cpv + sigma**2 / 12

    d = (16*av**4*cv - 4*av**3*bv**2 - 128*av**2*cv**2
         + 144*av*bv**2*cv - 27*bv**4 + 256*cv**3)
    af = av**2 + 12*cv
    bf = 2*av**3 - 8*av*cv + 9*bv**2

    if af == 0 or bf == 0:
        return None, d, af, bf, False

    inv_phi = -d / (4 * af * bf)

    # CORRECT validity: Delta > 0 AND 1/Phi_4 > 0 (i.e., A*B < 0)
    valid = (d > 0) and (inv_phi > 0)

    return inv_phi, d, af, bf, valid

# ============================================================
print(SEP)
print("SECTION 1: Check CE-18b 'counterexample' with corrected filter")
print(SEP)

s1, s2 = Rational(3,10), Rational(1,2)
b1, b2 = Rational(-1,20), Rational(-1,20)
c1, c2 = Rational(1,25), Rational(0)

for label, sv, bv, cv in [("p (input 1)", s1, b1, c1),
                           ("q (input 2)", s2, b2, c2),
                           ("h (convolution)", s1+s2, b1+b2, c1+c2)]:
    inv_phi, d, A, B, valid = eval_all(sv, bv, cv)
    print("\n%s: sigma=%s, b=%s, cp=%s" % (label, sv, bv, cv))
    print("  Delta = %s = %.8e (>0: %s)" % (d, float(d), d > 0))
    print("  A = %s = %.8e" % (A, float(A)))
    print("  B = %s = %.8e" % (B, float(B)))
    print("  A*B = %s = %.8e (%s)" % (A*B, float(A*B),
          "< 0 => 4 real roots" if A*B < 0 else "> 0 => 0 real roots!"))
    print("  1/Phi_4 = %s = %.8e" % (inv_phi, float(inv_phi) if inv_phi else 0))
    print("  VALID (4 simple real roots)? %s" % valid)

print("\n*** CE-18b 'counterexample' is INVALID — p has 0 real roots!")
print("*** The CE-17b filter (Delta > 0) was insufficient for quartics.")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Corrected superadditivity sweep")
print(SEP)
print("Using CORRECT filter: Delta > 0 AND 1/Phi_4 > 0")

sigma_vals = [Rational(3,10), Rational(1,2), Rational(1), Rational(3,2),
              Rational(2), Rational(3), Rational(5)]
b_vals = [Rational(i,20) for i in range(-6, 7)]  # -0.3 to 0.3 step 0.05
cp_vals = [Rational(i,100) for i in range(-5, 6)]  # -0.05 to 0.05 step 0.01

min_M = None
min_params = None
neg_count = 0
total_valid = 0
total_checked = 0
invalid_skip = 0

for s1 in sigma_vals:
    for s2 in sigma_vals:
        for b1 in b_vals:
            for b2 in b_vals:
                for c1 in cp_vals:
                    for c2 in cp_vals:
                        total_checked += 1
                        f1, d1, A1, B1, ok1 = eval_all(s1, b1, c1)
                        f2, d2, A2, B2, ok2 = eval_all(s2, b2, c2)
                        fs, ds, As, Bs, oks = eval_all(s1+s2, b1+b2, c1+c2)

                        if not (ok1 and ok2 and oks):
                            invalid_skip += 1
                            continue

                        total_valid += 1
                        M = fs - f1 - f2

                        if min_M is None or M < min_M:
                            min_M = M
                            min_params = (s1, s2, b1, b2, c1, c2)
                        if M < 0:
                            neg_count += 1

    elapsed = time.time() - t0
    print("  sigma1=%s done (%.0fs, valid so far: %d)" % (s1, elapsed, total_valid))
    sys.stdout.flush()

print("\nTotal checked: %d" % total_checked)
print("Valid (4 real simple roots for all 3): %d" % total_valid)
print("Invalid skipped: %d" % invalid_skip)
print("Negative M: %d" % neg_count)
if min_M is not None:
    print("Min M: %s = %.15e" % (min_M, float(min_M)))
    print("At: %s" % (min_params,))
    print("Sign: %s" % ("NEGATIVE => VIOLATION" if min_M < 0 else "NON-NEGATIVE => OK"))
else:
    print("No valid triples found!")
print("ALL M >= 0?", "YES" if neg_count == 0 else "NO (%d violations)" % neg_count)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: b=0 control (should all pass)")
print(SEP)

neg_b0 = 0
tot_b0 = 0
min_b0 = None
for s1 in [Rational(3,10), Rational(1,2), Rational(1), Rational(2), Rational(3), Rational(5)]:
    for s2 in [Rational(3,10), Rational(1,2), Rational(1), Rational(2), Rational(3), Rational(5)]:
        for c1 in [Rational(i,100) for i in range(-5, 6)]:
            for c2 in [Rational(i,100) for i in range(-5, 6)]:
                f1, d1, A1, B1, ok1 = eval_all(s1, Rational(0), c1)
                f2, d2, A2, B2, ok2 = eval_all(s2, Rational(0), c2)
                fs, ds, As, Bs, oks = eval_all(s1+s2, Rational(0), c1+c2)
                if not (ok1 and ok2 and oks):
                    continue
                tot_b0 += 1
                M = fs - f1 - f2
                if min_b0 is None or M < min_b0:
                    min_b0 = M
                if M < 0:
                    neg_b0 += 1

print("b=0 valid: %d, negative: %d" % (tot_b0, neg_b0))
if min_b0 is not None:
    print("Min M (b=0): %s = %.15e" % (min_b0, float(min_b0)))
print("b=0 all pass?", "YES" if neg_b0 == 0 else "NO")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Statistics on validity")
print(SEP)

# How many single-polynomial evaluations are valid?
valid_single = 0
total_single = 0
for sv in sigma_vals:
    for bv in b_vals:
        for cv in cp_vals:
            total_single += 1
            _, d, A, B, ok = eval_all(sv, bv, cv)
            if ok:
                valid_single += 1

print("Single polynomials: %d / %d valid (%.1f%%)" %
      (valid_single, total_single, 100*valid_single/total_single))

# Check specifically: how many with Delta > 0 but A*B > 0 (false positives from CE-17b)?
false_pos = 0
for sv in sigma_vals:
    for bv in b_vals:
        for cv in cp_vals:
            _, d, A, B, _ = eval_all(sv, bv, cv)
            if d > 0 and A*B > 0:  # Delta > 0 but NOT 4 real roots
                false_pos += 1

print("False positives (Delta>0, A*B>0): %d / %d (%.1f%%)" %
      (false_pos, total_single, 100*false_pos/total_single))
print("(These would have passed CE-17b's filter but are NOT real-rooted)")

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
print()
print("CE-17b bug: Delta > 0 insufficient for quartics (gives 0 or 4 real roots).")
print("Correct filter: Delta > 0 AND A*B < 0 (equivalently 1/Phi_4 > 0).")
print()
if neg_count == 0:
    print("*** With corrected filter: ALL M >= 0.")
    print("*** The 'counterexample' from CE-17b/CE-18b was from a non-real-rooted polynomial.")
    print("*** Superadditivity HOLDS on this grid for all valid (real-rooted) quartics.")
else:
    print("*** GENUINE violation confirmed even with corrected filter!")
    print("*** %d violations found." % neg_count)
