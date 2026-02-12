"""
ce18c_counterexample_verify.py — Full verification of the P04 counterexample.

CE-18b found: the superadditivity inequality 1/Phi_4(p ⊞ q) >= 1/Phi_4(p) + 1/Phi_4(q)
is FALSE for b != 0.

Counterexample in cumulant coordinates:
  (sigma1, b1, cp1) = (3/10, -1/20, 1/25)
  (sigma2, b2, cp2) = (1/2, -1/20, 0)

This script:
1. Converts to original polynomial coefficients (a, b, c for x^4 + ax^2 + bx + c)
2. Computes roots of p, q, and p ⊞₄ q
3. Computes Phi_4 directly from roots
4. Verifies the violation from first principles
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import Rational, sqrt, Poly, symbols, solve, nsimplify, factor, expand
from sympy import Float
import numpy as np

SEP = "=" * 70
x = symbols("x")

# ============================================================
print(SEP)
print("SECTION 1: Convert counterexample to polynomial coefficients")
print(SEP)

# Cumulant coordinates: sigma = -a, b = b, cp = c - sigma^2/12
# So: a = -sigma, c = cp + sigma^2/12

s1, b1_val, cp1 = Rational(3,10), Rational(-1,20), Rational(1,25)
s2, b2_val, cp2 = Rational(1,2), Rational(-1,20), Rational(0)

a1 = -s1  # = -3/10
c1 = cp1 + s1**2/12  # = 1/25 + 9/1200 = 1/25 + 3/400 = 16/400 + 3/400 = 19/400
b1_coeff = b1_val  # = -1/20

a2 = -s2  # = -1/2
c2 = cp2 + s2**2/12  # = 0 + 1/48
b2_coeff = b2_val  # = -1/20

print("Polynomial p(x) = x^4 + a1*x^2 + b1*x + c1:")
print("  a1 = %s = %.6f" % (a1, float(a1)))
print("  b1 = %s = %.6f" % (b1_coeff, float(b1_coeff)))
print("  c1 = %s = %.6f" % (c1, float(c1)))

print("\nPolynomial q(x) = x^4 + a2*x^2 + b2*x + c2:")
print("  a2 = %s = %.6f" % (a2, float(a2)))
print("  b2 = %s = %.6f" % (b2_coeff, float(b2_coeff)))
print("  c2 = %s = %.6f" % (c2, float(c2)))

# Compute ⊞₄ coefficients using the convolution formula
# For x^4 + a*x^2 + b*x + c (centered, so a1_coeff = 0):
# c_k = sum_{i+j=k} (4-i)!(4-j)! / (4!(4-k)!) * a_i * b_j
# where a_0 = b_0 = 1, a_1 = b_1 = 0 (centered), and coefficients multiply x^(4-k)

# For k=2: c_2 = sum_{i+j=2} (4-i)!(4-j)!/(4!*2!) * a_i b_j
# i=0,j=2: 4!*2!/(4!*2!) * 1 * a2_q = a2_q
# i=2,j=0: 2!*4!/(4!*2!) * a1_p * 1 = a1_p
# i=1,j=1: 3!*3!/(4!*2!) * 0 * 0 = 0
# So c_2 = a1_p + a2_q => a_sum = a1 + a2

# For k=3: c_3 = sum_{i+j=3}
# i=0,j=3: 4!*1!/(4!*1!) * 1 * b2_q = b2_q
# i=3,j=0: 1!*4!/(4!*1!) * b1_p * 1 = b1_p
# i=1,j=2: 3!*2!/(4!*1!) * 0 * a2_q = 0
# i=2,j=1: 2!*3!/(4!*1!) * a1_p * 0 = 0
# So c_3 = b1 + b2 => b_sum = b1 + b2

# For k=4: c_4 = sum_{i+j=4}
# i=0,j=4: 4!*0!/(4!*0!) = 1 => c2
# i=4,j=0: 0!*4!/(4!*0!) = 1 => c1
# i=1,j=3: 3!*1!/(4!*0!) = 6/24 = 1/4 => 0*b2 = 0
# i=3,j=1: 1!*3!/(4!*0!) = 6/24 = 1/4 => b1*0 = 0
# i=2,j=2: 2!*2!/(4!*0!) = 4/24 = 1/6 => a1*a2
# So c_4 = c1 + c2 + (1/6)*a1*a2

a_sum = a1 + a2
b_sum = b1_coeff + b2_coeff
c_sum = c1 + c2 + Rational(1,6)*a1*a2

print("\nConvolution h = p ⊞₄ q: x^4 + a_s*x^2 + b_s*x + c_s:")
print("  a_s = a1+a2 = %s = %.6f" % (a_sum, float(a_sum)))
print("  b_s = b1+b2 = %s = %.6f" % (b_sum, float(b_sum)))
print("  c_s = c1+c2+(1/6)a1*a2 = %s = %.6f" % (c_sum, float(c_sum)))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Verify discriminants (all must be > 0)")
print(SEP)

def disc4(a, b, c):
    """Discriminant of x^4 + ax^2 + bx + c."""
    return (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
            + 144*a*b**2*c - 27*b**4 + 256*c**3)

d1 = disc4(a1, b1_coeff, c1)
d2 = disc4(a2, b2_coeff, c2)
ds = disc4(a_sum, b_sum, c_sum)

print("Delta(p)   = %s = %.10f (>0: %s)" % (d1, float(d1), d1 > 0))
print("Delta(q)   = %s = %.10f (>0: %s)" % (d2, float(d2), d2 > 0))
print("Delta(h)   = %s = %.10f (>0: %s)" % (ds, float(ds), ds > 0))
print("All valid: %s" % (d1 > 0 and d2 > 0 and ds > 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Compute Phi_4 directly from roots")
print(SEP)

def compute_Phi4_from_roots(roots_list):
    """Compute Phi_4 = sum_i (sum_{j!=i} 1/(r_i - r_j))^2 from roots."""
    n = len(roots_list)
    total = Rational(0)
    for i in range(n):
        inner = Rational(0)
        for j in range(n):
            if j != i:
                inner += Rational(1, roots_list[i] - roots_list[j])
        total += inner**2
    return total

# Compute roots numerically (exact roots of quartic are messy)
p_poly = x**4 + a1*x**2 + b1_coeff*x + c1
q_poly = x**4 + a2*x**2 + b2_coeff*x + c2
h_poly = x**4 + a_sum*x**2 + b_sum*x + c_sum

print("p(x) =", p_poly)
print("q(x) =", q_poly)
print("h(x) =", h_poly)

# Use numpy for root finding with high precision
p_coeffs = [1, 0, float(a1), float(b1_coeff), float(c1)]
q_coeffs = [1, 0, float(a2), float(b2_coeff), float(c2)]
h_coeffs = [1, 0, float(a_sum), float(b_sum), float(c_sum)]

p_roots = np.sort(np.roots(p_coeffs).real)
q_roots = np.sort(np.roots(q_coeffs).real)
h_roots = np.sort(np.roots(h_coeffs).real)

print("\nRoots of p:", p_roots)
print("Roots of q:", q_roots)
print("Roots of h:", h_roots)
print("All real? p:%s q:%s h:%s" % (
    all(abs(r.imag) < 1e-10 for r in np.roots(p_coeffs)),
    all(abs(r.imag) < 1e-10 for r in np.roots(q_coeffs)),
    all(abs(r.imag) < 1e-10 for r in np.roots(h_coeffs))))

def phi4_numerical(roots):
    n = len(roots)
    total = 0.0
    for i in range(n):
        inner = sum(1.0/(roots[i] - roots[j]) for j in range(n) if j != i)
        total += inner**2
    return total

Phi_p = phi4_numerical(p_roots)
Phi_q = phi4_numerical(q_roots)
Phi_h = phi4_numerical(h_roots)

print("\nPhi_4(p) = %.10f" % Phi_p)
print("Phi_4(q) = %.10f" % Phi_q)
print("Phi_4(h) = %.10f" % Phi_h)

inv_p = 1.0/Phi_p
inv_q = 1.0/Phi_q
inv_h = 1.0/Phi_h

print("\n1/Phi_4(p) = %.10f" % inv_p)
print("1/Phi_4(q) = %.10f" % inv_q)
print("1/Phi_4(h) = %.10f" % inv_h)

M = inv_h - inv_p - inv_q
print("\nM = 1/Phi_4(h) - 1/Phi_4(p) - 1/Phi_4(q) = %.10e" % M)
print("M < 0?", M < 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Verify via the algebraic formula")
print(SEP)

# 1/Phi_4 = -Delta / (4 * A * B) where A = a^2+12c, B = 2a^3-8ac+9b^2
def inv_Phi4_formula(a, b, c):
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    D = disc4(a, b, c)
    if A == 0 or B == 0:
        return None
    return -D / (4 * A * B)

f_p = inv_Phi4_formula(a1, b1_coeff, c1)
f_q = inv_Phi4_formula(a2, b2_coeff, c2)
f_h = inv_Phi4_formula(a_sum, b_sum, c_sum)

print("1/Phi_4(p) [formula] = %s = %.10f" % (f_p, float(f_p)))
print("1/Phi_4(q) [formula] = %s = %.10f" % (f_q, float(f_q)))
print("1/Phi_4(h) [formula] = %s = %.10f" % (f_h, float(f_h)))

M_exact = f_h - f_p - f_q
print("\nM [exact] = %s" % M_exact)
print("M [float] = %.15e" % float(M_exact))
print("M < 0?", M_exact < 0)

# ============================================================
print("\n" + SEP)
print("SECTION 5: Cumulant-coordinate cross-check")
print(SEP)

# In cumulant coordinates, sigma = -a, b = b, cp = c - sigma^2/12
# Additivity: sigma_sum = s1 + s2, b_sum = b1 + b2, cp_sum = cp1 + cp2
# But c_sum = c1 + c2 + (1/6)*a1*a2 = cp1+s1^2/12 + cp2+s2^2/12 + (1/6)*(-s1)*(-s2)
# cp_sum = c_sum - (s1+s2)^2/12
cp_sum_direct = cp1 + cp2  # = 1/25
cp_sum_from_c = c_sum - (s1+s2)**2/12
print("cp_sum (direct additivity) = %s" % cp_sum_direct)
print("cp_sum (from c_sum) = %s" % cp_sum_from_c)
print("Match? %s" % (cp_sum_direct == cp_sum_from_c))

# Verify that the convolution formula gives cp_sum = cp1 + cp2
# c_sum = cp1 + s1^2/12 + cp2 + s2^2/12 + (1/6)*s1*s2
# cp_sum = c_sum - (s1+s2)^2/12 = cp1 + cp2 + s1^2/12 + s2^2/12 + s1*s2/6 - (s1^2+2s1s2+s2^2)/12
# = cp1 + cp2 + s1*s2/6 - 2s1s2/12 = cp1 + cp2 + s1s2/6 - s1s2/6 = cp1 + cp2
print("(This confirms cp IS additive under ⊞₄ — the cumulant coordinate is correct)")

# ============================================================
print("\n" + SEP)
print("COUNTEREXAMPLE SUMMARY")
print(SEP)
print()
print("Polynomials:")
print("  p(x) = x^4 + (%s)x^2 + (%s)x + (%s)" % (a1, b1_coeff, c1))
print("       = x^4 - (3/10)x^2 - (1/20)x + 19/400")
print("  q(x) = x^4 + (%s)x^2 + (%s)x + (%s)" % (a2, b2_coeff, c2))
print("       = x^4 - (1/2)x^2 - (1/20)x + 1/48")
print("  h(x) = p ⊞₄ q = x^4 + (%s)x^2 + (%s)x + (%s)" % (a_sum, b_sum, c_sum))
print()
print("All three have 4 simple real roots (Δ > 0).")
print()
print("Exact margin:")
print("  M = 1/Φ₄(h) - 1/Φ₄(p) - 1/Φ₄(q) = %s" % M_exact)
print("  M ≈ %.10e" % float(M_exact))
print("  M < 0: %s" % (M_exact < 0))
print()
if M_exact < 0:
    print("*** THE INEQUALITY 1/Φ₄(p ⊞₄ q) ≥ 1/Φ₄(p) + 1/Φ₄(q)")
    print("*** IS FALSE FOR GENERAL n=4 QUARTICS.")
    print("*** The violation is small (~0.4%) but rigorous (exact arithmetic).")
    print()
    print("*** P04 REVISED ANSWER:")
    print("***   n=2: YES (proved)")
    print("***   n=3: YES (proved)")
    print("***   n=4, b=0 (even quartics): YES (proved, CE-16)")
    print("***   n=4, b≠0 (general quartics): NO (counterexample above)")
    print("***   n≥5: UNKNOWN (likely NO given n=4 failure)")
