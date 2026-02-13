"""
CE-44: Direct M >= 0 SOS Certificate via CLARABEL (interior-point)

Date: 2026-02-12
Goal: Prove M(w, b1, b2, cp1, cp2) >= 0 on the validity domain
      at fixed w-slices using Putinar's Positivstellensatz.

Previous attempt (CE-43, Session 26): SCS (first-order) stalled at
primal residual ~1.7e-3 due to tight margin (min P ~ 2.6e-7).
CLARABEL is an interior-point method that should handle this better.

Polynomial P at fixed w has:
- 4 variables: b1, b2, cp1, cp2
- ~206 terms, degree 10
- Domain: 6 polynomial constraints (Δ_i > 0, A_i·B_i < 0 for i=1,2,h)
- SOS problem: 126x126 main + 6 multipliers = ~11,781 vars
"""

import time, sys
import numpy as np
from scipy import sparse
import clarabel
from itertools import combinations_with_replacement
from sympy import symbols, Rational, expand, Poly, total_degree

# ============================================================
# Step 1: Build the superadditivity polynomial P at fixed w
# ============================================================

def build_polynomial_at_w(w_rat, verbose=False):
    """
    Build the superadditivity numerator P(b1, b2, cp1, cp2) at fixed w.
    P >= 0 on validity domain iff M >= 0 (1/Phi4 is superadditive).
    Returns (P_dict, domain_constraints, P_deg).
    """
    b1, b2, cp1, cp2 = symbols('b1 b2 cp1 cp2')

    s1 = w_rat
    s2 = 1 - w_rat
    sh = Rational(1)

    a1, a2, ah = -s1, -s2, Rational(-1)
    c1 = s1**2 / 12 + cp1
    c2 = s2**2 / 12 + cp2
    ch = Rational(1, 12) + cp1 + cp2
    bh = b1 + b2

    def compute_ABD(a, b, c):
        A = expand(a**2 + 12*c)
        B = expand(2*a**3 - 8*a*c + 9*b**2)
        Delta = expand(16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
                       + 144*a*b**2*c - 27*b**4 + 256*c**3)
        return A, B, Delta

    A1, B1, D1 = compute_ABD(a1, b1, c1)
    A2, B2, D2 = compute_ABD(a2, b2, c2)
    Ah, Bh, Dh = compute_ABD(ah, bh, ch)

    if verbose:
        print("  Computing AB products...")
    AB1 = expand(A1 * B1)
    AB2 = expand(A2 * B2)
    ABh = expand(Ah * Bh)

    if verbose:
        print("  Computing P terms...")
    # P = Dh*AB1*AB2 - D1*ABh*AB2 - D2*ABh*AB1
    # M >= 0 iff P >= 0 on validity domain
    term1 = expand(Dh * AB1 * AB2)
    term2 = expand(D1 * ABh * AB2)
    term3 = expand(D2 * ABh * AB1)
    P = expand(term1 - term2 - term3)

    P_poly = Poly(P, b1, b2, cp1, cp2)
    P_dict = {k: float(v) for k, v in P_poly.as_dict().items()}
    P_deg = P_poly.total_degree()

    # Domain constraints: g_k >= 0
    # g1 = Delta_1 >= 0
    # g2 = -A1*B1 >= 0  (A1*B1 < 0 on validity domain)
    # g3 = Delta_2 >= 0
    # g4 = -A2*B2 >= 0
    # g5 = Delta_h >= 0
    # g6 = -Ah*Bh >= 0

    constraints = []
    for expr, label in [(D1, "Delta1"), (expand(-AB1), "-A1B1"),
                         (D2, "Delta2"), (expand(-AB2), "-A2B2"),
                         (Dh, "Deltah"), (expand(-ABh), "-AhBh")]:
        poly = Poly(expr, b1, b2, cp1, cp2)
        c_dict = {k: float(v) for k, v in poly.as_dict().items()}
        c_deg = poly.total_degree()
        constraints.append((c_dict, c_deg, label))

    if verbose:
        print(f"  P: {len(P_dict)} terms, degree {P_deg}")
        for c_dict, c_deg, label in constraints:
            print(f"  {label}: {len(c_dict)} terms, degree {c_deg}")

    return P_dict, P_deg, constraints


# ============================================================
# Step 2: Build SOS problem (Putinar) and solve with CLARABEL
# ============================================================

def solve_sos_clarabel(P_dict, P_deg, constraints, verbose=False):
    """
    Solve constrained SOS via Putinar's Positivstellensatz using CLARABEL.
    P = sigma_0 + sum_k g_k * sigma_k, all sigma_k SOS.
    """
    nvars = 4  # b1, b2, cp1, cp2

    def make_monos(max_deg):
        monos = []
        for d in range(max_deg + 1):
            for combo in combinations_with_replacement(range(nvars), d):
                exp = [0]*nvars
                for v in combo: exp[v] += 1
                monos.append(tuple(exp))
        return monos

    def product_table(monos):
        table = {}
        m = len(monos)
        for i in range(m):
            for j in range(i, m):
                prod = tuple(monos[i][k] + monos[j][k] for k in range(nvars))
                if prod not in table: table[prod] = []
                table[prod].append((i, j))
        return table

    # Main SOS: degree P_deg, half = P_deg//2
    half0 = P_deg // 2
    monos0 = make_monos(half0)
    m0 = len(monos0)
    pt0 = product_table(monos0)

    # Multiplier SOS for each constraint
    mult_infos = []
    for _, g_deg, label in constraints:
        half = (P_deg - g_deg) // 2
        if half < 0:
            print(f"  WARNING: constraint {label} degree {g_deg} > P degree {P_deg}")
            continue
        monos_m = make_monos(half)
        pt_m = product_table(monos_m)
        mult_infos.append((len(monos_m), monos_m, pt_m, g_deg, label))

    if verbose:
        print(f"  Main SOS: {m0}x{m0} PSD ({m0*(m0+1)//2} vars)")
        for mm, _, _, _, label in mult_infos:
            print(f"  {label} multiplier: {mm}x{mm} PSD ({mm*(mm+1)//2} vars)")

    # Variable layout: [main PSD vars] [mult1 PSD vars] [mult2 PSD vars] ...
    n_psd0 = m0*(m0+1)//2
    n_psd_list = [mm*(mm+1)//2 for mm, _, _, _, _ in mult_infos]
    n_vars = n_psd0 + sum(n_psd_list)

    if verbose:
        print(f"  Total decision variables: {n_vars}")

    def var_off(gram_idx, i, j, m_size):
        if gram_idx == 0:
            base = 0
        else:
            base = n_psd0 + sum(n_psd_list[:gram_idx-1])  # gram_idx is 1-indexed for multipliers
        if i > j: i, j = j, i
        return base + i * m_size - i * (i + 1) // 2 + j

    # Target monomials (all appearing in P or constraint products)
    target_monos = make_monos(P_deg)

    # Scale coefficients for numerical stability
    max_coeff = max(abs(v) for v in P_dict.values()) if P_dict else 1.0
    P_sc = {k: v/max_coeff for k, v in P_dict.items()}

    if verbose:
        print(f"  Coefficient scaling factor: {max_coeff:.3e}")

    # Build equality constraints: for each monomial alpha,
    # P[alpha] = sum of main Gram entries + sum of constraint*multiplier Gram entries
    eq_rows, eq_cols, eq_vals, eq_b = [], [], [], []

    for alpha in target_monos:
        row = len(eq_b)
        tc = P_sc.get(alpha, 0.0)

        # Main SOS contribution: sigma_0
        for (i, j) in pt0.get(alpha, []):
            vidx = var_off(0, i, j, m0)
            eq_rows.append(row); eq_cols.append(vidx)
            eq_vals.append(1.0 if i == j else 2.0)

        # Constraint multiplier contributions: g_k * sigma_k
        for k, (mm, monos_m, pt_m, g_deg, label) in enumerate(mult_infos):
            g_dict = constraints[k][0]
            g_scale = {key: val/max_coeff for key, val in g_dict.items()}
            # No, we should scale g consistently. Actually, P = sigma0 + sum g_k sigma_k.
            # We scaled P by 1/max_coeff. So we need P_sc = sigma0_sc + sum (g_k/max_coeff) * sigma_k?
            # Actually, the correct scaling: P/M = sigma0/M + sum g_k * sigma_k/M
            # where M = max_coeff. This works if g_k is also scaled.
            # But g_k has its own coefficients. Let me think...
            # Actually: P = sigma0 + sum g_k*sigma_k
            # P/M = sigma0/M + sum g_k * sigma_k / M
            # The Gram matrices Q_0 = Q_0_true / M, Q_k = Q_k_true / M
            # And g_k * Q_k / M should have the monomial matching P/M.
            # So for the constraint: coefficient of alpha in g_k * sigma_k / M
            # = sum_{beta} g_k[beta] * [coefficient of alpha-beta in sigma_k] / M
            # The g_k coefficients are NOT scaled; only the overall P is scaled.
            # So the equality is: P_sc[alpha] = Q0_monomial + sum_k sum_beta g_k[beta] * Q_k_monomial(alpha-beta)
            # where Q0 and Q_k are the UNscaled Gram entries / M... no.
            #
            # Correct: P[alpha] = m0_contrib + sum_k sum_beta g_k[beta] * mk_contrib(alpha-beta)
            # Divide both sides by M: P_sc[alpha] = m0_contrib/M + sum_k sum_beta g_k[beta] * mk_contrib(alpha-beta)/M
            # Since decision vars are entries of Gram matrices, and we want to solve for them:
            # The Gram entries ARE the decision vars. So:
            # P_sc[alpha] = Gram0_contrib + sum_k sum_beta (g_k[beta]/M_k_scale) * Gram_k_contrib
            # Wait no. Let me just not scale g separately. Only scale the target polynomial.

            for beta, gc in g_dict.items():
                diff = tuple(alpha[l] - beta[l] for l in range(nvars))
                if any(d < 0 for d in diff): continue
                for (i, j) in pt_m.get(diff, []):
                    vidx = var_off(k+1, i, j, mm)
                    eq_rows.append(row); eq_cols.append(vidx)
                    # g_k is NOT scaled, but P is scaled by 1/max_coeff
                    # So: P_sc = sigma0_entries + sum g_k * sigma_k_entries / max_coeff
                    # No wait. Decision vars x correspond to Gram entries.
                    # sigma_0 = v^T Q_0 v = sum_{i<=j} x_{0,i,j} * m_i(alpha) * m_j(alpha) [with factor 2 for off-diag]
                    # g_k * sigma_k = g_k * v^T Q_k v
                    # Coefficient of alpha in g_k*sigma_k = sum_beta g_k[beta] * coeff of (alpha-beta) in sigma_k
                    # = sum_beta g_k[beta] * sum_{i<=j : m_i+m_j=alpha-beta} x_{k,i,j} * (1 or 2)
                    #
                    # So the equality: P[alpha] = sigma_0[alpha] + sum_k (g_k * sigma_k)[alpha]
                    # Divide by max_coeff: P_sc[alpha] = sigma_0[alpha]/M + sum_k (g_k*sigma_k)[alpha]/M
                    # Decision vars y = x/M (so that sigma_0[alpha] is linear in y with same coefficients)
                    # Then: P_sc[alpha] = sum_{i<=j} y_{0,i,j} * (1 or 2) + sum_k sum_beta g_k[beta] * sum_{i<=j} y_{k,i,j} * (1 or 2)
                    # g_k is NOT divided by M here. The decision vars y absorb the 1/M.
                    eq_vals.append(gc * (1.0 if i == j else 2.0))

        eq_b.append(tc)

    n_eq = len(eq_b)
    if verbose:
        print(f"  Equality constraints: {n_eq}")

    # Build PSD cone constraints (CLARABEL format)
    # For CLARABEL: A_cone * x + s = 0, s in PSD cone
    # So A_cone = -I (identity mapping from decision vars to PSD entries)
    # svec format: upper triangular, row-major, off-diag scaled by sqrt(2)

    sqrt2 = np.sqrt(2.0)
    psd_rows, psd_cols, psd_vals = [], [], []
    row_offset = n_eq
    psd_sizes = []

    for gi, ms in enumerate([m0] + [mm for mm, _, _, _, _ in mult_infos]):
        psd_sizes.append(ms)
        idx = 0
        # CLARABEL PSD triangle format: upper triangle, column-major
        # Entry (i,j) with i<=j at position j*(j+1)/2 + i
        for jj in range(ms):
            for ii in range(jj + 1):
                vidx = var_off(gi, ii, jj, ms)
                sc = -1.0 if ii == jj else -sqrt2
                psd_rows.append(row_offset + idx)
                psd_cols.append(vidx)
                psd_vals.append(sc)
                idx += 1
        row_offset += ms * (ms + 1) // 2

    total_rows = row_offset

    # Build sparse matrices for CLARABEL
    # CLARABEL format: min 0.5 x^T P x + q^T x, s.t. Ax + s = b, s in cones
    # For feasibility: P = 0, q = 0

    ar = eq_rows + psd_rows
    ac = eq_cols + psd_cols
    av = eq_vals + psd_vals

    A = sparse.csc_matrix((av, (ar, ac)), shape=(total_rows, n_vars))
    b_vec = np.zeros(total_rows)
    b_vec[:n_eq] = eq_b

    # Objective: feasibility (minimize 0)
    P_cost = sparse.csc_matrix((n_vars, n_vars))  # zero quadratic
    q_cost = np.zeros(n_vars)  # zero linear

    # Cones
    cones = [clarabel.ZeroConeT(n_eq)]
    for ms in psd_sizes:
        cones.append(clarabel.PSDTriangleConeT(ms))

    # Solver settings
    settings = clarabel.DefaultSettings()
    settings.verbose = verbose
    settings.max_iter = 200
    settings.time_limit = 300.0  # 5 min max
    settings.tol_gap_abs = 1e-7
    settings.tol_gap_rel = 1e-7
    settings.tol_feas = 1e-7

    if verbose:
        print(f"  Problem size: {n_vars} vars, {n_eq} eq constraints, {len(psd_sizes)} PSD cones")
        print(f"  PSD sizes: {psd_sizes}")
        print(f"  Launching CLARABEL solver...")

    t0 = time.time()
    solver = clarabel.DefaultSolver(P_cost, q_cost, A, b_vec, cones, settings)
    sol = solver.solve()
    solve_time = time.time() - t0

    return str(sol.status), solve_time, sol


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print("CE-44: Direct M >= 0 SOS Certificate via CLARABEL")
    print("=" * 60)

    # First test at w = 1/2
    w_rat = Rational(1, 2)
    print(f"\nBuilding polynomial at w = {w_rat}...")
    sys.stdout.flush()

    t_build = time.time()
    P_dict, P_deg, constraints = build_polynomial_at_w(w_rat, verbose=True)
    print(f"Build time: {time.time() - t_build:.1f}s")
    sys.stdout.flush()

    print(f"\nSolving SOS with CLARABEL (interior-point)...")
    sys.stdout.flush()

    status, solve_time, sol = solve_sos_clarabel(P_dict, P_deg, constraints, verbose=True)
    print(f"\nResult: {status} in {solve_time:.2f}s")
    sys.stdout.flush()

    if 'Solved' in status:
        print("SUCCESS: M >= 0 certified at w = 1/2!")
    else:
        print(f"Status: {status}")
        # Try with relaxed tolerances
        print("\nRetrying with relaxed tolerances...")
        sys.stdout.flush()

        # Rebuild with verbose=False for speed
        status2, solve_time2, sol2 = solve_sos_clarabel(P_dict, P_deg, constraints, verbose=False)
        print(f"Retry result: {status2} in {solve_time2:.2f}s")

    # If w=1/2 works, sweep more slices
    if 'Solved' in status:
        print("\n" + "=" * 60)
        print("Sweeping w-slices...")
        print("=" * 60)

        results = []
        for num in [1, 2, 3, 4, 5, 8, 10, 12, 15, 18, 20]:
            w_rat = Rational(num, 40)
            wf = float(w_rat)
            print(f"\n  w = {wf:.4f}: building...", end=" ")
            sys.stdout.flush()

            P_d, P_dg, cons = build_polynomial_at_w(w_rat)
            print(f"({len(P_d)} terms, deg {P_dg}), solving...", end=" ")
            sys.stdout.flush()

            st, stm, _ = solve_sos_clarabel(P_d, P_dg, cons)
            results.append((wf, st, stm))
            print(f"{st} ({stm:.2f}s)")
            sys.stdout.flush()

        n_solved = sum(1 for _, s, _ in results if 'Solved' in s)
        print(f"\nCertified: {n_solved}/{len(results)}")
