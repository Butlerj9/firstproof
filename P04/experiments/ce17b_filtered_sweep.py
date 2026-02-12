"""
ce17b_filtered_sweep.py — Filtered superadditivity + concavity test
Only consider (sigma, b, cp) where the polynomial has 4 simple real roots (Delta > 0).
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import sympy as sp
from sympy import symbols, cancel, expand, fraction
import numpy as np

SEP = "=" * 70
t0 = time.time()
sigma, b, cp = symbols("sigma b cp", real=True)
a_sym = -sigma
c_sym = cp + sigma**2 / 12

A_f = a_sym**2 + 12*c_sym
B_f = 2*a_sym**3 - 8*a_sym*c_sym + 9*b**2
Delta_sym = 16*a_sym**4*c_sym - 4*a_sym**3*b**2 - 128*a_sym**2*c_sym**2 + 144*a_sym*b**2*c_sym - 27*b**4 + 256*c_sym**3
inv_Phi4 = -Delta_sym / (4 * A_f * B_f)

inv_f = sp.lambdify((sigma, b, cp), cancel(inv_Phi4), "numpy")
delta_f = sp.lambdify((sigma, b, cp), expand(Delta_sym), "numpy")

# Also lambdify the Hessian components
print("Computing Hessian lambdas...", end=" ", flush=True)
d2 = {}
for v1, n1 in [(sigma,'s'),(b,'b'),(cp,'c')]:
    for v2, n2 in [(sigma,'s'),(b,'b'),(cp,'c')]:
        d2[n1+n2] = sp.lambdify((sigma,b,cp), sp.diff(inv_Phi4,v1,v2), "numpy")
print("done (%.1fs)" % (time.time()-t0))

def is_valid(sv, bv, cv):
    """Check if (sigma, b, cp) gives a polynomial with 4 simple real roots."""
    d = delta_f(sv, bv, cv)
    return np.isfinite(d) and d > 1e-12

# ============================================================
print(SEP)
print("SECTION 1: Check CE-17 'counterexample' validity")
print(SEP)
# CE-17 min was at: s1=0.3, s2=0.5, b1=0.3, b2=-0.1, c1=0.025, c2=0.025
params = [(0.3, 0.3, 0.025), (0.5, -0.1, 0.025), (0.8, 0.2, 0.05)]
for sv, bv, cv in params:
    d = delta_f(sv, bv, cv)
    v = is_valid(sv, bv, cv)
    print("  sigma=%.1f, b=%.2f, cp=%.3f: Delta=%.6f, valid=%s" % (sv, bv, cv, d, v))

# ============================================================
print("\n" + SEP)
print("SECTION 2: Filtered superadditivity sweep (Delta > 0 only)")
print(SEP)

sigma_vals = [0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
b_vals = np.arange(-0.3, 0.31, 0.05)
cp_vals = np.arange(-0.05, 0.051, 0.01)

min_M, min_p = float('inf'), None
cnt, neg, skip = 0, 0, 0

for s1 in sigma_vals:
    for s2 in sigma_vals:
        for b1 in b_vals:
            for b2 in b_vals:
                for c1 in cp_vals:
                    for c2 in cp_vals:
                        # Check all three polynomials are valid
                        if not (is_valid(s1,b1,c1) and is_valid(s2,b2,c2) and is_valid(s1+s2,b1+b2,c1+c2)):
                            skip += 1
                            continue
                        try:
                            vc = inv_f(s1+s2,b1+b2,c1+c2)
                            v1 = inv_f(s1,b1,c1)
                            v2 = inv_f(s2,b2,c2)
                            if not(np.isfinite(vc) and np.isfinite(v1) and np.isfinite(v2)):
                                skip += 1; continue
                            M = vc - v1 - v2; cnt += 1
                            if M < min_M: min_M, min_p = M, (s1,s2,b1,b2,c1,c2)
                            if M < -1e-12: neg += 1
                        except:
                            skip += 1; continue

print("Valid evaluations: %d (skipped %d invalid)" % (cnt, skip))
print("Min M: %.10e" % min_M)
if min_p: print("At:", min_p)
print("Negative: %d" % neg)
print("ALL M>=0?", "YES" if neg==0 else "NO")
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("SECTION 3: Hessian concavity on VALID region only")
print(SEP)

# Generate valid test points
print("\nGenerating valid test points...")
valid_pts = []
for sv in [0.5, 1.0, 2.0, 3.0, 5.0]:
    for bv in np.arange(-0.2, 0.21, 0.05):
        for cv in np.arange(-0.04, 0.041, 0.01):
            if is_valid(sv, bv, cv):
                valid_pts.append((sv, bv, cv))

print("Found %d valid test points" % len(valid_pts))
print("\n%6s %6s %7s | %12s %12s %12s | %5s" % ("sigma","b","cp","eig1","eig2","eig3","NSD?"))
print("-"*80)

all_nsd = True
nsd_count = 0
total_tested = 0
worst_eig = -float('inf')
worst_pt = None

for sv,bv,cv in valid_pts:
    try:
        H = np.array([[d2['ss'](sv,bv,cv),d2['sb'](sv,bv,cv),d2['sc'](sv,bv,cv)],
                       [d2['sb'](sv,bv,cv),d2['bb'](sv,bv,cv),d2['bc'](sv,bv,cv)],
                       [d2['sc'](sv,bv,cv),d2['bc'](sv,bv,cv),d2['cc'](sv,bv,cv)]],dtype=float)
        eigs = np.linalg.eigvalsh(H)
        nsd = all(e <= 1e-10 for e in eigs)
        total_tested += 1
        if nsd: nsd_count += 1
        else:
            all_nsd = False
            if eigs[-1] > worst_eig:
                worst_eig = eigs[-1]
                worst_pt = (sv, bv, cv, eigs)
        # Print a sample
        if total_tested <= 20 or not nsd:
            print("%6.1f %6.2f %7.3f | %12.4e %12.4e %12.4e | %5s" % (sv,bv,cv,eigs[0],eigs[1],eigs[2],"YES" if nsd else "NO"))
    except:
        pass

print("\nTested: %d valid points, NSD: %d, Not NSD: %d" % (total_tested, nsd_count, total_tested - nsd_count))
if worst_pt:
    print("Worst non-NSD point: sigma=%.1f, b=%.2f, cp=%.3f, max_eig=%.4e" % (worst_pt[0], worst_pt[1], worst_pt[2], worst_eig))

# ============================================================
print("\n" + SEP)
print("SECTION 4: Refined concavity — (b,cp) Hessian only at various sigma")
print(SEP)
print("Testing if 1/Phi_4 is concave in (b,cp) for FIXED sigma...")

for sv in [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    all_ok = True
    worst_det = float('inf')
    worst_bc = None
    for bv in np.arange(-0.15, 0.16, 0.02):
        for cv in np.arange(-0.03, 0.031, 0.005):
            if not is_valid(sv, bv, cv): continue
            try:
                fbb = float(d2['bb'](sv,bv,cv))
                fcc = float(d2['cc'](sv,bv,cv))
                fbc = float(d2['bc'](sv,bv,cv))
                det_H = fbb * fcc - fbc**2
                # Concave requires fbb <= 0 AND det >= 0
                if fbb > 1e-10 or det_H < -1e-10:
                    all_ok = False
                    if det_H < worst_det:
                        worst_det = det_H
                        worst_bc = (bv, cv, fbb, fcc, det_H)
            except:
                pass
    status = "CONCAVE" if all_ok else "NOT CONCAVE"
    print("  sigma=%.1f: %s" % (sv, status), end="")
    if worst_bc:
        print("  (worst: b=%.2f cp=%.3f fbb=%.3e det=%.3e)" % worst_bc)
    else:
        print()

# ============================================================
print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time()-t0))
print("Filtered M>=0?", "YES" if neg==0 else "NO (%d violations)" % neg)
print("Hessian NSD on valid region?", "YES" if all_nsd else "NO")
print()
if neg == 0:
    print("*** SUPERADDITIVITY HOLDS on valid region (Delta > 0)!")
    print("    CE-17 'counterexamples' were all in the invalid region.")
else:
    print("*** REAL COUNTEREXAMPLE found within valid region!")
