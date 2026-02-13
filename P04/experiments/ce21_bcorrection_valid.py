"""
ce21_bcorrection_valid.py — Test whether CE-20's b-correction violations survive
when restricted to the valid (4-real-root) region.

CE-20 found: b-correction to margin NOT always non-negative (7.6% failure).
But CE-20 did NOT enforce the validity constraint Δ>0, A·B<0.

Hypothesis: The 7.6% violations occur ONLY outside the valid region.
If true, the 2nd-order b-expansion might actually be non-negative on the valid
region, giving a proof pathway.

The b-correction to 2nd order is:
  C = (1/2)[f_bb(σ_h, c'_h) · (b₁+b₂)² - f_bb(σ₁,c'₁) · b₁² - f_bb(σ₂,c'₂) · b₂²]

where f_bb = d²(1/Φ₄)/db²|_{b=0}.

Validity at b=0 requires: Δ₀ > 0, A·B₀ < 0 where B₀ = B|_{b=0}.
At b=0: Δ₀ = 16c(a⁴ - 8a²c + 16c²) = 16c(a² - 4c)²
  = 16(c'+σ²/12)(σ² - 4c' - σ²/3)² ... needs careful expansion.

Actually, let's just check validity numerically for each sampled point.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import numpy as np
from sympy import symbols, diff, cancel, factor, lambdify, Rational

SEP = "=" * 70
t0 = time.time()

# ============================================================
# SECTION 1: Compute f_bb symbolically (copy from CE-20)
# ============================================================
print(SEP)
print("SECTION 1: Computing f_bb symbolically")
print(SEP)

sigma, b, cp = symbols("sigma b cp", real=True)
a = -sigma
c = cp + sigma**2 / 12

A_sym = a**2 + 12*c
B_sym = 2*a**3 - 8*a*c + 9*b**2
Delta_sym = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
inv_Phi4 = -Delta_sym / (4 * A_sym * B_sym)

d2_b = diff(inv_Phi4, b, b)
d2_b_at0 = cancel(d2_b.subs(b, 0))
print("f_bb =", factor(d2_b_at0))
sys.stdout.flush()

fbb_func = lambdify((sigma, cp), d2_b_at0, "numpy")

# Also need validity check at b=0
A_at0 = lambdify((sigma, cp), A_sym.subs(b, 0), "numpy")
B_at0 = lambdify((sigma, cp), B_sym.subs(b, 0), "numpy")
Delta_at0 = lambdify((sigma, cp), Delta_sym.subs(b, 0), "numpy")

def is_valid_b0(s, c_prime):
    """Check if (σ, 0, c') corresponds to a valid quartic (4 real roots)."""
    a_val = A_at0(s, c_prime)
    b_val = B_at0(s, c_prime)
    d_val = Delta_at0(s, c_prime)
    return (d_val > 0) and (a_val * b_val < 0)

# ============================================================
# SECTION 2: Test b-correction with validity filter
# ============================================================
print("\n" + SEP)
print("SECTION 2: b-correction test WITH validity filter")
print(SEP)

np.random.seed(42)
violations_valid = 0
violations_invalid = 0
total_valid = 0
total_invalid = 0
total = 0
min_correction_valid = float('inf')
min_correction_params = None

for trial in range(200000):
    s1 = np.random.uniform(0.1, 5)
    s2 = np.random.uniform(0.1, 5)
    c1 = np.random.uniform(-0.1, 0.1)
    c2 = np.random.uniform(-0.1, 0.1)
    b1 = np.random.uniform(-0.5, 0.5)
    b2 = np.random.uniform(-0.5, 0.5)

    try:
        # Check validity of all three points at b=0
        ok1 = is_valid_b0(s1, c1)
        ok2 = is_valid_b0(s2, c2)
        okh = is_valid_b0(s1+s2, c1+c2)

        if not (ok1 and ok2 and okh):
            # Not valid at b=0 — skip for valid test
            fbb_sum = fbb_func(s1+s2, c1+c2)
            fbb_1 = fbb_func(s1, c1)
            fbb_2 = fbb_func(s2, c2)
            if np.isfinite(fbb_sum) and np.isfinite(fbb_1) and np.isfinite(fbb_2):
                correction = 0.5 * (fbb_sum*(b1+b2)**2 - fbb_1*b1**2 - fbb_2*b2**2)
                total_invalid += 1
                if correction < -1e-14:
                    violations_invalid += 1
            continue

        fbb_sum = fbb_func(s1+s2, c1+c2)
        fbb_1 = fbb_func(s1, c1)
        fbb_2 = fbb_func(s2, c2)

        if not (np.isfinite(fbb_sum) and np.isfinite(fbb_1) and np.isfinite(fbb_2)):
            continue

        correction = 0.5 * (fbb_sum*(b1+b2)**2 - fbb_1*b1**2 - fbb_2*b2**2)
        total_valid += 1
        total += 1

        if correction < min_correction_valid:
            min_correction_valid = correction
            min_correction_params = (s1, s2, b1, b2, c1, c2)

        if correction < -1e-14:
            violations_valid += 1

    except:
        continue

print("Total valid-region samples: %d" % total_valid)
print("b-correction violations (valid region): %d (%.2f%%)" %
      (violations_valid, 100*violations_valid/max(1,total_valid)))
print("Min b-correction (valid region): %.6e" % min_correction_valid)
if min_correction_params:
    print("At: s1=%.4f s2=%.4f b1=%.4f b2=%.4f c1=%.6f c2=%.6f" % min_correction_params)
print()
print("Total invalid-region samples: %d" % total_invalid)
print("b-correction violations (invalid region): %d (%.2f%%)" %
      (violations_invalid, 100*violations_invalid/max(1,total_invalid)))
sys.stdout.flush()

# ============================================================
# SECTION 3: More targeted test — near the valid-region boundary
# ============================================================
print("\n" + SEP)
print("SECTION 3: Targeted test near validity boundary")
print(SEP)

# Near B=0 boundary, 1/Phi4 → +∞, so margin should be very positive.
# Near Δ=0 boundary, 1/Phi4 → 0, so margin → 0.
# The "dangerous" region is the interior of the valid region where 1/Phi4 is moderate.

# Test with larger b values and c' near validity threshold
np.random.seed(123)
targeted_violations = 0
targeted_total = 0
min_targeted = float('inf')

for trial in range(200000):
    s1 = np.random.uniform(0.2, 3)
    s2 = np.random.uniform(0.2, 3)
    # c' must satisfy validity: at b=0, need c'_i < σ_i²/6 (approx)
    # Use a wider range and filter
    c1 = np.random.uniform(-0.2, 0.15) * s1
    c2 = np.random.uniform(-0.2, 0.15) * s2
    b1 = np.random.uniform(-1, 1) * s1
    b2 = np.random.uniform(-1, 1) * s2

    try:
        ok1 = is_valid_b0(s1, c1)
        ok2 = is_valid_b0(s2, c2)
        okh = is_valid_b0(s1+s2, c1+c2)

        if not (ok1 and ok2 and okh):
            continue

        fbb_sum = fbb_func(s1+s2, c1+c2)
        fbb_1 = fbb_func(s1, c1)
        fbb_2 = fbb_func(s2, c2)

        if not (np.isfinite(fbb_sum) and np.isfinite(fbb_1) and np.isfinite(fbb_2)):
            continue

        correction = 0.5 * (fbb_sum*(b1+b2)**2 - fbb_1*b1**2 - fbb_2*b2**2)
        targeted_total += 1

        if correction < min_targeted:
            min_targeted = correction

        if correction < -1e-14:
            targeted_violations += 1

    except:
        continue

print("Targeted valid-region samples: %d" % targeted_total)
print("b-correction violations: %d (%.2f%%)" %
      (targeted_violations, 100*targeted_violations/max(1,targeted_total)))
print("Min b-correction: %.6e" % min_targeted)
sys.stdout.flush()

# ============================================================
# SECTION 4: Test full margin (not just 2nd-order) via numerical optimization
# ============================================================
print("\n" + SEP)
print("SECTION 4: Full margin minimization via scipy")
print(SEP)

def eval_1_over_phi4(s_val, b_val, cp_val):
    """Evaluate 1/Phi4 at (sigma, b, c') numerically."""
    a_val = -s_val
    c_val = cp_val + s_val**2 / 12.0

    A = a_val**2 + 12*c_val
    B = 2*a_val**3 - 8*a_val*c_val + 9*b_val**2
    D = (16*a_val**4*c_val - 4*a_val**3*b_val**2 - 128*a_val**2*c_val**2
         + 144*a_val*b_val**2*c_val - 27*b_val**4 + 256*c_val**3)

    if A == 0 or B == 0:
        return None, False

    inv_phi = -D / (4 * A * B)
    valid = (D > 0) and (inv_phi > 0)

    return inv_phi, valid

def neg_margin(params):
    """Negative of margin M, to minimize."""
    s1, s2, b1, b2, c1, c2 = params
    if s1 <= 0.01 or s2 <= 0.01:
        return 1e10

    f1, ok1 = eval_1_over_phi4(s1, b1, c1)
    f2, ok2 = eval_1_over_phi4(s2, b2, c2)
    fh, okh = eval_1_over_phi4(s1+s2, b1+b2, c1+c2)

    if not (ok1 and ok2 and okh):
        return 1e10  # penalty for invalid region

    M = fh - f1 - f2
    return -M  # minimize negative margin = maximize violation

from scipy.optimize import minimize as sp_minimize

np.random.seed(999)
best_neg_M = float('inf')
best_params = None
n_runs = 500

for run in range(n_runs):
    s1_init = np.random.uniform(0.3, 3)
    s2_init = np.random.uniform(0.3, 3)
    b1_init = np.random.uniform(-0.3, 0.3)
    b2_init = np.random.uniform(-0.3, 0.3)
    c1_init = np.random.uniform(-0.02, 0.02)
    c2_init = np.random.uniform(-0.02, 0.02)

    x0 = [s1_init, s2_init, b1_init, b2_init, c1_init, c2_init]

    try:
        res = sp_minimize(neg_margin, x0, method='Nelder-Mead',
                         options={'maxiter': 2000, 'xatol': 1e-12, 'fatol': 1e-14})
        if res.fun < best_neg_M:
            best_neg_M = res.fun
            best_params = res.x
    except:
        continue

print("Scipy optimization: %d runs" % n_runs)
print("Best -M found: %.10e" % best_neg_M)
if best_params is not None:
    s1, s2, b1, b2, c1, c2 = best_params
    print("At: s1=%.6f s2=%.6f b1=%.6f b2=%.6f c1=%.8f c2=%.8f" %
          (s1, s2, b1, b2, c1, c2))
    # Check validity
    f1, ok1 = eval_1_over_phi4(s1, b1, c1)
    f2, ok2 = eval_1_over_phi4(s2, b2, c2)
    fh, okh = eval_1_over_phi4(s1+s2, b1+b2, c1+c2)
    print("Valid? p:%s q:%s h:%s" % (ok1, ok2, okh))
    if ok1 and ok2 and okh:
        M = fh - f1 - f2
        print("M = %.15e" % M)
        print("b values: b1=%.6f b2=%.6f (both zero? %s)" % (b1, b2, abs(b1)<1e-6 and abs(b2)<1e-6))

print("\nAll runs converge to b1≈0, b2≈0?")
# Do a focused search specifically with b≠0
print("\n--- Focused search with b constrained away from 0 ---")
best_constrained = float('inf')
best_c_params = None
for run in range(500):
    s1_init = np.random.uniform(0.3, 3)
    s2_init = np.random.uniform(0.3, 3)
    # Force b away from 0
    b1_init = np.random.choice([-1, 1]) * np.random.uniform(0.05, 0.4)
    b2_init = np.random.choice([-1, 1]) * np.random.uniform(0.05, 0.4)
    c1_init = np.random.uniform(-0.02, 0.02)
    c2_init = np.random.uniform(-0.02, 0.02)

    x0 = [s1_init, s2_init, b1_init, b2_init, c1_init, c2_init]

    try:
        res = sp_minimize(neg_margin, x0, method='Nelder-Mead',
                         options={'maxiter': 5000, 'xatol': 1e-12, 'fatol': 1e-14})
        if res.fun < best_constrained:
            best_constrained = res.fun
            best_c_params = res.x
    except:
        continue

print("Best -M (b-constrained starts): %.10e" % best_constrained)
if best_c_params is not None:
    s1, s2, b1, b2, c1, c2 = best_c_params
    print("At: s1=%.6f s2=%.6f b1=%.6f b2=%.6f c1=%.8f c2=%.8f" %
          (s1, s2, b1, b2, c1, c2))
    f1, ok1 = eval_1_over_phi4(s1, b1, c1)
    f2, ok2 = eval_1_over_phi4(s2, b2, c2)
    fh, okh = eval_1_over_phi4(s1+s2, b1+b2, c1+c2)
    print("Valid? p:%s q:%s h:%s" % (ok1, ok2, okh))
    if ok1 and ok2 and okh:
        M = fh - f1 - f2
        print("M = %.15e" % M)
        print("b values: b1=%.6f b2=%.6f" % (b1, b2))

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
