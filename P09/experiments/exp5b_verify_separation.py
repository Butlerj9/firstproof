"""
P09 EXP-5b: Verify that the degree-4 vanishing polynomials actually separate
rank-1 from random tau.

Key questions:
1. Does the 351-dim null space stabilize with more A samples?
2. Are these polynomials nontrivial on random tau?
3. Do they give a genuine polynomial separator for the rank-1 variety?
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations_with_replacement

np.random.seed(42)

print("P09 EXP-5b: Verify degree-4 polynomial separation")
print("=" * 70)

n = 6
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)


def compute_Q(A, n, alpha, beta, gamma, delta, i, j, k, l):
    M = np.vstack([A[alpha][i, :], A[beta][j, :],
                    A[gamma][k, :], A[delta][l, :]])
    return np.linalg.det(M)


def compute_Q_vec(A, n, T):
    v = np.zeros(81)
    idx = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    v[idx] = compute_Q(A, n, *T, i, j, k, l)
                    idx += 1
    return v


def compute_gram(A, n, tuples):
    Q_vecs = [compute_Q_vec(A, n, T) for T in tuples]
    nt = len(tuples)
    K = np.zeros((nt, nt))
    for i in range(nt):
        for j in range(i, nt):
            K[i, j] = Q_vecs[i] @ Q_vecs[j]
            K[j, i] = K[i, j]
    return K


# Setup polynomial basis
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
deg4_pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
n_d4 = len(deg4_pairs)

u_monoms = list(combinations_with_replacement(free_indices, 4))
v_monoms = list(combinations_with_replacement(free_indices, 4))
u_idx = {m: i for i, m in enumerate(u_monoms)}
v_idx = {m: i for i, m in enumerate(v_monoms)}
n_uv = len(u_monoms) * len(v_monoms)


def build_constraint_matrix(K, tuples, free_indices):
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
            if s1 != t1:
                mult *= 2
            if s2 != t2:
                mult *= 2
            if p != q:
                mult *= 2
            B[row, di] += k_val * mult
    return B


# ============================================================
# TEST 1: Null space stability with increasing A samples
# ============================================================
print(f"\nTest 1: Null space dimension vs number of A samples")
print("-" * 50)

B_all = np.zeros((0, n_d4))
for num_A in range(1, 21):
    np.random.seed(4000 + num_A - 1)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, n, tuples)
    B = build_constraint_matrix(K, tuples, free_indices)
    B_all = np.vstack([B_all, B])

    _, s_vals, Vt = np.linalg.svd(B_all, full_matrices=True)
    rank_all = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_d4 - rank_all
    print(f"  {num_A:2d} A samples: stacked {B_all.shape[0]}x{B_all.shape[1]}, "
          f"rank={rank_all}, null dim={null_dim}")

    # Save null space at 20 samples
    if num_A == 20:
        null_vectors = Vt[rank_all:]  # rows of Vt after rank
        print(f"\n  Null space dimension stabilized at: {null_dim}")
        print(f"  Null space basis: {null_vectors.shape}")


# ============================================================
# TEST 2: Evaluate vanishing polynomials on rank-1 and random tau
# ============================================================
print(f"\n\nTest 2: Evaluate vanishing polynomials on rank-1 vs random tau")
print("-" * 50)

if null_vectors.shape[0] == 0:
    print("  No vanishing polynomials found. Skipping.")
else:
    # Pick the first few null space vectors as candidate polynomials
    n_test_polys = min(5, null_vectors.shape[0])

    def eval_polynomial(c_vec, K, tuples, tau_dict):
        """Evaluate the degree-4 polynomial with coefficient vector c."""
        val = 0
        for di, (p, q) in enumerate(deg4_pairs):
            if abs(c_vec[di]) < 1e-15:
                continue
            s1, t1 = deg2_pairs[p]
            s2, t2 = deg2_pairs[q]
            # <R^s1, R^t1> = tau_s1 * tau_t1 * K[s1,t1]
            Fr_p = tau_dict[tuples[s1]] * tau_dict[tuples[t1]] * K[s1, t1]
            Fr_q = tau_dict[tuples[s2]] * tau_dict[tuples[t2]] * K[s2, t2]
            mult = 1
            if s1 != t1:
                mult *= 2
            if s2 != t2:
                mult *= 2
            if p != q:
                mult *= 2
            val += c_vec[di] * Fr_p * Fr_q * mult
        return val

    # Test on multiple (A, tau) combinations
    print(f"  Testing {n_test_polys} null space vectors:")

    for poly_idx in range(n_test_polys):
        c = null_vectors[poly_idx]
        print(f"\n  Polynomial #{poly_idx}:")
        print(f"    Nonzero coefficients: {np.sum(np.abs(c) > 1e-10)} of {n_d4}")

        r1_vals = []
        rnd_vals = []

        for trial in range(10):
            np.random.seed(6000 + trial)
            A = [np.random.randn(3, 4) for _ in range(n)]
            K = compute_gram(A, n, tuples)

            # Rank-1 tau
            np.random.seed(7000 + trial)
            u = np.random.randn(n) + 0.5
            v = np.random.randn(n) + 0.5
            for vec in [u, v]:
                for i in range(n):
                    if abs(vec[i]) < 0.1:
                        vec[i] = 0.5
            w2, x3 = 1.0, 1.0  # common factor doesn't matter
            tau_r1 = {}
            for T in tuples:
                a, b = T[0], T[1]
                tau_r1[T] = u[a] * v[b] * w2 * x3

            # Random tau
            np.random.seed(8000 + trial)
            tau_rnd = {T: np.random.randn() for T in tuples}

            val_r1 = eval_polynomial(c, K, tuples, tau_r1)
            val_rnd = eval_polynomial(c, K, tuples, tau_rnd)
            r1_vals.append(val_r1)
            rnd_vals.append(val_rnd)

        r1_max = max(abs(v) for v in r1_vals)
        rnd_max = max(abs(v) for v in rnd_vals)
        rnd_min = min(abs(v) for v in rnd_vals)
        print(f"    rank-1: max|f| = {r1_max:.2e}, values = "
              f"{[f'{v:.2e}' for v in r1_vals[:4]]}...")
        print(f"    random: max|f| = {rnd_max:.2e}, min|f| = {rnd_min:.2e}, values = "
              f"{[f'{v:.2e}' for v in rnd_vals[:4]]}...")

        # Threshold: degree-4 double-precision noise is ~1e-6 for typical coefficient magnitudes
        separation_ratio = rnd_max / r1_max if r1_max > 0 else float('inf')
        if r1_max < 1e-4 and rnd_max > 1e-2:
            print(f"    *** GENUINE SEPARATOR: vanishes on rank-1 (noise ~{r1_max:.0e}), "
                  f"nonzero on random, ratio={separation_ratio:.0e} ***")
        elif r1_max < 1e-4 and rnd_max < 1e-4:
            print(f"    TRIVIALLY ZERO: vanishes on both rank-1 and random")
        elif r1_max > 1e-4:
            print(f"    NOT VANISHING on rank-1 (max|f|={r1_max:.2e} exceeds noise threshold)")


# ============================================================
# TEST 3: Check if vanishing polynomials come from 2x2 minor relations
# ============================================================
print(f"\n\nTest 3: Analyze structure of vanishing polynomials")
print("-" * 50)

if null_vectors.shape[0] > 0:
    # Count how many involve the same tau monomial
    c = null_vectors[0]
    # Group by tau monomial (which (u,v) monomial they contribute to)
    tau_groups = {}
    for di, (p, q) in enumerate(deg4_pairs):
        if abs(c[di]) < 1e-15:
            continue
        s1, t1 = deg2_pairs[p]
        s2, t2 = deg2_pairs[q]
        a_list = tuple(sorted([tuples[s1][0], tuples[t1][0],
                                tuples[s2][0], tuples[t2][0]]))
        b_list = tuple(sorted([tuples[s1][1], tuples[t1][1],
                                tuples[s2][1], tuples[t2][1]]))
        key = (a_list, b_list)
        if key not in tau_groups:
            tau_groups[key] = []
        tau_groups[key].append((di, c[di], (s1, t1, s2, t2)))

    print(f"  Polynomial #0 has {len(tau_groups)} distinct (u,v) monomials:")
    for (akey, bkey), entries in sorted(tau_groups.items())[:8]:
        print(f"    u^{akey} v^{bkey}: {len(entries)} terms")
        for di, coeff, (s1, t1, s2, t2) in entries[:3]:
            print(f"      c={coeff:.4f}: "
                  f"<R^{tuples[s1]},R^{tuples[t1]}> * "
                  f"<R^{tuples[s2]},R^{tuples[t2]}>")

    # Check: does this polynomial exploit the 2x2 minor structure?
    # For rank-1 M_{a,b} = u_a v_b, the 2x2 minors are:
    # M_{a1,b1} M_{a2,b2} - M_{a1,b2} M_{a2,b1} = 0
    # In tau terms: tau_{(a1,b1,g,d)} tau_{(a2,b2,g,d)} - tau_{(a1,b2,g,d)} tau_{(a2,b1,g,d)} = 0
    print(f"\n  2x2 minor structure check:")
    print(f"  For tau_{'{(a1,b1,g,d)}'} tau_{'{(a2,b2,g,d)}'} = "
          f"tau_{'{(a1,b2,g,d)}'} tau_{'{(a2,b1,g,d)}'}")
    print(f"  This means: the degree-4 polynomial can exploit these")
    print(f"  vanishing conditions, weighted by K products that match")
    print(f"  the tau monomial equivalence classes.")


# ============================================================
# TEST 4: Verify on DIFFERENT (g,d) pairs
# ============================================================
print(f"\n\nTest 4: Does the vanishing polynomial work for different (g,d)?")
print("-" * 50)
print(f"  The polynomial was derived for (g,d)=(2,3).")
print(f"  If it encodes a UNIVERSAL rank-1 test, it should work for any (g,d).")

if null_vectors.shape[0] > 0:
    c = null_vectors[0]

    # Test on (g,d) = (0,1) with free = {2,3,4,5}
    gd_tests = [(0, 1), (3, 4), (1, 5)]
    for g_test, d_test in gd_tests:
        free_test = [i for i in range(n) if i != g_test and i != d_test]
        tuples_test = [(a, b, g_test, d_test) for a in free_test for b in free_test
                       if a != b and len({a, b, g_test, d_test}) == 4]

        if len(tuples_test) != nt:
            print(f"  (g,d)=({g_test},{d_test}): {len(tuples_test)} tuples != {nt}, skip")
            continue

        # Test: does the same polynomial c vanish on rank-1 for this (g,d)?
        r1_vals_test = []
        rnd_vals_test = []
        for trial in range(5):
            np.random.seed(9000 + trial)
            A = [np.random.randn(3, 4) for _ in range(n)]
            K_test = np.zeros((nt, nt))
            Q_vecs = [compute_Q_vec(A, n, T) for T in tuples_test]
            for i in range(nt):
                for j in range(i, nt):
                    K_test[i, j] = Q_vecs[i] @ Q_vecs[j]
                    K_test[j, i] = K_test[i, j]

            # Rank-1 tau for this (g,d)
            np.random.seed(7000 + trial)
            u = np.random.randn(n) + 0.5
            v = np.random.randn(n) + 0.5
            w = np.random.randn(n) + 0.5
            x_vec = np.random.randn(n) + 0.5
            tau_r1 = {}
            for T in tuples_test:
                a, b, g, d = T
                tau_r1[T] = u[a] * v[b] * w[g] * x_vec[d]

            tau_rnd = {T: np.random.randn() for T in tuples_test}

            val_r1 = eval_polynomial(c, K_test, tuples_test, tau_r1)
            val_rnd = eval_polynomial(c, K_test, tuples_test, tau_rnd)
            r1_vals_test.append(val_r1)
            rnd_vals_test.append(val_rnd)

        r1_max_t = max(abs(v) for v in r1_vals_test)
        rnd_max_t = max(abs(v) for v in rnd_vals_test)
        print(f"  (g,d)=({g_test},{d_test}): rank-1 max|f|={r1_max_t:.2e}, "
              f"random max|f|={rnd_max_t:.2e}")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'=' * 70}")
print("EXP-5b Summary:")
print("  Tested null space stability and separation power of degree-4")
print("  Frobenius-product polynomials in the restricted tuple subspace.")
