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

## Final Results (External Adjudication View)

| Problem | Domain | External expected | Repo claim | Final status |
|---|---|---|---|---|
| P01 | Stochastic analysis | NO | YES | Conflict |
| P02 | Representation theory | YES | YES | Aligned |
| P03 | Algebraic combinatorics | YES (full theorem) | Partial (`n<=4`) | Partial mismatch |
| P04 | Finite free convolution | YES (general `n`) | Partial (`n<=4`) | Partial mismatch |
| P05 | Equivariant homotopy | YES (characterization) | YES | Directionally aligned (documentation inconsistency) |
| P06 | Spectral graph theory | YES vs NO (quantifier-form ambiguity) | NO | **Disputed quantifier form** |
| P07 | Lattices in Lie groups | NO | YES | Conflict |
| P08 | Symplectic geometry | YES | NO | Conflict |
| P09 | Tensor polynomial map | YES | YES | Aligned |
| P10 | RKHS CP-ALS | YES | YES | Aligned |

## Internal Run Outcomes (Pre-Adjudication)

| Problem | Status | Internal sprint outcome |
|---|---|---|
| P01 | ✅ Submitted | YES (quasi-invariance route accepted during sprint) |
| P02 | ✅ Submitted | YES |
| P03 | 🟡 Candidate | YES route, proved for `n<=4`; `n>=5` unresolved in sprint |
| P04 | ✅ Submitted | YES route, proved/certified for `n<=4`; `n>=5` conjectured |
| P05 | ✅ Submitted | YES route, full biconditional claimed |
| P06 | ✅ Submitted | NO route via `K_n` counterexample |
| P07 | ✅ Submitted | YES route |
| P08 | ✅ Submitted | NO route via octahedron + Gromov |
| P09 | ✅ Submitted | YES |
| P10 | ✅ Submitted | YES |

## External Comparison Snapshot (2026-02-14)

The table under **Final Results (External Adjudication View)** is the canonical expected-vs-actual table.
This section provides score bands and source links.

Adjudication score bands (depending on `P06` ruling):

1. Strict theorem-level alignment: `30%-40%` (`3/10` to `4/10`).
2. Directional alignment: `60%-70%` (`6/10` to `7/10`).
3. Risk-adjusted score: `47.5%-57.5%` (neutral midpoint `52.5%`).

Primary source documents:

- `docs/results/solution_comparison_2026-02-14.md`
- `docs/results/solution_comparison_full_audit_2026-02-14.md`
- `docs/results/post_mortem_2026-02-14.md`

Precedence note:

- The **Final Results (External Adjudication View)** table above is the canonical expected-vs-actual record.
- Remaining sections in this README are primarily internal run telemetry (methods, costs, escalation history, and artifact provenance).

## Sprint summary

**9 of 10 problems submitted** across 28 sessions, ~414 agent messages, ~1M artifact tokens, ~10M total compute tokens, ~$400 estimated cost. One problem (P03) remains at Candidate status with an L5 barrier (n=2,3,4 proved; n>=5 not closed in-sprint). Operationally this was a time-allocation issue (late start on P03 + effort split across other lanes), not a hard compute-resource outage.

## Conclusions: Throughput and Closure Economics

The post-mortem indicates that the dominant residual errors were primarily **control-plane errors** (formalization, polarity control, contradiction gating), not a uniform lack of model capability. In practice, this makes the main optimization target an improved agent/model harness and orchestration pipeline.

Estimated performance ranges versus an unaided baseline (scenario-dependent):

| Operating mode | Throughput multiplier | Theorem-closure multiplier | Primary limiting factor |
|---|---:|---:|---|
| Current constrained run (observed stack) | ~3x-8x | ~1.5x-3x | Statement/polarity control gaps |
| Expert orchestrator with stronger policy controls | ~10x-20x | ~3x-8x | Frontier invariant discovery |
| Expert orchestrator + curated lemma corpus + automated contradiction checks | ~20x-50x | ~5x-15x | Novel structural bridge lemmas |

Closure cost rises nonlinearly near the frontier: early lanes close cheaply, while the final one or two lanes absorb most marginal effort. The highest-ROI upgrades were identified as:

1. Statement lock at G0 (`PXX/statement_lock.md`).
2. Mandatory contradiction gate before `✅`.
3. Mandatory independent opposition pass on binary-sign lanes.
4. Early parallel compute pre-provisioning for projected long serial sweeps.
5. Final-form normalization lint before release.

See detailed analysis in:

- `docs/results/post_mortem_2026-02-14.md` (forensic root-cause, ROI, debt, upgrade paths)
- `docs/results/workflow_adjustment_impact_2026-02-14.md` (counterfactual uplift and cost model)
- `docs/results/postmortem_root_cause_2026-02-14.md` (lane-by-lane root-cause matrix)

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

Cost is dominated by Claude Opus. Heaviest per-problem consumers: P04 (~$130, 28 sessions of SOS solver development) and P03/P05/P09 (~$55–80 each).

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

Scouts used: GPT-pro 5.2, Claude Opus Research, DeepSeek-R1, Qwen3-480B, Kimi K2.5. Best results from GPT-pro and Claude Opus Research to address blockers with the agentic flow; DeepSeek-R1 and Qwen3-480B were good at structured math problems; Kimi K2.5 irrecoverable on complex problems (spends all tokens on reasoning, zero usable output).

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
