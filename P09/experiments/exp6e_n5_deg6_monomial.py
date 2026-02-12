"""
P09 EXP-6e: Degree-6 Frobenius-product vanishing at n=5 via monomial decomposition.

Correct approach: for each A, decompose into (u_mon, v_mon) coefficients.
No multiplicity factors needed — each (p,q,r) maps to exactly one monomial pair.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations_with_replacement

np.random.seed(42)

print("P09 EXP-6e: n=5 degree-6 monomial decomposition")
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

# Extract a-index and b-index for each tuple
tuple_a = [t[0] for t in tuples]  # first free index
tuple_b = [t[1] for t in tuples]  # second free index

deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)

# Degree-6 triples
d6_triples = [(p, q, r) for p in range(n_d2)
              for q in range(p, n_d2) for r in range(q, n_d2)]
n_d6 = len(d6_triples)

# Monomial indices
u_monoms = list(combinations_with_replacement(free_indices, 6))
v_monoms = list(combinations_with_replacement(free_indices, 6))
u_idx = {m: i for i, m in enumerate(u_monoms)}
v_idx = {m: i for i, m in enumerate(v_monoms)}
n_uv = len(u_monoms) * len(v_monoms)

print(f"  n={n}, free={free_indices}, tuples={nt}")
print(f"  deg2_pairs={n_d2}, deg6_triples={n_d6}")
print(f"  u_monoms={len(u_monoms)}, v_monoms={len(v_monoms)}, n_uv={n_uv}")
print(f"  System per A: {n_uv} rows x {n_d6} cols")

# Build constraint matrix
B_all = None
for a_trial in range(30):
    np.random.seed(6200 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, tuples)

    B = np.zeros((n_uv, n_d6))
    for di, (p, q, r) in enumerate(d6_triples):
        s1, t1 = deg2_pairs[p]
        s2, t2 = deg2_pairs[q]
        s3, t3 = deg2_pairs[r]

        k_val = K[s1, t1] * K[s2, t2] * K[s3, t3]

        # u-indices: a-components of all 6 tuples involved
        u_list = sorted([tuple_a[s1], tuple_a[t1],
                         tuple_a[s2], tuple_a[t2],
                         tuple_a[s3], tuple_a[t3]])
        v_list = sorted([tuple_b[s1], tuple_b[t1],
                         tuple_b[s2], tuple_b[t2],
                         tuple_b[s3], tuple_b[t3]])

        u_mon = tuple(u_list)
        v_mon = tuple(v_list)

        if u_mon in u_idx and v_mon in v_idx:
            row = u_idx[u_mon] * len(v_monoms) + v_idx[v_mon]
            B[row, di] += k_val

    if B_all is None:
        B_all = B.copy()
    else:
        B_all = np.vstack([B_all, B])

    _, s_vals, Vt = np.linalg.svd(B_all, full_matrices=False)
    rank_B = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_d6 - rank_B

    if a_trial < 5 or a_trial % 5 == 4:
        print(f"    After A #{a_trial}: {B_all.shape[0]}x{n_d6}, "
              f"rank={rank_B}, null={null_dim}")
        sys.stdout.flush()

# Final
_, s_final, Vt_final = np.linalg.svd(B_all, full_matrices=False)
rank_final = np.sum(s_final > 1e-10 * s_final[0])
null_final = n_d6 - rank_final
print(f"\n  FINAL (n=5, deg 6): rank={rank_final}, null dim={null_final}")

if null_final > 0:
    print(f"  *** NONTRIVIAL KERNEL! dim = {null_final} ***")

    # Verify on fresh (A, rank-1 tau) — use the actual polynomial evaluation
    kernel = Vt_final[rank_final:]
    print(f"\n  Verification via polynomial evaluation:")
    for vt in range(5):
        rng = np.random.RandomState(80000 + vt)
        A_test = [rng.randn(3, 4) for _ in range(n)]
        K_test = compute_gram(A_test, tuples)

        u, v, w, x = rng.randn(n), rng.randn(n), rng.randn(n), rng.randn(n)

        # Compute Frobenius products
        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = u[T_s[0]] * v[T_s[1]] * w[T_s[2]] * x[T_s[3]]
            tau_t = u[T_t[0]] * v[T_t[1]] * w[T_t[2]] * x[T_t[3]]
            frob[pi] = tau_s * tau_t * K_test[s, t]

        # Degree-6 products
        d6_vals = np.array([frob[p] * frob[q] * frob[r] for p, q, r in d6_triples])
        results = kernel @ d6_vals
        max_abs = np.max(np.abs(results))
        print(f"    rank-1 #{vt}: max|f| = {max_abs:.3e}")

    print(f"\n  Random tau separation:")
    for vt in range(5):
        rng = np.random.RandomState(90000 + vt)
        A_test = [rng.randn(3, 4) for _ in range(n)]
        K_test = compute_gram(A_test, tuples)
        tau = rng.randn(n, n, n, n)

        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            frob[pi] = (tau[T_s[0], T_s[1], T_s[2], T_s[3]] *
                        tau[T_t[0], T_t[1], T_t[2], T_t[3]] *
                        K_test[s, t])

        d6_vals = np.array([frob[p] * frob[q] * frob[r] for p, q, r in d6_triples])
        results = kernel @ d6_vals
        max_abs = np.max(np.abs(results))
        print(f"    random #{vt}: max|f| = {max_abs:.3e}")
else:
    print(f"  *** TRIVIAL KERNEL at degree 6 ***")
    print(f"  Even degree-6 Frobenius products fail at n=5.")

print(f"\n{'='*70}")
print("DONE")
