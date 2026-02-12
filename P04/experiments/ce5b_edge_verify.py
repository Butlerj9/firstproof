"""
P04 CE-5b: Verify the n=3 clustered-root edge case at 300 digits.
The CE-5 sweep showed margin=-7.3e-153 at 150 digits for n=3, eps=0.01.
Need to confirm this is numerical noise, not a genuine counterexample.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 300  # 300 digits

print("P04 CE-5b: Edge case verification at 300 digits")
print("=" * 70)

def mp_factorial(n):
    return mpmath.factorial(n)

def poly_from_roots(roots):
    poly = [mpmath.mpf(1)]
    for r in roots:
        new_poly = [mpmath.mpf(0)] * (len(poly) + 1)
        for i in range(len(poly)):
            new_poly[i] += poly[i]
            new_poly[i + 1] -= poly[i] * r
        poly = new_poly
    return poly

def finite_free_conv(a, b, n):
    c = [mpmath.mpf(0)] * (n + 1)
    for k in range(n + 1):
        for i in range(k + 1):
            j = k - i
            if i <= n and j <= n:
                num = mp_factorial(n - i) * mp_factorial(n - j)
                den = mp_factorial(n) * mp_factorial(n - k)
                c[k] += (num / den) * a[i] * b[j]
    return c

def phi_n(roots):
    n = len(roots)
    total = mpmath.mpf(0)
    for i in range(n):
        s = mpmath.mpf(0)
        for j in range(n):
            if j != i:
                s += 1 / (roots[i] - roots[j])
        total += s ** 2
    return total

# Edge case: n=3, eps=0.01, offset=0.5
n = 3
eps = mpmath.mpf('1') / 100
rp = [mpmath.mpf(0), eps, 2*eps]
rq = [mpmath.mpf('1')/2, mpmath.mpf('1')/2 + eps, mpmath.mpf('1')/2 + 2*eps]

print(f"p roots: {[mpmath.nstr(r, 10) for r in rp]}")
print(f"q roots: {[mpmath.nstr(r, 10) for r in rq]}")

a = poly_from_roots(rp)
b = poly_from_roots(rq)
c = finite_free_conv(a, b, n)

print(f"\nConvolution coefficients: {[mpmath.nstr(ci, 20) for ci in c]}")

# Find roots at high precision
roots_h = sorted(mpmath.polyroots(c, maxsteps=2000, extraprec=200),
                 key=lambda r: mpmath.re(r))
roots_h_real = [mpmath.re(r) for r in roots_h]
max_imag = max(abs(mpmath.im(r)) for r in roots_h)
print(f"Max |Im(root)|: {mpmath.nstr(max_imag, 10)}")
print(f"Conv roots: {[mpmath.nstr(r, 20) for r in roots_h_real]}")

pp = phi_n(rp)
pq = phi_n(rq)
ph = phi_n(roots_h_real)

inv_p = 1 / pp
inv_q = 1 / pq
inv_h = 1 / ph

margin = inv_h - inv_p - inv_q

print(f"\nPhi(p) = {mpmath.nstr(pp, 30)}")
print(f"Phi(q) = {mpmath.nstr(pq, 30)}")
print(f"Phi(h) = {mpmath.nstr(ph, 30)}")
print(f"\n1/Phi(h) = {mpmath.nstr(inv_h, 30)}")
print(f"1/Phi(p) + 1/Phi(q) = {mpmath.nstr(inv_p + inv_q, 30)}")
print(f"Margin = {mpmath.nstr(margin, 30)}")

if margin >= 0:
    print(f"\nVERDICT: PASS (margin >= 0)")
    # How many digits of precision in the margin?
    if margin > 0:
        log_margin = mpmath.log10(margin)
        log_rhs = mpmath.log10(inv_p + inv_q)
        rel_digits = -int(mpmath.log10(abs(margin / (inv_p + inv_q))))
        print(f"Margin / RHS = {mpmath.nstr(margin / (inv_p + inv_q), 15)}")
else:
    print(f"\nVERDICT: FAIL (margin < 0)")
    print(f"  |margin| = {mpmath.nstr(abs(margin), 15)}")
    print(f"  |margin|/RHS = {mpmath.nstr(abs(margin) / (inv_p + inv_q), 15)}")
    print(f"  This is at 10^{int(mpmath.log10(abs(margin)))} — below 300-digit precision?")

# Also check: is this EXACTLY equality? The n=3 case with equally-spaced roots
# on both sides might have algebraic structure
print(f"\n--- Algebraic analysis ---")
print(f"For n=3 with p roots 0, h, 2h and q roots c, c+h, c+2h:")
print(f"Both have gap^2 structure similar to n=2...")

# Check: for ANY equally-spaced triple, Phi_3 depends only on the spacing
# p(x) = (x)(x-h)(x-2h) = x^3 - 3hx^2 + 2h^2 x
# All roots equally spaced with gap h.
# Phi_3 = sum_i (sum_{j!=i} 1/(r_i-r_j))^2
# r0=0: 1/(-h) + 1/(-2h) = -3/(2h), squared = 9/(4h^2)
# r1=h: 1/h + 1/(-h) = 0, squared = 0
# r2=2h: 1/(2h) + 1/h = 3/(2h), squared = 9/(4h^2)
# Phi_3 = 18/(4h^2) = 9/(2h^2)
# 1/Phi_3 = 2h^2/9

h = eps
print(f"\nFor equally-spaced n=3 with gap h={mpmath.nstr(h, 10)}:")
print(f"  Phi_3 = 9/(2h^2) = {mpmath.nstr(9/(2*h**2), 20)}")
print(f"  Computed Phi(p) = {mpmath.nstr(pp, 20)}")
print(f"  Match: {mpmath.nstr(abs(pp - 9/(2*h**2)), 10)}")

# Convolution of two equally-spaced triples
# p: 0, h, 2h -> coeffs [1, -3h, 2h^2, 0]
# q: c, c+h, c+2h -> coeffs [1, -3(c+h), 2h^2+3ch+3c^2, ...]
# Actually let's just check if h ⊞_3 q is also equally spaced

gaps_h = [roots_h_real[i+1] - roots_h_real[i] for i in range(2)]
print(f"\n  Conv root gaps: {[mpmath.nstr(g, 20) for g in gaps_h]}")
print(f"  Gap ratio: {mpmath.nstr(gaps_h[1] / gaps_h[0], 20)}")
print(f"  Equally spaced: {abs(gaps_h[1] - gaps_h[0]) < mpmath.mpf(10)**(-100)}")
