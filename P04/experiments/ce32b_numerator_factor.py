"""
ce32b_numerator_factor.py — Factor the numerator of f'' = d^2(1/Phi4)/dc'^2.

From CE-32: den(f'') = (A/2)^3 * (3B)^3 = (27/8)*(AB)^3
Numerator has 15 terms. Goal: factor it.

If f'' = Num / ((27/8)*(AB)^3), and on the valid domain AB < 0 so (AB)^3 < 0,
then f'' < 0 (concavity) iff Num > 0.
"""
import sys, io, time
from sympy import (symbols, diff, simplify, factor, cancel, expand,
                   numer, denom, Rational, Poly, collect, degree)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

sigma, b, cp = symbols('sigma b cp', real=True)

# Quartic x^4 + ax^2 + bx + c with a = -sigma, c = sigma^2/12 + cp
a = -sigma
c = sigma**2 / 12 + cp

A = a**2 + 12*c  # = 2*sigma^2 + 12*cp
B = 2*a**3 - 8*a*c + 9*b**2  # = (27b^2+24*cp*sigma-4*sigma^3)/3

# 1/Phi4 = -Delta/(4*A*B)
Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
         + 144*a*b**2*c - 27*b**4 + 256*c**3)
f = -Delta / (4*A*B)

# ============================================================
print(SEP)
print("SECTION 1: Compute and factor numerator of f''")
print(SEP)
sys.stdout.flush()

f_pp = diff(f, cp, 2)
f_pp_canc = cancel(f_pp)

num_pp = numer(f_pp_canc)
den_pp = denom(f_pp_canc)

num_exp = expand(num_pp)
den_exp = expand(den_pp)

print("Numerator terms:", len(num_exp.as_ordered_terms()))
print("Denominator terms:", len(den_exp.as_ordered_terms()))
sys.stdout.flush()

# Factor numerator
print("\nFactoring numerator...")
sys.stdout.flush()
try:
    num_fac = factor(num_exp)
    print("Numerator factored:", num_fac)
except Exception as e:
    print("Factor failed:", e)
    num_fac = num_exp
sys.stdout.flush()

# Factor denominator (should be (AB)^3 up to constant)
print("\nFactoring denominator...")
sys.stdout.flush()
den_fac = factor(den_exp)
print("Denominator factored:", den_fac)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Express f'' = Num_factored / Den_factored")
print(SEP)

# Verify the denominator factorization
A_half = expand(A/2)  # sigma^2 + 6*cp
B_triple = expand(3*B)  # 27*b^2 + 24*cp*sigma - 4*sigma^3

den_check = expand(A_half**3 * B_triple**3)
den_diff = expand(den_exp - den_check)
print("Den = (A/2)^3*(3B)^3? Diff:", den_diff)

# So f'' = Num / ((sigma^2+6cp)^3 * (27b^2+24*cp*sigma-4*sigma^3)^3)
# Since A/2 = sigma^2 + 6cp > 0 on valid domain (A > 0 is part of validity)
# And 3B = 27b^2 + 24*cp*sigma - 4*sigma^3; B < 0 on valid domain (since AB < 0 and A > 0)
# So (3B)^3 < 0, and (A/2)^3 > 0, so den < 0.
# f'' < 0 iff Num > 0 on valid domain.

print("\nSign analysis:")
print("  A/2 = sigma^2 + 6*cp > 0 (since A > 0 on valid domain)")
print("  3B = 27*b^2 + 24*cp*sigma - 4*sigma^3; B < 0 on valid domain")
print("  Den = (A/2)^3 * (3B)^3 = (+)*(−) = (−)")
print("  f'' < 0 iff Num > 0")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Analyze numerator structure")
print(SEP)

# Print the numerator as a polynomial in cp
print("\nNumerator as polynomial in c':")
num_poly_cp = Poly(num_exp, cp)
print("  Degree in c':", num_poly_cp.degree())
print("  Coefficients (in sigma, b):")
for i, coeff in enumerate(num_poly_cp.all_coeffs()):
    coeff_fac = factor(coeff)
    print("    c'^%d: %s" % (num_poly_cp.degree() - i, coeff_fac))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Numerator as polynomial in b^2")
print(SEP)

# Since f'' is even in b, numerator should be polynomial in b^2
print("Checking evenness in b...")
num_neg_b = num_exp.subs(b, -b)
diff_b = expand(num_exp - num_neg_b)
print("Num(b) - Num(-b) =", diff_b)
if diff_b == 0:
    print("CONFIRMED: Numerator is even in b")
    # Substitute b^2 = beta * sigma^3 for scale-invariant analysis
    beta = symbols('beta', positive=True)
    # Replace b^2 with beta where possible
    num_in_b2 = Poly(num_exp, b)
    print("\nDegree in b:", num_in_b2.degree())
    print("Only even powers of b present:", all(c == 0 for i, c in enumerate(num_in_b2.all_coeffs()) if (num_in_b2.degree() - i) % 2 == 1))
else:
    print("NOT even in b — unexpected!")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Evaluate at specific c' values for factoring hints")
print(SEP)

# At c'=0 (already known from CE-30):
num_at_0 = num_exp.subs(cp, 0)
num_at_0_fac = factor(num_at_0)
print("Num at c'=0:", num_at_0_fac)

# At c' = sigma^2/12 (which makes the original c = sigma^2/6):
num_at_s12 = expand(num_exp.subs(cp, sigma**2/12))
num_at_s12_fac = factor(num_at_s12)
print("Num at c'=sigma^2/12:", num_at_s12_fac)

# At b=0:
num_at_b0 = expand(num_exp.subs(b, 0))
num_at_b0_fac = factor(num_at_b0)
print("Num at b=0:", num_at_b0_fac)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Scale-invariant form")
print(SEP)

# By dimensional analysis: sigma^? * f''(sigma, b, c') depends on
# dimensionless combinations beta = b^2/sigma^3 and gamma = c'/sigma^2
beta, gamma = symbols('beta gamma', real=True)

# Substitute: b^2 = beta*sigma^3, cp = gamma*sigma^2
# f''(sigma, b, c') should be sigma^(-3) * H(beta, gamma) for some H.

# Let's verify this by computing sigma^3 * f''
sigma3_fpp = expand(sigma**3 * f_pp_canc)
sigma3_fpp_canc = cancel(sigma3_fpp)

# Now substitute b^2 -> beta*sigma^3, cp -> gamma*sigma^2
sigma3_fpp_sub = sigma3_fpp_canc.subs([(b**2, beta*sigma**3), (cp, gamma*sigma**2)])
sigma3_fpp_sub = cancel(sigma3_fpp_sub)

print("sigma^3 * f'' after substitution:")
print("  =", sigma3_fpp_sub)

# Check if sigma cancels
num_sub = numer(sigma3_fpp_sub)
den_sub = denom(sigma3_fpp_sub)
print("\nNumerator:", expand(num_sub))
print("Denominator:", expand(den_sub))
sys.stdout.flush()

# Factor the substituted form
print("\nFactoring scale-invariant numerator...")
try:
    num_sub_fac = factor(num_sub)
    print("Factored:", num_sub_fac)
except:
    print("Factor failed")
    num_sub_fac = num_sub

print("\nFactoring scale-invariant denominator...")
try:
    den_sub_fac = factor(den_sub)
    print("Factored:", den_sub_fac)
except:
    print("Factor failed")
    den_sub_fac = den_sub
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Sign of numerator on valid domain")
print(SEP)

import numpy as np

# Numerical check: compute Num at random valid points
np.random.seed(42)
n_check = 0
n_num_neg = 0
n_num_pos = 0

for _ in range(100000):
    sig = np.random.uniform(0.3, 3.0)
    b_max = (4*sig**3/27)**0.5 * 0.9
    bv = np.random.uniform(-b_max, b_max)
    cpv = np.random.uniform(-sig**2/6, sig**2/6)  # broader range

    # Check validity
    av = -sig
    cv = sig**2/12.0 + cpv
    Av = av**2 + 12*cv
    Bv = 2*av**3 - 8*av*cv + 9*bv**2
    Dv = (16*av**4*cv - 4*av**3*bv**2 - 128*av**2*cv**2
          + 144*av*bv**2*cv - 27*bv**4 + 256*cv**3)

    if Dv <= 0 or Av*Bv >= 0:
        continue

    # Evaluate numerator symbolically
    num_val = float(num_exp.subs([(sigma, sig), (b, bv), (cp, cpv)]))
    n_check += 1

    if num_val < -1e-6:
        n_num_neg += 1
    elif num_val > 1e-6:
        n_num_pos += 1

print("Numerator sign check: %d valid points" % n_check)
print("  Positive: %d (%.1f%%)" % (n_num_pos, 100*n_num_pos/max(1,n_check)))
print("  Negative: %d (%.1f%%)" % (n_num_neg, 100*n_num_neg/max(1,n_check)))
print("  Num > 0 universally: %s" % ("YES" if n_num_neg == 0 else "NO"))
sys.stdout.flush()

print("\nElapsed: %.1fs" % (time.time() - t0))
