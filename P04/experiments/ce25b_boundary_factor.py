"""
ce25b_boundary_factor.py — Test whether N vanishes on validity boundaries.

Hypothesis: N(w, b1, b2) vanishes when any validity condition becomes equality:
  (a) 27*b1^2 = 4*w^3       (component 1 boundary)
  (b) 27*b2^2 = 4*(1-w)^3   (component 2 boundary)
  (c) 27*(b1+b2)^2 = 4       (total polynomial boundary)

If all three divide N, then N = (27b1^2 - 4w^3)(27b2^2 - 4(1-w)^3)(27(b1+b2)^2 - 4) * Q
with Q degree 2 in (b1,b2). On valid interior all three factors < 0, product < 0.
If Q >= 0 then N <= 0. QED.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import (symbols, Rational, factor, cancel, expand, collect,
                   Poly, together, simplify, div, rem, quo, sqrt, degree,
                   groebner, resultant, diff, Symbol, apart, fraction,
                   numer, denom)

SEP = "=" * 70
t0 = time.time()

w, b1, b2 = symbols("w b1 b2", real=True)

def phi4_inv_cp0(s, b):
    num = 729*b**4 + 216*b**2*s**3 - 16*s**6
    den = 72*s**2*(27*b**2 - 4*s**3)
    return num, den

# Build margin numerator
s1, s2 = symbols("s1 s2")
S = s1 + s2
B = b1 + b2
f1_num, f1_den = phi4_inv_cp0(s1, b1)
f2_num, f2_den = phi4_inv_cp0(s2, b2)
fh_num, fh_den = phi4_inv_cp0(S, B)

N_raw = expand(fh_num * f1_den * f2_den
               - f1_num * fh_den * f2_den
               - f2_num * fh_den * f1_den)

# Gauge-fix
N_gauge = N_raw.subs(s2, 1 - w).subs(s1, w)
N_gauge = expand(N_gauge)

# ============================================================
print(SEP)
print("SECTION 1: Test boundary factor (a): 27*b1^2 - 4*w^3")
print(SEP)

# Substitute b1^2 = 4w^3/27, i.e. b1 = 2*w^(3/2)/sqrt(27)
# Since N is even in b1 (after simultaneous flip), actually N has mixed b1*b2 terms.
# Let's just substitute numerically at several (w, b2) pairs.

R = Rational
print("Test: set 27*b1^2 = 4*w^3 and evaluate N")
for w_val in [R(1,3), R(1,2), R(2,3)]:
    b1_sq = 4*w_val**3 / 27
    # Substitute b1^2 where possible. Since N has odd powers of b1 too,
    # let's use b1 = sqrt(4w^3/27). But sqrt isn't rational.
    # Instead, check: does (27*b1^2 - 4*w^3) divide N as polynomial in b1?
    pass

# Better approach: polynomial division
print("\nPolynomial remainder of N modulo (27*b1^2 - 4*w^3) in ring Q(w,b2)[b1]:")
sys.stdout.flush()

# Treat N as polynomial in b1 with coefficients in Q(w, b2)
Np = Poly(N_gauge, b1)
Dp = Poly(27*b1**2 - 4*w**3, b1)
q, r = div(Np, Dp, domain='ZZ(w,b2)')
r_expanded = expand(r.as_expr())
print("Remainder:", r_expanded)
print("Remainder == 0?", r_expanded == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Test boundary factor (b): 27*b2^2 - 4*(1-w)^3")
print(SEP)

Np2 = Poly(N_gauge, b2)
Dp2 = Poly(27*b2**2 - 4*(1-w)**3, b2)
q2, r2 = div(Np2, Dp2, domain='ZZ(w,b1)')
r2_expanded = expand(r2.as_expr())
print("Remainder:", r2_expanded)
print("Remainder == 0?", r2_expanded == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Test boundary factor (c): 27*(b1+b2)^2 - 4")
print(SEP)

# Substitute u = b1+b2, v = b1-b2 (b1 = (u+v)/2, b2 = (u-v)/2)
u, v = symbols("u v")
N_uv = N_gauge.subs([(b1, (u+v)/2), (b2, (u-v)/2)])
N_uv = expand(N_uv)

Np3 = Poly(N_uv, u)
Dp3 = Poly(27*u**2 - 4, u)
q3, r3 = div(Np3, Dp3, domain='ZZ(w,v)')
r3_expanded = expand(r3.as_expr())
print("Remainder:", r3_expanded)
print("Remainder == 0?", r3_expanded == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: If any factor works, do sequential division")
print(SEP)

# Try dividing by all three factors sequentially
factors_found = []

if r_expanded == 0:
    print("Factor (a) divides N. Quotient has %d terms." % len(expand(q.as_expr()).as_ordered_terms()))
    N_after_a = expand(q.as_expr())
    factors_found.append("(a)")
else:
    N_after_a = N_gauge
    print("Factor (a) does NOT divide N.")

if r2_expanded == 0:
    print("Factor (b) divides N.")
    factors_found.append("(b)")
else:
    print("Factor (b) does NOT divide N.")

if r3_expanded == 0:
    print("Factor (c) divides N.")
    factors_found.append("(c)")
else:
    print("Factor (c) does NOT divide N.")

print("\nFactors that divide N:", factors_found if factors_found else "NONE")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Alternative — try GCD with discriminant factors")
print(SEP)

# Each discriminant factor is part of the denominator.
# Delta_1 = 256*sigma_1^3*c1^3 - ... at c'=0, reduces to 27b1^2 - 4*sigma1^3
# Compute GCD of N with each factor

from sympy import gcd

print("Computing GCD(N, 27*b1^2 - 4*w^3) as polynomials in b1...")
sys.stdout.flush()
g1 = gcd(Poly(N_gauge, b1), Poly(27*b1**2 - 4*w**3, b1))
print("GCD:", g1)

print("\nComputing GCD(N, 27*b2^2 - 4*(1-w)^3) as polynomials in b2...")
sys.stdout.flush()
g2 = gcd(Poly(N_gauge, b2), Poly(27*b2**2 - 4*(1-w)**3, b2))
print("GCD:", g2)

print("\nComputing GCD(N_uv, 27*u^2 - 4) as polynomials in u...")
sys.stdout.flush()
g3 = gcd(Poly(N_uv, u), Poly(27*u**2 - 4, u))
print("GCD:", g3)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Direct numerical check at boundary")
print(SEP)

# At boundary (a): 27*b1^2 = 4*w^3
# Set b1 = 2*w^{3/2}/sqrt(27). For rational check, set w = k^2/m^2
# so w^{3/2} = k^3/m^3. Then b1 = 2k^3/(m^3*sqrt(27)).
# Not rational. Try w=1, b1=2/sqrt(27) — not rational either.

# Use floating point:
import math
for w_val in [0.3, 0.5, 0.7]:
    b1_val = math.sqrt(4*w_val**3/27) * 0.999999  # just inside boundary
    for b2_val in [0.0, 0.01, -0.01, 0.05]:
        # Check all three validity conditions
        v1 = 27*b1_val**2 - 4*w_val**3
        v2 = 27*b2_val**2 - 4*(1-w_val)**3
        vh = 27*(b1_val+b2_val)**2 - 4
        N_val = float(N_gauge.subs([(w, w_val), (b1, b1_val), (b2, b2_val)]))
        valid = (v1 < 0) and (v2 < 0) and (vh < 0)
        print("w=%.1f, b1=%.4f(near bdry1), b2=%.2f: N=%.2e, valid=%s, v1=%.2e" %
              (w_val, b1_val, b2_val, N_val, valid, v1))

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Factor out common content from N")
print(SEP)

# Maybe there's a large common factor
Np_full = Poly(N_gauge, w, b1, b2)
cont = Np_full.content()
print("Content (common integer factor):", cont)
N_primitive = expand(N_gauge / cont)
print("Primitive part has %d terms" % len(N_primitive.as_ordered_terms()))

# Try factoring the primitive part (might be slow)
print("\nAttempting full factorization of primitive part...")
sys.stdout.flush()
t1 = time.time()
try:
    N_factored = factor(N_primitive)
    print("Done in %.1fs" % (time.time() - t1))
    print("Factored form:", str(N_factored)[:500])
except Exception as e:
    print("Full factorization failed: %s" % e)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
