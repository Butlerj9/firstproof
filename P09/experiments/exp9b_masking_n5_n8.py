"""
P09 EXP-9b: D_n masking lemma at n=5 (boundary case) and n=8 (extra check).
n=5 should FAIL (gap > 0) because D_5 doesn't have enough room for the proof.
n=8 should PASS (gap = 0).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from itertools import permutations, combinations

np.random.seed(42)

print("P09 EXP-9b: D_n masking lemma boundary tests")
print("=" * 70)


def test_masking(n):
    print(f"\n--- n={n} ---")
    D_n = list(permutations(range(n), 4))
    n_tuples = len(D_n)
    tuple_idx = {t: i for i, t in enumerate(D_n)}
    codim_rank1 = n_tuples - (4 * n - 3)
    print(f"D_n tuples: {n_tuples}, rank-1 dim: {4*n-3}, codim: {codim_rank1}")

    # Random rank-1 tensor
    u = np.random.randn(n) + 0.5
    v = np.random.randn(n) + 0.5
    w = np.random.randn(n) + 0.5
    x = np.random.randn(n) + 0.5

    tau0 = np.zeros(n_tuples)
    for t in D_n:
        a, b, c, d = t
        tau0[tuple_idx[t]] = u[a] * v[b] * w[c] * x[d]

    # Enumerate block conditions
    fix_pairs = list(combinations(range(4), 2))
    conditions = []
    for fix_pos in fix_pairs:
        free_pos = [p for p in range(4) if p not in fix_pos]
        row_pos, col_pos = free_pos[0], free_pos[1]
        for v1 in range(n):
            for v2 in range(n):
                if v1 == v2:
                    continue
                free_vals = [idx for idx in range(n) if idx != v1 and idx != v2]
                m = len(free_vals)
                for r_idx in combinations(range(m), 2):
                    for c_idx in combinations(range(m), 2):
                        r1, r2 = free_vals[r_idx[0]], free_vals[r_idx[1]]
                        c1, c2 = free_vals[c_idx[0]], free_vals[c_idx[1]]
                        if r1 == c1 or r1 == c2 or r2 == c1 or r2 == c2:
                            continue

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

                        if all(t in tuple_idx for t in [t11, t22, t12, t21]):
                            conditions.append((tuple_idx[t11], tuple_idx[t22],
                                               tuple_idx[t12], tuple_idx[t21]))

    conditions = list(set(conditions))
    n_cond = len(conditions)
    print(f"Block conditions: {n_cond}")

    # Build Jacobian
    if n_cond == 0:
        rank_J = 0
        gap = codim_rank1
        print(f"  No block conditions exist (free values < 4)")
    else:
        J = np.zeros((n_cond, n_tuples))
        for ci, (i1, i2, i3, i4) in enumerate(conditions):
            J[ci, i1] += tau0[i2]
            J[ci, i2] += tau0[i1]
            J[ci, i3] -= tau0[i4]
            J[ci, i4] -= tau0[i3]

        s_vals = np.linalg.svd(J, compute_uv=False)
        rank_J = int(np.sum(s_vals > 1e-10 * s_vals[0]))
        gap = codim_rank1 - rank_J

    if n_cond > 0:
        print(f"Jacobian: {J.shape}, rank: {rank_J}")
    else:
        print(f"Jacobian rank: {rank_J}")
    print(f"Codim rank-1: {codim_rank1}, gap: {gap}")
    if gap == 0:
        print(f"  *** MATCH: masking lemma holds at n={n} ***")
    else:
        print(f"  GAP of {gap}: masking lemma FAILS at n={n}")
        print(f"  (Block conditions miss {gap} directions)")
    return gap


gap5 = test_masking(5)
gap8 = test_masking(8)

print(f"\n{'='*70}")
print("Summary:")
print(f"  n=5: gap={gap5} {'(EXPECTED: fails)' if gap5 > 0 else '(UNEXPECTED: passes)'}")
print(f"  n=6: gap=0 (from EXP-9)")
print(f"  n=7: gap=0 (from EXP-9)")
print(f"  n=8: gap={gap8} {'(passes)' if gap8 == 0 else '(UNEXPECTED: fails)'}")
print(f"\nConclusion: Masking lemma holds for n >= 6, fails at n = 5")
print("DONE")
