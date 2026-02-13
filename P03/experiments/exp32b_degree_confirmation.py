"""
P03 EXP-32b: Confirm R_i degree pattern and check at second t value.

Findings from EXP-32: R_i(q) is a degree-9 polynomial in q (n=3, t=7/10).
Question: Is degree 9 independent of t? Is it = weight*(n-1) - 1 = 5*2-1 = 9?

Also: check the FULL degree of E*_{lambda^-} in q (to understand the factorization).
"""
import sys, io, time
from fractions import Fraction
from itertools import permutations

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


def rational_interp_degree(q_vals, r_vals):
    n_pts = len(q_vals)
    for total_deg in range(n_pts):
        for dd in range(total_deg + 1):
            dp = total_deg - dd
            n_unk = dp + 1 + dd
            if n_unk > n_pts:
                continue
            rows = []
            rhs = []
            for i in range(n_unk):
                row = []
                for j in range(dp + 1):
                    row.append(q_vals[i] ** j)
                for j in range(1, dd + 1):
                    row.append(-r_vals[i] * q_vals[i] ** j)
                rows.append(row)
                rhs.append(r_vals[i])
            try:
                sol, rank = gauss_solve(rows, rhs)
                if sol is None:
                    continue
                max_res = Fraction(0)
                for i in range(n_pts):
                    p_val = sum(sol[j] * q_vals[i] ** j for j in range(dp + 1))
                    d_val = Fraction(1) + sum(sol[dp + 1 + j] * q_vals[i] ** (j + 1) for j in range(dd))
                    if d_val == Fraction(0):
                        max_res = Fraction(10 ** 10)
                        break
                    pred = p_val / d_val
                    res = abs(pred - r_vals[i])
                    if res > max_res:
                        max_res = res
                if max_res == Fraction(0):
                    return dp, dd, Fraction(0)
            except Exception:
                continue
    return -1, -1, Fraction(-1)


# ============================================================
print(SEP)
print("SECTION 1: Degree of E* coefficients in q (direct)")
print(SEP)
sys.stdout.flush()

# Test at multiple t values
for t_val in [Fraction(7, 10), Fraction(1, 3), Fraction(5, 2), Fraction(3, 7)]:
    print(f"\nt = {t_val}:")
    q_values = [Fraction(k, k + 1) for k in range(1, 16)]
    all_coeffs = {}  # m -> list of (q, c)
    for q_val in q_values:
        A, b = build_system(q_val, t_val)
        sol, rank = gauss_solve(A, b)
        if sol is None:
            continue
        for i, m in enumerate(unk_monoms):
            if m not in all_coeffs:
                all_coeffs[m] = []
            all_coeffs[m].append((q_val, sol[i]))

    # Determine degree of c_m(q) for a few monomials
    sample = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
              (2, 0, 0), (0, 0, 2), (1, 1, 1), (0, 2, 1)]
    max_deg = 0
    for m in sample:
        if m in all_coeffs and len(all_coeffs[m]) >= 3:
            qs = [x[0] for x in all_coeffs[m][:12]]
            cs = [x[1] for x in all_coeffs[m][:12]]
            dp, dd, res = rational_interp_degree(qs, cs)
            total = dp + dd
            if total > max_deg:
                max_deg = total
            print(f"  c_{m}(q): deg_num={dp}, deg_den={dd}, total={total}")

    print(f"  Max total degree of E* coefficients in q: {max_deg}")

# ============================================================
print("\n" + SEP)
print("SECTION 2: Confirm R_i degree at different t values")
print(SEP)
sys.stdout.flush()


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


for t_val in [Fraction(1, 3), Fraction(5, 2), Fraction(3, 7)]:
    print(f"\nt = {t_val}:")
    q_values = [Fraction(k, k + 1) for k in range(1, 14)]
    R0_by_monom = {}  # m -> [(q, R0_coeff)]
    R1_by_monom = {}

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
        R0 = poly_scale(D0, Fraction(1) / omq)
        R1 = poly_scale(D1, Fraction(1) / omq)

        for m, c in R0.items():
            if m not in R0_by_monom:
                R0_by_monom[m] = []
            R0_by_monom[m].append((q_val, c))
        for m, c in R1.items():
            if m not in R1_by_monom:
                R1_by_monom[m] = []
            R1_by_monom[m].append((q_val, c))

    # Check degrees
    sample = [(1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)]
    print("  R0 degrees:")
    for m in sample:
        if m in R0_by_monom and len(R0_by_monom[m]) >= 3:
            qs = [x[0] for x in R0_by_monom[m][:12]]
            cs = [x[1] for x in R0_by_monom[m][:12]]
            dp, dd, res = rational_interp_degree(qs, cs)
            print(f"    m={m}: deg_num={dp}, deg_den={dd}, total={dp + dd}, res={float(res):.2e}")

    print("  R1 degrees:")
    for m in sample:
        if m in R1_by_monom and len(R1_by_monom[m]) >= 3:
            qs = [x[0] for x in R1_by_monom[m][:12]]
            cs = [x[1] for x in R1_by_monom[m][:12]]
            dp, dd, res = rational_interp_degree(qs, cs)
            print(f"    m={m}: deg_num={dp}, deg_den={dd}, total={dp + dd}, res={float(res):.2e}")

# ============================================================
print("\n" + SEP)
print("SECTION 3: Degree pattern analysis")
print(SEP)
print("""
For n=3, weight=5:
  E* coefficients: polynomial in q, degree to be determined
  R_i = (T_i - t)E* / (1-q): polynomial in q, degree 9

Pattern hypothesis: deg(R_i) = weight * (n-1) - 1 = 5*2-1 = 9 ✓

For n=4, weight=9: predicted deg(R_i) = 9*3-1 = 26
For n=5, weight=14: predicted deg(R_i) = 14*4-1 = 55

Alternatively: deg(E* coeff in q) = weight*(n-1) = 10 for n=3
and deg(R_i) = deg(E*) - 1 = 9.

If E* coefficients have total q-degree D, then:
  (T_i - t)E* has q-degree D (Hecke op preserves q-degree)
  Divisibility by (1-q) reduces degree by 1
  => deg(R_i) = D - 1
""")
print(f"\nTotal elapsed: {time.time() - t0:.1f}s")
