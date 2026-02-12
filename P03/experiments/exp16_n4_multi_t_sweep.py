"""
P03 EXP-16: n=4 multi-t symmetry sweep.
Tests symmetry at many rational t values mod two primes.
If symmetry holds at N > degree_bound values, the Symmetry Conjecture is proved.
"""
import sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)
os.environ['PYTHONUNBUFFERED'] = '1'
import numpy as np
from itertools import permutations as perms

print("P03 EXP-16: n=4 Multi-t Symmetry Sweep")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)
PRIMES = [99999989, 99999971]

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

def k_stat(nu, i):
    count = 0
    for j in range(i):
        if nu[j] > nu[i]: count += 1
    for j in range(i + 1, len(nu)):
        if nu[j] >= nu[i]: count += 1
    return count

k_stats = {nu: tuple(k_stat(nu, i) for i in range(n)) for nu in comps}

# Precompute dot products and t-exponents
dot_prods = np.zeros((N, N), dtype=np.int64)
t_exps = np.zeros((N, N), dtype=np.int64)
dot_prods_l = np.zeros(N, dtype=np.int64)
t_exps_l = np.zeros(N, dtype=np.int64)
for i, nu in enumerate(van_comps):
    k = k_stats[nu]
    for j, m in enumerate(unk_monoms):
        dot_prods[i, j] = nu[0]*m[0] + nu[1]*m[1] + nu[2]*m[2] + nu[3]*m[3]
        t_exps[i, j] = -(k[0]*m[0] + k[1]*m[1] + k[2]*m[2] + k[3]*m[3])
    dot_prods_l[i] = nu[0]*leading[0] + nu[1]*leading[1] + nu[2]*leading[2] + nu[3]*leading[3]
    t_exps_l[i] = -(k[0]*leading[0] + k[1]*leading[1] + k[2]*leading[2] + k[3]*leading[3])

MAX_P = int(dot_prods.max())
MAX_P_L = int(dot_prods_l.max())
MAX_P = max(MAX_P, MAX_P_L)

def build_binom_table_mod(max_p, max_k, p):
    """Compute binom mod p to avoid overflow."""
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
            te = int(t_exps[i, j])
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
    pivots = []
    ri = 0
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
                f = int(aug[r, col])
                aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1
    return pivots, aug[:, ncols:]

def modular_matmul(A, B, p):
    if B.ndim == 1:
        B = B.reshape(-1, 1)
        result = np.zeros((A.shape[0], 1), dtype=np.int64)
        chunk = 100
        for i in range(0, A.shape[1], chunk):
            j = min(i + chunk, A.shape[1])
            result = (result + A[:, i:j] @ B[i:j, :]) % p
        return result.flatten()
    result = np.zeros((A.shape[0], B.shape[1]), dtype=np.int64)
    chunk = 100
    for i in range(0, A.shape[1], chunk):
        j = min(i + chunk, A.shape[1])
        result = (result + A[:, i:j] @ B[i:j, :]) % p
    return result

def solve_A0_batch(T, pivots, B, p):
    if B.ndim == 1:
        TB = modular_matmul(T, B, p)
        X = np.zeros(len(B), dtype=np.int64)
        for ri, ci in pivots: X[ci] = TB[ri] % p
        return X
    TB = modular_matmul(T, B, p)
    X = np.zeros_like(B)
    for ri, ci in pivots: X[ci] = TB[ri] % p
    return X

def gauss_elim_constraint(rows, rhs, n_null, p):
    nr = len(rows)
    aug = np.zeros((nr, n_null + 1), dtype=np.int64)
    for i in range(nr):
        aug[i, :n_null] = np.array(rows[i], dtype=np.int64) % p
        aug[i, n_null] = rhs[i] % p
    pivots = []
    ri = 0
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
                f = int(aug[r, col])
                aug[r] = (aug[r] - f * aug[ri]) % p
        ri += 1
    return len(pivots), pivots, aug

def solve_at_t(t_num, t_den, p, max_order=12):
    binom_tab = build_binom_table_mod(MAX_P, max_order, p)
    t_den_inv = pow(t_den, p - 2, p)
    t_mod = (t_num * t_den_inv) % p
    t_inv_mod = pow(t_mod, p - 2, p)

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
        for ri, ci in pivots0:
            null_mat[ci, k] = (-RREF[ri, fc]) % p

    A0T = A0.T.copy()
    pivsT, TT = gauss_rref_mod(A0T, p)
    pcT = set(c for _, c in pivsT)
    free_colsT = [c for c in range(N) if c not in pcT]
    n_left = len(free_colsT)
    RREFT = modular_matmul(TT, A0T, p)
    left_mat = np.zeros((n_left, N), dtype=np.int64)
    for l, fc in enumerate(free_colsT):
        left_mat[l, fc] = 1
        for ri, ci in pivsT:
            left_mat[l, ci] = (-RREFT[ri, fc]) % p

    A_mats = {0: A0}
    b_vecs = {0: b0}
    for order in range(1, max_order + 1):
        A_mats[order], b_vecs[order] = build_matrix_mod(order, t_mod, t_inv_mod, p, binom_tab)

    ck_bases = {0: c0_part}
    ck_nulls = {0: null_mat}
    all_C_rows = []
    all_C_rhs = []

    for order in range(1, max_order + 1):
        L_b = modular_matmul(left_mat, b_vecs[order], p)
        const = L_b.copy()
        lin = np.zeros((n_left, n_null), dtype=np.int64)
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om not in ck_bases: continue
            Am_base = modular_matmul(A_mats[m_idx], ck_bases[om], p)
            const = (const - modular_matmul(left_mat, Am_base, p)) % p
            if om in ck_nulls:
                Am_null = modular_matmul(A_mats[m_idx], ck_nulls[om], p)
                lin = (lin + modular_matmul(left_mat, Am_null, p)) % p
        for l in range(n_left):
            all_C_rows.append(lin[l].tolist())
            all_C_rhs.append(int(const[l]))
        rank_cum, pvs, aug = gauss_elim_constraint(all_C_rows, all_C_rhs, n_null, p)
        if rank_cum >= n_null:
            alpha = np.zeros(n_null, dtype=np.int64)
            for ri, ci in pvs: alpha[ci] = aug[ri, n_null]
            c0 = (c0_part + modular_matmul(null_mat, alpha, p)) % p
            return c0, rank0, n_null, order
        rhs_base = b_vecs[order].copy()
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_bases:
                rhs_base = (rhs_base - modular_matmul(A_mats[m_idx], ck_bases[om], p)) % p
        ck_bases[order] = solve_A0_batch(T0, pivots0, rhs_base, p)
        rhs_null = np.zeros((N, n_null), dtype=np.int64)
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_nulls:
                rhs_null = (rhs_null - modular_matmul(A_mats[m_idx], ck_nulls[om], p)) % p
        ck_nulls[order] = solve_A0_batch(T0, pivots0, rhs_null, p)
    return None, rank0, n_null, max_order

def check_symmetry_mod(c0, p):
    coeff_dict = {}
    for i, m in enumerate(unk_monoms): coeff_dict[m] = int(c0[i]) % p
    coeff_dict[leading] = 1
    broken = 0
    total = 0
    for m, val in coeff_dict.items():
        for perm in perms(m):
            if perm > m and perm in coeff_dict:
                total += 1
                if coeff_dict[perm] % p != val % p: broken += 1
    return broken, total

# Generate t values: p/q for 1 <= p,q <= 12, p != q, t != 1
from fractions import Fraction
t_set = set()
for p_num in range(1, 13):
    for q_den in range(1, 13):
        if p_num != q_den:
            f = Fraction(p_num, q_den)
            if f != 1 and f > 0:
                t_set.add((f.numerator, f.denominator))
t_values = sorted(t_set, key=lambda x: x[0] / x[1])
print(f"Testing {len(t_values)} t values x {len(PRIMES)} primes", flush=True)
print(f"Estimated time: {len(t_values) * len(PRIMES) * 75 / 3600:.1f} hours", flush=True)
print(flush=True)

results = {}
t_total_start = time.time()
for idx, (t_num, t_den) in enumerate(t_values):
    t_val = Fraction(t_num, t_den)
    t0 = time.time()
    all_sym = True
    orders_needed = 0
    for prime in PRIMES:
        c0, rank, n_null, order = solve_at_t(t_num, t_den, prime)
        if c0 is None:
            all_sym = False
            break
        broken, total = check_symmetry_mod(c0, prime)
        if broken > 0:
            all_sym = False
            break
        orders_needed = max(orders_needed, order)
    elapsed = time.time() - t0
    eta = (time.time() - t_total_start) / (idx + 1) * (len(t_values) - idx - 1)
    status = "SYM" if all_sym else "BROKEN"
    results[(t_num, t_den)] = all_sym
    print(f"  [{idx+1:3d}/{len(t_values)}] t={t_num}/{t_den:2d} ({float(t_val):6.3f}): {status} (order {orders_needed}, {elapsed:.0f}s, ETA {eta/60:.0f}m)", flush=True)

# Summary
n_sym = sum(1 for v in results.values() if v)
n_total = len(results)
print(f"\n{'='*70}")
print(f"RESULTS: {n_sym}/{n_total} t-values show SYMMETRY mod both primes")
if n_sym == n_total:
    print(f"*** ALL {n_total} t-values SYMMETRIC ***")
    print(f"If degree bound D < {n_total}, Symmetry Conjecture PROVED for n=4")
else:
    broken_ts = [f"{t[0]}/{t[1]}" for t, v in results.items() if not v]
    print(f"BROKEN at: {', '.join(broken_ts)}")
print(f"\nTotal time: {(time.time()-t_total_start)/60:.1f} min")
print("DONE")
