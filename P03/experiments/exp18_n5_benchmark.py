"""
P03 EXP-18: n=5 feasibility benchmark (corrected).
- Monomials have total degree <= weight (not = weight)
- For n=4: C(13,4)=715 monomials, N=714 (matches original scripts)
- For n=5: C(19,5)=11628 monomials, N=11627
- Time Gaussian elimination on actual n=4 system, extrapolate to n=5
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from math import comb

print("P03 EXP-18: n=5 Feasibility Benchmark (corrected)")
print("=" * 70)

# ==========================================
# Part 1: Correct system dimensions
# ==========================================
print("\n--- Part 1: System dimensions ---")

def monomial_count(weight, n):
    """Monomials x^nu with |nu| <= weight in n variables = C(weight+n, n)"""
    return comb(weight + n, n)

# n=4
n4 = 4
weight4 = 9  # lam=(4,3,2,0)
N4 = monomial_count(weight4, n4) - 1  # minus leading term
print(f"n=4: weight={weight4}, monomials={N4+1} = C({weight4+n4},{n4}), system N={N4}")

# n=5
n5 = 5
weight5 = 14  # lam=(5,4,3,2,0)
N5 = monomial_count(weight5, n5) - 1
print(f"n=5: weight={weight5}, monomials={N5+1} = C({weight5+n5},{n5}), system N={N5}")

# Degree bounds
deg4 = 2 * (n4 - 1) * weight4  # = 54
deg5 = 2 * (n5 - 1) * weight5  # = 112
print(f"\nn=4 degree bound: {deg4}, zero-test needs >{deg4} values")
print(f"n=5 degree bound: {deg5}, zero-test needs >{deg5} values")

# Perturbation orders (from observed pattern)
orders4 = 8
orders5_low = 8
orders5_high = 16
print(f"\nn=4 perturbation order: {orders4}")
print(f"n=5 perturbation order: {orders5_low}-{orders5_high} (estimated)")

# ==========================================
# Part 2: n=4 baseline — time Gauss on 714x714
# ==========================================
print("\n--- Part 2: n=4 Gauss baseline ({0}x{0}) ---".format(N4))

PRIME = 99999989

# Generate a random 714x714 matrix mod p (same structure as actual system)
np.random.seed(42)
A4 = np.random.randint(0, PRIME, size=(N4, N4), dtype=np.int64)

print(f"Running Gaussian elimination on {N4}x{N4} mod {PRIME}...")
t0 = time.perf_counter()

# Gauss elimination mod p (column pivoting)
aug = np.copy(A4)
nrows, ncols = aug.shape
pivot_row = 0
for col in range(ncols):
    found = -1
    for row in range(pivot_row, nrows):
        if aug[row, col] % PRIME != 0:
            found = row
            break
    if found == -1:
        continue
    if found != pivot_row:
        aug[[pivot_row, found]] = aug[[found, pivot_row]]
    inv_piv = pow(int(aug[pivot_row, col]), PRIME - 2, PRIME)
    aug[pivot_row] = (aug[pivot_row] * inv_piv) % PRIME
    for row in range(nrows):
        if row != pivot_row and aug[row, col] % PRIME != 0:
            factor = aug[row, col]
            aug[row] = (aug[row] - factor * aug[pivot_row]) % PRIME
    pivot_row += 1

t_gauss4 = time.perf_counter() - t0
rank4 = pivot_row
print(f"Gauss time (714x714): {t_gauss4:.2f}s, rank={rank4}")

# Also time the augmented version [A|I] which is what the actual code does
print(f"\nRunning augmented Gauss [A|I] ({N4}x{2*N4})...")
aug2 = np.zeros((N4, 2*N4), dtype=np.int64)
aug2[:, :N4] = np.random.randint(0, PRIME, size=(N4, N4), dtype=np.int64)
for i in range(N4):
    aug2[i, N4+i] = 1

t0 = time.perf_counter()
nrows, ncols = N4, 2*N4
pivot_row = 0
for col in range(N4):  # only pivot on first N4 columns
    found = -1
    for row in range(pivot_row, nrows):
        if aug2[row, col] % PRIME != 0:
            found = row
            break
    if found == -1:
        continue
    if found != pivot_row:
        aug2[[pivot_row, found]] = aug2[[found, pivot_row]]
    inv_piv = pow(int(aug2[pivot_row, col]), PRIME - 2, PRIME)
    aug2[pivot_row] = (aug2[pivot_row] * inv_piv) % PRIME
    for row in range(nrows):
        if row != pivot_row and aug2[row, col] % PRIME != 0:
            factor = aug2[row, col]
            aug2[row] = (aug2[row] - factor * aug2[pivot_row]) % PRIME
    pivot_row += 1

t_gauss4_aug = time.perf_counter() - t0
print(f"Augmented Gauss time: {t_gauss4_aug:.2f}s")

# Use augmented time as baseline (more realistic)
t_baseline = t_gauss4_aug
print(f"\nBaseline per Gauss: {t_baseline:.2f}s")
t_per_tv_n4 = t_baseline * orders4
print(f"Baseline per t-value (x{orders4} orders): {t_per_tv_n4:.1f}s")

# ==========================================
# Part 3: n=5 extrapolation
# ==========================================
print("\n--- Part 3: n=5 extrapolation ---")

# Gauss is O(N^2 * M) where M = number of columns
# For [A|I]: M = 2N, so O(N^3)
# For the actual RREF: O(N^2 * N) = O(N^3) per order
scaling = (N5 / N4) ** 3
print(f"Scaling factor: ({N5}/{N4})^3 = {scaling:.1f}")

t_gauss5_est = t_baseline * scaling
print(f"n=5 Gauss per order: {t_gauss5_est:.0f}s = {t_gauss5_est/3600:.1f} hours")

for orders5 in [orders5_low, 12, orders5_high]:
    t_per_tv5 = t_gauss5_est * orders5
    n_values = deg5 + 1  # need > degree_bound values
    t_total = n_values * t_per_tv5
    print(f"\n  With {orders5} perturbation orders:")
    print(f"    Per t-value: {t_per_tv5:.0f}s = {t_per_tv5/3600:.1f} hours")
    print(f"    Total ({n_values} values): {t_total:.0f}s = {t_total/3600:.0f} hours = {t_total/86400:.1f} days")

# ==========================================
# Part 4: Memory estimate
# ==========================================
print("\n--- Part 4: Memory estimate ---")

# Augmented matrix [A|I]: N5 x 2*N5 int64
mem_aug = N5 * 2 * N5 * 8
# Plus transformation matrix, RHS vectors, workspace
mem_total = 4 * N5 * N5 * 8  # ~4 full matrices
print(f"Single {N5}x{N5} int64 matrix: {N5*N5*8/1e9:.2f} GB")
print(f"Working set (~4 matrices): {mem_total/1e9:.1f} GB")
print(f"Available: 192 GB — {'SUFFICIENT' if mem_total < 192e9 else 'INSUFFICIENT'}")

# ==========================================
# Part 5: Verdict
# ==========================================
print("\n" + "=" * 70)
print("VERDICT")
print("=" * 70)

# Use middle estimate (12 orders)
orders_mid = 12
t_mid = t_gauss5_est * orders_mid * (deg5 + 1)
print(f"  System: {N5}x{N5} matrix, {deg5+1} t-values, ~{orders_mid} perturbation orders")
print(f"  RAM: {mem_total/1e9:.1f} GB needed / 192 GB available — SUFFICIENT")
print(f"  CPU: {t_mid/86400:.0f} days (single-threaded, 12 orders)")
print(f"  Bottleneck: CPU time")

if t_mid > 86400:
    print(f"  STATUS: INFEASIBLE within 1-day sprint ({t_mid/86400:.0f}x over)")
elif t_mid > 3600:
    print(f"  STATUS: MARGINAL ({t_mid/3600:.1f} hours)")
else:
    print(f"  STATUS: FEASIBLE ({t_mid:.0f}s)")
