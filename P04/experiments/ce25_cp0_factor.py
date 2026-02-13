"""
ce25_cp0_factor.py — Factor the c'=0 margin polynomial.

From CE-24: N(w, b1, b2) is degree 8 in (b1,b2) with 20 terms at each w.
N is even in (b1,b2), so monomials are b1^a * b2^b with a+b even.
N=0 at b1=b2=0 (no constant term), and N is negative on valid region.

Strategy: extract explicit polynomial at several w values, attempt factorization,
look for a pattern that gives a general proof.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import (symbols, Rational, factor, cancel, expand, collect,
                   Poly, together, simplify, apart, sqrt, Symbol, degree,
                   numer, denom, fraction, LC, groebner, resultant, diff)

SEP = "=" * 70
t0 = time.time()

# Setup
s1, s2, b1, b2, w = symbols("s1 s2 b1 b2 w", real=True)

def phi4_inv_cp0(s, b):
    """1/Phi4 at c'=0."""
    num = 729*b**4 + 216*b**2*s**3 - 16*s**6
    den = 72*s**2*(27*b**2 - 4*s**3)
    return num, den

# Build margin numerator in (s1, s2, b1, b2)
S = s1 + s2
B = b1 + b2
f1_num, f1_den = phi4_inv_cp0(s1, b1)
f2_num, f2_den = phi4_inv_cp0(s2, b2)
fh_num, fh_den = phi4_inv_cp0(S, B)

N = expand(fh_num * f1_den * f2_den
           - f1_num * fh_den * f2_den
           - f2_num * fh_den * f1_den)

# Gauge-fix: s1=w, s2=1-w
N_gauge = N.subs(s2, 1 - w).subs(s1, w)
N_gauge = expand(N_gauge)

# ============================================================
print(SEP)
print("SECTION 1: Explicit polynomial at w=1/2 (symmetric case)")
print(SEP)

R = Rational
N_half = expand(N_gauge.subs(w, R(1,2)))
p_half = Poly(N_half, b1, b2)
print("w=1/2: degree=%d, terms=%d" % (p_half.total_degree(), len(N_half.as_ordered_terms())))

# Print all monomials
print("\nMonomials (coeff, b1_exp, b2_exp):")
for (e1, e2), coeff in sorted(p_half.as_dict().items()):
    print("  b1^%d * b2^%d : %s" % (e1, e2, coeff))

# Try to factor
print("\nAttempting factorization...")
sys.stdout.flush()
N_half_factored = factor(N_half)
print("Factored form:", N_half_factored)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Substitute b2 = t*b1 (ratio parametrization)")
print(SEP)

t = symbols("t", real=True)
N_ratio = N_half.subs(b2, t*b1)
N_ratio = expand(N_ratio)
p_ratio = Poly(N_ratio, b1)
print("N(1/2, b1, t*b1) as polynomial in b1:")
print("Degree in b1:", p_ratio.degree())
print("\nCoefficients (b1^k):")
for k in range(p_ratio.degree() + 1):
    c = p_ratio.nth(k)
    if c != 0:
        print("  b1^%d : %s" % (k, factor(c)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: General w polynomial structure")
print(SEP)

# Collect by b1, b2 powers
Ng = Poly(N_gauge, b1, b2)
print("Total degree in (b1,b2):", Ng.total_degree())
print("\nCoefficients as functions of w:")
for (e1, e2), coeff in sorted(Ng.as_dict().items()):
    c_simplified = factor(coeff)
    if len(str(c_simplified)) < 200:
        print("  b1^%d * b2^%d : %s" % (e1, e2, c_simplified))
    else:
        print("  b1^%d * b2^%d : [%d chars]" % (e1, e2, len(str(c_simplified))))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Check if N factors as b1^2 * b2^2 * Q(w, b1, b2)")
print(SEP)

# Since N=0 at b1=0 and N=0 at b2=0 (from the b=0 subcase),
# and N is even in (b1,b2), check divisibility by b1^2 * b2^2
N_at_b1_0 = expand(N_gauge.subs(b1, 0))
N_at_b2_0 = expand(N_gauge.subs(b2, 0))
print("N at b1=0:", N_at_b1_0)
print("N at b2=0:", N_at_b2_0)

# If b1=0, then the margin is f(1, b2) - f(w, 0) - f(1-w, b2)
# = (1-w)*g(b2^2/(1-w)^3) + w*g(0) - (1-w)*g(b2^2/(1-w)^3) - w*g(0) ... wait
# Actually: f(s, b) = s*g(b^2/s^3). f(1, b2) = g(b2^2). f(w, 0) = w*g(0) = w/18.
# f(1-w, b2) = (1-w)*g(b2^2/(1-w)^3).
# M = g(b2^2) - w/18 - (1-w)*g(b2^2/(1-w)^3)
# This is NOT obviously zero. So N at b1=0 should NOT be zero in general.

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Try variable change u=b1+b2, v=b1-b2")
print(SEP)

u, v = symbols("u v", real=True)
# b1 = (u+v)/2, b2 = (u-v)/2
N_uv = N_gauge.subs([(b1, (u+v)/2), (b2, (u-v)/2)])
N_uv = expand(N_uv)
N_uv_half = expand(N_uv.subs(w, R(1,2)))
p_uv = Poly(N_uv_half, u, v)
print("w=1/2 in (u,v) coords: degree=%d, terms=%d" % (p_uv.total_degree(), len(N_uv_half.as_ordered_terms())))
print("\nMonomials:")
for (eu, ev), coeff in sorted(p_uv.as_dict().items()):
    print("  u^%d * v^%d : %s" % (eu, ev, coeff))

# Factor in u,v
print("\nAttempting factorization in (u,v)...")
sys.stdout.flush()
N_uv_factored = factor(N_uv_half)
print("Factored:", N_uv_factored)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Hessian of N at b1=b2=0 (should be NSD)")
print(SEP)

H11 = diff(N_gauge, b1, 2).subs([(b1, 0), (b2, 0)])
H12 = diff(N_gauge, b1, b2).subs([(b1, 0), (b2, 0)])
H22 = diff(N_gauge, b2, 2).subs([(b1, 0), (b2, 0)])
print("d2N/db1^2 at 0:", factor(H11))
print("d2N/db1db2 at 0:", factor(H12))
print("d2N/db2^2 at 0:", factor(H22))
print("det(H) =", factor(expand(H11*H22 - H12**2)))
print("trace(H) =", factor(expand(H11 + H22)))

# For NSD: trace <= 0 and det >= 0
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Critical points dN/db1 = dN/db2 = 0")
print(SEP)

# At w=1/2, compute resultant to find critical points
dN1 = diff(N_half, b1)
dN2 = diff(N_half, b2)
print("deg(dN/db1) in b1:", Poly(dN1, b1).degree())
print("deg(dN/db1) in b2:", Poly(dN1, b2).degree())
print("deg(dN/db2) in b1:", Poly(dN2, b1).degree())
print("deg(dN/db2) in b2:", Poly(dN2, b2).degree())
sys.stdout.flush()

print("\nComputing resultant(dN/db1, dN/db2, b2)...")
sys.stdout.flush()
t1 = time.time()
try:
    R_b2 = resultant(dN1, dN2, b2)
    R_b2 = expand(R_b2)
    print("Done in %.1fs" % (time.time() - t1))
    R_poly = Poly(R_b2, b1)
    print("Resultant degree in b1:", R_poly.degree())
    print("Resultant:", factor(R_b2))
except Exception as e:
    print("Resultant computation failed: %s" % e)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
