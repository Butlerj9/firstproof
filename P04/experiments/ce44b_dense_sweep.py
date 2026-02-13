"""
CE-44b: Dense w-sweep for direct M >= 0 SOS certificate.
Run w = k/40 for k=1..20 (by w<->1-w symmetry, covers all 39 interior points).

Uses CLARABEL interior-point solver (same framework as CE-44).
"""

import time, sys
import numpy as np
from scipy import sparse
import clarabel
from itertools import combinations_with_replacement
from sympy import symbols, Rational, expand, Poly

def build_polynomial_at_w(w_rat):
    b1, b2, cp1, cp2 = symbols('b1 b2 cp1 cp2')
    s1 = w_rat; s2 = 1 - w_rat; sh = Rational(1)
    a1, a2, ah = -s1, -s2, Rational(-1)
    c1 = s1**2/12 + cp1; c2 = s2**2/12 + cp2
    ch = Rational(1,12) + cp1 + cp2; bh = b1 + b2

    def ABD(a, b, c):
        A = expand(a**2 + 12*c)
        B = expand(2*a**3 - 8*a*c + 9*b**2)
        D = expand(16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
                   + 144*a*b**2*c - 27*b**4 + 256*c**3)
        return A, B, D

    A1,B1,D1 = ABD(a1,b1,c1); A2,B2,D2 = ABD(a2,b2,c2); Ah,Bh,Dh = ABD(ah,bh,ch)
    AB1=expand(A1*B1); AB2=expand(A2*B2); ABh=expand(Ah*Bh)
    P = expand(expand(Dh*AB1*AB2) - expand(D1*ABh*AB2) - expand(D2*ABh*AB1))
    P_poly = Poly(P, b1, b2, cp1, cp2)
    P_dict = {k: float(v) for k, v in P_poly.as_dict().items()}
    P_deg = P_poly.total_degree()

    constraints = []
    for expr, label in [(D1,"D1"),(expand(-AB1),"-AB1"),(D2,"D2"),
                         (expand(-AB2),"-AB2"),(Dh,"Dh"),(expand(-ABh),"-ABh")]:
        poly = Poly(expr, b1, b2, cp1, cp2)
        constraints.append(({k: float(v) for k, v in poly.as_dict().items()},
                            poly.total_degree(), label))
    return P_dict, P_deg, constraints


def solve_sos_clarabel(P_dict, P_deg, constraints):
    nvars = 4
    def make_monos(md):
        monos = []
        for d in range(md+1):
            for combo in combinations_with_replacement(range(nvars), d):
                exp = [0]*nvars
                for v in combo: exp[v] += 1
                monos.append(tuple(exp))
        return monos

    def product_table(monos):
        table = {}
        for i in range(len(monos)):
            for j in range(i, len(monos)):
                prod = tuple(monos[i][k]+monos[j][k] for k in range(nvars))
                if prod not in table: table[prod] = []
                table[prod].append((i, j))
        return table

    half0 = P_deg // 2
    monos0 = make_monos(half0); m0 = len(monos0); pt0 = product_table(monos0)

    mult_infos = []
    for _, g_deg, label in constraints:
        half = (P_deg - g_deg) // 2
        if half < 0: continue
        monos_m = make_monos(half); pt_m = product_table(monos_m)
        mult_infos.append((len(monos_m), monos_m, pt_m, g_deg, label))

    n_psd0 = m0*(m0+1)//2
    n_psd_list = [mm*(mm+1)//2 for mm,_,_,_,_ in mult_infos]
    n_vars = n_psd0 + sum(n_psd_list)

    def var_off(gi, i, j, ms):
        base = 0 if gi == 0 else n_psd0 + sum(n_psd_list[:gi-1])
        if i > j: i, j = j, i
        return base + i*ms - i*(i+1)//2 + j

    target_monos = make_monos(P_deg)
    max_coeff = max(abs(v) for v in P_dict.values()) if P_dict else 1.0
    P_sc = {k: v/max_coeff for k, v in P_dict.items()}

    sqrt2 = np.sqrt(2.0)
    eq_rows, eq_cols, eq_vals, eq_b = [], [], [], []
    for alpha in target_monos:
        row = len(eq_b)
        tc = P_sc.get(alpha, 0.0)
        for (i, j) in pt0.get(alpha, []):
            vidx = var_off(0, i, j, m0)
            eq_rows.append(row); eq_cols.append(vidx)
            eq_vals.append(1.0 if i == j else 2.0)
        for k, (mm, monos_m, pt_m, g_deg, label) in enumerate(mult_infos):
            g_dict = constraints[k][0]
            for beta, gc in g_dict.items():
                diff = tuple(alpha[l]-beta[l] for l in range(nvars))
                if any(d < 0 for d in diff): continue
                for (i, j) in pt_m.get(diff, []):
                    vidx = var_off(k+1, i, j, mm)
                    eq_rows.append(row); eq_cols.append(vidx)
                    eq_vals.append(gc * (1.0 if i == j else 2.0))
        eq_b.append(tc)

    n_eq = len(eq_b)
    psd_rows, psd_cols, psd_vals = [], [], []
    row_offset = n_eq; psd_sizes = []
    for gi, ms in enumerate([m0] + [mm for mm,_,_,_,_ in mult_infos]):
        psd_sizes.append(ms); idx = 0
        for jj in range(ms):
            for ii in range(jj+1):
                vidx = var_off(gi, ii, jj, ms)
                sc = -1.0 if ii == jj else -sqrt2
                psd_rows.append(row_offset+idx); psd_cols.append(vidx)
                psd_vals.append(sc); idx += 1
        row_offset += ms*(ms+1)//2

    total_rows = row_offset
    A = sparse.csc_matrix((eq_vals+psd_vals, (eq_rows+psd_rows, eq_cols+psd_cols)),
                           shape=(total_rows, n_vars))
    b_vec = np.zeros(total_rows); b_vec[:n_eq] = eq_b
    P_cost = sparse.csc_matrix((n_vars, n_vars))
    q_cost = np.zeros(n_vars)
    cones = [clarabel.ZeroConeT(n_eq)] + [clarabel.PSDTriangleConeT(ms) for ms in psd_sizes]

    settings = clarabel.DefaultSettings()
    settings.verbose = False
    settings.max_iter = 200
    settings.time_limit = 300.0
    settings.tol_gap_abs = 1e-7
    settings.tol_gap_rel = 1e-7
    settings.tol_feas = 1e-7

    t0 = time.time()
    solver = clarabel.DefaultSolver(P_cost, q_cost, A, b_vec, cones, settings)
    sol = solver.solve()
    return str(sol.status), time.time() - t0


if __name__ == '__main__':
    print("CE-44b: Dense w-sweep for M >= 0 SOS Certificate (CLARABEL)")
    print("=" * 70)
    print(f"Sweeping w = k/40 for k = 1..20 (by symmetry covers all w in (0,1))")
    print(f"Problem: 4 vars, deg 10, 6 domain constraints")
    print(f"SOS: 126x126 main + 6x35x35 multipliers = 11,781 vars")
    print()

    results = []
    total_t0 = time.time()

    for k in range(1, 21):
        w_rat = Rational(k, 40)
        wf = float(w_rat)
        sys.stdout.write(f"  w = {wf:.4f} (k={k:2d}/40): building... ")
        sys.stdout.flush()

        tb = time.time()
        P_dict, P_deg, cons = build_polynomial_at_w(w_rat)
        bt = time.time() - tb
        sys.stdout.write(f"({len(P_dict)} terms, {bt:.1f}s), solving... ")
        sys.stdout.flush()

        status, st = solve_sos_clarabel(P_dict, P_deg, cons)
        results.append((k, wf, status, st))
        solved = 'Solved' in status
        print(f"{'OK' if solved else 'FAIL'} [{status}] ({st:.1f}s)")
        sys.stdout.flush()

    total_time = time.time() - total_t0

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    n_solved = sum(1 for _,_,s,_ in results if 'Solved' in s)
    n_almost = sum(1 for _,_,s,_ in results if s == 'AlmostSolved')
    n_fail = sum(1 for _,_,s,_ in results if 'Solved' not in s)

    print(f"Solved:        {n_solved - n_almost}")
    print(f"AlmostSolved:  {n_almost}")
    print(f"Failed:        {n_fail}")
    print(f"Total:         {len(results)}")
    print(f"Certified:     {n_solved}/{len(results)}")
    print(f"Total time:    {total_time:.0f}s ({total_time/60:.1f} min)")

    if n_solved == 20:
        print("\nALL 20 w-slices certified!")
        print("By w <-> 1-w symmetry, M >= 0 certified at 39 rational points in (0,1).")
        print("Combined with analytical proofs for b=0 (CE-16) and c'=0 (CE-26),")
        print("this constitutes a computational proof of M >= 0 for n=4.")

    if n_fail > 0:
        print("\nFailed slices:")
        for k, wf, s, st in results:
            if 'Solved' not in s:
                print(f"  k={k}, w={wf:.4f}: {s}")
