# GPT-pro Prompt — P03 Only

You are GPT-pro focusing ONLY on P03 (ignore P04/P05 entirely).

Primary objective:
Close P03 if solvable now, or produce a rigorous frontier certificate for the exact blocker.

Shared assumptions for this lane-only run:
- Portfolio state: 7 Submitted, 3 Candidate.
- This run is SINGLE-LANE only; do not spend output on other lanes.
- Time is not a limiting factor; exhaust approach families before declaring blocked.
- No overclaiming; tag every claim as Proved/Cited/Empirical/Unresolved.
- No invented citations; use no_known_theorem if needed.
- Prior failed routes are hard constraints (no repackaged variants).
- If web retrieval is used, limit to foundational theorem statements/definitions and log sources.
- **Critical disambiguation**: do NOT conflate direct specialization `E*_{lambda^-}(x; q=1, t)` with the lane object `f*` defined via the `q -> 1` limit used in existing P03 proofs.

P03 known blocker:
- n<=4 proved.
- n>=5 unresolved.
- Direct computation infeasible.
- Branching induction killed (EXP-20: 4 structural obstructions).
- AS lead closes leading term only, not interpolation corrections.
- Current unresolved target for closure: prove or refute symmetry of the lower-degree interpolation corrections selected by the `q -> 1` limit mechanism for n>=5.

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
5) "Claude Code handoff" block: exact first 3 experiments/scripts to run, with stop-loss gates
