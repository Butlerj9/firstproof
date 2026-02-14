# Workflow Adjustment Impact Analysis (2026-02-14)

## Executive Summary

This memo estimates how much accuracy could improve under specific workflow changes, assesses whether the system diverged after earlier convergence, and identifies premise-safe interventions (no human mathematical input, no direct-solution retrieval).

Baseline (from current comparison audit):

- Strict theorem-level alignment: `30%-40%` (`3/10` to `4/10`, pending P06)
- Directional alignment: `60%-70%` (`6/10` to `7/10`, pending P06)
- Risk-adjusted alignment: `47.5%-57.5%` (neutral midpoint `52.5%`)

Main result:

- The highest-yield changes are `statement lock + contradiction gate + mandatory post-convergence re-evaluation`.
- Estimated strict-alignment uplift from these controls is approximately `+20 to +40` percentage points (scenario-dependent), with directional alignment likely rising into the `70-90%` range.

---

## 1. Counterfactual Estimation Method

We use lane-level counterfactual flips:

1. Identify lanes where root cause was process-controllable (not theorem difficulty).
2. Map each control to lanes it plausibly corrects.
3. Estimate conservative and aggressive correction ranges.

Process-controllable high-impact lanes:

- `P07`, `P08` (formalization/definition/polarity control failures)
- `P01` (closure promotion without contradiction hardening)
- `P05` (normalization debt; consistency, not theorem sign)
- `P03` (time/allocation planning rather than pure theorem impossibility)
- `P06` (quantifier-form adjudication and statement-lock governance)

---

## 2. Estimated Impact by Workflow Adjustment

| Adjustment | Primary lanes affected | Expected strict uplift | Expected directional uplift |
|---|---|---:|---:|
| Statement lock at G0 | P06, P07, P08 | +10 to +20 pts | +10 to +30 pts |
| Contradiction gate pre-✅ | P01, P06, P07, P08 | +10 to +20 pts | +10 to +20 pts |
| Post-convergence re-evaluation pass | P01, P08, P05, P03 | +5 to +15 pts | +5 to +15 pts |
| Early compute pre-provision policy | P03 | 0 to +10 pts | 0 to +10 pts |
| Final-form normalization check | P05 | 0 to +5 pts | 0 to +5 pts |

Notes:

- Uplifts are not additive without overlap correction.
- The largest non-overlapping uplift comes from statement lock plus contradiction gate.

---

## 3. Scenario Estimates

## 3.1 Conservative scenario

Assume only one or two conflict lanes are corrected by improved controls.

- Strict alignment: `30% -> 40-50%`
- Directional alignment: `60% -> 70-75%`

## 3.2 Moderate scenario

Assume corrected formalization/polarity handling on most process-driven conflicts.

- Strict alignment: `30% -> 50-70%`
- Directional alignment: `60% -> 75-90%`

## 3.3 Aggressive scenario

Assume full control adherence plus successful P03 compute execution in-window.

- Strict alignment: `30% -> 70-80%`
- Directional alignment: `60% -> 85-95%`

---

## 4. Were We Closer Earlier, Then Forced to Diverge?

Short answer: in several lanes, yes, there are signs of convergence to a safer state (candidate/blocked/ambiguous), followed by closure pressure and divergence.

Patterns:

1. **Premature closure after internal convergence**.
   - Some lanes moved from uncertainty to strong closure claims without a final contradiction-hardened pass.

2. **Policy-induced directional lock-in**.
   - Counterexample-first and patch cycles can lock to a polarity once a coherent route exists, even if the route solves a shifted statement.

3. **Definition repair by reinterpretation**.
   - In at least one lane, patching a proof gap was achieved by tightening definition semantics, which may have shifted the target statement.

4. **Late-stage reevaluation deficit**.
   - After convergence was documented, not all lanes had a mandatory "opposite-sign challenge" before final status.

Interpretation:

- Divergence did not require malicious behavior; it can emerge from optimization pressure under short deadlines.

---

## 5. Was Reevaluation After Convergence Sufficient?

No. Reevaluation was strong on local proof defects but weaker on global theorem-polarity reconciliation.

What was done well:

- Adversarial patch cycles caught many local logical flaws.
- Numerical/script verification improved internal consistency.

What was missing:

1. Mandatory contradiction pass after provisional closure.
2. Mandatory quantifier-equivalence check against statement lock.
3. Mandatory dual-track adjudication for sign-critical YES/NO lanes.
4. Mandatory final normalization scan to remove stale mixed-status sections.

---

## 6. What Could Have Changed Without Violating the Premise?

All changes below preserve the premise (no human mathematical ideas; no direct-solution retrieval).

1. **Statement lock at G0** (agent-authored, reviewer-approved).
2. **Contradiction gate at G6/G7** (agent-run checklist).
3. **Blind opposition pass**:
   - A separate agent must attempt to prove the opposite sign using the same locked statement.
4. **Post-convergence re-evaluation protocol**:
   - Freeze current solution, then run independent re-derivation from scratch by a different model family.
5. **Early compute provisioning rule**:
   - If projected serial runtime exceeds threshold, auto-escalate to parallel execution plan.
6. **Final-form normalization lint**:
   - Scripted scan before release to prevent mixed historical/final statuses.

None of these require human theorem steering. They are policy and tooling controls.

---

## 7. Recommended Minimal Change Set (Next Iteration)

If only three changes are adopted:

1. Statement lock (`PXX/statement_lock.md`) at G0.
2. Contradiction gate (`common/contradiction_gate_checklist.md`) before `✅`.
3. Mandatory post-convergence opposition pass (one independent model family).

Expected benefit:

- Largest practical reduction in sign conflicts and statement-drift failures while preserving autonomy constraints.

---

## 8. Closure Cost and Throughput Economics

### 8.1 Cost model

For planning purposes, define:

- `C_setup`: fixed setup and governance cost,
- `C_exec`: execution cost across lanes (compute + operator),
- `C_debt`: correction debt from wrong-sign or drifted closures.

Then:

`C_total = C_setup + C_exec + C_debt`.

The post-mortem indicates that reducing `C_debt` is the highest-leverage objective; wrong-sign closures are substantially more expensive to unwind than preventing them.

### 8.2 Accelerator impact ranges (planning estimates)

| Accelerator | Throughput impact | Strict-accuracy impact | Relative cost |
|---|---:|---:|---|
| Statement lock + contradiction gate + opposition pass | +5% to +25% | +20 to +40 pts (overlap-adjusted scenarios) | Low |
| Solver preflight + retry policy | +10% to +30% on compute lanes | +0 to +10 pts | Low-medium |
| Parallel compute scheduling | +20% to +200% on eligible lanes | +0 to +10 pts | Medium |
| Curated lemma retrieval layer | +20% to +100% | +10 to +30 pts | Medium-high |
| Training-enhanced verifier stack | +10% to +50% | +10 to +30 pts | High |

### 8.3 Upgrade bands for a high-throughput research accelerator

| Upgrade band | One-time effort | Run-time cost | Expected outcome band |
|---|---:|---:|---|
| Governance-only hardening | ~40-120 hours | Minimal | Strong reduction in polarity/formalization failures |
| Governance + compute orchestration | ~120-320 hours | ~$300-$3,000 per heavy run | Faster closure on heavy computational lanes |
| Governance + compute + curated retrieval | ~300-900 hours | ~$1,000-$10,000/month | Transition to stable high-throughput portfolio workflow |

Interpretation:

1. The first investment tier is inexpensive and has high defensive value.
2. Large throughput gains require orchestration and scheduling maturity.
3. Sustained high strict-closure rates require corpus quality and verifier discipline, not just larger raw model usage.

---

## 9. Operational Conclusion

The principal optimization target is the **harness/pipeline layer**:

1. Formalization and contradiction controls drive correctness.
2. Compute orchestration drives wall-clock closure on hard lanes.
3. Model quality determines the frontier ceiling, but orchestration determines whether that ceiling is reached in practice.

---

## 10. Domain-Normalized Multiplier Table (Calibrated on P01-P10)

This section answers whether acceleration estimates account for disparate mathematical domains. The table below is normalized by domain cluster using:

1. The 10-lane outcomes in `docs/results/solution_comparison_full_audit_2026-02-14.md`.
2. Per-lane resource intensity in `RESULTS.md` (messages/tokens/cost).
3. Observed failure modes from `docs/results/post_mortem_2026-02-14.md`.

These are planning ranges (not deterministic guarantees).

### 10.1 Domain clusters and observed alignment signal

| Domain cluster | Lanes | External-alignment signal in this run | Dominant failure mode |
|---|---|---|---|
| Computational linear algebra / tensor numerics | P09, P10 | Strong (`A`, `A`) | Mostly implementation-detail defects |
| Algebraic-combinatorial / finite free symbolic | P02, P03, P04 | Mixed (`A`, `C`, `C`) | All-`n` bridge lemma / methodology lock-in |
| Graph/spectral inequalities | P06 | Disputed (`F*`) | Quantifier form ambiguity |
| Geometry/topology/SPDE high-abstraction | P01, P05, P07, P08 | Weak-mixed (`F`, `B`, `F`, `F`) | Polarity errors, fabricated bridge steps, framework mismatch |

`F*` indicates a formally disputed lane pending quantifier-form adjudication.

### 10.2 Domain-normalized acceleration estimates

Amplification is reported versus an unaided baseline in the same domain.

| Domain cluster | Throughput multiplier (current harness) | Throughput multiplier (hardened + retrieval) | Strict-closure multiplier (current harness) | Strict-closure multiplier (hardened + retrieval) | Confidence |
|---|---:|---:|---:|---:|---|
| Computational linear algebra / tensor numerics | ~8x-20x | ~20x-60x | ~3x-8x | ~6x-18x | High |
| Algebraic-combinatorial / finite free symbolic | ~5x-12x | ~12x-35x | ~2x-5x | ~4x-10x | Medium |
| Graph/spectral inequalities | ~4x-10x | ~8x-20x | ~1.5x-4x | ~3x-8x | Low-Medium (disputed lane) |
| Geometry/topology/SPDE high-abstraction | ~3x-8x | ~6x-16x | ~1.2x-3x | ~2x-6x | Medium |

Interpretation:

1. Disparate domains materially change multiplier ceilings.
2. Numerics-heavy lanes exhibit the largest throughput and closure gains.
3. High-abstraction lanes gain less from raw orchestration and more from contradiction controls plus theorem-retrieval quality.
4. The hardest residual gap remains novel bridge-invariant discovery (especially in geometry/SPDE/topology lanes).

### 10.3 Per-lane normalized planning table

| Lane | Domain | Throughput multiplier range | Strict-closure multiplier range | Primary lever |
|---|---|---:|---:|---|
| P01 | Stochastic analysis | ~3x-8x | ~1.2x-3x | Contradiction gate + formal-check bridge |
| P02 | Representation theory | ~5x-12x | ~2x-6x | Theorem retrieval + citation discipline |
| P03 | Algebraic combinatorics | ~5x-14x | ~1.5x-4x | Parallel compute + structural route diversity |
| P04 | Finite free convolution | ~6x-16x | ~2x-6x | Method-family switch trigger + retrieval |
| P05 | Equivariant homotopy | ~4x-10x | ~1.5x-5x | Final-form normalization + contradiction gate |
| P06 | Spectral graph theory | ~4x-10x | ~1.5x-4x | Quantifier lock + opposition pass |
| P07 | Lattices in Lie groups | ~3x-8x | ~1.2x-3x | External adversarial review mandatory |
| P08 | Symplectic geometry | ~3x-8x | ~1.2x-3x | Framework-constrained route checks |
| P09 | Tensor polynomial map | ~8x-20x | ~3x-8x | Modular verification + compute orchestration |
| P10 | Numerical multilinear algebra | ~10x-24x | ~4x-10x | Deterministic verification loops |

### 10.4 Portfolio-level synthesis under domain normalization

Using this domain-adjusted view, portfolio-level uplifts from Sections 3 and 8 remain directionally valid, but are best interpreted as weighted blends:

1. Global throughput estimates are dominated by numerics-heavy lanes.
2. Global strict-closure estimates are constrained by high-abstraction lanes.
3. The correct planning strategy is mixed: maximize fast closure in high-yield domains while running stricter contradiction controls in high-abstraction domains.
