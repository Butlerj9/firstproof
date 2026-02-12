"""
P03 EXP-11: Solve at q very close to 1 with exact Fraction arithmetic.
Use h = q-1 = -1/k for k = 50, 100, 200, etc.
Then polynomial extrapolation on c(h) as h -> 0.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction
from itertools import permutations as perms

print("P03 EXP-11: Close-to-1 exact solves + extrapolation")
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

def symmetry_deviation(c):
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c[i]
    coeffs[leading] = Fraction(1)
    max_dev = Fraction(0)
    for m, val in coeffs.items():
        for p in perms(m):
            if p in coeffs:
                d = abs(coeffs[p] - val)
                if d > max_dev: max_dev = d
    return max_dev

t_val = Fraction(7, 10)

# Phase 1: Time test at different q values
print(f"\n  Phase 1: Timing test (t = 7/10)")
for k in [10, 20, 50]:
    q_val = Fraction(k-1, k)
    t0 = time.time()
    c = solve_at_q(q_val, t_val)
    elapsed = time.time() - t0
    if c:
        dev = symmetry_deviation(c)
        # Check fraction size
        max_num = max(abs(x.numerator) for x in c if x != 0)
        max_den = max(abs(x.denominator) for x in c if x != 0)
        num_digits = len(str(max_num))
        den_digits = len(str(max_den))
        print(f"  q={k-1}/{k}: {elapsed:.1f}s, asym={float(dev):.4e}, digits~{num_digits}/{den_digits}")
    sys.stdout.flush()

# Phase 2: Solve at geometrically-spaced q values and Richardson extrapolate
print(f"\n  Phase 2: Geometric spacing + Richardson")
# Use h = -1/k^2 to get rapid convergence
h_vals = []
c_vals = []

for k in [5, 7, 10, 14, 20, 28, 40]:
    q_val = Fraction(k*k - 1, k*k)  # q = 1 - 1/k^2
    h = q_val - 1  # = -1/k^2
    t0 = time.time()
    c = solve_at_q(q_val, t_val)
    elapsed = time.time() - t0
    if c:
        h_vals.append(h)
        c_vals.append(c)
        dev = symmetry_deviation(c)
        print(f"  q=1-1/{k}^2={q_val}: {elapsed:.1f}s, asym={float(dev):.4e}")
    sys.stdout.flush()

if len(c_vals) >= 3:
    print(f"\n  Phase 3: Richardson extrapolation to h=0")
    for n_pts in range(3, len(c_vals)+1):
        hs = h_vals[:n_pts]
        cs = c_vals[:n_pts]

        # Neville's algorithm targeting h=0
        m = len(hs)
        T = [[None]*m for _ in range(m)]
        for i in range(m):
            T[i][0] = list(cs[i])
        target = Fraction(0)
        for j in range(1, m):
            for i in range(j, m):
                T[i][j] = [Fraction(0)] * N
                for idx in range(N):
                    num = (target - hs[i-j]) * T[i][j-1][idx] - (target - hs[i]) * T[i-1][j-1][idx]
                    den = hs[i] - hs[i-j]
                    T[i][j][idx] = Fraction(num, den)

        c_ext = T[m-1][m-1]
        dev = symmetry_deviation(c_ext)
        print(f"  {n_pts}-point: asym = {float(dev):.6e}")

        if dev == Fraction(0):
            print(f"  *** EXACT SYMMETRY at q=1 ***")
            coeffs = {}
            for i, m_idx in enumerate(unk_monoms):
                coeffs[m_idx] = c_ext[i]
            coeffs[leading] = Fraction(1)
            seen = set()
            for m_idx in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
                key = tuple(sorted(m_idx, reverse=True))
                if key not in seen:
                    seen.add(key)
                    print(f"    m_{key} = {coeffs[m_idx]}")
            break
        sys.stdout.flush()

print(f"\n{'='*70}")
print("DONE")
