"""
ce25c_boundary_test.py — Test boundary vanishing by direct substitution.

For polynomial in b1: replace b1^2 = 4w^3/27 to get remainder.
If remainder = 0, then (27b1^2 - 4w^3) divides N.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from sympy import (symbols, Rational, factor, expand, Poly, diff, sqrt,
                   collect, cancel, gcd as sym_gcd, lcm, simplify)

SEP = "=" * 70
t0 = time.time()

w, b1, b2 = symbols("w b1 b2", real=True)

def phi4_inv_cp0(s, b):
    num = 729*b**4 + 216*b**2*s**3 - 16*s**6
    den = 72*s**2*(27*b**2 - 4*s**3)
    return num, den

# Build gauge-fixed N
s1_sym, s2_sym = symbols("s1 s2")
S = s1_sym + s2_sym
B = b1 + b2
f1n, f1d = phi4_inv_cp0(s1_sym, b1)
f2n, f2d = phi4_inv_cp0(s2_sym, b2)
fhn, fhd = phi4_inv_cp0(S, B)

N_raw = expand(fhn * f1d * f2d - f1n * fhd * f2d - f2n * fhd * f1d)
N_gauge = expand(N_raw.subs(s2_sym, 1 - w).subs(s1_sym, w))

print(SEP)
print("SECTION 1: Collect N by powers of b1")
print(SEP)

# Collect N by b1 powers
Np = Poly(N_gauge, b1)
print("Degree in b1:", Np.degree())
for k in range(Np.degree() + 1):
    c = Np.nth(k)
    if c != 0:
        print("  b1^%d: nonzero (simplified len: %d)" % (k, len(str(factor(c)))))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Substitute b1^2 -> 4w^3/27 in N")
print(SEP)

# If (27b1^2 - 4w^3) | N, then N(b1) mod (b1^2 - 4w^3/27) = 0.
# This means: collecting even and odd parts, both evaluate to 0 at b1^2 = 4w^3/27.

# Separate even and odd parts in b1
R = Rational
alpha = symbols("alpha")  # alpha = b1^2 = 4w^3/27

coeffs = {}
for k in range(Np.degree() + 1):
    c = Np.nth(k)
    if c != 0:
        coeffs[k] = c

# Even part: sum of c_k * b1^k for even k. Set b1^2 = alpha:
# E(alpha) = c_0 + c_2*alpha + c_4*alpha^2 + c_6*alpha^3 + c_8*alpha^4
E = sum(coeffs.get(2*j, 0) * alpha**j for j in range(5))
E = expand(E)

# Odd part: sum of c_k * b1^k for odd k = b1 * (c_1 + c_3*alpha + c_5*alpha^2 + c_7*alpha^3)
O = sum(coeffs.get(2*j+1, 0) * alpha**j for j in range(4))
O = expand(O)

# N mod (b1^2 - alpha) = E(alpha) + b1 * O(alpha)
# For (27*b1^2 - 4w^3) to divide N, need E(4w^3/27) = 0 AND O(4w^3/27) = 0.

E_bdry = expand(E.subs(alpha, 4*w**3/27))
O_bdry = expand(O.subs(alpha, 4*w**3/27))

print("E(4w^3/27) = 0?", E_bdry == 0)
if E_bdry != 0:
    # Might need clearing denominators
    E_bdry_cleared = expand(E_bdry * 27**4)  # clear all 27 denominators
    print("E * 27^4:", E_bdry_cleared)
    print("  zero?", E_bdry_cleared == 0)

print("O(4w^3/27) = 0?", O_bdry == 0)
if O_bdry != 0:
    O_bdry_cleared = expand(O_bdry * 27**3)
    print("O * 27^3:", O_bdry_cleared)
    print("  zero?", O_bdry_cleared == 0)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Same test for boundary (b): 27*b2^2 = 4*(1-w)^3")
print(SEP)

Np2 = Poly(N_gauge, b2)
print("Degree in b2:", Np2.degree())

coeffs2 = {}
for k in range(Np2.degree() + 1):
    c = Np2.nth(k)
    if c != 0:
        coeffs2[k] = c

beta = symbols("beta")  # beta = b2^2 = 4*(1-w)^3/27
E2 = sum(coeffs2.get(2*j, 0) * beta**j for j in range(5))
E2 = expand(E2)
O2 = sum(coeffs2.get(2*j+1, 0) * beta**j for j in range(4))
O2 = expand(O2)

E2_bdry = expand(E2.subs(beta, 4*(1-w)**3/27))
O2_bdry = expand(O2.subs(beta, 4*(1-w)**3/27))

E2_bdry_cleared = expand(E2_bdry * 27**4)
O2_bdry_cleared = expand(O2_bdry * 27**3)

print("E2(4(1-w)^3/27) * 27^4 = 0?", E2_bdry_cleared == 0)
if E2_bdry_cleared != 0:
    print("  value:", str(E2_bdry_cleared)[:200])
print("O2(4(1-w)^3/27) * 27^3 = 0?", O2_bdry_cleared == 0)
if O2_bdry_cleared != 0:
    print("  value:", str(O2_bdry_cleared)[:200])
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Same test for boundary (c): 27*(b1+b2)^2 = 4")
print(SEP)

u_var = b1 + b2
# This is more complex. Use u,v coords: b1 = (u+v)/2, b2 = (u-v)/2
u, v = symbols("u v")
N_uv = expand(N_gauge.subs([(b1, (u+v)/2), (b2, (u-v)/2)]))

Np3 = Poly(N_uv, u)
print("Degree in u:", Np3.degree())

coeffs3 = {}
for k in range(Np3.degree() + 1):
    c = Np3.nth(k)
    if c != 0:
        coeffs3[k] = c

gamma = symbols("gamma")  # gamma = u^2 = 4/27
E3 = sum(coeffs3.get(2*j, 0) * gamma**j for j in range(5))
E3 = expand(E3)
O3 = sum(coeffs3.get(2*j+1, 0) * gamma**j for j in range(4))
O3 = expand(O3)

E3_bdry = expand(E3.subs(gamma, R(4,27)))
O3_bdry = expand(O3.subs(gamma, R(4,27)))

print("E3(4/27) = 0?", E3_bdry == 0)
if E3_bdry != 0:
    print("  E3:", str(factor(E3_bdry))[:300])
print("O3(4/27) = 0?", O3_bdry == 0)
if O3_bdry != 0:
    print("  O3:", str(factor(O3_bdry))[:300])
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Look for ACTUAL factors via sympy factor()")
print(SEP)

# Factor the full N in all variables
print("Attempting full factorization of N(w, b1, b2)...")
sys.stdout.flush()
t1 = time.time()
N_factored = factor(N_gauge)
print("Done in %.1fs" % (time.time() - t1))
# Print factored form (may be large)
s = str(N_factored)
if len(s) > 1000:
    print("Factored form (first 1000 chars):", s[:1000])
else:
    print("Factored form:", s)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 6: Content extraction + factor of content-free part")
print(SEP)

# First get integer content
Np_full = Poly(N_gauge, w, b1, b2)
cont = Np_full.content()
print("Integer content:", cont)
N_prim = expand(N_gauge / cont)
Np_prim = Poly(N_prim, w, b1, b2)
print("Primitive polynomial: %d terms, total degree %d" %
      (len(N_prim.as_ordered_terms()), Np_prim.total_degree()))

print("\nFactoring primitive part...")
sys.stdout.flush()
t1 = time.time()
N_prim_factored = factor(N_prim)
print("Done in %.1fs" % (time.time() - t1))
s = str(N_prim_factored)
if len(s) > 1000:
    print("Factored (first 1000 chars):", s[:1000])
else:
    print("Factored:", s)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 7: Evaluate N at specific boundary points (exact)")
print(SEP)

# Use exact arithmetic. At w=1/2, boundary (a): b1^2 = 4*(1/2)^3/27 = 1/54
# b1 = 1/sqrt(54). Not rational. Try b1^2 = 1/54 directly.
# Since N has odd b1 powers, we need to set b1 = ±sqrt(1/54).
# Instead, evaluate the even and odd parts separately.

from fractions import Fraction

for w_val in [R(1,3), R(1,2), R(2,3)]:
    alpha_val = 4*w_val**3 / 27
    E_val = E.subs(alpha, alpha_val)
    O_val = O.subs(alpha, alpha_val)
    # These should still depend on b2
    print("\nw=%s, alpha=b1^2=%s:" % (w_val, alpha_val))
    E_val_b2_0 = E_val.subs(b2, 0)
    O_val_b2_0 = O_val.subs(b2, 0)
    print("  E(alpha) at b2=0: %s" % E_val_b2_0)
    print("  O(alpha) at b2=0: %s" % O_val_b2_0)
    for b2v in [R(1,20), R(1,10)]:
        E_v = E_val.subs(b2, b2v)
        O_v = O_val.subs(b2, b2v)
        print("  E(alpha) at b2=%s: %s" % (b2v, E_v))
        print("  O(alpha) at b2=%s: %s" % (b2v, O_v))

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
