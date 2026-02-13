# Claude Code Checklist — P04 (From Claude Research Round 2)

Date: 2026-02-13  
Lane: P04 only  
Goal: convert the remaining `n=4` blocker into either a proof certificate or a precise irreducible frontier statement.

---

## 0) Load this context first

1. `P04/answer.md`
2. `P04/audit.md`
3. `P04/README.md`
4. `P04/RESULTS.md`
5. `P04/MEMORY.md`
6. `claude-research-final/transcripts/P04_claude_research_response_2026-02-13.md`
7. `claude-research-final/transcripts/P04_claude_research_breakdown_2026-02-13.md`
8. `claude-research-final/transcripts/P04_claude_research_full_exchange_2026-02-13.md`
9. `claude-research-final/P04/101_claude_code_checklist_from_gpt_pro_round3.md`
10. `P04/experiments/ce28b_cp_convexity_deep.py`
11. `P04/experiments/ce28c_convexity_proof_structure.py`
12. `P04/experiments/ce29_exact_polynomial.py`
13. `P04/experiments/ce29b_fast_polynomial.py`
14. `P04/experiments/ce29c_discriminant_bound.py`
15. `P04/experiments/ce29d_individual_convexity.py`
16. `P04/experiments/ce30_symbolic_mpp.py`
17. `P04/experiments/ce30b_phi_subadditivity.py`
18. `P04/experiments/ce30c_subadditivity_polynomial.py`

---

## 1) Hard constraints

1. No theorem claim without a checkable symbolic or certified-computation artifact.
2. Empirical sweeps are supporting evidence only; never closure evidence.
3. Keep one canonical statement + one canonical variable/domain system.
4. If external references are newly adopted, log contamination explicitly.

---

## 2) Route A (primary): bounded certification pipeline

### A1) Canonical target freeze
1. Write one canonical normalized margin statement and its exact domain constraints.
2. Map it explicitly to the current `M(t)` chain so there is no dual-notation drift.
3. Artifact:
   - `P04/experiments/ce36_canonical_target.md`

### A2) Symmetry reduction first
1. Apply available variable symmetries (including swap symmetry) before any heavy certificate call.
2. Emit reduced polynomial/object plus invertible map back to original variables.
3. Artifacts:
   - `P04/experiments/ce37_symmetry_reduce.py`
   - `P04/experiments/ce37_symmetry_reduce_report.md`

### A3) Sparse certificate attempts
1. Run sparse positivity attempts in this order:
   - sparse SOS/TSSOS-style,
   - SONC/SAGE-style,
   - DSOS/SDSOS-style quick feasibility.
2. Keep each attempt bounded with clear stop criteria.
3. Artifacts:
   - `P04/experiments/ce38_sparse_cert_attempts.md`

### A4) Subdivision fallback
1. If full-domain sparse certificates stall, subdivide normalized domain and certify subregions.
2. Prefer reducing to lower-dimensional subproblems where possible.
3. Artifacts:
   - `P04/experiments/ce39_subdivision_cert.py`
   - `P04/experiments/ce39_subdivision_cert_report.md`

---

## 3) Route B (secondary): symbolic chain closure (Step 2/3)

1. Re-attempt symbolic closure of:
   - `M''(t) >= kappa > 0`,
   - `2*kappa*M(0) >= M'(0)^2`.
2. Reuse canonicalized objects from Route A and explicit boundary/interior split.
3. Artifacts:
   - `P04/experiments/ce40_step2_symbolic_retry.py`
   - `P04/experiments/ce41_step3_symbolic_retry.py`
   - `P04/experiments/ce41_symbolic_retry_report.md`

---

## 4) Route C (tertiary): structural explorations (strictly gated)

Only run if A and B produce no shrinking of the unresolved remainder:

1. Score-function transfer route: proceed only with an explicit finite identity candidate.
2. Heat-flow route: proceed only with a concrete derivative-sign lemma tied to current polynomial target.
3. If no explicit lemma emerges quickly, stop C immediately.

Artifact:
- `P04/experiments/ce42_structural_memo.md`

---

## 5) Stop-loss gates

1. If Route A cannot produce either a certificate or a smaller unresolved set, freeze and report exact blocker.
2. If Route B repeats previous algebraic sprawl without new lemma, terminate B.
3. No route drift: all work must reduce the current blocker directly.

---

## 6) Required outputs at end of cycle

1. Lane verdict table with pass/fail per route.
2. Updated blocker statement in one sentence.
3. Update:
   - `P04/audit.md`,
   - `P04/answer.md` (only if theorem-level),
   - `P04/README.md`,
   - `P04/RESULTS.md`,
   - `P04/MEMORY.md`.
4. If unresolved: include exact remaining polynomial/domain object and why current tools failed.

---

## 7) Minimal command skeleton

```powershell
git status -sb

python P04/experiments/ce37_symmetry_reduce.py
# run certificate attempts / reports
# run subdivision fallback if needed

python P04/experiments/ce40_step2_symbolic_retry.py
python P04/experiments/ce41_step3_symbolic_retry.py

git status -sb
```

