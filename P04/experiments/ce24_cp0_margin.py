"""
ce24_cp0_margin.py — Symbolic margin computation at c'=0 (3-variable reduction).

At c'=0: 1/Phi4(sigma, b, 0) = (729b^4 + 216b^2*sigma^3 - 16*sigma^6)
                                / (72*sigma^2*(27*b^2 - 4*sigma^3))

Margin: M = f(s1+s2, b1+b2) - f(s1, b1) - f(s2, b2)

Gauge-fix s1+s2=1 (w=s1), clear denominators, get polynomial numerator.
Check degree and sign on valid region.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import (symbols, Rational, factor, cancel, expand, collect,
                   degree, Poly, resultant, groebner, sqrt as Sqrt)
from fractions import Fraction

SEP = "=" * 70
t0 = time.time()

# ============================================================
print(SEP)
print("SECTION 1: Setup and common denominator")
print(SEP)

s1, s2, b1, b2 = symbols("s1 s2 b1 b2", real=True)
S = s1 + s2
B = b1 + b2

def phi4_inv_cp0(s, b):
    """1/Phi4 at c'=0 as rational function in (sigma, b)."""
    num = 729*b**4 + 216*b**2*s**3 - 16*s**6
    den = 72*s**2*(27*b**2 - 4*s**3)
    return num, den

f1_num, f1_den = phi4_inv_cp0(s1, b1)
f2_num, f2_den = phi4_inv_cp0(s2, b2)
fh_num, fh_den = phi4_inv_cp0(S, B)

print("f1_num degree:", Poly(f1_num, s1, b1).total_degree())
print("f1_den degree:", Poly(f1_den, s1, b1).total_degree())
print("fh_num degree:", Poly(expand(fh_num), s1, s2, b1, b2).total_degree())
print("fh_den degree:", Poly(expand(fh_den), s1, s2, b1, b2).total_degree())
sys.stdout.flush()

# Common denominator for M = fh - f1 - f2
# M = fh_num/(fh_den) - f1_num/(f1_den) - f2_num/(f2_den)
# = [fh_num * f1_den * f2_den - f1_num * fh_den * f2_den - f2_num * fh_den * f1_den]
#   / [fh_den * f1_den * f2_den]

print("\nComputing margin numerator N (this may take a moment)...")
sys.stdout.flush()
t1 = time.time()

N = expand(fh_num * f1_den * f2_den
           - f1_num * fh_den * f2_den
           - f2_num * fh_den * f1_den)

print("Done in %.1fs" % (time.time() - t1))
print("N has %d terms" % len(N.as_ordered_terms()))
Np = Poly(N, s1, s2, b1, b2)
print("Total degree:", Np.total_degree())
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Check sign of denominator on valid region")
print(SEP)

# Denominator = fh_den * f1_den * f2_den
# Each factor: 72*s^2*(27*b^2 - 4*s^3) = 72*s^2*(negative on valid region)
# Product: 72^3 * s1^2 * s2^2 * S^2 * D1 * D2 * Dh
# where Di = 27*bi^2 - 4*si^3 < 0, Dh = 27*B^2 - 4*S^3 < 0
# Product of three negatives = negative
# Times 72^3 * s1^2 * s2^2 * S^2 > 0
# Overall denominator < 0

print("Denominator sign on valid region: NEGATIVE")
print("So M >= 0 iff N <= 0 (numerator is non-positive)")

# ============================================================
print("\n" + SEP)
print("SECTION 3: Check N at b1=b2=0")
print(SEP)

N_b0 = N.subs([(b1, 0), (b2, 0)])
print("N at b1=b2=0:", expand(N_b0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Factor out b-dependence structure")
print(SEP)

# Since 1/Phi4 is even in b, M is even in each b_i when the other is 0.
# More precisely: M(s1,s2,b1,b2) = M(s1,s2,-b1,b2) is FALSE
# (because b_h = b1+b2 changes sign when b1 → -b1).
# But M(s1,s2,b1,b2) = M(s1,s2,-b1,-b2) IS TRUE (all b's flip together).

# Check: b -> -b for both
N_negb = N.subs([(b1, -b1), (b2, -b2)])
diff_check = expand(N - N_negb)
print("N(b1,b2) - N(-b1,-b2) = 0?", diff_check == 0)

# So N is even under (b1,b2) → (-b1,-b2). This means N only has
# even total degree in (b1,b2).

# Also check exchange symmetry: s1↔s2, b1↔b2
N_swap = N.subs([(s1, s2), (s2, s1), (b1, b2), (b2, b1)])
print("N symmetric under (s1,b1)↔(s2,b2)?", expand(N - N_swap) == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Gauge-fix s1+s2=1 (set s2=1-s1=1-w)")
print(SEP)

w = symbols("w", positive=True)
N_gauge = N.subs(s2, 1 - w).subs(s1, w)
N_gauge_expanded = expand(N_gauge)
Ng = Poly(N_gauge_expanded, w, b1, b2)
print("After gauge-fixing s1=w, s2=1-w:")
print("Total degree:", Ng.total_degree())
print("Number of terms:", len(N_gauge_expanded.as_ordered_terms()))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Evaluate at specific w values to check sign")
print(SEP)

from sympy import Rational as R

for w_val in [R(1,2), R(1,3), R(1,4), R(1,5), R(1,10)]:
    N_w = N_gauge_expanded.subs(w, w_val)
    N_w = expand(N_w)
    p = Poly(N_w, b1, b2)
    print("w=%s: degree=%d, terms=%d" % (w_val, p.total_degree(), len(N_w.as_ordered_terms())))

    # Evaluate at a few (b1,b2) points in valid region
    for b1v, b2v in [(R(1,10), R(1,10)), (R(1,20), R(-1,20)),
                     (R(1,5), R(0)), (R(0), R(1,5))]:
        val = N_w.subs([(b1, b1v), (b2, b2v)])
        print("  b1=%s, b2=%s: N = %s (sign: %s)" %
              (b1v, b2v, val, "≤0" if val <= 0 else ">0 VIOLATION"))

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Homogeneity check")
print(SEP)

# 1/Phi4 is degree 1 homogeneous under (sigma,b,c') → (lambda*sigma, lambda^{3/2}*b, lambda^2*c')
# At c'=0: f(lambda*sigma, lambda^{3/2}*b) = lambda * f(sigma, b)
# Check: f(sigma, b) = sigma * g(b^2/sigma^3)
# f(lambda*sigma, lambda^{3/2}*b) = lambda*sigma * g(lambda^3*b^2/(lambda^3*sigma^3))
#                                  = lambda*sigma * g(b^2/sigma^3) = lambda * f(sigma, b) ✓

# For the margin: M(lambda*s1, lambda^{3/2}*b1, lambda*s2, lambda^{3/2}*b2) = lambda * M
# The margin numerator N scales differently because of the denominator.

# Let's verify the scaling of N:
lam = symbols("lambda", positive=True)
N_scaled = N.subs([(s1, lam*s1), (s2, lam*s2), (b1, lam**Rational(3,2)*b1), (b2, lam**Rational(3,2)*b2)])
# N_scaled should be lambda^k * N for some k, since M = N/D and M scales as lambda, D scales as lambda^{k-1}
# D = fh_den * f1_den * f2_den, each 72*s^2*(27b^2-4s^3)
# Under scaling: 72*(lam*s)^2*(27*(lam^{3/2}*b)^2 - 4*(lam*s)^3) = 72*lam^2*s^2*(27*lam^3*b^2 - 4*lam^3*s^3)
# = 72*lam^5*s^2*(27b^2-4s^3)
# So each D_i scales as lam^5. D_total scales as lam^15.
# M = N/D scales as lam, so N scales as lam^{15+1} = lam^{16}.

print("N should be homogeneous of degree 16 under")
print("(s1,s2) → (λs1,λs2), (b1,b2) → (λ^{3/2}b1,λ^{3/2}b2)")
print("with weight: σ has weight 1, b has weight 3/2")
print("Total weighted degree of N should be 16")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
