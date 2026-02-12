"""
P09 EXP-6c: Direct degree-4 and degree-6 vanishing at n=5 via evaluation.

Clean approach: instead of monomial decomposition, directly evaluate
degree-D products at many random (A, rank-1 tau) pairs and find kernel.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
np.random.seed(42)

print("P09 EXP-6c: Direct evaluation approach for n=5")
print("=" * 70)

def compute_gram(A, tuples):
    """Compute Q vectors and Gram matrix K."""
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

# Setup
n = 5
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)

print(f"  n={n}, free={free_indices}, tuples={nt}, deg2_pairs={n_d2}")

# Degree-4 products (pairs of deg-2)
d4_pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
n_d4 = len(d4_pairs)

# Degree-6 products (triples of deg-2)
d6_triples = [(p, q, r) for p in range(n_d2)
              for q in range(p, n_d2) for r in range(q, n_d2)]
n_d6 = len(d6_triples)

print(f"  Degree-4 products: {n_d4}")
print(f"  Degree-6 products: {n_d6}")

def eval_products(K, tuples, deg2_pairs, tau_func, degree):
    """Evaluate all degree-D products for given K and tau."""
    n_d2 = len(deg2_pairs)

    # Compute Frobenius products
    frob = np.zeros(n_d2)
    for pi, (s, t) in enumerate(deg2_pairs):
        frob[pi] = tau_func(tuples[s]) * tau_func(tuples[t]) * K[s, t]

    if degree == 4:
        pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
        vals = np.array([frob[p] * frob[q] for p, q in pairs])
    elif degree == 6:
        triples = [(p, q, r) for p in range(n_d2)
                   for q in range(p, n_d2) for r in range(q, n_d2)]
        vals = np.array([frob[p] * frob[q] * frob[r] for p, q, r in triples])
    return vals

# ============================================================
# Build constraint matrix by evaluating at many (A, rank-1 tau)
# ============================================================
for degree, n_prod, label in [(4, n_d4, "Degree-4"), (6, n_d6, "Degree-6")]:
    print(f"\n{label} ({n_prod} products)")
    print("-" * 60)

    rows = []
    for trial in range(200):
        np.random.seed(5000 + trial * 7)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)

        np.random.seed(6000 + trial * 13)
        u = np.random.randn(n)
        v = np.random.randn(n)
        w = np.random.randn(n)
        x = np.random.randn(n)

        def tau_rank1(T):
            return u[T[0]] * v[T[1]] * w[T[2]] * x[T[3]]

        row = eval_products(K, tuples, deg2_pairs, tau_rank1, degree)
        rows.append(row)

    C = np.array(rows)
    print(f"  Constraint matrix: {C.shape}")

    _, s_vals, Vt = np.linalg.svd(C, full_matrices=True)
    rank = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_prod - rank
    print(f"  Rank: {rank}, Null dim: {null_dim}")

    if null_dim > 0:
        kernel = Vt[rank:]
        print(f"  *** NONTRIVIAL KERNEL: dim = {null_dim} ***")

        # Verify on fresh rank-1 tau
        print(f"  Verification on 5 fresh (A, rank-1 tau):")
        for vt in range(5):
            np.random.seed(20000 + vt * 31)
            A_test = [np.random.randn(3, 4) for _ in range(n)]
            K_test = compute_gram(A_test, tuples)

            np.random.seed(30000 + vt * 37)
            u2 = np.random.randn(n)
            v2 = np.random.randn(n)
            w2 = np.random.randn(n)
            x2 = np.random.randn(n)

            def tau_r1(T):
                return u2[T[0]] * v2[T[1]] * w2[T[2]] * x2[T[3]]

            vals = eval_products(K_test, tuples, deg2_pairs, tau_r1, degree)
            results = kernel @ vals
            print(f"    trial {vt}: max|f| = {np.max(np.abs(results)):.3e}")

        # Test random (non-rank-1) tau
        print(f"  Separation on 5 random tau:")
        for vt in range(5):
            np.random.seed(40000 + vt * 41)
            A_test = [np.random.randn(3, 4) for _ in range(n)]
            K_test = compute_gram(A_test, tuples)

            np.random.seed(50000 + vt * 43)
            tau_rand = np.random.randn(n, n, n, n)

            def tau_gen(T):
                return tau_rand[T[0], T[1], T[2], T[3]]

            vals = eval_products(K_test, tuples, deg2_pairs, tau_gen, degree)
            results = kernel @ vals
            print(f"    trial {vt}: max|f| = {np.max(np.abs(results)):.3e}")
    else:
        print(f"  *** TRIVIAL KERNEL ***")

print(f"\n{'='*70}")
print("DONE")
