# GPT-pro Prompt — P05 Only

You are GPT-pro focusing ONLY on P05 (ignore P03/P04 entirely).

Primary objective:
Close P05 if solvable now, or produce a rigorous frontier certificate for the exact blocker.

Shared assumptions for this lane-only run:
- Portfolio state: 7 Submitted, 3 Candidate.
- This run is SINGLE-LANE only; do not spend output on other lanes.
- Time is not a limiting factor; exhaust approach families before declaring blocked.
- No overclaiming; tag every claim as Proved/Cited/Empirical/Unresolved.
- No invented citations; use no_known_theorem if needed.
- Prior failed routes are hard constraints (no repackaged variants).
- If web retrieval is used, limit to foundational theorem statements/definitions and log sources.

P05 current blocker snapshot:
- 8 theorems proved + frontier theorem.
- New closure: Z/4 smallest Class II case CLOSED (Theorem 8) via geometric triviality + isotropy separation.
- Remaining gap: non-cyclic Class II "if" direction only.
- New smallest open case: Z/2 × Z/2 (intermediate transfer systems).
- Core unresolved component: global lifting/compatibility across multi-width subgroup lattices (multiple strata at same level).

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
