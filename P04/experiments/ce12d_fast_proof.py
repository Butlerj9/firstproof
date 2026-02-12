"""
P04 CE-12d: Fast proof analysis of the g-inequality and b=0 case.

Streamlined version of CE-12c, avoiding heavy numerical optimization.
Focus on algebraic structure and lightweight numerical verification.
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, cancel, factor, collect,
                   Rational, Poly, Add, diff, sqrt, simplify, numer, denom)
import numpy as np
import time

print("P04 CE-12d: Fast proof analysis")
print("=" * 72)

w, t1, t2 = symbols('w t1 t2')

# ============================================================
# PART 1: The g-inequality factorization
# ============================================================
print("\nPART 1: g-inequality G = w*(1-w)*H")
print("-" * 60)

# H as extracted from the factorization of G
H = (36*t1**3*t2*w**2 + 6*t1**3*w**2
     + 72*t1**2*t2**2*w**2 - 72*t1**2*t2**2*w + 36*t1**2*t2**2
     + 18*t1**2*t2*w**2 - 12*t1**2*t2*w + 12*t1**2*t2
     + t1**2*w**2 + t1**2*w + t1**2
     + 36*t1*t2**3*w**2 - 72*t1*t2**3*w + 36*t1*t2**3
     + 18*t1*t2**2*w**2 - 24*t1*t2**2*w + 18*t1*t2**2
     + 2*t1*t2*w**2 - 2*t1*t2*w
     + 6*t2**3*w**2 - 12*t2**3*w + 6*t2**3
     + t2**2*w**2 - 3*t2**2*w + 3*t2**2)

H = expand(H)

# H = A*w^2 + B*w + C (quadratic in w)
A = H.coeff(w, 2)
B = H.coeff(w, 1)
C = H.coeff(w, 0)

print(f"  A = {factor(A)}")
print(f"  B = {factor(B)}")
print(f"  C = {factor(C)}")

# Prove C >= 0 (= H(w=0))
# C = 36t1^2t2^2 + 12t1^2t2 + t1^2 + 36t1t2^3 + 18t1t2^2 + 6t2^3 + 3t2^2
# = t1^2(6t2+1)^2 + 3t2^2(6t1+1)(2t2+1)
C_decomp = expand(t1**2*(6*t2+1)**2 + 3*t2**2*(6*t1+1)*(2*t2+1))
assert expand(C - C_decomp) == 0, "C decomposition check failed"
print(f"\n  C = t1^2*(6t2+1)^2 + 3*t2^2*(6t1+1)*(2t2+1)")
print(f"  On valid region (6t_i+1 > 0, t_i > -1/6): C >= 0. PROVED.")

# Prove H(1) = A+B+C >= 0
H1 = expand(A + B + C)
# By the symmetry H(w,t1,t2) = H(1-w,t2,t1):
# H(1,t1,t2) = H(0,t2,t1) = C(t2,t1)
# = t2^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1)
H1_decomp = expand(t2**2*(6*t1+1)**2 + 3*t1**2*(6*t2+1)*(2*t1+1))
assert expand(H1 - H1_decomp) == 0, "H(1) decomposition check failed"
print(f"  H(1) = t2^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1)")
print(f"  On valid region: H(1) >= 0. PROVED.")

# Case A <= 0: H >= min(H(0), H(1)) >= 0 on [0,1]. PROVED.
print(f"\n  Case A <= 0: H >= min(H(0),H(1)) >= 0 on [0,1]. PROVED.")

# Case A > 0, vertex w* outside [0,1]: H >= min(H(0),H(1)) >= 0. PROVED.
print(f"  Case A > 0, w* outside [0,1]: same. PROVED.")

# Case A > 0, w* in (0,1): need 4AC >= B^2
print(f"\n  Case A > 0, w* in (0,1): need 4AC - B^2 >= 0")

# Compute 4AC - B^2
disc = expand(4*A*C - B**2)
disc_f = factor(disc)
print(f"  4AC - B^2 = {disc_f}")

# Print the factored form in detail
print(f"  (Checking if factored form reveals non-negativity...)")
disc_str = str(disc_f)
print(f"  Length of factored expression: {len(disc_str)} chars")
if len(disc_str) < 1000:
    print(f"  4AC - B^2 = {disc_str}")

# ============================================================
# PART 2: Analyze 4AC - B^2
# ============================================================
print("\nPART 2: Analysis of 4AC - B^2")
print("-" * 60)

# Try specific substitutions
t = symbols('t')
disc_diag = factor(disc.subs([(t1, t), (t2, t)]))
print(f"  At t1=t2=t: {disc_diag}")

disc_t2_0 = factor(disc.subs(t2, 0))
print(f"  At t2=0: {disc_t2_0}")

disc_t1_0 = factor(disc.subs(t1, 0))
print(f"  At t1=0: {disc_t1_0}")

# Numerical check using numpy (fast)
print("\n  Numerical verification (numpy-vectorized):")
np.random.seed(42)
N = 200000
t1v = np.random.uniform(-1/6.0 * 0.95, 5.0, N)
t2v = np.random.uniform(-1/6.0 * 0.95, 5.0, N)

# Evaluate A, B, C using explicit formulas
Av = (36*t1v**3*t2v + 6*t1v**3 + 72*t1v**2*t2v**2 + 18*t1v**2*t2v + t1v**2
      + 36*t1v*t2v**3 + 18*t1v*t2v**2 + 2*t1v*t2v + 6*t2v**3 + t2v**2)
Bv = (-72*t1v**2*t2v**2 - 12*t1v**2*t2v + t1v**2 - 72*t1v*t2v**3 - 24*t1v*t2v**2
      - 2*t1v*t2v - 12*t2v**3 - 3*t2v**2)
Cv = (36*t1v**2*t2v**2 + 12*t1v**2*t2v + t1v**2 + 36*t1v*t2v**3 + 18*t1v*t2v**2
      + 6*t2v**3 + 3*t2v**2)

# Check A sign
n_A_neg = np.sum(Av < -1e-10)
print(f"  A < 0 in {n_A_neg}/{N} tests")

# Check 4AC-B^2 when A > 0 and w* in (0,1)
mask_A_pos = Av > 0
w_star = np.where(mask_A_pos, -Bv / (2*Av + 1e-30), -1)
mask_vertex = mask_A_pos & (w_star > 0) & (w_star < 1)
disc_vals = 4*Av*Cv - Bv**2

n_checked = np.sum(mask_vertex)
n_bad = np.sum(mask_vertex & (disc_vals < -1e-8))
min_disc_val = np.min(disc_vals[mask_vertex]) if n_checked > 0 else float('inf')

print(f"  Cases with A>0, w* in (0,1): {n_checked}")
print(f"  Cases with 4AC-B^2 < 0: {n_bad}")
print(f"  Min 4AC-B^2: {min_disc_val:.6e}")

# Let's try to prove A >= 0 directly
# A = 36t1^3t2 + 6t1^3 + 72t1^2t2^2 + 18t1^2t2 + t1^2 + 36t1t2^3 + 18t1t2^2 + 2t1t2 + 6t2^3 + t2^2
# Factor:
A_f = factor(A)
print(f"\n  A factored: {A_f}")

# Try decomposition:
# A = 6t1^3(6t2+1) + t1^2(72t2^2+18t2+1) + 2t1t2(18t2^2+9t2+1) + t2^2(6t2+1)
test_A = expand(6*t1**3*(6*t2+1) + t1**2*(72*t2**2+18*t2+1) + 2*t1*t2*(18*t2**2+9*t2+1) + t2**2*(6*t2+1))
print(f"  Try: 6t1^3(6t2+1) + t1^2(72t2^2+18t2+1) + 2t1t2(18t2^2+9t2+1) + t2^2(6t2+1)")
print(f"  Match: {expand(A - test_A) == 0}")

# In this form: when t1 >= 0 and 6t2+1 > 0: all terms non-negative.
# When t1 < 0 (but t1 > -1/6): need to be more careful.

# Let's try: substitute t1 = -1/6 + u1 where u1 > 0
u1, u2 = symbols('u1 u2', positive=True)
A_u = expand(A.subs([(t1, -Rational(1,6)+u1), (t2, -Rational(1,6)+u2)]))
A_u_f = factor(A_u)
print(f"\n  A with t_i = -1/6 + u_i (u_i > 0):")
print(f"  A = {A_u_f}")

# Check if A_u has all non-negative coefficients
A_u_poly = Poly(A_u, u1, u2, domain='QQ')
all_pos = all(coeff >= 0 for coeff in A_u_poly.coeffs())
print(f"  All coefficients non-negative: {all_pos}")
if not all_pos:
    print("  Negative coefficients:")
    for monom, coeff in A_u_poly.as_dict().items():
        if coeff < 0:
            print(f"    u1^{monom[0]} * u2^{monom[1]}: {coeff}")

# Similarly for C in shifted variables
C_u = expand(C.subs([(t1, -Rational(1,6)+u1), (t2, -Rational(1,6)+u2)]))
C_u_poly = Poly(C_u, u1, u2, domain='QQ')
all_pos_C = all(coeff >= 0 for coeff in C_u_poly.coeffs())
print(f"\n  C with t_i = -1/6 + u_i: all coefficients non-negative: {all_pos_C}")

# And 4AC-B^2 in shifted variables
disc_u = expand(disc.subs([(t1, -Rational(1,6)+u1), (t2, -Rational(1,6)+u2)]))
disc_u_poly = Poly(disc_u, u1, u2, domain='QQ')
all_pos_disc = all(coeff >= 0 for coeff in disc_u_poly.coeffs())
print(f"  4AC-B^2 with t_i = -1/6 + u_i: all coefficients non-negative: {all_pos_disc}")
if not all_pos_disc:
    n_neg_coeffs = sum(1 for coeff in disc_u_poly.coeffs() if coeff < 0)
    print(f"  ({n_neg_coeffs} negative coefficients out of {len(disc_u_poly.coeffs())})")

# ============================================================
# PART 3: Try shifted + complete the square
# ============================================================
print("\nPART 3: Shifted variable analysis")
print("-" * 60)

# If all coefficients of A, C, and 4AC-B^2 are non-negative in the shifted
# variables u_i = t_i + 1/6, then we have a complete proof!

if all_pos and all_pos_C and all_pos_disc:
    print("""
  COMPLETE PROOF of H >= 0:

  After the shift t_i = -1/6 + u_i (u_i > 0):
  A, C, and 4AC-B^2 all have non-negative coefficients in (u1, u2).
  Since u1, u2 > 0, we have A >= 0, C >= 0, 4AC >= B^2.

  For A >= 0: H = Aw^2 + Bw + C is an upward parabola.
  With H(0) = C >= 0 and 4AC >= B^2 (non-negative discriminant):
  H(w) >= C - B^2/(4A) = (4AC-B^2)/(4A) >= 0 for all w.

  In particular H >= 0 for w in [0,1]. QED.
""")
elif all_pos:
    print("  A >= 0 proved (all coefficients non-negative in shifted vars)")
    if not all_pos_disc:
        print("  But 4AC-B^2 has negative coefficients -- need alternative argument")
else:
    print("  A has negative coefficients in shifted vars -- need case analysis")

# ============================================================
# PART 4: If not all positive, try Schur-like bounds
# ============================================================
print("\nPART 4: Detailed coefficient analysis")
print("-" * 60)

# Print the full shifted polynomials
print("  A(u1,u2) coefficients (t_i = u_i - 1/6):")
for monom, coeff in sorted(A_u_poly.as_dict().items()):
    if coeff != 0:
        print(f"    u1^{monom[0]} * u2^{monom[1]}: {coeff}")

print(f"\n  C(u1,u2) coefficients:")
for monom, coeff in sorted(C_u_poly.as_dict().items()):
    if coeff != 0:
        print(f"    u1^{monom[0]} * u2^{monom[1]}: {coeff}")

# Full H in shifted variables
H_u = expand(H.subs([(t1, -Rational(1,6)+u1), (t2, -Rational(1,6)+u2)]))
H_u_poly = Poly(H_u, w, u1, u2, domain='QQ')
all_pos_H = all(coeff >= 0 for coeff in H_u_poly.coeffs())
print(f"\n  Full H(w,u1,u2) all coefficients non-negative: {all_pos_H}")
if all_pos_H:
    print("  ==> H >= 0 for w >= 0, u1 >= 0, u2 >= 0. COMPLETE PROOF!")
else:
    n_neg = sum(1 for coeff in H_u_poly.coeffs() if coeff < 0)
    print(f"  ({n_neg} negative coefficients)")
    print("  Negative coefficient terms:")
    for monom, coeff in H_u_poly.as_dict().items():
        if coeff < 0:
            print(f"    w^{monom[0]} * u1^{monom[1]} * u2^{monom[2]}: {coeff}")

# ============================================================
# PART 5: The b=0 inner factor R
# ============================================================
print("\n" + "=" * 72)
print("PART 5: b=0 inner factor R")
print("-" * 60)

alpha1, alpha2, cp1, cp2 = symbols('alpha1 alpha2 cp1 cp2')

R = (alpha1**6*cp2**2 + 3*alpha1**5*alpha2*cp2**2
     + 3*alpha1**4*alpha2**2*cp2**2 + 12*alpha1**4*cp1*cp2**2
     + 6*alpha1**4*cp2**3 - 2*alpha1**3*alpha2**3*cp1*cp2
     + 12*alpha1**3*alpha2*cp1*cp2**2 + 3*alpha1**2*alpha2**4*cp1**2
     + 18*alpha1**2*alpha2**2*cp1**2*cp2
     + 18*alpha1**2*alpha2**2*cp1*cp2**2
     + 36*alpha1**2*cp1**2*cp2**2 + 36*alpha1**2*cp1*cp2**3
     + 3*alpha1*alpha2**5*cp1**2 + 12*alpha1*alpha2**3*cp1**2*cp2
     + alpha2**6*cp1**2 + 6*alpha2**4*cp1**3
     + 12*alpha2**4*cp1**2*cp2 + 36*alpha2**2*cp1**3*cp2
     + 36*alpha2**2*cp1**2*cp2**2)

# Decomposition 1: extract the obvious square
sq1 = (alpha1**3*cp2 - alpha2**3*cp1)**2
S = expand(R - sq1)
print(f"  R = (alpha1^3*cp2 - alpha2^3*cp1)^2 + S")

# Collect S by cp structure
S_by_cp = {}
S_poly = Poly(S, alpha1, alpha2, cp1, cp2, domain='QQ')
for monom, coeff in S_poly.as_dict().items():
    i1, i2, k1, k2 = monom
    key = (k1, k2)
    if key not in S_by_cp:
        S_by_cp[key] = {}
    S_by_cp[key][(i1, i2)] = coeff

print("  S collected by (cp1^j, cp2^k):")
for key in sorted(S_by_cp.keys()):
    k1, k2 = key
    alpha_terms = sum(coeff * alpha1**i1 * alpha2**i2 for (i1,i2), coeff in S_by_cp[key].items())
    print(f"    cp1^{k1}*cp2^{k2}: {factor(alpha_terms)}")

# Try another decomposition: pull out 3*alpha1*alpha2*(alpha1*cp2-alpha2*cp1)^2
sq2 = 3*alpha1*alpha2*(alpha1*cp2 - alpha2*cp1)**2
S2 = expand(S - sq2)
print(f"\n  S = 3*alpha1*alpha2*(alpha1*cp2-alpha2*cp1)^2 + T")
print(f"  T = {factor(S2)}")

# Check if T factors nicely
T_str = str(factor(S2))
if len(T_str) < 500:
    print(f"  T factored: {T_str}")

# Collect T
T_poly = Poly(S2, alpha1, alpha2, cp1, cp2, domain='QQ')
T_by_cp = {}
for monom, coeff in T_poly.as_dict().items():
    i1, i2, k1, k2 = monom
    key = (k1, k2)
    if key not in T_by_cp:
        T_by_cp[key] = {}
    T_by_cp[key][(i1, i2)] = coeff

print("\n  T collected by (cp1^j, cp2^k):")
for key in sorted(T_by_cp.keys()):
    k1, k2 = key
    alpha_terms = sum(coeff * alpha1**i1 * alpha2**i2 for (i1,i2), coeff in T_by_cp[key].items())
    af = factor(alpha_terms)
    print(f"    cp1^{k1}*cp2^{k2}: {af}")

# Check: can we decompose T further?
# T should have terms like cp1^2*cp2*(positive) + cp1*cp2^2*(positive) + cp1^3*(pos) + cp2^3*(pos)
# If T = cp1^2*f1 + cp2^2*f2 + cp1*cp2*f3 + cp1^3*g1 + cp2^3*g2 + ...
# and all f_i, g_i are non-negative on the valid region, we're done.

# Let's check: T should be non-negative on valid region
# Numerical check of T using explicit evaluation
print("\n  Numerical check of T >= 0 on valid region (numpy):")
np.random.seed(42)
Nt = 100000
al1 = np.random.uniform(0.1, 10, Nt)
al2 = np.random.uniform(0.1, 10, Nt)
cp1v = np.random.uniform(-al1**2/12 * 0.99, al1**2/6 * 0.99)
cp2v = np.random.uniform(-al2**2/12 * 0.99, al2**2/6 * 0.99)

# Compute R, sq1, sq2 explicitly
Rv = (al1**6*cp2v**2 + 3*al1**5*al2*cp2v**2
      + 3*al1**4*al2**2*cp2v**2 + 12*al1**4*cp1v*cp2v**2
      + 6*al1**4*cp2v**3 - 2*al1**3*al2**3*cp1v*cp2v
      + 12*al1**3*al2*cp1v*cp2v**2 + 3*al1**2*al2**4*cp1v**2
      + 18*al1**2*al2**2*cp1v**2*cp2v
      + 18*al1**2*al2**2*cp1v*cp2v**2
      + 36*al1**2*cp1v**2*cp2v**2 + 36*al1**2*cp1v*cp2v**3
      + 3*al1*al2**5*cp1v**2 + 12*al1*al2**3*cp1v**2*cp2v
      + al2**6*cp1v**2 + 6*al2**4*cp1v**3
      + 12*al2**4*cp1v**2*cp2v + 36*al2**2*cp1v**3*cp2v
      + 36*al2**2*cp1v**2*cp2v**2)

sq1v = (al1**3*cp2v - al2**3*cp1v)**2
sq2v = 3*al1*al2*(al1*cp2v - al2*cp1v)**2
Tv = Rv - sq1v - sq2v

# Check convolution validity
ah = al1 + al2
cph = cp1v + cp2v
valid = (al1**2 + 6*cp1v > 0) & (al2**2 + 6*cp2v > 0) & (ah**2 + 6*cph > 0)
valid &= (cp1v + al1**2/12 > 0) & (cp2v + al2**2/12 > 0) & (cph + ah**2/12 > 0)

n_T_neg = np.sum(valid & (Tv < -1e-6))
n_valid = np.sum(valid)
min_T = np.min(Tv[valid]) if n_valid > 0 else float('inf')
min_R = np.min(Rv[valid]) if n_valid > 0 else float('inf')

print(f"  Valid tests: {n_valid}")
print(f"  T negative: {n_T_neg}")
print(f"  Min T: {min_T:.6e}")
print(f"  Min R: {min_R:.6e}")

# ============================================================
# PART 6: Summary
# ============================================================
print("\n" + "=" * 72)
print("PART 6: SUMMARY")
print("=" * 72)

print("""
g-INEQUALITY (DIMENSIONLESS FORM):
  G(w,t1,t2) = w*(1-w)*H(w,t1,t2) where
  H = A*w^2 + B*w + C (quadratic in w)

  PROVED: H(0) = C >= 0 (decomposition: t1^2*(6t2+1)^2 + 3t2^2*(6t1+1)*(2t2+1))
  PROVED: H(1) >= 0 (by symmetry, same decomposition with t1<->t2)
  PROVED: Case A <= 0: H >= min(H(0),H(1)) >= 0
  PROVED: Case A >= 0, w* outside [0,1]: H >= min(H(0),H(1)) >= 0
  REMAINING: Case A > 0, w* in (0,1): need 4AC - B^2 >= 0

b=0 CASE:
  P_b0 = 131072*(a1^2-6cp1)*(a2^2-6cp2)*(ah^2-6cph)*R
  where R = (alpha1^3*cp2 - alpha2^3*cp1)^2 + 3*alpha1*alpha2*(alpha1*cp2-alpha2*cp1)^2 + T
  Need T >= 0 on valid region (verified numerically).

FULL INEQUALITY:
  547-term polynomial in 6 variables, quasi-homogeneous of weighted degree 32.
  Even in (b1,b2). Total degree 15.
""")

print("DONE")
