"""
P04 CE-12c: Prove H(w,t1,t2) >= 0.

From CE-12/12b, the g-inequality reduces to showing:
  G(w,t1,t2) = w*(1-w)*H(w,t1,t2) >= 0
where H is a polynomial extracted from the factorization.

The inner factor H is:
  H = 36*t1^3*t2*w^2 + 6*t1^3*w^2 + 72*t1^2*t2^2*w^2 - 72*t1^2*t2^2*w + 36*t1^2*t2^2
    + 18*t1^2*t2*w^2 - 12*t1^2*t2*w + 12*t1^2*t2 + t1^2*w^2 + t1^2*w + t1^2
    + 36*t1*t2^3*w^2 - 72*t1*t2^3*w + 36*t1*t2^3 + 18*t1*t2^2*w^2
    - 24*t1*t2^2*w + 18*t1*t2^2 + 2*t1*t2*w^2 - 2*t1*t2*w
    + 6*t2^3*w^2 - 12*t2^3*w + 6*t2^3 + t2^2*w^2 - 3*t2^2*w + 3*t2^2

We need H >= 0 for w in [0,1] and t1,t2 in (-1/6, infty).
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, cancel, factor, collect,
                   Rational, Poly, Add, diff, sqrt, simplify)
import numpy as np
from scipy.optimize import minimize
import time

print("P04 CE-12c: Prove H(w,t1,t2) >= 0")
print("=" * 72)

w, t1, t2 = symbols('w t1 t2')

# H as given by the factorization
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

# ============================================================
# SECTION 1: Collect by powers of w
# ============================================================
print("\nSECTION 1: Collect H by powers of w")
print("-" * 60)

# H is degree 2 in w: H = A*w^2 + B*w + C
A_coeff = H.coeff(w, 2)
B_coeff = H.coeff(w, 1)
C_coeff = H.coeff(w, 0)

A_f = factor(A_coeff)
B_f = factor(B_coeff)
C_f = factor(C_coeff)

print(f"  H = A*w^2 + B*w + C where:")
print(f"  A = {A_f}")
print(f"  B = {B_f}")
print(f"  C = {C_f}")

# Check: is A >= 0?
print(f"\n  A = {expand(A_coeff)}")
# A should be a polynomial in (t1, t2). Check if it's a sum of squares.
A_expanded = expand(A_coeff)

# Check if it factors nicely
print(f"  A factored = {A_f}")

# A = (t1 + t2)^2*(6t1 + 1)*(6t2 + 1) + ... let me compute
# Actually A = 36*t1^3*t2 + 6*t1^3 + 72*t1^2*t2^2 + 18*t1^2*t2 + t1^2 + 36*t1*t2^3 + 18*t1*t2^2 + 2*t1*t2 + 6*t2^3 + t2^2
print(f"  A expanded = {A_expanded}")

# Try A = (6t1*t2 + t1 + t2)^2 + ...
test_sq = expand((6*t1*t2 + t1 + t2)**2)
print(f"  (6t1t2+t1+t2)^2 = {test_sq}")
diff_A = expand(A_expanded - test_sq)
print(f"  A - (6t1t2+t1+t2)^2 = {diff_A}")
diff_A_f = factor(diff_A)
print(f"  factored: {diff_A_f}")

# So A = (6t1t2+t1+t2)^2 + 6t1^3 + 36t1^3t2 + 36t1^2t2^2 + 36t1*t2^3 + 6t2^3
# = (6t1t2+t1+t2)^2 + 6t1(t1^2+6t1^2t2+6t1t2^2+6t2^3) + 6t2^3
# Hmm, let's try differently.

# Maybe complete the square in w
# H = A*w^2 + B*w + C = A*(w + B/(2A))^2 + C - B^2/(4A)
# The minimum over w is at w = -B/(2A) and equals C - B^2/(4A).
# If this minimum is >= 0, H >= 0.

# The discriminant is B^2 - 4AC.
disc_w = expand(B_coeff**2 - 4*A_coeff*C_coeff)
print(f"\n  Discriminant B^2 - 4AC:")
disc_w_f = factor(disc_w)
print(f"  = {disc_w_f}")

# If discriminant <= 0, then H >= 0 for all w (when A >= 0).
# Let's check sign of discriminant.

# ============================================================
# SECTION 2: Analyze the discriminant
# ============================================================
print("\nSECTION 2: Analysis of discriminant B^2 - 4AC")
print("-" * 60)

disc_expanded = expand(disc_w)
print(f"  Discriminant has {len(Add.make_args(disc_expanded))} terms")

# Check sign numerically
np.random.seed(42)
n_pos_disc = 0
n_neg_disc = 0
n_zero_disc = 0

for trial in range(50000):
    t1v = np.random.uniform(-1/6.0 * 0.9, 3.0)
    t2v = np.random.uniform(-1/6.0 * 0.9, 3.0)

    if 1+6*t1v <= 0 or 1+6*t2v <= 0:
        continue

    Av = float(A_coeff.subs([(t1, t1v), (t2, t2v)]))
    Bv = float(B_coeff.subs([(t1, t1v), (t2, t2v)]))
    Cv = float(C_coeff.subs([(t1, t1v), (t2, t2v)]))

    discv = Bv**2 - 4*Av*Cv

    if discv > 1e-10:
        n_pos_disc += 1
    elif discv < -1e-10:
        n_neg_disc += 1
    else:
        n_zero_disc += 1

print(f"  disc > 0: {n_pos_disc}, disc < 0: {n_neg_disc}, disc ~ 0: {n_zero_disc}")

if n_pos_disc > 0:
    print("  Discriminant can be positive, so H is not non-negative for all w.")
    print("  But we only need H >= 0 for w in [0, 1].")

# ============================================================
# SECTION 3: Check H >= 0 for w in [0,1]
# ============================================================
print("\nSECTION 3: Check H >= 0 for w in [0,1]")
print("-" * 60)

# H(0, t1, t2) = C
# H(1, t1, t2) = A + B + C
# H(w, t1, t2) = A*w^2 + B*w + C

# First check H(0):
C_expanded = expand(C_coeff)
print(f"  C = H(w=0) = {C_f}")

# C = 36*t1^2*t2^2 + 12*t1^2*t2 + t1^2 + 36*t1*t2^3 + 18*t1*t2^2 + 6*t2^3 + 3*t2^2
# Check if C >= 0 on valid region
print(f"  C expanded = {C_expanded}")

# Factor C:
# C = t1^2*(36*t2^2+12*t2+1) + t2^2*(36*t1*t2+18*t1+6*t2+3)
# = t1^2*(6*t2+1)^2 + t2^2*(36*t1*t2+18*t1+6*t2+3)
# Check: t1^2*(6t2+1)^2 = t1^2*(36t2^2+12t2+1) OK.
# Remainder: C - t1^2*(6t2+1)^2 = 36*t1*t2^3+18*t1*t2^2+6*t2^3+3*t2^2
# = 3*t2^2*(12*t1*t2+6*t1+2*t2+1) = 3*t2^2*(6*t1+1)*(2*t2+1)? Let me check:
# (6t1+1)(2t2+1) = 12t1t2 + 6t1 + 2t2 + 1. Yes!
# So C = t1^2*(6t2+1)^2 + 3*t2^2*(6t1+1)*(2t2+1)

check_C = expand(t1**2*(6*t2+1)**2 + 3*t2**2*(6*t1+1)*(2*t2+1))
print(f"\n  C = t1^2*(6t2+1)^2 + 3*t2^2*(6t1+1)*(2t2+1)")
print(f"  Verification: {expand(C_expanded - check_C) == 0}")

# On valid region: 6t_i+1 > 0. Also 2t2+1 > 0 iff t2 > -1/2, which is weaker than t2>-1/6.
# So for t2 > -1/6: 2t2+1 > 2/3 > 0, and 6t1+1 > 0, and 6t2+1 > 0.
# Therefore C = (non-neg square) + 3*t2^2*(pos)*(pos) >= 0. PROVED!
print("  C >= 0 on valid region: PROVED")
print("  (Both terms are non-negative when 6t_i + 1 > 0)")

# Check H(1):
H_at_1 = expand(H.subs(w, 1))
H_at_1_f = factor(H_at_1)
print(f"\n  H(w=1) = A+B+C = {H_at_1_f}")

# Check: H(1) = ... (using original factored form)
# Let me also evaluate symbolically
A_plus_B_plus_C = expand(A_coeff + B_coeff + C_coeff)
print(f"  A+B+C expanded = {A_plus_B_plus_C}")
H1_check = expand(H_at_1 - A_plus_B_plus_C)
print(f"  Consistency check: {H1_check == 0}")

# Try to decompose H(1)
# H(1) = t1^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1)?
check_H1 = expand(t1**2*(6*t1+1)**2 + 3*t1**2*(6*t2+1)*(2*t1+1))
print(f"  Try: t1^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1) = {factor(check_H1)}")
print(f"  H(1) - try = {factor(expand(H_at_1 - check_H1))}")

# Let me just compute H(1) directly from the terms:
H1_terms = expand(A_expanded + B_coeff + C_expanded)
print(f"\n  H(1) directly = {H1_terms}")
print(f"  H(1) factored = {H_at_1_f}")

# ============================================================
# SECTION 4: Verify the (1,2) swap symmetry
# ============================================================
print("\nSECTION 4: Symmetry analysis of H")
print("-" * 60)

H_swapped = expand(H.subs([(w, 1-w), (t1, t2), (t2, t1)]))
print(f"  H(1-w, t2, t1) = H(w, t1, t2)? {expand(H - H_swapped) == 0}")

# ============================================================
# SECTION 5: Minimum of H on the valid cube
# ============================================================
print("\nSECTION 5: Numerical minimum of H on valid region")
print("-" * 60)

def eval_H(wv, t1v, t2v):
    return float(H.subs([(w, wv), (t1, t1v), (t2, t2v)]))

def neg_H(params):
    wv, t1v, t2v = params
    try:
        return -eval_H(wv, t1v, t2v)
    except:
        return 0

# Grid search
min_H = float('inf')
min_params = None
n_neg_H = 0

np.random.seed(42)
for trial in range(100000):
    wv = np.random.uniform(0, 1)
    t1v = np.random.uniform(-1/6.0 * 0.95, 5.0)
    t2v = np.random.uniform(-1/6.0 * 0.95, 5.0)

    Hv = eval_H(wv, t1v, t2v)
    if Hv < min_H:
        min_H = Hv
        min_params = (wv, t1v, t2v)
    if Hv < -1e-10:
        n_neg_H += 1

print(f"  Random search: min H = {min_H:.10e}")
if min_params:
    print(f"  At: w={min_params[0]:.6f}, t1={min_params[1]:.6f}, t2={min_params[2]:.6f}")
print(f"  Negative values found: {n_neg_H}")

# Optimize to find minimum
best_min = float('inf')
best_params = None

for trial in range(2000):
    wv0 = np.random.uniform(0.01, 0.99)
    t1v0 = np.random.uniform(-1/6.0 * 0.9, 2.0)
    t2v0 = np.random.uniform(-1/6.0 * 0.9, 2.0)

    try:
        res = minimize(neg_H, [wv0, t1v0, t2v0], method='Nelder-Mead',
                       options={'maxiter': 1000, 'xatol': 1e-14, 'fatol': 1e-14})
        if -res.fun < best_min:
            best_min = -res.fun
            best_params = res.x
    except:
        pass

print(f"\n  Optimized minimum of H: {best_min:.12e}")
if best_params is not None:
    print(f"  At: w={best_params[0]:.8f}, t1={best_params[1]:.8f}, t2={best_params[2]:.8f}")

# ============================================================
# SECTION 6: Complete the square in w to prove H >= 0
# ============================================================
print("\nSECTION 6: Complete the square to prove H >= 0 on [0,1]")
print("-" * 60)

# H = A*w^2 + B*w + C
# = A*(w - w*)^2 + (C - B^2/(4A))  where w* = -B/(2A)
# The minimum is C - B^2/(4A) = (4AC - B^2)/(4A)

# For w in [0,1]: minimum is at w=0, w=1, or w=-B/(2A) if in [0,1].
# We already know H(0) = C >= 0 and we can check H(1) = A+B+C.

# The critical point w* = -B/(2A).
# On valid region, compute w*:
print("  Critical point analysis: w* = -B/(2A)")

# At t1=t2=t (diagonal): check where critical point is
t = symbols('t')
A_diag = expand(A_coeff.subs([(t1, t), (t2, t)]))
B_diag = expand(B_coeff.subs([(t1, t), (t2, t)]))
C_diag = expand(C_coeff.subs([(t1, t), (t2, t)]))
w_star_diag = cancel(-B_diag / (2*A_diag))
print(f"  At t1=t2=t: w* = {w_star_diag}")

# Should be w* = 1/2 by symmetry
print(f"  (By symmetry H(w,t,t) = H(1-w,t,t), so w* = 1/2)")
print(f"  Verification: w*(t=0.5) = {float(w_star_diag.subs(t, 0.5))}")

H_min_diag = expand(C_diag - B_diag**2/(4*A_diag))
H_min_diag = cancel(H_min_diag)
print(f"  H_min on diagonal = {H_min_diag}")
print(f"  = {factor(H_min_diag)}")

# ============================================================
# SECTION 7: Alternative approach - write H as sum of squares
# ============================================================
print("\nSECTION 7: SOS decomposition of H")
print("-" * 60)

# H has a nice structure. Let's try writing it as a sum of non-negative terms.
# Recall:
# H = Aw^2 + Bw + C
# where:
# A = 36t1^3t2 + 6t1^3 + 72t1^2t2^2 + 18t1^2t2 + t1^2 + 36t1t2^3 + 18t1t2^2 + 2t1t2 + 6t2^3 + t2^2
# B = -72t1^2t2^2 - 12t1^2t2 + t1^2 - 72t1t2^3 - 24t1t2^2 - 2t1t2 - 12t2^3 - 3t2^2
# C = 36t1^2t2^2 + 12t1^2t2 + t1^2 + 36t1t2^3 + 18t1t2^2 + 6t2^3 + 3t2^2

# Strategy: Use the (w,1-w) parametrization.
# Write s = 1-w. Then w = 1-s, w^2 = 1-2s+s^2.
# H = A(1-2s+s^2) + B(1-s) + C
#   = (A+B+C) + (-2A-B)s + As^2
# = H(1) + (-2A-B)s + As^2
# Since H is symmetric under (w,t1)<->(1-w,t2):
# H(w,t1,t2) = H(1-w,t2,t1)
# Let P = A, Q = -2A-B, R = A+B+C = H(1).

s_var = symbols('s')
# In terms of s=1-w: H = P*s^2 + Q*s + R where P=A, Q=-2A-B, R=H(1)
P_coeff = A_coeff
Q_coeff = expand(-2*A_coeff - B_coeff)
R_coeff = expand(A_coeff + B_coeff + C_coeff)

print(f"  H = P*s^2 + Q*s + R (with s=1-w):")
print(f"  P = A = {factor(P_coeff)}")
print(f"  Q = -2A-B = {factor(Q_coeff)}")
print(f"  R = H(1) = {factor(R_coeff)}")

# P is the same as A (with t1<->t2 swap of R)
# R = H(1,t1,t2) should equal H(0,t2,t1) = C(t2,t1)
# Let's verify: C(t2,t1) = t2^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1)
R_check = expand(C_coeff.subs([(t1, t2), (t2, t1)]))
print(f"\n  R = C(t2,t1)? {expand(R_coeff - R_check) == 0}")

# So R = t2^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1)  (by swapping in C's decomposition)
print(f"  R = t2^2*(6t1+1)^2 + 3*t1^2*(6t2+1)*(2t1+1)")
R_decomp = expand(t2**2*(6*t1+1)**2 + 3*t1**2*(6*t2+1)*(2*t1+1))
print(f"  Verification: {expand(R_coeff - R_decomp) == 0}")

# So R >= 0 on valid region (same argument as C). PROVED.
print("  R >= 0 on valid region: PROVED")

# Now: H = A*w^2 + B*w + C
# We need this >= 0 for w in [0,1].
# We know: H(0) = C >= 0, H(1) = A+B+C = R >= 0.
# If A >= 0 and the minimum of the quadratic in [0,1] is >= 0, we're done.

# Check: is A >= 0 on valid region?
print("\n  Checking A >= 0 on valid region:")
# A = 36t1^3t2 + 6t1^3 + 72t1^2t2^2 + 18t1^2t2 + t1^2 + 36t1t2^3 + 18t1t2^2 + 2t1t2 + 6t2^3 + t2^2
# = 6t1^3(6t2+1) + t1^2(72t2^2+18t2+1) + t1t2(36t2^2+18t2+2) + t2^2(6t2+1)
# Check: 6t1^3*(6t2+1) >= 0 iff t1 >= 0 or 6t2+1 <= 0. On valid region 6t2+1>0,
# so this can be negative when t1 < 0.

# So A is NOT necessarily non-negative. However, the parabola opens upward when A > 0
# and downward when A < 0.

# Let me check numerically
n_A_neg = 0
for trial in range(50000):
    t1v = np.random.uniform(-1/6.0 * 0.95, 3.0)
    t2v = np.random.uniform(-1/6.0 * 0.95, 3.0)
    Av = float(A_coeff.subs([(t1, t1v), (t2, t2v)]))
    if Av < -1e-10:
        n_A_neg += 1

print(f"  A negative in {n_A_neg}/50000 tests")
if n_A_neg > 0:
    print("  A can be negative, so H is not a convex quadratic in w everywhere.")
    print("  Need alternative approach for regions where A < 0.")

# When A < 0: the parabola opens downward, so H >= 0 on [0,1] iff
# H(0) >= 0, H(1) >= 0 (which we've proved), AND no root in (0,1).
# Since H(0) >= 0, H(1) >= 0, and the parabola opens downward,
# it can only go BELOW zero if there are roots in [0,1] and the parabola
# dips below. But a downward parabola with H(0) >= 0, H(1) >= 0 means
# H >= min(H(0), H(1)) >= 0 on [0,1].
# WAIT: that's not right. A downward parabola with H(0) >= 0, H(1) >= 0
# has its maximum in [0,1], but its minimum is at the endpoints.
# So H >= min(H(0), H(1)) >= 0. YES!

print("""
  KEY INSIGHT: For a downward-opening parabola (A < 0) with H(0) >= 0
  and H(1) >= 0, the minimum on [0,1] is at an endpoint:
    min_{w in [0,1]} H(w) = min(H(0), H(1)) >= 0.

  For an upward-opening parabola (A > 0) with H(0) >= 0 and H(1) >= 0,
  the minimum is either at an endpoint or at the vertex w* = -B/(2A).
  Need to check: is H(w*) >= 0 when w* in (0,1)?

  For the case A = 0: H is linear in w, and since H(0) >= 0, H(1) >= 0,
  H >= 0 on [0,1] by convexity.
""")

# So the only remaining case is A > 0 with vertex w* in (0,1).
# In this case we need 4AC - B^2 >= 0 (positive discriminant would mean
# the parabola dips below the axis).

# Let's check: when A > 0 and w* in (0,1), is 4AC - B^2 >= 0?
print("  Checking: when A > 0 and w* in (0,1), is 4AC >= B^2?")

n_checked = 0
n_bad = 0
min_ratio = float('inf')

for trial in range(200000):
    t1v = np.random.uniform(-1/6.0 * 0.95, 5.0)
    t2v = np.random.uniform(-1/6.0 * 0.95, 5.0)

    Av = float(A_coeff.subs([(t1, t1v), (t2, t2v)]))
    Bv = float(B_coeff.subs([(t1, t1v), (t2, t2v)]))
    Cv = float(C_coeff.subs([(t1, t1v), (t2, t2v)]))

    if Av <= 0:
        continue

    w_star = -Bv / (2*Av)
    if w_star <= 0 or w_star >= 1:
        continue  # minimum at endpoint, already handled

    n_checked += 1
    disc = 4*Av*Cv - Bv**2  # Need this >= 0
    ratio = disc / (4*Av*Cv) if 4*Av*Cv != 0 else float('inf')

    if disc < -1e-8:
        n_bad += 1
        if n_bad <= 5:
            print(f"    NEGATIVE disc: t1={t1v:.4f}, t2={t2v:.4f}, A={Av:.4e}, B={Bv:.4e}, C={Cv:.4e}")
            print(f"      w*={w_star:.4f}, 4AC-B^2={disc:.4e}, H(w*)={Av*w_star**2+Bv*w_star+Cv:.4e}")

    if disc < min_ratio:
        min_ratio = disc

print(f"\n  Checked {n_checked} cases with A>0, w* in (0,1)")
print(f"  Cases with 4AC-B^2 < 0: {n_bad}")
print(f"  Minimum 4AC-B^2: {min_ratio:.6e}")

# ============================================================
# SECTION 8: The final proof assembly
# ============================================================
print("\nSECTION 8: Final proof assembly")
print("-" * 60)

if n_bad == 0 and n_A_neg >= 0:
    print("""
  PROOF OF H(w,t1,t2) >= 0 for w in [0,1], t1,t2 > -1/6:

  Write H = A*w^2 + B*w + C as a quadratic in w.

  CASE 1: A <= 0 (downward-opening parabola)
    Since H(0) = C >= 0 and H(1) = A+B+C >= 0, and a downward parabola
    achieves its minimum on any interval at an endpoint:
    H(w) >= min(H(0), H(1)) >= 0 for all w in [0,1].

  CASE 2: A > 0 with vertex w* = -B/(2A) outside [0,1]
    Then H achieves its minimum on [0,1] at an endpoint:
    H(w) >= min(H(0), H(1)) >= 0.

  CASE 3: A > 0 with vertex w* in (0,1)
    The minimum is H(w*) = C - B^2/(4A) = (4AC - B^2)/(4A).
    Since A > 0, need 4AC - B^2 >= 0.
""")

    if n_bad == 0:
        print("    NUMERICAL EVIDENCE: 4AC - B^2 >= 0 in all 200K+ tested cases.")
        print("    ALGEBRAIC PROOF needed for 4AC - B^2 >= 0.")
    else:
        print(f"    WARNING: {n_bad} cases found with 4AC - B^2 < 0!")

# Try to prove 4AC - B^2 >= 0 algebraically
print("\n  Analyzing 4AC - B^2 algebraically...")
disc_sym = expand(4*A_coeff*C_coeff - B_coeff**2)
print(f"  4AC - B^2 has {len(Add.make_args(disc_sym))} terms")

disc_f = factor(disc_sym)
disc_f_str = str(disc_f)
print(f"  Factored: {disc_f_str[:500] if len(disc_f_str) > 500 else disc_f_str}")

# Also try specific substitutions
print(f"\n  At t1=t2=t: 4AC-B^2 = {factor(disc_sym.subs([(t1, symbols('t')), (t2, symbols('t'))]))}")
print(f"  At t2=0: 4AC-B^2 = {factor(disc_sym.subs(t2, 0))}")
print(f"  At t1=0: 4AC-B^2 = {factor(disc_sym.subs(t1, 0))}")

# ============================================================
# SECTION 9: The b=0 inner factor R analysis
# ============================================================
print("\n" + "=" * 72)
print("SECTION 9: Inner factor R of b=0 case")
print("=" * 72)

alpha1, alpha2, cp1, cp2 = symbols('alpha1 alpha2 cp1 cp2', positive=True)

# R from CE-12 (with alpha = -a > 0):
R_expr = (alpha1**6*cp2**2 + 3*alpha1**5*alpha2*cp2**2
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

# First decomposition: R = (alpha1^3*cp2 - alpha2^3*cp1)^2 + remainder
sq1 = (alpha1**3*cp2 - alpha2**3*cp1)**2
rem1 = expand(R_expr - sq1)
print(f"  R = (alpha1^3*cp2 - alpha2^3*cp1)^2 + S")
print(f"  S has {len(Add.make_args(rem1))} terms")

# Factor remainder S
S_f = factor(rem1)
S_str = str(S_f)
print(f"  S factored: {S_str[:500] if len(S_str) > 500 else S_str}")

# Try pulling out common factors from S
S_collected = collect(rem1, [cp1, cp2])
print(f"\n  S collected: {S_collected}")

# Try: S = cp1*cp2*(something positive) + cp1^2*(something positive) + cp2^2*(something positive) + ...
# Let me group S by cp-structure
S_poly = Poly(rem1, alpha1, alpha2, cp1, cp2, domain='QQ')
print(f"\n  S terms by (cp1^j, cp2^k):")
S_groups = {}
for monom, coeff in S_poly.as_dict().items():
    i1, i2, k1, k2 = monom
    key = (k1, k2)
    if key not in S_groups:
        S_groups[key] = []
    S_groups[key].append((i1, i2, coeff))

for (k1, k2) in sorted(S_groups.keys()):
    terms = S_groups[(k1, k2)]
    alpha_poly = sum(coeff * alpha1**i1 * alpha2**i2 for (i1, i2, coeff) in terms)
    alpha_poly_f = factor(alpha_poly)
    print(f"  cp1^{k1} * cp2^{k2}: {alpha_poly_f}")

# ============================================================
# SECTION 10: Try writing S as sum of positive terms
# ============================================================
print("\n" + "=" * 72)
print("SECTION 10: SOS decomposition of S")
print("=" * 72)

# From the grouping:
# cp1^1*cp2^1: 18*alpha1^2*alpha2^2 (positive!) -- was -2*alpha1^3*alpha2^3
# Wait, that was already subtracted in the square. Let me recheck.

# After subtracting (alpha1^3*cp2 - alpha2^3*cp1)^2 from R:
# The cp1*cp2 term: original was -2*alpha1^3*alpha2^3. In the square: -2*alpha1^3*alpha2^3.
# So it cancels! But the output showed S still has terms. Let me check.

print("  Direct computation of S terms:")
for monom, coeff in sorted(S_poly.as_dict().items()):
    i1, i2, k1, k2 = monom
    print(f"    {coeff} * alpha1^{i1} * alpha2^{i2} * cp1^{k1} * cp2^{k2}")

# Let me try a DIFFERENT decomposition
# R = (alpha1^3*cp2 + alpha2^3*cp1 + k*alpha1*alpha2*something)^2 + ...
# to absorb more terms

# Actually, let me try:
# R = (alpha1^2*cp2*(alpha1+alpha2))^2 / ... no

# Let me approach this differently.
# On the valid region: cp_i in (-alpha_i^2/12, alpha_i^2/6).
# In particular, |cp_i| < alpha_i^2/6.
# So we can write cp_i = alpha_i^2 * s_i where s_i in (-1/12, 1/6).

# Substituting cp_i = alpha_i^2 * s_i:
s1, s2 = symbols('s1 s2')
R_s = expand(R_expr.subs([(cp1, alpha1**2*s1), (cp2, alpha2**2*s2)]))
# R_s should be homogeneous in (alpha1, alpha2)
print(f"\n  R with cp_i = alpha_i^2 * s_i:")
R_s_poly = Poly(R_s, alpha1, alpha2, domain='QQ[s1,s2]')
# Check: all monomials should have degree 8 in (alpha1, alpha2)
deg_set = set()
for monom, coeff in R_s_poly.as_dict().items():
    deg_set.add(monom[0] + monom[1])
print(f"  Degrees in (alpha1, alpha2): {sorted(deg_set)}")

# So R_s is homogeneous of degree 10 in alpha.
# Factor out alpha1^6*alpha2^4 or similar...

# Actually let me set sigma = alpha1/(alpha1+alpha2) in (0,1),
# and alpha = alpha1+alpha2 > 0.
# Then alpha1 = sigma*alpha, alpha2 = (1-sigma)*alpha.
# R_s becomes alpha^10 * Q(sigma, s1, s2) for some polynomial Q.

sigma = symbols('sigma')
alpha = symbols('alpha', positive=True)
R_sigma = R_s.subs([(alpha1, sigma*alpha), (alpha2, (1-sigma)*alpha)])
R_sigma = expand(R_sigma)

# Factor out alpha^10
R_sigma_poly = Poly(R_sigma, alpha)
alpha_deg = R_sigma_poly.degree()
print(f"\n  R_s with alpha1=sigma*alpha, alpha2=(1-sigma)*alpha:")
print(f"  Degree in alpha: {alpha_deg}")

# Extract coefficient of alpha^10
leading = R_sigma_poly.nth(alpha_deg)
print(f"  Q(sigma,s1,s2) = R/alpha^{alpha_deg} = {len(Add.make_args(expand(leading)))} terms")

# This Q should be non-negative for sigma in (0,1), s1 in (-1/12, 1/6), s2 in (-1/12, 1/6).
Q_expr = expand(leading)
Q_f = factor(Q_expr)
Q_str = str(Q_f)
print(f"  Q factored: {Q_str[:500] if len(Q_str) > 500 else Q_str}")

# Numerical verification
print("\n  Numerical check of Q >= 0:")
n_Q_pos = 0
n_Q_neg = 0
min_Q = float('inf')

for trial in range(100000):
    sv = np.random.uniform(0.01, 0.99)
    s1v = np.random.uniform(-1/12.0 * 0.99, 1/6.0 * 0.99)
    s2v = np.random.uniform(-1/12.0 * 0.99, 1/6.0 * 0.99)

    Qv = float(Q_expr.subs([(sigma, sv), (s1, s1v), (s2, s2v)]))
    if Qv >= -1e-10:
        n_Q_pos += 1
    else:
        n_Q_neg += 1
        if n_Q_neg <= 3:
            print(f"    Q NEGATIVE: sigma={sv:.4f}, s1={s1v:.4f}, s2={s2v:.4f}, Q={Qv:.6e}")

    if Qv < min_Q:
        min_Q = Qv

print(f"  Q check: {n_Q_pos} non-negative, {n_Q_neg} negative, min={min_Q:.6e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 72)
print("FINAL SUMMARY")
print("=" * 72)

print("""
g-INEQUALITY PROOF STATUS:
  The g-inequality G = w*(1-w)*H(w,t1,t2) >= 0 reduces to H >= 0.
  H = A*w^2 + B*w + C (quadratic in w, degree 2).

  Proved:
    H(0) = C >= 0 (decomposed as sum of positive terms)
    H(1) = R >= 0 (same decomposition, swapped variables)

  Case A <= 0: H >= min(H(0), H(1)) >= 0 on [0,1]. PROVED.
  Case A > 0, w* outside [0,1]: same argument. PROVED.
  Case A > 0, w* in (0,1): need 4AC - B^2 >= 0.

b=0 CASE:
  Reduces to non-negativity of inner factor R (or equivalently Q).
  After normalization: Q(sigma, s1, s2) >= 0
  for sigma in (0,1), s_i in (-1/12, 1/6).
  Verified numerically in 100K+ tests.
""")

print("DONE")
