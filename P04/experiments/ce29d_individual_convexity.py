"""
ce29d_individual_convexity.py — Test if each 1/Phi4(sigma, b, c') is convex in c'.

If f(c') = 1/Phi4(sigma, b, c') is convex in c' for each polynomial,
this would be a key ingredient for proving the discriminant condition.

Also: compute exact symbolic M'(0) and M''(0) to understand the discriminant
condition algebraically.
"""
import sys, io, time
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def phi4_inv(sigma, b, cp):
    a = -sigma
    c = sigma**2 / 12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    if Delta <= 0 or A * B >= 0:
        return None, False
    val = -Delta / (4.0 * A * B)
    return val, val > 0

# ============================================================
print(SEP)
print("SECTION 1: Convexity of 1/Phi4(sigma, b, c') in c'")
print(SEP)

h = 1e-6
np.random.seed(42)
n_tested = 0
n_violations = 0
min_d2 = float('inf')

for _ in range(200000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.95
    b = np.random.uniform(-b_max, b_max)
    cp = np.random.uniform(-0.1, 0.1)

    f0, ok0 = phi4_inv(sigma, b, cp)
    fp, okp = phi4_inv(sigma, b, cp + h)
    fm, okm = phi4_inv(sigma, b, cp - h)

    if not (ok0 and okp and okm):
        continue

    n_tested += 1
    d2 = (fp - 2*f0 + fm) / h**2

    if d2 < min_d2:
        min_d2 = d2

    if d2 < -1e-3:
        n_violations += 1

print("Individual f(c') convexity tests: %d" % n_tested)
print("Violations (d²f/dc'² < -1e-3): %d" % n_violations)
print("Min d²f/dc'²: %.6e" % min_d2)
print("Individual 1/Phi4 convex in c': %s" % (n_violations == 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Concavity of 1/Phi4(sigma, b, c') in c'?")
print(SEP)

n_concave_viol = 0
max_d2 = -float('inf')

for _ in range(200000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.95
    b = np.random.uniform(-b_max, b_max)
    cp = np.random.uniform(-0.1, 0.1)

    f0, ok0 = phi4_inv(sigma, b, cp)
    fp, okp = phi4_inv(sigma, b, cp + h)
    fm, okm = phi4_inv(sigma, b, cp - h)

    if not (ok0 and okp and okm):
        continue

    d2 = (fp - 2*f0 + fm) / h**2
    if d2 > max_d2:
        max_d2 = d2
    if d2 > 1e-3:
        n_concave_viol += 1

print("Concavity violations (d²f/dc'² > 1e-3): %d" % n_concave_viol)
print("Max d²f/dc'²: %.6e" % max_d2)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Sign of df/dc' — is 1/Phi4 monotone in c'?")
print(SEP)

n_pos_deriv = 0
n_neg_deriv = 0
n_tested_deriv = 0

for _ in range(200000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.95
    b = np.random.uniform(-b_max, b_max)
    cp = np.random.uniform(-0.1, 0.1)

    fp, okp = phi4_inv(sigma, b, cp + h)
    fm, okm = phi4_inv(sigma, b, cp - h)

    if not (okp and okm):
        continue

    n_tested_deriv += 1
    d1 = (fp - fm) / (2*h)
    if d1 > 1e-6:
        n_pos_deriv += 1
    elif d1 < -1e-6:
        n_neg_deriv += 1

print("Monotonicity tests: %d" % n_tested_deriv)
print("df/dc' > 0: %d (%.1f%%)" % (n_pos_deriv, 100.0*n_pos_deriv/max(1,n_tested_deriv)))
print("df/dc' < 0: %d (%.1f%%)" % (n_neg_deriv, 100.0*n_neg_deriv/max(1,n_tested_deriv)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Convexity of 1/Phi4 in b (for comparison)")
print(SEP)

n_b_tested = 0
n_b_viol = 0
min_d2_b = float('inf')

for _ in range(200000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.9
    b = np.random.uniform(-b_max, b_max)
    cp = np.random.uniform(-0.05, 0.05)

    h_b = min(1e-5, b_max * 0.01)
    if abs(b) + h_b > b_max:
        continue

    f0, ok0 = phi4_inv(sigma, b, cp)
    fp, okp = phi4_inv(sigma, b + h_b, cp)
    fm, okm = phi4_inv(sigma, b - h_b, cp)

    if not (ok0 and okp and okm):
        continue

    n_b_tested += 1
    d2 = (fp - 2*f0 + fm) / h_b**2

    if d2 < min_d2_b:
        min_d2_b = d2
    if d2 < -1e-3:
        n_b_viol += 1

print("d²f/db² tests: %d" % n_b_tested)
print("Violations: %d" % n_b_viol)
print("Min d²f/db²: %.6e" % min_d2_b)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Cross-derivative d²f/dbdc' sign")
print(SEP)

n_cross = 0
n_cross_pos = 0
n_cross_neg = 0

for _ in range(200000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.9
    b = np.random.uniform(-b_max*0.8, b_max*0.8)
    cp = np.random.uniform(-0.05, 0.05)

    h_b = 1e-5
    h_c = 1e-6

    fpp, _ = phi4_inv(sigma, b+h_b, cp+h_c)
    fpm, _ = phi4_inv(sigma, b+h_b, cp-h_c)
    fmp, _ = phi4_inv(sigma, b-h_b, cp+h_c)
    fmm, _ = phi4_inv(sigma, b-h_b, cp-h_c)

    if any(x is None for x in [fpp, fpm, fmp, fmm]):
        continue

    n_cross += 1
    d2_cross = (fpp - fpm - fmp + fmm) / (4*h_b*h_c)

    if d2_cross > 1e-3:
        n_cross_pos += 1
    elif d2_cross < -1e-3:
        n_cross_neg += 1

print("Cross-derivative tests: %d" % n_cross)
print("d²f/(db dc') > 0: %d (%.1f%%)" % (n_cross_pos, 100.0*n_cross_pos/max(1,n_cross)))
print("d²f/(db dc') < 0: %d (%.1f%%)" % (n_cross_neg, 100.0*n_cross_neg/max(1,n_cross)))
print("Mixed sign: %s" % ("YES" if n_cross_pos > 0 and n_cross_neg > 0 else "NO"))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Hessian of 1/Phi4 in (b, c') — PSD check")
print(SEP)

n_hess = 0
n_psd = 0
n_nsd = 0
n_indef = 0

for _ in range(200000):
    sigma = np.random.uniform(0.1, 2.0)
    b_max = (4*sigma**3/27)**0.5 * 0.9
    b = np.random.uniform(-b_max*0.8, b_max*0.8)
    cp = np.random.uniform(-0.05, 0.05)

    h_b = 1e-5
    h_c = 1e-6

    f0, ok0 = phi4_inv(sigma, b, cp)

    # d2f/db2
    fp_b, _ = phi4_inv(sigma, b+h_b, cp)
    fm_b, _ = phi4_inv(sigma, b-h_b, cp)
    if any(x is None for x in [f0, fp_b, fm_b]):
        continue
    fbb = (fp_b - 2*f0 + fm_b) / h_b**2

    # d2f/dc'2
    fp_c, _ = phi4_inv(sigma, b, cp+h_c)
    fm_c, _ = phi4_inv(sigma, b, cp-h_c)
    if any(x is None for x in [fp_c, fm_c]):
        continue
    fcc = (fp_c - 2*f0 + fm_c) / h_c**2

    # d2f/dbdc'
    fpp, _ = phi4_inv(sigma, b+h_b, cp+h_c)
    fpm, _ = phi4_inv(sigma, b+h_b, cp-h_c)
    fmp, _ = phi4_inv(sigma, b-h_b, cp+h_c)
    fmm, _ = phi4_inv(sigma, b-h_b, cp-h_c)
    if any(x is None for x in [fpp, fpm, fmp, fmm]):
        continue
    fbc = (fpp - fpm - fmp + fmm) / (4*h_b*h_c)

    n_hess += 1
    # Check PSD: trace >= 0 and det >= 0
    tr = fbb + fcc
    det = fbb * fcc - fbc**2

    if tr >= -1e-3 and det >= -1e-3:
        n_psd += 1
    elif tr <= 1e-3 and det >= -1e-3:
        n_nsd += 1
    else:
        n_indef += 1

print("Hessian tests: %d" % n_hess)
print("PSD (convex): %d (%.1f%%)" % (n_psd, 100.0*n_psd/max(1,n_hess)))
print("NSD (concave): %d (%.1f%%)" % (n_nsd, 100.0*n_nsd/max(1,n_hess)))
print("Indefinite: %d (%.1f%%)" % (n_indef, 100.0*n_indef/max(1,n_hess)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("VERDICT")
print(SEP)

if n_violations == 0 and n_concave_viol > 0:
    print("1/Phi4 is CONVEX in c' (for fixed sigma, b)")
    print("This is key: if each component is convex in c', then")
    print("M''(t) = (cp1+cp2)^2 * f_h'' - cp1^2 * f_1'' - cp2^2 * f_2''")
    print("= convexity of SUPERADDITIVITY in the c'-direction")
elif n_violations == 0 and n_concave_viol == 0:
    print("1/Phi4 appears LINEAR in c' (both convex and concave pass)")
elif n_violations > 0 and n_concave_viol > 0:
    print("1/Phi4 is NEITHER convex nor concave in c'")
elif n_violations > 0:
    print("1/Phi4 is NOT convex in c'")

if n_b_viol == 0:
    print("1/Phi4 is CONVEX in b")
else:
    print("1/Phi4 is NOT convex in b")

print("\nElapsed: %.1fs" % (time.time() - t0))
