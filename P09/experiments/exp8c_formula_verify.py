"""
P09 EXP-8c: Verify kernel formula kernel_dim = 9 * C(m, 4) at n=10 (m=8).
Prediction: 9 * C(8, 4) = 9 * 70 = 630.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from math import comb
import time

np.random.seed(42)

print("P09 EXP-8c: Formula verification at n=10")
print("=" * 70)

n = 10
gamma, delta = 2, 3
free = sorted([i for i in range(n) if i != gamma and i != delta])
m = len(free)
tuples = [(a, b, gamma, delta) for a in free for b in free if a != b]
nt = len(tuples)

print(f"n={n}, m={m}, tuples={nt}")

# Build deg2 pairs
t0 = time.time()
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
print(f"deg2_pairs: {n_d2}")
print(f"Expected deg4_pairs: {n_d2 * (n_d2 + 1) // 2}")

# Group by monomial during construction (don't store full deg4 list)
monomial_products = {}
n_d4 = 0
for p in range(n_d2):
    s1, t1 = deg2_pairs[p]
    a_s1, b_s1 = tuples[s1][0], tuples[s1][1]
    a_t1, b_t1 = tuples[t1][0], tuples[t1][1]
    for q in range(p, n_d2):
        s2, t2 = deg2_pairs[q]
        a_list = tuple(sorted([a_s1, a_t1, tuples[s2][0], tuples[t2][0]]))
        b_list = tuple(sorted([b_s1, b_t1, tuples[s2][1], tuples[t2][1]]))
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
max_grp = max(sizes)
print(f"deg4_pairs: {n_d4}")
print(f"monomials: {n_mon}, max group: {max_grp}, mean: {sum(sizes)/n_mon:.1f}")
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


# Need enough A samples (>= max_grp)
num_A_max = max_grp + 20
print(f"\nComputing {num_A_max} K matrices...")
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
print(f"K computation: {time.time()-t0:.1f}s")

# Compute kernel dim at max A
print(f"\nComputing kernel dimension with {num_A_max} A samples...")
t0 = time.time()
total_null = 0
for mon, products in monomial_products.items():
    count_m = len(products)
    C = np.zeros((num_A_max, count_m))
    for ai in range(num_A_max):
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
print(f"Computation: {elapsed:.1f}s")

predicted = 9 * comb(m, 4)
print(f"\nResult:")
print(f"  kernel_dim = {total_null}")
print(f"  9 * C({m}, 4) = 9 * {comb(m, 4)} = {predicted}")
print(f"  Match: {'YES' if total_null == predicted else 'NO'}")

# Summary table
print(f"\n{'='*70}")
print("Complete verification table:")
print(f"{'n':>4} {'m':>4} {'kernel':>8} {'9*C(m,4)':>10} {'match':>6}")
data = [(6, 4, 9), (7, 5, 45), (8, 6, 135), (9, 7, 315), (10, 8, total_null)]
for ni, mi, ki in data:
    pred = 9 * comb(mi, 4)
    print(f"{ni:4d} {mi:4d} {ki:8d} {pred:10d} {'YES' if ki == pred else 'NO':>6}")

print(f"\nFormula: kernel_dim(degree 4, n) = 9 * C(n-2, 4) for n >= 6")
print(f"       = 3(n-2)(n-3)(n-4)(n-5)/8")
print(f"\nInterpretation:")
print(f"  Each 4-element subset of m={m} free indices contributes 9 = (4-1)^2")
print(f"  independent A-weighted 2x2 minor conditions. Total = 9 * C(m,4).")
print(f"  At n=5 (m=3): C(3,4)=0, so kernel=0 (need degree 6).")
print("DONE")
