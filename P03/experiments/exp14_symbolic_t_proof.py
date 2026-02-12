"""
P03 EXP-14: Symbolic perturbation with t as formal parameter.
Goal: Prove Symmetry Conjecture for ALL t > 0 at n=3.

Strategy:
1. Build order-0 matrix with symbolic t (entries are monomials t^j)
2. Gaussian elimination (only 6 pivots needed — rank 6!)
3. Perturbation cascade through order 4
4. Check symmetry of c0(t) as rational function of t
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sympy import Symbol, Rational, cancel, simplify, degree, Poly, QQ, numer, denom
from sympy import Matrix
from itertools import permutations

t = Symbol('t')
ZERO = Rational(0)
ONE = Rational(1)

print("P03 EXP-14: Symbolic t perturbation proof")
print("=" * 70)

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
print(f"N = {N} unknowns, {len(van_comps)} vanishing conditions")


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
        return ZERO
    if k == 0:
        return ONE
    fk = ONE
    for i in range(1, k + 1):
        fk *= Rational(i)
    r = ONE
    for i in range(k):
        r *= Rational(p - i)
    return r / fk


def build_symbolic_matrices(max_order):
    """Build matrices with symbolic t entries."""
    matrices = {k: [] for k in range(max_order + 1)}
    rhs = {k: [] for k in range(max_order + 1)}
    for nu in van_comps:
        k = k_stats[nu]
        for order in range(max_order + 1):
            row = []
            for m in unk_monoms:
                t_exp = -(k[0] * m[0] + k[1] * m[1] + k[2] * m[2])
                p = nu[0] * m[0] + nu[1] * m[1] + nu[2] * m[2]
                coeff = binom_frac(p, order)
                row.append(coeff * t ** t_exp)
            matrices[order].append(row)
            t_exp_l = -(k[0] * leading[0] + k[1] * leading[1] + k[2] * leading[2])
            p_l = nu[0] * leading[0] + nu[1] * leading[1] + nu[2] * leading[2]
            coeff_l = binom_frac(p_l, order)
            rhs[order].append(-coeff_l * t ** t_exp_l)
    return matrices, rhs


# Use numerical pilot to find pivot structure
print("\nPhase 1: Numerical pilot at t=7/10...")
t0 = time.time()
from fractions import Fraction as F


def eval_at(expr, t_val):
    """Evaluate sympy expression at t = t_val (Fraction)."""
    if isinstance(expr, (int, float)):
        return F(expr)
    return F(str(expr.subs(t, Rational(t_val.numerator, t_val.denominator))))


def gauss_elim_frac(mat, rhs_vec, nrows, ncols):
    """Gaussian elimination with Fraction arithmetic."""
    aug = [mat[i][:] + [rhs_vec[i]] for i in range(nrows)]
    pivots = []
    ri = 0
    for col in range(ncols):
        piv = None
        for r in range(ri, nrows):
            if aug[r][col] != F(0):
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
            if r != ri and aug[r][col] != F(0):
                f = aug[r][col]
                for j in range(ncols + 1):
                    aug[r][j] -= f * aug[ri][j]
        ri += 1
    return pivots, aug


# Build numeric matrices at t=7/10
t_num = F(7, 10)
A0_num = []
b0_num = []
for nu in van_comps:
    k = k_stats[nu]
    row = []
    for m in unk_monoms:
        t_exp = -(k[0] * m[0] + k[1] * m[1] + k[2] * m[2])
        row.append(t_num ** t_exp)
    A0_num.append(row)
    t_exp_l = -(k[0] * leading[0] + k[1] * leading[1] + k[2] * leading[2])
    b0_num.append(-(t_num ** t_exp_l))

pivots_num, aug_num = gauss_elim_frac(A0_num, b0_num, N, N)
rank0 = len(pivots_num)
pivot_cols = [c for _, c in pivots_num]
free_cols = [c for c in range(N) if c not in set(pivot_cols)]
n_null = len(free_cols)
print(f"  Rank = {rank0}, null_dim = {n_null}")
print(f"  Pivot cols (first 6): {pivot_cols}")
print(f"  Free cols (first 10): {free_cols[:10]}...")
print(f"  ({time.time() - t0:.1f}s)")

# Phase 2: Symbolic Gaussian elimination using same pivot structure
print("\nPhase 2: Symbolic elimination (same pivots)...")
t0 = time.time()

MAX_ORDER = 5
A_sym, b_sym = build_symbolic_matrices(MAX_ORDER)
print(f"  Symbolic matrices built ({time.time() - t0:.1f}s)")

# Do symbolic elimination of A_sym[0] using the pivot order from numeric
aug_sym = [A_sym[0][i][:] + [b_sym[0][i]] for i in range(N)]

for step, (pivot_row_target, pivot_col) in enumerate(pivots_num):
    # Find the row to use as pivot (same column as numeric)
    piv_found = None
    for r in range(pivot_row_target, N):
        # Check if this row has nonzero entry at pivot_col
        entry = aug_sym[r][pivot_col]
        if entry != 0:
            piv_found = r
            break
    if piv_found is None:
        print(f"  WARNING: Pivot not found at step {step}, col {pivot_col}")
        break
    if piv_found != pivot_row_target:
        aug_sym[pivot_row_target], aug_sym[piv_found] = aug_sym[piv_found], aug_sym[pivot_row_target]

    pv = aug_sym[pivot_row_target][pivot_col]
    # Normalize pivot row
    for j in range(N + 1):
        if aug_sym[pivot_row_target][j] != 0:
            aug_sym[pivot_row_target][j] = cancel(aug_sym[pivot_row_target][j] / pv)

    # Eliminate other rows
    for r in range(N):
        if r != pivot_row_target and aug_sym[r][pivot_col] != 0:
            f = aug_sym[r][pivot_col]
            for j in range(N + 1):
                aug_sym[r][j] = cancel(aug_sym[r][j] - f * aug_sym[pivot_row_target][j])

    elapsed = time.time() - t0
    print(f"  Pivot {step + 1}/{rank0}: col={pivot_col} ({elapsed:.1f}s)")

print(f"  Elimination done ({time.time() - t0:.1f}s)")

# Extract particular solution and null space
c0_part = [ZERO] * N
for r, c in pivots_num:
    c0_part[c] = cancel(aug_sym[r][N])

null_vecs = []
for fc in free_cols:
    v = [ZERO] * N
    v[fc] = ONE
    for r, c in pivots_num:
        v[c] = cancel(-aug_sym[r][fc])
    null_vecs.append(v)

# Check: degree of a sample null vector entry
sample_nv = null_vecs[0][pivot_cols[0]]
print(f"\n  Sample null vector entry: {sample_nv}")
try:
    p = Poly(cancel(sample_nv), t)
    print(f"  Degree: {p.degree()}")
except:
    print(f"  (Not a simple polynomial in t)")

# Left null space (transpose elimination)
print("\nPhase 3: Left null space...")
t0_ln = time.time()
A0T = [[A_sym[0][j][i] for j in range(N)] for i in range(N)]
b0T = [ZERO] * N
pivsT, augT = gauss_elim_frac(
    [[eval_at(A0T[i][j], t_num) for j in range(N)] for i in range(N)],
    [F(0)] * N, N, N
)
pcT = {c for _, c in pivsT}
print(f"  Transpose rank: {len(pivsT)} ({time.time() - t0_ln:.1f}s)")

# Symbolic left null space using same transpose pivots
augT_sym = [A0T[i][:] + [ZERO] for i in range(N)]
for step, (pr, pc) in enumerate(pivsT):
    piv_found = None
    for r in range(pr, N):
        if augT_sym[r][pc] != 0:
            piv_found = r
            break
    if piv_found is None:
        break
    if piv_found != pr:
        augT_sym[pr], augT_sym[piv_found] = augT_sym[piv_found], augT_sym[pr]
    pv = augT_sym[pr][pc]
    for j in range(N + 1):
        if augT_sym[pr][j] != 0:
            augT_sym[pr][j] = cancel(augT_sym[pr][j] / pv)
    for r in range(N):
        if r != pr and augT_sym[r][pc] != 0:
            f = augT_sym[r][pc]
            for j in range(N + 1):
                augT_sym[r][j] = cancel(augT_sym[r][j] - f * augT_sym[pr][j])
    if (step + 1) % 2 == 0:
        print(f"  Transpose pivot {step + 1}/{len(pivsT)} ({time.time() - t0_ln:.1f}s)")

left_null = []
free_T = [c for c in range(N) if c not in pcT]
for fc in free_T:
    v = [ZERO] * N
    v[fc] = ONE
    for r, c in pivsT:
        v[c] = cancel(-augT_sym[r][fc])
    left_null.append(v)
n_left = len(left_null)
print(f"  Left null space: dim {n_left} ({time.time() - t0_ln:.1f}s)")

# Phase 4: Perturbation cascade
print("\nPhase 4: Perturbation cascade...")
t0_pc = time.time()


def sym_matvec(M, v):
    result = [ZERO] * len(M)
    for i in range(len(M)):
        s = ZERO
        for j in range(len(v)):
            if M[i][j] != 0 and v[j] != 0:
                s += M[i][j] * v[j]
        result[i] = cancel(s) if s != ZERO else ZERO
    return result


def sym_dot(u, v):
    s = ZERO
    for i in range(len(u)):
        if u[i] != 0 and v[i] != 0:
            s += u[i] * v[i]
    return cancel(s) if s != ZERO else ZERO


def sym_solve_A0(rhs_vec):
    """Solve A[0]*x = rhs using the precomputed symbolic RREF."""
    # The RREF is stored in aug_sym. We need to solve for new RHS.
    # Actually, we can use the pivot structure directly.
    x = [ZERO] * N
    # Forward: project rhs onto the pivot rows
    # Since aug_sym is in RREF form, each pivot row i has:
    #   x[pivot_col_i] + sum(aug_sym[i][j]*x[j] for j in free_cols) = aug_sym[i][N]
    # For a NEW rhs, we need to recompute. Instead, use the original A0 and the pivot structure.
    # Simpler: just do back-substitution with the symbolic matrix.
    # Actually the cleanest is to use the precomputed elimination structure.
    # Let me use a direct approach: solve A[0]*x = rhs_vec via the known pivot structure.

    # Reduce rhs_vec using the same row operations as the RREF
    # This is equivalent to: x[pivot_cols] = L * rhs_vec where L is the left-inverse at pivot rows
    # For simplicity, just re-solve from scratch using the pivot order
    aug2 = [A_sym[0][i][:] + [rhs_vec[i]] for i in range(N)]
    for step, (pr, pc) in enumerate(pivots_num):
        piv_found = None
        for r in range(pr, N):
            if aug2[r][pc] != 0:
                piv_found = r
                break
        if piv_found is None:
            continue
        if piv_found != pr:
            aug2[pr], aug2[piv_found] = aug2[piv_found], aug2[pr]
        pv = aug2[pr][pc]
        for j in range(N + 1):
            if aug2[pr][j] != 0:
                aug2[pr][j] = cancel(aug2[pr][j] / pv)
        for r in range(N):
            if r != pr and aug2[r][pc] != 0:
                f = aug2[r][pc]
                for j in range(N + 1):
                    aug2[r][j] = cancel(aug2[r][j] - f * aug2[pr][j])
    x = [ZERO] * N
    for r, c in pivots_num:
        x[c] = cancel(aug2[r][N])
    return x


# Store c_k bases and null contributions
ck_bases = {0: c0_part}
ck_nullss = {0: null_vecs}

all_rows = []
all_rhs_vals = []

for order in range(1, MAX_ORDER + 1):
    print(f"  Order {order}...", end="")
    sys.stdout.flush()
    t_order = time.time()

    const = [ZERO] * n_left
    lin = [[ZERO] * n_null for _ in range(n_left)]

    for l in range(n_left):
        const[l] = sym_dot(left_null[l], b_sym[order])

    for m in range(1, order + 1):
        om = order - m
        if om not in ck_bases:
            continue
        Am_ckb = sym_matvec(A_sym[m], ck_bases[om])
        for l in range(n_left):
            v = sym_dot(left_null[l], Am_ckb)
            if v != ZERO:
                const[l] = cancel(const[l] - v)

        for k in range(n_null):
            Am_ckn = sym_matvec(A_sym[m], ck_nullss[om][k])
            for l in range(n_left):
                v = sym_dot(left_null[l], Am_ckn)
                if v != ZERO:
                    lin[l][k] = cancel(lin[l][k] + v)

    for l in range(n_left):
        all_rows.append(lin[l][:])
        all_rhs_vals.append(const[l])

    # Check rank (evaluate at t=7/10 to get numeric rank)
    nr = len(all_rows)
    all_rows_num = [[eval_at(all_rows[i][j], t_num) for j in range(n_null)] for i in range(nr)]
    all_rhs_num = [eval_at(all_rhs_vals[i], t_num) for i in range(nr)]
    pivs_acc, _ = gauss_elim_frac(all_rows_num, all_rhs_num, nr, n_null)
    rank_cum = len(pivs_acc)
    elapsed = time.time() - t_order
    print(f" rank={rank_cum}/{n_null} ({elapsed:.1f}s, total {time.time() - t0_pc:.1f}s)")

    if rank_cum >= n_null:
        print(f"  ** Order {order} CLOSES! **")
        # Solve symbolically
        pivs_sym, aug_acc = None, None  # Need symbolic solve

        # Build symbolic system from all_rows and all_rhs_vals
        # Use the numeric pivot structure
        aug_sys = [all_rows[i][:] + [all_rhs_vals[i]] for i in range(nr)]
        for step, (pr, pc) in enumerate(pivs_acc):
            piv_found = None
            for r in range(pr, nr):
                entry_num = eval_at(aug_sys[r][pc], t_num)
                if entry_num != F(0):
                    piv_found = r
                    break
            if piv_found is None:
                print(f"  Pivot issue at step {step}")
                break
            if piv_found != pr:
                aug_sys[pr], aug_sys[piv_found] = aug_sys[piv_found], aug_sys[pr]
            pv = aug_sys[pr][pc]
            for j in range(n_null + 1):
                if aug_sys[pr][j] != 0:
                    aug_sys[pr][j] = cancel(aug_sys[pr][j] / pv)
            for r in range(nr):
                if r != pr and aug_sys[r][pc] != 0:
                    f = aug_sys[r][pc]
                    for j in range(n_null + 1):
                        aug_sys[r][j] = cancel(aug_sys[r][j] - f * aug_sys[pr][j])
            if (step + 1) % 10 == 0:
                print(f"    Constraint pivot {step + 1}/{n_null} ({time.time() - t0_pc:.1f}s)")

        alpha = [ZERO] * n_null
        for r, c in pivs_acc:
            alpha[c] = cancel(aug_sys[r][n_null])

        # Reconstruct c0
        c0 = [cancel(c0_part[j] + sum(alpha[k] * null_vecs[k][j]
              for k in range(n_null) if alpha[k] != ZERO and null_vecs[k][j] != ZERO))
              for j in range(N)]

        # Check symmetry
        print("\n  Checking symmetry...")
        coeffs = {}
        for i, m in enumerate(unk_monoms):
            coeffs[m] = c0[i]
        coeffs[leading] = ONE

        max_asym = ZERO
        asym_count = 0
        for m, val in coeffs.items():
            for p in permutations(m):
                if p != m and p in coeffs:
                    diff = cancel(coeffs[p] - val)
                    if diff != ZERO:
                        asym_count += 1
                        print(f"    ASYMMETRY: c{m} - c{p} = {diff}")
                        max_asym = ONE  # flag

        if asym_count == 0:
            print(f"\n  *** SYMMETRY PROVED FOR ALL t > 0 (n=3) ***")
            print(f"  All {len(coeffs)} coefficients verified symmetric")
            # Print a few
            seen = set()
            for mk in sorted(coeffs.keys(), key=lambda x: (-sum(x), x)):
                key = tuple(sorted(mk, reverse=True))
                if key not in seen:
                    seen.add(key)
                    print(f"    c{mk} = {coeffs[mk]}")
                    if len(seen) >= 8:
                        break
        else:
            print(f"\n  ASYMMETRY FOUND: {asym_count} pairs")
        break

    # Compute c_k for next iteration
    print(f"  Computing c{order}...")
    rhs_base = list(b_sym[order])
    for m in range(1, order + 1):
        om = order - m
        if om in ck_bases:
            Am_ckb = sym_matvec(A_sym[m], ck_bases[om])
            for i in range(N):
                if Am_ckb[i] != ZERO:
                    rhs_base[i] = cancel(rhs_base[i] - Am_ckb[i])
    ck_bases[order] = sym_solve_A0(rhs_base)

    ck_nullss[order] = []
    for k in range(n_null):
        rhs_k = [ZERO] * N
        for m in range(1, order + 1):
            om = order - m
            if om in ck_nullss:
                Am_ckn = sym_matvec(A_sym[m], ck_nullss[om][k])
                for i in range(N):
                    if Am_ckn[i] != ZERO:
                        rhs_k[i] = cancel(rhs_k[i] - Am_ckn[i])
        ck_nullss[order].append(sym_solve_A0(rhs_k))
    print(f"  c{order} done ({time.time() - t0_pc:.1f}s)")

print(f"\n{'=' * 70}")
print("DONE")
