# P04 Claude Research Run Packet (Round 2)

Date: 2026-02-13  
Owner: Codex package prep  
Purpose: run-ready Claude Research packet for one more P04 lane pass.

---

## Inputs to provide Claude Research

1. `tools/claude-research-final/P04/00_claude_research_prompt_p04.md`
2. `tools/claude-research-final/P04/01_problem_context.md`
3. `tools/claude-research-final/P04/02_experiments_bundle.md`
4. `tools/claude-research-final/P04/03_lane_packet_full.md`

---

## Mandatory run constraints

1. Single lane only (`P04`).
2. Preserve CE-19 corrected domain.
3. Do not re-solve already closed subcases except as dependencies.
4. Prioritize non-contaminating routes first; contamination block required if escalated.
5. Must output an executable Claude Code handoff block.

---

## Expected output artifact naming

1. `tools/claude-research-final/transcripts/P04_claude_research_response_2026-02-13_round2.md`
2. `tools/claude-research-final/transcripts/P04_claude_research_full_exchange_2026-02-13_round2.md`
3. `tools/claude-research-final/transcripts/P04_claude_research_breakdown_2026-02-13_round2.md`

---

## Acceptance gate

Accept run output only if all are present:

1. Exact unresolved statement + minimal blocker lemma.
2. >=12 approach families with novelty filter.
3. Top 3 include bridge lemma + kill-test + proof skeleton.
4. Complete escalation/contamination log.
5. Claude Code handoff includes first 3 scripts + stop-loss + upgrade criteria.

