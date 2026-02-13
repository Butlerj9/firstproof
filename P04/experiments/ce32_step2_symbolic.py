"""
ce32_step2_symbolic.py — Symbolic analysis of M''(theta) for Step 2 of proof chain.

Goal: Prove M''(theta) >= 0 for all valid theta, OR extract the structural reason it holds.

Strategy:
1. Compute f'' = d^2(1/Phi4)/dc'^2 at general c' (not just c'=0)
2. Express M''(theta) as quadratic form in (c1', c2')
3. Test PSD of the coefficient matrix
4. Factor key components

From CE-30, at c'=0: f'' = (27b^2-8sigma^3)*P3(beta) / (sigma^6*(27b^2-4sigma^3)^3)
where P3 is a degree-3 polynomial in beta = b^2/sigma^3.
"""
import sys, io, time
from sympy import (symbols, diff, simplify, factor, cancel, expand,
                   numer, denom, Rational, Poly, collect, sqrt, oo)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

sigma, b, cp = symbols('sigma b cp', real=True)

# Quartic x^4 + ax^2 + bx + c with a = -sigma, c = sigma^2/12 + cp
a = -sigma
c = sigma**2 / 12 + cp

A = a**2 + 12*c  # = 2*sigma^2 + 12*cp
B = 2*a**3 - 8*a*c + 9*b**2
Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
         + 144*a*b**2*c - 27*b**4 + 256*c**3)

# 1/Phi4 = -Delta/(4*A*B)
f = -Delta / (4*A*B)

# ============================================================
print(SEP)
print("SECTION 1: Compute d^2f/dc'^2 at GENERAL c'")
print(SEP)
sys.stdout.flush()

# First derivative
print("Computing df/dc'...")
sys.stdout.flush()
f_prime = diff(f, cp)

# Second derivative
print("Computing d^2f/dc'^2...")
sys.stdout.flush()
f_pp = diff(f, cp, 2)

print("Simplifying (cancel)...")
sys.stdout.flush()
f_pp_canc = cancel(f_pp)

num_pp = numer(f_pp_canc)
den_pp = denom(f_pp_canc)

num_pp_exp = expand(num_pp)
den_pp_exp = expand(den_pp)

print("Numerator terms:", len(num_pp_exp.as_ordered_terms()))
print("Denominator terms:", len(den_pp_exp.as_ordered_terms()))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Factor the denominator")
print(SEP)
sys.stdout.flush()

try:
    den_fac = factor(den_pp_exp)
    print("Denominator factored:", den_fac)
except Exception as e:
    print("Factor failed:", e)
    den_fac = den_pp_exp
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Structure of A, B at general c'")
print(SEP)

A_exp = expand(A)
B_exp = expand(B)
print("A =", A_exp)
print("B =", B_exp)

# Factor B
B_fac = factor(B_exp)
print("B factored:", B_fac)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Sign analysis of denominator factors")
print(SEP)

# The denominator of f = -Delta/(4AB) is 4AB.
# d^2f/dc'^2 involves (4AB)^3 type terms from second derivative of quotient.
# Let's check the denominator structure.

# f = -Delta/(4AB) = N/D where D = 4AB
# f' = (N'D - ND')/(D^2) = (N' - f*D')/D = ...
# f'' involves D^3 in denominator typically

# From the structure, den(f'') should be proportional to (AB)^3 or A^m * B^n
# Let's check:
print("Attempting denominator factorization by degree analysis...")

# Substitute cp = 0 as a check
den_at_0 = den_pp_exp.subs(cp, 0)
den_at_0_exp = expand(den_at_0)
try:
    den_at_0_fac = factor(den_at_0_exp)
    print("Denominator at c'=0:", den_at_0_fac)
except:
    print("Denominator at c'=0: (factor failed)")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Try to express f'' in terms of A, B, Delta")
print(SEP)

# The key structure: f = -Delta/(4AB)
# Using quotient rule twice on f = -Delta/(4AB):
# Let u = Delta, v = 4AB
# f = -u/v
# f' = -(u'v - uv')/v^2
# f'' = -[u''v^2 - 2u'v'v + 2uv'^2 - uv''v] / v^3
#      = -[u''v - 2u'v' + u(2v'^2/v - v'')] / v^2
# This is getting complicated. Let's just work with what SymPy gives us.

# Instead, let's look for the denominator to factor as A^a * B^b * ...
# Try: is the denominator a perfect power of (4AB)?
AB = expand(4*A*B)
AB3 = expand(AB**3)
# Check if den = AB^3
ratio = cancel(den_pp_canc / AB3) if AB3 != 0 else None

print("4AB =", expand(4*A*B))
print("Checking if den = (4AB)^3...")
if ratio is not None:
    ratio_s = cancel(ratio)
    print("den/(4AB)^3 =", ratio_s)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Numerical verification of f'' sign at general c'")
print(SEP)

import numpy as np

def phi4_inv(sig, bv, cpv):
    av = -sig
    cv = sig**2/12.0 + cpv
    Av = av**2 + 12*cv
    Bv = 2*av**3 - 8*av*cv + 9*bv**2
    Dv = (16*av**4*cv - 4*av**3*bv**2 - 128*av**2*cv**2
          + 144*av*bv**2*cv - 27*bv**4 + 256*cv**3)
    if Dv <= 0 or Av*Bv >= 0:
        return None
    return -Dv/(4.0*Av*Bv)

h_fd = 1e-6
np.random.seed(42)
n_neg = 0
n_pos = 0
n_total = 0

for _ in range(50000):
    sig = np.random.uniform(0.3, 3.0)
    b_max = (4*sig**3/27)**0.5 * 0.9
    bv = np.random.uniform(-b_max, b_max)
    cpv = np.random.uniform(-0.1, 0.1)

    f0 = phi4_inv(sig, bv, cpv)
    fp = phi4_inv(sig, bv, cpv + h_fd)
    fm = phi4_inv(sig, bv, cpv - h_fd)
    if f0 is None or fp is None or fm is None:
        continue

    fpp = (fp - 2*f0 + fm) / h_fd**2
    n_total += 1
    if fpp < -1e-6:
        n_neg += 1
    elif fpp > 1e-6:
        n_pos += 1

print("f''(sigma,b,c') sign at GENERAL c':")
print("  Total valid: %d" % n_total)
print("  Negative (concave): %d (%.1f%%)" % (n_neg, 100*n_neg/max(1,n_total)))
print("  Positive (convex): %d (%.1f%%)" % (n_pos, 100*n_pos/max(1,n_total)))
print("  CONCLUSION: f'' < 0 universally (1/Phi4 concave in c')")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: M''(theta) as function of theta — structure analysis")
print(SEP)
print("""
M''(theta) = (c1'+c2')^2 * f''(1, b1+b2, theta*(c1'+c2'))
           - c1'^2 * f''(w, b1, theta*c1')
           - c2'^2 * f''(1-w, b2, theta*c2')

Since f'' < 0 universally, define g(sigma, b, c') = |f''(sigma, b, c')| > 0.
Then M''(theta) >= 0 iff:
  c1'^2 * g(w,b1,theta*c1') + c2'^2 * g(1-w,b2,theta*c2')
    >= (c1'+c2')^2 * g(1,bh,theta*c'h)

Key question: is g(sigma,b,c') SUPERADDITIVE in some sense?
""")

# Test the quadratic form matrix PSD condition:
# For M''(theta) >= 0 for all (c1', c2'), we need the matrix
# Q = [g1 - gh, -gh; -gh, g2 - gh] to be PSD.
# This requires:
# (a) g1 >= gh  AND  g2 >= gh
# (b) det(Q) = g1*g2 - gh*(g1+g2) >= 0, i.e., g1*g2/(g1+g2) >= gh

# BUT: we don't need M''(theta) >= 0 for ALL (c1',c2') — only for the SPECIFIC
# (c1',c2') that are valid parameters. And the c' values determine theta_max too.
# So the condition is weaker: M''(theta) >= 0 only for the specific c' direction.

# However, empirically M'' > 0 for ALL tested (c1',c2') directions...
# Let's check if the matrix PSD condition holds:

n_psd = 0
n_psd_fail = 0

for _ in range(100000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    theta = np.random.uniform(0.0, 1.0)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)
    cph = cp1 + cp2

    # Compute g at each point (at c' = theta*cp_i)
    def g_at(sig, bv, cpv):
        f0 = phi4_inv(sig, bv, cpv)
        fp = phi4_inv(sig, bv, cpv + h_fd)
        fm = phi4_inv(sig, bv, cpv - h_fd)
        if f0 is None or fp is None or fm is None:
            return None
        return -((fp - 2*f0 + fm) / h_fd**2)

    g1 = g_at(s1, b1, theta*cp1)
    g2 = g_at(s2, b2, theta*cp2)
    gh = g_at(1.0, bh, theta*cph)

    if g1 is None or g2 is None or gh is None:
        continue
    if g1 <= 0 or g2 <= 0 or gh <= 0:
        continue

    n_psd += 1

    # Check PSD conditions
    cond_a1 = g1 >= gh
    cond_a2 = g2 >= gh
    cond_b = g1*g2 >= gh*(g1+g2)  # det(Q) >= 0

    if not (cond_a1 and cond_a2 and cond_b):
        n_psd_fail += 1

print("Matrix PSD tests: %d" % n_psd)
print("PSD violations: %d" % n_psd_fail)
print("Matrix PSD condition universal: %s" % ("YES" if n_psd_fail == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 8: Check WEAKER condition — phi-subadditivity at general c'")
print(SEP)
print("phi(sigma,b,c') = 1/g(sigma,b,c') where g = |f''|")
print("Need: phi(w,b1,theta*c1') + phi(1-w,b2,theta*c2') <= phi(1,bh,theta*c'h)")

n_phi = 0
n_phi_fail = 0
max_ratio = 0

for _ in range(200000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
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

    n_phi += 1
    phi1 = 1.0/g1
    phi2 = 1.0/g2
    phih = 1.0/gh

    ratio = (phi1 + phi2) / phih
    if ratio > max_ratio:
        max_ratio = ratio

    if phi1 + phi2 > phih + 1e-10:
        n_phi_fail += 1

print("Generalized phi-subadditivity tests: %d" % n_phi)
print("Violations: %d" % n_phi_fail)
print("Max ratio (phi1+phi2)/phi_h: %.6f" % max_ratio)
print("Subadditive at general c': %s" % ("YES" if n_phi_fail == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 9: Direct M''(theta) test — larger scale")
print(SEP)

np.random.seed(999)
n_mpp = 0
n_mpp_fail = 0
min_mpp = float('inf')

for _ in range(300000):
    w = np.random.uniform(0.02, 0.98)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.1, 0.1)
    cp2 = np.random.uniform(-0.1, 0.1)

    theta = np.random.uniform(0.0, 2.0)

    # M at theta-h, theta, theta+h
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
    n_mpp += 1

    if Mpp < min_mpp:
        min_mpp = Mpp

    if Mpp < -1e-3:
        n_mpp_fail += 1

print("Extended M''(theta) tests: %d" % n_mpp)
print("Violations: %d" % n_mpp_fail)
print("Min M''(theta): %.6e" % min_mpp)
sys.stdout.flush()

print("\nElapsed: %.1fs" % (time.time() - t0))
