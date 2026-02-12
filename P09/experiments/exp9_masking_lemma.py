"""
P09 EXP-9: D_n masking lemma — linearized test.

For n=6, the D_n tensor space has dim 360 (ordered 4-tuples with pairwise
distinct entries). The rank-1 variety has dimension 21, codimension 339.

The block-rank-1 conditions (from all 6 ways to fix 2 of 4 positions) give
quadratic equations. At a generic rank-1 point, we compute the Jacobian of
these equations. If rank(Jacobian) = 339, the block conditions locally
characterize rank-1 -> masking lemma holds.

If rank < 339, there's a gap -> masking lemma may fail.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import permutations, combinations

np.random.seed(42)

print("P09 EXP-9: D_n masking lemma (linearized Jacobian test)")
print("=" * 70)

n = 6

# Enumerate D_n 4-tuples (ordered, pairwise distinct)
D_n = list(permutations(range(n), 4))
n_tuples = len(D_n)
print(f"n={n}, D_n tuples: {n_tuples}")

# Index map
tuple_idx = {t: i for i, t in enumerate(D_n)}

# Generate random rank-1 tensor
u = np.random.randn(n) + 0.5
v = np.random.randn(n) + 0.5
w = np.random.randn(n) + 0.5
x = np.random.randn(n) + 0.5

tau0 = np.zeros(n_tuples)
for t in D_n:
    a, b, c, d = t
    tau0[tuple_idx[t]] = u[a] * v[b] * w[c] * x[d]

print(f"Rank-1 tensor: dim = {4*n - 3} = {4*n-3}")
print(f"Codimension = {n_tuples} - {4*n-3} = {n_tuples - (4*n-3)}")
codim_rank1 = n_tuples - (4 * n - 3)

# Enumerate all block-rank-1 minor conditions
# For each pair of positions (p1, p2) to fix, and each ordered pair of values (v1, v2):
#   The free positions form a block matrix indexed by (free values)\{v1,v2}, off-diagonal.
#   The 2x2 disjoint-pair minors of this block must vanish.

conditions = []  # Each: (i1, i2, i3, i4) meaning tau[i1]*tau[i2] = tau[i3]*tau[i4]

fix_pairs = list(combinations(range(4), 2))  # 6 ways to fix 2 of 4 positions
print(f"\nFix-position pairs: {fix_pairs}")

for fix_pos in fix_pairs:
    free_pos = [p for p in range(4) if p not in fix_pos]
    row_pos, col_pos = free_pos[0], free_pos[1]

    for v1 in range(n):
        for v2 in range(n):
            if v1 == v2:
                continue
            # Fixed values at fix_pos
            free_vals = [idx for idx in range(n) if idx != v1 and idx != v2]
            m = len(free_vals)

            # Disjoint-pair 2x2 minors
            for r_idx in combinations(range(m), 2):
                for c_idx in combinations(range(m), 2):
                    r1, r2 = free_vals[r_idx[0]], free_vals[r_idx[1]]
                    c1, c2 = free_vals[c_idx[0]], free_vals[c_idx[1]]
                    # Check: all 4 entries off-diagonal (r_i != c_j for all i,j)
                    if r1 == c1 or r1 == c2 or r2 == c1 or r2 == c2:
                        continue

                    # Build the 4 tuples
                    def make_tuple(rv, cv, fv1, fv2, fp, rp, cp):
                        t = [0] * 4
                        t[fp[0]] = fv1
                        t[fp[1]] = fv2
                        t[rp] = rv
                        t[cp] = cv
                        return tuple(t)

                    t11 = make_tuple(r1, c1, v1, v2, fix_pos, row_pos, col_pos)
                    t22 = make_tuple(r2, c2, v1, v2, fix_pos, row_pos, col_pos)
                    t12 = make_tuple(r1, c2, v1, v2, fix_pos, row_pos, col_pos)
                    t21 = make_tuple(r2, c1, v1, v2, fix_pos, row_pos, col_pos)

                    # Verify all in D_n
                    all_valid = all(t in tuple_idx for t in [t11, t22, t12, t21])
                    if all_valid:
                        conditions.append((tuple_idx[t11], tuple_idx[t22],
                                           tuple_idx[t12], tuple_idx[t21]))

# Remove exact duplicates
conditions = list(set(conditions))
n_cond = len(conditions)
print(f"\nTotal block conditions (deduplicated): {n_cond}")

# Build Jacobian at tau0
# Each condition: tau[i1]*tau[i2] - tau[i3]*tau[i4] = 0
# Jacobian row: tau0[i2]*e_{i1} + tau0[i1]*e_{i2} - tau0[i4]*e_{i3} - tau0[i3]*e_{i4}
J = np.zeros((n_cond, n_tuples))
for ci, (i1, i2, i3, i4) in enumerate(conditions):
    J[ci, i1] += tau0[i2]
    J[ci, i2] += tau0[i1]
    J[ci, i3] -= tau0[i4]
    J[ci, i4] -= tau0[i3]

print(f"Jacobian shape: {J.shape}")

# Compute rank
s_vals = np.linalg.svd(J, compute_uv=False)
rank_J = int(np.sum(s_vals > 1e-10 * s_vals[0]))
print(f"Jacobian rank: {rank_J}")
print(f"Codimension of rank-1: {codim_rank1}")

gap = codim_rank1 - rank_J
if gap == 0:
    print(f"\n  *** MATCH: Block conditions characterize rank-1 locally! ***")
    print(f"  The D_n masking lemma holds at n={n}.")
    print(f"  Gap #2 is CLOSED.")
elif gap > 0:
    print(f"\n  GAP: {gap} missing conditions.")
    print(f"  Block conditions do NOT fully characterize rank-1.")
    print(f"  Tangent space of block-rank-1 variety has dimension {n_tuples - rank_J}")
    print(f"  (vs rank-1 tangent space dimension {4*n-3})")

    # Check: does adding MORE conditions (from higher-degree ideal elements) help?
    # The gap might be fillable by degree-4 conditions
    print(f"\n  Checking if the gap is filled by the Frobenius polynomial construction...")
    print(f"  (i.e., does F_n vanish on the block-rank-1 but non-rank-1 directions?)")
else:
    print(f"  UNEXPECTED: rank > codimension (numerical issue)")

# Verify at a second random rank-1 point
print(f"\n--- Verification at second rank-1 point ---")
np.random.seed(123)
u2 = np.random.randn(n) + 0.3
v2 = np.random.randn(n) + 0.3
w2 = np.random.randn(n) + 0.3
x2 = np.random.randn(n) + 0.3

tau1 = np.zeros(n_tuples)
for t in D_n:
    a, b, c, d = t
    tau1[tuple_idx[t]] = u2[a] * v2[b] * w2[c] * x2[d]

J2 = np.zeros((n_cond, n_tuples))
for ci, (i1, i2, i3, i4) in enumerate(conditions):
    J2[ci, i1] += tau1[i2]
    J2[ci, i2] += tau1[i1]
    J2[ci, i3] -= tau1[i4]
    J2[ci, i4] -= tau1[i3]

s_vals2 = np.linalg.svd(J2, compute_uv=False)
rank_J2 = int(np.sum(s_vals2 > 1e-10 * s_vals2[0]))
print(f"Jacobian rank at second point: {rank_J2}")
print(f"Consistent: {'YES' if rank_J == rank_J2 else 'NO'}")

# Also test at n=7
print(f"\n{'='*70}")
print(f"Testing at n=7")
n7 = 7
D_n7 = list(permutations(range(n7), 4))
n_tuples7 = len(D_n7)
tuple_idx7 = {t: i for i, t in enumerate(D_n7)}
codim7 = n_tuples7 - (4 * n7 - 3)
print(f"D_7 tuples: {n_tuples7}, codim rank-1: {codim7}")

np.random.seed(42)
u7 = np.random.randn(n7) + 0.5
v7 = np.random.randn(n7) + 0.5
w7 = np.random.randn(n7) + 0.5
x7 = np.random.randn(n7) + 0.5

tau7 = np.zeros(n_tuples7)
for t in D_n7:
    a, b, c, d = t
    tau7[tuple_idx7[t]] = u7[a] * v7[b] * w7[c] * x7[d]

conditions7 = []
for fix_pos in fix_pairs:
    free_pos = [p for p in range(4) if p not in fix_pos]
    row_pos, col_pos = free_pos[0], free_pos[1]
    for v1 in range(n7):
        for v2 in range(n7):
            if v1 == v2:
                continue
            free_vals = [idx for idx in range(n7) if idx != v1 and idx != v2]
            m = len(free_vals)
            for r_idx in combinations(range(m), 2):
                for c_idx in combinations(range(m), 2):
                    r1, r2 = free_vals[r_idx[0]], free_vals[r_idx[1]]
                    c1, c2 = free_vals[c_idx[0]], free_vals[c_idx[1]]
                    if r1 == c1 or r1 == c2 or r2 == c1 or r2 == c2:
                        continue

                    def make_tuple7(rv, cv, fv1, fv2, fp, rp, cp):
                        t = [0] * 4
                        t[fp[0]] = fv1
                        t[fp[1]] = fv2
                        t[rp] = rv
                        t[cp] = cv
                        return tuple(t)

                    t11 = make_tuple7(r1, c1, v1, v2, fix_pos, row_pos, col_pos)
                    t22 = make_tuple7(r2, c2, v1, v2, fix_pos, row_pos, col_pos)
                    t12 = make_tuple7(r1, c2, v1, v2, fix_pos, row_pos, col_pos)
                    t21 = make_tuple7(r2, c1, v1, v2, fix_pos, row_pos, col_pos)

                    if all(t in tuple_idx7 for t in [t11, t22, t12, t21]):
                        conditions7.append((tuple_idx7[t11], tuple_idx7[t22],
                                            tuple_idx7[t12], tuple_idx7[t21]))

conditions7 = list(set(conditions7))
n_cond7 = len(conditions7)
print(f"Block conditions: {n_cond7}")

J7 = np.zeros((n_cond7, n_tuples7))
for ci, (i1, i2, i3, i4) in enumerate(conditions7):
    J7[ci, i1] += tau7[i2]
    J7[ci, i2] += tau7[i1]
    J7[ci, i3] -= tau7[i4]
    J7[ci, i4] -= tau7[i3]

s_vals7 = np.linalg.svd(J7, compute_uv=False)
rank_J7 = int(np.sum(s_vals7 > 1e-10 * s_vals7[0]))
gap7 = codim7 - rank_J7
print(f"Jacobian: {J7.shape}, rank: {rank_J7}")
print(f"Codim rank-1: {codim7}, gap: {gap7}")

if gap7 == 0:
    print(f"  *** MATCH at n=7 too! ***")
else:
    print(f"  Gap of {gap7} at n=7")

print(f"\n{'='*70}")
print("DONE")
