"""
P09 EXP-6b: Test degree-6 Frobenius-product polynomials at n=5.

Since degree-4 has trivial kernel at n=5 (EXP-6), try degree-6:
products of THREE Frobenius inner products (each degree 2).

If nontrivial kernel exists, then D <= 6 is sufficient for n=5.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations_with_replacement

np.random.seed(42)

print("P09 EXP-6b: n=5 degree-6 Frobenius-product test")
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
    for a in range(nt):
        for b in range(a, nt):
            K[a, b] = Q_vecs[a] @ Q_vecs[b]
            K[b, a] = K[a, b]
    return K

# ============================================================
# n=5 setup
# ============================================================
n = 5
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)

print(f"  n={n}, free indices: {free_indices}, tuples: {nt}")

# Degree-2 pairs (Frobenius products)
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
print(f"  Degree-2 pairs: {n_d2}")

# Degree-6 triples: products of 3 Frobenius products
deg6_triples = [(p, q, r) for p in range(n_d2)
                for q in range(p, n_d2)
                for r in range(q, n_d2)]
n_d6 = len(deg6_triples)
print(f"  Degree-6 triples: {n_d6}")

# Monomial space: u_a1 * u_a2 * ... * u_a6 (6 free indices from tuples)
u_monoms = list(combinations_with_replacement(free_indices, 6))
v_monoms = list(combinations_with_replacement(free_indices, 6))
n_uv = len(u_monoms) * len(v_monoms)
print(f"  Monomial space: {len(u_monoms)} x {len(v_monoms)} = {n_uv}")
print(f"  System per A: {n_uv} rows x {n_d6} cols")

if n_d6 > 30000:
    print(f"  WARNING: large system ({n_d6} cols), may be slow")

u_idx = {m: i for i, m in enumerate(u_monoms)}
v_idx = {m: i for i, m in enumerate(v_monoms)}

# Build constraint matrix
B_all = None
for a_trial in range(25):
    np.random.seed(6100 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, tuples)

    B = np.zeros((n_uv, n_d6))
    for di, (p, q, r) in enumerate(deg6_triples):
        s1, t1 = deg2_pairs[p]
        s2, t2 = deg2_pairs[q]
        s3, t3 = deg2_pairs[r]
        k_val = K[s1, t1] * K[s2, t2] * K[s3, t3]

        # a-indices from all 6 tuple positions
        a_list = [tuples[s1][0], tuples[t1][0],
                  tuples[s2][0], tuples[t2][0],
                  tuples[s3][0], tuples[t3][0]]
        b_list = [tuples[s1][1], tuples[t1][1],
                  tuples[s2][1], tuples[t2][1],
                  tuples[s3][1], tuples[t3][1]]
        u_mon = tuple(sorted(a_list))
        v_mon = tuple(sorted(b_list))
        if u_mon in u_idx and v_mon in v_idx:
            row = u_idx[u_mon] * len(v_monoms) + v_idx[v_mon]
            # Multiplicity from symmetry
            mult = 1
            if s1 != t1: mult *= 2
            if s2 != t2: mult *= 2
            if s3 != t3: mult *= 2
            if p == q == r:
                pass  # all same
            elif p == q or q == r:
                mult *= 3  # two same
            else:
                mult *= 6  # all different
            B[row, di] += k_val * mult

    if B_all is None:
        B_all = B.copy()
    else:
        B_all = np.vstack([B_all, B])

    _, s_vals, Vt = np.linalg.svd(B_all, full_matrices=False)
    rank_B = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_d6 - rank_B

    if a_trial < 5 or a_trial % 5 == 4:
        print(f"    After A #{a_trial}: stacked {B_all.shape[0]}x{n_d6}, "
              f"rank={rank_B}, null dim={null_dim}")
        sys.stdout.flush()

# Final
_, s_final, Vt_final = np.linalg.svd(B_all, full_matrices=False)
rank_final = np.sum(s_final > 1e-10 * s_final[0])
null_final = n_d6 - rank_final
print(f"\n  FINAL (n=5, degree 6): null dim = {null_final}")

if null_final > 0:
    print(f"  *** NONTRIVIAL KERNEL! Dimension = {null_final} ***")
    print(f"  D <= 6 may suffice for n=5")

    # Quick rank-1 vanishing check
    kernel = Vt_final[rank_final:]
    print(f"\n  Rank-1 vanishing verification:")
    for tau_trial in range(3):
        np.random.seed(7100 + tau_trial)
        u = np.random.randn(n)
        v = np.random.randn(n)
        w = np.random.randn(n)
        x = np.random.randn(n)

        np.random.seed(8100 + tau_trial)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)

        frob_vals = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = u[T_s[0]] * v[T_s[1]] * w[T_s[2]] * x[T_s[3]]
            tau_t = u[T_t[0]] * v[T_t[1]] * w[T_t[2]] * x[T_t[3]]
            frob_vals[pi] = tau_s * tau_t * K[s, t]

        d6_vals = np.zeros(n_d6)
        for di, (p, q, r) in enumerate(deg6_triples):
            d6_vals[di] = frob_vals[p] * frob_vals[q] * frob_vals[r]

        results = kernel @ d6_vals
        max_abs = np.max(np.abs(results))
        print(f"    rank-1 tau #{tau_trial}: max |f(R)| = {max_abs:.3e}")

    print(f"\n  Random tau separation:")
    for tau_trial in range(3):
        np.random.seed(9100 + tau_trial)
        tau_full = np.random.randn(n, n, n, n)

        np.random.seed(10100 + tau_trial)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)

        frob_vals = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = tau_full[T_s[0], T_s[1], T_s[2], T_s[3]]
            tau_t = tau_full[T_t[0], T_t[1], T_t[2], T_t[3]]
            frob_vals[pi] = tau_s * tau_t * K[s, t]

        d6_vals = np.zeros(n_d6)
        for di, (p, q, r) in enumerate(deg6_triples):
            d6_vals[di] = frob_vals[p] * frob_vals[q] * frob_vals[r]

        results = kernel @ d6_vals
        max_abs = np.max(np.abs(results))
        print(f"    random tau #{tau_trial}: max |f(R)| = {max_abs:.3e}")
else:
    print(f"  *** TRIVIAL KERNEL at degree 6 ***")
    print(f"  Even degree-6 Frobenius products fail at n=5.")

print(f"\n{'='*70}")
print("DONE")
