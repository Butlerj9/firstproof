# Contamination Log

## Policy
- No browsing of claimed solutions to numbered First Proof questions
- No searching "[author name] + [problem keywords]"
- All web searches logged below
- If accidental exposure occurs: freeze problem, log here, do NOT incorporate
- External scout model API calls are allowed for independent reasoning checks, but do not include retrieval of known solutions.
- For llm-only tracks, avoid web-searching foundational lemmas unless the run is explicitly marked as a relaxed-constraints pass.

## Definition-level citations used (no proof text)

| row_id | Problem | Citation | What was used | Classification | Escalation event (audit.md) |
|--------|---------|----------|---------------|----------------|-----------------------------|
| C1 | P02 | AGRS (2010), *Ann. Math.* 172, 1407–1434 | Statement-level: multiplicity-one for (GL_{n+1}, GL_n) | CITE_ONLY | P02 E4 |
| C2 | P04 | MSS (2015), arXiv:1507.05506 | Statement-level: real-rootedness preservation under ⊞_n | CITE_ONLY | P04 E1 (G0 background) |
| C3 | P08 | Gromov (1985), §2.3.B₂' | Statement-level: Lagrangian non-squeezing | CITE_ONLY | P08 E2 |
| C4 | P07 | Shapiro's lemma; Borel–Serre | Statement-level: standard algebraic topology | CITE_ONLY | P07 E2 |
| C5 | P05 | Blumberg-Hill (2015), arXiv:1309.1750, Def 3.7 | Statement-level: N∞ operad definition | CITE_ONLY | P05 E3 |
| C6 | P05 | Blumberg-Hill (2015), arXiv:1309.1750, Def 3.22 | Statement-level: indexing system definition | CITE_ONLY | P05 E3 |
| C7 | P05 | Blumberg-Hill (2015), arXiv:1309.1750, Def 4.3 | Statement-level: admissible H-set definition | CITE_ONLY | P05 E3 |
| C8 | P05 | Blumberg-Hill (2015), arXiv:1309.1750, Thm 3.24 | Statement-level: N∞ → indexing system classification | CITE_ONLY | P05 E3 |
| C9 | P05 | Rubin (2019), arXiv:1903.08723, Def 2.1/3.4 | Statement-level: indexing system + transfer system definitions | CITE_ONLY | P05 E3 |
| C10 | P05 | Rubin (2019), arXiv:1903.08723, Thm 3.7 + Cor 3.9 | Statement-level: Ind ↔ Tr equivalence | CITE_ONLY | P05 E3 |
| C11 | P05 | Hill-Yarnall (2017), arXiv:1703.10526, Def 1.1/2.6, Thm 2.5 | Statement-level: slice connectivity + geometric FP characterization | CITE_ONLY | P05 E3 |

## Scout model deployments (no web search, no solution retrieval)

| row_id | Problem | Provider/Model | Purpose | Exposure risk | Escalation event |
|--------|---------|---------------|---------|--------------|-----------------|
| S1 | P10 | GPT-5.2-pro | Initial candidate solution (solvability evaluation) | NONE (LLM reasoning only) | P10 E1 |
| S2 | P03 | groq/gptoss120b, fw/kimi-instruct, fw/deepseek-v3p2 | Symmetry Conjecture closure routes | NONE (3 scouts, no consensus) | P03 E6 |

## Search log
| Timestamp | Query | Purpose | Exposure risk |
|-----------|-------|---------|--------------|
| 2026-02-11 | WebFetch ar5iv.labs.arxiv.org/html/1309.1750 | P05 definition extraction (BH N∞ operad) | NONE (definition-only, primary source) |
| 2026-02-11 | WebFetch ar5iv.labs.arxiv.org/html/1903.08723 | P05 definition extraction (Rubin transfer systems) | NONE (definition-only, primary source) |
| 2026-02-11 | WebFetch ar5iv.labs.arxiv.org/html/1703.10526 | P05 definition extraction (HY slice connectivity) | NONE (definition-only, primary source) |

## Exposure events
None.

## Statement
We did not incorporate any externally found solutions into our proofs.
