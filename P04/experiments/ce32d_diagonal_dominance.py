"""
ce32d_diagonal_dominance.py — Prove diagonal dominance g(w,b1,0) >= g(1,bh,0).

New finding from CE-32c: |f''(sigma_i, b_i, c_i')| >= |f''(sigma_h, b_h, c_h')| universally.

At c'=0: g(sigma, b, 0) = |h(beta)|/sigma^3 = -h(beta)/sigma^3
where h(beta) = (531441*beta^4 - 393660*beta^3 + 81648*beta^2 - 5184*beta + 512)
                / (19683*beta^3 - 8748*beta^2 + 1296*beta - 64)
and beta = b^2/sigma^3 in [0, 4/27).

Condition: g(w, b1, 0) >= g(1, b1+b2, 0)
i.e., |h(beta_1)|/w^3 >= |h(beta_h)|
where beta_1 = b1^2/w^3, beta_h = (b1+b2)^2.

Strategy: Express g1/gh - 1 as a rational function and show >= 0.
"""
import sys, io, time
from sympy import (symbols, diff, simplify, factor, cancel, expand,
                   numer, denom, Rational, Poly, collect, sqrt,
                   solve, together, apart)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

# ============================================================
print(SEP)
print("SECTION 1: Scale-invariant g function and diagonal dominance")
print(SEP)

# g(sigma, b, 0) = |h(beta)|/sigma^3 where h < 0
# h(beta) = N(beta)/D(beta) where:
# N(beta) = 531441*beta^4 - 393660*beta^3 + 81648*beta^2 - 5184*beta + 512
# D(beta) = 19683*beta^3 - 8748*beta^2 + 1296*beta - 64
# Note D(0) = -64 < 0, and D is negative on [0, 4/27).

# g(sigma, b, 0) = -h(beta)/sigma^3 = -N(beta)/(D(beta)*sigma^3)
# Since N > 0 and D < 0 on [0, 4/27), g = N/(|D|*sigma^3) > 0.

# Test: What is g(sigma, b, 0) in terms of original variables?
# beta = b^2/sigma^3, so:
# g = -h(b^2/sigma^3) / sigma^3

# For diagonal dominance at c'=0:
# g(w, b1, 0) >= g(1, bh, 0) where bh = b1+b2
# <=> -h(b1^2/w^3)/w^3 >= -h((b1+b2)^2)
# <=> |h(b1^2/w^3)|/w^3 >= |h((b1+b2)^2)|

# Since h = N/D with D < 0, |h| = N/|D| = -N/D.
# So condition is: N(b1^2/w^3) / (w^3 * |D(b1^2/w^3)|) >= N(bh^2) / |D(bh^2)|

# Define G(beta) = N(beta)/|D(beta)| = -N(beta)/D(beta)
# Condition: G(b1^2/w^3) / w^3 >= G(bh^2)

# Let's verify G is indeed increasing (making larger beta give larger |h|)
beta = symbols('beta', nonneg=True)
N_beta = 531441*beta**4 - 393660*beta**3 + 81648*beta**2 - 5184*beta + 512
D_beta = 19683*beta**3 - 8748*beta**2 + 1296*beta - 64

G = -N_beta / D_beta  # = N/|D| since D < 0

print("G(beta) = N(beta)/|D(beta)| = -N/D =", cancel(G))

G_prime = diff(G, beta)
G_prime_canc = cancel(G_prime)
G_prime_num = numer(G_prime_canc)
G_prime_den = denom(G_prime_canc)

print("\nG'(beta) numerator:", factor(G_prime_num))
print("G'(beta) denominator:", factor(G_prime_den))

# Check sign of G' on [0, 4/27)
# D^2 > 0 (denominator of G' after quotient rule), so sign = sign of numerator
print("\nG'(beta) numerator at beta=0:", G_prime_num.subs(beta, 0))
print("G'(beta) numerator at beta=4/27:", G_prime_num.subs(beta, Rational(4, 27)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Concrete test — is G(beta)/sigma^3 monotone in sigma?")
print(SEP)

# g(sigma, b, 0) = G(b^2/sigma^3) / sigma^3
# Fix b and vary sigma. How does g depend on sigma?
# beta = b^2/sigma^3, so as sigma decreases, beta increases.
# If G is increasing, then G(beta) increases as sigma decreases.
# And 1/sigma^3 also increases as sigma decreases.
# So g is increasing as sigma decreases.
# This means g(w, b1, 0) >= g(1, b1, 0) for w <= 1 when b2=0.

# But with b2 != 0, we compare g(w, b1, 0) with g(1, b1+b2, 0)
# which involves different beta values.

# Let's try a specific parametrization. Set b1 = s*w^{3/2} and b2 = t*(1-w)^{3/2}.
# Then beta_1 = s^2*w^3/w^3 = s^2, and beta_h = (s*w^{3/2}+t*(1-w)^{3/2})^2.

w, s, t = symbols('w s t', real=True, positive=True)

beta_1 = s**2
bh = s*w**Rational(3,2) + t*(1-w)**Rational(3,2)
beta_h = bh**2

# Condition: G(s^2)/w^3 >= G(bh^2)
# G(s^2) = (-N(s^2)/D(s^2))
# G(bh^2) = (-N(bh^2)/D(bh^2))

print("This is getting complex. Let me try a simpler case first.")
print()

# ============================================================
print(SEP)
print("SECTION 3: Simplest case — b2 = 0")
print(SEP)

# With b2 = 0: bh = b1, beta_h = b1^2, beta_1 = b1^2/w^3
# Condition: G(b1^2/w^3)/w^3 >= G(b1^2)

# Define u = b1^2 (fixed). Then beta_1 = u/w^3, beta_h = u.
# Need: G(u/w^3)/w^3 >= G(u).
# Since w <= 1, u/w^3 >= u, and if G is increasing:
# G(u/w^3) >= G(u), so G(u/w^3)/w^3 >= G(u)/w^3 >= G(u) since w <= 1.
# PROVED for b2=0! ✓

print("Case b2=0: G(u/w^3)/w^3 >= G(u)")
print("  Since w <= 1: u/w^3 >= u")
print("  G is increasing (if proved) => G(u/w^3) >= G(u)")
print("  1/w^3 >= 1 => G(u/w^3)/w^3 >= G(u)/w^3 >= G(u)")
print("  PROVED for b2=0! ✓")
print()

# So we need G increasing. Let's prove this.
# ============================================================
print(SEP)
print("SECTION 4: Prove G(beta) is strictly increasing on [0, 4/27)")
print(SEP)

# G'(beta) = d/dbeta[-N(beta)/D(beta)]
# = -(N'*D - N*D')/(D^2)
# Sign of G' = sign of -(N'D - ND') since D^2 > 0.

Np = diff(N_beta, beta)
Dp = diff(D_beta, beta)

numerator_Gprime = -(Np * D_beta - N_beta * Dp)
numerator_Gprime_exp = expand(numerator_Gprime)
print("G'(beta) numerator (expanded):", numerator_Gprime_exp)
print("Number of terms:", len(numerator_Gprime_exp.as_ordered_terms()))

# Try to factor
numerator_Gprime_fac = factor(numerator_Gprime_exp)
print("G'(beta) numerator (factored):", numerator_Gprime_fac)
sys.stdout.flush()

# Check at boundaries
print("\nG'(0) numerator:", numerator_Gprime_exp.subs(beta, 0))
print("G'(4/27) numerator:", expand(numerator_Gprime_exp.subs(beta, Rational(4, 27))))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Prove G(beta) is convex on [0, 4/27)")
print(SEP)

G_pp = diff(G, beta, 2)
G_pp_canc = cancel(G_pp)
G_pp_num = numer(G_pp_canc)
G_pp_den = denom(G_pp_canc)

print("G''(beta) numerator:", factor(G_pp_num))
print("G''(beta) denominator:", factor(G_pp_den))

# Check sign at boundaries
print("\nG''(0) numerator:", G_pp_num.subs(beta, 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Full diagonal dominance — general b2")
print(SEP)

# Need: G(b1^2/w^3)/w^3 >= G((b1+b2)^2)
# Let u = b1^2/w^3 (beta_1), v = (b1+b2)^2 (beta_h).
# Domain: u in [0, 4/27), v in [0, 4/27), w in (0, 1).
# Relationship: w^3*u = b1^2, v = (b1+b2)^2.

# The condition is: G(u)/w^3 >= G(v).

# If G is increasing AND v <= u (which happens when b2 decreases |b1+b2|):
# G(u) >= G(v), so G(u)/w^3 >= G(v)/w^3 >= G(v). ✓

# If v > u (b2 amplifies the sum): need G(u)/w^3 >= G(v).
# Since G is convex and increasing: G(v) <= G(u) + G'(u)(v-u).
# And G(u)/w^3 >= G(u) (since w <= 1).
# So we need G(u)(1/w^3 - 1) >= G'(u)(v-u).
# This requires bounding v-u in terms of w.

# v - u = (b1+b2)^2 - b1^2/w^3.
# Hmm, this can be positive or negative.

# Let's think about the maximum of v for given u, w:
# b1 = ±(u*w^3)^{1/2}, b2 is free (subject to validity of q).
# b2 max: 27*b2^2/(4*(1-w)^3) < 1, i.e., |b2| < (4*(1-w)^3/27)^{1/2}
# v = (b1+b2)^2 can be as large as (|b1|+|b2|)^2 <= ((uw^3)^{1/2} + (4(1-w)^3/27)^{1/2})^2

# The maximum v occurs when b1, b2 have the same sign and are at their max.
# In this case, v can be close to 4/27 (the validity bound for the sum).

# This analysis shows that diagonal dominance at general b2 requires
# a more careful argument. Let me test numerically whether the condition
# G(u)/w^3 >= G(v) can be tight.

import numpy as np

np.random.seed(42)
n_dd = 0
min_ratio_dd = float('inf')

for _ in range(500000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv
    s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.99
    b2_max = (4*s2**3/27)**0.5 * 0.99
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    # Check validity
    if 27*bh**2 >= 4*0.99:
        continue

    u = b1**2 / s1**3
    v = bh**2

    if u >= 4/27*0.99 or v >= 4/27*0.99:
        continue

    # Compute G
    def G_val(beta_val):
        N_val = 531441*beta_val**4 - 393660*beta_val**3 + 81648*beta_val**2 - 5184*beta_val + 512
        D_val = 19683*beta_val**3 - 8748*beta_val**2 + 1296*beta_val - 64
        if D_val >= 0:
            return None
        return -N_val/D_val

    G1 = G_val(u)
    Gh = G_val(v)
    if G1 is None or Gh is None:
        continue
    if G1 <= 0 or Gh <= 0:
        continue

    n_dd += 1
    ratio = G1 / (wv**3 * Gh)
    if ratio < min_ratio_dd:
        min_ratio_dd = ratio

print("Diagonal dominance (c'=0) tests: %d" % n_dd)
print("Min G(beta_1)/(w^3*G(beta_h)): %.6f" % min_ratio_dd)
print("Diagonal dominance holds: %s" % ("YES" if min_ratio_dd >= 1.0 - 1e-6 else "NO"))
sys.stdout.flush()

# Similarly for g2 >= gh:
np.random.seed(123)
n_dd2 = 0
min_ratio_dd2 = float('inf')

for _ in range(500000):
    wv = np.random.uniform(0.02, 0.98)
    s1 = wv
    s2 = 1.0 - wv
    b1_max = (4*s1**3/27)**0.5 * 0.99
    b2_max = (4*s2**3/27)**0.5 * 0.99
    b1 = np.random.uniform(-b1_max, b1_max)
    b2 = np.random.uniform(-b2_max, b2_max)
    bh = b1 + b2

    if 27*bh**2 >= 4*0.99:
        continue

    u2 = b2**2 / s2**3
    v = bh**2

    if u2 >= 4/27*0.99 or v >= 4/27*0.99:
        continue

    G2 = G_val(u2)
    Gh = G_val(v)
    if G2 is None or Gh is None:
        continue
    if G2 <= 0 or Gh <= 0:
        continue

    n_dd2 += 1
    ratio2 = G2 / (s2**3 * Gh)
    if ratio2 < min_ratio_dd2:
        min_ratio_dd2 = ratio2

print("\ng2 >= gh tests: %d" % n_dd2)
print("Min G(beta_2)/((1-w)^3*G(beta_h)): %.6f" % min_ratio_dd2)
print("g2 >= gh holds: %s" % ("YES" if min_ratio_dd2 >= 1.0 - 1e-6 else "NO"))
sys.stdout.flush()

print("\nElapsed: %.1fs" % (time.time() - t0))
