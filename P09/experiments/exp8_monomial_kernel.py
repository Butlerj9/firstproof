"""
P09 EXP-8: Monomial-decomposed kernel dimension for degree-4 Frobenius products.

Key insight: Each degree-4 product contributes to exactly one (u,v) monomial.
So the vanishing constraint system decomposes into many small independent
problems (one per monomial). This makes n=7 and n=8 computationally feasible
without building the full constraint matrix.

Tests:
  n=6 (sanity check, expect kernel_dim = 9)
  n=7 (prediction: (7-3)^2 = 16)
  n=8 (prediction: (8-3)^2 = 25)

Formula: kernel_dim(degree 4, n) = (n-3)^2 for n >= 6.
This equals the codimension of rank-1 matrices in M^{m x m} where m = n-2.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import time

np.random.seed(42)

print("P09 EXP-8: Monomial-decomposed kernel dimension")
print("=" * 70)


def compute_Q_vec(A, T):
    """Compute Q^T as flat 81-vector (all latin index combinations)."""
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
    """Compute K_{s,t} = <Q^s, Q^t> for all tuple pairs."""
    Q_vecs = [compute_Q_vec(A, T) for T in tuples]
    nt = len(tuples)
    K = np.zeros((nt, nt))
    for i in range(nt):
        for j in range(i, nt):
            K[i, j] = Q_vecs[i] @ Q_vecs[j]
            K[j, i] = K[i, j]
    return K


def test_kernel_dim(n, gamma, delta, num_A_max=20):
    """Compute degree-4 Frobenius-product kernel dimension at given n.

    Uses monomial decomposition: the system splits into independent small
    problems, one per (u,v) monomial. Total kernel dim = sum of per-monomial
    kernel dims.
    """
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
    t0 = time.time()
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
    sizes = [len(v) for v in monomial_products.values()]
    print(f"  monomials: {n_mon}, max group: {max(sizes)}, "
          f"mean group: {sum(sizes)/n_mon:.1f}")
    print(f"  grouping time: {time.time()-t0:.1f}s")

    # Verify partition: sum of group sizes = n_d4
    assert sum(sizes) == n_d4, f"Partition error: {sum(sizes)} != {n_d4}"

    # Compute K matrices for all A samples
    t0 = time.time()
    K_all = []
    for ai in range(num_A_max):
        np.random.seed(4000 + n * 100 + ai)
        A = [np.random.randn(3, 4) for _ in range(n)]
        K = compute_gram(A, tuples)
        K_all.append(K)
    print(f"  K computation ({num_A_max} A): {time.time()-t0:.1f}s")

    # Track convergence: kernel dim vs number of A samples
    # Need num_A >= max_group_size for convergence
    checkpoints = sorted(set(
        [c for c in [1, 2, 5, 10, 20, 30, 40, 50, 60, 80] if c <= num_A_max]
    ))
    predicted = (n - 3) ** 2

    print(f"\n  Need >= {max(sizes)} A samples for convergence (max group size)")
    print(f"\n  Convergence (kernel dim vs A samples):")
    print(f"  {'A':>4}  {'kernel_dim':>12}  {'predicted':>10}  match")

    final_dim = None
    for num_A in checkpoints:
        t0 = time.time()
        total_null = 0
        for mon, products in monomial_products.items():
            count_m = len(products)
            # Build small constraint matrix: num_A rows x count_m cols
            C = np.zeros((num_A, count_m))
            for ai in range(num_A):
                K = K_all[ai]
                for ci, (s1, t1, s2, t2, mult) in enumerate(products):
                    C[ai, ci] = K[s1, t1] * K[s2, t2] * mult

            # Compute rank of this small matrix
            if count_m == 1:
                rank_m = 1 if np.max(np.abs(C)) > 1e-10 else 0
            else:
                s_vals = np.linalg.svd(C, compute_uv=False)
                tol = 1e-10 * s_vals[0] if s_vals[0] > 1e-10 else 1e-10
                rank_m = int(np.sum(s_vals > tol))

            total_null += count_m - rank_m

        elapsed = time.time() - t0
        match_str = "YES" if total_null == predicted else "---"
        print(f"  {num_A:4d}  {total_null:12d}  {predicted:10d}  {match_str}"
              f"  ({elapsed:.1f}s)")
        final_dim = total_null

    return final_dim


# ============================================================
# Run tests for n = 6, 7, 8
# ============================================================
results = {}

for n_test in [6, 7, 8]:
    print(f"\n{'='*70}")
    print(f"Testing n = {n_test}")
    # Need enough A to exceed max monomial group size
    max_A = {6: 25, 7: 50, 8: 60}
    dim = test_kernel_dim(n_test, gamma=2, delta=3, num_A_max=max_A.get(n_test, 60))
    results[n_test] = dim

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("SUMMARY")
print("-" * 70)
print(f"{'n':>4} {'m':>4} {'kernel_dim':>12} {'(n-3)^2':>10} {'match':>8}")
for n_test in sorted(results.keys()):
    dim = results[n_test]
    pred = (n_test - 3) ** 2
    match = "YES" if dim == pred else "NO"
    print(f"{n_test:4d} {n_test-2:4d} {dim:12d} {pred:10d} {match:>8}")

all_match = all(results[n] == (n-3)**2 for n in results)
if all_match:
    print(f"\n  *** ALL MATCH: kernel_dim(degree 4, n) = (n-3)^2 for n >= 6 ***")
    print(f"  = codim(rank-1 in M^{{m x m}}) where m = n-2")
    print(f"  This confirms n-uniformity of the degree-4 construction.")
    print(f"  Gap #1 (n-uniformity) addressed: pattern holds at n=6,7,8.")
    print(f"  Gap #3 (K-compatibility) strengthened: dimension matches")
    print(f"  algebraic prediction at 3 independent n values.")
else:
    print(f"\n  Discrepancies found. Formula may be incorrect.")

print(f"\nDONE")
