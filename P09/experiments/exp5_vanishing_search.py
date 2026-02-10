"""
P09 EXP-5: Definitive test — do degree-4 polynomials with A-independent coefficients
exist that vanish on rank-1 tau?

Method: For n=6, restrict to a small set of Greek tuples sharing (g,d)=(2,3).
Build the constraint matrix for degree-4 polynomials in the Frobenius-product
subspace. Check if the null space across multiple A samples is nontrivial.

If the null space is trivial for 2-3 A samples: NO degree-4 polynomial exists.
If nontrivial: candidate YES, need verification.

Also checks degree-2 as a sanity check (expected: trivial).
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np

np.random.seed(42)

print("P09 EXP-5: Vanishing polynomial search")
print("=" * 70)

n = 6

# ============================================================
# SETUP: Greek tuples with fixed (g,d)
# ============================================================
# Tuples (a,b,2,3) with a,b in {0,1,4,5}, a!=b, and {a,b,2,3} pairwise distinct
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)
print(f"  n={n}, fixed (g,d)=({g_fix},{d_fix})")
print(f"  Free indices: {free_indices}")
print(f"  Tuples: {nt} total")
for t in tuples:
    print(f"    {t}")


def compute_Q(A, n, alpha, beta, gamma, delta, i, j, k, l):
    M = np.vstack([A[alpha][i, :], A[beta][j, :],
                    A[gamma][k, :], A[delta][l, :]])
    return np.linalg.det(M)


def compute_Q_vec(A, n, T):
    """Q^T as a flat 81-vector."""
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
    """Compute K_{s,t} = <Q^{T_s}, Q^{T_t}> for all pairs."""
    Q_vecs = [compute_Q_vec(A, n, T) for T in tuples]
    nt = len(tuples)
    K = np.zeros((nt, nt))
    for i in range(nt):
        for j in range(i, nt):
            K[i, j] = Q_vecs[i] @ Q_vecs[j]
            K[j, i] = K[i, j]
    return K


# ============================================================
# TEST 1: Degree-2 vanishing (sanity check)
# ============================================================
print(f"\n\nTest 1: Degree-2 Frobenius polynomial vanishing (sanity)")
print("-" * 50)
print(f"  P(R) = Σ_{{s,t}} c_{{s,t}} <R^{{T_s}}, R^{{T_t}}>")
print(f"  For rank-1 tau: = Σ c_st τ_s τ_t K_st(A)")
print(f"  Vanishing condition: Σ c_st K_st(A) * (u-v monomial) = 0")

# For tuples (a,b,2,3): rank-1 tau = u_a v_b w_2 x_3
# The tau product τ_s τ_t = (w2 x3)^2 u_{as} v_{bs} u_{at} v_{bt}
# Monomial in (u,v): each u_a appears 0,1, or 2 times across the 4 indices
# u-degree: 2 (from two tau values), v-degree: 2

# Enumerate u-monomials of degree 2 in free_indices
from itertools import combinations_with_replacement

u_monoms = list(combinations_with_replacement(free_indices, 2))
v_monoms = list(combinations_with_replacement(free_indices, 2))
n_u = len(u_monoms)
n_v = len(v_monoms)
n_uv = n_u * n_v
print(f"  u-monomials (deg 2): {n_u}, v-monomials (deg 2): {n_v}")
print(f"  Total (u,v) monomials: {n_uv}")

# Coefficient pairs (s,t) with s <= t
pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_pairs = len(pairs)
print(f"  Number of c_{'{s,t}'} unknowns: {n_pairs}")

# For a given A: build the constraint matrix B(A)
# B has n_uv rows and n_pairs columns
# B_{(um,vm), (s,t)} = coefficient of (u-monom um)(v-monom vm) in K_st(A) * τ_s τ_t

def build_constraint_matrix_deg2(K, tuples, free_indices):
    """Build B(A) for degree-2 vanishing."""
    nt = len(tuples)
    pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
    u_monoms = list(combinations_with_replacement(free_indices, 2))
    v_monoms = list(combinations_with_replacement(free_indices, 2))
    n_uv = len(u_monoms) * len(v_monoms)
    n_pairs = len(pairs)

    # Map monomial tuples to indices
    u_idx = {m: i for i, m in enumerate(u_monoms)}
    v_idx = {m: i for i, m in enumerate(v_monoms)}

    B = np.zeros((n_uv, n_pairs))
    for pi, (s, t) in enumerate(pairs):
        a_s, b_s = tuples[s][0], tuples[s][1]
        a_t, b_t = tuples[t][0], tuples[t][1]
        k_val = K[s, t]
        # tau_s * tau_t contributes u_{a_s} u_{a_t} * v_{b_s} v_{b_t}
        u_mon = tuple(sorted([a_s, a_t]))
        v_mon = tuple(sorted([b_s, b_t]))
        if u_mon in u_idx and v_mon in v_idx:
            row = u_idx[u_mon] * len(v_monoms) + v_idx[v_mon]
            mult = 1 if s == t else 2  # symmetry factor
            B[row, pi] += k_val * mult
    return B


# Compute constraint matrices for multiple A
null_spaces = []
for a_trial in range(5):
    np.random.seed(3000 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, n, tuples)
    B = build_constraint_matrix_deg2(K, tuples, free_indices)

    # Null space of B
    _, s_vals, Vt = np.linalg.svd(B, full_matrices=True)
    rank_B = np.sum(s_vals > 1e-10 * s_vals[0])
    null_dim = n_pairs - rank_B
    null_spaces.append((rank_B, null_dim))
    print(f"    A#{a_trial}: B is {B.shape[0]}x{B.shape[1]}, "
          f"rank={rank_B}, null dim={null_dim}")

# Intersect null spaces
print(f"\n  Stacking constraint matrices across A samples:")
B_stack = np.zeros((0, n_pairs))
for a_trial in range(5):
    np.random.seed(3000 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, n, tuples)
    B = build_constraint_matrix_deg2(K, tuples, free_indices)
    B_stack = np.vstack([B_stack, B])

_, s_stack, _ = np.linalg.svd(B_stack, full_matrices=True)
rank_stack = np.sum(s_stack > 1e-10 * s_stack[0])
null_stack = n_pairs - rank_stack
print(f"  Stacked: {B_stack.shape[0]}x{B_stack.shape[1]}, "
      f"rank={rank_stack}, null dim={null_stack}")

if null_stack == 0:
    print(f"  CONFIRMED: NO degree-2 Frobenius polynomial vanishes for all A.")
else:
    print(f"  UNEXPECTED: {null_stack}-dimensional space of vanishing polynomials!")


# ============================================================
# TEST 2: Degree-4 vanishing (main test)
# ============================================================
print(f"\n\nTest 2: Degree-4 Frobenius-product polynomial vanishing")
print("-" * 50)
print(f"  P(R) = Σ c_{{pq}} <R^T_p1,R^T_p2> <R^T_q1,R^T_q2>")
print(f"  For rank-1 tau: = Σ c_pq τ_p1 τ_p2 τ_q1 τ_q2 K_p(A) K_q(A)")

# Degree-4 monomials in (u,v): degree 4 in u (from 4 tau values), degree 4 in v
u_monoms4 = list(combinations_with_replacement(free_indices, 4))
v_monoms4 = list(combinations_with_replacement(free_indices, 4))
n_u4 = len(u_monoms4)
n_v4 = len(v_monoms4)
n_uv4 = n_u4 * n_v4
print(f"  u-monomials (deg 4): {n_u4}, v-monomials (deg 4): {n_v4}")
print(f"  Total (u,v) monomials: {n_uv4}")

# Degree-4 unknowns: products of pairs (s,t) * (s',t')
# Number of Frobenius pair products with s<=t and s'<=t' and (s,t)<=(s',t')
deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)
deg4_pairs = [(p, q) for p in range(n_d2) for q in range(p, n_d2)]
n_d4 = len(deg4_pairs)
print(f"  Degree-2 Frobenius pairs: {n_d2}")
print(f"  Degree-4 products: {n_d4}")
print(f"  Constraint rows: {n_uv4}")

if n_uv4 > 10000 or n_d4 > 10000:
    print(f"  WARNING: Large system ({n_uv4} x {n_d4}). May be slow.")


def build_constraint_matrix_deg4(K, tuples, free_indices):
    """Build constraint matrix for degree-4 vanishing."""
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
        # tau product: τ_{s1} τ_{t1} τ_{s2} τ_{t2}
        # u-indices: a_{s1}, a_{t1}, a_{s2}, a_{t2}
        # v-indices: b_{s1}, b_{t1}, b_{s2}, b_{t2}
        a_list = [tuples[s1][0], tuples[t1][0], tuples[s2][0], tuples[t2][0]]
        b_list = [tuples[s1][1], tuples[t1][1], tuples[s2][1], tuples[t2][1]]
        u_mon = tuple(sorted(a_list))
        v_mon = tuple(sorted(b_list))
        if u_mon in u_idx and v_mon in v_idx:
            row = u_idx[u_mon] * len(v_monoms) + v_idx[v_mon]
            # Symmetry factor from (s,t) ordering and (p,q) ordering
            mult = 1
            if s1 != t1:
                mult *= 2
            if s2 != t2:
                mult *= 2
            if p != q:
                mult *= 2
            B[row, di] += k_val * mult
    return B


# Compute and intersect constraint matrices
print(f"\n  Computing constraint matrices:")
B_all = np.zeros((0, n_d4))
for a_trial in range(6):
    np.random.seed(4000 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram(A, n, tuples)
    B = build_constraint_matrix_deg4(K, tuples, free_indices)

    _, s_vals, _ = np.linalg.svd(B, full_matrices=True)
    rank_B = np.sum(s_vals > 1e-10 * s_vals[0])
    null_B = n_d4 - rank_B
    print(f"    A#{a_trial}: B is {B.shape[0]}x{B.shape[1]}, "
          f"rank={rank_B}, null dim={null_B}")

    B_all = np.vstack([B_all, B])

print(f"\n  Intersecting across all A samples:")
_, s_all, _ = np.linalg.svd(B_all, full_matrices=True)
rank_all = np.sum(s_all > 1e-10 * s_all[0])
null_all = n_d4 - rank_all
print(f"  Stacked: {B_all.shape[0]}x{B_all.shape[1]}, "
      f"rank={rank_all}, null dim={null_all}")

if null_all == 0:
    print(f"\n  *** CONFIRMED: NO degree-4 Frobenius-product polynomial ***")
    print(f"  *** vanishes on rank-1 for all A (in this tuple subspace). ***")
    print(f"  STRONG EVIDENCE FOR NO.")
elif null_all > 0:
    print(f"\n  *** FOUND: {null_all}-dimensional space of vanishing degree-4 ***")
    print(f"  *** polynomials! Need to verify on more A samples. ***")
    print(f"  EVIDENCE FOR YES.")


# ============================================================
# TEST 3: Cross-ratio polynomial (not in Frobenius subspace)
# ============================================================
print(f"\n\nTest 3: Cross-ratio polynomial structure")
print("-" * 50)
print(f"  The ratio <R^T1,R^T4>/<R^T2,R^T3> is tau-independent for rank-1.")
print(f"  The polynomial f = <R^T1,R^T4>·<R^T2',R^T3'> - <R^T2,R^T3>·<R^T1',R^T4'>")
print(f"  does NOT vanish on rank-1 (Q ratios differ).")
print(f"  Verifying numerically:")

np.random.seed(42)
A = [np.random.randn(3, 4) for _ in range(n)]
K = compute_gram(A, n, tuples)

# Pick two matched minors from the (a,b) swap family
# Minor 1: T1=(0,1,2,3), T2=(4,1,2,3), T3=(0,5,2,3), T4=(4,5,2,3)
# Verify tau_T1*tau_T4 = tau_T2*tau_T3 for rank-1
T1 = (0, 1, 2, 3)
T4 = (4, 5, 2, 3)
T2 = (4, 1, 2, 3)
T3 = (0, 5, 2, 3)

t1i = tuples.index(T1) if T1 in tuples else -1
t2i = tuples.index(T2) if T2 in tuples else -1
t3i = tuples.index(T3) if T3 in tuples else -1
t4i = tuples.index(T4) if T4 in tuples else -1

if all(i >= 0 for i in [t1i, t2i, t3i, t4i]):
    K14 = K[t1i, t4i]
    K23 = K[t2i, t3i]
    print(f"  Minor 1: T1={T1}, T4={T4}, T2={T2}, T3={T3}")
    print(f"    <Q^T1,Q^T4> = {K14:.4f}")
    print(f"    <Q^T2,Q^T3> = {K23:.4f}")
    print(f"    Ratio K14/K23 = {K14/K23:.4f}")

    # For rank-1 tau: <R^T1,R^T4>/<R^T2,R^T3> = K14/K23 (constant)
    # For a SECOND matched minor:
    # Minor 2: T1'=(0,4,2,3), T4'=(1,5,2,3), T2'=(1,4,2,3), T3'=(0,5,2,3)
    T1p = (0, 4, 2, 3)
    T4p = (1, 5, 2, 3)
    T2p = (1, 4, 2, 3)
    T3p = (0, 5, 2, 3)
    t1pi = tuples.index(T1p) if T1p in tuples else -1
    t2pi = tuples.index(T2p) if T2p in tuples else -1
    t3pi = tuples.index(T3p) if T3p in tuples else -1
    t4pi = tuples.index(T4p) if T4p in tuples else -1

    if all(i >= 0 for i in [t1pi, t2pi, t3pi, t4pi]):
        K14p = K[t1pi, t4pi]
        K23p = K[t2pi, t3pi]
        print(f"\n  Minor 2: T1'={T1p}, T4'={T4p}, T2'={T2p}, T3'={T3p}")
        print(f"    <Q^T1',Q^T4'> = {K14p:.4f}")
        print(f"    <Q^T2',Q^T3'> = {K23p:.4f}")
        print(f"    Ratio K14'/K23' = {K14p/K23p:.4f}")

        # Cross polynomial:
        # f = <R^T1,R^T4>*<R^T2',R^T3'> - <R^T2,R^T3>*<R^T1',R^T4'>
        # For rank-1: = (tau_T1*tau_T4) * (tau_T2'*tau_T3') * K14*K23'
        #             - (tau_T2*tau_T3) * (tau_T1'*tau_T4') * K23*K14'
        # With tau_T1*tau_T4 = tau_T2*tau_T3 and tau_T1'*tau_T4' = tau_T2'*tau_T3':
        # = tau_prod1 * tau_prod2 * (K14*K23' - K23*K14')
        cross = K14 * K23p - K23 * K14p
        print(f"\n  Cross term K14*K23' - K23*K14' = {cross:.4f}")
        if abs(cross) > 1e-8:
            print(f"  NONZERO => cross-ratio polynomial does NOT vanish on rank-1")
            print(f"  (as predicted: Q ratios are A-dependent)")

            # Verify across A
            print(f"\n  Cross term across A samples:")
            for a_trial in range(5):
                np.random.seed(5000 + a_trial)
                A = [np.random.randn(3, 4) for _ in range(n)]
                K = compute_gram(A, n, tuples)
                cross = K[t1i, t4i] * K[t2pi, t3pi] - K[t2i, t3i] * K[t1pi, t4pi]
                print(f"    A#{a_trial}: cross = {cross:.4f}")
        else:
            print(f"  ZERO! Need to investigate.")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'=' * 70}")
print("EXP-5 Summary:")
print("  1. Degree-2 Frobenius polynomials: expected to have no vanishing")
print("  2. Degree-4 Frobenius-product polynomials: main test")
print("  3. Cross-ratio polynomials: don't vanish (Q ratios A-dependent)")
print()
print("OVERALL EVIDENCE SUMMARY (EXP-1 through EXP-5):")
print("  - EXP-1: Q tensor structure verified")
print("  - EXP-2: Plücker flattening separates, but degree = O(n^2)")
print("  - EXP-3: Cross-ratios detect rank-1, but as ratio tests, not vanishing")
print("  - EXP-4: Plücker rank grows as 3n(n-1), separation degree unbounded")
print("          Q-Gram matrix full-rank at n>=6 (all of R^81 spanned)")
print("          K14/K23 ratio VARIES with A => no A-independent degree-2 vanishing")
print("  - EXP-5: Degree-4 Frobenius-product test (see above)")
print()
print("CONCLUSION (updated after EXP-5b): Degree-4 Frobenius-product polynomials")
print("DO have a nontrivial A-independent kernel (dim 9, stabilized at 20 A samples).")
print("See EXP-5b for separation verification. Evidence shifted to YES, D=4.")
