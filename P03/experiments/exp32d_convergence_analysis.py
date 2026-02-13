"""
P03 EXP-32d: Convergence analysis near q=1.

Key insight from exp32c: E* coefficients c_m(q) are RATIONAL functions of q
(Vandermonde determinant in Cramer's rule vanishes at q=1 due to spectral collisions).
Polynomial degree fitting was a red herring.

This script:
1. Evaluates E* at q values approaching 1 to confirm the pole behavior
2. Checks whether D_i = (T_i - t)E* has the same pole order as E*
3. Tests if D_i/(1-q) converges or diverges
4. Tests if E* * (1-q)^k converges for some k (determines pole order)
5. Checks what the NORMALIZED quantity (T_i - t)E* / E* does at q=1
"""
import sys, io, time
from fractions import Fraction

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SEP = "=" * 70
t0 = time.time()

n = 3
leading = (0, 2, 3)

comps = []
for a in range(6):
    for b in range(6 - a):
        for c in range(6 - a - b):
            comps.append((a, b, c))

monoms = list(comps)
van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in monoms if m != leading]
N = len(unk_monoms)


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


def spectral_vec(nu, q_val, t_val):
    ks = k_stats[nu]
    return tuple(q_val ** nu[i] * t_val ** (-ks[i]) for i in range(n))


def build_system(q_val, t_val):
    A = []
    b = []
    for nu in van_comps:
        eta = spectral_vec(nu, q_val, t_val)
        row = []
        for m in unk_monoms:
            val = Fraction(1)
            for i in range(n):
                val *= eta[i] ** m[i]
            row.append(val)
        A.append(row)
        val_lead = Fraction(1)
        for i in range(n):
            val_lead *= eta[i] ** leading[i]
        b.append(-val_lead)
    return A, b


def gauss_solve(A, b_vec):
    nrows = len(A)
    ncols = len(A[0])
    aug = [A[i][:] + [b_vec[i]] for i in range(nrows)]
    pivots = []
    ri = 0
    for col in range(ncols):
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
        for j in range(ncols + 1):
            aug[ri][j] /= pv
        for r in range(nrows):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(ncols + 1):
                    aug[r][j] -= f * aug[ri][j]
        ri += 1
    rank = len(pivots)
    if rank < ncols:
        return None, rank
    x = [Fraction(0)] * ncols
    for r, c in pivots:
        x[c] = aug[r][ncols]
    return x, rank


# Hecke operator
def swap_vars(poly, i, j):
    result = {}
    for m, c in poly.items():
        new_m = list(m)
        new_m[i], new_m[j] = new_m[j], new_m[i]
        new_m = tuple(new_m)
        result[new_m] = result.get(new_m, Fraction(0)) + c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def poly_sub(p1, p2):
    result = dict(p1)
    for m, c in p2.items():
        result[m] = result.get(m, Fraction(0)) - c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def poly_add(p1, p2):
    result = dict(p1)
    for m, c in p2.items():
        result[m] = result.get(m, Fraction(0)) + c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def poly_scale(p, s):
    if s == Fraction(0):
        return {}
    return {m: c * s for m, c in p.items()}


def poly_mul_var(p, var_idx, power=1):
    return {tuple(m[j] + (power if j == var_idx else 0) for j in range(n)): c
            for m, c in p.items()}


def poly_div_by_diff(f_minus_sf, i, j):
    other_vars = [k for k in range(n) if k != i and k != j]
    groups = {}
    for m, c in f_minus_sf.items():
        other_key = tuple(m[k] for k in other_vars)
        ai, aj = m[i], m[j]
        if other_key not in groups:
            groups[other_key] = {}
        groups[other_key][(ai, aj)] = groups[other_key].get((ai, aj), Fraction(0)) + c
    result = {}
    for other_key, terms in groups.items():
        quotient = {}
        for (ai, aj), c in terms.items():
            if c == Fraction(0):
                continue
            if ai > aj:
                for k in range(ai - aj):
                    qi, qj = aj + k, ai - 1 - k
                    quotient[(qi, qj)] = quotient.get((qi, qj), Fraction(0)) + c
        for (qi, qj), c in quotient.items():
            if c == Fraction(0):
                continue
            new_m = [0] * n
            for idx, k in enumerate(other_vars):
                new_m[k] = other_key[idx]
            new_m[i] = qi
            new_m[j] = qj
            new_m = tuple(new_m)
            result[new_m] = result.get(new_m, Fraction(0)) + c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def hecke_operator(poly, i, t_val):
    j = i + 1
    sf = swap_vars(poly, i, j)
    f_minus_sf = poly_sub(poly, sf)
    quotient = poly_div_by_diff(f_minus_sf, i, j)
    term1 = poly_scale(sf, t_val)
    x_i_times_q = poly_mul_var(quotient, i, 1)
    term2 = poly_scale(x_i_times_q, t_val - Fraction(1))
    return poly_add(term1, term2)


# ============================================================
print(SEP)
print("SECTION 1: E* coefficient behavior near q=1")
print(SEP)
sys.stdout.flush()

t_val = Fraction(7, 10)
# q values approaching 1
q_vals_near_1 = [Fraction(1, 2), Fraction(3, 4), Fraction(7, 8),
                 Fraction(9, 10), Fraction(19, 20), Fraction(49, 50),
                 Fraction(99, 100), Fraction(199, 200)]

sample_monoms = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1)]

print(f"\nt = {t_val}")
print(f"Monitoring E* coefficients as q -> 1:\n")
print(f"{'q':>10s} | {'1-q':>10s} | ", end="")
for m in sample_monoms:
    print(f"{'c_'+str(m):>18s} | ", end="")
print()
print("-" * (12 + 21 * len(sample_monoms)))

for q_val in q_vals_near_1:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        print(f"  q={q_val}: singular (rank deficit)")
        continue
    eps = Fraction(1) - q_val
    print(f"{float(q_val):10.5f} | {float(eps):10.1e} | ", end="")
    for m in sample_monoms:
        idx = unk_monoms.index(m)
        val = sol[idx]
        print(f"{float(val):18.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 2: (1-q) * c_m(q) near q=1 — testing for simple pole")
print(SEP)
sys.stdout.flush()

print(f"\n{'q':>10s} | {'1-q':>10s} | ", end="")
for m in sample_monoms:
    print(f"{'(1-q)*c_'+str(m):>18s} | ", end="")
print()
print("-" * (12 + 21 * len(sample_monoms)))

for q_val in q_vals_near_1:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        continue
    eps = Fraction(1) - q_val
    print(f"{float(q_val):10.5f} | {float(eps):10.1e} | ", end="")
    for m in sample_monoms:
        idx = unk_monoms.index(m)
        val = sol[idx] * eps
        print(f"{float(val):18.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 3: D_i = (T_i - t)E* coefficient behavior near q=1")
print(SEP)
sys.stdout.flush()

# Track a few monomials in D0
D_sample_monoms = [(0, 1, 0), (1, 0, 0), (0, 1, 1), (1, 1, 0)]

print(f"\n{'q':>10s} | {'1-q':>10s} | ", end="")
for m in D_sample_monoms:
    print(f"{'D0_'+str(m):>18s} | ", end="")
print()
print("-" * (12 + 21 * len(D_sample_monoms)))

for q_val in q_vals_near_1:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        continue
    poly = {}
    for i, m in enumerate(unk_monoms):
        if sol[i] != Fraction(0):
            poly[m] = sol[i]
    poly[leading] = Fraction(1)

    T0_poly = hecke_operator(poly, 0, t_val)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    eps = Fraction(1) - q_val

    print(f"{float(q_val):10.5f} | {float(eps):10.1e} | ", end="")
    for m in D_sample_monoms:
        val = D0.get(m, Fraction(0))
        print(f"{float(val):18.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 4: R0 = D0/(1-q) coefficient behavior near q=1")
print(SEP)
sys.stdout.flush()

print(f"\n{'q':>10s} | {'1-q':>10s} | ", end="")
for m in D_sample_monoms:
    print(f"{'R0_'+str(m):>18s} | ", end="")
print()
print("-" * (12 + 21 * len(D_sample_monoms)))

for q_val in q_vals_near_1:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        continue
    poly = {}
    for i, m in enumerate(unk_monoms):
        if sol[i] != Fraction(0):
            poly[m] = sol[i]
    poly[leading] = Fraction(1)

    T0_poly = hecke_operator(poly, 0, t_val)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    eps = Fraction(1) - q_val

    print(f"{float(q_val):10.5f} | {float(eps):10.1e} | ", end="")
    for m in D_sample_monoms:
        val = D0.get(m, Fraction(0))
        R_val = val / eps if eps != Fraction(0) else Fraction(0)
        print(f"{float(R_val):18.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Normalized quantity (T_0 - t)E* / E* near q=1")
print(SEP)
sys.stdout.flush()

# Instead of looking at raw coefficients, evaluate E* and D0 at a specific x point
# and compute D0(x)/E*(x)
x_test = [Fraction(2), Fraction(3), Fraction(5)]

print(f"\nTest point x = {[float(x) for x in x_test]}")

def eval_poly(poly, x):
    val = Fraction(0)
    for m, c in poly.items():
        term = c
        for i in range(len(m)):
            term *= x[i] ** m[i]
        val += term
    return val

print(f"\n{'q':>10s} | {'1-q':>10s} | {'E*(x)':>18s} | {'D0(x)':>18s} | {'D0/E*':>14s} | {'D0/(1-q)':>18s} | {'D0/((1-q)*E*)':>18s}")
print("-" * 130)

for q_val in q_vals_near_1:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        continue
    poly = {}
    for i, m in enumerate(unk_monoms):
        if sol[i] != Fraction(0):
            poly[m] = sol[i]
    poly[leading] = Fraction(1)

    T0_poly = hecke_operator(poly, 0, t_val)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    eps = Fraction(1) - q_val

    E_val = eval_poly(poly, x_test)
    D0_val = eval_poly(D0, x_test)
    ratio = D0_val / E_val if E_val != Fraction(0) else None
    R_val = D0_val / eps if eps != Fraction(0) else None
    norm_R = D0_val / (eps * E_val) if eps != Fraction(0) and E_val != Fraction(0) else None

    print(f"{float(q_val):10.5f} | {float(eps):10.1e} | {float(E_val):18.6e} | {float(D0_val):18.6e} | ", end="")
    print(f"{float(ratio):14.6e} | " if ratio else "N/A            | ", end="")
    print(f"{float(R_val):18.6e} | " if R_val else "N/A                | ", end="")
    print(f"{float(norm_R):18.6e}" if norm_R else "N/A")

# ============================================================
print("\n" + SEP)
print("SECTION 6: (1-q)^2 * c_m(q) near q=1 — testing for double pole")
print(SEP)
sys.stdout.flush()

print(f"\n{'q':>10s} | {'1-q':>10s} | ", end="")
for m in sample_monoms[:3]:
    print(f"{'(1-q)^2*c_'+str(m):>18s} | ", end="")
print()
print("-" * (12 + 21 * 3))

for q_val in q_vals_near_1:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        continue
    eps = Fraction(1) - q_val
    print(f"{float(q_val):10.5f} | {float(eps):10.1e} | ", end="")
    for m in sample_monoms[:3]:
        idx = unk_monoms.index(m)
        val = sol[idx] * eps * eps
        print(f"{float(val):18.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Direct computation at q=1 (collapsed spectral vectors)")
print(SEP)
sys.stdout.flush()

# At q=1, spectral vectors are (t^{-k_0}, t^{-k_1}, t^{-k_2})
# Group compositions by their k-statistics
k_groups = {}
for nu in comps:
    ks = k_stats[nu]
    if ks not in k_groups:
        k_groups[ks] = []
    k_groups[ks].append(nu)

print(f"\nDistinct spectral vectors at q=1: {len(k_groups)}")
for ks, group in sorted(k_groups.items()):
    sv = tuple(t_val ** (-k) for k in ks)
    print(f"  k={ks} -> xi=(t^{-ks[0]}, t^{-ks[1]}, t^{-ks[2]}) = {tuple(float(x) for x in sv)}")
    print(f"    Compositions: {group}")

# Build the q=1 vanishing system
# Only use DISTINCT spectral vectors for vanishing conditions
distinct_svs = {}
for nu in van_comps:
    ks = k_stats[nu]
    sv = tuple(t_val ** (-k) for k in ks)
    if sv not in distinct_svs:
        distinct_svs[sv] = nu  # keep first representative

print(f"\nDistinct vanishing conditions at q=1: {len(distinct_svs)}")
print(f"Unknown monomials: {N}")
print(f"Underdetermined by: {N - len(distinct_svs)} dimensions")

# Build and solve the collapsed system
van_svs = list(distinct_svs.values())
A_collapsed = []
b_collapsed = []
for nu in van_svs:
    sv = tuple(t_val ** (-k) for k in k_stats[nu])
    row = []
    for m in unk_monoms:
        val = Fraction(1)
        for i in range(n):
            val *= sv[i] ** m[i]
        row.append(val)
    A_collapsed.append(row)
    val_lead = Fraction(1)
    for i in range(n):
        val_lead *= sv[i] ** leading[i]
    b_collapsed.append(-val_lead)

print(f"\nCollapsed system: {len(A_collapsed)} equations x {N} unknowns")

# Find the rank and null space dimension
aug = [A_collapsed[i][:] + [b_collapsed[i]] for i in range(len(A_collapsed))]
nrows = len(aug)
ncols = N

# Gaussian elimination on the collapsed system
aug2 = [row[:] for row in aug]
pivots = []
ri = 0
for col in range(ncols):
    piv = None
    for r in range(ri, nrows):
        if aug2[r][col] != Fraction(0):
            piv = r
            break
    if piv is None:
        continue
    pivots.append((ri, col))
    if piv != ri:
        aug2[ri], aug2[piv] = aug2[piv], aug2[ri]
    pv = aug2[ri][col]
    for j in range(ncols + 1):
        aug2[ri][j] /= pv
    for r in range(nrows):
        if r != ri and aug2[r][col] != Fraction(0):
            f = aug2[r][col]
            for j in range(ncols + 1):
                aug2[r][j] -= f * aug2[ri][j]
    ri += 1

rank = len(pivots)
nullity = N - rank
print(f"Rank: {rank}, Nullity (solution space dim): {nullity}")
print(f"  (need nullity > 0 for solutions to exist with the normalization)")

# Find a particular solution (set free variables to 0)
if rank > 0:
    pivot_cols = [c for _, c in pivots]
    free_cols = [c for c in range(ncols) if c not in pivot_cols]
    x_particular = [Fraction(0)] * ncols
    for r, c in pivots:
        x_particular[c] = aug2[r][ncols]
    # Check if this particular solution satisfies vanishing
    poly_q1 = {}
    for i, m in enumerate(unk_monoms):
        if x_particular[i] != Fraction(0):
            poly_q1[m] = x_particular[i]
    poly_q1[leading] = Fraction(1)

    # Check symmetry of the particular solution
    T0_q1 = hecke_operator(poly_q1, 0, t_val)
    T1_q1 = hecke_operator(poly_q1, 1, t_val)
    D0_q1 = poly_sub(T0_q1, poly_scale(poly_q1, t_val))
    D1_q1 = poly_sub(T1_q1, poly_scale(poly_q1, t_val))

    print(f"\nParticular solution (free vars = 0):")
    print(f"  Number of nonzero coefficients: {len(poly_q1)}")
    print(f"  (T_0 - t)E*|_q=1 has {len(D0_q1)} nonzero terms")
    print(f"  (T_1 - t)E*|_q=1 has {len(D1_q1)} nonzero terms")

    if len(D0_q1) == 0 and len(D1_q1) == 0:
        print("  => PARTICULAR SOLUTION IS SYMMETRIC!")
    else:
        # Show a few nonzero terms
        print("  Sample D0 terms:")
        for m in sorted(D0_q1.keys())[:5]:
            print(f"    D0_{m} = {D0_q1[m]} = {float(D0_q1[m]):.6e}")
        print("  Sample D1 terms:")
        for m in sorted(D1_q1.keys())[:5]:
            print(f"    D1_{m} = {D1_q1[m]} = {float(D1_q1[m]):.6e}")

        # Check: is there a symmetric solution in the solution space?
        # We need to find free variable values such that (T_i - t)(E*) = 0
        print(f"\n  Free variables: {len(free_cols)} (indices: {free_cols[:10]}...)")

print(f"\nTotal elapsed: {time.time() - t0:.1f}s")
