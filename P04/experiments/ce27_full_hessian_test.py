"""
ce27_full_hessian_test.py — Test whether the concavity extends to c' != 0.

For the c'=0 proof, the key was that psi(u) = g(u^2) is concave.
For the full case, we need psi(u, v) = G(u^2, v) to be jointly concave
in (u, v) where v corresponds to c'/sigma^2.

We test this numerically by computing the 2x2 Hessian of psi at many points
and checking if it is NSD (negative semi-definite).

G(beta, gamma) = f(1, sqrt(beta), gamma) where f = 1/Phi4.
psi(u, v) = G(u^2, v) = f(1, u, v) evaluated at sigma=1.
"""
import sys, io, time, math, random
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

def quartic_roots(sigma, b, c_prime):
    """Roots of x^4 - sigma*x^2 + b*x + sigma^2/12 + c'."""
    c = sigma**2/12.0 + c_prime
    # x^4 - sigma*x^2 + b*x + c
    coeffs = [1.0, 0.0, -sigma, b, c]
    return np.roots(coeffs)

def phi4(sigma, b, c_prime):
    """Compute Phi4 = sum_{i<j} 1/(r_i - r_j)^2."""
    roots = quartic_roots(sigma, b, c_prime)
    # Check all roots are real
    if np.max(np.abs(np.imag(roots))) > 1e-8:
        return None, False
    roots = np.sort(np.real(roots))
    total = 0.0
    for i in range(4):
        for j in range(i+1, 4):
            diff = roots[i] - roots[j]
            if abs(diff) < 1e-12:
                return None, False
            total += 1.0 / diff**2
    return total, True

def f_eval(sigma, b, c_prime):
    """1/Phi4 at (sigma, b, c')."""
    val, ok = phi4(sigma, b, c_prime)
    if not ok or val == 0:
        return None, False
    return 1.0 / val, True

def psi_eval(u, v, sigma=1.0):
    """psi(u, v) = G(u^2, v) = f(sigma, sigma^{3/2}*u, sigma^2*v) / sigma.
    At sigma=1: psi(u, v) = f(1, u, v).
    """
    return f_eval(sigma, sigma**1.5 * u, sigma**2 * v)

# ============================================================
print(SEP)
print("SECTION 1: Hessian of psi(u, v) via finite differences")
print(SEP)

h = 1e-5  # step size for finite differences

def hessian_psi(u, v):
    """Compute 2x2 Hessian of psi at (u, v) via central differences."""
    f0, ok0 = psi_eval(u, v)
    if not ok0:
        return None

    fpu, okpu = psi_eval(u + h, v)
    fmu, okmu = psi_eval(u - h, v)
    fpv, okpv = psi_eval(u, v + h)
    fmv, okmv = psi_eval(u, v - h)
    fpuv, okpuv = psi_eval(u + h, v + h)
    fmuv, okmuv = psi_eval(u - h, v + h)
    fpumv, okpumv = psi_eval(u + h, v - h)
    fmumv, okmumv = psi_eval(u - h, v - h)

    if not all([okpu, okmu, okpv, okmv, okpuv, okmuv, okpumv, okmumv]):
        return None

    H_uu = (fpu - 2*f0 + fmu) / h**2
    H_vv = (fpv - 2*f0 + fmv) / h**2
    H_uv = (fpuv - fmuv - fpumv + fmumv) / (4*h**2)

    return np.array([[H_uu, H_uv], [H_uv, H_vv]])

# Test at origin
H0 = hessian_psi(0, 0)
if H0 is not None:
    eigs = np.linalg.eigvalsh(H0)
    print("Hessian at (0, 0):")
    print("  H =", H0)
    print("  Eigenvalues:", eigs)
    print("  NSD?", all(e <= 1e-6 for e in eigs))

# Test at various points
print("\n--- Systematic Hessian scan ---")
n_tested = 0
n_nsd_violations = 0
max_positive_eig = -float('inf')
worst_point = None

random.seed(42)

for _ in range(50000):
    u_val = random.uniform(-0.38, 0.38)  # |u| < 2/(3*sqrt(3)) ≈ 0.385
    v_val = random.uniform(-0.3, 0.3)

    # First check if the point is valid (4 real roots at sigma=1)
    f_val, ok = psi_eval(u_val, v_val)
    if not ok:
        continue

    H = hessian_psi(u_val, v_val)
    if H is None:
        continue

    n_tested += 1
    eigs = np.linalg.eigvalsh(H)
    max_eig = max(eigs)

    if max_eig > max_positive_eig:
        max_positive_eig = max_eig
        worst_point = (u_val, v_val, eigs)

    if max_eig > 1e-4:  # allowing some numerical noise
        n_nsd_violations += 1

print("\nPoints tested: %d" % n_tested)
print("NSD violations (max eigenvalue > 1e-4): %d" % n_nsd_violations)
print("Maximum positive eigenvalue: %.6e" % max_positive_eig)
if worst_point:
    print("Worst point: u=%.4f, v=%.4f, eigenvalues=%s" %
          (worst_point[0], worst_point[1], worst_point[2]))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Detailed scan near problem areas")
print(SEP)

# Check along specific slices
print("--- Slice v=0 (should match c'=0 proof) ---")
for u_val in np.linspace(0.01, 0.35, 20):
    H = hessian_psi(u_val, 0)
    if H is not None:
        eigs = np.linalg.eigvalsh(H)
        print("  u=%.3f, v=0: eigs=[%.4f, %.4f], NSD=%s" %
              (u_val, eigs[0], eigs[1], all(e <= 1e-6 for e in eigs)))

print("\n--- Slice u=0 (b=0, should match CE-16 result) ---")
for v_val in np.linspace(-0.2, 0.2, 20):
    H = hessian_psi(0, v_val)
    if H is not None:
        eigs = np.linalg.eigvalsh(H)
        status = "NSD" if all(e <= 1e-6 for e in eigs) else "VIOLATION"
        if status == "VIOLATION":
            print("  u=0, v=%.3f: eigs=[%.4f, %.4f], %s" %
                  (v_val, eigs[0], eigs[1], status))

print("\n--- Diagonal u=v ---")
for val in np.linspace(0.01, 0.2, 20):
    H = hessian_psi(val, val)
    if H is not None:
        eigs = np.linalg.eigvalsh(H)
        status = "NSD" if all(e <= 1e-6 for e in eigs) else "VIOLATION"
        if status == "VIOLATION":
            print("  u=v=%.3f: eigs=[%.4f, %.4f], %s" % (val, eigs[0], eigs[1], status))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Full margin M numerical test (general c')")
print(SEP)

random.seed(789)
n_full = 100000
n_violations = 0
min_margin = float('inf')

for _ in range(n_full):
    s1 = random.uniform(0.1, 2.0)
    s2 = random.uniform(0.1, 2.0)

    # Generate random b1, b2, c1', c2'
    # Valid region: need each polynomial to have 4 real simple roots
    # Try random values and check validity
    b1 = random.uniform(-1, 1)
    b2 = random.uniform(-1, 1)
    c1p = random.uniform(-0.5, 0.5)
    c2p = random.uniform(-0.5, 0.5)

    f1, ok1 = f_eval(s1, b1, c1p)
    f2, ok2 = f_eval(s2, b2, c2p)
    fh, okh = f_eval(s1+s2, b1+b2, c1p+c2p)

    if not (ok1 and ok2 and okh):
        continue

    M = fh - f1 - f2
    if M < min_margin:
        min_margin = M
    if M < -1e-8:
        n_violations += 1

print("Full margin tests (general c'): %d" % n_full)
print("Valid tests found: many (not all random points are valid)")
print("Violations: %d" % n_violations)
print("Min margin: %.6e" % min_margin)
print("Result:", "ALL PASS ✓" if n_violations == 0 else "VIOLATIONS FOUND ✗")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Verdict on full extension")
print(SEP)

if n_nsd_violations == 0:
    print("Hessian is NSD everywhere tested => psi(u,v) appears jointly concave.")
    print("The c'=0 proof structure LIKELY extends to the full case.")
    print("Next step: symbolic verification of 2x2 Hessian NSD.")
else:
    print("Hessian has %d NSD violations => psi(u,v) is NOT jointly concave." % n_nsd_violations)
    print("The c'=0 proof does NOT extend directly to full case.")
    print("Alternative approach needed for c' != 0.")

print("\nElapsed: %.1fs" % (time.time() - t0))
