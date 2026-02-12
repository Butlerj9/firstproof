"""
P03 EXP-6b: Perturbation expansion approach for Symmetry Conjecture at n=3.

Strategy: Write q = 1-eps. At eps=0, the 55x55 system degenerates to rank 5.
Use perturbation theory to find the specific element of the 50-dim null space
that is selected as eps -> 0. Check if it's symmetric.

Uses exact Fraction arithmetic for algebraic certainty.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fractions import Fraction
import time

print("P03 EXP-6b: Perturbation expansion for n=3 symmetry")
print("=" * 70)

def k_stat(nu, i):
    n = len(nu)
    count = 0
    for j in range(i):
        if nu[j] > nu[i]:
            count += 1
    for j in range(i+1, n):
        if nu[j] >= nu[i]:
            count += 1
    return count

# Enumerate compositions and monomials
comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

leading = (0, 2, 3)
vanishing_comps = [nu for nu in comps if nu != leading]
monoms = list(comps)
unknown_monoms = [m for m in monoms if m != leading]
n_unk = len(unknown_monoms)

print(f"  Compositions: {len(comps)}, Unknowns: {n_unk}")

# Fix t (rational)
t = Fraction(7, 10)

# ============================================================
# Phase 1: Solve at multiple q values near 1 using exact Fraction
# Then use polynomial fitting to extrapolate to q=1
# ============================================================
print(f"\nPhase 1: Exact Fraction solve at multiple q values")
print("-" * 60)

def solve_at_q(q_val, t_val):
    """Solve the 55x55 vanishing system at exact (q, t) using Fraction."""
    # Build system
    A = []
    b = []
    for nu in vanishing_comps:
        sv = [q_val**nu[i] * t_val**(-k_stat(nu, i)) for i in range(3)]
        row = [sv[0]**m[0] * sv[1]**m[1] * sv[2]**m[2] for m in unknown_monoms]
        A.append(row)
        rhs = -(sv[0]**leading[0] * sv[1]**leading[1] * sv[2]**leading[2])
        b.append(rhs)

    # Gaussian elimination
    n = n_unk
    aug = [A[i][:] + [b[i]] for i in range(n)]

    for col in range(n):
        pivot_row = None
        for row in range(col, n):
            if aug[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            return None
        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        pivot = aug[col][col]
        for row in range(col+1, n):
            if aug[row][col] != 0:
                factor = Fraction(aug[row][col], pivot)
                for j in range(col, n+1):
                    aug[row][j] -= factor * aug[col][j]

    solution = [Fraction(0)] * n
    for row in range(n-1, -1, -1):
        val = aug[row][n]
        for j in range(row+1, n):
            val -= aug[row][j] * solution[j]
        solution[row] = Fraction(val, aug[row][row])

    return solution

# Solve at several q values (small denominators for speed)
q_values = [Fraction(2, 3), Fraction(3, 4), Fraction(4, 5),
            Fraction(5, 6), Fraction(6, 7), Fraction(7, 8),
            Fraction(8, 9), Fraction(9, 10)]

solutions = {}
for q_val in q_values:
    start = time.time()
    sol = solve_at_q(q_val, t)
    elapsed = time.time() - start
    if sol is not None:
        solutions[q_val] = sol
        # Quick symmetry check
        coeffs = {m: sol[i] for i, m in enumerate(unknown_monoms)}
        coeffs[leading] = Fraction(1)

        max_asym = Fraction(0)
        for m, c in coeffs.items():
            key = tuple(sorted(m))
            for m2, c2 in coeffs.items():
                if tuple(sorted(m2)) == key and m2 != m:
                    diff = abs(c - c2)
                    if diff > max_asym:
                        max_asym = diff

        print(f"  q={q_val}: solved in {elapsed:.1f}s, max_asym={float(max_asym):.4e}")
    else:
        print(f"  q={q_val}: SINGULAR")
    sys.stdout.flush()

# ============================================================
# Phase 2: Neville's algorithm for polynomial extrapolation to q=1
# ============================================================
print(f"\nPhase 2: Neville extrapolation to q=1")
print("-" * 60)

q_list = sorted(solutions.keys())
n_pts = len(q_list)
print(f"  Using {n_pts} data points")

# For each coefficient, extrapolate to q=1
coeffs_q1 = {}
for idx, m in enumerate(unknown_monoms):
    # Neville's algorithm
    P = [[Fraction(0)] * n_pts for _ in range(n_pts)]
    for i in range(n_pts):
        P[i][0] = solutions[q_list[i]][idx]

    for j in range(1, n_pts):
        for i in range(n_pts - j):
            num = (Fraction(1) - q_list[i]) * P[i+1][j-1] - (Fraction(1) - q_list[i+j]) * P[i][j-1]
            den = q_list[i+j] - q_list[i]
            P[i][j] = Fraction(num, den)

    coeffs_q1[m] = P[0][n_pts - 1]

coeffs_q1[leading] = Fraction(1)

# Check symmetry
print(f"\n  Symmetry check at extrapolated q=1:")
sym_groups = {}
for m, c in coeffs_q1.items():
    key = tuple(sorted(m))
    if key not in sym_groups:
        sym_groups[key] = []
    sym_groups[key].append((m, c))

all_symmetric = True
max_asym = Fraction(0)
asym_pairs = 0
for key, group in sorted(sym_groups.items()):
    vals = [c for _, c in group]
    if len(vals) > 1:
        for i in range(1, len(vals)):
            diff = abs(vals[i] - vals[0])
            if diff > max_asym:
                max_asym = diff
            if diff > 0:
                all_symmetric = False
                asym_pairs += 1

if all_symmetric:
    print(f"  *** EXACT SYMMETRY at q=1 (Neville extrapolation, {n_pts} points) ***")
    print(f"  All coefficient groups match exactly")
else:
    print(f"  NOT exactly symmetric: max_asym = {float(max_asym):.6e}, pairs = {asym_pairs}")
    print(f"  (This may be due to extrapolation error with limited q points)")

    # Try with more points - add q values with larger denominators
    print(f"\n  Trying with additional q values...")

# ============================================================
# Phase 3: Higher-order extrapolation
# ============================================================
print(f"\nPhase 3: Extended q range + more points")
print("-" * 60)

extra_q = [Fraction(10, 11), Fraction(11, 12), Fraction(12, 13),
           Fraction(13, 14), Fraction(14, 15), Fraction(15, 16)]

for q_val in extra_q:
    start = time.time()
    sol = solve_at_q(q_val, t)
    elapsed = time.time() - start
    if sol is not None:
        solutions[q_val] = sol
        print(f"  q={q_val}: solved in {elapsed:.1f}s")
    sys.stdout.flush()

q_list = sorted(solutions.keys())
n_pts = len(q_list)
print(f"\n  Now using {n_pts} data points for Neville extrapolation")

# Re-extrapolate with more points
coeffs_q1_v2 = {}
for idx, m in enumerate(unknown_monoms):
    P = [[Fraction(0)] * n_pts for _ in range(n_pts)]
    for i in range(n_pts):
        P[i][0] = solutions[q_list[i]][idx]

    for j in range(1, n_pts):
        for i in range(n_pts - j):
            num = (Fraction(1) - q_list[i]) * P[i+1][j-1] - (Fraction(1) - q_list[i+j]) * P[i][j-1]
            den = q_list[i+j] - q_list[i]
            P[i][j] = Fraction(num, den)

    coeffs_q1_v2[m] = P[0][n_pts - 1]

coeffs_q1_v2[leading] = Fraction(1)

# Check symmetry
sym_groups_v2 = {}
for m, c in coeffs_q1_v2.items():
    key = tuple(sorted(m))
    if key not in sym_groups_v2:
        sym_groups_v2[key] = []
    sym_groups_v2[key].append((m, c))

all_symmetric_v2 = True
max_asym_v2 = Fraction(0)
for key, group in sorted(sym_groups_v2.items()):
    vals = [c for _, c in group]
    if len(vals) > 1:
        for i in range(1, len(vals)):
            diff = abs(vals[i] - vals[0])
            if diff > max_asym_v2:
                max_asym_v2 = diff
            if diff > 0:
                all_symmetric_v2 = False

if all_symmetric_v2:
    print(f"  *** EXACT SYMMETRY at q=1 (extended Neville, {n_pts} points) ***")

    # Verify: print a few coefficient groups
    print(f"\n  Sample symmetric coefficient groups:")
    for key in sorted(sym_groups_v2.keys())[:5]:
        group = sym_groups_v2[key]
        if len(group) > 1:
            val = float(group[0][1])
            mons = [m for m, _ in group]
            print(f"    {key} ({len(group)} monomials): value = {val:.10f}")
else:
    print(f"  NOT exactly symmetric: max_asym = {float(max_asym_v2):.6e}")

    # Show which groups are asymmetric
    print(f"\n  Asymmetric groups:")
    count = 0
    for key, group in sorted(sym_groups_v2.items()):
        vals = [c for _, c in group]
        if len(vals) > 1:
            diffs = [abs(vals[i] - vals[0]) for i in range(1, len(vals))]
            max_d = max(diffs)
            if max_d > 0:
                print(f"    {key}: max_diff = {float(max_d):.6e}")
                count += 1
                if count >= 5:
                    break

print(f"\n{'='*70}")
print("DONE")
