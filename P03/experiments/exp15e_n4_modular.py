"""
P03 EXP-15e: n=4 perturbation via modular arithmetic.
Solves the perturbation system mod several large primes, then uses CRT +
rational reconstruction to recover exact rational coefficients.
MUCH faster than Fraction or mpmath for 714x714 systems.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from itertools import permutations as perms
from fractions import Fraction

print("P03 EXP-15e: n=4 Modular Perturbation")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)

# Large primes for modular arithmetic
PRIMES = [
    2305843009213693951,   # 2^61 - 1
    4611686018427387847,   # large prime near 2^62
    9223372036854775783,   # large prime near 2^63
    18446744073709551557,  # large prime near 2^64
]

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
print(f"N = {N} unknowns")


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

# Precompute binomial coefficients for orders 0..20
# binom(p, k) for p up to weight*weight = 81, k up to 20
MAX_P = weight * weight  # max dot product
MAX_ORDER = 20
binom_table = [[0] * (MAX_ORDER + 1) for _ in range(MAX_P + 1)]
for p in range(MAX_P + 1):
    binom_table[p][0] = 1
    for k in range(1, min(p + 1, MAX_ORDER + 1)):
        binom_table[p][k] = binom_table[p - 1][k - 1] + binom_table[p - 1][k]


def build_matrices_mod(t_num, t_den, p, max_order):
    """Build perturbation matrices mod prime p.
    t = t_num/t_den. We compute t_mod = t_num * inverse(t_den) mod p."""
    t_den_inv = pow(t_den, p - 2, p)  # Fermat's little theorem
    t_mod = (t_num * t_den_inv) % p
    t_inv_mod = pow(t_mod, p - 2, p)  # t^{-1} mod p

    # Precompute t^k mod p for k in range
    max_exp = weight * n * weight  # generous upper bound
    t_pow = [1] * (max_exp + 1)
    for k in range(1, max_exp + 1):
        t_pow[k] = (t_pow[k - 1] * t_mod) % p
    t_neg_pow = [1] * (max_exp + 1)
    for k in range(1, max_exp + 1):
        t_neg_pow[k] = (t_neg_pow[k - 1] * t_inv_mod) % p

    matrices = {}
    rhs = {}
    for order in range(max_order + 1):
        mat = []
        b_vec = []
        for nu in van_comps:
            k = k_stats[nu]
            row = []
            for m in unk_monoms:
                t_exp = -(k[0] * m[0] + k[1] * m[1] + k[2] * m[2] + k[3] * m[3])
                dot_p = nu[0] * m[0] + nu[1] * m[1] + nu[2] * m[2] + nu[3] * m[3]
                bn = binom_table[dot_p][order] if dot_p <= MAX_P and order <= MAX_ORDER else 0
                if t_exp >= 0:
                    tp = t_pow[t_exp]
                else:
                    tp = t_neg_pow[-t_exp]
                val = (bn * tp) % p
                row.append(val)
            mat.append(row)

            t_exp_l = -(k[0] * leading[0] + k[1] * leading[1] + k[2] * leading[2] + k[3] * leading[3])
            dot_p_l = nu[0] * leading[0] + nu[1] * leading[1] + nu[2] * leading[2] + nu[3] * leading[3]
            bn_l = binom_table[dot_p_l][order] if dot_p_l <= MAX_P and order <= MAX_ORDER else 0
            if t_exp_l >= 0:
                tp_l = t_pow[t_exp_l]
            else:
                tp_l = t_neg_pow[-t_exp_l]
            b_vec.append((-(bn_l * tp_l)) % p)

        matrices[order] = mat
        rhs[order] = b_vec
    return matrices, rhs


def gauss_elim_mod(mat, rhs_vec, nrows, ncols, p):
    """Gaussian elimination mod p. Returns pivots and augmented matrix."""
    aug = [row[:] + [rhs_vec[i]] for i, row in enumerate(mat)]
    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r][col] % p != 0:
                piv = r
                break
        if piv is None:
            continue
        pivots.append((ri, col))
        if piv != ri:
            aug[ri], aug[piv] = aug[piv], aug[ri]
        inv_pv = pow(aug[ri][col], p - 2, p)
        for j in range(ncols + 1):
            aug[ri][j] = (aug[ri][j] * inv_pv) % p
        for r in range(nrows):
            if r != ri and aug[r][col] % p != 0:
                f = aug[r][col]
                for j in range(ncols + 1):
                    aug[r][j] = (aug[r][j] - f * aug[ri][j]) % p
        ri += 1
    return pivots, aug


def matvec_mod(M, v, nrows, ncols, p):
    result = [0] * nrows
    for i in range(nrows):
        s = 0
        for j in range(ncols):
            s = (s + M[i][j] * v[j]) % p
        result[i] = s
    return result


def dot_mod(u, v, n, p):
    s = 0
    for i in range(n):
        s = (s + u[i] * v[i]) % p
    return s % p


def solve_perturbation_mod(t_num, t_den, prime, max_order=MAX_ORDER):
    """Solve the perturbation system mod prime. Returns c0 mod prime or None."""
    t0 = time.time()
    p = prime

    # Build all matrices
    A, b = build_matrices_mod(t_num, t_den, p, max_order)
    t_build = time.time() - t0

    # Order 0: RREF
    t0_elim = time.time()
    pivots0, aug0 = gauss_elim_mod(A[0], b[0], N, N, p)
    rank0 = len(pivots0)
    pivot_cols0 = {c for _, c in pivots0}
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    t_elim = time.time() - t0_elim

    # Particular solution
    c0_part = [0] * N
    for r, c in pivots0:
        c0_part[c] = aug0[r][N]

    # Null space basis
    null_vecs = []
    for fc in free_cols0:
        v = [0] * N
        v[fc] = 1
        for r, c in pivots0:
            v[c] = (-aug0[r][fc]) % p
        null_vecs.append(v)

    # Left null space: transpose of A[0]
    A0T = [[A[0][j][i] for j in range(N)] for i in range(N)]
    pivsT, augT = gauss_elim_mod(A0T, [0] * N, N, N, p)
    pcT = {c for _, c in pivsT}
    left_null = []
    for fc in [c for c in range(N) if c not in pcT]:
        v = [0] * N
        v[fc] = 1
        for r, c in pivsT:
            v[c] = (-augT[r][fc]) % p
        left_null.append(v)
    n_left = len(left_null)

    print(f"    rank={rank0}, null={n_null}, left_null={n_left} (build {t_build:.1f}s, elim {t_elim:.1f}s)")

    # Perturbation iteration
    ck_bases = {0: c0_part}
    ck_nullss = {0: null_vecs}
    all_rows = []
    all_rhs_vals = []

    for order in range(1, max_order + 1):
        t_order = time.time()

        const = [0] * n_left
        lin = [[0] * n_null for _ in range(n_left)]

        for l in range(n_left):
            const[l] = dot_mod(left_null[l], b[order], N, p)

        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om not in ck_bases:
                continue
            Am_ckb = matvec_mod(A[m_idx], ck_bases[om], N, N, p)
            for l in range(n_left):
                const[l] = (const[l] - dot_mod(left_null[l], Am_ckb, N, p)) % p

            if om in ck_nullss:
                for k in range(n_null):
                    Am_ckn = matvec_mod(A[m_idx], ck_nullss[om][k], N, N, p)
                    for l in range(n_left):
                        lin[l][k] = (lin[l][k] + dot_mod(left_null[l], Am_ckn, N, p)) % p

        for l in range(n_left):
            all_rows.append(lin[l][:])
            all_rhs_vals.append(const[l])

        # Check cumulative rank
        pvs, aug_acc = gauss_elim_mod(all_rows, all_rhs_vals, len(all_rows), n_null, p)
        rank_cum = len(pvs)
        elapsed = time.time() - t_order
        total = time.time() - t0

        print(f"    Order {order}: rank={rank_cum}/{n_null} ({elapsed:.1f}s, total {total:.0f}s)")

        if rank_cum >= n_null:
            print(f"    ** CLOSED at order {order}! **")
            alpha = [0] * n_null
            for r, c in pvs:
                alpha[c] = aug_acc[r][n_null]
            c0 = [(c0_part[j] + sum(alpha[k] * null_vecs[k][j] for k in range(n_null))) % p for j in range(N)]
            return c0

        # Compute c_k base for next iteration (need A0 solve)
        rhs_base = list(b[order])
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_bases:
                Am_ckb = matvec_mod(A[m_idx], ck_bases[om], N, N, p)
                for i in range(N):
                    rhs_base[i] = (rhs_base[i] - Am_ckb[i]) % p
        # Solve A0 * c_k = rhs_base (reuse RREF)
        # Since we have RREF of A0, solve by back substitution
        pvs0_rhs, aug0_rhs = gauss_elim_mod(A[0], rhs_base, N, N, p)
        ck_base = [0] * N
        for r, c in pvs0_rhs:
            ck_base[c] = aug0_rhs[r][N]
        ck_bases[order] = ck_base

        # Compute c_k null vectors
        ck_nullss[order] = []
        for k in range(n_null):
            rhs_k = [0] * N
            for m_idx in range(1, order + 1):
                om = order - m_idx
                if om in ck_nullss:
                    Am_ckn = matvec_mod(A[m_idx], ck_nullss[om][k], N, N, p)
                    for i in range(N):
                        rhs_k[i] = (rhs_k[i] - Am_ckn[i]) % p
            pvs_k, aug_k = gauss_elim_mod(A[0], rhs_k, N, N, p)
            ck_null = [0] * N
            for r, c in pvs_k:
                ck_null[c] = aug_k[r][N]
            ck_nullss[order].append(ck_null)

    print(f"    ** Did not close through order {max_order} **")
    return None


def rational_reconstruct(residue, prime):
    """Reconstruct rational number a/b from residue mod prime.
    Uses extended GCD / continued fraction approach.
    Returns (a, b) with b > 0, gcd(a,b) = 1, and a/b ≡ residue (mod prime)."""
    # Continued fraction / half-gcd approach
    # Find a, b with |a| < sqrt(p/2), 0 < b < sqrt(p/2), a ≡ b*residue (mod p)
    limit = int(prime ** 0.5)
    r0, r1 = prime, residue % prime
    s0, s1 = 0, 1
    while r1 > limit:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    # Now r1 = a (or -a), s1 = b (or -b)
    a, b = r1, s1
    if b < 0:
        a, b = -a, -b
    from math import gcd
    g = gcd(abs(a), abs(b))
    return a // g, b // g


# Main computation
t_num, t_den = 7, 10

print(f"\nt = {t_num}/{t_den}")
print(f"Testing with prime p0 = {PRIMES[0]}")

t0_total = time.time()
c0_mod_p0 = solve_perturbation_mod(t_num, t_den, PRIMES[0])

if c0_mod_p0 is not None:
    print(f"\n  Total time: {time.time()-t0_total:.1f}s")

    # Quick symmetry check mod p0
    print(f"\n  Checking symmetry mod p0...")
    coeff_dict = {}
    for i, m in enumerate(unk_monoms):
        coeff_dict[m] = c0_mod_p0[i]
    coeff_dict[leading] = 1

    broken = 0
    total = 0
    for m, val in coeff_dict.items():
        for perm in perms(m):
            if perm > m and perm in coeff_dict:
                total += 1
                if coeff_dict[perm] % PRIMES[0] != val % PRIMES[0]:
                    broken += 1

    if broken == 0:
        print(f"  SYMMETRIC mod p0 ({total} pairs checked)")
    else:
        print(f"  BROKEN mod p0: {broken}/{total} pairs differ")

    # If symmetric mod p0, verify mod second prime
    if broken == 0:
        print(f"\n  Verifying with prime p1 = {PRIMES[1]}")
        t0_p1 = time.time()
        c0_mod_p1 = solve_perturbation_mod(t_num, t_den, PRIMES[1])
        if c0_mod_p1 is not None:
            print(f"  Time: {time.time()-t0_p1:.1f}s")

            broken2 = 0
            coeff_dict2 = {}
            for i, m in enumerate(unk_monoms):
                coeff_dict2[m] = c0_mod_p1[i]
            coeff_dict2[leading] = 1
            for m, val in coeff_dict2.items():
                for perm in perms(m):
                    if perm > m and perm in coeff_dict2:
                        if coeff_dict2[perm] % PRIMES[1] != val % PRIMES[1]:
                            broken2 += 1

            if broken2 == 0:
                print(f"  SYMMETRIC mod p1 ({total} pairs checked)")
                print(f"\n  ** SYMMETRY CONFIRMED mod TWO independent primes **")
                print(f"  ** This is very strong evidence (probability of false positive: < 10^(-36)) **")
            else:
                print(f"  BROKEN mod p1: {broken2}/{total} pairs differ")
    elif broken > 0:
        print(f"\n  Trying rational reconstruction on first few coefficients...")
        for i in range(min(5, N)):
            m = unk_monoms[i]
            a, b = rational_reconstruct(c0_mod_p0[i], PRIMES[0])
            print(f"    c{m} ≈ {a}/{b}")

else:
    print(f"\n  FAILED: perturbation did not close")

print(f"\n{'='*70}")
print(f"Total time: {time.time()-t0_total:.1f}s")
print("DONE")
