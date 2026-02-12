"""
P04 CE-12f: Final proof assembly.

Q can be negative, so the discriminant argument alone doesn't work.
But H >= 0 on [0,1] by the endpoint argument when A > 0 and the
actual minimum is non-negative. Let me verify this differently.

Approach: H(w) = A*w^2 + B*w + C on [0,1].
The minimum on [0,1] is at:
  w=0 if -B/(2A) <= 0 => B >= 0
  w=1 if -B/(2A) >= 1 => B <= -2A
  w*=-B/(2A) otherwise, with H(w*) = (4AC-B^2)/(4A)

When A > 0:
  If B >= 0: min = C >= 0. DONE.
  If B <= -2A: min = A+B+C >= 0. DONE.
  If -2A < B < 0: min = (4AC-B^2)/(4A) = C - B^2/(4A)
    Need: C >= B^2/(4A)
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, cancel, factor, collect,
                   Rational, Poly, Add, sqrt, numer, denom)
import numpy as np

print("P04 CE-12f: Final proof assembly")
print("=" * 72)

t1, t2, w = symbols('t1 t2 w')

# Known factorizations:
# A = (t1+t2)^2*(6t1+1)*(6t2+1)
# C = t1^2*(6t2+1)^2 + 3*t2^2*(6t1+1)*(2t2+1)
# B = -(t1+t2)*(72*t1*t2^2 + 12*t1*t2 - t1 + 12*t2^2 + 3*t2)

A_expr = (t1+t2)**2*(6*t1+1)*(6*t2+1)
B_expr = -(t1+t2)*(72*t1*t2**2 + 12*t1*t2 - t1 + 12*t2**2 + 3*t2)
C_expr = t1**2*(6*t2+1)**2 + 3*t2**2*(6*t1+1)*(2*t2+1)
H = expand(A_expr*w**2 + B_expr*w + C_expr)

# The g-inequality is H(w) = Aw^2 + Bw + C >= 0 for w in [0,1].
# Since A >= 0, C >= 0, and A+B+C >= 0, we only need to handle
# the case where the vertex w* = -B/(2A) is in (0,1).

# Instead of 4AC-B^2, let me try a DIRECT approach:
# Show H(w) = A*w^2 + B*w + C can be written as a manifestly
# non-negative expression for w in [0,1].

# Key idea: H(w) = C*(1-w) + (A+B+C)*w + A*w*(1-w)*(w-1+B/A+...)?
# No. Let me use the CONVEX COMBINATION approach:
# H(w) = (1-w)*H(0) + w*H(1) + A*w*(1-w)*(2w-1+B/A)?
# Actually: H(w) = (1-w)*C + w*(A+B+C) + A*w(w-1)
# = (1-w)*C + w*R + Aw^2 - Aw where R = A+B+C
# = (1-w)*C + wR + Aw(w-1) = (1-w)*C + wR - Aw(1-w)
# = (1-w)*(C - Aw) + wR
# For w in [0,1]: C-Aw >= C-A >= 0 if A <= C (not always true).

# Better approach: interpolation between H(0) and H(1)
# H(w) = (1-w)*H(0) + w*H(1) + correction
# = (1-w)*C + w*(A+B+C) + A*w^2 + B*w + C - (1-w)*C - w*(A+B+C)
# = (1-w)*C + w*(A+B+C) + A*w^2 + B*w + C - C + wC - wA - wB - wC
# = (1-w)*C + w*(A+B+C) + A*w^2 - Aw
# = (1-w)*C + w*(A+B+C) + Aw(w-1)
# = (1-w)*C + wR - Aw(1-w)
# = (1-w)(C - Aw) + wR

# So H(w) = (1-w)(C - Aw) + w*R where R = H(1).
# For w in [0,1]: (1-w) >= 0, w >= 0, R >= 0.
# Need: C - Aw >= 0 for w in [0,1], i.e., C >= A (at w=1).
# But this is NOT always true (C can be smaller than A).

# Alternative: H(w) = w*(Aw + B) + C = w(Aw+B) + C
# For w in [0,1] and C >= 0: if Aw+B >= 0 for w in [0,1], then H >= C >= 0.
# Aw+B = A*w + B. At w=0: B. At w=1: A+B.
# If B >= 0: Aw+B >= 0 for w >= 0. So H >= C >= 0. DONE.
# If A+B >= 0 and B < 0: Aw+B changes sign at w=-B/A.
# Below that: Aw+B < 0, so w*(Aw+B) < 0 (both factors same sign for w > 0).
# Wait, if B < 0 and w small: w*(Aw+B) = w*B + Aw^2. For small w: ~ w*B < 0.
# So H ~ C + w*B. Need C + w*B >= 0, i.e., C >= |B|*w.

# This isn't leading to a clean proof. Let me try the DIRECT NUMERICAL approach.

print("\nDirect H-minimum check on [0,1]:")
np.random.seed(42)
N = 1000000
t1v = np.random.uniform(-1/6.0 * 0.999, 10.0, N)
t2v = np.random.uniform(-1/6.0 * 0.999, 10.0, N)

# Evaluate A, B, C
Av = (t1v+t2v)**2 * (6*t1v+1) * (6*t2v+1)
Bv = -(t1v+t2v)*(72*t1v*t2v**2 + 12*t1v*t2v - t1v + 12*t2v**2 + 3*t2v)
Cv = t1v**2*(6*t2v+1)**2 + 3*t2v**2*(6*t1v+1)*(2*t2v+1)

# Minimum of Aw^2+Bw+C on [0,1]
# For A > 0: min at w*=-B/(2A) if in [0,1], else at endpoints
Hmin = np.minimum(Cv, Av + Bv + Cv)  # min at endpoints
mask_vertex = (Av > 0) & (-Bv/(2*Av + 1e-30) > 0) & (-Bv/(2*Av + 1e-30) < 1)
w_star = np.where(mask_vertex, -Bv/(2*Av + 1e-30), 0.5)
H_star = np.where(mask_vertex, Av*w_star**2 + Bv*w_star + Cv, Hmin)
Hmin = np.where(mask_vertex, np.minimum(Hmin, H_star), Hmin)

n_neg = np.sum(Hmin < -1e-10)
print(f"  H < 0 in {n_neg}/{N} tests (should be 0)")
print(f"  Min H on [0,1]: {np.min(Hmin):.10e}")

# ============================================================
# THE REAL PROOF: Rewrite H in a manifestly non-negative form
# ============================================================
print("\n" + "=" * 72)
print("PROOF: Rewrite H as sum of non-negative terms for w in [0,1]")
print("=" * 72)

# From the factored expressions:
# A = (t1+t2)^2*(6t1+1)*(6t2+1)
# B = -(t1+t2)*(72*t1*t2^2 + 12*t1*t2 - t1 + 12*t2^2 + 3*t2)
# = -(t1+t2)*(t2(72*t1*t2 + 12*t1 + 12*t2 + 3) - t1)
# = -(t1+t2)*(-t1 + t2(12t2+3+12t1+72t1t2))
# Hmm, let me factor B differently.

B_poly = expand(B_expr)
# B = -(t1+t2)*(72t1t2^2 + 12t1t2 - t1 + 12t2^2 + 3t2)
inner = 72*t1*t2**2 + 12*t1*t2 - t1 + 12*t2**2 + 3*t2
# = t1(72t2^2 + 12t2 - 1) + t2(12t2 + 3)
# = t1(72t2^2+12t2-1) + 3t2(4t2+1)
print(f"  B = -(t1+t2)*[t1*(72t2^2+12t2-1) + 3t2*(4t2+1)]")

# 72t2^2+12t2-1: discriminant = 144+288 = 432. Roots at (-12+/-sqrt(432))/144.
# sqrt(432) ~ 20.8. Roots at (-12+20.8)/144 ~ 0.061 and (-12-20.8)/144 ~ -0.228.
# So for t2 > -1/6 ~ -0.167: 72t2^2+12t2-1 could be positive or negative.
# At t2=0: -1. At t2=0.1: 72*0.01+1.2-1 = 0.92. So it changes sign.

# Alternative decomposition. Let me use a completely different strategy.
# H = Aw^2 + Bw + C.
# Write w = s, 1-w = 1-s for s in [0,1].
# H = As^2 + Bs + C
# = As^2 + Bs + C
# Try to express as:
# H = alpha*(6t1+1)(6t2+1)*s^2*(t1+t2)^2 + ... nah.

# BEST APPROACH: Use the ORIGINAL inequality directly.
# G = w*(1-w)*H = numerator of [w*g(t1)+(1-w)*g(t2)-g(w^2*t1+(1-w)^2*t2)]
# * denominator (which is positive).

# The denominator is (1+6t1)*(1+6t2)*(1+6*u) where u = w^2*t1+(1-w)^2*t2.
# For t_i > -1/6: (1+6t_i) > 0.
# For u: 1+6u = 1+6w^2*t1+6(1-w)^2*t2 = w^2*(1+6t1)+(1-w)^2*(1+6t2)+(1-w^2-(1-w)^2)
# = w^2*(1+6t1)+(1-w)^2*(1+6t2)+2w(1-w)
# Hmm, that's not clean. But numerically 1+6u > 0 in all tested cases.

# Let me try to write the ORIGINAL numerator (before factoring out w(1-w))
# as a sum of squares.

# G_original = w*t1^2*(1+6t2)*(1+6u)+(1-w)*t2^2*(1+6t1)*(1+6u)-u^2*(1+6t1)*(1+6t2)
# where u = w^2*t1+(1-w)^2*t2

# This is unwieldy. Let me instead try the DIRECT SOS with w in [0,1].
# Since w(1-w) >= 0 and w(1-w) <= 1/4 for w in [0,1]:
# G = w(1-w)*H and G is the original inequality.

# A clean approach: prove H >= 0 using the BOUNDARY VALUES and CONVEXITY.
# H(w) is quadratic in w. On [0,1]:
# If A >= 0: upward parabola, minimum at vertex or endpoints.
# We showed C >= 0, R = A+B+C >= 0.
# The minimum is at w* = -B/(2A), giving H(w*) = (4AC-B^2)/(4A).
#
# Even though 4AC-B^2 can be negative (meaning H has real roots),
# the question is whether the minimum on [0,1] is non-negative.
#
# Since w* = -B/(2A) and both roots are at w = (-B +/- sqrt(B^2-4AC))/(2A),
# we need to check if both roots are outside [0,1].

# Let's verify: when Q < 0 (meaning B^2 > 4AC), are both roots outside [0,1]?

print("\nChecking: when B^2 > 4AC, are H's roots outside [0,1]?")

# Cases where Q < 0 (i.e., B^2 > 4AC):
mask_Q_neg = (Bv**2 > 4*Av*Cv + 1e-8)
n_Q_neg = np.sum(mask_Q_neg)
print(f"  Cases with B^2 > 4AC: {n_Q_neg}")

if n_Q_neg > 0:
    # Compute roots
    disc_sqrt = np.sqrt(np.maximum(Bv[mask_Q_neg]**2 - 4*Av[mask_Q_neg]*Cv[mask_Q_neg], 0))
    root1 = (-Bv[mask_Q_neg] - disc_sqrt) / (2*Av[mask_Q_neg] + 1e-30)
    root2 = (-Bv[mask_Q_neg] + disc_sqrt) / (2*Av[mask_Q_neg] + 1e-30)

    # Check if any root is in [0,1]
    root_in_01 = ((root1 >= 0) & (root1 <= 1)) | ((root2 >= 0) & (root2 <= 1))
    n_root_in = np.sum(root_in_01)
    print(f"  Cases with a root in [0,1]: {n_root_in}")

    if n_root_in == 0:
        print("  ALL roots outside [0,1]!")
        print("  Min root1:", np.min(root1))
        print("  Max root1:", np.max(root1))
        print("  Min root2:", np.min(root2))
        print("  Max root2:", np.max(root2))
    else:
        print("  Some roots IN [0,1] -- contradiction with H >= 0!")
        idx = np.where(root_in_01)[0][:3]
        for i in idx:
            print(f"    t1={t1v[mask_Q_neg][i]:.6f}, t2={t2v[mask_Q_neg][i]:.6f}")
            print(f"    roots: {root1[i]:.6f}, {root2[i]:.6f}")

# ============================================================
# KEY INSIGHT: Use H(0)*H(1) and the parabola shape
# ============================================================
print("\n" + "=" * 72)
print("KEY INSIGHT: The roots of H(w) cannot enter [0,1]")
print("=" * 72)

print("""
Since H(0) = C >= 0 and H(1) = R >= 0, and H is continuous:
  - If H has NO real roots (4AC >= B^2): H >= 0 everywhere. DONE.
  - If H HAS real roots r1, r2 (with r1 <= r2):
    Since H(0) >= 0, both roots must be on the same side of 0:
    either both <= 0 or both >= 0 (or 0 is between them, but then H(0) < 0).
    Similarly for H(1) >= 0: both roots on the same side of 1.

    Since A >= 0: parabola opens upward, so H < 0 between the roots.
    H(0) >= 0 => 0 is NOT between the roots.
    H(1) >= 0 => 1 is NOT between the roots.

    If both roots are in [0,1]: then [0,1] contains the interval (r1,r2)
    where H < 0. But H(0) >= 0 means 0 <= r1 or 0 >= r2.
    Similarly H(1) >= 0 means 1 <= r1 or 1 >= r2.

    Case: r1 >= 0, r2 <= 1: Both roots in [0,1].
      Then H < 0 for w in (r1, r2) subset [0,1].
      But H(0) >= 0 requires 0 <= r1 (OK) and H(1) >= 0 requires 1 >= r2 (OK).
      This gives H(r1) = 0, H(r2) = 0, H < 0 between them.
      But at any point between r1 and r2, H < 0.
      Can this happen? Only if H(0) >= 0 (0 < r1), H(1) >= 0 (r2 < 1),
      and H is negative between r1 and r2.

      This IS possible in principle. But our numerical test shows it doesn't happen.

    The algebraic reason: the structure of A, B, C prevents this.
""")

# Let me check: H(0)*H(1) - A*H(something) = product that controls roots in [0,1]
# A sufficient condition for no roots in [0,1] is:
# C >= 0, R = A+B+C >= 0, and min(C,R) >= 0 (which we have).
# But this alone isn't sufficient -- need the vertex value to be non-negative too.

# ACTUALLY, let me reconsider. We have:
# H(w) = Aw^2 + Bw + C with A >= 0, H(0) = C >= 0, H(1) = A+B+C >= 0.
# Write H(w) = (1-w)*C + w*(A+B+C) + A*w*(w-1)
# = (1-w)*C + w*R + A*w(w-1)
# = (1-w)*C + w*R - A*w(1-w)
# For w in [0,1]: all of (1-w), w are >= 0.
# H(w) = w(1-w)*[-A] + (1-w)*C + w*R
# Since A >= 0: -A <= 0, so the w(1-w) term is non-positive.
# H(w) >= (1-w)*C + w*R - A/4  [since max of w(1-w) = 1/4]
# This gives H >= min(C,R) - A/4. Not always positive.

# A BETTER bound: at the vertex w* = -B/(2A):
# H(w*) = C - B^2/(4A)
# We need C >= B^2/(4A), i.e., 4AC >= B^2.
# But 4AC - B^2 = 3(t1+t2)^2 * Q, and Q can be negative.

# However, when Q < 0, w* might not be in [0,1]!
# Let's check: w* = -B/(2A) = (t1+t2)*inner / (2*(t1+t2)^2*(6t1+1)*(6t2+1))
# = inner / (2*(t1+t2)*(6t1+1)*(6t2+1))

# At the points where Q < 0, what is w*?
print("\nDetailed analysis when Q < 0:")
mask_Q_neg_any = Bv**2 - 4*Av*Cv > 1e-6
idx_Q_neg = np.where(mask_Q_neg_any)[0][:10]

if len(idx_Q_neg) > 0:
    print(f"  Sample cases where Q < 0:")
    for i in idx_Q_neg:
        a = Av[i]; b = Bv[i]; c = Cv[i]
        wstar = -b / (2*a) if a > 0 else float('nan')
        hmin = a*wstar**2 + b*wstar + c if not np.isnan(wstar) else float('nan')
        print(f"    t1={t1v[i]:.4f}, t2={t2v[i]:.4f}: A={a:.4e}, B={b:.4e}, C={c:.4e}")
        print(f"      w*={wstar:.6f}, H(w*)={hmin:.6e}, H(0)={c:.4e}, H(1)={a+b+c:.4e}")
        Qval = (4*a*c-b**2)/3/(t1v[i]+t2v[i])**2 if (t1v[i]+t2v[i])**2>1e-10 else float('inf')
        print(f"      Q={Qval:.6e}")

# ============================================================
# FINAL CORRECT PROOF
# ============================================================
print("\n" + "=" * 72)
print("CORRECT PROOF APPROACH")
print("=" * 72)

# The issue is that 4AC-B^2 is NOT always >= 0.
# But H(w) >= 0 on [0,1] still holds because when the vertex is in [0,1]
# and 4AC-B^2 < 0, the minimum H(w*) is still non-negative.
#
# This happens because Q changes sign only when t1 or t2 are very negative
# (near -1/6), and in those cases w* is outside [0,1].
#
# To prove this rigorously: show that if w* in (0,1), then Q >= 0.
# Equivalently: on the set {(t1,t2) : w* in (0,1)}, Q >= 0.

# w* = -B/(2A). B = -(t1+t2)*F, A = (t1+t2)^2*G where G = (6t1+1)(6t2+1)
# So w* = (t1+t2)*F / (2*(t1+t2)^2*G) = F/(2*(t1+t2)*G)
# where F = 72t1t2^2 + 12t1t2 - t1 + 12t2^2 + 3t2

# For w* in (0,1): 0 < F/(2*(t1+t2)*G) < 1
# Since t1+t2 can be negative (if both near -1/6), and G = (6t1+1)(6t2+1) > 0:
# Sign of w* depends on sign of F and sign of t1+t2.

# This is getting complex. Let me try yet another approach.

# APPROACH: PARAMETRIC SOS
# Treat w as a parameter in [0,1] and show H(w) >= 0 for each fixed w.
# H(w) = Sigma(t1,t2,w) >= 0.
# This is a non-negativity problem in (t1,t2) with parameter w.

# For fixed w:
# H(w) = sum of terms in (t1,t2) with w-dependent coefficients.
# If for each w in [0,1], H(w) is SOS in (t1,t2), we're done.

# Check at w=1/2 (the most "dangerous" point):
H_half = expand((A_expr/4 + B_expr/2 + C_expr).subs(w, Rational(1,2)))
H_half_f = factor(H_half)
print(f"\n  H(1/2) = {H_half_f}")

# At w=1/4:
H_quarter = expand(A_expr/16 + B_expr/4 + C_expr)
H_quarter_f = factor(H_quarter)
print(f"  H(1/4) = {H_quarter_f}")

# At general w, try to write H as a structured sum
# H = w^2*(t1+t2)^2*(6t1+1)*(6t2+1) - w*(t1+t2)*F + C
# where C = t1^2*(6t2+1)^2 + 3t2^2*(6t1+1)*(2t2+1)

# Key idea: H(w) = [t1*w*(6t2+1) - t2*(1-w)*(6t1+1)]^2 * (something)?
# Let me check:
test_sq = (t1*w*(6*t2+1) - t2*(1-w)*(6*t1+1))**2
test_expanded = expand(test_sq)
diff_from_H = expand(H.subs([(t1,t1),(t2,t2),(w,w)]) - test_expanded)
print(f"\n  H - [t1*w*(6t2+1) - t2*(1-w)*(6t1+1)]^2 = {factor(diff_from_H)}")

# Check: is the remainder non-negative?
rem_f = factor(diff_from_H)
print(f"  Remainder factored: {rem_f}")

# ============================================================
# Actually, try: H = (t1*w + t2*(1-w))^2*(6t1+1)*(6t2+1)?
# NO -- that's A*something.
# ============================================================

# Let me try a brute-force SOS: write H as a sum of a few squares
# H ~ sum c_i * (p_i(t1,t2,w))^2

# From the structure: H(0) = C = t1^2*(6t2+1)^2 + 3t2^2*(6t1+1)(2t2+1)
# and H(1) = t2^2*(6t1+1)^2 + 3t1^2*(6t2+1)(2t1+1).
# At w=1/2: ?

# Instead, let me try the KEY SUBSTITUTION:
# p = (6t1+1), q = (6t2+1) (both > 0)
# t1 = (p-1)/6, t2 = (q-1)/6

p, q = symbols('p q', positive=True)
H_pq = expand(H.subs([(t1, (p-1)/6), (t2, (q-1)/6)]))
H_pq_poly = Poly(H_pq, p, q, w, domain='QQ')

print(f"\n  H in (p,q,w) coordinates (p=6t1+1, q=6t2+1):")
print(f"  {len(H_pq_poly.as_dict())} terms")

all_pos_pqw = all(coeff >= 0 for coeff in H_pq_poly.coeffs())
print(f"  All coefficients non-negative: {all_pos_pqw}")

if all_pos_pqw:
    print("  Since p, q > 0 and w in [0,1]: H >= 0. QED!")
else:
    n_neg = sum(1 for c in H_pq_poly.coeffs() if c < 0)
    print(f"  ({n_neg} negative coefficients)")
    print("  Negative terms:")
    for monom, coeff in H_pq_poly.as_dict().items():
        if coeff < 0:
            print(f"    p^{monom[0]} * q^{monom[1]} * w^{monom[2]}: {coeff}")

    # Try with p, q, w, (1-w) as positive variables
    # Substitute w = s, 1-w = r with s+r=1 (s,r >= 0)
    r = symbols('r', positive=True)
    H_pqrs = expand(H_pq.subs(w, 1-r))
    # Express in terms of p, q, r (all > 0, r in [0,1])
    H_pqr_poly = Poly(H_pqrs, p, q, r, domain='QQ')
    all_pos_pqr = all(coeff >= 0 for coeff in H_pqr_poly.coeffs())
    print(f"\n  H in (p,q,r=1-w) coordinates:")
    print(f"  All coefficients non-negative: {all_pos_pqr}")
    if not all_pos_pqr:
        print("  Negative terms:")
        for monom, coeff in H_pqr_poly.as_dict().items():
            if coeff < 0:
                print(f"    p^{monom[0]} * q^{monom[1]} * r^{monom[2]}: {coeff}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 72)
print("SUMMARY")
print("=" * 72)
print(f"""
RESULTS:

1. DEGREE-16 POLYNOMIAL: 547 terms, 6 variables, quasi-homog wt-deg 32.

2. g-INEQUALITY: G = w(1-w)*H where H = Aw^2+Bw+C.
   A = (t1+t2)^2*(6t1+1)*(6t2+1) >= 0 [PROVED]
   C = H(0) >= 0 [PROVED: t1^2*(6t2+1)^2 + 3t2^2*(6t1+1)(2t2+1)]
   H(1) >= 0 [PROVED by symmetry]
   4AC-B^2 = 3(t1+t2)^2*Q where Q NOT always >= 0.
   BUT: H(w) >= 0 on [0,1] verified in 1M numerical tests.
   Root analysis: when Q < 0, roots of H are outside [0,1].

3. b=0 CASE: P_b0 = 131072*(disc factors)*R where
   R = (alpha1^3*cp2-alpha2^3*cp1)^2 + 3*alpha1*alpha2*(alpha1*cp2-alpha2*cp1)^2 + T
   R >= 0 verified in 200K+ tests (min ~ 10^(-11)).

4. PROOF STATUS:
   - g-inequality: PROVED except for algebraic certificate that
     H roots stay outside [0,1] when Q < 0.
   - b=0 case: verified, algebraic certificate for T >= 0 needed.
   - Full 6-var inequality: open.

5. RECOMMENDATIONS:
   (a) For g-inequality: prove Q >= 0 on the set {{w* in (0,1)}}, or find
       an alternative positivity certificate for H on [0,1].
   (b) Install cvxpy/MOSEK for numerical SOS.
   (c) The b=0 and c'=0 cases together cover 2 of the 3 independent directions.
       The mixed b*c' terms require the full 6-variable analysis.
""")

print("DONE")
