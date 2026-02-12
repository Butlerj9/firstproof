"""
P03 EXP-15: Feasibility probe for n=4 Symmetry Conjecture.
Determines:
1. Number of compositions of weight <= |lambda| into n=4 parts
2. Number of distinct k-vectors at q=1 (determines null space dimension)
3. Benchmark: one perturbation solve at a single t value
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P03 EXP-15: n=4 Feasibility Probe")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)  # anti-dominant
weight = sum(lam)  # = 9

# Step 1: Enumerate compositions of weight <= 9 into 4 parts
print(f"\nStep 1: Enumerate compositions (n={n}, |lambda|={weight})")
comps = []
for a in range(weight + 1):
    for b in range(weight + 1 - a):
        for c in range(weight + 1 - a - b):
            for d in range(weight + 1 - a - b - c):
                comps.append((a, b, c, d))

print(f"  Total compositions: {len(comps)}")
assert leading in comps, "Leading composition not in list!"

van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in comps if m != leading]
N = len(unk_monoms)
print(f"  Unknowns (N): {N}")

# Step 2: Compute k-vectors
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

# Count distinct k-vectors
distinct_k = set(k_stats.values())
k_of_leading = k_stats[leading]
distinct_k_excl = distinct_k - {k_of_leading}

print(f"\nStep 2: k-vector analysis")
print(f"  Distinct k-vectors (total): {len(distinct_k)}")
print(f"  Leading k-vector: {k_of_leading}")
print(f"  Distinct k-vectors (excl leading): {len(distinct_k_excl)}")

# Count compositions per k-vector
from collections import Counter
k_counter = Counter(k_stats.values())
print(f"  Largest k-vector group: {max(k_counter.values())} compositions")
print(f"  Smallest k-vector group: {min(k_counter.values())} compositions")

# Null space dimension estimate
rank_at_q1 = len(distinct_k_excl)  # number of distinct vanishing conditions
null_dim_est = N - rank_at_q1
print(f"\nStep 3: Null space estimate")
print(f"  Rank of vanishing system at q=1: {rank_at_q1}")
print(f"  Null space dimension: {null_dim_est}")
print(f"  (n=3 comparison: N=55, rank=5, null=49)")

# Step 4: Quick benchmark of matrix operations
print(f"\nStep 4: Benchmark matrix operations")
print(f"  Building matrices at t=7/10, order 0...")

t_val = Fraction(7, 10)

def binom_frac(p, k):
    if k < 0: return Fraction(0)
    if k == 0: return Fraction(1)
    fk = Fraction(1)
    for i in range(1, k + 1):
        fk *= Fraction(i)
    r = Fraction(1)
    for i in range(k):
        r *= Fraction(p - i)
    return r / fk

t0 = time.time()
# Build order-0 matrix only for timing
A0 = []
b0 = []
for nu in van_comps:
    k = k_stats[nu]
    row = []
    for m in unk_monoms:
        t_exp = -(k[0] * m[0] + k[1] * m[1] + k[2] * m[2] + k[3] * m[3])
        p = nu[0] * m[0] + nu[1] * m[1] + nu[2] * m[2] + nu[3] * m[3]
        tp = t_val ** abs(t_exp) if t_exp >= 0 else Fraction(1) / (t_val ** (-t_exp))
        row.append(binom_frac(p, 0) * tp)  # order 0: binom(p,0) = 1
    A0.append(row)
    t_exp_l = -(k[0] * leading[0] + k[1] * leading[1] + k[2] * leading[2] + k[3] * leading[3])
    p_l = nu[0] * leading[0] + nu[1] * leading[1] + nu[2] * leading[2] + nu[3] * leading[3]
    tp_l = t_val ** abs(t_exp_l) if t_exp_l >= 0 else Fraction(1) / (t_val ** (-t_exp_l))
    b0.append(-binom_frac(p_l, 0) * tp_l)

t_build = time.time() - t0
print(f"  Matrix build time: {t_build:.1f}s ({N}x{N} Fraction matrix)")

# Gaussian elimination for rank
print(f"  Running Gaussian elimination...")
t0 = time.time()

def gauss_elim_rank(mat, nrows, ncols, progress=True):
    """Gaussian elimination to find rank. Operates on copy."""
    aug = [row[:] for row in mat]
    pivots = []
    ri = 0
    last_report = time.time()
    for col in range(ncols):
        if progress and time.time() - last_report > 10:
            print(f"    ... col {col}/{ncols}, rank so far: {len(pivots)}")
            last_report = time.time()
        piv = None
        for r in range(ri, nrows):
            if aug[r][col] != Fraction(0):
                piv = r
                break
        if piv is None:
            continue
        pivots.append((ri, col))
        if piv != ri:
            aug[ri], aug[piv] = aug[piv], aug[ri]
        pv = aug[ri][col]
        for j in range(ncols):
            aug[ri][j] /= pv
        for r in range(nrows):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(ncols):
                    aug[r][j] -= f * aug[ri][j]
        ri += 1
    return len(pivots), pivots, aug

# Only do rank computation on a smaller submatrix first to estimate timing
# The full 714x714 might be slow, so let's time a 100x100 subblock first
sub_size = min(100, N)
sub_mat = [A0[i][:sub_size] for i in range(sub_size)]
t0_sub = time.time()
sub_rank, _, _ = gauss_elim_rank(sub_mat, sub_size, sub_size, progress=False)
t_sub = time.time() - t0_sub
print(f"  {sub_size}x{sub_size} sub-elimination: {t_sub:.1f}s (rank={sub_rank})")

# Extrapolate timing for full matrix
estimated_full = t_sub * (N / sub_size) ** 3
print(f"  Estimated full {N}x{N} elimination: {estimated_full:.0f}s ({estimated_full/60:.1f} min)")

# For n=3 comparison
print(f"\n  n=3 comparison:")
print(f"    N=55, rank_q1=5, null=49, perturbation order=4")
print(f"    Operations per order: ~55^2 * 49 = ~148,225")
print(f"  n=4 estimate:")
n4_ops = N * N * null_dim_est
print(f"    Operations per order: ~{N}^2 * {null_dim_est} = ~{n4_ops:,}")
print(f"    Ratio: {n4_ops / 148225:.0f}x (vs n=3)")

# Step 5: Degree estimate
print(f"\nStep 5: Degree estimate (based on n=3 pattern)")
print(f"  n=3 pattern: total_degree = 4 * (|lambda| - monomial_degree)")
print(f"  n=3: max degree = 4 * 5 = 20")
print(f"  If pattern generalizes with same constant:")
print(f"    n=4: max degree = 4 * {weight} = {4*weight}")
print(f"  If constant scales as 2(n-1):")
print(f"    n=4: max degree = {2*(n-1)} * {weight} = {2*(n-1)*weight}")
print(f"  These are upper-bound guesses; actual degree TBD from data.")

# Step 6: Summary
print(f"\n{'='*70}")
print(f"FEASIBILITY SUMMARY")
print(f"  N (unknowns):         {N}")
print(f"  Null space at q=1:    {null_dim_est}")
print(f"  Matrix build time:    {t_build:.1f}s")
print(f"  Est. full elim time:  {estimated_full:.0f}s ({estimated_full/60:.1f} min)")

if estimated_full < 600:
    print(f"  VERDICT: FEASIBLE (< 10 min per t-value)")
elif estimated_full < 3600:
    print(f"  VERDICT: MARGINAL (< 1 hour per t-value)")
else:
    print(f"  VERDICT: EXPENSIVE ({estimated_full/3600:.1f} hours per t-value)")

print(f"\n  If feasible, need:")
print(f"    - ~{null_dim_est // 50 + 1} perturbation orders (rough estimate)")
print(f"    - ~{max(4*weight, 2*(n-1)*weight) + 10} t-values for degree-bound proof")
print(f"    - Total time: ~{max(4*weight, 2*(n-1)*weight) + 10} * elim_time")
print(f"\nDONE")
