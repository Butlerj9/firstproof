# Claude Code Checklist — P03 (From Claude Research Round 1)

Date: 2026-02-12  
Lane: P03 only  
Goal: Convert the new 14-route research output into one bounded, reproducible closure attempt.

---

## 0) Load context first

1. `P03/answer.md`
2. `P03/audit.md`
3. `P03/transcript.md`
4. `P03/experiments/exp18_n5_benchmark.py`
5. `P03/experiments/exp20_branching_test.py`
6. `tools/claude-research-final/transcripts/P03_claude_research_response_2026-02-12.md`
7. `tools/claude-research-final/transcripts/P03_claude_research_breakdown_2026-02-12.md`

---

## 1) Hard constraints

1. No status upgrade without theorem-level closure or mechanically checkable certificate.
2. Preserve labels: `Proved / Cited / Empirical / Unresolved`.
3. Treat old blocked routes as blocked unless the bridge lemma is genuinely distinct.
4. Log every external source used in escalation format (source, UTC, extracted statement, risk, use decision).
5. Keep cycle bounded; avoid unbounded symbolic expansion at `n=5`.

---

## 2) Route order (one-cycle execution)

### Route A (primary): symmetric-subspace vanishing dimension test (Approach 10)

1. Build collapsed spectral set at `q=1` for selected `n=5` anti-dominant targets.
2. Construct linear constraints in the symmetric polynomial basis up to degree `|lambda|`.
3. Compute dimension of constrained symmetric subspace.
4. Test whether dimension is exactly 1 in sampled targets.
5. Artifacts:
   - `P03/experiments/exp21_symmetric_vanishing_dim.py`
   - `P03/experiments/exp21_symmetric_vanishing_dim_report.md`

### Route B (secondary): signed multiline queue q=1 invariance pilot (Approach 1)

1. Extract explicit signed multiline queue weights from cited source.
2. Implement small-instance evaluator at `q=1`.
3. Test transposition invariance under `x_i <-> x_{i+1}` for anti-dominant test cases.
4. Artifacts:
   - `P03/experiments/exp22_signed_queue_q1_probe.py`
   - `P03/experiments/exp22_signed_queue_q1_report.md`

### Route C (optional bounded): rational KZ mapping pilot (Approach 5)

1. Identify smallest case where interpolation object maps to shifted Jack/KZ setting.
2. Determine whether monodromy test is computable in that case.
3. Produce “viable/non-viable” memo, not a full proof.
4. Artifacts:
   - `P03/experiments/exp23_kz_mapping_probe.md`

---

## 3) Stop-loss gates

1. If Route A cannot produce stable dimension computations in bounded runtime:
   - stop Route A and report computational blocker.
2. If Route B lacks enough explicit formula details to implement faithfully:
   - mark dependency-blocked and do not speculate.
3. If Route C cannot produce a concrete computable monodromy test:
   - terminate Route C immediately.
4. If all routes stall without bridge-lemma progress:
   - keep P03 at candidate and update frontier text only.

---

## 4) Required deliverables after cycle

1. Lane verdict line: `CLOSEABLE_NOW` or `BLOCKED_WITH_FRONTIER`.
2. Table of tested routes (A/B/C), with pass/fail/dependency-blocked.
3. `P03/audit.md` escalation row summarizing this cycle.
4. `P03/transcript.md` compact transcript entry with artifact paths.
5. `CONTAMINATION.md` entries for any new external references.

---

## 5) Minimal command skeleton

```powershell
git status -sb

# route A
python P03/experiments/exp21_symmetric_vanishing_dim.py

# route B
python P03/experiments/exp22_signed_queue_q1_probe.py

git status -sb
```

