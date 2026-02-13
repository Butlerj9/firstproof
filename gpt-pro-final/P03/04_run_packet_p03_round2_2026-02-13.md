# P03 GPT-pro Run Packet (Round 2)

Date: 2026-02-13  
Owner: Codex package prep  
Purpose: run-ready scout packet for a new GPT-pro P03 cycle while Claude Code continues lane execution.

---

## Inputs to provide GPT-pro

1. `gpt-pro-final/P03/00_gpt_pro_prompt_p03.md`
2. `gpt-pro-final/P03/01_problem_context.md`
3. `gpt-pro-final/P03/02_experiments_bundle.md`
4. `gpt-pro-final/P03/03_lane_packet_full.md`

---

## Mandatory run constraints

1. Single-lane: P03 only.
2. Must preserve the specialization-vs-limit disambiguation.
3. Must not repackage previously killed routes.
4. Must end with:
   - lane verdict table,
   - top-3 actionable approaches,
   - explicit Claude Code handoff tests.

---

## Expected output artifact naming

1. `gpt-pro-final/transcripts/P03_gpt_pro_response_2026-02-13_round2.md`
2. `gpt-pro-final/transcripts/P03_gpt_pro_full_exchange_2026-02-13_round2.md`
3. `gpt-pro-final/transcripts/P03_gpt_pro_breakdown_2026-02-13_round2.md`

---

## Acceptance gate

Accept the run only if all items are present:

1. Minimal blocking lemma is precise and falsifiable.
2. At least 12 approach families with novelty gate.
3. Top 3 include earliest fail-point + fallback bridge lemma.
4. Handoff block contains first 3 executable experiments + stop-loss criteria.

