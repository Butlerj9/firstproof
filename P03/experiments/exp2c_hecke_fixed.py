"""
P03 EXP-2c: ASEP polynomials via Hecke operators (FIXED convention).

Correct Hecke operator (Convention B):
  T_i f = t * s_i(f) + (t-1) * x_i/(x_i - x_{i+1}) * (f - s_i f)

Verification:
  T_i(x_{i+1}) = t * x_i + (t-1)*x_i*(-1) = x_i  ✓ (at t=1: s_i(x_{i+1}) = x_i)
  T_i(x_i) = t * x_{i+1} + (t-1)*x_i  ✓

Starting from anti-dominant E_{(0,2,3)} = x_2^2 * x_3^3.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, simplify, factor, Rational, Poly,
                   cancel, together)

print("P03 EXP-2c: ASEP polynomials (fixed Hecke convention)")
print("=" * 70)

x1, x2, x3 = symbols('x1 x2 x3')
t = symbols('t')
x = [x1, x2, x3]
n = 3
lam_minus = (0, 2, 3)


def swap_vars(f, i):
    tmp = symbols('_tmp')
    return f.subs(x[i], tmp).subs(x[i+1], x[i]).subs(tmp, x[i+1])


def hecke_T(f, i):
    """CORRECT Hecke operator:
    T_i f = t * s_i(f) + (t-1) * x_i/(x_i - x_{i+1}) * (f - s_i f)
    """
    si_f = swap_vars(f, i)
    diff = f - si_f
    # diff / (x_i - x_{i+1}) is a polynomial
    divided = cancel(diff / (x[i] - x[i+1]))
    result = t * si_f + (t - 1) * x[i] * divided
    return expand(result)


# Quick sanity check
print("Sanity check:")
print(f"  T_0(x2) = {hecke_T(x2, 0)}")  # should be x1
print(f"  T_0(x1) = {hecke_T(x1, 0)}")  # should be (t-1)*x1 + t*x2
print(f"  T_1(x3) = {hecke_T(x3, 1)}")  # should be x2
print(f"  T_1(x2) = {hecke_T(x2, 1)}")  # should be (t-1)*x2 + t*x3


# E_{(0,2,3)} = x_2^2 * x_3^3
E_antid = x2**2 * x3**3

# Correct permutation words (verified by apply_word)
perms = {
    (0, 2, 3): [],
    (0, 3, 2): [1],
    (2, 0, 3): [0],
    (2, 3, 0): [0, 1],   # s_1 s_0: apply T_0 first, then T_1
    (3, 0, 2): [1, 0],   # s_0 s_1: apply T_1 first, then T_0
    (3, 2, 0): [0, 1, 0],
}

def apply_word(comp, word):
    mu = list(comp)
    for i in word:
        mu[i], mu[i+1] = mu[i+1], mu[i]
    return tuple(mu)

print(f"\nVerifying permutation words:")
for mu, word in sorted(perms.items()):
    result = apply_word(lam_minus, word)
    print(f"  word {word}: {lam_minus} -> {result} == {mu} {'✓' if result == mu else '✗'}")


# Compute f_mu
print(f"\nComputing f_mu:")
print("-" * 50)

f_polys = {}
for mu, word in sorted(perms.items()):
    f = E_antid
    for i in word:
        f = hecke_T(f, i)
    f = expand(f)
    f_polys[mu] = f

    # Print polynomial terms
    p = Poly(f, x1, x2, x3)
    terms = sorted(p.as_dict().items(), reverse=True)
    print(f"\n  f_{mu}:")
    for monom, coeff in terms[:8]:
        print(f"    {coeff} * x1^{monom[0]} x2^{monom[1]} x3^{monom[2]}")
    if len(terms) > 8:
        print(f"    ... ({len(terms)} terms total)")


# Check P_lambda = sum
P_lam = expand(sum(f_polys.values()))
P_s0 = swap_vars(P_lam, 0)
P_s1 = swap_vars(P_lam, 1)
print(f"\n\nP_lambda = sum of f_mu:")
p = Poly(P_lam, x1, x2, x3)
print(f"  {len(p.as_dict())} terms")
print(f"  Symmetric under s_0 (x1<->x2)? {expand(P_lam - P_s0) == 0}")
print(f"  Symmetric under s_1 (x2<->x3)? {expand(P_lam - P_s1) == 0}")


# Numerical evaluation
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

all_pos = True
print(f"\n  pi(mu):")
for mu in sorted(f_vals.keys()):
    pi = f_vals[mu] / P_val
    pos = float(pi) > 0
    if not pos:
        all_pos = False
    print(f"    pi{mu} = {float(pi):.8f} {'✓' if pos else '✗ NEGATIVE'}")
print(f"\n  All positive: {all_pos}")


# Detailed balance ratios
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
            print(f"    ratio = {ratio_f}")

            # Check simple forms
            checks = {
                't': t,
                '1/t': 1/t,
            }
            for name, cand in checks.items():
                if simplify(ratio - cand) == 0:
                    print(f"    *** MATCHES {name} ***")


# x1 = x2 = x3 = 1
print(f"\n\nSpecial case x1=x2=x3=1:")
print("-" * 50)
x_unif = {x1: 1, x2: 1, x3: 1}
for mu in sorted(f_polys.keys()):
    val = simplify(f_polys[mu].subs(x_unif))
    print(f"  f_{mu}(1,1,1; t) = {val}")


# ASEP check
print(f"\n\nASEP detailed balance check (ratio should be t for downhill swap):")
print("-" * 50)
print("For mu[i] > mu[i+1] (larger part first), the ASEP rate is 1 (rightward),")
print("  so pi(mu)/pi(nu) should equal 1/t (where nu = s_i(mu) has parts swapped).")
print("For mu[i] < mu[i+1], rate is t, so pi(mu)/pi(nu) should equal t.")

for mu in sorted(f_polys.keys()):
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in f_polys and mu < nu:
            ratio = cancel(f_polys[mu] / f_polys[nu])
            # mu < nu in lex order. What about the parts?
            # At position pos: mu[pos] vs mu[pos+1]
            if mu[pos] < mu[pos+1]:
                # mu has smaller part first, nu has larger first
                # For ASEP: rate from mu to nu is 1 (sort), rate from nu to mu is t
                # DB: pi(mu)*1 = pi(nu)*t => pi(mu)/pi(nu) = t
                expected = t
                label = f"({mu[pos]}<{mu[pos+1]}, expect t)"
            else:
                expected = 1/t
                label = f"({mu[pos]}>{mu[pos+1]}, expect 1/t)"

            match = simplify(ratio - expected) == 0
            print(f"  {mu}<->{nu} pos {pos} {label}: {'✓' if match else '✗'} ratio={factor(ratio)}")
