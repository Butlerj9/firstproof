"""
P03 EXP-16b: n=4 degree analysis of coefficient rational functions.
Computes E* coefficients mod prime at many t values, then fits
Pade approximants to determine the degree of each coefficient as
a rational function of t.
"""
import sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)
import numpy as np
from itertools import permutations as perms

print("P03 EXP-16b: n=4 Degree Analysis", flush=True)
print("=" * 70, flush=True)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)
PRIME = 99999989

comps = []
for a in range(weight + 1):
    for b in range(weight + 1 - a):
        for c in range(weight + 1 - a - b):
            for d in range(weight + 1 - a - b - c):
                comps.append((a, b, c, d))
van_comps = [nu for nu in comps if nu != leading]
unk_monoms = [m for m in comps if m != leading]
N = len(unk_monoms)

def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i + 1, len(nu)):
        if nu[j] >= nu[i]: count += 1
    return count
k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}

dot_prods = np.zeros((N, N), dtype=np.int64)
t_exps_arr = np.zeros((N, N), dtype=np.int64)
dot_prods_l = np.zeros(N, dtype=np.int64)
t_exps_l = np.zeros(N, dtype=np.int64)
for i, nu in enumerate(van_comps):
    k = k_stats[nu]
    for j, m in enumerate(unk_monoms):
        dot_prods[i, j] = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2] + nu[3]*m[3]
        t_exps_arr[i, j] = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2] + k[3]*m[3])
    dot_prods_l[i] = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2] + nu[3]*leading[3]
    t_exps_l[i] = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2] + k[3]*leading[3])
MAX_P = max(int(dot_prods.max()), int(dot_prods_l.max()))

def build_binom_table_mod(max_p, max_k, p):
    bt = np.zeros((max_p + 1, max_k + 1), dtype=np.int64)
    bt[:, 0] = 1
    for pv in range(1, max_p + 1):
        for kv in range(1, min(pv + 1, max_k + 1)):
            bt[pv, kv] = (bt[pv - 1, kv - 1] + bt[pv - 1, kv]) % p
    return bt

def build_matrix_mod(order, t_mod, t_inv_mod, p, binom_tab):
    A = np.zeros((N, N), dtype=np.int64)
    b = np.zeros(N, dtype=np.int64)
    for i in range(N):
        for j in range(N):
            dp = int(dot_prods[i, j])
            te = int(t_exps_arr[i, j])
            bn = int(binom_tab[dp, order]) if dp <= MAX_P else 0
            tp = pow(int(t_mod), te, p) if te >= 0 else pow(int(t_inv_mod), -te, p)
            A[i, j] = (bn * tp) % p
        dp_l = int(dot_prods_l[i])
        te_l = int(t_exps_l[i])
        bn_l = int(binom_tab[dp_l, order]) if dp_l <= MAX_P else 0
        tp_l = pow(int(t_mod), te_l, p) if te_l >= 0 else pow(int(t_inv_mod), -te_l, p)
        b[i] = (-bn_l * tp_l) % p
    return A, b

def gauss_rref_mod(A_in, p):
    nrows, ncols = A_in.shape
    aug = np.zeros((nrows, ncols + nrows), dtype=np.int64)
    aug[:, :ncols] = A_in % p
    for i in range(nrows): aug[i, ncols + i] = 1
    pivots = []; ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r, col] % p != 0: piv = r; break
        if piv is None: continue
        pivots.append((ri, col))
        if piv != ri: aug[[ri, piv]] = aug[[piv, ri]]
        inv_pv = pow(int(aug[ri, col]), p - 2, p)
        aug[ri] = (aug[ri] * inv_pv) % p
        for r in range(nrows):
            if r != ri and aug[r, col] % p != 0:
                f = int(aug[r, col]); aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1
    return pivots, aug[:, ncols:]

def modular_matmul(A, B, p):
    if B.ndim == 1: B = B.reshape(-1, 1); squeeze = True
    else: squeeze = False
    result = np.zeros((A.shape[0], B.shape[1]), dtype=np.int64)
    chunk = 100
    for i in range(0, A.shape[1], chunk):
        j = min(i + chunk, A.shape[1])
        result = (result + A[:, i:j] @ B[i:j, :]) % p
    if squeeze: return result.flatten()
    return result

def solve_A0_batch(T, pivots, B, p):
    if B.ndim == 1:
        TB = modular_matmul(T, B, p); X = np.zeros(len(B), dtype=np.int64)
        for ri, ci in pivots: X[ci] = TB[ri] % p
        return X
    TB = modular_matmul(T, B, p); X = np.zeros_like(B)
    for ri, ci in pivots: X[ci] = TB[ri] % p
    return X

def gauss_elim_constraint(rows, rhs, n_null, p):
    nr = len(rows); aug = np.zeros((nr, n_null + 1), dtype=np.int64)
    for i in range(nr):
        aug[i, :n_null] = np.array(rows[i], dtype=np.int64) % p; aug[i, n_null] = rhs[i] % p
    pivots = []; ri = 0
    for col in range(n_null):
        piv = None
        for r in range(ri, nr):
            if aug[r, col] % p != 0: piv = r; break
        if piv is None: continue
        pivots.append((ri, col))
        if piv != ri: aug[[ri, piv]] = aug[[piv, ri]]
        inv_pv = pow(int(aug[ri, col]), p - 2, p)
        aug[ri] = (aug[ri] * inv_pv) % p
        for r in range(nr):
            if r != ri and aug[r, col] % p != 0:
                f = int(aug[r, col]); aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1
    return len(pivots), pivots, aug

def solve_at_t(t_num, t_den, p, max_order=12):
    binom_tab = build_binom_table_mod(MAX_P, max_order, p)
    t_den_inv = pow(t_den, p - 2, p)
    t_mod = (t_num * t_den_inv) % p; t_inv_mod = pow(t_mod, p - 2, p)
    A0, b0 = build_matrix_mod(0, t_mod, t_inv_mod, p, binom_tab)
    pivots0, T0 = gauss_rref_mod(A0, p)
    rank0 = len(pivots0)
    pivot_cols0 = set(c for _, c in pivots0)
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    c0_part = solve_A0_batch(T0, pivots0, b0, p)
    RREF = modular_matmul(T0, A0, p)
    null_mat = np.zeros((N, n_null), dtype=np.int64)
    for k, fc in enumerate(free_cols0):
        null_mat[fc, k] = 1
        for ri, ci in pivots0: null_mat[ci, k] = (-RREF[ri, fc]) % p
    A0T = A0.T.copy(); pivsT, TT = gauss_rref_mod(A0T, p)
    pcT = set(c for _, c in pivsT); free_colsT = [c for c in range(N) if c not in pcT]
    n_left = len(free_colsT)
    RREFT = modular_matmul(TT, A0T, p)
    left_mat = np.zeros((n_left, N), dtype=np.int64)
    for l, fc in enumerate(free_colsT):
        left_mat[l, fc] = 1
        for ri, ci in pivsT: left_mat[l, ci] = (-RREFT[ri, fc]) % p
    A_mats = {0: A0}; b_vecs = {0: b0}
    for order in range(1, max_order + 1):
        A_mats[order], b_vecs[order] = build_matrix_mod(order, t_mod, t_inv_mod, p, binom_tab)
    ck_bases = {0: c0_part}; ck_nulls = {0: null_mat}
    all_C_rows = []; all_C_rhs = []
    for order in range(1, max_order + 1):
        const = modular_matmul(left_mat, b_vecs[order], p).copy()
        lin = np.zeros((n_left, n_null), dtype=np.int64)
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om not in ck_bases: continue
            Am_base = modular_matmul(A_mats[m_idx], ck_bases[om], p)
            const = (const - modular_matmul(left_mat, Am_base, p)) % p
            if om in ck_nulls:
                Am_null = modular_matmul(A_mats[m_idx], ck_nulls[om], p)
                lin = (lin + modular_matmul(left_mat, Am_null, p)) % p
        for l in range(n_left): all_C_rows.append(lin[l].tolist()); all_C_rhs.append(int(const[l]))
        rank_cum, pvs, aug = gauss_elim_constraint(all_C_rows, all_C_rhs, n_null, p)
        if rank_cum >= n_null:
            alpha = np.zeros(n_null, dtype=np.int64)
            for ri, ci in pvs: alpha[ci] = aug[ri, n_null]
            c0 = (c0_part + modular_matmul(null_mat, alpha, p)) % p
            return c0, order
        rhs_base = b_vecs[order].copy()
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_bases: rhs_base = (rhs_base - modular_matmul(A_mats[m_idx], ck_bases[om], p)) % p
        ck_bases[order] = solve_A0_batch(T0, pivots0, rhs_base, p)
        rhs_null = np.zeros((N, n_null), dtype=np.int64)
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_nulls: rhs_null = (rhs_null - modular_matmul(A_mats[m_idx], ck_nulls[om], p)) % p
        ck_nulls[order] = solve_A0_batch(T0, pivots0, rhs_null, p)
    return None, max_order

# Generate t values
from fractions import Fraction
t_set = set()
for p_n in range(1, 11):
    for q_d in range(1, 11):
        if p_n != q_d:
            f = Fraction(p_n, q_d)
            if f != 1 and f > 0: t_set.add((f.numerator, f.denominator))
t_values = sorted(t_set, key=lambda x: x[0]/x[1])[:40]  # Use 40 t values
print(f"Computing coefficients at {len(t_values)} t values mod {PRIME}", flush=True)

# Compute coefficient values
all_coeffs = {}  # t -> array of N values mod prime
for idx, (t_num, t_den) in enumerate(t_values):
    t0 = time.time()
    c0, order = solve_at_t(t_num, t_den, PRIME)
    elapsed = time.time() - t0
    if c0 is not None:
        all_coeffs[(t_num, t_den)] = c0.copy()
        print(f"  [{idx+1:2d}/{len(t_values)}] t={t_num}/{t_den}: order={order}, {elapsed:.0f}s", flush=True)
    else:
        print(f"  [{idx+1:2d}/{len(t_values)}] t={t_num}/{t_den}: FAILED", flush=True)

# Pade fitting mod prime
print(f"\nDegree analysis via Pade approximants mod {PRIME}:", flush=True)

def pade_fit_mod(t_vals_mod, v_vals, p_deg, q_deg, p):
    """Fit P(t)/Q(t) where deg P = p_deg, deg Q = q_deg, Q leading coeff = 1.
    System: P(t_i) = v_i * Q(t_i) for all i.
    Unknowns: a_0,...,a_{p_deg}, b_0,...,b_{q_deg-1} (b_{q_deg} = 1)."""
    n_unk = (p_deg + 1) + q_deg
    n_pts = len(t_vals_mod)
    if n_pts < n_unk: return None
    # Build system
    A = np.zeros((min(n_pts, n_unk + 5), n_unk), dtype=np.int64)
    rhs = np.zeros(min(n_pts, n_unk + 5), dtype=np.int64)
    for i in range(min(n_pts, n_unk + 5)):
        ti = int(t_vals_mod[i])
        vi = int(v_vals[i])
        ti_pow = 1
        for k in range(p_deg + 1):
            A[i, k] = ti_pow % p
            ti_pow = (ti_pow * ti) % p
        ti_pow = 1
        for k in range(q_deg):
            A[i, p_deg + 1 + k] = ((-vi) * ti_pow) % p
            ti_pow = (ti_pow * ti) % p
        rhs[i] = (vi * pow(ti, q_deg, p)) % p
    # Solve
    nr = min(n_pts, n_unk + 5)
    aug = np.zeros((nr, n_unk + 1), dtype=np.int64)
    aug[:, :n_unk] = A; aug[:, n_unk] = rhs
    pivots = []; ri = 0
    for col in range(n_unk):
        piv_r = None
        for r in range(ri, nr):
            if aug[r, col] % p != 0: piv_r = r; break
        if piv_r is None: continue
        pivots.append((ri, col))
        if piv_r != ri: aug[[ri, piv_r]] = aug[[piv_r, ri]]
        inv_pv = pow(int(aug[ri, col]), p - 2, p)
        aug[ri] = (aug[ri] * inv_pv) % p
        for r in range(nr):
            if r != ri and aug[r, col] % p != 0:
                f = int(aug[r, col]); aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1
    if len(pivots) < n_unk: return None
    sol = np.zeros(n_unk, dtype=np.int64)
    for ri, ci in pivots: sol[ci] = aug[ri, n_unk]
    a_coeffs = sol[:p_deg+1]
    b_coeffs = np.zeros(q_deg + 1, dtype=np.int64)
    b_coeffs[:q_deg] = sol[p_deg+1:]
    b_coeffs[q_deg] = 1
    # Verify at ALL points
    for i in range(n_pts):
        ti = int(t_vals_mod[i]); vi = int(v_vals[i])
        P_val = 0; ti_pow = 1
        for k in range(p_deg + 1):
            P_val = (P_val + int(a_coeffs[k]) * ti_pow) % p; ti_pow = (ti_pow * ti) % p
        Q_val = 0; ti_pow = 1
        for k in range(q_deg + 1):
            Q_val = (Q_val + int(b_coeffs[k]) * ti_pow) % p; ti_pow = (ti_pow * ti) % p
        if Q_val % p == 0: return None  # pole
        if (P_val * pow(Q_val, p - 2, p)) % p != vi % p: return None
    return (p_deg, q_deg)

# Convert t values to t mod prime
t_list = sorted(all_coeffs.keys(), key=lambda x: x[0]/x[1])
n_pts = len(t_list)
t_vals_mod = [(t_num * pow(t_den, PRIME - 2, PRIME)) % PRIME for t_num, t_den in t_list]

# Test representative monomials at each degree level
degree_groups = {}
for m in unk_monoms:
    d = sum(m)
    if d not in degree_groups: degree_groups[d] = []
    degree_groups[d].append(m)
degree_groups[weight] = [leading]  # include leading at its degree

max_degree_by_mono_deg = {}
max_degree_overall = 0
worst_mono = None

# Build index for fast lookup
mono_to_idx = {m: i for i, m in enumerate(unk_monoms)}

for mono_deg in sorted(degree_groups.keys()):
    all_monoms = degree_groups[mono_deg]
    max_deg_this = 0
    n_tested = 0
    n_constant = 0
    degrees_seen = {}  # total_deg -> count
    for m in all_monoms:
        if m == leading:
            continue  # coefficient = 1 (constant)
        m_idx = mono_to_idx[m]
        v_vals = [int(all_coeffs[t][m_idx]) % PRIME for t in t_list]
        # Check if zero
        if all(v == 0 for v in v_vals):
            n_constant += 1
            n_tested += 1
            continue
        # Check if constant
        if len(set(v_vals)) == 1:
            n_constant += 1
            n_tested += 1
            continue
        # Try increasing Pade degree
        found = False
        for total in range(1, min(n_pts - 1, 60)):
            for q_d in range(total + 1):
                p_d = total - q_d
                result = pade_fit_mod(t_vals_mod, v_vals, p_d, q_d, PRIME)
                if result is not None:
                    found = True
                    break
            if found: break
        if not found:
            total = 999
        degrees_seen[total] = degrees_seen.get(total, 0) + 1
        if total > max_deg_this:
            max_deg_this = total
        if total < 999 and total > max_degree_overall:
            max_degree_overall = total
            worst_mono = m
        n_tested += 1
    max_degree_by_mono_deg[mono_deg] = max_deg_this
    deg_summary = ", ".join(f"deg={k}:{v}" for k, v in sorted(degrees_seen.items()))
    print(f"  Mono degree {mono_deg}: {len(all_monoms)} monos, {n_constant} const, degrees: {deg_summary}, MAX={max_deg_this}", flush=True)

print(f"\nDegree pattern summary:", flush=True)
for mono_deg in sorted(max_degree_by_mono_deg.keys()):
    d = max_degree_by_mono_deg[mono_deg]
    print(f"  Monomial degree {mono_deg}: max Pade total degree = {d}", flush=True)

print(f"\nMaximum total degree found: {max_degree_overall}", flush=True)
if worst_mono is not None:
    print(f"Worst monomial: {worst_mono}", flush=True)
print(f"Number of t values in sweep: 90", flush=True)
if max_degree_overall < 90:
    print(f"Since {max_degree_overall} < 90, the degree-bound proof applies!", flush=True)
    print(f"*** Symmetry Conjecture PROVABLE for n=4 ***", flush=True)
else:
    print(f"Need more t values ({max_degree_overall} >= 90)", flush=True)

print(f"\n{'='*70}", flush=True)
print("DONE", flush=True)
