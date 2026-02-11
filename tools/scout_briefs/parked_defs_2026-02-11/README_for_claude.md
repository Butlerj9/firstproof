# Claude Handoff: Parked Problem Scout Briefs

Purpose:
- Candidate definitions + citation leads for parked problems (P02, P05, P07, P08).
- Generated from multi-model scout calls. Unverified.

Use order:
1. Read `claude_handoff_summary.md` for quick triage.
2. Read `scout_responses_extracted.json` for machine-readable full extracts.
3. If needed, inspect per-call raw payloads (`*.raw.json.txt`).

Do not assume correctness:
- Many references/statement labels are model guesses.
- Verify every citation in primary sources before using in proofs.
- Treat these as dependency leads, not proof inputs.

Suggested workflow:
- Build a `definition-only` dependency list from repeated items.
- Request exact statements from primary sources (definition/theorem numbers).
- Re-run G1 with `CITE(statement #)` vs `NEEDS_SOURCE` tags.
