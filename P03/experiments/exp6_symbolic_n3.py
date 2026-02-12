"""
P03 EXP-6: Attempt symbolic proof of Symmetry Conjecture for n=3.

Strategy: Fix t to a specific rational value, solve the 55x55 vanishing
system symbolically in q using SymPy, then take the q->1 limit and check symmetry.

If symmetry holds at a specific rational t, and we verify at multiple t values,
this provides algebraic certainty (not just numerical).
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fractions import Fraction
from itertools import product as cartprod
import time

print("P03 EXP-6: Symbolic n=3 Symmetry Conjecture attempt")
print("=" * 70)

# ============================================================
# Phase 1: Exact rational arithmetic at q very close to 1
# ============================================================
print("\nPhase 1: Exact rational arithmetic at specific (q, t)")
print("-" * 60)

def k_stat(nu, i):
    """k_i(nu) = #{j<i: nu[j]>nu[i]} + #{j>i: nu[j]>=nu[i]}"""
    n = len(nu)
    count = 0
    for j in range(i):
        if nu[j] > nu[i]:
            count += 1
    for j in range(i+1, n):
        if nu[j] >= nu[i]:
            count += 1
    return count

def spectral_vector_frac(nu, q, t):
    """Spectral vector using Fraction arithmetic."""
    return [q**nu[i] * t**(-k_stat(nu, i)) for i in range(len(nu))]

# Enumerate all compositions of weight <= 5 into 3 parts
comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))
print(f"  Total compositions: {len(comps)}")

# Monomials of total degree <= 5 in 3 vars
monoms = list(comps)  # Same enumeration
leading = (0, 2, 3)
leading_idx = monoms.index(leading)
print(f"  Leading monomial index: {leading_idx}")

# Vanishing compositions (all except lambda^-)
vanishing_comps = [nu for nu in comps if nu != leading]
unknown_monoms = [m for m in monoms if m != leading]
n_unknowns = len(unknown_monoms)
print(f"  Unknowns: {n_unknowns}, Vanishing conditions: {len(vanishing_comps)}")

# Solve at specific (q, t) using Fraction
t_val = Fraction(7, 10)

# Test at several q values near 1, check how symmetric the result is
for q_num, q_den in [(99, 100), (999, 1000), (9999, 10000)]:
    q_val = Fraction(q_num, q_den)

    # Build system A*c = b
    A = []
    b = []
    for nu in vanishing_comps:
        sv = spectral_vector_frac(nu, q_val, t_val)
        row = []
        for m in unknown_monoms:
            val = sv[0]**m[0] * sv[1]**m[1] * sv[2]**m[2]
            row.append(val)
        A.append(row)
        # RHS: -leading_monomial(sv)
        rhs = -(sv[0]**leading[0] * sv[1]**leading[1] * sv[2]**leading[2])
        b.append(rhs)

    # Solve using Gaussian elimination with Fraction
    n = n_unknowns
    # Augmented matrix
    aug = [A[i][:] + [b[i]] for i in range(n)]

    start = time.time()
    # Forward elimination
    for col in range(n):
        # Find pivot
        pivot_row = None
        for row in range(col, n):
            if aug[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            print(f"    q={q_num}/{q_den}: SINGULAR at col {col}")
            break
        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        pivot = aug[col][col]
        for row in range(col+1, n):
            if aug[row][col] != 0:
                factor = aug[row][col] / pivot
                for j in range(col, n+1):
                    aug[row][j] -= factor * aug[col][j]
    else:
        # Back substitution
        solution = [Fraction(0)] * n
        for row in range(n-1, -1, -1):
            val = aug[row][n]
            for j in range(row+1, n):
                val -= aug[row][j] * solution[j]
            solution[row] = val / aug[row][row]

        elapsed = time.time() - start

        # Build coefficient dict
        coeffs = {}
        for i, m in enumerate(unknown_monoms):
            coeffs[m] = solution[i]
        coeffs[leading] = Fraction(1)

        # Check symmetry: group by sorted monomial
        sym_groups = {}
        for m, c in coeffs.items():
            key = tuple(sorted(m))
            if key not in sym_groups:
                sym_groups[key] = []
            sym_groups[key].append((m, c))

        max_asym = Fraction(0)
        asym_count = 0
        for key, group in sym_groups.items():
            vals = [c for _, c in group]
            if len(vals) > 1:
                for i in range(1, len(vals)):
                    diff = abs(vals[i] - vals[0])
                    if diff > max_asym:
                        max_asym = diff
                    if diff > 0:
                        asym_count += 1

        print(f"    q={q_num}/{q_den}: solved in {elapsed:.1f}s, "
              f"max asymmetry = {float(max_asym):.3e}, "
              f"asymmetric pairs = {asym_count}")

        # If close to q=1, show a few coefficient values
        if q_num == 9999:
            print(f"    Sample coefficients:")
            for key in sorted(sym_groups.keys())[:3]:
                group = sym_groups[key]
                if len(group) > 1:
                    print(f"      {key}: {[float(c) for _, c in group[:3]]}")

print(f"\n{'='*70}")

# ============================================================
# Phase 2: SymPy symbolic solve (if fast enough)
# ============================================================
print("\nPhase 2: SymPy symbolic solve at fixed t=7/10")
print("-" * 60)

try:
    from sympy import symbols, Rational, solve, limit, simplify, Matrix, expand
    from sympy import Symbol

    q = Symbol('q')
    t_sym = Rational(7, 10)

    print(f"  Building 55x55 system with symbolic q...")
    start = time.time()

    # Build system
    A_sym = []
    b_sym = []
    for nu in vanishing_comps:
        sv = [q**nu[i] * t_sym**(-k_stat(nu, i)) for i in range(3)]
        row = []
        for m in unknown_monoms:
            val = sv[0]**m[0] * sv[1]**m[1] * sv[2]**m[2]
            row.append(expand(val))
        A_sym.append(row)
        rhs = -(sv[0]**leading[0] * sv[1]**leading[1] * sv[2]**leading[2])
        b_sym.append(expand(rhs))

    build_time = time.time() - start
    print(f"  System built in {build_time:.1f}s")

    # Try solving with Matrix
    A_mat = Matrix(A_sym)
    b_vec = Matrix(b_sym)

    print(f"  Matrix shape: {A_mat.shape}")
    print(f"  Attempting LU solve... (this may take a while)")
    sys.stdout.flush()

    start = time.time()
    # Use a timeout - if this takes too long, skip
    import signal

    # On Windows, signal.alarm doesn't work. Use a simpler approach.
    sol = A_mat.solve(b_vec)
    solve_time = time.time() - start
    print(f"  Solved in {solve_time:.1f}s")

    # Build coefficient dict
    coeffs_sym = {}
    for i, m in enumerate(unknown_monoms):
        coeffs_sym[m] = sol[i]
    coeffs_sym[leading] = 1

    # Take q -> 1 limit
    print(f"  Taking q -> 1 limit...")
    coeffs_q1 = {}
    for m, c in coeffs_sym.items():
        lim = limit(c, q, 1)
        coeffs_q1[m] = lim

    # Check symmetry
    sym_groups = {}
    for m, c in coeffs_q1.items():
        key = tuple(sorted(m))
        if key not in sym_groups:
            sym_groups[key] = []
        sym_groups[key].append((m, c))

    all_symmetric = True
    for key, group in sym_groups.items():
        vals = [c for _, c in group]
        if len(vals) > 1:
            for i in range(1, len(vals)):
                diff = simplify(vals[i] - vals[0])
                if diff != 0:
                    all_symmetric = False
                    print(f"    ASYMMETRIC: {key}, diff = {diff}")

    if all_symmetric:
        print(f"  *** SYMMETRY PROVED for n=3, t=7/10! ***")
    else:
        print(f"  Symmetry check: NOT all symmetric")

except Exception as e:
    print(f"  SymPy solve failed: {e}")

print(f"\n{'='*70}")
print("DONE")
