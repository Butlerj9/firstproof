"""
ce28c_convexity_proof_structure.py — Analyze the proof structure of parametric c' convexity.

CE-28b confirmed: M(w, b1, b2, t*cp1, t*cp2) is convex in t (61,535 tests, 0 violations).
But convexity + M(0) >= 0 does NOT imply M(t) >= 0 unless we also know:
  (a) M is monotone non-decreasing (M'(0) >= 0), OR
  (b) M at the minimum of the convex curve is >= 0

This script investigates:
  1. Fix Section 4 bug and properly compute dM/dt at t=0
  2. When dM/dt(0) < 0, compute the minimum of M(t) over t >= 0
  3. Analyze boundary behavior: what happens as Delta -> 0?
  4. Test if a DIFFERENT parameterization gives convexity with M'(0) >= 0
  5. Look for a direct non-negativity proof of the convex minimum
"""
import sys, io, time, random
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_formula(sigma, b, cp):
    """1/Phi4 via closed form."""
    a = -sigma
    c = sigma**2 / 12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    if Delta <= 0:
        return None, False
    if A * B >= 0:
        return None, False
    val = -Delta / (4.0 * A * B)
    if val <= 0:
        return None, False
    return val, True

def margin(w, b1, b2, cp1, cp2):
    s1, s2, sh = w, 1.0 - w, 1.0
    fh, okh = phi4_formula(sh, b1+b2, cp1+cp2)
    f1, ok1 = phi4_formula(s1, b1, cp1)
    f2, ok2 = phi4_formula(s2, b2, cp2)
    if not (okh and ok1 and ok2):
        return None, False
    return fh - f1 - f2, True

def margin_t(w, b1, b2, cp1, cp2, t):
    """Margin with c' scaled by t."""
    return margin(w, b1, b2, t*cp1, t*cp2)

# ============================================================
print(SEP)
print("SECTION 1: Proper dM/dt at t=0 (fixed)")
print(SEP)

h = 1e-6
random.seed(42)
n_tested = 0
n_negative = 0
min_deriv = float('inf')
max_deriv = -float('inf')
max_abs_deriv = 0.0

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    M_0, ok0 = margin(w, b1, b2, 0, 0)  # t=0: c'=0
    Mp, okp = margin_t(w, b1, b2, cp1, cp2, h)
    Mm, okm = margin_t(w, b1, b2, cp1, cp2, -h)

    if not (ok0 and okp and okm):
        continue

    n_tested += 1
    # Central difference for first derivative
    d1 = (Mp - Mm) / (2 * h)

    if d1 < 0:
        n_negative += 1

    if d1 < min_deriv:
        min_deriv = d1
    if d1 > max_deriv:
        max_deriv = d1
    if abs(d1) > max_abs_deriv:
        max_abs_deriv = abs(d1)

print("Tests: %d" % n_tested)
print("dM/dt < 0 at t=0: %d (%.1f%%)" % (n_negative, 100.0 * n_negative / max(1, n_tested)))
print("Min dM/dt: %.6e" % min_deriv)
print("Max dM/dt: %.6e" % max_deriv)
print("Max |dM/dt|: %.6e" % max_abs_deriv)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Find minimum of convex M(t) when dM/dt(0) < 0")
print(SEP)
print("(If M is convex, min is at unique t* where M'(t*) = 0)")

random.seed(123)
n_minima = 0
min_M_star = float('inf')
worst_min = None

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    M_0, ok0 = margin(w, b1, b2, 0, 0)
    if not ok0:
        continue

    # Check if dM/dt < 0 at t=0
    Mp, okp = margin_t(w, b1, b2, cp1, cp2, h)
    Mm, okm = margin_t(w, b1, b2, cp1, cp2, -h)
    if not (okp and okm):
        continue
    d1 = (Mp - Mm) / (2 * h)
    if d1 >= 0:
        continue  # M is non-decreasing from t=0, so min is at t=0 (proved >= 0)

    # Find minimum via golden section search on [0, t_max]
    # First find t_max
    t_hi = 5.0
    while t_hi > 0.01:
        _, ok = margin_t(w, b1, b2, cp1, cp2, t_hi)
        if ok:
            break
        t_hi *= 0.8

    if t_hi < 0.01:
        continue

    # Golden section search for minimum (convex function)
    phi = (1 + 5**0.5) / 2
    a_gs, b_gs = 0.0, t_hi
    tol = 1e-8
    for _ in range(100):
        if b_gs - a_gs < tol:
            break
        c_gs = b_gs - (b_gs - a_gs) / phi
        d_gs = a_gs + (b_gs - a_gs) / phi
        Mc, okc = margin_t(w, b1, b2, cp1, cp2, c_gs)
        Md, okd = margin_t(w, b1, b2, cp1, cp2, d_gs)
        if not okc:
            a_gs = c_gs + tol
            continue
        if not okd:
            b_gs = d_gs - tol
            continue
        if Mc < Md:
            b_gs = d_gs
        else:
            a_gs = c_gs

    t_star = (a_gs + b_gs) / 2
    M_star, ok_star = margin_t(w, b1, b2, cp1, cp2, t_star)
    if not ok_star:
        continue

    n_minima += 1
    if M_star < min_M_star:
        min_M_star = M_star
        worst_min = (w, b1, b2, cp1, cp2, t_star, M_star, M_0)

print("Cases with dM/dt(0) < 0: %d" % n_minima)
if n_minima > 0:
    print("Min M(t*): %.6e" % min_M_star)
    if worst_min:
        w, b1, b2, cp1, cp2, ts, ms, m0 = worst_min
        print("Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f" % (w, b1, b2, cp1, cp2))
        print("  t*=%.6f, M(t*)=%.6e, M(0)=%.6e, ratio M(t*)/M(0)=%.4f" %
              (ts, ms, m0, ms / max(1e-15, m0)))
    print("All minima >= 0: %s" % (min_M_star >= -1e-10))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Ratio analysis — how much does M drop from M(0)?")
print(SEP)

random.seed(456)
n_ratio = 0
min_ratio = float('inf')
max_drop = 0.0

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    s1 = w
    s2 = 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = random.uniform(-b1_max, b1_max)
    b2 = random.uniform(-b2_max, b2_max)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    M_0, ok0 = margin(w, b1, b2, 0, 0)
    M_1, ok1 = margin(w, b1, b2, cp1, cp2)

    if not (ok0 and ok1) or M_0 < 1e-10:
        continue

    n_ratio += 1
    ratio = M_1 / M_0
    drop = M_0 - M_1

    if ratio < min_ratio:
        min_ratio = ratio
    if drop > max_drop:
        max_drop = drop

print("Ratio tests: %d" % n_ratio)
print("Min M(1)/M(0) ratio: %.6f" % min_ratio)
print("Max drop M(0)-M(1): %.6e" % max_drop)
print("All M(1) >= 0: %s" % (min_ratio >= -1e-10))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Boundary limit analysis (as discriminant -> 0)")
print(SEP)

# At boundary, one discriminant -> 0 means one polynomial gets a repeated root.
# 1/Phi4 -> 0 at a repeated root (Phi4 -> infinity).
# Which polynomial degenerates determines the sign:
#   - If p or q degenerates: their 1/Phi4 -> 0, so RHS decreases -> M increases
#   - If p⊞q degenerates: 1/Phi4(p⊞q) -> 0 while p, q have finite 1/Phi4 -> M could be very negative
# Key question: can p⊞q degenerate while p, q stay non-degenerate?

random.seed(789)
n_bdry_sum = 0
n_bdry_part = 0

for _ in range(50000):
    w = random.uniform(0.15, 0.85)
    s1, s2, sh = w, 1.0 - w, 1.0
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = random.uniform(-b1_max, b1_max)
    b2 = random.uniform(-b2_max, b2_max)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    # Binary search for t_max
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

    # Check which polynomial degenerates at t_max
    a1 = -s1; c1 = s1**2/12 + t_max*cp1
    a2 = -s2; c2 = s2**2/12 + t_max*cp2
    ah = -sh; ch = sh**2/12 + t_max*(cp1+cp2)
    bh = b1 + b2

    def disc(a, b, c):
        return 16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2 + 144*a*b**2*c - 27*b**4 + 256*c**3

    D1 = disc(a1, b1, c1)
    D2 = disc(a2, b2, c2)
    Dh = disc(ah, bh, ch)

    min_D = min(D1, D2, Dh)
    if abs(min_D) > 1e-3:
        continue  # Not near boundary

    if Dh == min_D:
        n_bdry_sum += 1
    else:
        n_bdry_part += 1

print("Near-boundary cases: %d" % (n_bdry_sum + n_bdry_part))
print("  Sum p⊞q degenerates first: %d" % n_bdry_sum)
print("  Part p or q degenerates first: %d" % n_bdry_part)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Alternative — test if M(t)/M(0) is convex with value 1 at t=0")
print(SEP)
print("(If M(t)/M(0) >= 0 and is convex with value 1 at t=0, then M(t) >= 0)")

random.seed(999)
n_ratio_convex = 0
n_ratio_viol = 0
h2 = 1e-5

for _ in range(30000):
    w = random.uniform(0.15, 0.85)
    b1 = random.uniform(-0.3, 0.3)
    b2 = random.uniform(-0.3, 0.3)
    cp1 = random.uniform(-0.05, 0.05)
    cp2 = random.uniform(-0.05, 0.05)

    M_0, ok0 = margin(w, b1, b2, 0, 0)
    if not ok0 or M_0 < 1e-10:
        continue

    for t_val in np.linspace(0.1, 2.0, 8):
        f0, ok_f = margin_t(w, b1, b2, cp1, cp2, t_val)
        fp, okp = margin_t(w, b1, b2, cp1, cp2, t_val + h2)
        fm, okm = margin_t(w, b1, b2, cp1, cp2, t_val - h2)

        if not (ok_f and okp and okm):
            continue

        n_ratio_convex += 1
        # Test convexity of ratio R(t) = M(t)/M(0)
        R0 = f0 / M_0
        Rp = fp / M_0
        Rm = fm / M_0
        d2R = (Rp - 2*R0 + Rm) / h2**2

        if d2R < -1e-3:
            n_ratio_viol += 1

print("Ratio convexity tests: %d" % n_ratio_convex)
print("Violations: %d" % n_ratio_viol)
print("(Expected 0 if M(t)/M(0) is convex — same as M(t) convexity since M(0) > 0)")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Key test — M(t*) vs M(0) bound")
print(SEP)
print("For convex M(t) with min at t*, check M(t*)/M(0) lower bound")

random.seed(7777)
n_bound = 0
min_rel = float('inf')
worst_rel = None

for _ in range(100000):
    w = random.uniform(0.1, 0.9)
    s1 = w
    s2 = 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1 = random.uniform(-b1_max, b1_max)
    b2 = random.uniform(-b2_max, b2_max)
    cp1 = random.uniform(-0.08, 0.08)
    cp2 = random.uniform(-0.08, 0.08)

    M_0, ok0 = margin(w, b1, b2, 0, 0)
    if not ok0 or M_0 < 1e-12:
        continue

    # Find the minimum M over all valid t
    min_M = M_0
    t_vals = np.linspace(0, 5.0, 200)
    for tv in t_vals:
        M_t, ok_t = margin_t(w, b1, b2, cp1, cp2, tv)
        if not ok_t:
            break
        if M_t < min_M:
            min_M = M_t

    if min_M >= M_0 - 1e-15:
        continue  # M(t) >= M(0) everywhere, no drop

    n_bound += 1
    rel = min_M / M_0
    if rel < min_rel:
        min_rel = rel
        worst_rel = (w, b1, b2, cp1, cp2, min_M, M_0)

print("Cases where M drops below M(0): %d" % n_bound)
if n_bound > 0:
    print("Min M(t*)/M(0) ratio: %.6f" % min_rel)
    print("Worst drop: %.4f%% of M(0)" % ((1 - min_rel) * 100))
    if worst_rel:
        w, b1, b2, cp1, cp2, mmin, m0 = worst_rel
        print("Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f" % (w, b1, b2, cp1, cp2))
        print("  min M=%.6e, M(0)=%.6e" % (mmin, m0))
    print("All min M >= 0: %s" % (min_rel >= -1e-10))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("VERDICT")
print(SEP)

elapsed = time.time() - t0
print("Elapsed: %.1fs" % elapsed)
