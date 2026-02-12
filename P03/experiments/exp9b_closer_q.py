"""
P03 EXP-9b: Exact rational-q with values closer to 1.

Use q = (k-1)/k for k = 2,3,...,20 and Richardson extrapolation.
"""

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P03 EXP-9b: Exact solve near q=1 + Richardson extrapolation")
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
            entry = (t_val ** t_exp) * (q_val ** q_exp)
            row.append(entry)
        A.append(row)
        m_lead = leading
        t_exp_l = -(k[0]*m_lead[0] + k[1]*m_lead[1] + k[2]*m_lead[2])
        q_exp_l = nu[0]*m_lead[0] + nu[1]*m_lead[1] + nu[2]*m_lead[2]
        b.append(-(t_val ** t_exp_l) * (q_val ** q_exp_l))

    aug = [A[i][:] + [b[i]] for i in range(N)]
    for col in range(N):
        piv = None
        for r in range(col, N):
            if aug[r][col] != Fraction(0):
                piv = r
                break
        if piv is None: return None
        if piv != col:
            aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        for r in range(col+1, N):
            if aug[r][col] != Fraction(0):
                f = Fraction(aug[r][col], pv)
                for j in range(col, N+1):
                    aug[r][j] -= f * aug[col][j]
    c = [Fraction(0)] * N
    for col in range(N-1, -1, -1):
        s = aug[col][N]
        for j in range(col+1, N):
            s -= aug[col][j] * c[j]
        c[col] = Fraction(s, aug[col][col])
    return c

def check_symmetry(c):
    from itertools import permutations as perms
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c[i]
    coeffs[leading] = Fraction(1)

    max_asym = Fraction(0)
    for m, val in coeffs.items():
        key = tuple(sorted(m, reverse=True))
        for p in perms(m):
            if p in coeffs:
                diff = abs(coeffs[p] - val)
                if diff > max_asym:
                    max_asym = diff
    return max_asym

t_val = Fraction(7, 10)

# Solve at q = (k-1)/k for various k
print(f"\n  Phase 1: Solve at q values near 1 (t=7/10)")
q_values = []
c_values = []

for k in range(2, 16):
    q_val = Fraction(k-1, k)
    t0 = time.time()
    c = solve_at_q(q_val, t_val)
    elapsed = time.time() - t0
    if c is None:
        print(f"    q={k-1}/{k}: SINGULAR ({elapsed:.1f}s)")
        continue
    q_values.append(q_val)
    c_values.append(c)
    asym = check_symmetry(c)
    print(f"    q={k-1}/{k}: solved ({elapsed:.1f}s), asym={float(asym):.4e}")
    sys.stdout.flush()

# Richardson extrapolation using subsets
print(f"\n  Phase 2: Richardson extrapolation")

for n_pts in [4, 6, 8, 10, 12, 14]:
    if n_pts > len(q_values):
        break
    # Use last n_pts values (closest to q=1)
    qs = q_values[-n_pts:]
    cs = c_values[-n_pts:]

    # Neville
    m = len(qs)
    T = [[None]*m for _ in range(m)]
    for i in range(m):
        T[i][0] = list(cs[i])

    target = Fraction(1)
    for j in range(1, m):
        for i in range(j, m):
            T[i][j] = [Fraction(0)] * N
            for idx in range(N):
                num = (target - qs[i-j]) * T[i][j-1][idx] - (target - qs[i]) * T[i-1][j-1][idx]
                den = qs[i] - qs[i-j]
                T[i][j][idx] = Fraction(num, den)

    c_ext = T[m-1][m-1]
    asym = check_symmetry(c_ext)
    print(f"    {n_pts}-point Richardson: asym = {float(asym):.6e}")
    sys.stdout.flush()

    if asym == Fraction(0):
        print(f"    *** EXACT SYMMETRY ***")
        # Print coefficients
        coeffs = {}
        for i, m_idx in enumerate(unk_monoms):
            coeffs[m_idx] = c_ext[i]
        coeffs[leading] = Fraction(1)

        print(f"\n    Partition coefficients:")
        seen = set()
        for m_idx in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
            key = tuple(sorted(m_idx, reverse=True))
            if key not in seen:
                seen.add(key)
                print(f"      m_{key} = {coeffs[m_idx]}")
        break

print(f"\n{'='*70}")
print("DONE")
