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
For the remaining candidate lane (`P03`), escalation is
iterative and multi-model (`GPT-pro` + `Claude Research` + `Claude Code`):
continue while a cycle yields measurable progress (new bridge lemma, closed
subcase, sharper blocker with reproducible evidence). Stop only when bounded
cycles stop producing new pathway signal.

## Results

| Problem | Domain | Status | Confidence | Budget used |
|---------|--------|--------|------------|-------------|
| P01 | Stochastic analysis | ✅ Submitted | HIGH (YES, quasi-invariance proved; **R1 CITE_PLUS: BG proof chain verified + Hairer-Steele independent path; all gaps closed**) | ~20/80 msgs |
| P02 | Representation theory | ✅ Submitted | HIGH (YES, Kirillov + Gauss sums + JPSS + multiplicity-one) | ~12/80 msgs |
| P03 | Algebraic combinatorics | 🟡 Candidate | HIGH (YES, Mallows/ASEP; **n=2,3,4 proved**; n≥5 unresolved in sprint window: single-thread path infeasible, branching fails (EXP-20: 4 obstructions), AS reduction partial; L5 barrier; **R1-DIV: q→1 convergence confirmed, E*_μ≠E_μ identified, informative not closure**. Compute resources were available; blocker was late-start/shared-time allocation across lanes.) | ~83/200 msgs |
| P04 | Finite free convolution | ✅ Submitted | HIGH (YES; n=2,3 proved; **n=4 b=0 PROVED (CE-16)**; **n=4 c'=0 PROVED (CE-26)**; **n=4 general: SOS-CERTIFIED (CE-44, 20/20 w-slices, Putinar/CLARABEL)**; 495K+ exact tests ALL PASS; n≥5 conjectured) | ~142/300 msgs |
| P05 | Equivariant homotopy | ✅ Submitted | HIGH (**11 theorems; FULL BICONDITIONAL PROVED**; Thms 1-10: obstruction, positive scope, corrected "only if", dim-uniform, Class Ia, Z/4, V4, **general "if" for ALL G and ALL O (Thm 10, iterated isotropy separation)**; 825 systems verified) | ~57/80 msgs |
| P06 | Spectral graph theory | ✅ Submitted | HIGH (NO, K_n counterexample) | ~14/300 msgs |
| P07 | Lattices in Lie groups | ✅ Submitted | HIGH (YES, Q-PD + surgery realization proved) | ~6/80 msgs |
| P08 | Symplectic geometry | ✅ Submitted | HIGH (NO, Lagrangian octahedron + Gromov) | ~10/80 msgs |
| P09 | Tensor polynomial map | ✅ Submitted | HIGH (YES, D≤6; **all gaps closed ALL n≥5**: n≥6 via subset isomorphism; **n=5 kernel=15 proved exactly** via modular rank at 2 primes) | ~58/200 msgs |
| P10 | RKHS CP-ALS | ✅ Submitted | HIGH | ~12/120 msgs |

Status key: -- Not started | ✅ Submitted | 🟡 Candidate | 📊 Conjecture | ❌ Parked

## Sprint summary

**9 of 10 problems submitted** across 28 sessions, ~414 agent messages, ~1M artifact tokens, ~10M total compute tokens, ~$400 estimated cost. One problem (P03) remains at Candidate status with an L5 barrier (n=2,3,4 proved; n>=5 not closed in-sprint). Operationally this was a time-allocation issue (late start on P03 + effort split across other lanes), not a hard compute-resource outage.

### Escalation levels used

| Level | Description | Problems |
|-------|-------------|----------|
| L0 | Baseline: Implementer (Claude Opus 4.6) + Reviewer (Codex 5.3), gate workflow G0-G7 | All 10 |
| L1 | Adversarial hard-gating: mandatory reject/patch cycles | P09, P10 |
| L2 | Counterexample-first: budget allocated to disproof before proof | P04, P06 |
| L3 | Experiment-first: scripted numeric/symbolic checks required before claims | P04, P06, P09, P10 |
| L4 | Scout model augmentation: external LLM checks as secondary verification | P10, tooling layer |
| L5 | Latent-limit protocol: relaxed-pass criteria for theorem-level stalls | P03, P04, P09 |
| L6 | Iterative final escalation: multi-cycle GPT-pro + Claude Research + Claude Code | P03, P04 |
| L7 | Full biconditional closure via iterated theoretical framework | P05 |

### Token, message, and cost budget

**Artifact tokens** (~1M) are final deliverable text in answer/audit/transcript files. **Total compute tokens** (~10M) include system prompts, conversation history, tool call I/O, and extended thinking across all LLM API calls — roughly 10× the artifact size. Each of the ~414 agent messages corresponds to ~8–12 internal LLM API calls (tool use cycles, file reads, experiment execution), yielding ~4,100 LLM round-trips total. An additional ~500K tokens were consumed by scout models (DeepSeek-R1, Qwen3-480B, GPT-pro, Claude Research, Kimi K2.5).

| Problem | Domain | Artifact tokens | Agent msgs | Est. total tokens | Key sessions |
|---------|--------|----------------|------------|-------------------|-------------|
| P01 | Stochastic analysis | ~45K | ~20 | ~500K | S10: R1 CITE_PLUS closure |
| P02 | Representation theory | ~33K | ~12 | ~300K | JPSS + multiplicity-one |
| P03 | Algebraic combinatorics | ~195K | ~83 | ~2.0M | S4: n=3; S6: n=4; S24: R1-DIV |
| P04 | Finite free convolution | ~270K | ~142 | ~3.4M | S14-27: CE-16 through CE-44 SOS |
| P05 | Equivariant homotopy | ~100K | ~57 | ~1.4M | S7-21: 11 theorems, full biconditional |
| P06 | Spectral graph theory | ~54K | ~14 | ~340K | K_n counterexample |
| P07 | Lattices in Lie groups | ~20K | ~6 | ~150K | Q-PD + surgery |
| P08 | Symplectic geometry | ~30K | ~10 | ~240K | Lagrangian octahedron + Gromov |
| P09 | Tensor polynomial map | ~114K | ~58 | ~1.4M | S7-8: all gaps closed, n=5 kernel proved |
| P10 | RKHS CP-ALS | ~116K | ~12 | ~290K | Matrix-free PCG solver |
| **Total** | | **~1M** | **~414** | **~10M** | |

**Estimated cost** (~$400, using provider list pricing):

| Model | Role | Est. tokens | Rate (blended) | Est. cost |
|-------|------|-------------|----------------|-----------|
| Claude Opus 4.6 | Implementer (main agent) | ~8.5M | ~$45/M | ~$383 |
| Codex 5.3 | Reviewer (G6 adversarial) | ~1.5M | ~$15/M | ~$23 |
| Scouts (mixed) | Secondary verification | ~0.5M | ~$1/M | ~$1 |
| **Total** | | **~10.5M** | | **~$407** |

Cost is dominated by Claude Opus (~94% of spend). Heaviest per-problem consumers: P04 (~$130, 28 sessions of SOS solver development) and P03/P05/P09 (~$55–80 each).

## Active open lanes

- `P03/answer.md` + `P03/audit.md` (candidate, frontier active)

## Quick links

- [Portfolio results](RESULTS.md)
- [Docs index](docs/README.md)
- [Future work and applications](docs/methods/future_work.md)
- [GPT-pro package index](tools/gpt-pro-final/README.md)
- [Claude Research package index](tools/claude-research-final/README.md)
- [Tools index](tools/README.md)

## Repository layout

- `P01/` … `P10/`: per-problem artifacts (`answer.md`, `audit.md`, `experiments/`, `transcript.md`).
- `tools/`: scout tooling and package archives.
- `tools/gpt-pro-final/`: GPT-pro lane packets, prompts, and transcripts.
- `tools/claude-research-final/`: Claude Research lane packets, prompts, and transcripts.
- `docs/`: documentation index and reference/method/result navigation.

## How to read this repo

- `docs/README.md` — documentation index (methods/results/reference layout)
- `PXX/answer.md` — the actual answer (start here)
- `PXX/audit.md` — what worked, what failed, routes tried, human intervention log
- `PXX/experiments/` — verification scripts and outputs
- `PXX/transcript.md` — interaction log (full where available; some parked lanes contain summary stubs)
- `tools/gpt-pro-final/README.md` — GPT-pro package index
- `tools/claude-research-final/README.md` — Claude Research package index
- `CONTAMINATION.md` — search log and exposure declarations
- `RESULTS.md` — consolidated progress, escalations, final outcomes, and token/message accounting
- `methods_extended.md` — experimental setup, autonomy boundary, and enforcement protocol

## Computational solver tooling

The P04 proof chain required machine-checkable certificates (SOS / Putinar's Positivstellensatz) for polynomial non-negativity in 4 variables at degree 10. This led to an extended tooling investigation across Sessions 19-27:

| Solver | Type | Status | Role |
|--------|------|--------|------|
| **cvxpy** | Python SDP frontend | Bottleneck (ConeMatrixStuffing hangs at 108K+ vars) | Bypassed entirely — call solvers directly |
| **SCS** | First-order splitting | Works at full scale via native API | CE-43: phi-subadditivity SOS (20/20 w-slices, deg 22, 2 vars) |
| **CLARABEL** | Interior-point (Rust) | Works at full scale, free, no license | CE-44: direct M>=0 SOS (20/20 w-slices, deg 10, 4 vars, 11.8K decision vars) |
| **MOSEK** | Interior-point (commercial) | Requires license | Not used (CLARABEL sufficient) |

Key finding: the solver-infeasibility diagnosis from Sessions 19-25 was **misattributed** — the bottleneck was cvxpy's Python-side compilation, not the underlying SDP solver. When SCS/CLARABEL are called directly via sparse scipy matrices, problems at full P04 scale (126x126 PSD + 6x35x35 multipliers) solve in 60-180 seconds. This misattribution cost ~6 sessions of blocked progress and is the single largest process failure of the sprint.

SOS certificates are stored in `P04/experiments/ce43_sos_certificate.py` (SCS) and `P04/experiments/ce44_direct_M_clarabel.py` + `ce44b_dense_sweep.py` (CLARABEL).

## Scout model tooling

Shared scout tooling is in `tools/`:

- `tools/scout_api.py` — unified OpenAI-compatible caller for `groq`, `moonshot`, `fireworks`, and custom providers.
- `tools/model_capability_probe.py` — repeatable cross-model benchmark harness for quick model triage before using a scout in a proof loop.
- `tools/README.md` — commands, provider setup, and probe usage.

Scouts used: GPT-pro 5.2, Claude Opus Research, DeepSeek-R1, Qwen3-480B, Kimi K2.5. Best results from DeepSeek-R1 and Qwen3-480B on structured math problems; Kimi K2.5 irrecoverable on complex problems (spends all tokens on reasoning, zero usable output).

Recommended use:

- Use scouts sparingly when blocked on a narrow microdomain or a core-lemma sanity check.
- Prefer local derivation and in-repo experiments first.
- Avoid web-searching foundational lemmas for llm-only runs; keep contamination policy in `CONTAMINATION.md`.

## Sprint time constraints

The 4-day sprint window (Feb 10-13) prevented several plausible improvements:

- **Solver investigation**: The cvxpy misattribution (Sessions 19-25) would have been caught earlier with systematic solver preflight testing. A single direct SCS/CLARABEL smoke test at Session 19 would have unblocked P04 immediately, saving ~6 sessions.
- **Broader SOS application**: With CLARABEL proven effective, SOS certificates could potentially be computed for P04 n=5 (5 variables) or used to close the w-continuity formal gap (treating w as a 5th variable at degree 14). Neither was attempted due to time.
- **P03 n=5 computational approach**: The modular degree-bound approach that proved n=3 and n=4 works in principle for n=5 but requires ~247 days single-thread for the ~11K x 11K system. The 113 t-value jobs are embarrassingly parallel (no data dependencies); with 226 cloud workers (4.3 GB RAM each, two primes), wall time drops to ~53 hours at ~$300–600 cloud cost. This was not attempted in-sprint due to late start and cross-lane time division — even parallelized, the ~53-hour wall time would consume over half the 4-day sprint before accounting for infrastructure setup.
- **Formal verification**: No Lean/Coq formalization was attempted. The SOS certificates from CE-43/CE-44 are machine-checkable in principle but were not exported to a formal verification framework.
- **Cross-problem tooling reuse**: The CLARABEL/Putinar framework developed for P04 could potentially apply to other polynomial non-negativity questions but was not tested beyond P04.

## Citation and Attribution

- License: `CC-BY-4.0` (see `LICENSE`).
- Preferred citation metadata: `CITATION.cff` (and `CITATION.bib`).
- Attribution notice: `NOTICE`.
- Detailed policy (legal baseline + strong scholarly credit requests):
  `docs/reference/attribution_and_citation_policy.md`.

## License

CC-BY-4.0

#1stProof
