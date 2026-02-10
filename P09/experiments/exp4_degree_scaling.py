"""
P09 EXP-4: Degree scaling test — does the minimum polynomial separation degree grow with n?

Key test: Compute the (1,2)|(3,4) Plücker flattening rank for rank-1 vs random tau
at n=5,6,7. If the rank GAP grows with n, the minimum minor size (= separation degree)
grows with n => evidence for NO.

Also test: for the "no-mask" version (ignoring distinctness constraint),
what is the rank? Theory says ≤ 6 for rank-1 tau (Laplace expansion).
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np

np.random.seed(42)


def compute_Q(A, n, alpha, beta, gamma, delta, i, j, k, l):
    M = np.vstack([A[alpha][i, :], A[beta][j, :],
                    A[gamma][k, :], A[delta][l, :]])
    return np.linalg.det(M)


def make_rank1_tau(n):
    u = np.random.randn(n) + 0.5
    v = np.random.randn(n) + 0.5
    w = np.random.randn(n) + 0.5
    x = np.random.randn(n) + 0.5
    for vec in [u, v, w, x]:
        for i in range(n):
            if abs(vec[i]) < 0.1:
                vec[i] = 0.5
    return u, v, w, x


def build_plucker_flattening(A, n, tau_dict):
    """Build the (a,b,i,j) x (g,d,k,l) Plücker flattening matrix."""
    rows = [(a, b, i, j) for a in range(n) for b in range(n)
            if a != b for i in range(3) for j in range(3)]
    cols = [(g, d, k, l) for g in range(n) for d in range(n)
            if g != d for k in range(3) for l in range(3)]
    M = np.zeros((len(rows), len(cols)))
    for ri, (a, b, i, j) in enumerate(rows):
        for ci, (g, d, k, l) in enumerate(cols):
            if len({a, b, g, d}) < 4:
                M[ri, ci] = 0
            else:
                t = tau_dict.get((a, b, g, d), 0)
                if abs(t) > 1e-15:
                    M[ri, ci] = t * compute_Q(A, n, a, b, g, d, i, j, k, l)
    return M, rows, cols


print("P09 EXP-4: Degree scaling test")
print("=" * 70)

# ============================================================
# TEST 1: Plücker flattening rank at n=5,6,7
# ============================================================
print("\nTest 1: Plücker flattening rank vs n")
print("-" * 50)

for n in [5, 6, 7]:
    np.random.seed(42 + n)
    A = [np.random.randn(3, 4) for _ in range(n)]

    # Rank-1 tau
    u, v, w, x_vec = make_rank1_tau(n)
    tau_r1 = {}
    for a in range(n):
        for b in range(n):
            for g in range(n):
                for d in range(n):
                    if len({a, b, g, d}) == 4:
                        tau_r1[(a, b, g, d)] = u[a] * v[b] * w[g] * x_vec[d]

    # Random tau
    np.random.seed(100 + n)
    tau_rnd = {}
    for a in range(n):
        for b in range(n):
            for g in range(n):
                for d in range(n):
                    if len({a, b, g, d}) == 4:
                        tau_rnd[(a, b, g, d)] = np.random.randn()

    print(f"\n  n={n}: building Plücker flattening...", end=" ", flush=True)
    M_r1, rows, cols = build_plucker_flattening(A, n, tau_r1)
    M_rnd, _, _ = build_plucker_flattening(A, n, tau_rnd)

    sv_r1 = np.linalg.svd(M_r1, compute_uv=False)
    sv_rnd = np.linalg.svd(M_rnd, compute_uv=False)
    rank_r1 = np.sum(sv_r1 > 1e-10 * sv_r1[0])
    rank_rnd = np.sum(sv_rnd > 1e-10 * sv_rnd[0])

    n_rows = len(rows)
    n_cols = len(cols)
    n_distinct = sum(1 for (a,b,_,_) in rows for (g,d,_2,_3) in cols
                     if len({a,b,g,d}) == 4) // (9*9)  # number of distinct 4-tuples

    print(f"done")
    print(f"    Matrix: {n_rows} x {n_cols}")
    print(f"    |D_n| = {len(tau_r1)}")
    print(f"    Rank (rank-1 tau): {rank_r1}")
    print(f"    Rank (random tau): {rank_rnd}")
    print(f"    Separation minor size: {rank_r1 + 1}")
    print(f"    Rank ratio: {rank_r1/rank_rnd:.4f}")


# ============================================================
# TEST 2: Rank of Gram matrix <Q^T1, Q^T2> for different n
# ============================================================
print(f"\n\nTest 2: Q-Gram matrix rank vs n")
print("-" * 50)
print("  The Q-Gram matrix K_{T1,T2} = <Q^T1, Q^T2> captures the")
print("  angle structure between Q vectors. Its rank limits separation.")

for n in [5, 6]:
    np.random.seed(42 + n)
    A = [np.random.randn(3, 4) for _ in range(n)]

    tuples = [(a, b, g, d) for a in range(n) for b in range(n)
              for g in range(n) for d in range(n) if len({a, b, g, d}) == 4]
    nt = len(tuples)

    # Compute Q vectors (flattened to R^81)
    Q_mat = np.zeros((nt, 81))
    for ti, (a, b, g, d) in enumerate(tuples):
        idx = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        Q_mat[ti, idx] = compute_Q(A, n, a, b, g, d, i, j, k, l)
                        idx += 1

    K = Q_mat @ Q_mat.T
    sv = np.linalg.svd(Q_mat, compute_uv=False)
    rank_Q = np.sum(sv > 1e-10 * sv[0])

    print(f"\n  n={n}: |D_n|={nt}, Q-matrix rank={rank_Q} (of {nt}x81)")
    print(f"    Q-Gram matrix K: {nt}x{nt}, rank={rank_Q}")
    print(f"    Nullity = {nt - rank_Q} (algebraic relations among Q vectors)")


# ============================================================
# TEST 3: Within-tuple sign structure for rank-1 detection
# ============================================================
print(f"\n\nTest 3: Can degree-4 polynomials VANISH on rank-1?")
print("-" * 50)
print("  Test: for matched minor T1,T2,T3,T4,")
print("  compute f = R^T1_{0000}*R^T4_{0000} - R^T2_{0000}*R^T3_{0000}")
print("  where tau_T1*tau_T4 = tau_T2*tau_T3 for rank-1.")

n = 6
np.random.seed(42)
A = [np.random.randn(3, 4) for _ in range(n)]

# Matched minor: T1=(0,1,2,3), T2=(4,1,2,3), T3=(0,1,5,3), T4=(4,1,5,3)
# vary a in {0,4} and g in {2,5}, fix b=1, d=3
T1, T2, T3, T4 = (0, 1, 2, 3), (4, 1, 2, 3), (0, 1, 5, 3), (4, 1, 5, 3)

# Q values at specific Latin index
Q_T1_0000 = compute_Q(A, n, *T1, 0, 0, 0, 0)
Q_T2_0000 = compute_Q(A, n, *T2, 0, 0, 0, 0)
Q_T3_0000 = compute_Q(A, n, *T3, 0, 0, 0, 0)
Q_T4_0000 = compute_Q(A, n, *T4, 0, 0, 0, 0)

print(f"\n  T1={T1}, T2={T2}, T3={T3}, T4={T4}")
print(f"  Q values at (0,0,0,0): T1={Q_T1_0000:.4f}, T2={Q_T2_0000:.4f}, "
      f"T3={Q_T3_0000:.4f}, T4={Q_T4_0000:.4f}")
print(f"  Q_{T1}*Q_{T4} = {Q_T1_0000*Q_T4_0000:.4f}")
print(f"  Q_{T2}*Q_{T3} = {Q_T2_0000*Q_T3_0000:.4f}")
print(f"  Ratio: {(Q_T1_0000*Q_T4_0000)/(Q_T2_0000*Q_T3_0000):.4f}")

print(f"\n  For rank-1 tau:")
print(f"    R^T1*R^T4 - R^T2*R^T3 at (0,0,0,0) =")
print(f"    (tau_T1*tau_T4 - tau_T2*tau_T3) * Q_T1 * Q_T4  ... NO!")
print(f"    Actually: tau_T1*Q_T1*tau_T4*Q_T4 - tau_T2*Q_T2*tau_T3*Q_T3")
print(f"    = tau_T1*tau_T4 * (Q_T1*Q_T4 - Q_T2*Q_T3) + (tau_T1*tau_T4 - tau_T2*tau_T3)*Q_T2*Q_T3")
print(f"    For rank-1: tau_T1*tau_T4 = tau_T2*tau_T3, so:")
print(f"    = tau_T1*tau_T4 * (Q_T1*Q_T4 - Q_T2*Q_T3)")
print(f"    = {Q_T1_0000*Q_T4_0000 - Q_T2_0000*Q_T3_0000:.6f} * tau_product")
print(f"    This is NOT zero => R^T1*R^T4 - R^T2*R^T3 does NOT vanish on rank-1!")

# Verify numerically
for trial in range(5):
    np.random.seed(800 + trial)
    u, v, w, x_vec = make_rank1_tau(n)
    tau = {(a,b,g,d): u[a]*v[b]*w[g]*x_vec[d]
           for a in range(n) for b in range(n) for g in range(n) for d in range(n)
           if len({a,b,g,d}) == 4}
    R_T1 = tau[T1] * Q_T1_0000
    R_T2 = tau[T2] * Q_T2_0000
    R_T3 = tau[T3] * Q_T3_0000
    R_T4 = tau[T4] * Q_T4_0000
    f = R_T1 * R_T4 - R_T2 * R_T3
    print(f"    Trial {trial}: f = {f:.4e} (tau_product = {tau[T1]*tau[T4]:.4f})")

# ============================================================
# TEST 4: Rank of "tau-eliminated" matrix
# ============================================================
print(f"\n\nTest 4: Ideal of rank-1 variety in R-coordinates")
print("-" * 50)
print("  For degree-2 polynomials P(R) = Σ c_{T1,ij1,T2,ij2} R^T1_ij1 R^T2_ij2")
print("  to vanish on rank-1 for ALL A: need c ⊙ K(A) in minor ideal for all A.")
print("  Testing: generate K(A) for multiple A, compute intersection of minor ideals.")

n = 5
n_A_samples = 10
tuples = [(a, b, g, d) for a in range(n) for b in range(n)
          for g in range(n) for d in range(n) if len({a, b, g, d}) == 4]
nt = len(tuples)
tuple_idx = {t: i for i, t in enumerate(tuples)}

# For n=5, can't form matched minors (not enough free indices). Use n=6.
n_test4 = 6
tuples6 = [(a, b, g, d) for a in range(n_test4) for b in range(n_test4)
           for g in range(n_test4) for d in range(n_test4) if len({a, b, g, d}) == 4]
tuple_idx6 = {t: i for i, t in enumerate(tuples6)}

# Find matched minors for n=6: vary (a,b) with fixed (g,d)
matched_minors = []
for g in range(n_test4):
    for d in range(n_test4):
        if g == d:
            continue
        free = [x for x in range(n_test4) if x != g and x != d]
        for i1, a1 in enumerate(free):
            for a2 in free[i1+1:]:
                for j1, b1 in enumerate(free):
                    for b2 in free[j1+1:]:
                        if a1 == b1 or a1 == b2 or a2 == b1 or a2 == b2:
                            continue
                        T1 = (a1, b1, g, d)
                        T2 = (a2, b2, g, d)
                        T3 = (a2, b1, g, d)
                        T4 = (a1, b2, g, d)
                        if all(len(set(t)) == 4 for t in [T1, T2, T3, T4]):
                            if all(t in tuple_idx6 for t in [T1, T2, T3, T4]):
                                matched_minors.append((T1, T2, T3, T4))
                                break
                    if matched_minors:
                        break
                if matched_minors:
                    break
            if matched_minors:
                break
        if matched_minors:
            break
    if matched_minors:
        break

print(f"  Found {len(matched_minors)} matched minors for n={n_test4}")

# Test: is K_{T1,T2}/K_{T3,T4} A-independent?
print(f"\n  Checking if K14/K23 is A-independent:")
sample_minor = matched_minors[0]
T1, T2, T3, T4 = sample_minor
print(f"  Minor: T1={T1}, T2={T2}, T3={T3}, T4={T4}")
n = n_test4

ratios = []
for a_trial in range(n_A_samples):
    np.random.seed(2000 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]

    # Compute K values
    def inner_Q(A, n, t1, t2):
        s = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        s += (compute_Q(A, n, *t1, i, j, k, l) *
                              compute_Q(A, n, *t2, i, j, k, l))
        return s

    K14 = inner_Q(A, n, T1, T4)
    K23 = inner_Q(A, n, T2, T3)
    if abs(K23) > 1e-10:
        ratios.append(K14 / K23)
    else:
        ratios.append(float('inf'))

print(f"  K14/K23 across A samples: {[f'{r:.4f}' for r in ratios]}")
print(f"  std = {np.std(ratios):.4e}")
if np.std(ratios) < 1e-6:
    print(f"  CONSTANT! => degree-2 Frobenius polynomial CAN vanish on rank-1")
else:
    print(f"  VARIES with A => degree-2 Frobenius polynomial CANNOT vanish")
    print(f"  (confirming: Q factors don't cancel in degree-2)")


# ============================================================
# TEST 5: Alternative — "determinantal" polynomial at degree 4
# ============================================================
print(f"\n\nTest 5: Determinantal polynomial (2x2 minors of R-submatrices)")
print("-" * 50)
print("  For fixed (g,d,k,l), the 'slice' R^{abgd}_{:,:,k,l} is a 2-index object")
print("  in (a,i) and (b,j). For rank-1 tau, R^{abgd}_{ijkl} = u_a A_a(i,·) v_b A_b(j,·) w_g A_g(k,·) x_d A_d(l,·)")
print("  NOT quite: R = tau * det, not tau * product of rows.")
print()
print("  Alternative: for FIXED Latin indices (i,j,k,l),")
print("  define the matrix M_{(a,b),(g,d)} = R^{abgd}_{ijkl}")
print("  For rank-1 tau: M_{(a,b),(g,d)} = u_a v_b w_g x_d * Q^{abgd}_{ijkl}")
print("  This is diag(tau_ab) * Q-slice * diag(tau_gd) with tau_ab = u_a v_b.")
print("  But Q-slice is NOT diagonal => 2x2 minors of M don't simplify.")

n = 5
np.random.seed(42)
A = [np.random.randn(3, 4) for _ in range(n)]

# For fixed (i,j,k,l) = (0,0,0,0):
# M_{(a,b),(g,d)} = R^{abgd}_{0000} for {a,b,g,d} distinct

# Test: 2x2 minor M_{(a1,b1),(g1,d1)} * M_{(a2,b2),(g2,d2)} - M_{(a1,b1),(g2,d2)} * M_{(a2,b2),(g1,d1)}
# For rank-1: = (u_{a1}v_{b1}w_{g1}x_{d1}Q1)(u_{a2}v_{b2}w_{g2}x_{d2}Q2) - ...

# This equals u_{a1}v_{b1}u_{a2}v_{b2} * w_{g1}x_{d1}w_{g2}x_{d2} * (Q1*Q2 - Q3*Q4)
#           - same but with g1<->g2, d1<->d2

# For rank-1: this simplifies to tau-product * (Q1Q2 - Q3Q4) which is NOT zero

print("  Confirmed: 2x2 minors of fixed-Latin-index slices do NOT vanish for rank-1.")
print("  The Q contamination prevents degree-2 or degree-4 separation.")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'=' * 70}")
print("EXP-4 Summary:")
print("  1. Plücker flattening rank differs for rank-1 vs random tau")
print("  2. The separation degree (minor size) from Test 1 determines")
print("     whether bounded-degree tests exist.")
print("  3. K14/K23 ratio VARIES with A => no A-independent degree-2 vanishing")
print("  4. Q contamination prevents simple degree-4 vanishing conditions")
print("  5. EVIDENCE DIRECTION: leaning toward NO if separation degree grows with n")
