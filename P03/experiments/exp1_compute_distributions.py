"""
P03 EXP-1: Compute interpolation ASEP polynomials f*_mu and interpolation
Macdonald polynomial P*_lambda at q=1 for n=3, lambda=(3,2,0).

Strategy: Use the vanishing characterization to compute f*_mu.
- f*_mu is the unique polynomial g of degree <= |lambda| such that:
  (a) g(nu_tilde) = 0 for all compositions nu with |nu| <= |lambda|, nu not in S_n(lambda)
  (b) [x^tau]g = delta_{tau,mu} for all tau in S_n(lambda)

At q=1, the spectral vector simplifies:
  nu_tilde_i = q^{nu_i} * t^{-k_i(nu)}  ->  1 * t^{-k_i(nu)} = t^{-k_i(nu)}

where k_i(nu) = #{j < i : nu_j > nu_i} + #{j > i : nu_j >= nu_i}

So at q=1, all spectral vectors only depend on the ORDERING of the parts, not their values!
This is a massive simplification.

Wait — that can't be right for distinct parts. Let me reconsider.

Actually at q=1: nu_tilde_i = 1^{nu_i} * t^{-k_i} = t^{-k_i}. So the spectral vector
at q=1 only depends on the relative ordering of the nu_i, not their actual values.
This means compositions with different parts but the same relative ordering would have
the same spectral vector. The vanishing conditions may become degenerate.

Let me compute carefully for general q first, then specialize.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import permutations, product
from fractions import Fraction
from functools import reduce

print("P03 EXP-1: Compute interpolation polynomial distributions")
print("=" * 70)

# ============================================================
# Setup: n=3, lambda = (3, 2, 0)
# ============================================================
n = 3
lam = (3, 2, 0)
d = sum(lam)  # = 5

# State space S_n(lambda): all permutations of lambda
S_n_lam = list(set(permutations(lam)))
S_n_lam.sort()
print(f"\nn={n}, lambda={lam}, |lambda|={d}")
print(f"S_n(lambda) = {S_n_lam}")
print(f"|S_n(lambda)| = {len(S_n_lam)}")

# ============================================================
# Spectral vectors at general q
# ============================================================
def k_i(nu, i):
    """k_i(nu) = #{j < i : nu_j > nu_i} + #{j > i : nu_j >= nu_i}"""
    n = len(nu)
    count = 0
    for j in range(n):
        if j < i and nu[j] > nu[i]:
            count += 1
        elif j > i and nu[j] >= nu[i]:
            count += 1
    return count

def spectral_vector(nu, q, t):
    """nu_tilde_i = q^{nu_i} * t^{-k_i(nu)}"""
    n = len(nu)
    return tuple(q**nu[i] * t**(-k_i(nu, i)) for i in range(n))

# Test: compute spectral vectors for S_n(lambda)
print(f"\nSpectral vectors (symbolic):")
for mu in S_n_lam:
    ks = [k_i(mu, i) for i in range(n)]
    print(f"  mu={mu}: k = {ks}, tilde = (q^{mu[0]}*t^{-ks[0]}, q^{mu[1]}*t^{-ks[1]}, q^{mu[2]}*t^{-ks[2]})")


# ============================================================
# Enumerate all compositions nu with |nu| <= d and n parts >= 0
# ============================================================
def compositions_up_to(n, d):
    """All compositions (nu_1, ..., nu_n) with nu_i >= 0 and sum <= d."""
    if n == 1:
        return [(k,) for k in range(d + 1)]
    result = []
    for k in range(d + 1):
        for rest in compositions_up_to(n - 1, d - k):
            result.append((k,) + rest)
    return result

all_comps = compositions_up_to(n, d)
print(f"\nTotal compositions with |nu| <= {d}, n={n} parts: {len(all_comps)}")

# Compositions NOT in S_n(lambda)
comps_not_in_Sn = [nu for nu in all_comps if nu not in S_n_lam]
print(f"Compositions not in S_n(lambda): {len(comps_not_in_Sn)}")


# ============================================================
# At q=1, spectral vectors collapse
# ============================================================
print(f"\n\nTest: Spectral vectors at q=1")
print("-" * 50)

t_val = 0.7  # concrete t value for testing

for mu in S_n_lam:
    sv = spectral_vector(mu, 1.0, t_val)
    print(f"  mu={mu}: tilde = ({sv[0]:.4f}, {sv[1]:.4f}, {sv[2]:.4f})")

print(f"\n  Check: are any spectral vectors equal at q=1?")
seen = {}
for nu in all_comps:
    sv = spectral_vector(nu, 1.0, t_val)
    sv_round = tuple(round(x, 10) for x in sv)
    if sv_round in seen:
        print(f"  COLLISION: nu={nu} and nu'={seen[sv_round]} have same spectral vector at q=1")
    else:
        seen[sv_round] = nu

n_distinct = len(seen)
print(f"  {n_distinct} distinct spectral vectors out of {len(all_comps)} compositions")


# ============================================================
# Since q=1 causes massive collisions, let's work with general q
# and specialize at the end.
# ============================================================
print(f"\n\nCompute with general q (numerical), then take q->1 limit")
print("-" * 50)

# Use small q near 1 to check limiting behavior
q_vals = [0.5, 0.8, 0.9, 0.95, 0.99, 0.999]
t_val = 0.7

# ============================================================
# Build the monomial basis for polynomials of degree <= d in n vars
# ============================================================
def monomials_up_to_degree(n, d):
    """All monomials x^alpha with |alpha| <= d."""
    if n == 1:
        return [(k,) for k in range(d + 1)]
    result = []
    for k in range(d + 1):
        for rest in monomials_up_to_degree(n - 1, d - k):
            result.append((k,) + rest)
    return result

monoms = monomials_up_to_degree(n, d)
n_monoms = len(monoms)
print(f"Monomial basis: {n_monoms} monomials of degree <= {d} in {n} variables")

monom_idx = {m: i for i, m in enumerate(monoms)}


def eval_monomial(alpha, x):
    """Evaluate x^alpha."""
    return reduce(lambda a, b: a * b, (x[i]**alpha[i] for i in range(len(alpha))), 1.0)


# ============================================================
# For each q value, solve for f*_mu via the vanishing characterization
# ============================================================
print(f"\nSolving for f*_mu via vanishing characterization:")

for q_val in q_vals:
    print(f"\n  q = {q_val}:")

    # Build the constraint matrix
    # f*_mu = sum_alpha c_alpha x^alpha
    # Constraints:
    # (A) f*_mu(nu_tilde) = 0 for nu not in S_n(lambda) with |nu| <= d
    # (B) [x^tau] f*_mu = delta_{tau, mu} for tau in S_n(lambda)
    #     i.e., the coefficient of x^tau in f*_mu is 1 if tau=mu, 0 otherwise

    # For constraint (B): the coefficient of x^tau is directly c_tau
    # (since tau is a monomial exponent).
    # But wait — tau is a composition (permutation of lambda), so
    # x^tau = x_1^{tau_1} * x_2^{tau_2} * x_3^{tau_3}.
    # The constraint [x^tau]f*_mu = delta_{tau,mu} means:
    # c_{tau} = delta_{tau, mu}

    # This directly fixes 6 coefficients (one for each tau in S_n(lambda)).
    # The remaining coefficients are determined by the vanishing conditions.

    # Total unknowns: n_monoms = 56 (monomials of degree <= 5 in 3 vars)
    # Fixed by (B): 6 coefficients
    # Free unknowns: 50
    # Vanishing constraints: len(comps_not_in_Sn)

    # But some spectral vectors may collide. Let's check.
    vanishing_points = []
    for nu in comps_not_in_Sn:
        sv = spectral_vector(nu, q_val, t_val)
        vanishing_points.append(sv)

    # Remove duplicate spectral vectors
    unique_sv = {}
    for i, sv in enumerate(vanishing_points):
        sv_round = tuple(round(x, 12) for x in sv)
        if sv_round not in unique_sv:
            unique_sv[sv_round] = sv
    n_unique = len(unique_sv)

    # Constraint matrix: for each unique spectral vector sv,
    # sum_alpha c_alpha * sv^alpha = 0
    # where the c_alpha for alpha in S_n(lambda) are already fixed.

    # Let free_monoms = monoms not in S_n(lambda)
    free_monoms = [m for m in monoms if m not in S_n_lam]
    n_free = len(free_monoms)
    free_idx = {m: i for i, m in enumerate(free_monoms)}

    # For each vanishing constraint at spectral vector sv:
    # sum_{alpha free} c_alpha * sv^alpha = -sum_{tau in S_n(lambda)} delta_{tau,mu} * sv^tau
    # = -sv^mu  (since c_tau = delta_{tau,mu})

    sv_list = list(unique_sv.values())

    A = np.zeros((len(sv_list), n_free))
    for i, sv in enumerate(sv_list):
        for j, m in enumerate(free_monoms):
            A[i, j] = eval_monomial(m, sv)

    # Solve for each mu in S_n(lambda)
    distributions = {}
    for mu in S_n_lam:
        # RHS: -sv^mu for each constraint
        b = np.zeros(len(sv_list))
        for i, sv in enumerate(sv_list):
            b[i] = -eval_monomial(mu, sv)

        # Solve least squares (should be exact if system is determined)
        c_free, residuals, rank, sv_vals = np.linalg.lstsq(A, b, rcond=None)

        # Reconstruct full polynomial
        c_full = np.zeros(n_monoms)
        for j, m in enumerate(free_monoms):
            c_full[monom_idx[m]] = c_free[j]
        c_full[monom_idx[mu]] = 1.0  # constraint (B)

        # Evaluate f*_mu at some test point x
        x_test = (1.5, 0.8, 1.2)
        f_val = sum(c_full[monom_idx[m]] * eval_monomial(m, x_test) for m in monoms)
        distributions[mu] = f_val

    # P*_lambda should be sum of f*_mu
    P_star = sum(distributions.values())

    # Stationary distribution
    pi = {mu: distributions[mu] / P_star for mu in S_n_lam}

    print(f"    Unique vanishing spectral vectors: {n_unique}")
    print(f"    Free coefficients: {n_free}")
    print(f"    System shape: {len(sv_list)} x {n_free}, rank={np.linalg.matrix_rank(A, tol=1e-10)}")
    print(f"    f*_mu values at x={x_test}:")
    for mu in S_n_lam:
        print(f"      f*_{mu} = {distributions[mu]:.6f}")
    print(f"    P*_lambda = sum = {P_star:.6f}")
    print(f"    pi(mu) = f*_mu / P*_lambda:")
    for mu in S_n_lam:
        print(f"      pi{mu} = {pi[mu]:.6f}")
    print(f"    Sum pi = {sum(pi.values()):.10f}")

    # Check: are all pi positive?
    all_pos = all(v > 0 for v in pi.values())
    print(f"    All positive: {all_pos}")


# ============================================================
# TEST 2: Detailed balance check for adjacent transposition chain
# ============================================================
print(f"\n\n{'=' * 70}")
print("Test 2: Adjacent transposition chain — detailed balance")
print("=" * 70)

q_val = 0.99  # near q=1
x_test = (1.5, 0.8, 1.2)

# Recompute distributions at this q
vanishing_points_q = []
for nu in comps_not_in_Sn:
    sv = spectral_vector(nu, q_val, t_val)
    vanishing_points_q.append(sv)

unique_sv_q = {}
for sv in vanishing_points_q:
    sv_round = tuple(round(x, 12) for x in sv)
    if sv_round not in unique_sv_q:
        unique_sv_q[sv_round] = sv

sv_list_q = list(unique_sv_q.values())
free_monoms = [m for m in monoms if m not in S_n_lam]

A_q = np.zeros((len(sv_list_q), len(free_monoms)))
for i, sv in enumerate(sv_list_q):
    for j, m in enumerate(free_monoms):
        A_q[i, j] = eval_monomial(m, sv)

distributions_q = {}
for mu in S_n_lam:
    b = np.zeros(len(sv_list_q))
    for i, sv in enumerate(sv_list_q):
        b[i] = -eval_monomial(mu, sv)
    c_free, _, _, _ = np.linalg.lstsq(A_q, b, rcond=None)
    c_full = np.zeros(n_monoms)
    for j, m in enumerate(free_monoms):
        c_full[monom_idx[m]] = c_free[j]
    c_full[monom_idx[mu]] = 1.0
    f_val = sum(c_full[monom_idx[m]] * eval_monomial(m, x_test) for m in monoms)
    distributions_q[mu] = f_val

P_star_q = sum(distributions_q.values())
pi_q = {mu: distributions_q[mu] / P_star_q for mu in S_n_lam}

print(f"\nq={q_val}, t={t_val}, x={x_test}")
print(f"Stationary distribution:")
for mu in S_n_lam:
    print(f"  pi{mu} = {pi_q[mu]:.8f}")

# Adjacent transpositions: swap positions i and i+1
# For mu, the neighbor is mu with mu_i <-> mu_{i+1}
print(f"\nDetailed balance ratios pi(mu)/pi(nu) for adjacent transpositions:")
for mu in S_n_lam:
    for pos in range(n - 1):
        nu = list(mu)
        nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
        nu = tuple(nu)
        if nu in pi_q and mu != nu:
            ratio = pi_q[mu] / pi_q[nu]
            # For ASEP-like chain, we'd want ratio = t^{something} * x_ratio
            print(f"  swap pos {pos},{pos+1}: mu={mu}->nu={nu}: "
                  f"pi(mu)/pi(nu) = {ratio:.6f}")


# ============================================================
# TEST 3: Check if ratios have simple t-dependence
# ============================================================
print(f"\n\n{'=' * 70}")
print("Test 3: Are detailed balance ratios simple functions of t?")
print("=" * 70)

t_vals_test = [0.3, 0.5, 0.7, 0.9, 1.5, 2.0, 3.0]
q_val = 0.999
x_test = (1.5, 0.8, 1.2)

# For each t, compute pi and the detailed balance ratios
# Focus on one specific swap: (3,2,0) <-> (2,3,0) (swap positions 0,1)
mu_test = (3, 2, 0)
nu_test = (2, 3, 0)

print(f"\nSwap: {mu_test} <-> {nu_test} (positions 0,1)")
print(f"q = {q_val}, x = {x_test}")
print(f"{'t':>6} | {'pi(mu)/pi(nu)':>15} | {'t itself':>8} | {'x1/x2':>8} | {'t*x1/x2':>10}")

for t_v in t_vals_test:
    # Recompute for this t
    unique_sv_t = {}
    for nu_comp in comps_not_in_Sn:
        sv = spectral_vector(nu_comp, q_val, t_v)
        sv_round = tuple(round(x, 12) for x in sv)
        if sv_round not in unique_sv_t:
            unique_sv_t[sv_round] = sv

    sv_list_t = list(unique_sv_t.values())
    A_t = np.zeros((len(sv_list_t), len(free_monoms)))
    for i, sv in enumerate(sv_list_t):
        for j, m in enumerate(free_monoms):
            A_t[i, j] = eval_monomial(m, sv)

    dists_t = {}
    for mu in [mu_test, nu_test]:
        b = np.zeros(len(sv_list_t))
        for i, sv in enumerate(sv_list_t):
            b[i] = -eval_monomial(mu, sv)
        c_free, _, _, _ = np.linalg.lstsq(A_t, b, rcond=None)
        c_full = np.zeros(n_monoms)
        for j, m in enumerate(free_monoms):
            c_full[monom_idx[m]] = c_free[j]
        c_full[monom_idx[mu]] = 1.0
        f_val = sum(c_full[monom_idx[m]] * eval_monomial(m, x_test) for m in monoms)
        dists_t[mu] = f_val

    ratio = dists_t[mu_test] / dists_t[nu_test]
    x_ratio = x_test[0] / x_test[1]
    print(f"{t_v:6.2f} | {ratio:15.6f} | {t_v:8.4f} | {x_ratio:8.4f} | {t_v * x_ratio:10.4f}")


print(f"\n\n{'=' * 70}")
print("EXP-1 Summary")
print("=" * 70)
print("Computed interpolation ASEP polynomials f*_mu at various q, t values.")
print("Key questions for next steps:")
print("1. Do the detailed balance ratios have simple t/x dependence?")
print("2. Is the distribution well-defined (positive) at q=1?")
print("3. Can we read off transition rates from the ratio structure?")
