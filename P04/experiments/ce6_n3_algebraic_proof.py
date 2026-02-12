"""
P04 CE-6: Algebraic proof verification for n=3 general case.

Key result: For centered cubic f(x) = x^3 + ax + b with discriminant
Delta = -4a^3 - 27b^2 > 0 (simple real roots):

    Phi_3(f) = 18a^2 / Delta

Therefore 1/Phi_3 = Delta / (18a^2) = -4a/18 - 27b^2/(18a^2).

The inequality 1/Phi_3(h) >= 1/Phi_3(p) + 1/Phi_3(q)
where h = x^3 + (a+c)x + (b+d) reduces to:

    ((b+d)/(a+c))^2 <= (b/a)^2 + (d/c)^2

which follows from Jensen's inequality for x^2 (convex).

This script verifies all steps numerically.
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P04 CE-6: Algebraic proof verification for n=3")
print("=" * 70)

# Step 1: Verify Phi_3 = 18a^2 / Delta for specific cubics

print("\n  Step 1: Verify Phi_3 formula")

def phi3_from_roots(roots):
    """Compute Phi_3 directly from roots."""
    n = len(roots)
    total = Fraction(0)
    for i in range(n):
        s = Fraction(0)
        for j in range(n):
            if j != i:
                s += Fraction(1, roots[i] - roots[j])
        total += s * s
    return total

def phi3_formula(a, b):
    """Compute Phi_3 from the closed-form formula."""
    delta = Fraction(-4) * a**3 - Fraction(27) * b**2
    if delta == 0:
        return None  # Multiple root
    return Fraction(18) * a**2 / delta

# Test cases (centered cubics with known roots)
test_cases = [
    # (a, b, description)
    (Fraction(-1), Fraction(0), "x^3 - x, roots {-1, 0, 1}"),
    (Fraction(-3), Fraction(0), "x^3 - 3x, roots {-sqrt(3), 0, sqrt(3)}"),
    (Fraction(-7), Fraction(0), "x^3 - 7x"),
    (Fraction(-3), Fraction(1), "x^3 - 3x + 1"),
    (Fraction(-4), Fraction(2), "x^3 - 4x + 2"),
    (Fraction(-10), Fraction(3), "x^3 - 10x + 3"),
    (Fraction(-5, 2), Fraction(1, 3), "x^3 - 5/2 x + 1/3"),
]

all_pass = True
for a, b, desc in test_cases:
    delta = -4 * a**3 - 27 * b**2
    if delta <= 0:
        print(f"    {desc}: Delta = {delta} <= 0, skip (not simple-rooted)")
        continue

    phi_formula = phi3_formula(a, b)

    # Compute roots numerically to verify
    import numpy as np
    coeffs_np = [1, 0, float(a), float(b)]
    roots_np = sorted(np.roots(coeffs_np).real)

    # Compute Phi_3 from roots numerically
    phi_numeric = 0.0
    for i in range(3):
        s = sum(1.0/(roots_np[i]-roots_np[j]) for j in range(3) if j != i)
        phi_numeric += s**2

    phi_formula_f = float(phi_formula)
    rel_err = abs(phi_formula_f - phi_numeric) / max(abs(phi_numeric), 1e-15)
    status = "PASS" if rel_err < 1e-10 else "FAIL"
    if status == "FAIL":
        all_pass = False
    print(f"    {desc}: Phi3_formula={phi_formula_f:.10f}, Phi3_numeric={phi_numeric:.10f}, rel_err={rel_err:.2e} [{status}]")

print(f"    Step 1 result: {'ALL PASS' if all_pass else 'SOME FAILED'}")

# Step 2: Verify the derivation algebraically using exact fractions
print("\n  Step 2: Exact verification with rational roots")

# x^3 - x = x(x-1)(x+1), a=-1, b=0
roots_exact = [Fraction(-1), Fraction(0), Fraction(1)]
phi_exact = phi3_from_roots(roots_exact)
phi_form = phi3_formula(Fraction(-1), Fraction(0))
print(f"    x^3 - x: Phi3_roots = {phi_exact}, Phi3_formula = {phi_form}, match = {phi_exact == phi_form}")

# x^3 - 4x = x(x-2)(x+2), a=-4, b=0
roots_exact2 = [Fraction(-2), Fraction(0), Fraction(2)]
phi_exact2 = phi3_from_roots(roots_exact2)
phi_form2 = phi3_formula(Fraction(-4), Fraction(0))
print(f"    x^3 - 4x: Phi3_roots = {phi_exact2}, Phi3_formula = {phi_form2}, match = {phi_exact2 == phi_form2}")

# x^3 - 7x + 6 = (x-1)(x-2)(x+3), a=-7, b=6
roots_exact3 = [Fraction(-3), Fraction(1), Fraction(2)]
phi_exact3 = phi3_from_roots(roots_exact3)
phi_form3 = phi3_formula(Fraction(-7), Fraction(6))
print(f"    x^3 - 7x + 6: Phi3_roots = {phi_exact3}, Phi3_formula = {phi_form3}, match = {phi_exact3 == phi_form3}")

# x^3 - 19x + 30 = (x-2)(x-3)(x+5), a=-19, b=30
roots_exact4 = [Fraction(-5), Fraction(2), Fraction(3)]
phi_exact4 = phi3_from_roots(roots_exact4)
phi_form4 = phi3_formula(Fraction(-19), Fraction(30))
print(f"    x^3 - 19x + 30: Phi3_roots = {phi_exact4}, Phi3_formula = {phi_form4}, match = {phi_exact4 == phi_form4}")

# x^3 - 14x + 8 = ... let's check with (x+4)(x-1-sqrt(3))(x-1+sqrt(3)) no
# Use (x-1)(x-2)(x+3) = x^3 - 7x + 6 already done
# Use (x-1)(x+2)(x-3) ... roots sum to 0? 1-2+3=2, not centered
# Let's use roots {-2, -1, 3}: sum=0, a = (-2)(-1)+(-2)(3)+(-1)(3) = 2-6-3 = -7, b = -(-2)(-1)(3) = -6
roots_exact5 = [Fraction(-2), Fraction(-1), Fraction(3)]
phi_exact5 = phi3_from_roots(roots_exact5)
phi_form5 = phi3_formula(Fraction(-7), Fraction(-6))
print(f"    roots {{-2,-1,3}}: Phi3_roots = {phi_exact5}, Phi3_formula = {phi_form5}, match = {phi_exact5 == phi_form5}")

# Step 3: Verify the main inequality reduction
print("\n  Step 3: Verify inequality reduction")
print("    For centered cubics under boxplus_3, coefficients add:")
print("    h = x^3 + (a+c)x + (b+d)")
print()
print("    1/Phi_3 = Delta/(18a^2) = (-4a^3 - 27b^2)/(18a^2) = -4a/18 - 27b^2/(18a^2)")
print()
print("    The inequality 1/Phi_3(h) >= 1/Phi_3(p) + 1/Phi_3(q) becomes:")
print("    -4(a+c)/18 - 27(b+d)^2/(18(a+c)^2) >= -4a/18 - 27b^2/(18a^2) - 4c/18 - 27d^2/(18c^2)")
print("    The -4/18 terms cancel, leaving:")
print("    -27(b+d)^2/(18(a+c)^2) >= -27b^2/(18a^2) - 27d^2/(18c^2)")
print("    Dividing by -27/18 and flipping:")
print("    ((b+d)/(a+c))^2 <= (b/a)^2 + (d/c)^2")
print()
print("    This is the KEY INEQUALITY to prove.")

# Step 4: Verify the key inequality numerically
print("\n  Step 4: Numerical verification of ((b+d)/(a+c))^2 <= (b/a)^2 + (d/c)^2")
print("          with a, c < 0 (required for real roots)")

import random
random.seed(42)
n_trials = 100000
min_margin = float('inf')
all_pass_ineq = True

for trial in range(n_trials):
    # Generate random a, c < 0 and b, d such that discriminants are positive
    a = -random.uniform(0.1, 10)
    c = -random.uniform(0.1, 10)
    # Need -4a^3 - 27b^2 > 0, i.e., b^2 < -4a^3/27 = 4|a|^3/27
    b_max = (4 * abs(a)**3 / 27) ** 0.5
    b = random.uniform(-b_max * 0.99, b_max * 0.99)
    d_max = (4 * abs(c)**3 / 27) ** 0.5
    d = random.uniform(-d_max * 0.99, d_max * 0.99)

    lhs = ((b + d) / (a + c)) ** 2
    rhs = (b / a) ** 2 + (d / c) ** 2
    margin = rhs - lhs

    if margin < min_margin:
        min_margin = margin
    if margin < -1e-12:
        all_pass_ineq = False
        print(f"    FAIL at trial {trial}: a={a}, c={c}, b={b}, d={d}, margin={margin}")
        break

print(f"    {n_trials} trials, min margin = {min_margin:.6e}, {'ALL PASS' if all_pass_ineq else 'FAILED'}")

# Step 5: Verify via Jensen's inequality proof
print("\n  Step 5: Proof via Jensen's inequality")
print("    Let w1 = a/(a+c), w2 = c/(a+c). Since a,c < 0: w1, w2 > 0 and w1+w2 = 1.")
print("    Let u = b/a, v = d/c. Then (b+d)/(a+c) = (ua + vc)/(a+c) = w1*u + w2*v.")
print()
print("    By Jensen (x^2 convex):")
print("      (w1*u + w2*v)^2 <= w1*u^2 + w2*v^2       ... (i)")
print()
print("    Since w1, w2 in (0,1):")
print("      w1*u^2 + w2*v^2 <= u^2 + v^2             ... (ii)")
print("    Proof of (ii): u^2 + v^2 - w1*u^2 - w2*v^2 = w2*u^2 + w1*v^2 >= 0")
print()
print("    Combining (i) and (ii):")
print("      ((b+d)/(a+c))^2 <= (b/a)^2 + (d/c)^2     QED")

# Step 6: Verify the Jensen step exactly
print("\n  Step 6: Exact verification of Jensen step")
random.seed(123)
for _ in range(5):
    a = Fraction(-random.randint(1, 20), random.randint(1, 5))
    c = Fraction(-random.randint(1, 20), random.randint(1, 5))
    b = Fraction(random.randint(-10, 10), random.randint(1, 10))
    d = Fraction(random.randint(-10, 10), random.randint(1, 10))

    w1 = a / (a + c)
    w2 = c / (a + c)
    u = b / a
    v = d / c

    lhs = (w1 * u + w2 * v) ** 2
    jensen_rhs = w1 * u**2 + w2 * v**2
    full_rhs = u**2 + v**2

    assert lhs <= jensen_rhs, f"Jensen failed: {lhs} > {jensen_rhs}"
    assert jensen_rhs <= full_rhs, f"Weight bound failed: {jensen_rhs} > {full_rhs}"
    print(f"    a={a}, c={c}: (w1u+w2v)^2={float(lhs):.6f} <= w1u^2+w2v^2={float(jensen_rhs):.6f} <= u^2+v^2={float(full_rhs):.6f} OK")

# Step 7: Verify the full Phi_3 inequality
print("\n  Step 7: Full Phi_3 inequality verification (exact fractions)")
random.seed(42)
n_exact = 20
all_exact_pass = True

for trial in range(n_exact):
    # Generate cubics with rational integer roots that sum to 0
    while True:
        r1 = random.randint(-5, 5)
        r2 = random.randint(-5, 5)
        r3 = -(r1 + r2)
        if len(set([r1, r2, r3])) == 3:
            break
    while True:
        s1 = random.randint(-5, 5)
        s2 = random.randint(-5, 5)
        s3 = -(s1 + s2)
        if len(set([s1, s2, s3])) == 3:
            break

    roots_p = [Fraction(r1), Fraction(r2), Fraction(r3)]
    roots_q = [Fraction(s1), Fraction(s2), Fraction(s3)]

    # Coefficients
    a_p = roots_p[0]*roots_p[1] + roots_p[0]*roots_p[2] + roots_p[1]*roots_p[2]
    b_p = -(roots_p[0]*roots_p[1]*roots_p[2])
    a_q = roots_q[0]*roots_q[1] + roots_q[0]*roots_q[2] + roots_q[1]*roots_q[2]
    b_q = -(roots_q[0]*roots_q[1]*roots_q[2])

    # Convolution: h = x^3 + (a_p+a_q)x + (b_p+b_q)
    a_h = a_p + a_q
    b_h = b_p + b_q

    delta_h = -4 * a_h**3 - 27 * b_h**2
    if delta_h <= 0:
        continue  # h has multiple or complex roots

    phi_p = phi3_from_roots(roots_p)
    phi_q = phi3_from_roots(roots_q)

    # Compute phi_h from formula
    phi_h = phi3_formula(a_h, b_h)

    inv_h = Fraction(1, 1) / phi_h
    inv_p = Fraction(1, 1) / phi_p
    inv_q = Fraction(1, 1) / phi_q

    margin = inv_h - inv_p - inv_q
    status = "PASS" if margin >= 0 else "FAIL"
    if margin < 0:
        all_exact_pass = False
    print(f"    Trial {trial}: p_roots={[int(r) for r in roots_p]}, q_roots={[int(r) for r in roots_q]}, margin={float(margin):.6e} [{status}]")

print(f"    Exact verification: {'ALL PASS' if all_exact_pass else 'FAILED'}")

# Step 8: Verify equality conditions
print("\n  Step 8: Equality conditions")
print("    Equality holds iff b/a = d/c = 0, i.e., b = d = 0")
print("    (both inputs are equally-spaced cubics)")

# Verify: b=d=0 gives exact equality
for a_val, c_val in [(Fraction(-1), Fraction(-3)), (Fraction(-2), Fraction(-5)), (Fraction(-7, 2), Fraction(-1, 3))]:
    a_h = a_val + c_val
    phi_p = phi3_formula(a_val, Fraction(0))
    phi_q = phi3_formula(c_val, Fraction(0))
    phi_h = phi3_formula(a_h, Fraction(0))
    margin = Fraction(1)/phi_h - Fraction(1)/phi_p - Fraction(1)/phi_q
    print(f"    a={a_val}, c={c_val}, b=d=0: margin = {margin} {'(EXACT EQUALITY)' if margin == 0 else '(NONZERO!)'}")

print(f"\n{'='*70}")
print("Step 9: Summary of n=3 algebraic proof")
print("=" * 70)
print("""
THEOREM: For n=3, the Phi_3 inequality holds for ALL monic cubics p, q
with simple real roots:
    1/Phi_3(p boxplus_3 q) >= 1/Phi_3(p) + 1/Phi_3(q)

PROOF OUTLINE:
1. WLOG both p, q are centered (shift x -> x - mean). Phi_3 is
   translation-invariant; boxplus_3 preserves centering.

2. For centered cubics under boxplus_3, coefficients add:
   p = x^3+ax+b, q = x^3+cx+d => h = x^3+(a+c)x+(b+d).

3. Closed-form: Phi_3(x^3+ax+b) = 18a^2 / (-4a^3 - 27b^2)
   Derived via: Phi_3 = -3a * Sum 1/f'(lambda_i)^2
   where Sum 1/f'(lambda_i)^2 = 6a/(4a^3+27b^2) [by residue calculus].

4. The inequality reduces to:
   ((b+d)/(a+c))^2 <= (b/a)^2 + (d/c)^2

5. With weights w1 = a/(a+c), w2 = c/(a+c) in (0,1):
   LHS = (w1*(b/a) + w2*(d/c))^2
       <= w1*(b/a)^2 + w2*(d/c)^2    [Jensen, x^2 convex]
       <= (b/a)^2 + (d/c)^2 = RHS    [w_i in (0,1)]

6. Equality iff b = d = 0 (equally-spaced roots), recovering Section 4b. QED
""")
print("DONE")
