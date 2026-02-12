"""
P04 CE-13b: Extract the exact numerator polynomial of the b=0 superadditivity margin
and assess SOS decomposability.

For b=0 centered quartics, 1/Phi_4 = 2c(4c-a^2)/(a(a^2+12c)).
With c = a^2*(t + 1/12) where t = c'/(a^2):
  1/Phi_4(a,t) = 2*a^2*(t+1/12)*(4*a^2*(t+1/12) - a^2) / (a*(a^2+12*a^2*(t+1/12)))
               = 2*a*(t+1/12)*(4t+1/3-1) / (1+12t+1)
               [let me compute properly]

Parametrize: a_total = a1+a2 = -S (S > 0), w = a1/a_total, so a1 = -wS, a2 = -(1-w)S.
c_i = a_i^2 * (t_i + 1/12).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from sympy import symbols, simplify, expand, Poly, factor, numer, denom, Rational, together

print("P04 CE-13b: Numerator extraction for b=0 margin")
print("=" * 70)

w, t1, t2 = symbols('w t1 t2', real=True)

# Parameters (WLOG a_total = -1, so S = 1)
a1 = -w
a2 = -(1 - w)
c1 = a1**2 * (t1 + Rational(1, 12))
c2 = a2**2 * (t2 + Rational(1, 12))

# Convolution
a_h = a1 + a2  # = -1
c_h = c1 + c2 + a1*a2/6

print("Computing 1/Phi_4 for p, q, h...")

def inv_phi(a, c):
    """1/Phi_4 = 2c(4c-a^2) / (a(a^2+12c))"""
    return 2*c*(4*c - a**2) / (a*(a**2 + 12*c))

f_p = inv_phi(a1, c1)
f_q = inv_phi(a2, c2)
f_h = inv_phi(a_h, c_h)

print("Computing margin...")
margin = f_h - f_p - f_q
margin_simplified = together(margin)

print("Extracting numerator and denominator...")
num = numer(margin_simplified)
den = denom(margin_simplified)

num_expanded = expand(num)
den_expanded = expand(den)

print(f"\nNumerator degree in w: ", end="")
num_poly_w = Poly(num_expanded, w)
print(num_poly_w.degree())

print(f"Denominator degree in w: ", end="")
den_poly_w = Poly(den_expanded, w)
print(den_poly_w.degree())

# Factor out w(1-w) from numerator
print("\nChecking if w(1-w) divides numerator...")
num_at_0 = num_expanded.subs(w, 0)
num_at_1 = num_expanded.subs(w, 1)
print(f"  num(w=0) = {simplify(num_at_0)}")
print(f"  num(w=1) = {simplify(num_at_1)}")

if simplify(num_at_0) == 0 and simplify(num_at_1) == 0:
    print("  YES: w(1-w) divides numerator.")
    # Extract the quotient
    from sympy import div as poly_div, Symbol
    # Use polynomial division
    rem1 = Poly(num_expanded, w)
    q1, r1 = rem1.div(Poly(w, w))
    print(f"  After dividing by w: remainder = {r1}")
    q2, r2 = q1.div(Poly(1 - w, w))
    print(f"  After dividing by (1-w): remainder = {r2}")

    H_poly = q2
    print(f"\n  H(w, t1, t2) degree in w: {H_poly.degree()}")

    # Get coefficients of H as polynomial in w
    H_expanded = expand(H_poly.as_expr())
    H_poly_w = Poly(H_expanded, w)
    coeffs = H_poly_w.all_coeffs()
    print(f"  H has {len(coeffs)} coefficients in w (degree {H_poly_w.degree()}):")
    for i, c in enumerate(coeffs):
        c_simp = simplify(c)
        print(f"    w^{H_poly_w.degree()-i}: {c_simp}")

    # Check total degree
    from sympy import total_degree
    td = total_degree(H_expanded, w, t1, t2)
    print(f"\n  Total degree of H(w, t1, t2): {td}")

    # Check denominator structure
    print(f"\nDenominator (expanded):")
    den_factored = factor(den_expanded)
    print(f"  {den_factored}")

    # Check sign of denominator on valid region
    # Valid: w in (0,1), t1 > -1/12, t2 > -1/12, and also need a1*(a1^2+12c1) < 0
    # Since a1 = -w < 0 and a1^2+12c1 = w^2+12w^2(t1+1/12) = w^2(1+12t1+1) = w^2(12t1+2)
    # So a1*(a1^2+12c1) = -w*w^2*(12t1+2) = -w^3*(12t1+2) < 0 when 12t1+2 > 0 (t1 > -1/6).
    print("\n  Denominator sign analysis:")
    print("  On valid region (w in (0,1), ti > 0), denominator is a product of factors")
    print("  involving a_i * (a_i^2 + 12c_i) which are all negative (since a_i < 0).")
    print("  Product of 3 negative terms = negative. So denominator < 0.")
    print("  => margin >= 0 iff numerator <= 0 iff w(1-w)*H <= 0 iff H <= 0.")
    print("  Wait -- need to check sign convention carefully.")

    # Let me just evaluate numerically
    print("\n  Numerical sign check:")
    for tt1, tt2, ww in [(0.5, 0.5, 0.3), (1.0, 2.0, 0.5), (0.1, 0.1, 0.5)]:
        m_val = float(margin_simplified.subs([(w, ww), (t1, tt1), (t2, tt2)]))
        n_val = float(num_expanded.subs([(w, ww), (t1, tt1), (t2, tt2)]))
        d_val = float(den_expanded.subs([(w, ww), (t1, tt1), (t2, tt2)]))
        print(f"    t1={tt1}, t2={tt2}, w={ww}: margin={m_val:.4e}, num={n_val:.4e}, den={d_val:.4e}")

else:
    print("  NO: w(1-w) does NOT divide numerator!")
    print(f"  num(0) = {num_at_0}")
    print(f"  num(1) = {num_at_1}")
