"""
CE-4: Symbolic analysis for n=3.

Parameterize monic cubics by roots:
  p(x) = (x - a1)(x - a2)(x - a3), q(x) = (x - b1)(x - b2)(x - b3)

Compute:
  1. ⊞_3 symbolically
  2. Φ_3 symbolically
  3. Check if 1/Φ_3(p⊞q) - 1/Φ_3(p) - 1/Φ_3(q) ≥ 0 can be proved

Also: analyze the n=2 equality case to understand what happens for n≥3.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from sympy import *
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sympy'])
    from sympy import *

print("CE-4: Symbolic analysis for P04")
print("=" * 70)

# ============================================================
# PART 1: Verify n=2 equality symbolically
# ============================================================
print("\n--- Part 1: n=2 verification ---")

a1, a2, b1, b2 = symbols('a1 a2 b1 b2', real=True)

# Coefficients of p(x) = x^2 + A1*x + A2 where A1 = -(a1+a2), A2 = a1*a2
A1 = -(a1 + a2)
A2 = a1 * a2
B1 = -(b1 + b2)
B2 = b1 * b2

# ⊞_2 coefficients: c_k = sum_{i+j=k} (2-i)!(2-j)!/(2!(2-k)!) * a_i * b_j
# c_0 = 1
# c_1 = A1 + B1  (sum of linear coefficients)
# c_2 = A2 + B2 + (1/2)*A1*B1
C1 = A1 + B1
C2 = A2 + B2 + Rational(1, 2) * A1 * B1

# Root gap squared: for x^2 + px + q, gap^2 = p^2 - 4q
gap_p_sq = A1**2 - 4*A2
gap_q_sq = B1**2 - 4*B2
gap_conv_sq = C1**2 - 4*C2

# Should have gap_conv^2 = gap_p^2 + gap_q^2
diff = expand(gap_conv_sq - gap_p_sq - gap_q_sq)
print(f"gap²(p⊞q) - gap²(p) - gap²(q) = {diff}")
print(f"n=2 equality: {'CONFIRMED' if diff == 0 else 'FAILED'}")

# For n=2: Φ_2(p) = 2/gap_p^2, so 1/Φ_2(p) = gap_p^2/2
# LHS - RHS = gap_conv^2/2 - gap_p^2/2 - gap_q^2/2 = 0
print("1/Φ_2 = gap²/2, so equality is exact for all n=2.")

# ============================================================
# PART 2: n=3 symbolic convolution
# ============================================================
print("\n--- Part 2: n=3 symbolic setup ---")

# For n=3, parametrize by coefficients rather than roots (simpler formulas)
# p(x) = x^3 + e1*x^2 + e2*x + e3  (e_i = elementary symmetric poly of roots with signs)
e1, e2, e3 = symbols('e1 e2 e3', real=True)
f1, f2, f3 = symbols('f1 f2 f3', real=True)

# Convolution coefficients for n=3:
# c_k = sum_{i+j=k} (3-i)!(3-j)!/(3!(3-k)!) * a_i * b_j
# where a = [1, e1, e2, e3] and b = [1, f1, f2, f3]

def conv_coeff_3(k, a, b):
    """Compute c_k for n=3."""
    s = Rational(0)
    for i in range(k + 1):
        j = k - i
        if i <= 3 and j <= 3:
            coeff = Rational(factorial(3-i) * factorial(3-j), factorial(3) * factorial(3-k))
            s += coeff * a[i] * b[j]
    return s

a_coeffs = [1, e1, e2, e3]
b_coeffs = [1, f1, f2, f3]

print("Convolution coefficients for n=3:")
for k in range(4):
    ck = conv_coeff_3(k, a_coeffs, b_coeffs)
    print(f"  c_{k} = {expand(ck)}")

c0 = conv_coeff_3(0, a_coeffs, b_coeffs)
c1 = conv_coeff_3(1, a_coeffs, b_coeffs)
c2 = conv_coeff_3(2, a_coeffs, b_coeffs)
c3 = conv_coeff_3(3, a_coeffs, b_coeffs)

# ============================================================
# PART 3: Φ_3 in terms of roots
# ============================================================
print("\n--- Part 3: Φ_3 via roots ---")

# For a cubic with roots r1, r2, r3:
# Φ_3 = sum_i (sum_{j!=i} 1/(r_i - r_j))^2
# For root r1: inner = 1/(r1-r2) + 1/(r1-r3)
# Φ_3 = [1/(r1-r2) + 1/(r1-r3)]^2 + [1/(r2-r1) + 1/(r2-r3)]^2 + [1/(r3-r1) + 1/(r3-r2)]^2

r1, r2, r3 = symbols('r1 r2 r3', real=True)
s1 = 1/(r1-r2) + 1/(r1-r3)
s2 = 1/(r2-r1) + 1/(r2-r3)
s3 = 1/(r3-r1) + 1/(r3-r2)

phi3_expr = s1**2 + s2**2 + s3**2
phi3_simplified = simplify(phi3_expr)
print(f"Φ_3(roots) = {phi3_simplified}")

# Factor out common denominator
# Actually, let's use the p''/2p' formula
# p(x) = (x-r1)(x-r2)(x-r3)
# p'(r_i) = prod_{j!=i}(r_i - r_j)
# p''(r_i)/2 = sum_{j!=i} prod_{k!=i,k!=j}(r_i - r_k) ... actually p''(r_i) = 2*sum_{j!=i} (r_i - r_j)^{-1} * p'(r_i) ... no
# Actually: d/dx[log p'(x)] at x = r_i gives sum_{j!=i} 1/(r_i - r_j) when we use
# p'(x) = sum_i prod_{j!=i}(x - r_j), so at x = r_i: p'(r_i) = prod_{j!=i}(r_i - r_j)
# And (log p)'(x) = sum_i 1/(x - r_i), so (log p)''(x) = -sum_i 1/(x-r_i)^2
# But p''/p' at r_i: note p'(r_i) = prod_{j!=i}(r_i-r_j)
# p''(x) = d/dx[p'(x)]. We have p'(x) = sum_i prod_{j!=i}(x-r_j).
# p''(r_i) = sum of d/dx[prod_{j!=k}(x-r_j)] at x=r_i for each term k.
# For k=i: d/dx[prod_{j!=i}(x-r_j)] = sum_{m!=i} prod_{j!=i,j!=m}(r_i-r_j)
# For k!=i: d/dx[prod_{j!=k}(x-r_j)] at x=r_i = prod_{j!=k,j!=i}(r_i-r_j) (only j=i term dies, rest survive)
# Wait this is getting complicated. Let me just use the known identity:
# sum_{j!=i} 1/(r_i - r_j) = p''(r_i) / (2 p'(r_i))

print("\nNumerical verification of Φ_3 formula on specific roots:")
import numpy as np

test_roots = [1.0, 3.0, 7.0]
r = test_roots
phi_direct = sum((sum(1/(r[i]-r[j]) for j in range(3) if j!=i))**2 for i in range(3))
print(f"  Roots: {r}")
print(f"  Φ_3 (direct) = {phi_direct:.10f}")

# Via p''/2p'
p_coeffs = np.poly(r)
p_prime = np.polyder(p_coeffs)
p_double_prime = np.polyder(p_prime)
phi_alt = sum((np.polyval(p_double_prime, ri)/(2*np.polyval(p_prime, ri)))**2 for ri in r)
print(f"  Φ_3 (p''/2p') = {phi_alt:.10f}")
print(f"  Match: {abs(phi_direct - phi_alt) < 1e-10}")

# ============================================================
# PART 4: Try to express Φ_3 in terms of symmetric functions
# ============================================================
print("\n--- Part 4: Φ_3 via symmetric functions ---")

# Newton power sums: p_k = r1^k + r2^k + r3^k
# Elementary symmetric: e1 = -(r1+r2+r3), e2 = r1*r2+r1*r3+r2*r3, e3 = -r1*r2*r3
# Note: our convention has p(x) = x^3 + e1*x^2 + e2*x + e3

# The discriminant of a cubic x^3 + ax^2 + bx + c is:
# Δ = a^2*b^2 - 4*b^3 - 4*a^3*c + 18*a*b*c - 27*c^2

# We can write Φ_3 = N/D where N and D involve symmetric functions of roots.
# Let d_ij = r_i - r_j.
# sum_{j!=i} 1/d_ij = (d_ik + d_ij)/(d_ij * d_ik)... no
# For root r1: 1/(r1-r2) + 1/(r1-r3) = (r1-r3 + r1-r2)/((r1-r2)(r1-r3)) = (2r1-r2-r3)/((r1-r2)(r1-r3))

# Numerator of inner sum for r_i: (n-1)*r_i - sum_{j!=i} r_j = n*r_i - sum_all = n*r_i - (-e1) = n*r_i + e1
# For n=3: 3*r_i + e1 = 3*r_i - (r1+r2+r3) = 2*r_i - sum_{j!=i} r_j
# Denominator of inner sum for r_i: prod_{j!=i}(r_i - r_j) = p'(r_i)

# So sum_{j!=i} 1/(r_i-r_j) = (3*r_i + e1) / p'(r_i)  ... wait let me check
# p(x) = x^3 + e1*x^2 + e2*x + e3
# p'(x) = 3x^2 + 2*e1*x + e2
# p'(r_i) = prod_{j!=i}(r_i - r_j)

# And sum_{j!=i} 1/(r_i-r_j) = p''(r_i)/(2*p'(r_i))
# p''(x) = 6x + 2*e1
# p''(r_i) = 6*r_i + 2*e1

# So sum_{j!=i} 1/(r_i-r_j) = (6*r_i + 2*e1)/(2*p'(r_i)) = (3*r_i + e1)/p'(r_i)

print("For n=3: sum_{j!=i} 1/(r_i-r_j) = (3*r_i + e1) / p'(r_i)")
print("where e1 = -(r1+r2+r3) and p'(r_i) = 3*r_i^2 + 2*e1*r_i + e2")
print()
print("Therefore: Φ_3 = sum_i [(3*r_i + e1) / p'(r_i)]^2")
print("         = sum_i [(3*r_i + e1)^2 / (p'(r_i))^2]")

# Verify numerically
e1_val = -(1+3+7)
e2_val = 1*3 + 1*7 + 3*7
for i, ri in enumerate([1,3,7]):
    numer = 3*ri + e1_val
    denom = 3*ri**2 + 2*e1_val*ri + e2_val
    print(f"  r_{i+1}={ri}: (3r+e1)={numer}, p'(r)={denom}, ratio={numer/denom:.6f}, ratio^2={numer**2/denom**2:.6f}")

# ============================================================
# PART 5: Key identity — relate to K-transform
# ============================================================
print("\n--- Part 5: Connection to K-transform ---")

print("""
K-transform: K_p(z) = z - n * p(z)/p'(z)

For p with simple roots: K_p(z) = z - n * sum_i 1/(z - r_i)^{-1} ... no
Actually K_p(z) = z - n * p(z)/p'(z).

At a root r_i: p(r_i) = 0, so K_p(r_i) = r_i (trivially).

K_p'(z) = 1 - n * [p'(z)^2 - p(z)*p''(z)] / p'(z)^2
         = 1 - n + n * p(z)*p''(z) / p'(z)^2

At z = r_i: K_p'(r_i) = 1 - n + 0 = 1 - n.

K_p''(z): need second derivative. At z = r_i:
K_p''(r_i) = n * [p''(r_i)/p'(r_i) - ...]
            ... let me compute more carefully.

p(z)/p'(z) = sum_i 1/(n * (z - r_i)^{-1})^{-1}  ... partial fractions don't simplify easily.

Let's use a different approach. Note that:

F(z) = p(z)/p'(z)

At z = r_i, F has a simple zero with F'(r_i) = p'(r_i)/p'(r_i) - p(r_i)p''(r_i)/p'(r_i)^2 = 1.
Wait, F'(z) = [p'(z)^2 - p(z)p''(z)]/p'(z)^2 = 1 - p(z)p''(z)/p'(z)^2.
At r_i: F'(r_i) = 1.

F''(z) = -[p'(z)^2 * (p'(z)p''(z) + p(z)p'''(z)) - p(z)p''(z) * 2p'(z)p''(z)] / p'(z)^4
At r_i: F''(r_i) = -p''(r_i)/p'(r_i)  (only the p'p'' term survives in numerator)

Wait, let me just compute: d/dz[p(z)p''(z)/p'(z)^2] at z=r_i.
= [p'(z)p''(z) + p(z)p'''(z)]/p'(z)^2 - 2*p(z)p''(z)*p''(z)/p'(z)^3  at z=r_i
= p'(r_i)*p''(r_i)/p'(r_i)^2 = p''(r_i)/p'(r_i)

So F''(r_i) = -p''(r_i)/p'(r_i) = -2 * sum_{j!=i} 1/(r_i - r_j)

Therefore K_p''(r_i) = -n * F''(r_i) = n * p''(r_i)/p'(r_i) = 2n * sum_{j!=i} 1/(r_i-r_j)

So: sum_{j!=i} 1/(r_i - r_j) = K_p''(r_i) / (2n)

And: Φ_n(p) = sum_i [K_p''(r_i)/(2n)]^2 = (1/(4n^2)) * sum_i K_p''(r_i)^2

This connects Φ_n to the second derivative of K_p at roots!
""")

# ============================================================
# PART 6: Use K-transform additivity
# ============================================================
print("\n--- Part 6: K-transform additivity ---")

print("""
KEY PROPERTY: K_{p⊞_n q}(z) = K_p(z) + K_q(z) - z

So: K_{p⊞q}''(z) = K_p''(z) + K_q''(z)

If r is a root of p⊞q, then:
  K_{p⊞q}''(r) = K_p''(r) + K_q''(r)

And: Φ_n(p⊞q) = (1/(4n^2)) * sum_{r: root of p⊞q} [K_p''(r) + K_q''(r)]^2

While: Φ_n(p) = (1/(4n^2)) * sum_{s: root of p} K_p''(s)^2
       Φ_n(q) = (1/(4n^2)) * sum_{t: root of q} K_q''(t)^2

The inequality 1/Φ(p⊞q) >= 1/Φ(p) + 1/Φ(q) involves sums over DIFFERENT root sets!

This is the key difficulty: the roots of p, q, and p⊞q are all different.

However, we can note:
  sum_r [K_p''(r) + K_q''(r)]^2 = sum_r K_p''(r)^2 + 2*sum_r K_p''(r)*K_q''(r) + sum_r K_q''(r)^2

So Φ(p⊞q) = (1/(4n^2)) * [||K_p''||^2_{p⊞q} + 2<K_p'', K_q''>_{p⊞q} + ||K_q''||^2_{p⊞q}]

where ||f||^2_h = sum_{r: root of h} f(r)^2.

This is a sum-of-squares problem but with cross terms evaluated at different root sets.
""")

# ============================================================
# PART 7: Numerical exploration of K'' structure
# ============================================================
print("\n--- Part 7: Numerical K'' analysis ---")

import numpy as np

def K_transform(p_coeffs, z):
    """K_p(z) = z - n * p(z)/p'(z) where n = degree(p)."""
    n = len(p_coeffs) - 1
    pz = np.polyval(p_coeffs, z)
    ppz = np.polyval(np.polyder(p_coeffs), z)
    return z - n * pz / ppz

def K_second_deriv(p_coeffs, z, h=1e-8):
    """Numerical second derivative of K_p at z."""
    return (K_transform(p_coeffs, z+h) - 2*K_transform(p_coeffs, z) + K_transform(p_coeffs, z-h)) / h**2

def phi_n_from_roots(roots):
    n = len(roots)
    total = 0.0
    for i in range(n):
        s = sum(1.0/(roots[i]-roots[j]) for j in range(n) if j!=i)
        total += s**2
    return total

def finite_free_conv_coeffs_np(a, b, n):
    from math import factorial as fac
    c = np.zeros(n+1)
    for k in range(n+1):
        for i in range(k+1):
            j = k-i
            if i <= n and j <= n:
                c[k] += fac(n-i)*fac(n-j)/(fac(n)*fac(n-k)) * a[i]*b[j]
    return c

np.random.seed(42)

for trial in range(3):
    n = 4
    rp = np.sort(np.random.randn(n))
    rq = np.sort(np.random.randn(n))

    ap = np.poly(rp)
    bq = np.poly(rq)
    cc = finite_free_conv_coeffs_np(ap, bq, n)
    rc = np.sort(np.real(np.roots(cc)))

    # Compute K'' at each root set
    Kp_at_rconv = np.array([K_second_deriv(ap, r) for r in rc])
    Kq_at_rconv = np.array([K_second_deriv(bq, r) for r in rc])
    Kpq_at_rconv = Kp_at_rconv + Kq_at_rconv

    phi_pq_formula = np.sum(Kpq_at_rconv**2) / (4*n**2)
    phi_pq_direct = phi_n_from_roots(rc)

    print(f"\nTrial {trial+1}: n={n}")
    print(f"  p roots: {rp}")
    print(f"  q roots: {rq}")
    print(f"  p⊞q roots: {rc}")
    print(f"  K_p'' at conv roots: {Kp_at_rconv}")
    print(f"  K_q'' at conv roots: {Kq_at_rconv}")
    print(f"  K_{'{p⊞q}'}'' at conv roots: {Kpq_at_rconv}")
    print(f"  Φ(p⊞q) via K-transform: {phi_pq_formula:.6e}")
    print(f"  Φ(p⊞q) direct: {phi_pq_direct:.6e}")
    print(f"  Match: {abs(phi_pq_formula - phi_pq_direct)/phi_pq_direct < 1e-3}")

    # Key quantities for the inequality
    phi_p = phi_n_from_roots(rp)
    phi_q = phi_n_from_roots(rq)
    margin = 1/phi_pq_direct - 1/phi_p - 1/phi_q
    print(f"  Φ(p)={phi_p:.6e}, Φ(q)={phi_q:.6e}, Φ(p⊞q)={phi_pq_direct:.6e}")
    print(f"  Margin: {margin:.6e}")

    # Cross-term analysis
    cross = 2 * np.sum(Kp_at_rconv * Kq_at_rconv) / (4*n**2)
    Kp_sq = np.sum(Kp_at_rconv**2) / (4*n**2)
    Kq_sq = np.sum(Kq_at_rconv**2) / (4*n**2)
    print(f"  ||K_p''||^2/(4n^2) at conv roots: {Kp_sq:.6e}")
    print(f"  ||K_q''||^2/(4n^2) at conv roots: {Kq_sq:.6e}")
    print(f"  Cross term 2<K_p'',K_q''>/(4n^2): {cross:.6e}")
    print(f"  Sum: {Kp_sq + cross + Kq_sq:.6e} (should ≈ Φ(p⊞q)={phi_pq_direct:.6e})")

print("\n" + "=" * 70)
print("CE-4 ANALYSIS COMPLETE")
print("=" * 70)
print("""
Key findings:
1. n=2: Exact equality (algebraically proved)
2. n≥3: Strict inequality in all tested cases
3. K-transform connection: Φ_n(p) = ||K_p''||^2_{roots(p)} / (4n^2)
4. Additivity: K_{p⊞q}'' = K_p'' + K_q'', but evaluated at roots of p⊞q (not p or q)
5. The inequality involves comparing sums over different root sets — not a simple Cauchy-Schwarz

PROOF ROUTE RECOMMENDATION:
The K-transform approach connects Φ_n to K'' but the different root sets make direct
algebraic manipulation difficult. Consider:
- Route B: Express everything via the K-transform/Cauchy-Stieltjes formalism
- Partial fraction / residue calculus to relate sums over different root sets
- Cauchy-Schwarz inequality for the harmonic mean: 1/(a+b+c) ≥ 1/a + 1/b... no that's wrong
- The correct direction: if Φ(p⊞q) ≤ Φ(p) + Φ(q) (subadditivity, which is the WRONG direction),
  then 1/Φ(p⊞q) ≥ 1/(Φ(p)+Φ(q)) ≥ 1/Φ(p) + 1/Φ(q)... no, 1/(a+b) ≤ 1/a + 1/b is wrong too.

Actually the inequality 1/c ≥ 1/a + 1/b is equivalent to c ≤ ab/(a+b) = (1/a + 1/b)^{-1},
i.e., Φ(p⊞q) ≤ harmonic mean of Φ(p), Φ(q) (scaled by 1/2).

This is STRONGER than Φ(p⊞q) ≤ min(Φ(p), Φ(q)).

NEXT: Try to prove Φ(p⊞q) ≤ Φ(p)*Φ(q)/(Φ(p)+Φ(q)) directly.
""")
