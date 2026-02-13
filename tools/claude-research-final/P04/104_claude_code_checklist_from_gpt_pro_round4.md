# Claude Code Checklist — P04 (From GPT-pro Round 4)

Date: 2026-02-13  
Lane: P04 only  
Goal: execute the invariant-reduction route first (`P_+`, `P_-`) and either produce a certificate or a tighter irreducible frontier.

---

## 0) Load context first

1. `P04/answer.md`
2. `P04/audit.md`
3. `P04/RESULTS.md`
4. `tools/gpt-pro-final/transcripts/P04_gpt_pro_response_2026-02-13_round2.md`
5. `tools/claude-research-final/P04/103_claude_code_checklist_from_claude_research_round3.md`
6. `P04/experiments/ce29_exact_polynomial.py`
7. `P04/experiments/ce30c_subadditivity_polynomial.py`
8. `P04/experiments/ce31_canonical_target.md`

---

## 1) Hard constraints

1. No status upgrade from empirical sweeps alone.
2. Keep one canonical reduced target/object throughout this cycle.
3. Every new transformation must be reversible back to original variables.
4. If external theorem statements are newly adopted, log in `CONTAMINATION.md`.

---

## 2) Primary execution route (GPT-pro derived)

### A) Build invariant reduction object

1. Implement reduction to variables:
   - `(alpha, beta, t1, t2, x1, x2, r)` with `alpha^2 + beta^2 = 1`, `r in {+1,-1}`.
2. Construct reduced margin numerator `P(alpha,beta,t1,t2,x1,x2,r)`.
3. Derive `P_+` and `P_-` by fixing `r = +1` and `r = -1`.
4. Confirm:
   - total degree and term count,
   - quadratic dependence in `r`,
   - explicit factorization of `[r^2]` coefficient.
5. Artifacts:
   - `P04/experiments/ce42_reduce_invariants.py`
   - `P04/experiments/ce42_reduce_invariants_report.md`

### B) Reduced-domain kill test

1. Implement feasible-domain sampler for reduced constraints.
2. Run robust random + local minimization for both `P_+`, `P_-`.
3. If robust negative interior point found, validate in original coordinates.
4. Artifacts:
   - `P04/experiments/ce43_reduced_killtest.py`
   - `P04/experiments/ce43_reduced_killtest_report.md`

### C) Certificate attempt on reduced problem

1. Attempt constrained SOS/Positivstellensatz for `P_+`, `P_-` on reduced semialgebraic set.
2. Start with low multiplier degree; increase once before stop-loss.
3. If possible, rationalize/verify certificate coefficients.
4. Artifacts:
   - `P04/experiments/ce44_reduced_sos_cert.py`
   - `P04/experiments/ce44_reduced_sos_cert_report.md`

---

## 3) Secondary route (if C stalls)

### D) Boundary-minimizer reduction

1. Test whether minima concentrate on boundary faces (`x1=0`, `x2=0`, discriminant boundary).
2. Reduce to lower-dimensional boundary systems and certify those.
3. Artifacts:
   - `P04/experiments/ce45_boundary_min_reduction.py`
   - `P04/experiments/ce45_boundary_min_reduction_report.md`

### E) Parametric slices fallback

1. Run fixed-`w` (or equivalent reduced coordinate) slice certificates.
2. Combine with Lipschitz interpolation only if margins are explicit and safe.
3. Artifacts:
   - `P04/experiments/ce46_parametric_slice_cert.py`
   - `P04/experiments/ce46_parametric_slice_cert_report.md`

---

## 4) Stop-loss gates

1. If reduced object exceeds practical complexity (degree/terms far above scout expectation), stop and report mismatch.
2. If reduced kill test finds validated interior negative, stop and escalate as candidate counterexample.
3. If SOS remains infeasible after one degree escalation, stop blind escalation and pivot to boundary reduction.
4. If boundary/slice routes do not shrink unresolved region measurably, return frontier update and halt.

---

## 5) Required end-of-cycle outputs

1. Route verdict table:
   - `A/B/C/D/E => success / fail / inconclusive`.
2. One-line blocker update (or closure statement with certificate reference).
3. Update:
   - `P04/audit.md` (required),
   - `P04/answer.md` (only on theorem-level closure),
   - `P04/RESULTS.md` (state/metrics sync).

---

## 6) Minimal command skeleton

```powershell
git status -sb

python P04/experiments/ce42_reduce_invariants.py
python P04/experiments/ce43_reduced_killtest.py
python P04/experiments/ce44_reduced_sos_cert.py

# fallback
python P04/experiments/ce45_boundary_min_reduction.py
python P04/experiments/ce46_parametric_slice_cert.py

git status -sb
```

