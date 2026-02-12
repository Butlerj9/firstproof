"""
ce20_perturbative_b.py — Perturbative analysis of b!=0 case using validity constraint.

The validity constraint B < 0 forces 9b^2 < 4sigma^3/3 - 8*sigma*cp,
meaning b is constrained. Can we prove superadditivity by:
1. Showing the margin M(sigma,b,cp) is a smooth function of b near b=0
2. Using M(sigma,0,cp) >= 0 (proved, CE-16) and the constraint on b to bound the deviation

Strategy: Write M = M_0 + M_2*b + M_4*b^2 + ... and show M_2 >= 0 or M_0 dominates.
Actually M has no odd-order terms in b if we expand around b=0 (b enters quadratically in 1/Phi4).

Wait — b enters linearly in B = 2a^3-8ac+9b^2 and in Delta. Let me check the symmetry.
1/Phi4 = -Delta/(4*A*B) where A = a^2+12c, B = 2a^3-8ac+9b^2, and Delta has b^2 and b^4 terms.

Under b -> -b: A is unchanged, B is unchanged (9b^2), Delta has b^2 and b^4 (even powers only
in the standard discriminant). So 1/Phi4(a,b,c) = 1/Phi4(a,-b,c). The function is EVEN in b.

So M(sigma_1, sigma_2, b_1, b_2, cp_1, cp_2) is NOT even in (b_1,b_2) because the sum
b_1+b_2 enters. But each individual 1/Phi4 is even in its b argument.

Let me think about this differently. For the margin M = f(sigma_s, b_s, cp_s) - f(sigma_1, b_1, cp_1) - f(sigma_2, b_2, cp_2):
- f is even in b, so f(sigma, b, cp) = g(sigma, b^2, cp) for some g
- M is NOT simply a function of b_1^2, b_2^2 because b_s = b_1 + b_2 enters as (b_1+b_2)^2

Let me compute the exact degree-2 expansion in (b_1, b_2) around (0,0):
M ≈ M_0(sigma_1,sigma_2,cp_1,cp_2) + (∂²M/∂b_1²)(b_1²) + (∂²M/∂b_1∂b_2)(b_1*b_2) + (∂²M/∂b_2²)(b_2²)

where M_0 = f(sigma_s,0,cp_s) - f(sigma_1,0,cp_1) - f(sigma_2,0,cp_2) >= 0 (CE-16).

The Hessian in (b_1, b_2) should be PSD for M to stay non-negative.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import Rational, symbols, diff, simplify, cancel, factor, expand, collect

SEP = "=" * 70
t0 = time.time()

sigma, b, cp = symbols("sigma b cp", real=True)
a = -sigma
c = cp + sigma**2 / 12

A_sym = a**2 + 12*c
B_sym = 2*a**3 - 8*a*c + 9*b**2
Delta_sym = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
inv_Phi4 = -Delta_sym / (4 * A_sym * B_sym)

# ============================================================
print(SEP)
print("SECTION 1: Symmetry in b")
print(SEP)

# Check that 1/Phi4 is even in b
inv_neg_b = inv_Phi4.subs(b, -b)
diff_check = simplify(cancel(inv_Phi4 - inv_neg_b))
print("1/Phi4(sigma,b,cp) - 1/Phi4(sigma,-b,cp) =", diff_check)
print("Even in b?", diff_check == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Second derivative d²(1/Phi4)/db² at b=0")
print(SEP)
print("Computing...", end=" ", flush=True)

d2_b = diff(inv_Phi4, b, b)
d2_b_at0 = cancel(d2_b.subs(b, 0))
print("done (%.1fs)" % (time.time()-t0))
print("d²/db²(1/Phi4)|_{b=0} =", d2_b_at0)
print("Simplified:", factor(d2_b_at0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Margin Hessian in (b1,b2) at b1=b2=0")
print(SEP)

# M = f(s1+s2, b1+b2, c1+c2) - f(s1, b1, c1) - f(s2, b2, c2)
# d²M/db1² = f_bb(sum) - f_bb(1)
# d²M/db1db2 = f_bb(sum)
# d²M/db2² = f_bb(sum) - f_bb(2)
#
# At b1=b2=0: f_bb at any point = d2_b_at0 evaluated at that point's (sigma, cp)
# So the Hessian of M in (b1,b2) is:
# H = [f_bb(sum) - f_bb(1), f_bb(sum)]
#     [f_bb(sum),            f_bb(sum) - f_bb(2)]
#
# For this to be PSD (M doesn't decrease), we need:
# det(H) >= 0 and trace <= 0 (for NSD, since M should not decrease from M_0)
# Actually for superadditivity to hold to 2nd order in b, we need M - M_0 >= 0
# i.e., the b-correction should be non-negative.
# The b-correction to 2nd order is: (1/2)[H11*b1^2 + 2*H12*b1*b2 + H22*b2^2]
# = (1/2)[f_bb(sum)*b1^2 + 2*f_bb(sum)*b1*b2 + f_bb(sum)*b2^2 - f_bb(1)*b1^2 - f_bb(2)*b2^2]
# = (1/2)[f_bb(sum)*(b1+b2)^2 - f_bb(1)*b1^2 - f_bb(2)*b2^2]
# This is EXACTLY the same structure as the Jensen part from §9.1!

# Let's verify: f_bb = d2_b_at0 = some function of (sigma, cp)
# The b-correction to the margin is:
# (1/2) * [f_bb(s1+s2, cp1+cp2) * (b1+b2)^2 - f_bb(s1,cp1) * b1^2 - f_bb(s2,cp2) * b2^2]

# From §9.1: f_bb at the equality manifold cp=0 is -3/(4*sigma^2)
# So f_bb(sigma, 0) = -3/(4*sigma^2) (negative, confirming local concavity)

# The Jensen argument says: if f_bb(sigma, cp) = g(sigma, cp) and the function
# sigma -> 1/g(sigma, cp) is convex (or more precisely if the Cauchy-Schwarz
# structure applies), then the correction is non-negative.

print("f_bb := d²(1/Phi4)/db²|_{b=0}")
print("f_bb =", d2_b_at0)

# Let's see the structure
print("\nAs a function of sigma and cp:")
d2_collected = collect(expand(d2_b_at0), [sigma, cp])
print("Collected:", d2_collected)
print("Factored:", factor(d2_b_at0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Does the Jensen structure hold?")
print(SEP)
print("Need: f_bb(s1+s2, c1+c2)*(b1+b2)^2 - f_bb(s1,c1)*b1^2 - f_bb(s2,c2)*b2^2 >= 0")
print("i.e., the function (sigma, cp) -> f_bb(sigma, cp) is superadditive when weighted by b^2")
print()

# For the Jensen argument to work, we need f_bb = -phi(sigma,cp) with phi > 0,
# and then need phi(s1+s2,c1+c2)*(b1+b2)^2 <= phi(s1,c1)*b1^2 + phi(s2,c2)*b2^2
# i.e., phi satisfies a "reverse superadditivity" when weighted by b^2.
# This is exactly the structure from the n=3 proof.

# Let me compute f_bb in closed form
s, cp_s = symbols("s cp_s", positive=True)
a_s = -s
c_s = cp_s + s**2/12
A_s = a_s**2 + 12*c_s
B_s = 2*a_s**3 - 8*a_s*c_s

# At b=0: 1/Phi4 = -Delta_0/(4*A*B_0) where Delta_0 and B_0 are b=0 values
Delta_0 = (16*a_s**4*c_s - 128*a_s**2*c_s**2 + 256*c_s**3)
# = 16*c_s*(a_s^4 - 8*a_s^2*c_s + 16*c_s^2) = 16*c_s*(a_s^2 - 4*c_s)^2

inv_0 = -Delta_0 / (4 * A_s * B_s)

# d²/db²(1/Phi4)|_{b=0}: Need to differentiate the full expression wrt b twice, set b=0
# 1/Phi4 = -Delta/(4*A*B)
# A doesn't depend on b
# d(1/Phi4)/db = -(dDelta/db * 4AB - Delta * 4A * dB/db) / (4AB)^2
# This gets complicated. Let me just use the symbolic result.

print("f_bb simplified:")
fb = factor(d2_b_at0)
print("  ", fb)
sys.stdout.flush()

# Now let's test numerically: is the margin correction non-negative?
print("\n" + SEP)
print("SECTION 5: Numerical test of b-correction non-negativity")
print(SEP)

import numpy as np
from sympy import lambdify

fbb_func = lambdify((sigma, cp), d2_b_at0, "numpy")

# Test: for pairs (s1,c1), (s2,c2), and (b1,b2), compute the b-correction
np.random.seed(42)
violations = 0
total = 0

for _ in range(100000):
    s1 = np.random.uniform(0.3, 5)
    s2 = np.random.uniform(0.3, 5)
    c1 = np.random.uniform(-0.04, 0.04)
    c2 = np.random.uniform(-0.04, 0.04)
    b1 = np.random.uniform(-0.3, 0.3)
    b2 = np.random.uniform(-0.3, 0.3)

    try:
        fbb_sum = fbb_func(s1+s2, c1+c2)
        fbb_1 = fbb_func(s1, c1)
        fbb_2 = fbb_func(s2, c2)

        if not (np.isfinite(fbb_sum) and np.isfinite(fbb_1) and np.isfinite(fbb_2)):
            continue

        correction = 0.5 * (fbb_sum*(b1+b2)**2 - fbb_1*b1**2 - fbb_2*b2**2)
        total += 1
        if correction < -1e-14:
            violations += 1
    except:
        continue

print("Tested: %d, Violations: %d" % (total, violations))
if violations > 0:
    print("b-correction can be NEGATIVE => Jensen structure does NOT hold in general")
else:
    print("b-correction always non-negative => Jensen structure HOLDS")

# ============================================================
print("\n" + SEP)
print("SECTION 6: Full 4th-order expansion")
print(SEP)
print("Computing d^4/db^4(1/Phi4)|_{b=0}...")

d4_b = diff(inv_Phi4, b, b, b, b)
d4_b_at0 = cancel(d4_b.subs(b, 0))
print("d⁴/db⁴(1/Φ₄)|_{b=0} =", factor(d4_b_at0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
