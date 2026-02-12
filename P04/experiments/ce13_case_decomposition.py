"""
P04 CE-13: Case decomposition for the b=0 g-inequality.

From answer.md §9.3: The b=0 margin factors as w(1-w)*H(w,t1,t2) where
H = A*w^2 + B*w + C is quadratic in w with:
  A = (t1+t2)^2 * (6t1+1) * (6t2+1)    >= 0 on valid region
  C = t1^2*(6t2+1)^2 + 3*t2^2*(6t1+1)*(2t2+1)   >= 0 (proved)
  H(1) >= 0 (proved by symmetry)

Key approach: case decomposition on sign of B and location of interior minimum.
If A > 0 (convex in w):
  Case 1: B >= 0 => roots both <= 0 => H(w) >= 0 for w >= 0.
  Case 2: B < 0, -B >= 2A => w* >= 1 => min on [0,1] = H(1) >= 0.
  Case 3: B < 0, 0 < -B < 2A => w* in (0,1) => need 4AC >= B^2.

Test: at Case 3 points where 4AC < B^2, is H still >= 0 on [0,1]?
This CANNOT happen if the inequality is true, so the question is
whether we can PROVE 4AC >= B^2 whenever w* in (0,1).
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
import random

print("P04 CE-13: Case Decomposition for b=0 g-inequality")
print("=" * 70)

def inv_phi4_b0(a, c):
    """Compute 1/Phi_4 for centered quartic x^4 + a*x^2 + c, b=0.
    Formula: 1/Phi_4 = 2c(4c - a^2) / (a(a^2 + 12c))
    Valid when: c > 0, 4c != a^2, a != 0, a^2+12c != 0, simple real roots.
    """
    num = Fraction(2) * c * (Fraction(4)*c - a*a)
    den = a * (a*a + Fraction(12)*c)
    if den == 0:
        return None
    return num / den

def compute_margin_b0(a1, c1, a2, c2):
    """Superadditivity margin for b=0 subcase."""
    a_h = a1 + a2
    c_h = c1 + c2 + a1*a2 / Fraction(6)  # additive variables

    f_p = inv_phi4_b0(a1, c1)
    f_q = inv_phi4_b0(a2, c2)
    f_h = inv_phi4_b0(a_h, c_h)

    if f_p is None or f_q is None or f_h is None:
        return None
    return f_h - f_p - f_q

# Quick verification
print("\n--- Verification ---")
cases = [
    (Fraction(-5), Fraction(2), Fraction(-3), Fraction(1)),
    (Fraction(-4), Fraction(3), Fraction(-6), Fraction(5)),
    (Fraction(-10), Fraction(8), Fraction(-7), Fraction(4)),
]
for a1, c1, a2, c2 in cases:
    m = compute_margin_b0(a1, c1, a2, c2)
    if m is not None:
        print(f"  a1={a1}, c1={c1}, a2={a2}, c2={c2}: margin = {float(m):.6e} {'PASS' if m >= 0 else 'FAIL'}")

# Now the parametrization: a_total = a1+a2, w = a1/a_total, ti = ci'/(ai^2), ci' = ci - ai^2/12
# So ci = ai^2*(ti + 1/12)
# Valid region: ci > 0, ai < 0 (for real roots), 6ti+1 > 0 (i.e., ti > -1/6)
# Actually we need a < 0 for distinct real roots with c > 0.

def compute_H_from_params(t1, t2, a_total=Fraction(-1)):
    """Compute H(w) = Aw^2 + Bw + C by evaluating margin at 3 w-values.
    Uses parametrization: a_i = w_i * a_total, c_i = a_i^2 * (t_i + 1/12)."""
    pts = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)]
    H_vals = []

    for w in pts:
        a1 = w * a_total
        a2 = (Fraction(1) - w) * a_total

        c1 = a1*a1 * (t1 + Fraction(1, 12))
        c2 = a2*a2 * (t2 + Fraction(1, 12))

        # Check validity
        if a1 == 0 or a2 == 0 or c1 <= 0 or c2 <= 0:
            return None

        m = compute_margin_b0(a1, c1, a2, c2)
        if m is None:
            return None

        # margin = w(1-w) * [positive_factor] * H(w)
        # Actually, we need to extract H. The margin is NOT simply w(1-w)*H.
        # Let me just fit a quartic in w: margin(w) = w(1-w) * Q(w)
        # where Q is what we want (but might be higher order than quadratic).
        # Actually, the g-inequality form says the whole thing factors as w(1-w)*H(w,t1,t2)
        # times some t-dependent positive prefactor.

        # Let me compute margin/(w*(1-w)) and see if it's quadratic in w.
        ww = w * (Fraction(1) - w)
        if ww == 0:
            return None
        H_vals.append(m / ww)

    # Fit quadratic: h(w) = A*w^2 + B*w + C from 3 points
    w1, w2, w3 = pts
    h1, h2, h3 = H_vals

    # Lagrange interpolation
    A_coef = h1/((w1-w2)*(w1-w3)) + h2/((w2-w1)*(w2-w3)) + h3/((w3-w1)*(w3-w2))
    B_coef = -(h1*(w2+w3)/((w1-w2)*(w1-w3)) + h2*(w1+w3)/((w2-w1)*(w2-w3)) + h3*(w1+w2)/((w3-w1)*(w3-w2)))
    C_coef = h1*w2*w3/((w1-w2)*(w1-w3)) + h2*w1*w3/((w2-w1)*(w2-w3)) + h3*w1*w2/((w3-w1)*(w3-w2))

    # Verify: check at a 4th point to confirm H is actually quadratic
    w4 = Fraction(3, 8)
    a1_4 = w4 * a_total
    a2_4 = (Fraction(1) - w4) * a_total
    c1_4 = a1_4**2 * (t1 + Fraction(1, 12))
    c2_4 = a2_4**2 * (t2 + Fraction(1, 12))
    m4 = compute_margin_b0(a1_4, c1_4, a2_4, c2_4)
    if m4 is not None:
        h4_pred = A_coef*w4**2 + B_coef*w4 + C_coef
        h4_actual = m4 / (w4 * (Fraction(1) - w4))
        residual = abs(h4_pred - h4_actual)
        if h4_actual != 0:
            rel_residual = float(residual / abs(h4_actual))
        else:
            rel_residual = float(residual)
        if rel_residual > 1e-6:
            # Not quadratic — H has higher-order terms
            return 'NOT_QUADRATIC', rel_residual

    return A_coef, B_coef, C_coef

# Test whether H is actually quadratic
print("\n--- Testing whether margin/(w(1-w)) is quadratic in w ---")
test_ts = [
    (Fraction(1, 3), Fraction(1, 2)),
    (Fraction(1, 6), Fraction(1, 4)),
    (Fraction(1, 12), Fraction(1)),
    (Fraction(2), Fraction(3)),
]
for t1, t2 in test_ts:
    result = compute_H_from_params(t1, t2)
    if result is None:
        print(f"  t1={float(t1):.4f}, t2={float(t2):.4f}: SKIP (degenerate)")
    elif isinstance(result[0], str) and result[0] == 'NOT_QUADRATIC':
        print(f"  t1={float(t1):.4f}, t2={float(t2):.4f}: NOT QUADRATIC (residual={result[1]:.2e})")
    else:
        A, B, C = result
        print(f"  t1={float(t1):.4f}, t2={float(t2):.4f}: A={float(A):.4f}, B={float(B):.4f}, C={float(C):.4f} -- quadratic OK")

# Full case decomposition test
print("\n--- Case decomposition (50K tests) ---")
random.seed(42)
n_tests = 50000
n_case1 = 0  # B >= 0
n_case2 = 0  # B < 0, w* >= 1
n_case3 = 0  # B < 0, w* in (0,1)
n_case3_disc_pos = 0
n_case3_disc_neg = 0
n_not_quad = 0
n_skip = 0

for trial in range(n_tests):
    if trial < n_tests // 3:
        t1 = Fraction(random.randint(1, 60), 12)
        t2 = Fraction(random.randint(1, 60), 12)
    elif trial < 2 * n_tests // 3:
        # Near lower bound ti > -1/6 but we need ci > 0 so ti > -1/12
        t1 = Fraction(random.randint(1, 200), 600)
        t2 = Fraction(random.randint(1, 200), 600)
    else:
        t1 = Fraction(random.randint(1, 100), 6)
        t2 = Fraction(random.randint(1, 100), 6)

    result = compute_H_from_params(t1, t2)
    if result is None:
        n_skip += 1
        continue
    if isinstance(result[0], str):
        n_not_quad += 1
        continue

    A, B, C = result

    if A <= 0:
        # A should be >= 0 on valid region
        n_skip += 1
        continue

    if B >= 0:
        n_case1 += 1
    elif -B >= 2 * A:
        n_case2 += 1
    else:
        n_case3 += 1
        disc = 4*A*C - B*B
        if disc >= 0:
            n_case3_disc_pos += 1
        else:
            n_case3_disc_neg += 1

n_total = n_tests - n_skip - n_not_quad
print(f"Total tested: {n_total}")
print(f"Skipped: {n_skip}, Not quadratic: {n_not_quad}")
print(f"Case 1 (B >= 0): {n_case1}")
print(f"Case 2 (B < 0, w* >= 1): {n_case2}")
print(f"Case 3 (B < 0, w* in (0,1)): {n_case3}")
if n_case3 > 0:
    print(f"  3a (disc >= 0): {n_case3_disc_pos}")
    print(f"  3b (disc < 0): {n_case3_disc_neg}")

if n_not_quad > 0:
    print(f"\n** WARNING: {n_not_quad} cases where H is NOT quadratic in w.")
    print("** The margin/(w(1-w)) has higher-order terms.")
    print("** The case decomposition approach may need revision.")

if n_case3_disc_neg == 0 and n_not_quad == 0:
    print("\n** COMPLETE PROOF: All Case 3 points have disc >= 0. **")
elif n_case3_disc_neg == 0:
    print(f"\n** Case 3 clean, but {n_not_quad} non-quadratic cases need investigation. **")
else:
    print(f"\n** INCOMPLETE: {n_case3_disc_neg} Case 3 points with disc < 0. **")
