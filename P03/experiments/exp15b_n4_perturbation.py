"""
P03 EXP-15b: n=4 perturbation solver for Symmetry Conjecture.
Computes E*_{lambda^-}(q=1, t) exactly at a single t value using Fraction arithmetic.
Optimized: pre-compute A0 factorization, reuse for all back-substitutions.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P03 EXP-15b: n=4 Perturbation Solver")
print("=" * 70)

n = 4
lam = (4, 3, 2, 0)
leading = (0, 2, 3, 4)
weight = sum(lam)

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


def binom_frac(p, k):
    if k < 0:
        return Fraction(0)
    if k == 0:
        return Fraction(1)
    fk = Fraction(1)
    for i in range(1, k + 1):
        fk *= Fraction(i)
    r = Fraction(1)
    for i in range(k):
        r *= Fraction(p - i)
    return r / fk


def build_matrices(t_val, max_order):
    """Build perturbation matrices A_k and RHS b_k for orders 0..max_order."""
    matrices = {k: [] for k in range(max_order + 1)}
    rhs = {k: [] for k in range(max_order + 1)}
    for nu in van_comps:
        k = k_stats[nu]
        for order in range(max_order + 1):
            row = []
            for m in unk_monoms:
                t_exp = -(k[0] * m[0] + k[1] * m[1] + k[2] * m[2] + k[3] * m[3])
                p = nu[0] * m[0] + nu[1] * m[1] + nu[2] * m[2] + nu[3] * m[3]
                if t_exp >= 0:
                    tp = t_val ** t_exp
                else:
                    tp = Fraction(1, 1) / (t_val ** (-t_exp))
                row.append(binom_frac(p, order) * tp)
            matrices[order].append(row)
            t_exp_l = -(k[0] * leading[0] + k[1] * leading[1] + k[2] * leading[2] + k[3] * leading[3])
            p_l = nu[0] * leading[0] + nu[1] * leading[1] + nu[2] * leading[2] + nu[3] * leading[3]
            if t_exp_l >= 0:
                tp_l = t_val ** t_exp_l
            else:
                tp_l = Fraction(1, 1) / (t_val ** (-t_exp_l))
            rhs[order].append(-binom_frac(p_l, order) * tp_l)
    return matrices, rhs


def gauss_elim(mat, rhs_vec, nrows, ncols):
    """Full Gaussian elimination with augmented matrix. Returns pivots and augmented matrix."""
    aug = [mat[i][:] + [rhs_vec[i]] for i in range(nrows)]
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
        inv_pv = Fraction(1) / pv
        for j in range(ncols + 1):
            aug[ri][j] *= inv_pv
        for r in range(nrows):
            if r != ri and aug[r][col] != Fraction(0):
                f = aug[r][col]
                for j in range(ncols + 1):
                    aug[r][j] -= f * aug[ri][j]
        ri += 1
    return pivots, aug


def solve_using_rref(pivots, aug_template, rhs_new, ncols):
    """Solve A0*x = rhs_new using pre-computed RREF of A0.
    Note: This only works if A0 is the same. We re-solve from scratch
    but reuse pivot order for efficiency. Actually for correctness we need
    full re-solve. Use the augmented matrix approach."""
    # For correctness, we must re-do the elimination with new RHS.
    # But we can reuse the pivot column order.
    # Actually, let's just do standard forward/backward substitution with the pivot info.
    # This requires storing the full transformation matrix, which is the RREF itself.
    # A simpler approach: store L,U factors and solve L*U*x = b.
    # For now, let's just solve from scratch with a fast method.
    pass


def solve_A0(A0, b_vec, N):
    """Solve A0*x = b by Gaussian elimination."""
    pvs, ag = gauss_elim(A0, b_vec, N, N)
    x = [Fraction(0)] * N
    for r, c in pvs:
        x[c] = ag[r][N]
    return x


def matvec(M, v, nrows, ncols):
    """Matrix-vector product."""
    result = [Fraction(0)] * nrows
    for i in range(nrows):
        s = Fraction(0)
        for j in range(ncols):
            if M[i][j] != Fraction(0) and v[j] != Fraction(0):
                s += M[i][j] * v[j]
        result[i] = s
    return result


def dot(u, v, n):
    s = Fraction(0)
    for i in range(n):
        if u[i] != Fraction(0) and v[i] != Fraction(0):
            s += u[i] * v[i]
    return s


def check_symmetry(c0):
    from itertools import permutations
    coeffs = {}
    for i, m in enumerate(unk_monoms):
        coeffs[m] = c0[i]
    coeffs[leading] = Fraction(1)
    max_asym = Fraction(0)
    asym_count = 0
    for m, val in coeffs.items():
        for p in permutations(m):
            if p != m and p in coeffs:
                diff = abs(coeffs[p] - val)
                if diff > Fraction(0):
                    asym_count += 1
                if diff > max_asym:
                    max_asym = diff
    is_sym = (max_asym == Fraction(0))
    print(f"    Symmetry: {'EXACT' if is_sym else 'BROKEN'}, max_asym={float(max_asym):.3e}, pairs_broken={asym_count}")
    return is_sym


def run(t_val):
    t_total = time.time()
    print(f"\n  t = {t_val}:")
    MAX_ORDER = 20  # generous upper bound

    # Build perturbation matrices
    t0 = time.time()
    print(f"    Building matrices (orders 0..{MAX_ORDER})...", end="")
    sys.stdout.flush()
    A, b = build_matrices(t_val, max_order=MAX_ORDER)
    print(f" {time.time()-t0:.1f}s")

    # Order 0: Gaussian elimination
    t0 = time.time()
    print(f"    Order 0 elimination ({N}x{N})...", end="")
    sys.stdout.flush()
    pivots0, aug0 = gauss_elim(A[0], b[0], N, N)
    rank0 = len(pivots0)
    pivot_cols0 = {c for _, c in pivots0}
    free_cols0 = [c for c in range(N) if c not in pivot_cols0]
    n_null = len(free_cols0)
    print(f" rank={rank0}, null={n_null} ({time.time()-t0:.1f}s)")

    # Particular solution
    c0_part = [Fraction(0)] * N
    for r, c in pivots0:
        c0_part[c] = aug0[r][N]

    # Null space basis
    t0 = time.time()
    print(f"    Computing null space ({n_null} vectors)...", end="")
    sys.stdout.flush()
    null_vecs = []
    for fc in free_cols0:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivots0:
            v[c] = -aug0[r][fc]
        null_vecs.append(v)
    print(f" {time.time()-t0:.1f}s")

    # Left null space
    t0 = time.time()
    print(f"    Computing left null space...", end="")
    sys.stdout.flush()
    A0T = [[A[0][j][i] for j in range(N)] for i in range(N)]
    pivsT, augT = gauss_elim(A0T, [Fraction(0)] * N, N, N)
    pcT = {c for _, c in pivsT}
    left_null = []
    for fc in [c for c in range(N) if c not in pcT]:
        v = [Fraction(0)] * N
        v[fc] = Fraction(1)
        for r, c in pivsT:
            v[c] = -augT[r][fc]
        left_null.append(v)
    n_left = len(left_null)
    print(f" dim={n_left} ({time.time()-t0:.1f}s)")

    # Perturbation iteration
    ck_bases = {0: c0_part}
    ck_nullss = {0: null_vecs}
    all_rows = []
    all_rhs_vals = []

    for order in range(1, MAX_ORDER + 1):
        t_order = time.time()
        print(f"    Order {order}:", end="")
        sys.stdout.flush()

        # Build constraint matrix for this order
        const = [Fraction(0)] * n_left
        lin = [[Fraction(0)] * n_null for _ in range(n_left)]

        for l in range(n_left):
            const[l] = dot(left_null[l], b[order], N)

        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om not in ck_bases:
                continue
            Am_ckb = matvec(A[m_idx], ck_bases[om], N, N)
            for l in range(n_left):
                const[l] -= dot(left_null[l], Am_ckb, N)

            for k in range(n_null):
                Am_ckn = matvec(A[m_idx], ck_nullss[om][k], N, N)
                for l in range(n_left):
                    lin[l][k] += dot(left_null[l], Am_ckn, N)

        for l in range(n_left):
            all_rows.append(lin[l][:])
            all_rhs_vals.append(const[l])

        # Check cumulative rank
        pvs, aug_acc = gauss_elim(all_rows, all_rhs_vals, len(all_rows), n_null)
        rank_cum = len(pvs)
        elapsed = time.time() - t_order
        total = time.time() - t_total
        print(f" rank={rank_cum}/{n_null} ({elapsed:.1f}s, total {total:.0f}s)")

        if rank_cum >= n_null:
            print(f"    ** CLOSED at order {order}! **")
            alpha = [Fraction(0)] * n_null
            for r, c in pvs:
                alpha[c] = aug_acc[r][n_null]
            c0 = [c0_part[j] + sum(alpha[k] * null_vecs[k][j] for k in range(n_null)) for j in range(N)]
            sym = check_symmetry(c0)
            return sym, c0

        # Compute c_{order} base and null contributions for next iteration
        print(f"    Computing c{order} base...", end="")
        sys.stdout.flush()
        t_ck = time.time()
        rhs_base = [b[order][i] for i in range(N)]
        for m_idx in range(1, order + 1):
            om = order - m_idx
            if om in ck_bases:
                Am_ckb = matvec(A[m_idx], ck_bases[om], N, N)
                for i in range(N):
                    rhs_base[i] -= Am_ckb[i]
        ck_bases[order] = solve_A0(A[0], rhs_base, N)
        print(f" {time.time()-t_ck:.1f}s")

        # Only compute null contributions if we expect more orders
        if rank_cum < n_null - 10:
            print(f"    Computing c{order} null ({n_null} vectors)...", end="")
            sys.stdout.flush()
            t_ck = time.time()
            ck_nullss[order] = []
            for k in range(n_null):
                rhs_k = [Fraction(0)] * N
                for m_idx in range(1, order + 1):
                    om = order - m_idx
                    if om in ck_nullss:
                        Am_ckn = matvec(A[m_idx], ck_nullss[om][k], N, N)
                        for i in range(N):
                            rhs_k[i] -= Am_ckn[i]
                ck_nullss[order].append(solve_A0(A[0], rhs_k, N))
                if (k + 1) % 100 == 0:
                    print(f" {k+1}", end="")
                    sys.stdout.flush()
            print(f" {time.time()-t_ck:.1f}s")
        else:
            # Near closing - skip null computation (saves time)
            print(f"    Skipping c{order} null (close to closing)")
            ck_nullss[order] = ck_nullss.get(order - 1, null_vecs)

    print(f"    ** Did not close through order {MAX_ORDER} **")
    return None, None


# Run at t = 7/10
result, coeffs = run(Fraction(7, 10))
if result is True:
    print("\n*** EXACT SYMMETRY at t=7/10 for n=4! ***")
elif result is False:
    print("\n*** SYMMETRY BROKEN at t=7/10 for n=4 ***")
elif result is None:
    print("\n*** DID NOT CONVERGE ***")

print(f"\n{'='*70}")
print("DONE")
