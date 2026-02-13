# First Proof — Agentic LLM Orchestration for Research-Grade Mathematics

**Sprint**: Feb 10-13, 2026 | **Answers release**: Feb 13 11:59 PM PT
**Agents**: Claude Opus 4.6 (Implementer) + Codex 5.3 (Reviewer) + multi-model scouts
**Human role**: Logistics only (no mathematical ideas or content)
**Paper**: [arXiv:2602.05192](https://arxiv.org/abs/2602.05192) | [1stproof.org](https://1stproof.org)

## Autonomy statement

This run follows the [1stproof.org](https://1stproof.org) autonomy standard:
no human mathematical ideas/content and no human isolation of the mathematical
core. All mathematical artifacts were agent-authored.

Producer activity was runtime-operator only: prompt dispatch/handoffs, rule-bound
administrative decisions under pre-decided gates/escalation policy, and verbatim
execution of agent-authored procedures. No expert-level mathematical judgment
was used for domain interpretation, solution procedures, or solution content.
The operator remained abstracted from problem/solution steps and evaluated only
structural response quality (gate compliance, artifact completeness, status
classification consistency), while mathematical correctness was delegated to
agent review and executable checks.
Full protocol and constraints are in `methods_extended.md`. Enforcement and
provenance are logged in `PXX/audit.md`, `PXX/transcript.md`, and
`CONTAMINATION.md`.

## Escalation note (active policy)

Final escalation does **not** stop after a single GPT-pro run.
For the remaining candidate lanes (`P03`, `P04`), escalation is
iterative and multi-model (`GPT-pro` + `Claude Research` + `Claude Code`):
continue while a cycle yields measurable progress (new bridge lemma, closed
subcase, sharper blocker with reproducible evidence). Stop only when bounded
cycles stop producing new pathway signal.

## Results

| Problem | Domain | Status | Confidence | Budget used |
|---------|--------|--------|------------|-------------|
| P01 | Stochastic analysis | ✅ Submitted | HIGH (YES, quasi-invariance proved; **R1 CITE_PLUS: BG proof chain verified + Hairer-Steele independent path; all gaps closed**) | ~20/80 msgs |
| P02 | Representation theory | ✅ Submitted | HIGH (YES, Kirillov + Gauss sums + JPSS + multiplicity-one) | ~12/80 msgs |
| P03 | Algebraic combinatorics | 🟡 Candidate | HIGH (YES, Mallows/ASEP; **n=2,3,4 proved**; n≥5 infeasible — branching fails (EXP-20: 4 obstructions), AS reduction partial; L5 barrier; **R1-DIV: q→1 convergence confirmed, E*_μ≠E_μ identified, informative not closure**) | ~83/200 msgs |
| P04 | Finite free convolution | ✅ Submitted | HIGH (YES; n=2,3 proved; **n=4 b=0 PROVED (CE-16)**; **n=4 c'=0 PROVED (CE-26)**; **n=4 general: SOS-CERTIFIED (CE-44, 20/20 w-slices, Putinar/CLARABEL)**; 495K+ exact tests ALL PASS; n≥5 conjectured) | ~142/300 msgs |
| P05 | Equivariant homotopy | ✅ Submitted | HIGH (**11 theorems; FULL BICONDITIONAL PROVED**; Thms 1-10: obstruction, positive scope, corrected "only if", dim-uniform, Class Ia, Z/4, V4, **general "if" for ALL G and ALL O (Thm 10, iterated isotropy separation)**; 825 systems verified) | ~57/80 msgs |
| P06 | Spectral graph theory | ✅ Submitted | HIGH (NO, K_n counterexample) | ~14/300 msgs |
| P07 | Lattices in Lie groups | ✅ Submitted | HIGH (YES, Q-PD + surgery realization proved) | ~6/80 msgs |
| P08 | Symplectic geometry | ✅ Submitted | HIGH (NO, Lagrangian octahedron + Gromov) | ~10/80 msgs |
| P09 | Tensor polynomial map | ✅ Submitted | HIGH (YES, D≤6; **all gaps closed ALL n≥5**: n≥6 via subset isomorphism; **n=5 kernel=15 proved exactly** via modular rank at 2 primes) | ~58/200 msgs |
| P10 | RKHS CP-ALS | ✅ Submitted | HIGH | ~12/120 msgs |

Status key: -- Not started | ✅ Submitted | 🟡 Candidate | 📊 Conjecture | ❌ Parked

## Active Open Lanes

- `P03/answer.md` + `P03/audit.md` (candidate, frontier active)
- `P04/answer.md` + `P04/audit.md` (candidate, frontier active)
- `P05/answer.md` + `P05/audit.md` (resolved reference lane, ✅ submitted)

## How to read this repo

- `docs/README.md` — documentation index (methods/results/reference layout)
- `PXX/answer.md` — the actual answer (start here)
- `PXX/audit.md` — what worked, what failed, routes tried, human intervention log
- `PXX/experiments/` — verification scripts and outputs
- `PXX/transcript.md` — interaction log (full where available; some parked lanes contain summary stubs)
- `CONTAMINATION.md` — search log and exposure declarations
- `RESULTS.md` — consolidated progress, escalations, final outcomes, and token/message accounting
- `methods_extended.md` — experimental setup, autonomy boundary, and enforcement protocol

## Extended Model Tooling

Shared scout tooling is in `tools/`:

- `tools/scout_api.py` — unified OpenAI-compatible caller for `groq`, `moonshot`, `fireworks`, and custom providers.
- `tools/model_capability_probe.py` — repeatable cross-model benchmark harness for quick model triage before using a scout in a proof loop.
- `tools/README.md` — commands, provider setup, and probe usage.

Recommended use:

- Use scouts sparingly when blocked on a narrow microdomain or a core-lemma sanity check.
- Prefer local derivation and in-repo experiments first.
- Avoid web-searching foundational lemmas for llm-only runs; keep contamination policy in `CONTAMINATION.md`.

## Citation and Attribution

- License: `CC-BY-4.0` (see `LICENSE`).
- Preferred citation metadata: `CITATION.cff` (and `CITATION.bib`).
- Attribution notice: `NOTICE`.
- Detailed policy (legal baseline + strong scholarly credit requests):
  `docs/reference/attribution_and_citation_policy.md`.

## License

CC-BY-4.0

#1stProof
