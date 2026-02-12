"""
P03 EXP-15d: n=4 symmetry check via mpmath Richardson extrapolation.
Uses high-precision floating point (200+ digits) to extrapolate to q=1.
Much faster than Fraction arithmetic for the 714x714 system.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import mpmath
from itertools import permutations as perms

# Set precision: 300 decimal digits
mpmath.mp.dps = 300

print("P03 EXP-15d: n=4 mpmath Richardson Extrapolation")
print(f"Precision: {mpmath.mp.dps} decimal digits")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)

# Enumerate compositions
comps = []
for a in range(weight + 1):
    for b in range(weight + 1 - a):
        for c in range(weight + 1 - a - b):
            for d in range(weight + 1 - a - b - c):
                comps.append((a, b, c, d))

van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in comps if m != leading]
N = len(unk_monoms)
print(f"N = {N} unknowns")


def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]:
            count += 1
    for j in range(i + 1, len(nu)):
        if nu[j] >= nu[i]:
            count += 1
    return count


k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}


def build_system_mpmath(q_val, t_val):
    """Build the vanishing system at (q, t) using mpmath."""
    A = mpmath.matrix(N, N)
    b = mpmath.matrix(N, 1)
    for row_i, nu in enumerate(van_comps):
        k = k_stats[nu]
        spec = [q_val ** nu[j] * t_val ** (-k[j]) for j in range(n)]
        for col_j, m in enumerate(unk_monoms):
            val = mpmath.mpf(1)
            for j in range(n):
                val *= spec[j] ** m[j]
            A[row_i, col_j] = val
        val_l = mpmath.mpf(1)
        for j in range(n):
            val_l *= spec[j] ** leading[j]
        b[row_i] = -val_l
    return A, b


def solve_at_q(q_val, t_val):
    """Solve for coefficients at (q, t)."""
    A, b = build_system_mpmath(q_val, t_val)
    try:
        c = mpmath.lu_solve(A, b)
        return [c[i] for i in range(N)]
    except Exception as e:
        print(f"    Solve failed: {e}")
        return None


def richardson_extrapolate(t_val, n_points=10, k_start=3, k_step=3):
    """Richardson extrapolation to q=1 using Neville's algorithm.
    Uses q = 1 - 10^{-k} for k = k_start, k_start+k_step, ..."""
    ks = [k_start + i * k_step for i in range(n_points)]
    hs = [mpmath.mpf(10) ** (-k) for k in ks]
    qs = [mpmath.mpf(1) - h for h in hs]

    print(f"    Solving at {n_points} q values (k={ks[0]}..{ks[-1]})...")
    solutions = []
    for idx, q_val in enumerate(qs):
        t0 = time.time()
        c = solve_at_q(q_val, t_val)
        elapsed = time.time() - t0
        if c is None:
            print(f"    q=1-10^(-{ks[idx]}): FAILED")
            return None
        solutions.append(c)
        if idx == 0 or idx == n_points - 1:
            print(f"    q=1-10^(-{ks[idx]}): solved ({elapsed:.1f}s)")

    # Neville's algorithm for each coefficient
    print(f"    Richardson extrapolation...", end="")
    sys.stdout.flush()
    t0 = time.time()
    result = [mpmath.mpf(0)] * N
    for j in range(N):
        P = [solutions[i][j] for i in range(n_points)]
        for k_nev in range(1, n_points):
            for i in range(n_points - k_nev):
                P[i] = (hs[i] * P[i + 1] - hs[i + k_nev] * P[i]) / (hs[i] - hs[i + k_nev])
        result[j] = P[0]
    print(f" {time.time()-t0:.1f}s")
    return result


def check_symmetry(coeffs, tol_digits=20):
    """Check symmetry with high precision."""
    coeff_dict = {}
    for i, m in enumerate(unk_monoms):
        coeff_dict[m] = coeffs[i]
    coeff_dict[leading] = mpmath.mpf(1)

    max_asym = mpmath.mpf(0)
    broken = 0
    total = 0
    tol = mpmath.mpf(10) ** (-tol_digits)

    for m, val in coeff_dict.items():
        for p in perms(m):
            if p > m and p in coeff_dict:  # check each pair once
                diff = abs(coeff_dict[p] - val)
                total += 1
                if diff > tol:
                    broken += 1
                if diff > max_asym:
                    max_asym = diff

    # Report
    if max_asym > 0:
        log_asym = float(mpmath.log10(max_asym)) if max_asym > 0 else -999
    else:
        log_asym = -999
    return max_asym, broken, total, log_asym


# Test at several t values
t_values = [
    mpmath.mpf('7') / mpmath.mpf('10'),
    mpmath.mpf('1') / mpmath.mpf('3'),
    mpmath.mpf('3') / mpmath.mpf('2'),
    mpmath.mpf('5') / mpmath.mpf('3'),
]

print(f"\nTesting symmetry at {len(t_values)} t values:\n")

for t_val in t_values:
    t0 = time.time()
    print(f"  t = {mpmath.nstr(t_val, 5)}:")
    coeffs = richardson_extrapolate(t_val, n_points=10, k_start=3, k_step=3)
    if coeffs is None:
        print(f"    FAILED\n")
        continue
    max_asym, broken, total, log_asym = check_symmetry(coeffs, tol_digits=20)
    elapsed = time.time() - t0
    sym_str = "SYMMETRIC" if broken == 0 else f"BROKEN ({broken}/{total})"
    print(f"    Result: max_asym ~ 10^({log_asym:.0f}), {sym_str}")
    print(f"    Digits of symmetry: ~{-log_asym:.0f}")
    print(f"    Total time: {elapsed:.1f}s\n")

print("=" * 70)
print("DONE")
