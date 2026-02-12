"""
P04 CE-5c: Investigate equality cases in the Phi_n inequality.

Key discovery from CE-5b: for n=3 equally-spaced roots, EXACT EQUALITY holds.
This script verifies:
1. Equality for n=3 equally-spaced with DIFFERENT gaps
2. Whether equality extends to n=4,5 equally-spaced
3. General pattern: when does equality hold?
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mpmath
mpmath.mp.dps = 200

print("P04 CE-5c: Equality cases in Phi_n inequality")
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


# ============================================================
# TEST 1: n=3 equally-spaced with different gaps
# ============================================================
print("\nTEST 1: n=3 equally-spaced, different gaps")
print("-" * 60)

for h1, h2 in [(1, 1), (1, 2), (1, 3), (2, 3), (1, 10)]:
    h1 = mpmath.mpf(h1) / 10
    h2 = mpmath.mpf(h2) / 10

    rp = [mpmath.mpf(0), h1, 2*h1]
    rq = [mpmath.mpf(5), mpmath.mpf(5) + h2, mpmath.mpf(5) + 2*h2]

    a = poly_from_roots(rp)
    b = poly_from_roots(rq)
    c = finite_free_conv(a, b, 3)
    rh = sorted([mpmath.re(r) for r in mpmath.polyroots(c, maxsteps=1000, extraprec=100)])

    pp = phi_n(rp)
    pq = phi_n(rq)
    ph = phi_n(rh)

    margin = 1/ph - 1/pp - 1/pq
    rhs = 1/pp + 1/pq

    # Check if conv is equally spaced
    gaps = [rh[i+1] - rh[i] for i in range(2)]
    eq_spaced = abs(gaps[1] - gaps[0]) < mpmath.mpf(10)**(-100)

    # Check gap^2 additivity
    g_sq = (gaps[0])**2
    predicted_g_sq = h1**2 + h2**2
    gap_additive = abs(g_sq - predicted_g_sq) < mpmath.mpf(10)**(-100)

    print(f"  h1={mpmath.nstr(h1,3)}, h2={mpmath.nstr(h2,3)}: "
          f"margin={mpmath.nstr(margin, 8)}, eq_spaced={eq_spaced}, "
          f"gap^2_additive={gap_additive}, "
          f"conv_gap={mpmath.nstr(gaps[0], 10)}, "
          f"sqrt(h1^2+h2^2)={mpmath.nstr(mpmath.sqrt(h1**2+h2**2), 10)}")


# ============================================================
# TEST 2: n=4 equally-spaced
# ============================================================
print(f"\nTEST 2: n=4 equally-spaced roots")
print("-" * 60)

for h1, h2 in [(1, 1), (1, 2), (1, 3), (2, 5)]:
    h1 = mpmath.mpf(h1) / 10
    h2 = mpmath.mpf(h2) / 10
    n = 4

    rp = [mpmath.mpf(i) * h1 for i in range(n)]
    rq = [mpmath.mpf(10) + mpmath.mpf(i) * h2 for i in range(n)]

    a = poly_from_roots(rp)
    b = poly_from_roots(rq)
    c = finite_free_conv(a, b, n)
    rh = sorted([mpmath.re(r) for r in mpmath.polyroots(c, maxsteps=1000, extraprec=100)])

    pp = phi_n(rp)
    pq = phi_n(rq)
    ph = phi_n(rh)

    margin = 1/ph - 1/pp - 1/pq
    rhs = 1/pp + 1/pq

    # Check if conv is equally spaced
    gaps = [rh[i+1] - rh[i] for i in range(n-1)]
    max_gap_dev = max(abs(gaps[i] - gaps[0]) for i in range(1, len(gaps)))

    rel_margin = margin / rhs if rhs > 0 else margin

    print(f"  h1={mpmath.nstr(h1,3)}, h2={mpmath.nstr(h2,3)}: "
          f"margin={mpmath.nstr(margin, 10)}, "
          f"rel_margin={mpmath.nstr(rel_margin, 8)}, "
          f"max_gap_dev={mpmath.nstr(max_gap_dev, 5)}")


# ============================================================
# TEST 3: n=5 equally-spaced
# ============================================================
print(f"\nTEST 3: n=5 equally-spaced roots")
print("-" * 60)

for h1, h2 in [(1, 1), (1, 2), (2, 3)]:
    h1 = mpmath.mpf(h1) / 10
    h2 = mpmath.mpf(h2) / 10
    n = 5

    rp = [mpmath.mpf(i) * h1 for i in range(n)]
    rq = [mpmath.mpf(10) + mpmath.mpf(i) * h2 for i in range(n)]

    a = poly_from_roots(rp)
    b = poly_from_roots(rq)
    c = finite_free_conv(a, b, n)
    rh = sorted([mpmath.re(r) for r in mpmath.polyroots(c, maxsteps=1000, extraprec=100)])

    pp = phi_n(rp)
    pq = phi_n(rq)
    ph = phi_n(rh)

    margin = 1/ph - 1/pp - 1/pq
    rhs = 1/pp + 1/pq

    gaps = [rh[i+1] - rh[i] for i in range(n-1)]
    max_gap_dev = max(abs(gaps[i] - gaps[0]) for i in range(1, len(gaps)))

    rel_margin = margin / rhs if rhs > 0 else margin

    print(f"  h1={mpmath.nstr(h1,3)}, h2={mpmath.nstr(h2,3)}: "
          f"margin={mpmath.nstr(margin, 10)}, "
          f"rel_margin={mpmath.nstr(rel_margin, 8)}, "
          f"max_gap_dev={mpmath.nstr(max_gap_dev, 5)}")


# ============================================================
# TEST 4: Phi_n formula for equally-spaced roots
# ============================================================
print(f"\nTEST 4: Phi_n for equally-spaced roots (formula check)")
print("-" * 60)

for n in [2, 3, 4, 5, 6]:
    h = mpmath.mpf('1') / 7
    roots = [mpmath.mpf(i) * h for i in range(n)]
    phi = phi_n(roots)
    inv_phi = 1/phi

    # For n=2: Phi_2 = 2/h^2, 1/Phi_2 = h^2/2
    # For n=3: Phi_3 = 9/(2h^2), 1/Phi_3 = 2h^2/9
    # General pattern?
    ratio = inv_phi / h**2  # Should be a rational constant depending on n

    print(f"  n={n}: Phi = {mpmath.nstr(phi, 15)}, "
          f"1/Phi = {mpmath.nstr(inv_phi, 15)}, "
          f"1/(Phi*h^2) = {mpmath.nstr(1/(phi*h**2), 15)}, "
          f"(1/Phi)/h^2 = {mpmath.nstr(ratio, 15)}")


# ============================================================
# TEST 5: 1/Phi_n(equally-spaced, gap h) = C_n * h^2
# ============================================================
print(f"\nTEST 5: Determine C_n in 1/Phi_n = C_n * h^2")
print("-" * 60)

for n in [2, 3, 4, 5, 6, 7, 8]:
    h = mpmath.mpf(1)
    roots = [mpmath.mpf(i) * h for i in range(n)]
    phi = phi_n(roots)
    C_n = 1 / (phi * h**2)

    # Check: is C_n = 1/n (or some other simple formula)?
    print(f"  n={n}: C_n = {mpmath.nstr(C_n, 20)}, "
          f"C_n * n = {mpmath.nstr(C_n * n, 15)}, "
          f"C_n * n^2 = {mpmath.nstr(C_n * n**2, 15)}, "
          f"C_n * n*(n-1) = {mpmath.nstr(C_n * n * (n-1), 15)}")


# ============================================================
# TEST 6: Gap-squared additivity for general n
# ============================================================
print(f"\nTEST 6: Gap additivity for equally-spaced under box_n")
print("-" * 60)

for n in [3, 4, 5]:
    h1 = mpmath.mpf('3') / 10
    h2 = mpmath.mpf('5') / 10

    rp = [mpmath.mpf(i) * h1 for i in range(n)]
    rq = [mpmath.mpf(10) + mpmath.mpf(i) * h2 for i in range(n)]

    a = poly_from_roots(rp)
    b = poly_from_roots(rq)
    c = finite_free_conv(a, b, n)
    rh = sorted([mpmath.re(r) for r in mpmath.polyroots(c, maxsteps=1000, extraprec=100)])

    gaps = [rh[i+1] - rh[i] for i in range(n-1)]
    max_gap_dev = max(abs(gaps[i] - gaps[0]) for i in range(1, len(gaps)))
    mean_gap = sum(gaps) / len(gaps)

    predicted_gap = mpmath.sqrt(h1**2 + h2**2)

    print(f"  n={n}: conv gap = {mpmath.nstr(mean_gap, 20)}, "
          f"sqrt(h1^2+h2^2) = {mpmath.nstr(predicted_gap, 20)}, "
          f"eq_spaced = {max_gap_dev < mpmath.mpf(10)**(-50)}, "
          f"gap_match = {abs(mean_gap - predicted_gap) < mpmath.mpf(10)**(-50)}")

print(f"\n{'='*70}")
print("SUMMARY")
print("=" * 70)
