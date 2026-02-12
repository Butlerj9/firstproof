"""
P09 EXP-11: Exact verification of n=5 degree-6 kernel dimension.

Strategy:
1. Float SVD → singular value gap confirms rank = 1756, kernel = 15
2. Modular rank at two large primes → proves rank_Q >= 1756
3. Combined: kernel = 15 exactly over Q

If rank = 1756 at both primes and SVD gap is clear: PROVED.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import combinations_with_replacement
import time

np.random.seed(42)

print("P09 EXP-11: n=5 degree-6 exact kernel verification")
print("=" * 70)

# ============================================================
# Setup (same as EXP-6e)
# ============================================================
n = 5
g_fix, d_fix = 2, 3
free_indices = [i for i in range(n) if i != g_fix and i != d_fix]
tuples = [(a, b, g_fix, d_fix) for a in free_indices for b in free_indices
          if a != b and len({a, b, g_fix, d_fix}) == 4]
nt = len(tuples)

# Extract a-index and b-index for each tuple
tuple_a = [t[0] for t in tuples]
tuple_b = [t[1] for t in tuples]

deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
n_d2 = len(deg2_pairs)

deg6_triples = [(p, q, r) for p in range(n_d2)
                for q in range(p, n_d2) for r in range(q, n_d2)]
n_d6 = len(deg6_triples)

u_monoms = list(combinations_with_replacement(free_indices, 6))
v_monoms = list(combinations_with_replacement(free_indices, 6))
u_idx = {m: i for i, m in enumerate(u_monoms)}
v_idx = {m: i for i, m in enumerate(v_monoms)}
n_uv = len(u_monoms) * len(v_monoms)

print(f"  n={n}, free={free_indices}, tuples={nt}")
print(f"  deg2_pairs={n_d2}, deg6_triples={n_d6}")
print(f"  u_monoms={len(u_monoms)}, v_monoms={len(v_monoms)}, n_uv={n_uv}")
print(f"  System per A: {n_uv} rows x {n_d6} cols")
print()

# Precompute triple-to-monomial mapping (shared across all A)
triple_u_mon = []
triple_v_mon = []
triple_row = []
for di, (p_idx, q_idx, r_idx) in enumerate(deg6_triples):
    s1, t1 = deg2_pairs[p_idx]
    s2, t2 = deg2_pairs[q_idx]
    s3, t3 = deg2_pairs[r_idx]
    u_list = sorted([tuple_a[s1], tuple_a[t1],
                     tuple_a[s2], tuple_a[t2],
                     tuple_a[s3], tuple_a[t3]])
    v_list = sorted([tuple_b[s1], tuple_b[t1],
                     tuple_b[s2], tuple_b[t2],
                     tuple_b[s3], tuple_b[t3]])
    u_mon = tuple(u_list)
    v_mon = tuple(v_list)
    if u_mon in u_idx and v_mon in v_idx:
        row = u_idx[u_mon] * len(v_monoms) + v_idx[v_mon]
        triple_row.append(row)
    else:
        triple_row.append(-1)
triple_row = np.array(triple_row)

# ============================================================
# Part 1: Float SVD for singular value gap
# ============================================================
print("Part 1: Float SVD (singular value gap)")
print("-" * 50)

def compute_gram_float(A_list, tuples):
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
                        M = np.vstack([A_list[alpha][i,:], A_list[beta][j,:],
                                       A_list[gamma][k,:], A_list[delta][l,:]])
                        v[idx] = np.linalg.det(M)
                        idx += 1
        Q_vecs.append(v)
    K = np.zeros((nt, nt))
    for a in range(nt):
        for b in range(a, nt):
            K[a, b] = Q_vecs[a] @ Q_vecs[b]
            K[b, a] = K[a, b]
    return K

n_A_float = 30
t0 = time.time()
B_float = None

for a_trial in range(n_A_float):
    np.random.seed(6200 + a_trial)
    A = [np.random.randn(3, 4) for _ in range(n)]
    K = compute_gram_float(A, tuples)

    B = np.zeros((n_uv, n_d6))
    for di, (p_idx, q_idx, r_idx) in enumerate(deg6_triples):
        s1, t1 = deg2_pairs[p_idx]
        s2, t2 = deg2_pairs[q_idx]
        s3, t3 = deg2_pairs[r_idx]
        k_val = K[s1, t1] * K[s2, t2] * K[s3, t3]
        row = triple_row[di]
        if row >= 0:
            B[row, di] += k_val

    if B_float is None:
        B_float = B.copy()
    else:
        B_float = np.vstack([B_float, B])

t_build = time.time() - t0
print(f"  Built float matrix: {B_float.shape}, time={t_build:.1f}s")

_, s_vals, Vt = np.linalg.svd(B_float, full_matrices=False)
rank_float = np.sum(s_vals > 1e-10 * s_vals[0])
null_float = n_d6 - rank_float

print(f"  SVD rank = {rank_float}, kernel = {null_float}")
print(f"  Largest SV: {s_vals[0]:.6e}")
print(f"  SV at rank-1: {s_vals[rank_float-1]:.6e}")
if null_float > 0:
    print(f"  SV at rank:   {s_vals[rank_float]:.6e}")
    gap = s_vals[rank_float-1] / s_vals[rank_float]
    print(f"  SINGULAR VALUE GAP: {gap:.3e} (ratio)")
    print(f"  Gap is {np.log10(gap):.1f} orders of magnitude")
print()

# ============================================================
# Part 2: Modular rank verification
# ============================================================
print("Part 2: Modular rank verification")
print("-" * 50)

def det4x4_int(r0, r1, r2, r3):
    """4x4 determinant using cofactor expansion, Python ints."""
    # Expand along first row
    def det3(a, b, c):
        return (a[0]*(b[1]*c[2]-b[2]*c[1])
               -a[1]*(b[0]*c[2]-b[2]*c[0])
               +a[2]*(b[0]*c[1]-b[1]*c[0]))
    return (r0[0]*det3(r1[1:], r2[1:], r3[1:])
           -r0[1]*det3([r1[0]]+list(r1[2:]), [r2[0]]+list(r2[2:]), [r3[0]]+list(r3[2:]))
           +r0[2]*det3([r1[0],r1[1],r1[3]], [r2[0],r2[1],r2[3]], [r3[0],r3[1],r3[3]])
           -r0[3]*det3(r1[:3], r2[:3], r3[:3]))

def compute_gram_int(A_list, tuples):
    """Compute Gram matrix with Python ints (exact)."""
    nt_local = len(tuples)
    Q_vecs = []
    for T in tuples:
        alpha, beta, gamma, delta = T
        v = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        r0 = [int(A_list[alpha][i][c]) for c in range(4)]
                        r1 = [int(A_list[beta][j][c]) for c in range(4)]
                        r2 = [int(A_list[gamma][k][c]) for c in range(4)]
                        r3 = [int(A_list[delta][l][c]) for c in range(4)]
                        v.append(det4x4_int(r0, r1, r2, r3))
        Q_vecs.append(v)
    K = [[0]*nt_local for _ in range(nt_local)]
    for a in range(nt_local):
        for b in range(a, nt_local):
            val = sum(Q_vecs[a][i] * Q_vecs[b][i] for i in range(81))
            K[a][b] = val
            K[b][a] = val
    return K

def gauss_rank_mod(M, p):
    """Compute rank of numpy int64 matrix mod p via Gaussian elimination."""
    M = M.copy()
    rows, cols = M.shape
    rank = 0
    for col in range(cols):
        # Find pivot in column col, from row rank downward
        pivot_row = -1
        for r in range(rank, rows):
            if M[r, col] % p != 0:
                pivot_row = r
                break
        if pivot_row == -1:
            continue
        # Swap
        if pivot_row != rank:
            M[[rank, pivot_row]] = M[[pivot_row, rank]]
        # Eliminate all rows below using vectorized ops
        inv_piv = pow(int(M[rank, col] % p), p - 2, p)
        # Get factors for all rows below
        below = M[rank+1:, col] % p
        nonzero_mask = below != 0
        if np.any(nonzero_mask):
            nonzero_rows = np.where(nonzero_mask)[0] + rank + 1
            factors = (M[nonzero_rows, col] * inv_piv) % p
            # Vectorized elimination
            M[nonzero_rows] = (M[nonzero_rows] - np.outer(factors, M[rank])) % p
        rank += 1
        if rank % 200 == 0:
            print(f"    ... col {col}/{cols}, rank so far = {rank}", flush=True)
    return rank

primes = [999999937, 999999893]  # Two large primes near 10^9
n_A_mod = 15  # A samples for modular verification

for pi, prime in enumerate(primes):
    print(f"\n  Prime {pi+1}: p = {prime}")
    t0 = time.time()

    # Build constraint matrix with integer A, reduce mod p
    B_mod_list = []
    for a_trial in range(n_A_mod):
        rng = np.random.RandomState(11000 + a_trial)
        A_int = [rng.randint(-5, 6, size=(3, 4)).tolist() for _ in range(n)]
        K_int = compute_gram_int(A_int, tuples)

        B_block = np.zeros((n_uv, n_d6), dtype=np.int64)
        for di, (p_idx, q_idx, r_idx) in enumerate(deg6_triples):
            s1, t1 = deg2_pairs[p_idx]
            s2, t2 = deg2_pairs[q_idx]
            s3, t3 = deg2_pairs[r_idx]
            k_val = (K_int[s1][t1] * K_int[s2][t2] % prime) * K_int[s3][t3] % prime
            row = triple_row[di]
            if row >= 0:
                B_block[row, di] = (B_block[row, di] + k_val) % prime

        B_mod_list.append(B_block)
        if a_trial < 3 or a_trial % 5 == 4:
            print(f"    Built A #{a_trial} mod p", flush=True)

    B_mod = np.vstack(B_mod_list).astype(np.int64)
    B_mod = B_mod % prime
    t_build = time.time() - t0
    print(f"  Matrix built: {B_mod.shape}, time={t_build:.1f}s")

    t0 = time.time()
    rank_mod = gauss_rank_mod(B_mod, prime)
    t_gauss = time.time() - t0
    kernel_mod = n_d6 - rank_mod
    print(f"  rank mod {prime} = {rank_mod}, kernel = {kernel_mod}, time={t_gauss:.1f}s")

# ============================================================
# Part 3: Separation verification (float)
# ============================================================
print(f"\nPart 3: Separation verification")
print("-" * 50)

if null_float > 0:
    kernel_vecs = Vt[rank_float:]  # 15 x n_d6

    print("  Rank-1 vanishing (should be ~0):")
    for vt in range(5):
        rng = np.random.RandomState(80000 + vt)
        A_test = [rng.randn(3, 4) for _ in range(n)]
        K_test = compute_gram_float(A_test, tuples)
        u, v, w, x = rng.randn(n), rng.randn(n), rng.randn(n), rng.randn(n)

        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            tau_s = u[T_s[0]] * v[T_s[1]] * w[T_s[2]] * x[T_s[3]]
            tau_t = u[T_t[0]] * v[T_t[1]] * w[T_t[2]] * x[T_t[3]]
            frob[pi] = tau_s * tau_t * K_test[s, t]

        d6_vals = np.array([frob[p_i]*frob[q_i]*frob[r_i]
                           for p_i, q_i, r_i in deg6_triples])
        results = kernel_vecs @ d6_vals
        max_abs = np.max(np.abs(results))
        print(f"    rank-1 #{vt}: max|f| = {max_abs:.3e}")

    print("  Random tau separation (should be >>0):")
    for vt in range(5):
        rng = np.random.RandomState(90000 + vt)
        A_test = [rng.randn(3, 4) for _ in range(n)]
        K_test = compute_gram_float(A_test, tuples)
        tau = rng.randn(n, n, n, n)

        frob = np.zeros(n_d2)
        for pi, (s, t) in enumerate(deg2_pairs):
            T_s, T_t = tuples[s], tuples[t]
            frob[pi] = (tau[T_s[0], T_s[1], T_s[2], T_s[3]] *
                        tau[T_t[0], T_t[1], T_t[2], T_t[3]] *
                        K_test[s, t])

        d6_vals = np.array([frob[p_i]*frob[q_i]*frob[r_i]
                           for p_i, q_i, r_i in deg6_triples])
        results = kernel_vecs @ d6_vals
        max_abs = np.max(np.abs(results))
        print(f"    random #{vt}: max|f| = {max_abs:.3e}")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*70}")
print("SUMMARY")
print(f"  Float SVD: rank={rank_float}, kernel={null_float}")
if null_float > 0:
    print(f"  SV gap: {gap:.3e} ({np.log10(gap):.1f} orders of magnitude)")
print(f"  Expected kernel = 15")
print()
print("DONE")
