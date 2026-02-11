# FIRSTPROOF — Consolidated Results Report

Snapshot date: 2026-02-10 (updated after RED-feasibility blitz)
Scope: full portfolio (all 10 problems assessed)

## 1. Portfolio status

| Problem | Status | Outcome summary |
|---------|--------|-----------------|
| P01 | ❌ Parked | Φ⁴₃ quasi-invariance. Blocked on 3+ refs (Hairer, Barashkov-Gubinelli). G0-G2 done. |
| P02 | ❌ Parked | Rankin-Selberg nonvanishing. Blocked on automorphic forms refs (JPSS, Matringe). G0-G2 done. |
| P03 | 📊 Conjecture | YES — Mallows/ASEP chain. n=2 proved exactly; n≥3 conjectured with strong numerics. G0-G7 done. |
| P04 | 📊 Conjecture | n=2 case proved (equality); n>=3 remains conjectural with strong numerics. |
| P05 | ❌ Parked | O-slice connectivity. Blocked on Blumberg-Hill refs; open-ended formulation. G0-G2 done. |
| P06 | 🟡 Candidate | Answer is NO via complete-graph counterexample route; packaged and reviewed. |
| P07 | ❌ Parked | Lattices + Q-acyclic manifolds. Needs surgery theory (Wall, Davis). Q-PD route identified. G0-G2 done. |
| P08 | ❌ Parked | Lagrangian smoothing. Most tractable parked problem. Tropical-Lagrangian connection identified. G0-G2 done. |
| P09 | 📊 Conjecture | Candidate D=4 mechanism found numerically; theorem-level closure still open. |
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

| Problem | Est. tokens | Prompt/message count | Notes |
|---------|-------------|----------------------|-------|
| P01 | ~8,000 | ~2 | G0-G2 feasibility only |
| P02 | ~8,000 | ~2 | G0-G2 feasibility only |
| P03 | ~65,000 | ~18 | Full G0-G7 pipeline |
| P04 | ~76,000 | ~18 | from transcript metrics/log |
| P05 | ~8,000 | ~2 | G0-G2 feasibility only |
| P06 | ~53,600 | ~14 | from transcript metrics/log |
| P07 | ~8,000 | ~2 | G0-G2 feasibility only |
| P08 | ~8,000 | ~2 | G0-G2 feasibility only |
| P09 | ~70,600 | ~21 | from transcript metrics/log |
| P10 | ~116,000 | ~12 | tokens from transcript component sums; message budget from audit/transcript |
| **Total (all problems)** | **~421,200** | **~93** | all values are estimates, not API-billed absolutes |

## 4. What worked vs. what stalled

Worked:
- High-confidence derivation + implementation tasks with checkable algebra and experiments (P10).
- Counterexample-oriented graph route with explicit spectral checks (P06).
- Fast falsification loops to prevent overclaiming.

Stalled:
- Theorem-level finite-n closure when numeric evidence is strong but symbolic bridge is missing (P04, P09).
- Masked-domain equivalence and uniform-n algebraic closure (P09).

## 5. Final result at this stage

- Fully submitted: 1 problem (P10).
- Candidate-level: 1 problem (P06).
- Conjecture-level: 3 problems (P03, P04, P09).
- Parked (feasibility assessed): 5 problems (P01, P02, P05, P07, P08).
- Not started: 0 problems.

All 10 problems have been assessed to at least G2 (route map) level.

## 6. Final planned attempt (explicit)

After all active problem tracks are settled, run one final synthesis pass with GPT-5.2-pro:

1. Input all finalized artifacts (`answer.md`, `audit.md`, `transcript.md`, experiments) for each attempted problem.
2. Require strict mode: no new external theorem search for foundational lemmas in llm-only runs.
3. Ask for end-to-end reconciliation of unresolved MAJOR/FATAL bottlenecks only.
4. If GPT-5.2-pro still cannot close those bottlenecks with full artifact context, record this as evidence that the remaining gaps are not currently solvable with LLM-only methods (given current training/architecture).

## 7. Artifact map

- Runbook: `firstproof.md`
- Sprint pipeline: `firstproof_sprint_plan.md`
- Progress board: `README.md`
- Contamination policy/log: `CONTAMINATION.md`
- Shared scout tooling: `tools/scout_api.py`, `tools/model_capability_probe.py`, `tools/README.md`

## 8. Out-of-scope improvements (time-constrained sprint)

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
