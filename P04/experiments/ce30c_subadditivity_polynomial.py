"""
ce30c_subadditivity_polynomial.py — Compute the phi-subadditivity polynomial.

phi(sigma, b) = sigma^3 * F(u), where u = 27*b^2/(4*sigma^3),
F(u) = (1-u)^3 / (4*(2-u)*((1-u)^3 + 2u)).

Subadditivity: phi(w, b1) + phi(1-w, b2) <= phi(1, b1+b2)

After clearing denominators, this becomes a polynomial inequality.
Compute it and look for factorization/decomposition.
"""
import sys, io, time
from sympy import (symbols, Rational, expand, factor, cancel, numer, denom,
                   simplify, collect, Poly, sqrt, together, apart, degree)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

w, a, d = symbols('w a d', positive=True)  # a = b1^2, d = b2^2

# ============================================================
print(SEP)
print("SECTION 1: Compute subadditivity polynomial")
print(SEP)
sys.stdout.flush()

# F(u) = (1-u)^3 / (4*(2-u)*((1-u)^3 + 2*u))
# phi(sigma, b) = sigma^3 * F(27*b^2/(4*sigma^3))

# For part 1: sigma = w, b^2 = a, u1 = 27*a/(4*w^3)
# For part 2: sigma = 1-w, b^2 = d, u2 = 27*d/(4*(1-w)^3)
# For sum: sigma = 1, b^2 = (b1+b2)^2

# To avoid square roots, work with b1^2 = a, b2^2 = d
# and consider worst case b1*b2 >= 0 (same sign)
# so (b1+b2)^2 = a + d + 2*sqrt(a*d)

# But sqrt makes it non-polynomial. Let me work with s = b1 and t = b2 directly.
s, t_var = symbols('s t', real=True)  # b1 = s, b2 = t

# phi(sigma, b) in terms of b directly (b^2 appears in u)
def phi_sym(sigma, b):
    """Symbolic phi(sigma, b)."""
    u = 27*b**2 / (4*sigma**3)
    num = sigma**3 * (1-u)**3
    den = 4 * (2-u) * ((1-u)**3 + 2*u)
    return num / den

print("Computing phi(w, s)...")
sys.stdout.flush()
phi1 = phi_sym(w, s)
print("Computing phi(1-w, t)...")
sys.stdout.flush()
phi2 = phi_sym(1-w, t_var)
print("Computing phi(1, s+t)...")
sys.stdout.flush()
phi_h = phi_sym(1, s + t_var)

print("Computing difference phi_h - phi1 - phi2...")
sys.stdout.flush()
diff_expr = phi_h - phi1 - phi2

# Clear denominators
print("Clearing denominators...")
sys.stdout.flush()
diff_together = together(diff_expr)
num_diff = numer(diff_together)
den_diff = denom(diff_together)

print("Expanding numerator...")
sys.stdout.flush()
num_exp = expand(num_diff)
print("Numerator terms:", len(num_exp.as_ordered_terms()))

print("Denominator factoring...")
sys.stdout.flush()
den_fac = factor(den_diff)
print("Denominator:", den_fac)
sys.stdout.flush()

# Check sign of denominator on domain
print("\nDenominator sign: on the valid domain, each factor of the")
print("denominator involves (2-u_i) and ((1-u_i)^3+2u_i) with u_i in [0,1),")
print("so all factors are positive. Denominator > 0.")
print("Therefore subadditivity iff numerator >= 0.")

# ============================================================
print("\n" + SEP)
print("SECTION 2: Numerator analysis")
print(SEP)
sys.stdout.flush()

# Try to factor the numerator
print("Attempting to factor numerator...")
sys.stdout.flush()
try:
    num_fac = factor(num_exp)
    print("Factored numerator:", str(num_fac)[:500])
    print("(truncated if long)")
except Exception as e:
    print("Factor failed:", e)
    num_fac = num_exp
sys.stdout.flush()

# Check if s or t divides the numerator (at s=0 or t=0, should be 0)
print("\nChecking special values:")
num_s0 = num_exp.subs(s, 0)
num_s0_exp = expand(num_s0)
print("Numerator at s=0 (terms):", len(num_s0_exp.as_ordered_terms()))
if num_s0_exp == 0:
    print("  = 0 (s divides numerator)")
sys.stdout.flush()

num_t0 = num_exp.subs(t_var, 0)
num_t0_exp = expand(num_t0)
print("Numerator at t=0 (terms):", len(num_t0_exp.as_ordered_terms()))
if num_t0_exp == 0:
    print("  = 0 (t divides numerator)")
sys.stdout.flush()

# At w=1/2 (symmetric case)
print("\nNumerator at w=1/2:")
num_half = num_exp.subs(w, Rational(1, 2))
num_half_exp = expand(num_half)
print("Terms:", len(num_half_exp.as_ordered_terms()))
sys.stdout.flush()

# At s=t (equal b values)
print("\nNumerator at s=t:")
num_st = num_exp.subs(t_var, s)
num_st_exp = expand(num_st)
print("Terms:", len(num_st_exp.as_ordered_terms()))
sys.stdout.flush()

# Try w=1/2, s=t
print("\nNumerator at w=1/2, s=t:")
num_sym = num_exp.subs([(w, Rational(1, 2)), (t_var, s)])
num_sym_exp = expand(num_sym)
print("Terms:", len(num_sym_exp.as_ordered_terms()))
try:
    num_sym_fac = factor(num_sym_exp)
    print("Factored:", num_sym_fac)
except:
    print("Could not factor symmetric case")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Polynomial degree analysis")
print(SEP)
sys.stdout.flush()

# Get the polynomial in (w, s, t)
try:
    p = Poly(num_exp, w, s, t_var)
    print("Total degree:", p.total_degree())
    print("Degree in w:", p.degree(w))
    print("Degree in s:", p.degree(s))
    print("Degree in t:", p.degree(t_var))
    print("Number of terms:", len(p.as_dict()))
except Exception as e:
    print("Poly conversion:", e)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Substitution s^2 -> a, t^2 -> d (even function)")
print(SEP)

# The numerator should be even in both s and t
# Check: subs s -> -s
num_neg_s = num_exp.subs(s, -s)
print("Even in s:", expand(num_neg_s - num_exp) == 0)

num_neg_t = num_exp.subs(t_var, -t_var)
print("Even in t:", expand(num_neg_t - num_exp) == 0)
sys.stdout.flush()

# If even in both, can substitute a = s^2, d = t^2
# But cross-terms s*t from (s+t)^2 will give sqrt(ad)...
# Actually phi_h uses (s+t)^2 = s^2 + 2st + t^2 = a + 2st + d
# So odd powers of s*t appear. Let me check.
print("\nChecking odd s*t terms:")
# The numerator involves (s+t)^2, (s+t)^4, (s+t)^6 from F(u_h)
# (s+t)^{2k} has terms s^i * t^j with i+j = 2k, both even or both odd
# So the numerator involves both s^{even}*t^{even} and s^{odd}*t^{odd} terms

# Let's check the structure by collecting powers
num_collected = collect(num_exp, s)
# Count odd vs even powers of s
from sympy import Poly as SPoly
try:
    p_s = SPoly(num_exp, s)
    coeffs = p_s.all_coeffs()
    deg_s = p_s.degree()
    print("Max degree in s:", deg_s)
    for i, c in enumerate(coeffs):
        power = deg_s - i
        if c != 0:
            c_exp = expand(c)
            print("  s^%d: %d terms" % (power, len(c_exp.as_ordered_terms())))
except Exception as e:
    print("Poly in s analysis:", e)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Exact rational verification")
print(SEP)

from fractions import Fraction
import numpy as np

def F_exact(u):
    """F(u) = (1-u)^3 / (4*(2-u)*((1-u)^3 + 2*u)) using Fraction."""
    one = Fraction(1)
    two = Fraction(2)
    four = Fraction(4)
    v = one - u
    num = v**3
    den = four * (two - u) * (v**3 + two*u)
    return num / den

def phi_exact(sigma, b):
    """phi(sigma, b) using exact Fraction arithmetic."""
    u = Fraction(27) * b**2 / (Fraction(4) * sigma**3)
    if u >= 1:
        return None
    return sigma**3 * F_exact(u)

# Test subadditivity with exact arithmetic
np.random.seed(42)
n_exact = 0
n_exact_fail = 0
min_ratio_exact = Fraction(10)

for _ in range(1000):
    # Generate random w, b1, b2 as rationals
    w_val = Fraction(np.random.randint(1, 20), 20)
    b1_num = np.random.randint(-5, 6)
    b2_num = np.random.randint(-5, 6)
    b1_val = Fraction(b1_num, 20)
    b2_val = Fraction(b2_num, 20)

    # Check validity
    s1 = w_val
    s2 = Fraction(1) - w_val
    if s1 <= 0 or s2 <= 0:
        continue

    if Fraction(27)*b1_val**2 >= Fraction(4)*s1**3:
        continue
    if Fraction(27)*b2_val**2 >= Fraction(4)*s2**3:
        continue
    bh = b1_val + b2_val
    if Fraction(27)*bh**2 >= Fraction(4):
        continue

    p1 = phi_exact(s1, b1_val)
    p2 = phi_exact(s2, b2_val)
    ph = phi_exact(Fraction(1), bh)

    if p1 is None or p2 is None or ph is None or ph <= 0:
        continue

    n_exact += 1
    ratio = (p1 + p2) / ph

    if ratio < min_ratio_exact:
        min_ratio_exact = ratio

    if p1 + p2 > ph:
        n_exact_fail += 1

print("Exact Fraction tests: %d" % n_exact)
print("Subadditivity violations: %d" % n_exact_fail)
print("Min ratio (phi1+phi2)/phi_h: %s = %.6f" % (min_ratio_exact, float(min_ratio_exact)))
sys.stdout.flush()

print("\nElapsed: %.1fs" % (time.time() - t0))
