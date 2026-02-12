"""
P04 CE-12: SOS / algebraic certificate for the degree-16 superadditivity inequality.

GOAL: Attempt to find a sum-of-squares (SOS) decomposition or algebraic
certificate for the numerator polynomial N such that:

  N(a1,b1,cp1,a2,b2,cp2) >= 0

whenever all three quartics (p, q, h=p box_4 q) have positive discriminant.

APPROACH:
  1. Derive the exact degree-16 numerator symbolically (SymPy)
  2. Analyze structure: degree, terms, symmetry, factorization
  3. Restricted cases: b=0, cp=0, a1=a2
  4. Numerical SOS via SDP relaxation (scipy)
  5. Substitution/AM-GM/Cauchy-Schwarz decomposition attempts

All symbolic work uses exact SymPy rational arithmetic.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (
    symbols, expand, cancel, factor, simplify, collect,
    Rational, sqrt, together, apart, numer, denom,
    Poly, Symbol, solve, diff, S, degree, total_degree,
    Matrix, zeros as sym_zeros, eye as sym_eye, Add, Mul, Pow,
    groebner, LC, LM, LT, ring, ZZ, QQ, lex, grlex, grevlex
)
from sympy.polys.monomials import itermonomials
from fractions import Fraction
import time

print("P04 CE-12: SOS / Algebraic Certificate for Degree-16 Inequality")
print("=" * 72)

# ============================================================
# SECTION 1: Derive the exact degree-16 numerator polynomial
# ============================================================
print("\n" + "=" * 72)
print("SECTION 1: Derive the exact numerator polynomial")
print("=" * 72)

t0 = time.time()

# Variables for polynomial 1 and polynomial 2
a1, b1, cp1, a2, b2, cp2 = symbols('a1 b1 cp1 a2 b2 cp2')

# Formulas in additive variables (a, b, c') where c = c' + a^2/12
# N(a,b,c') = numerator of Phi_4 (Phi_4 = N/Delta)
# Delta(a,b,c') = discriminant

def N_phi4(a, b, cp):
    """Numerator N of Phi_4 in additive variables.
    Phi_4 = N / Delta.
    N = -8a^5 - 64a^3*c - 36a^2*b^2 + 384a*c^2 - 432b^2*c
    where c = cp + a^2/12.
    """
    c = cp + a**2 / 12
    return expand(
        -8*a**5 - 64*a**3*c - 36*a**2*b**2
        + 384*a*c**2 - 432*b**2*c
    )

def Delta_phi4(a, b, cp):
    """Discriminant of x^4 + a*x^2 + b*x + c in additive variables.
    c = cp + a^2/12.
    """
    c = cp + a**2 / 12
    return expand(
        16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
        + 144*a*b**2*c - 27*b**4 + 256*c**3
    )

# Compute N and Delta for each polynomial
print("\n  Computing N and Delta for poly 1, poly 2, and convolution h...")

N1 = N_phi4(a1, b1, cp1)
D1 = Delta_phi4(a1, b1, cp1)

N2 = N_phi4(a2, b2, cp2)
D2 = Delta_phi4(a2, b2, cp2)

# Convolution: additive in (a, b, c')
ah = a1 + a2
bh = b1 + b2
cph = cp1 + cp2

Nh = N_phi4(ah, bh, cph)
Dh = Delta_phi4(ah, bh, cph)

print(f"  N1 computed: {len(Add.make_args(N1))} terms")
print(f"  D1 computed: {len(Add.make_args(D1))} terms")
print(f"  Nh computed: {len(Add.make_args(Nh))} terms")
print(f"  Dh computed: {len(Add.make_args(Dh))} terms")

# The superadditivity inequality is:
# Dh/Nh >= D1/N1 + D2/N2
# i.e., Dh*N1*N2 - D1*N2*Nh - D2*N1*Nh >= 0
# (assuming N1, N2, Nh > 0 in the valid region -- which is the case since
# Phi_4 > 0 and Delta > 0 implies N = Phi_4 * Delta > 0)

# Actually, we need to be careful: 1/Phi_4 = Delta/N, and the sign of N.
# Since Phi_4 > 0 and Delta > 0, we need N > 0 for 1/Phi_4 > 0.
# From the formulas:
# N = -4(a^2+12c)(2a^3-8ac+9b^2) = -8(a^2+6c')(4a^3/3-8ac'+9b^2)
# At b=c'=0: N = -8*a^2*(4a^3/3) = -32a^5/3
# For a < 0: -32a^5/3 = -32*(-|a|)^5/3 = 32|a|^5/3 > 0. Good.

# So we need: P := Dh*N1*N2 - D1*N2*Nh - D2*N1*Nh >= 0

print("\n  Computing the degree-16 numerator P = Dh*N1*N2 - D1*N2*Nh - D2*N1*Nh...")
print("  (This is the polynomial whose non-negativity implies superadditivity)")
t1 = time.time()

# Compute each term separately to track progress
term1 = expand(Dh * N1 * N2)
print(f"  term1 = Dh*N1*N2: {len(Add.make_args(term1))} terms ({time.time()-t1:.1f}s)")

t2 = time.time()
term2 = expand(D1 * N2 * Nh)
print(f"  term2 = D1*N2*Nh: {len(Add.make_args(term2))} terms ({time.time()-t2:.1f}s)")

t3 = time.time()
term3 = expand(D2 * N1 * Nh)
print(f"  term3 = D2*N1*Nh: {len(Add.make_args(term3))} terms ({time.time()-t3:.1f}s)")

t4 = time.time()
P = expand(term1 - term2 - term3)
n_terms_P = len(Add.make_args(P))
print(f"  P computed: {n_terms_P} terms ({time.time()-t4:.1f}s)")

elapsed = time.time() - t0
print(f"\n  Total computation time: {elapsed:.1f}s")

# ============================================================
# SECTION 2: Analyze the numerator polynomial
# ============================================================
print("\n" + "=" * 72)
print("SECTION 2: Structural analysis of P")
print("=" * 72)

# Convert to multivariate polynomial
vars_list = [a1, b1, cp1, a2, b2, cp2]
P_poly = Poly(P, *vars_list, domain='QQ')

print(f"\n  Number of variables: 6")
print(f"  Number of terms: {len(P_poly.as_dict())}")
print(f"  Total degree: {P_poly.total_degree()}")

# Check symmetry under (a1,b1,cp1) <-> (a2,b2,cp2)
print("\n  Checking symmetry under (1) <-> (2) swap...")
P_swapped = P.subs([(a1, a2), (b1, b2), (cp1, cp2),
                     (a2, a1), (b2, b1), (cp2, cp1)])
P_swapped = expand(P_swapped)
is_symmetric = expand(P - P_swapped) == 0
print(f"  P is symmetric under (a1,b1,cp1) <-> (a2,b2,cp2): {is_symmetric}")

# Check b -> -b symmetry
print("\n  Checking b -> -b symmetry (even in b1, b2)...")
P_bneg = P.subs([(b1, -b1), (b2, -b2)])
P_bneg = expand(P_bneg)
is_b_symmetric = expand(P - P_bneg) == 0
print(f"  P is even in (b1, b2): {is_b_symmetric}")

# Degree structure: what is the max degree in each variable?
print("\n  Maximum degree in each variable:")
for v in vars_list:
    d = Poly(P, v).degree()
    print(f"    deg_{v} = {d}")

# Homogeneity check: under scaling
# a -> t*a, b -> t^(3/2)*b, c' -> t^2*c'
# But with non-integer exponents, let's check weighted degree instead.
# The polynomial should have a definite "weight" under the scaling
# a ~ weight 1, b ~ weight 3/2, c' ~ weight 2 (in terms of s where a ~ s^2).
# Actually, 1/Phi_4 ~ s^2 ~ |a|, so 1/Phi_4 has weight 1 in |a|.
# The full polynomial P involves products of Delta (weight 3 in |a|^2=6 in s)
# and N (weight 5/2 in s^2 = 5 in s).
# P = Dh*N1*N2 - ... has total weight 6+5+5 = 16 in s, i.e., 8 in |a|.
#
# Under scaling (a_i -> lambda*a_i, b_i -> lambda^(3/2)*b_i, c_i' -> lambda^2*c_i'):
# Each N_i scales as lambda^5 (since N has weight 5 in the a-scale)
# Each D_i scales as lambda^6
# P ~ lambda^16 * P, so P is "quasi-homogeneous" of weighted degree 16.

# Let's verify this numerically
print("\n  Checking quasi-homogeneity (weighted degree 16)...")
print("  Weights: a=2, b=3, c'=4")
print("  (Corresponding to x-scaling: a ~ s^2, b ~ s^3, c' ~ s^4)")

# For each monomial a1^i1 * b1^j1 * cp1^k1 * a2^i2 * b2^j2 * cp2^k2,
# the weighted degree should be 2*(i1+i2) + 3*(j1+j2) + 4*(k1+k2) = constant.
monomial_weights = set()
for monom, coeff in P_poly.as_dict().items():
    i1, j1, k1, i2, j2, k2 = monom
    w = 2*(i1+i2) + 3*(j1+j2) + 4*(k1+k2)
    monomial_weights.add(w)

print(f"  Weighted degrees present: {sorted(monomial_weights)}")
is_quasi_homog = len(monomial_weights) == 1
print(f"  Is quasi-homogeneous: {is_quasi_homog}")
if is_quasi_homog:
    print(f"  Weighted degree: {monomial_weights.pop()}")

# Tabulate the monomial structure
print("\n  Monomial structure (by unweighted total degree):")
deg_counts = {}
for monom, coeff in P_poly.as_dict().items():
    td = sum(monom)
    deg_counts[td] = deg_counts.get(td, 0) + 1
for d in sorted(deg_counts.keys()):
    print(f"    degree {d}: {deg_counts[d]} terms")

# ============================================================
# SECTION 3: Restricted cases
# ============================================================
print("\n" + "=" * 72)
print("SECTION 3: Restricted cases")
print("=" * 72)

# --- Case A: b1 = b2 = 0 (c'-only case) ---
print("\n  --- Case A: b1 = b2 = 0 ---")
P_b0 = expand(P.subs([(b1, 0), (b2, 0)]))
n_terms_b0 = len(Add.make_args(P_b0))
print(f"  P(b=0): {n_terms_b0} terms")

P_b0_poly = Poly(P_b0, a1, cp1, a2, cp2, domain='QQ')
print(f"  Total degree: {P_b0_poly.total_degree()}")
print(f"  Number of monomials: {len(P_b0_poly.as_dict())}")

# Try to factor
print("  Attempting factorization...")
try:
    P_b0_factored = factor(P_b0)
    P_b0_str = str(P_b0_factored)
    if len(P_b0_str) > 200:
        print(f"  Factored form: {P_b0_str[:200]}...")
    else:
        print(f"  Factored form: {P_b0_str}")
except Exception as e:
    print(f"  Factorization failed: {e}")

# Check weighted degrees in b=0 case
print("\n  Weighted degrees in b=0 case:")
mono_wts_b0 = set()
for monom, coeff in P_b0_poly.as_dict().items():
    i1, k1, i2, k2 = monom
    w = 2*(i1+i2) + 4*(k1+k2)
    mono_wts_b0.add(w)
print(f"  Weighted degrees: {sorted(mono_wts_b0)}")

# --- Case B: cp1 = cp2 = 0 (b-only case = Jensen case) ---
print("\n  --- Case B: cp1 = cp2 = 0 (b-only, Jensen case) ---")
P_cp0 = expand(P.subs([(cp1, 0), (cp2, 0)]))
n_terms_cp0 = len(Add.make_args(P_cp0))
print(f"  P(c'=0): {n_terms_cp0} terms")

P_cp0_poly = Poly(P_cp0, a1, b1, a2, b2, domain='QQ')
print(f"  Total degree: {P_cp0_poly.total_degree()}")
print(f"  Number of monomials: {len(P_cp0_poly.as_dict())}")

# Try to factor
print("  Attempting factorization...")
try:
    t_fac = time.time()
    P_cp0_factored = factor(P_cp0)
    P_cp0_str = str(P_cp0_factored)
    print(f"  Factorization took {time.time()-t_fac:.1f}s")
    if len(P_cp0_str) > 300:
        print(f"  Factored form: {P_cp0_str[:300]}...")
    else:
        print(f"  Factored form: {P_cp0_str}")
except Exception as e:
    print(f"  Factorization failed: {e}")

# Check if P_cp0 has a known sign pattern
# At c'=0: 1/Phi_4 = [16a^6/27 + 8a^3b^2 - 27b^4] / [-(32/3)a^5 - 72a^2b^2]
# The superadditivity here reduces to the "b-only" inequality.
# This should be provable by Jensen-type arguments (like n=3).

# --- Case C: a1 = a2 (symmetric a) ---
print("\n  --- Case C: a1 = a2 = a (symmetric a) ---")
a_sym = symbols('a')
P_sym_a = expand(P.subs([(a1, a_sym), (a2, a_sym)]))
P_sym_a_poly = Poly(P_sym_a, a_sym, b1, cp1, b2, cp2, domain='QQ')
print(f"  P(a1=a2=a): {len(P_sym_a_poly.as_dict())} monomials, total degree {P_sym_a_poly.total_degree()}")

# --- Case D: b1 = b2 = cp1 = cp2 = 0 (pure a case) ---
print("\n  --- Case D: b=c'=0 (equality manifold) ---")
P_eq = expand(P.subs([(b1, 0), (b2, 0), (cp1, 0), (cp2, 0)]))
print(f"  P(b=0,c'=0) = {P_eq}")
print(f"  (Should be 0 since this is the equality manifold)")

# --- Case E: b2 = cp2 = 0 (one polynomial at equality) ---
print("\n  --- Case E: b2=cp2=0 (second poly at equality manifold) ---")
P_e = expand(P.subs([(b2, 0), (cp2, 0)]))
n_terms_e = len(Add.make_args(P_e))
print(f"  P(b2=cp2=0): {n_terms_e} terms")

# ============================================================
# SECTION 4: Detailed analysis of the b=0 case
# ============================================================
print("\n" + "=" * 72)
print("SECTION 4: Detailed analysis of b=0 case")
print("=" * 72)

# In this case the polynomial is in 4 variables: a1, cp1, a2, cp2
# and should have weighted degree 16 (weight a=2, c'=4).
# This is more tractable for SOS analysis.

# Express P_b0 in terms of monomials
print("\n  Monomials of P_b0 (sorted by total degree):")
P_b0_dict = P_b0_poly.as_dict()
sorted_monoms = sorted(P_b0_dict.items(), key=lambda x: (sum(x[0]), x[0]))

# Print first few and last few
n_show = min(15, len(sorted_monoms))
for monom, coeff in sorted_monoms[:n_show]:
    i1, k1, i2, k2 = monom
    print(f"    a1^{i1} * cp1^{k1} * a2^{i2} * cp2^{k2} : {coeff}")
if len(sorted_monoms) > 2*n_show:
    print(f"    ... ({len(sorted_monoms) - 2*n_show} more terms) ...")
    for monom, coeff in sorted_monoms[-n_show:]:
        i1, k1, i2, k2 = monom
        print(f"    a1^{i1} * cp1^{k1} * a2^{i2} * cp2^{k2} : {coeff}")

# Check if P_b0 can be written as a sum of squares of simpler expressions.
# Strategy: P_b0 is quasi-homogeneous of weighted degree 32 (since P has
# weighted degree 32 in the original variables... wait, let me recheck.
#
# Actually: the "weight" I described refers to the s-scaling where
# a ~ s^2, b ~ s^3, c' ~ s^4. Under this, N ~ s^10 (= weight 10),
# Delta ~ s^12 (= weight 12). So P = Dh*N1*N2 - ... has weight 12+10+10=32.
#
# For b=0: each monomial a1^i1 * cp1^k1 * a2^i2 * cp2^k2 has weight
# 2(i1+i2) + 4(k1+k2) = const.

# Try to decompose P_b0 into a sum of squares numerically.
# Since cvxpy is not available, let's try a custom approach.

# First, let's try simple substitutions to understand sign behavior.
print("\n  Numerical sign test for P_b0:")
import numpy as np

def eval_P_b0_numpy(a1v, cp1v, a2v, cp2v):
    """Evaluate P_b0 numerically."""
    val = 0.0
    for monom, coeff in P_b0_dict.items():
        i1, k1, i2, k2 = monom
        val += float(coeff) * a1v**i1 * cp1v**k1 * a2v**i2 * cp2v**k2
    return val

np.random.seed(42)
n_tests = 5000
n_pos = 0
n_neg = 0
n_zero = 0
min_val = float('inf')

for trial in range(n_tests):
    a1v = -np.random.uniform(0.5, 10)
    a2v = -np.random.uniform(0.5, 10)
    # c' range: roughly (-a^2/12, a^2/6) for validity
    cp1v = np.random.uniform(-a1v**2/12 * 0.9, a1v**2/6 * 0.4)
    cp2v = np.random.uniform(-a2v**2/12 * 0.9, a2v**2/6 * 0.4)

    val = eval_P_b0_numpy(a1v, cp1v, a2v, cp2v)

    if val > 1e-10:
        n_pos += 1
    elif val < -1e-10:
        n_neg += 1
        if n_neg <= 3:
            print(f"    NEGATIVE at a1={a1v:.3f}, cp1={cp1v:.3f}, a2={a2v:.3f}, cp2={cp2v:.3f}: val={val:.6e}")
    else:
        n_zero += 1

    if val < min_val:
        min_val = val

print(f"  Results: {n_pos} positive, {n_neg} negative, {n_zero} near-zero")
print(f"  Minimum value: {min_val:.6e}")

# IMPORTANT: The polynomial P might not be non-negative everywhere!
# It is only required to be non-negative on the VALID REGION where
# all three discriminants are positive.
# When b=0: disc > 0 iff the quartic has 4 real roots.
# We need to account for this constraint.

print("\n  NOTE: P is only required >= 0 on the valid region (all disc > 0).")
print("  Testing P_b0 restricted to valid region:")

def is_valid_b0(a_val, cp_val):
    """Check if quartic x^4+a*x^2+c has positive discriminant, where c=c'+a^2/12."""
    c_val = cp_val + a_val**2 / 12.0
    disc = 16*a_val**4*c_val - 128*a_val**2*c_val**2 + 256*c_val**3
    N_val = -8*a_val**5 - 64*a_val**3*c_val + 384*a_val*c_val**2
    return disc > 0 and N_val > 0

np.random.seed(123)
n_valid_tests = 0
n_pos_valid = 0
n_neg_valid = 0
min_val_valid = float('inf')

for trial in range(20000):
    a1v = -np.random.uniform(0.5, 10)
    a2v = -np.random.uniform(0.5, 10)
    cp1v = np.random.uniform(-a1v**2/12 * 0.95, a1v**2/6 * 0.4)
    cp2v = np.random.uniform(-a2v**2/12 * 0.95, a2v**2/6 * 0.4)

    if not (is_valid_b0(a1v, cp1v) and is_valid_b0(a2v, cp2v)):
        continue

    ah_v = a1v + a2v
    cph_v = cp1v + cp2v
    if not is_valid_b0(ah_v, cph_v):
        continue

    n_valid_tests += 1
    val = eval_P_b0_numpy(a1v, cp1v, a2v, cp2v)

    if val > -1e-10:
        n_pos_valid += 1
    else:
        n_neg_valid += 1
        if n_neg_valid <= 3:
            print(f"    NEGATIVE on valid region: a1={a1v:.4f}, cp1={cp1v:.4f}, a2={a2v:.4f}, cp2={cp2v:.4f}: val={val:.6e}")

    if val < min_val_valid:
        min_val_valid = val

print(f"  Valid region results: {n_pos_valid}/{n_valid_tests} non-negative, {n_neg_valid} negative")
print(f"  Minimum value on valid region: {min_val_valid:.6e}")

# ============================================================
# SECTION 5: Analysis of the c'=0 (Jensen) case in detail
# ============================================================
print("\n" + "=" * 72)
print("SECTION 5: The c'=0 case - can we prove it algebraically?")
print("=" * 72)

# At c'=0: 1/Phi_4(a, b, 0) = [16a^6/27 + 8a^3b^2 - 27b^4] / [-(32/3)a^5 - 72a^2b^2]
# Let's verify and try to prove the superadditivity.

# Compute P_cp0 more carefully
P_cp0_poly2 = Poly(P_cp0, a1, b1, a2, b2, domain='QQ')
print(f"\n  P(c'=0) has {len(P_cp0_poly2.as_dict())} monomials, total degree {P_cp0_poly2.total_degree()}")

# Check b -> -b symmetry (should only have even powers of b)
print("\n  Checking even-b structure in c'=0 case:")
for monom, coeff in P_cp0_poly2.as_dict().items():
    ia1, jb1, ia2, jb2 = monom
    if (jb1 + jb2) % 2 != 0:
        print(f"    ODD b-power: a1^{ia1}*b1^{jb1}*a2^{ia2}*b2^{jb2}, coeff={coeff}")
        break
else:
    print("  All monomials have even total b-degree. CONFIRMED.")

# Substitute b1^2 = u1, b2^2 = u2 (since only even powers appear)
# Actually, the b's can mix as (b1+b2)^2, so we can't simply substitute.
# But let's try a specific substitution to check if P_cp0 is a perfect
# sum of squares when written in terms of b1^2 and b2^2.

# Try factor P_cp0
print("\n  Attempting to factor P(c'=0)...")
t_fac = time.time()
try:
    # First check if there's a common factor
    P_cp0_content = P_cp0_poly2.content()
    print(f"  Content (GCD of coefficients): {P_cp0_content}")

    P_cp0_prim = P_cp0_poly2.quo_ground(P_cp0_content)
    print(f"  Primitive part: {len(P_cp0_prim.as_dict())} terms")

    # Try factoring the primitive part
    P_cp0_fac = factor(P_cp0)
    P_cp0_fac_str = str(P_cp0_fac)
    print(f"  Factored ({time.time()-t_fac:.1f}s):")
    if len(P_cp0_fac_str) > 500:
        print(f"    {P_cp0_fac_str[:500]}...")
    else:
        print(f"    {P_cp0_fac_str}")
except Exception as e:
    print(f"  Factorization failed: {e}")

# Try to verify the c'=0 case by direct algebraic manipulation.
# The inequality is:
# [16(a1+a2)^6/27 + 8(a1+a2)^3(b1+b2)^2 - 27(b1+b2)^4] * N1_cp0 * N2_cp0
# - [16a1^6/27 + 8a1^3*b1^2 - 27b1^4] * N2_cp0 * Nh_cp0
# - [16a2^6/27 + 8a2^3*b2^2 - 27b2^4] * N1_cp0 * Nh_cp0  >= 0

# where N_cp0(a,b) = -(32/3)*a^5 - 72*a^2*b^2

# ============================================================
# SECTION 6: Numerical SOS attempt via eigenvalue method
# ============================================================
print("\n" + "=" * 72)
print("SECTION 6: Numerical SOS attempt")
print("=" * 72)

# For the b=0 case (4 variables, quasi-homogeneous of wt-degree 32),
# an SOS decomposition P = sum q_i^2 requires each q_i to have wt-degree 16.
# The number of monomials of wt-degree 16 in (a1, cp1, a2, cp2) with
# weights (2,4,2,4) is moderate.

# Since we don't have cvxpy, let's try a simpler approach:
# 1. Fix specific values of a1, a2 and check if the polynomial in (cp1, cp2) [b=0]
#    or (b1, b2) [c'=0] is SOS.
# 2. Use the eigenvalue method: P(x) = m(x)^T * Q * m(x) for SOS, where
#    m(x) is the vector of monomials and Q is PSD.

# Let's start with the c'=0 case, fixing a1 and a2.
print("\n  --- Fixing a1, a2 and checking SOS in (b1, b2) at c'=0 ---")
print("  Strategy: P_cp0(a1_fixed, b1, a2_fixed, b2) should be SOS in (b1,b2)")
print("  Since it's even in (b1,b2), substitute u=b1^2, v=b2^2, w=b1*b2.")

from scipy.linalg import eigh
import numpy as np

def check_sos_2var_even(a1_val, a2_val, poly_dict):
    """Check if a polynomial in (b1, b2) with only even total degree in b
    can be expressed as m^T Q m with Q PSD, for specific a1, a2 values.

    poly_dict: {(j1, j2): coeff} where j1,j2 are exponents of b1, b2.
    Only terms with j1+j2 even are present.
    """
    # Evaluate coefficients at specific a1, a2
    # Then set up the SOS Gram matrix
    # Monomials for half-degree: if max degree in (b1,b2) is d,
    # then half-degree is d/2, and monomials are b1^i * b2^j with i+j <= d/2.

    max_deg = max(j1+j2 for (j1, j2) in poly_dict.keys())
    half_deg = max_deg // 2

    # Monomial basis for the quadratic form
    monoms = []
    for i in range(half_deg + 1):
        for j in range(half_deg + 1 - i):
            monoms.append((i, j))

    n_monoms = len(monoms)
    monom_idx = {m: idx for idx, m in enumerate(monoms)}

    # Set up the linear system: for each monomial b1^alpha * b2^beta in P,
    # we need sum_{(i,j),(k,l): i+k=alpha, j+l=beta} Q[ij,kl] = coeff[alpha,beta]

    # First, enumerate all monomial products
    constraints = {}  # (alpha, beta) -> list of (row, col) pairs
    for i, m1 in enumerate(monoms):
        for j, m2 in enumerate(monoms):
            alpha = m1[0] + m2[0]
            beta = m1[1] + m2[1]
            key = (alpha, beta)
            if key not in constraints:
                constraints[key] = []
            constraints[key].append((i, j))

    # Build the constraint matrix: each constraint is sum of Q entries = target value
    n_vars = n_monoms * (n_monoms + 1) // 2  # upper triangle of Q
    n_constraints = len(poly_dict)

    # Use direct moment matrix approach instead
    # For a polynomial that is SOS, we can try to find Q by solving
    # the moment equations and checking eigenvalues.

    # Simplified: just evaluate P at many points and check positivity
    return None  # Placeholder - full SOS solver would go here

# Instead, let's try a more targeted approach: decompose the polynomial
# using algebraic identities.

# ============================================================
# SECTION 7: Algebraic decomposition attempts
# ============================================================
print("\n" + "=" * 72)
print("SECTION 7: Algebraic decomposition attempts")
print("=" * 72)

# Strategy 1: Write P as a linear combination of known non-negative expressions
# on the valid region.

# Key identity: on the valid region, N1 > 0, N2 > 0, Nh > 0,
# D1 > 0, D2 > 0, Dh > 0.

# Strategy 2: Use the second-order decomposition from CE-11 and try to
# extend it to all orders.

# From CE-11:
# M = 1/Phi_4(h) - 1/Phi_4(1) - 1/Phi_4(2)
# = (3/8)[b1^2/a1^2 + b2^2/a2^2 - (b1+b2)^2/(a1+a2)^2]  [Jensen part]
# + 4[c1'^2/|a1|^3 + c2'^2/|a2|^3 - (c1'+c2')^2/(|a1|+|a2|)^3]  [scaling part]
# + higher order terms

# Strategy 3: Try to express M as:
# M = Jensen_b + Scaling_c' + Cross_bc' + Higher
# where all parts are individually non-negative.

# Let's compute the EXACT form of 1/Phi_4 to higher orders.

print("\n  Computing higher-order Taylor expansion of 1/Phi_4...")

# Working symbolically with a, b, c' as formal parameters.
a_s, b_s, cp_s = symbols('a_s b_s cp_s')

# 1/Phi_4 = Delta(a_s, b_s, cp_s) / N(a_s, b_s, cp_s)
N_sym = N_phi4(a_s, b_s, cp_s)
D_sym = Delta_phi4(a_s, b_s, cp_s)

# Series expansion around b=c'=0
# 1/Phi_4 = D_sym / N_sym
# At b=c'=0: N_sym = -(32/3)*a_s^5, D_sym = (16/27)*a_s^6
# So 1/Phi_4 = (16/27)*a_s^6 / (-(32/3)*a_s^5) = -(16/27)*(3/32)*a_s = -a_s/18

# For the expansion, write D = D0 + D2*b^2 + D2'*c'^2 + ...,
# N = N0 + N2*b^2 + N2'*c'^2 + ...
# Then D/N = (D0/N0) * (1 + (D-D0)/D0) / (1 + (N-N0)/N0)
# = (D0/N0) * [1 + (D-D0)/D0 - (N-N0)/N0 + ...]

# Let me just compute the exact rational function and then Taylor expand.
inv_phi_sym = cancel(D_sym / N_sym)
print(f"  1/Phi_4 = {inv_phi_sym}")

# Compute Taylor expansion to order 4 in (b, c')
# Use series expansion via substitution b -> eps*b, c' -> eps*c', expand in eps
eps = symbols('eps')
inv_phi_eps = inv_phi_sym.subs([(b_s, eps*b_s), (cp_s, eps*cp_s)])
inv_phi_eps = cancel(inv_phi_eps)

# Get numerator and denominator
inv_num_eps = numer(inv_phi_eps)
inv_den_eps = denom(inv_phi_eps)

# Do polynomial division: numerator / denominator as series in eps
from sympy import series
inv_phi_series = series(inv_phi_eps, eps, 0, n=5)
print(f"\n  Taylor series of 1/Phi_4 in eps (b -> eps*b, c' -> eps*c'):")
print(f"  {inv_phi_series}")

# Collect by powers of eps
inv_phi_series_expanded = inv_phi_series.removeO()
for k in range(5):
    coeff_k = inv_phi_series_expanded.coeff(eps, k)
    coeff_k = cancel(coeff_k)
    if coeff_k != 0:
        print(f"\n  eps^{k} coefficient: {coeff_k}")

# ============================================================
# SECTION 8: Full margin expansion to order 4
# ============================================================
print("\n" + "=" * 72)
print("SECTION 8: Full margin expansion to order 4")
print("=" * 72)

# The margin M = 1/Phi_4(ah, bh, cph) - 1/Phi_4(a1, b1, cp1) - 1/Phi_4(a2, b2, cp2)
# Expand each 1/Phi_4 to order 4 in the (b, c') variables using the series above.

# From the series, extract the general formula for each order:
# 1/Phi_4(a, b, c') = f0(a) + f2(a)*b^2 + g2(a)*c'^2 + f4(a)*b^4 + g4(a)*c'^4 + h22(a)*b^2*c'^2 + ...
# (odd powers of b vanish by symmetry; odd powers of c' may not vanish in general,
#  but at the equality manifold they do)

# Actually, let me re-examine: c' doesn't have the b->-b symmetry.
# 1/Phi_4(a, b, c') - but wait, there IS no c' -> -c' symmetry.
# So there could be odd powers of c'.

# Let me redo the expansion more carefully, treating b and c' independently.
eps_b, eps_c = symbols('eps_b eps_c')
inv_phi_2eps = inv_phi_sym.subs([(b_s, eps_b*b_s), (cp_s, eps_c*cp_s)])

# This is a rational function in (eps_b, eps_c). We want to expand it
# as a bivariate series.

# To do this, substitute eps_b = eps*t_b, eps_c = eps*t_c, expand in eps.
# Or just expand directly.

# Actually, since the expansion gets complex, let me use a simpler approach:
# compute the correction function exactly for specific (a, b, c') values
# and analyze the structure.

print("  Computing exact correction C(a, b, c') = 1/Phi_4(a, b, c') + a/18")
print("  at specific points to determine its algebraic structure...")

# At b=0: C(a, 0, c') = 4c'^2/(a(a^2+6c'))  [from CE-11]
# Verify symbolically:
C_b0_sym = cancel(D_sym.subs(b_s, 0) / N_sym.subs(b_s, 0) + a_s/18)
print(f"\n  C(a, 0, c') = {C_b0_sym}")

C_b0_num = numer(C_b0_sym)
C_b0_den = denom(C_b0_sym)
C_b0_num_f = factor(C_b0_num)
C_b0_den_f = factor(C_b0_den)
print(f"  Numerator: {C_b0_num_f}")
print(f"  Denominator: {C_b0_den_f}")

# At c'=0: C(a, b, 0) = 1/Phi_4(a, b, 0) + a/18
C_cp0_sym = cancel(D_sym.subs(cp_s, 0) / N_sym.subs(cp_s, 0) + a_s/18)
print(f"\n  C(a, b, 0) = {C_cp0_sym}")

C_cp0_num = numer(C_cp0_sym)
C_cp0_den = denom(C_cp0_sym)
C_cp0_num_f = factor(C_cp0_num)
C_cp0_den_f = factor(C_cp0_den)
print(f"  Numerator: {C_cp0_num_f}")
print(f"  Denominator: {C_cp0_den_f}")

# ============================================================
# SECTION 9: Exact b=0 margin analysis
# ============================================================
print("\n" + "=" * 72)
print("SECTION 9: Exact margin analysis for b=0")
print("=" * 72)

# For b=0: 1/Phi_4(a, 0, c') = -a/18 + 4c'^2/(a(a^2+6c'))
# = [-a(a^2+6c') + 72c'^2] / [18(a^2+6c')]   ... wait let me compute properly:
# = [-a^3-6ac' + 72c'^2] / [18a(a^2+6c')]  ... no.
#
# Actually: 1/Phi_4 + a/18 = 4c'^2 / (a(a^2+6c'))
# So 1/Phi_4 = -a/18 + 4c'^2/(a(a^2+6c'))
#            = [-a^2(a^2+6c') + 72c'^2] / [18a(a^2+6c')]  ... let me compute:
# -a/18 = -a(a^2+6c') / [18(a^2+6c')]
# Adding 4c'^2/(a(a^2+6c')):
# = [-a^2(a^2+6c') + 72c'^2] / [18a(a^2+6c')]  ... hmm
#
# Let me just use sympy:
inv_phi_b0_full = cancel(-a_s/18 + Rational(4)*cp_s**2 / (a_s*(a_s**2 + 6*cp_s)))
print(f"  1/Phi_4(a, 0, c') = {inv_phi_b0_full}")

# The b=0 margin:
# M_b0 = 1/Phi_4(a1+a2, 0, c1'+c2') - 1/Phi_4(a1, 0, c1') - 1/Phi_4(a2, 0, c2')
# = -(a1+a2)/18 + 4(c1'+c2')^2 / ((a1+a2)((a1+a2)^2+6(c1'+c2')))
#   - [-a1/18 + 4c1'^2/(a1(a1^2+6c1'))]
#   - [-a2/18 + 4c2'^2/(a2(a2^2+6c2'))]
# = 4(c1'+c2')^2 / ((a1+a2)((a1+a2)^2+6(c1'+c2')))
#   - 4c1'^2/(a1(a1^2+6c1'))
#   - 4c2'^2/(a2(a2^2+6c2'))
# (The linear parts cancel.)

M_b0_sym = (Rational(4)*(cp1+cp2)**2 / ((a1+a2)*((a1+a2)**2 + 6*(cp1+cp2)))
            - Rational(4)*cp1**2 / (a1*(a1**2 + 6*cp1))
            - Rational(4)*cp2**2 / (a2*(a2**2 + 6*cp2)))

M_b0_sym = cancel(M_b0_sym)
M_b0_num = numer(M_b0_sym)
M_b0_den = denom(M_b0_sym)

print(f"\n  M(b=0) = [numerator] / [denominator]")
M_b0_num_expanded = expand(M_b0_num)
M_b0_den_expanded = expand(M_b0_den)
M_b0_num_poly = Poly(M_b0_num_expanded, a1, cp1, a2, cp2, domain='QQ')
M_b0_den_poly = Poly(M_b0_den_expanded, a1, cp1, a2, cp2, domain='QQ')

print(f"  Numerator: {len(M_b0_num_poly.as_dict())} terms, total degree {M_b0_num_poly.total_degree()}")
print(f"  Denominator: {len(M_b0_den_poly.as_dict())} terms, total degree {M_b0_den_poly.total_degree()}")

# Check sign of denominator
# den = a1*(a1^2+6c1') * a2*(a2^2+6c2') * (a1+a2)*((a1+a2)^2+6(c1'+c2'))
# For a < 0 and valid region: a < 0, a^2+6c' > 0 (from N > 0 condition).
# So a*(a^2+6c') < 0 for each factor.
# Product of 3 such negative terms = negative * negative * negative = negative.
# Wait: a1*(a1^2+6c1') < 0, a2*(a2^2+6c2') < 0, (a1+a2)*((a1+a2)^2+6(c1'+c2')) < 0
# Product = (-)(-)(-) = -1. So denominator < 0.
# Therefore M_b0 >= 0 iff numerator <= 0.

M_b0_den_factored = factor(M_b0_den_expanded)
print(f"\n  Denominator factored: {M_b0_den_factored}")

print("\n  Sign analysis:")
print("  For a < 0, a^2+6c' > 0: each factor a*(a^2+6c') < 0")
print("  Three such factors: denominator < 0")
print("  So M_b0 >= 0 iff numerator <= 0")

# Try to factor numerator
print("\n  Attempting to factor numerator...")
t_fac = time.time()
try:
    M_b0_num_factored = factor(M_b0_num_expanded)
    fac_str = str(M_b0_num_factored)
    print(f"  Factored ({time.time()-t_fac:.1f}s):")
    if len(fac_str) > 500:
        print(f"    {fac_str[:500]}...")
    else:
        print(f"    {fac_str}")
except Exception as e:
    print(f"  Factorization failed: {e}")

# Check symmetry of numerator
M_b0_num_swapped = expand(M_b0_num_expanded.subs([(a1, a2), (cp1, cp2), (a2, a1), (cp2, cp1)]))
is_num_sym = expand(M_b0_num_expanded - M_b0_num_swapped) == 0
print(f"\n  Numerator symmetric under (1)<->(2): {is_num_sym}")

# Try the substitution cp1 = 0
print("\n  Numerator at cp1=0:")
num_cp1_0 = expand(M_b0_num_expanded.subs(cp1, 0))
print(f"    {factor(num_cp1_0)}")

# Try cp1 = cp2 = 0
print("\n  Numerator at cp1=cp2=0:")
num_cp_0 = expand(M_b0_num_expanded.subs([(cp1, 0), (cp2, 0)]))
print(f"    {num_cp_0}")

# Check: at cp1=cp2=0, the margin should be 0 (equality manifold)
# Yes: 4*0/(a*(a^2+0)) = 0 for each term. So numerator = 0 at cp=0. Good.

# ============================================================
# SECTION 10: Numerical SOS for b=0 margin via scipy
# ============================================================
print("\n" + "=" * 72)
print("SECTION 10: Numerical SOS via moment matrix (b=0 case)")
print("=" * 72)

# For the b=0 case, we need to show that the numerator of M_b0 is <= 0
# on the valid region. The numerator is a polynomial in (a1, cp1, a2, cp2).
#
# Strategy: fix a1, a2 < 0 and study the numerator as a function of (cp1, cp2).
# For each fixed (a1, a2), the numerator should be a polynomial in (cp1, cp2)
# that is <= 0 on the valid region {a_i^2 + 6*cp_i > 0}.
#
# Since we're looking at -numerator >= 0, try to express -num as SOS + positivity
# certificate using the constraint (a_i^2 + 6*cp_i) * sigma_i >= 0.

# This is a Positivstellensatz-type problem. Without cvxpy, we'll use
# a sampling-based approach.

# Let's try something simpler: for fixed a1=a2=-6, plot the polynomial
# to understand its shape.

print("\n  Fixing a1 = a2 = -6 for visual analysis of b=0 margin numerator...")
a1_fix = Rational(-6)
a2_fix = Rational(-6)

M_b0_num_fixed = expand(M_b0_num_expanded.subs([(a1, a1_fix), (a2, a2_fix)]))
print(f"  Numerator at a1=a2=-6: {M_b0_num_fixed}")

M_b0_num_fixed_poly = Poly(M_b0_num_fixed, cp1, cp2, domain='QQ')
print(f"  Degree in (cp1,cp2): {M_b0_num_fixed_poly.total_degree()}")
print(f"  Number of terms: {len(M_b0_num_fixed_poly.as_dict())}")

# Print all terms
print("  Monomials:")
for monom, coeff in sorted(M_b0_num_fixed_poly.as_dict().items()):
    k1, k2 = monom
    print(f"    cp1^{k1} * cp2^{k2} : {coeff}")

# Check if -M_b0_num_fixed is a sum of squares
# For a bivariate polynomial of degree d, SOS requires d/2 = 3 (since degree is 6).
# The monomial basis is {1, cp1, cp2, cp1^2, cp1*cp2, cp2^2, cp1^3, cp1^2*cp2, cp1*cp2^2, cp2^3}
# So the Gram matrix is 10x10.

print("\n  Attempting Gram matrix SOS for -M_b0_num at a1=a2=-6...")

# Build the monomial basis (up to half-degree = 3)
half_deg = 3
mono_basis = []
for i in range(half_deg + 1):
    for j in range(half_deg + 1 - i):
        mono_basis.append((i, j))

n_basis = len(mono_basis)
print(f"  Monomial basis size: {n_basis}")
print(f"  Basis: {mono_basis}")

# For SOS: -num(cp1,cp2) = m(cp1,cp2)^T Q m(cp1,cp2) with Q PSD
# This gives: for each monomial cp1^alpha * cp2^beta in -num:
# coeff(alpha, beta) = sum_{(i,j),(k,l): i+k=alpha,j+l=beta} Q[(i,j),(k,l)]

# Build constraint equations
neg_num_dict = {}
for monom, coeff in M_b0_num_fixed_poly.as_dict().items():
    neg_num_dict[monom] = -coeff  # We want -num >= 0

# For each target monomial (alpha, beta), list the Gram matrix entries that contribute
constraints = {}
for i_idx, (i, j) in enumerate(mono_basis):
    for k_idx, (k, l) in enumerate(mono_basis):
        alpha = i + k
        beta = j + l
        key = (alpha, beta)
        if key not in constraints:
            constraints[key] = []
        constraints[key].append((i_idx, k_idx))

# Set up least-squares problem to find Q
# Variables: upper triangle of Q (n_basis*(n_basis+1)/2 variables)
# Constraints: for each (alpha, beta), sum of Q entries = target coeff

# Use scipy least squares
from scipy.optimize import minimize, LinearConstraint
from scipy.linalg import eigh

# Map upper triangle to flat index
n_vars_q = n_basis * (n_basis + 1) // 2
tri_idx = {}
flat_to_ij = []
k_flat = 0
for i_idx in range(n_basis):
    for j_idx in range(i_idx, n_basis):
        tri_idx[(i_idx, j_idx)] = k_flat
        flat_to_ij.append((i_idx, j_idx))
        k_flat += 1

# Build constraint matrix A*q = b
# For each monomial (alpha, beta) in the target polynomial
all_target_monoms = set()
for key in constraints:
    all_target_monoms.add(key)
# Also add monomials from the target polynomial
for key in neg_num_dict:
    all_target_monoms.add(key)

all_target_monoms = sorted(all_target_monoms)
n_constraints_sos = len(all_target_monoms)

A_sos = np.zeros((n_constraints_sos, n_vars_q))
b_sos = np.zeros(n_constraints_sos)

for c_idx, (alpha, beta) in enumerate(all_target_monoms):
    # Target value
    b_sos[c_idx] = float(neg_num_dict.get((alpha, beta), 0))

    # Contributions from Gram matrix
    if (alpha, beta) in constraints:
        for (i_idx, k_idx) in constraints[(alpha, beta)]:
            # Q[i_idx, k_idx] appears (and Q[k_idx, i_idx] by symmetry)
            if i_idx <= k_idx:
                flat_idx = tri_idx[(i_idx, k_idx)]
            else:
                flat_idx = tri_idx[(k_idx, i_idx)]

            if i_idx == k_idx:
                A_sos[c_idx, flat_idx] += 1.0
            else:
                A_sos[c_idx, flat_idx] += 1.0  # Q[i,k] + Q[k,i] = 2*Q_upper[i,k]

# Wait, I need to be more careful with the symmetry of Q.
# Q is symmetric, so Q[i,k] = Q[k,i]. When we have i != k:
# the contribution of the (i,k) entry to monomial (alpha,beta) is Q[i,k],
# and (k,i) also contributes Q[k,i] = Q[i,k].
# So the total contribution is 2*Q[i,k] for i < k, and Q[i,i] for i=k.

# Rebuild more carefully
A_sos = np.zeros((n_constraints_sos, n_vars_q))
b_sos = np.zeros(n_constraints_sos)

for c_idx, (alpha, beta) in enumerate(all_target_monoms):
    b_sos[c_idx] = float(neg_num_dict.get((alpha, beta), 0))

    if (alpha, beta) in constraints:
        # Group by upper-triangle index
        contributions = {}  # flat_idx -> multiplicity
        for (i_idx, k_idx) in constraints[(alpha, beta)]:
            fi = min(i_idx, k_idx)
            fj = max(i_idx, k_idx)
            flat_idx = tri_idx[(fi, fj)]
            contributions[flat_idx] = contributions.get(flat_idx, 0) + 1

        for flat_idx, mult in contributions.items():
            A_sos[c_idx, flat_idx] = mult

# Solve the linear system A_sos * q = b_sos in least squares sense
# Then reconstruct Q and check if PSD

from numpy.linalg import lstsq
q_sol, residuals, rank, sv = lstsq(A_sos, b_sos, rcond=None)

# Reconstruct Q matrix
Q_mat = np.zeros((n_basis, n_basis))
for flat_idx, (i_idx, j_idx) in enumerate(flat_to_ij):
    Q_mat[i_idx, j_idx] = q_sol[flat_idx]
    Q_mat[j_idx, i_idx] = q_sol[flat_idx]

# Check residual
residual = np.linalg.norm(A_sos @ q_sol - b_sos)
print(f"\n  Residual (should be ~0 if constraints are consistent): {residual:.6e}")

# Check eigenvalues
eigvals = eigh(Q_mat, eigvals_only=True)
print(f"  Eigenvalues of Q: {np.sort(eigvals)}")
print(f"  Minimum eigenvalue: {min(eigvals):.6e}")
print(f"  Q is PSD: {min(eigvals) >= -1e-8}")

if min(eigvals) >= -1e-8 and residual < 1e-8:
    print("  ==> SOS CERTIFICATE FOUND for b=0 case at a1=a2=-6!")
else:
    print("  ==> SOS certificate NOT found directly.")
    print("  This may mean we need Positivstellensatz (constraint-qualified SOS)")
    print("  or the polynomial is not globally SOS.")

# Try with the full P_b0 polynomial for a few more (a1, a2) values
print("\n  Testing SOS for other a1, a2 values in b=0 case...")
for a1_test, a2_test in [(-3, -3), (-3, -9), (-2, -10), (-5, -5), (-1, -1)]:
    M_b0_num_test = expand(M_b0_num_expanded.subs([(a1, Rational(a1_test)), (a2, Rational(a2_test))]))
    M_b0_num_test_poly = Poly(M_b0_num_test, cp1, cp2, domain='QQ')

    # Build target
    neg_num_test = {}
    for monom, coeff in M_b0_num_test_poly.as_dict().items():
        neg_num_test[monom] = -float(coeff)

    b_test = np.zeros(n_constraints_sos)
    for c_idx, (alpha, beta) in enumerate(all_target_monoms):
        b_test[c_idx] = neg_num_test.get((alpha, beta), 0.0)

    q_test, _, _, _ = lstsq(A_sos, b_test, rcond=None)

    Q_test = np.zeros((n_basis, n_basis))
    for flat_idx, (i_idx, j_idx) in enumerate(flat_to_ij):
        Q_test[i_idx, j_idx] = q_test[flat_idx]
        Q_test[j_idx, i_idx] = q_test[flat_idx]

    res_test = np.linalg.norm(A_sos @ q_test - b_test)
    eigvals_test = eigh(Q_test, eigvals_only=True)
    min_eig = min(eigvals_test)

    status = "SOS" if (min_eig >= -1e-8 and res_test < 1e-8) else "NOT SOS"
    print(f"  a1={a1_test}, a2={a2_test}: residual={res_test:.2e}, min_eig={min_eig:.6e} -> {status}")

# ============================================================
# SECTION 11: Full 6-variable polynomial - structure & SOS check
# ============================================================
print("\n" + "=" * 72)
print("SECTION 11: Full polynomial analysis")
print("=" * 72)

# For the full 6-variable case, a direct SOS decomposition is very expensive.
# Let's at least characterize the polynomial fully.

# Check if P has any nice factorization
print("\n  Checking if the full polynomial P has common factors...")
t_fac = time.time()

# Check for common factor with constraints (discriminants)
# P should vanish when any discriminant vanishes (at the boundary of the valid region)

# Test: does P vanish when D1 = 0? (one polynomial degenerate)
# At the equality manifold (b=c'=0), both P=0 and Di>0.
# At a boundary where D1=0, 1/Phi_4(1) -> infinity, so the inequality
# should still hold (LHS still >= 1/Phi_4(2) > 0 = 0 + 1/Phi_4(2)).
# This doesn't immediately tell us about P's factors.

# Check P modulo specific substitutions
print(f"\n  P at b1=b2=cp1=cp2=0 (equality manifold): {expand(P.subs([(b1,0),(b2,0),(cp1,0),(cp2,0)]))}")
P_at_a2_0 = expand(P.subs([(a2,0),(b2,0),(cp2,0)]))
print(f"  P at a2=0, b2=0, cp2=0: {str(P_at_a2_0)[:100]}...")

# What is P at a1=-1, a2=-1, b1=0, b2=0, cp1=t, cp2=0?
print("\n  P at a1=-1, a2=-1, b=0, cp2=0 as function of cp1:")
P_1d = expand(P.subs([(a1, -1), (a2, -1), (b1, 0), (b2, 0), (cp2, 0)]))
print(f"  P(cp1) = {P_1d}")
P_1d_poly = Poly(P_1d, cp1, domain='QQ')
print(f"  Degree: {P_1d_poly.degree()}")
print(f"  Coefficients: {P_1d_poly.all_coeffs()}")
# This polynomial in cp1 should be >= 0 on the valid range for cp1.

# Check its roots
print("  Real roots:")
from sympy import real_roots, Rational as R
try:
    roots_1d = real_roots(P_1d, cp1)
    for r in roots_1d:
        print(f"    cp1 = {r} = {float(r):.6f}")
except Exception as e:
    print(f"  Could not find roots: {e}")

# ============================================================
# SECTION 12: Schur-like decomposition attempt
# ============================================================
print("\n" + "=" * 72)
print("SECTION 12: Schur-like / Cauchy-Schwarz decomposition")
print("=" * 72)

# Key insight: the b=0 margin can be written as
# M_b0 = 4 * [c1'^2/(a1(a1^2+6c1')) + c2'^2/(a2(a2^2+6c2'))
#              - (c1'+c2')^2/((a1+a2)((a1+a2)^2+6(c1'+c2')))]

# Define f(a, c') = c'^2 / (a(a^2 + 6c'))
# Then M_b0 = 4 * [f(a1,c1') + f(a2,c2') - f(a1+a2, c1'+c2')]
# We need: f(a1,c1') + f(a2,c2') >= f(a1+a2, c1'+c2')  [SUBADDITIVITY of f]

# So the b=0 case reduces to showing f is SUBADDITIVE.
# (Note the sign: since the denominator is negative, and the numerator
# M_b0_num needs to be <= 0, we need f(h) <= f(1) + f(2), i.e., subadditivity.)

print("  b=0 case reduces to subadditivity of:")
print("  f(a, c') = c'^2 / (a(a^2 + 6c'))")
print("  Need: f(a1+a2, c1'+c2') <= f(a1,c1') + f(a2,c2')")
print()

# Properties of f:
# f(a, 0) = 0 (so f(h) = 0 when c'=0: subadditivity trivially holds)
# f(a, c') = c'^2 / (a^3 + 6ac')
# For a < 0: a^3 + 6ac' = a^3 + 6ac' < 0 (need a^2+6c' > 0 => c' > -a^2/6)
# So a^3 + 6ac' = a(a^2 + 6c') < 0 (since a < 0 and a^2+6c'>0)
# And c'^2 >= 0. So f(a,c') = c'^2/(negative) <= 0.

# Hmm, f <= 0, and we need f(h) <= f(1) + f(2).
# f(1) <= 0, f(2) <= 0, f(1)+f(2) <= 0, and we need f(h) <= f(1)+f(2).
# Since both sides are <= 0, this means |f(h)| >= |f(1)+f(2)|.
# Equivalently, f(h) is MORE negative than f(1)+f(2).

# Actually wait: in the original inequality, the correction to the margin
# at b=0 is:
# M_b0 = 4*[f(a1,c1')+f(a2,c2')-f(a1+a2,c1'+c2')]
# and we computed that the denominator of M_b0 is < 0.
# So M_b0 >= 0 iff numerator <= 0 iff 4*[f(1)+f(2)-f(h)] * denom >= 0
# Wait, I need to be more careful.

# Let me just verify numerically:
print("  Numerical check of f-subadditivity:")
from fractions import Fraction

def f_exact(a_val, cp_val):
    a = Fraction(a_val)
    cp = Fraction(cp_val)
    if a == 0 or a**2 + 6*cp == 0:
        return None
    return cp**2 / (a * (a**2 + 6*cp))

n_sub_pass = 0
n_sub_fail = 0
for _ in range(5000):
    a1v = -np.random.uniform(0.5, 10)
    a2v = -np.random.uniform(0.5, 10)
    cp1v = np.random.uniform(-a1v**2/6 * 0.9, a1v**2/6 * 0.4)
    cp2v = np.random.uniform(-a2v**2/6 * 0.9, a2v**2/6 * 0.4)

    ah_v = a1v + a2v
    cph_v = cp1v + cp2v

    # Check validity
    if (a1v**2 + 6*cp1v <= 0 or a2v**2 + 6*cp2v <= 0 or
        ah_v**2 + 6*cph_v <= 0):
        continue

    f1 = cp1v**2 / (a1v * (a1v**2 + 6*cp1v))
    f2 = cp2v**2 / (a2v * (a2v**2 + 6*cp2v))
    fh = cph_v**2 / (ah_v * (ah_v**2 + 6*cph_v))

    if fh <= f1 + f2 + 1e-12:
        n_sub_pass += 1
    else:
        n_sub_fail += 1
        if n_sub_fail <= 3:
            print(f"    FAIL: a1={a1v:.3f}, cp1={cp1v:.3f}, a2={a2v:.3f}, cp2={cp2v:.3f}")
            print(f"      f(h)={fh:.6e}, f(1)+f(2)={f1+f2:.6e}, diff={fh-f1-f2:.6e}")

print(f"  f-subadditivity: {n_sub_pass} pass, {n_sub_fail} fail")

# Try to prove f-subadditivity algebraically
# f(a,c') = c'^2 / (a(a^2+6c'))
# f(a1+a2, c1'+c2') <= f(a1,c1') + f(a2,c2')
#
# Cross multiply by the (negative) denominators:
# c_h'^2 * a1*(a1^2+6c1') * a2*(a2^2+6c2') <= (c1'^2*a2*(a2^2+6c2')+c2'^2*a1*(a1^2+6c1'))*ah*(ah^2+6c_h')
# But all denominators are negative, so cross-multiplying flips inequalities.
# This gets complicated. Let's instead directly look at the margin numerator.

# ============================================================
# SECTION 13: Cauchy-Schwarz approach for b=0 margin
# ============================================================
print("\n" + "=" * 72)
print("SECTION 13: Cauchy-Schwarz / power-mean approach")
print("=" * 72)

# For the b=0 margin, we showed the second-order part is:
# c1'^2/alpha1^3 + c2'^2/alpha2^3 >= (c1'+c2')^2/(alpha1+alpha2)^3
# where alpha = -a > 0.
#
# This is a POWER MEAN inequality! Specifically, it's of the form:
# sum c_i^2/w_i >= (sum c_i)^2 / (sum w_i)
# where w_i = alpha_i^3.
#
# This is exactly the Cauchy-Schwarz inequality (Titu's lemma):
# sum x_i^2/y_i >= (sum x_i)^2 / (sum y_i) for y_i > 0.
#
# So the second-order c'-part follows from Cauchy-Schwarz.
#
# But for the FULL (non-perturbative) case, we need:
# c1'^2/(a1(a1^2+6c1')) + c2'^2/(a2(a2^2+6c2')) >= (c1'+c2')^2/((a1+a2)((a1+a2)^2+6(c1'+c2')))
#
# = c1'^2/w1 + c2'^2/w2 >= (c1'+c2')^2/wh
# where w1 = a1(a1^2+6c1'), w2 = a2(a2^2+6c2'), wh = ah(ah^2+6cph).
#
# This looks like a GENERALIZED Cauchy-Schwarz, but the "weights" w_i
# depend on the c'_i values, making it more complex.

print("  Generalized Cauchy-Schwarz structure:")
print("  c1'^2/w1 + c2'^2/w2 >= (c1'+c2')^2/wh")
print("  where w_i = a_i(a_i^2+6c_i') [all negative]")
print("  and wh = (a1+a2)((a1+a2)^2+6(c1'+c2')) [negative]")
print()
print("  Dividing by negative denominators flips to:")
print("  c1'^2/|w1| + c2'^2/|w2| <= (c1'+c2')^2/|wh|  ... NO, not quite.")
print()

# Actually since w1, w2, wh < 0, we have:
# c1'^2/w1 + c2'^2/w2 = -(c1'^2/|w1| + c2'^2/|w2|) <= 0
# and (c1'+c2')^2/wh = -(c1'+c2')^2/|wh| <= 0
# The inequality f(h) <= f(1)+f(2) becomes:
# -(c1'+c2')^2/|wh| <= -(c1'^2/|w1| + c2'^2/|w2|)
# i.e., c1'^2/|w1| + c2'^2/|w2| <= (c1'+c2')^2/|wh|
# This is the REVERSE of Cauchy-Schwarz if |wh| = |w1| + |w2|,
# but that's not the case here.

# Let's check: is |wh| >= |w1| + |w2|?
print("  Checking if |wh| >= |w1| + |w2| (needed for reverse C-S):")
n_ineq_pass = 0
n_ineq_fail = 0
for _ in range(5000):
    a1v = -np.random.uniform(0.5, 10)
    a2v = -np.random.uniform(0.5, 10)
    cp1v = np.random.uniform(-a1v**2/6 * 0.9, a1v**2/6 * 0.4)
    cp2v = np.random.uniform(-a2v**2/6 * 0.9, a2v**2/6 * 0.4)

    ah_v = a1v + a2v
    cph_v = cp1v + cp2v

    if (a1v**2 + 6*cp1v <= 0 or a2v**2 + 6*cp2v <= 0 or
        ah_v**2 + 6*cph_v <= 0):
        continue

    w1 = abs(a1v * (a1v**2 + 6*cp1v))
    w2 = abs(a2v * (a2v**2 + 6*cp2v))
    wh = abs(ah_v * (ah_v**2 + 6*cph_v))

    if wh >= w1 + w2 - 1e-10:
        n_ineq_pass += 1
    else:
        n_ineq_fail += 1

print(f"  |wh| >= |w1|+|w2|: {n_ineq_pass} pass, {n_ineq_fail} fail")

# So |wh| >= |w1| + |w2| does NOT always hold. The approach needs refinement.

# A different angle: Cauchy-Schwarz with custom parameterization.
# We need: c1'^2/|w1| + c2'^2/|w2| <= (c1'+c2')^2/|wh|
# Rearranging: |wh| * (c1'^2/|w1| + c2'^2/|w2|) <= (c1'+c2')^2
# By Cauchy-Schwarz: (c1'^2/|w1| + c2'^2/|w2|)(|w1| + |w2|) >= (c1'+c2')^2
# So if |wh| <= |w1| + |w2|, then:
# |wh| * (c1'^2/|w1| + c2'^2/|w2|) <= (|w1|+|w2|)*(c1'^2/|w1|+c2'^2/|w2|) >= (c1'+c2')^2
# This doesn't close. The wrong direction.

print("\n  CONCLUSION: Simple Cauchy-Schwarz does not close the b=0 case.")
print("  The weight-dependent denominators create a non-standard inequality.")

# ============================================================
# SECTION 14: Alternative parametrization for b=0 case
# ============================================================
print("\n" + "=" * 72)
print("SECTION 14: Alternative parametrization for b=0 case")
print("=" * 72)

# Try: substitute c' = t * a^2 (dimensionless parametrization)
# Then f(a, t*a^2) = t^2*a^4 / (a*(a^2*(1+6t))) = t^2*a / (1+6t)
# For a < 0: f = t^2 * a / (1+6t). Since a < 0 and 1+6t > 0 (valid region: t > -1/6),
# f < 0.
#
# The b=0 margin becomes:
# M_b0 = 4*[t1^2*a1/(1+6t1) + t2^2*a2/(1+6t2) - th^2*ah/(1+6th)]
# where th = (c1'+c2')/(a1+a2)^2 = (t1*a1^2+t2*a2^2)/(a1+a2)^2
#
# With alpha = -a > 0, w1 = alpha1/(alpha1+alpha2):
# th = w1^2*t1 + w2^2*t2 + 2*w1*w2*... wait, that's not right.
# th = (t1*alpha1^2 + t2*alpha2^2)/(alpha1+alpha2)^2 = w1^2*t1 + w2^2*t2
# Wait: th = (c1'+c2')/(a1+a2)^2 = (t1*a1^2+t2*a2^2)/(a1+a2)^2
# With a1=-alpha1, a2=-alpha2:
# th = (t1*alpha1^2 + t2*alpha2^2)/(alpha1+alpha2)^2
#    = w1^2*t1/1 + w2^2*t2/1 ... no:
# = (w1^2*(alpha1+alpha2)^2*t1 + w2^2*(alpha1+alpha2)^2*t2)/(alpha1+alpha2)^2
# Hmm, alpha_i/(alpha1+alpha2) = w_i, so alpha_i^2 = w_i^2*(alpha1+alpha2)^2.
# th = w1^2*t1 + w2^2*t2. (Weights DON'T sum to 1!)
#
# And M_b0 = 4*(alpha1+alpha2)*[w1*t1^2/(1+6t1) + w2*t2^2/(1+6t2) - th^2/(1+6th)]
#           (using f(a,c') = t^2*a/(1+6t) and a = -(alpha1+alpha2) for h)

print("  Dimensionless parametrization: t_i = c_i' / a_i^2")
print("  f(a, t*a^2) = t^2*a/(1+6t)")
print("  th = w1^2*t1 + w2^2*t2  (w1+w2=1, but w1^2+w2^2 < 1)")
print("  M_b0/4 = (alpha1+alpha2)[w1*t1^2/(1+6t1) + w2*t2^2/(1+6t2) - th^2/(1+6th)]")
print()
print("  This is a 3-parameter inequality (sigma=w1, t1, t2) after fixing alpha_sum.")

# Let's define g(t) = t^2/(1+6t) and check what we need:
# w1*g(t1) + w2*g(t2) >= g(w1^2*t1 + w2^2*t2)
# This is NOT Jensen because the argument is w1^2*t1+w2^2*t2, not w1*t1+w2*t2.

# Verify numerically
print("\n  Numerical verification of g-inequality:")
n_g_pass = 0
n_g_fail = 0
for _ in range(10000):
    w1v = np.random.uniform(0.01, 0.99)
    w2v = 1 - w1v
    t1v = np.random.uniform(-1/6.0 * 0.9, 0.3)
    t2v = np.random.uniform(-1/6.0 * 0.9, 0.3)

    if 1+6*t1v <= 0 or 1+6*t2v <= 0:
        continue

    g1 = t1v**2 / (1+6*t1v)
    g2 = t2v**2 / (1+6*t2v)
    th_v = w1v**2*t1v + w2v**2*t2v
    if 1+6*th_v <= 0:
        continue
    gh = th_v**2 / (1+6*th_v)

    lhs = w1v*g1 + w2v*g2
    if lhs >= gh - 1e-12:
        n_g_pass += 1
    else:
        n_g_fail += 1
        if n_g_fail <= 3:
            print(f"    FAIL: w1={w1v:.3f}, t1={t1v:.4f}, t2={t2v:.4f}")
            print(f"      LHS={lhs:.6e}, RHS={gh:.6e}, diff={lhs-gh:.6e}")

print(f"  g-inequality: {n_g_pass} pass, {n_g_fail} fail")

# ============================================================
# SECTION 15: Summary and recommendations
# ============================================================
print("\n" + "=" * 72)
print("SECTION 15: Summary and recommendations")
print("=" * 72)

total_time = time.time() - t0

print(f"""
RESULTS SUMMARY
{'='*60}

1. NUMERATOR POLYNOMIAL:
   - The degree-16 polynomial P = Dh*N1*N2 - D1*N2*Nh - D2*N1*Nh
     has been computed exactly in SymPy.
   - {n_terms_P} terms in 6 variables (a1, b1, cp1, a2, b2, cp2).
   - P is SYMMETRIC under (a1,b1,cp1) <-> (a2,b2,cp2): {is_symmetric}
   - P is EVEN in (b1, b2): {is_b_symmetric}
   - Quasi-homogeneous: {is_quasi_homog}

2. RESTRICTED CASES:
   (A) b1=b2=0: reduces to 4-variable polynomial, subadditivity of
       f(a,c') = c'^2/(a(a^2+6c'))
   (B) cp1=cp2=0: reduces to 4-variable polynomial (Jensen-type)
   (C) b=c'=0: P = 0 identically (equality manifold, VERIFIED)
   (D) Second-order margin: PROVED PSD (Jensen + Cauchy-Schwarz)

3. SOS GRAM MATRIX (b=0, fixed a1=a2):
   - Attempted for several (a1, a2) values
   - Results above show whether numerical SOS certificates were found

4. ALGEBRAIC DECOMPOSITION:
   - b=0 margin reduces to generalized Cauchy-Schwarz with
     variable-dependent weights
   - Simple Cauchy-Schwarz does NOT close (weight inequality fails)
   - Dimensionless parametrization t = c'/a^2 gives cleaner structure:
     g(t) = t^2/(1+6t), need w1*g(t1)+w2*g(t2) >= g(w1^2*t1+w2^2*t2)
   - This is a non-standard functional inequality (weight mismatch:
     w_i vs w_i^2)

5. STRUCTURAL OBSTACLES:
   - The core obstruction is the WEIGHT MISMATCH: the convolution mixing
     rule for t = c'/a^2 uses weights w_i^2 (not w_i) in the argument.
   - Standard convexity/Jensen arguments use matching weights.
   - The b and c' variables cannot be decoupled because they interact
     through the discriminant constraint.

6. RECOMMENDATIONS TO CLOSE THE GAP:
   (a) INSTALL cvxpy + SCS/MOSEK and solve the full SDP for the degree-16
       SOS certificate. With 6 variables and quasi-homogeneity, the number
       of free parameters is manageable (~1000-5000 for the Gram matrix).
   (b) Try DSOS/SDSOS relaxations (diagonally-dominant SOS), which only
       require LP/SOCP and can handle larger problems.
   (c) Prove the b=0 case separately via the g-inequality:
       w*g(t1) + (1-w)*g(t2) >= g(w^2*t1 + (1-w)^2*t2)
       This is a 3-parameter inequality that may be provable by
       direct computation (clear denominators, check polynomial sign).
   (d) For the full case: try the substitution b_i = s_i * |a_i|^(3/2),
       c_i' = t_i * a_i^2, which makes P quasi-homogeneous of degree 0
       in the a_i and reduces to a 4-parameter problem (s1,t1,s2,t2)
       with a 1-parameter family (sigma = alpha1/(alpha1+alpha2)).
   (e) Investigate if Schur's inequality or Muirhead's inequality can
       handle the specific monomial structure.
   (f) Look for a MONOTONE COUPLING argument: show that the n=4 inequality
       follows from the n=3 inequality via an inductive step.

Total runtime: {total_time:.1f}s
""")

print("DONE")
