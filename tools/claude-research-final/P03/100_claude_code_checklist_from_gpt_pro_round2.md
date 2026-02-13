# Claude Code Checklist — P03 (From GPT-pro Round 2)

Date: 2026-02-12  
Lane: P03 only  
Goal: Execute one bounded cycle using the corrected target from GPT-pro P03.

---

## 0) Critical correction (must apply first)

1. Do **not** target the old x-independent Mallows proportionality route.
2. New target is an explicit chain (likely x-dependent) or equivalent local exchange-relations proof.
3. Keep P03 status unchanged unless theorem-level closure appears.

---

## 1) Inputs to load

1. `P03/answer.md`
2. `P03/audit.md`
3. `P03/transcript.md`
4. `P03/experiments/exp20_branching_test.py`
5. `tools/gpt-pro-final/transcripts/P03_gpt_pro_response_2026-02-12.md`
6. `tools/gpt-pro-final/transcripts/P03_gpt_pro_breakdown_2026-02-12.md`
7. `tools/claude-research-final/P03/99_claude_code_checklist_from_research_round1.md`

---

## 2) Primary route order for this cycle

### Route A — n=2 exact anchor (mandatory)

1. Re-derive q=1 weights for the smallest restricted case from cited interpolation formulas.
2. Build explicit two-state continuous-time chain candidate with x-dependent rates.
3. Verify detailed balance and normalization exactly.
4. Artifacts:
   - `P03/experiments/exp24_n2_q1_anchor.py`
   - `P03/experiments/exp24_n2_q1_anchor_report.md`

### Route B — n=3 local generator fit (mandatory)

1. Compute/assemble q=1 weight vector on `S_3(lambda)` from available formula/enumerator.
2. Fit/test local move sets:
   - adjacent swaps only,
   - adjacent swaps + push moves.
3. Verify:
   - rate nonnegativity on selected `(x,t)` domains,
   - `L^T w = 0`,
   - irreducibility/nontriviality.
4. Artifacts:
   - `P03/experiments/exp25_n3_local_generator_fit.py`
   - `P03/experiments/exp25_n3_local_generator_fit_report.md`

### Route C — signed-MLQ lumping probe (bounded)

1. Define a minimal local-update chain on signed MLQ objects (if formula details sufficient).
2. Test bottom-row lumpability in smallest cases.
3. Artifacts:
   - `P03/experiments/exp26_smq_lumping_probe.py`
   - `P03/experiments/exp26_smq_lumping_probe_report.md`

---

## 3) Hard stop-loss gates

1. If Route A cannot produce an exact two-state stationarity identity:
   - stop cycle and mark dependency/interpretation mismatch.
2. If Route B fails positivity or closure in n=3 for all tested local move families:
   - stop and keep frontier unchanged.
3. If Route C cannot be implemented from explicit rules in bounded time:
   - mark dependency-blocked, do not speculate.
4. No unbounded route expansion in this cycle.

---

## 4) Evidence and contamination requirements

1. Tag every claim: `Proved / Cited / Empirical / Unresolved`.
2. For each external statement used:
   - source + UTC,
   - exact extracted statement,
   - contamination risk,
   - use/quarantine decision.
3. Do not import unresolved/forthcoming claims as established facts.

---

## 5) Required outputs after cycle

1. Lane verdict: `CLOSEABLE_NOW` or `BLOCKED_WITH_FRONTIER`.
2. Route table for A/B/C with pass/fail/dependency-blocked.
3. `P03/audit.md` escalation row.
4. `P03/transcript.md` entry with artifact paths.
5. `CONTAMINATION.md` updates for new citations.

---

## 6) Minimal command skeleton

```powershell
git status -sb

# Route A
python P03/experiments/exp24_n2_q1_anchor.py

# Route B
python P03/experiments/exp25_n3_local_generator_fit.py

# Route C (optional if implementable)
python P03/experiments/exp26_smq_lumping_probe.py

git status -sb
```

