"""
ce15_critical_point.py - Test t1=t2 hypothesis for -H critical points
"""

import numpy as np
import sympy as sp
from sympy import symbols, Rational, expand, simplify, solve, Poly

SEP = chr(61) * 72

# ===== SECTION 1 =====
print(SEP)
print("SECTION 1: Symbolic definition of -H(w, t1, t2)")
print(SEP)

w, t1, t2 = symbols("w t1 t2")

negA = 144 * (t1 + t2)**2 * (6*t1 + 1) * (6*t2 + 1)
negB = -144 * (t1 + t2) * (72*t1*t2**2 + 12*t1*t2 - t1 + 12*t2**2 + 3*t2)
negC = 144 * (36*t1**2*t2**2 + 12*t1**2*t2 + t1**2 + 36*t1*t2**3 + 18*t1*t2**2 + 6*t2**3 + 3*t2**2)

negH = negA * w**2 + negB * w + negC
negH_expanded = expand(negH)

print()
print("-A =", expand(negA))
print()
print("-B =", expand(negB))
print()
print("-C =", expand(negC))
print()
print("-H (expanded) has", len(negH_expanded.as_ordered_terms()), "terms")

# ===== SECTION 2: Gradient =====
print()
print(SEP)
print("SECTION 2: Gradient of -H")
print(SEP)

dH_dw = sp.diff(negH, w)
dH_dt1 = sp.diff(negH, t1)
dH_dt2 = sp.diff(negH, t2)

dH_dw_exp = expand(dH_dw)
print()
print("d(-H)/dw =", dH_dw_exp)

# ===== SECTION 3: Critical w* =====
print()
print(SEP)
print("SECTION 3: Optimal w* and reduced critical-point system")
print(SEP)

w_star = -negB / (2 * negA)
w_star_simplified = simplify(w_star)
print()
print("w* = -(-B) / (2*(-A)) =", w_star_simplified)

negH_star = negA * w_star**2 + negB * w_star + negC
negH_star = simplify(negH_star)
print()
print("-H(w*, t1, t2) =", negH_star)

negH_star_expanded = expand(negH_star)
print()
print("-H(w*, t1, t2) expanded =", negH_star_expanded)

print()
print("Differentiating -H(w*, t1, t2) w.r.t. t1 and t2...")
dHstar_dt1 = sp.diff(negH_star, t1)
dHstar_dt2 = sp.diff(negH_star, t2)

dHstar_dt1_simplified = simplify(dHstar_dt1)
dHstar_dt2_simplified = simplify(dHstar_dt2)

print()
print("d(-H*)/dt1 simplified =", dHstar_dt1_simplified)
print()
print("d(-H*)/dt2 simplified =", dHstar_dt2_simplified)

# ===== SECTION 3a: Symmetry check =====
print()
print(SEP)
print("SECTION 3a: Testing if t1=t2 is forced at critical points")
print(SEP)

negH_swapped = negH.subs([(t1, t2), (t2, t1)])
diff_sym = expand(negH - negH_swapped)
print()
print("-H(w,t1,t2) - -H(w,t2,t1) =", diff_sym)
if diff_sym == 0:
    print("  => -H IS symmetric in (t1, t2)")
else:
    print("  => -H is NOT symmetric in (t1, t2)")
    print("  Asymmetry:", diff_sym)

negH_star_swapped = negH_star.subs([(t1, t2), (t2, t1)])
diff_star_sym = simplify(negH_star - negH_star_swapped)
print()
print("-H*(t1,t2) - -H*(t2,t1) =", simplify(diff_star_sym))

# Solve on the t1=t2 slice
print()
print("--- Solving on the t1=t2 slice ---")
s = symbols("s")

negH_sym = negH.subs([(t1, s), (t2, s)])
negH_sym_exp = expand(negH_sym)
print()
print("-H(w, s, s) =", negH_sym_exp)

dHsym_dw = sp.diff(negH_sym, w)
w_star_sym = solve(dHsym_dw, w)
print()
print("w* on t1=t2 slice:", w_star_sym)

if w_star_sym:
    negH_reduced = negH_sym.subs(w, w_star_sym[0])
    negH_reduced = simplify(negH_reduced)
    print()
    print("-H(w*, s, s) =", negH_reduced)

    d_reduced_ds = sp.diff(negH_reduced, s)
    d_reduced_ds_simplified = simplify(d_reduced_ds)
    print()
    print("d/ds[-H(w*, s, s)] =", d_reduced_ds_simplified)

    numer_ds = sp.numer(sp.together(d_reduced_ds_simplified))
    print()
    print("Numerator of d/ds =", expand(numer_ds))

    crit_s = solve(numer_ds, s)
    print()
    print("Critical s values:", crit_s)

    for cs in crit_s:
        cs_float = float(cs)
        print()
        print("  s =", cs, "=", f"{cs_float:.6f}")
        if -Rational(1, 12) < cs < Rational(1, 6):
            print("    -> IN domain (-1/12, 1/6)")
            w_val = w_star_sym[0].subs(s, cs)
            w_val_s = simplify(w_val)
            print("    -> w* =", w_val_s, "=", f"{float(w_val_s):.6f}")
            if 0 < float(w_val_s) < 1:
                print("    -> w* IN (0,1)")
                negH_val = negH_sym.subs([(w, w_val_s), (s, cs)])
                print("    -> -H =", simplify(negH_val), "=", f"{float(simplify(negH_val)):.10f}")
            else:
                print("    -> w* OUTSIDE (0,1)")
        else:
            print("    -> OUTSIDE domain (-1/12, 1/6)")

# ===== SECTION 3b: Full gradient system =====
print()
print(SEP)
print("SECTION 3b: Analyzing gradient system for t1=t2 constraint")
print(SEP)

eq1 = expand(dH_dw)
eq2 = expand(dH_dt1)
eq3 = expand(dH_dt2)

print()
print("Equation 1 (dH/dw=0): polynomial of total degree", sp.degree(Poly(eq1, w, t1, t2)))
print("Equation 2 (dH/dt1=0): polynomial of total degree", sp.degree(Poly(eq2, w, t1, t2)))
print("Equation 3 (dH/dt2=0): polynomial of total degree", sp.degree(Poly(eq3, w, t1, t2)))

print()
print("--- Substitution t2 = t1 + d, checking if d=0 is forced ---")
d = symbols("d")
eq1_d = eq1.subs(t2, t1 + d)
eq2_d = eq2.subs(t2, t1 + d)
eq3_d = eq3.subs(t2, t1 + d)

w_from_eq1 = solve(eq1_d, w)
print()
print("w from eq1:", len(w_from_eq1), "solution(s)")

if w_from_eq1:
    w_sol = w_from_eq1[0]
    print("  w =", simplify(w_sol))

    eq2_sub = eq2_d.subs(w, w_sol)
    eq3_sub = eq3_d.subs(w, w_sol)

    eq2_sub_s = simplify(eq2_sub)
    eq3_sub_s = simplify(eq3_sub)

    eq2_num = sp.numer(sp.together(eq2_sub_s))
    eq3_num = sp.numer(sp.together(eq3_sub_s))

    eq2_num = expand(eq2_num)
    eq3_num = expand(eq3_num)

    print()
    print("Numerator of eq2 after substitution:", len(str(eq2_num)), "chars")
    print("Numerator of eq3 after substitution:", len(str(eq3_num)), "chars")

    eq2_poly_d = Poly(eq2_num, d)
    eq3_poly_d = Poly(eq3_num, d)

    print()
    print("eq2_num as poly in d: degree =", eq2_poly_d.degree())
    eq2_const = simplify(eq2_poly_d.nth(0))
    print("  Constant term (coeff of d^0) =", eq2_const)

    print()
    print("eq3_num as poly in d: degree =", eq3_poly_d.degree())
    eq3_const = simplify(eq3_poly_d.nth(0))
    print("  Constant term (coeff of d^0) =", eq3_const)

    eq2_const_zero = (eq2_const == 0)
    eq3_const_zero = (eq3_const == 0)

    print()
    print("eq2 constant term is zero:", eq2_const_zero)
    print("eq3 constant term is zero:", eq3_const_zero)

    if eq2_const_zero and eq3_const_zero:
        print()
        print("*** Both constant terms vanish => d | eq2_num and d | eq3_num")
        print("*** This means t1=t2 (d=0) is ALWAYS a solution branch")

        eq2_reduced = sp.quo(eq2_poly_d, Poly(d, d))
        eq3_reduced = sp.quo(eq3_poly_d, Poly(d, d))
        print()
        print("After dividing by d:")
        print("  eq2_reduced degree in d:", eq2_reduced.degree())
        print("  eq3_reduced degree in d:", eq3_reduced.degree())

# ===== SECTION 4: Numerical grid search =====
print()
print(SEP)
print("SECTION 4: Numerical grid search (50 x 50 x 50)")
print(SEP)

Nw, Nt = 50, 50
w_arr = np.linspace(0.0, 1.0, Nw)
t1_arr = np.linspace(-1/12, 1/6, Nt)
t2_arr = np.linspace(-1/12, 1/6, Nt)

W, T1, T2 = np.meshgrid(w_arr, t1_arr, t2_arr, indexing="ij")

negA_num = 144 * (T1 + T2)**2 * (6*T1 + 1) * (6*T2 + 1)
negB_num = -144 * (T1 + T2) * (72*T1*T2**2 + 12*T1*T2 - T1 + 12*T2**2 + 3*T2)
negC_num = 144 * (36*T1**2*T2**2 + 12*T1**2*T2 + T1**2 + 36*T1*T2**3 + 18*T1*T2**2 + 6*T2**3 + 3*T2**2)

negH_num = negA_num * W**2 + negB_num * W + negC_num

min_val = np.min(negH_num)
min_idx = np.unravel_index(np.argmin(negH_num), negH_num.shape)
w_min = W[min_idx]
t1_min = T1[min_idx]
t2_min = T2[min_idx]

print()
print(f"Grid minimum of -H: {min_val:.10e}")
print(f"  at w  = {w_min:.6f}")
print(f"     t1 = {t1_min:.6f}")
print(f"     t2 = {t2_min:.6f}")
print(f"  |t1 - t2| = {abs(t1_min - t2_min):.6e}")

if abs(t1_min - t2_min) < 1e-6:
    print("  => t1 ~ t2 at minimum (within grid resolution)")
else:
    print(f"  => t1 != t2 at minimum (gap = {abs(t1_min - t2_min):.6e})")

flat = negH_num.flatten()
top10_idx = np.argpartition(flat, 10)[:10]
top10_idx = top10_idx[np.argsort(flat[top10_idx])]

print()
print("Top 10 smallest -H values:")
for rank, fi in enumerate(top10_idx):
    idx = np.unravel_index(fi, negH_num.shape)
    val = negH_num[idx]
    wv, t1v, t2v = W[idx], T1[idx], T2[idx]
    print(f"  {rank+1:>4}  {val:>16.8e}  w={wv:>8.4f}  t1={t1v:>10.6f}  t2={t2v:>10.6f}  |t1-t2|={abs(t1v-t2v):>10.6e}")

# Refined search near minimum
print()
print("--- Refined grid near minimum (200^3 local) ---")
dw_half = (w_arr[1] - w_arr[0]) * 2
dt_half = (t1_arr[1] - t1_arr[0]) * 2

Nref = 200
w_ref = np.linspace(max(0, w_min - dw_half), min(1, w_min + dw_half), Nref)
t1_ref = np.linspace(max(-1/12, t1_min - dt_half), min(1/6, t1_min + dt_half), Nref)
t2_ref = np.linspace(max(-1/12, t2_min - dt_half), min(1/6, t2_min + dt_half), Nref)

Wr, T1r, T2r = np.meshgrid(w_ref, t1_ref, t2_ref, indexing="ij")

negA_r = 144 * (T1r + T2r)**2 * (6*T1r + 1) * (6*T2r + 1)
negB_r = -144 * (T1r + T2r) * (72*T1r*T2r**2 + 12*T1r*T2r - T1r + 12*T2r**2 + 3*T2r)
negC_r = 144 * (36*T1r**2*T2r**2 + 12*T1r**2*T2r + T1r**2 + 36*T1r*T2r**3 + 18*T1r*T2r**2 + 6*T2r**3 + 3*T2r**2)

negH_r = negA_r * Wr**2 + negB_r * Wr + negC_r

min_val_r = np.min(negH_r)
min_idx_r = np.unravel_index(np.argmin(negH_r), negH_r.shape)
w_min_r = Wr[min_idx_r]
t1_min_r = T1r[min_idx_r]
t2_min_r = T2r[min_idx_r]

print()
print(f"Refined minimum of -H: {min_val_r:.10e}")
print(f"  at w  = {w_min_r:.8f}")
print(f"     t1 = {t1_min_r:.8f}")
print(f"     t2 = {t2_min_r:.8f}")
print(f"  |t1 - t2| = {abs(t1_min_r - t2_min_r):.6e}")

# ===== SECTION 5: Scipy optimization =====
print()
print(SEP)
print("SECTION 5: Scipy minimization from multiple start points")
print(SEP)

from scipy.optimize import minimize

def negH_func(x):
    ww, tt1, tt2 = x
    A = 144 * (tt1 + tt2)**2 * (6*tt1 + 1) * (6*tt2 + 1)
    B = -144 * (tt1 + tt2) * (72*tt1*tt2**2 + 12*tt1*tt2 - tt1 + 12*tt2**2 + 3*tt2)
    C = 144 * (36*tt1**2*tt2**2 + 12*tt1**2*tt2 + tt1**2 + 36*tt1*tt2**3 + 18*tt1*tt2**2 + 6*tt2**3 + 3*tt2**2)
    return A * ww**2 + B * ww + C

bounds = [(1e-8, 1-1e-8), (-1/12 + 1e-8, 1/6 - 1e-8), (-1/12 + 1e-8, 1/6 - 1e-8)]

np.random.seed(42)
n_starts = 200
results = []

for i in range(n_starts):
    w0 = np.random.uniform(0.01, 0.99)
    t10 = np.random.uniform(-1/12 + 0.001, 1/6 - 0.001)
    t20 = np.random.uniform(-1/12 + 0.001, 1/6 - 0.001)
    res = minimize(negH_func, [w0, t10, t20], method="L-BFGS-B", bounds=bounds)
    results.append((res.fun, res.x, res.success))

results.sort(key=lambda r: r[0])

print()
print(f"Top 15 local minima from {n_starts} random starts:")
seen = set()
unique_results = []
for val, x, success in results:
    key = tuple(np.round(x, 4))
    if key not in seen:
        seen.add(key)
        unique_results.append((val, x, success))

for rank, (val, x, success) in enumerate(unique_results[:15]):
    w_v, t1_v, t2_v = x
    ok = "Y" if success else "N"
    print(f"  {rank+1:>4}  {val:>16.8e}  w={w_v:>10.6f}  t1={t1_v:>10.6f}  t2={t2_v:>10.6f}  |t1-t2|={abs(t1_v-t2_v):>12.6e}  {ok}")

tol = 1e-4
sym_count = sum(1 for v, x, ss in unique_results if abs(x[1] - x[2]) < tol)
asym_count = len(unique_results) - sym_count
print()
print(f"Unique local minima: {len(unique_results)}")
print(f"  With |t1-t2| < {tol}: {sym_count}")
print(f"  With |t1-t2| >= {tol}: {asym_count}")

# ===== SECTION 6: Boundary analysis =====
print()
print(SEP)
print("SECTION 6: Boundary analysis (6 faces)")
print(SEP)

Nb = 200

def eval_negH_np(w_v, t1_v, t2_v):
    A = 144 * (t1_v + t2_v)**2 * (6*t1_v + 1) * (6*t2_v + 1)
    B = -144 * (t1_v + t2_v) * (72*t1_v*t2_v**2 + 12*t1_v*t2_v - t1_v + 12*t2_v**2 + 3*t2_v)
    C = 144 * (36*t1_v**2*t2_v**2 + 12*t1_v**2*t2_v + t1_v**2 + 36*t1_v*t2_v**3 + 18*t1_v*t2_v**2 + 6*t2_v**3 + 3*t2_v**2)
    return A * w_v**2 + B * w_v + C

def eval_face_2d(func, arr1, arr2, name1, name2):
    A1, A2 = np.meshgrid(arr1, arr2, indexing="ij")
    vals = func(A1, A2)
    min_val = np.min(vals)
    max_val = np.max(vals)
    min_idx = np.unravel_index(np.argmin(vals), vals.shape)
    return min_val, max_val, arr1[min_idx[0]], arr2[min_idx[1]], name1, name2

t_grid = np.linspace(-1/12, 1/6, Nb)
w_grid = np.linspace(0, 1, Nb)

face_list = [
    ("w=0", lambda: eval_face_2d(lambda a, b: eval_negH_np(0, a, b), t_grid, t_grid, "t1", "t2")),
    ("w=1", lambda: eval_face_2d(lambda a, b: eval_negH_np(1, a, b), t_grid, t_grid, "t1", "t2")),
    ("t1=-1/12", lambda: eval_face_2d(lambda a, b: eval_negH_np(a, -1/12, b), w_grid, t_grid, "w", "t2")),
    ("t1=1/6", lambda: eval_face_2d(lambda a, b: eval_negH_np(a, 1/6, b), w_grid, t_grid, "w", "t2")),
    ("t2=-1/12", lambda: eval_face_2d(lambda a, b: eval_negH_np(a, b, -1/12), w_grid, t_grid, "w", "t1")),
    ("t2=1/6", lambda: eval_face_2d(lambda a, b: eval_negH_np(a, b, 1/6), w_grid, t_grid, "w", "t1")),
]

print()
for face_name, face_func in face_list:
    min_v, max_v, c1, c2, n1, n2 = face_func()
    print(f"{face_name:>12}  min={min_v:>16.8e}  max={max_v:>16.8e}  {n1}={c1:>8.5f}  {n2}={c2:>8.5f}")

# ===== SECTION 7: Summary =====
print()
print(SEP)
print("SECTION 7: Summary and conclusions")
print(SEP)

global_min_val = results[0][0]
global_min_x = results[0][1]
print()
print(f"Global minimum found (scipy): {global_min_val:.10e}")
print(f"  at w={global_min_x[0]:.8f}, t1={global_min_x[1]:.8f}, t2={global_min_x[2]:.8f}")
print(f"  |t1-t2| = {abs(global_min_x[1]-global_min_x[2]):.2e}")

if global_min_val >= -1e-12:
    print()
    print("  => -H >= 0 on the entire domain (within numerical precision)")
else:
    print()
    print(f"  => -H can be NEGATIVE (min = {global_min_val:.6e})")

if abs(global_min_x[1] - global_min_x[2]) < 1e-4:
    print("  => Global minimum satisfies t1 ~ t2")
else:
    print("  => Global minimum does NOT satisfy t1 ~ t2")

all_sym = all(abs(x[1] - x[2]) < 1e-3 for v, x, ss in unique_results if v < global_min_val + 0.01)
print()
print(f"  All near-optimal points have t1 ~ t2: {all_sym}")

print()
print(SEP)
print("HYPOTHESIS: All interior critical points satisfy t1 = t2")
if sym_count > 0 and asym_count == 0:
    print("VERDICT: SUPPORTED by numerical evidence")
elif asym_count > 0:
    asym_interior = [(v, x) for v, x, ss in unique_results
                     if abs(x[1] - x[2]) >= tol
                     and 0.01 < x[0] < 0.99
                     and -1/12 + 0.01 < x[1] < 1/6 - 0.01
                     and -1/12 + 0.01 < x[2] < 1/6 - 0.01]
    if len(asym_interior) == 0:
        print("VERDICT: SUPPORTED - asymmetric critical points are all on boundaries")
    else:
        print(f"VERDICT: REFUTED - found {len(asym_interior)} interior critical points with t1 != t2")
        for v, x in asym_interior[:5]:
            print(f"  Counterexample: val={v:.6e}, w={x[0]:.6f}, t1={x[1]:.6f}, t2={x[2]:.6f}")
else:
    print("VERDICT: INCONCLUSIVE")
print(SEP)
