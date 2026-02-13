# P04 GPT-pro Run Packet (Round 2)

Date: 2026-02-13  
Owner: Codex package prep  
Purpose: run-ready GPT-pro packet for one more P04 lane pass.

---

## Inputs to provide GPT-pro

1. `gpt-pro-final/P04/00_gpt_pro_prompt_p04.md`
2. `gpt-pro-final/P04/01_problem_context.md`
3. `gpt-pro-final/P04/02_experiments_bundle.md`
4. `gpt-pro-final/P04/03_lane_packet_full.md`

---

## Mandatory run constraints

1. Single lane only (`P04`).
2. Do not rework solved scopes (`n<=3`, `n=4,b=0`, `n=4,c'=0`).
3. Keep CE-19 corrected domain assumptions.
4. Must produce executable handoff tests (not generic planning).

---

## Expected output artifact naming

1. `gpt-pro-final/transcripts/P04_gpt_pro_response_2026-02-13_round2.md`
2. `gpt-pro-final/transcripts/P04_gpt_pro_full_exchange_2026-02-13_round2.md`
3. `gpt-pro-final/transcripts/P04_gpt_pro_breakdown_2026-02-13_round2.md`

---

## Acceptance gate

Accept run output only if all are present:

1. Minimal blocking lemma is explicit and falsifiable.
2. >=12 approach families with novelty gate.
3. Top 3 include earliest fail-point and fallback bridge lemma.
4. Claude Code handoff includes first 3 scripts + stop-loss + upgrade criteria.

