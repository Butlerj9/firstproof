"""
P06 CE-1: Verify the complete graph counterexample to the alpha-light set question.

Claim: In K_n, a subset S of size k is alpha-light iff k <= 1 or k <= alpha*n.
Equivalently, max alpha-light set size = max(1, floor(alpha*n)).

Verification approach:
1. Build L_{K_n} and L_S for various S.
2. Check eigenvalues of alpha*L - L_S.
3. Confirm PSD iff k <= alpha*n (for k >= 2).
4. Test the exact boundary: k = floor(alpha*n) should be PSD, k = floor(alpha*n)+1 should not.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations

def laplacian_complete(n):
    """Laplacian of K_n: L = nI - J."""
    return n * np.eye(n) - np.ones((n, n))

def laplacian_induced(n, S):
    """Laplacian of G_S = (V, E(S,S)) where G = K_n.
    Only edges between vertices in S; vertex set is [n].
    """
    L = np.zeros((n, n))
    S = list(S)
    k = len(S)
    for i in range(k):
        for j in range(i + 1, k):
            u, v = S[i], S[j]
            L[u, u] += 1
            L[v, v] += 1
            L[u, v] -= 1
            L[v, u] -= 1
    return L

def is_psd(M, tol=1e-10):
    """Check if matrix M is positive semidefinite."""
    eigvals = np.linalg.eigvalsh(M)
    return np.min(eigvals) >= -tol, np.min(eigvals)

def test_kn_alpha_light(n, alpha, k):
    """Test whether a size-k subset of K_n is alpha-light.
    Returns (is_psd, min_eigenvalue).
    Since K_n is vertex-transitive, all size-k subsets are equivalent.
    """
    S = list(range(k))
    L = laplacian_complete(n)
    L_S = laplacian_induced(n, S)
    M = alpha * L - L_S
    return is_psd(M)

# =============================================================
# TEST 1: Verify eigenvalue formula for K_n
# Predicted: min eigenvalue of alpha*L_{K_n} - L_S = alpha*n - k (for k >= 2)
# =============================================================
print("=" * 60)
print("TEST 1: Eigenvalue formula verification")
print("=" * 60)

test1_pass = True
for n in range(3, 15):
    for k in range(2, n + 1):
        for alpha in [0.01, 0.1, 0.25, 0.5, 0.75, 0.99]:
            S = list(range(k))
            L = laplacian_complete(n)
            L_S = laplacian_induced(n, S)
            M = alpha * L - L_S
            eigvals = sorted(np.linalg.eigvalsh(M))
            min_eig = eigvals[0]
            predicted = alpha * n - k
            # The min nonzero eigenvalue should be alpha*n - k (for k >= 2)
            # But there's also a 0 eigenvalue from the all-ones vector
            # The actual min eigenvalue is min(0, alpha*n - k)
            predicted_min = min(0, alpha * n - k)
            if abs(min_eig - predicted_min) > 1e-8:
                print(f"  MISMATCH: n={n}, k={k}, alpha={alpha:.2f}: "
                      f"min_eig={min_eig:.10f}, predicted={predicted_min:.10f}")
                test1_pass = False

if test1_pass:
    print("  ALL MATCH: min eigenvalue = min(0, alpha*n - k) for all tested cases")
else:
    print("  SOME MISMATCHES FOUND")

# =============================================================
# TEST 2: Boundary verification
# k = floor(alpha*n) should be PSD, k = floor(alpha*n)+1 should not
# =============================================================
print(f"\n{'=' * 60}")
print("TEST 2: Boundary verification (floor(alpha*n))")
print("=" * 60)

test2_pass = True
for n in range(3, 25):
    for alpha_num in range(1, 100):
        alpha = alpha_num / 100.0
        k_max = int(np.floor(alpha * n))

        # k_max should be alpha-light (if k_max >= 2)
        if k_max >= 2:
            psd, min_eig = test_kn_alpha_light(n, alpha, k_max)
            if not psd:
                print(f"  FAIL: n={n}, alpha={alpha:.2f}, k={k_max} should be PSD "
                      f"but min_eig={min_eig:.10e}")
                test2_pass = False

        # k_max + 1 should NOT be alpha-light (if k_max + 1 <= n and k_max + 1 >= 2)
        if k_max + 1 <= n and k_max + 1 >= 2:
            psd, min_eig = test_kn_alpha_light(n, alpha, k_max + 1)
            if psd and alpha * n != k_max + 1:  # exact integer case: both could be PSD
                # Only flag if alpha*n is not exactly k_max+1
                if abs(alpha * n - (k_max + 1)) > 1e-10:
                    print(f"  FAIL: n={n}, alpha={alpha:.2f}, k={k_max+1} should NOT be PSD "
                          f"but min_eig={min_eig:.10e}")
                    test2_pass = False

if test2_pass:
    print("  ALL PASS: boundary at floor(alpha*n) confirmed")
else:
    print("  SOME FAILURES FOUND")

# =============================================================
# TEST 3: Single vertex is always alpha-light
# =============================================================
print(f"\n{'=' * 60}")
print("TEST 3: Single vertex always alpha-light")
print("=" * 60)

test3_pass = True
for n in range(2, 20):
    for alpha in [0.001, 0.01, 0.1, 0.5, 0.99]:
        psd, min_eig = test_kn_alpha_light(n, alpha, 1)
        if not psd:
            print(f"  FAIL: n={n}, alpha={alpha}, k=1: min_eig={min_eig:.10e}")
            test3_pass = False

if test3_pass:
    print("  ALL PASS: single vertex is always alpha-light (L_S = 0)")
else:
    print("  SOME FAILURES")

# =============================================================
# TEST 4: Exhaustive small-case verification
# For small n, check ALL subsets
# =============================================================
print(f"\n{'=' * 60}")
print("TEST 4: Exhaustive verification (n <= 8)")
print("=" * 60)

test4_pass = True
for n in range(3, 9):
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        max_light_size = 0
        predicted_max = max(1, int(np.floor(alpha * n)))

        for k in range(n + 1):
            if k == 0:
                max_light_size = max(max_light_size, 0)
                continue
            # Check one representative subset of size k (vertex-transitive)
            psd, _ = test_kn_alpha_light(n, alpha, k)
            if psd:
                max_light_size = max(max_light_size, k)

        if max_light_size != predicted_max:
            print(f"  MISMATCH: n={n}, alpha={alpha:.1f}: "
                  f"max_light={max_light_size}, predicted={predicted_max}")
            test4_pass = False

if test4_pass:
    print("  ALL MATCH: max alpha-light set size = max(1, floor(alpha*n))")
else:
    print("  SOME MISMATCHES")

# =============================================================
# TEST 5: The counterexample argument
# For c > 0, show that alpha = c/2 on K_n fails for large n
# =============================================================
print(f"\n{'=' * 60}")
print("TEST 5: Counterexample demonstration")
print("=" * 60)

for c in [0.5, 0.1, 0.01, 0.001]:
    alpha = c / 2
    print(f"\n  c = {c}, alpha = c/2 = {alpha}")
    print(f"  {'n':>6} | {'max |S|':>8} | {'c*n':>8} | {'|S| >= c*n?':>12}")
    print(f"  {'-'*6}-+-{'-'*8}-+-{'-'*8}-+-{'-'*12}")
    for n in [10, 50, 100, 500, 1000]:
        max_S = max(1, int(np.floor(alpha * n)))
        cn = c * n
        ok = max_S >= cn
        print(f"  {n:>6} | {max_S:>8} | {cn:>8.1f} | {'YES' if ok else 'NO':>12}")

# =============================================================
# SUMMARY
# =============================================================
print(f"\n{'=' * 60}")
print("SUMMARY")
print("=" * 60)
all_pass = test1_pass and test2_pass and test3_pass and test4_pass
print(f"Test 1 (eigenvalue formula): {'PASS' if test1_pass else 'FAIL'}")
print(f"Test 2 (boundary):           {'PASS' if test2_pass else 'FAIL'}")
print(f"Test 3 (single vertex):      {'PASS' if test3_pass else 'FAIL'}")
print(f"Test 4 (exhaustive small):   {'PASS' if test4_pass else 'FAIL'}")
print(f"\nOVERALL: {'ALL TESTS PASS — K_n counterexample confirmed' if all_pass else 'SOME TESTS FAILED'}")
print(f"\nConclusion: Answer to P06 is NO.")
print(f"For any c > 0, take alpha = c/2 and G = K_n with n > 4/c.")
print(f"Max alpha-light set in K_n has size floor(alpha*n) = floor(cn/2) < cn = c|V|.")
