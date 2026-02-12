"""
ce17_cumulant_decomp.py — Decompose 1/Phi_4 in cumulant coordinates
and test concavity => superadditivity for the general n=4 case.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import sympy as sp
from sympy import symbols, cancel, expand, factor, collect, fraction, series
import numpy as np
import warnings
warnings.filterwarnings("ignore")

SEP = "=" * 70
t0 = time.time()
sigma, b, cp = symbols("sigma b cp", real=True)
a = -sigma
c = cp + sigma**2 / 12

print(SEP)
print("SECTION 1: Define 1/Phi_4 in cumulant coordinates")
print(SEP)
A_factor = a**2 + 12*c
B_factor = 2*a**3 - 8*a*c + 9*b**2
Delta = 16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2 + 144*a*b**2*c - 27*b**4 + 256*c**3
inv_Phi4 = -Delta / (4 * A_factor * B_factor)
print("a=-sigma, c=cp+sigma^2/12")
A_sub = sp.simplify(expand(A_factor))
B_sub = collect(expand(B_factor), [sigma, b, cp])
print("A =", A_sub, " factored:", factor(A_sub))
print("B =", B_sub, " factored:", factor(B_sub))
sys.stdout.flush()

print("\n" + SEP)
print("SECTION 2: Simplify 1/Phi_4")
print(SEP)
inv_s = cancel(inv_Phi4)
num, den = fraction(inv_s)
print("Num:", collect(expand(num), [sigma, b, cp]))
print("Den:", collect(expand(den), [sigma, b, cp]))
print("Den factored:", factor(den))
try:
    den_poly = sp.Poly(expand(den), sigma, b, cp)
    print("Den terms:", len(den_poly.as_dict()), "=> Laurent?" if len(den_poly.as_dict())==1 else "=> rational")
except: pass
sys.stdout.flush()

print("\n" + SEP)
print("SECTION 3: b=0 and cp=0 slices")
print(SEP)
print("b=0:", factor(cancel(inv_Phi4.subs(b, 0))))
print("cp=0:", factor(cancel(inv_Phi4.subs(cp, 0))))
sys.stdout.flush()

print("\n" + SEP)
print("SECTION 4: Taylor expansion around b=0, cp=0 (order 4)")
print(SEP)
tp = symbols("tp")
inv_scaled = inv_Phi4.subs([(b, tp*b), (cp, tp*cp)])
taylor = series(inv_scaled, tp, 0, 5)
for k in range(5):
    c_k = sp.simplify(taylor.coeff(tp, k))
    print("  t^%d: %s" % (k, c_k))
sys.stdout.flush()

print("\n" + SEP)
print("SECTION 5: Homogeneity")
print(SEP)
lam = symbols("lam", positive=True)
inv_nat = inv_Phi4.subs([(sigma, lam**2*sigma), (b, lam**3*b), (cp, lam**4*cp)])
print("Root scaling ratio:", sp.simplify(cancel(inv_nat / inv_Phi4)))
inv_unif = inv_Phi4.subs([(sigma, lam*sigma), (b, lam*b), (cp, lam*cp)])
print("Additive scaling ratio:", cancel(inv_unif / inv_Phi4))
sys.stdout.flush()

print("\n" + SEP)
print("SECTION 6: Hessian concavity test (3x3)")
print(SEP)
print("Computing 2nd derivatives...", end=" ", flush=True)
d2 = {}
for v1, n1 in [(sigma,'s'),(b,'b'),(cp,'c')]:
    for v2, n2 in [(sigma,'s'),(b,'b'),(cp,'c')]:
        d2[n1+n2] = sp.lambdify((sigma,b,cp), sp.diff(inv_Phi4,v1,v2), "numpy")
print("done (%.1fs)" % (time.time()-t0))

pts = [
    (1,0,0),(2,0,0),(1,.1,0),(1,0,.01),(1,.1,.01),(1,-.1,-.01),
    (2,.2,.02),(3,.1,.01),(.5,.05,.005),(1,.2,.02),(1,.3,0),(1,0,.05),
    (1,.3,.03),(5,.5,.1),(.3,.02,.001),(10,0,0),(1,.05,.005),
    (1,.15,.015),(1,-.2,.01),(1,.1,-.02),(2,.3,.05),(4,.2,.04),
]
print("\n%6s %6s %7s | %12s %12s %12s | %5s" % ("sigma","b","cp","eig1","eig2","eig3","NSD?"))
print("-"*80)
all_nsd = True
for sv,bv,cv in pts:
    try:
        H = np.array([[d2['ss'](sv,bv,cv),d2['sb'](sv,bv,cv),d2['sc'](sv,bv,cv)],
                       [d2['sb'](sv,bv,cv),d2['bb'](sv,bv,cv),d2['bc'](sv,bv,cv)],
                       [d2['sc'](sv,bv,cv),d2['bc'](sv,bv,cv),d2['cc'](sv,bv,cv)]],dtype=float)
        eigs = np.linalg.eigvalsh(H)
        nsd = all(e <= 1e-10 for e in eigs)
        if not nsd: all_nsd = False
        print("%6.1f %6.2f %7.3f | %12.4e %12.4e %12.4e | %5s" % (sv,bv,cv,eigs[0],eigs[1],eigs[2],"YES" if nsd else "NO"))
    except Exception as e:
        print("%6.1f %6.2f %7.3f | ERROR: %s" % (sv,bv,cv,e)); all_nsd=False
print("\nALL NSD?", all_nsd)
sys.stdout.flush()

print("\n" + SEP)
print("SECTION 7: Superadditivity sweep")
print(SEP)
inv_f = sp.lambdify((sigma,b,cp), cancel(inv_Phi4), "numpy")
svals = [.3,.5,1,1.5,2,3,5]
bvals = np.arange(-.3,.31,.1)
cvals = np.arange(-.05,.051,.025)
min_M, min_p, cnt, neg = float('inf'), None, 0, 0
for s1 in svals:
    for s2 in svals:
        for b1 in bvals:
            for b2 in bvals:
                for c1 in cvals:
                    for c2 in cvals:
                        try:
                            vc = inv_f(s1+s2,b1+b2,c1+c2)
                            v1 = inv_f(s1,b1,c1)
                            v2 = inv_f(s2,b2,c2)
                            if not(np.isfinite(vc) and np.isfinite(v1) and np.isfinite(v2)): continue
                            M = vc - v1 - v2; cnt += 1
                            if M < min_M: min_M, min_p = M, (s1,s2,b1,b2,c1,c2)
                            if M < -1e-12: neg += 1
                        except: continue
print("Evaluations:", cnt)
print("Min M: %.10e" % min_M)
if min_p: print("At:", min_p)
print("Negative count:", neg)
print("ALL M>=0?", neg==0)
sys.stdout.flush()

print("\n" + SEP)
print("SUMMARY")
print(SEP)
print("Elapsed: %.1fs" % (time.time()-t0))
print("Hessian NSD everywhere?", "YES" if all_nsd else "NO")
print("Superadditivity M>=0?", "YES" if neg==0 else "NO")
if all_nsd and neg==0:
    print("\n*** MAJOR: 1/Phi_4 appears GLOBALLY CONCAVE in (sigma,b,cp).")
    print("    If confirmed, superadditivity follows => closes general n=4.")
