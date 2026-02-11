"""
P03 EXP-3: Interpolation ASEP polynomials via Hecke operators.

Strategy:
1. Compute E*_mu (interpolation nonsymmetric Macdonald polynomial) for anti-dominant
   mu = (0,2,3) using vanishing characterization — NUMERICALLY with numpy.
2. Apply Hecke operators T_i to get f*_nu for all nu in S_3(lambda).
3. Vary q toward 1 to study the q->1 limit.
4. Check positivity and detailed balance.

Uses numpy for fast linear algebra, sympy only for polynomial manipulation.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import permutations
from fractions import Fraction

print("P03 EXP-3: Interpolation ASEP polynomials (numerical)")
print("=" * 70)

n = 3
lam = (3, 2, 0)
lam_minus = (0, 2, 3)


def spectral_vector(nu, q_val, t_val):
    """Compute numerical spectral vector."""
    result = []
    for i in range(len(nu)):
        k_i = sum(1 for j in range(i) if nu[j] > nu[i]) + \
              sum(1 for j in range(i+1, len(nu)) if nu[j] >= nu[i])
        result.append(q_val**nu[i] * t_val**(-k_i))
    return result


def compositions_of(total, nparts):
    """Generate all compositions of total into nparts non-negative parts."""
    if nparts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions_of(total - first, nparts - 1):
            yield (first,) + rest


# Monomial basis: all (a,b,c) with a+b+c <= 5
monoms = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            monoms.append((a, b, c))

# Index of leading monomial (0,2,3)
leading_idx = monoms.index((0, 2, 3))
# Separate: unknown monomials (all except leading)
unknown_monoms = [m for m in monoms if m != (0, 2, 3)]
print(f"Total monomials (degree <= 5): {len(monoms)}")
print(f"Unknown coefficients: {len(unknown_monoms)}")

# All compositions with |nu| <= 5, excluding (0,2,3)
all_comps_le5 = []
for total in range(6):
    all_comps_le5.extend(list(compositions_of(total, 3)))
vanishing_comps = [nu for nu in all_comps_le5 if nu != lam_minus]
print(f"Vanishing constraints: {len(vanishing_comps)}")


def compute_E_star(q_val, t_val):
    """Compute E*_{(0,2,3)} numerically at given q, t."""
    # Build constraint matrix: for each vanishing composition nu,
    # sum_j c_j * eval(monom_j, sv(nu)) = -eval(leading, sv(nu))
    A = np.zeros((len(vanishing_comps), len(unknown_monoms)))
    b = np.zeros(len(vanishing_comps))

    for row_idx, nu in enumerate(vanishing_comps):
        sv = spectral_vector(nu, q_val, t_val)
        for col_idx, monom in enumerate(unknown_monoms):
            A[row_idx, col_idx] = sv[0]**monom[0] * sv[1]**monom[1] * sv[2]**monom[2]
        # RHS: negative of leading monomial at spectral vector
        b[row_idx] = -(sv[0]**0 * sv[1]**2 * sv[2]**3)

    # Solve least-squares
    coeffs, residuals, rank, sv_vals = np.linalg.lstsq(A, b, rcond=None)
    return coeffs, rank


def eval_poly(coeffs, x_vals):
    """Evaluate E*_{(0,2,3)} at x_vals = (x1, x2, x3).
    coeffs are for unknown_monoms; leading monomial (0,2,3) has coeff 1.
    """
    result = x_vals[1]**2 * x_vals[2]**3  # leading term
    for i, monom in enumerate(unknown_monoms):
        result += coeffs[i] * x_vals[0]**monom[0] * x_vals[1]**monom[1] * x_vals[2]**monom[2]
    return result


def swap_poly_coeffs(coeffs, pos):
    """Swap x_{pos} <-> x_{pos+1} in the polynomial.
    Returns new coefficient vector (for unknown_monoms) and new leading coeff.

    The full polynomial is: x2^2 x3^3 + sum c_j x^{monom_j}.
    After swapping, we get a new polynomial in a different monomial basis.
    We need to re-express it in the SAME basis.

    For the full monoms list (including leading), we have a coefficient vector.
    """
    # Build full coefficient vector
    full_coeffs = np.zeros(len(monoms))
    full_coeffs[leading_idx] = 1.0
    for i, monom in enumerate(unknown_monoms):
        idx = monoms.index(monom)
        full_coeffs[idx] = coeffs[i]

    # Apply swap: x_{pos} <-> x_{pos+1}
    new_coeffs = np.zeros(len(monoms))
    for idx, monom in enumerate(monoms):
        a, b, c = monom
        if pos == 0:
            # swap x1 <-> x2: (a,b,c) -> (b,a,c)
            new_monom = (b, a, c)
        else:
            # swap x2 <-> x3: (a,b,c) -> (a,c,b)
            new_monom = (a, c, b)

        if new_monom in monoms:
            new_idx = monoms.index(new_monom)
            new_coeffs[new_idx] += full_coeffs[idx]
        # else: new monom has degree > 5, shouldn't happen for our polynomials

    return new_coeffs


def hecke_T_poly(coeffs, pos, t_val):
    """Apply Hecke operator T_{pos} to the polynomial.
    T_i f = t * s_i(f) + (t-1) * x_i / (x_i - x_{i+1}) * (f - s_i f)

    This is done coefficient-by-coefficient:
    The divided difference Delta_i(f) = (f - s_i f) / (x_i - x_{i+1})
    is a polynomial (no denominators).

    So T_i f = t * s_i(f) + (t-1) * x_i * Delta_i(f)
    """
    # Build full coefficient vector
    full_coeffs = np.zeros(len(monoms))
    full_coeffs[leading_idx] = 1.0
    for i, monom in enumerate(unknown_monoms):
        idx = monoms.index(monom)
        full_coeffs[idx] = coeffs[i]

    # Compute s_i(f): swap x_{pos} <-> x_{pos+1}
    si_full = swap_poly_coeffs(coeffs, pos)

    # Compute f - s_i(f)
    diff_full = full_coeffs - si_full

    # Compute divided difference: (f - s_i f) / (x_i - x_{i+1})
    # For a monomial x^a: (x_i^a - x_{i+1}^a)/(x_i - x_{i+1}) is computed term by term
    # But for a general polynomial, we need to do this monomial by monomial.
    #
    # Actually, let's use a different approach: evaluate at grid points and solve.
    # Or better: use the fact that x_i/(x_i - x_{i+1}) * (f - s_i f) can be computed
    # by multiplying the divided difference by x_i.
    #
    # For the divided difference of a single monomial x1^a * x2^b * x3^c under s_0 (swap x1,x2):
    # (x1^a x2^b - x1^b x2^a) / (x1 - x2)  * x3^c
    # This equals x3^c * sum_{k=0}^{max(a,b)-1} ... (symmetric function formula)
    #
    # This is getting complicated. Let me use evaluation + interpolation instead.

    pass


def eval_full_poly(full_coeffs, x_vals):
    """Evaluate polynomial from full coefficient vector."""
    result = 0.0
    for idx, monom in enumerate(monoms):
        result += full_coeffs[idx] * x_vals[0]**monom[0] * x_vals[1]**monom[1] * x_vals[2]**monom[2]
    return result


def apply_hecke_by_eval(coeffs, pos, t_val, x_grid):
    """Apply Hecke operator by evaluation and interpolation.

    1. Evaluate f and s_i(f) at grid points.
    2. Compute T_i f = t * s_i(f) + (t-1) * x_i * (f - s_i(f)) / (x_i - x_{i+1})
    3. Fit polynomial to recover coefficients.
    """
    # Build full coefficient vector for f
    full_coeffs = np.zeros(len(monoms))
    full_coeffs[leading_idx] = 1.0
    for i, monom in enumerate(unknown_monoms):
        idx = monoms.index(monom)
        full_coeffs[idx] = coeffs[i]

    # Evaluate T_i f at each grid point
    T_vals = np.zeros(len(x_grid))
    for g, x_pt in enumerate(x_grid):
        f_val = eval_full_poly(full_coeffs, x_pt)

        # s_i(x_pt): swap x_{pos} and x_{pos+1}
        x_swapped = list(x_pt)
        x_swapped[pos], x_swapped[pos+1] = x_swapped[pos+1], x_swapped[pos]
        si_f_val = eval_full_poly(full_coeffs, x_swapped)

        diff = f_val - si_f_val
        xi = x_pt[pos]
        xi1 = x_pt[pos+1]

        if abs(xi - xi1) < 1e-14:
            # L'Hopital / derivative
            T_vals[g] = t_val * si_f_val  # degenerate case
        else:
            divided = diff / (xi - xi1)
            T_vals[g] = t_val * si_f_val + (t_val - 1) * xi * divided

    # Fit polynomial: solve Vandermonde-like system
    V = np.zeros((len(x_grid), len(monoms)))
    for g, x_pt in enumerate(x_grid):
        for idx, monom in enumerate(monoms):
            V[g, idx] = x_pt[0]**monom[0] * x_pt[1]**monom[1] * x_pt[2]**monom[2]

    result_coeffs, _, _, _ = np.linalg.lstsq(V, T_vals, rcond=None)
    return result_coeffs


# Generate a grid of evaluation points (need at least len(monoms) = 56 points)
np.random.seed(42)
n_grid = 80  # more than 56 for overdetermined system
x_grid = np.random.uniform(0.5, 2.0, (n_grid, 3))
# Ensure x_i != x_{i+1} (for divided differences)
for i in range(n_grid):
    while abs(x_grid[i, 0] - x_grid[i, 1]) < 0.1 or abs(x_grid[i, 1] - x_grid[i, 2]) < 0.1:
        x_grid[i] = np.random.uniform(0.5, 2.0, 3)


# ====================================================================
# WARM-UP: n=2 case
# ====================================================================
print("\n" + "=" * 70)
print("WARM-UP: n=2, lambda=(2,0)")
print("=" * 70)

n2_monoms = []
for a in range(3):
    for b in range(3 - a):
        n2_monoms.append((a, b))
print(f"Monomials (degree <= 2, n=2): {n2_monoms}")

n2_leading_idx = n2_monoms.index((0, 2))
n2_unknown_monoms = [m for m in n2_monoms if m != (0, 2)]

n2_comps_le2 = []
for total in range(3):
    n2_comps_le2.extend(list(compositions_of(total, 2)))
n2_vanishing = [nu for nu in n2_comps_le2 if nu != (0, 2)]
print(f"Vanishing compositions (n=2): {len(n2_vanishing)}")
print(f"Unknowns: {len(n2_unknown_monoms)}")

for q_test in [0.5, 0.9, 0.99, 0.999]:
    t_test = 0.4
    A2 = np.zeros((len(n2_vanishing), len(n2_unknown_monoms)))
    b2 = np.zeros(len(n2_vanishing))
    for row_idx, nu in enumerate(n2_vanishing):
        sv = spectral_vector(nu, q_test, t_test)
        for col_idx, monom in enumerate(n2_unknown_monoms):
            A2[row_idx, col_idx] = sv[0]**monom[0] * sv[1]**monom[1]
        b2[row_idx] = -(sv[0]**0 * sv[1]**2)

    coeffs2, _, rank2, _ = np.linalg.lstsq(A2, b2, rcond=None)
    # Evaluate at a test point
    def eval_2d(coeffs, x_vals):
        result = x_vals[1]**2
        for i, monom in enumerate(n2_unknown_monoms):
            result += coeffs[i] * x_vals[0]**monom[0] * x_vals[1]**monom[1]
        return result

    x_test = [1.5, 0.8]
    val = eval_2d(coeffs2, x_test)
    print(f"  q={q_test}: rank={rank2}, E*_02(1.5, 0.8) = {val:.8f}, coeffs = {coeffs2.round(8)}")


# ====================================================================
# MAIN: n=3 case
# ====================================================================
print("\n" + "=" * 70)
print("MAIN: n=3, lambda=(3,2,0)")
print("=" * 70)

perms = {
    (0, 2, 3): [],
    (0, 3, 2): [1],
    (2, 0, 3): [0],
    (2, 3, 0): [0, 1],
    (3, 0, 2): [1, 0],
    (3, 2, 0): [0, 1, 0],
}

S_n_lambda = sorted(perms.keys())

# Test at several q values approaching 1
for q_val in [0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 0.999]:
    t_val = 0.4

    # Compute E*_{(0,2,3)}
    coeffs, rank = compute_E_star(q_val, t_val)

    # Build full coefficient vector
    full_coeffs_E = np.zeros(len(monoms))
    full_coeffs_E[leading_idx] = 1.0
    for i, monom in enumerate(unknown_monoms):
        idx = monoms.index(monom)
        full_coeffs_E[idx] = coeffs[i]

    # Apply Hecke operators to get f*_mu
    f_star_full = {}
    for mu, word in sorted(perms.items()):
        current = full_coeffs_E.copy()
        for pos in word:
            # Apply T_{pos} by evaluation
            # Need to convert current to "unknown_monoms" format? No — use full coeffs directly.
            T_vals = np.zeros(len(x_grid))
            for g, x_pt in enumerate(x_grid):
                f_val = eval_full_poly(current, x_pt)
                x_swapped = list(x_pt)
                x_swapped[pos], x_swapped[pos+1] = x_swapped[pos+1], x_swapped[pos]
                si_f_val = eval_full_poly(current, x_swapped)
                diff = f_val - si_f_val
                xi = x_pt[pos]
                xi1 = x_pt[pos+1]
                divided = diff / (xi - xi1)
                T_vals[g] = t_val * si_f_val + (t_val - 1) * xi * divided

            V = np.zeros((len(x_grid), len(monoms)))
            for g, x_pt in enumerate(x_grid):
                for idx, monom in enumerate(monoms):
                    V[g, idx] = x_pt[0]**monom[0] * x_pt[1]**monom[1] * x_pt[2]**monom[2]

            current, _, _, _ = np.linalg.lstsq(V, T_vals, rcond=None)

        f_star_full[mu] = current

    # Evaluate all f*_mu at a test point
    x_test = np.array([1.5, 0.8, 1.2])
    f_vals = {}
    for mu in S_n_lambda:
        f_vals[mu] = eval_full_poly(f_star_full[mu], x_test)

    P_val = sum(f_vals.values())
    all_pos = all(v > 0 for v in f_vals.values())

    # Check symmetry of P*: evaluate at swapped points
    x_s0 = np.array([0.8, 1.5, 1.2])  # swap x1, x2
    x_s1 = np.array([1.5, 1.2, 0.8])  # swap x2, x3
    P_s0 = sum(eval_full_poly(f_star_full[mu], x_s0) for mu in S_n_lambda)
    P_s1 = sum(eval_full_poly(f_star_full[mu], x_s1) for mu in S_n_lambda)
    sym_err = max(abs(P_val - P_s0), abs(P_val - P_s1))

    # Detailed balance ratios at the test point
    ratios = []
    for mu in S_n_lambda:
        for pos in range(2):
            nu = list(mu)
            nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
            nu = tuple(nu)
            if nu in f_vals and mu < nu:
                ratios.append((mu, nu, pos, f_vals[mu] / f_vals[nu]))

    print(f"\nq={q_val}, t={t_val}: rank={rank}, P_val={P_val:.6f}, sym_err={sym_err:.2e}, all_pos={all_pos}")
    for mu, nu, pos, r in ratios:
        t_match = "=t" if abs(r - t_val) < 1e-6 else ("=1/t" if abs(r - 1/t_val) < 1e-6 else "")
        print(f"  {mu}/{nu} (pos {pos}): {r:.8f} {t_match}")


# ====================================================================
# Comparison: homogeneous vs interpolation at q->1
# ====================================================================
print("\n" + "=" * 70)
print("Comparison: interpolation f*_mu vs homogeneous f_mu at q->1")
print("=" * 70)

# Compute homogeneous (using x^{anti-dominant} as starting point)
# For the homogeneous case, E_{(0,2,3)} = x2^2 * x3^3
hom_coeffs = np.zeros(len(monoms))
hom_leading_idx = monoms.index((0, 2, 3))
hom_coeffs[hom_leading_idx] = 1.0

t_val = 0.4

# Compute homogeneous f_mu
f_hom_full = {}
for mu, word in sorted(perms.items()):
    current = hom_coeffs.copy()
    for pos in word:
        T_vals = np.zeros(len(x_grid))
        for g, x_pt in enumerate(x_grid):
            f_val = eval_full_poly(current, x_pt)
            x_swapped = list(x_pt)
            x_swapped[pos], x_swapped[pos+1] = x_swapped[pos+1], x_swapped[pos]
            si_f_val = eval_full_poly(current, x_swapped)
            diff = f_val - si_f_val
            xi = x_pt[pos]
            xi1 = x_pt[pos+1]
            divided = diff / (xi - xi1)
            T_vals[g] = t_val * si_f_val + (t_val - 1) * xi * divided

        V = np.zeros((len(x_grid), len(monoms)))
        for g, x_pt in enumerate(x_grid):
            for idx, monom in enumerate(monoms):
                V[g, idx] = x_pt[0]**monom[0] * x_pt[1]**monom[1] * x_pt[2]**monom[2]

        current, _, _, _ = np.linalg.lstsq(V, T_vals, rcond=None)

    f_hom_full[mu] = current

# Compare at test point
x_test = np.array([1.5, 0.8, 1.2])
print(f"\nAt x = {x_test}, t = {t_val}:")
print(f"{'mu':<15} {'f_mu (hom)':>15} {'f*_mu (q=0.99)':>15} {'f*_mu (q=0.999)':>15} {'ratio hom':>12}")

# Recompute interpolation at q=0.99 and q=0.999
for q_val in [0.99, 0.999]:
    coeffs, _ = compute_E_star(q_val, t_val)
    full_coeffs_E = np.zeros(len(monoms))
    full_coeffs_E[leading_idx] = 1.0
    for i, monom in enumerate(unknown_monoms):
        idx = monoms.index(monom)
        full_coeffs_E[idx] = coeffs[i]

    f_star_full_q = {}
    for mu, word in sorted(perms.items()):
        current = full_coeffs_E.copy()
        for pos in word:
            T_vals = np.zeros(len(x_grid))
            for g, x_pt in enumerate(x_grid):
                f_val = eval_full_poly(current, x_pt)
                x_swapped = list(x_pt)
                x_swapped[pos], x_swapped[pos+1] = x_swapped[pos+1], x_swapped[pos]
                si_f_val = eval_full_poly(current, x_swapped)
                diff = f_val - si_f_val
                xi = x_pt[pos]
                xi1 = x_pt[pos+1]
                divided = diff / (xi - xi1)
                T_vals[g] = t_val * si_f_val + (t_val - 1) * xi * divided

            V = np.zeros((len(x_grid), len(monoms)))
            for g, x_pt in enumerate(x_grid):
                for idx, monom in enumerate(monoms):
                    V[g, idx] = x_pt[0]**monom[0] * x_pt[1]**monom[1] * x_pt[2]**monom[2]

            current, _, _, _ = np.linalg.lstsq(V, T_vals, rcond=None)

        f_star_full_q[mu] = current

    for mu in S_n_lambda:
        f_hom_val = eval_full_poly(f_hom_full[mu], x_test)
        f_star_val = eval_full_poly(f_star_full_q[mu], x_test)
        ratio = f_star_val / f_hom_val if abs(f_hom_val) > 1e-10 else float('inf')
        print(f"  {mu}  hom={f_hom_val:>12.6f}  interp(q={q_val})={f_star_val:>12.6f}  ratio={ratio:.6f}")


# ====================================================================
# KEY: Check if interpolation ratios become simpler at q->1
# ====================================================================
print("\n" + "=" * 70)
print("Detailed balance ratios as q -> 1 (interpolation)")
print("=" * 70)

# Multiple test points to check if ratio is x-independent
x_tests = [
    np.array([1.5, 0.8, 1.2]),
    np.array([2.0, 1.0, 0.5]),
    np.array([1.0, 1.0, 1.0]),
    np.array([0.7, 1.3, 0.9]),
]

for q_val in [0.5, 0.9, 0.99, 0.999, 0.9999]:
    coeffs, _ = compute_E_star(q_val, t_val)
    full_coeffs_E = np.zeros(len(monoms))
    full_coeffs_E[leading_idx] = 1.0
    for i, monom in enumerate(unknown_monoms):
        idx = monoms.index(monom)
        full_coeffs_E[idx] = coeffs[i]

    f_star_full_q = {}
    for mu, word in sorted(perms.items()):
        current = full_coeffs_E.copy()
        for pos in word:
            T_vals = np.zeros(len(x_grid))
            for g, x_pt in enumerate(x_grid):
                f_val = eval_full_poly(current, x_pt)
                x_swapped = list(x_pt)
                x_swapped[pos], x_swapped[pos+1] = x_swapped[pos+1], x_swapped[pos]
                si_f_val = eval_full_poly(current, x_swapped)
                diff = f_val - si_f_val
                xi = x_pt[pos]
                xi1 = x_pt[pos+1]
                divided = diff / (xi - xi1)
                T_vals[g] = t_val * si_f_val + (t_val - 1) * xi * divided

            V = np.zeros((len(x_grid), len(monoms)))
            for g, x_pt in enumerate(x_grid):
                for idx, monom in enumerate(monoms):
                    V[g, idx] = x_pt[0]**monom[0] * x_pt[1]**monom[1] * x_pt[2]**monom[2]

            current, _, _, _ = np.linalg.lstsq(V, T_vals, rcond=None)

        f_star_full_q[mu] = current

    print(f"\nq={q_val}:")
    for mu in S_n_lambda:
        for pos in range(2):
            nu = list(mu)
            nu[pos], nu[pos + 1] = nu[pos + 1], nu[pos]
            nu = tuple(nu)
            if nu in f_star_full_q and mu < nu:
                ratios_at_pts = []
                for x_pt in x_tests:
                    f_mu = eval_full_poly(f_star_full_q[mu], x_pt)
                    f_nu = eval_full_poly(f_star_full_q[nu], x_pt)
                    if abs(f_nu) > 1e-12:
                        ratios_at_pts.append(f_mu / f_nu)
                    else:
                        ratios_at_pts.append(float('nan'))

                # Check if ratio is constant (x-independent)
                r_arr = np.array(ratios_at_pts)
                std = np.std(r_arr) if not any(np.isnan(r_arr)) else float('nan')
                mean = np.mean(r_arr) if not any(np.isnan(r_arr)) else float('nan')
                const_str = "CONSTANT" if std < 1e-6 * abs(mean) else f"varies (std={std:.6f})"
                print(f"  {mu}/{nu} (pos {pos}): mean={mean:.8f}, {const_str}")
