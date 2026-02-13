# Claude Code Checklist — P04 (Post GPT-pro Round 3)

Date: 2026-02-13  
Lane: P04 only  
Scope: Continue from Session 18 state without rerunning Claude Research.

---

## 0) Inputs to load first

1. `P04/answer.md`
2. `P04/audit.md`
3. `P04/README.md`
4. `P04/RESULTS.md`
5. `P04/MEMORY.md`
6. `P04/experiments/ce28b_cp_convexity_deep.py`
7. `P04/experiments/ce28c_convexity_proof_structure.py`
8. `P04/experiments/ce29_exact_polynomial.py`
9. `P04/experiments/ce29b_fast_polynomial.py`
10. `P04/experiments/ce29c_discriminant_bound.py`
11. `P04/experiments/ce29d_individual_convexity.py`
12. `P04/experiments/ce30_symbolic_mpp.py`
13. `P04/experiments/ce30b_phi_subadditivity.py`
14. `P04/experiments/ce30c_subadditivity_polynomial.py`
15. `tools/gpt-pro-final/transcripts/P04_gpt_pro_response_2026-02-13.md`
16. `tools/gpt-pro-final/transcripts/P04_gpt_pro_breakdown_2026-02-13.md`
17. `tools/gpt-pro-final/transcripts/P04_gpt_pro_full_exchange_2026-02-13.md`

---

## 1) Immediate objective

1. Close the remaining P04 proof chain for general `n=4` (`b != 0`, `c' != 0`) by proving steps 2-3 symbolically:
   - `M''(t) >= kappa > 0` on the valid domain.
   - `2*kappa*M(0) >= (M'(0))^2`.
2. If symbolic closure fails, return a rigorous certificate path (interval/CAD) with exact blocker boundary.

---

## 2) Primary execution track (no generic restarts)

### A) Canonicalize the target inequality
1. Freeze one canonical normalized statement (P04-B1 style) and map it to existing `M(t)` formulation.
2. Ensure one source of truth for variables and domain constraints (remove parallel notations that drift).
3. Record this in a single memo:
   - `P04/experiments/ce31_canonical_normalized_form.md`

### B) Step-2 symbolic closure (`M'' >= kappa`)
1. Start from exact polynomial object already extracted in CE-29.
2. Attempt constrained positivity proof on the valid semialgebraic region using:
   - algebraic decomposition with known positive factors,
   - boundary-interior split (not raw SOS only),
   - reduced-variable normalization (scale fixing).
3. Artifact targets:
   - `P04/experiments/ce32_step2_symbolic.py`
   - `P04/experiments/ce32_step2_report.md`

### C) Step-3 symbolic closure (`2*kappa*M(0) >= M'(0)^2`)
1. Formalize `kappa` choice from Step 2 and derive exact inequality.
2. Prove with discriminant-aware factor decomposition and domain constraints.
3. Artifact targets:
   - `P04/experiments/ce33_step3_symbolic.py`
   - `P04/experiments/ce33_step3_report.md`

---

## 3) Secondary track (only if B/C stall): rigorous certification

1. Implement interval-certified positivity on normalized compact domain for the margin.
2. If needed, reduce to boundary families and run CAD/elimination on reduced systems.
3. Artifact targets:
   - `P04/experiments/ce34_interval_cert.py`
   - `P04/experiments/ce34_interval_report.md`
   - `P04/experiments/ce35_boundary_cad.py`
   - `P04/experiments/ce35_boundary_cad_report.md`

---

## 4) Stop-loss rules

1. If symbolic work does not reduce unsolved remainder within one bounded cycle, switch to certified computation.
2. If certified computation cannot complete, return a precise frontier certificate:
   - exact remaining inequality,
   - exact domain,
   - why current toolchain fails.
3. Do not claim theorem closure from empirical sweeps alone.

---

## 5) Required end-of-cycle updates

1. Update `P04/answer.md` only for theorem-level changes.
2. Update `P04/audit.md` with route outcomes and blocker status.
3. Sync summary statements across:
   - `P04/README.md`
   - `P04/RESULTS.md`
   - `P04/MEMORY.md`
4. Keep verdict explicit: `CLOSEABLE_NOW` only with proof/certificate; else `BLOCKED_WITH_FRONTIER`.

---

## 6) Minimal command skeleton

```powershell
git status -sb

python P04/experiments/ce32_step2_symbolic.py
python P04/experiments/ce33_step3_symbolic.py

# fallback if needed
python P04/experiments/ce34_interval_cert.py
python P04/experiments/ce35_boundary_cad.py

git status -sb
```

