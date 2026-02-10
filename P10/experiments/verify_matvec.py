"""
P10 Verification: Matrix-free matvec vs explicit A*vec(W)
Tests on toy dimensions: n=4, r=2, q=8, M=6, d=3
Expected: matrix-free matvec matches explicit computation to machine precision.
"""
import numpy as np
np.random.seed(42)

# Dimensions
n = 4   # mode-k size
r = 2   # CP rank
d = 3   # tensor order
# Mode sizes for other modes (arbitrary, product = M)
other_sizes = [3, 2]  # so M = 6
M = int(np.prod(other_sizes))
N = n * M  # = 24
q = 8   # observed entries (subset of N)
lam = 0.5  # regularization

print(f"n={n}, r={r}, M={M}, N={N}, q={q}, d={d}")

# Generate random factor matrices for other modes
A_others = [np.random.randn(sz, r) for sz in other_sizes]

# Khatri-Rao product Z (M x r) - explicit construction for verification
# Z = A_others[1] odot A_others[0] (Khatri-Rao = column-wise Kronecker)
# For d=3 with mode k=1 (0-indexed): Z = A_3 odot A_2
# Khatri-Rao: Z[j, :] = A_others[0][j0, :] * A_others[1][j1, :]
# where j = j0 * other_sizes[1] + j1 (column-major of other indices)
Z = np.zeros((M, r))
for j0 in range(other_sizes[0]):
    for j1 in range(other_sizes[1]):
        j = j1 * other_sizes[0] + j0  # column-major ordering
        Z[j, :] = A_others[0][j0, :] * A_others[1][j1, :]

print(f"Z shape: {Z.shape}")

# SPD kernel matrix K (n x n)
K_half = np.random.randn(n, n)
K = K_half @ K_half.T + 0.1 * np.eye(n)  # ensure SPD

# Selection matrix S: pick q random positions from N
observed_indices = np.sort(np.random.choice(N, q, replace=False))
S = np.zeros((N, q))
for p_idx, obs_idx in enumerate(observed_indices):
    S[obs_idx, p_idx] = 1.0

# Convert observed positions to (i, j) in the n x M unfolding (column-major)
obs_i = observed_indices % n   # row index (mode-k index)
obs_j = observed_indices // n  # column index (multi-index into Z)

print(f"Observed positions (i,j): {list(zip(obs_i, obs_j))}")

# Unknown W
W = np.random.randn(n, r)
vec_W = W.flatten(order='F')  # column-major vectorization

# ============================================================
# METHOD 1: Explicit A*vec(W)
# ============================================================
# A = (Z kron K)^T S S^T (Z kron K) + lambda (I_r kron K)
ZkronK = np.kron(Z, K)  # N x nr
SST = S @ S.T           # N x N (diagonal)
A_explicit = ZkronK.T @ SST @ ZkronK + lam * np.kron(np.eye(r), K)
y_explicit = A_explicit @ vec_W

print(f"\nExplicit A shape: {A_explicit.shape}")
print(f"A is symmetric: {np.allclose(A_explicit, A_explicit.T)}")
eigvals = np.linalg.eigvalsh(A_explicit)
print(f"A eigenvalues (min, max): ({eigvals.min():.6f}, {eigvals.max():.6f})")
print(f"A is SPD: {eigvals.min() > 0}")

# ============================================================
# METHOD 2: Matrix-free matvec
# ============================================================
def matrix_free_matvec(W_input, K, obs_i, obs_j, Z_rows_func, lam, n, r, q):
    """
    Compute A * vec(W) without forming any N-dimensional object.

    W_input: n x r matrix
    K: n x n SPD kernel
    obs_i: array of mode-k indices for each observation
    obs_j: array of multi-indices for each observation
    Z_rows_func: function(j) -> r-vector (row j of Z, computed on the fly)
    lam: regularization
    """
    # Step 1: U = K @ W
    U = K @ W_input  # n x r, cost O(n^2 r)

    # Step 2: Accumulate C from observations
    C = np.zeros((n, r))
    for p in range(q):
        z_p = Z_rows_func(obs_j[p])     # r-vector, cost O((d-1)*r)
        y_p = U[obs_i[p], :] @ z_p      # scalar, cost O(r)
        C[obs_i[p], :] += y_p * z_p     # cost O(r)

    # Step 3: D = K @ C
    D = K @ C  # n x r, cost O(n^2 r)

    # Step 4: Add regularization: lambda * K @ W = lambda * U
    result = D + lam * U  # n x r

    return result.flatten(order='F')

# Z row accessor (in practice, computed from factor matrices via Hadamard)
def get_Z_row(j):
    return Z[j, :]

y_matfree = matrix_free_matvec(W, K, obs_i, obs_j, get_Z_row, lam, n, r, q)

# ============================================================
# COMPARE
# ============================================================
error = np.linalg.norm(y_explicit - y_matfree)
rel_error = error / np.linalg.norm(y_explicit)
print(f"\n=== COMPARISON ===")
print(f"||y_explicit - y_matfree|| = {error:.2e}")
print(f"Relative error = {rel_error:.2e}")
print(f"MATCH: {rel_error < 1e-12}")

# ============================================================
# VERIFY RHS computation
# ============================================================
# B = T @ Z where T is mode-k unfolding with zeros at missing entries
# RHS = vec(K @ B)
# But we compute B from observations without forming T

# Create T (mode-k unfolding) for verification
T_tensor = np.random.randn(n, M)
# Zero out unobserved entries
T_masked = np.zeros_like(T_tensor)
for p in range(q):
    T_masked[obs_i[p], obs_j[p]] = T_tensor[obs_i[p], obs_j[p]]

B_explicit = T_masked @ Z  # n x r
rhs_explicit = (np.kron(np.eye(r), K) @ B_explicit.flatten(order='F'))

# Matrix-free RHS
B_matfree = np.zeros((n, r))
for p in range(q):
    z_p = get_Z_row(obs_j[p])
    t_p = T_tensor[obs_i[p], obs_j[p]]  # observed value
    B_matfree[obs_i[p], :] += t_p * z_p
rhs_matfree = (K @ B_matfree).flatten(order='F')

rhs_error = np.linalg.norm(rhs_explicit - rhs_matfree) / np.linalg.norm(rhs_explicit)
print(f"\n=== RHS COMPARISON ===")
print(f"Relative error = {rhs_error:.2e}")
print(f"MATCH: {rhs_error < 1e-12}")

# ============================================================
# VERIFY Gram identity: Z^T Z = Hadamard of (A_j^T A_j)
# ============================================================
ZTZ_explicit = Z.T @ Z
ZTZ_hadamard = np.ones((r, r))
for A_j in A_others:
    ZTZ_hadamard *= (A_j.T @ A_j)

gram_error = np.linalg.norm(ZTZ_explicit - ZTZ_hadamard) / np.linalg.norm(ZTZ_explicit)
print(f"\n=== GRAM IDENTITY ===")
print(f"Z^T Z (explicit):\n{ZTZ_explicit}")
print(f"Hadamard of Grams:\n{ZTZ_hadamard}")
print(f"Relative error = {gram_error:.2e}")
print(f"MATCH: {gram_error < 1e-12}")

# ============================================================
# VERIFY PCG convergence
# ============================================================
from scipy.sparse.linalg import LinearOperator, cg

def matvec_callback(v):
    V = v.reshape((n, r), order='F')
    return matrix_free_matvec(V, K, obs_i, obs_j, get_Z_row, lam, n, r, q)

A_op = LinearOperator((n*r, n*r), matvec=matvec_callback)

# Solve with CG (no preconditioner)
rhs = rhs_matfree
x_cg, info = cg(A_op, rhs, atol=1e-10, maxiter=100)
print(f"\n=== PCG (no preconditioner) ===")
print(f"CG converged: {info == 0} (info={info})")

# Compare with direct solve
x_direct = np.linalg.solve(A_explicit, rhs_explicit)
solve_error = np.linalg.norm(x_cg - x_direct) / np.linalg.norm(x_direct)
print(f"||x_cg - x_direct|| / ||x_direct|| = {solve_error:.2e}")
print(f"MATCH: {solve_error < 1e-8}")

# ============================================================
# VERIFY Preconditioner B (Cholesky of K)
# ============================================================
L_chol = np.linalg.cholesky(K)

def precond_B(v):
    """Preconditioner: M = lambda * (I_r kron K). Apply M^{-1}."""
    V = v.reshape((n, r), order='F')
    # Solve K @ Y = V for each column
    Y = np.linalg.solve(K, V)
    return (Y / lam).flatten(order='F')

M_precond = LinearOperator((n*r, n*r), matvec=precond_B)
x_pcg, info_pcg = cg(A_op, rhs, M=M_precond, atol=1e-10, maxiter=100)
print(f"\n=== PCG (preconditioner B: lambda*I_r kron K) ===")
print(f"PCG converged: {info_pcg == 0} (info={info_pcg})")
pcg_error = np.linalg.norm(x_pcg - x_direct) / np.linalg.norm(x_direct)
print(f"||x_pcg - x_direct|| / ||x_direct|| = {pcg_error:.2e}")
print(f"MATCH: {pcg_error < 1e-8}")

# ============================================================
# VERIFY Preconditioner A (Kronecker approximation)
# ============================================================
rho = q / N
G = ZTZ_hadamard  # r x r
# M_A = rho * (G kron K^2) + lambda * (I_r kron K)
# Diagonalize: K = V Lambda V^T, G = U Sigma U^T
eigvals_K, V_K = np.linalg.eigh(K)
eigvals_G, U_G = np.linalg.eigh(G)

def precond_A(v):
    """Preconditioner A: rho*(G kron K^2) + lambda*(I_r kron K)."""
    X = v.reshape((n, r), order='F')
    # Transform: X_tilde = V_K^T @ X @ U_G
    X_tilde = V_K.T @ X @ U_G
    # Divide by diagonal: rho * sigma_j * lambda_i^2 + lambda * lambda_i
    for i in range(n):
        for j in range(r):
            denom = rho * eigvals_G[j] * eigvals_K[i]**2 + lam * eigvals_K[i]
            X_tilde[i, j] /= denom
    # Back-transform
    result = V_K @ X_tilde @ U_G.T
    return result.flatten(order='F')

M_precond_A = LinearOperator((n*r, n*r), matvec=precond_A)
x_pcgA, info_pcgA = cg(A_op, rhs, M=M_precond_A, atol=1e-10, maxiter=100)
print(f"\n=== PCG (preconditioner A: Kronecker approx) ===")
print(f"PCG converged: {info_pcgA == 0} (info={info_pcgA})")
pcgA_error = np.linalg.norm(x_pcgA - x_direct) / np.linalg.norm(x_direct)
print(f"||x_pcgA - x_direct|| / ||x_direct|| = {pcgA_error:.2e}")
print(f"MATCH: {pcgA_error < 1e-8}")

print("\n" + "="*60)
print("ALL TESTS PASSED" if all([
    rel_error < 1e-12,
    rhs_error < 1e-12,
    gram_error < 1e-12,
    solve_error < 1e-8,
    pcg_error < 1e-8,
    pcgA_error < 1e-8,
]) else "SOME TESTS FAILED")
print("="*60)
