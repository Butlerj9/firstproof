# Claude Code Checklist — P04 (From Claude Research Round 3)

Date: 2026-02-13  
Lane: P04 only  
Objective: execute the new `CLOSEABLE_NOW` computational routes first; only run analytic routes if computational certificates stall.

---

## 0) Load these first

1. `P04/answer.md`
2. `P04/audit.md`
3. `P04/RESULTS.md`
4. `tools/claude-research-final/transcripts/P04_claude_research_response_2026-02-13_round2.md`
5. `tools/claude-research-final/P04/102_claude_code_checklist_from_claude_research_round2.md`
6. `P04/experiments/ce29_exact_polynomial.py`
7. `P04/experiments/ce29b_fast_polynomial.py`
8. `P04/experiments/ce30c_subadditivity_polynomial.py`
9. `P04/experiments/ce31_canonical_target.md`
10. `P04/experiments/ce34_interval_cert.py`

---

## 1) Hard constraints

1. No theorem closure claim without a checkable certificate artifact.
2. Keep one canonical polynomial/domain target (no notation drift).
3. Empirical sweeps are evidence, not closure.
4. Log any new external theorem adoption in `CONTAMINATION.md`.

---

## 2) Primary route (execute in this order)

### A) Canonical target freeze

1. Reconfirm exact canonical objects:
   - degree-14, 837-term constrained target (`CE-29` family),
   - degree-34, 1612-term `phi`-subadditivity target (`CE-30c` family),
   - exact validity-domain inequalities.
2. Artifact:
   - `P04/experiments/ce36_canonical_targets_round3.md`

### B) Parametric SOS stratification (highest priority)

1. Build slice pipeline for `w = k/N`:
   - start with `N=40`, then `N=100` if margins are small.
2. For each fixed `w` slice:
   - solve constrained positivity for the reduced polynomial.
   - record certified lower bound `eps(w)`.
3. Compute global bound on `|dP/dw|` over domain.
4. Verify interpolation criterion: `max|dP/dw|/N < min_w eps(w)`.
5. Artifacts:
   - `P04/experiments/ce37_parametric_sos.py`
   - `P04/experiments/ce37_parametric_sos_report.md`

### C) Sparse full certificate attempt

1. Attempt sparse SOS/TSSOS-style certificate on full 5-variable target.
2. Capture solver settings, order, runtime, memory, and final status.
3. Artifacts:
   - `P04/experiments/ce38_sparse_full_cert.py`
   - `P04/experiments/ce38_sparse_full_cert_report.md`

### D) Bernstein subdivision fallback (3-variable target)

1. Convert 3-variable polynomial to Bernstein form on boxed valid domain.
2. Certify coefficient positivity or recursively subdivide.
3. Emit explicit “certified boxes” + unresolved boxes.
4. Artifacts:
   - `P04/experiments/ce39_bernstein_subdivision.py`
   - `P04/experiments/ce39_bernstein_subdivision_report.md`

---

## 3) Secondary route (only if section 2 does not close)

### E) Cumulant-coordinate scout test

1. Implement a minimal d=4 cumulant-coordinate transform prototype.
2. Numerically test superadditivity in cumulant coordinates.
3. Stop if transform does not yield tractable rational objective.
4. Artifacts:
   - `P04/experiments/ce40_cumulant_probe.py`
   - `P04/experiments/ce40_cumulant_probe_report.md`

### F) Score-projection scout test

1. Numerical sanity check for a finite score decomposition candidate on random quartic pairs.
2. Stop immediately if decomposition/projection contraction fails.
3. Artifacts:
   - `P04/experiments/ce41_score_projection_probe.py`
   - `P04/experiments/ce41_score_projection_probe_report.md`

---

## 4) Stop-loss gates

1. If route B yields negative certified slices after escalation (degree/order increase), stop and isolate those slices exactly.
2. If route C exceeds practical resource bounds without tightening lower bounds, stop and continue with route D.
3. If route D leaves unresolved boxes larger than tolerance with no shrinking trend, stop and output frontier certificate.
4. Do not run long analytic route work if no concrete bridge identity appears within one bounded cycle.

---

## 5) Required end-of-cycle outputs

1. A route verdict table: `closed / improved frontier / no progress`.
2. One-sentence current blocker (if not closed).
3. Update, at minimum:
   - `P04/audit.md`
   - `P04/answer.md` (only if proof-level closure)
   - `P04/RESULTS.md`
4. Sync status wording with root docs if lane status changes.

---

## 6) Minimal command skeleton

```powershell
git status -sb

python P04/experiments/ce37_parametric_sos.py
python P04/experiments/ce38_sparse_full_cert.py
python P04/experiments/ce39_bernstein_subdivision.py

# optional secondary probes
python P04/experiments/ce40_cumulant_probe.py
python P04/experiments/ce41_score_projection_probe.py

git status -sb
```

