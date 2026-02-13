"""
ce32g_tau_convexity.py — Prove P(tau) = N(sqrt(tau)) is convex.

KEY STRUCTURAL INSIGHT from ce32f:
- N(theta) = M(w, theta*b1, theta*b2, cp1, cp2) (b-scaling from proved b=0 case)
- Since 1/Phi4 depends on b only through b^2, N(theta) = P(theta^2) where P is a fn of tau = b^2 scaling.
- P(tau) IS convex (100% of 5030 tests) even though N(theta) is NOT convex.
- P(0) = M(w, 0, 0, cp1, cp2) >= 0 (proved b=0 case)

Algebraic structure:
- f~(u) = 1/Phi4(sigma, sqrt(u), c') = (27u^2 - Delta_2*u - Delta_0) / (4A(B_0 + 9u))
  where u = b^2, A = 2sigma^2 + 12c', B_0 + 9u = B.
- f~''(u) = C(sigma,c') / [4A(B_0+9u)]^3
  where C is INDEPENDENT of u (constant numerator!).
- This is because (quadratic)/(linear) has degree-0 second derivative numerator.

This script:
1. Computes and verifies C(sigma, c') symbolically
2. Tests sign of C on valid domain
3. Verifies P''(tau) >= 0 condition with large-scale exact tests
4. Attempts to prove P convex from the structure C/q^3
"""
import sys, io, time
from sympy import (symbols, diff, simplify, factor, cancel, expand,
                   numer, denom, Rational, Poly, together, apart, collect)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

# ============================================================
print(SEP)
print("SECTION 1: Compute f~''(u) where u = b^2")
print(SEP)
sys.stdout.flush()

sigma, u, cp = symbols('sigma u cp', real=True)

a = -sigma
c = sigma**2 / 12 + cp

A = a**2 + 12*c   # = 2*sigma^2 + 12*cp
B0 = 2*a**3 - 8*a*c  # B at b=0

# 1/Phi4 as function of u = b^2:
# Numerator: -Delta = -(Delta_0 + Delta_2*u - 27*u^2) = 27u^2 - Delta_2*u - Delta_0
# where Delta_0 = Delta|_{b=0}, Delta_2 = d(Delta)/d(b^2)|_{b=0}

# Full Delta:
b = symbols('b', real=True)
Delta_full = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
              + 144*a*b**2*c - 27*b**4 + 256*c**3)

# Delta as polynomial in b^2:
Delta_0 = expand(Delta_full.subs(b, 0))
# Coefficient of b^2:
Delta_2_coeff = expand(diff(Delta_full, b, 2).subs(b, 0) / 2)  # d(Delta)/d(b^2)
# This is (-4a^3 + 144ac)/1 ... wait
# Delta = Delta_0 + Delta_2*b^2 - 27*b^4
# So Delta_2 = coefficient of b^2 in Delta = -4a^3 + 144ac

Delta_2 = expand(-4*a**3 + 144*a*c)

print("Delta_0 =", factor(Delta_0))
print("Delta_2 =", factor(Delta_2))
print("B_0 =", factor(B0))
print("A =", factor(A))

# Verify: Delta = Delta_0 + Delta_2*b^2 - 27*b^4
Delta_check = expand(Delta_0 + Delta_2*b**2 - 27*b**4 - Delta_full)
print("\nDelta decomposition check:", Delta_check)
sys.stdout.flush()

# f~(u) = (27u^2 - Delta_2*u - Delta_0) / (4A*(B0 + 9u))
# = p(u) / q(u)
# p(u) = 27u^2 - Delta_2*u - Delta_0
# q(u) = 4A*(B0 + 9u)
# p'' = 54
# q' = 36A
# q'' = 0

# f~'' = [p''q^2 - 2(p'q - pq')q'] / q^3
# Using the formula:  f~'' = (p''q - 2q'f~')/q ... hmm
# Better: f~'' = d/du[(p'q - pq')/q^2]

# Let's compute directly:
p = 27*u**2 - Delta_2*u - Delta_0
q = 4*A*(B0 + 9*u)

f_tilde = p / q
f_tilde_prime = diff(f_tilde, u)
f_tilde_pp = diff(f_tilde, u, 2)
f_tilde_pp_canc = cancel(f_tilde_pp)

num_fpp = numer(f_tilde_pp_canc)
den_fpp = denom(f_tilde_pp_canc)

print("\n--- f~''(u) ---")
print("f~''(u) = Num / Den")
num_fpp_fac = factor(num_fpp)
den_fpp_fac = factor(den_fpp)
print("Num factored:", num_fpp_fac)
print("Den factored:", den_fpp_fac)
sys.stdout.flush()

# KEY TEST: Is Num independent of u?
num_as_poly_u = Poly(expand(num_fpp), u)
print("\nDegree of Num in u:", num_as_poly_u.degree())
if num_as_poly_u.degree() == 0:
    print("CONFIRMED: Numerator is INDEPENDENT of u (= b^2)")
    C = num_as_poly_u.all_coeffs()[0]
    C_fac = factor(C)
    print("C(sigma, c') =", C_fac)
else:
    print("Numerator DEPENDS on u — structural insight was wrong!")
    C = None
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Analyze C(sigma, c') — sign on valid domain")
print(SEP)
sys.stdout.flush()

if C is not None:
    # At c'=0:
    C_at_0 = C.subs(cp, 0)
    C_at_0_fac = factor(C_at_0)
    print("C(sigma, 0) =", C_at_0_fac)

    # As polynomial in c':
    C_poly_cp = Poly(expand(C), cp)
    print("\nC as polynomial in c':")
    print("  Degree:", C_poly_cp.degree())
    for i, coeff in enumerate(C_poly_cp.all_coeffs()):
        coeff_fac = factor(coeff)
        print("  c'^%d: %s" % (C_poly_cp.degree() - i, coeff_fac))

    # At c' = -sigma^2/6 (lower boundary of A>0 region, A=0):
    C_at_neg = expand(C.subs(cp, -sigma**2/6))
    print("\nC(sigma, -sigma^2/6) =", factor(C_at_neg), " (A=0 boundary)")

    # Numerical sign test
    import numpy as np
    np.random.seed(42)
    n_pos = 0
    n_neg = 0
    n_check = 0
    for _ in range(100000):
        sig_v = np.random.uniform(0.1, 5.0)
        cp_v = np.random.uniform(-sig_v**2/6 + 0.01, sig_v**2/3)
        # Check A > 0: 2*sig^2 + 12*cp > 0 => cp > -sig^2/6
        if 2*sig_v**2 + 12*cp_v <= 0:
            continue
        C_val = float(C.subs([(sigma, sig_v), (cp, cp_v)]))
        n_check += 1
        if C_val > 0:
            n_pos += 1
        elif C_val < 0:
            n_neg += 1

    print("\nC sign check: %d tests" % n_check)
    print("  Positive: %d (%.1f%%)" % (n_pos, 100*n_pos/max(1,n_check)))
    print("  Negative: %d (%.1f%%)" % (n_neg, 100*n_neg/max(1,n_check)))
    sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Verify P''(tau) >= 0 condition")
print("P''(tau) = bh^4 * f~''_h - b1^4 * f~''_1 - b2^4 * f~''_2")
print(SEP)
sys.stdout.flush()

import numpy as np

def phi4_inv(sig, bv, cpv):
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

def f_tilde_pp_val(sig_v, u_v, cp_v):
    """Compute f~''(u) = C / q^3 numerically."""
    av = -sig_v
    cv = sig_v**2/12.0 + cp_v
    Av = av**2 + 12*cv
    B0v = 2*av**3 - 8*av*cv
    qv = 4*Av*(B0v + 9*u_v)
    if abs(qv) < 1e-15:
        return None
    # C value (from symbolic computation — to be filled after Section 1)
    Cv = float(C.subs([(sigma, sig_v), (cp, cp_v)]))
    return Cv / (qv**3)

# Large-scale P''(tau) >= 0 test
np.random.seed(42)
n_ppp = 0
n_ppp_neg = 0
min_ppp = float('inf')

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

    tau = np.random.uniform(0, 1)

    # Check validity at this tau
    if phi4_inv(1.0, (tau**0.5)*bhv, cphv) is None:
        continue
    if phi4_inv(s1, (tau**0.5)*b1v, cp1v) is None:
        continue
    if phi4_inv(s2, (tau**0.5)*b2v, cp2v) is None:
        continue

    # Compute f~'' at each component
    # u_i(tau) = tau * b_i^2
    fpp_h = f_tilde_pp_val(1.0, tau*bhv**2, cphv)
    fpp_1 = f_tilde_pp_val(s1, tau*b1v**2, cp1v)
    fpp_2 = f_tilde_pp_val(s2, tau*b2v**2, cp2v)

    if fpp_h is None or fpp_1 is None or fpp_2 is None:
        continue

    # P''(tau) = bh^4 * fpp_h - b1^4 * fpp_1 - b2^4 * fpp_2
    Ppp = bhv**4 * fpp_h - b1v**4 * fpp_1 - b2v**4 * fpp_2
    n_ppp += 1
    if Ppp < -1e-10:
        n_ppp_neg += 1
    if Ppp < min_ppp:
        min_ppp = Ppp

    if trial % 100000 == 99999:
        print("  %d trials, %d valid, %d neg, min=%.6e, elapsed %.1fs" %
              (trial+1, n_ppp, n_ppp_neg, min_ppp, time.time()-t0))
        sys.stdout.flush()

print("\nP''(tau) >= 0 test: %d valid" % n_ppp)
print("  Negative: %d" % n_ppp_neg)
print("  Min P'': %.6e" % min_ppp)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: P'(0) sign and discriminant bound test")
print(SEP)
sys.stdout.flush()

# P'(0) = N''(0)/2 where N''(0) = bh^2 * f~''(sigma_h, 0, c'_h) - ...
# f~''(sigma, 0, c') = C(sigma,c') / [4A*B_0]^3

np.random.seed(123)
n_pprime = 0
n_pprime_neg = 0
n_disc_pass = 0
n_disc_fail = 0

for _ in range(200000):
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

    # Check validity at tau=1
    if phi4_inv(1.0, bhv, cphv) is None:
        continue
    if phi4_inv(s1, b1v, cp1v) is None:
        continue
    if phi4_inv(s2, b2v, cp2v) is None:
        continue

    # P'(0) = bh^2 * f~'(1,0,cph) - b1^2 * f~'(w,0,cp1) - b2^2 * f~'(1-w,0,cp2)
    # f~'(sigma, 0, c') = [p'(0)*q(0) - p(0)*q'(0)] / q(0)^2
    # p(0) = -Delta_0, p'(0) = -Delta_2
    # q(0) = 4A*B_0, q'(0) = 36A

    def f_tilde_prime_at_0(sig_v, cp_v):
        av = -sig_v; cv = sig_v**2/12 + cp_v
        Av = av**2 + 12*cv
        B0v = 2*av**3 - 8*av*cv
        D0v = 16*av**4*cv - 128*av**2*cv**2 + 256*cv**3  # Delta_0
        D2v = -4*av**3 + 144*av*cv  # Delta_2
        q0 = 4*Av*B0v
        if abs(q0) < 1e-15:
            return None
        # p(0) = -D0v = -(Delta_0), p'(0) = -D2v
        # f~'(0) = ((-D2v)*q0 - (-D0v)*36*Av) / q0^2
        # = (-D2v*4*Av*B0v + D0v*36*Av) / (4*Av*B0v)^2
        num = -D2v * q0 + D0v * 36 * Av
        return num / (q0**2)

    fp_h = f_tilde_prime_at_0(1.0, cphv)
    fp_1 = f_tilde_prime_at_0(s1, cp1v)
    fp_2 = f_tilde_prime_at_0(s2, cp2v)

    if fp_h is None or fp_1 is None or fp_2 is None:
        continue

    Pprime0 = bhv**2 * fp_h - b1v**2 * fp_1 - b2v**2 * fp_2
    n_pprime += 1
    if Pprime0 < -1e-10:
        n_pprime_neg += 1

    # Discriminant bound: 2*P''_min*P(0) >= P'(0)^2
    # For now just count sign
    P0 = phi4_inv(1.0, 0, cphv)
    P0_1 = phi4_inv(s1, 0, cp1v)
    P0_2 = phi4_inv(s2, 0, cp2v)
    if P0 is None or P0_1 is None or P0_2 is None:
        continue
    M0 = P0 - P0_1 - P0_2  # = M at b=0 = P(0)

    if M0 >= 0:
        # Compute P''(0) = bh^4*f~''(1,0,cph) - ...
        fpp_h0 = f_tilde_pp_val(1.0, 0, cphv)
        fpp_10 = f_tilde_pp_val(s1, 0, cp1v)
        fpp_20 = f_tilde_pp_val(s2, 0, cp2v)
        if fpp_h0 is not None and fpp_10 is not None and fpp_20 is not None:
            Ppp0 = bhv**4*fpp_h0 - b1v**4*fpp_10 - b2v**4*fpp_20
            if Ppp0 > 0:  # convex at tau=0
                disc = Pprime0**2 - 2*Ppp0*M0
                if disc <= 1e-10:
                    n_disc_pass += 1
                else:
                    n_disc_fail += 1

print("P'(0) sign: %d tests" % n_pprime)
print("  P'(0) >= 0: %d (%.1f%%)" % (n_pprime-n_pprime_neg, 100*(n_pprime-n_pprime_neg)/max(1,n_pprime)))
print("  P'(0) < 0: %d (%.1f%%)" % (n_pprime_neg, 100*n_pprime_neg/max(1,n_pprime)))
print("\nDiscriminant bound 2*P''(0)*P(0) >= P'(0)^2:")
print("  Pass: %d, Fail: %d" % (n_disc_pass, n_disc_fail))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Scale-invariant form of C")
print(SEP)
sys.stdout.flush()

if C is not None:
    # Substitute c' = gamma * sigma^2 for scale-invariant analysis
    gamma = symbols('gamma', real=True)
    C_sub = C.subs(cp, gamma*sigma**2)
    C_sub = cancel(C_sub)
    # Factor out sigma powers
    C_sub_exp = expand(C_sub)
    print("C(sigma, gamma*sigma^2) =", factor(C_sub_exp))

    # Check sigma power
    C_poly_sigma = Poly(C_sub_exp, sigma)
    print("Degree in sigma:", C_poly_sigma.degree())

    # Extract the gamma-dependent part
    # Expected form: sigma^k * H(gamma)
    print("\nC as polynomial in gamma (after dividing by sigma^k):")
    k = C_poly_sigma.degree()
    H_gamma = cancel(C_sub_exp / sigma**k)
    if H_gamma.has(sigma):
        print("  Still depends on sigma — not pure scale-invariant")
        print("  H =", factor(H_gamma))
    else:
        print("  H(gamma) =", factor(H_gamma))
        # Sign of H on valid domain gamma > -1/6
        print("\n  H(-1/6) =", H_gamma.subs(gamma, Rational(-1,6)))
        print("  H(0) =", H_gamma.subs(gamma, 0))
        print("  H(1/6) =", H_gamma.subs(gamma, Rational(1,6)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Structure of f~'' and the superadditivity condition")
print(SEP)
sys.stdout.flush()

if C is not None:
    # f~''(sigma, u, c') = C(sigma,c') / [4A*(B0+9u)]^3
    # On valid domain: AB < 0 with A > 0, so B < 0, so 4AB < 0, so q^3 < 0.
    # sign(f~'') = sign(C) / sign(q^3) = sign(C) * (-1)
    # So if C > 0: f~'' < 0 (concave in u)
    # If C < 0: f~'' > 0 (convex in u)

    print("Summary of f~'' structure:")
    print("  f~''(sigma, u, c') = C(sigma,c') / [4A(B_0+9u)]^3")
    print("  C is INDEPENDENT of u = b^2")
    print("  q = 4A(B_0+9u) < 0 on valid domain (AB < 0, A > 0)")
    print("  q^3 < 0")
    print()
    print("P''(tau) = sum_i eps_i * b_i^4 * C_i / q_i(tau)^3")
    print("  where q_i(tau) = 4*A_i*(B_0_i + 9*tau*b_i^2)")
    print("  eps_h = +1, eps_1 = eps_2 = -1")
    print()

    # The key is: does the structure C/q^3 with q = 4A(B0+9*tau*b^2) enable a proof?
    # Since q_i depends on tau linearly through b_i^2, and we're taking q^{-3},
    # the tau dependence is (linear)^{-3}.

    # At tau = 0:
    # P''(0) = bh^4 * C_h / (4A_h*B_0h)^3 - b1^4 * C1 / (4A1*B_01)^3 - b2^4 * C2 / (4A2*B_02)^3
    # This involves C_i and (4A_i*B_0i)^3 at b=0.

    print("At tau=0: B_i = B_0_i (independent of b)")
    print("  The condition becomes algebraic in (sigma_i, c'_i, b_i)")
    print("  with the key advantage that C_i depends only on (sigma_i, c'_i)")

print("\nElapsed: %.1fs" % (time.time() - t0))
