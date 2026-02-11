"""
P03 EXP-3b: Symbolic interpolation polynomials for n=2 case.

Goal: Compute E*_{(0,2)} symbolically with q as formal parameter,
apply Hecke operator to get f*_{(2,0)}, take q->1 limit, and check
if the detailed balance ratio is exactly 1/t.

n=2, lambda=(2,0), anti-dominant = (0,2).
System of 5 equations in 5 unknowns (small enough for symbolic solve).
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import (symbols, expand, simplify, factor, Rational, Poly,
                   cancel, together, solve, limit, Symbol, collect,
                   numer, denom, fraction, apart, Matrix)

print("P03 EXP-3b: Symbolic interpolation polynomials (n=2)")
print("=" * 70)

y1, y2 = symbols('y1 y2')
q, t = symbols('q t')


def spectral_vector_sym(nu):
    """Symbolic spectral vector."""
    n = len(nu)
    result = []
    for i in range(n):
        k_i = sum(1 for j in range(i) if nu[j] > nu[i]) + \
              sum(1 for j in range(i+1, n) if nu[j] >= nu[i])
        result.append(q**nu[i] * t**(-k_i))
    return result


# Compositions with |nu| <= 2
comps = [
    (0, 0),  # |nu|=0
    (0, 1), (1, 0),  # |nu|=1
    (0, 2), (1, 1), (2, 0),  # |nu|=2
]

print("Spectral vectors:")
for nu in comps:
    sv = spectral_vector_sym(nu)
    print(f"  {nu}: ({sv[0]}, {sv[1]})")

# E*_{(0,2)} = y2^2 + c1*y1*y2 + c2*y1^2 + c3*y1 + c4*y2 + c5
c1, c2, c3, c4, c5 = symbols('c1 c2 c3 c4 c5')
E_star = y2**2 + c1*y1*y2 + c2*y1**2 + c3*y1 + c4*y2 + c5

# Vanishing at all nu != (0,2) with |nu| <= 2
vanishing = [nu for nu in comps if nu != (0, 2)]
print(f"\nVanishing conditions: {vanishing}")

equations = []
for nu in vanishing:
    sv = spectral_vector_sym(nu)
    eq = E_star.subs(y1, sv[0]).subs(y2, sv[1])
    eq = expand(eq)
    equations.append(eq)
    print(f"  E*({nu}_tilde) = {eq}")

print(f"\nSolving 5 equations in 5 unknowns...")
sol = solve(equations, [c1, c2, c3, c4, c5], dict=True)
print(f"Number of solutions: {len(sol)}")

if sol:
    sol = sol[0]
    for var in [c1, c2, c3, c4, c5]:
        val = sol[var]
        val_simplified = factor(val)
        print(f"  {var} = {val_simplified}")

    E_star_solved = E_star
    for var, val in sol.items():
        E_star_solved = E_star_solved.subs(var, val)
    E_star_solved = expand(E_star_solved)
    print(f"\nE*_{{(0,2)}}(y1,y2; q,t) = {E_star_solved}")

    # Verify vanishing
    print(f"\nVerification:")
    for nu in vanishing:
        sv = spectral_vector_sym(nu)
        val = E_star_solved.subs(y1, sv[0]).subs(y2, sv[1])
        val = simplify(val)
        print(f"  E*({nu}_tilde) = {val} {'✓' if val == 0 else '✗'}")

    # Value at own spectral vector
    sv_02 = spectral_vector_sym((0, 2))
    val_02 = simplify(E_star_solved.subs(y1, sv_02[0]).subs(y2, sv_02[1]))
    print(f"  E*((0,2)_tilde) = {factor(val_02)} (should be nonzero)")

    # ====================================================================
    # Apply Hecke operator T_0 to get f*_{(2,0)}
    # ====================================================================
    print(f"\n{'='*70}")
    print("Applying Hecke operator T_0")
    print(f"{'='*70}")

    def swap_vars(f):
        """Swap y1 <-> y2."""
        tmp = symbols('_tmp')
        return f.subs(y1, tmp).subs(y2, y1).subs(tmp, y2)

    def hecke_T(f):
        """T_0 f = t * s_0(f) + (t-1) * y1/(y1-y2) * (f - s_0(f))"""
        sf = swap_vars(f)
        diff = f - sf
        divided = cancel(diff / (y1 - y2))
        result = t * sf + (t - 1) * y1 * divided
        return expand(result)

    # f*_{(0,2)} = E*_{(0,2)} (no Hecke operators needed)
    f_star_02 = E_star_solved
    print(f"f*_{{(0,2)}} = {f_star_02}")

    # f*_{(2,0)} = T_0 * E*_{(0,2)}
    print(f"\nComputing T_0(E*_{{(0,2)}})...")
    f_star_20 = hecke_T(E_star_solved)
    f_star_20 = expand(f_star_20)
    print(f"f*_{{(2,0)}} = {f_star_20}")

    # Sum = P*_lambda
    P_star = expand(f_star_02 + f_star_20)
    print(f"\nP*_{{(2,0)}} = f*_02 + f*_20 = {P_star}")

    # Check symmetry
    P_star_swapped = swap_vars(P_star)
    is_symmetric = expand(P_star - P_star_swapped) == 0
    print(f"P* symmetric? {is_symmetric}")

    # ====================================================================
    # Ratio f*_02 / f*_20
    # ====================================================================
    print(f"\n{'='*70}")
    print("Detailed balance ratio")
    print(f"{'='*70}")

    ratio = cancel(f_star_02 / f_star_20)
    ratio_factored = factor(ratio)
    print(f"f*_02 / f*_20 = {ratio_factored}")

    # Check if ratio = 1/t
    check_1_over_t = simplify(ratio - 1/t)
    print(f"ratio - 1/t = {simplify(check_1_over_t)}")
    if check_1_over_t == 0:
        print("*** RATIO = 1/t EXACTLY (for all q, t) ***")

    # ====================================================================
    # q -> 1 limit
    # ====================================================================
    print(f"\n{'='*70}")
    print("q -> 1 limit")
    print(f"{'='*70}")

    f_star_02_q1 = limit(f_star_02, q, 1)
    f_star_20_q1 = limit(f_star_20, q, 1)
    P_star_q1 = limit(P_star, q, 1)

    print(f"f*_02(q=1) = {expand(f_star_02_q1)}")
    print(f"f*_20(q=1) = {expand(f_star_20_q1)}")
    print(f"P*(q=1) = {expand(P_star_q1)}")

    # Ratio at q=1
    ratio_q1 = cancel(f_star_02_q1 / f_star_20_q1)
    ratio_q1_f = factor(ratio_q1)
    print(f"\nf*_02/f*_20 at q=1 = {ratio_q1_f}")

    check = simplify(ratio_q1 - 1/t)
    print(f"ratio - 1/t at q=1 = {check}")
    if check == 0:
        print("*** RATIO = 1/t at q=1 ***")

    # Positivity of f*_02(q=1) and f*_20(q=1)
    print(f"\nPositivity check at y1=3/2, y2=4/5, t=7/10:")
    test_vals = {y1: Rational(3, 2), y2: Rational(4, 5), t: Rational(7, 10)}
    v02 = f_star_02_q1.subs(test_vals)
    v20 = f_star_20_q1.subs(test_vals)
    print(f"  f*_02 = {v02} = {float(v02):.8f}")
    print(f"  f*_20 = {v20} = {float(v20):.8f}")
    print(f"  Both positive: {v02 > 0 and v20 > 0}")
    print(f"  pi_02 = {float(v02/(v02+v20)):.8f}")
    print(f"  pi_20 = {float(v20/(v02+v20)):.8f}")

    # ====================================================================
    # Compare with homogeneous case
    # ====================================================================
    print(f"\n{'='*70}")
    print("Comparison with homogeneous case (E_{(0,2)} = y2^2)")
    print(f"{'='*70}")

    E_hom = y2**2
    f_hom_02 = E_hom
    f_hom_20 = hecke_T(E_hom)
    f_hom_20 = expand(f_hom_20)

    ratio_hom = cancel(f_hom_02 / f_hom_20)
    print(f"f_02 = {f_hom_02}")
    print(f"f_20 = {f_hom_20}")
    print(f"f_02/f_20 = {factor(ratio_hom)}")
    print(f"Is ratio = 1/t? {simplify(ratio_hom - 1/t) == 0}")

    # ====================================================================
    # Explicit form of the Markov chain
    # ====================================================================
    print(f"\n{'='*70}")
    print("Markov chain for n=2 (if ratio = 1/t)")
    print(f"{'='*70}")

    print("States: (0,2) and (2,0)")
    print("Chain: rate t to go (0,2)->(2,0), rate 1 to go (2,0)->(0,2)")
    print("Or equivalently: at bond (pos 0, pos 1):")
    print("  if mu[0] < mu[1]: swap at rate t (uphill)")
    print("  if mu[0] > mu[1]: swap at rate 1 (downhill)")
    print("Detailed balance: pi(0,2)*t = pi(2,0)*1")
    print("  => pi(0,2)/pi(2,0) = 1/t  ✓")
    print("This is the standard ASEP with asymmetry parameter t!")

else:
    print("No solution found!")
