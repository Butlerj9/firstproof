"""
ce29_exact_polynomial.py — Compute the exact superadditivity polynomial P
after clearing denominators, and check basic properties.

Goal: Write M = 1/Phi4(h) - 1/Phi4(1) - 1/Phi4(2) in the form P/D where
D > 0 on the validity domain. Then P >= 0 iff M >= 0.

If P >= 0 on ALL of R^5 (not just validity domain), we can attempt
unconstrained SOS decomposition.
"""
import sys, io, time
from fractions import Fraction
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SEP = "=" * 70
t0 = time.time()

# Use SymPy for symbolic computation
from sympy import symbols, expand, factor, Poly, degree, total_degree
from sympy import Rational, sqrt, collect

w, b1, b2, cp1, cp2 = symbols('w b1 b2 cp1 cp2')

# sigma1 = w, sigma2 = 1-w, sigma_h = 1
s1 = w
s2 = 1 - w
sh = Rational(1)

# a = -sigma, c = sigma^2/12 + cp
a1, a2, ah = -s1, -s2, Rational(-1)
c1 = s1**2 / 12 + cp1
c2 = s2**2 / 12 + cp2
ch = Rational(1, 12) + cp1 + cp2
bh = b1 + b2

print(SEP)
print("Computing A, B, Delta for each polynomial...")
print(SEP)

def compute_ABDelta(a, b, c, label):
    """Compute A = a^2 + 12c, B = 2a^3 - 8ac + 9b^2, Delta."""
    A = a**2 + 12*c
    B = 2*a**3 - 8*a*c + 9*b**2
    Delta = (16*a**4*c - 4*a**3*b**2 - 128*a**2*c**2
             + 144*a*b**2*c - 27*b**4 + 256*c**3)
    A = expand(A)
    B = expand(B)
    Delta = expand(Delta)
    print("%s: A has %d terms, B has %d terms, Delta has %d terms" %
          (label, len(A.as_ordered_terms()), len(B.as_ordered_terms()),
           len(Delta.as_ordered_terms())))
    return A, B, Delta

A1, B1, D1 = compute_ABDelta(a1, b1, c1, "Poly 1 (w, b1, cp1)")
A2, B2, D2 = compute_ABDelta(a2, b2, c2, "Poly 2 (1-w, b2, cp2)")
Ah, Bh, Dh = compute_ABDelta(ah, bh, ch, "Sum (1, b1+b2, cp1+cp2)")
sys.stdout.flush()

print("\n" + SEP)
print("Computing numerator polynomial P...")
print(SEP)
print("P = Dh*(A1*B1)*(A2*B2) - D1*(Ah*Bh)*(A2*B2) - D2*(Ah*Bh)*(A1*B1)")

# 1/Phi4 = -Delta/(4*A*B)
# M = -Dh/(4*Ah*Bh) - (-D1/(4*A1*B1)) - (-D2/(4*A2*B2))
#   = -Dh/(4*Ah*Bh) + D1/(4*A1*B1) + D2/(4*A2*B2)
#
# Common denominator: 4*(Ah*Bh)*(A1*B1)*(A2*B2)
# On validity domain, each A*B < 0, so product (Ah*Bh)*(A1*B1)*(A2*B2) < 0
# So 4*D = 4*(Ah*Bh)*(A1*B1)*(A2*B2) < 0
#
# Numerator (with sign): -Dh*(A1*B1)*(A2*B2) + D1*(Ah*Bh)*(A2*B2) + D2*(Ah*Bh)*(A1*B1)
# M = numerator / 4*D
# Since D < 0, M >= 0 iff numerator <= 0
# i.e., Dh*(A1*B1)*(A2*B2) - D1*(Ah*Bh)*(A2*B2) - D2*(Ah*Bh)*(A1*B1) >= 0
#
# Let P = Dh*(A1*B1)*(A2*B2) - D1*(Ah*Bh)*(A2*B2) - D2*(Ah*Bh)*(A1*B1)

AB1 = expand(A1 * B1)
AB2 = expand(A2 * B2)
ABh = expand(Ah * Bh)

print("AB1 terms: %d" % len(AB1.as_ordered_terms()))
print("AB2 terms: %d" % len(AB2.as_ordered_terms()))
print("ABh terms: %d" % len(ABh.as_ordered_terms()))
sys.stdout.flush()

# Build P piece by piece
print("\nComputing term 1: Dh * AB1 * AB2...")
sys.stdout.flush()
term1 = expand(Dh * AB1 * AB2)
n1 = len(term1.as_ordered_terms())
print("  %d terms" % n1)
sys.stdout.flush()

print("Computing term 2: D1 * ABh * AB2...")
sys.stdout.flush()
term2 = expand(D1 * ABh * AB2)
n2 = len(term2.as_ordered_terms())
print("  %d terms" % n2)
sys.stdout.flush()

print("Computing term 3: D2 * ABh * AB1...")
sys.stdout.flush()
term3 = expand(D2 * ABh * AB1)
n3 = len(term3.as_ordered_terms())
print("  %d terms" % n3)
sys.stdout.flush()

print("\nComputing P = term1 - term2 - term3...")
sys.stdout.flush()
P = expand(term1 - term2 - term3)
terms = P.as_ordered_terms()
n_terms = len(terms)
print("P has %d terms" % n_terms)

td = total_degree(P)
print("Total degree of P: %d" % td)
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("Checking sign of P at random float points")
print(SEP)

import random
import numpy as np
random.seed(42)

# First check on validity domain
n_valid = 0
n_valid_neg = 0
min_P_valid = float('inf')

# Check on all of R^5
n_all = 0
n_all_neg = 0
min_P_all = float('inf')

for _ in range(100000):
    wv = random.uniform(0.05, 0.95)
    b1v = random.uniform(-0.5, 0.5)
    b2v = random.uniform(-0.5, 0.5)
    cp1v = random.uniform(-0.1, 0.1)
    cp2v = random.uniform(-0.1, 0.1)

    subs = {w: wv, b1: b1v, b2: b2v, cp1: cp1v, cp2: cp2v}
    Pval = float(P.subs(subs))

    n_all += 1
    if Pval < 0:
        n_all_neg += 1
    if Pval < min_P_all:
        min_P_all = Pval

    # Check if on validity domain
    A1v = float(A1.subs(subs))
    B1v = float(B1.subs(subs))
    A2v = float(A2.subs(subs))
    B2v = float(B2.subs(subs))
    Ahv = float(Ah.subs(subs))
    Bhv = float(Bh.subs(subs))
    D1v = float(D1.subs(subs))
    D2v = float(D2.subs(subs))
    Dhv = float(Dh.subs(subs))

    if (D1v > 0 and D2v > 0 and Dhv > 0 and
        A1v * B1v < 0 and A2v * B2v < 0 and Ahv * Bhv < 0):
        n_valid += 1
        if Pval < 0:
            n_valid_neg += 1
        if Pval < min_P_valid:
            min_P_valid = Pval

print("All R^5: %d tested, %d negative (%.2f%%)" % (n_all, n_all_neg, 100.0 * n_all_neg / max(1, n_all)))
print("Min P (all): %.6e" % min_P_all)
print("Validity domain: %d tested, %d negative" % (n_valid, n_valid_neg))
if n_valid > 0:
    print("Min P (valid): %.6e" % min_P_valid)
print("P >= 0 on validity domain: %s" % (n_valid_neg == 0))
print("P >= 0 everywhere: %s" % (n_all_neg == 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("Structure of P")
print(SEP)

# Print the polynomial in a readable form
poly_P = Poly(P, w, b1, b2, cp1, cp2)
print("Degree in each variable:")
for var in [w, b1, b2, cp1, cp2]:
    print("  %s: %d" % (var, degree(P, var)))

# Count monomials by degree
from collections import Counter
deg_counts = Counter()
for monom, coeff in poly_P.as_dict().items():
    total_deg = sum(monom)
    deg_counts[total_deg] += 1

print("\nMonomial count by total degree:")
for d in sorted(deg_counts.keys()):
    print("  degree %d: %d monomials" % (d, deg_counts[d]))

# Check symmetries
print("\nSymmetry checks:")
# b1 <-> b2 with cp1 <-> cp2 and w <-> 1-w
P_swapped = P.subs({b1: b2, b2: b1, cp1: cp2, cp2: cp1, w: 1-w})
P_swapped = expand(P_swapped)
print("  P(w,b1,b2,cp1,cp2) = P(1-w,b2,b1,cp2,cp1): %s" % (expand(P - P_swapped) == 0))

# b1 -> -b1, b2 -> -b2
P_neg = P.subs({b1: -b1, b2: -b2})
P_neg = expand(P_neg)
print("  P(w,b1,b2,cp1,cp2) = P(w,-b1,-b2,cp1,cp2): %s" % (expand(P - P_neg) == 0))
sys.stdout.flush()

# ============================================================
print("\n" + SEP)
print("VERDICT")
print(SEP)
if n_all_neg == 0:
    print("P >= 0 EVERYWHERE -> unconstrained SOS feasible!")
    print("Number of terms: %d, total degree: %d" % (n_terms, td))
    print("This is tractable for SOS decomposition")
elif n_valid_neg == 0:
    print("P >= 0 only on validity domain -> constrained SOS needed")
    print("Number of terms: %d, total degree: %d" % (n_terms, td))
else:
    print("P < 0 found on validity domain -> COUNTEREXAMPLE or formula error")

print("\nElapsed: %.1fs" % (time.time() - t0))
