"""
P09 EXP-7: D_n masking analysis — why degree-4 fails at n=5.

Key structural insight:
For fixed (gamma0, delta0), the (a,b)-block has entries M_{a,b} = u_a * v_b
for a,b in [n] \ {gamma0, delta0}, a != b. This is an m x m matrix (m = n-2)
with the DIAGONAL REMOVED.

Rank-1 detection via 2x2 minors requires entries M_{a1,b1}, M_{a1,b2},
M_{a2,b1}, M_{a2,b2} with all four being off-diagonal (a_i != b_j for all i,j).
This is only possible when m >= 4 (n >= 6).

At m = 3 (n = 5): NO 2x2 minor can be formed from off-diagonal entries alone.
This explains the degree-4 failure at n=5 and the need for degree-6.
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("P09 EXP-7: Masking analysis for D_n diagonal removal")
print("=" * 70)

# Verify: for m x m matrix with diagonal removed, count valid 2x2 minors
# A valid 2x2 minor uses rows {r1, r2} and columns {c1, c2}
# with r_i != c_j for ALL i, j (so all 4 entries are off-diagonal)

for m in range(2, 8):
    n = m + 2
    count = 0
    examples = []
    for r1 in range(m):
        for r2 in range(r1+1, m):
            for c1 in range(m):
                for c2 in range(c1+1, m):
                    # Check: all 4 entries off-diagonal
                    ok = True
                    for ri in [r1, r2]:
                        for ci in [c1, c2]:
                            if ri == ci:
                                ok = False
                    if ok:
                        count += 1
                        if len(examples) < 2:
                            examples.append(((r1, r2), (c1, c2)))
    print(f"  m={m} (n={n}): {count} valid off-diagonal 2x2 minors", end="")
    if count == 0:
        print(f"  ** NO RANK-1 DETECTION VIA 2x2 MINORS **")
    else:
        print(f"  (examples: {examples[:2]})")

# Explain the implication
print()
print("Implication:")
print("  n=5 (m=3): Cannot form any 2x2 off-diagonal minor.")
print("    => Degree-4 Frobenius products (= K-weighted 2x2 minors) have trivial kernel.")
print("    => Need degree-6 (K-weighted 3x3 off-diagonal determinant conditions).")
print()
print("  n>=6 (m>=4): Off-diagonal 2x2 minors exist and detect rank-1.")
print("    => Degree-4 Frobenius products suffice (9-dim kernel at n=6).")

# Verify: the codimension of rank-1 matrices in off-diagonal entries
# For m x m rank-1 matrix M = u * v^T:
#   Parameters: m (for u) + m (for v) - 1 (scaling) = 2m - 1
#   Ambient (off-diagonal): m^2 - m = m(m-1)
#   Codimension: m(m-1) - (2m-1) = m^2 - 3m + 1

print()
print("Codimension of rank-1 in off-diagonal entries:")
for m in range(3, 8):
    n = m + 2
    ambient = m * (m - 1)
    param = 2 * m - 1
    codim = ambient - param
    # Number of independent 2x2 minors needed
    print(f"  m={m} (n={n}): ambient={ambient}, rank-1 dim={param}, codim={codim}")

# Compare with kernel dimensions found in experiments
print()
print("Comparison with experimental kernel dimensions:")
print("  n=5 (m=3): EXP-6 deg-4 kernel = 0    (codim in off-diag = 1, but no 2x2 minors!)")
print("  n=5 (m=3): EXP-6e deg-6 kernel = 15   (3x3 det-based conditions)")
print("  n=6 (m=4): EXP-5b deg-4 kernel = 9    (2x2 minors available)")
print(f"    Predicted codim at m=4: {4*3 - 7} = 5... but kernel=9. Discrepancy!")
print(f"    NOTE: kernel dim counts Frobenius-product coefficient vectors,")
print(f"    not the minors directly. The 9-dim kernel in a 3081-dim space")
print(f"    reflects the polynomial structure, not just matrix codimension.")

print(f"\n{'='*70}")
print("DONE")
