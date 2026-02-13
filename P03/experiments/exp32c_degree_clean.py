"""
P03 EXP-32c: Clean degree determination with overconstrained verification.

Resolves discrepancy between exp32 (degree 9 for R_i) and exp32b (degree 11).
The exp32b result used only 12 points for Padé fitting, giving exact-fit artifacts.

This script uses 20+ q values and validates degrees with overconstrained checks.
Also explicitly tests D_m(1) = 0 for each monomial to confirm (1-q) divisibility.
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

print(f"n={n}, weight=5, leading={leading}")
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


def poly_fit_degree(q_vals, r_vals, max_deg=20):
    """Fit polynomial of increasing degree with overconstrained check.
    Returns (degree, max_residual) where max_residual is over ALL points."""
    n_pts = len(q_vals)
    for deg in range(max_deg + 1):
        n_unk = deg + 1
        if n_unk > n_pts:
            return -1, Fraction(-1)
        # Use first n_unk points to fit
        rows = []
        rhs = []
        for i in range(n_unk):
            row = [q_vals[i] ** j for j in range(n_unk)]
            rows.append(row)
            rhs.append(r_vals[i])
        sol, rank = gauss_solve(rows, rhs)
        if sol is None:
            continue
        # Check ALL points (including overconstrained ones)
        max_res = Fraction(0)
        for i in range(n_pts):
            pred = sum(sol[j] * q_vals[i] ** j for j in range(n_unk))
            res = abs(pred - r_vals[i])
            if res > max_res:
                max_res = res
        if max_res == Fraction(0):
            return deg, Fraction(0)
    return -1, Fraction(-1)


# Hecke operator infrastructure
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
print("SECTION 1: E* coefficient degrees (20 q values, overconstrained)")
print(SEP)
sys.stdout.flush()

t_val = Fraction(7, 10)
q_values = [Fraction(k, 100) for k in range(2, 96, 5)]  # 0.02, 0.07, ..., 0.92 (19 values)

all_E_coeffs = {}  # m -> list of (q, c)
for q_val in q_values:
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        print(f"  WARNING: System singular at q={q_val}")
        continue
    for i, m in enumerate(unk_monoms):
        if m not in all_E_coeffs:
            all_E_coeffs[m] = []
        all_E_coeffs[m].append((q_val, sol[i]))

# Determine degree with overconstrained check
sample_monoms = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
                 (2, 0, 0), (0, 0, 2), (1, 1, 1), (0, 2, 1),
                 (0, 0, 1), (2, 1, 0), (3, 0, 0), (0, 1, 2)]
max_E_deg = 0
print(f"\nt = {t_val}, {len(q_values)} q values:")
for m in sample_monoms:
    if m in all_E_coeffs and len(all_E_coeffs[m]) >= 3:
        qs = [x[0] for x in all_E_coeffs[m]]
        cs = [x[1] for x in all_E_coeffs[m]]
        deg, res = poly_fit_degree(qs, cs)
        over = len(qs) - (deg + 1)
        if deg > max_E_deg:
            max_E_deg = deg
        print(f"  c_{m}(q): degree {deg} (overconstrained by {over} points)")

print(f"\n  => Max E* coefficient degree in q: {max_E_deg}")

# ============================================================
print("\n" + SEP)
print("SECTION 2: R_i degrees (20 q values, overconstrained)")
print(SEP)
sys.stdout.flush()

R0_by_monom = {}
R1_by_monom = {}
D0_by_monom = {}  # Before (1-q) division
D1_by_monom = {}

for q_val in q_values:
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
    T1_poly = hecke_operator(poly, 1, t_val)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    D1 = poly_sub(T1_poly, poly_scale(poly, t_val))
    omq = Fraction(1) - q_val

    for m, c in D0.items():
        if m not in D0_by_monom:
            D0_by_monom[m] = []
        D0_by_monom[m].append((q_val, c))
        if m not in R0_by_monom:
            R0_by_monom[m] = []
        R0_by_monom[m].append((q_val, c / omq))

    for m, c in D1.items():
        if m not in D1_by_monom:
            D1_by_monom[m] = []
        D1_by_monom[m].append((q_val, c))
        if m not in R1_by_monom:
            R1_by_monom[m] = []
        R1_by_monom[m].append((q_val, c / omq))

# Get all monomials that appear in D0 or D1
all_D0_monoms = sorted(D0_by_monom.keys())
all_D1_monoms = sorted(D1_by_monom.keys())

print(f"\nD0 = (T_0 - t)E* has {len(all_D0_monoms)} nonzero monomial coefficients")
print(f"D1 = (T_1 - t)E* has {len(all_D1_monoms)} nonzero monomial coefficients")

# Check D_i degrees
print("\n--- D0 monomial coefficient degrees in q ---")
max_D0_deg = 0
for m in all_D0_monoms[:15]:  # Show first 15
    qs = [x[0] for x in D0_by_monom[m]]
    cs = [x[1] for x in D0_by_monom[m]]
    deg, res = poly_fit_degree(qs, cs)
    over = len(qs) - (deg + 1)
    if deg > max_D0_deg:
        max_D0_deg = deg
    print(f"  D0_{m}(q): degree {deg} (overconstrained by {over})")

print(f"\n  => Max D0 degree in q: {max_D0_deg}")

# Check R_i degrees
print("\n--- R0 = D0/(1-q) monomial coefficient degrees in q ---")
max_R0_deg = 0
for m in all_D0_monoms[:15]:
    if m in R0_by_monom and len(R0_by_monom[m]) >= 3:
        qs = [x[0] for x in R0_by_monom[m]]
        cs = [x[1] for x in R0_by_monom[m]]
        deg, res = poly_fit_degree(qs, cs)
        over = len(qs) - (deg + 1)
        if deg > max_R0_deg:
            max_R0_deg = deg
        print(f"  R0_{m}(q): degree {deg} (overconstrained by {over})")

print(f"\n  => Max R0 degree in q: {max_R0_deg}")

print("\n--- R1 = D1/(1-q) monomial coefficient degrees in q ---")
max_R1_deg = 0
for m in all_D1_monoms[:15]:
    if m in R1_by_monom and len(R1_by_monom[m]) >= 3:
        qs = [x[0] for x in R1_by_monom[m]]
        cs = [x[1] for x in R1_by_monom[m]]
        deg, res = poly_fit_degree(qs, cs)
        over = len(qs) - (deg + 1)
        if deg > max_R1_deg:
            max_R1_deg = deg
        print(f"  R1_{m}(q): degree {deg} (overconstrained by {over})")

print(f"\n  => Max R1 degree in q: {max_R1_deg}")

# ============================================================
print("\n" + SEP)
print("SECTION 3: Explicit divisibility check — D_m(q=1) via polynomial evaluation")
print(SEP)
sys.stdout.flush()

# For each monomial m of D0, fit the polynomial D0_m(q) and evaluate at q=1
print("\n--- D0_m(1) values (should all be 0 for divisibility) ---")
div0_pass = 0
div0_total = 0
for m in all_D0_monoms:
    qs = [x[0] for x in D0_by_monom[m]]
    cs = [x[1] for x in D0_by_monom[m]]
    deg, res = poly_fit_degree(qs, cs)
    if deg < 0:
        print(f"  D0_{m}: could not determine degree")
        continue
    # Fit polynomial coefficients
    n_unk = deg + 1
    rows = [[qs[i] ** j for j in range(n_unk)] for i in range(n_unk)]
    rhs = [cs[i] for i in range(n_unk)]
    sol, rank = gauss_solve(rows, rhs)
    if sol is None:
        print(f"  D0_{m}: fit failed")
        continue
    # Evaluate at q=1
    val_at_1 = sum(sol[j] for j in range(n_unk))
    div0_total += 1
    if val_at_1 == Fraction(0):
        div0_pass += 1
    else:
        print(f"  D0_{m}(1) = {val_at_1}  *** NONZERO ***")

print(f"\n  D0 divisibility: {div0_pass}/{div0_total} monomials have D0_m(1) = 0")

print("\n--- D1_m(1) values (should all be 0 for divisibility) ---")
div1_pass = 0
div1_total = 0
for m in all_D1_monoms:
    qs = [x[0] for x in D1_by_monom[m]]
    cs = [x[1] for x in D1_by_monom[m]]
    deg, res = poly_fit_degree(qs, cs)
    if deg < 0:
        continue
    n_unk = deg + 1
    rows = [[qs[i] ** j for j in range(n_unk)] for i in range(n_unk)]
    rhs = [cs[i] for i in range(n_unk)]
    sol, rank = gauss_solve(rows, rhs)
    if sol is None:
        continue
    val_at_1 = sum(sol[j] for j in range(n_unk))
    div1_total += 1
    if val_at_1 == Fraction(0):
        div1_pass += 1
    else:
        print(f"  D1_{m}(1) = {val_at_1}  *** NONZERO ***")

print(f"\n  D1 divisibility: {div1_pass}/{div1_total} monomials have D1_m(1) = 0")

# ============================================================
print("\n" + SEP)
print("SECTION 4: Confirm at second t value")
print(SEP)
sys.stdout.flush()

t_val2 = Fraction(3, 7)
D0_by_monom2 = {}
D1_by_monom2 = {}
R0_by_monom2 = {}
R1_by_monom2 = {}

for q_val in q_values:
    A, b = build_system(q_val, t_val2)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        continue
    poly = {}
    for i, m in enumerate(unk_monoms):
        if sol[i] != Fraction(0):
            poly[m] = sol[i]
    poly[leading] = Fraction(1)

    T0_poly = hecke_operator(poly, 0, t_val2)
    T1_poly = hecke_operator(poly, 1, t_val2)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val2))
    D1 = poly_sub(T1_poly, poly_scale(poly, t_val2))
    omq = Fraction(1) - q_val

    for m, c in D0.items():
        if m not in D0_by_monom2:
            D0_by_monom2[m] = []
        D0_by_monom2[m].append((q_val, c))
        if m not in R0_by_monom2:
            R0_by_monom2[m] = []
        R0_by_monom2[m].append((q_val, c / omq))

    for m, c in D1.items():
        if m not in D1_by_monom2:
            D1_by_monom2[m] = []
        D1_by_monom2[m].append((q_val, c))
        if m not in R1_by_monom2:
            R1_by_monom2[m] = []
        R1_by_monom2[m].append((q_val, c / omq))

# Check divisibility
print(f"\nt = {t_val2}:")
div0_pass2 = 0
div0_total2 = 0
for m in sorted(D0_by_monom2.keys()):
    qs = [x[0] for x in D0_by_monom2[m]]
    cs = [x[1] for x in D0_by_monom2[m]]
    deg, res = poly_fit_degree(qs, cs)
    if deg < 0:
        continue
    n_unk = deg + 1
    rows = [[qs[i] ** j for j in range(n_unk)] for i in range(n_unk)]
    rhs = [cs[i] for i in range(n_unk)]
    sol, rank = gauss_solve(rows, rhs)
    if sol is None:
        continue
    val_at_1 = sum(sol[j] for j in range(n_unk))
    div0_total2 += 1
    if val_at_1 == Fraction(0):
        div0_pass2 += 1
    else:
        print(f"  D0_{m}(1) = {val_at_1}  *** NONZERO ***")

div1_pass2 = 0
div1_total2 = 0
for m in sorted(D1_by_monom2.keys()):
    qs = [x[0] for x in D1_by_monom2[m]]
    cs = [x[1] for x in D1_by_monom2[m]]
    deg, res = poly_fit_degree(qs, cs)
    if deg < 0:
        continue
    n_unk = deg + 1
    rows = [[qs[i] ** j for j in range(n_unk)] for i in range(n_unk)]
    rhs = [cs[i] for i in range(n_unk)]
    sol, rank = gauss_solve(rows, rhs)
    if sol is None:
        continue
    val_at_1 = sum(sol[j] for j in range(n_unk))
    div1_total2 += 1
    if val_at_1 == Fraction(0):
        div1_pass2 += 1
    else:
        print(f"  D1_{m}(1) = {val_at_1}  *** NONZERO ***")

print(f"\n  D0 divisibility: {div0_pass2}/{div0_total2}")
print(f"  D1 divisibility: {div1_pass2}/{div1_total2}")

# Check R_i degrees at t2
max_R0_deg2 = 0
max_R1_deg2 = 0
for m in sorted(R0_by_monom2.keys()):
    qs = [x[0] for x in R0_by_monom2[m]]
    cs = [x[1] for x in R0_by_monom2[m]]
    deg, res = poly_fit_degree(qs, cs)
    if deg > max_R0_deg2:
        max_R0_deg2 = deg
for m in sorted(R1_by_monom2.keys()):
    qs = [x[0] for x in R1_by_monom2[m]]
    cs = [x[1] for x in R1_by_monom2[m]]
    deg, res = poly_fit_degree(qs, cs)
    if deg > max_R1_deg2:
        max_R1_deg2 = deg
print(f"  Max R0 degree: {max_R0_deg2}")
print(f"  Max R1 degree: {max_R1_deg2}")

# ============================================================
print("\n" + SEP)
print("SECTION 5: Summary")
print(SEP)
print(f"""
n=3, weight=5, leading=(0,2,3)

Degree results (t={t_val}, {len(q_values)} q-values):
  E* coefficient max degree in q: {max_E_deg}
  D0 = (T_0 - t)E* max degree in q: {max_D0_deg}
  R0 = D0/(1-q) max degree in q: {max_R0_deg}
  R1 = D1/(1-q) max degree in q: {max_R1_deg}

Divisibility (t={t_val}):
  D0_m(1) = 0 for all m: {div0_pass}/{div0_total}
  D1_m(1) = 0 for all m: {div1_pass}/{div1_total}

Divisibility (t={t_val2}):
  D0_m(1) = 0 for all m: {div0_pass2}/{div0_total2}
  D1_m(1) = 0 for all m: {div1_pass2}/{div1_total2}

Degree results (t={t_val2}):
  R0 max degree: {max_R0_deg2}
  R1 max degree: {max_R1_deg2}

Structural implication:
  (T_i - t)E*_{{lambda^-}} = (1-q) * R_i(q)  [exact polynomial identity]
  At q=1: T_i(E*|_{{q=1}}) = t * E*|_{{q=1}}  => E*|_{{q=1}} is symmetric
""")

print(f"Total elapsed: {time.time() - t0:.1f}s")
