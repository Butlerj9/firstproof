"""
P03 EXP-3c: High-precision n=3 interpolation polynomials using mpmath.

Use mpmath with 80 digits of precision to compute E*_{(0,2,3)},
apply Hecke operators, and verify that ratios are exactly 1/t at q->1.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 80  # 80 decimal places

print("P03 EXP-3c: High-precision n=3 interpolation polynomials")
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


# Monomial basis: all (a,b,c) with a+b+c <= 5
monoms = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            monoms.append((a, b, c))

leading = (0, 2, 3)
leading_idx = monoms.index(leading)
unknown_monoms = [m for m in monoms if m != leading]
unknown_indices = [i for i, m in enumerate(monoms) if m != leading]

# All compositions with |nu| <= 5, excluding (0,2,3)
all_comps_le5 = []
for total in range(6):
    all_comps_le5.extend(list(compositions_of(total, 3)))
vanishing_comps = [nu for nu in all_comps_le5 if nu != lam_minus]

print(f"System: {len(vanishing_comps)} eqs, {len(unknown_monoms)} unknowns")


def compute_E_star(q, t):
    """Compute E*_{(0,2,3)} coefficient vector using mpmath."""
    nrows = len(vanishing_comps)
    ncols = len(unknown_monoms)
    A = mpmath.matrix(nrows, ncols)
    b = mpmath.matrix(nrows, 1)

    for row, nu in enumerate(vanishing_comps):
        sv = spectral_vector(nu, q, t)
        for col, monom in enumerate(unknown_monoms):
            A[row, col] = sv[0]**monom[0] * sv[1]**monom[1] * sv[2]**monom[2]
        b[row] = -(sv[0]**leading[0] * sv[1]**leading[1] * sv[2]**leading[2])

    # Solve via LU decomposition
    coeffs = mpmath.lu_solve(A, b)
    return coeffs


def eval_poly(coeffs, xv):
    """Evaluate E* at point xv = (x1, x2, x3)."""
    result = xv[1]**2 * xv[2]**3  # leading term
    for i, monom in enumerate(unknown_monoms):
        result += coeffs[i] * xv[0]**monom[0] * xv[1]**monom[1] * xv[2]**monom[2]
    return result


def build_full_coeffs(E_coeffs):
    """Build full coefficient vector (including leading = 1)."""
    full = [mpmath.mpf(0)] * len(monoms)
    full[leading_idx] = mpmath.mpf(1)
    for i, idx in enumerate(unknown_indices):
        full[idx] = E_coeffs[i]
    return full


def eval_full(full_coeffs, xv):
    """Evaluate polynomial from full coefficient vector."""
    result = mpmath.mpf(0)
    for idx, monom in enumerate(monoms):
        result += full_coeffs[idx] * xv[0]**monom[0] * xv[1]**monom[1] * xv[2]**monom[2]
    return result


def apply_hecke(full_coeffs, pos, t_val, grid):
    """Apply Hecke T_{pos} by evaluation at grid points and solve."""
    ngrid = len(grid)
    nmonoms = len(monoms)

    # Evaluate T_i f at each grid point
    T_vals = mpmath.matrix(ngrid, 1)
    V = mpmath.matrix(ngrid, nmonoms)

    for g in range(ngrid):
        xv = grid[g]
        f_val = eval_full(full_coeffs, xv)

        # s_i(x): swap x_{pos} and x_{pos+1}
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

    # Solve overdetermined system
    result = mpmath.lu_solve(V, T_vals)
    return [result[i] for i in range(nmonoms)]


# Generate grid points (need > 56 points for overdetermined system)
import random
random.seed(42)
ngrid = 80
grid = []
for _ in range(ngrid):
    while True:
        pt = [mpmath.mpf(random.uniform(0.5, 2.5)) for _ in range(3)]
        if abs(pt[0] - pt[1]) > 0.2 and abs(pt[1] - pt[2]) > 0.2 and abs(pt[0] - pt[2]) > 0.2:
            grid.append(pt)
            break

perms = {
    (0, 2, 3): [],
    (0, 3, 2): [1],
    (2, 0, 3): [0],
    (2, 3, 0): [0, 1],
    (3, 0, 2): [1, 0],
    (3, 2, 0): [0, 1, 0],
}

S_n_lambda = sorted(perms.keys())

# Test points for checking ratios
test_points = [
    [mpmath.mpf('1.5'), mpmath.mpf('0.8'), mpmath.mpf('1.2')],
    [mpmath.mpf('2.0'), mpmath.mpf('1.0'), mpmath.mpf('0.5')],
    [mpmath.mpf('0.7'), mpmath.mpf('1.3'), mpmath.mpf('0.9')],
    [mpmath.mpf('1.1'), mpmath.mpf('2.1'), mpmath.mpf('0.6')],
    [mpmath.mpf('1.0'), mpmath.mpf('1.0'), mpmath.mpf('1.0')],
]

t_val = mpmath.mpf('0.4')
inv_t = 1 / t_val

print(f"\nt = {t_val}, 1/t = {inv_t}")

for q_val in [mpmath.mpf('0.5'), mpmath.mpf('0.9'), mpmath.mpf('0.95'),
              mpmath.mpf('0.99'), mpmath.mpf('0.999'), mpmath.mpf('0.9999')]:
    print(f"\n{'='*60}")
    print(f"q = {q_val}")
    print(f"{'='*60}")

    try:
        E_coeffs = compute_E_star(q_val, t_val)
        full_E = build_full_coeffs(E_coeffs)

        # Compute f*_mu for all mu
        f_star_full = {}
        for mu, word in sorted(perms.items()):
            current = list(full_E)
            for pos in word:
                current = apply_hecke(current, pos, t_val, grid)
            f_star_full[mu] = current

        # Check ratios at multiple test points
        print(f"\nRatios f*_mu/f*_nu at test points (should be 1/t = {float(inv_t)}):")
        pairs = []
        for mu in S_n_lambda:
            for pos in range(2):
                nu = list(mu)
                nu[pos], nu[pos+1] = nu[pos+1], nu[pos]
                nu = tuple(nu)
                if nu in f_star_full and mu < nu:
                    pairs.append((mu, nu, pos))

        for mu, nu, pos in pairs:
            ratios_at_pts = []
            for xv in test_points:
                f_mu = eval_full(f_star_full[mu], xv)
                f_nu = eval_full(f_star_full[nu], xv)
                if abs(f_nu) > mpmath.mpf('1e-40'):
                    ratios_at_pts.append(f_mu / f_nu)

            if ratios_at_pts:
                mean_r = sum(ratios_at_pts) / len(ratios_at_pts)
                max_dev = max(abs(r - inv_t) for r in ratios_at_pts)
                all_match = max_dev < mpmath.mpf('1e-10')
                print(f"  {mu}/{nu} pos {pos}: mean={float(mean_r):.15f}, max|r-1/t|={float(max_dev):.3e} {'✓' if all_match else ''}")

        # Check positivity at one point
        xv = test_points[0]
        f_vals = {mu: eval_full(f_star_full[mu], xv) for mu in S_n_lambda}
        all_pos = all(v > 0 for v in f_vals.values())
        P_val = sum(f_vals.values())

        # Check symmetry
        xs0 = [xv[1], xv[0], xv[2]]
        xs1 = [xv[0], xv[2], xv[1]]
        P_s0 = sum(eval_full(f_star_full[mu], xs0) for mu in S_n_lambda)
        P_s1 = sum(eval_full(f_star_full[mu], xs1) for mu in S_n_lambda)
        sym_err = max(abs(P_val - P_s0), abs(P_val - P_s1))

        print(f"\n  P* = {float(P_val):.10f}, sym_err = {float(sym_err):.3e}, all_pos = {all_pos}")

    except Exception as e:
        print(f"  ERROR: {e}")

# ====================================================================
# Also check at q=1 with HOMOGENEOUS polynomials for comparison
# ====================================================================
print(f"\n{'='*60}")
print("COMPARISON: Homogeneous f_mu (E = x^{lam_minus})")
print(f"{'='*60}")

full_E_hom = [mpmath.mpf(0)] * len(monoms)
full_E_hom[leading_idx] = mpmath.mpf(1)

f_hom_full = {}
for mu, word in sorted(perms.items()):
    current = list(full_E_hom)
    for pos in word:
        current = apply_hecke(current, pos, t_val, grid)
    f_hom_full[mu] = current

print(f"\nRatios at test points (homogeneous, 1/t = {float(inv_t)}):")
for mu, nu, pos in pairs:
    ratios_at_pts = []
    for xv in test_points:
        f_mu = eval_full(f_hom_full[mu], xv)
        f_nu = eval_full(f_hom_full[nu], xv)
        if abs(f_nu) > mpmath.mpf('1e-40'):
            ratios_at_pts.append(f_mu / f_nu)

    if ratios_at_pts:
        mean_r = sum(ratios_at_pts) / len(ratios_at_pts)
        std_r = (sum((r - mean_r)**2 for r in ratios_at_pts) / len(ratios_at_pts))**mpmath.mpf('0.5')
        max_dev = max(abs(r - inv_t) for r in ratios_at_pts)
        print(f"  {mu}/{nu} pos {pos}: mean={float(mean_r):.10f}, std={float(std_r):.6f}, max|r-1/t|={float(max_dev):.6f}")
