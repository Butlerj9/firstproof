"""
ce30b_phi_subadditivity.py — Test phi-subadditivity and M''(t) structure.

From CE-30: f''(sigma, b, 0) = h(beta)/sigma^3 where h < 0.
Define phi(sigma, b) = 1/g(sigma, b) = sigma^3/|h(beta)|.

M''(0) >= 0 follows from Titu's lemma IF phi is subadditive:
  phi(w, b1) + phi(1-w, b2) <= phi(1, b1+b2)

This script tests:
1. phi-subadditivity
2. M''(t) at general t (not just t=0)
3. Whether M'''(t) has definite sign (monotonicity of M'')
4. Whether M''(t) is itself convex in t
"""
import sys, io, time
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_inv(sigma, b, cp):
    a = -sigma
    c = sigma**2/12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    if Delta <= 0 or A*B >= 0:
        return None
    return -Delta/(4.0*A*B)

def g_func(sigma, b):
    """g(sigma, b) = -f''(sigma, b, 0) > 0 via finite differences."""
    h = 1e-6
    f0 = phi4_inv(sigma, b, 0)
    fp = phi4_inv(sigma, b, h)
    fm = phi4_inv(sigma, b, -h)
    if f0 is None or fp is None or fm is None:
        return None
    return -((fp - 2*f0 + fm) / h**2)

def phi_func(sigma, b):
    """phi = 1/g = sigma^3/|h(beta)|."""
    g = g_func(sigma, b)
    if g is None or g <= 0:
        return None
    return 1.0 / g

# ============================================================
print(SEP)
print("SECTION 1: phi-subadditivity test")
print("phi(w, b1) + phi(1-w, b2) <= phi(1, b1+b2)?")
print(SEP)
sys.stdout.flush()

np.random.seed(42)
n_sub = 0
n_sub_fail = 0
max_excess = -float('inf')
worst_sub = None

for _ in range(300000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)

    # Check sum is also valid
    bh = b1 + b2
    bh_max = (4.0/27)**0.5 * 0.95
    if abs(bh) >= bh_max:
        continue

    p1 = phi_func(s1, b1)
    p2 = phi_func(s2, b2)
    ph = phi_func(1.0, bh)

    if p1 is None or p2 is None or ph is None:
        continue

    n_sub += 1
    excess = (p1 + p2) - ph  # should be <= 0

    if excess > max_excess:
        max_excess = excess
        worst_sub = (w, b1, b2, p1, p2, ph, excess)

    if excess > 1e-10:
        n_sub_fail += 1

print("Tests: %d" % n_sub)
print("Subadditivity violations (phi1+phi2 > phi_h): %d" % n_sub_fail)
print("Max excess: %.6e" % max_excess)
if worst_sub:
    w, b1, b2, p1, p2, ph, exc = worst_sub
    print("Worst: w=%.4f b1=%.6f b2=%.6f" % (w, b1, b2))
    print("  phi1=%.6e phi2=%.6e phi_h=%.6e excess=%.6e" % (p1, p2, ph, exc))
    print("  phi1+phi2=%.6e vs phi_h=%.6e" % (p1+p2, ph))
print("SUBADDITIVE: %s" % ("YES" if n_sub_fail == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: M''(t) at general t (not just t=0)")
print(SEP)

h_fd = 1e-6
np.random.seed(123)
n_mpp = 0
n_mpp_fail = 0
min_mpp = float('inf')

for _ in range(200000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)

    t = np.random.uniform(0.0, 1.5)

    # Check validity at this t
    fh = phi4_inv(1.0, b1+b2, t*(cp1+cp2))
    f1 = phi4_inv(s1, b1, t*cp1)
    f2 = phi4_inv(s2, b2, t*cp2)

    fh_p = phi4_inv(1.0, b1+b2, (t+h_fd)*(cp1+cp2))
    fh_m = phi4_inv(1.0, b1+b2, (t-h_fd)*(cp1+cp2))
    f1_p = phi4_inv(s1, b1, (t+h_fd)*cp1)
    f1_m = phi4_inv(s1, b1, (t-h_fd)*cp1)
    f2_p = phi4_inv(s2, b2, (t+h_fd)*cp2)
    f2_m = phi4_inv(s2, b2, (t-h_fd)*cp2)

    if any(x is None for x in [fh, f1, f2, fh_p, fh_m, f1_p, f1_m, f2_p, f2_m]):
        continue

    M_t = fh - f1 - f2
    M_p = fh_p - f1_p - f2_p
    M_m = fh_m - f1_m - f2_m

    Mpp = (M_p - 2*M_t + M_m) / h_fd**2

    n_mpp += 1
    if Mpp < min_mpp:
        min_mpp = Mpp

    if Mpp < -1e-3:
        n_mpp_fail += 1

print("M''(t) tests at random t: %d" % n_mpp)
print("Violations: %d" % n_mpp_fail)
print("Min M''(t): %.6e" % min_mpp)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Is M''(t) monotone increasing in t?")
print(SEP)

np.random.seed(456)
n_mono = 0
n_increase = 0
n_decrease = 0

for _ in range(100000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)

    # Compute M'' at t=0 and t=0.5 and t=1.0
    mpp_vals = []
    valid = True
    for t_val in [0.0, 0.3, 0.6, 1.0]:
        vals = []
        for dt in [-h_fd, 0, h_fd]:
            tv = t_val + dt
            fh = phi4_inv(1.0, b1+b2, tv*(cp1+cp2))
            f1 = phi4_inv(s1, b1, tv*cp1)
            f2 = phi4_inv(s2, b2, tv*cp2)
            if fh is None or f1 is None or f2 is None:
                valid = False
                break
            vals.append(fh - f1 - f2)
        if not valid:
            break
        mpp_vals.append((vals[2] - 2*vals[1] + vals[0]) / h_fd**2)

    if not valid or len(mpp_vals) < 4:
        continue

    n_mono += 1
    increasing = all(mpp_vals[i+1] >= mpp_vals[i] - 1e-3 for i in range(3))
    decreasing = all(mpp_vals[i+1] <= mpp_vals[i] + 1e-3 for i in range(3))
    if increasing:
        n_increase += 1
    if decreasing:
        n_decrease += 1

print("Monotonicity tests: %d" % n_mono)
print("M''(t) increasing: %d (%.1f%%)" % (n_increase, 100.0*n_increase/max(1,n_mono)))
print("M''(t) decreasing: %d (%.1f%%)" % (n_decrease, 100.0*n_decrease/max(1,n_mono)))
print("Neither: %d (%.1f%%)" % (n_mono-n_increase-n_decrease+min(n_increase,n_decrease),
      100.0*(n_mono-n_increase-n_decrease+min(n_increase,n_decrease))/max(1,n_mono)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Is M''(t) convex in t?")
print(SEP)

np.random.seed(789)
n_conv_test = 0
n_conv_fail = 0
min_d4 = float('inf')

for _ in range(100000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    cp1 = np.random.uniform(-0.08, 0.08)
    cp2 = np.random.uniform(-0.08, 0.08)

    t = np.random.uniform(0.1, 0.9)

    # Compute M'' at t-h, t, t+h
    ht = 0.05
    mpp_vals = []
    valid = True
    for dt in [-ht, 0, ht]:
        tv = t + dt
        inner_vals = []
        for ddt in [-h_fd, 0, h_fd]:
            ttv = tv + ddt
            fh = phi4_inv(1.0, b1+b2, ttv*(cp1+cp2))
            f1 = phi4_inv(s1, b1, ttv*cp1)
            f2 = phi4_inv(s2, b2, ttv*cp2)
            if fh is None or f1 is None or f2 is None:
                valid = False
                break
            inner_vals.append(fh - f1 - f2)
        if not valid:
            break
        mpp_vals.append((inner_vals[2] - 2*inner_vals[1] + inner_vals[0]) / h_fd**2)

    if not valid or len(mpp_vals) < 3:
        continue

    n_conv_test += 1
    d4 = (mpp_vals[2] - 2*mpp_vals[1] + mpp_vals[0]) / ht**2  # d²(M'')/dt²

    if d4 < min_d4:
        min_d4 = d4

    if d4 < -1e-2:
        n_conv_fail += 1

print("M''''(t) tests: %d" % n_conv_test)
print("M'' concavity violations (d²M''/dt² < -0.01): %d" % n_conv_fail)
print("Min d²M''/dt²: %.6e" % min_d4)
print("M''(t) convex in t: %s" % ("YES" if n_conv_fail == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Alternative — is phi(sigma, b) CONCAVE?")
print(SEP)
print("If phi is concave, subadditivity follows from concavity + phi(0,0)=0.")

# Check concavity of phi in (sigma, b) jointly
n_conc = 0
n_conc_fail = 0
hs = 1e-4

for _ in range(100000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.9
    bv = np.random.uniform(-b_max, b_max)

    # Hessian of phi via finite differences
    p00 = phi_func(sigma, bv)
    ps_p = phi_func(sigma+hs, bv)
    ps_m = phi_func(sigma-hs, bv)
    pb_p = phi_func(sigma, bv+hs)
    pb_m = phi_func(sigma, bv-hs)
    psb_pp = phi_func(sigma+hs, bv+hs)
    psb_pm = phi_func(sigma+hs, bv-hs)
    psb_mp = phi_func(sigma-hs, bv+hs)
    psb_mm = phi_func(sigma-hs, bv-hs)

    if any(x is None for x in [p00, ps_p, ps_m, pb_p, pb_m, psb_pp, psb_pm, psb_mp, psb_mm]):
        continue

    n_conc += 1

    pss = (ps_p - 2*p00 + ps_m) / hs**2
    pbb = (pb_p - 2*p00 + pb_m) / hs**2
    psb = (psb_pp - psb_pm - psb_mp + psb_mm) / (4*hs**2)

    # NSD check: both eigenvalues <= 0
    tr = pss + pbb
    det = pss*pbb - psb**2

    if tr > 1e-3 or det < -1e-3:
        n_conc_fail += 1

print("phi Hessian NSD tests: %d" % n_conc)
print("NSD violations: %d" % n_conc_fail)
print("phi(sigma,b) jointly concave: %s" % ("YES" if n_conc_fail == 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: phi ratio analysis — phi1/phi_h and phi2/phi_h")
print(SEP)

np.random.seed(321)
n_ratio = 0
max_sum_ratio = -float('inf')
min_sum_ratio = float('inf')

for _ in range(200000):
    w = np.random.uniform(0.05, 0.95)
    s1, s2 = w, 1.0 - w
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)

    bh = b1 + b2
    bh_max = (4.0/27)**0.5 * 0.95
    if abs(bh) >= bh_max:
        continue

    p1 = phi_func(s1, b1)
    p2 = phi_func(s2, b2)
    ph = phi_func(1.0, bh)

    if p1 is None or p2 is None or ph is None or ph < 1e-20:
        continue

    n_ratio += 1
    ratio = (p1 + p2) / ph

    if ratio > max_sum_ratio:
        max_sum_ratio = ratio
    if ratio < min_sum_ratio:
        min_sum_ratio = ratio

print("Ratio tests: %d" % n_ratio)
print("Max (phi1+phi2)/phi_h: %.6f" % max_sum_ratio)
print("Min (phi1+phi2)/phi_h: %.6f" % min_sum_ratio)
print("Subadditivity iff max ratio <= 1.0")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Analytic form of phi via exact h(beta)")
print(SEP)

# h(beta) = (27beta-8)((4-27beta)^3 - 864*beta) / (-(4-27beta)^3)
# |h(beta)| = (8-27beta)((4-27beta)^3 + 864*beta) / (4-27beta)^3
# phi = sigma^3 / |h(beta)| = sigma^3 * (4-27beta)^3 / ((8-27beta)*((4-27beta)^3 + 864*beta))

# At beta=0: phi = sigma^3 * 64 / (8 * 64) = sigma^3/8

# Let u = 27*beta/4 in [0,1). Then beta = 4u/27.
# (4-27beta) = 4(1-u)
# (8-27beta) = 4(2-u)  [since 8 = 2*4]
# 864*beta = 864*4u/27 = 128u

# phi = sigma^3 * 64(1-u)^3 / (4(2-u)*(64(1-u)^3 + 128u))
#      = sigma^3 * 64(1-u)^3 / (4(2-u)*64((1-u)^3 + 2u))
#      = sigma^3 * (1-u)^3 / (4(2-u)*((1-u)^3 + 2u))

# At u=0: phi = sigma^3 / (4*2*1) = sigma^3/8  ✓

print("phi(sigma, b) = sigma^3 * (1-u)^3 / (4*(2-u)*((1-u)^3 + 2u))")
print("where u = 27*b^2/(4*sigma^3) in [0, 1)")
print()

# Verify with numerical
for sig_test in [0.5, 1.0, 2.0]:
    for b_test in [0, 0.05, 0.1]:
        p_num = phi_func(sig_test, b_test)
        if p_num is None:
            continue
        beta_test = b_test**2 / sig_test**3
        u_test = 27*beta_test/4
        if u_test >= 1:
            continue
        p_formula = sig_test**3 * (1-u_test)**3 / (4*(2-u_test)*((1-u_test)**3 + 2*u_test))
        err = abs(p_num - p_formula) / (abs(p_num) + 1e-20)
        print("  sig=%.1f b=%.2f: phi_num=%.6e, phi_formula=%.6e, err=%.2e" %
              (sig_test, b_test, p_num, p_formula, err))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 8: Subadditivity in u-coordinates")
print(SEP)
print("phi(sigma, b) = sigma^3 * F(u) where F(u) = (1-u)^3 / (4*(2-u)*((1-u)^3+2u))")
print("u = 27b^2/(4*sigma^3)")
print()

# Under free convolution: sigma_h = sigma_1 + sigma_2, b_h = b_1 + b_2
# u_h = 27*(b1+b2)^2 / (4*(sigma_1+sigma_2)^3)
# u_i = 27*bi^2 / (4*sigma_i^3)

# Subadditivity condition: sigma_1^3*F(u_1) + sigma_2^3*F(u_2) <= (sigma_1+sigma_2)^3*F(u_h)

# Normalized: let w = sigma_1/(sigma_1+sigma_2), so sigma_1 = w, sigma_2 = 1-w
# w^3*F(u_1) + (1-w)^3*F(u_2) <= F(u_h)

print("Normalized condition: w^3*F(u1) + (1-w)^3*F(u2) <= F(u_h)")
print("where u_h = 27*(b1+b2)^2/4, u1 = 27*b1^2/(4*w^3), u2 = 27*b2^2/(4*(1-w)^3)")
print()

# Compute F and check properties
def F_func(u):
    if u >= 1 or u < 0:
        return None
    return (1-u)**3 / (4*(2-u)*((1-u)**3 + 2*u))

# F'(u) via finite differences
h_u = 1e-7
us = np.linspace(0.001, 0.95, 200)
Fs = [F_func(u) for u in us]
Fs_valid = [(u, F) for u, F in zip(us, Fs) if F is not None]

print("F(u) profile:")
for u_val in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
    F = F_func(u_val)
    print("  F(%.1f) = %.6f" % (u_val, F if F else float('nan')))

# Check if F is concave
print("\nF(u) concavity check:")
n_F_conv = 0
for u_val in np.linspace(0.01, 0.95, 100):
    F0 = F_func(u_val)
    Fp = F_func(u_val + h_u)
    Fm = F_func(u_val - h_u)
    if F0 is None or Fp is None or Fm is None:
        continue
    d2F = (Fp - 2*F0 + Fm) / h_u**2
    if d2F > 1e-3:
        n_F_conv += 1
print("F(u) convex intervals: %d / 100" % n_F_conv)
print("F is concave: %s" % ("YES" if n_F_conv == 0 else "NO"))

# Check if F is decreasing
print("\nF(u) monotonicity:")
n_F_inc = 0
for u_val in np.linspace(0.01, 0.95, 100):
    Fp = F_func(u_val + h_u)
    Fm = F_func(u_val - h_u)
    if Fp is None or Fm is None:
        continue
    dF = (Fp - Fm) / (2*h_u)
    if dF > 1e-3:
        n_F_inc += 1
print("F(u) increasing intervals: %d / 100" % n_F_inc)
print("F is decreasing: %s" % ("YES" if n_F_inc == 0 else "NO"))
sys.stdout.flush()

print("\nElapsed: %.1fs" % (time.time() - t0))
