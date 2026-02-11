"""
P03 EXP-2: Compute ASEP polynomials via Hecke operators.

For the homogeneous (non-interpolation) case:
  f_mu = T_{sigma_mu} * x^lambda
where T_i is the Hecke generator and lambda is dominant.

For n=3, lambda=(3,2,0), compute f_mu for all 6 permutations mu in S_3(lambda).

Hecke operator (Macdonald convention):
  T_i f = t*f + (t-1) * x_{i+1}/(x_i - x_{i+1}) * (f - s_i f)

where s_i swaps x_i and x_{i+1}.

Then check:
1. Is the distribution f_mu / sum(f_mu) positive?
2. Do detailed balance ratios have simple form?
3. Does the standard ASEP chain work?
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import symbols, expand, simplify, factor, Rational, Poly, degree
from sympy import cancel, together, apart, collect
from itertools import permutations

print("P03 EXP-2: ASEP polynomials via Hecke operators")
print("=" * 70)

# Variables
x1, x2, x3 = symbols('x1 x2 x3', positive=True)
t = symbols('t', positive=True)
x = [x1, x2, x3]
n = 3
lam = (3, 2, 0)


def swap_vars(f, i):
    """Swap x_i and x_{i+1} in polynomial f (0-indexed)."""
    return f.subs([(x[i], x[i+1]), (x[i+1], x[i])])


def hecke_T(f, i):
    """Apply Hecke operator T_i to polynomial f.
    T_i f = t*f + (t-1) * x_{i+1}/(x_i - x_{i+1}) * (f - s_i(f))
    """
    si_f = swap_vars(f, i)
    diff = f - si_f
    # diff / (x_i - x_{i+1}) should be a polynomial (no remainder)
    divided = cancel(diff / (x[i] - x[i+1]))
    result = t * f + (t - 1) * x[i+1] * divided
    return expand(result)


# ============================================================
# Compute E_lambda for dominant lambda = (3,2,0)
# In the dominant convention, E_lambda = x^lambda
# ============================================================
E_lam = x1**3 * x2**2  # x3^0 = 1

print(f"\nlambda = {lam}")
print(f"E_lambda = {E_lam}")

# ============================================================
# Shortest permutations mapping lambda to each mu
# ============================================================
# lambda = (3,2,0) is dominant
# Permutations and their shortest words:
# (3,2,0) -> id -> []
# (2,3,0) -> s_0 (swap pos 0,1) -> [0]
# (3,0,2) -> s_1 (swap pos 1,2) -> [1]
# (0,2,3) -> s_0 s_1 s_0 = w_0 -> [0,1,0]
# (2,0,3) -> s_1 s_0 -> [1,0]
# (0,3,2) -> s_0 s_1 -> [0,1]

# Wait, need to verify: sigma_mu maps lambda to mu
# s_0 swaps position 0 and 1: s_0(3,2,0) = (2,3,0) ✓
# s_1 swaps position 1 and 2: s_1(3,2,0) = (3,0,2) ✓
# s_0 s_1(3,2,0) = s_0(3,0,2) = (0,3,2) ✓
# s_1 s_0(3,2,0) = s_1(2,3,0) = (2,0,3) ✓
# s_0 s_1 s_0(3,2,0) = s_0(0,3,2) = wait...
#   s_0(0,3,2) = (3,0,2)? No, s_0 swaps positions 0,1: (0,3,2) -> (3,0,2)
#   That's not (0,2,3).
# Let me redo: s_1 s_0 s_1(3,2,0) = s_1 s_0(3,0,2) = s_1(0,3,2) = (0,2,3) ✓

# For (0,2,3): we need sigma such that sigma(3,2,0) = (0,2,3)
# This maps 3->0, 2->2, 0->3. As a permutation of positions:
# position 0: was 3, now 0 -> send to position 2
# position 1: was 2, now 2 -> stays
# position 2: was 0, now 3 -> send to position 0
# So sigma = (0 2) as a position permutation, which is s_0 s_1 s_0 or s_1 s_0 s_1

# Actually, for permutations acting on parts:
# If sigma acts on POSITIONS: sigma(mu)_i = mu_{sigma^{-1}(i)}
# If sigma acts on VALUES: sigma(mu) = (mu_{sigma(1)}, mu_{sigma(2)}, mu_{sigma(3)})

# In the ASEP convention, sigma permutes positions.
# sigma_mu is the shortest permutation s.t. sigma_mu(lambda) = mu
# where sigma acts on positions: (sigma(lambda))_i = lambda_{sigma^{-1}(i)}

# Let me use the convention: sigma acts as sigma(mu) = (mu_{sigma^{-1}(1)}, ..., mu_{sigma^{-1}(n)})
# Then sigma = s_i swaps positions i and i+1.

# Actually I think the convention is simpler: s_i acting on a composition just swaps the i-th and (i+1)-th parts.
# s_0(3,2,0) = (2,3,0)
# s_1(3,2,0) = (3,0,2)

# So:
# (3,2,0) = id(3,2,0) -> word: []
# (2,3,0) = s_0(3,2,0) -> word: [0]
# (3,0,2) = s_1(3,2,0) -> word: [1]
# (2,0,3) = s_1(s_0(3,2,0)) = s_1(2,3,0) = (2,0,3) -> word: [0,1]... wait
#   s_1(2,3,0) = (2,0,3) ✓, so s_1 s_0(lambda) = (2,0,3). Word: [1,0]
#   But the word for the permutation is read right-to-left: sigma = s_1 s_0, word = [1,0]
#   T_{sigma} = T_1 T_0

# Let me reconsider. f_mu = T_{sigma_mu} E_lambda
# If sigma_mu = s_{i_1} s_{i_2} ... s_{i_k} (reduced word)
# then T_{sigma_mu} = T_{i_1} T_{i_2} ... T_{i_k}
# The operators are applied LEFT to RIGHT to E_lambda:
# f_mu = T_{i_1}(T_{i_2}(...(T_{i_k}(E_lambda))...))
# Actually, it depends on convention. Usually T_w = T_{i_1} T_{i_2} ... T_{i_k}
# acts as composition: T_w(f) = T_{i_1}(T_{i_2}(...(T_{i_k}(f))...))

# Let me just carefully determine sigma_mu for each mu and compute.

perms = {
    (3, 2, 0): [],           # identity
    (2, 3, 0): [0],          # s_0
    (3, 0, 2): [1],          # s_1
    (2, 0, 3): [0, 1],       # s_0 then s_1: s_1(s_0(lambda)) = s_1(2,3,0) = (2,0,3)
    (0, 3, 2): [1, 0],       # s_1 then s_0: s_0(s_1(lambda)) = s_0(3,0,2) = (0,3,2)
                              # wait: s_0(3,0,2) = (0,3,2)? s_0 swaps pos 0,1: (3,0,2)->(0,3,2) ✓
    (0, 2, 3): [0, 1, 0],    # longest element
}

# Verify: apply the permutation words to lambda
def apply_word(lam, word):
    """Apply sequence of transpositions to composition."""
    mu = list(lam)
    for i in word:
        mu[i], mu[i+1] = mu[i+1], mu[i]
    return tuple(mu)

print(f"\nVerifying permutation words:")
for mu, word in perms.items():
    result = apply_word(lam, word)
    check = "✓" if result == mu else f"✗ (got {result})"
    print(f"  word {word} -> {result} == {mu} {check}")


# ============================================================
# Compute f_mu = T_{word} E_lambda
# ============================================================
print(f"\nComputing ASEP polynomials f_mu:")
print("-" * 50)

f_polys = {}
for mu, word in sorted(perms.items()):
    f = E_lam
    # Apply Hecke operators in order (left to right in the word)
    for i in word:
        f = hecke_T(f, i)
    f = expand(f)
    f_polys[mu] = f
    print(f"\n  f_{mu}:")
    # Collect by monomials
    p = Poly(f, x1, x2, x3)
    for monom, coeff in sorted(p.as_dict().items(), reverse=True):
        print(f"    {coeff} * x1^{monom[0]} x2^{monom[1]} x3^{monom[2]}")


# ============================================================
# Verify: P_lambda = sum of f_mu (should be symmetric)
# ============================================================
P_lam = sum(f_polys.values())
P_lam = expand(P_lam)
print(f"\n\nP_lambda = sum of f_mu:")
p = Poly(P_lam, x1, x2, x3)
for monom, coeff in sorted(p.as_dict().items(), reverse=True):
    print(f"  {coeff} * x1^{monom[0]} x2^{monom[1]} x3^{monom[2]}")

# Check symmetry
P_s1 = swap_vars(P_lam, 0)
P_s2 = swap_vars(P_lam, 1)
print(f"\n  P_lambda symmetric under s_0? {expand(P_lam - P_s1) == 0}")
print(f"  P_lambda symmetric under s_1? {expand(P_lam - P_s2) == 0}")


# ============================================================
# Evaluate at specific x values and check positivity
# ============================================================
print(f"\n\nNumerical evaluation:")
print("-" * 50)

x_vals = {x1: Rational(3, 2), x2: Rational(4, 5), x3: Rational(6, 5)}
t_val_sym = Rational(7, 10)

print(f"x = {dict(x_vals)}, t = {t_val_sym}")
print()

f_vals = {}
for mu in sorted(f_polys.keys()):
    val = f_polys[mu].subs(x_vals).subs(t, t_val_sym)
    f_vals[mu] = val
    print(f"  f_{mu} = {val} = {float(val):.6f}")

P_val = sum(f_vals.values())
print(f"\n  P_lambda = {P_val} = {float(P_val):.6f}")

print(f"\n  pi(mu) = f_mu / P_lambda:")
all_pos = True
for mu in sorted(f_vals.keys()):
    pi_val = f_vals[mu] / P_val
    pos = float(pi_val) > 0
    if not pos:
        all_pos = False
    print(f"    pi{mu} = {float(pi_val):.6f} {'✓' if pos else '✗ NEGATIVE'}")

print(f"\n  All positive: {all_pos}")


# ============================================================
# Detailed balance for adjacent transposition chain
# ============================================================
print(f"\n\nDetailed balance ratios:")
print("-" * 50)
print(f"For swap at position i: mu <-> nu where nu = s_i(mu)")

for mu in sorted(f_vals.keys()):
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in f_vals and mu < nu:  # avoid duplicates
            ratio = f_vals[mu] / f_vals[nu]
            ratio_simplified = simplify(ratio)
            print(f"\n  swap pos {pos}: {mu} <-> {nu}")
            print(f"    f_{mu}/f_{nu} = {float(ratio):.6f}")
            print(f"    simplified: {ratio_simplified}")

            # For ASEP: the ratio should be related to t and x_i/x_{i+1}
            # For standard multispecies ASEP on ring, detailed balance gives:
            # pi(mu)/pi(nu) for s_i swap = t * x_i/x_{i+1} if mu_i > mu_{i+1}
            # Check this
            if mu[pos] > mu[pos + 1]:
                expected = t_val_sym * float(x_vals[x[pos]]) / float(x_vals[x[pos+1]])
                print(f"    t * x_{pos+1}/x_{pos+2} = {float(expected):.6f}")
            else:
                expected = float(x_vals[x[pos]]) / (t_val_sym * float(x_vals[x[pos+1]]))
                print(f"    x_{pos+1}/(t*x_{pos+2}) = {float(expected):.6f}")


# ============================================================
# Try symbolic detailed balance
# ============================================================
print(f"\n\nSymbolic detailed balance ratios:")
print("-" * 50)

for mu in sorted(f_polys.keys()):
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in f_polys and mu < nu:
            ratio = together(f_polys[mu] / f_polys[nu])
            ratio_simplified = cancel(ratio)
            # Try to factor
            ratio_factored = factor(ratio_simplified)
            print(f"  swap pos {pos}: {mu} <-> {nu}")
            print(f"    ratio = {ratio_factored}")
