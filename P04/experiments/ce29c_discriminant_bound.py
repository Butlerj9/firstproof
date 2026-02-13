"""
ce29c_discriminant_bound.py — Test the discriminant condition for convex minimum.

For convex M(t) with M(0) >= 0:
  M(t) >= M(0) + M'(0)*t (tangent line bound)
  Minimum at t* = -M'(0)/M''(t*) ... need uniform M'' bound

If M'' >= kappa > 0 uniformly, then M(t*) >= M(0) - M'(0)^2 / (2*kappa).
Condition: 2*kappa*M(0) >= M'(0)^2.

But kappa varies per parameter set. So test per-parameter-set:
  For each (w, b1, b2, cp1, cp2), compute M(0), M'(0), min M''(t).
  Check: 2*min_M''*M(0) >= M'(0)^2

Also test: boundary factorization.
At Delta_1 = 0: P = (A1*B1) * (Dh*A2B2 - D2*AhBh)
So M >= 0 at boundary iff 1/Phi4(h) >= 1/Phi4(q).
Test this "monotonicity" property directly.
"""
import sys, io, time
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_inv(sigma, b, cp):
    """1/Phi4 via closed form. Returns (value, valid)."""
    a = -sigma
    c = sigma**2 / 12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    if Delta <= 0 or A * B >= 0:
        return None, False
    val = -Delta / (4.0 * A * B)
    return val, val > 0

def margin(w, b1, b2, cp1, cp2):
    fh, okh = phi4_inv(1.0, b1+b2, cp1+cp2)
    f1, ok1 = phi4_inv(w, b1, cp1)
    f2, ok2 = phi4_inv(1.0-w, b2, cp2)
    if not (okh and ok1 and ok2):
        return None, False
    return fh - f1 - f2, True

def margin_t(w, b1, b2, cp1, cp2, t):
    return margin(w, b1, b2, t*cp1, t*cp2)

# ============================================================
print(SEP)
print("SECTION 1: Discriminant condition 2*M''*M(0) >= M'(0)^2")
print(SEP)

h = 1e-5
np.random.seed(42)
n_tested = 0
n_disc_fail = 0
min_slack = float('inf')
worst_disc = None

for _ in range(200000):
    w = np.random.uniform(0.1, 0.9)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)

    M0, ok0 = margin(w, b1, b2, 0, 0)  # M(t=0)
    if not ok0 or M0 < 1e-15:
        continue

    # M'(0) via central difference
    Mp_h, okp = margin_t(w, b1, b2, cp1, cp2, h)
    Mm_h, okm = margin_t(w, b1, b2, cp1, cp2, -h)
    if not (okp and okm):
        continue

    Mprime0 = (Mp_h - Mm_h) / (2*h)

    # Find min M''(t) over valid t range
    # First find t_max
    t_lo, t_hi = 0.0, 10.0
    for _ in range(50):
        t_mid = (t_lo + t_hi) / 2
        _, ok = margin_t(w, b1, b2, cp1, cp2, t_mid)
        if ok:
            t_lo = t_mid
        else:
            t_hi = t_mid
    t_max = t_lo
    if t_max < 0.1:
        continue

    # Sample M''(t) at several t values and find minimum
    min_Mpp = float('inf')
    for t_val in np.linspace(max(h, 0.01), min(t_max - h, t_max * 0.99), 20):
        f0, ok0t = margin_t(w, b1, b2, cp1, cp2, t_val)
        fp, okp2 = margin_t(w, b1, b2, cp1, cp2, t_val + h)
        fm, okm2 = margin_t(w, b1, b2, cp1, cp2, t_val - h)
        if not (ok0t and okp2 and okm2):
            continue
        Mpp = (fp - 2*f0 + fm) / h**2
        if Mpp < min_Mpp:
            min_Mpp = Mpp

    if min_Mpp == float('inf') or min_Mpp < 0:
        continue

    n_tested += 1

    # Discriminant condition: 2*min_Mpp*M0 >= Mprime0^2
    slack = 2 * min_Mpp * M0 - Mprime0**2

    if slack < min_slack:
        min_slack = slack
        worst_disc = (w, b1, b2, cp1, cp2, M0, Mprime0, min_Mpp, slack)

    if slack < -1e-8:
        n_disc_fail += 1

print("Tests: %d" % n_tested)
print("Discriminant failures (2M''M(0) < M'(0)^2): %d" % n_disc_fail)
print("Min slack: %.6e" % min_slack)
if worst_disc:
    w, b1, b2, cp1, cp2, m0, mp, mpp, sl = worst_disc
    print("Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f" % (w, b1, b2, cp1, cp2))
    print("  M(0)=%.6e, M'(0)=%.6e, min M''=%.6e, slack=%.6e" % (m0, mp, mpp, sl))
    print("  M'(0)^2/(2*min_M'') = %.6e vs M(0) = %.6e" % (mp**2/(2*max(mpp,1e-20)), m0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Boundary monotonicity — 1/Phi4(p⊞q) >= 1/Phi4(q)")
print(SEP)
print("At boundary where p degenerates, need 1/Phi4(h) >= 1/Phi4(q)")

np.random.seed(123)
n_mono = 0
n_mono_fail = 0

for _ in range(200000):
    w = np.random.uniform(0.05, 0.95)
    s2 = 1.0 - w
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b2 = np.random.uniform(-b2_max, b2_max)
    cp2 = np.random.uniform(-0.1, 0.1)

    # p is degenerate (1/Phi4 = 0), so its free cumulants contribute to h
    # h has sigma=1, b = b1+b2, cp = cp1+cp2
    # Choose b1, cp1 such that p is near-degenerate (Δ₁ ≈ 0)
    b1 = np.random.uniform(-0.5, 0.5)
    # cp1 is chosen so that Δ₁(w, b1, cp1) = 0 or just barely > 0
    # For simplicity, test with random cp1 and check the monotonicity condition

    cp1 = np.random.uniform(-0.1, 0.1)

    fh, okh = phi4_inv(1.0, b1+b2, cp1+cp2)
    fq, okq = phi4_inv(s2, b2, cp2)

    if not (okh and okq):
        continue

    n_mono += 1
    if fh < fq - 1e-10:
        n_mono_fail += 1

print("Monotonicity tests: %d" % n_mono)
print("Failures (1/Phi4(h) < 1/Phi4(q)): %d" % n_mono_fail)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Monotonicity focused — p exactly degenerate (Δ₁=0)")
print(SEP)
print("Set cp1 so that Δ₁(w, b1, cp1) = 0, then check 1/Phi4(h) >= 1/Phi4(q)")

from scipy.optimize import brentq

np.random.seed(456)
n_exact = 0
n_exact_fail = 0
min_gap = float('inf')

for _ in range(100000):
    w = np.random.uniform(0.1, 0.9)
    s1 = w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)

    # Find cp1 such that Δ₁(w, b1, cp1) = 0
    def delta1(cp1_val):
        a = -s1
        c = s1**2 / 12.0 + cp1_val
        return (16*a**4*c - 4*a**3*b1**2 - 128*a**2*c**2
                + 144*a*b1**2*c - 27*b1**4 + 256*c**3)

    # Try to find root of Δ₁ in cp1
    try:
        d_lo = delta1(-0.2)
        d_hi = delta1(0.2)
        if d_lo * d_hi >= 0:
            continue
        cp1_star = brentq(delta1, -0.2, 0.2)
    except:
        continue

    # Now test with various (b2, cp2)
    for _ in range(5):
        s2 = 1.0 - w
        b2_max = (4*s2**3/27)**0.5 * 0.9
        b2 = np.random.uniform(-b2_max, b2_max)
        cp2 = np.random.uniform(-0.08, 0.08)

        fh, okh = phi4_inv(1.0, b1+b2, cp1_star+cp2)
        fq, okq = phi4_inv(s2, b2, cp2)

        if not (okh and okq):
            continue

        n_exact += 1
        gap = fh - fq

        if gap < min_gap:
            min_gap = gap

        if gap < -1e-10:
            n_exact_fail += 1

print("Exact boundary tests: %d" % n_exact)
print("Failures: %d" % n_exact_fail)
if n_exact > 0:
    print("Min gap 1/Phi4(h) - 1/Phi4(q): %.6e" % min_gap)
    print("Monotonicity holds at boundary: %s" % (n_exact_fail == 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Scale analysis — what determines M(0)/M'(0)?")
print(SEP)
print("Key ratio: M(0)/|M'(0)| = how far M can drop before tangent hits 0")

np.random.seed(789)
n_ratio = 0
min_ratio = float('inf')

for _ in range(100000):
    w = np.random.uniform(0.1, 0.9)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)

    M0, ok0 = margin(w, b1, b2, 0, 0)
    if not ok0 or M0 < 1e-12:
        continue

    Mp_h, okp = margin_t(w, b1, b2, cp1, cp2, h)
    Mm_h, okm = margin_t(w, b1, b2, cp1, cp2, -h)
    if not (okp and okm):
        continue

    Mprime0 = (Mp_h - Mm_h) / (2*h)
    if Mprime0 >= 0:
        continue  # M is increasing, no risk

    n_ratio += 1
    ratio = M0 / abs(Mprime0)  # How long before tangent line hits 0

    if ratio < min_ratio:
        min_ratio = ratio

print("Cases with M'(0) < 0: %d" % n_ratio)
if n_ratio > 0:
    print("Min M(0)/|M'(0)| ratio: %.6f" % min_ratio)
    print("Tangent line reaches 0 at t = %.6f" % min_ratio)
    print("If t_max < this, then tangent bound suffices")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Compare t_zero (tangent=0) vs t_max (validity boundary)")
print(SEP)

np.random.seed(999)
n_compare = 0
n_tangent_wins = 0  # tangent reaches 0 before t_max (gap not closed by tangent)
n_boundary_wins = 0  # t_max < t_zero (tangent bound sufficient)

for _ in range(100000):
    w = np.random.uniform(0.1, 0.9)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)

    M0, ok0 = margin(w, b1, b2, 0, 0)
    if not ok0 or M0 < 1e-12:
        continue

    Mp_h, okp = margin_t(w, b1, b2, cp1, cp2, h)
    Mm_h, okm = margin_t(w, b1, b2, cp1, cp2, -h)
    if not (okp and okm):
        continue

    Mprime0 = (Mp_h - Mm_h) / (2*h)
    if Mprime0 >= 0:
        continue

    t_zero = M0 / abs(Mprime0)

    # Find t_max
    t_lo, t_hi = 0.0, 10.0
    for _ in range(50):
        t_mid = (t_lo + t_hi) / 2
        _, ok = margin_t(w, b1, b2, cp1, cp2, t_mid)
        if ok:
            t_lo = t_mid
        else:
            t_hi = t_mid
    t_max = t_lo

    if t_max < 0.01:
        continue

    n_compare += 1
    if t_zero > t_max:
        n_boundary_wins += 1  # tangent stays >= 0 for all valid t
    else:
        n_tangent_wins += 1  # tangent goes negative before t_max

print("Comparisons: %d" % n_compare)
print("Tangent bound sufficient (t_zero > t_max): %d (%.1f%%)" %
      (n_boundary_wins, 100.0 * n_boundary_wins / max(1, n_compare)))
print("Tangent insufficient (t_zero < t_max): %d (%.1f%%)" %
      (n_tangent_wins, 100.0 * n_tangent_wins / max(1, n_compare)))

if n_tangent_wins > 0:
    print("\n=> Tangent line bound alone does NOT suffice")
    print("   Need either: discriminant condition, or direct boundary proof")

print("\nElapsed: %.1fs" % (time.time() - t0))
