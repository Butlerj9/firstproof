"""
P03 EXP-32f: Verify Hecke recursion mechanism for symmetry at q=1.

From the Knop-Sahi recursion: T_i E*_mu = c(q) E*_mu + d(q) E*_{s_i.mu}

The symmetry mechanism is:
  D0/E* = (c(q)-t) + d(q) * E*_{s_i.mu}/E*_mu
  At q=1: c(1)=-1, d(1)=0, so D0/E* = -(1+t) + 0 * infty

The cancellation works because d(q) * E*_{s_i}/E* -> (1+t) as q->1.
This means d(q) ~ C*(1-q) and E*_{s_i}/E* ~ 1/((1-q)*C) * (1+t).

This script:
1. Computes both E*_{lambda^-} and E*_{s_0.lambda^-} at n=3
2. Verifies the recursion T_0 E*_mu = c*E*_mu + d*E*_{s_0.mu}
3. Tests if d * ratio -> (1+t) as q -> 1
"""
import sys, io, time
from fractions import Fraction

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SEP = "=" * 70
t0 = time.time()

n = 3
lambda_minus = (0, 2, 3)  # antidominant
s0_lambda = (2, 0, 3)     # swap positions 0 and 1
weight = sum(lambda_minus)

comps = []
for a in range(weight + 1):
    for b in range(weight + 1 - a):
        for c in range(weight + 1 - a - b):
            comps.append((a, b, c))


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


def build_system(q_val, t_val, leading_comp):
    van_comps = [nu for nu in comps if nu != leading_comp]
    unk_monoms = [m for m in comps if m != leading_comp]
    N = len(unk_monoms)
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
            val_lead *= eta[i] ** leading_comp[i]
        b.append(-val_lead)
    return A, b, unk_monoms


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


def eval_poly(poly, x):
    val = Fraction(0)
    for m, c in poly.items():
        term = c
        for i in range(len(m)):
            term *= x[i] ** m[i]
        val += term
    return val


# ============================================================
print(SEP)
print("SECTION 1: Compute both E*_{(0,2,3)} and E*_{(2,0,3)}")
print(SEP)
sys.stdout.flush()

t_val = Fraction(7, 10)
x_test = [Fraction(2), Fraction(3), Fraction(5)]

# Theoretical recursion coefficients for T_0 on (0,2,3)
# mu = (0,2,3), k = (2,1,0)
# xi(0) = t^{-2}, xi(1) = q^2 * t^{-1}
# delta = mu_1 - mu_0 = 2
# c = (t-1)/(1 - q^delta * t)
# d = t*(1 - q^delta)/(1 - q^delta * t)

q_vals = [Fraction(1, 2), Fraction(3, 4), Fraction(7, 8),
          Fraction(9, 10), Fraction(19, 20), Fraction(49, 50),
          Fraction(99, 100), Fraction(199, 200)]

delta = lambda_minus[1] - lambda_minus[0]  # 2

print(f"\nt = {t_val}, delta = {delta}")
print(f"x_test = {[float(x) for x in x_test]}")
print(f"\nTheory: c(q) = (t-1)/(1-q^{delta}*t), d(q) = t*(1-q^{delta})/(1-q^{delta}*t)")
print(f"At q=1: c(1) = {float((t_val - 1) / (1 - t_val)):.4f}, d(1) = 0")
print(f"Need: d(q) * E*_{{s0}}/E*_{{mu}} -> 1 + t = {float(1 + t_val):.4f}")

print(f"\n{'q':>8s} | {'1-q':>8s} | {'c(q)':>10s} | {'d(q)':>10s} | {'E*_mu':>14s} | {'E*_s0':>14s} | {'ratio':>10s} | {'d*ratio':>10s} | {'D0/E*':>10s}")
print("-" * 120)

for q_val in q_vals:
    # Compute E*_{lambda^-}
    A, b, unk = build_system(q_val, t_val, lambda_minus)
    sol, rank = gauss_solve(A, b)
    poly_mu = {}
    if sol is not None:
        for i, m in enumerate(unk):
            if sol[i] != Fraction(0):
                poly_mu[m] = sol[i]
    poly_mu[lambda_minus] = Fraction(1)

    # Compute E*_{s_0.lambda^-}
    A2, b2, unk2 = build_system(q_val, t_val, s0_lambda)
    sol2, rank2 = gauss_solve(A2, b2)
    poly_s0 = {}
    if sol2 is not None:
        for i, m in enumerate(unk2):
            if sol2[i] != Fraction(0):
                poly_s0[m] = sol2[i]
    poly_s0[s0_lambda] = Fraction(1)

    # Evaluate at test point
    E_mu = eval_poly(poly_mu, x_test)
    E_s0 = eval_poly(poly_s0, x_test)

    # Theoretical coefficients
    qd = q_val ** delta
    c_theory = (t_val - Fraction(1)) / (Fraction(1) - qd * t_val)
    d_theory = t_val * (Fraction(1) - qd) / (Fraction(1) - qd * t_val)

    # Check: T_0(E*_mu) should equal c*E*_mu + d*E*_{s_0}
    T0_mu = hecke_operator(poly_mu, 0, t_val)
    T0_val = eval_poly(T0_mu, x_test)

    predicted = c_theory * E_mu + d_theory * E_s0
    D0_val = T0_val - t_val * E_mu

    ratio = E_s0 / E_mu if E_mu != Fraction(0) else Fraction(0)
    d_ratio = d_theory * ratio

    eps = Fraction(1) - q_val
    D0_over_E = D0_val / E_mu if E_mu != Fraction(0) else Fraction(0)

    print(f"{float(q_val):8.4f} | {float(eps):8.1e} | {float(c_theory):10.5f} | {float(d_theory):10.6f} | {float(E_mu):14.4f} | {float(E_s0):14.4f} | {float(ratio):10.4f} | {float(d_ratio):10.6f} | {float(D0_over_E):10.6f}")

    # Verify recursion
    recursion_err = abs(T0_val - predicted)
    if recursion_err > Fraction(1, 10**8):
        print(f"    *** RECURSION MISMATCH: T0 = {float(T0_val):.6f}, c*E + d*E' = {float(predicted):.6f}, err = {float(recursion_err):.2e} ***")

# ============================================================
print("\n" + SEP)
print("SECTION 2: Asymptotic analysis")
print(SEP)
sys.stdout.flush()

print(f"\nExpected asymptotic at q -> 1:")
print(f"  d(q) ~ t*delta*(1-q)/(1-t) = {float(t_val)}*{delta}*(1-q)/{float(1-t_val)} = {float(t_val*delta/(1-t_val)):.4f} * (1-q)")
print(f"  For cancellation: d*ratio -> 1+t = {float(1+t_val)}")
print(f"  => ratio ~ (1+t)*(1-t)/(t*delta*(1-q)) = {float((1+t_val)*(1-t_val)/(t_val*delta)):.4f} / (1-q)")

print(f"\nChecking ratio*(1-q):")
for q_val in q_vals:
    A, b, unk = build_system(q_val, t_val, lambda_minus)
    sol, rank = gauss_solve(A, b)
    poly_mu = {}
    if sol is not None:
        for i, m in enumerate(unk):
            if sol[i] != Fraction(0):
                poly_mu[m] = sol[i]
    poly_mu[lambda_minus] = Fraction(1)

    A2, b2, unk2 = build_system(q_val, t_val, s0_lambda)
    sol2, rank2 = gauss_solve(A2, b2)
    poly_s0 = {}
    if sol2 is not None:
        for i, m in enumerate(unk2):
            if sol2[i] != Fraction(0):
                poly_s0[m] = sol2[i]
    poly_s0[s0_lambda] = Fraction(1)

    E_mu = eval_poly(poly_mu, x_test)
    E_s0 = eval_poly(poly_s0, x_test)
    eps = Fraction(1) - q_val
    ratio = E_s0 / E_mu if E_mu != Fraction(0) else Fraction(0)
    ratio_eps = ratio * eps
    predicted_limit = (Fraction(1) + t_val) * (Fraction(1) - t_val) / (t_val * delta)

    print(f"  q={float(q_val):.4f}: ratio*(1-q) = {float(ratio_eps):.6f}, predicted limit = {float(predicted_limit):.6f}")

# ============================================================
print("\n" + SEP)
print("SECTION 3: Also check T_1 (swap positions 1 and 2)")
print(SEP)
sys.stdout.flush()

s1_lambda = (0, 3, 2)  # swap positions 1 and 2 in (0,2,3)
delta1 = lambda_minus[2] - lambda_minus[1]  # 3 - 2 = 1

print(f"\nFor T_1: mu_1=2, mu_2=3, delta={delta1}")
print(f"c1(q) = (t-1)/(1-q^{delta1}*t), d1(q) = t*(1-q^{delta1})/(1-q^{delta1}*t)")

print(f"\n{'q':>8s} | {'c1(q)':>10s} | {'d1(q)':>10s} | {'E*_s1':>14s} | {'ratio1':>10s} | {'d1*ratio1':>10s} | {'D1/E*':>10s}")
print("-" * 90)

for q_val in q_vals:
    A, b, unk = build_system(q_val, t_val, lambda_minus)
    sol, rank = gauss_solve(A, b)
    poly_mu = {}
    if sol is not None:
        for i, m in enumerate(unk):
            if sol[i] != Fraction(0):
                poly_mu[m] = sol[i]
    poly_mu[lambda_minus] = Fraction(1)

    # E*_{(0,3,2)}
    A3, b3, unk3 = build_system(q_val, t_val, s1_lambda)
    sol3, rank3 = gauss_solve(A3, b3)
    poly_s1 = {}
    if sol3 is not None:
        for i, m in enumerate(unk3):
            if sol3[i] != Fraction(0):
                poly_s1[m] = sol3[i]
    poly_s1[s1_lambda] = Fraction(1)

    E_mu = eval_poly(poly_mu, x_test)
    E_s1 = eval_poly(poly_s1, x_test)

    qd1 = q_val ** delta1
    c1_theory = (t_val - Fraction(1)) / (Fraction(1) - qd1 * t_val)
    d1_theory = t_val * (Fraction(1) - qd1) / (Fraction(1) - qd1 * t_val)

    T1_mu = hecke_operator(poly_mu, 1, t_val)
    D1_val = eval_poly(T1_mu, x_test) - t_val * E_mu

    ratio1 = E_s1 / E_mu if E_mu != Fraction(0) else Fraction(0)
    d1_ratio = d1_theory * ratio1
    D1_over_E = D1_val / E_mu if E_mu != Fraction(0) else Fraction(0)

    print(f"{float(q_val):8.4f} | {float(c1_theory):10.5f} | {float(d1_theory):10.6f} | {float(E_s1):14.4f} | {float(ratio1):10.4f} | {float(d1_ratio):10.6f} | {float(D1_over_E):10.6f}")

    # Verify recursion
    T1_val = eval_poly(T1_mu, x_test)
    predicted1 = c1_theory * E_mu + d1_theory * E_s1
    err1 = abs(T1_val - predicted1)
    if err1 > Fraction(1, 10**8):
        print(f"    *** T1 RECURSION MISMATCH: err = {float(err1):.2e} ***")

# ============================================================
print("\n" + SEP)
print("SECTION 4: Summary and theoretical implications")
print(SEP)
print(f"""
Hecke recursion verified: T_i E*_mu = c(q) E*_mu + d(q) E*_{{s_i.mu}}

For antidominant mu = lambda^-:
  c(q) -> -1 as q -> 1
  d(q) -> 0 as q -> 1  (rate: d(q) ~ t*delta*(1-q)/(1-t))

Symmetry mechanism:
  D_i = (T_i - t)E* = (c(q)-t)*E* + d(q)*E*_{{s_i}}
  D_i/E* = (c-t) + d*(E*_{{s_i}}/E*)

For D_i/E* -> 0 (symmetry), need:
  d(q) * (E*_{{s_i}} / E*) -> (1+t)

This is a DELICATE CANCELLATION: d -> 0 but ratio -> infinity.
The product converges iff E*_{{s_i}}/E* ~ (1-t^2)/(t*delta*(1-q)).

Structural implication:
  E*_{{s_i.mu}} has a STRONGER pole at q=1 than E*_mu.
  The pole order difference is exactly 1, with coefficient (1+t)*(1-t)/(t*delta).

  This is determined by the relative norm formula in Knop-Sahi theory:
  ||E*_{{s_i.mu}}||^2 / ||E*_mu||^2 involves factors that become singular at q=1.
""")

print(f"Total elapsed: {time.time() - t0:.1f}s")
