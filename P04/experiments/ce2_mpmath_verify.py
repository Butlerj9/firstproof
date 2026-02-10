"""
High-precision verification of CE-2 candidate counterexamples using mpmath.

The CE-2 failures were:
- n=4, ε=1e-4: clustered roots (0, 0.0001, 0.0002, 0.0003) vs (0.5, 0.5001, 0.5002, 0.5003)
- n=5, ε=1e-4: clustered roots (0, ..., 0.0004) vs (0.5, ..., 0.5004)
- n=6, ε=1e-4: clustered roots (0, ..., 0.0005) vs (0.5, ..., 0.5005)

All had margins of order -1e-9 to -1e-10. Need to check at 50+ digits.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import mpmath
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mpmath'])
    import mpmath

# Set high precision
mpmath.mp.dps = 80  # 80 decimal digits

def mp_factorial(n):
    return mpmath.factorial(n)

def mp_poly_from_roots(roots):
    """Build polynomial coefficients from roots using mpmath."""
    n = len(roots)
    # a_0 = 1, a_k = (-1)^k * e_k(roots) where e_k is elementary symmetric polynomial
    coeffs = [mpmath.mpf(1)]
    for k in range(1, n + 1):
        # Compute e_k via recurrence
        # Actually, build polynomial by multiplying (x - r_i) factors
        pass

    # Build via convolution: start with [1], multiply by [1, -r_i] for each root
    poly = [mpmath.mpf(1)]
    for r in roots:
        new_poly = [mpmath.mpf(0)] * (len(poly) + 1)
        for i in range(len(poly)):
            new_poly[i] += poly[i]
            new_poly[i + 1] -= poly[i] * r
        poly = new_poly
    return poly  # [a_0=1, a_1, ..., a_n] in descending power

def mp_finite_free_conv(a, b, n):
    """Compute p ⊞_n q coefficients at high precision."""
    c = [mpmath.mpf(0)] * (n + 1)
    for k in range(n + 1):
        s = mpmath.mpf(0)
        for i in range(k + 1):
            j = k - i
            if i <= n and j <= n:
                num = mp_factorial(n - i) * mp_factorial(n - j)
                den = mp_factorial(n) * mp_factorial(n - k)
                s += (num / den) * a[i] * b[j]
        c[k] = s
    return c

def mp_roots(coeffs):
    """Find roots of polynomial using mpmath polyroots with high maxsteps."""
    try:
        roots = mpmath.polyroots(coeffs, maxsteps=500, extraprec=100)
    except mpmath.libmp.libhyper.NoConvergence:
        # Try even harder
        try:
            roots = mpmath.polyroots(coeffs, maxsteps=2000, extraprec=200)
        except mpmath.libmp.libhyper.NoConvergence:
            print("  WARNING: polyroots failed to converge even with maxsteps=2000")
            # Fall back to companion matrix via numpy, then refine
            import numpy as np
            approx = np.roots([float(c) for c in coeffs])
            roots = [mpmath.findroot(lambda x: mpmath.polyval(coeffs, x),
                                     mpmath.mpc(float(r.real), float(r.imag)))
                     for r in approx]
    return sorted(roots, key=lambda r: mpmath.re(r))

def mp_phi_n(roots):
    """Compute Φ_n at high precision."""
    n = len(roots)
    # Check for multiple roots
    for i in range(n):
        for j in range(i + 1, n):
            if abs(roots[i] - roots[j]) < mpmath.mpf(10) ** (-60):
                return mpmath.inf

    total = mpmath.mpf(0)
    for i in range(n):
        s = mpmath.mpf(0)
        for j in range(n):
            if j != i:
                s += 1 / (roots[i] - roots[j])
        total += s ** 2
    return total

def verify_case(n, eps, offset_q=0.5, label=""):
    """Verify a clustered-roots case at high precision."""
    print(f"\n{'='*60}")
    print(f"Verifying: n={n}, ε={eps}, {label}")
    print(f"{'='*60}")

    # Build roots
    roots_p = [mpmath.mpf(i) * mpmath.mpf(eps) for i in range(n)]
    roots_q = [mpmath.mpf(i) * mpmath.mpf(eps) + mpmath.mpf(offset_q) for i in range(n)]

    print(f"p roots: {[float(r) for r in roots_p]}")
    print(f"q roots: {[float(r) for r in roots_q]}")

    # Build polynomial coefficients
    a = mp_poly_from_roots(roots_p)
    b = mp_poly_from_roots(roots_q)

    # Compute convolution
    c = mp_finite_free_conv(a, b, n)
    print(f"Convolution coefficients: {[float(ci) for ci in c]}")

    # Find roots of convolution
    roots_conv = mp_roots(c)

    # Check if roots are real
    max_imag = max(abs(mpmath.im(r)) for r in roots_conv)
    print(f"Max |Im(root)|: {float(max_imag):.4e}")

    # Take real parts
    roots_conv_real = sorted([mpmath.re(r) for r in roots_conv])
    print(f"Conv roots (real parts): {[float(r) for r in roots_conv_real]}")

    # Min gap
    gaps = [abs(roots_conv_real[i+1] - roots_conv_real[i]) for i in range(n-1)]
    min_gap = min(gaps)
    print(f"Min root gap in conv: {float(min_gap):.10e}")

    # Compute Φ_n values
    phi_p = mp_phi_n(roots_p)
    phi_q = mp_phi_n(roots_q)

    if max_imag > mpmath.mpf(10) ** (-20):
        print(f"WARNING: Conv roots have significant imaginary parts!")
        print(f"  MSS guarantees real-rootedness, so this indicates numerical issue in root-finding,")
        print(f"  OR the coefficient formula produces non-real-rooted output for these inputs.")
        print(f"  Computing Φ_n on real parts anyway...")

    phi_conv = mp_phi_n(roots_conv_real)

    print(f"\nΦ_n(p) = {float(phi_p):.15e}")
    print(f"Φ_n(q) = {float(phi_q):.15e}")
    print(f"Φ_n(p⊞q) = {float(phi_conv) if phi_conv != mpmath.inf else 'inf'}")

    # Compute inequality
    inv_p = 0 if phi_p == mpmath.inf else 1 / phi_p
    inv_q = 0 if phi_q == mpmath.inf else 1 / phi_q
    inv_conv = 0 if phi_conv == mpmath.inf else 1 / phi_conv

    lhs = inv_conv
    rhs = inv_p + inv_q
    margin = lhs - rhs

    print(f"\n1/Φ(p⊞q) = {float(lhs):.20e}")
    print(f"1/Φ(p) + 1/Φ(q) = {float(rhs):.20e}")
    print(f"Margin (LHS - RHS) = {float(margin):.20e}")

    if margin >= 0:
        print(f"STATUS: PASS (margin >= 0)")
    else:
        rel_margin = float(margin / rhs) if rhs != 0 else float('nan')
        print(f"STATUS: FAIL (margin < 0, relative = {rel_margin:.6e})")

    # Also check: is the polynomial p ⊞_n q actually real-rooted?
    # Verify by checking discriminant sign, or just checking all roots
    all_real = all(abs(mpmath.im(r)) < mpmath.mpf(10) ** (-40) for r in roots_conv)
    print(f"\nAll conv roots real (|Im| < 1e-40): {all_real}")

    return float(margin)


# ============================================================
# VERIFY ALL CE-2 CANDIDATE COUNTEREXAMPLES
# ============================================================
print("P04 CE-2 mpmath verification (80-digit precision)")
print("=" * 60)

results = {}

for n in [4, 5, 6]:
    m = verify_case(n, "0.0001", 0.5, f"clustered n={n}")
    results[n] = m

# Also check n=3 with even smaller ε
for n in [3, 4]:
    for eps_str, eps_val in [("1e-6", "0.000001"), ("1e-8", "0.00000001")]:
        m = verify_case(n, eps_val, 0.5, f"clustered n={n} ε={eps_str}")
        results[(n, eps_str)] = m

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
for key, margin in results.items():
    status = "PASS" if margin >= 0 else "FAIL"
    print(f"  {key}: margin = {margin:.10e} [{status}]")

all_pass = all(m >= -1e-50 for m in results.values())
print(f"\nOVERALL: {'ALL PASS — CE-2 failures were numerical artifacts' if all_pass else 'REAL COUNTEREXAMPLE CONFIRMED'}")
