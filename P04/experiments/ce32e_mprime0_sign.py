"""
ce32e_mprime0_sign.py — Test sign of M'(0).

M(theta) = 1/Phi4(1, bh, theta*cph) - 1/Phi4(w, b1, theta*cp1) - 1/Phi4(1-w, b2, theta*cp2)

M'(0) = cph * f'(1, bh, 0) - cp1 * f'(w, b1, 0) - cp2 * f'(1-w, b2, 0)

where f'(sigma, b, 0) = [d(1/Phi4)/dc']|_{c'=0}.

Since cph = cp1 + cp2:
M'(0) = cp1*(f'h - f'1) + cp2*(f'h - f'2)

KEY OBSERVATION: If f'h >= f'1 and f'h >= f'2 always, then:
- For cp1,cp2 >= 0: M'(0) >= 0  =>  M(theta) >= M(0) >= 0 by convexity.
- For mixed signs: need more analysis.

But if M'(0) >= 0 universally (for ALL valid cp1,cp2,b1,b2,w),
then with M convex => M(theta) >= M(0) >= 0 for all theta >= 0.

This script:
1. Computes f'(sigma, b, 0) symbolically
2. Tests M'(0) sign numerically
3. Tests f'h vs f'1, f'h vs f'2 comparisons
"""
import sys, io, time
import numpy as np
from fractions import Fraction
from sympy import (symbols, diff, simplify, factor, cancel, expand,
                   numer, denom, Rational, Poly)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

# ============================================================
print(SEP)
print("SECTION 1: Compute f'(sigma, b, 0) = d(1/Phi4)/dc' at c'=0")
print(SEP)
sys.stdout.flush()

sigma, b, cp = symbols('sigma b cp', real=True)

a = -sigma
c = sigma**2 / 12 + cp

A = a**2 + 12*c  # = 2*sigma^2 + 12*cp
B = 2*a**3 - 8*a*c + 9*b**2
Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
         + 144*a*b**2*c - 27*b**4 + 256*c**3)
f = -Delta / (4*A*B)

f_prime_cp = diff(f, cp)
f_prime_at_0 = cancel(f_prime_cp.subs(cp, 0))

num_fp = numer(f_prime_at_0)
den_fp = denom(f_prime_at_0)

print("f'(sigma, b, 0) = Num/Den where:")
print("  Num =", factor(num_fp))
print("  Den =", factor(den_fp))
sys.stdout.flush()

# Scale-invariant form: substitute b^2 = beta*sigma^3
beta = symbols('beta', nonneg=True)
num_fp_sub = expand(num_fp.subs(b**2, beta*sigma**3))
den_fp_sub = expand(den_fp.subs(b**2, beta*sigma**3))

# Factor out sigma powers
print("\nScale-invariant substitution b^2 = beta*sigma^3:")
num_fp_sub_fac = factor(num_fp_sub)
den_fp_sub_fac = factor(den_fp_sub)
print("  Num =", num_fp_sub_fac)
print("  Den =", den_fp_sub_fac)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Compare f'_h vs f'_1 — is f'(1,bh,0) >= f'(w,b1,0)?")
print(SEP)
sys.stdout.flush()

def f_prime_val(sig_v, b_v):
    """Evaluate f'(sigma, b, 0) numerically."""
    return float(f_prime_at_0.subs([(sigma, sig_v), (b, b_v)]))

# Numerical comparison
np.random.seed(42)
n_comp = 0
n_fp_h_ge_fp1 = 0
n_fp_h_ge_fp2 = 0
n_fp_h_lt_fp1 = 0
n_fp_h_lt_fp2 = 0

for _ in range(50000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv
    s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v

    # Validity check for sum
    if 27*bhv**2 >= 4*0.99:
        continue

    try:
        fp_h = f_prime_val(1.0, bhv)
        fp_1 = f_prime_val(s1, b1v)
        fp_2 = f_prime_val(s2, b2v)
    except:
        continue

    n_comp += 1
    if fp_h >= fp_1:
        n_fp_h_ge_fp1 += 1
    else:
        n_fp_h_lt_fp1 += 1
    if fp_h >= fp_2:
        n_fp_h_ge_fp2 += 1
    else:
        n_fp_h_lt_fp2 += 1

print("Comparison f'_h vs f'_1: %d tests" % n_comp)
print("  f'_h >= f'_1: %d (%.1f%%)" % (n_fp_h_ge_fp1, 100*n_fp_h_ge_fp1/max(1,n_comp)))
print("  f'_h < f'_1:  %d (%.1f%%)" % (n_fp_h_lt_fp1, 100*n_fp_h_lt_fp1/max(1,n_comp)))
print("  f'_h >= f'_2: %d (%.1f%%)" % (n_fp_h_ge_fp2, 100*n_fp_h_ge_fp2/max(1,n_comp)))
print("  f'_h < f'_2:  %d (%.1f%%)" % (n_fp_h_lt_fp2, 100*n_fp_h_lt_fp2/max(1,n_comp)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Test M'(0) sign directly")
print(SEP)
sys.stdout.flush()

np.random.seed(123)
n_mp = 0
n_mp_pos = 0
n_mp_neg = 0
min_mp = float('inf')
worst_mp = None

for trial in range(200000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv
    s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v

    if 27*bhv**2 >= 4*0.95:
        continue

    # Random c' values (small to moderate)
    cp1v = np.random.uniform(-0.1, 0.1)
    cp2v = np.random.uniform(-0.1, 0.1)
    cphv = cp1v + cp2v

    # Check validity at theta=0 (c'=0 is always valid if beta < 4/27)
    # But check validity at theta=1 too
    a1 = -s1; c1 = s1**2/12 + cp1v
    A1 = a1**2 + 12*c1; B1 = 2*a1**3 - 8*a1*c1 + 9*b1v**2
    D1 = 16*a1**4*c1 - 4*a1**3*b1v**2 - 128*a1**2*c1**2 + 144*a1*b1v**2*c1 - 27*b1v**4 + 256*c1**3
    if D1 <= 0 or A1*B1 >= 0:
        continue

    a2 = -s2; c2 = s2**2/12 + cp2v
    A2 = a2**2 + 12*c2; B2 = 2*a2**3 - 8*a2*c2 + 9*b2v**2
    D2 = 16*a2**4*c2 - 4*a2**3*b2v**2 - 128*a2**2*c2**2 + 144*a2*b2v**2*c2 - 27*b2v**4 + 256*c2**3
    if D2 <= 0 or A2*B2 >= 0:
        continue

    ah = -1; ch = 1.0/12 + cphv
    Ah = ah**2 + 12*ch; Bh = 2*ah**3 - 8*ah*ch + 9*bhv**2
    Dh = 16*ah**4*ch - 4*ah**3*bhv**2 - 128*ah**2*ch**2 + 144*ah*bhv**2*ch - 27*bhv**4 + 256*ch**3
    if Dh <= 0 or Ah*Bh >= 0:
        continue

    try:
        fp_h = f_prime_val(1.0, bhv)
        fp_1 = f_prime_val(s1, b1v)
        fp_2 = f_prime_val(s2, b2v)
    except:
        continue

    # M'(0) = cph * fp_h - cp1 * fp_1 - cp2 * fp_2
    mp0 = cphv * fp_h - cp1v * fp_1 - cp2v * fp_2

    n_mp += 1
    if mp0 >= -1e-12:
        n_mp_pos += 1
    else:
        n_mp_neg += 1

    if mp0 < min_mp:
        min_mp = mp0
        worst_mp = (wv, b1v, b2v, cp1v, cp2v, fp_h, fp_1, fp_2)

    if trial % 50000 == 49999:
        print("  %d trials, %d valid, %d neg, min=%.6e, elapsed %.1fs" %
              (trial+1, n_mp, n_mp_neg, min_mp, time.time()-t0))
        sys.stdout.flush()

print("\nM'(0) sign test: %d valid" % n_mp)
print("  M'(0) >= 0: %d (%.1f%%)" % (n_mp_pos, 100*n_mp_pos/max(1,n_mp)))
print("  M'(0) < 0:  %d (%.1f%%)" % (n_mp_neg, 100*n_mp_neg/max(1,n_mp)))
print("  Min M'(0): %.6e" % min_mp)

if worst_mp and n_mp_neg > 0:
    w, b1, b2, cp1, cp2, fph, fp1, fp2 = worst_mp
    print("  Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.4f cp2=%.4f" % (w, b1, b2, cp1, cp2))
    print("    f'_h=%.6f f'_1=%.6f f'_2=%.6f" % (fph, fp1, fp2))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Alternative — test f'(sigma,b,0) as function of sigma")
print("Does f'(sigma,b,0) increase with sigma (for fixed beta)?")
print(SEP)
sys.stdout.flush()

# f'(sigma, b, 0) in scale-invariant form:
# f' should scale as sigma^{-k} for some k, times a function of beta.
# Let's check: f'(lambda*sigma, lambda^{3/2}*b, 0) = lambda^? * f'(sigma,b,0)

# Test numerically
print("\nHomogeneity test:")
for lam in [2.0, 0.5, 3.0]:
    sig0, b0 = 1.0, 0.3
    fp_orig = f_prime_val(sig0, b0)
    fp_scaled = f_prime_val(lam*sig0, lam**1.5 * b0)
    if abs(fp_orig) > 1e-15:
        ratio = fp_scaled / fp_orig
        print("  lambda=%.1f: f'(lam*s, lam^1.5*b) / f'(s,b) = %.6f (lambda^? = %.6f)" %
              (lam, ratio, ratio))
        # Check if ratio is a power of lambda
        import math
        power = math.log(abs(ratio)) / math.log(lam)
        print("    => power = %.3f" % power)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Test sign of f'(sigma,b,0)")
print("Is f' always positive? Or sign-changing?")
print(SEP)
sys.stdout.flush()

n_fpos = 0
n_fneg = 0
n_ftest = 0
for _ in range(100000):
    sig_v = np.random.uniform(0.1, 3.0)
    b_max = (4*sig_v**3/27)**0.5 * 0.95
    b_v = np.random.uniform(-b_max, b_max)
    fp = f_prime_val(sig_v, b_v)
    n_ftest += 1
    if fp > 0:
        n_fpos += 1
    elif fp < 0:
        n_fneg += 1

print("f'(sigma,b,0) sign: %d tests" % n_ftest)
print("  Positive: %d (%.1f%%)" % (n_fpos, 100*n_fpos/max(1,n_ftest)))
print("  Negative: %d (%.1f%%)" % (n_fneg, 100*n_fneg/max(1,n_ftest)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: If M'(0) can be negative, test M'(0) >= 0 for SAME-SIGN c'")
print(SEP)
sys.stdout.flush()

# When cp1, cp2 >= 0 (same sign), M'(0) = cp1*(fph-fp1) + cp2*(fph-fp2)
# So M'(0) >= 0 iff fph >= fp1 and fph >= fp2 (which we tested in Section 2).
# But if fph < fp1 sometimes, then cp1 > 0 can make the first term negative.

# Test: For same-sign c', is M'(0) >= 0?
np.random.seed(456)
n_ss = 0
n_ss_neg = 0
min_ss = float('inf')

for _ in range(100000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v
    if 27*bhv**2 >= 4*0.95:
        continue

    # Same-sign c' (both positive)
    cp1v = np.random.uniform(0, 0.1)
    cp2v = np.random.uniform(0, 0.1)

    # Check validity at theta=1
    a1 = -s1; c1 = s1**2/12 + cp1v
    A1 = a1**2 + 12*c1; B1 = 2*a1**3 - 8*a1*c1 + 9*b1v**2
    D1 = 16*a1**4*c1 - 4*a1**3*b1v**2 - 128*a1**2*c1**2 + 144*a1*b1v**2*c1 - 27*b1v**4 + 256*c1**3
    if D1 <= 0 or A1*B1 >= 0:
        continue

    a2 = -s2; c2 = s2**2/12 + cp2v
    A2 = a2**2 + 12*c2; B2 = 2*a2**3 - 8*a2*c2 + 9*b2v**2
    D2 = 16*a2**4*c2 - 4*a2**3*b2v**2 - 128*a2**2*c2**2 + 144*a2*b2v**2*c2 - 27*b2v**4 + 256*c2**3
    if D2 <= 0 or A2*B2 >= 0:
        continue

    cphv = cp1v + cp2v
    ah = -1; ch = 1.0/12 + cphv
    Ah = ah**2 + 12*ch; Bh = 2*ah**3 - 8*ah*ch + 9*bhv**2
    Dh = 16*ah**4*ch - 4*ah**3*bhv**2 - 128*ah**2*ch**2 + 144*ah*bhv**2*ch - 27*bhv**4 + 256*ch**3
    if Dh <= 0 or Ah*Bh >= 0:
        continue

    try:
        fp_h = f_prime_val(1.0, bhv)
        fp_1 = f_prime_val(s1, b1v)
        fp_2 = f_prime_val(s2, b2v)
    except:
        continue

    mp0 = cphv * fp_h - cp1v * fp_1 - cp2v * fp_2
    n_ss += 1
    if mp0 < -1e-12:
        n_ss_neg += 1
    if mp0 < min_ss:
        min_ss = mp0

print("Same-sign c' tests: %d valid" % n_ss)
print("  M'(0) < 0: %d" % n_ss_neg)
print("  Min M'(0): %.6e" % min_ss)
sys.stdout.flush()

# Similarly for both negative c'
np.random.seed(789)
n_sn = 0
n_sn_neg = 0
min_sn = float('inf')

for _ in range(100000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v
    if 27*bhv**2 >= 4*0.95:
        continue

    cp1v = np.random.uniform(-0.1, 0)
    cp2v = np.random.uniform(-0.1, 0)

    a1 = -s1; c1 = s1**2/12 + cp1v
    A1 = a1**2 + 12*c1; B1 = 2*a1**3 - 8*a1*c1 + 9*b1v**2
    D1 = 16*a1**4*c1 - 4*a1**3*b1v**2 - 128*a1**2*c1**2 + 144*a1*b1v**2*c1 - 27*b1v**4 + 256*c1**3
    if D1 <= 0 or A1*B1 >= 0:
        continue

    a2 = -s2; c2 = s2**2/12 + cp2v
    A2 = a2**2 + 12*c2; B2 = 2*a2**3 - 8*a2*c2 + 9*b2v**2
    D2 = 16*a2**4*c2 - 4*a2**3*b2v**2 - 128*a2**2*c2**2 + 144*a2*b2v**2*c2 - 27*b2v**4 + 256*c2**3
    if D2 <= 0 or A2*B2 >= 0:
        continue

    cphv = cp1v + cp2v
    ah = -1; ch = 1.0/12 + cphv
    Ah = ah**2 + 12*ch; Bh = 2*ah**3 - 8*ah*ch + 9*bhv**2
    Dh = 16*ah**4*ch - 4*ah**3*bhv**2 - 128*ah**2*ch**2 + 144*ah*bhv**2*ch - 27*bhv**4 + 256*ch**3
    if Dh <= 0 or Ah*Bh >= 0:
        continue

    try:
        fp_h = f_prime_val(1.0, bhv)
        fp_1 = f_prime_val(s1, b1v)
        fp_2 = f_prime_val(s2, b2v)
    except:
        continue

    mp0 = cphv * fp_h - cp1v * fp_1 - cp2v * fp_2
    n_sn += 1
    if mp0 < -1e-12:
        n_sn_neg += 1
    if mp0 < min_sn:
        min_sn = mp0

print("\nBoth negative c' tests: %d valid" % n_sn)
print("  M'(0) < 0: %d" % n_sn_neg)
print("  Min M'(0): %.6e" % min_sn)
sys.stdout.flush()

print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("If M'(0) >= 0 universally: PROOF CLOSES via convexity + M(0) >= 0")
print("  (M convex + M'(0) >= 0 => M increasing => M(theta) >= M(0) >= 0)")
print("If M'(0) can be < 0: need full discriminant chain")
print("\nElapsed: %.1fs" % (time.time() - t0))
