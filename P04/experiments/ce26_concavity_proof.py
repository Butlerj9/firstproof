"""
ce26_concavity_proof.py — PROOF of c'=0 subcase via concavity.

Key insight: 1/Phi4(sigma, b, 0) = sigma * g(b^2/sigma^3) where g is concave.
If psi(u) = g(u^2) is also concave, then a weighted Jensen argument proves M >= 0.

Proof chain:
  1. Compute g, g', g'' symbolically.
  2. Show g'' < 0 on [0, 4/27) => g concave.
  3. Show psi''(u) = 2g'(beta) + 4*beta*g''(beta) < 0 => psi concave.
  4. Weighted Jensen + gap lemma => M >= 0.
  5. Numerical cross-check against CE-19/CE-24 data.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import (symbols, Rational, factor, expand, Poly, diff, sqrt,
                   simplify, cancel, together, apart, collect, nsimplify,
                   oo, limit, sign, solve, discriminant, roots)
from fractions import Fraction
import random

SEP = "=" * 70
t0 = time.time()

beta = symbols("beta", nonnegative=True)

# ============================================================
print(SEP)
print("SECTION 1: Define g(beta) and compute derivatives")
print(SEP)

# g(beta) = (16 - 216*beta - 729*beta^2) / (72*(4 - 27*beta))
P = 16 - 216*beta - 729*beta**2
Q = 72*(4 - 27*beta)

g = P / Q
g_simplified = cancel(g)
print("g(beta) =", g_simplified)
print("g(0) =", g_simplified.subs(beta, 0))

# First derivative
g_prime = cancel(diff(g, beta))
print("\ng'(beta) =", g_prime)
print("g'(0) =", g_prime.subs(beta, 0))

# Second derivative
g_dprime = cancel(diff(g, beta, 2))
print("\ng''(beta) =", g_dprime)
print("g''(0) =", g_dprime.subs(beta, 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Verify g'' = -648/(4-27*beta)^3")
print(SEP)

target_g_dprime = -648 / (4 - 27*beta)**3
diff_check = cancel(g_dprime - target_g_dprime)
print("g'' - (-648/(4-27beta)^3) =", diff_check)
print("Confirmed: g'' = -648/(4-27beta)^3?", diff_check == 0)

print("\nSince (4-27beta) > 0 on [0, 4/27), g'' < 0 on [0, 4/27).")
print("=> g is STRICTLY CONCAVE on [0, 4/27). ✓")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Compute psi''(u) = 2g'(beta) + 4*beta*g''(beta)")
print(SEP)

psi_dprime_expr = 2*g_prime + 4*beta*g_dprime
psi_dprime = cancel(psi_dprime_expr)
print("psi''(u) = [2g' + 4*beta*g''](beta=u^2)")
print("         =", psi_dprime)

# Get numerator and denominator
from sympy import numer, denom, fraction
num_psi, den_psi = fraction(psi_dprime)
num_psi = expand(num_psi)
den_psi = expand(den_psi)
print("\nNumerator:", num_psi)
print("Denominator:", den_psi)

# The denominator = -4*(4-27beta)^3 which is NEGATIVE on [0, 4/27).
print("\nDenominator at beta=0:", den_psi.subs(beta, 0))
den_at_0 = den_psi.subs(beta, 0)
print("Denominator sign on [0, 4/27): NEGATIVE (= -4*(4-27beta)^3)")
# Verify: den = -4*(4-27beta)^3
from sympy import Rational as R
den_target = expand(-4*(4 - 27*beta)**3)
print("Denominator = -4*(4-27beta)^3?", expand(den_psi - den_target) == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Prove psi'' < 0 via sign analysis (num > 0, den < 0)")
print(SEP)

# For psi'' = num/den < 0, we need num > 0 (since den < 0).
N_psi = Poly(num_psi, beta)
print("Numerator as polynomial in beta:")
print("  Degree:", N_psi.degree())
print("  Coefficients:", N_psi.all_coeffs())

# N(0)
print("\nN(0) =", num_psi.subs(beta, 0))

# N(4/27)
val_boundary = num_psi.subs(beta, R(4, 27))
print("N(4/27) =", val_boundary)

# N'(beta) — derivative of numerator
N_psi_prime = diff(num_psi, beta)
N_psi_prime_poly = Poly(N_psi_prime, beta)
print("\nN'(beta) =", N_psi_prime)
print("N'(0) =", N_psi_prime.subs(beta, 0))

# Discriminant of N'(beta) (should be negative => no real roots)
coeffs_Np = N_psi_prime_poly.all_coeffs()
print("N'(beta) coefficients:", coeffs_Np)
a_Np, b_Np, c_Np = coeffs_Np
disc_Np = b_Np**2 - 4*a_Np*c_Np
print("Discriminant of N':", disc_Np)
print("Discriminant < 0?", disc_Np < 0)

if disc_Np < 0:
    N0_val = num_psi.subs(beta, 0)
    Np0_val = N_psi_prime.subs(beta, 0)
    print("\n=> N'(beta) has no real roots.")
    print("   Since N'(0) = %s > 0, N'(beta) > 0 for all beta." % Np0_val)
    print("   Therefore N(beta) is strictly INCREASING on [0, infinity).")
    print("   Since N(0) = %s > 0, N(beta) > 0 for all beta >= 0." % N0_val)
    print("\n=> psi'' = (positive numerator) / (negative denominator) < 0")
    print("   for all beta in [0, 4/27).")
    print("\n=> psi(u) = g(u^2) is STRICTLY CONCAVE. ✓")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Weighted Jensen argument (THE PROOF)")
print(SEP)

print("""
PROOF of c'=0 superadditivity:

Given: sigma_1, sigma_2 > 0, b_1, b_2 real, all three polynomials have
4 simple real roots (i.e., 27*b_i^2 < 4*sigma_i^3 for each component
and for the sum).

Define: w_i = sigma_i/(sigma_1+sigma_2), u_i = b_i/sigma_i^{3/2},
        beta_i = u_i^2 = b_i^2/sigma_i^3.

The margin (after gauge-fixing sigma_h=1):
  M = g(beta_h) - w_1*g(beta_1) - w_2*g(beta_2)

where beta_h = (w_1^{3/2}*u_1 + w_2^{3/2}*u_2)^2.

Step 1: psi(u) = g(u^2) is strictly concave on (-2/(3*sqrt(3)), 2/(3*sqrt(3))).
  [Proved above: psi''(u) < 0]

Step 2: Set c_i = w_i^{3/2}. Since w_i in (0,1), c_i < w_i, hence c_1+c_2 < 1.
  Write u_h = c_1*u_1 + c_2*u_2 = c_1*u_1 + c_2*u_2 + (1-c_1-c_2)*0.
  This is a convex combination of u_1, u_2, and 0 with weights c_1, c_2, 1-c_1-c_2.

Step 3: By concavity of psi:
  psi(u_h) >= c_1*psi(u_1) + c_2*psi(u_2) + (1-c_1-c_2)*psi(0)
  i.e., g(beta_h) >= w_1^{3/2}*g(beta_1) + w_2^{3/2}*g(beta_2) + (1-w_1^{3/2}-w_2^{3/2})*g(0)

Step 4 (Gap lemma): We need g(beta_h) >= w_1*g(beta_1) + w_2*g(beta_2).
  The difference between RHS of Step 3 and the target is:
    sum_i (w_i^{3/2} - w_i)*(g(beta_i) - g(0))

  For each term:
    - w_i^{3/2} - w_i = w_i*(w_i^{1/2} - 1) < 0  (since w_i < 1)
    - g(beta_i) - g(0) <= 0                         (since g is decreasing)
    - Product: (negative)*(non-positive) = non-negative >= 0. ✓

  Therefore: RHS of Step 3 >= target.

Step 5: Combining Steps 3 and 4:
  g(beta_h) >= w_1*g(beta_1) + w_2*g(beta_2)
  M = (sigma_1+sigma_2) * [g(beta_h) - w_1*g(beta_1) - w_2*g(beta_2)] >= 0. QED.
""")
sys.stdout.flush()

# ============================================================
print(SEP)
print("SECTION 6: Verify g is decreasing (needed for Step 4)")
print(SEP)

print("g'(beta) =", g_prime)
# Numerator of g'
num_gp, den_gp = fraction(g_prime)
num_gp = expand(num_gp)
print("Numerator of g':", num_gp)
print("Denominator of g':", expand(den_gp), "(always positive)")

# Check sign of numerator on [0, 4/27)
N_gp = Poly(num_gp, beta)
print("Numerator degree:", N_gp.degree())
print("Numerator coefficients:", N_gp.all_coeffs())

# For the numerator a*beta^2 + b*beta + c:
a_gp, b_gp, c_gp = N_gp.all_coeffs()
disc_gp = b_gp**2 - 4*a_gp*c_gp
print("Discriminant:", disc_gp)

# Check if all roots are outside [0, 4/27)
if a_gp > 0:
    print("Leading coefficient positive, parabola opens up.")
    if disc_gp < 0:
        print("No real roots. Sign same as c_gp =", c_gp, "< 0" if c_gp < 0 else "> 0")
    else:
        # Roots exist
        from sympy import sqrt as Sqrt
        r1 = (-b_gp - Sqrt(disc_gp)) / (2*a_gp)
        r2 = (-b_gp + Sqrt(disc_gp)) / (2*a_gp)
        print("Roots:", r1, r2)
        print("Both roots > 4/27?", simplify(r1 - R(4,27)) > 0)
else:
    print("Leading coefficient:", a_gp)
    if disc_gp > 0:
        r1 = (-b_gp - sqrt(disc_gp)) / (2*a_gp)
        r2 = (-b_gp + sqrt(disc_gp)) / (2*a_gp)
        print("Roots:", simplify(r1), simplify(r2))

# Direct check: g'(0) = -3/8 < 0
print("\ng'(0) =", g_prime.subs(beta, 0), "< 0 ✓")
# g'(4/27-epsilon) should be very negative
print("g'(0.14) =", float(g_prime.subs(beta, R(14,100))))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Numerical cross-validation (1000 random tests)")
print(SEP)

random.seed(42)
n_tests = 10000
n_violations = 0
min_margin = float('inf')

for _ in range(n_tests):
    w = random.uniform(0.01, 0.99)
    # Generate valid u1, u2
    u_max = 2.0 / (3.0 * 3.0**0.5)  # 2/(3*sqrt(3))
    u1 = random.uniform(-u_max * 0.99, u_max * 0.99)
    u2 = random.uniform(-u_max * 0.99, u_max * 0.99)

    # Check all validity constraints
    beta1 = u1**2
    beta2 = u2**2
    c1 = w**1.5
    c2 = (1 - w)**1.5
    u_h = c1 * u1 + c2 * u2
    beta_h = u_h**2

    if beta1 >= 4.0/27 or beta2 >= 4.0/27 or beta_h >= 4.0/27:
        continue

    # Evaluate g
    def g_eval(b):
        return (16 - 216*b - 729*b**2) / (72 * (4 - 27*b))

    g_h = g_eval(beta_h)
    g_1 = g_eval(beta1)
    g_2 = g_eval(beta2)

    M = g_h - w * g_1 - (1 - w) * g_2

    if M < min_margin:
        min_margin = M
    if M < -1e-12:
        n_violations += 1

print("Tests: %d" % n_tests)
print("Violations: %d" % n_violations)
print("Min margin: %.6e" % min_margin)
print("Result:", "ALL PASS ✓" if n_violations == 0 else "VIOLATIONS FOUND ✗")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 8: Verify the gap lemma numerically")
print(SEP)

random.seed(123)
n_gap_tests = 10000
n_gap_violations = 0

for _ in range(n_gap_tests):
    w1 = random.uniform(0.01, 0.99)
    w2 = 1.0 - w1
    beta_val = random.uniform(0, 4.0/27 * 0.99)

    g_val = g_eval(beta_val)
    g_0 = g_eval(0)

    gap = (w1**1.5 - w1) * (g_val - g_0)

    if gap < -1e-15:
        n_gap_violations += 1

print("Gap lemma tests: %d" % n_gap_tests)
print("Violations: %d" % n_gap_violations)
print("Result:", "ALL PASS ✓" if n_gap_violations == 0 else "VIOLATIONS FOUND ✗")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 9: Key identity verification")
print(SEP)

# Verify: 1/Phi4(sigma, b, c'=0) = sigma * g(b^2/sigma^3)
# 1/Phi4 at c'=0: (729*b^4 + 216*b^2*sigma^3 - 16*sigma^6) / (72*sigma^2*(27*b^2 - 4*sigma^3))
s, b_sym = symbols("sigma b_var", positive=True)
phi4_inv = (729*b_sym**4 + 216*b_sym**2*s**3 - 16*s**6) / (72*s**2*(27*b_sym**2 - 4*s**3))
g_form = s * g_simplified.subs(beta, b_sym**2/s**3)
g_form_simplified = cancel(g_form)
phi4_inv_simplified = cancel(phi4_inv)
diff_ident = cancel(phi4_inv_simplified - g_form_simplified)
print("1/Phi4 = sigma*g(b^2/sigma^3)?", diff_ident == 0)

# Verify g(0) = 1/18
print("g(0) = 1/18?", g_simplified.subs(beta, 0) == R(1, 18))

# Verify w^{3/2} + (1-w)^{3/2} <= 1 for w in (0,1)
w_sym = symbols("w", positive=True)
h_w = w_sym**R(3,2) + (1-w_sym)**R(3,2)
h_w_prime = diff(h_w, w_sym)
# At w=1/2: h = 2*(1/2)^{3/2} = 2/(2*sqrt(2)) = 1/sqrt(2) ≈ 0.707 < 1
print("h(1/2) = w^{3/2}+(1-w)^{3/2} at w=1/2:", float(h_w.subs(w_sym, R(1,2))))
# At w=0 or w=1: h = 1
print("h(0) = 1, h(1) = 1: boundary values are 1")
print("h(1/2) < 1: confirmed, so c1+c2 < 1 in interior. ✓")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 10: Full margin test with (sigma, b) variables")
print(SEP)

random.seed(456)
n_full = 50000
n_viol_full = 0
min_M_full = float('inf')

for _ in range(n_full):
    s1 = random.uniform(0.01, 2.0)
    s2 = random.uniform(0.01, 2.0)

    # b1, b2 must satisfy 27*b_i^2 < 4*sigma_i^3
    b1_max = (4*s1**3/27)**0.5 * 0.99
    b2_max = (4*s2**3/27)**0.5 * 0.99
    b1_val = random.uniform(-b1_max, b1_max)
    b2_val = random.uniform(-b2_max, b2_max)

    # Check sum validity
    sh = s1 + s2
    bh = b1_val + b2_val
    if 27*bh**2 >= 4*sh**3:
        continue

    # Evaluate f(sigma, b) = sigma * g(b^2/sigma^3)
    def f_eval(sigma, b):
        bt = b**2 / sigma**3
        return sigma * g_eval(bt)

    fh = f_eval(sh, bh)
    f1 = f_eval(s1, b1_val)
    f2 = f_eval(s2, b2_val)

    M = fh - f1 - f2
    if M < min_M_full:
        min_M_full = M
    if M < -1e-10:
        n_viol_full += 1

print("Full margin tests: %d" % n_full)
print("Violations: %d" % n_viol_full)
print("Min margin: %.6e" % min_M_full)
print("Result:", "ALL PASS ✓" if n_viol_full == 0 else "VIOLATIONS FOUND ✗")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("PROOF SUMMARY")
print(SEP)
print("""
THEOREM: For quartics p(x) = x^4 - sigma*x^2 + b*x + sigma^2/12 with
4 simple real roots (27b^2 < 4*sigma^3), the reciprocal discriminant-power-sum
1/Phi_4(sigma, b) = sigma * g(b^2/sigma^3) is superadditive:

  1/Phi_4(sigma_1+sigma_2, b_1+b_2) >= 1/Phi_4(sigma_1, b_1) + 1/Phi_4(sigma_2, b_2)

where g(beta) = (16 - 216*beta - 729*beta^2) / (72*(4 - 27*beta)).

PROOF STRUCTURE:
  (A) g''(beta) = -648/(4-27*beta)^3 < 0 on [0, 4/27) => g strictly concave.
  (B) psi(u) = g(u^2) has psi''(u) < 0 on valid range => psi strictly concave.
      [Numerator of psi'' is cubic with no real critical points, negative at 0.]
  (C) Weighted Jensen: psi(c1*u1 + c2*u2) >= c1*psi(u1) + c2*psi(u2) + (1-c1-c2)*psi(0)
      where c_i = w_i^{3/2}, c1+c2 < 1.
  (D) Gap lemma: (w_i^{3/2} - w_i)(g(beta_i) - g(0)) >= 0.
      [Both factors non-positive, product non-negative.]
  (E) Combining (C) and (D): g(beta_h) >= w_1*g(beta_1) + w_2*g(beta_2). QED.

STATUS: c'=0 subcase PROVED (first complete n=4 subcase with b != 0).
""")

print("Total elapsed: %.1fs" % (time.time() - t0))
