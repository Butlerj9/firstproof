"""
P04 CE-7: Check if n=4 ⊞₄ for centered quartics has cross-terms.
If coefficients don't add cleanly, the n=3 proof technique fails.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from fractions import Fraction

print("P04 CE-7: n=4 coefficient check under boxplus_4")
print("=" * 60)

n = 4
# c_k = sum_{i+j=k} [(n-i)!(n-j)! / (n!(n-k)!)] a_i b_j
# For centered: a_1 = b_1 = 0

def coeff(n, i, j):
    from math import factorial
    k = i + j
    return Fraction(factorial(n-i) * factorial(n-j), factorial(n) * factorial(n-k))

print(f"\n  boxplus_{n} coefficients for centered polynomials (a_1=b_1=0):\n")

for k in range(n+1):
    terms = []
    for i in range(k+1):
        j = k - i
        if i > n or j > n: continue
        c = coeff(n, i, j)
        if i == 1 or j == 1:  # vanishes for centered
            terms.append(f"  ({c})*a_{i}*b_{j} [=0, centered]")
        else:
            terms.append(f"  ({c})*a_{i}*b_{j}")
    print(f"  c_{k} = " + " + ".join(terms))

# For centered quartics:
print(f"\n  Simplified (centered):")
print(f"  c_0 = 1")
print(f"  c_1 = 0")
print(f"  c_2 = a_2 + b_2")
print(f"  c_3 = a_3 + b_3")

c22 = coeff(4, 2, 2)
print(f"  c_4 = a_4 + b_4 + ({c22})*a_2*b_2 = a_4 + b_4 + (1/6)*a_2*b_2")
print(f"\n  ** CROSS TERM in c_4: (1/6)*a_2*b_2 **")
print(f"  This breaks the clean additivity used in the n=3 proof.")
print(f"  The n=3 Jensen reduction does NOT generalize to n=4.")

print(f"\n  For n=3 (verification):")
for k in range(4):
    terms = []
    for i in range(k+1):
        j = k - i
        if i > 3 or j > 3: continue
        c = coeff(3, i, j)
        if i == 1 or j == 1:
            continue
        terms.append(f"({c})*a_{i}*b_{j}")
    nz = [t for t in terms if 'a_0' not in t and 'b_0' not in t]
    if nz:
        print(f"  c_{k} cross-terms: {', '.join(nz)}")
    else:
        print(f"  c_{k}: no cross-terms (clean addition)")

print(f"\n{'='*60}")
print("Verdict: n=3 proof exploits clean coefficient additivity,")
print("which fails for n>=4 due to cross-terms. Different approach needed.")
print("DONE")
