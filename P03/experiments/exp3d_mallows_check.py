"""
P03 EXP-3d: Verify Mallows distribution prediction.

If f*_mu(q=1) = C(x,t) * t^{inv(mu)}, then:
1. The ratio f*_mu / t^{inv(mu)} should be the SAME for all mu (= C).
2. pi(mu) = t^{inv(mu)} / sum_nu t^{inv(nu)} should be x-independent.
3. For n=3, [3]_t! = (1+t)(1+t+t^2) = 1 + 2t + 2t^2 + t^3.

We verify by computing f*_mu at q close to 1 and checking if f*_mu / t^{inv(mu)}
is constant across mu.

Also verify the n=2 symbolic result more explicitly.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 80

import random
random.seed(42)

print("P03 EXP-3d: Mallows distribution verification")
print("=" * 70)

n = 3
lam_minus = (0, 2, 3)


def compositions_of(total, nparts):
    if nparts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions_of(total - first, nparts - 1):
            yield (first,) + rest


def spectral_vector(nu, q, t):
    result = []
    for i in range(len(nu)):
        k_i = sum(1 for j in range(i) if nu[j] > nu[i]) + \
              sum(1 for j in range(i+1, len(nu)) if nu[j] >= nu[i])
        result.append(q**nu[i] * t**(-k_i))
    return result


def inversions(mu):
    """Count inversions: #{(i,j): i<j, mu_i > mu_j}."""
    n = len(mu)
    inv = 0
    for i in range(n):
        for j in range(i+1, n):
            if mu[i] > mu[j]:
                inv += 1
    return inv


# Monomial basis
monoms = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            monoms.append((a, b, c))

leading = (0, 2, 3)
leading_idx = monoms.index(leading)
unknown_monoms = [m for m in monoms if m != leading]
unknown_indices = [i for i, m in enumerate(monoms) if m != leading]

all_comps_le5 = []
for total in range(6):
    all_comps_le5.extend(list(compositions_of(total, 3)))
vanishing_comps = [nu for nu in all_comps_le5 if nu != lam_minus]

perms = {
    (0, 2, 3): [],
    (0, 3, 2): [1],
    (2, 0, 3): [0],
    (2, 3, 0): [0, 1],
    (3, 0, 2): [1, 0],
    (3, 2, 0): [0, 1, 0],
}
S_n_lambda = sorted(perms.keys())


def compute_E_star(q, t):
    nrows = len(vanishing_comps)
    ncols = len(unknown_monoms)
    A = mpmath.matrix(nrows, ncols)
    b = mpmath.matrix(nrows, 1)
    for row, nu in enumerate(vanishing_comps):
        sv = spectral_vector(nu, q, t)
        for col, monom in enumerate(unknown_monoms):
            A[row, col] = sv[0]**monom[0] * sv[1]**monom[1] * sv[2]**monom[2]
        b[row] = -(sv[0]**leading[0] * sv[1]**leading[1] * sv[2]**leading[2])
    return mpmath.lu_solve(A, b)


def build_full_coeffs(E_coeffs):
    full = [mpmath.mpf(0)] * len(monoms)
    full[leading_idx] = mpmath.mpf(1)
    for i, idx in enumerate(unknown_indices):
        full[idx] = E_coeffs[i]
    return full


def eval_full(full_coeffs, xv):
    result = mpmath.mpf(0)
    for idx, monom in enumerate(monoms):
        result += full_coeffs[idx] * xv[0]**monom[0] * xv[1]**monom[1] * xv[2]**monom[2]
    return result


# Grid for Hecke evaluation/interpolation
ngrid = 80
grid = []
for _ in range(ngrid):
    while True:
        pt = [mpmath.mpf(random.uniform(0.5, 2.5)) for _ in range(3)]
        if abs(pt[0] - pt[1]) > 0.2 and abs(pt[1] - pt[2]) > 0.2 and abs(pt[0] - pt[2]) > 0.2:
            grid.append(pt)
            break


def apply_hecke(full_coeffs, pos, t_val, grid):
    ngrid = len(grid)
    nmonoms = len(monoms)
    T_vals = mpmath.matrix(ngrid, 1)
    V = mpmath.matrix(ngrid, nmonoms)
    for g in range(ngrid):
        xv = grid[g]
        f_val = eval_full(full_coeffs, xv)
        xs = list(xv)
        xs[pos], xs[pos+1] = xs[pos+1], xs[pos]
        si_f_val = eval_full(full_coeffs, xs)
        diff = f_val - si_f_val
        xi = xv[pos]
        xi1 = xv[pos+1]
        divided = diff / (xi - xi1)
        T_vals[g] = t_val * si_f_val + (t_val - 1) * xi * divided
        for idx, monom in enumerate(monoms):
            V[g, idx] = xv[0]**monom[0] * xv[1]**monom[1] * xv[2]**monom[2]
    result = mpmath.lu_solve(V, T_vals)
    return [result[i] for i in range(nmonoms)]


# Print inversion counts
print("Inversion counts:")
for mu in S_n_lambda:
    print(f"  inv({mu}) = {inversions(mu)}")

# Predicted distribution: Mallows
print(f"\nMallows prediction: pi(mu) = t^inv(mu) / [3]_t!")
print("  [3]_t! = (1+t)(1+t+t^2) = 1 + 2t + 2t^2 + t^3")


# Test at multiple t values
for t_val in [mpmath.mpf('0.4'), mpmath.mpf('0.7'), mpmath.mpf('1.5'), mpmath.mpf('3.0')]:
    print(f"\n{'='*60}")
    print(f"t = {t_val}")
    print(f"{'='*60}")

    q_val = mpmath.mpf('0.9999')
    E_coeffs = compute_E_star(q_val, t_val)
    full_E = build_full_coeffs(E_coeffs)

    # Compute f*_mu
    f_star_full = {}
    for mu, word in sorted(perms.items()):
        current = list(full_E)
        for pos in word:
            current = apply_hecke(current, pos, t_val, grid)
        f_star_full[mu] = current

    # Test at multiple x-points
    test_points = [
        [mpmath.mpf('1.5'), mpmath.mpf('0.8'), mpmath.mpf('1.2')],
        [mpmath.mpf('2.0'), mpmath.mpf('1.0'), mpmath.mpf('0.5')],
        [mpmath.mpf('0.7'), mpmath.mpf('1.3'), mpmath.mpf('0.9')],
        [mpmath.mpf('1.0'), mpmath.mpf('1.0'), mpmath.mpf('1.0')],
    ]

    # For each test point, compute C(x,t) = f*_mu / t^{inv(mu)}
    print(f"\nC(x,t) = f*_mu / t^inv(mu) — should be same for all mu at each x:")
    for xv in test_points:
        C_vals = {}
        for mu in S_n_lambda:
            f_val = eval_full(f_star_full[mu], xv)
            inv = inversions(mu)
            C_val = f_val / t_val**inv
            C_vals[mu] = C_val

        C_list = list(C_vals.values())
        C_mean = sum(C_list) / len(C_list)
        max_dev = max(abs(c - C_mean) for c in C_list) / abs(C_mean) if abs(C_mean) > 0 else 0

        print(f"  x=({float(xv[0]):.1f},{float(xv[1]):.1f},{float(xv[2]):.1f}): "
              f"C_mean={float(C_mean):.8f}, rel_dev={float(max_dev):.3e}")

    # Mallows distribution check: pi(mu) should be t^inv(mu)/[3]_t!
    n_t_fact = (1 + t_val) * (1 + t_val + t_val**2)  # [3]_t!
    print(f"\n  [3]_t! = {float(n_t_fact):.8f}")
    print(f"  Mallows prediction vs computed pi(mu) at x=(1.5, 0.8, 1.2):")

    xv = test_points[0]
    f_vals = {mu: eval_full(f_star_full[mu], xv) for mu in S_n_lambda}
    P_val = sum(f_vals.values())

    for mu in S_n_lambda:
        pi_computed = float(f_vals[mu] / P_val)
        pi_mallows = float(t_val**inversions(mu) / n_t_fact)
        err = abs(pi_computed - pi_mallows)
        print(f"    mu={mu}, inv={inversions(mu)}: computed={pi_computed:.10f}, "
              f"Mallows={pi_mallows:.10f}, err={err:.3e}")


# ====================================================================
# Also verify n=2 symbolically
# ====================================================================
print(f"\n\n{'='*70}")
print("VERIFICATION: n=2 symbolic (from EXP-3b)")
print("=" * 70)

from sympy import symbols, expand, factor, cancel, simplify, Rational, limit, Symbol

y1, y2 = symbols('y1 y2')
q_sym, t_sym = symbols('q t')

# From EXP-3b, E*_{(0,2)} was computed symbolically.
# Let me recompute the q->1 limit and factor as C(x,t) * t^{inv(mu)}.

# f*_02(q=1) from EXP-3b:
f02_q1 = y1**2 + 2*y1*y2 - 2*y1 + y2**2 - 2*y2 + 1 - 2*y1/t_sym - 2*y2/t_sym + 2/t_sym + t_sym**(-2)
# f*_20(q=1):
f20_q1 = t_sym*y1**2 + 2*t_sym*y1*y2 - 2*t_sym*y1 + t_sym*y2**2 - 2*t_sym*y2 + t_sym - 2*y1 - 2*y2 + 2 + 1/t_sym

# Check: f*_02 = C * t^0 = C, f*_20 = C * t^1
# So C = f*_02 and f*_20/t should equal f*_02
check = simplify(f20_q1 / t_sym - f02_q1)
print(f"f*_20/t - f*_02 = {check}")
if check == 0:
    print("*** f*_20 = t * f*_02, confirming f*_mu = C * t^inv(mu) ***")

# Factor C
C_factor = factor(f02_q1)
print(f"\nC(y1,y2,t) = f*_02(q=1) = {C_factor}")

# Verify C > 0 for y1, y2, t > 0
# C = (y1 + y2 - 1 - 1/t)^2 / t^2 ??
# Let me try to factor it more
C_expanded = expand(f02_q1 * t_sym**2)
print(f"t^2 * C = {C_expanded}")
C_factored2 = factor(C_expanded)
print(f"t^2 * C factored = {C_factored2}")

# Try (t*y1 + t*y2 - t - 1)^2 / t^2
test_expr = (t_sym*y1 + t_sym*y2 - t_sym - 1)**2 / t_sym**2
diff = simplify(f02_q1 - test_expr)
print(f"\nf*_02 - (t*y1+t*y2-t-1)^2/t^2 = {diff}")
if diff == 0:
    print("*** f*_02(q=1) = ((t(y1+y2) - t - 1) / t)^2 = (y1+y2-1-1/t)^2 ***")
    print("*** This is a PERFECT SQUARE! Always >= 0 ***")
    print("*** C(x,t) = (y1+y2-1-1/t)^2 ***")

# Check P*_lambda(q=1) for n=2
P_q1 = expand(f02_q1 + f20_q1)
print(f"\nP*_lambda(q=1) = {factor(P_q1)}")
print(f"  = C * (1 + t) where [2]_t! = 1 + t")

# Verify
check_P = simplify(P_q1 - f02_q1 * (1 + t_sym))
print(f"P* - C*(1+t) = {check_P}")
