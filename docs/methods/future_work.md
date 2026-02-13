# Future Work and Open Directions

## Abstract

This note records the principal boundary findings of the current run and outlines plausible next steps for extending capability. The goal is methodological: to identify which parts of theorem-space are presently reachable under strict autonomy constraints, and which parts remain open. We emphasize that this is a forward-looking research program, not a retrospective account of missed tactics.

## 1. Problem Setting and Scope

We evaluate a tool-augmented, multi-agent LLM workflow under the following fixed constraint: no human mathematical content in the proof loop. Within this setting, we ask two questions:

1. Which classes of problems are currently tractable for closure with high reliability?
2. Which classes remain blocked, and for what technical reasons?

Throughout, "future work" refers to boundary-shifting directions that were intentionally out of scope for the sprint baseline.

## 2. Main Empirical Findings

The observed outcomes separate into three regimes.

### 2.1 Closeable regime

Structured derivations in bounded algebraic settings were frequently tractable for closure under adversarial review plus deterministic validation.

### 2.2 Evidence-driven regime

Counterexample-sensitive and computation-heavy lanes were tractable for closure when supported by high-precision scripts, reproducible sweeps, and explicit certificate workflows.

### 2.3 Frontier regime

Machinery-heavy lanes requiring non-local abstraction remained open. Recurring blockers included:

- finite-to-uniform bridges (e.g., finite-n to all-n transitions),
- high-sensitivity formulation dependencies,
- missing invariant-level reductions,
- long-horizon composition across deep technical frameworks.

These blockers persisted after strong workflow controls, indicating that the residual gap is not primarily operational.

## 3. Limitation Profile

The unresolved lanes are best explained by two limitation classes.

### 3.1 Coverage and statement-precision limitations

Some domains depend on niche definitions and theorem statements with delicate hypotheses. Failure here is often traceable to weak prior coverage or retrieval precision.

### 3.2 Structural-composition limitations

Other domains require new organizing structure (for example, a bridge invariant or a global reduction lemma). In these cases, empirical evidence is strong, but symbolic closure remains open.

In short: retrieval improves correctness at the statement level, but does not by itself generate missing structural glue.

## 4. Immediate Scientific Uses of the Current Pipeline

Even before full domain-level autonomy, the current workflow has direct research value.

### 4.1 Lane triage and ranking

The gate/escalation protocol supports fast separation of:
- closeable lanes,
- certificate-limited lanes,
- and structurally open lanes.

### 4.2 Conjecture sharpening

Weak hypotheses can be upgraded to precise frontier statements with explicit blocker lemmas and reproducible evidence.

### 4.3 Obstruction and counterexample discovery

The workflow is effective at producing negative results, impossibility frontiers, and corrected scope statements that are independently publishable.

### 4.4 Reproducible artifact production

Outputs are audit-ready: experiments, review logs, and status transitions are preserved in a form suitable for independent replication.

### 4.5 Automation-ready workflow control

The current Producer role is largely policy execution (gate control, escalation triggers, run control, logging). This is a practical candidate for replacement by a controller agent or deterministic orchestration engine without changing the no-human-math boundary.

## 5. Directions for Boundary Expansion (Out of Scope for This Sprint)

The following directions are plausible mechanisms for reducing the observed frontier.

### 5.1 Domain-adaptive fine-tuning

Fine-tune on adjacent theorem families and foundational corpora to improve statement fidelity and invariant recognition in target domains.

### 5.2 Formal verification coupling

Integrate Lean/Coq/SMT feedback loops to enforce quantifier discipline and convert proof-check failures into structured search signals.

### 5.3 Structure-aware theorem retrieval

Move from keyword retrieval to hypothesis-shape and operator-structure matching.

### 5.4 Verifier-oriented process training

Train on audit traces and patch cycles (e.g., quantifier failures, citation misapplication, dependency leaks) to improve internal proof hygiene.

### 5.5 Class-level program design

Target families of adjacent problems rather than isolated instances, so successful reductions can be reused across a growing domain neighborhood.

### 5.6 Architecture-level improvements

Likely contributors include stronger compositional biases, neural-symbolic coupling, and improved long-range abstraction tracking.

## 6. From Individual Closures to Class-Level Programs

A central open direction is methodological: replacing one-off theorem closure with procedural expansion of a solvable class.

Concretely:

1. Solve adjacent families with shared structure.
2. Promote successful reductions into reusable templates.
3. Reuse certification patterns and experiment harnesses across neighboring lanes.
4. Treat solved subspaces as foundations for harder adjacent regions.

This reframes progress as controlled enlargement of reachable theorem-space.

## 7. Why These Directions Were Excluded Here

These extensions were excluded to preserve baseline comparability under strict autonomy constraints. Introducing heavy specialization in the sprint would have confounded interpretation of what general frontier models plus orchestration can already achieve.

## 8. Concluding Remarks

The present evidence supports three conclusions.

1. Under strict no-human-math constraints, general frontier models can close nontrivial advanced lanes with high rigor when scaffolded correctly.
2. Remaining blockers are concentrated in structural-composition gaps, not merely prompt quality or workflow hygiene.
3. The most credible path forward is class-level system development (training, retrieval, formal verification, and orchestration), not isolated prompt-level optimization.

## 9. Related Documents

- Method protocol: `methods_extended.md`
- Limitation analysis: `docs/methods/technical_limitations.md`
- Portfolio outcomes: `RESULTS.md`
