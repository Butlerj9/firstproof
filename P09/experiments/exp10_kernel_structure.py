"""
P09 EXP-10: Kernel structure decomposition.

Goal: For each (u,v) monomial, determine whether it contributes to the kernel.
Classify monomials by:
  - Are a-indices all distinct? (4-element subset of [m])
  - Are b-indices all distinct?
  - Is a-set == b-set?
  - What is the per-monomial kernel dimension?

This helps formalize the kernel formula 9*C(m,4) by identifying the structural
pattern behind which monomials contribute.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from collections import Counter
import time

np.random.seed(42)

print("P09 EXP-10: Kernel structure decomposition")
print("=" * 70)


def compute_Q_vec(A, T):
    """Compute Q^T as flat 81-vector."""
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


def compute_gram(A, tuples):
    """Compute K_{s,t} = <Q^s, Q^t>."""
    Q_vecs = [compute_Q_vec(A, T) for T in tuples]
    nt = len(tuples)
    K = np.zeros((nt, nt))
    for i in range(nt):
        for j in range(i, nt):
            K[i, j] = Q_vecs[i] @ Q_vecs[j]
            K[j, i] = K[i, j]
    return K


def analyze_kernel_structure(n, gamma, delta, num_A=30):
    """Decompose kernel by monomial and classify each monomial's contribution."""
    free = sorted([i for i in range(n) if i != gamma and i != delta])
    m = len(free)
    tuples = [(a, b, gamma, delta) for a in free for b in free if a != b]
    nt = len(tuples)

    # Build pair and product indices
    deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
    n_d2 = len(deg2_pairs)
    deg4_pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
    n_d4 = len(deg4_pairs)

    print(f"\n  n={n}, m={m}, free={free}")
    print(f"  tuples: {nt}, deg2_pairs: {n_d2}, deg4_pairs: {n_d4}")

    # Group products by (u,v) monomial
    monomial_products = {}
    for di, (p, q) in enumerate(deg4_pairs):
        s1, t1 = deg2_pairs[p]
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

    n_mon = len(monomial_products)
    print(f"  monomials: {n_mon}")

    # Compute K matrices
    t0 = time.time()
    K_all = []
    for ai in range(num_A):
        np.random.seed(4000 + n * 100 + ai)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)
        K_all.append(K)
    print(f"  K computation ({num_A} A): {time.time()-t0:.1f}s")

    # Classify each monomial
    results = []
    total_kernel = 0

    for mon, products in monomial_products.items():
        a_list, b_list = mon
        count_m = len(products)

        # Build constraint matrix
        C = np.zeros((num_A, count_m))
        for ai in range(num_A):
            K = K_all[ai]
            for ci, (s1, t1, s2, t2, mult) in enumerate(products):
                C[ai, ci] = K[s1, t1] * K[s2, t2] * mult

        # Compute rank
        if count_m == 1:
            rank_m = 1 if np.max(np.abs(C)) > 1e-10 else 0
        else:
            s_vals = np.linalg.svd(C, compute_uv=False)
            tol = 1e-10 * s_vals[0] if s_vals[0] > 1e-10 else 1e-10
            rank_m = int(np.sum(s_vals > tol))

        kernel_m = count_m - rank_m

        # Classify monomial type
        a_distinct = len(set(a_list)) == 4
        b_distinct = len(set(b_list)) == 4
        a_set = tuple(sorted(set(a_list)))
        b_set = tuple(sorted(set(b_list)))
        same_set = (a_set == b_set) if (a_distinct and b_distinct) else None

        results.append({
            'mon': mon,
            'a_list': a_list,
            'b_list': b_list,
            'a_distinct': a_distinct,
            'b_distinct': b_distinct,
            'same_set': same_set,
            'products': count_m,
            'rank': rank_m,
            'kernel': kernel_m
        })
        total_kernel += kernel_m

    # Print summary by category
    print(f"\n  Total kernel: {total_kernel}")
    print(f"  Expected (9*C(m,4)): {9 * max(0, m*(m-1)*(m-2)*(m-3)//24)}")

    # Categorize
    cats = {
        'both_distinct_same': [],
        'both_distinct_diff': [],
        'a_only_distinct': [],
        'b_only_distinct': [],
        'neither_distinct': []
    }

    for r in results:
        if r['a_distinct'] and r['b_distinct']:
            if r['same_set']:
                cats['both_distinct_same'].append(r)
            else:
                cats['both_distinct_diff'].append(r)
        elif r['a_distinct']:
            cats['a_only_distinct'].append(r)
        elif r['b_distinct']:
            cats['b_only_distinct'].append(r)
        else:
            cats['neither_distinct'].append(r)

    print(f"\n  Category breakdown:")
    for cat_name, cat_list in cats.items():
        if not cat_list:
            continue
        total_k = sum(r['kernel'] for r in cat_list)
        n_with_kernel = sum(1 for r in cat_list if r['kernel'] > 0)
        print(f"    {cat_name}: {len(cat_list)} monomials, "
              f"{n_with_kernel} with nonzero kernel, total kernel = {total_k}")

    # Detail: list all monomials with nonzero kernel
    nonzero = [r for r in results if r['kernel'] > 0]
    print(f"\n  Monomials with nonzero kernel ({len(nonzero)}):")
    for r in nonzero:
        cat = "SAME" if r['same_set'] == True else ("DIFF" if r['same_set'] == False else "RPT")
        print(f"    a={r['a_list']} b={r['b_list']}  "
              f"prods={r['products']:4d} rank={r['rank']:4d} ker={r['kernel']:3d}  [{cat}]")

    # Check: do same-set monomials each contribute exactly 9?
    same_set_monomials = [r for r in cats['both_distinct_same'] if r['kernel'] > 0]
    if same_set_monomials:
        kernels = [r['kernel'] for r in same_set_monomials]
        print(f"\n  Same-set kernel dims: {kernels}")
        if all(k == 9 for k in kernels):
            print(f"  *** ALL same-set monomials contribute exactly 9! ***")
        else:
            print(f"  Not all 9: {set(kernels)}")

    return results, total_kernel


# Run for n=6, 7, 8
for n_test in [6, 7, 8]:
    print(f"\n{'='*70}")
    print(f"Testing n = {n_test}")
    num_A_map = {6: 25, 7: 40, 8: 50}
    results, total = analyze_kernel_structure(
        n_test, gamma=n_test-2, delta=n_test-1,
        num_A=num_A_map.get(n_test, 30)
    )

print(f"\n{'='*70}")
print("FORMALIZATION CONCLUSION")
print("-" * 70)
print("""
If the kernel comes ONLY from 'both_distinct_same' monomials, each contributing
exactly 9, then:
  kernel_dim = 9 * (number of 4-element subsets of m free indices)
             = 9 * C(m, 4)
             = 9 * C(n-2, 4)

This would reduce the algebraic proof to showing:
  1. For each 4-element subset S, the S-restricted Gram system has a 9-dim kernel
     (matching codim of rank-1 in 4x4 matrices)
  2. For monomials with a-set != b-set, the Gram system is full-rank
  3. For monomials with repeated indices, the Gram system is full-rank
""")
print("DONE")
