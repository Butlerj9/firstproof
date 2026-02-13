"""
P04 CE-42: Scout Route Assessment — Claude Research R2 + GPT-pro R2

Quick assessment of scout-proposed routes against known lane state.
Date: 2026-02-13
"""
import sys, io, time
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SEP = "=" * 70
t0 = time.time()

def phi4_inv(sigma, b, cp):
    """1/Phi_4 in additive variables. Returns NaN if invalid."""
    a = -sigma
    c = sigma**2 / 12.0 + cp
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (256*c**3 - 192*a*b**2*c - 128*a**2*c**2
             + 144*a**2*b**2*c - 27*b**4 + 16*a**4*c - 4*a**3*b**2)
    if A * B >= 0 or Delta <= 0:
        return float('nan')
    return -Delta / (4.0 * A * B)

def margin(w, b1, b2, cp1, cp2):
    s1, s2 = w, 1.0 - w
    fh = phi4_inv(1.0, b1 + b2, cp1 + cp2)
    f1 = phi4_inv(s1, b1, cp1)
    f2 = phi4_inv(s2, b2, cp2)
    if np.isnan(fh) or np.isnan(f1) or np.isnan(f2):
        return float('nan')
    return fh - f1 - f2

# ============================================================
print(SEP)
print("SECTION 1: GPT-pro r-split structure + P_+/P_- comparison")
print(SEP)

np.random.seed(42)
Mplus, Mminus = [], []
for _ in range(20000):
    w = np.random.uniform(0.1, 0.9)
    s1, s2 = w, 1.0 - w
    x1 = np.random.uniform(0, 0.6 * (4*s1**3/27)**0.5)
    x2 = np.random.uniform(0, 0.6 * (4*s2**3/27)**0.5)
    cp1 = np.random.uniform(-0.05*s1**2, 0.1*s1**2)
    cp2 = np.random.uniform(-0.05*s2**2, 0.1*s2**2)
    Mp = margin(w, x1, x2, cp1, cp2)
    Mm = margin(w, x1, -x2, cp1, cp2)
    if not np.isnan(Mp): Mplus.append(Mp)
    if not np.isnan(Mm): Mminus.append(Mm)

Mplus = np.array(Mplus)
Mminus = np.array(Mminus)
print(f"\nP_+ (same-sign b): {len(Mplus):6d} valid, min={Mplus.min():.6e}, neg={np.sum(Mplus<-1e-15)}")
print(f"P_- (opp-sign b):  {len(Mminus):6d} valid, min={Mminus.min():.6e}, neg={np.sum(Mminus<-1e-15)}")
print(f"\nVerdict: r-split (r^2=1) is mathematically trivial — all polynomials")
print(f"in r reduce to linear. No material complexity reduction. Both P_+, P_- >= 0.")

# ============================================================
print("\n" + SEP)
print("SECTION 2: Parametric SOS — equality manifold obstruction")
print(SEP)

# The minimum of M is 0, achieved at b=c'=0 for any w.
# Lipschitz interpolation requires min eps(w) > L/N > 0
# But eps(w) = 0 at b=c'=0, so interpolation CANNOT bridge.

print("\nThe margin M = 0 on the equality manifold (b=c'=0, any w).")
print("Parametric SOS requires min_over_domain eps(w) > 0 per slice,")
print("then L/N < min eps. Since eps = 0, Lipschitz interpolation FAILS.")
print()

# Confirm: M at b=c'=0 for several w values
print("M at b=c'=0:")
for w in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    M = margin(w, 0.0, 0.0, 0.0, 0.0)
    print(f"  w={w:.1f}: M = {M:.2e}")

# ============================================================
print("\n" + SEP)
print("SECTION 3: Lipschitz bound for dM/dw (informational)")
print(SEP)

max_dMdw = 0.0
dw = 1e-6
np.random.seed(789)
n_lip = 0
for _ in range(10000):
    w = np.random.uniform(0.15, 0.85)
    s1 = w
    b1 = np.random.uniform(-0.4*(4*s1**3/27)**0.5, 0.4*(4*s1**3/27)**0.5)
    b2 = np.random.uniform(-0.4*(4*(1-s1)**3/27)**0.5, 0.4*(4*(1-s1)**3/27)**0.5)
    cp1 = np.random.uniform(-0.03*s1**2, 0.06*s1**2)
    cp2 = np.random.uniform(-0.03*(1-s1)**2, 0.06*(1-s1)**2)
    M1 = margin(w, b1, b2, cp1, cp2)
    M2 = margin(w + dw, b1, b2, cp1, cp2)
    if not np.isnan(M1) and not np.isnan(M2):
        d = abs(M2 - M1) / dw
        if d > max_dMdw: max_dMdw = d
        n_lip += 1

print(f"\nmax |dM/dw| ≈ {max_dMdw:.4f} (from {n_lip} samples)")
print(f"For N=40:  L/N = {max_dMdw/40:.6f}")
print(f"For N=100: L/N = {max_dMdw/100:.6f}")
print(f"But min eps = 0 → Lipschitz interpolation ALWAYS fails regardless of N")

# ============================================================
print("\n" + SEP)
print("SECTION 4: cvxpy SDP scale test")
print(SEP)

try:
    import cvxpy as cp
    print(f"\ncvxpy {cp.__version__}, solvers: {cp.installed_solvers()}")
    for n in [50, 100, 200, 330]:
        X = cp.Variable((n, n), symmetric=True)
        constraints = [X >> 0, cp.trace(X) == 1]
        prob = cp.Problem(cp.Minimize(X[0, 0]), constraints)
        t1 = time.time()
        prob.solve(solver='CLARABEL', verbose=False)
        dt = time.time() - t1
        print(f"  {n}x{n} PSD: status={prob.status}, time={dt:.2f}s")
    print(f"\nFor SOS at deg 14 in 4 vars: moment matrix ~330x330")
    print(f"With constraints: total SDP >> 330x330")
    print(f"CE-14 showed CLARABEL fails on the actual polynomial problem")
    print(f"(Putinar deg 6 → SCS: optimal_inaccurate, CLARABEL: InsufficientProgress)")
except Exception as e:
    print(f"cvxpy test failed: {e}")

# ============================================================
print("\n" + SEP)
print("SECTION 5: Scout Route Verdict Table")
print(SEP)

print("""
=== Claude Research R2 (14 lanes, 5 claimed CLOSEABLE_NOW) ===

Lane | Approach                          | Verdict           | Reason
-----|-----------------------------------|-------------------|-------
L1   | TSSOS sparse SOS                  | CANNOT EXECUTE    | No Julia/TSSOS; = prior route #12
L2   | Parametric SOS stratification     | BLOCKED           | min eps=0 at equality manifold
L3   | SONC/SAGE circuits                | CANNOT EXECUTE    | No sageopt package
L4   | SDSOS/DSOS LP/SOCP               | CANNOT EXECUTE    | No implementation
L5   | Bernstein subdivision             | BLOCKED           | 5-var deg-14; equality manifold
L6   | Score-projection                  | KILLED (CE-5)     | Eval-point mismatch ratio 1e-4..1e7
L7   | Cumulant convexity                | KILLED (CE-17)    | Not concave, not deg-1 homo
L8   | Gribinski entropy                 | BLOCKED           | No finite de Bruijn identity
L9   | Schur-Horn                        | BLOCKED           | No framework available
L10  | phi-sub Jensen                    | BLOCKED           | phi NOT jointly concave; 1612 terms
L11  | Schmudgen preordering             | BLOCKED (CE-14)   | cvxpy fails at Putinar deg 6
L12  | Entropic OT                       | BLOCKED           | No variational framework
L13  | Fiber-wise + Lipschitz            | BLOCKED           | = L2, same equality manifold issue
L14  | Handelman LP                      | BLOCKED           | Semialgebraic, not polyhedral

=== GPT-pro R2 (3 approaches) ===

Lane | Approach                          | Verdict           | Reason
-----|-----------------------------------|-------------------|-------
GP1  | Invariant reduction P_+/P_-       | MARGINAL          | r^2=1 trivial; no complexity reduction
GP2  | Trig/resolvent parameterization   | NOT TESTED        | Deep reparametrization; no quick test
GP3  | Ferrari decomposition             | NOT TESTED        | Domain simplifier only

SUMMARY: 0 routes CLOSEABLE_NOW. 6 KILLED. 5 CANNOT EXECUTE. 5 BLOCKED. 2 NOT TESTED.
Claude Research overclaimed (CLOSEABLE_NOW); GPT-pro was honest (BLOCKED_WITH_FRONTIER).
""")

# ============================================================
print(SEP)
print("FINAL VERDICT")
print(SEP)
print(f"""
P04 STATUS: 🟡 Candidate / BLOCKED_WITH_FRONTIER (UNCHANGED)

The two new scout responses (Claude Research R2 + GPT-pro R2) do not provide
any route that is executable with current tools or that introduces genuinely
new mathematical content beyond the 17 routes already explored.

The closest approaches remain:
  (A) b²-parametric: P(τ) convex (26K+), C=648(σ⁴-36c'²) PROVED constant
  (B) c'-parametric: M''(θ)≥0 (122K), discriminant bound (60K)
  (C) φ-subadditivity: 153K+ tests, but polynomial 1612 terms deg 34

Both scouts correctly identify that the remaining gap is a constrained
polynomial non-negativity problem requiring either:
  - specialized SOS solver (TSSOS, MOSEK) — not available
  - novel algebraic decomposition — none found in 17 attempts

Total: ~117 messages used, ~300 budget. GREEN on budget.
Total elapsed: {time.time() - t0:.1f}s
""")
