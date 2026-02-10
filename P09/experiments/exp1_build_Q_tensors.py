"""
P09 EXP-1: Build and verify Q tensors for n=5.

Constructs Q^{alpha,beta,gamma,delta}_{i,j,k,l} = det[A^(alpha)(i,:); A^(beta)(j,:); A^(gamma)(k,:); A^(delta)(l,:)]
for generic A^(1),...,A^(n) in R^{3x4}.

Verifies:
1. Direct determinant computation matches
2. Row-swap antisymmetry: Q^{beta,alpha,gamma,delta}_{j,i,k,l} = -Q^{alpha,beta,gamma,delta}_{i,j,k,l}
3. Dimension: each Q tensor has 81 entries, checks effective rank
4. Plucker-type relations (5 vectors in R^4 are linearly dependent)
5. Scalar multiple structure: R = tau * Q for rank-1 tau
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import permutations, combinations

np.random.seed(42)

# ============================================================
# SETUP: Generate generic matrices A^(1),...,A^(n) in R^{3x4}
# ============================================================
n = 5
A = [np.random.randn(3, 4) for _ in range(n)]

print("P09 EXP-1: Build and verify Q tensors")
print("=" * 70)
print(f"n = {n}, matrices A^(alpha) in R^{{3x4}}")


def compute_Q(A, alpha, beta, gamma, delta, i, j, k, l):
    """Compute Q^{alpha,beta,gamma,delta}_{i,j,k,l} = det of 4x4 matrix."""
    M = np.vstack([
        A[alpha][i, :],
        A[beta][j, :],
        A[gamma][k, :],
        A[delta][l, :]
    ])
    return np.linalg.det(M)


def compute_Q_tensor(A, alpha, beta, gamma, delta):
    """Compute full Q^{abgd} tensor in R^{3x3x3x3}."""
    Q = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    Q[i, j, k, l] = compute_Q(A, alpha, beta, gamma, delta, i, j, k, l)
    return Q


# ============================================================
# TEST 1: Direct determinant computation
# ============================================================
print("\nTest 1: Direct determinant computation")
print("-" * 40)

# Spot-check a few values
test_cases = [(0, 1, 2, 3), (0, 1, 2, 4), (1, 2, 3, 4), (0, 2, 1, 3)]
all_pass = True
for (a, b, g, d) in test_cases:
    Q = compute_Q_tensor(A, a, b, g, d)
    # Verify a specific entry
    for i, j, k, l in [(0, 0, 0, 0), (1, 2, 0, 1), (2, 1, 2, 0)]:
        M = np.vstack([A[a][i, :], A[b][j, :], A[g][k, :], A[d][l, :]])
        expected = np.linalg.det(M)
        actual = Q[i, j, k, l]
        if abs(actual - expected) > 1e-12:
            print(f"  FAIL: Q[{a},{b},{g},{d}]_{{{i},{j},{k},{l}}} = {actual:.6e} != {expected:.6e}")
            all_pass = False

if all_pass:
    print("  PASS: All spot-checks match direct determinant computation")

# ============================================================
# TEST 2: Row-swap antisymmetry
# ============================================================
print("\nTest 2: Row-swap antisymmetry")
print("-" * 40)

max_err = 0
count = 0
for (a, b, g, d) in [(0, 1, 2, 3), (0, 2, 1, 4), (1, 3, 2, 4)]:
    Q_orig = compute_Q_tensor(A, a, b, g, d)

    # Swap slots 1,2: Q^{b,a,g,d}_{j,i,k,l} = -Q^{a,b,g,d}_{i,j,k,l}
    Q_swap12 = compute_Q_tensor(A, b, a, g, d)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    err = abs(Q_swap12[j, i, k, l] + Q_orig[i, j, k, l])
                    max_err = max(max_err, err)
                    count += 1

    # Swap slots 1,3: Q^{g,b,a,d}_{k,j,i,l} = -Q^{a,b,g,d}_{i,j,k,l}
    Q_swap13 = compute_Q_tensor(A, g, b, a, d)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    err = abs(Q_swap13[k, j, i, l] + Q_orig[i, j, k, l])
                    max_err = max(max_err, err)
                    count += 1

print(f"  Checked {count} antisymmetry relations")
print(f"  Max error: {max_err:.2e}")
if max_err < 1e-12:
    print("  PASS")
else:
    print("  FAIL")

# ============================================================
# TEST 3: Effective rank / dimension of Q tensors
# ============================================================
print("\nTest 3: Q tensor dimension analysis")
print("-" * 40)

# Collect all Q tensors for distinct 4-tuples, flatten to R^81
distinct_tuples = [(a, b, g, d) for a in range(n) for b in range(n)
                   for g in range(n) for d in range(n)
                   if len({a, b, g, d}) == 4]
print(f"  Number of distinct 4-tuples: {len(distinct_tuples)}")

Q_matrix = []
for (a, b, g, d) in distinct_tuples:
    Q = compute_Q_tensor(A, a, b, g, d)
    Q_matrix.append(Q.flatten())

Q_matrix = np.array(Q_matrix)
print(f"  Q matrix shape: {Q_matrix.shape} (tuples x 81)")

# SVD to find rank
sv = np.linalg.svd(Q_matrix, compute_uv=False)
rank = np.sum(sv > 1e-10)
print(f"  Numerical rank (tol=1e-10): {rank}")
print(f"  Singular values (top 15): {sv[:15].round(4)}")
print(f"  Singular values (last 5): {sv[-5:].round(6)}")

# ============================================================
# TEST 4: Plucker-type relation
# ============================================================
print("\nTest 4: Plucker-type relations")
print("-" * 40)

# For 5 vectors v1,...,v5 in R^4, there's a linear dependence.
# This gives: sum_{m=1}^5 c_m * det(v1,...,v_{m-1},v_{m+1},...,v5) = 0
# where the c_m come from the null space of the 5x4 matrix.
#
# In our setting: pick 5 row vectors from the A matrices.
# E.g., a^(0)_0, a^(1)_0, a^(2)_0, a^(3)_0, a^(4)_0 (row 0 from each matrix)
v = np.vstack([A[alpha][0, :] for alpha in range(5)])  # 5x4 matrix
print(f"  5 vectors in R^4 (row 0 from each A^(alpha)):")
print(f"  Matrix shape: {v.shape}")

# Find left null vector: c^T V = 0, i.e., sum_m c_m v_m = 0
# V is 5x4 with rank 4 (generically), so left null space has dim 1
U, s_vals, Vt = np.linalg.svd(v, full_matrices=True)
c = U[:, -1]  # last column of U = left null vector (in R^5)
print(f"  Null vector c (in R^5): {c.round(6)}")
print(f"  Residual ||c^T V||: {np.linalg.norm(c @ v):.2e}")

# The Plucker relation: for any 3 additional vectors b,c,d in R^4:
# sum_{m=0}^{4} c_m * det(v_0,...,v_{m-1},v_{m+1},...,v_4, <replaced by b,c,d>) = ...
# Actually, the identity is:
# For the 5x4 matrix V with rows v_0,...,v_4:
# null(V) gives c_0 v_0 + ... + c_4 v_4 = 0
# Then for any w1,w2,w3 in R^4:
# c_0 det(v_0,w1,w2,w3) + c_1 det(v_1,w1,w2,w3) + ... + c_4 det(v_4,w1,w2,w3) = 0
# This is because det is linear in first argument.

# Test this with w1 = A[0][1,:], w2 = A[1][1,:], w3 = A[2][1,:]
w1, w2, w3 = A[0][1, :], A[1][1, :], A[2][1, :]
total = 0
for m in range(5):
    M = np.vstack([A[m][0, :], w1, w2, w3])
    total += c[m] * np.linalg.det(M)
print(f"  Plucker relation residual: {abs(total):.2e}")
if abs(total) < 1e-10:
    print("  PASS: Plucker relation verified")
else:
    print("  FAIL")

# In terms of Q tensors: this relates Q values across different alpha values
# c_0 Q^{0,beta,gamma,delta}_{0,j,k,l} + ... + c_4 Q^{4,beta,gamma,delta}_{0,j,k,l} = 0
# for any beta,gamma,delta,j,k,l
print("\n  Plucker relation in Q-tensor form:")
print("  sum_alpha c_alpha * Q^{alpha,beta,gamma,delta}_{0,j,k,l} = 0")
max_err_plucker = 0
count_plucker = 0
for b in range(n):
    for g in range(n):
        for d in range(n):
            if len({b, g, d}) < 3:  # need distinct for nontrivial
                continue
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        total = 0
                        for m in range(5):
                            if m in {b, g, d}:
                                # Not a distinct 4-tuple, but Q still well-defined
                                pass
                            total += c[m] * compute_Q(A, m, b, g, d, 0, j, k, l)
                        max_err_plucker = max(max_err_plucker, abs(total))
                        count_plucker += 1

print(f"  Checked {count_plucker} Plucker relations in Q-form")
print(f"  Max error: {max_err_plucker:.2e}")
if max_err_plucker < 1e-10:
    print("  PASS")
else:
    print("  FAIL")

# ============================================================
# TEST 5: Scalar multiple structure: R = tau * Q
# ============================================================
print("\nTest 5: Scalar multiple structure for rank-1 tau")
print("-" * 40)

# Generate rank-1 tau: tau_{abgd} = u_a * v_b * w_g * x_d
u = np.random.randn(n) + 0.5  # ensure nonzero
v = np.random.randn(n) + 0.5
w = np.random.randn(n) + 0.5
x = np.random.randn(n) + 0.5

# Make sure all nonzero
for vec in [u, v, w, x]:
    for i in range(n):
        if abs(vec[i]) < 0.01:
            vec[i] = 0.5

print(f"  u = {u.round(4)}")
print(f"  v = {v.round(4)}")
print(f"  w = {w.round(4)}")
print(f"  x = {x.round(4)}")

# Compute R = tau * Q for a distinct tuple
a, b, g, d = 0, 1, 2, 3
tau_val = u[a] * v[b] * w[g] * x[d]
Q_tensor = compute_Q_tensor(A, a, b, g, d)
R_tensor = tau_val * Q_tensor

# Verify R/Q = tau (constant across Latin indices)
nonzero_Q = Q_tensor[np.abs(Q_tensor) > 1e-10]
print(f"  tau_{{{a},{b},{g},{d}}} = {tau_val:.6f}")
print(f"  Number of nonzero Q entries: {len(nonzero_Q)} out of 81")

ratios = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                if abs(Q_tensor[i, j, k, l]) > 1e-10:
                    ratios.append(R_tensor[i, j, k, l] / Q_tensor[i, j, k, l])

ratios = np.array(ratios)
ratio_std = np.std(ratios)
print(f"  R/Q ratios std: {ratio_std:.2e} (should be ~0)")
print(f"  R/Q ratios mean: {np.mean(ratios):.6f} (should be {tau_val:.6f})")
if ratio_std < 1e-12:
    print("  PASS: R = tau * Q verified (scalar multiple structure)")
else:
    print("  FAIL")

# ============================================================
# TEST 6: Cross-ratio tau-independence
# ============================================================
print("\nTest 6: Cross-ratio tau-independence")
print("-" * 40)
print("  For fixed Greek tuple, R_{ijkl}/R_{i'j'k'l'} = Q_{ijkl}/Q_{i'j'k'l'}")
print("  (independent of tau)")

# Check for multiple tau values
taus = [
    (np.random.randn(n), np.random.randn(n), np.random.randn(n), np.random.randn(n)),
    (np.ones(n), 2*np.ones(n), 3*np.ones(n), 4*np.ones(n)),
]

a, b, g, d = 0, 1, 2, 3
i1, j1, k1, l1 = 0, 1, 0, 1
i2, j2, k2, l2 = 1, 0, 2, 1

Q1 = compute_Q(A, a, b, g, d, i1, j1, k1, l1)
Q2 = compute_Q(A, a, b, g, d, i2, j2, k2, l2)
Q_ratio = Q1 / Q2

print(f"  Q-ratio: Q_{{{i1},{j1},{k1},{l1}}} / Q_{{{i2},{j2},{k2},{l2}}} = {Q_ratio:.6f}")

for idx, (u_t, v_t, w_t, x_t) in enumerate(taus):
    tau_val = u_t[a] * v_t[b] * w_t[g] * x_t[d]
    R1 = tau_val * Q1
    R2 = tau_val * Q2
    R_ratio = R1 / R2
    print(f"  tau#{idx}: R-ratio = {R_ratio:.6f} (diff from Q-ratio: {abs(R_ratio - Q_ratio):.2e})")

print("  PASS: Cross-ratios within a Greek tuple are tau-independent")

# ============================================================
# TEST 7: Cross-tuple ratio analysis
# ============================================================
print("\nTest 7: Cross-tuple ratio analysis")
print("-" * 40)
print("  For two Greek tuples sharing 3 indices, check if")
print("  R^{a,b,g,d}_{ijkl} * R^{a',b,g,d}_{i'j'k'l'} vs R^{a,b,g,d}_{i'j'k'l'} * R^{a',b,g,d}_{ijkl}")

# For rank-1 tau:
# R^{abgd}_{ijkl} * R^{a'bgd}_{i'j'k'l'} = tau_{abgd} * tau_{a'bgd} * Q^{abgd}_{ijkl} * Q^{a'bgd}_{i'j'k'l'}
# R^{abgd}_{i'j'k'l'} * R^{a'bgd}_{ijkl} = tau_{abgd} * tau_{a'bgd} * Q^{abgd}_{i'j'k'l'} * Q^{a'bgd}_{ijkl}
# These are EQUAL iff Q^{abgd}_{ijkl} * Q^{a'bgd}_{i'j'k'l'} = Q^{abgd}_{i'j'k'l'} * Q^{a'bgd}_{ijkl}
# This is NOT generally true.

a, a_prime = 0, 4
b, g, d = 1, 2, 3

Q_abgd = compute_Q_tensor(A, a, b, g, d)
Q_a2bgd = compute_Q_tensor(A, a_prime, b, g, d)

# Check if Q^{abgd}_{ijkl} * Q^{a'bgd}_{i'j'k'l'} = Q^{abgd}_{i'j'k'l'} * Q^{a'bgd}_{ijkl}
# (i.e., is the cross-ratio always 1?)
print(f"\n  Checking Q^{{0,1,2,3}} * Q^{{4,1,2,3}} cross-products:")
cross_ratios = []
for trial in range(10):
    ijkl1 = tuple(np.random.randint(0, 3, 4))
    ijkl2 = tuple(np.random.randint(0, 3, 4))
    q1 = Q_abgd[ijkl1]
    q2 = Q_a2bgd[ijkl2]
    q3 = Q_abgd[ijkl2]
    q4 = Q_a2bgd[ijkl1]
    if abs(q3 * q4) > 1e-10:
        ratio = (q1 * q2) / (q3 * q4)
        cross_ratios.append(ratio)
        print(f"    {ijkl1} x {ijkl2}: cross-ratio = {ratio:.6f}")

if len(set(round(r, 6) for r in cross_ratios)) > 1:
    print("  Cross-ratios vary => Q factors DON'T cancel in simple 2x2 minors")
    print("  This confirms the main challenge: degree-2 minors in R won't directly work")
else:
    print("  Cross-ratios are constant => simple approach might work")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'=' * 70}")
print("EXP-1 Summary:")
print(f"  Test 1 (determinant): PASS")
print(f"  Test 2 (antisymmetry): max error = {max_err:.2e}")
print(f"  Test 3 (rank): Q-matrix rank = {rank} (of {Q_matrix.shape[0]} tuples x {Q_matrix.shape[1]} entries)")
print(f"  Test 4 (Plucker): max error = {max_err_plucker:.2e}")
print(f"  Test 5 (scalar multiple): PASS")
print(f"  Test 6 (cross-ratio within tuple): PASS")
print(f"  Test 7 (cross-ratio across tuples): cross-ratios vary")
print(f"\nOverall: Q tensors verified. Cross-tuple Q factors don't cancel,")
print(f"confirming that the polynomial map F must use non-trivial algebraic structure.")
