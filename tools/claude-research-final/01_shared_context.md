# Shared Context Bundle (Research Mode)
Generated: 2026-02-12 12:52:25 -08:00
Root: D:\firstproof

> **Supersession note (2026-02-13):** This file is an archival snapshot generated before Sessions 20-23.  
> Authoritative current state is in root `README.md` and `RESULTS.md`: **8 submitted / 2 candidate (P03, P04), P05 closed**.  
> Any contradictory status/totals below are historical context only.



======================================================================
SOURCE: README.md
======================================================================

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

## Results

| Problem | Domain | Status | Confidence | Budget used |
|---------|--------|--------|------------|-------------|
| P01 | Stochastic analysis | ✅ Submitted | HIGH (YES, quasi-invariance proved; **R1 CITE_PLUS: BG proof chain verified + Hairer-Steele independent path; all gaps closed**) | ~20/80 msgs |
| P02 | Representation theory | ✅ Submitted | HIGH (YES, Kirillov + Gauss sums + JPSS + multiplicity-one) | ~12/80 msgs |
| P03 | Algebraic combinatorics | 🟡 Candidate | HIGH (YES, Mallows/ASEP; **n=2,3,4 proved**; n≥5 infeasible — branching fails (EXP-20: 4 obstructions), AS reduction partial; L5 barrier) | ~67/200 msgs |
| P04 | Finite free convolution | 🟡 Candidate | HIGH (n=2,3 proved; **n=4 even quartic (b=0) PROVED (CE-16)**; general n≥4: **495K exact tests ALL PASS (CE-19, corrected validity filter)**; 9 proof routes failed; b-c' cross-terms uncontrolled) | ~66/300 msgs |
| P05 | Equivariant homotopy | 🟡 Candidate | HIGH (**7 theorems** + Frontier Thm; Class Ia proved, Class II open; 8+ proof approaches blocked; 825 total / 793 intermediate systems exhaustively tested) | ~37/80 msgs |
| P06 | Spectral graph theory | ✅ Submitted | HIGH (NO, K_n counterexample) | ~14/300 msgs |
| P07 | Lattices in Lie groups | ✅ Submitted | HIGH (YES, Q-PD + surgery realization proved) | ~6/80 msgs |
| P08 | Symplectic geometry | ✅ Submitted | HIGH (NO, Lagrangian octahedron + Gromov) | ~10/80 msgs |
| P09 | Tensor polynomial map | ✅ Submitted | HIGH (YES, D≤6; **all gaps closed ALL n≥5**: n≥6 via subset isomorphism; **n=5 kernel=15 proved exactly** via modular rank at 2 primes) | ~58/200 msgs |
| P10 | RKHS CP-ALS | ✅ Submitted | HIGH | ~12/120 msgs |

Status key: -- Not started | ✅ Submitted | 🟡 Candidate | 📊 Conjecture | ❌ Parked

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



======================================================================
SOURCE: RESULTS.md
======================================================================

# FIRSTPROOF — Consolidated Results Report

Snapshot date: 2026-02-12 (Session 15: Closeout Escalation Chain complete. CE-19 corrects quartic validity filter, 495K exact tests ALL PASS. EXP-20 kills P03 branching. 9 proof routes failed for P04 b≠0. All 3 🟡 barriers confirmed genuine.)
Scope: full portfolio (all 10 problems assessed, synthesis pass + escalation complete)
Methodology and autonomy constraints: see `methods_extended.md`.

## 1. Portfolio status

| Problem | Status | Outcome summary |
|---------|--------|-----------------|
| P01 | ✅ Submitted | **YES** — Φ⁴₃ quasi-invariance proved. **R1 CITE_PLUS (Session 10, E11)**: BG proof chain (arXiv:2004.01513) verified lemma-by-lemma for V_c; all 6 lemmas extend via (α) quartic coercivity + (β) UV scaling. **Independent path**: Hairer-Steele (arXiv:2102.11685) sub-Gaussian tails + Young directly yield A4. Two lines close the former gap. |
| P02 | ✅ Submitted | YES — modified RS integral. Key identity proved (all n); n=1 complete (Kirillov + Gauss sums); general n proved (JPSS + multiplicity-one). G0-G6 + upgrade cycle done. |
| P03 | 🟡 Candidate | YES — Mallows/ASEP chain. n=2,3,4 proved. **L5 barrier**: n≥5 formally infeasible; branching rule induction killed (EXP-20: 4 obstructions); AS reduction partial; 4 approaches all fail. |
| P04 | 🟡 Candidate | n=2,3 proved. **n=4 even quartic (b=0) PROVED (CE-16).** General n=4 (b≠0): **495K exact tests ALL PASS (CE-19, corrected quartic validity filter)**; 9 proof routes failed; b-c' cross-terms uncontrolled. |
| P05 | 🟡 Candidate | O-slice connectivity. **7 theorems** + **Impossibility Frontier Theorem**. Class Ia proved; Class II open; **8+ proof approaches blocked**. 825 total / 793 intermediate systems exhaustively tested. No CE found. |
| P06 | ✅ Submitted | Answer is NO via complete-graph counterexample. **Synthesis pass**: proof verified complete, all tests pass, upgraded to ✅. |
| P07 | ✅ Submitted | Answer is YES. Q-PD proved (Shapiro). Surgery realization proved self-contained: surgery below middle dim + UCSS duality forces Q-acyclicity. G0-G6 done. |
| P08 | ✅ Submitted | Answer is NO via Lagrangian octahedron counterexample. G6 patch: topology-preserving definition eliminates regularity gap; proof is 3-step (S² topology → exactness → Gromov). G0-G6 done. |
| P09 | ✅ Submitted | YES, D≤6. **All gaps closed for ALL n≥5**: n≥6 via subset isomorphism + exact base case; **n=5 kernel=15 proved exactly** (EXP-11b: modular rank = 1756 at 2 primes + float SVD 10.7 order gap). D_n masking proved (§2.5a); separation genericity proved algebraically (§2.5b). |
| P10 | ✅ Submitted | Matrix-free PCG solver package completed and adversarially patched. |

## 2. Method escalations used

| Escalation level | What changed | Where it mattered |
|------------------|-------------|-------------------|
| L0: Baseline | Implementer (Claude) + Reviewer (Codex), gate workflow G0-G7 | All attempted problems |
| L1: Adversarial hard-gating | Mandatory reject/patch cycles for proof-risk claims | P10, P09 |
| L2: Counterexample-first protocol | Early budget allocated to disproof search before proof drafting | P04, P06 |
| L3: Experiment-first validation | Scripted numeric/symbolic checks required before claims | P04, P06, P09, P10 |
| L4: Scout model augmentation | External LLM checks as secondary verification channel | P10, tooling layer |
| L5: Latent-limit protocol | Explicit relaxed-pass criteria for theorem-level stalls | P04, P09 (policy enabled) |
| L6: Final synthesis pass (planned) | Single end-stage GPT-5.2-pro consolidation over all artifacts | Planned after all active problems settle |

## 3. Token and prompt/message accounting

Source of truth: per-problem `transcript.md` and `audit.md` estimates.

Note: transcript fidelity is mixed. Active closure lanes (e.g., P04/P06/P08/P09/P10) retain detailed logs; several parked/summary lanes currently store compact transcript stubs rather than full message-by-message history.

| Problem | Est. tokens | Prompt/message count | Notes |
|---------|-------------|----------------------|-------|
| P01 | ~45,000 | ~20 | G0-G2 + Sessions 3-10: A4 closed, CITE_ONLY ingest (E7), scout cross-check (E8), gap analysis (E9-E10: 7 approaches), **Session 10 (E11): R1 CITE_PLUS — BG proof chain verified + Hairer-Steele independent path; gap CLOSED** |
| P02 | ~33,000 | ~12 | G0-G6 + upgrade cycle: key identity + n=1 proof + JPSS + multiplicity-one |
| P03 | ~175,000 | ~67 | Full G0-G7 + synthesis + Sessions 9-11 + **Session 15: EXP-20 branching test (4 obstructions → BRANCHING_FAILS)** |
| P04 | ~155,000 | ~66 | Sessions 8-15 + CE-9/10/11/12d/12e/13/16/17/18/19/20 + **Session 15: quartic validity filter corrected (CE-19: 495K exact ALL PASS); 9 routes failed** |
| P05 | ~73,000 | ~37 | G0-G5 + Sessions 7-15: 7 theorems + Frontier + 8+ approaches blocked + Kimi scout eval |
| P06 | ~53,600 | ~14 | from transcript metrics/log |
| P07 | ~20,000 | ~6 | G0-G6 + patch: Q-PD via Shapiro + surgery realization (self-contained) |
| P08 | ~30,000 | ~10 | G0-G6 + patch: octahedron counterexample + Gromov obstruction |
| P09 | ~114,000 | ~58 | from transcript metrics/log + upgrade cycle (EXP-6/6e) + formalization (EXP-10/10b) + Session 7-8: n=5 closure |
| P10 | ~116,000 | ~12 | tokens from transcript component sums; message budget from audit/transcript |
| **Total (all problems)** | **~814,600** | **~300** | all values are estimates (token_source: estimate), not API-billed absolutes; sum: 45+33+175+155+73+53.6+20+30+114+116=814.6K tokens, 20+12+67+66+37+14+6+10+58+12=302 msgs |

## 4. What worked vs. what stalled

Worked:
- High-confidence derivation + implementation tasks with checkable algebra and experiments (P10).
- Counterexample-oriented graph route with explicit spectral checks (P06).
- Counterexample-first + topological obstruction (Gromov) for symplectic problem (P08).
- Fast falsification loops to prevent overclaiming.
- Definition-only escalation protocol: scout briefs enabled P08 and P07 re-opening without proof contamination.
- Shapiro's lemma + surgery citation for lattice Q-PD argument (P07).
- Multiplicity-one theorem (AGRS) + PID argument to close partial ideal gap (P02).

Stalled:
- ~~Theorem-level finite-n closure when numeric evidence is strong but symbolic bridge is missing (P09).~~ **RESOLVED**: All 4 gaps closed algebraically for n≥6 (Session 7: §2.5b separation genericity + §2.5c base-case coverage).
- ~~n=3 symmetry conjecture algebraic closure despite 48+ digit numerical evidence (P03).~~ **RESOLVED (n=3)**: Degree-bound + 82-zero test (Session 4). ~~n=4 remains open.~~ **RESOLVED (n=4)**: Modular degree-bound 54 + 90-value sweep (Session 6). n ≥ 5 remains open (computationally infeasible).
- ~~Masked-domain equivalence and uniform-n algebraic closure (P09).~~ **RESOLVED**: D_n masking proved (§2.5a); kernel formula proved exact via lower bound + base-case coverage (§2.5c).

## 5. Final result after synthesis pass

- **Fully submitted: 7 problems** (P01, P02, P06, P07, P08, P09, P10).
- Candidate: 3 problems (P03, P04, P05).
- Parked: 0 problems.
- Not started: 0 problems.

All 10 problems assessed to at least G2 (route map) level.

### Synthesis pass delta (this session)

| Problem | Before | After | Change |
|---------|--------|-------|--------|
| P06 | 🟡 Candidate | ✅ Submitted | Proof verified complete; all numerical tests pass; upgraded |
| P03 | 📊 Conjecture | 🟡 Candidate | EXP-5: Richardson extrapolation (48+ digits); upgraded to 🟡. **Session 4: n=3 PROVED (degree-bound 20 + 82-zero).** **Session 6: n=4 PROVED (modular degree-bound 54 + 90-sweep × 2 primes).** |
| P04 | 📊 Conjecture | 🟡 Candidate | CE-5/6: n=3 proved. CE-10: closed-form Φ₄ + additive vars. CE-11: 2nd-order PSD + 105K exact tests. **CE-16: n=4 even quartic (b=0) subcase PROVED (convexity + algebraic decomposition).** General n=4 (b≠0) remains open. |
| P09 | 📊 Conjecture | **✅ Submitted** | EXP-6/6e: D≤6 established. EXP-8 series: kernel formula 9·C(n−2,4). **EXP-9: D_n masking PROVED n≥6.** **EXP-10/10b: Kernel formula exact.** **Session 7: All 4 gaps closed n≥6.** **Session 8: n=5 kernel=15 proved exactly (EXP-11b: modular rank 1756 at 2 primes).** Upgraded to ✅. |
| P07 | ❌ Parked | ✅ Submitted | Escalation success: Q-PD proved (Shapiro); surgery gap closed (below-middle-dim surgery + UCSS duality); upgraded to ✅ |
| P08 | ❌ Parked | ✅ Submitted | Escalation produced counterexample; G6 patch adopted topology-preserving definition, eliminating regularity gap; upgraded to ✅ |
| P01 | ❌ Parked | **✅ Submitted** | A4 closed; full proof assembled. **R1 CITE_PLUS (E11): BG proof chain verified + Hairer-Steele independent path. Gap CLOSED; upgraded to ✅.** |
| P02 | ❌ Parked | ✅ Submitted | Key identity proved (all n); n=1 complete (Kirillov + Gauss sums); general n proved (JPSS + multiplicity-one via AGRS) |

## 5b. Per-problem escalation matrix

| Problem | Level Reached | Closure Level | Validation Level | Blocking Claim | Primary Toolchain | Independent Check | Outcome | Confidence Tier |
|---------|--------------|---------------|-----------------|---------------|-------------------|-------------------|---------|----------------|
| P01 | **L3** | **L3** | **G7 (unconditional; G6 ACCEPT, G7 ACCEPT)** | ~~BG Thm 3 gap~~ CLOSED | Claude Opus 4.6 + CITE_PLUS (BG proof chain) + Hairer-Steele | R1 CITE_PLUS: all 6 BG lemmas verified for V_c; Hairer-Steele independent path | **✅ Submitted** | Proved + CITE_PLUS verified |
| P02 | L0 (Mode R) | L0 | G6 C3 | Partial ideal gen (JPSS) | Claude Opus 4.6 + scout briefs | AGRS multiplicity-one (CITE) | ✅ Submitted | Proved + Cited |
| P03 | **L5** | L3 | G6 C2 + EXP-14b + EXP-16 + EXP-17 | Symmetry Conjecture n≥5 | Perturbation + degree-bound + 5 reduction attempts (EXP-17) | 8 structural shortcuts all fail; L5 barrier certificate | 🟡 Candidate | Proved (n≤4) + L5 barrier (n≥5, 8 shortcuts) |
| P04 | L4 | **L4 (n=4 b=0 proved)** | G6 + CE-6 + CE-10 + CE-11 + CE-13 + **CE-16** | General n=4 (b≠0): b-c' cross-terms; SDP/SOS solver needed | Φ₄ closed-form + additive vars + 2nd-order PSD (CE-11) + **CE-16: convexity proof for b=0** | CE-11: 105K exact ALL PASS; **CE-16: algebraic proof verified** | 🟡 Candidate | **Proved (n≤3 + n=4 b=0)** + Empirical (general n≥4) |
| P05 | **L5** | — | G5 (7 theorems + frontier theorem) | "If" direction Class II genuinely new; t-structure for non-regular cells | Claude Opus 4.6, WebFetch (ar5iv ×3), Python exhaustive computation | 5 approaches blocked; Thms 6-7: dim-uniform char + restricted sufficiency; 825 total / 793 intermediate systems tested; Class Ia proved; no CE | 🟡 Candidate | 7 theorems + Frontier Thm + restricted sufficiency |
| P06 | L3 | L2 | G6 + CE-1/CE-2 + synthesis | K_n eigenspace boundary | ce1 (n=3-24), ce2 (non-complete) | Synthesis pass | ✅ Submitted | Proved |
| P07 | L0 (Mode R) | L0 | G6 patch | Surgery realization gap | Shapiro + surgery below mid-dim | EXP-1 Q-PD verification | ✅ Submitted | Proved + Cited |
| P08 | L1 | L0 | External G6 + EXP-1/2 | Hausdorff vs topology-preserving def | exp1 octahedron + exp2 action | Codex external review | ✅ Submitted | Proved + Cited |
| P09 | L5 | **L5** (all gaps closed ALL n≥5) | G6 C2 + EXP-10b + EXP-11b + §2.5b/c | D_n masking + kernel exact + n=5 modular rank + separation genericity | Monomial decomposition + exact base case + modular rank verification + Zariski argument | EXP-8 series + EXP-9b + EXP-10/10b + EXP-11/11b + §2.5b/c proofs | **✅ Submitted** | All gaps closed ALL n≥5 |
| P10 | L4 | L0 | G6 C2 | SPD/PSD distinction | verify_matvec.py (6 tests) | GPT-5.2-pro scout | ✅ Submitted | Proved |

## 6. Escalation path for parked problems

A definition-only reference escalation protocol has been established at `common/definition_only_escalation.md`. This allows re-opening parked problems by ingesting ONLY definitions, notation, and theorem statements from primary sources — no proof text, no secondary sources, no human interpretation.

Priority order (by tractability):
1. **P08** (Symplectic) — ✅ RESOLVED: Lagrangian octahedron counterexample + topology-preserving definition + Gromov. Upgraded to Submitted.
2. **P07** (Lattices) — ✅ RESOLVED: Q-PD proved (Shapiro), surgery realization proved (self-contained). Upgraded to Submitted.
3. **P01** (Stochastic) — ✅ RESOLVED: quasi-invariance proved. R1 CITE_PLUS (E11): BG proof chain verified lemma-by-lemma; Hairer-Steele independent path. Upgraded to Submitted.
4. **P02** (Rep theory) — ✅ RESOLVED: general n proved via JPSS + multiplicity-one (AGRS). Upgraded to Submitted.
5. **P05** (Eq. homotopy) — 🟡 STRENGTHENED: **7 theorems** (Thms 1-4, 6-7) + **Impossibility Frontier Theorem (Thm 5)**. Class Ia (regular-only systems) PROVED by Thm 7 (restricted sufficiency). Class II (non-regular intermediate) remains open; **5 proof approaches blocked** (Session 13: isotropy separation for Z/4). Exhaustive computation: 104/793 intermediate systems proved (825 total across 17 groups).

## 7. GPT-5.2-pro final synthesis (planned)

After all active problem tracks are settled, run one final synthesis pass with GPT-5.2-pro:

1. Input all finalized artifacts (`answer.md`, `audit.md`, `transcript.md`, experiments) for each attempted problem.
2. Require strict mode: no new external theorem search for foundational lemmas in llm-only runs.
3. Ask for end-to-end reconciliation of unresolved MAJOR/FATAL bottlenecks only.
4. If GPT-5.2-pro still cannot close those bottlenecks with full artifact context, record this as evidence that the remaining gaps are not currently solvable with LLM-only methods (given current training/architecture).

## 8. Tooling provenance index

| Problem | Discovery tool | Validation tool | Script paths | Expected output |
|---------|---------------|-----------------|-------------|-----------------|
| P02 | Claude Opus 4.6 (Kirillov model derivation) | exp1_gauss_sum_verification.py | `P02/experiments/exp1_gauss_sum_verification.py` | ALL PASS (Gauss sums + conductor match) |
| P03 | Claude Opus 4.6 (perturbation theory + degree bound) | exp13c (82-zero), exp14b (deg n=3), exp16 (90-sweep), exp16b/16d (deg n=4) | `P03/experiments/exp13c*.py`, `exp14b*.py`, `exp16*.py` | n=3: 82/82 exact sym, deg 20<82; n=4: 90/90 modular sym, deg 54<90 |
| P04 | Claude Opus 4.6 (Φ₃ closed-form + Jensen) | ce6_n3_algebraic_proof.py | `P04/experiments/ce1_numeric_sweep.py` through `ce7_n4_check.py` | 285K+450 trials ALL PASS; n=3 proved; n=4 obstruction |
| P06 | Claude Opus 4.6 (K_n eigenspace decomposition) | ce1_complete_graph_verify.py | `P06/experiments/ce1_complete_graph_verify.py`, `ce2_other_graphs.py` | n=3-24 ALL PASS |
| P07 | Claude Opus 4.6 (Shapiro + surgery) | exp1_qpd_verification.py | `P07/experiments/exp1_qpd_verification.py` | Q-PD verified |
| P08 | Claude Opus 4.6 (octahedron construction) | exp1 + exp2 | `P08/experiments/exp1_octahedron_lagrangian.py`, `exp2_action_obstruction.py` | 8/8 Lagrangian; zero λ-integrals |
| P09 | Claude Opus 4.6 (monomial kernel + masking proof + formalization) | exp8 series + exp9/9b + exp10/10b | `P09/experiments/exp8*.py`, `exp9*.py`, `exp10*.py` | Kernel lower bound proved (exact over Q); Jacobian rank = codim |
| P10 | GPT-5.2-pro (scout candidate) → Claude Opus 4.6 (verification) | verify_matvec.py | `P10/experiments/verify_matvec.py` | 6/6 tests PASS |

## 9. Artifact map

- Runbook: `firstproof.md`
- Sprint pipeline: `firstproof_sprint_plan.md`
- Experimental setup and constraints: `methods_extended.md`
- Progress board: `README.md`
- Contamination policy/log: `CONTAMINATION.md`
- Shared scout tooling: `tools/scout_api.py`, `tools/model_capability_probe.py`, `tools/README.md`
- Handoff checklist: `common/claude_handoff_checklist.md`
- Escalation protocol: `common/definition_only_escalation.md`
- **Escalation ledgers**: `PXX/audit.md` (§ Escalation Ledger) — per-event rows with full provenance
- **Escalation events**: `PXX/transcript.md` (§ Escalation Events) — prompt/model/script/output per event

## 10. Out-of-scope improvements (time-constrained sprint)

The following were intentionally not executed in this sprint, but are plausible improvement paths:

1. Domain-adaptive fine-tuning on orthogonal-but-related proof corpora
   - Examples: adjacent theorem families, foundational lemmas, and structurally similar solved problems.
   - Goal: improve lemma selection and long-chain consistency without directly training on target First Proof solutions.

2. Process-supervised verifier fine-tuning
   - Train or adapt a verifier on step-level proof correctness signals, then loop with proposer models.
   - Goal: reduce false-positive proof completion and tighten G6 pass rates.

3. Formal-tool-coupled training/evaluation
   - Integrate Lean/SMT feedback for micro-lemma acceptance during generation.
   - Goal: improve symbolic rigor on bottleneck lemmas.

4. Retrieval-augmented foundational theorem memory (non-solution corpus)
   - Build a curated statement-index with precise hypotheses and statement numbers.
   - Goal: reduce citation/hypothesis slippage while preserving contamination constraints.

5. Longer-horizon multi-agent curricula
   - Train/tune agents on failure-replay from audit/transcript corpora (route failures, patch loops, reviewer faults).
   - Goal: improve route switching and reduce rewrite loops.

These are marked out-of-scope due schedule and reproducibility constraints for this run.

## 11. Final closeout note (Cycle 6, 2026-02-12)

Closeout Cycle 6: R1 websearch + SDP check + final assessment. Candidate-G6 ACCEPT (0 faults) on all 3 lanes.

| Lane | Closure tier | Cycle 6 action | Unresolved core claim | Why not escalated further |
|------|-------------|---------------|----------------------|--------------------------|
| P03 | L5 (barrier cert) | **R1 websearch: Alexandersson-Sawhney (arXiv:1801.04550).** Leading term E_{λ⁻}(x;1,t) proved symmetric for all n via AS+Hecke. Full E*_{λ⁻} gap persists (interpolation corrections not covered). Author correction applied. | Symmetry Conjecture for n ≥ 5 (lower-degree corrections) | 8 shortcuts fail; R1 lead partially closes (leading term only); same blocker class |
| P04 | L4 (b=0 proved) | **CE-16 (Session 14)**: Convexity in w + algebraic decomposition at endpoints proves −H ≥ 0 for b=0 subcase. General n=4 (b≠0) still open. | General n=4 (b≠0): b-c' cross-terms in degree-16 polynomial | b=0 RESOLVED; general case needs SDP or novel analytic technique |
| P05 | L5 (frontier thm) | **Final assessment**: no 6th approach identified. All 5 approaches reduce to non-uniform dim(V^L). L5 barrier reconfirmed. | "If" direction for Class II: t-structure for non-regular cells | 5 approaches blocked; irreducible at current tool level |

**Escalation policy compliance**: All 4 policy rules satisfied:
1. Current method-space exhausted (8/7/5 approaches per lane)
2. No escalation beyond definitions attempted (R1 websearch for P03 used CITE_ONLY)
3. Blockers are sharply defined single-sentence statements
4. Each lane frozen after same blocker class repeated across multiple attempts

---

## 12. Methodological observations for researchers

### Proved / Cited / Empirical taxonomy

Each claim in the portfolio falls into one of three evidence tiers:

| Tier | Definition | Examples |
|------|-----------|----------|
| **Proved inline** | Complete proof from first principles, no external citation needed | P06 counterexample; P10 SPD proofs; P07 Q-PD via Shapiro + surgery realization (self-contained); **P03 n=2 symbolic proof + n=3 Symmetry Conjecture (degree-bound + 82-zero test) + n=4 Symmetry Conjecture (modular degree-bound + 90-sweep)**; P02 n=1 (Kirillov + Gauss sums) |
| **Cited (statement-level)** | Argument depends on a published theorem cited with statement number | P08 Gromov §2.3.B₂'; P07 Selberg/Borel (classical, statement-level); P04 Voiculescu inequality (motivation only); P02 general n (JPSS [1] + AGRS multiplicity-one [5]) |
| **CITE_PLUS (verified)** | Argument depends on a published result verified at proof-lemma level via CITE_PLUS ingest | **P01 quasi-invariance (BG 2021 arXiv:2004.01513 — CITE_PLUS: all 6 lemmas verified for V_c; Hairer-Steele arXiv:2102.11685 — CITE_ONLY: sub-Gaussian tails + Young yields A4 independently)** |
| **Proved inline (algebraic)** | Construction + all gaps closed via algebraic proofs | **P09 n≥6**: kernel formula exact (9·C(n-2,4), lower bound + base-case coverage §2.5c); D_n masking proved (§2.5a); separation genericity proved (§2.5b) |
| **Empirical only** | Numerical/computational evidence without theorem-level proof | P03 n>=5 Symmetry Conjecture (48+ digits, 7 t-values for n=3); P04 n>=4 (285K trials + 150-digit high-precision; CE-7 cross-term obstruction for extending n=3 proof); P09 n=5 degree-6 kernel (EXP-6e, numerical only); P08 construction checks |

### Characteristic failure modes observed

1. **Algebra-to-geometry gap** (P07, resolved): The agent initially proved the algebraic claim (Q-Poincaré duality) rigorously via Shapiro's lemma but stalled on the geometric realization step, seeking a general surgery citation. The gap was closed by specializing to dimension 5, where surgery below the middle dimension is elementary and UCSS duality forces Q-acyclicity — yielding a fully self-contained proof. This illustrates how a citation gap can sometimes be bypassed by finding a more elementary, dimension-specific argument.

2. **Set-theoretic vs analytic convergence** (P08): The agent constructed a valid counterexample candidate and proved action invariance, but the limit argument conflated Hausdorff convergence of sets with convergence of line integrals. This highlights a systematic weakness in handling regularity questions at the boundary of point-set topology and analysis.

3. **Finite-n theorem gap** (P03, P04, P09): Strong numerical evidence (relative errors 10^{-4} to 10^{-6}) was obtained for finite cases, but the symbolic/algebraic bridge from numerics to theorem was not crossed. P04's n=3 gap was resolved by deriving a closed-form for Φ₃ and reducing to Jensen's inequality (CE-6), but the n≥4 gap remains open — CE-7 confirms that the n=3 technique (clean coefficient additivity under ⊞₃) does not extend. **P03's n=3 gap was resolved** by a degree-bound argument (EXP-14b/13c: max degree 20, 82 zeros > 20). **P03's n=4 gap was resolved** by the same logical structure scaled to modular arithmetic (EXP-16/16b/16d: max degree 54, 90 zeros > 54, two independent primes). **P09's gaps #1–#4 were ALL closed** in Session 7: separation genericity proved algebraically (§2.5b), kernel upper bound proved via base-case coverage (§2.5c). P09 upgraded to 🟡 Candidate. P03 n≥5 and P04 n≥4 remain open.

4. **Reference-blocked domains** (P01 FULLY RESOLVED; P02 fully unblocked; P05 partially unblocked): **P01 was FULLY RESOLVED** at R1 CITE_PLUS level (Session 10, E11). Two independent lines close the former gap: (1) BG proof chain (arXiv:2004.01513) verified lemma-by-lemma — all 6 lemmas extend to V_c via (α) quartic coercivity + (β) UV scaling hierarchy; (2) Hairer-Steele (arXiv:2102.11685) sub-Gaussian tails + Young's inequality directly yield A4 without needing BG extension. This resolves the L5 barrier from E10 (7 approaches exhausted at CITE_ONLY level). P02 was fully unblocked by deriving the key identity from first principles and closing the general-n gap via the AGRS multiplicity-one theorem. P05 was partially unblocked via CITE_ONLY definition ingest (BH, Rubin, HY), enabling formulation of candidate characterizations — but a Z/p² counterexample shows the stated characterization fails for intermediate transfer systems. **4 theorems proved** for P05: obstruction (Thm 1), positive scope (Thms 2-3), corrected "only if" with ν_O^eff (Thm 4). **Session 10**: "if" direction analyzed — 3 proof approaches blocked (equivariant Whitehead requires unproved t-structure; orbit filtration blocked by cross-level mixing in ν_O^eff; geometric detection requires RO(G)-graded extension); no counterexample found; classified as genuinely new technical result. **Session 11**: 4th approach (norm/restriction adjunction) also blocked (requires multiplicative structure; Wirthmüller bypass fails due to non-uniform isotropy separation). **Impossibility Frontier Theorem (Thm 5)** formalizes Class I (proved) vs Class II (open) boundary with explicit subgroup-lattice class map. **Session 13 (Cycle 5)**: 5th approach (isotropy separation for Z/4) reduces "if" to localized t-structure for non-regular representation spheres; BLOCKED — confirms gap irreducible at current tool level.

5. **Definition sensitivity** (P08): The external review revealed that the self-review had conflated two different definitions of "smoothing" (topological isotopy vs Hausdorff convergence). The agent's self-review accepted the proof under the stronger definition while the answer was written under the weaker one. This definitional drift is a subtle failure mode that only surfaced under adversarial external review.

### What the gate system caught

The G0-G7 gate system with adversarial G6 review was the single most important quality control mechanism. Specific catches:

- **P03 G6 Cycle 1**: Overclaim (YES for all n) downgraded to conjecture (n=2 proved, n>=3 conjectured)
- **P08 G6 External**: Step 2/5 regularity gap caught by external reviewer; self-review had accepted it
- **P09 G6 Cycle 1**: 5 faults including overclaim of "theorem" status for numerical results
- **P10 G6 Cycle 1**: 4 red flags including incomplete indexing specification

In every case, the G6 reject-then-patch cycle improved the final artifact quality. The pattern suggests that self-review alone is insufficient; external adversarial review (by a different model or agent) is necessary for reliable quality control.

### Contamination hygiene

Direct-solution web search was not performed during this sprint. The default operating mode was llm-only, with controlled exceptions:
- Scout model API calls (different LLM families) for independent reasoning checks
- Definition-only primary-source retrieval in relaxed passes (logged in `CONTAMINATION.md`)
- Producer-provided problem PDF (`arXiv:2602.05192`)

No contamination events were recorded. The definition-only escalation protocol (`common/definition_only_escalation.md`) was used to allow statement-level reference access while preventing proof contamination.

### Reproducibility

All experiment scripts in `PXX/experiments/` directories are self-contained Python scripts with:
- Fixed random seeds where applicable
- Version-pinned dependencies (numpy, scipy, sympy, mpmath, networkx)
- Tolerance thresholds documented in script comments
- Output logs preserved in `*_output.txt` files where generated

Scripts verified to reproduce during this review session:
- `P06/experiments/ce1_complete_graph_verify.py` (pass)
- `P06/experiments/ce2_other_graphs.py` (pass)
- `P07/experiments/exp1_qpd_verification.py` (pass)
- `P08/experiments/exp1_octahedron_lagrangian.py` (pass)
- `P08/experiments/exp2_action_obstruction.py` (pass)
- `P02/experiments/exp1_gauss_sum_verification.py` (pass, all tests)
- `P10/experiments/verify_matvec.py` (pass, all 6 tests)



======================================================================
SOURCE: methods_extended.md
======================================================================

# Methods: Agentic LLM Orchestration for Research-Grade Proof Attempts

## Abstract

This repository evaluates a tool-augmented, multi-model agentic LLM system applied to advanced mathematics problems under a strict "no human mathematical content" boundary. The human administrator ("Producer") performs workflow operations only (scheduling, budgeting, repo/logging hygiene, tool execution, publication cadence, and contamination enforcement). Operationally, the Producer is a runtime operator: actions and process decisions follow pre-decided policy rules rather than expert mathematical judgment. The Producer is abstracted from problem content, solution content, and solution steps; process evaluation is limited to structural response quality (gate compliance, artifact completeness, and status classification consistency), not mathematical correctness. Models generate essentially all mathematical content: formalizations, route selection, lemma decomposition, proof/counterexample construction, experiments, and writeups.

Critically, the system does not rely on a separate, human-engineered proof toolchain. Beyond commodity infrastructure (a shell, a runtime to execute code, version control, and constrained web access for references), the only active "tool" the Producer uses is prompting model agents, and the agents themselves author the tooling they need (scripts, checkers, experiment harnesses, templates, and coordination artifacts) as part of an organic bootstrapping process. The Producer runs agent-authored commands and scripts verbatim and records outputs; the Producer does not design or implement bespoke technical tooling intended to influence mathematical outcomes.

A relaxed mode permits limited internet retrieval strictly for published definitions and standard methods that may not be reliably encoded in model priors; it explicitly forbids searching for or incorporating existing solutions to the numbered problems. All external queries and sources are logged, and any accidental exposure to a direct solution is quarantined and marked as contamination.

### Tooling and scaffolding provenance (explicit)

- Agents may use external tooling (e.g., code execution, CAS, numeric computation, repository automation) and scaffolding documents (templates, gate checklists, escalation policies, coordination notes) for context and coordination.
- Provenance constraint: these tools and scaffolding artifacts are created by the agents themselves during the run (or derived from agent-authored instructions), as part of a self-bootstrapping workflow.
- The Producer's role is restricted to executing agent-authored procedures, enforcing rigid constraints, and maintaining high-reliability continuity (logging, audits, contamination hygiene, and publication).
- With additional engineering time, the Producer role could be replaced by a controller agent or deterministic automation (policy engine + executor) that applies the same constraints, escalation triggers, and publishing cadence; the nontrivial part is project-management dynamics, not mathematical content injection.

---

## 1. What is being evaluated

### 1.1 Unit under test

The evaluated object is the system, not a single prompt or model:

- multiple LLM roles with separation of duties
- explicit gate/phase structure
- deterministic verification via model-written scripts
- cross-model falsification passes
- escalation and stop-loss policies
- controlled internet retrieval for foundational references only (in relaxed mode)
- complete logging suitable for external audit

### 1.2 What success means in this repo

The output is always publishable as an attempt, even without a full proof:

- Solved: a proof or counterexample reaches publication-grade standards and passes adversarial review.
- Candidate: coherent draft with clearly identified remaining gaps or dependencies.
- Conjecture: strong evidence and partial structure, no complete proof.
- Parked: explored routes, documented blockers, and clear failure analysis.

The system is optimized to avoid silent failure (unlogged reasoning, untestable claims, overconfident proofs) and maximize the informational value of partial progress.

### 1.3 Non-goals

This repo does not claim:

- a raw single-shot model baseline
- human-guided theorem proving
- fine-tuning on the numbered problems
- incorporation of externally discovered solutions to the numbered problems
- proof that frontier models can solve arbitrary open research questions without domain adaptation

---

## 2. Autonomy boundary: what humans may and may not do

### 2.1 Human role: Producer (workflow only)

In this run, Producer activity is constrained to operational control:

- prompt dispatch and handoffs between model roles
- occasional administrative decisions (prioritization, budgets, park/escalate, publication timing)
- process decisions under pre-decided rules (gate criteria, stop-loss caps, escalation triggers)
- execution of model-authored scripts/commands (verbatim)
- enforcement of logging, status taxonomy, and contamination policy
- evaluation of structural response quality (coherence, completeness, and classification consistency)

Operationally, the Producer functions as a runtime operator, not a domain expert. The Producer does not add mathematical ideas, proof strategy, or domain interpretation, and does not exercise expert-level judgment over solution procedures or eventual solution content. Mathematical correctness is evaluated by agent review/falsification and deterministic checks, not by the Producer.

### 2.2 Disallowed human actions (mathematical content)

The Producer must not:

- supply proof ideas, reductions, lemma suggestions, or route hints
- isolate "the crux" via human mathematical judgment
- interpret references in a way that selects key mathematical ideas
- rewrite mathematical prompts to steer outcomes
- silently correct mathematical errors

If a boundary violation occurs, it must be logged and the affected claim treated as non-autonomous.

### 2.3 Prompt authorship discipline (anti-leakage)

Prompts containing mathematical content should be authored by model roles (Implementer/Reviewer) and relayed verbatim when dispatched to other models/tools. This mitigates accidental human signal injection through prompt rewriting.

Evidence for boundary enforcement is maintained in:

- per-problem transcripts: `PXX/transcript.md`
- per-problem intervention logs: `PXX/audit.md` ("Human interventions")
- contamination log: `CONTAMINATION.md`

---

## 3. System architecture (roles and rationale)

### 3.0 Full control stack

The run uses a layered control stack:

- Layer 3 (workflow/policy): gate rules, stop-loss caps, escalation triggers, acceptance criteria, and publication cadence.
- Layer 2 (agent orchestration): role-scoped implementer/reviewer/scout loops, handoffs, and patch cycles.
- Layer 1 (LLM reasoning/generation): mathematical drafts, decompositions, scripts, critiques, and revisions.
- Layer 0 (model internals): opaque in-model representations and inference behavior.

In this sprint, Layer 3 is human-operated as a runtime function. The stack is automation-amenable because control logic is explicit and rule-based.

### 3.1 Roles

- Implementer (I): produces math artifacts (formalization, route map, lemma DAG, proof drafts, experiments, scripts, writeups).
- Reviewer (R): adversarially audits Implementer outputs for missing hypotheses, quantifier errors, circularity, uncited dependencies, and overclaim.
- Scouts (S): independent model families used primarily for falsification, gap-finding, and independent re-derivation checks.
- Producer (H): workflow administration only.

### 3.2 Why role separation matters

Role separation reduces:

- self-confirmation loops
- hidden edge-case failures
- overclaiming without closure
- unbounded exploration without exits

Reviewer and Scout roles provide internal adversarial pressure analogous to seminar and peer-review dynamics.

---

## 4. Artifacts and auditability

### 4.1 Canonical per-problem artifacts

Each problem lane maintains:

- `answer.md`: clean result (proof/counterexample/conjecture) with explicit status and uncertainty flags
- `audit.md`: gate history, routes, blockers, dependency ledger, escalation events, intervention log
- `transcript.md`: interaction provenance (prompts, responses, tool calls, outputs)
- `experiments/`: model-authored scripts and reproducible outputs

### 4.2 Why this design is used

The artifact split provides:

- reproducibility (scripts + outputs)
- auditability (decision trace)
- failure analysis (preserved route failures)
- clean external presentation (`answer.md`)

This structure prevents result laundering by preserving unsuccessful attempts and unresolved gaps.

---

## 5. Gate protocol (main control loop)

Execution follows gate phases with required deliverables:

- G0 Formalize: explicit quantifiers, types, symbol glossary, ambiguity list
- G1 Background/dependency ledger: required definitions/theorems, internal vs external dependencies
- G2 Route map: multiple routes, falsification tests, first experiment plan
- G3 Lemma DAG: dependency structure with internal/cited/empirical labeling
- G4 Experiments/falsification: minimal reproducible tests and counterexample search
- G5 Proof draft: end-to-end argument plus explicit unresolved gap list
- G6 Adversarial review: severity-ranked defects, patch cycles, acceptance gate
- G7 Package: polished artifacts with citation precision and reproducibility pointers

Gate/stop-loss/escalation policy is defined in:

- `firstproof.md` (canonical)
- `firstproof_sprint_plan.md`
- `common/claude_handoff_checklist.md`

---

## 6. Stop-loss and escalation

### 6.1 Why stop-loss is necessary

Without explicit stop-loss, LLM workflows tend to burn budget in:

- rewrite loops (same argument rephrased)
- idea sprawl without closure
- pseudo-rigor with untracked gaps

### 6.2 Stall detection (conceptual)

Escalation should trigger when repeated iterations produce:

- no new lemma closure
- no new experiment signal
- no route change
- repeated Reviewer rejection of the same defect class

### 6.3 Escalation ladder

Typical progression:

1. constrained retry on the blocking lemma
2. Reviewer-minimal patch request with explicit defect categories
3. Scout falsification/gap pass
4. relaxed definition-only retrieval if blocked by missing machinery
5. park with explicit failure analysis if unresolved

### 6.4 Parking is valid

Parking is successful process execution when it yields:

- precise blocker dependency
- evidence of attempted routes
- explicit failure reason
- continuation-ready artifacts

---

## 7. Verification stack (why claims are trusted)

### 7.1 Deterministic computation (model-authored)

Where relevant, models author scripts for identity checks, boundary tests, and counterexample search; outputs are committed as evidence. Scripts support claims but do not replace logical proof where theorem closure is required.

### 7.2 Adversarial review for strong claims

No submitted claim is accepted without Reviewer sign-off. Reviewer checks target:

- hidden assumptions
- quantifier/type errors
- circular dependency
- numerics used where symbolic closure is required
- citation misuse or missing statement-level support

### 7.3 Cross-model falsification

Scouts are tasked to:

- produce counterexample attempts
- identify proof gaps
- re-derive key lemmas independently
- expose missing hypotheses

Cross-model agreement is a stability signal, not proof; disagreement is logged as a risk signal.

### 7.4 Inter-model resonance (working hypothesis)

A practical observation in this run: stronger outcomes correlate with independent structural convergence across model families plus survival under adversarial review and deterministic checks.

---

## 8. Relaxed mode: controlled internet use

### 8.1 Motivation

Relaxed mode exists for cases where missing definitions or theorem statements block progress and are unreliable in model priors.

### 8.2 Allowed retrieval

Permitted targets:

- formal definitions and canonical notation
- published methods and standard lemmas
- citation metadata (paper IDs, statement numbers, hypotheses)

Purpose:

- reduce definition drift
- avoid hallucinated foundational facts
- improve statement-level citation accuracy

### 8.3 Disallowed retrieval

Prohibited:

- direct solution search for numbered problems
- queries likely to retrieve direct solution writeups
- incorporation of external solution text into mathematical content

### 8.4 Contamination handling

If accidental direct-solution exposure occurs:

- log timestamp/URL/exposure details
- quarantine affected lane
- do not incorporate exposed content
- mark affected claim as contaminated/non-autonomous

Policy and logging references:

- `common/definition_only_escalation.md`
- `CONTAMINATION.md`

---

## 9. Why this method vs single-shot prompting

### 9.1 Single-shot limitations

Single-shot workflows are often bottlenecked by:

- prompt variance and hidden human judgment
- no adversarial pressure
- no deterministic verification
- weak counterexample coverage
- poor long-horizon state management

### 9.2 Orchestration gains

This method adds:

- explicit decomposition (gates + lemma DAG)
- systematic falsification
- adversarial correctness pressure
- reproducible computational evidence
- bounded exploration (stop-loss/escalation)
- auditable provenance

Net effect: reduced overclaim risk and higher value partial results.

---

## 10. Threat model and validity

### 10.1 Autonomy threats

Threat: subtle human mathematical injection (prompt edits, lemma guidance, interpretive summaries).  
Mitigation: role boundary, transcript logging, intervention classification, prompt authorship discipline.

Threat: contamination through retrieval.  
Mitigation: constrained relaxed mode, explicit logging, quarantine protocol.

### 10.2 Correctness threats

Threat: hallucinated citations/statements.  
Mitigation: statement-level citation requirements, Reviewer enforcement, controlled retrieval.

Threat: numerics misread as proof.  
Mitigation: explicit proved/cited/empirical separation and Reviewer blocking of theorem overclaims.

Threat: proof-by-verbosity.  
Mitigation: lemma DAG + defect tracking + adversarial gate.

---

## 11. Interpreting failure modes

Different unresolved outcomes provide different signals:

- blocked on definitions/machinery -> retrieval/corpus coverage bottleneck
- blocked on symbolic bridge despite strong numerics -> representation/composition bottleneck
- repeated same-class Reviewer defects -> process/taxonomy tuning issue
- cross-model instability -> fragile route or false/underspecified claim

These failures are treated as informative outputs, not discarded noise.

---

## 12. Reproducibility and replication

A third party should be able to:

- read clean claims in `answer.md`
- audit decisions/escalations in `audit.md`
- inspect execution provenance in `transcript.md`
- rerun evidence scripts from `experiments/`

Portfolio summaries are maintained in:

- `README.md`
- `RESULTS.md`

---

## 13. Practical autonomy in this project

Autonomy is operationalized as:

- no human mathematical ideas/content
- no human isolation of core mathematical bottlenecks
- model-authored solution and verification artifacts
- human role restricted to runtime operation, operational continuity, and integrity enforcement under pre-decided rules

This is a laboratory protocol, not a prompt demo. It is intended to measure what frontier models can do when human input is reduced to administrative functions that are, in principle, automatable.

---

## 14. Minimal executive summary (README-sized)

- We use an agentic, multi-model LLM pipeline with explicit gates, adversarial review, falsification, and deterministic verification.
- Human input is restricted to workflow administration and integrity enforcement; no mathematical content is provided by the human operator.
- Relaxed mode allows internet retrieval only for published definitions and standard methods; direct solution retrieval is prohibited and contamination is logged/quarantined.
- Outputs are auditable: proofs/counterexamples where achieved, and explicit, high-value failure analyses where not.

---

## 15. Observed Capability Boundaries and Future Work

This sprint identified a practical boundary between:

- lanes that close under structured orchestration plus adversarial review, and
- lanes that stall at abstraction-bridging steps despite strong evidence and process discipline.

Observed stalls were concentrated in domains requiring new structural glue (for example finite-to-uniform symbolic closure), not primarily in domains requiring only better workflow hygiene.

Key implication:
- escalation improves reliability, but does not itself create new representational capacity.

Future boundary shifts are more likely to come from:

- domain-adaptive fine-tuning on adjacent theorem families,
- theorem retrieval with structural matching,
- formal verifier coupling (Lean/Coq/SMT),
- process-level verifier training from audit/failure corpora,
- and neural-symbolic architecture improvements.

Extended discussion:

- `docs/methods/technical_limitations.md`
- `docs/methods/future_work.md`

---

## 16. Agent-to-LLM Prompt Equivalency (Heuristic)

For documentation and replication planning, this project uses a rough equivalency estimate between:

- one orchestrated agent prompt (role-aware, gate-scoped, with artifact constraints), and
- an equivalent amount of single-model (llm-only) prompting needed to reach comparable control and validation.

### 16.1 Working conversion used in this repo

Heuristic:

- `1` agent-orchestration prompt ~= `10` llm-only prompts
- split as:
  - `8` short prompts (state updates, local repairs, checklists, narrow retries)
  - `2` long prompts (route reset, synthesis, closure packaging)

This is intentionally approximate. It is a planning aid, not a measured law.

### 16.2 Why this conversion is reasonable here

In this workflow, a single agent prompt usually bundles:

- role assignment (Implementer/Reviewer/Scout behavior),
- gate requirements,
- stop-loss rules,
- artifact write targets,
- and acceptance tests.

Without role orchestration, those controls are often reconstructed manually across many smaller prompts.

### 16.3 Suggested use in reporting

When reporting effort in documentation:

- keep API token counts as primary quantitative accounting,
- use the `1:10` prompt-equivalency only as secondary interpretation of orchestration overhead,
- and always label it as heuristic (`8 short + 2 long`) rather than empirical measurement.

### 16.4 Limits of the heuristic

Do not use this conversion:

- as a benchmark claim across unrelated projects,
- as a model-quality metric,
- or as evidence of theorem correctness.

It is only an operational estimate for this repository's gate-driven process.

---



======================================================================
SOURCE: docs/methods/technical_limitations.md
======================================================================

# Technical Limitations and Escalation Rationale

## Purpose

This document explains why escalation was necessary in this project, what escalation can and cannot fix, and why some lanes stalled despite strong workflow controls.

Human role note for interpretation: the Producer operated as a runtime operator under pre-decided policy rules (gates, stop-loss, escalation), not as a domain expert supplying mathematical judgment or solution content. The operator remained abstracted from problem/solution details and assessed structural process quality/classification only; correctness adjudication was delegated to agent review and deterministic validation.

Control-stack framing used in this repo:
- policy/workflow layer (runtime operation against fixed rules),
- agent orchestration layer (implementer/reviewer/scout loops),
- base LLM generation layer,
- opaque in-model inference layer.

The short version:
- A lane like `P03` is not "unsolvable in principle."
- Under the current autonomy and training constraints, some lanes sit outside reliable closure for a general frontier LLM stack.
- Others (`P01`, `P09`) were eventually closed via escalation (CITE_PLUS, modular rank proofs), demonstrating that the boundary is not static.

## 1. Two distinct failure modes

### 1.1 Coverage failure (missing definitions/machinery)

Some domains depend on highly specific technical references and exact hypotheses. When those are weakly represented in model priors, the model may:
- blur neighboring definitions,
- import the wrong theorem schema,
- or generate plausible but invalid analogies.

This is a knowledge-coverage limitation.

### 1.2 Representational failure (missing structural glue)

Even when references are present, some closures require:
- discovering new invariants,
- finding non-local abstraction bridges,
- proving uniform finite-to-all-n statements,
- or composing theorems in combinations not strongly represented in training traces.

This is not only a retrieval problem. It is a representation/composition limitation.

## 2. Why escalation was required

Escalation in this repo exists to reduce false confidence and preserve progress quality:
- adversarial review catches hidden quantifier and hypothesis errors,
- deterministic experiments catch algebraic or numerical contradictions,
- stop-loss prevents unbounded rewrite loops,
- definition-only retrieval reduces hallucinated background dependencies.

Without escalation, the system overstates closure risk on difficult lanes.

## 3. What escalation can fix vs cannot fix

Escalation can fix:
- definition drift,
- missing statement-level citations,
- weak empirical validation protocols,
- overclaiming and artifact inconsistency.

Escalation cannot directly create:
- new invariants,
- new theorem-composition operators,
- robust finite-to-general symbolic bridges,
- domain-specific abstraction leaps absent from model behavior.

## 4. Why some gaps persisted (and why others closed)

Observed in this project:
- `P01` depended on deep renormalization machinery — closed via R1 CITE_PLUS (BG proof chain) + independent path (Hairer-Steele). Escalation from CITE_ONLY to CITE_PLUS was the key unlock.
- `P09` reached strong partial structure, then closed via modular rank proofs at two primes + subset isomorphism for n≥6.
- `P04` reached strong empirical/formal partial structure (n≤3 proved, 105K exact tests at n=4) but stalled at a degree-16 polynomial certificate. 6 proof routes exhausted.
- `P03` proved n≤4 via degree-bound closure but n≥5 is computationally infeasible (~65-260 days for n=5 alone).
- `P05` proved 7 theorems but the "if" direction for Class II transfer systems remains open — 4 approaches all reduce to the same non-uniform dimension obstruction.

Inference:
- workflow quality improved substantially,
- escalation (CITE_PLUS, modular arithmetic, exhaustive computation) closed some gaps,
- but remaining blockers are mostly representational rather than process hygiene failures.

## 5. Why "not baked in" is not the whole explanation

Missing references are only part of the story.

Even with better retrieval or broader pretraining exposure, closure still requires:
- correct decomposition,
- consistent multi-layer hypothesis tracking,
- and reliable synthesis of several technical components without leaks.

Training-data density raises probability of success but does not guarantee theorem closure.

## 6. Latent interpolation boundary (practical framing)

The current stack is strong at:
- local algebraic manipulation,
- theorem application when hypotheses are explicit,
- numerical/symbolic test generation,
- bounded derivation loops.

It is weaker at:
- identifying entirely new organizing principles,
- long-horizon structural synthesis with no stable template,
- uniformly closing symbolic bridges from finite evidence.

This is the practical boundary observed in the sprint.

## 7. Emergent resonant coherence for representative model refinement

This project used a practical reliability signal we call emergent resonant coherence:
- independent model families converge on similar structural decompositions,
- those decompositions survive adversarial review,
- and they remain stable under deterministic checks.

Here, "representative model refinement" means selecting diverse model roles/families (implementer, reviewer, scouts), then refining claims only when cross-model structure and executable evidence remain consistent.

### 7.1 What this addresses

It addresses common single-model failure modes:
- prompt-fragile reasoning,
- self-confirmation loops,
- narrow route fixation,
- and low-visibility hypothesis drift.

Operationally, it improves triage: when independent models converge and checks pass, the lane is prioritized for closure; when they diverge, escalation or park decisions are triggered earlier.

### 7.2 What this augments vs human-insight-driven workflows

Compared to standard human-insight-driven work, this mechanism augments:
- route selection (from one-model intuition to multi-model structural agreement),
- early fault detection (from manual spot-checking to adversarial and scripted checks),
- and claim confidence calibration (from narrative confidence to convergence-plus-validation evidence).

It can partially replace informal human "sanity filtering" in early and middle phases, especially for:
- candidate route ranking,
- falsification targeting,
- and patch-cycle prioritization.

### 7.3 What this does not replace

It does not replace:
- theorem-level proof obligations,
- discovery of genuinely new invariants when no model supplies the bridge,
- deep domain taste that identifies fundamentally new organizing principles,
- or formal correctness guarantees by itself.

Resonance is a reliability amplifier, not a proof substitute. Cross-model agreement can still converge to a shared mistake; deterministic validation and adversarial review remain mandatory.

### 7.4 Why it still matters under autonomy constraints

Under strict no-human-math constraints, resonant coherence is one of the few available mechanisms to increase reliability without injecting human mathematical content.

It does not remove representational ceilings, but it:
- reduces wasted budget on unstable routes,
- increases reproducibility of intermediate claims,
- and makes escalation decisions auditable.

## 8. Repo-level evidence pattern

Closed or strongly closed lanes clustered in domains with:
- direct algebraic reductions,
- bounded symbolic structure,
- or known global obstructions that can be applied cleanly.

Stalled lanes clustered where closure required:
- a new structural bridge,
- heavy machinery composition with subtle quantifiers,
- or theorem-level upgrades from high-quality finite evidence.

This pattern supports the need for escalation and strict claim-tier separation.

## 9. Implication for claim policy

The correct policy is:
- keep `proved / cited / empirical` separation strict,
- keep escalation logs explicit,
- treat parked/candidate states as valid scientific outputs when blockers are precise and reproducible.

This is a strength, not a weakness: it avoids result laundering and preserves high-value failure information.

## 10. If pushing beyond the current boundary

Likely required improvements include:
- domain-adaptive fine-tuning on adjacent theorem families,
- stronger theorem-retrieval with structural matching,
- symbolic search/formal-method coupling (Lean/SMT/CAS),
- or neural-symbolic hybrid planning for theorem-space exploration.

Workflow improvements alone are unlikely to close every remaining lane.

## 11. Takeaway

For this project, escalation was necessary for reliability and rigor, but insufficient for full closure in all domains.

The key finding is not "some references were missing." The stronger finding is:
- current general LLM orchestration handles deep application of known structure well,
- but remains limited on problems requiring new structural glue under strict autonomy constraints.

## 12. Prompt Equivalency Note (Documentation Heuristic)

For reporting-only interpretation of orchestration effort, this repo uses a rough mapping:

- `1` agent-orchestration prompt ~= `10` llm-only prompts
- typical split: `8` short prompts + `2` long prompts

This is a planning/documentation heuristic, not an empirical benchmark.
Primary accounting remains token and message logs in `RESULTS.md` and per-lane transcripts/audits.



======================================================================
SOURCE: CONTAMINATION.md
======================================================================

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
| C12 | P01 | Barashkov-Gubinelli (2021), arXiv:2004.01513 | **CITE_PLUS** (upgraded from CITE_ONLY at E11): Theorem 1-3, Corollaries 1-2, Lemmas 1-6 proof structure. Proof chain traced: drift equation (Eq. 13), stochastic objects (Table 1: W, W², W³), paracontrolled decomposition. All 6 lemmas verified to extend to V_c via (α) quartic coercivity + (β) UV scaling. | CITE_PLUS | P01 E7 (CITE_ONLY), **E11 (CITE_PLUS)** |
| C13 | P01 | Bogachev (1998), *Gaussian Measures* | Training-knowledge: Cameron-Martin theorem for GFF quasi-invariance under H¹ translations | TRAINING | P01 E5 |
| C14 | P01 | Hairer-Steele (2021), arXiv:2102.11685, J. Stat. Phys. 2022 | Statement-level: Φ⁴₃ measure has sub-Gaussian tails, E_μ[exp(c∫:φ⁴:)] < ∞ for small c > 0 | CITE_ONLY | P01 E11 |
| C15 | P01 | Barashkov-Gubinelli (2020), arXiv:1805.10814, Duke Math J. 2020 | Proof-level: variational method for Φ⁴₃ (Boué-Dupuis formula framework) | CITE_PLUS | P01 E11 |
| C16 | P01 | Barashkov-Gubinelli (2022), arXiv:2112.05562 | Statement-level: variational method extends to P(φ)₂ theories (general polynomial potentials) | CITE_ONLY | P01 E11 |
| C17 | P03 | Alexandersson-Sawhney (2019), arXiv:1801.04550, Annals of Combinatorics 23:219–239 | Statement-level (abstract only): E_λ(x;1,t) symmetric and t-independent for partitions λ. Hecke extension derived. Author correction from prior misattribution. | CITE_ONLY | P03 E13 |

## Scout model deployments (no web search, no solution retrieval)

| row_id | Problem | Provider/Model | Purpose | Exposure risk | Escalation event |
|--------|---------|---------------|---------|--------------|-----------------|
| S1 | P10 | GPT-5.2-pro | Initial candidate solution (solvability evaluation) | NONE (LLM reasoning only) | P10 E1 |
| S2 | P03 | groq/gptoss120b, fw/kimi-instruct, fw/deepseek-v3p2 | Symmetry Conjecture closure routes | NONE (3 scouts, no consensus) | P03 E6 |
| S3 | P03, P04, P05 | Fireworks/qwen3-coder-480b-a35b-instruct | Failure-conditioned scout packets for P03, P04, P05. Received proposed approaches only. No solution content, no problem statements from competition, no citations used. Pure brainstorming output. | NONE (LLM reasoning only) | P03 E14, P04 E-scout, P05 E-scout |
| S4 | P03, P04, P05 | Fireworks/deepseek-r1-0528 | Failure-conditioned scout packets for P03, P04, P05. Same as S3: proposed approaches only, no solution content, no competition problem statements, no citations used. Pure brainstorming output. | NONE (LLM reasoning only) | P03 E14, P04 E-scout, P05 E-scout |
| S5 | P03, P04, P05 | Fireworks/kimi-k2p5 | Failure-conditioned scout packets sent but responses truncated (thinking model, 4096 token limit). No usable content received. | NONE (truncated, no content) | P03 E14, P04 E-scout, P05 E-scout |
| S6 | P03, P04, P05 | Groq/qwen3-32b | Round 1 scouts, partially truncated. Some reasoning but no solution content. | NONE (partially truncated, no solution content) | P03 E14, P04 E-scout, P05 E-scout |
| S7 | P03, P04, P05 | Fireworks/qwen3-235b-a22b-instruct-2507 | Round 1 scouts, some proposals received. No solution content, no competition problem statements. | NONE (LLM reasoning only) | P03 E14, P04 E-scout, P05 E-scout |

## Search log
| Timestamp | Query | Purpose | Exposure risk |
|-----------|-------|---------|--------------|
| 2026-02-11 | WebFetch ar5iv.labs.arxiv.org/html/1309.1750 | P05 definition extraction (BH N∞ operad) | NONE (definition-only, primary source) |
| 2026-02-11 | WebFetch ar5iv.labs.arxiv.org/html/1903.08723 | P05 definition extraction (Rubin transfer systems) | NONE (definition-only, primary source) |
| 2026-02-11 | WebFetch ar5iv.labs.arxiv.org/html/1703.10526 | P05 definition extraction (HY slice connectivity) | NONE (definition-only, primary source) |
| 2026-02-12 | WebFetch ar5iv.labs.arxiv.org/html/2004.01513 (×3) | P01 CITE_ONLY ingest: BG (2020) Theorems 1-3, Corollaries 1-2 | NONE (theorem statements only, primary source) |
| 2026-02-12 | WebFetch/WebSearch ar5iv + arxiv.org (×8+) | P01 R1 CITE_PLUS: BG proof chain (Lemmas 1-6, Table 1, Eq. 13, paracontrolled structure) | NONE (proof structure, primary source, no solutions to competition problem) |
| 2026-02-12 | WebSearch "Hairer Steele sub-Gaussian Phi43" | P01 R1: Hairer-Steele (2102.11685) sub-Gaussian tails result | NONE (published result, primary source) |
| 2026-02-12 | WebFetch arxiv.org/abs/2102.11685 | P01 R1: Hairer-Steele abstract extraction | NONE (abstract only, primary source) |
| 2026-02-12 | WebFetch arxiv.org/abs/1805.10814 | P01 R1: BG variational method abstract/structure | NONE (primary source) |
| 2026-02-12 | WebFetch arxiv.org/abs/2112.05562 | P01 R1: BG P(φ)₂ extension abstract | NONE (abstract only, primary source) |
| 2026-02-12 | WebFetch ar5iv/1801.04550 + arxiv.org/abs/1801.04550 + arxiv.org/pdf/1801.04550 + link.springer.com + symmetricfunctions.com (×5) | P03 R1: Alexandersson-Sawhney (2019) non-symmetric Macdonald at q=1. Abstract extracted; PDF/HTML unreadable. | NONE (abstract only, primary source, no competition solution) |

## Exposure events
None.

## Statement
We did not incorporate any externally found solutions into our proofs.



======================================================================
SOURCE: common/definition_only_escalation.md
======================================================================

# Definition-Only Reference Escalation Protocol

## Purpose

Enable re-opening of parked problems (P01, P02, P05, P07, P08) without breaking
llm-only hygiene, by ingesting only definitions, notation, and theorem statements
from primary sources.

## Scope-limited ingest rules

### ALLOWED (CITE_ONLY)
- Definitions and notation from original papers/books
- Theorem/lemma/proposition **statements** (with numbering)
- Hypothesis blocks (conditions under which a result holds)
- Object type signatures (e.g., "E*_mu is a polynomial in x1,...,xn with coefficients in Q(q,t)")

### NOT ALLOWED
- Proof sections or proof sketches
- Commentary, motivation, or "how to apply this" discussion
- Blog posts, surveys, or secondary summaries (primary-source only)
- Any text that reveals or hints at solutions to First Proof questions

## Protocol

### Step 1: Producer identifies source
- Producer locates the specific paper/book for a blocked dependency.
- Producer identifies the exact section containing the needed definition/statement.

### Step 2: Producer extracts verbatim text
- Producer copies ONLY the definition/statement text (verbatim, no paraphrasing).
- Producer does NOT read or relay proof sections.
- Producer does NOT provide interpretation or guidance on how to use the result.

### Step 3: Quarantine logging
For each imported item, log in BOTH:
- `CONTAMINATION.md`: source, section, what was extracted, exposure risk
- `PXX/audit.md`: tagged as `CITE_ONLY` or `PROVE_INLINE`

Format:
```
| Timestamp | Source | Section | Item type | Tag | Exposure risk |
|-----------|--------|---------|-----------|-----|---------------|
| YYYY-MM-DD | Author (Year), Title | Def 3.1 | Definition | CITE_ONLY | LOW |
```

### Step 4: Hypothesis-check gate
- Claude/Codex MUST explicitly verify all hypotheses before using any cited statement.
- If hypotheses cannot be verified from available information, treat as unresolved
  dependency and keep parked.
- No "well known" claims without CITE_ONLY or PROVE_INLINE tag.

### Step 5: Hard contamination fail-safe
- If proof/solution text for ANY First Proof question is accidentally seen:
  1. IMMEDIATELY freeze that problem lane
  2. Log the exposure in CONTAMINATION.md with full details
  3. Mark the problem as CONTAMINATED — do NOT incorporate any content
  4. Continue only if the exposed content is unrelated to the solution path

## Priority order for escalation

Based on tractability assessment from RED-feasibility blitz:

| Priority | Problem | What's needed | Est. definitions to ingest |
|----------|---------|---------------|---------------------------|
| 1 | P08 (Symplectic) | Polyhedral Lagrangian smoothing, tropical-Lagrangian correspondence | 3-5 definitions from Matessi, Mikhalkin |
| 2 | P07 (Lattices) | Q-Poincare duality for groups with torsion, surgery obstruction theory | 3-4 definitions from Davis, Wall, Luck |
| 3 | P01 (Stochastic) | Phi^4_3 construction, variational framework, :phi^3: integrability | 4-6 definitions from Barashkov-Gubinelli |
| 4 | P02 (Rep theory) | Essential Whittaker functions, conductor theory, modified RS integrals | 5-8 definitions from JPSS, Matringe |
| 5 | P05 (Eq. homotopy) | N-infinity operads, incomplete transfer systems, O-slice filtration | 6-10 definitions from Blumberg-Hill |

## Expected yield

- P08: HIGH — concrete objects, local smoothing construction likely follows from definitions
- P07: MEDIUM — Q-PD + surgery theory could close with 2-3 key definitions
- P01: MEDIUM — core question (exp(int :phi^3: psi) in L^1) may resolve with variational bounds
- P02: LOW-MEDIUM — deep automorphic forms; definitions alone may not suffice
- P05: LOW — open-ended formulation; definitions needed even to STATE the answer

## Human intervention classification

All definition-only ingests are classified as LOGISTICS (verbatim relay of published
definitions, no mathematical interpretation by producer).



======================================================================
SOURCE: common/claude_handoff_checklist.md
======================================================================

# Producer -> Claude Checklist (Standard Handoff)

Use this checklist at the start of every new problem and at each gate transition.
Goal: maximize throughput, prevent rewrite loops, and keep artifacts publishable.

## 0) Handoff Header (always include)

- Problem ID and domain.
- Current date/time (PT) and remaining sprint window.
- Message budget for this problem (hard cap).
- Current gate target (start at G0 unless resuming).
- Current status target options: `✅` / `🟡` / `📊` / `❌`.
- Contamination mode reminder (llm-only unless explicitly relaxed).

## 1) Immediate Work Plan Request

Ask Claude to return a compact execution plan before deep work:

- Gate sequence to run now.
- Expected message spend per gate.
- Stop-loss trigger for each gate.
- Exact artifacts to update (`answer.md`, `audit.md`, `transcript.md`, `experiments/`).

## 2) Gate-by-Gate Execution Checklist

## G0 Formalize (hard cap: 10 messages)

- Explicit quantifiers (`forall`, `exists`, order).
- Full symbol/type glossary.
- Precise YES/NO restatement.
- Counterexample shape (concrete falsifier template).
- Truth mode selected (`PROVE`, `DISPROVE`, or `EXPLORE BOTH`) with rationale.

Pass condition:
- No hidden assumptions.
- Ambiguities listed as open dependencies.

## G1 Background (hard cap: 15 messages)

- Prerequisite list complete.
- Each dependency tagged:
  - `PROVE_INLINE`
  - `CITE(statement number required)`
  - `NEEDS_SOURCE`
- If `NEEDS_SOURCE > 3`, stop and park or switch problem.

Pass condition:
- No "well known" claims without source or proof.

## G2 Route Map (hard cap: 15 messages)

- At least 2 distinct routes (not cosmetic variants).
- Each route includes:
  - lemma chain
  - bottleneck lemma
  - failure conditions
- YES/NO problems must include a counterexample track.

Pass condition:
- Chosen route is justified against alternatives.

## G3 Lemma DAG

- Every lemma has precise statement + acceptance test.
- No circular dependencies.
- Explicit map from lemmas -> final claim.

Pass condition:
- No "then result follows" gap.

## G4 Experiments (hard cap: 15 messages)

- Reproducible scripts (seed/version/tolerance).
- Adversarial test cases, not only random easy cases.
- Numerical stability checks (precision escalation near boundary).
- Edge-case coverage (degenerate/nullspace/disconnected/etc. as relevant).

Pass condition:
- Experiments test the exact claim, not a proxy.

## G5 Proof Draft (hard cap: 40 messages)

- Every nontrivial step justified.
- All theorem hypotheses checked explicitly.
- Quantifier scope verified line-by-line.
- Boundary cases handled explicitly.
- Claim level matches evidence level (do not overclaim).

Pass condition:
- Draft is internally coherent and citation-complete.

## G6 Reviewer Readiness Package

- Prepare concise relay summary for reviewer:
  - what is fully proved
  - what is only empirical
  - known gaps and risk flags
- Include explicit "key questions for reviewer to attack".

Pass condition:
- Reviewer can falsify/test quickly without extra context hunting.

## G7 Package

- `answer.md` self-contained.
- `audit.md` includes full gate history and patch cycles.
- `transcript.md` complete enough for reconstruction.
- `README.md` and `RESULTS.md` status rows updated.
- Commit with clear status label in message.

Pass condition:
- Repo reflects true state without overclaim.

## 3) Stall / Park Rules (always enforce)

- If no new lemma closure or experimental signal in 10 messages:
  - force route change once.
- If still stalled after route change:
  - park as `📊` or `❌` and move on.
- Never spend more than cap trying to "polish" a stuck proof.

## 4) Token + Prompt Logging Requirement

Require Claude to append/update in `audit.md` at every gate:

- Estimated messages used / budget.
- Estimated token usage so far.
- New scripts run and outputs produced.
- Net progress since last checkpoint (what closed, what remains).

If logging is missing, pause progression until logs are updated.

## 5) Standard Closing Ask to Claude

At the end of each working block, require:

- Current status recommendation (`✅` / `🟡` / `📊` / `❌`).
- Top 3 unresolved risks.
- Exact next action with estimated message cost.



======================================================================
SOURCE: common/definition_shopping_list.md
======================================================================

# Definition-Only Unblocking Queue (Claude Prep)

Generated: 2026-02-11  
Protocol: `common/definition_only_escalation.md`

This file is the single low-noise prep artifact for unsolved lanes.
Use it to dispatch Claude immediately when available.

## 0. Hygiene rules (mandatory)

- Ingest **statements only**: definitions, theorem statements, hypotheses, notation.
- Do **not** ingest proof text, proof sketches, survey commentary, or blog summaries.
- Primary sources only (journal/arXiv/book originals).
- Every ingest must be logged in both:
  - `CONTAMINATION.md` (row with source/section/tag/risk)
  - `PXX/audit.md` (Escalation Ledger event + dependency tag)
- If accidental direct-solution exposure occurs: freeze lane and log contamination.

## 1. Current unsolved lanes (canonical)

| Problem | Status | Bottleneck type | Priority |
|---------|--------|-----------------|----------|
| P05 | 🟡 Candidate | Proof gap (orbit-counting "only if"); definitions resolved | 5 (done this cycle) |
| P01 | 🟡 Candidate | Proof complete (conditional on BG stability extension from training knowledge); upgrade path: CITE_ONLY ingest of BG (2020) `thm:equicoerc` | 2 |
| P09 | 📊 Conjecture | Algebraic formalization gap | 3 |
| P04 | 🟡 Candidate | n>=4 theorem gap | 4 |
| P03 | 🟡 Candidate | n>=4 closure still open | 5 |

## 2. Immediate queue for Claude (gate-scoped)

### Q1. P05 re-open (G1 only, definition unlock)

- Cap: 25 messages.
- Goal: produce a precise candidate definition of O-adapted slice filtration with explicit dependency tags.
- Must output:
  - `P05/audit.md`: G1 refresh + Escalation row with citations.
  - `P05/transcript.md`: ingest provenance and rejected/accepted statements.
  - `P05/answer.md`: no theorem claim; definition candidates only unless fully closed.
- Stop condition:
  - If canonical O-adapted definition remains ambiguous after two candidate formulations, keep `❌ Parked`.

### Q2. P01 re-open (G1->G2 dependency closure check)

- Cap: 20 messages.
- Goal: resolve whether existing primary statements suffice to advance Route A without overclaim.
- Must output:
  - `P01/audit.md`: updated dependency ledger (resolved/unresolved).
  - `P01/transcript.md`: exact statement references used.
  - `P01/answer.md`: keep uncertainty explicit if any core theorem is still unresolved.
- Stop condition:
  - If deterministic shift quasi-invariance statement is still missing, keep `❌ Parked`.

### Q3. P09 closure prep (no new docs, no status upgrade by numerics alone)

- Cap: 30 messages.
- Goal: target only algebraic formalization tasks from existing experiments.
- Must output:
  - `P09/audit.md`: exact remaining formalization claims and pass/fail checks.
  - `P09/transcript.md`: independent check record.
- Stop condition:
  - If only empirical strengthening is added, status remains `📊`.

### Q4. P04 closure prep (n>=4 triage)

- Cap: 35 messages.
- Goal: bounded route test for n>=4 only; no rewrite loops.
- Must output:
  - `P04/audit.md`: route verdict with explicit blocker theorem.
  - `P04/transcript.md`: verification scripts and outcomes.
- Stop condition:
  - If no theorem closure and no verified counterexample, remain `🟡`.

### Q5. P03 monitoring prep (n>=4 hygiene checks)

- Cap: 15 messages for review cycle.
- Goal: enforce theorem-vs-empirical separation for n>=4 claims.
- Must output:
  - `P03/audit.md`: checklist results (degree-bound applicability, pole safety, modular consistency).

## 3. Minimal-contamination reference packet (statement targets only)

## P05 core references

1. Blumberg-Hill (2015), *Operadic multiplications in equivariant spectra, norms, and transfers*  
   URL: https://arxiv.org/abs/1309.1750  
   Extract only:
   - `Definition` of N-infinity operad (`def:geinfop`)
   - `Definition` of indexing system
   - `Definition` of admissible H-set
   - Main theorem mapping operads to indexing systems

2. Rubin (2019), *Characterizations of equivariant Steiner and linear isometries operads*  
   URL: https://arxiv.org/abs/1903.08723  
   Extract only:
   - `defn:indsys` (indexing system)
   - `defn:transys` (transfer system)
   - `thm:transys` (equivalence indexing systems <-> transfer systems)
   - `cor:transysBH2` (transfer systems <-> indexing categories)

3. Hill-Yarnall (2017), *A new formulation of the equivariant slice filtration...*  
   URL: https://arxiv.org/abs/1703.10526  
   Extract only:
   - theorem characterizing slice n-connectivity via geometric fixed points (`thm:GeomFPVersion`)
   - statement-level definitions of slice-connective categories used by that theorem

## P01 core references

1. Barashkov-Gubinelli (2018), *A variational method for Phi^4_3*  
   URL: https://arxiv.org/abs/1805.10814  
   Extract only:
   - main variational theorem (`th:main`)
   - Boue-Dupuis variational theorem statement (`th:variational`)
   - statement defining the limiting measure / Laplace transform characterization

2. Barashkov-Gubinelli (2020), *The Phi^4_3 measure via Girsanov's theorem*  
   URL: https://arxiv.org/abs/2004.01513  
   Extract only:
   - theorem giving variational/Girsanov representation (`eq:th1`)
   - coercivity / integrability theorem (`thm:equicoerc`)
   - statement-level absolute-continuity result wrt drift measure
   - statement-level singularity result wrt Gaussian free field (for route sanity check)

## 4. Dispatch-ready checklist (paste into Claude handoff)

1. Run `G0/G1` for target lane with stop-loss cap from Section 2.
2. Use only references in Section 3 and extract statement-level text only.
3. Update artifacts: `answer.md`, `audit.md`, `transcript.md`.
4. Add message/token delta and escalation event row in `audit.md`.
5. Return one of: `proceed`, `park`, `escalate`.

## 5. Required logging row format

Use this row format in `CONTAMINATION.md` and in `PXX/audit.md`:

`| timestamp | source | section/label | item_type | tag(CITE_ONLY) | exposure_risk | used_for |`



======================================================================
SOURCE: AUTHORS
======================================================================

Joshua Butler <josh.d.butler@gmail.com>

Project lead and repository author.

