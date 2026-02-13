# Claude Code Checklist — P04 (Post GPT-pro Round 2)

Date: 2026-02-12  
Lane: P04 only  
Goal: either close general `n=4` (`b != 0`) or return a strict frontier certificate with reproducible evidence.

---

## 0) Inputs to load first

1. `P04/answer.md`
2. `P04/audit.md`
3. `P04/transcript.md` (if present)
4. `P04/experiments/ce16_symbolic_proof.py` (proved `b=0` subcase)
5. `P04/experiments/ce19_corrected_validity.py` (corrected admissibility sweeps)
6. `gpt-pro-final/transcripts/P04_gpt_pro_response_2026-02-12.md`
7. `gpt-pro-final/transcripts/P04_gpt_pro_breakdown_2026-02-12.md`
8. `gpt-pro-final/transcripts/P04_gpt_pro_full_exchange_2026-02-12.md`

---

## 1) Hard constraints (do not violate)

1. Do not claim closure without a checkable theorem-level certificate.
2. Treat prior failed routes as blocked unless you add a genuinely new bridge lemma.
3. Keep all claims tagged: `Proved / Cited / Empirical / Unresolved`.
4. If any external/off-limits source is used, log contamination immediately (source, UTC time, exact extracted statement, risk, integration decision).
5. Stop if repeating algebraic sprawl without new lemma progress.

---

## 2) Primary route (highest ROI): boundary-minimum/KKT

### A) Rebuild exact target object
1. Reconstruct cleared-margin inequality for
   - `1/Phi4(p boxplus4 q) >= 1/Phi4(p) + 1/Phi4(q)`.
2. Verify denominator sign fixed on strict-valid region.
3. Extract final numerator polynomial `N(a1,b1,c1',a2,b2,c2')`.
4. Save the exact symbolic expression to a reproducible artifact:
   - `P04/experiments/ce21_margin_numerator_extract.py`
   - `P04/experiments/ce21_margin_numerator.txt`

### B) Interior critical-point attack
1. Build system `grad(N)=0` on strict-valid interior.
2. Try elimination in stages (not all-at-once):
   - raw system,
   - normalized gauge reduction,
   - symmetry-reduced branch cases.
3. Record whether real solutions survive admissibility constraints.
4. Artifact targets:
   - `P04/experiments/ce22_kkt_interior_elimination.py`
   - `P04/experiments/ce22_kkt_report.md`

### C) Boundary stratification closure
1. Enumerate boundary families:
   - `b1=0`, `b2=0`, `c1'=0`, `c2'=0`, `Delta1=0`, `Delta2=0`, `Deltah=0`.
2. Reduce each stratum to known solved forms or 1D checks.
3. Document any surviving unsolved stratum explicitly.
4. Artifact targets:
   - `P04/experiments/ce23_boundary_strata.py`
   - `P04/experiments/ce23_boundary_report.md`

---

## 3) Stop-loss gates (strict)

1. If `ce22` cannot eliminate interior solutions after gauge + symmetry reductions:
   - mark primary route `UNRESOLVED`,
   - move to external CAD escalation.
2. If any boundary stratum produces a fresh unsolved inequality:
   - no status upgrade,
   - freeze at frontier.
3. If runtime balloons without narrowing the blocker:
   - terminate and summarize blockers only.

---

## 4) Last-resort escalation (allowed, high-contamination)

1. External CAD/quantifier elimination or exact SOS certificate tooling is allowed as final resort.
2. Required logs for each escalated run:
   - tool/system,
   - version,
   - UTC timestamp,
   - exact input formula/constraints,
   - exact output artifact (certificate or counterexample),
   - contamination rating.
3. If certificate is found, store raw certificate and verifier script.
4. If no certificate/counterexample, return `BLOCKED_WITH_FRONTIER`.

---

## 5) Optional secondary route (only if time remains)

1. U-transform / Fisher-information analogy:
   - only continue if a concrete identity candidate for `Phi4` as a norm/energy is produced.
2. Haar-unitary Dirichlet route:
   - only continue if an explicit candidate quadratic form and projection-contraction statement are formalized.
3. Otherwise stop; do not burn cycle budget on speculative route drift.

---

## 6) Required end-of-run deliverables

1. Lane verdict table (`CLOSEABLE_NOW` or `BLOCKED_WITH_FRONTIER`).
2. Evidence table with `Proved / Cited / Empirical / Unresolved`.
3. Updated `P04/audit.md` escalation row.
4. Updated `P04/answer.md` only if theorem-level content changed.
5. Updated `CONTAMINATION.md` entries for all escalations.
6. Short “what changed / what failed / why frozen” note for `RESULTS.md` if status unchanged.

---

## 7) Minimal command skeleton

```powershell
# Preflight
git status -sb

# Run primary scripts (names may differ if already existing)
python P04/experiments/ce21_margin_numerator_extract.py
python P04/experiments/ce22_kkt_interior_elimination.py
python P04/experiments/ce23_boundary_strata.py

# Record outputs
git status -sb
```

