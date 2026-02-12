"""
P09 EXP-6: Verify degree-4 vanishing at n=5 (boundary case only).

Streamlined version: only n=5, no n=7 (which requires huge SVD).
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations_with_replacement

np.random.seed(42)

print("P09 EXP-6: n=5 boundary verification (streamlined)")
print("=" * 70)

def compute_Q(A, T, i, j, k, l):
    alpha, beta, gamma, delta = T
    M = np.vstack([A[alpha][i, :], A[beta][j, :],
                    A[gamma][k, :], A[delta][l, :]])
    return np.linalg.det(M)

def compute_gram(A, tuples):
    nt = len(tuples)
    Q_vecs = []
    for T in tuples:
        v = np.zeros(81)
        idx = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        v[idx] = compute_Q(A, T, i, j, k, l)
                        idx += 1
        Q_vecs.append(v)
    K = np.zeros((nt, nt))
    for i in range(nt):
        for j in range(i, nt):
            K[i, j] = Q_vecs[i] @ Q_vecs[j]
            K[j, i] = K[i, j]
    return K

# ============================================================
# n=5 test
# ============================================================
n = 5
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)

print(f"  n={n}, free indices: {free_indices}")
print(f"  Tuples ({nt}):")
for t in tuples:
    print(f"    {t}")

# System size
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
deg4_pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
n_d4 = len(deg4_pairs)
u_monoms = list(combinations_with_replacement(free_indices, 4))
v_monoms = list(combinations_with_replacement(free_indices, 4))
n_uv = len(u_monoms) * len(v_monoms)
print(f"  System per A: {n_uv} rows x {n_d4} cols")

# Build constraint matrix from multiple A samples
B_all = None
for a_trial in range(30):
    np.random.seed(6000 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, tuples)

    # Build degree-4 constraint
    u_idx = {m: i for i, m in enumerate(u_monoms)}
    v_idx = {m: i for i, m in enumerate(v_monoms)}

    B = np.zeros((n_uv, n_d4))
    for di, (p, q) in enumerate(deg4_pairs):
        s1, t1 = deg2_pairs[p]
        s2, t2 = deg2_pairs[q]
        k_val = K[s1, t1] * K[s2, t2]
        a_list = [tuples[s1][0], tuples[t1][0], tuples[s2][0], tuples[t2][0]]
        b_list = [tuples[s1][1], tuples[t1][1], tuples[s2][1], tuples[t2][1]]
        u_mon = tuple(sorted(a_list))
        v_mon = tuple(sorted(b_list))
        if u_mon in u_idx and v_mon in v_idx:
            row = u_idx[u_mon] * len(v_monoms) + v_idx[v_mon]
            mult = 1
            if s1 != t1: mult *= 2
            if s2 != t2: mult *= 2
            if p != q: mult *= 2
            B[row, di] += k_val * mult

    if B_all is None:
        B_all = B.copy()
    else:
        B_all = np.vstack([B_all, B])

    _, s_vals, Vt = np.linalg.svd(B_all, full_matrices=True)
    rank_B = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_d4 - rank_B

    if a_trial < 5 or a_trial % 5 == 4:
        print(f"    After A #{a_trial}: stacked {B_all.shape[0]}x{n_d4}, "
              f"rank={rank_B}, null dim={null_dim}")
        sys.stdout.flush()

# Final result
_, s_final, Vt_final = np.linalg.svd(B_all, full_matrices=True)
rank_final = np.sum(s_final > 1e-10 * s_final[0])
null_final = n_d4 - rank_final
print(f"\n  FINAL (n=5): null dim = {null_final}")

if null_final > 0:
    print(f"  *** NONTRIVIAL KERNEL at n=5! Dimension = {null_final} ***")
    kernel = Vt_final[rank_final:]
    print(f"  Kernel shape: {kernel.shape}")

    # Quick rank-1 vanishing test (simplified)
    print(f"\n  Rank-1 vanishing verification (5 trials):")
    for tau_trial in range(5):
        np.random.seed(7000 + tau_trial)
        u = np.random.randn(n)
        v = np.random.randn(n)
        w = np.random.randn(n)
        x = np.random.randn(n)

        np.random.seed(8000 + tau_trial)
        A = [np.random.randn(3, 4) for _ in range(n)]

        # Build R for this (A, tau)
        K = compute_gram(A, tuples)

        # Compute Frobenius inner products for rank-1 tau
        frob_vals = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = u[T_s[0]] * v[T_s[1]] * w[T_s[2]] * x[T_s[3]]
            tau_t = u[T_t[0]] * v[T_t[1]] * w[T_t[2]] * x[T_t[3]]
            frob_vals[pi] = tau_s * tau_t * K[s, t]

        # Compute degree-4 products
        d4_vals = np.zeros(n_d4)
        for di, (p, q) in enumerate(deg4_pairs):
            d4_vals[di] = frob_vals[p] * frob_vals[q]

        # Apply kernel
        results = kernel @ d4_vals
        max_abs = np.max(np.abs(results))
        print(f"    tau #{tau_trial}: max |f(R)| = {max_abs:.3e}")

    # Random (non-rank-1) tau test
    print(f"\n  Random tau separation test (5 trials):")
    for tau_trial in range(5):
        np.random.seed(9000 + tau_trial)
        tau_full = np.random.randn(n, n, n, n)

        np.random.seed(10000 + tau_trial)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)

        # Compute Frobenius inner products for random tau
        frob_vals = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = tau_full[T_s[0], T_s[1], T_s[2], T_s[3]]
            tau_t = tau_full[T_t[0], T_t[1], T_t[2], T_t[3]]
            frob_vals[pi] = tau_s * tau_t * K[s, t]

        d4_vals = np.zeros(n_d4)
        for di, (p, q) in enumerate(deg4_pairs):
            d4_vals[di] = frob_vals[p] * frob_vals[q]

        results = kernel @ d4_vals
        max_abs = np.max(np.abs(results))
        print(f"    random tau #{tau_trial}: max |f(R)| = {max_abs:.3e}")

else:
    print(f"  *** TRIVIAL KERNEL at n=5 ***")
    print(f"  No degree-4 Frobenius-product polynomial vanishes at n=5.")
    print(f"  This is SIGNIFICANT: either D>4 for n=5 or the construction needs modification.")

print(f"\n{'='*70}")
print("CONCLUSION")
print("=" * 70)
if null_final > 0:
    print(f"  Degree-4 vanishing exists at n=5 with kernel dim = {null_final}")
    print(f"  This SUPPORTS the conjecture D=4 works for all n >= 5")
else:
    print(f"  No degree-4 vanishing at n=5 (kernel dim 0)")
    print(f"  This UNDERMINES the n-uniformity conjecture at D=4")
