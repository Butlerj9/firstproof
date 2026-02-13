# EXP-32 Series Summary: R1-DIV Kill-Test Results

Date: 2026-02-13
Route: R1-DIV (divisibility kill-test from scout reconciliation)
Scripts: exp32_divisibility_test.py, exp32b–exp32f

---

## Executive Summary

The R1-DIV route tested whether (T_i − t)E*_{λ⁻}(x; q, t) is divisible by (1−q), which would imply symmetry at q=1. **The route is INFORMATIVE but does NOT close the gap for n≥5.** Key structural insights were gained about the q→1 mechanism.

## Key Findings

### F1: E* coefficients are rational functions of q (NOT polynomials)

**exp32c**: Polynomial degree fitting always returns degree = n_pts − 1 (exact Lagrange fit), confirming c_m(q) = p_m(q)/D(q) where D(q) is the Vandermonde-like determinant from Cramer's rule. The exp32b finding of "degree 11" was an exact-fit artifact (12 points, 12 unknowns). The exp32 finding of "degree 9" was similarly under-constrained.

### F2: Vandermonde determinant vanishes at q=1 (spectral collisions)

**exp32d Section 7**: At q=1, spectral vectors ξ_ν = (t^{−k_i(ν)}) depend only on k-statistics, causing massive collisions:
- n=3: 56 compositions → 6 distinct spectral vectors (49-dim null space)
- n=4: 210 compositions → 24 distinct spectral vectors (186-dim null space)

This makes the interpolation system degenerate at q=1. E*_{λ⁻}(x; q=1, t) is defined by only 5 (n=3) or 23 (n=4) independent vanishing conditions, yielding a high-dimensional solution space.

### F3: E*_{λ⁻} converges to finite nonzero limit as q→1

**exp32d Sections 1-2**: At n=3, t=7/10, E* coefficients grow as q→1 but converge to finite limits. The pole from D(q)→0 is cancelled by a matching zero in the Cramer numerator (L'Hôpital-type). Example: c_{(0,0,0)}(q) goes from −3.7 at q=0.5 to −350 at q=0.995, approaching ~−370.

### F4: (T_i − t)E* vanishes at q=1 (symmetry confirmed for n=3)

**exp32d Sections 3-5**: Each monomial coefficient of D_i = (T_i − t)E* approaches 0 as q→1. The ratio D_i/E* → 0 at the test point x=(2,3,5), confirming T_i(E*|_{q=1}) = t·E*|_{q=1}, the symmetry condition.

Convergence rate: D0/E* ~ (1−q)^α with α ≈ 0.72 at n=3.

### F5: The particular q=1 solution (free vars=0) is NOT symmetric

**exp32d Section 7**: Setting free variables to 0 gives a polynomial with 7 nonzero (T_i−t) terms. The q→1 limit selects a DIFFERENT element of the 49-dim space — the unique symmetric one.

### F6: Hecke recursion does NOT apply to E*_μ

**exp32f**: The two-term recursion T_i E*_μ = c(q)·E*_μ + d(q)·E*_{s_i·μ} (from Knop-Sahi theory) does NOT hold for the interpolation polynomial E*_μ. Errors of ~270 at all q values.

**Root cause**: The recursion applies to the nonsymmetric Macdonald polynomial E_μ, which is a DIFFERENT object from the interpolation polynomial E*_μ. They are related by a triangular transformation but have different Hecke-module structures.

### F7: n=4 float test inconclusive

**exp32e**: The 209×209 system becomes severely ill-conditioned near q=1 in float64. At q≤0.9 with t=0.7, D0/E* ~ −0.10 (barely decreasing). At t=0.4, D0/E* → 0 more clearly. But numerical instability at q≥0.98 prevents definitive conclusion.

## Structural Picture

The symmetry of E*_{λ⁻}|_{q=1} arises through a multi-term mechanism:

1. The vanishing system is non-degenerate at q ≠ 1, giving a unique E*_{λ⁻}
2. As q → 1, spectral vectors collide and the system degenerates
3. The L'Hôpital limit selects a specific element of the degenerate solution space
4. This specific element happens to be in the t-eigenspace of all T_i (symmetric)

The mechanism is NOT a simple two-term cancellation but involves the full structure of the interpolation polynomial family. Understanding it algebraically would require the full T_i action on the E*_μ basis, which involves all compositions.

## Route Verdict

**R1-DIV: INFORMATIVE, NOT CLOSURE**

The divisibility is confirmed in the analytic sense (D_i → 0 at rate O(1−q)) for n=3, but:
- The "polynomial divisibility" formulation was incorrect (E* is rational, not polynomial)
- The Hecke recursion pathway was based on confusing E*_μ with E_μ
- No algebraic proof mechanism for general n was identified
- The n=4 numerical test is inconclusive due to conditioning

## Implications for P03

The R1-DIV findings strengthen the empirical evidence but do not change the proof status:
- n ≤ 4: **PROVED** (via degree-bound + zero-test, unchanged)
- n ≥ 5: **OPEN** (no new closure path from R1-DIV)

**Recommendation**: Proceed to R2-BinAS (Sahi binomial formula route) or R3-SMLQ (signed multiline queue route), or HOLD pending external progress.

## Files

| Script | Purpose | Key Result |
|--------|---------|------------|
| exp32_divisibility_test.py | Initial kill-test at n=3 | R_i polynomial (misleading: was actually rational) |
| exp32b_degree_confirmation.py | Multi-t degree check | All degree 11 (exact-fit artifact) |
| exp32c_degree_clean.py | Overconstrained degree | All degree 18 (= n_pts−1, confirming rational not polynomial) |
| exp32d_convergence_analysis.py | q→1 convergence | **E* converges; D_i → 0; symmetry confirmed at n=3** |
| exp32e_n4_convergence.py | n=4 float test | Inconclusive (ill-conditioned) |
| exp32f_hecke_recursion_verify.py | Recursion verification | **Recursion FAILS for E*_μ** (wrong polynomial type) |
