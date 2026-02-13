# Claude Code Checklist — P03 (Review Both Recent Scout Attempts)

Date: 2026-02-13  
Lane: P03 only  
Goal: review and reconcile the two latest P03 scout attempts, then select one execution path for the next bounded lane cycle.

---

## 0) Load these inputs first

1. `P03/answer.md`
2. `P03/audit.md`
3. `P03/transcript.md` (if present)
4. `tools/gpt-pro-final/transcripts/P03_gpt_pro_response_2026-02-13_round2.md`
5. `tools/gpt-pro-final/transcripts/P03_gpt_pro_full_exchange_2026-02-13_round2.md`
6. `tools/gpt-pro-final/transcripts/P03_gpt_pro_breakdown_2026-02-13_round2.md`
7. `tools/claude-research-final/transcripts/P03_claude_research_response_2026-02-13_round3.md`
8. `tools/claude-research-final/transcripts/P03_claude_research_full_exchange_2026-02-13_round3.md`
9. `tools/claude-research-final/transcripts/P03_claude_research_breakdown_2026-02-13_round3.md`
10. `tools/claude-research-final/P03/100_claude_code_checklist_from_gpt_pro_round2.md`

---

## 1) Hard review constraints

1. Preserve the lane disambiguation:
   - direct `q=1` specialization object vs
   - `q->1` limit-selected object used in lane proofs.
2. Reject any route that ignores limit-selection mechanics.
3. No theorem-level status change from scout text alone.
4. Tag all review outcomes as `Proved / Cited / Empirical / Unresolved`.

---

## 2) Reconciliation tasks (scout-vs-scout)

### A) Claim compatibility matrix
1. Build a matrix of major claims from each scout:
   - blocker statement,
   - minimal bridge lemma,
   - top 3 routes,
   - kill-tests,
   - stop-loss criteria.
2. Mark each row as:
   - compatible,
   - contradictory,
   - complementary.
3. Artifact:
   - `P03/experiments/exp27_scout_reconciliation_matrix.md`

### B) Route de-dup and ranking
1. Merge overlapping routes:
   - GPT-pro: divisibility/LRW/BDW
   - Claude research: BinAS/SMLQ/SSD (+ others)
2. Produce one ranked shortlist (max 3 routes) with:
   - bridge lemma,
   - concrete kill-test,
   - earliest fail-point.
3. Artifact:
   - `P03/experiments/exp28_scout_route_rank.md`

### C) Contradiction audit
1. Explicitly test for internal conflicts against existing lane artifacts:
   - EXP-5b null-space findings,
   - EXP-20 branching obstruction,
   - existing `n<=4` proof mechanisms.
2. Any incompatible scout claim is quarantined (not adopted).
3. Artifact:
   - `P03/experiments/exp29_scout_conflict_audit.md`

---

## 3) Immediate bounded execution picks (after reconciliation)

Choose exactly one route to run first:

1. **Route R1 (divisibility kill-test)**:
   - implement/execute `p03_exp_divisibility_n5.py` equivalent in lane style.
2. **Route R2 (BinAS support-collapse probe)**:
   - test LRW/Sahi expansion behavior at q=1 in small tractable scope.
3. **Route R3 (SMLQ q=1 factorization probe)**:
   - small-case queue computation with strict stop-loss.

Artifact:
- `P03/experiments/exp30_selected_route_plan.md`

---

## 4) Stop-loss gates

1. If reconciliation yields no route with a falsifiable kill-test under bounded runtime, stop and keep frontier unchanged.
2. If selected route fails its kill-test, do not continue symbolic sprawl; return to ranked fallback route.
3. No broad route expansion in this cycle.

---

## 5) Required outputs after review cycle

1. One-page "combined scout decision memo":
   - `P03/experiments/exp31_combined_scout_decision.md`
2. Updated `P03/audit.md` row for this scout-review cycle.
3. No `P03/answer.md` status change unless a new checkable proof artifact appears.

---

## 6) Minimal command skeleton

```powershell
git status -sb

# produce reconciliation docs
# (manual + script-backed extraction as needed)

git status -sb
```

