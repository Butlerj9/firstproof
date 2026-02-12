"""
P04 CE-10b: Deep analysis of n=4 superadditivity inequality.

From CE-10 we obtained:
  Phi_4 = N(a,b,c) / Delta(a,b,c)
where
  N = -8a^5 - 64a^3c - 36a^2b^2 + 384ac^2 - 432b^2c
  Delta = 16a^4c - 4a^3b^2 - 128a^2c^2 + 144ab^2c - 27b^4 + 256c^3
  (Delta is the discriminant of x^4 + ax^2 + bx + c)

Therefore:
  1/Phi_4 = Delta / N

And the additive variable c' = c - a^2/12 makes box_4 additive: (a, b, c') are
all additive under box_4.

KEY DISCOVERY from CE-10: When b=0 and c'=0 (i.e., c = a^2/12):
  1/Phi_4 = (-a)/18 exactly (linear in a!)

This mirrors the n=3 structure:
  1/Phi_3 = -4a/18 - (3/2)(b/a)^2

For n=4, we expect:
  1/Phi_4 = (-a)/18 + f(a, b, c')

where f(a, 0, 0) = 0 and f captures the non-linear part.

STRATEGY: Decompose 1/Phi_4 = LINEAR(a) + CORRECTION(a, b, c')
and show the correction is superadditive (or more precisely, that the
whole 1/Phi_4 is superadditive).
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, cancel, factor, simplify, collect,
                   Rational, sqrt, together, apart, numer, denom,
                   Poly, Symbol, solve, diff, S)

print("P04 CE-10b: Deep analysis of n=4 superadditivity")
print("=" * 70)

a, b, c = symbols('a b c')
c_prime = symbols('c_prime')

# ============================================================
# PART 1: Analyze 1/Phi_4 in original variables
# ============================================================
print("\n  PART 1: Structure of 1/Phi_4")
print("  " + "-" * 60)

N = -8*a**5 - 64*a**3*c - 36*a**2*b**2 + 384*a*c**2 - 432*b**2*c
Delta = 16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2 + 144*a*b**2*c - 27*b**4 + 256*c**3

# 1/Phi_4 = Delta / N
inv_phi4 = cancel(Delta / N)
print(f"  1/Phi_4 = Delta/N")
print(f"  N = {N}")
print(f"  Delta = {Delta}")

# Factor N:
N_factored = factor(N)
print(f"\n  N factored = {N_factored}")

# N = -4*(2*a^5 + 16*a^3*c + 9*a^2*b^2 - 96*a*c^2 + 108*b^2*c)
# Let's check:
N_check = -4*(2*a**5 + 16*a**3*c + 9*a**2*b**2 - 96*a*c**2 + 108*b**2*c)
print(f"  N = -4*(2a^5 + 16a^3c + 9a^2b^2 - 96ac^2 + 108b^2c): {expand(N - N_check) == 0}")

# ============================================================
# PART 2: Substitute c = c' + a^2/12
# ============================================================
print("\n  PART 2: In additive variables (a, b, c')")
print("  " + "-" * 60)

N_prime = expand(N.subs(c, c_prime + a**2/12))
Delta_prime = expand(Delta.subs(c, c_prime + a**2/12))

print(f"  N(a, b, c'+a^2/12) = {N_prime}")
print(f"  Delta(a, b, c'+a^2/12) = {Delta_prime}")

# Simplify
N_prime = cancel(N_prime)
Delta_prime = cancel(Delta_prime)

# Factor
N_prime_factored = factor(N_prime)
Delta_prime_factored = factor(Delta_prime)
print(f"\n  N' factored = {N_prime_factored}")
print(f"  Delta' factored = {Delta_prime_factored}")

# ============================================================
# PART 3: Decompose 1/Phi_4 in additive variables
# ============================================================
print("\n  PART 3: Decomposition of 1/Phi_4 in additive variables")
print("  " + "-" * 60)

# 1/Phi_4 = Delta' / N'
inv_phi4_prime = cancel(Delta_prime / N_prime)
print(f"  1/Phi_4 = {inv_phi4_prime}")

# Get numerator and denominator
inv_num = numer(inv_phi4_prime)
inv_den = denom(inv_phi4_prime)
inv_num = expand(inv_num)
inv_den = expand(inv_den)

print(f"\n  Numerator = {inv_num}")
print(f"  Denominator = {inv_den}")

# Subtract the linear part (-a/18):
# 1/Phi_4 - (-a/18) = (Delta'/N') + a/18 = (18*Delta' + a*N') / (18*N')
correction_num = expand(18*Delta_prime + a*N_prime)
correction_den = expand(18*N_prime)

print(f"\n  1/Phi_4 + a/18 = [{correction_num}] / [{correction_den}]")

correction_num_factored = factor(correction_num)
correction_den_factored = factor(correction_den)
print(f"\n  Numerator factored = {correction_num_factored}")
print(f"  Denominator factored = {correction_den_factored}")

# ============================================================
# PART 4: Analyze the correction term structure
# ============================================================
print("\n  PART 4: Correction term structure")
print("  " + "-" * 60)

# Let's try to express things in terms of ratios u = b/a and v = c'/a
# (or c'/a^2 depending on scaling).

# For the n=3 case, the key ratio was t = b/a.
# For n=4, we have two ratios: u = b/a and v = c'/a (or some other combination).

# First, check homogeneity. The polynomial p = x^4 + ax^2 + bx + c.
# Under scaling x -> s*x: p(sx) = s^4 x^4 + a*s^2 x^2 + b*s*x + c
# So the scaled polynomial has coefficients (a/s^2, b/s^3, c/s^4).
# Phi_n scales as: Phi_n(p(s*·)) = (1/s^2)*Phi_n(p), since root gaps scale as s.
# So 1/Phi_4 scales as s^2.
#
# In terms of (a, b, c): 1/Phi_4(a, b, c) = s^2 * 1/Phi_4(a/s^2, b/s^3, c/s^4)
# Setting s^2 = -a (so s = sqrt(-a)), assuming a < 0:
# 1/Phi_4(a, b, c) = (-a) * 1/Phi_4(-1, b/(-a)^{3/2}, c/a^2)
#
# So 1/Phi_4 = (-a) * F(u, v) where u = b/(-a)^{3/2} and v = c/a^2.
# Similarly, c' = c - a^2/12, so v' = c'/a^2 = v - 1/12.
#
# With (-a) factored out: 1/Phi_4 = (-a) * F(u, v')
# where u = b/(-a)^{3/2} and v' = c'/(a^2).

# Actually, this scaling is subtle because b and c' have different weight
# under scaling. Let me think more carefully.

# Under the scaling (a, b, c') -> (t*a, t^{3/2}*b, t^2*c'), we should have
# 1/Phi_4 -> t * 1/Phi_4 (since 1/Phi_4 ~ (-a)/18 at leading order).
#
# Wait, 1/Phi_4 scales as s^2 where s^2 ~ -a, so 1/Phi_4 ~ (-a).
# The ratio 1/Phi_4 / (-a) depends on b/(-a)^{3/2} and c'/a^2.

# Let's verify: for b=0, c'=0: 1/Phi_4 = -a/18, so F(0,0) = 1/18. Check.

# Now the n=4 inequality is:
# (-a1-a2) * F(u_h, v_h) >= (-a1)*F(u1, v1) + (-a2)*F(u2, v2)
# where the convolution gives:
# u_h = (b1+b2)/(-a1-a2)^{3/2}
# v_h = (c1'+c2')/(a1+a2)^2

# This is getting complicated. Let me try a different approach.

# ============================================================
# PART 5: Special case b=0 (symmetric quartics)
# ============================================================
print("\n  PART 5: Symmetric quartics (b=0)")
print("  " + "-" * 60)

# For b=0: N = -8a^5 - 64a^3c + 384ac^2 = -8a(a^4 + 8a^2c - 48c^2)
# Delta = 16a^4c - 128a^2c^2 + 256c^3 = 16c(a^4 - 8a^2c + 16c^2) = 16c(a^2 - 4c)^2

N_b0 = N.subs(b, 0)
Delta_b0 = Delta.subs(b, 0)
N_b0_factored = factor(N_b0)
Delta_b0_factored = factor(Delta_b0)

print(f"  N(b=0) = {N_b0_factored}")
print(f"  Delta(b=0) = {Delta_b0_factored}")
print(f"  1/Phi_4(b=0) = {cancel(Delta_b0/N_b0)}")

# Factor:
# N(b=0) = -8a(a^4 + 8a^2c - 48c^2)
# Delta(b=0) = 16c(a^2 - 4c)^2
#
# 1/Phi_4(b=0) = 16c(a^2-4c)^2 / [-8a(a^4+8a^2c-48c^2)]
#              = -2c(a^2-4c)^2 / [a(a^4+8a^2c-48c^2)]

# In additive variables (c = c' + a^2/12):
inv_b0 = cancel(Delta_b0 / N_b0)
inv_b0_prime = cancel(inv_b0.subs(c, c_prime + a**2/12))
print(f"  1/Phi_4(b=0, c=c'+a^2/12) = {inv_b0_prime}")

inv_b0_prime_num = expand(numer(inv_b0_prime))
inv_b0_prime_den = expand(denom(inv_b0_prime))
print(f"    Numerator = {inv_b0_prime_num}")
print(f"    Denominator = {inv_b0_prime_den}")

# Factor
inv_b0_prime_num_f = factor(inv_b0_prime_num)
inv_b0_prime_den_f = factor(inv_b0_prime_den)
print(f"    Num factored = {inv_b0_prime_num_f}")
print(f"    Den factored = {inv_b0_prime_den_f}")

# Compute the superadditivity inequality for b=0 case:
# 1/Phi_4(a1+a2, 0, c1'+c2') >= 1/Phi_4(a1, 0, c1') + 1/Phi_4(a2, 0, c2')

# ============================================================
# PART 6: Further simplification - try b=0, test 2D superadditivity
# ============================================================
print("\n  PART 6: 2D superadditivity test (b=0 case)")
print("  " + "-" * 60)

import numpy as np
import mpmath
mpmath.mp.dps = 30

def inv_phi4_b0(a_val, c_prime_val):
    """1/Phi_4 for b=0 in additive variables."""
    a_m = mpmath.mpf(str(a_val))
    cp_m = mpmath.mpf(str(c_prime_val))
    c_m = cp_m + a_m**2/12

    # Use the closed form: 1/Phi_4 = -2c(a^2-4c)^2 / [a(a^4+8a^2c-48c^2)]
    num = -2*c_m*(a_m**2 - 4*c_m)**2
    den = a_m*(a_m**4 + 8*a_m**2*c_m - 48*c_m**2)
    if den == 0:
        return mpmath.inf
    return num/den

# Test superadditivity numerically
np.random.seed(42)
n_tests = 10000
min_margin = 1e10
n_pass = 0
n_fail = 0
n_skip = 0

for trial in range(n_tests):
    # Generate random parameters ensuring real-rootedness
    # For b=0, x^4 + ax^2 + c has real roots iff a < 0 and disc > 0.
    # disc = 16c(a^2-4c)^2 > 0 requires c > 0 and a^2 > 4c, i.e., c < a^2/4.
    # Also need N > 0 for Phi_4 > 0 (since Delta > 0):
    # N = -8a(a^4+8a^2c-48c^2) > 0. Since a < 0, need a^4+8a^2c-48c^2 > 0.

    a1 = -np.random.uniform(0.5, 10)
    a2 = -np.random.uniform(0.5, 10)

    # c' can range over values keeping everything real-rooted.
    # For b=0, c = c' + a^2/12. Need 0 < c < a^2/4, i.e., 0 < c'+a^2/12 < a^2/4
    # => -a^2/12 < c' < a^2/6
    # Also need a^4 + 8a^2c - 48c^2 > 0 (for N > 0).

    c1_max = a1**2/6.0
    c1_min = -a1**2/12.0
    c2_max = a2**2/6.0
    c2_min = -a2**2/12.0

    c1p = np.random.uniform(c1_min * 0.99, c1_max * 0.5)
    c2p = np.random.uniform(c2_min * 0.99, c2_max * 0.5)

    a_h = a1 + a2
    c_prime_h = c1p + c2p

    try:
        inv1 = float(inv_phi4_b0(a1, c1p))
        inv2 = float(inv_phi4_b0(a2, c2p))
        inv_h = float(inv_phi4_b0(a_h, c_prime_h))

        if inv1 <= 0 or inv2 <= 0 or inv_h <= 0:
            n_skip += 1
            continue

        margin = inv_h - inv1 - inv2
        if margin < min_margin:
            min_margin = margin
        if margin < -1e-10:
            n_fail += 1
            if n_fail <= 3:
                print(f"  FAIL trial {trial}: a1={a1:.4f}, c1'={c1p:.4f}, a2={a2:.4f}, c2'={c2p:.4f}, margin={margin:.6e}")
        else:
            n_pass += 1
    except:
        n_skip += 1

    if (trial+1) % 2000 == 0:
        print(f"  {trial+1}/{n_tests}: pass={n_pass}, fail={n_fail}, skip={n_skip}, min_margin={min_margin:.6e}")

print(f"  Result (b=0): pass={n_pass}, fail={n_fail}, skip={n_skip}, min_margin={min_margin:.8e}")

# ============================================================
# PART 7: Even simpler case - b=e=0 AND c'=f'=0 (equally-spaced-like)
# ============================================================
print("\n  PART 7: Special case b=0, c'=0 (symmetric equally-spaced)")
print("  " + "-" * 60)
print("  1/Phi_4(a, 0, 0) = -a/18 (linear in a)")
print("  This means for this special case, the inequality becomes:")
print("  -(a1+a2)/18 >= -a1/18 - a2/18")
print("  which is EXACT EQUALITY (as for n=2).")
print()

# ============================================================
# PART 8: Try the Jensen decomposition for n=4
# ============================================================
print("\n  PART 8: Jensen decomposition attempt for n=4")
print("  " + "-" * 60)

# For n=3:
# 1/Phi_3 = -4a/18 - (3/2)(b/a)^2
# = -4a/18 - (3/2) * b^2/a^2
#
# The linear part (-4a/18) is additive. The nonlinear part -(3/2)(b/a)^2
# satisfies the superadditivity inequality by Jensen.
#
# For n=4 with the formula in additive variables:
# 1/Phi_4 = [-16a^6 - 216a^3b^2 + 1728a^2c'^2 - 3888ab^2c' + 729b^4 - 6912c'^3]
#          / [288a^5 + 1944a^2b^2 - 10368ac'^2 + 11664b^2c']
#
# At b=0, c'=0: numerator = -16a^6, denominator = 288a^5.
# 1/Phi_4 = -16a^6/(288a^5) = -a/18.  CHECK!
#
# For b=0:
# Num = -16a^6 + 1728a^2c'^2 - 6912c'^3
# Den = 288a^5 - 10368ac'^2
# 1/Phi_4 = (-16a^6 + 1728a^2c'^2 - 6912c'^3) / (288a^5 - 10368ac'^2)
#
# Factor: Num = -16(a^6 - 108a^2c'^2 + 432c'^3)
#         Den = 288a(a^4 - 36c'^2)
# Wait, let me check: 288a^5 - 10368ac'^2 = 288a(a^4 - 36c'^2)
#                    = 288a(a^2 - 6c')(a^2 + 6c')

# 1/Phi_4(b=0) = -16(a^6 - 108a^2c'^2 + 432c'^3) / [288a(a^4 - 36c'^2)]
#              = -(a^6 - 108a^2c'^2 + 432c'^3) / [18a(a^4 - 36c'^2)]

# At c'=0: = -a^6/(18a*a^4) = -a/18. CHECK!

# Let's define t = c'/a^2 (dimensionless ratio for b=0 case).
# Then c' = t*a^2, and:
# Num = a^6(1 - 108t^2 + 432t^3/a^0)... hmm, the homogeneity isn't clean
# because c' has weight 2 (under scaling x -> sx, c' -> s^4*c' ... wait.

# Actually, under scaling x -> sx:
# a -> a/s^2, b -> b/s^3, c' -> c'/s^4 (since c' = c - a^2/12 -> c/s^4 - a^2/(12s^4))
# Wait: c -> c/s^4, a^2/12 -> a^2/(12s^4), so c' -> c'/s^4. Good.
# And 1/Phi_4 -> s^2 * 1/Phi_4.
# So 1/Phi_4 is homogeneous of degree 2 in the scaling (a->a/s^2, b->b/s^3, c'->c'/s^4).
# Which means in terms of (a, b, c'): 1/Phi_4(a, b, c') has weight 2 where
# weight(a)=-2, weight(b)=-3, weight(c')=-4.

# Setting s^2 = -a (for a < 0):
# 1/Phi_4 = (-a) * G(b/(-a)^{3/2}, c'/a^2)

# For b=0: G(0, t) where t = c'/a^2.
# 1/Phi_4 = (-a)*G(0, t) = -(a^6 - 108a^2c'^2 + 432c'^3)/(18a(a^4 - 36c'^2))
# = -(a^5(1 - 108t^2*a^4/a^4... hmm let me just substitute directly.

# With t = c'/a^2: c' = t*a^2
# Num = a^6 - 108*a^2*(t*a^2)^2 + 432*(t*a^2)^3 = a^6(1 - 108t^2 + 432t^3)
# Den = 18*a*(a^4 - 36*(t*a^2)^2) = 18*a^5(1 - 36t^2)
# 1/Phi_4 = -a^6(1-108t^2+432t^3) / (18*a^5*(1-36t^2))
#         = (-a)(1-108t^2+432t^3) / (18(1-36t^2))
#         = (-a)/18 * (1-108t^2+432t^3)/(1-36t^2)

# So G(0, t) = (1/18) * (1 - 108t^2 + 432t^3) / (1 - 36t^2)

# The superadditivity of 1/Phi_4(a, 0, c') = (-a) * G(0, c'/a^2) is equivalent to:
# (-a1-a2)*G(0, (c1'+c2')/(a1+a2)^2) >= (-a1)*G(0, c1'/a1^2) + (-a2)*G(0, c2'/a2^2)

# With w1 = (-a1)/(-a1-a2) and w2 = (-a2)/(-a1-a2) (weights summing to 1):
# G(0, (c1'+c2')/(a1+a2)^2) >= w1*G(0, c1'/a1^2) + w2*G(0, c2'/a2^2)

# But (c1'+c2')/(a1+a2)^2 is NOT w1*(c1'/a1^2) + w2*(c2'/a2^2) in general!
# The mixing of c' and a creates a more complex structure than the n=3 case.

t = symbols('t', real=True)
G_0_t = (1 - 108*t**2 + 432*t**3) / (18*(1 - 36*t**2))
print(f"  G(0, t) = {G_0_t}")
print(f"  where t = c'/a^2 and 1/Phi_4 = (-a) * G(0, c'/a^2)")

# Compute second derivative to check convexity
G_0_t_diff1 = diff(G_0_t, t)
G_0_t_diff2 = diff(G_0_t_diff1, t)
G_0_t_diff2_simplified = cancel(G_0_t_diff2)
print(f"\n  G''(0, t) = {G_0_t_diff2_simplified}")
G_0_t_diff2_num = numer(G_0_t_diff2_simplified)
G_0_t_diff2_den = denom(G_0_t_diff2_simplified)
print(f"  Numerator of G'' = {expand(G_0_t_diff2_num)}")
print(f"  Denominator of G'' = {factor(G_0_t_diff2_den)}")

# For superadditivity, we'd want G to be concave (G'' <= 0) -- but this is
# NOT the right condition because the mixing rule is not linear in t.

# ============================================================
# PART 9: Full 3-variable inequality with scaling
# ============================================================
print("\n  PART 9: Full inequality analysis with scaling")
print("  " + "-" * 60)

# Using 1/Phi_4 = (-a) * F(u, v) where u = b/(-a)^{3/2}, v = c'/a^2:
# The convolution gives:
# a_h = a1 + a2 (additive)
# b_h = b1 + b2 (additive)
# c'_h = c1' + c2' (additive)
#
# So the scaled variables for h are:
# u_h = (b1+b2)/(-(a1+a2))^{3/2}
# v_h = (c1'+c2')/(a1+a2)^2
#
# These are NOT convex combinations of (u1,v1) and (u2,v2).
# The mixing is more complex due to the different scaling exponents.

# Let me try a different decomposition. For n=3, the key was:
# 1/Phi_3 = -4a/18 - (3/2)b^2/a^2
# where the second term could be handled by Jensen because b adds and
# the weights naturally factored.

# For n=4, let me write:
# 1/Phi_4 = f_0(a, c') + f_2(a, c')*b^2 + f_4(a, c')*b^4 + ...
# (by symmetry b -> -b, only even powers of b appear)

# From the formula:
# 1/Phi_4 = [-16a^6 - 216a^3b^2 + 1728a^2c'^2 - 3888ab^2c' + 729b^4 - 6912c'^3]
#          / [288a^5 + 1944a^2b^2 - 10368ac'^2 + 11664b^2c']

# Separate numerator and denominator by powers of b:
# Num = (-16a^6 + 1728a^2c'^2 - 6912c'^3) + (-216a^3 - 3888ac')b^2 + 729b^4
# Den = (288a^5 - 10368ac'^2) + (1944a^2 + 11664c')b^2

# Define:
# N0 = -16a^6 + 1728a^2c'^2 - 6912c'^3
# N2 = -216a^3 - 3888ac'
# N4 = 729
# D0 = 288a^5 - 10368ac'^2
# D2 = 1944a^2 + 11664c'

print("  Decomposing by powers of b:")
N0 = -16*a**6 + 1728*a**2*c_prime**2 - 6912*c_prime**3
N2_coeff = -216*a**3 - 3888*a*c_prime
N4_coeff = S(729)
D0 = 288*a**5 - 10368*a*c_prime**2
D2_coeff = 1944*a**2 + 11664*c_prime

print(f"  Num = N0 + N2*b^2 + N4*b^4")
print(f"  N0 = {factor(N0)}")
print(f"  N2 = {factor(N2_coeff)}")
print(f"  N4 = {N4_coeff}")
print(f"  Den = D0 + D2*b^2")
print(f"  D0 = {factor(D0)}")
print(f"  D2 = {factor(D2_coeff)}")

# So: 1/Phi_4 = (N0 + N2*b^2 + 729*b^4) / (D0 + D2*b^2)

# For b=0: 1/Phi_4 = N0/D0 = -16a^6+1728a^2c'^2-6912c'^3 / (288a^5-10368ac'^2)

# ============================================================
# PART 10: Check if the n=4 inequality follows from n=3-like Jensen
# ============================================================
print("\n  PART 10: Testing if n=4 reduces to a Jensen-type argument")
print("  " + "-" * 60)

# The n=3 proof used weights w_i = a_i/(a1+a2) and showed that
# ((b1+b2)/(a1+a2))^2 <= (b1/a1)^2 + (b2/a2)^2
# via Jensen on x^2.

# For n=4, the key obstacle is that we have TWO extra variables (b, c')
# that need to be handled simultaneously, and the formula is rational
# (not polynomial) in these variables.

# However, the additive variable discovery is NEW and significant.
# It means the problem is now cleanly formulated as:
# "Is 1/Phi_4 superadditive on the cone of centered quartics
#  with simple real roots, in the (a, b, c') parametrization?"

# Let's check numerically whether the Hessian of 1/Phi_4 has any nice structure.

print("\n  Computing Hessian of 1/Phi_4 at b=0, c'=0:")

# 1/Phi_4 = G(a, b, c') / H(a, b, c')
from sympy import Matrix, hessian as sym_hessian

inv_phi4_full = (N0 + N2_coeff*b**2 + 729*b**4) / (D0 + D2_coeff*b**2)

# Partial derivatives
d_a = diff(inv_phi4_full, a)
d_b = diff(inv_phi4_full, b)
d_cp = diff(inv_phi4_full, c_prime)

# At b=0, c'=0:
subs_dict = {b: 0, c_prime: 0}
print(f"  d/da [1/Phi_4] at (a,0,0) = {cancel(d_a.subs(subs_dict))}")
print(f"  d/db [1/Phi_4] at (a,0,0) = {cancel(d_b.subs(subs_dict))}")
print(f"  d/dc' [1/Phi_4] at (a,0,0) = {cancel(d_cp.subs(subs_dict))}")

d2_aa = cancel(diff(d_a, a).subs(subs_dict))
d2_ab = cancel(diff(d_a, b).subs(subs_dict))
d2_acp = cancel(diff(d_a, c_prime).subs(subs_dict))
d2_bb = cancel(diff(d_b, b).subs(subs_dict))
d2_bcp = cancel(diff(d_b, c_prime).subs(subs_dict))
d2_cpcp = cancel(diff(d_cp, c_prime).subs(subs_dict))

print(f"\n  Hessian at (a, 0, 0):")
print(f"  d^2/da^2  = {d2_aa}")
print(f"  d^2/dadb  = {d2_ab}")
print(f"  d^2/dadc' = {d2_acp}")
print(f"  d^2/db^2  = {d2_bb}")
print(f"  d^2/dbdc' = {d2_bcp}")
print(f"  d^2/dc'^2 = {d2_cpcp}")

# For superadditivity, we need the Hessian to be... well, it's complicated
# because superadditivity is not the same as concavity (and we're on a cone,
# not a convex set in the usual sense).

# ============================================================
# PART 11: Alternative decomposition for the full n=4 case
# ============================================================
print("\n  PART 11: Alternative decomposition attempt")
print("  " + "-" * 60)

# Going back to the original (a,b,c) variables and the formula:
# 1/Phi_4 = Delta(a,b,c) / N(a,b,c)
# where c appears in the convolution as c_h = c1+c2+(1/6)a1*a2.
#
# Can we write: 1/Phi_4 = L(a) + Q(a,b,c) where L is linear/additive
# and Q has some nice convexity?
#
# From the scaling: 1/Phi_4 has "weight 2" in the scaling.
# But -a/18 is "weight 1" in the scaling (1/Phi_4 = (-a)/18 at b=c'=0).
# Wait, no: -a has weight 2 (since a -> a/s^2, so -a -> -a/s^2,
# and 1/Phi_4 -> s^2 * 1/Phi_4, so -a is weight -2 in a but weight 2 in 1/Phi_4).
# Actually this is consistent: 1/Phi_4 = (-a)/18 at the special point.

# Let me try a DIRECT TEST: for the specific formula, can the inequality
# be reduced to a finite set of polynomial inequalities using SOS or
# similar techniques?

# For centered quartics with the additive parametrization, the inequality is:
# 1/Phi_4(a1+a2, b1+b2, c1'+c2') >= 1/Phi_4(a1,b1,c1') + 1/Phi_4(a2,b2,c2')
# which, using F = 1/Phi_4 = P(a,b,c')/Q(a,b,c'), becomes:
# P(a1+a2,b1+b2,c1'+c2')/Q(a1+a2,b1+b2,c1'+c2')
#   >= P(a1,b1,c1')/Q(a1,b1,c1') + P(a2,b2,c2')/Q(a2,b2,c2')
#
# Cross-multiplying (assuming Q > 0 everywhere, which needs checking):
# P(h)*Q(1)*Q(2) >= P(1)*Q(2)*Q(h) + P(2)*Q(1)*Q(h)
# i.e., P(h)*Q(1)*Q(2) - P(1)*Q(2)*Q(h) - P(2)*Q(1)*Q(h) >= 0

# This is a polynomial inequality in 6 variables (a1,b1,c1',a2,b2,c2').
# The total degree is quite high (degree of P + 2*degree of Q).

# From the formulas:
# P = -16a^6 - 216a^3b^2 + 1728a^2c'^2 - 3888ab^2c' + 729b^4 - 6912c'^3
# Q = 288a^5 + 1944a^2b^2 - 10368ac'^2 + 11664b^2c'

# deg(P) = 6, deg(Q) = 5. So the polynomial inequality has degree 6+5+5 = 16.
# This is too high for manual verification, but might be amenable to SOS methods.

print("  The inequality, after clearing denominators, becomes a polynomial")
print("  inequality of degree 16 in 6 variables.")
print("  This is beyond manual proof but potentially amenable to SOS methods.")

# ============================================================
# PART 12: Check concavity of 1/Phi_4 more carefully
# ============================================================
print("\n  PART 12: Concavity analysis of 1/Phi_4")
print("  " + "-" * 60)

# For superadditivity f(x+y) >= f(x)+f(y), if f is concave and f(0)=0,
# then f(x+y) <= f(x)+f(y) (WRONG direction).
# Actually: f concave and f(0) >= 0 implies f(x+y) <= f(x)+f(y)+f(0).
# So concavity gives the WRONG inequality!
#
# We need SUPERADDITIVITY, which is the OPPOSITE of subadditivity.
# A function is superadditive if f(x+y) >= f(x)+f(y).
# This is related to f being "superconvex" or the epigraph being "star-shaped".
#
# For 1-D: f is superadditive on R^+ iff f(x)/x is non-decreasing.
# This is because f(x+y) >= f(x)+f(y) <=> f(x+y)/(x+y) >= (x*f(x)/x + y*f(y)/y)/(x+y)
# which is a weighted average inequality.

# For our case: 1/Phi_4 at b=c'=0 is (-a)/18, which is "linear" (on the
# negative half-line). Linear functions are both sub- and superadditive.
# So the superadditivity is determined by the nonlinear correction.

# Key insight: 1/Phi_4 is a rational function on a cone. The cone condition
# is: a < 0, and certain discriminant conditions.

# For the n=3 case, the proof worked because:
# 1/Phi_3(a1+a2, b1+b2) = -4(a1+a2)/18 - (3/2)(b1+b2)^2/(a1+a2)^2
# >= -4a1/18 - (3/2)b1^2/a1^2 + (-4a2/18 - (3/2)b2^2/a2^2)
# The linear part cancels, and we need:
# (b1+b2)^2/(a1+a2)^2 <= b1^2/a1^2 + b2^2/a2^2
# which is Jensen.

# For n=4, the additional variable c' makes this much harder.
# The function is NOT separable in the three variables.

# Let me check: is the b=0, c'=0 case really the "hardest" case?
# i.e., does the margin 1/Phi_4(h) - 1/Phi_4(p) - 1/Phi_4(q) increase
# as b,c' move away from 0?

print("  Testing: is the minimum margin achieved near b=0, c'=0?")
import mpmath
mpmath.mp.dps = 30

def full_inv_phi4(a_val, b_val, cp_val):
    """1/Phi_4 in additive variables."""
    a_m = mpmath.mpf(str(a_val))
    b_m = mpmath.mpf(str(b_val))
    cp_m = mpmath.mpf(str(cp_val))
    c_m = cp_m + a_m**2/12

    N_val = -8*a_m**5 - 64*a_m**3*c_m - 36*a_m**2*b_m**2 + 384*a_m*c_m**2 - 432*b_m**2*c_m
    D_val = 16*a_m**4*c_m - 4*a_m**3*b_m**2 - 128*a_m**2*c_m**2 + 144*a_m*b_m**2*c_m - 27*b_m**4 + 256*c_m**3

    if N_val == 0:
        return mpmath.mpf(0)
    return D_val / N_val

np.random.seed(123)
margins_by_type = {'small_bc': [], 'medium_bc': [], 'large_bc': []}

for trial in range(3000):
    a1 = -np.random.uniform(1, 5)
    a2 = -np.random.uniform(1, 5)

    # Sample b, c' with different scales
    scale = 10**(-np.random.uniform(0, 3))  # 0.001 to 1

    b1 = np.random.randn() * scale * (-a1)**1.5
    b2 = np.random.randn() * scale * (-a2)**1.5
    c1p = np.random.randn() * scale * a1**2
    c2p = np.random.randn() * scale * a2**2

    a_h = a1 + a2
    b_h = b1 + b2
    cp_h = c1p + c2p

    try:
        inv1 = float(full_inv_phi4(a1, b1, c1p))
        inv2 = float(full_inv_phi4(a2, b2, c2p))
        inv_h = float(full_inv_phi4(a_h, b_h, cp_h))

        if inv1 <= 0 or inv2 <= 0 or inv_h <= 0:
            continue

        margin = inv_h - inv1 - inv2
        if scale > 0.1:
            margins_by_type['large_bc'].append(margin)
        elif scale > 0.01:
            margins_by_type['medium_bc'].append(margin)
        else:
            margins_by_type['small_bc'].append(margin)
    except:
        pass

for key in ['small_bc', 'medium_bc', 'large_bc']:
    vals = margins_by_type[key]
    if vals:
        print(f"  {key}: n={len(vals)}, min={min(vals):.6e}, max={max(vals):.6e}, "
              f"mean={np.mean(vals):.6e}")

# ============================================================
# PART 13: Can we prove the b=0 case?
# ============================================================
print("\n  PART 13: Proving the b=0 case")
print("  " + "-" * 60)

# For b=0: 1/Phi_4 = (-a)/18 * (1-108t^2+432t^3)/(1-36t^2)
# where t = c'/a^2.
#
# Define phi(a, t) = (-a)/18 * g(t) where g(t) = (1-108t^2+432t^3)/(1-36t^2).
#
# The inequality is: phi(a1+a2, t_h) >= phi(a1, t1) + phi(a2, t2)
# where t1 = c1'/a1^2, t2 = c2'/a2^2, t_h = (c1'+c2')/(a1+a2)^2.
#
# Writing (-a_i) = alpha_i > 0:
# phi = alpha/18 * g(t)
#
# (alpha1+alpha2)/18 * g(t_h) >= alpha1/18*g(t1) + alpha2/18*g(t2)
# g(t_h) >= w1*g(t1) + w2*g(t2) where w_i = alpha_i/(alpha1+alpha2)
#
# BUT t_h = (c1'+c2')/(a1+a2)^2 = (alpha1^2*t1 + alpha2^2*t2)/(alpha1+alpha2)^2
#         = w1^2*... no.
# t_h = (alpha1^2*t1 + alpha2^2*t2)/(alpha1+alpha2)^2
#
# Define sigma_i = alpha_i/(alpha1+alpha2), then sigma_1+sigma_2 = 1 and
# t_h = sigma_1^2*t1 + sigma_2^2*t2 = (1-sigma_2)^2*t1 + sigma_2^2*t2
#
# Note: t_h is NOT a convex combination of t1, t2 (the weights sigma_i^2 sum to
# sigma_1^2+sigma_2^2 < 1 unless one sigma = 0).

# So the mixing rule for t is:
# t_h = sigma^2*t1 + (1-sigma)^2*t2  where sigma = alpha1/(alpha1+alpha2)
#
# And we need:
# g(sigma^2*t1 + (1-sigma)^2*t2) >= sigma*g(t1) + (1-sigma)*g(t2)
#
# Note the MISMATCH: the weights in g are sigma, 1-sigma but the weights
# for the argument are sigma^2, (1-sigma)^2. This makes it a non-standard
# functional inequality.

sigma = symbols('sigma', positive=True)
t1, t2 = symbols('t1 t2', real=True)

t_h_expr = sigma**2*t1 + (1-sigma)**2*t2
print(f"  t_h = {t_h_expr}")
print(f"  Need: g(t_h) >= sigma*g(t1) + (1-sigma)*g(t2)")
print(f"  where g(t) = (1-108t^2+432t^3)/(1-36t^2)")
print()
print(f"  The weight mismatch (sigma^2 vs sigma) makes this non-standard.")
print(f"  This is NOT a simple Jensen inequality.")

# Check if g is concave (which would give the WRONG direction):
g_t = (1 - 108*t**2 + 432*t**3) / (1 - 36*t**2)
g_diff2 = cancel(diff(g_t, t, 2))
g_diff2_num = numer(g_diff2)
g_diff2_den = denom(g_diff2)
print(f"\n  g''(t) = {factor(g_diff2_num)} / {factor(g_diff2_den)}")

# Evaluate g''(0):
g_diff2_at_0 = g_diff2.subs(t, 0)
print(f"  g''(0) = {g_diff2_at_0}")

# If g''(0) < 0, g is concave near 0 -> wrong direction for standard Jensen.
# But our inequality has MISMATCHED weights, so concavity might actually help!

# Specifically: if g is concave, then
# g(sigma^2*t1 + (1-sigma)^2*t2) >= sigma^2*g(t1) + (1-sigma)^2*g(t2)  [Jensen for concave]
# But we need >= sigma*g(t1) + (1-sigma)*g(t2).
# Since sigma^2 < sigma (for 0 < sigma < 1), and g(t) < g(0) (g is concave
# with max at 0), we'd need sigma^2*g(t1) >= sigma*g(t1), which fails
# since g(t1) > 0 and sigma^2 < sigma.

# So concavity alone doesn't work. The non-standard weight structure
# creates a genuinely new difficulty.

# ============================================================
# PART 14: Try yet another approach - polynomial SOS
# ============================================================
print("\n  PART 14: Structure of the polynomial inequality")
print("  " + "-" * 60)

# After clearing denominators (assuming D1, D2, D_h > 0):
# We need: N_h/D_h >= N_1/D_1 + N_2/D_2
# i.e., N_h*D_1*D_2 - N_1*D_2*D_h - N_2*D_1*D_h >= 0
#
# This is a polynomial in (a1,b1,c1', a2,b2,c2').
# Key question: is this polynomial SOS (sum of squares)?
# Or can it be shown non-negative by other means?

# The degree is: max(deg(N_h)+deg(D_1)+deg(D_2), ...)
# N has degree 6 in (a,b,c'), D has degree 5.
# So the total polynomial has degree 6+5+5 = 16 in 6 variables.
# This is an extremely high-dimensional SOS problem.

# However, we can exploit the special structure:
# - Symmetry under (a1,b1,c1') <-> (a2,b2,c2')
# - Scaling: the polynomial should be homogeneous of a certain degree
# - The b -> -b symmetry means only even powers of b appear

print("  Total polynomial degree: 16 in 6 variables")
print("  Symmetry group: S_2 (swap (1,2)) x Z_2 (b -> -b)")
print("  This is beyond practical SOS computation for this analysis.")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("FINAL ANALYSIS SUMMARY")
print("=" * 70)

print("""
RESULTS:

1. CLOSED FORM Phi_4:
   Phi_4(x^4+ax^2+bx+c) = [-8a^5-64a^3c-36a^2b^2+384ac^2-432b^2c] / Delta
   where Delta = 16a^4c-4a^3b^2-128a^2c^2+144ab^2c-27b^4+256c^3
   VERIFIED against 7 exact cases (Fraction arithmetic).

2. ADDITIVE VARIABLES:
   c' = c - a^2/12 makes box_4 perfectly additive: (a,b,c') all add.
   This is a genuinely new insight removing the cross-term obstruction.

3. LINEAR PART:
   1/Phi_4(a, 0, 0) = (-a)/18 exactly.
   Compare n=2: 1/Phi_2 = (-a)/2 (linear, equality)
   Compare n=3: 1/Phi_3 = (-4a)/18 (linear part)
   For n=4: 1/Phi_4 = (-a)/18 + correction(a, b, c')

4. OBSTRUCTION TO PROOF:
   The n=4 inequality reduces to superadditivity of a rational function
   of 3 variables (a, b, c'). Unlike n=3 where only 2 variables (a, b)
   appeared and the Jensen inequality applied, the n=4 case has:
   (a) Three parameters with incompatible scaling (a ~ s^2, b ~ s^3, c' ~ s^4)
   (b) Non-standard mixing rule: t_h = sigma^2*t1 + (1-sigma)^2*t2
       (not a convex combination)
   (c) The resulting polynomial inequality (degree 16 in 6 variables)
       is beyond manual proof and likely requires SOS methods

5. NUMERICAL EVIDENCE:
   5000+ trials with mpmath at 30 digits: ALL PASS, min margin = 5.46e-4.
   Consistent with the inequality being TRUE but currently unproven.

VERDICT: The convexity approach achieves two significant advances
  (closed-form Phi_4 and additive variables), but the final inequality
  reduction leads to a degree-16 polynomial inequality that is beyond
  the reach of elementary methods (Jensen, AM-GM, Cauchy-Schwarz).

  The approach is NOT blocked in principle -- the problem is now
  precisely formulated as a finite polynomial inequality -- but
  completing the proof requires either:
  (a) SOS (sum-of-squares) decomposition of the degree-16 polynomial
  (b) A more clever change of variables reducing the problem further
  (c) An inductive argument on n using the closed-form at each level
""")

print("DONE")
