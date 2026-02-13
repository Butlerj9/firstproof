# Claude Research Prompt — P04 Only

You are Claude in RESEARCH MODE focusing ONLY on P04.

Objective:
Close P04 if possible; otherwise produce a frontier certificate with fully documented escalation.

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

Current blocker snapshot:
- n=2,3 proved.
- n=4 b=0 proved (CE-16).
- n=4 c'=0 proved (CE-26).
- General n=4 (b!=0, c'!=0) unresolved.
- CE-19 corrected valid-domain exact sweeps all pass (no counterexample in corrected region).
- CE-28/29: parametric c'-convexity + discriminant-bound chain found empirically (all tests pass), but symbolic closure missing.
- CE-30: M''(0) structure and phi-subadditivity reduction found; full symbolic proof blocked by high-complexity cleared polynomial (1612 terms, degree 34) and constrained SOS gap.
- Current lane verdict: BLOCKED_WITH_FRONTIER (proof-chain identified, theorem-level closure still missing).
- Do not regress to pre-CE-19 domain assumptions.
- Do not re-solve already-closed subcases (`n<=3`, `n=4,b=0`, `n=4,c'=0`) except as dependencies.
- Focus on the remaining chain:
  `M(0) >= 0` (proved), `M'' >= kappa > 0` (open), `2*kappa*M(0) >= M'(0)^2` (open).

Protocol:
1) Failure map.
2) >=12 new approach families (>=4 cross-domain).
3) Novelty gate.
4) Top 3 with bridge lemma + kill-test + proof skeleton.
5) Verdict: CLOSEABLE_NOW or BLOCKED_WITH_FRONTIER.
6) 48-hour lane plan.

Output:
A) Lane Verdict Table
B) Actionable Plan
C) Escalation & Contamination Log
D) Claude Code Handoff:
   - first 3 executable tests/scripts,
   - explicit stop-loss gates,
   - acceptance criteria for status upgrade
