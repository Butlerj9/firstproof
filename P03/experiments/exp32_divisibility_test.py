"""
P03 EXP-32: (1-q)-divisibility kill-test for Hecke eigenvalue.

Target: (T_i - t) E*_{lambda^-}(x; q, t) is divisible by (1-q).

Method: Compute E*_{lambda^-} at exact rational q values (Fraction arithmetic),
apply Hecke operator T_i, compute (T_i - t)E* / (1-q), and analyze the quotient.

For n=3 where symmetry IS proved, divisibility is guaranteed. The goal is to
see the STRUCTURE of R_i(q) = (T_i-t)E*/(1-q) and assess generalizability.
"""
import sys, io, time
from fractions import Fraction
from itertools import permutations

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SEP = "=" * 70
t0 = time.time()

n = 3
leading = (0, 2, 3)  # anti-dominant

# All compositions of weight <= 5 into 3 parts
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
    """Compute spectral vector eta_i = q^{nu_i} * t^{-k_i}."""
    ks = k_stats[nu]
    return tuple(q_val ** nu[i] * t_val ** (-ks[i]) for i in range(n))


def build_system(q_val, t_val):
    """Build vanishing system A*c = b at specific (q, t)."""
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
        # RHS: -eval of leading monomial at eta
        val_lead = Fraction(1)
        for i in range(n):
            val_lead *= eta[i] ** leading[i]
        b.append(-val_lead)
    return A, b


def gauss_solve(A, b_vec):
    """Gaussian elimination with full pivoting, returns solution vector."""
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
        return None, rank  # underdetermined

    x = [Fraction(0)] * ncols
    for r, c in pivots:
        x[c] = aug[r][ncols]
    return x, rank


def compute_estar(q_val, t_val):
    """Compute E*_{lambda^-} at (q, t) as a polynomial dict {monom: coeff}."""
    A, b = build_system(q_val, t_val)
    sol, rank = gauss_solve(A, b)
    if sol is None:
        return None, rank

    poly = {}
    for i, m in enumerate(unk_monoms):
        if sol[i] != Fraction(0):
            poly[m] = sol[i]
    poly[leading] = Fraction(1)
    return poly, rank


def swap_vars(poly, i, j):
    """Swap variables x_i and x_j in polynomial."""
    result = {}
    for m, c in poly.items():
        new_m = list(m)
        new_m[i], new_m[j] = new_m[j], new_m[i]
        new_m = tuple(new_m)
        result[new_m] = result.get(new_m, Fraction(0)) + c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def poly_sub(p1, p2):
    """p1 - p2."""
    result = dict(p1)
    for m, c in p2.items():
        result[m] = result.get(m, Fraction(0)) - c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def poly_add(p1, p2):
    """p1 + p2."""
    result = dict(p1)
    for m, c in p2.items():
        result[m] = result.get(m, Fraction(0)) + c
    return {k: v for k, v in result.items() if v != Fraction(0)}


def poly_scale(p, s):
    """s * p."""
    if s == Fraction(0):
        return {}
    return {m: c * s for m, c in p.items()}


def poly_mul_var(p, var_idx, power=1):
    """Multiply polynomial by x_{var_idx}^power."""
    return {tuple(m[j] + (power if j == var_idx else 0) for j in range(n)): c
            for m, c in p.items()}


def poly_div_by_diff(f_minus_sf, i, j):
    """
    Divide (f - s_i f) by (x_i - x_j).
    Since f - s_i(f) is always divisible by (x_i - x_j), this is exact.

    We use the identity: for a polynomial g(x_i, x_j) antisymmetric under x_i <-> x_j,
    g / (x_i - x_j) can be computed via synthetic division.
    """
    # Collect by x_i, x_j powers. For each monomial c * x_i^a * x_j^b * (other vars),
    # group by (other vars) and work in the 2-variable ring.
    other_vars = [k for k in range(n) if k != i and k != j]

    # Group terms by "other" exponents
    groups = {}
    for m, c in f_minus_sf.items():
        other_key = tuple(m[k] for k in other_vars)
        ai, aj = m[i], m[j]
        if other_key not in groups:
            groups[other_key] = {}
        groups[other_key][(ai, aj)] = groups[other_key].get((ai, aj), Fraction(0)) + c

    result = {}
    for other_key, terms in groups.items():
        # Divide bivariate polynomial by (x_i - x_j)
        # Use the fact that p(x_i, x_j) antisymmetric => p = (x_i - x_j) * q(x_i, x_j)
        # q can be computed by: q = sum_{a>b} c_{a,b} * sum_{k=0}^{a-b-1} x_i^{b+k} x_j^{a-1-k}
        # plus symmetric handling
        quotient = {}
        for (ai, aj), c in terms.items():
            if c == Fraction(0):
                continue
            if ai > aj:
                # x_i^ai * x_j^aj - x_i^aj * x_j^ai = (x_i - x_j) * sum_{k=0}^{ai-aj-1} x_i^{aj+k} * x_j^{ai-1-k}
                # So c * x_i^ai * x_j^aj contribution to f-sf has:
                # This term's contribution to quotient: c * sum_{k} x_i^{aj+k} x_j^{ai-1-k}
                for k in range(ai - aj):
                    qi, qj = aj + k, ai - 1 - k
                    quotient[(qi, qj)] = quotient.get((qi, qj), Fraction(0)) + c
            elif ai == aj:
                # This shouldn't appear in f - s(f) for antisymmetric part
                if c != Fraction(0):
                    print(f"  WARNING: diagonal term ({ai},{aj}) with coeff {c}")
            # ai < aj case: handled by antisymmetry (c_{aj,ai} = -c_{ai,aj})

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
    """
    Apply T_i to polynomial poly.
    T_i f = t * s_i(f) + (t-1) * x_i/(x_i - x_{i+1}) * (f - s_i(f))

    Since f - s_i(f) is divisible by (x_i - x_{i+1}), we have:
    T_i f = t * s_i(f) + (t-1) * x_i * [(f - s_i(f)) / (x_i - x_{i+1})]
    """
    j = i + 1  # T_i swaps x_i and x_{i+1}
    sf = swap_vars(poly, i, j)
    f_minus_sf = poly_sub(poly, sf)

    # Divide (f - s_i f) by (x_i - x_{i+1})
    quotient = poly_div_by_diff(f_minus_sf, i, j)

    # T_i f = t * s_i(f) + (t-1) * x_i * quotient
    term1 = poly_scale(sf, t_val)
    x_i_times_q = poly_mul_var(quotient, i, 1)
    term2 = poly_scale(x_i_times_q, t_val - Fraction(1))

    return poly_add(term1, term2)


# ============================================================
print(SEP)
print("SECTION 1: Divisibility test — (T_i - t)E* / (1-q) at exact q values")
print(SEP)
sys.stdout.flush()

t_val = Fraction(7, 10)
q_values = [Fraction(1, 2), Fraction(2, 3), Fraction(3, 4),
            Fraction(4, 5), Fraction(5, 6), Fraction(6, 7),
            Fraction(7, 8), Fraction(8, 9), Fraction(9, 10),
            Fraction(10, 11), Fraction(11, 12), Fraction(19, 20),
            Fraction(29, 30), Fraction(49, 50), Fraction(99, 100)]

print(f"t = {t_val}, n = {n}, lambda^- = {leading}")
print(f"Testing {len(q_values)} q values\n")

# Store R_i values for analysis
R0_data = {}  # q -> {monom: R0_coeff}
R1_data = {}  # q -> {monom: R1_coeff}

for qi, q_val in enumerate(q_values):
    t1 = time.time()
    poly, rank = compute_estar(q_val, t_val)
    if poly is None:
        print(f"  q={q_val}: DEGENERATE (rank={rank})")
        continue

    # Apply T_0 and T_1
    T0_poly = hecke_operator(poly, 0, t_val)
    T1_poly = hecke_operator(poly, 1, t_val)

    # Compute (T_i - t) E* = T_i(E*) - t * E*
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
    D1 = poly_sub(T1_poly, poly_scale(poly, t_val))

    # Divide by (1-q)
    one_minus_q = Fraction(1) - q_val
    R0 = poly_scale(D0, Fraction(1) / one_minus_q)
    R1 = poly_scale(D1, Fraction(1) / one_minus_q)

    R0_data[q_val] = R0
    R1_data[q_val] = R1

    # Report
    D0_max = max(abs(c) for c in D0.values()) if D0 else Fraction(0)
    D1_max = max(abs(c) for c in D1.values()) if D1 else Fraction(0)
    R0_max = max(abs(c) for c in R0.values()) if R0 else Fraction(0)
    R1_max = max(abs(c) for c in R1.values()) if R1 else Fraction(0)

    elapsed = time.time() - t1
    print(f"  q={str(q_val):>6s}: |D0|_max={float(D0_max):.4e}, |R0|_max={float(R0_max):.4e}, "
          f"|D1|_max={float(D1_max):.4e}, |R1|_max={float(R1_max):.4e} ({elapsed:.1f}s)")
    sys.stdout.flush()

print(f"\nElapsed: {time.time() - t0:.1f}s")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Convergence analysis — does R_i(q) converge as q -> 1?")
print(SEP)
sys.stdout.flush()

# Check a few specific monomial coefficients in R0 and R1
# Pick monomials that appear in E* (non-trivially)
sample_monoms = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                 (1, 1, 0), (1, 0, 1), (0, 1, 1), (2, 0, 0),
                 (0, 2, 0), (0, 0, 2), (1, 1, 1)]

print("\nR0 coefficients (sample monomials):")
for m in sample_monoms:
    vals = []
    for q_val in q_values[-5:]:  # last 5 q values (closest to 1)
        if q_val in R0_data:
            c = R0_data[q_val].get(m, Fraction(0))
            vals.append((q_val, float(c)))
    if vals:
        val_str = ", ".join(f"q={q:.4f}:{v:.6f}" for q, v in vals)
        print(f"  m={m}: {val_str}")

print("\nR1 coefficients (sample monomials):")
for m in sample_monoms:
    vals = []
    for q_val in q_values[-5:]:
        if q_val in R1_data:
            c = R1_data[q_val].get(m, Fraction(0))
            vals.append((q_val, float(c)))
    if vals:
        val_str = ", ".join(f"q={q:.4f}:{v:.6f}" for q, v in vals)
        print(f"  m={m}: {val_str}")

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Rational function degree analysis via Pade interpolation")
print(SEP)
sys.stdout.flush()

# For each monomial in R0 and R1, determine the rational function degree in q
# Use the method: if R(q) = p(q)/d(q) with deg p = dp, deg d = dd,
# then (dp+dd+1) interpolation points suffice.
# Try successive (dp, dd) pairs and check consistency.

def rational_interp_degree(q_vals, r_vals):
    """
    Given (q_i, R(q_i)) pairs, determine (deg_num, deg_den) of R(q) = p(q)/d(q).
    Try (p,d) for p+d = 0,1,2,...,max and check if system is consistent.
    Returns (p, d, residual) for best fit.
    """
    n_pts = len(q_vals)
    best = None
    for total_deg in range(n_pts):
        for dd in range(total_deg + 1):
            dp = total_deg - dd
            # Need dp + dd + 1 = total_deg + 1 data points
            if total_deg + 1 > n_pts:
                break
            # System: p(q_i) = R(q_i) * d(q_i)
            # p(q) = sum_{j=0}^{dp} a_j q^j, d(q) = 1 + sum_{j=1}^{dd} b_j q^j
            # => sum a_j q_i^j - R(q_i) * sum b_j q_i^j = R(q_i)
            n_unk = dp + 1 + dd
            if n_unk > n_pts:
                continue
            rows = []
            rhs = []
            for i in range(min(n_unk, n_pts)):
                row = []
                for j in range(dp + 1):
                    row.append(q_vals[i] ** j)
                for j in range(1, dd + 1):
                    row.append(-r_vals[i] * q_vals[i] ** j)
                rows.append(row)
                rhs.append(r_vals[i])

            # Solve
            try:
                sol, rank = gauss_solve(rows, rhs)
                if sol is None:
                    continue
                # Check residual on remaining points
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
                if best is None or max_res < best[2]:
                    best = (dp, dd, max_res)
            except Exception:
                continue
    return best if best else (-1, -1, Fraction(-1))


# Analyze a few monomials
print("\nRational function degree of R0(q) by monomial:")
for m in sample_monoms:
    q_vals_f = []
    r_vals_f = []
    for q_val in q_values:
        if q_val in R0_data:
            c = R0_data[q_val].get(m, Fraction(0))
            q_vals_f.append(q_val)
            r_vals_f.append(c)
    if len(q_vals_f) >= 3:
        dp, dd, res = rational_interp_degree(q_vals_f[:10], r_vals_f[:10])
        print(f"  m={m}: deg_num={dp}, deg_den={dd}, total={dp+dd}, residual={float(res):.2e}")
    else:
        print(f"  m={m}: insufficient data")

print("\nRational function degree of R1(q) by monomial:")
for m in sample_monoms:
    q_vals_f = []
    r_vals_f = []
    for q_val in q_values:
        if q_val in R1_data:
            c = R1_data[q_val].get(m, Fraction(0))
            q_vals_f.append(q_val)
            r_vals_f.append(c)
    if len(q_vals_f) >= 3:
        dp, dd, res = rational_interp_degree(q_vals_f[:10], r_vals_f[:10])
        print(f"  m={m}: deg_num={dp}, deg_den={dd}, total={dp+dd}, residual={float(res):.2e}")
    else:
        print(f"  m={m}: insufficient data")

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: R_i(q=1) limit via extrapolation")
print(SEP)
sys.stdout.flush()

# Use the last 5 q values (closest to 1) to extrapolate R_i(1)
# Simple polynomial extrapolation in (1-q)
print("\nR0(q→1) extrapolation (polynomial in 1-q):")
for m in sample_monoms[:6]:
    q_list = q_values[-5:]
    eps_list = [Fraction(1) - q for q in q_list]
    r_list = [R0_data.get(q, {}).get(m, Fraction(0)) for q in q_list]
    if all(r == Fraction(0) for r in r_list):
        print(f"  m={m}: identically 0")
        continue
    # Linear extrapolation: R(q) ≈ a + b*(1-q) => R(1) ≈ a
    # Use 2-point fit from last 2 values
    if len(r_list) >= 2:
        e1, e2 = eps_list[-2], eps_list[-1]
        r1, r2 = r_list[-2], r_list[-1]
        if e1 != e2:
            slope = (r2 - r1) / (e2 - e1)
            intercept = r1 - slope * e1  # R at eps=0, i.e., q=1
            print(f"  m={m}: R0(1) ≈ {float(intercept):.8f} (slope={float(slope):.4f})")
        else:
            print(f"  m={m}: degenerate")

print("\nR1(q→1) extrapolation (polynomial in 1-q):")
for m in sample_monoms[:6]:
    q_list = q_values[-5:]
    eps_list = [Fraction(1) - q for q in q_list]
    r_list = [R1_data.get(q, {}).get(m, Fraction(0)) for q in q_list]
    if all(r == Fraction(0) for r in r_list):
        print(f"  m={m}: identically 0")
        continue
    if len(r_list) >= 2:
        e1, e2 = eps_list[-2], eps_list[-1]
        r1, r2 = r_list[-2], r_list[-1]
        if e1 != e2:
            slope = (r2 - r1) / (e2 - e1)
            intercept = r1 - slope * e1
            print(f"  m={m}: R1(1) ≈ {float(intercept):.8f} (slope={float(slope):.4f})")
        else:
            print(f"  m={m}: degenerate")

# ============================================================
print("\n" + SEP)
print("SECTION 5: Second t value (t=1/3) — verify structure persists")
print(SEP)
sys.stdout.flush()

t_val2 = Fraction(1, 3)
q_test = [Fraction(9, 10), Fraction(19, 20), Fraction(99, 100)]

print(f"t = {t_val2}")
for q_val in q_test:
    poly, rank = compute_estar(q_val, t_val2)
    if poly is None:
        print(f"  q={q_val}: DEGENERATE")
        continue
    T0_poly = hecke_operator(poly, 0, t_val2)
    T1_poly = hecke_operator(poly, 1, t_val2)
    D0 = poly_sub(T0_poly, poly_scale(poly, t_val2))
    D1 = poly_sub(T1_poly, poly_scale(poly, t_val2))
    one_minus_q = Fraction(1) - q_val
    R0 = poly_scale(D0, Fraction(1) / one_minus_q)
    R1 = poly_scale(D1, Fraction(1) / one_minus_q)
    R0_max = max(abs(c) for c in R0.values()) if R0 else Fraction(0)
    R1_max = max(abs(c) for c in R1.values()) if R1 else Fraction(0)
    print(f"  q={str(q_val):>5s}: |R0|_max={float(R0_max):.4e}, |R1|_max={float(R1_max):.4e}")

# ============================================================
print("\n" + SEP)
print("SECTION 6: Symmetry of R_i — is R_i itself symmetric?")
print(SEP)
sys.stdout.flush()

# Check if R0 and R1 are symmetric polynomials at a specific q
q_check = Fraction(9, 10)
poly, _ = compute_estar(q_check, t_val)
T0_poly = hecke_operator(poly, 0, t_val)
D0 = poly_sub(T0_poly, poly_scale(poly, t_val))
R0_check = poly_scale(D0, Fraction(1) / (Fraction(1) - q_check))

asym_count = 0
max_asym = Fraction(0)
for m, c in R0_check.items():
    for p in permutations(m):
        if p != m and p in R0_check:
            diff = abs(R0_check[p] - c)
            if diff > Fraction(0):
                asym_count += 1
            if diff > max_asym:
                max_asym = diff

print(f"R0 at q={q_check}, t={t_val}: asymmetric pairs={asym_count}, max_asym={float(max_asym):.4e}")
if asym_count > 0:
    print("  R0 is NOT symmetric (expected — R_i describes the rate of symmetrization)")
else:
    print("  R0 IS symmetric")

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("""
KILL-TEST RESULTS:
- Divisibility (T_i - t)E* by (1-q): AUTOMATIC for n=3 (consequence of proved symmetry)
- R_i(q) = (T_i - t)E* / (1-q) is bounded as q -> 1: check convergence above
- R_i(q) degree analysis: check Section 3 above
- R_i(1) limit: check Section 4 above

KEY QUESTION: Does R_i(q) have structure (low degree, clean form) that
generalizes to n >= 5 where symmetry is NOT yet proved?

If R_i is a low-degree rational function in q with denominator vanishing only at
q = roots of unity (t-dependent), this suggests a Hecke-algebraic proof strategy.
""")

print(f"Total elapsed: {time.time() - t0:.1f}s")
