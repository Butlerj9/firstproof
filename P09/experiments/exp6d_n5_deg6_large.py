"""
P09 EXP-6d: Direct degree-6 vanishing at n=5 with sufficient samples.

Need >> 1771 evaluation points to fully constrain the 1771-dim space.
Use 5000 (A, rank-1 tau) pairs.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
np.random.seed(42)

print("P09 EXP-6d: n=5 degree-6 with 5000 samples")
print("=" * 70)

def compute_gram(A, tuples):
    nt = len(tuples)
    Q_vecs = []
    for T in tuples:
        alpha, beta, gamma, delta = T
        v = np.zeros(81)
        idx = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        M = np.vstack([A[alpha][i,:], A[beta][j,:],
                                       A[gamma][k,:], A[delta][l,:]])
                        v[idx] = np.linalg.det(M)
                        idx += 1
        Q_vecs.append(v)
    K = np.zeros((nt, nt))
    for a in range(nt):
        for b in range(a, nt):
            K[a, b] = Q_vecs[a] @ Q_vecs[b]
            K[b, a] = K[a, b]
    return K

n = 5
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)

# Degree-6 triples
d6_triples = [(p, q, r) for p in range(n_d2)
              for q in range(p, n_d2) for r in range(q, n_d2)]
n_d6 = len(d6_triples)
print(f"  n={n}, deg2_pairs={n_d2}, deg6_triples={n_d6}")

# Build constraint rows in batches
N_SAMPLES = 4000
BATCH = 500
print(f"  Building {N_SAMPLES} constraint rows...")

rank_history = []
# Use incremental SVD via stacking
C_all = None

for batch_start in range(0, N_SAMPLES, BATCH):
    batch_end = min(batch_start + BATCH, N_SAMPLES)
    batch_rows = []

    for trial in range(batch_start, batch_end):
        rng = np.random.RandomState(trial * 7 + 1234)
        A = [rng.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)

        u = rng.randn(n)
        v = rng.randn(n)
        w = rng.randn(n)
        x = rng.randn(n)

        # Compute Frobenius products for rank-1 tau
        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = u[T_s[0]] * v[T_s[1]] * w[T_s[2]] * x[T_s[3]]
            tau_t = u[T_t[0]] * v[T_t[1]] * w[T_t[2]] * x[T_t[3]]
            frob[pi] = tau_s * tau_t * K[s, t]

        row = np.array([frob[p] * frob[q] * frob[r] for p, q, r in d6_triples])
        batch_rows.append(row)

    batch_matrix = np.array(batch_rows)
    if C_all is None:
        C_all = batch_matrix
    else:
        C_all = np.vstack([C_all, batch_matrix])

    # Compute rank (use SVD on the accumulated matrix)
    # For efficiency, compute rank via QR on the smaller dimension
    if C_all.shape[0] <= n_d6:
        _, s_vals, _ = np.linalg.svd(C_all, full_matrices=False)
    else:
        # Use thin SVD on transpose for efficiency
        _, s_vals, _ = np.linalg.svd(C_all.T, full_matrices=False)

    rank = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_d6 - rank
    print(f"    {batch_end} samples: rank={rank}/{n_d6}, null dim={null_dim}")
    sys.stdout.flush()

    rank_history.append((batch_end, rank, null_dim))

    # Early stopping if rank stabilized
    if len(rank_history) >= 3 and all(r[1] == rank for r in rank_history[-3:]):
        print(f"  Rank stabilized at {rank} after {batch_end} samples")
        break

# Final result
print(f"\n  FINAL: rank={rank}, null dim={null_dim}")

if null_dim > 0:
    print(f"  *** NONTRIVIAL KERNEL at degree 6! dim = {null_dim} ***")

    # Extract kernel
    if C_all.shape[0] <= n_d6:
        _, _, Vt = np.linalg.svd(C_all, full_matrices=True)
    else:
        _, _, Vt = np.linalg.svd(C_all.T @ C_all)
    kernel = Vt[rank:]

    # Verify
    print(f"\n  Verification on fresh data:")
    for vt in range(5):
        rng = np.random.RandomState(99000 + vt)
        A_test = [rng.randn(3, 4) for _ in range(n)]
        K_test = compute_gram(A_test, tuples)
        u2, v2, w2, x2 = rng.randn(n), rng.randn(n), rng.randn(n), rng.randn(n)

        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            frob[pi] = (u2[T_s[0]] * v2[T_s[1]] * w2[T_s[2]] * x2[T_s[3]] *
                        u2[T_t[0]] * v2[T_t[1]] * w2[T_t[2]] * x2[T_t[3]] *
                        K_test[s, t])

        vals = np.array([frob[p] * frob[q] * frob[r] for p, q, r in d6_triples])
        results = kernel @ vals
        print(f"    rank-1 #{vt}: max|f| = {np.max(np.abs(results)):.3e}")

    print(f"\n  Random tau separation:")
    for vt in range(5):
        rng = np.random.RandomState(88000 + vt)
        A_test = [rng.randn(3, 4) for _ in range(n)]
        K_test = compute_gram(A_test, tuples)
        tau = rng.randn(n, n, n, n)

        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            frob[pi] = (tau[T_s[0], T_s[1], T_s[2], T_s[3]] *
                        tau[T_t[0], T_t[1], T_t[2], T_t[3]] *
                        K_test[s, t])

        vals = np.array([frob[p] * frob[q] * frob[r] for p, q, r in d6_triples])
        results = kernel @ vals
        print(f"    random #{vt}: max|f| = {np.max(np.abs(results)):.3e}")
else:
    print(f"  *** TRIVIAL KERNEL at degree 6 ***")

print(f"\n{'='*70}")
print("DONE")
