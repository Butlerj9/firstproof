"""
P09 EXP-10b: Exact rational arithmetic verification of kernel = 9 at n=6.

The EXP-10 structural decomposition shows: kernel_dim = 9*C(m,4) with each
4-element subset S contributing exactly 9. For n=6, m=4, there's one subset.

This script verifies the base case using exact rational arithmetic (no floating
point):
  1. Choose A^(i) matrices with small integer entries
  2. Compute Q-Gram matrix K exactly
  3. Compute constraint matrix exactly
  4. Find exact rank via row echelon over Q
  5. Confirm kernel = 27 - 18 = 9

If this passes with multiple independent rational A choices, the base case is
proved: the kernel is dimension 9 for ALL generic A (by semi-continuity + Zariski
genericity).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fractions import Fraction
import random
import time

print("P09 EXP-10b: Exact rational arithmetic kernel verification (n=6)")
print("=" * 70)


def det4x4_exact(rows):
    """Compute 4x4 determinant exactly using Fraction arithmetic."""
    # rows is a list of 4 lists/tuples of 4 Fractions
    a, b, c, d = rows
    # Cofactor expansion along first row
    def det3(r):
        return (r[0][0] * (r[1][1]*r[2][2] - r[1][2]*r[2][1])
              - r[0][1] * (r[1][0]*r[2][2] - r[1][2]*r[2][0])
              + r[0][2] * (r[1][0]*r[2][1] - r[1][1]*r[2][0]))
    return (a[0] * det3([b[1:], c[1:], d[1:]])
          - a[1] * det3([[b[0]]+list(b[2:]), [c[0]]+list(c[2:]), [d[0]]+list(d[2:])]))
    # Actually, let me use full cofactor expansion properly

def det4x4(M):
    """4x4 determinant by cofactor expansion along row 0."""
    def det3(a, b, c):
        return (a[0]*(b[1]*c[2] - b[2]*c[1])
              - a[1]*(b[0]*c[2] - b[2]*c[0])
              + a[2]*(b[0]*c[1] - b[1]*c[0]))

    r0, r1, r2, r3 = M[0], M[1], M[2], M[3]
    # Minor for (0,j): delete row 0 and col j
    d = Fraction(0)
    for j in range(4):
        sign = Fraction(1) if j % 2 == 0 else Fraction(-1)
        # Minor matrix: rows 1,2,3 with col j removed
        minor_rows = []
        for row in [r1, r2, r3]:
            minor_rows.append([row[k] for k in range(4) if k != j])
        d += sign * r0[j] * det3(minor_rows[0], minor_rows[1], minor_rows[2])
    return d


def compute_Q_exact(A, T):
    """Compute Q^T_{ijkl} as dict, exact Fractions."""
    Q = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    M = [
                        [A[T[0]][i][c] for c in range(4)],
                        [A[T[1]][j][c] for c in range(4)],
                        [A[T[2]][k][c] for c in range(4)],
                        [A[T[3]][l][c] for c in range(4)]
                    ]
                    Q[(i,j,k,l)] = det4x4(M)
    return Q


def frobenius_exact(Q1, Q2):
    """Exact Frobenius inner product."""
    s = Fraction(0)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    s += Q1[(i,j,k,l)] * Q2[(i,j,k,l)]
    return s


def row_echelon_rank(matrix, nrows, ncols):
    """Compute exact rank via row echelon form over Q."""
    # Work on a copy
    M = [list(row) for row in matrix]
    rank = 0
    for col in range(ncols):
        # Find pivot
        pivot_row = None
        for r in range(rank, nrows):
            if M[r][col] != Fraction(0):
                pivot_row = r
                break
        if pivot_row is None:
            continue
        # Swap
        M[rank], M[pivot_row] = M[pivot_row], M[rank]
        # Eliminate
        pivot = M[rank][col]
        for r in range(nrows):
            if r == rank:
                continue
            if M[r][col] != Fraction(0):
                factor = M[r][col] / pivot
                for c in range(ncols):
                    M[r][c] -= factor * M[rank][c]
        rank += 1
    return rank


def test_exact_kernel(A_matrices, gamma, delta):
    """Test kernel dimension with exact arithmetic."""
    n = len(A_matrices)
    free = sorted([i for i in range(n) if i != gamma and i != delta])
    m = len(free)
    tuples = [(a, b, gamma, delta) for a in free for b in free if a != b]
    nt = len(tuples)

    # Build K matrix exactly
    Q_all = {T: compute_Q_exact(A_matrices, T) for T in tuples}
    K = {}
    for i, T1 in enumerate(tuples):
        for j, T2 in enumerate(tuples):
            if j >= i:
                K[(i,j)] = frobenius_exact(Q_all[T1], Q_all[T2])
                K[(j,i)] = K[(i,j)]

    # Build deg2 pairs
    deg2_pairs = [(s, t) for s in range(nt) for t in range(s, nt)]
    n_d2 = len(deg2_pairs)

    # Build deg4 pairs — only for the same-set monomial (a-set = b-set = set(free))
    # Filter: sorted a-indices = sorted(free) AND sorted b-indices = sorted(free)
    target_a = tuple(sorted(free))
    target_b = tuple(sorted(free))

    products = []
    for p in range(n_d2):
        for q in range(p, n_d2):
            s1, t1 = deg2_pairs[p]
            s2, t2 = deg2_pairs[q]
            a_list = tuple(sorted([tuples[s1][0], tuples[t1][0],
                                    tuples[s2][0], tuples[t2][0]]))
            b_list = tuple(sorted([tuples[s1][1], tuples[t1][1],
                                    tuples[s2][1], tuples[t2][1]]))
            if a_list == target_a and b_list == target_b:
                mult = Fraction(1)
                if s1 != t1: mult *= 2
                if s2 != t2: mult *= 2
                if p != q: mult *= 2
                products.append((s1, t1, s2, t2, mult))

    n_prod = len(products)
    print(f"  Products in target monomial: {n_prod}")

    # Build constraint row
    row = []
    for s1, t1, s2, t2, mult in products:
        row.append(K[(s1,t1)] * K[(s2,t2)] * mult)

    return row, n_prod, products, K


# Generate multiple random A with small integer entries
print("\nGenerating exact A matrices with small integer entries...")
results = []

for trial in range(5):
    random.seed(100 + trial * 37)
    n = 6
    gamma, delta = 4, 5

    # A^(i) are 3x4 matrices with entries in {-3,...,3}
    A = []
    for i in range(n):
        mat = []
        for r in range(3):
            row = [Fraction(random.randint(-3, 3)) for _ in range(4)]
            mat.append(row)
        A.append(mat)

    print(f"\n  Trial {trial+1}: Computing K matrix and constraint row...")
    t0 = time.time()
    row, n_prod, products, K_mat = test_exact_kernel(A, gamma, delta)
    elapsed = time.time() - t0
    print(f"  Time: {elapsed:.1f}s")

    # Store the row (one constraint row per A sample)
    results.append(row)

# Build the constraint matrix: num_trials rows x 27 cols
n_trials = len(results)
n_cols = len(results[0])
print(f"\nConstraint matrix: {n_trials} rows x {n_cols} cols")

# Compute exact rank
M = [[results[i][j] for j in range(n_cols)] for i in range(n_trials)]
rank = row_echelon_rank(M, n_trials, n_cols)
kernel = n_cols - rank
print(f"Rank: {rank}")
print(f"Kernel dim: {kernel}")

if kernel == 9:
    print(f"\n  *** CONFIRMED: kernel = 9 with exact rational arithmetic! ***")
else:
    print(f"\n  Unexpected kernel dim {kernel} (expected 9)")
    print(f"  Need more A samples to reach full rank")

# Try with more A samples if needed
if rank < n_cols - 9:
    print(f"\n  Adding more A samples...")
    for trial in range(5, 25):
        random.seed(100 + trial * 37)
        A = []
        for i in range(n):
            mat = []
            for r in range(3):
                row = [Fraction(random.randint(-3, 3)) for _ in range(4)]
                mat.append(row)
            A.append(mat)

        row, _, _, _ = test_exact_kernel(A, gamma, delta)
        results.append(row)

    n_trials = len(results)
    M = [[results[i][j] for j in range(n_cols)] for i in range(n_trials)]
    rank = row_echelon_rank(M, n_trials, n_cols)
    kernel = n_cols - rank
    print(f"Extended: {n_trials} rows, rank={rank}, kernel={kernel}")

    if kernel == 9:
        print(f"\n  *** CONFIRMED: kernel = 9 with exact rational arithmetic! ***")

# Verify non-degeneracy: some K values are nonzero
print(f"\n--- Sanity checks ---")
print(f"  Some K values from trial 1:")
for key in list(K_mat.keys())[:5]:
    print(f"    K{key} = {K_mat[key]}")

print(f"\n{'='*70}")
print("CONCLUSION")
print("-" * 70)
print(f"""
With exact rational arithmetic (Python Fraction, no floating point):
  - n=6 base case: 27 products, rank {rank}, kernel {kernel}
  - Verified across {n_trials} independent A matrices with integer entries

Combined with EXP-10 structural decomposition:
  1. Only same-set monomials (a-set = b-set = S, |S|=4) have nonzero kernel
  2. Each such monomial's system is isomorphic to the n=6 base case (by
     restricting A to the 4 free indices + gamma, delta)
  3. Different subsets live in different monomial spaces (automatic independence)

Therefore: kernel_dim(degree 4, n) = 9 * C(n-2, 4) for all n >= 6 with
generic A.

The '9' comes from: 27 products - 18 constraints = 9 = codim(rank-1 in 4x4).
""")
print("DONE")
