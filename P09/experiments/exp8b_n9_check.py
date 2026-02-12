"""
P09 EXP-8b: Quick n=9 kernel dimension check.
Uses same monomial decomposition as EXP-8.
Tests whether kernel(m=7) = 279 (quadratic formula) or something else.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import time

np.random.seed(42)

print("P09 EXP-8b: n=9 (m=7) kernel dimension")
print("=" * 70)

n = 9
gamma, delta = 2, 3
free = sorted([i for i in range(n) if i != gamma and i != delta])
m = len(free)
tuples = [(a, b, gamma, delta) for a in free for b in free if a != b]
nt = len(tuples)

print(f"n={n}, m={m}, free={free}, tuples={nt}")

# Build pair and product indices
t0 = time.time()
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
print(f"deg2_pairs: {n_d2}")

# Build deg4 products and group by monomial simultaneously (memory efficient)
monomial_products = {}
n_d4 = 0
for p in range(n_d2):
    s1, t1 = deg2_pairs[p]
    for q in range(p, n_d2):
        s2, t2 = deg2_pairs[q]
        a_list = tuple(sorted([tuples[s1][0], tuples[t1][0],
                                tuples[s2][0], tuples[t2][0]]))
        b_list = tuple(sorted([tuples[s1][1], tuples[t1][1],
                                tuples[s2][1], tuples[t2][1]]))
        mult = 1
        if s1 != t1: mult *= 2
        if s2 != t2: mult *= 2
        if p != q: mult *= 2
        mon = (a_list, b_list)
        if mon not in monomial_products:
            monomial_products[mon] = []
        monomial_products[mon].append((s1, t1, s2, t2, mult))
        n_d4 += 1

n_mon = len(monomial_products)
sizes = [len(v) for v in monomial_products.values()]
print(f"deg4_pairs: {n_d4}")
print(f"monomials: {n_mon}, max group: {max(sizes)}, mean: {sum(sizes)/n_mon:.1f}")
print(f"grouping time: {time.time()-t0:.1f}s")


def compute_Q_vec(A, T):
    v = np.zeros(81)
    rows = [A[T[s]] for s in range(4)]
    idx = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    M = np.array([rows[0][i], rows[1][j], rows[2][k], rows[3][l]])
                    v[idx] = np.linalg.det(M)
                    idx += 1
    return v


# Compute K matrices
num_A_max = 80  # need > max group size
t0 = time.time()
K_all = []
for ai in range(num_A_max):
    np.random.seed(4000 + n * 100 + ai)
    A = [np.random.randn(3, 4) for _ in range(n)]
    Q_vecs = [compute_Q_vec(A, T) for T in tuples]
    K = np.zeros((nt, nt))
    for i in range(nt):
        for j in range(i, nt):
            K[i, j] = Q_vecs[i] @ Q_vecs[j]
            K[j, i] = K[i, j]
    K_all.append(K)
print(f"K computation ({num_A_max} A): {time.time()-t0:.1f}s")

# Convergence tracking
checkpoints = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80]

print(f"\nNeed >= {max(sizes)} A samples for convergence")
print(f"\nConvergence:")
for num_A in checkpoints:
    t0 = time.time()
    total_null = 0
    for mon, products in monomial_products.items():
        count_m = len(products)
        C = np.zeros((num_A, count_m))
        for ai in range(num_A):
            K = K_all[ai]
            for ci, (s1, t1, s2, t2, mult) in enumerate(products):
                C[ai, ci] = K[s1, t1] * K[s2, t2] * mult
        if count_m == 1:
            rank_m = 1 if np.max(np.abs(C)) > 1e-10 else 0
        else:
            s_vals = np.linalg.svd(C, compute_uv=False)
            tol = 1e-10 * s_vals[0] if s_vals[0] > 1e-10 else 1e-10
            rank_m = int(np.sum(s_vals > tol))
        total_null += count_m - rank_m
    elapsed = time.time() - t0
    print(f"  {num_A:3d} A: kernel_dim = {total_null:6d}  ({elapsed:.1f}s)")

# Predictions
quad_pred = 27 * m**2 - 207 * m + 405
cubic_pred = int(3 * m**3 - 18 * m**2 + 15 * m + 45)  # if a=3 in the cubic
print(f"\nPredictions for m={m}:")
print(f"  Quadratic (27m^2-207m+405): {quad_pred}")
print(f"  (n-3)^2: {(n-3)**2}")
print(f"  Final kernel dim: {total_null}")
print("DONE")
