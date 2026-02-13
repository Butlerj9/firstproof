"""
ce30_symbolic_mpp.py — Symbolic computation of d²(1/Φ₄)/dc'² for M''(t) analysis.

Goal: Compute f''(σ, b, c') = d²(1/Φ₄)/dc'² symbolically.
At c'=0, express M''(0) and attempt to prove M''(0) ≥ 0.

Key insight from CE-29d: each 1/Φ₄ is CONCAVE in c' (f'' < 0).
So M''(0) ≥ 0 ⟺ "parts more concave than whole".

By dimensional analysis: f''(σ, b, 0) = h(β)/σ³ where β = b²/σ³.
"""
import sys, io, time
from sympy import symbols, diff, simplify, factor, cancel, Rational
from sympy import collect, numer, denom, expand, Poly, degree
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

# Variables
sigma, b, cp = symbols('sigma b cp', real=True)

# Quartic x^4 + ax^2 + bx + c with a = -sigma, c = sigma^2/12 + cp
a_val = -sigma
c_val = sigma**2 / 12 + cp

A = a_val**2 + 12*c_val
B = 2*a_val**3 - 8*a_val*c_val + 9*b**2
Delta = (16*a_val**4*c_val - 4*a_val**3*b**2 - 128*a_val**2*c_val**2
         + 144*a_val*b**2*c_val - 27*b**4 + 256*c_val**3)

# 1/Phi4 = -Delta/(4*A*B)
f = -Delta / (4*A*B)

# ============================================================
print(SEP)
print("SECTION 1: Compute d²f/dc'² symbolically")
print(SEP)
sys.stdout.flush()

# Simplify A, B first
A_s = expand(A)
B_s = expand(B)
Delta_s = expand(Delta)
print("A =", A_s)
print("B =", B_s)
print("Delta has %d terms" % len(Delta_s.as_ordered_terms()))
sys.stdout.flush()

# First derivative df/dc'
print("\nComputing df/dc'...")
sys.stdout.flush()
f_prime = diff(f, cp)
# Don't simplify yet, evaluate at c'=0 first to keep it manageable

# Second derivative d²f/dc'²
print("Computing d²f/dc'²...")
sys.stdout.flush()
f_pp = diff(f, cp, 2)
print("Raw d²f/dc'² computed. Evaluating at c'=0...")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Evaluate at c'=0")
print(SEP)
sys.stdout.flush()

f_pp_0 = f_pp.subs(cp, 0)
print("Substituted c'=0. Simplifying...")
sys.stdout.flush()

f_pp_0_canc = cancel(f_pp_0)
print("Cancelled.")

# Get numerator and denominator
num0 = numer(f_pp_0_canc)
den0 = denom(f_pp_0_canc)

num0_exp = expand(num0)
den0_exp = expand(den0)

print("Numerator terms:", len(num0_exp.as_ordered_terms()))
print("Denominator terms:", len(den0_exp.as_ordered_terms()))
sys.stdout.flush()

# Try to factor
print("\nFactoring numerator...")
sys.stdout.flush()
try:
    num0_fac = factor(num0_exp)
    print("Numerator factored:", num0_fac)
except Exception as e:
    print("Factor failed:", e)
    num0_fac = num0_exp

print("\nFactoring denominator...")
sys.stdout.flush()
try:
    den0_fac = factor(den0_exp)
    print("Denominator factored:", den0_fac)
except Exception as e:
    print("Factor failed:", e)
    den0_fac = den0_exp

print("\nd²f/dc'²|_{c'=0} = (%s) / (%s)" % (num0_fac, den0_fac))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Scale-invariant form h(β) where β = b²/σ³")
print(SEP)

# By dimensional analysis, σ³ · f''(σ, b, 0) should depend only on β = b²/σ³
# Let's verify by substituting b = sqrt(β·σ³) — or just compute σ³·f''
beta = symbols('beta', positive=True)

# Substitute b² = β·σ³ into σ³·f''(σ, b, 0)
# Since f''(σ, b, 0) is even in b, it depends on b² only
h_raw = sigma**3 * f_pp_0_canc
h_raw = cancel(h_raw)
print("σ³ · f''(σ,b,0) =", cancel(h_raw))
sys.stdout.flush()

# Try substituting b² → β·σ³
h_sub = h_raw.subs(b**2, beta * sigma**3)
h_sub = cancel(h_sub)
print("\nAfter b² → β·σ³:")
print("h(σ, β) =", h_sub)
sys.stdout.flush()

# Check if σ cancels
h_simplified = cancel(h_sub)
print("Simplified:", h_simplified)

# Check dependence on σ
from sympy import degree as sym_degree
h_num = numer(h_simplified)
h_den = denom(h_simplified)
print("\nh numerator:", expand(h_num))
print("h denominator:", expand(h_den))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Also compute df/dc'|_{c'=0}")
print(SEP)

f_prime_0 = f_prime.subs(cp, 0)
f_prime_0_canc = cancel(f_prime_0)
num_fp = numer(f_prime_0_canc)
den_fp = denom(f_prime_0_canc)

print("df/dc'|_{c'=0} numerator terms:", len(expand(num_fp).as_ordered_terms()))
print("df/dc'|_{c'=0} denominator terms:", len(expand(den_fp).as_ordered_terms()))

try:
    num_fp_fac = factor(num_fp)
    den_fp_fac = factor(den_fp)
    print("df/dc'|_{c'=0} =", num_fp_fac, "/", den_fp_fac)
except:
    print("df/dc'|_{c'=0} = (%s) / (%s)" % (expand(num_fp), expand(den_fp)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Numerical verification")
print(SEP)

import numpy as np

def phi4_inv(sig, bv, cpv):
    av = -sig
    cv = sig**2/12.0 + cpv
    Av = av**2 + 12*cv
    Bv = 2*av**3 - 8*av*cv + 9*bv**2
    Dv = (16*av**4*cv - 4*av**3*bv**2 - 128*av**2*cv**2
          + 144*av*bv**2*cv - 27*bv**4 + 256*cv**3)
    if Dv <= 0 or Av*Bv >= 0:
        return None
    return -Dv/(4.0*Av*Bv)

# Numerical f'' via finite differences
h_fd = 1e-6
np.random.seed(42)
n_check = 0
max_err = 0

# Also check that f'' is even in b (depends on b² only)
for _ in range(5000):
    sig = np.random.uniform(0.3, 3.0)
    bv = np.random.uniform(-0.3, 0.3)
    b_max = (4*sig**3/27)**0.5 * 0.9
    if abs(bv) >= b_max:
        continue

    f0 = phi4_inv(sig, bv, 0)
    fp = phi4_inv(sig, bv, h_fd)
    fm = phi4_inv(sig, bv, -h_fd)
    if f0 is None or fp is None or fm is None:
        continue

    fpp_num = (fp - 2*f0 + fm) / h_fd**2

    # Also compute for -b
    f0n = phi4_inv(sig, -bv, 0)
    fpn = phi4_inv(sig, -bv, h_fd)
    fmn = phi4_inv(sig, -bv, -h_fd)
    if f0n is None or fpn is None or fmn is None:
        continue
    fpp_num_neg = (fpn - 2*f0n + fmn) / h_fd**2

    n_check += 1
    err = abs(fpp_num - fpp_num_neg) / (abs(fpp_num) + 1e-20)
    if err > max_err:
        max_err = err

print("b-symmetry check: %d tests, max relative error: %.2e" % (n_check, max_err))
print("Confirms f'' is even in b (depends on b² only)")
sys.stdout.flush()

# Check sign of f''
n_neg = 0
n_pos = 0
for _ in range(10000):
    sig = np.random.uniform(0.3, 3.0)
    b_max = (4*sig**3/27)**0.5 * 0.9
    bv = np.random.uniform(-b_max, b_max)

    f0 = phi4_inv(sig, bv, 0)
    fp = phi4_inv(sig, bv, h_fd)
    fm = phi4_inv(sig, bv, -h_fd)
    if f0 is None or fp is None or fm is None:
        continue
    fpp_num = (fp - 2*f0 + fm) / h_fd**2
    if fpp_num < -1e-6:
        n_neg += 1
    elif fpp_num > 1e-6:
        n_pos += 1

print("\nSign of f''(σ,b,0): negative=%d, positive=%d" % (n_neg, n_pos))
print("Confirms f'' < 0 at c'=0 (concavity)")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: M''(0) structure analysis")
print(SEP)
print("""
M''(0) = (c1'+c2')² · f''(1, b1+b2, 0)
       - c1'² · f''(w, b1, 0)
       - c2'² · f''(1-w, b2, 0)

Since f'' < 0, define g(σ,b) = -f''(σ,b,0) > 0.
Then M''(0) ≥ 0 ⟺ c1'²·g(w,b1) + c2'²·g(1-w,b2) ≥ (c1'+c2')²·g(1,b1+b2)

Using scale-invariant form: g(σ,b) = -h(β)/σ³ where β = b²/σ³.
""")

# Test M''(0) ≥ 0 numerically
n_mpp_test = 0
n_mpp_fail = 0
min_mpp = float('inf')

for _ in range(200000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.1, 0.1)
    cp2 = np.random.uniform(-0.1, 0.1)

    # Check validity at c'=0
    fh = phi4_inv(1.0, b1+b2, 0)
    f1 = phi4_inv(s1, b1, 0)
    f2 = phi4_inv(s2, b2, 0)
    if fh is None or f1 is None or f2 is None:
        continue

    # Compute f'' at c'=0 for each via finite differences
    fh_p = phi4_inv(1.0, b1+b2, h_fd)
    fh_m = phi4_inv(1.0, b1+b2, -h_fd)
    f1_p = phi4_inv(s1, b1, h_fd)
    f1_m = phi4_inv(s1, b1, -h_fd)
    f2_p = phi4_inv(s2, b2, h_fd)
    f2_m = phi4_inv(s2, b2, -h_fd)

    if any(x is None for x in [fh_p, fh_m, f1_p, f1_m, f2_p, f2_m]):
        continue

    fpp_h = (fh_p - 2*fh + fh_m) / h_fd**2
    fpp_1 = (f1_p - 2*f1 + f1_m) / h_fd**2
    fpp_2 = (f2_p - 2*f2 + f2_m) / h_fd**2

    Mpp_0 = (cp1+cp2)**2 * fpp_h - cp1**2 * fpp_1 - cp2**2 * fpp_2

    n_mpp_test += 1
    if Mpp_0 < min_mpp:
        min_mpp = Mpp_0
    if Mpp_0 < -1e-4:
        n_mpp_fail += 1

print("M''(0) tests: %d" % n_mpp_test)
print("M''(0) < 0 violations: %d" % n_mpp_fail)
print("Min M''(0): %.6e" % min_mpp)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Test if g(σ,b) = σ³·|f''(σ,b,0)| satisfies superadditivity-type condition")
print(SEP)
print("Need: c1'²·g1 + c2'²·g2 ≥ (c1'+c2')²·gh")
print("Equivalently: (c1'-c2')² ≥ 0 part + ... (look for structure)\n")

# Check the ratio g(σ,b) across different σ values at fixed β
print("g(σ,b) = σ³·|f''(σ,b,0)| as function of β = b²/σ³:")
for beta_val in [0.0, 0.01, 0.05, 0.1, 0.13, 0.145]:
    sig = 1.0
    bv = (beta_val * sig**3)**0.5

    f0 = phi4_inv(sig, bv, 0)
    fp = phi4_inv(sig, bv, h_fd)
    fm = phi4_inv(sig, bv, -h_fd)
    if f0 is None or fp is None or fm is None:
        print("  β=%.3f: invalid" % beta_val)
        continue

    fpp = (fp - 2*f0 + fm) / h_fd**2
    g_val = sig**3 * abs(fpp)
    print("  β=%.4f: g = %.6f, f'' = %.6f" % (beta_val, g_val, fpp))

sys.stdout.flush()

# Check if g(σ,b) = -h(β)/σ³ · σ³ = -h(β) is concave/convex in β
print("\nIs -h(β) (i.e., g at σ=1) concave in β?")
betas = np.linspace(0.001, 0.145, 50)
g_vals = []
for beta_val in betas:
    bv = beta_val**0.5  # σ=1, so β = b²
    f0 = phi4_inv(1.0, bv, 0)
    fp = phi4_inv(1.0, bv, h_fd)
    fm = phi4_inv(1.0, bv, -h_fd)
    if f0 is None or fp is None or fm is None:
        g_vals.append(None)
        continue
    fpp = (fp - 2*f0 + fm) / h_fd**2
    g_vals.append(-fpp)  # g = -f'' > 0

# Check concavity of g in β via second finite differences
hb = betas[1] - betas[0]
n_conv = 0
n_conc = 0
for i in range(1, len(betas)-1):
    if g_vals[i-1] is None or g_vals[i] is None or g_vals[i+1] is None:
        continue
    d2g = (g_vals[i+1] - 2*g_vals[i] + g_vals[i-1]) / hb**2
    if d2g > 1e-3:
        n_conv += 1
    elif d2g < -1e-3:
        n_conc += 1

print("g(β) second-derivative sign: convex=%d, concave=%d" % (n_conv, n_conc))
if g_vals[0] is not None and g_vals[-1] is not None:
    print("g(0) = %.6f, g(0.145) = %.6f" % (g_vals[0], g_vals[-1] if g_vals[-1] else float('nan')))

sys.stdout.flush()

print("\nElapsed: %.1fs" % (time.time() - t0))
