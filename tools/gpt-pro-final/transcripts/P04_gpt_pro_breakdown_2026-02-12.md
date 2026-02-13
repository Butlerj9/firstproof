# GPT-pro Breakdown — P04

Date: 2026-02-12  
Source: User-provided GPT-pro response  
Lane: P04  
Purpose: Extract actionable signal for one final Claude round.

---

## 1) High-Value Signal

### New primary bridge target
- **Boundary-minimum lemma** for the cleared-margin polynomial in `(a1,b1,c1',a2,b2,c2')`.
- Core reduction claim: if no interior minimizer exists in strict valid region, minimum lies on boundary strata reducible to previously solved subcases (`b=0`, `c'=0`, or discriminant boundary).

### Why this matters
- Directly attacks the known blocker (`b–c'` cross-terms).
- Avoids repeating failed Jensen/SOS/low-order perturbation routes.

---

## 2) Evidence-tier extraction

### Proved (already established in-lane)
- n=2,3 complete proofs.
- n=4 `b=0` subcase proof.
- coefficient-side setup and validity constraints used in CE-19 pipeline.
- normalized-coordinate reparameterization (`alpha,u,v`) repeatedly reconstructed in the trace and internally consistency-checked.

### Cited
- U-transform source (Marcus et al. finite free convolution representation).
- classical Stam/Fisher references (suggestive only, not closure).

### Empirical
- No counterexample on corrected exact sweeps (CE-19 context preserved).
- GPT response recommends symbolic KKT elimination as kill-test.
- Trace includes additional symbolic/numeric probes for transformed-domain concavity/structure, but no theorem-level certificate.

### Unresolved
- theorem-level sign certificate for general n=4 (`b≠0`) cleared-margin polynomial.

---

## 3) Novelty gate vs prior failed routes

### Non-variant enough to try
1. Boundary-minimum lemma + no-interior-critical-point attack.
2. External CAS decision-procedure fallback (CAD/quantifier elimination) with contamination logging.

### Likely low ROI for immediate cycle
1. U-transform to Fisher-information analogue (missing core identification lemma).
2. Haar-unitary Dirichlet form construction (speculative, high setup cost).

---

## 4) Added thinking-trace extraction (from extended transcript)

### Key technical additions from the long trace
1. Dimensionless normalization was pushed further than in the first summary:
   - `a = -alpha`, `u = b^2/alpha^3`, `v = c'/alpha^2`,
   - repeated attempts to express `1/Phi_4 = alpha * f(u,v)`.
2. Explicit effort to convert admissibility into a bounded semialgebraic region in `(u,v)` plus sign constraints.
3. Symbolic decomposition attempts (`f = const + g`) used to isolate cross-term behavior.
4. Directional second-derivative checks were explored to hunt for convexity/concavity leverage.
5. Net outcome unchanged: this did not remove the mixed `b-c'` obstruction.

### Practical implication
- The long trace strengthens confidence that local algebraic simplification has been materially explored.
- Best incremental value remains: boundary-minimum/KKT elimination plus hard stop to external CAD.

---

## 5) Recommended one-cycle plan (Claude)

### Route order
1. Boundary-minimum route (primary, bounded).
2. External CAS fallback only if primary route stalls.
3. U-transform/Haar routes deferred unless a concrete bridge lemma appears.

### Hard stop criteria
- If interior-critical-point elimination remains intractable after normalization + reduced-variable attempts, escalate to external CAD and stop local algebra sprawl.
- If external CAD does not produce a certificate/counterexample in allotted time, freeze status at candidate.

---

## 6) Contamination handling implication

- GPT response explicitly contemplates high-contamination escalation (external CAS + broad source search).
- If executed, must log:
  - exact source/tool,
  - UTC timestamp,
  - extracted statement/certificate,
  - contamination risk level,
  - integrate/quarantine decision.

---

## 7) Integration guidance

- Add one escalation event row to `P04/audit.md` referencing this GPT round.
- Add one compact entry in `P04/transcript.md` with:
  - prompt path,
  - response archive path,
  - accepted/rejected suggested routes.
- Update `RESULTS.md` only if new theorem-level closure or new formal blocker statement is adopted.
