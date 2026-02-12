"""
P04 CE-14: SDP-based SOS certificate for -H(w, t1, t2) >= 0.

Domain: w in (0,1), t1,t2 in (-1/12, 1/6).
Substitution: w = s/(1+s), t_i = (p_i - 1)/12 with p_i = u_i/(1+u_i)*3
  => w in (0,1) via s > 0; t_i in (-1/12, 1/6) via u_i > 0 and p_i in (0,3).

Strategy: Use Putinar's Positivstellensatz on the bounded box directly.
Since we have explicit bounds, multiply -H by products of
(w)(1-w)(t1+1/12)(1/6-t1)(t2+1/12)(1/6-t2) constraints.

Approach: SOS program via cvxpy with SDP solver.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from sympy import symbols, expand, Rational, Poly, Matrix
from itertools import product as iterproduct
import cvxpy as cp

print("P04 CE-14: SDP-based SOS certificate")
print("=" * 70)

w, t1, t2 = symbols('w t1 t2')

# H coefficients from CE-13b
A_coef = (-5184*t1**3*t2 - 864*t1**3 - 10368*t1**2*t2**2 - 2592*t1**2*t2
           - 144*t1**2 - 5184*t1*t2**3 - 2592*t1*t2**2 - 288*t1*t2
           - 864*t2**3 - 144*t2**2)

B_coef = (10368*t1**2*t2**2 + 1728*t1**2*t2 - 144*t1**2 + 10368*t1*t2**3
          + 3456*t1*t2**2 + 288*t1*t2 + 1728*t2**3 + 432*t2**2)

C_coef = (-5184*t1**2*t2**2 - 1728*t1**2*t2 - 144*t1**2 - 5184*t1*t2**3
          - 2592*t1*t2**2 - 864*t2**3 - 432*t2**2)

H_poly = A_coef * w**2 + B_coef * w + C_coef
neg_H = expand(-H_poly)

print("Target: -H(w,t1,t2) >= 0 on w in (0,1), t_i in (-1/12, 1/6)")
print(f"-H has degree 6 in 3 variables")

# ===== Approach 1: Direct SOS on shifted variables =====
# Substitute: w = w, p1 = 12*t1 + 1 in (0,3), p2 = 12*t2 + 1 in (0,3)
# Then further: w in (0,1) means w*(1-w) >= 0
#               p_i in (0,3) means p_i*(3-p_i) >= 0
# Putinar: -H = s0 + s1*w*(1-w) + s2*p1*(3-p1) + s3*p2*(3-p2)
# where s0, s1, s2, s3 are SOS polynomials.

p1, p2 = symbols('p1 p2')

# Substituted -H
neg_H_sub = neg_H.subs([(t1, (p1-1)/12), (t2, (p2-1)/12)])
neg_H_sub = expand(neg_H_sub)

# Clear denominator: multiply by 12^4 = 20736
neg_H_cleared = expand(neg_H_sub * Rational(12**4))
print(f"\n-H * 12^4 in (w, p1, p2) variables:")
neg_H_poly = Poly(neg_H_cleared, w, p1, p2)
print(f"  Total degree: {neg_H_poly.total_degree()}")
print(f"  # terms: {len(neg_H_poly.as_dict())}")

# Constraint polynomials
g1 = w * (1 - w)          # >= 0 on w in (0,1)
g2 = p1 * (3 - p1)        # >= 0 on p1 in (0,3)
g3 = p2 * (3 - p2)        # >= 0 on p2 in (0,3)

# For Putinar: -H*12^4 = sigma_0 + sigma_1 * g1 + sigma_2 * g2 + sigma_3 * g3
# where sigma_i are SOS (sum-of-squares).
#
# -H*12^4 has degree 6. g1 has degree 2, so sigma_1 can have degree 4.
# g2,g3 have degree 2, so sigma_2, sigma_3 can have degree 4.
# sigma_0 can have degree 6.

def monomial_basis(vars_list, max_degree):
    """Generate all monomials up to max_degree in given variables."""
    n = len(vars_list)
    basis = []
    for degs in iterproduct(range(max_degree + 1), repeat=n):
        if sum(degs) <= max_degree:
            mono = 1
            for v, d in zip(vars_list, degs):
                mono *= v**d
            basis.append((degs, mono))
    return basis

def poly_to_coeff_vec(poly_expr, vars_list, max_degree):
    """Convert a sympy polynomial to a coefficient vector indexed by monomials."""
    poly = Poly(expand(poly_expr), *vars_list)
    basis = monomial_basis(vars_list, max_degree)
    vec = np.zeros(len(basis))
    poly_dict = poly.as_dict()
    for i, (degs, _) in enumerate(basis):
        vec[i] = float(poly_dict.get(degs, 0))
    return vec

vars3 = [w, p1, p2]
target_deg = 6

# Build monomial basis for degree 6 (target space)
target_basis = monomial_basis(vars3, target_deg)
n_target = len(target_basis)
print(f"\nTarget monomial basis size (deg <= 6): {n_target}")

# Target coefficient vector
target_vec = poly_to_coeff_vec(neg_H_cleared, vars3, target_deg)
print(f"Target vector nonzeros: {np.count_nonzero(target_vec)}")

# SOS basis for sigma_0 (degree 6 SOS => degree 3 basis)
sos0_basis = monomial_basis(vars3, 3)
n_sos0 = len(sos0_basis)
print(f"SOS_0 basis size (deg <= 3): {n_sos0}")

# SOS basis for sigma_1, sigma_2, sigma_3 (degree 4 SOS => degree 2 basis)
sos_mult_basis = monomial_basis(vars3, 2)
n_sos_mult = len(sos_mult_basis)
print(f"SOS_mult basis size (deg <= 2): {n_sos_mult}")

def build_sos_constraint_matrix(basis, constraint_poly, vars_list, target_deg):
    """
    For sigma = v^T Q v where v is the monomial basis vector,
    sigma * constraint_poly = sum_{i,j} Q[i,j] * basis[i] * basis[j] * constraint_poly.

    Returns: list of (matrix_coeff_for_target_mono) for each target monomial.
    Each is an n_basis x n_basis matrix.
    """
    target_basis = monomial_basis(vars_list, target_deg)
    n_basis = len(basis)
    n_tgt = len(target_basis)

    # For each pair (i,j), compute basis[i]*basis[j]*constraint_poly
    # and express in target basis
    # This gives a coefficient for each target monomial

    # Build lookup from degree tuple to target index
    tgt_lookup = {}
    for idx, (degs, _) in enumerate(target_basis):
        tgt_lookup[degs] = idx

    # Result: for each target monomial k, A_k is n_basis x n_basis
    A_matrices = [np.zeros((n_basis, n_basis)) for _ in range(n_tgt)]

    for i in range(n_basis):
        for j in range(i, n_basis):
            prod = expand(basis[i][1] * basis[j][1] * constraint_poly)
            prod_poly = Poly(prod, *vars_list)
            prod_dict = prod_poly.as_dict()

            for degs, coeff in prod_dict.items():
                if degs in tgt_lookup:
                    k = tgt_lookup[degs]
                    c = float(coeff)
                    if i == j:
                        A_matrices[k][i, j] += c
                    else:
                        A_matrices[k][i, j] += c
                        A_matrices[k][j, i] += c

    return A_matrices

print("\nBuilding constraint matrices...")
print("  sigma_0 (SOS, no multiplier)...")
A0 = build_sos_constraint_matrix(sos0_basis, 1, vars3, target_deg)
print(f"  done. {len(A0)} target monomials.")

print("  sigma_1 * w*(1-w)...")
A1 = build_sos_constraint_matrix(sos_mult_basis, g1, vars3, target_deg)
print(f"  done.")

print("  sigma_2 * p1*(3-p1)...")
A2 = build_sos_constraint_matrix(sos_mult_basis, g2, vars3, target_deg)
print(f"  done.")

print("  sigma_3 * p2*(3-p2)...")
A3 = build_sos_constraint_matrix(sos_mult_basis, g3, vars3, target_deg)
print(f"  done.")

# SDP variables
Q0 = cp.Variable((n_sos0, n_sos0), symmetric=True)
Q1 = cp.Variable((n_sos_mult, n_sos_mult), symmetric=True)
Q2 = cp.Variable((n_sos_mult, n_sos_mult), symmetric=True)
Q3 = cp.Variable((n_sos_mult, n_sos_mult), symmetric=True)

# Constraints: all Q_i >> 0
constraints = [Q0 >> 0, Q1 >> 0, Q2 >> 0, Q3 >> 0]

# Equality constraints: for each target monomial k,
# trace(A0[k] @ Q0) + trace(A1[k] @ Q1) + trace(A2[k] @ Q2) + trace(A3[k] @ Q3) = target_vec[k]
print(f"\nSetting up {n_target} equality constraints...")
for k in range(n_target):
    lhs = cp.trace(A0[k] @ Q0) + cp.trace(A1[k] @ Q1) + cp.trace(A2[k] @ Q2) + cp.trace(A3[k] @ Q3)
    constraints.append(lhs == target_vec[k])

# Solve
print("Solving SDP...")
prob = cp.Problem(cp.Minimize(0), constraints)

# Try SCS first (handles large problems), then Clarabel
for solver_name in ['SCS', 'CLARABEL']:
    try:
        if solver_name == 'SCS':
            prob.solve(solver=cp.SCS, verbose=True, max_iters=50000, eps=1e-8)
        else:
            prob.solve(solver=cp.CLARABEL, verbose=True)
        print(f"\nSolver: {solver_name}")
        print(f"Status: {prob.status}")

        if prob.status in ['optimal', 'optimal_inaccurate']:
            # Verify PSD
            eig0 = np.linalg.eigvalsh(Q0.value)
            eig1 = np.linalg.eigvalsh(Q1.value)
            eig2 = np.linalg.eigvalsh(Q2.value)
            eig3 = np.linalg.eigvalsh(Q3.value)
            print(f"Q0 min eigenvalue: {eig0.min():.6e}")
            print(f"Q1 min eigenvalue: {eig1.min():.6e}")
            print(f"Q2 min eigenvalue: {eig2.min():.6e}")
            print(f"Q3 min eigenvalue: {eig3.min():.6e}")

            # Check residual
            residual = np.zeros(n_target)
            for k_idx in range(n_target):
                val = (np.trace(A0[k_idx] @ Q0.value) + np.trace(A1[k_idx] @ Q1.value)
                       + np.trace(A2[k_idx] @ Q2.value) + np.trace(A3[k_idx] @ Q3.value))
                residual[k_idx] = val - target_vec[k_idx]
            print(f"Max absolute residual: {np.max(np.abs(residual)):.6e}")
            print(f"** SOS CERTIFICATE FOUND! -H >= 0 on the bounded box. **")
            break
        elif prob.status == 'infeasible':
            print(f"SDP infeasible with {solver_name}. Putinar degree may be insufficient.")
        else:
            print(f"Solver returned: {prob.status}")
    except Exception as e:
        print(f"Solver {solver_name} failed: {e}")
else:
    print("\nAll solvers exhausted. Trying higher degree multipliers...")

    # ===== Approach 2: Higher degree multipliers =====
    # sigma_0 degree 6 (basis 3), sigma_i degree 6 (basis 3)
    # This allows higher-degree multipliers: g_i * sigma_i can have degree 8
    # But target is degree 6, so we'd need sigma_i of degree 4 (basis 2) with g_i degree 2
    # That's what we already tried. Instead try cross-constraints.

    # Try: add product constraints g1*g2, g1*g3, g2*g3
    print("\nApproach 2: Adding cross-product constraints g_i*g_j...")
    g12 = expand(g1 * g2)  # degree 4 => sigma degree 2 (basis 1)
    g13 = expand(g1 * g3)
    g23 = expand(g2 * g3)

    sos_cross_basis = monomial_basis(vars3, 1)
    n_cross = len(sos_cross_basis)
    print(f"Cross-product SOS basis size (deg <= 1): {n_cross}")

    A12 = build_sos_constraint_matrix(sos_cross_basis, g12, vars3, target_deg)
    A13 = build_sos_constraint_matrix(sos_cross_basis, g13, vars3, target_deg)
    A23 = build_sos_constraint_matrix(sos_cross_basis, g23, vars3, target_deg)

    Q0b = cp.Variable((n_sos0, n_sos0), symmetric=True)
    Q1b = cp.Variable((n_sos_mult, n_sos_mult), symmetric=True)
    Q2b = cp.Variable((n_sos_mult, n_sos_mult), symmetric=True)
    Q3b = cp.Variable((n_sos_mult, n_sos_mult), symmetric=True)
    Q12 = cp.Variable((n_cross, n_cross), symmetric=True)
    Q13 = cp.Variable((n_cross, n_cross), symmetric=True)
    Q23 = cp.Variable((n_cross, n_cross), symmetric=True)

    constraints2 = [Q0b >> 0, Q1b >> 0, Q2b >> 0, Q3b >> 0, Q12 >> 0, Q13 >> 0, Q23 >> 0]

    for k in range(n_target):
        lhs = (cp.trace(A0[k] @ Q0b) + cp.trace(A1[k] @ Q1b) + cp.trace(A2[k] @ Q2b)
               + cp.trace(A3[k] @ Q3b) + cp.trace(A12[k] @ Q12) + cp.trace(A13[k] @ Q13)
               + cp.trace(A23[k] @ Q23))
        constraints2.append(lhs == target_vec[k])

    prob2 = cp.Problem(cp.Minimize(0), constraints2)
    for solver_name in ['SCS', 'CLARABEL']:
        try:
            if solver_name == 'SCS':
                prob2.solve(solver=cp.SCS, verbose=True, max_iters=50000, eps=1e-8)
            else:
                prob2.solve(solver=cp.CLARABEL, verbose=True)
            print(f"\nApproach 2 Solver: {solver_name}")
            print(f"Status: {prob2.status}")
            if prob2.status in ['optimal', 'optimal_inaccurate']:
                print("** SOS CERTIFICATE FOUND (with cross constraints)! **")
                break
            elif prob2.status == 'infeasible':
                print("Infeasible even with cross constraints.")
        except Exception as e:
            print(f"Solver {solver_name} failed: {e}")

print("\n=== CE-14 complete ===")
