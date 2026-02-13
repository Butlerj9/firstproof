"""
ce29b_fast_polynomial.py — Fast numerical sign test of P on validity domain and all R^5.

Uses numpy vectorized evaluation instead of SymPy substitution.
P = Dh*(A1*B1)*(A2*B2) - D1*(Ah*Bh)*(A2*B2) - D2*(Ah*Bh)*(A1*B1)
"""
import sys, io, time
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def compute_ABDelta(sigma, b, cp):
    """Compute A, B, Delta for quartic x^4 + ax^2 + bx + c with a=-sigma, c=sigma^2/12+cp."""
    a = -sigma
    c = sigma**2 / 12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    return A, B, Delta

def compute_P(w, b1, b2, cp1, cp2):
    """Compute polynomial P = Dh*(A1B1)(A2B2) - D1*(AhBh)(A2B2) - D2*(AhBh)(A1B1)."""
    s1, s2 = w, 1.0 - w
    A1, B1, D1 = compute_ABDelta(s1, b1, cp1)
    A2, B2, D2 = compute_ABDelta(s2, b2, cp2)
    Ah, Bh, Dh = compute_ABDelta(1.0, b1+b2, cp1+cp2)

    AB1 = A1 * B1
    AB2 = A2 * B2
    ABh = Ah * Bh

    P = Dh * AB1 * AB2 - D1 * ABh * AB2 - D2 * ABh * AB1
    return P, A1, B1, D1, A2, B2, D2, Ah, Bh, Dh

# ============================================================
print(SEP)
print("SECTION 1: Sign of P on validity domain (500K tests)")
print(SEP)

np.random.seed(42)
N = 500000

w_arr = np.random.uniform(0.05, 0.95, N)
b1_arr = np.random.uniform(-0.5, 0.5, N)
b2_arr = np.random.uniform(-0.5, 0.5, N)
cp1_arr = np.random.uniform(-0.1, 0.1, N)
cp2_arr = np.random.uniform(-0.1, 0.1, N)

P_arr, A1, B1, D1, A2, B2, D2, Ah, Bh, Dh = compute_P(
    w_arr, b1_arr, b2_arr, cp1_arr, cp2_arr)

# Validity mask
valid = ((D1 > 0) & (D2 > 0) & (Dh > 0) &
         (A1*B1 < 0) & (A2*B2 < 0) & (Ah*Bh < 0))

n_valid = valid.sum()
P_valid = P_arr[valid]
n_valid_neg = (P_valid < -1e-8).sum()

print("Total tested: %d" % N)
print("On validity domain: %d (%.1f%%)" % (n_valid, 100.0*n_valid/N))
print("P < 0 on validity domain: %d" % n_valid_neg)
if n_valid > 0:
    print("Min P (valid): %.6e" % P_valid.min())
    print("Max P (valid): %.6e" % P_valid.max())
    print("Mean P (valid): %.6e" % P_valid.mean())
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Sign of P on ALL of R^5 (500K tests)")
print(SEP)

n_all_neg = (P_arr < -1e-8).sum()
print("P < 0 anywhere: %d (%.2f%%)" % (n_all_neg, 100.0*n_all_neg/N))
print("Min P (all): %.6e" % P_arr.min())

if n_all_neg > 0:
    # Find the worst case
    idx = P_arr.argmin()
    print("Worst: w=%.4f b1=%.4f b2=%.4f cp1=%.5f cp2=%.5f P=%.4e" %
          (w_arr[idx], b1_arr[idx], b2_arr[idx], cp1_arr[idx], cp2_arr[idx], P_arr[idx]))
    print("  Validity: D1=%.4e D2=%.4e Dh=%.4e A1B1=%.4e A2B2=%.4e AhBh=%.4e" %
          (D1[idx], D2[idx], Dh[idx], A1[idx]*B1[idx], A2[idx]*B2[idx], Ah[idx]*Bh[idx]))
    print("P >= 0 everywhere: False")
    print("=> CONSTRAINED SOS needed (P negative outside validity domain)")
else:
    print("P >= 0 everywhere: True")
    print("=> UNCONSTRAINED SOS feasible!")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Wider range test (b, cp up to ±2)")
print(SEP)

np.random.seed(123)
w2 = np.random.uniform(0.01, 0.99, N)
b1_2 = np.random.uniform(-2, 2, N)
b2_2 = np.random.uniform(-2, 2, N)
cp1_2 = np.random.uniform(-1, 1, N)
cp2_2 = np.random.uniform(-1, 1, N)

P2, A12, B12, D12, A22, B22, D22, Ah2, Bh2, Dh2 = compute_P(
    w2, b1_2, b2_2, cp1_2, cp2_2)

valid2 = ((D12 > 0) & (D22 > 0) & (Dh2 > 0) &
          (A12*B12 < 0) & (A22*B22 < 0) & (Ah2*Bh2 < 0))

n_valid2 = valid2.sum()
if n_valid2 > 0:
    P_valid2 = P2[valid2]
    n_neg2 = (P_valid2 < -1e-8).sum()
    print("Validity domain points: %d" % n_valid2)
    print("P < 0: %d" % n_neg2)
    print("Min P (valid): %.6e" % P_valid2.min())
else:
    print("No points in validity domain at this scale")

n_all_neg2 = (P2 < -1e-8).sum()
print("P < 0 anywhere (wide): %d (%.2f%%)" % (n_all_neg2, 100.0*n_all_neg2/N))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Stress test near b=0 (where P should be smallest)")
print(SEP)

np.random.seed(456)
N2 = 500000
w3 = np.random.uniform(0.05, 0.95, N2)
# Near b=0 boundary (where M is smallest)
s1_3 = w3
s2_3 = 1.0 - w3
b1_max = np.sqrt(4*s1_3**3/27) * 0.99
b2_max = np.sqrt(4*s2_3**3/27) * 0.99
b1_3 = np.random.uniform(-1, 1, N2) * b1_max
b2_3 = np.random.uniform(-1, 1, N2) * b2_max
cp1_3 = np.random.uniform(-0.08, 0.08, N2)
cp2_3 = np.random.uniform(-0.08, 0.08, N2)

P3, A13, B13, D13, A23, B23, D23, Ah3, Bh3, Dh3 = compute_P(
    w3, b1_3, b2_3, cp1_3, cp2_3)

valid3 = ((D13 > 0) & (D23 > 0) & (Dh3 > 0) &
          (A13*B13 < 0) & (A23*B23 < 0) & (Ah3*Bh3 < 0))

n_valid3 = valid3.sum()
if n_valid3 > 0:
    P_valid3 = P3[valid3]
    n_neg3 = (P_valid3 < -1e-8).sum()
    print("Validity domain (stress): %d" % n_valid3)
    print("P < 0: %d" % n_neg3)
    print("Min P (valid, stress): %.6e" % P_valid3.min())
    # Also check where P is smallest
    if n_neg3 == 0:
        # Find the smallest P on validity domain
        idx = P_valid3.argmin()
        valid_indices = np.where(valid3)[0]
        j = valid_indices[idx]
        print("Smallest P case: w=%.4f b1=%.6f b2=%.6f cp1=%.6f cp2=%.6f" %
              (w3[j], b1_3[j], b2_3[j], cp1_3[j], cp2_3[j]))
        print("  P=%.6e" % P_valid3[idx])
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Denominator sign analysis")
print(SEP)
print("On validity domain, D = (AhBh)(A1B1)(A2B2)")
print("Each AiBi < 0, so D = (-)(-)(-) = -1 < 0")
print("M = P / (4*D), so M >= 0 iff P <= 0 ... wait")

# Let me recheck the sign carefully
# 1/Phi4 = -Delta/(4*A*B)
# M = 1/Phi4_h - 1/Phi4_1 - 1/Phi4_2
#   = -Dh/(4*AhBh) + D1/(4*A1B1) + D2/(4*A2B2)
#
# Common denom = 4*(AhBh)(A1B1)(A2B2) = 4*D < 0
#
# Numerator = -Dh*(A1B1)(A2B2) + D1*(AhBh)(A2B2) + D2*(AhBh)(A1B1)
#           = -(Dh*(A1B1)(A2B2) - D1*(AhBh)(A2B2) - D2*(AhBh)(A1B1))
#           = -P
#
# M = -P / (4*D)
# D < 0, so -P/(4*D) = P/(4*|D|)
# Wait: D < 0, so 4*D < 0, so -P/(4*D) = P/(-4*D) = P/(4|D|)
# So M = P/(4|D|)
# M >= 0 iff P >= 0

# Verify numerically
M_direct = np.zeros(N)
valid_mask = valid.copy()
for i in range(min(1000, N)):
    if not valid[i]:
        continue
    f_h = -Dh[i] / (4.0 * Ah[i] * Bh[i])
    f_1 = -D1[i] / (4.0 * A1[i] * B1[i])
    f_2 = -D2[i] / (4.0 * A2[i] * B2[i])
    M_direct[i] = f_h - f_1 - f_2

# Check P and M_direct have same sign
n_check = 0
n_agree = 0
for i in range(min(1000, N)):
    if not valid[i]:
        continue
    n_check += 1
    denom = 4.0 * Ah[i] * Bh[i] * A1[i] * B1[i] * A2[i] * B2[i]
    M_from_P = P_arr[i] / abs(denom) if denom < 0 else -P_arr[i] / abs(denom)
    if (M_direct[i] >= 0) == (P_arr[i] >= 0):
        n_agree += 1

print("Sign agreement check (first 1000 valid): %d/%d agree" % (n_agree, n_check))

# So P >= 0 on validity domain iff M >= 0
print("\nConclusion: P >= 0 on validity domain <=> M >= 0 (superadditivity)")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("VERDICT")
print(SEP)
total_valid_neg = n_valid_neg
if n_valid2 > 0:
    total_valid_neg += n_neg2
if n_valid3 > 0:
    total_valid_neg += n_neg3

if total_valid_neg == 0:
    print("P >= 0 on validity domain: CONFIRMED (%.1fM tests)" %
          ((n_valid + (n_valid2 if n_valid2 > 0 else 0) + (n_valid3 if n_valid3 > 0 else 0)) / 1e6))
    if n_all_neg == 0:
        print("P >= 0 everywhere: YES -> unconstrained SOS attempt viable!")
    else:
        print("P < 0 outside validity domain: YES -> constrained SOS needed")
        print("  %d violations in %d tests" % (n_all_neg, N))
else:
    print("WARNING: P < 0 found on validity domain!")

print("\nPolynomial stats: 837 terms, degree 14, 5 variables")
print("Elapsed: %.1fs" % (time.time() - t0))
