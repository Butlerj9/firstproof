"""
P04 CE-13c: Attempt SOS-like decomposition of -H(w, t1, t2).

-H must be >= 0 on: w in (0,1), t1, t2 in (-1/12, 1/6).

Strategy: substitute p = 12t + 1 in (0, 3) for each ti, and s = w in (0,1).
Then try to express -H as a sum of non-negative terms.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from sympy import symbols, expand, Rational, factor, collect, Poly, groebner
from sympy import simplify

print("P04 CE-13c: SOS attempt for -H")
print("=" * 70)

w, t1, t2 = symbols('w t1 t2')

# H coefficients from CE-13b
A_coef = (-5184*t1**3*t2 - 864*t1**3 - 10368*t1**2*t2**2 - 2592*t1**2*t2
           - 144*t1**2 - 5184*t1*t2**3 - 2592*t1*t2**2 - 288*t1*t2
           - 864*t2**3 - 144*t2**2)

B_coef = (10368*t1**2*t2**2 + 1728*t1**2*t2 - 144*t1**2 + 10368*t1*t2**3
          + 3456*t1*t2**2 + 288*t1*t2 + 1728*t2**3 + 432*t2**2)

C_coef = (-5184*t1**2*t2**2 - 1728*t1**2*t2 - 144*t1**2 - 5184*t1*t2**3
          - 2592*t1*t2**2 - 864*t2**3 - 432*t2**2)

H = A_coef * w**2 + B_coef * w + C_coef
neg_H = expand(-H)

print("H(w,t1,t2) = A*w^2 + B*w + C")
print(f"\nA = {A_coef}")
print(f"\nB = {B_coef}")
print(f"\nC = {C_coef}")

# Factor out common factors
print("\n--- Factoring -H ---")
neg_H_factored = factor(neg_H)
print(f"-H factored: {neg_H_factored}")

# Try collecting by different variables
print("\n--- Collect -H by t1 ---")
neg_H_t1 = collect(neg_H, t1)
print(f"-H collected by t1:\n{neg_H_t1}")

# Factor -A (w^2 coefficient of -H)
neg_A = expand(-A_coef)
print(f"\n-A = {neg_A}")
neg_A_factored = factor(neg_A)
print(f"-A factored = {neg_A_factored}")

# Factor -C (w^0 coefficient of -H)
neg_C = expand(-C_coef)
print(f"\n-C = {neg_C}")
neg_C_factored = factor(neg_C)
print(f"-C factored = {neg_C_factored}")

# Factor -B (w^1 coefficient of -H, with sign flip)
neg_B = expand(-B_coef)
print(f"\n-B = {neg_B}")
neg_B_factored = factor(neg_B)
print(f"-B factored = {neg_B_factored}")

# Key question: is -H = sum of non-negative terms?
# -H is quadratic in w with leading coefficient -A.
# If -A >= 0 and discriminant (-B)^2 - 4*(-A)*(-C) = B^2 - 4AC <= 0,
# then -H >= 0 everywhere.
# We already know 4AC - B^2 = 3*(t1+t2)^2 * Q where Q can be negative.
# So discriminant approach fails globally.

# Try substitution: p_i = 12*t_i + 1 in (0, 3)
p1, p2 = symbols('p1 p2', positive=True)
# t_i = (p_i - 1)/12
neg_H_sub = neg_H.subs([(t1, (p1-1)/12), (t2, (p2-1)/12)])
neg_H_sub = expand(neg_H_sub)

# Clear denominators (12^6 = 2985984)
neg_H_cleared = expand(neg_H_sub * 12**6)
print(f"\n-H in (w, p1, p2) variables (x 12^6):")
neg_H_poly = Poly(neg_H_cleared, w, p1, p2)
print(f"  Total degree: {neg_H_poly.total_degree()}")
print(f"  Terms: {len(neg_H_poly.as_dict())}")

# Check if all coefficients are non-negative (would give SOS-free proof on p_i > 0)
coeffs_dict = neg_H_poly.as_dict()
n_pos = sum(1 for v in coeffs_dict.values() if v > 0)
n_neg = sum(1 for v in coeffs_dict.values() if v < 0)
n_zero = sum(1 for v in coeffs_dict.values() if v == 0)
print(f"  Positive coefficients: {n_pos}")
print(f"  Negative coefficients: {n_neg}")
print(f"  Zero coefficients: {n_zero}")

if n_neg == 0:
    print("  ** ALL COEFFICIENTS NON-NEGATIVE! Polynomial is non-negative on p_i > 0. **")
else:
    print(f"\n  Negative coefficient terms:")
    for (e_w, e_p1, e_p2), coeff in sorted(coeffs_dict.items()):
        if coeff < 0:
            print(f"    w^{e_w} * p1^{e_p1} * p2^{e_p2}: {coeff}")

# Also try domain constraint: p_i in (0, 3), so substitute p_i = 3*s_i with s_i in (0,1)
s1, s2 = symbols('s1 s2', positive=True)
neg_H_s = neg_H_cleared.subs([(p1, 3*s1), (p2, 3*s2)])
neg_H_s = expand(neg_H_s)
neg_H_s_poly = Poly(neg_H_s, w, s1, s2)
coeffs_s = neg_H_s_poly.as_dict()
n_pos_s = sum(1 for v in coeffs_s.values() if v > 0)
n_neg_s = sum(1 for v in coeffs_s.values() if v < 0)
print(f"\n  In s_i = p_i/3 variables (s_i in (0,1)):")
print(f"  Positive coefficients: {n_pos_s}")
print(f"  Negative coefficients: {n_neg_s}")

if n_neg_s == 0:
    print("  ** ALL COEFFICIENTS NON-NEGATIVE on s_i > 0! **")
else:
    print(f"\n  Negative terms in s-variables:")
    for (e_w, e_s1, e_s2), coeff in sorted(coeffs_s.items()):
        if coeff < 0:
            print(f"    w^{e_w} * s1^{e_s1} * s2^{e_s2}: {coeff}")
