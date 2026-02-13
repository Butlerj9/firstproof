"""
P03 EXP-32e: n=4 convergence test for (T_i - t)E*/(1-q).

Tests whether the q->1 symmetry mechanism found at n=3 extends to n=4.
Uses float arithmetic for speed (n=4 system is 209x209).

Key questions:
1. Does E*_{lambda^-}(x; q, t) converge to a finite nonzero limit as q->1?
2. Does (T_i - t)E* -> 0 as q->1?
3. Does (T_i - t)E* / (1-q) converge to a finite limit?

If all yes -> strong evidence for the conjecture at n=4 (and general n).
"""
import sys, io, time
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SEP = "=" * 70
t0 = time.time()

n = 4
leading = (0, 1, 2, 3)  # weight = 6, antidominant
weight = sum(leading)

# Generate compositions of total weight <= weight
comps = []
for a in range(weight + 1):
    for b in range(weight + 1 - a):
        for c in range(weight + 1 - a - b):
            for d in range(weight + 1 - a - b - c):
                comps.append((a, b, c, d))

van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in comps if m != leading]
N = len(unk_monoms)
print(f"n={n}, weight={weight}, leading={leading}")
print(f"Number of compositions: {len(comps)}")
print(f"Number of unknowns: {N}")
print(f"Number of vanishing conditions: {len(van_comps)}")


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


def build_system_float(q_val, t_val):
    A = np.zeros((len(van_comps), N))
    b = np.zeros(len(van_comps))
    for ri, nu in enumerate(van_comps):
        eta = spectral_vec(nu, q_val, t_val)
        for ci, m in enumerate(unk_monoms):
            val = 1.0
            for i in range(n):
                val *= eta[i] ** m[i]
            A[ri, ci] = val
        val_lead = 1.0
        for i in range(n):
            val_lead *= eta[i] ** leading[i]
        b[ri] = -val_lead
    return A, b


# Hecke operator on float dict-based polynomials
def swap_vars(poly, i, j):
    result = {}
    for m, c in poly.items():
        new_m = list(m)
        new_m[i], new_m[j] = new_m[j], new_m[i]
        new_m = tuple(new_m)
        result[new_m] = result.get(new_m, 0.0) + c
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def poly_sub(p1, p2):
    result = dict(p1)
    for m, c in p2.items():
        result[m] = result.get(m, 0.0) - c
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def poly_add(p1, p2):
    result = dict(p1)
    for m, c in p2.items():
        result[m] = result.get(m, 0.0) + c
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def poly_scale(p, s):
    if abs(s) < 1e-15:
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
        groups[other_key][(ai, aj)] = groups[other_key].get((ai, aj), 0.0) + c
    result = {}
    for other_key, terms in groups.items():
        quotient = {}
        for (ai, aj), c in terms.items():
            if abs(c) < 1e-15:
                continue
            if ai > aj:
                for k in range(ai - aj):
                    qi, qj = aj + k, ai - 1 - k
                    quotient[(qi, qj)] = quotient.get((qi, qj), 0.0) + c
        for (qi, qj), c in quotient.items():
            if abs(c) < 1e-15:
                continue
            new_m = [0] * n
            for idx, k in enumerate(other_vars):
                new_m[k] = other_key[idx]
            new_m[i] = qi
            new_m[j] = qj
            new_m = tuple(new_m)
            result[new_m] = result.get(new_m, 0.0) + c
    return {k: v for k, v in result.items() if abs(v) > 1e-15}


def hecke_operator(poly, i, t_val):
    j = i + 1
    sf = swap_vars(poly, i, j)
    f_minus_sf = poly_sub(poly, sf)
    quotient = poly_div_by_diff(f_minus_sf, i, j)
    term1 = poly_scale(sf, t_val)
    x_i_times_q = poly_mul_var(quotient, i, 1)
    term2 = poly_scale(x_i_times_q, t_val - 1.0)
    return poly_add(term1, term2)


def eval_poly(poly, x):
    val = 0.0
    for m, c in poly.items():
        term = c
        for i in range(len(m)):
            term *= x[i] ** m[i]
        val += term
    return val


# ============================================================
print(SEP)
print("SECTION 1: q->1 convergence at n=4")
print(SEP)
sys.stdout.flush()

t_val = 0.7
q_vals_near_1 = [0.5, 0.75, 0.875, 0.9, 0.95, 0.98, 0.99, 0.995]
x_test = [2.0, 3.0, 5.0, 7.0]  # test point

print(f"\nt = {t_val}")
print(f"Test point x = {x_test}")

# Track a few monomial coefficients
sample_monoms = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]

print(f"\n{'q':>8s} | {'1-q':>10s} | {'E*(x)':>14s} | ", end="")
for i in range(n - 1):
    print(f"{'D'+str(i)+'(x)':>14s} | {'R'+str(i)+'(x)':>14s} | ", end="")
print()
print("-" * (35 + 32 * (n - 1)))

for q_val in q_vals_near_1:
    A, b = build_system_float(q_val, t_val)
    try:
        sol = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        print(f"  q={q_val}: singular system")
        continue

    # Build polynomial
    poly = {}
    for i, m in enumerate(unk_monoms):
        if abs(sol[i]) > 1e-15:
            poly[m] = sol[i]
    poly[leading] = 1.0

    E_val = eval_poly(poly, x_test)
    eps = 1.0 - q_val

    print(f"{q_val:8.4f} | {eps:10.1e} | {E_val:14.6e} | ", end="")

    for op_i in range(n - 1):
        Ti_poly = hecke_operator(poly, op_i, t_val)
        Di = poly_sub(Ti_poly, poly_scale(poly, t_val))
        Di_val = eval_poly(Di, x_test)
        Ri_val = Di_val / eps if eps != 0 else 0.0
        print(f"{Di_val:14.6e} | {Ri_val:14.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 2: D_i/E* ratio (should -> 0 for symmetry)")
print(SEP)
sys.stdout.flush()

print(f"\n{'q':>8s} | {'1-q':>10s} | ", end="")
for i in range(n - 1):
    print(f"{'D'+str(i)+'/E*':>14s} | ", end="")
print()
print("-" * (22 + 17 * (n - 1)))

for q_val in q_vals_near_1:
    A, b = build_system_float(q_val, t_val)
    try:
        sol = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        continue

    poly = {}
    for i, m in enumerate(unk_monoms):
        if abs(sol[i]) > 1e-15:
            poly[m] = sol[i]
    poly[leading] = 1.0

    E_val = eval_poly(poly, x_test)
    eps = 1.0 - q_val

    print(f"{q_val:8.4f} | {eps:10.1e} | ", end="")

    for op_i in range(n - 1):
        Ti_poly = hecke_operator(poly, op_i, t_val)
        Di = poly_sub(Ti_poly, poly_scale(poly, t_val))
        Di_val = eval_poly(Di, x_test)
        ratio = Di_val / E_val if abs(E_val) > 1e-10 else float('nan')
        print(f"{ratio:14.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Monomial-by-monomial convergence (sample)")
print(SEP)
sys.stdout.flush()

# Track specific monomials in D0 and D1
D_monoms = [(0, 1, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]

print(f"\n--- D0 monomial coefficients ---")
print(f"{'q':>8s} | {'1-q':>10s} | ", end="")
for m in D_monoms:
    print(f"{'D0_'+str(m):>18s} | ", end="")
print()
print("-" * (22 + 21 * len(D_monoms)))

for q_val in q_vals_near_1:
    A, b = build_system_float(q_val, t_val)
    try:
        sol = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        continue

    poly = {}
    for i, m in enumerate(unk_monoms):
        if abs(sol[i]) > 1e-15:
            poly[m] = sol[i]
    poly[leading] = 1.0

    T0_poly = hecke_operator(poly, 0, t_val)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    eps = 1.0 - q_val

    print(f"{q_val:8.4f} | {eps:10.1e} | ", end="")
    for m in D_monoms:
        val = D0.get(m, 0.0)
        print(f"{val:18.6e} | ", end="")
    print()

print(f"\n--- R0 = D0/(1-q) monomial coefficients ---")
print(f"{'q':>8s} | {'1-q':>10s} | ", end="")
for m in D_monoms:
    print(f"{'R0_'+str(m):>18s} | ", end="")
print()
print("-" * (22 + 21 * len(D_monoms)))

for q_val in q_vals_near_1:
    A, b = build_system_float(q_val, t_val)
    try:
        sol = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        continue

    poly = {}
    for i, m in enumerate(unk_monoms):
        if abs(sol[i]) > 1e-15:
            poly[m] = sol[i]
    poly[leading] = 1.0

    T0_poly = hecke_operator(poly, 0, t_val)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    eps = 1.0 - q_val

    print(f"{q_val:8.4f} | {eps:10.1e} | ", end="")
    for m in D_monoms:
        val = D0.get(m, 0.0)
        r_val = val / eps if abs(eps) > 1e-15 else 0.0
        print(f"{r_val:18.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Spectral collision analysis at q=1 (n=4)")
print(SEP)
sys.stdout.flush()

k_groups = {}
for nu in comps:
    ks = k_stats[nu]
    if ks not in k_groups:
        k_groups[ks] = []
    k_groups[ks].append(nu)

print(f"\nTotal compositions: {len(comps)}")
print(f"Distinct spectral vectors at q=1: {len(k_groups)}")
print(f"Underdetermined by: {N - (len(k_groups) - 1)} dimensions")

for ks in sorted(k_groups.keys()):
    group = k_groups[ks]
    print(f"  k={ks}: {len(group)} compositions")

# ============================================================
print("\n" + SEP)
print("SECTION 5: Second test point and second t value")
print(SEP)
sys.stdout.flush()

x_test2 = [1.5, 2.5, 4.0, 6.0]
t_val2 = 0.4

print(f"\nt = {t_val2}, x = {x_test2}")
print(f"\n{'q':>8s} | {'1-q':>10s} | {'E*(x)':>14s} | ", end="")
for i in range(n - 1):
    print(f"{'D'+str(i)+'/E*':>14s} | ", end="")
print()
print("-" * (35 + 17 * (n - 1)))

for q_val in q_vals_near_1:
    A, b = build_system_float(q_val, t_val2)
    try:
        sol = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        continue

    poly = {}
    for i, m in enumerate(unk_monoms):
        if abs(sol[i]) > 1e-15:
            poly[m] = sol[i]
    poly[leading] = 1.0

    E_val = eval_poly(poly, x_test2)
    eps = 1.0 - q_val

    print(f"{q_val:8.4f} | {eps:10.1e} | {E_val:14.6e} | ", end="")

    for op_i in range(n - 1):
        Ti_poly = hecke_operator(poly, op_i, t_val2)
        Di = poly_sub(Ti_poly, poly_scale(poly, t_val2))
        Di_val = eval_poly(Di, x_test2)
        ratio = Di_val / E_val if abs(E_val) > 1e-10 else float('nan')
        print(f"{ratio:14.6e} | ", end="")
    print()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Summary")
print(SEP)
print(f"""
n={n}, weight={weight}
Leading composition: {leading}
System size: {N}x{N}
Distinct spectral vectors at q=1: {len(k_groups)} (out of {len(comps)})
Underdetermined at q=1 by: {N - (len(k_groups) - 1)} dimensions

Key findings:
- If E*(x) converges to finite nonzero limit: E* limit exists
- If D_i/E* -> 0: symmetry of limit confirmed
- If D_i/(1-q) converges: (T_i-t)E* vanishes at rate O(1-q)
""")
print(f"Total elapsed: {time.time() - t0:.1f}s")
