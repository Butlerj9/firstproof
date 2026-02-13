"""
ce22_margin_minimize.py — Proper numerical minimization of the full margin M
on the valid (4-real-root) region.

Goal: Find the global minimum of M = 1/Phi4(h) - 1/Phi4(p) - 1/Phi4(q)
subject to all three polynomials having 4 simple real roots.

Key: Use gauge-fixing (sigma_h = 1) and bounded optimization.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import numpy as np
from scipy.optimize import minimize as sp_minimize, differential_evolution

SEP = "=" * 70
t0 = time.time()

def eval_1_over_phi4(s_val, b_val, cp_val):
    """Evaluate 1/Phi4 at (sigma, b, c') numerically.
    Returns (value, valid_flag)."""
    a_val = -s_val
    c_val = cp_val + s_val**2 / 12.0

    A = a_val**2 + 12*c_val
    B = 2*a_val**3 - 8*a_val*c_val + 9*b_val**2
    D = (16*a_val**4*c_val - 4*a_val**3*b_val**2 - 128*a_val**2*c_val**2
         + 144*a_val*b_val**2*c_val - 27*b_val**4 + 256*c_val**3)

    denom = 4 * A * B
    if abs(denom) < 1e-30:
        return 0.0, False

    inv_phi = -D / denom
    valid = (D > 1e-30) and (inv_phi > 1e-30)

    return inv_phi, valid

def margin(params):
    """Compute margin M. Returns (M, valid)."""
    w, b1, b2, c1, c2 = params
    # Gauge: sigma_h = 1, so sigma_1 = w, sigma_2 = 1-w
    s1 = w
    s2 = 1.0 - w

    f1, ok1 = eval_1_over_phi4(s1, b1, c1)
    f2, ok2 = eval_1_over_phi4(s2, b2, c2)
    fh, okh = eval_1_over_phi4(s1+s2, b1+b2, c1+c2)

    if not (ok1 and ok2 and okh):
        return None, False

    M = fh - f1 - f2
    return M, True

def obj_func(params):
    """Objective: minimize M (find most negative value)."""
    M, valid = margin(params)
    if not valid:
        return 1e10  # penalty
    return M

# ============================================================
print(SEP)
print("SECTION 1: Differential evolution on gauge-fixed domain")
print(SEP)
print("Gauge: sigma_h = sigma_1 + sigma_2 = 1")
print("Variables: w=sigma_1 in (0.01, 0.99), b1, b2, c1', c2'")
print()

# Bounds: w in (0.01, 0.99), b in (-0.5, 0.5), c' in (-0.05, 0.05)
bounds = [(0.01, 0.99),  # w
          (-0.5, 0.5),   # b1
          (-0.5, 0.5),   # b2
          (-0.05, 0.05), # c1'
          (-0.05, 0.05)] # c2'

result = differential_evolution(obj_func, bounds, seed=42,
                                maxiter=1000, tol=1e-14, polish=True,
                                popsize=30)
print("DE result: M = %.15e" % result.fun)
print("At: w=%.8f b1=%.8f b2=%.8f c1=%.10f c2=%.10f" % tuple(result.x))
M_check, valid = margin(result.x)
print("Valid: %s, M = %.15e" % (valid, M_check if M_check is not None else float('nan')))
w, b1, b2, c1, c2 = result.x
print("b-values: b1=%.8f b2=%.8f (both ~0? %s)" %
      (b1, b2, abs(b1) < 0.001 and abs(b2) < 0.001))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 2: Multiple scales (different sigma_h values)")
print(SEP)

for sigma_h in [0.5, 1.0, 2.0, 5.0, 10.0]:
    def obj_scaled(params):
        w, b1, b2, c1, c2 = params
        s1 = w * sigma_h
        s2 = (1-w) * sigma_h
        f1, ok1 = eval_1_over_phi4(s1, b1*sigma_h, c1*sigma_h**2)
        f2, ok2 = eval_1_over_phi4(s2, b2*sigma_h, c2*sigma_h**2)
        fh, okh = eval_1_over_phi4(s1+s2, (b1+b2)*sigma_h, (c1+c2)*sigma_h**2)
        if not (ok1 and ok2 and okh):
            return 1e10
        return fh - f1 - f2

    res = differential_evolution(obj_scaled, bounds, seed=42, maxiter=500, tol=1e-14)
    w, b1, b2, c1, c2 = res.x
    print("sigma_h=%.1f: min M = %.10e  w=%.4f b1=%.4f b2=%.4f c1=%.6f c2=%.6f  b~0: %s" %
          (sigma_h, res.fun, w, b1, b2, c1, c2,
           abs(b1) < 0.001 and abs(b2) < 0.001))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Multi-start Nelder-Mead (1000 random starts, bounded)")
print(SEP)

np.random.seed(777)
best_M = float('inf')
best_p = None
n_valid_converged = 0
n_b_nonzero = 0

for run in range(1000):
    w0 = np.random.uniform(0.05, 0.95)
    b10 = np.random.uniform(-0.3, 0.3)
    b20 = np.random.uniform(-0.3, 0.3)
    c10 = np.random.uniform(-0.03, 0.03)
    c20 = np.random.uniform(-0.03, 0.03)

    x0 = [w0, b10, b20, c10, c20]
    try:
        res = sp_minimize(obj_func, x0, method='Nelder-Mead',
                         options={'maxiter': 5000, 'xatol': 1e-12, 'fatol': 1e-15})
        M_val, ok = margin(res.x)
        if ok and M_val is not None:
            n_valid_converged += 1
            if abs(res.x[1]) > 0.001 or abs(res.x[2]) > 0.001:
                n_b_nonzero += 1
            if M_val < best_M:
                best_M = M_val
                best_p = res.x
    except:
        continue

print("Converged to valid region: %d / 1000" % n_valid_converged)
print("Converged with b≠0: %d / %d" % (n_b_nonzero, n_valid_converged))
print("Best M found: %.15e" % best_M)
if best_p is not None:
    print("At: w=%.8f b1=%.8f b2=%.8f c1=%.10f c2=%.10f" % tuple(best_p))
    print("b values: b1=%.8f b2=%.8f" % (best_p[1], best_p[2]))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 4: Extreme asymmetric search")
print(SEP)
# Test cases where one input is much larger than the other

np.random.seed(444)
best_asym = float('inf')
for run in range(500):
    w0 = np.random.choice([np.random.uniform(0.01, 0.1), np.random.uniform(0.9, 0.99)])
    b10 = np.random.uniform(-0.4, 0.4)
    b20 = np.random.uniform(-0.4, 0.4)
    c10 = np.random.uniform(-0.04, 0.04)
    c20 = np.random.uniform(-0.04, 0.04)

    x0 = [w0, b10, b20, c10, c20]
    try:
        res = sp_minimize(obj_func, x0, method='Nelder-Mead',
                         options={'maxiter': 5000, 'xatol': 1e-12, 'fatol': 1e-15})
        M_val, ok = margin(res.x)
        if ok and M_val is not None and M_val < best_asym:
            best_asym = M_val
    except:
        continue

print("Best M (asymmetric): %.15e" % best_asym)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 5: Gradient analysis at equality manifold")
print(SEP)
# On the equality manifold: b1=b2=0, c1'=c2'=0, any w.
# M = 0 here. Check the Hessian of M in the (b1,b2,c1,c2) directions.

from scipy.optimize import approx_fprime

def M_at_b_c(bc_params, w):
    b1, b2, c1, c2 = bc_params
    return obj_func([w, b1, b2, c1, c2])

for w in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
    # Numerical Hessian at (0,0,0,0)
    eps = 1e-5
    n = 4
    H = np.zeros((n, n))
    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    for i in range(n):
        def fi(x):
            return M_at_b_c(x, w)
        grad_plus = approx_fprime(x0 + eps*np.eye(n)[i], fi, 1e-8)
        grad_minus = approx_fprime(x0 - eps*np.eye(n)[i], fi, 1e-8)
        H[i, :] = (grad_plus - grad_minus) / (2*eps)

    # Symmetrize
    H = (H + H.T) / 2
    eigvals = np.linalg.eigvalsh(H)
    print("w=%.1f: Hessian eigenvalues = [%s]  min=%.6e  PSD: %s" %
          (w, ", ".join("%.4e" % e for e in eigvals), min(eigvals),
           min(eigvals) >= -1e-8))

sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time() - t0))
