"""
P09 EXP-2: Test rank conditions on R-flattenings for rank-1 tau detection.

Key insight: R^{alpha,beta,gamma,delta}_{i,j,k,l} = tau * Q where Q = det[rows].
The determinant is linear in each row, so flattenings of R inherit rank structure.

For fixed (alpha, delta, i, l), define the matrix:
  M_{(beta,j),(gamma,k)} = R^{(alpha,beta,gamma,delta)}_{i,j,k,l}

For rank-1 tau: M = P * B * Q^T where B is 4x4 (cofactor matrix),
  P_{(beta,j),s} = v_beta * A^{(beta)}_{j,s}
  Q_{(gamma,k),t} = w_gamma * A^{(gamma)}_{k,t}
=> rank(M) <= 4.

For non-rank-1 tau: the tau_{alpha,beta,gamma,delta} factor couples beta and gamma,
potentially increasing rank beyond 4.

This experiment tests:
1. rank(M) for rank-1 tau (expect <= 4)
2. rank(M) for non-rank-1 tau (expect > 4 sometimes)
3. Whether 5x5 minors of M serve as polynomial separators
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations

np.random.seed(42)

# ============================================================
# SETUP
# ============================================================
def compute_R(A, n, tau):
    """Compute R^{abgd}_{ijkl} = tau_{abgd} * Q^{abgd}_{ijkl} for all indices."""
    R = np.zeros((n, n, n, n, 3, 3, 3, 3))
    for a in range(n):
        for b in range(n):
            for g in range(n):
                for d in range(n):
                    if len({a, b, g, d}) < 4:
                        continue  # tau = 0 for non-distinct
                    t = tau[a, b, g, d]
                    if abs(t) < 1e-15:
                        continue
                    for i in range(3):
                        for j in range(3):
                            for k in range(3):
                                for l in range(3):
                                    M = np.vstack([
                                        A[a][i, :], A[b][j, :],
                                        A[g][k, :], A[d][l, :]
                                    ])
                                    R[a, b, g, d, i, j, k, l] = t * np.linalg.det(M)
    return R


def make_rank1_tau(n):
    """Generate rank-1 tau: tau_{abgd} = u_a v_b w_g x_d for distinct (a,b,g,d)."""
    u = np.random.randn(n) + 0.5
    v = np.random.randn(n) + 0.5
    w = np.random.randn(n) + 0.5
    x = np.random.randn(n) + 0.5
    # Ensure all nonzero
    for vec in [u, v, w, x]:
        for i in range(n):
            if abs(vec[i]) < 0.1:
                vec[i] = 0.5
    tau = np.zeros((n, n, n, n))
    for a in range(n):
        for b in range(n):
            for g in range(n):
                for d in range(n):
                    if len({a, b, g, d}) == 4:
                        tau[a, b, g, d] = u[a] * v[b] * w[g] * x[d]
    return tau, u, v, w, x


def make_random_tau(n):
    """Generate random (non-rank-1) tau supported on distinct 4-tuples."""
    tau = np.zeros((n, n, n, n))
    for a in range(n):
        for b in range(n):
            for g in range(n):
                for d in range(n):
                    if len({a, b, g, d}) == 4:
                        tau[a, b, g, d] = np.random.randn()
    return tau


def build_flattening_matrix(R, n, alpha, delta, i_fix, l_fix):
    """Build the (beta,j) x (gamma,k) flattening matrix for fixed alpha,delta,i,l.

    M_{(beta,j),(gamma,k)} = R^{(alpha,beta,gamma,delta)}_{i,j,k,l}
    where beta,gamma in [n]\\{alpha,delta}, beta != gamma.
    """
    valid = [x for x in range(n) if x != alpha and x != delta]
    nv = len(valid)
    rows = [(b, j) for b in valid for j in range(3)]
    cols = [(g, k) for g in valid for k in range(3)]
    M = np.zeros((len(rows), len(cols)))
    for ri, (b, j) in enumerate(rows):
        for ci, (g, k) in enumerate(cols):
            if b == g:
                M[ri, ci] = 0  # not pairwise distinct
            else:
                M[ri, ci] = R[alpha, b, g, delta, i_fix, j, k, l_fix]
    return M, rows, cols


print("P09 EXP-2: Rank flattening test for rank-1 tau detection")
print("=" * 70)

# ============================================================
# TEST 1: n=5, rank of flattening for rank-1 vs random tau
# ============================================================
print("\nTest 1: n=5, flattening rank comparison")
print("-" * 50)

n = 5
A = [np.random.randn(3, 4) for _ in range(n)]

# Generate rank-1 tau
tau_r1, u, v, w, x = make_rank1_tau(n)
R_r1 = compute_R(A, n, tau_r1)

# Generate random tau
tau_rand = make_random_tau(n)
R_rand = compute_R(A, n, tau_rand)

print(f"  n={n}, valid beta/gamma values per (alpha,delta): {n-2}")
print(f"  Flattening matrix size: {3*(n-2)} x {3*(n-2)} = {3*(n-2)}x{3*(n-2)}")

ranks_r1 = []
ranks_rand = []

for alpha in range(n):
    for delta in range(n):
        if alpha == delta:
            continue
        for i_fix in range(3):
            for l_fix in range(3):
                M_r1, _, _ = build_flattening_matrix(R_r1, n, alpha, delta, i_fix, l_fix)
                M_rand, _, _ = build_flattening_matrix(R_rand, n, alpha, delta, i_fix, l_fix)
                sv_r1 = np.linalg.svd(M_r1, compute_uv=False)
                sv_rand = np.linalg.svd(M_rand, compute_uv=False)
                rank_r1 = np.sum(sv_r1 > 1e-10)
                rank_rand = np.sum(sv_rand > 1e-10)
                ranks_r1.append(rank_r1)
                ranks_rand.append(rank_rand)

print(f"\n  Rank-1 tau: ranks = {sorted(set(ranks_r1))}, "
      f"max={max(ranks_r1)}, min={min(ranks_r1)}")
print(f"  Random tau: ranks = {sorted(set(ranks_rand))}, "
      f"max={max(ranks_rand)}, min={min(ranks_rand)}")

if max(ranks_r1) <= 4 and max(ranks_rand) > 4:
    print("  ** SEPARATION FOUND: rank-1 => rank<=4, random => rank>4 **")
elif max(ranks_r1) <= 4:
    print("  Rank-1 has rank<=4, but random also has rank<=4 (no separation)")
else:
    print("  Rank-1 exceeds rank 4 (unexpected)")

# ============================================================
# TEST 2: n=7, same test (more rows => rank condition more powerful)
# ============================================================
print("\nTest 2: n=7, flattening rank comparison")
print("-" * 50)

n7 = 7
A7 = [np.random.randn(3, 4) for _ in range(n7)]

tau_r1_7, _, _, _, _ = make_rank1_tau(n7)
R_r1_7 = compute_R(A7, n7, tau_r1_7)

tau_rand_7 = make_random_tau(n7)
R_rand_7 = compute_R(A7, n7, tau_rand_7)

print(f"  n={n7}, valid beta/gamma values per (alpha,delta): {n7-2}")
print(f"  Flattening matrix size: {3*(n7-2)} x {3*(n7-2)} = {3*(n7-2)}x{3*(n7-2)}")

# Sample a few (alpha,delta,i,l) combinations
ranks_r1_7 = []
ranks_rand_7 = []
sample_count = 0

for alpha in range(n7):
    for delta in range(n7):
        if alpha == delta:
            continue
        for i_fix in [0, 1]:
            for l_fix in [0, 1]:
                M_r1, _, _ = build_flattening_matrix(R_r1_7, n7, alpha, delta, i_fix, l_fix)
                M_rand, _, _ = build_flattening_matrix(R_rand_7, n7, alpha, delta, i_fix, l_fix)
                sv_r1 = np.linalg.svd(M_r1, compute_uv=False)
                sv_rand = np.linalg.svd(M_rand, compute_uv=False)
                rank_r1 = np.sum(sv_r1 > 1e-10)
                rank_rand = np.sum(sv_rand > 1e-10)
                ranks_r1_7.append(rank_r1)
                ranks_rand_7.append(rank_rand)
                sample_count += 1
        if sample_count > 200:
            break
    if sample_count > 200:
        break

print(f"  Sampled {sample_count} flattening matrices")
print(f"  Rank-1 tau: ranks = {sorted(set(ranks_r1_7))}, "
      f"max={max(ranks_r1_7)}, min={min(ranks_r1_7)}")
print(f"  Random tau: ranks = {sorted(set(ranks_rand_7))}, "
      f"max={max(ranks_rand_7)}, min={min(ranks_rand_7)}")

if max(ranks_r1_7) <= 4 and max(ranks_rand_7) > 4:
    print("  ** SEPARATION FOUND: rank-1 => rank<=4, random => rank>4 **")

# ============================================================
# TEST 3: Different flattening -- fix (gamma,delta,k,l), vary (alpha,i,beta,j)
# ============================================================
print("\nTest 3: Alternative flattening (alpha,i,beta,j) x (k,l)")
print("-" * 50)
print("  For fixed gamma,delta: M_{(alpha,i,beta,j),(k,l)} = R^{abgd}_{ijkl}")
print("  This is a (n-2)^2 * 9 x 9 matrix")

n = 5

def build_alt_flattening(R, n, gamma, delta):
    """Build the (alpha,i,beta,j) x (k,l) flattening for fixed gamma,delta."""
    valid = [x for x in range(n) if x != gamma and x != delta]
    rows = [(a, i, b, j) for a in valid for b in valid
            if a != b for i in range(3) for j in range(3)]
    cols = [(k, l) for k in range(3) for l in range(3)]
    M = np.zeros((len(rows), len(cols)))
    for ri, (a, i, b, j) in enumerate(rows):
        for ci, (k, l) in enumerate(cols):
            M[ri, ci] = R[a, b, gamma, delta, i, j, k, l]
    return M

for gamma, delta in [(2, 3), (0, 4), (1, 3)]:
    M_r1 = build_alt_flattening(R_r1, n, gamma, delta)
    M_rand = build_alt_flattening(R_rand, n, gamma, delta)
    sv_r1 = np.linalg.svd(M_r1, compute_uv=False)
    sv_rand = np.linalg.svd(M_rand, compute_uv=False)
    rank_r1 = np.sum(sv_r1 > 1e-10)
    rank_rand = np.sum(sv_rand > 1e-10)
    print(f"  gamma={gamma},delta={delta}: "
          f"M is {M_r1.shape[0]}x{M_r1.shape[1]}, "
          f"rank(R1)={rank_r1}, rank(rand)={rank_rand}")

# ============================================================
# TEST 4: Plucker-based flattening (alpha,beta,i,j) x (gamma,delta,k,l)
# using Laplace expansion: det = sum of products of 2x2 minors
# ============================================================
print("\nTest 4: (1,2)|(3,4) Plucker flattening")
print("-" * 50)
print("  M_{(alpha,beta,i,j),(gamma,delta,k,l)} = R^{abgd}_{ijkl}")
print("  For rank-1 tau: rank <= 6 (Plucker dimension)")

def build_plucker_flattening(R, n):
    """Full (alpha,beta,i,j) x (gamma,delta,k,l) flattening."""
    rows = [(a, b, i, j) for a in range(n) for b in range(n)
            if a != b for i in range(3) for j in range(3)]
    cols = [(g, d, k, l) for g in range(n) for d in range(n)
            if g != d for k in range(3) for l in range(3)]
    M = np.zeros((len(rows), len(cols)))
    for ri, (a, b, i, j) in enumerate(rows):
        for ci, (g, d, k, l) in enumerate(cols):
            if len({a, b, g, d}) < 4:
                M[ri, ci] = 0
            else:
                M[ri, ci] = R[a, b, g, d, i, j, k, l]
    return M

M_r1_p = build_plucker_flattening(R_r1, n)
M_rand_p = build_plucker_flattening(R_rand, n)
sv_r1_p = np.linalg.svd(M_r1_p, compute_uv=False)
sv_rand_p = np.linalg.svd(M_rand_p, compute_uv=False)
rank_r1_p = np.sum(sv_r1_p > 1e-10)
rank_rand_p = np.sum(sv_rand_p > 1e-10)
print(f"  M shape: {M_r1_p.shape}")
print(f"  Rank-1 tau: rank = {rank_r1_p}")
print(f"  Random tau: rank = {rank_rand_p}")
print(f"  Top 10 SVs (rank-1): {sv_r1_p[:10].round(4)}")
print(f"  Top 10 SVs (random): {sv_rand_p[:10].round(4)}")

# ============================================================
# TEST 5: Multiple rank-1 and random samples, statistical analysis
# ============================================================
print("\nTest 5: Statistical analysis over multiple samples")
print("-" * 50)

n = 5
n_samples = 20
ranks_r1_all = []
ranks_rand_all = []

for trial in range(n_samples):
    np.random.seed(1000 + trial)
    A_trial = [np.random.randn(3, 4) for _ in range(n)]

    tau_r1_t, _, _, _, _ = make_rank1_tau(n)
    R_r1_t = compute_R(A_trial, n, tau_r1_t)

    tau_rand_t = make_random_tau(n)
    R_rand_t = compute_R(A_trial, n, tau_rand_t)

    # Check flattening rank for (alpha=0, delta=4, i=0, l=0)
    M_r1_t, _, _ = build_flattening_matrix(R_r1_t, n, 0, 4, 0, 0)
    M_rand_t, _, _ = build_flattening_matrix(R_rand_t, n, 0, 4, 0, 0)
    sv_r1_t = np.linalg.svd(M_r1_t, compute_uv=False)
    sv_rand_t = np.linalg.svd(M_rand_t, compute_uv=False)
    ranks_r1_all.append(np.sum(sv_r1_t > 1e-10))
    ranks_rand_all.append(np.sum(sv_rand_t > 1e-10))

print(f"  n={n}, {n_samples} trials, flattening (alpha=0,delta=4,i=0,l=0)")
print(f"  Matrix size: {3*(n-2)}x{3*(n-2)} = 9x9")
print(f"  Rank-1 tau ranks: {ranks_r1_all}")
print(f"  Random tau ranks:  {ranks_rand_all}")
print(f"  Rank-1 max: {max(ranks_r1_all)}, Random min: {min(ranks_rand_all)}")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'=' * 70}")
print("EXP-2 Summary:")
print(f"  Test 1 (n=5, all flattenings): rank-1 max={max(ranks_r1)}, "
      f"random max={max(ranks_rand)}")
print(f"  Test 2 (n=7, sampled): rank-1 max={max(ranks_r1_7)}, "
      f"random max={max(ranks_rand_7)}")
if max(ranks_r1) <= 4 and max(ranks_rand) > 4:
    print("  CONCLUSION: Rank flattening SEPARATES rank-1 from random at n=5")
    print("  Polynomial degree: 5 (5x5 minors of 9x9 matrix)")
    print("  Degree is INDEPENDENT of n => evidence for YES")
elif max(ranks_r1_7) <= 4 and max(ranks_rand_7) > 4:
    print("  CONCLUSION: Rank flattening separates at n=7 but not n=5")
    print("  Need to investigate n=5 case more carefully")
else:
    print("  CONCLUSION: Rank flattening does NOT separate")
    print("  Need alternative approach")
