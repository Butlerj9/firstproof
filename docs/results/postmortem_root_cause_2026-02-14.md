# Post-Mortem and Root-Cause Analysis (2026-02-14)

## Abstract

This report analyzes why portfolio outcomes diverged from the external First Proof solution packet on several lanes, and why some lanes remained partially closed. The central conclusion is that the largest failures were control-plane failures (problem formalization, claim validation, and escalation policy), not isolated coding or solver defects. No single actor is the principal fault point; the dominant causes are systemic.

For extended forensic analysis (retry timing, technical debt, ROI, and training-path recommendations), see `docs/results/post_mortem_2026-02-14.md`.

---

## 1. Scope and Method

### 1.1 Evidence base

The analysis uses:

- `P01/answer.md` ... `P10/answer.md`
- `P01/audit.md` ... `P10/audit.md`
- `RESULTS.md`
- `docs/results/solution_comparison_2026-02-14.md`
- `docs/results/solution_comparison_full_audit_2026-02-14.md`
- `external_solutions/text_clean/*.txt`
- `external_solutions/text_clean/FirstProofSolutionsComments.clean.txt`
- Git history (`git log`) for decision timing and status flips

### 1.2 Evaluation axes

For each lane, causes are decomposed across:

- `Model`: reasoning, theorem synthesis, citation interpretation
- `Agent`: implementer/reviewer claim discipline
- `Tooling`: solver/runtime/tool availability and diagnosis
- `Orchestration`: gating, escalation, route-switch policy
- `Workflow`: artifact hygiene, status consistency, documentation control
- `Time`: schedule and compute allocation constraints

---

## 2. Aggregate Findings

Using the full-audit scorecard:

- Strict theorem-level alignment: `3/10` (`30%`)
- Directional alignment (same YES/NO sign): `6/10` (`60%`)
- Risk-adjusted alignment: `47.5%`
- Critical sign conflicts: `4/10` (`P01`, `P06`, `P07`, `P08`)
- Partial-closure mismatches: `2/10` (`P03`, `P04`)

Interpretation:

1. The dominant failure mode was not "could not do math at all."
2. The dominant failure mode was "accepted wrong theorem polarity or wrong problem interpretation in a subset of lanes."
3. The second failure mode was "stopped at strong evidence / partial closure without final theorem-level closure."

---

## 3. Question-by-Question Forensic Analysis

### 3.1 P01

### Observed divergence

- External packet: negative (mutual singularity / lack of quasi-shift invariance).
- Repo: `YES` (`P01/answer.md:12`).

### Primary causes

- `Model`: citation-extension overreach from partial/adjacent results.
- `Agent`: accepted a synthesized extension as closure-grade.
- `Orchestration`: no hard contradiction gate against authoritative opposing theorem statement.

### Root cause

The lane crossed from "reference-assisted plausibility" into "closure claim" without an independent contradiction check against the canonical problem solution line.

### Fault attribution (lane-local)

- Model 35%, Agent 25%, Orchestration 25%, Workflow 10%, Time 5%

---

### 3.2 P02

### Observed divergence

- External packet and repo are aligned (`YES`).

### Residual risk (contained)

- Early failure risk (`W` depending on `\pi`) was known in external comments and appears to have been handled explicitly in repo proofs.

### Root cause status

No material failure. This lane is a positive control for the pipeline.

---

### 3.3 P03

### Observed divergence

- External packet: full positive theorem.
- Repo: partial closure (`n<=4`), open for `n>=5` (`P03/answer.md:3`).

### Primary causes

- `Time`: late lane start and cross-lane budget split.
- `Orchestration`: compute provisioning happened too late for the embarrassingly parallel `n=5` sweep.
- `Model`: no structural shortcut beyond computation found.

### Root cause

This was principally a time-allocation and execution-planning miss, not a solver impossibility:

- explicit estimate in audit (`P03/audit.md:553`, `P03/audit.md:568`)
- cloud-parallel route existed but was not executed in sprint window.

### Fault attribution (lane-local)

- Time 45%, Orchestration 30%, Model 20%, Tooling 5%

---

### 3.4 P04

### Observed divergence

- External packet: full finite-free Stam theorem (general `n`).
- Repo: strong `n=4` computational certification + `n>=5` conjectural.

### Primary causes

- `Tooling`: early false diagnosis ("solver unavailable/hanging") delayed effective route.
- `Orchestration`: prolonged route exploration before direct sparse/low-level solver path.
- `Time`: insufficient runway for full general-`n` bridge after n=4 closure effort.

### Root cause

A known internal correction documents the key misdiagnosis:

- `P04/audit.md:1056` (cvxpy compilation bottleneck, not solver failure).

This consumed high-value time before CLARABEL/SCS direct usage closed n=4 computational certificates.

### Fault attribution (lane-local)

- Tooling 30%, Orchestration 30%, Time 25%, Model 15%

---

### 3.5 P05

### Observed divergence

- Directionally aligned, but with internal consistency defects in artifact text.
- `answer.md` contains superseded open-state remnants despite top-level closure (`P05/answer.md:3` vs `P05/answer.md:301`, `P05/answer.md:694`).

### Primary causes

- `Workflow`: document consolidation debt (chronological log merged into final artifact without full normalization).
- `Agent`: stale-status pruning was incomplete.

### Root cause

Narrative accumulation without strict "final-form normalization" produced contradictory status sections.

### Fault attribution (lane-local)

- Workflow 60%, Agent 25%, Orchestration 15%

---

### 3.6 P06

### Observed divergence

- External packet: affirmative with size scaling `|S| >= eps*n/42` (`external_solutions/text_clean/lightSet - Dan Spielman.txt:19`, `external_solutions/text_clean/lightSet - Dan Spielman.txt:20`).
- Repo: `NO` with stronger target `|S| >= c|V|` independent of `alpha` (`P06/answer.md:4`, `P06/answer.md:27`).

### Primary causes

- `Workflow`: G0 formalization drift (critical quantifier/scale mismatch).
- `Agent`: solved a stronger altered statement and promoted it as the original.
- `Orchestration`: review gate did not include explicit quantifier-equivalence check against source text.

### Root cause

This lane likely solved the wrong problem specification (constant independent of `alpha`), making the counterexample irrelevant to the original claim family.

### Fault attribution (lane-local)

- Workflow 45%, Agent 25%, Orchestration 20%, Model 10%

---

### 3.7 P07

### Observed divergence

- External packet: impossibility (negative).
- Repo: existential `YES` (`P07/answer.md:4`), with explicit existential quantifier parsing (`P07/answer.md:26`).

### Primary causes

- `Workflow`: quantifier polarity interpretation error (existential vs universal reading).
- `Model`: false confidence in surgery-based realization route under this interpretation.
- `Orchestration`: insufficient semantic adjudication at G0 for quantifier intent.

### Root cause

The lane appears to have answered a different logical question than the one intended by the external solution authors.

### Fault attribution (lane-local)

- Workflow 40%, Model 25%, Orchestration 25%, Agent 10%

---

### 3.8 P08

### Observed divergence

- External packet: affirmative smoothing proposition (`external_solutions/text_clean/Abouzaid-solution.txt:19`).
- Repo: `NO` counterexample (`P08/answer.md:4`).

### Primary causes

- `Agent`: patch strategy changed definitions to eliminate a proof gap, then treated resulting route as definitive.
- `Workflow`: definition control was not anchored to a single frozen statement throughout all patches.
- `Model`: local contradiction route likely omitted hidden geometric compatibility assumptions.

### Root cause

Definition drift and patch-local proof repair replaced, rather than resolved, the original local-to-global compatibility burden highlighted in external comments.

### Fault attribution (lane-local)

- Workflow 35%, Agent 30%, Model 20%, Orchestration 15%

---

### 3.9 P09

### Observed divergence

- Aligned with external packet (`YES`).
- Multiple early overclaim faults were correctly caught and patched before upgrade.

### Root cause status

No final divergence. This lane demonstrates that adversarial review can work when quantifiers and statements remain stable.

---

### 3.10 P10

### Observed divergence

- Aligned with external packet.
- External comments also indicate this lane was one of the best LLM outcomes.

### Root cause status

No material failure. Strong positive control for tool-augmented linear algebra workflow.

---

## 4. Cross-Lane Critical Invariants

The following invariants explain most deviation:

1. **Statement-lock failure at G0**.
   - Quantifier/scaling mismatches were not mechanically prevented (`P06`, `P07`).

2. **Definition drift under patch pressure**.
   - Ambiguous terms were reinterpreted during fixes (`P08`).

3. **Citation-to-closure inflation**.
   - Frontier arguments were promoted to closure without contradiction-hardening (`P01`).

4. **Toolchain diagnosis lag**.
   - Wrong bottleneck diagnosis delayed closure routes (`P04`).

5. **Late compute planning on high-cost lanes**.
   - Parallel compute strategy identified but not operationalized in time (`P03`).

6. **Artifact normalization debt**.
   - Historical and final statuses coexisted in one file (`P05`).

7. **Review depth mismatch**.
   - Internal adversarial review caught local logical defects well, but did not reliably catch "global theorem polarity vs canonical solution" conflicts.

---

## 5. Responsibility Allocation (System-Level)

This is a systems attribution, not personal blame.

| Factor | Estimated contribution to deviation |
|---|---:|
| Problem formalization and statement control (`G0`) | 30% |
| Claim validation and contradiction-hardening (`G6/G7`) | 25% |
| Model theorem-synthesis/citation interpretation limits | 20% |
| Orchestration and escalation policy design | 15% |
| Tooling diagnosis and environment assumptions | 10% |

No evidence supports assigning primary fault to a single individual. The largest errors are architecture/process errors.

---

## 6. Corrective Actions

### 6.1 Immediate controls (next run)

1. Add a mandatory `statement_lock.md` per lane:
   - quantifier normal form
   - scaling factors
   - equivalent restatements
   - forbidden reinterpretations

2. Add a contradiction gate before `✅`:
   - if any primary-source theorem statement has opposite sign, lane cannot close without explicit reconciliation section.

3. Require two independent proof routes for sign-critical claims:
   - one constructive, one obstruction/counterexample-aware (or vice versa).

4. Freeze definitions at first G0 acceptance:
   - any definition change requires formal "problem changed?" adjudication.

5. Enforce final-form normalization:
   - remove superseded sections from `answer.md` or mark with strict archival block templates.

### 6.2 Resource policy

1. Pre-provision parallel compute for any lane with projected >12h serial runtime.
2. Add a "tool bottleneck verification" step:
   - test low-level solver API before concluding solver infeasibility.

---

## 7. Final Verdict

If the question is "Was this a 40% outcome?":

- Strict theorem-level alignment is `30%`.
- Risk-adjusted alignment is `47.5%`.
- Directional sign alignment is `60%`.

The principal deviation came from specification/control failures and validation design gaps, not from lack of effort or lack of tooling effort. The post-mortem indicates the fastest path to improvement is stronger statement discipline and contradiction-hardening, then earlier compute/tool provisioning on heavy lanes.
