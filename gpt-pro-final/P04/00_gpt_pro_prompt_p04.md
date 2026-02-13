# GPT-pro Prompt — P04 Only

You are GPT-pro focusing ONLY on P04 (ignore P03/P05 entirely).

Primary objective:
Close P04 if solvable now, or produce a rigorous frontier certificate for the exact blocker.

Shared assumptions for this lane-only run:
- Portfolio state: 7 Submitted, 3 Candidate.
- This run is SINGLE-LANE only; do not spend output on other lanes.
- Time is not a limiting factor; exhaust approach families before declaring blocked.
- No overclaiming; tag every claim as Proved/Cited/Empirical/Unresolved.
- No invented citations; use no_known_theorem if needed.
- Prior failed routes are hard constraints (no repackaged variants).
- If web retrieval is used, limit to foundational theorem statements/definitions and log sources.
- Do not regress to pre-CE-19 invalid-domain formulations.
- Do not spend output on already-proved subcases (`n<=3`, `n=4,b=0`, `n=4,c'=0`) except as dependencies.

P04 current blocker snapshot:
- n=2,3 proved.
- n=4 b=0 proved (CE-16).
- n=4 c'=0 proved (CE-26).
- General n=4 (b!=0, c'!=0) unresolved.
- CE-19 corrected valid-domain exact sweeps all pass (no counterexample in corrected region).
- CE-28/29: parametric c'-convexity + discriminant-bound chain found empirically (all tests pass), but symbolic closure missing.
- CE-30: M''(0) structure and phi-subadditivity reduction found; full symbolic proof blocked by high-complexity cleared polynomial (1612 terms, degree 34) and constrained SOS gap.
- Current lane verdict: BLOCKED_WITH_FRONTIER (proof-chain identified, theorem-level closure still missing).
- Working proof chain candidate to resolve:
  `M(0) >= 0` (proved) + `M'' >= kappa > 0` (missing symbolic/certified proof) + `2*kappa*M(0) >= M'(0)^2` (missing symbolic/certified proof).

Execution protocol:
1) Failure map: exact unresolved statement + minimal blocking lemma.
2) Generate >=12 candidate approach families (>=4 cross-domain analogical transfers).
3) Novelty/viability gate: keep only non-variants of failed routes.
4) Keep top 3; provide proof skeleton + earliest fail-point + fallback bridge lemma.
5) Verdict: CLOSEABLE_NOW or BLOCKED_WITH_FRONTIER.
6) 48-hour ranked plan with stop-loss criteria.

Required output format:
SECTION A: Lane Verdict Table
Lane | StatusBefore | BestNewBridgeLemma | KillTest | Verdict | Why

SECTION B: Actionable Plan
1) Top 3 novel approaches
2) Fastest theorem-level closure path
3) One-sentence frontier statement if blocked
4) Required external theorem statements or no_known_theorem
5) "Claude Code handoff" block:
   - first 3 executable tests/scripts,
   - explicit stop-loss gates,
   - acceptance criteria for status upgrade
