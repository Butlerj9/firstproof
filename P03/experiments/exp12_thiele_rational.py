"""
P03 EXP-12: Thiele continued fraction (rational interpolation) for exact q=1 limit.

c(q) is a rational function of q. Thiele's interpolation recovers rational
functions exactly from n+1 evaluation points if the degree is <= n/2.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from itertools import permutations as perms

print("P03 EXP-12: Thiele rational interpolation for exact q=1 limit")
print("=" * 70)

n = 3
leading = (0, 2, 3)

comps = []
for a in range(6):
    for b in range(6-a):
        for c in range(6-a-b):
            comps.append((a, b, c))

van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in comps if m != leading]
N = len(unk_monoms)

def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i+1, len(nu)):
        if nu[j] >= nu[i]: count += 1
    return count

k_stats = {}
for nu in comps:
    k_stats[nu] = tuple(k_stat(nu, i) for i in range(n))

def solve_at_q(q_val, t_val):
    A = []
    b = []
    for nu in van_comps:
        k = k_stats[nu]
        row = []
        for m in unk_monoms:
            t_exp = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2])
            q_exp = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2]
            row.append((t_val ** t_exp) * (q_val ** q_exp))
        A.append(row)
        t_exp_l = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2])
        q_exp_l = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2]
        b.append(-(t_val ** t_exp_l) * (q_val ** q_exp_l))

    aug = [A[i][:]+[b[i]] for i in range(N)]
    for col in range(N):
        piv = None
        for r in range(col, N):
            if aug[r][col] != Fraction(0): piv = r; break
        if piv is None: return None
        if piv != col: aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        for r in range(col+1, N):
            if aug[r][col] != Fraction(0):
                f = Fraction(aug[r][col], pv)
                for j in range(col, N+1): aug[r][j] -= f * aug[col][j]
    c = [Fraction(0)] * N
    for col in range(N-1, -1, -1):
        s = aug[col][N]
        for j in range(col+1, N): s -= aug[col][j] * c[j]
        c[col] = Fraction(s, aug[col][col])
    return c

def thiele_interpolate(xs, ys, target):
    """Thiele continued fraction interpolation.
    Returns the value at target of the rational function passing through (xs[i], ys[i])."""
    n_pts = len(xs)
    # Compute reciprocal differences
    # rho[i][0] = y[i]
    # rho[i][1] = (x[i] - x[i-1]) / (rho[i][0] - rho[i-1][0])
    # rho[i][k] = (x[i] - x[i-k]) / (rho[i][k-1] - rho[i-1][k-1]) + rho[i-1][k-2]
    rho = [[None]*n_pts for _ in range(n_pts)]
    for i in range(n_pts):
        rho[i][0] = ys[i]

    for k in range(1, n_pts):
        for i in range(k, n_pts):
            if k == 1:
                diff = rho[i][0] - rho[i-1][0]
                if diff == Fraction(0):
                    return None  # Pole in reciprocal differences
                rho[i][1] = Fraction(xs[i] - xs[i-1], 1) / diff
            else:
                diff = rho[i][k-1] - rho[i-1][k-1]
                if diff == Fraction(0):
                    return None
                rho[i][k] = Fraction(xs[i] - xs[i-k], 1) / diff + rho[i-1][k-2]

    # Evaluate continued fraction at target
    # f(x) = rho[0][0] + (x-x0) / (rho[1][1] + (x-x1) / (rho[2][2] - rho[0][0] + (x-x2) / (...)))
    # Actually, Thiele's formula is:
    # f(x) = a0 + (x-x0)/(a1 + (x-x1)/(a2 + (x-x2)/(a3 + ...)))
    # where a0 = rho[0][0], a1 = rho[1][1], a2 = rho[2][2], etc.

    # Build from bottom up
    val = rho[n_pts-1][n_pts-1]
    for k in range(n_pts-2, 0, -1):
        val = rho[k][k] + (target - xs[k]) / val
    val = rho[0][0] + (target - xs[0]) / val

    return val

t_val = Fraction(7, 10)

# Compute at several q values
print(f"\n  Computing solutions at multiple q values (t=7/10)...")
q_list = []
c_list = []
for k in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    q_val = Fraction(k, k+1)  # Use primes to avoid accidental cancellations
    t0 = time.time()
    c = solve_at_q(q_val, t_val)
    if c:
        q_list.append(q_val)
        c_list.append(c)
        print(f"  q={k}/{k+1}: solved ({time.time()-t0:.1f}s)")
    sys.stdout.flush()

print(f"\n  Total points: {len(q_list)}")

# Try Thiele interpolation on a single coefficient and check convergence
# Use coefficient index 0 (first unknown monomial)
target_q = Fraction(1)

print(f"\n  Phase 2: Thiele interpolation for individual coefficients")
# Test on a few coefficients
test_indices = [0, 1, 2, 5, 10]

for ci in test_indices:
    monom = unk_monoms[ci]
    partner = tuple(sorted(monom, reverse=True))
    # Find a permutation that's different
    for p in perms(monom):
        if p != monom and p in unk_monoms:
            pi = unk_monoms.index(p)
            break
    else:
        print(f"  Coeff {ci} {monom}: no permutation partner, skip")
        continue

    print(f"\n  Coeff {ci}: {monom} vs {unk_monoms[pi]}")

    for n_pts in range(5, len(q_list)+1, 2):
        qs = q_list[:n_pts]
        fs1 = [c_list[j][ci] for j in range(n_pts)]
        fs2 = [c_list[j][pi] for j in range(n_pts)]

        v1 = thiele_interpolate(qs, fs1, target_q)
        v2 = thiele_interpolate(qs, fs2, target_q)

        if v1 is not None and v2 is not None:
            diff = abs(v1 - v2)
            print(f"    {n_pts} pts: c[{monom}]={float(v1):.10f}, c[{unk_monoms[pi]}]={float(v2):.10f}, diff={float(diff):.6e}", end="")
            if diff == Fraction(0):
                print(f" ** EXACT MATCH **")
                break
            else:
                print()
        else:
            print(f"    {n_pts} pts: Thiele failed (pole in reciprocal diffs)")
    sys.stdout.flush()

# Phase 3: If individual coefficients match, do full symmetry check
print(f"\n  Phase 3: Full symmetry check with best Thiele interpolation")
n_pts = len(q_list)
qs = q_list[:n_pts]

c_extrap = []
success = True
for ci in range(N):
    fs = [c_list[j][ci] for j in range(n_pts)]
    v = thiele_interpolate(qs, fs, target_q)
    if v is None:
        print(f"  Thiele failed for coeff {ci}")
        success = False
        break
    c_extrap.append(v)

if success:
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c_extrap[i]
    coeffs[leading] = Fraction(1)

    max_dev = Fraction(0)
    for m, val in coeffs.items():
        for p in perms(m):
            if p in coeffs:
                d = abs(coeffs[p] - val)
                if d > max_dev: max_dev = d

    print(f"  Full symmetry deviation: {float(max_dev):.6e}")
    if max_dev == Fraction(0):
        print(f"  *** EXACT SYMMETRY PROVED (Thiele rational interpolation) ***")

        print(f"\n  Partition coefficients at q=1, t=7/10:")
        seen = set()
        for m_key in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
            key = tuple(sorted(m_key, reverse=True))
            if key not in seen:
                seen.add(key)
                print(f"    m_{key} = {coeffs[m_key]} = {float(coeffs[m_key]):.12f}")

print(f"\n{'='*70}")
print("DONE")
