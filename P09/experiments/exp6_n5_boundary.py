"""
P09 EXP-6: Verify degree-4 vanishing at n=5 (boundary case).

The main construction was verified at n=6. The n=5 case has only 3 free indices
(vs 4 at n=6), giving a smaller system. Key question: does the kernel remain
nontrivial at n=5?

Also: high-precision verification using mpmath for the n=6 kernel.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations_with_replacement

np.random.seed(42)

print("P09 EXP-6: n=5 boundary verification + high-precision n=6")
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

def build_constraint_deg4(K, tuples, free_indices):
    nt = len(tuples)
    deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
    n_d2 = len(deg2_pairs)
    deg4_pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
    n_d4 = len(deg4_pairs)

    u_monoms = list(combinations_with_replacement(free_indices, 4))
    v_monoms = list(combinations_with_replacement(free_indices, 4))
    u_idx = {m: i for i, m in enumerate(u_monoms)}
    v_idx = {m: i for i, m in enumerate(v_monoms)}
    n_uv = len(u_monoms) * len(v_monoms)

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
    return B, n_d4

# ============================================================
# PHASE 1: n=5 test
# ============================================================
print("\nPHASE 1: n=5 degree-4 vanishing")
print("-" * 60)

n = 5
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)

print(f"  n={n}, free indices: {free_indices}")
print(f"  Tuples: {nt}")
for t in tuples:
    print(f"    {t}")

# System size
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
deg4_pairs_count = n_d2 * (n_d2 + 1) // 2
u_monoms = list(combinations_with_replacement(free_indices, 4))
v_monoms = list(combinations_with_replacement(free_indices, 4))
n_uv = len(u_monoms) * len(v_monoms)
print(f"  System per A: {n_uv} rows x {deg4_pairs_count} cols")

# Sweep A samples
B_all = None
for a_trial in range(30):
    np.random.seed(6000 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, tuples)
    B, n_d4 = build_constraint_deg4(K, tuples, free_indices)

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

# Final result
_, s_final, Vt_final = np.linalg.svd(B_all, full_matrices=True)
rank_final = np.sum(s_final > 1e-10 * s_final[0])
null_final = n_d4 - rank_final
print(f"\n  FINAL (n=5): null dim = {null_final}")

if null_final > 0:
    print(f"  *** NONTRIVIAL KERNEL at n=5! Dimension = {null_final} ***")
    # Extract kernel vectors
    kernel = Vt_final[rank_final:]
    print(f"  Kernel shape: {kernel.shape}")

    # Verify: these should vanish on rank-1 tau
    print(f"\n  Verification on rank-1 tau:")
    for tau_trial in range(5):
        np.random.seed(7000 + tau_trial)
        u = np.random.randn(n)
        v = np.random.randn(n)
        w = np.random.randn(n)
        x = np.random.randn(n)
        tau = np.einsum('a,b,c,d->abcd', u, v, w, x)

        np.random.seed(8000 + tau_trial)
        A = [np.random.randn(3, 4) for _ in range(n)]

        R = np.zeros((n, n, n, n, 3, 3, 3, 3))
        for a in range(n):
            for b in range(n):
                for g in range(n):
                    for d in range(n):
                        if len({a,b,g,d}) == 4:
                            for i in range(3):
                                for j in range(3):
                                    for k in range(3):
                                        for l in range(3):
                                            R[a,b,g,d,i,j,k,l] = tau[a,b,g,d] * compute_Q(A, (a,b,g,d), i,j,k,l)

        # Compute degree-2 Frobenius products
        frob_vals = np.zeros(n_d2)
        deg2_pairs_list = [(s, t) for s in range(nt) for t in range(s, nt)]
        for pi, (s, t) in enumerate(deg2_pairs_list):
            T_s, T_t = tuples[s], tuples[t]
            val = 0.0
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        for l in range(3):
                            val += R[T_s[0],T_s[1],T_s[2],T_s[3],i,j,k,l] * \
                                   R[T_t[0],T_t[1],T_t[2],T_t[3],i,j,k,l]
            frob_vals[pi] = val

        # Compute degree-4 products
        deg4_pairs_list = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
        d4_vals = np.zeros(n_d4)
        for di, (p, q) in enumerate(deg4_pairs_list):
            d4_vals[di] = frob_vals[p] * frob_vals[q]

        # Apply kernel
        for ki in range(min(null_final, 3)):
            result = kernel[ki] @ d4_vals
            print(f"    tau #{tau_trial}, kernel vec #{ki}: f(R) = {result:.6e}")

else:
    print(f"  *** TRIVIAL KERNEL at n=5 ***")
    print(f"  No degree-4 Frobenius-product polynomial vanishes at n=5.")


# ============================================================
# PHASE 2: n=7 test (check growth)
# ============================================================
print(f"\nPHASE 2: n=7 degree-4 vanishing (growth check)")
print("-" * 60)

n = 7
free_indices_7 = [i for i in range(n) if i != 2 and i != 3]
tuples_7 = [(a, b, 2, 3) for a in free_indices_7 for b in free_indices_7
            if a != b and len({a, b, 2, 3}) == 4]
nt_7 = len(tuples_7)

deg2_pairs_7 = [(s, t) for s in range(nt_7) for t in range(s, nt_7)]
n_d2_7 = len(deg2_pairs_7)
deg4_count_7 = n_d2_7 * (n_d2_7 + 1) // 2
u_monoms_7 = list(combinations_with_replacement(free_indices_7, 4))
v_monoms_7 = list(combinations_with_replacement(free_indices_7, 4))
n_uv_7 = len(u_monoms_7) * len(v_monoms_7)

print(f"  n={n}, free indices: {free_indices_7}, tuples: {nt_7}")
print(f"  System per A: {n_uv_7} rows x {deg4_count_7} cols")

if deg4_count_7 < 50000 and n_uv_7 < 50000:
    B_all_7 = None
    for a_trial in range(20):
        np.random.seed(9000 + a_trial)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples_7)
        B, n_d4_7 = build_constraint_deg4(K, tuples_7, free_indices_7)

        if B_all_7 is None:
            B_all_7 = B.copy()
        else:
            B_all_7 = np.vstack([B_all_7, B])

        _, s_vals, _ = np.linalg.svd(B_all_7, full_matrices=True)
        rank_B = np.sum(s_vals > 1e-10 * s_vals[0])
        null_dim = n_d4_7 - rank_B

        if a_trial < 3 or a_trial % 5 == 4:
            print(f"    After A #{a_trial}: stacked {B_all_7.shape[0]}x{n_d4_7}, "
                  f"rank={rank_B}, null dim={null_dim}")

    print(f"\n  FINAL (n=7): null dim = {null_dim}")
else:
    print(f"  System too large ({n_uv_7} x {deg4_count_7}), skipping.")

print(f"\n{'='*70}")
print("CONCLUSION")
print("=" * 70)
