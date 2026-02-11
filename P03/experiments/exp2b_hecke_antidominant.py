"""
P03 EXP-2b: Compute ASEP polynomials starting from anti-dominant composition.

Correction: E_mu = x^mu only for ANTI-DOMINANT mu (increasing parts).
For lambda = (3,2,0), the anti-dominant rearrangement is lambda^- = (0,2,3).

So E_{(0,2,3)} = x_2^2 * x_3^3

Then f_mu = T_{sigma_mu} E_{lambda^-} where sigma_mu maps lambda^- to mu.

Permutations from (0,2,3) to each mu:
(0,2,3) -> id
(0,3,2) -> s_1
(2,0,3) -> s_0
(2,3,0) -> s_1 s_0
(3,0,2) -> s_0 s_1
(3,2,0) -> s_0 s_1 s_0

Hecke: T_i f = t*f + (t-1)*x_{i+1}/(x_i - x_{i+1}) * (f - s_i f)
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, simplify, factor, Rational, Poly,
                   cancel, together, Symbol)
from itertools import permutations

print("P03 EXP-2b: ASEP polynomials from anti-dominant starting point")
print("=" * 70)

x1, x2, x3 = symbols('x1 x2 x3')
t = symbols('t')
x = [x1, x2, x3]
n = 3
lam = (3, 2, 0)
lam_minus = (0, 2, 3)  # anti-dominant

def swap_vars(f, i):
    return f.subs([(x[i], x[i+1]), (x[i+1], x[i])])

def hecke_T(f, i):
    si_f = swap_vars(f, i)
    diff = f - si_f
    divided = cancel(diff / (x[i] - x[i+1]))
    result = t * f + (t - 1) * x[i+1] * divided
    return expand(result)


# E_{(0,2,3)} = x_2^2 * x_3^3
E_antid = x2**2 * x3**3
print(f"lambda^- = {lam_minus}")
print(f"E_{{lambda^-}} = {E_antid}")

# Words: sigma maps lambda^- to mu
# Applied as T_{i_1}(T_{i_2}(...)) to E
perms = {
    (0, 2, 3): [],
    (0, 3, 2): [1],
    (2, 0, 3): [0],
    (2, 3, 0): [1, 0],
    (3, 0, 2): [0, 1],
    (3, 2, 0): [0, 1, 0],
}

# Verify words
print(f"\nVerifying:")
def apply_word(comp, word):
    mu = list(comp)
    for i in word:
        mu[i], mu[i+1] = mu[i+1], mu[i]
    return tuple(mu)

for mu, word in sorted(perms.items()):
    result = apply_word(lam_minus, word)
    print(f"  word {word}: {lam_minus} -> {result} == {mu} {'✓' if result == mu else '✗'}")


# Compute f_mu
print(f"\nComputing f_mu = T_{{word}} E_{{lambda^-}}:")
print("-" * 50)

f_polys = {}
for mu, word in sorted(perms.items()):
    f = E_antid
    for i in word:
        f = hecke_T(f, i)
    f = expand(f)
    f_polys[mu] = f
    print(f"\n  f_{mu} = {f}")


# Sum = P_lambda
P_lam = expand(sum(f_polys.values()))
print(f"\n\nP_lambda = sum of f_mu:")
print(f"  {P_lam}")

# Check symmetry
P_s0 = swap_vars(P_lam, 0)
P_s1 = swap_vars(P_lam, 1)
print(f"\n  Symmetric under s_0? {expand(P_lam - P_s0) == 0}")
print(f"  Symmetric under s_1? {expand(P_lam - P_s1) == 0}")


# Evaluate numerically
print(f"\n\nNumerical evaluation:")
print("-" * 50)

x_vals = {x1: Rational(3, 2), x2: Rational(4, 5), x3: Rational(6, 5)}
t_val = Rational(7, 10)
print(f"x = ({x_vals[x1]}, {x_vals[x2]}, {x_vals[x3]}), t = {t_val}")

f_vals = {}
for mu in sorted(f_polys.keys()):
    val = f_polys[mu].subs(x_vals).subs(t, t_val)
    f_vals[mu] = val
    print(f"  f_{mu} = {float(val):.8f}")

P_val = sum(f_vals.values())
print(f"\n  P_lambda = {float(P_val):.8f}")

print(f"\n  pi(mu):")
all_pos = True
for mu in sorted(f_vals.keys()):
    pi = f_vals[mu] / P_val
    pos = float(pi) > 0
    if not pos:
        all_pos = False
    print(f"    pi{mu} = {float(pi):.8f} {'✓' if pos else '✗ NEGATIVE'}")

print(f"\n  All positive: {all_pos}")


# Symbolic detailed balance
print(f"\n\nSymbolic detailed balance ratios:")
print("-" * 50)

for mu in sorted(f_polys.keys()):
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in f_polys and mu < nu:
            ratio = cancel(f_polys[mu] / f_polys[nu])
            ratio_f = factor(ratio)
            print(f"\n  swap pos {pos}: {mu} <-> {nu}")
            print(f"    f_{mu} / f_{nu} = {ratio_f}")

            # Check: is ratio = t * x_{pos}/x_{pos+1} or something simple?
            # For standard ASEP: if mu[pos] < mu[pos+1], ratio should involve t
            if mu[pos] < mu[pos+1]:
                print(f"    (mu[{pos}]={mu[pos]} < mu[{pos+1}]={mu[pos+1]})")
            else:
                print(f"    (mu[{pos}]={mu[pos]} > mu[{pos+1}]={mu[pos+1]})")


# ============================================================
# Try x1=x2=x3=1 (uniform): does this simplify?
# ============================================================
print(f"\n\nSpecial case: x1 = x2 = x3 = 1")
print("-" * 50)
x_unif = {x1: 1, x2: 1, x3: 1}

for mu in sorted(f_polys.keys()):
    val = f_polys[mu].subs(x_unif)
    val_simplified = simplify(val)
    print(f"  f_{mu}(1,1,1; t) = {val_simplified}")


# ============================================================
# Check if the ASEP chain satisfies detailed balance
# ============================================================
print(f"\n\nASEP chain check:")
print("-" * 50)
print("Standard multispecies ASEP on a ring:")
print("  - From state mu, swap adjacent particles mu_i, mu_{i+1}")
print("  - Rate 1 if mu_i > mu_{i+1} (particle moves right)")
print("  - Rate t if mu_i < mu_{i+1} (particle moves left)")
print()
print("Detailed balance requires:")
print("  pi(mu) * rate(mu->nu) = pi(nu) * rate(nu->mu)")
print("  i.e., f_mu * rate_forward = f_nu * rate_backward")
print()

# For each adjacent pair (mu, nu = s_i(mu)):
# If mu[i] > mu[i+1]: forward rate = 1, backward rate = t
#   DB: f_mu * 1 = f_nu * t  =>  f_mu/f_nu = t
# If mu[i] < mu[i+1]: forward rate = t, backward rate = 1
#   DB: f_mu * t = f_nu * 1  =>  f_mu/f_nu = 1/t

for mu in sorted(f_polys.keys()):
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in f_polys and mu < nu:
            ratio = cancel(f_polys[mu] / f_polys[nu])
            ratio_f = factor(ratio)

            if mu[pos] < mu[pos+1]:
                expected = Rational(1, 1) / t
                check = simplify(ratio - expected) == 0
                print(f"  {mu} <-> {nu} (pos {pos}, {mu[pos]}<{mu[pos+1]}): "
                      f"ratio = {ratio_f}, expected 1/t. Match: {check}")
            else:
                expected = t
                check = simplify(ratio - expected) == 0
                print(f"  {mu} <-> {nu} (pos {pos}, {mu[pos]}>{mu[pos+1]}): "
                      f"ratio = {ratio_f}, expected t. Match: {check}")


# ============================================================
# Alternative: check if ratio = (x_i/x_{i+1})^{some power} * t^{some power}
# ============================================================
print(f"\n\nAlternative: check ratio structure")
print("-" * 50)

# For the multispecies TASEP with SITE-DEPENDENT rates:
# Rate of swap at site i depends on x_i, x_{i+1}
# Typical: rate = 1 if particle moves right, rate = t*x_{i+1}/x_i if left
# DB ratio: f_mu/f_nu = t * x_{pos+1}/x_{pos} if mu[pos] > mu[pos+1]

for mu in sorted(f_polys.keys()):
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in f_polys and mu < nu:
            ratio = cancel(f_polys[mu] / f_polys[nu])

            # Try various simple forms
            candidates = {
                't': t,
                '1/t': 1/t,
                f't*x{pos+1}/x{pos+2}': t * x[pos] / x[pos+1],
                f'x{pos+1}/(t*x{pos+2})': x[pos] / (t * x[pos+1]),
                f'x{pos+1}/x{pos+2}': x[pos] / x[pos+1],
            }

            matches = []
            for name, cand in candidates.items():
                if simplify(ratio - cand) == 0:
                    matches.append(name)

            print(f"  {mu} <-> {nu} (pos {pos}): ratio = {factor(ratio)}")
            if matches:
                print(f"    MATCHES: {matches}")
            else:
                print(f"    No simple match found")
