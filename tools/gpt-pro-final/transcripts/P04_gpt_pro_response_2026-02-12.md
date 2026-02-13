# GPT-pro Transcript — P04

Date captured: 2026-02-12  
Source: User-provided GPT-pro response (manual paste)  
Lane: P04  
Integration intent: Archive response for downstream Claude/Codex review and reconciliation.

---

## Raw Response

## SECTION A: Lane Verdict Table

| Lane | StatusBefore                                                               | BestNewBridgeLemma                                                                                                                                                                                                                                                | KillTest                                                                                                                                                                                                                          | Verdict                   | Why                                                                                                                                                                                                                                                                                                                              |
| ---- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P04  | [Unresolved] n=4 general (b≠0) only; [Proved] n=2,3; [Proved] n=4 with b=0 | [Unresolved] **Boundary-minimum lemma**: after scaling/centering, the superadditivity margin has no interior minimizer in the 4-real-root region, so the global minimum occurs on boundary strata where it reduces to already-proved subcases (b=0, c′=0, or Δ=0) | [Empirical] Symbolically compute Lagrange multiplier system for interior critical points of the cleared-denominator margin (degree-15/16 polynomial); attempt elimination → show no solutions in the admissible semialgebraic set | **BLOCKED_WITH_FRONTIER** | [Empirical] exhaustive sweeps (CE-19) found no counterexample; [Unresolved] but a proof needs a new structural lemma to control the **b–c′ cross-terms** in the cleared margin polynomial; [Cited] no known theorem in foundational sources implies it directly, and prior routes (1–9) block the standard convexity/SOS avenues |

---

## SECTION B: Actionable Plan

### 1) Top 3 novel approaches

#### 1.0 Failure map (exact unresolved statement + minimal blocking lemma)

* [Proved] For centered quartics (f(x)=x^4+a x^2+b x+c) with 4 real roots, define (c' := c - a^2/12).  
  [Proved] Under (\boxplus_4), the parameters ((a,b,c')) **add componentwise**: (a_h=a_1+a_2), (b_h=b_1+b_2), (c'_h=c'_1+c'_2).
* [Proved] The n=4 functional has closed form  
  [
  \Phi_4(f)=\frac{-4(a^2+12c)(2a^3-8ac+9b^2)}{\Delta(f)}\quad\Rightarrow\quad \frac{1}{\Phi_4(f)}=\frac{-\Delta(f)}{4(a^2+12c)(2a^3-8ac+9b^2)},
  ]  
  with (\Delta) the quartic discriminant.
* [Proved] Validity region for “4 real roots” can be encoded by (\Delta>0) **and** ((a^2+12c)(2a^3-8ac+9b^2)<0) (equivalently (1/\Phi_4>0)).
* [Unresolved] Goal: for all valid centered quartics (p,q), prove  
  [
  \frac{1}{\Phi_4(p\boxplus_4 q)};\ge;\frac{1}{\Phi_4(p)}+\frac{1}{\Phi_4(q)}.
  ]
* [Unresolved] Minimal blocking lemma: after clearing denominators using the closed form, the inequality is equivalent (on the valid region) to **a single explicit cleared-margin polynomial inequality** in ((a_1,b_1,c'_1,a_2,b_2,c'_2)) (reported as “degree-16”, computed symbolically as a high-degree polynomial numerator). The obstruction is that the polynomial has **mixed (b)–(c′)** terms preventing the successful decompositions that work for (b=0).

#### 1.1 Candidate approach families (≥12; ≥4 cross-domain transfers)

(Each bullet is a distinct “approach family”; cross-domain transfers are marked **[Xfer]**.)

1. [Xfer][Unresolved] **U-transform → classical sum model → Stam-style projection inequality** (finite-free convolution as expectation over sums of independent RVs after U-transform).
2. [Xfer][Unresolved] **Random-matrix / Haar unitary model + conditional expectation** (finite-free convolution as expected characteristic polynomial of (A+UBU^*)); try to build a “score” and reuse the classical proof pattern (projection lowers Fisher information).
3. [Xfer][Unresolved] **Lie-group functional inequalities (LSI/Poincaré on (U(n)))** to control a Dirichlet form naturally producing (\sum_i(\sum_{j\ne i}1/(\lambda_i-\lambda_j))^2).
4. [Xfer][Unresolved] **Calogero–Moser/Coulomb gas energy**: interpret (u_i=\sum_{j\ne i}1/(\lambda_i-\lambda_j)) as log-Vandermonde gradient; try energy convexity under the finite-free mixing operation.
5. [Unresolved] **Boundary-minimum / “no interior critical point” lemma** (real algebraic geometry + Lagrange multipliers) to reduce to boundary strata where known cases apply.
6. [Unresolved] **Resultant/discriminant parametrization**: eliminate (c) via (c'), reduce admissible region to inequalities in a smaller set of invariants, then prove margin positivity via Sturm chains.
7. [Unresolved] **Hyperbolic polynomial barrier method**: relate (1/\Phi) to curvature of the barrier for the hyperbolicity cone; attempt Minkowski-type superadditivity.
8. [Unresolved] **Majorization/Schur convexity on gap variables** (g_1,g_2,g_3) for quartic roots; prove the operation induced by (\boxplus_4) is a “mean” that decreases (\Phi).
9. [Unresolved] **Extremal principle**: show worst-case occurs for “most symmetric” quartics (two equal gaps, or “nearly double-root”), using rearrangement + perturbation about double roots.
10. [Unresolved] **Interpolation path**: define (p_t) with cumulants ((a,b,c')) linear in (t); prove (t\mapsto 1/\Phi_4(p_t)) is convex with explicit second derivative sign.
11. [Unresolved] **Certificate by structured SOS ansatz** (not full SDP): guess low-degree square terms informed by symmetries (swap 1↔2, sign (b\mapsto -b)), solve coefficients by linear constraints.
12. [Unresolved] **Moment-matching / orthogonal polynomial representation**: express quartics as truncated orthogonal polynomial expectations; try to lift to an inequality for moment matrices.

#### 1.2 Novelty/viability gate (remove variants of failed routes 1–9)

* [Proved] Discard as variants:

  * [Proved] Any direct “finite de Bruijn identity” route (failed route 1).
  * [Proved] K-transform Taylor-series-only arguments (failed route 2).
  * [Proved] “Just algebra in coefficients” hoping cancellation (failed route 3) unless it introduces a genuinely new invariant/decomposition.
  * [Proved] Pure Jensen/Cauchy-Schwarz weight-mismatch arguments (failed route 4).
  * [Proved] Generic SOS/SDP/Putinar attempts without new symmetry reduction (failed routes 5 & 7).
  * [Proved] Global concavity-in-cumulants (failed route 8).
  * [Proved] Low-order perturbative expansion in (b) (failed route 9).

* [Unresolved] Survivors (non-variants) with best plausibility-to-effort ratio:

  * (A) **Boundary-minimum lemma** (family 5).
  * (B) **U-transform → classical sum model** (family 1) + a new identification of (\Phi_4) as an information/Dirichlet form.
  * (C) **Random-matrix / Haar + group functional inequality** (families 2–3) to manufacture a projection inequality.

#### 1.3 Top 3 (kept) with skeleton, earliest fail-point, fallback bridge lemma

##### Top 1 — Boundary-minimum lemma (real algebraic geometry reduction)

* **Core idea** [Unresolved]: Work with the explicit rational margin
  [
  M:=\frac{1}{\Phi_4(h)}-\frac{1}{\Phi_4(p)}-\frac{1}{\Phi_4(q)},
  \quad h=p\boxplus_4 q,
  ]
  write (M=\text{num}/\text{den}) using the closed form for (1/\Phi_4), and use the sign-known admissible region to reduce (M\ge0) to (\text{num}\le 0) (or (-\text{num}\ge0)).
  [Proved] The denominator factors explicitly into ((a_i^2+6c'_i)(4a_i^3-24a_ic'_i+27b_i^2)) for (i=1,2,h) (up to a positive constant), so it has **fixed sign** on the valid region (product of three negatives).
* **Bridge lemma** [Unresolved]: The global minimum of (-\text{num}) on the semialgebraic “valid” set occurs on boundary strata where either:

  * (\Delta_1=0) or (\Delta_2=0) or (\Delta_h=0) (double root → (1/\Phi\to 0)), or
  * (b_1=0) or (b_2=0) (reduces to already proved b=0 machinery), or
  * (c'_1=0) or (c'_2=0) (the other easy axis),
    and hence the inequality follows by reduction to proved cases + continuity.
* **Earliest fail-point** [Unresolved]: Proving “no interior minimizer” (or that interior critical points cannot occur in the strict-valid region) is nontrivial; naïve KKT/Lagrange multiplier elimination may blow up.
* **Fallback bridge lemma** [Unresolved]: Show that any interior critical point forces an algebraic relation that contradicts (\Delta>0) and the sign constraints, e.g. by proving the critical-point ideal implies (\Delta_h\le 0) or (A_hB_h\ge 0).
* **Kill test** [Empirical]:

  * Symbolically set up KKT system: (\nabla(-\text{num})=\sum \lambda_j \nabla g_j) with (g_j) the active constraints (start with unconstrained interior: (\nabla(-\text{num})=0)).
  * Eliminate (\lambda_j) and verify the resulting variety has no real points in the strict-valid region (via resultants + random-direction sign checks).
  * If you can’t eliminate, attempt a targeted elimination under a normalization (e.g., fix a scaling gauge such as (a_h=-1) and a translation gauge), then compute Gröbner basis in the reduced ring.

##### Top 2 — U-transform + Stam-style projection (information-theoretic transfer)

* **Foundational hook** [Cited]: Marcus’ **U-transform** gives random variables (S,T) such that for degree (m) polynomials (p,q), the symmetric additive convolution satisfies
  [
  [p\ !m\ q](x)=\mathbb{E}\big[(x-S-T)^m\big]
  ]
  when (S,T) are independent and (p(x)=\mathbb{E}[(x-S)^m]), (q(x)=\mathbb{E}[(x-T)^m]). ([Princeton Math][1])
* **Core idea** [Unresolved]: Replicate the classical Fisher-information proof pattern (projection / conditional expectation) for the polynomial functional (\Phi_4) by:

  1. defining a “score” object (\rho_p) attached to (p(x)=\mathbb{E}[(x-S)^4]) such that (\Phi_4(p)=\mathbb{E}[\rho_p(S)^2]) (or a close analog),
  2. showing the score of (S+T) is the conditional expectation of component scores given (S+T), and
  3. applying the same Cauchy–Schwarz step as in Stam to conclude superadditivity of the reciprocal.
* **Earliest fail-point** [Unresolved]: There is **no known identification** (yet) of (\Phi_4(p)) as a Fisher information (or Dirichlet form) of the U-transform RV (S); additionally (S) may be complex-valued even if (p) is real-rooted (e.g., (p(x)=x^2-1) has U-transform ({\pm i})). ([Princeton Math][1])
* **Fallback bridge lemma** [Unresolved]: You don’t need a full Fisher-information interpretation—only a Hilbert-space identity of the form
  [
  \Phi_4(p)=|\Pi_p|^2,\quad \Pi_{p\boxplus q}=\mathbb{E}[\Pi_p,|,S+T]+\mathbb{E}[\Pi_q,|,S+T]
  ]
  with (|\cdot|) a norm for which conditional expectation is a contraction.
* **Kill test** [Empirical]:

  * Take many random quartics with 4 real roots, compute (\Phi_4(p)) from coefficients.
  * Compute the U-transform multiset for (p) (numerically from Marcus’ construction) and test candidate “score” formulas built from the weights ((\lambda-S)^k) at roots (\lambda) of (p).
  * If no stable candidate emerges (high variance, wrong scaling), abandon.

##### Top 3 — Random-matrix / Haar-unitary Dirichlet form (group-inequality transfer)

* **Core idea** [Unresolved]: Use the matrix model for finite free convolution: if (p,q) are characteristic polynomials of Hermitian (A,B), then (p\boxplus_n q) equals the expected characteristic polynomial of (A+U B U^*) with Haar (U).
  Then attempt to express (\Phi_n(p)) as a Dirichlet form (energy) of a natural function on (U(n)) or on eigenvalue configurations—so that a **Poincaré/LSI-type inequality** yields the desired reciprocal superadditivity (projection lowers energy).
* **Why it’s non-variant** [Proved]: This is not “Jensen weight-mismatch” (failed route 4) nor “generic SOS” (failed routes 5/7); it tries to manufacture a **projection contraction** at the group-measure level, mirroring the classical Stam proof mechanism.
* **Earliest fail-point** [Unresolved]: I don’t currently have a clean identity relating (\Phi_4) to a Dirichlet form on (U(4)); establishing it may require new derivations (HCIZ derivative identities, etc.).
* **Fallback bridge lemma** [Unresolved]: Prove a weaker inequality
  [
  \Phi_4(p\boxplus_4 q)\ \le\ \alpha^2 \Phi_4(p)+(1-\alpha)^2\Phi_4(q)
  ]
  for a smartly chosen (\alpha) (as in the classical route to Stam), by interpreting (\Phi_4) as a quadratic form of a score function and using orthogonal projection in (L^2(U(4))).
* **Kill test** [Empirical]:

  * Pick explicit diagonal (A,B\in\mathbb{R}^{4\times4}) with simple spectra.
  * Numerically sample many Haar (U), approximate (\mathbb{E}[\det(xI-(A+UBU^*))]) to recover (p\boxplus_4 q), then verify whether a candidate Dirichlet-form identity correlates with (\Phi_4).
  * If no correlation, this route is likely too speculative.

### 2) Fastest theorem-level closure path

**Recommendation (ranked)**

1. **Boundary-minimum lemma route** (Top 1) is the fastest to a fully rigorous n=4 closure **without importing large external machinery**, because it targets exactly the current blocker: the b–c′ cross-terms in a single explicit polynomial inequality. [Unresolved]

2. If boundary-minimum fails, escalate to an **off-limits computational decision procedure** (CAD / exact SDP / real quantifier elimination) run outside this environment (Mathematica/Maple/Sage + external solvers), documenting contamination as “high but mechanistic.” [Unresolved]

3. Only then pursue U-transform / matrix-information transfers (Top 2/3), which are elegant but currently missing the key identification lemma. [Unresolved]

**48-hour ranked plan with stop-loss**

* **T0–T6h: Set up the exact algebraic object**

  * [Proved] Write the margin (M) as a single rational function in ((a_1,b_1,c'_1,a_2,b_2,c'_2)) using (1/\Phi_4=-\Delta/(4AB)).
  * [Proved] Clear denominators to get a single polynomial “cleared margin numerator” (\mathcal{N}) such that (M\ge0) is equivalent (on the valid region) to (\mathcal{N}\le0).
  * **Stop-loss** [Unresolved]: If you cannot express (\mathcal{N}) cleanly with constraints in ≤6 variables, stop and move to external CAS.

* **T6–T20h: Prove or refute the “no interior minimizer” claim**

  * [Unresolved] Attempt: compute (\nabla \mathcal{N}=0) and eliminate to see if any real solutions exist with (\Delta_1,\Delta_2,\Delta_h>0) and ((a^2+6c')(4a^3-24ac'+27b^2)<0) for each of (p,q,h).
  * **Stop-loss** [Unresolved]: If Gröbner elimination grows beyond tractable size, pivot to partial normalizations (fix scale + translation gauge), then reattempt; if still intractable → go to external CAD.

* **T20–T36h: Boundary stratification proof**

  * [Unresolved] Prove that on each boundary stratum (e.g., (b_1=0), (b_2=0), (c'_1=0), (c'_2=0), (\Delta_i=0)) the inequality reduces to already proved subcases or to a 1D inequality in (w).
  * **Stop-loss** [Unresolved]: If any stratum introduces a genuinely new unsolved inequality, this plan won’t close.

* **T36–T48h: Escalation (explicitly “contaminated”)**

  * [Unresolved] Run external real-algebraic decision tools on (\mathcal{N}) with the semialgebraic constraints:

    * CAD / quantifier elimination, or
    * Exact SOS with symmetry reduction (if tool supports rational certificates).
  * [Unresolved] Output should be a checkable certificate: either “(\mathcal{N}\le 0) on region” with a certificate, or a counterexample.

**Contamination / escalation log**

* [Cited] I already used foundational external material only to confirm the U-transform representation of finite-free convolution. ([Princeton Math][1])
* [Empirical] I also searched the open web for an existing proof/solution of the exact (\Phi_4) inequality and found none (no usable theorem-level closure surfaced in results).
* [Unresolved] The planned escalation to CAD/SDP is “high contamination” (tool-dependent) but produces mechanically checkable artifacts.

### 3) One-sentence frontier statement if blocked

* [Unresolved] **Frontier:** P04 for n=4 reduces to showing a single explicit cleared-denominator polynomial (degree ≈15–16 in ((a_1,b_1,c'_1,a_2,b_2,c'_2))) is nonnegative/has fixed sign on the semialgebraic “4-real-root” region, and the only missing ingredient is a structural lemma that controls the mixed (b)–(c′) cross-terms (no such lemma or certificate is currently known from the explored routes).

### 4) Required external theorem statements or no_known_theorem

* [Cited] **U-transform sum representation** (Marcus): for degree (m) polynomials (p,q), with (p(x)=\mathbb{E}[(x-S)^m]), (q(x)=\mathbb{E}[(x-T)^m]) and independent (S,T), their symmetric additive convolution satisfies ([p\ m\ q](x)=\mathbb{E}[(x-S-T)^m]). ([Princeton Math][1])
* [Cited] **Classical Stam/Fisher information inequality**: for independent (X,Y) with suitable densities, (1/I(X+Y)\ge 1/I(X)+1/I(Y)). (Needed only if Top 2 succeeds in identifying (\Phi_4) as a Fisher information analogue.) ([yaroslavvb.com][2])
* [no_known_theorem][Unresolved] A theorem directly identifying (\Phi_4(p)) with a Fisher-information/Dirichlet-form of a U-transform or Haar-unitary model in a way that yields a projection contraction.

[1]: https://web.math.princeton.edu/~amarcus/papers/ff_main.pdf "https://web.math.princeton.edu/~amarcus/papers/ff_main.pdf"
[2]: https://www.yaroslavvb.com/papers/zamir-proof.pdf "https://www.yaroslavvb.com/papers/zamir-proof.pdf"

---

## Integration Notes

- This transcript is archived verbatim for auditability.
- Follow-up integration into core artifacts (`P04/audit.md`, `P04/transcript.md`, `RESULTS.md`) should preserve the proved/cited/empirical/unresolved taxonomy.
- External references proposed here should be logged to `CONTAMINATION.md` if incorporated in a subsequent lane cycle.
