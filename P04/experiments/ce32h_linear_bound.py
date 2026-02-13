"""
ce32h_linear_bound.py — Test P(0) + P'(0) >= 0 and combined proof chain.

If P(tau) is convex on [0,1] and P(0) >= 0:
  P(1) >= P(0) + P'(0) >= 0  iff  P(0) + P'(0) >= 0.

This is the SIMPLEST sufficient condition for closure.

Also test: M(w, b1, b2, c1', c2') >= 0 directly at large scale.

COMBINED ROUTE:
If P convex + P(0) + P'(0) >= 0: PROVED.
If P convex but P(0) + P'(0) < 0 sometimes: need tighter bound.
"""
import sys, io, time
import numpy as np
from fractions import Fraction
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def inv_phi4(sig, bv, cpv):
    av = -sig
    cv = sig**2/12.0 + cpv
    Av = av**2 + 12*cv
    Bv = 2*av**3 - 8*av*cv + 9*bv**2
    Dv = (16*av**4*cv - 4*av**3*bv**2 - 128*av**2*cv**2
          + 144*av*bv**2*cv - 27*bv**4 + 256*cv**3)
    ABv = Av*Bv
    if Dv <= 0 or ABv >= 0:
        return None
    return -Dv / (4*ABv)

def margin(w, b1, b2, cp1, cp2):
    s1 = w; s2 = 1.0 - w
    fh = inv_phi4(1.0, b1+b2, cp1+cp2)
    f1 = inv_phi4(s1, b1, cp1)
    f2 = inv_phi4(s2, b2, cp2)
    if fh is None or f1 is None or f2 is None:
        return None
    return fh - f1 - f2

def f_tilde_prime(sig_v, cp_v):
    """f~'(sigma, 0, c') = df/d(b^2)|_{b=0}."""
    av = -sig_v; cv = sig_v**2/12.0 + cp_v
    Av = av**2 + 12*cv
    B0v = 2*av**3 - 8*av*cv
    D0v = 16*av**4*cv - 128*av**2*cv**2 + 256*cv**3
    D2v = -4*av**3 + 144*av*cv
    q0 = 4*Av*B0v
    if abs(q0) < 1e-15:
        return None
    num = -D2v * q0 + D0v * 36 * Av
    return num / (q0**2)

# ============================================================
print(SEP)
print("SECTION 1: Test P(0) + P'(0) >= 0")
print("P(0) = M(w,0,0,cp1,cp2) >= 0 (proved)")
print("P'(0) = bh^2*f~'_h - b1^2*f~'_1 - b2^2*f~'_2")
print(SEP)
sys.stdout.flush()

np.random.seed(42)
n_test = 0
n_pass = 0
n_fail = 0
min_sum = float('inf')
worst = None

for trial in range(2000000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v
    cp1v = np.random.uniform(-0.1, 0.1)
    cp2v = np.random.uniform(-0.1, 0.1)
    cphv = cp1v + cp2v

    # Check validity at tau=1
    if inv_phi4(1.0, bhv, cphv) is None:
        continue
    if inv_phi4(s1, b1v, cp1v) is None:
        continue
    if inv_phi4(s2, b2v, cp2v) is None:
        continue

    # P(0) = M(w, 0, 0, cp1, cp2)
    P0 = margin(wv, 0, 0, cp1v, cp2v)
    if P0 is None:
        continue

    # P'(0) = bh^2 * f~'(1, 0, cph) - b1^2 * f~'(w, 0, cp1) - b2^2 * f~'(1-w, 0, cp2)
    ftp_h = f_tilde_prime(1.0, cphv)
    ftp_1 = f_tilde_prime(s1, cp1v)
    ftp_2 = f_tilde_prime(s2, cp2v)
    if ftp_h is None or ftp_1 is None or ftp_2 is None:
        continue

    Pp0 = bhv**2 * ftp_h - b1v**2 * ftp_1 - b2v**2 * ftp_2

    total = P0 + Pp0
    n_test += 1
    if total >= -1e-10:
        n_pass += 1
    else:
        n_fail += 1
        if total < min_sum:
            min_sum = total
            worst = (wv, b1v, b2v, cp1v, cp2v, P0, Pp0)

    if trial % 500000 == 499999:
        print("  %d trials, %d valid, %d fail, min=%.6e, elapsed %.1fs" %
              (trial+1, n_test, n_fail, min_sum if n_fail > 0 else 0, time.time()-t0))
        sys.stdout.flush()

print("\nP(0) + P'(0) >= 0 test: %d valid" % n_test)
print("  Pass: %d (%.1f%%)" % (n_pass, 100*n_pass/max(1,n_test)))
print("  Fail: %d (%.1f%%)" % (n_fail, 100*n_fail/max(1,n_test)))
if n_fail > 0:
    print("  Min P(0)+P'(0): %.6e" % min_sum)
    if worst:
        w, b1, b2, cp1, cp2, P0v, Pp0v = worst
        print("  Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.4f cp2=%.4f" % (w, b1, b2, cp1, cp2))
        print("    P(0)=%.6e  P'(0)=%.6e" % (P0v, Pp0v))
else:
    print("  ALL PASS — P(0)+P'(0) >= 0 universally!")
    print("  => With P convex, PROOF CLOSES: P(1) >= P(0)+P'(0) >= 0")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Alternative — test P(0) + P'(0) + P''(0)/2 >= 0")
print("(tighter bound from second-order Taylor)")
print(SEP)
sys.stdout.flush()

from sympy import symbols as sym_symbols, Rational as R

def C_val(sig_v, cp_v):
    """C(sigma,c') = -648*(6c'-sigma^2)*(6c'+sigma^2)"""
    return -648 * (6*cp_v - sig_v**2) * (6*cp_v + sig_v**2)

def f_tilde_pp_val(sig_v, u_v, cp_v):
    """f~''(sigma, u, c') = C(sigma,c') / [4A*(B0+9u)]^3"""
    Cv = C_val(sig_v, cp_v)
    Av = sig_v**2 + 12*cp_v  # A/2 = sigma^2 + 6c'... wait
    # A = 2*sigma^2 + 12*c' = 2*(sigma^2+6c')
    av = -sig_v; cv = sig_v**2/12 + cp_v
    Av = av**2 + 12*cv  # = sigma^2 + 12*c' + ... = 2sigma^2+12c'
    B0v = 2*av**3 - 8*av*cv
    qv = 4*Av*(B0v + 9*u_v)
    if abs(qv) < 1e-15:
        return None
    return Cv / (qv**3)

np.random.seed(123)
n_t2 = 0
n_t2_pass = 0
n_t2_fail = 0
min_t2 = float('inf')

for trial in range(2000000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.95
    b2_max = (4*s2**3/27)**0.5 * 0.95
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v
    cp1v = np.random.uniform(-0.1, 0.1)
    cp2v = np.random.uniform(-0.1, 0.1)
    cphv = cp1v + cp2v

    if inv_phi4(1.0, bhv, cphv) is None:
        continue
    if inv_phi4(s1, b1v, cp1v) is None:
        continue
    if inv_phi4(s2, b2v, cp2v) is None:
        continue

    P0 = margin(wv, 0, 0, cp1v, cp2v)
    if P0 is None:
        continue

    ftp_h = f_tilde_prime(1.0, cphv)
    ftp_1 = f_tilde_prime(s1, cp1v)
    ftp_2 = f_tilde_prime(s2, cp2v)
    if ftp_h is None or ftp_1 is None or ftp_2 is None:
        continue

    Pp0 = bhv**2 * ftp_h - b1v**2 * ftp_1 - b2v**2 * ftp_2

    # P''(0) = bh^4 * f~''_h(0) - b1^4 * f~''_1(0) - b2^4 * f~''_2(0)
    fpp_h = f_tilde_pp_val(1.0, 0, cphv)
    fpp_1 = f_tilde_pp_val(s1, 0, cp1v)
    fpp_2 = f_tilde_pp_val(s2, 0, cp2v)
    if fpp_h is None or fpp_1 is None or fpp_2 is None:
        continue

    Ppp0 = bhv**4 * fpp_h - b1v**4 * fpp_1 - b2v**4 * fpp_2

    # Second-order bound: P(1) >= P(0) + P'(0) + P''(0)/2
    # (valid when P'' >= P''(0) for all tau, which we haven't proved)
    # But if P is convex and P'' is increasing, this is a lower bound
    total2 = P0 + Pp0 + Ppp0/2

    n_t2 += 1
    if total2 >= -1e-10:
        n_t2_pass += 1
    else:
        n_t2_fail += 1
    if total2 < min_t2:
        min_t2 = total2

    if trial % 500000 == 499999:
        print("  %d trials, %d valid, %d fail, min=%.6e" %
              (trial+1, n_t2, n_t2_fail, min_t2 if min_t2 != float('inf') else 0))
        sys.stdout.flush()

print("\nP(0)+P'(0)+P''(0)/2 >= 0 test: %d valid" % n_t2)
print("  Pass: %d (%.1f%%)" % (n_t2_pass, 100*n_t2_pass/max(1,n_t2)))
print("  Fail: %d (%.1f%%)" % (n_t2_fail, 100*n_t2_fail/max(1,n_t2)))
if min_t2 != float('inf'):
    print("  Min: %.6e" % min_t2)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Does P'' increase with tau?")
print("If P''(tau) >= P''(0) for all tau >= 0, second-order bound is rigorous.")
print(SEP)
sys.stdout.flush()

np.random.seed(456)
n_inc = 0
n_inc_pass = 0
n_inc_fail = 0

for trial in range(500000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv; s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.9
    b2_max = (4*s2**3/27)**0.5 * 0.9
    b1v = np.random.uniform(-b1_max, b1_max)
    b2v = np.random.uniform(-b2_max, b2_max)
    bhv = b1v + b2v
    cp1v = np.random.uniform(-0.08, 0.08)
    cp2v = np.random.uniform(-0.08, 0.08)
    cphv = cp1v + cp2v

    # Compare P''(0) with P''(tau) for tau = 0.5 and tau = 1
    valid = True
    Ppp_vals = []
    for tau in [0, 0.25, 0.5, 0.75, 1.0]:
        if inv_phi4(1.0, tau**0.5*bhv, cphv) is None:
            valid = False; break
        if inv_phi4(s1, tau**0.5*b1v, cp1v) is None:
            valid = False; break
        if inv_phi4(s2, tau**0.5*b2v, cp2v) is None:
            valid = False; break

        fpp_h = f_tilde_pp_val(1.0, tau*bhv**2, cphv)
        fpp_1 = f_tilde_pp_val(s1, tau*b1v**2, cp1v)
        fpp_2 = f_tilde_pp_val(s2, tau*b2v**2, cp2v)
        if fpp_h is None or fpp_1 is None or fpp_2 is None:
            valid = False; break
        Ppp = bhv**4 * fpp_h - b1v**4 * fpp_1 - b2v**4 * fpp_2
        Ppp_vals.append(Ppp)
    if not valid or len(Ppp_vals) < 5:
        continue

    n_inc += 1
    # Check if P'' is increasing
    is_inc = all(Ppp_vals[i+1] >= Ppp_vals[i] - 1e-10 for i in range(4))
    if is_inc:
        n_inc_pass += 1
    else:
        n_inc_fail += 1

print("P''(tau) increasing test: %d valid" % n_inc)
print("  Increasing: %d (%.1f%%)" % (n_inc_pass, 100*n_inc_pass/max(1,n_inc)))
print("  NOT increasing: %d (%.1f%%)" % (n_inc_fail, 100*n_inc_fail/max(1,n_inc)))
sys.stdout.flush()

print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("If P(0)+P'(0) >= 0 always: PROOF CLOSES (with P convex)")
print("If P(0)+P'(0)+P''(0)/2 >= 0 AND P''(tau) increasing: PROOF CLOSES")
print("Otherwise: need full discriminant or alternative bound")
print("\nElapsed: %.1fs" % (time.time() - t0))
