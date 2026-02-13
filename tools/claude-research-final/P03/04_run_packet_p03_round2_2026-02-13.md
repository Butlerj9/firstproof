# P03 Claude Research Run Packet (Round 2)

Date: 2026-02-13  
Owner: Codex package prep  
Purpose: run-ready Claude Research packet for P03 while Claude Code continues lane execution.

---

## Inputs to provide Claude Research

1. `tools/claude-research-final/P03/00_claude_research_prompt_p03.md`
2. `tools/claude-research-final/P03/01_problem_context.md`
3. `tools/claude-research-final/P03/02_experiments_bundle.md`
4. `tools/claude-research-final/P03/03_lane_packet_full.md`

---

## Mandatory run constraints

1. Single-lane: P03 only.
2. Must preserve the specialization-vs-limit disambiguation.
3. Must prioritize non-contaminating routes first.
4. Any external escalation must include contamination metadata and integration decision.
5. Must end with:
   - lane verdict table,
   - top-3 actionable approaches,
   - explicit Claude Code handoff tests + stop-loss.

---

## Expected output artifact naming

1. `tools/claude-research-final/transcripts/P03_claude_research_response_2026-02-13_round2.md`
2. `tools/claude-research-final/transcripts/P03_claude_research_full_exchange_2026-02-13_round2.md`
3. `tools/claude-research-final/transcripts/P03_claude_research_breakdown_2026-02-13_round2.md`

---

## Acceptance gate

Accept the run only if all items are present:

1. Precise unresolved statement + minimal blocker lemma.
2. >=12 candidate families with novelty filtering.
3. Top-3 include bridge lemma + kill-test + proof skeleton.
4. Escalation/contamination block is complete.
5. Handoff block contains first 3 executable tests + stop-loss criteria.

