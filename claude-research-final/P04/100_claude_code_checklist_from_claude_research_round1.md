# Claude Code Checklist — P04 (From Claude Research Round 1)

Date: 2026-02-12  
Lane: P04 only  
Goal: Run one bounded cycle on the new sparse-certificate + Schur-complement leads.

---

## 0) Load context first

1. `P04/answer.md`
2. `P04/audit.md`
3. `P04/transcript.md` (if present)
4. `P04/experiments/ce16_symbolic_proof.py`
5. `P04/experiments/ce19_corrected_validity.py`
6. `claude-research-final/transcripts/P04_claude_research_response_2026-02-12.md`
7. `claude-research-final/transcripts/P04_claude_research_breakdown_2026-02-12.md`

---

## 1) Hard constraints

1. No status upgrade without a checkable theorem-level artifact.
2. Tag all claims: `Proved / Cited / Empirical / Unresolved`.
3. Log any external theorem import before using it in lane docs.
4. Keep cycle bounded; do not drift into unbounded framework-building.

---

## 2) Route A (primary): sparse constrained certificate

### A1) Environment gate (mandatory)
1. Check availability:
   - Julia runtime,
   - `TSSOS` package,
   - SDP backend (`Mosek`, `COSMO`, `SDPA`, etc.).
2. If unavailable, mark Route A `dependency-blocked` and stop A.

### A2) Problem assembly
1. Reconstruct exact degree-16 margin polynomial from existing lane algebra.
2. Reconstruct exact semialgebraic constraints for admissible real-rooted region.
3. Export canonical artifacts:
   - `P04/experiments/ce26_margin_poly_and_constraints.py`
   - `P04/experiments/ce26_margin_poly_and_constraints.md`

### A3) Sparse Putinar attempts
1. Try low/moderate relaxation orders first.
2. Record:
   - success/failure,
   - numerical status,
   - certificate or infeasibility diagnostics.
3. Artifacts:
   - `P04/experiments/ce27_tssos_putinar.jl`
   - `P04/experiments/ce27_tssos_putinar_report.md`

---

## 3) Route B: Schur-complement lifting

1. Attempt algebraic lifting of cleared-margin expression into block matrix form.
2. Identify whether `b-c'` cross terms can be isolated in off-diagonal blocks.
3. Derive explicit PSD subconditions if possible.
4. Artifacts:
   - `P04/experiments/ce28_schur_lift.py`
   - `P04/experiments/ce28_schur_lift_report.md`

---

## 4) Route C (bounded memo): finite-score/projection route

1. Formalize finite score notation in lane variables.
2. Identify exact missing lemma needed to translate projection contraction to finite setting.
3. Deliver either:
   - concrete lemma candidate + toy verification, or
   - explicit “analogy only, not executable”.
4. Artifact:
   - `P04/experiments/ce29_finite_score_projection_memo.md`

---

## 5) Stop-loss gates

1. If Route A has no toolchain, do not claim SOS progress.
2. If Route B does not isolate cross terms in bounded steps, stop B.
3. If Route C yields no exact finite identity, keep as strategic note only.
4. If all routes fail to produce a proof/certificate, keep P04 at frontier.

---

## 6) Required outputs after cycle

1. Lane verdict: `CLOSEABLE_NOW` or `BLOCKED_WITH_FRONTIER`.
2. Route table A/B/C with pass/fail/dependency-blocked.
3. `P04/audit.md` escalation row.
4. `CONTAMINATION.md` updates for new adopted external statements.
5. `RESULTS.md` update only if status/claims changed.

---

## 7) Minimal command skeleton

```powershell
git status -sb

# Route A gate
julia --version

# Route B
python P04/experiments/ce28_schur_lift.py

git status -sb
```

