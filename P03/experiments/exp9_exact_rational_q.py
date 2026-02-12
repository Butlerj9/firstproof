"""
P03 EXP-9: Exact rational-q computation and extrapolation to q=1.

Solve the 55x55 vanishing system at several rational q values using
exact Fraction arithmetic, then extrapolate to q=1 and check symmetry.

This avoids perturbation theory entirely: just compute the exact answer.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P03 EXP-9: Exact rational-q solve + extrapolation")
print("=" * 70)

n = 3
leading = (0, 2, 3)

comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

monoms = list(comps)
van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in monoms if m != leading]
N = len(unk_monoms)  # 55

def k_stat(nu, i):
    n = len(nu)
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i+1, n):
        if nu[j] >= nu[i]: count += 1
    return count

k_stats = {}
for nu in comps:
    k_stats[nu] = tuple(k_stat(nu, i) for i in range(n))

def solve_at_q(q_val, t_val):
    """Solve vanishing system at specific (q, t), return coefficient dict."""
    A = []
    b = []
    for nu in van_comps:
        k = k_stats[nu]
        row = []
        for m in unk_monoms:
            t_exp = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2])
            q_exp = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2]
            entry = (t_val ** t_exp) * (q_val ** q_exp)
            row.append(entry)
        A.append(row)

        m_lead = leading
        t_exp_l = -(k[0]*m_lead[0] + k[1]*m_lead[1] + k[2]*m_lead[2])
        q_exp_l = nu[0]*m_lead[0] + nu[1]*m_lead[1] + nu[2]*m_lead[2]
        b.append(-(t_val ** t_exp_l) * (q_val ** q_exp_l))

    # Gaussian elimination with partial pivoting (exact fractions)
    aug = [A[i][:] + [b[i]] for i in range(N)]

    for col in range(N):
        # Find pivot
        piv = None
        for r in range(col, N):
            if aug[r][col] != Fraction(0):
                piv = r
                break
        if piv is None:
            return None  # Singular
        if piv != col:
            aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        for r in range(col+1, N):
            if aug[r][col] != Fraction(0):
                f = Fraction(aug[r][col], pv)
                for j in range(col, N+1):
                    aug[r][j] -= f * aug[col][j]

    # Back substitution
    c = [Fraction(0)] * N
    for col in range(N-1, -1, -1):
        s = aug[col][N]
        for j in range(col+1, N):
            s -= aug[col][j] * c[j]
        c[col] = Fraction(s, aug[col][col])

    return c

def check_symmetry(c):
    """Check if coefficient vector gives a symmetric polynomial."""
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c[i]
    coeffs[leading] = Fraction(1)

    max_asym = Fraction(0)
    for m, val in coeffs.items():
        key = tuple(sorted(m, reverse=True))
        # Check all permutations
        from itertools import permutations
        for p in permutations(m):
            if p in coeffs:
                diff = abs(coeffs[p] - val)
                if diff > max_asym:
                    max_asym = diff
    return max_asym

def richardson_extrapolate(q_vals, c_vals):
    """Neville-style Richardson extrapolation of c values to q=1."""
    # q_vals: list of q values
    # c_vals: list of coefficient vectors (each a list of N Fractions)
    # Returns extrapolated coefficient vector at q=1
    m = len(q_vals)
    # Neville's algorithm: T[i][j] = extrapolation using points i-j..i
    # Evaluated at q = 1
    T = [[None]*m for _ in range(m)]
    for i in range(m):
        T[i][0] = list(c_vals[i])

    target = Fraction(1)
    for j in range(1, m):
        for i in range(j, m):
            T[i][j] = [Fraction(0)] * N
            for k in range(N):
                num = (target - q_vals[i-j]) * T[i][j-1][k] - (target - q_vals[i]) * T[i-1][j-1][k]
                den = q_vals[i] - q_vals[i-j]
                T[i][j][k] = Fraction(num, den)

    return T[m-1][m-1]

# Test: single solve at q=1/2
t_val = Fraction(7, 10)
print(f"\n  Phase 1: Single solve test at q=1/2, t=7/10")
t0 = time.time()
c_half = solve_at_q(Fraction(1, 2), t_val)
elapsed = time.time() - t0
if c_half:
    asym = check_symmetry(c_half)
    print(f"    Solve time: {elapsed:.1f}s")
    print(f"    Asymmetry at q=1/2: {float(asym):.6e}")
else:
    print(f"    System singular at q=1/2")
sys.stdout.flush()

# Phase 2: Multiple q values + extrapolation
print(f"\n  Phase 2: Multi-point extrapolation to q=1")
# Use q values not too close to 1 (to keep fractions manageable)
q_values = [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)]
c_values = []

for q_val in q_values:
    t0 = time.time()
    c = solve_at_q(q_val, t_val)
    elapsed = time.time() - t0
    if c is None:
        print(f"    q={q_val}: SINGULAR")
        break
    c_values.append(c)
    asym = check_symmetry(c)
    print(f"    q={q_val}: solved ({elapsed:.1f}s), asymmetry={float(asym):.6e}")
    sys.stdout.flush()

if len(c_values) == len(q_values):
    print(f"\n  Phase 3: Richardson extrapolation ({len(q_values)} points)")
    t0 = time.time()
    c_extrap = richardson_extrapolate(q_values, c_values)
    elapsed = time.time() - t0
    print(f"    Extrapolation time: {elapsed:.1f}s")

    asym_extrap = check_symmetry(c_extrap)
    print(f"    Asymmetry at extrapolated q=1: {float(asym_extrap):.6e}")

    if asym_extrap == Fraction(0):
        print(f"    *** EXACT SYMMETRY at q=1 (rational extrapolation) ***")

        # Print some coefficients
        coeffs = {}
        for i, m in enumerate(unk_monoms):
            coeffs[m] = c_extrap[i]
        coeffs[leading] = Fraction(1)

        print(f"\n    Sample symmetric coefficients:")
        seen = set()
        count = 0
        for m in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
            key = tuple(sorted(m, reverse=True))
            if key not in seen:
                seen.add(key)
                print(f"      m_{key} = {coeffs[m]}")
                count += 1
                if count >= 8:
                    break
    else:
        print(f"    Asymmetry nonzero — extrapolation order may be insufficient")
        print(f"    Trying with more points...")

        # Try more points
        q_values2 = [Fraction(k, k+1) for k in range(2, 12)]
        c_values2 = []
        for q_val in q_values2:
            c = solve_at_q(q_val, t_val)
            if c is None:
                print(f"    q={q_val}: SINGULAR")
                break
            c_values2.append(c)
        if len(c_values2) == len(q_values2):
            c_extrap2 = richardson_extrapolate(q_values2, c_values2)
            asym2 = check_symmetry(c_extrap2)
            print(f"    10-point asymmetry: {float(asym2):.6e}")
            if asym2 == Fraction(0):
                print(f"    *** EXACT SYMMETRY (10-point Richardson) ***")

print(f"\n{'='*70}")
print("DONE")
