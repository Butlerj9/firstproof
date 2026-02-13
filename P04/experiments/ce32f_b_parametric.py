"""
ce32f_b_parametric.py — Reverse parametric approach: scale b from 0 to full.

N(theta) = M(w, theta*b1, theta*b2, cp1, cp2)

N(0) = M(w, 0, 0, cp1, cp2) = b=0 margin, PROVED >= 0 (§9.4)
N(1) = M(w, b1, b2, cp1, cp2) = general target

If N is convex in theta: N(theta) >= min(N(0), lim_{theta->inf})
Since N(0) >= 0 and the asymptotic behavior would give N -> 0+, we'd need more.

Better: If N'(0) >= 0 AND N convex => N(theta) >= N(0) >= 0.

Also test: Is N convex (N'' >= 0)?

Since 1/Phi4 depends on b only through b^2, the scaling theta*b gives b^2 -> theta^2*b^2.
So N(theta) = f(1, theta*bh, cph) - f(w, theta*b1, cp1) - f(1-w, theta*b2, cp2)
where f depends on theta through theta^2*bi^2.

Let tau = theta^2. Then N(theta) = P(tau) where P is a function of tau = theta^2.
P'(tau) = sum_i +/- df/d(b^2) * bi^2
P(0) = N(0) >= 0 (proved)
P(1) = N(1) = target.
"""
import sys, io, time
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def inv_phi4(sig, bv, cpv):
    """Compute 1/Phi4(sigma, b, c')."""
    a = -sig
    c = sig**2/12.0 + cpv
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*bv**2
    Delta = (16*a**4*c - 4*a**3*bv**2 - 128*a**2*c**2
             + 144*a*bv**2*c - 27*bv**4 + 256*c**3)
    AB = A*B
    if Delta <= 0 or AB >= 0:
        return None
    return -Delta / (4*AB)

def margin(w, b1, b2, cp1, cp2):
    s1 = w; s2 = 1.0 - w
    fh = inv_phi4(1.0, b1+b2, cp1+cp2)
    f1 = inv_phi4(s1, b1, cp1)
    f2 = inv_phi4(s2, b2, cp2)
    if fh is None or f1 is None or f2 is None:
        return None
    return fh - f1 - f2

# ============================================================
print(SEP)
print("SECTION 1: Test N(theta) = M(w, theta*b1, theta*b2, cp1, cp2)")
print("Is N convex in theta? Is N'(0) >= 0?")
print(SEP)
sys.stdout.flush()

np.random.seed(42)
n_test = 0
n_convex = 0
n_non_convex = 0
n_nprime0_pos = 0
n_nprime0_neg = 0

eps = 1e-6

for _ in range(200000):
    wv = np.random.uniform(0.05, 0.95)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    cp1v = np.random.uniform(-0.08, 0.08)
    cp2v = np.random.uniform(-0.08, 0.08)

    # Check validity at theta=1
    M1 = margin(wv, b1v, b2v, cp1v, cp2v)
    if M1 is None:
        continue

    # Check validity at theta=0
    M0 = margin(wv, 0, 0, cp1v, cp2v)
    if M0 is None:
        continue

    # Compute N at several theta values
    thetas = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    N_vals = []
    valid = True
    for th in thetas:
        M = margin(wv, th*b1v, th*b2v, cp1v, cp2v)
        if M is None:
            valid = False
            break
        N_vals.append(M)
    if not valid:
        continue

    n_test += 1

    # Test convexity: N(t_mid) <= (N(t_left) + N(t_right))/2 for all triplets
    is_convex = True
    for i in range(len(thetas)-2):
        # Check if N(t_{i+1}) <= (N(t_i) + N(t_{i+2}))/2
        mid = N_vals[i+1]
        avg = (N_vals[i] + N_vals[i+2]) / 2
        if mid > avg + 1e-10:
            is_convex = False
            break
    if is_convex:
        n_convex += 1
    else:
        n_non_convex += 1

    # N'(0) approx using finite difference
    N_eps = margin(wv, eps*b1v, eps*b2v, cp1v, cp2v)
    if N_eps is not None:
        Nprime0 = (N_eps - N_vals[0]) / eps
        if Nprime0 >= -1e-6:
            n_nprime0_pos += 1
        else:
            n_nprime0_neg += 1

    if n_test % 20000 == 0:
        print("  %d tests: %d convex, %d non-convex, N'(0)>=0: %d/%d, elapsed %.1fs" %
              (n_test, n_convex, n_non_convex, n_nprime0_pos,
               n_nprime0_pos+n_nprime0_neg, time.time()-t0))
        sys.stdout.flush()

print("\nN(theta) convexity test: %d valid" % n_test)
print("  Convex: %d (%.1f%%)" % (n_convex, 100*n_convex/max(1,n_test)))
print("  Non-convex: %d (%.1f%%)" % (n_non_convex, 100*n_non_convex/max(1,n_test)))
print("  N'(0) >= 0: %d / %d (%.1f%%)" % (n_nprime0_pos, n_nprime0_pos+n_nprime0_neg,
      100*n_nprime0_pos/max(1,n_nprime0_pos+n_nprime0_neg)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Test N monotonicity — is N(theta) monotone increasing?")
print(SEP)
sys.stdout.flush()

np.random.seed(123)
n_mono = 0
n_mono_inc = 0
n_mono_dec = 0
n_non_mono = 0

for _ in range(200000):
    wv = np.random.uniform(0.05, 0.95)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    cp1v = np.random.uniform(-0.08, 0.08)
    cp2v = np.random.uniform(-0.08, 0.08)

    thetas = np.linspace(0, 1, 11)
    N_vals = []
    valid = True
    for th in thetas:
        M = margin(wv, th*b1v, th*b2v, cp1v, cp2v)
        if M is None:
            valid = False
            break
        N_vals.append(M)
    if not valid or len(N_vals) < 11:
        continue

    n_mono += 1

    # Check monotonicity
    is_inc = all(N_vals[i+1] >= N_vals[i] - 1e-12 for i in range(len(N_vals)-1))
    is_dec = all(N_vals[i+1] <= N_vals[i] + 1e-12 for i in range(len(N_vals)-1))

    if is_inc:
        n_mono_inc += 1
    elif is_dec:
        n_mono_dec += 1
    else:
        n_non_mono += 1

print("N(theta) monotonicity: %d valid" % n_mono)
print("  Increasing: %d (%.1f%%)" % (n_mono_inc, 100*n_mono_inc/max(1,n_mono)))
print("  Decreasing: %d (%.1f%%)" % (n_mono_dec, 100*n_mono_dec/max(1,n_mono)))
print("  Non-monotone: %d (%.1f%%)" % (n_non_mono, 100*n_non_mono/max(1,n_mono)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Alternative — P(tau) where tau = theta^2")
print("Test if P(tau) = N(sqrt(tau)) is convex in tau")
print(SEP)
sys.stdout.flush()

np.random.seed(456)
n_tau = 0
n_tau_convex = 0
n_tau_nonconvex = 0

for _ in range(200000):
    wv = np.random.uniform(0.05, 0.95)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    cp1v = np.random.uniform(-0.08, 0.08)
    cp2v = np.random.uniform(-0.08, 0.08)

    # Evaluate P at evenly spaced tau values
    taus = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    P_vals = []
    valid = True
    for tau in taus:
        th = tau**0.5
        M = margin(wv, th*b1v, th*b2v, cp1v, cp2v)
        if M is None:
            valid = False
            break
        P_vals.append(M)
    if not valid:
        continue

    n_tau += 1
    is_convex = True
    for i in range(len(taus)-2):
        mid = P_vals[i+1]
        avg = (P_vals[i] + P_vals[i+2]) / 2
        if mid > avg + 1e-10:
            is_convex = False
            break
    if is_convex:
        n_tau_convex += 1
    else:
        n_tau_nonconvex += 1

print("P(tau) convexity: %d valid" % n_tau)
print("  Convex: %d (%.1f%%)" % (n_tau_convex, 100*n_tau_convex/max(1,n_tau)))
print("  Non-convex: %d (%.1f%%)" % (n_tau_nonconvex, 100*n_tau_nonconvex/max(1,n_tau)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Bilinear parametric — M(s*b, t*c')")
print("R(s,t) = M(w, s*b1, s*b2, t*cp1, t*cp2)")
print("R(0,0) = M(w,0,0,0,0), R(0,1) = b=0 case, R(1,0) = c'=0 case")
print(SEP)
sys.stdout.flush()

np.random.seed(789)
n_bi = 0
n_bi_fail = 0
min_R = float('inf')

for _ in range(100000):
    wv = np.random.uniform(0.05, 0.95)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.85
    b2_max = (4*s2**3/27)**0.5 * 0.85
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    cp1v = np.random.uniform(-0.05, 0.05)
    cp2v = np.random.uniform(-0.05, 0.05)

    # Evaluate R on a 2D grid of (s, t)
    ss = np.linspace(0, 1, 6)
    ts = np.linspace(0, 1, 6)
    valid = True
    R_vals = np.zeros((6, 6))
    for i, sv in enumerate(ss):
        for j, tv in enumerate(ts):
            M = margin(wv, sv*b1v, sv*b2v, tv*cp1v, tv*cp2v)
            if M is None:
                valid = False
                break
            R_vals[i, j] = M
        if not valid:
            break
    if not valid:
        continue

    n_bi += 1
    min_val = R_vals.min()
    if min_val < min_R:
        min_R = min_val

    # Check if R(1,1) is the minimum
    if R_vals[-1, -1] < R_vals[0, 0] - 1e-10:
        n_bi_fail += 1

# Where is the minimum typically?
print("Bilinear test: %d valid, min R = %.6e" % (n_bi, min_R))
print("R(1,1) < R(0,0): %d" % n_bi_fail)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: KEY TEST — Is N(theta) always >= 0?")
print("(Does b-scaling preserve M >= 0, starting from proved b=0?)")
print(SEP)
sys.stdout.flush()

np.random.seed(1234)
n_key = 0
n_key_neg = 0
min_N = float('inf')

for _ in range(500000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    cp1v = np.random.uniform(-0.1, 0.1)
    cp2v = np.random.uniform(-0.1, 0.1)

    th = np.random.uniform(0, 1)
    M = margin(wv, th*b1v, th*b2v, cp1v, cp2v)
    if M is None:
        continue
    n_key += 1
    if M < -1e-10:
        n_key_neg += 1
    if M < min_N:
        min_N = M

    if n_key % 50000 == 0:
        print("  %d valid, %d neg, min=%.6e" % (n_key, n_key_neg, min_N))
        sys.stdout.flush()

print("\nN(theta) >= 0 test: %d valid" % n_key)
print("  Negative: %d" % n_key_neg)
print("  Min N: %.6e" % min_N)
sys.stdout.flush()

print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("\nIf N convex + N(0)>=0 + N'(0)>=0 → PROOF CLOSES (b-parametric)")
print("If N convex + N(0)>=0 but N'(0) can be <0 → need discriminant bound")
print("If N NOT convex → b-parametric approach fails")
print("\nElapsed: %.1fs" % (time.time() - t0))
