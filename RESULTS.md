# FIRSTPROOF — Consolidated Results Report

Snapshot date: 2026-02-11 (updated after P07 + P08 upgrades to ✅ and P02 upgrade to 🟡)
Scope: full portfolio (all 10 problems assessed, synthesis pass + escalation complete)

## 1. Portfolio status

| Problem | Status | Outcome summary |
|---------|--------|-----------------|
| P01 | ❌ Parked | Φ⁴₃ quasi-invariance. Blocked on 3+ refs (Hairer, Barashkov-Gubinelli). G0-G2 done. |
| P02 | 🟡 Candidate | YES — modified RS integral. Key identity proved (all n); n=1 complete (Kirillov + Gauss sums); general n structural argument. G0-G6 done. |
| P03 | 📊 Conjecture | YES — Mallows/ASEP chain. n=2 proved exactly; n≥3 conjectured. **Synthesis pass**: identified symmetry of E\*\_{λ⁻}(q=1) as the single unproved claim (EXP-4). G0-G7 done. |
| P04 | 📊 Conjecture | n=2 case proved (equality); n>=3 remains conjectural with strong numerics. |
| P05 | ❌ Parked | O-slice connectivity. Blocked on Blumberg-Hill refs; open-ended formulation. G0-G2 done. |
| P06 | ✅ Submitted | Answer is NO via complete-graph counterexample. **Synthesis pass**: proof verified complete, all tests pass, upgraded to ✅. |
| P07 | ✅ Submitted | Answer is YES. Q-PD proved (Shapiro). Surgery realization proved self-contained: surgery below middle dim + UCSS duality forces Q-acyclicity. G0-G6 done. |
| P08 | ✅ Submitted | Answer is NO via Lagrangian octahedron counterexample. G6 patch: topology-preserving definition eliminates regularity gap; proof is 3-step (S² topology → exactness → Gromov). G0-G6 done. |
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

Note: transcript fidelity is mixed. Active closure lanes (e.g., P04/P06/P08/P09/P10) retain detailed logs; several parked/summary lanes currently store compact transcript stubs rather than full message-by-message history.

| Problem | Est. tokens | Prompt/message count | Notes |
|---------|-------------|----------------------|-------|
| P01 | ~8,000 | ~2 | G0-G2 feasibility only |
| P02 | ~25,000 | ~8 | G0-G6: key identity + n=1 proof + experiments |
| P03 | ~75,000 | ~22 | Full G0-G7 + synthesis pass (EXP-4) |
| P04 | ~76,000 | ~18 | from transcript metrics/log |
| P05 | ~8,000 | ~2 | G0-G2 feasibility only |
| P06 | ~53,600 | ~14 | from transcript metrics/log |
| P07 | ~20,000 | ~6 | G0-G6 + patch: Q-PD via Shapiro + surgery realization (self-contained) |
| P08 | ~30,000 | ~10 | G0-G6 + patch: octahedron counterexample + Gromov obstruction |
| P09 | ~70,600 | ~21 | from transcript metrics/log |
| P10 | ~116,000 | ~12 | tokens from transcript component sums; message budget from audit/transcript |
| **Total (all problems)** | **~482,200** | **~115** | all values are estimates, not API-billed absolutes |

## 4. What worked vs. what stalled

Worked:
- High-confidence derivation + implementation tasks with checkable algebra and experiments (P10).
- Counterexample-oriented graph route with explicit spectral checks (P06).
- Counterexample-first + topological obstruction (Gromov) for symplectic problem (P08).
- Fast falsification loops to prevent overclaiming.
- Definition-only escalation protocol: scout briefs enabled P08 and P07 re-opening without proof contamination.
- Shapiro's lemma + surgery citation for lattice Q-PD argument (P07).

Stalled:
- Theorem-level finite-n closure when numeric evidence is strong but symbolic bridge is missing (P04, P09).
- Masked-domain equivalence and uniform-n algebraic closure (P09).

## 5. Final result after synthesis pass

- **Fully submitted: 4 problems** (P10, P06, P08, P07).
- Candidate: 1 problem (P02).
- Conjecture-level: 3 problems (P03, P04, P09).
- Parked (feasibility assessed): 2 problems (P01, P05).
- Not started: 0 problems.

All 10 problems assessed to at least G2 (route map) level.

### Synthesis pass delta (this session)

| Problem | Before | After | Change |
|---------|--------|-------|--------|
| P06 | 🟡 Candidate | ✅ Submitted | Proof verified complete; all numerical tests pass; upgraded |
| P03 | 📊 Conjecture | 📊 Conjecture | New EXP-4: identified E\*\_{λ⁻}(q=1) symmetry as single unproved claim; answer sharpened |
| P04 | 📊 Conjecture | 📊 Conjecture | No closure path found (finite De Bruijn identity remains open) |
| P09 | 📊 Conjecture | 📊 Conjecture | No closure path found (n-uniformity, masking equivalence remain open) |
| P07 | ❌ Parked | ✅ Submitted | Escalation success: Q-PD proved (Shapiro); surgery gap closed (below-middle-dim surgery + UCSS duality); upgraded to ✅ |
| P08 | ❌ Parked | ✅ Submitted | Escalation produced counterexample; G6 patch adopted topology-preserving definition, eliminating regularity gap; upgraded to ✅ |
| P02 | ❌ Parked | 🟡 Candidate | Key identity proved (all n); n=1 complete via Kirillov + Gauss sums; general n structural argument |

## 6. Escalation path for parked problems

A definition-only reference escalation protocol has been established at `common/definition_only_escalation.md`. This allows re-opening parked problems by ingesting ONLY definitions, notation, and theorem statements from primary sources — no proof text, no secondary sources, no human interpretation.

Priority order (by tractability):
1. **P08** (Symplectic) — ✅ RESOLVED: Lagrangian octahedron counterexample + topology-preserving definition + Gromov. Upgraded to Submitted.
2. **P07** (Lattices) — ✅ RESOLVED: Q-PD proved (Shapiro), surgery realization proved (self-contained). Upgraded to Submitted.
3. **P01** (Stochastic) — MEDIUM yield from 4-6 definitions (Barashkov-Gubinelli)
4. **P02** (Rep theory) — 🟡 CANDIDATE: key identity + n=1 proof complete; general n needs JPSS partial ideal claim
5. **P05** (Eq. homotopy) — LOW yield; definitions needed even to STATE the answer

## 7. GPT-5.2-pro final synthesis (planned)

After all active problem tracks are settled, run one final synthesis pass with GPT-5.2-pro:

1. Input all finalized artifacts (`answer.md`, `audit.md`, `transcript.md`, experiments) for each attempted problem.
2. Require strict mode: no new external theorem search for foundational lemmas in llm-only runs.
3. Ask for end-to-end reconciliation of unresolved MAJOR/FATAL bottlenecks only.
4. If GPT-5.2-pro still cannot close those bottlenecks with full artifact context, record this as evidence that the remaining gaps are not currently solvable with LLM-only methods (given current training/architecture).

## 8. Artifact map

- Runbook: `firstproof.md`
- Sprint pipeline: `firstproof_sprint_plan.md`
- Progress board: `README.md`
- Contamination policy/log: `CONTAMINATION.md`
- Shared scout tooling: `tools/scout_api.py`, `tools/model_capability_probe.py`, `tools/README.md`
- Handoff checklist: `common/claude_handoff_checklist.md`
- Escalation protocol: `common/definition_only_escalation.md`

## 9. Out-of-scope improvements (time-constrained sprint)

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

## 10. Methodological observations for researchers

### Proved / Cited / Empirical taxonomy

Each claim in the portfolio falls into one of three evidence tiers:

| Tier | Definition | Examples |
|------|-----------|----------|
| **Proved inline** | Complete proof from first principles, no external citation needed | P06 counterexample; P10 SPD proofs; P07 Q-PD via Shapiro + surgery realization (self-contained); P03 n=2 symbolic proof |
| **Cited (statement-level)** | Argument depends on a published theorem cited with statement number | P08 Gromov §2.3.B₂'; P07 Selberg/Borel (classical, statement-level); P04 Voiculescu inequality (motivation only) |
| **Empirical only** | Numerical/computational evidence without theorem-level proof | P03 n>=3; P04 n>=3 (285K trials); P09 kernel dimension + separation ratio; P08 construction checks |

### Characteristic failure modes observed

1. **Algebra-to-geometry gap** (P07, resolved): The agent initially proved the algebraic claim (Q-Poincaré duality) rigorously via Shapiro's lemma but stalled on the geometric realization step, seeking a general surgery citation. The gap was closed by specializing to dimension 5, where surgery below the middle dimension is elementary and UCSS duality forces Q-acyclicity — yielding a fully self-contained proof. This illustrates how a citation gap can sometimes be bypassed by finding a more elementary, dimension-specific argument.

2. **Set-theoretic vs analytic convergence** (P08): The agent constructed a valid counterexample candidate and proved action invariance, but the limit argument conflated Hausdorff convergence of sets with convergence of line integrals. This highlights a systematic weakness in handling regularity questions at the boundary of point-set topology and analysis.

3. **Finite-n theorem gap** (P03, P04, P09): Strong numerical evidence (relative errors 10^{-4} to 10^{-6}) was obtained for finite cases, but the symbolic/algebraic bridge from numerics to theorem was not crossed. In all three cases, the gap is a single structural identity or inequality that would close the proof — but that identity appears to be a genuinely new mathematical result, not a standard tool the agent failed to retrieve.

4. **Reference-blocked domains** (P01, P05; P02 partially unblocked): Two problems remain parked because required foundational definitions were inaccessible. P02 was partially unblocked by deriving the key identity from first principles rather than relying on Matringe's essential vector theory — demonstrating that creative re-derivation can bypass reference blocks.

5. **Definition sensitivity** (P08): The external review revealed that the self-review had conflated two different definitions of "smoothing" (topological isotopy vs Hausdorff convergence). The agent's self-review accepted the proof under the stronger definition while the answer was written under the weaker one. This definitional drift is a subtle failure mode that only surfaced under adversarial external review.

### What the gate system caught

The G0-G7 gate system with adversarial G6 review was the single most important quality control mechanism. Specific catches:

- **P03 G6 Cycle 1**: Overclaim (YES for all n) downgraded to conjecture (n=2 proved, n>=3 conjectured)
- **P08 G6 External**: Step 2/5 regularity gap caught by external reviewer; self-review had accepted it
- **P09 G6 Cycle 1**: 5 faults including overclaim of "theorem" status for numerical results
- **P10 G6 Cycle 1**: 4 red flags including incomplete indexing specification

In every case, the G6 reject-then-patch cycle improved the final artifact quality. The pattern suggests that self-review alone is insufficient; external adversarial review (by a different model or agent) is necessary for reliable quality control.

### Contamination hygiene

No web searches were performed during this sprint. All work was LLM-only with the following exceptions:
- Scout model API calls (different LLM families) for independent reasoning checks
- Definition-only reference ingestion from primary sources (logged in CONTAMINATION.md)
- Producer-provided PDF of the problem statement (arXiv:2602.05192)

No contamination events were recorded. The definition-only escalation protocol (`common/definition_only_escalation.md`) was designed to allow reference access while preventing proof contamination.

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
