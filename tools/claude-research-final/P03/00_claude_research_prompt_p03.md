# Claude Research Prompt — P03 Only

You are Claude in RESEARCH MODE focusing ONLY on P03.

Objective:
Close P03 if possible; otherwise produce a frontier certificate with fully documented escalation.

Research-mode escalation policy:
1) Exhaust non-contaminating routes first (local derivation, existing artifacts, experiments, controlled scouts).
2) If still blocked, you MAY use potentially contaminating references as a last resort.
3) Any potentially contaminating source MUST be documented in your response and artifacts with:
   - URL / identifier
   - access date/time (UTC)
   - why escalation was necessary
   - exact claim extracted (statement-level)
   - contamination risk rating (LOW/MED/HIGH)
   - whether incorporated, quarantined, or rejected
4) Prefer statement extraction over solution text. Never paste or mirror full external proofs.
5) If direct-solution exposure occurs, quarantine that thread and continue with a clean derivation path.

Known blocker:
- n<=4 proved.
- n>=5 unresolved.
- direct compute infeasible.
- branching induction killed (EXP-20).
- AS lead closes leading term only.
- **Critical disambiguation**: do NOT conflate direct specialization `E*_{lambda^-}(x; q=1, t)` with the lane object `f*` defined via the `q -> 1` limit used in existing P03 proofs.
- Current unresolved target for closure: prove or refute symmetry of the lower-degree interpolation corrections selected by the `q -> 1` limit mechanism for n>=5.

Protocol:
1) Failure map (exact unresolved statement + minimal blocker lemma).
2) >=12 new approach families (>=4 cross-domain).
3) Novelty gate (no variants of failed routes).
4) Top 3 with bridge lemma + kill-test + proof skeleton.
5) Verdict: CLOSEABLE_NOW or BLOCKED_WITH_FRONTIER.
6) 48-hour lane plan.

Output:
A) Lane Verdict Table
B) Actionable Plan
C) Escalation & Contamination Log
D) Claude Code Handoff: first 3 executable tests/scripts + explicit stop-loss gates
