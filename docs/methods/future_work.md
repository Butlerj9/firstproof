# Future Work: Shifting the Observed Capability Boundary

## Scope

This document describes practical system-level directions that could move the capability boundary observed in this sprint. It is intentionally framed as boundary analysis, not retrospective "how we could have won."

## 1. Empirical boundary observed in this sprint

Outcomes clustered into three regimes:

1. Structured derivations and bounded algebraic domains.
These closed reliably under orchestration plus adversarial review.

2. Counterexample-driven or computationally falsifiable domains.
These closed when deterministic experiments and high-precision checks were integrated.

3. Machinery-heavy or abstraction-bridging domains.
These stalled on:
- finite-n to uniform-n bridge construction,
- formulation-level definition precision,
- invariant discovery beyond direct theorem composition,
- deep categorical or functional-analytic abstraction jumps.

This pattern did not look primarily workflow-bound. It remained after strong orchestration, review pressure, and experiment discipline.

## 2. Limitation model

Two limitation classes best explain the stalls:

### 2.1 Coverage and encoding gaps

- niche definitions weakly represented in priors,
- theorem statements with delicate hypothesis structures,
- sparse public duplication of domain-specific machinery.

These are mainly training-distribution and retrieval-coverage problems.

### 2.2 Structural abstraction gaps

- new invariant discovery,
- non-local abstraction bridges,
- uniformization over arbitrary parameters,
- symbolic closure from strong empirical evidence.

These are representational and composition problems, not only missing-text problems.

## 3. Why orchestration did not fully remove the boundary

This pipeline already included:
- multi-agent adversarial review,
- falsification and counterexample pressure,
- deterministic experiment harnesses,
- stop-loss and escalation,
- artifact-level provenance and no-overclaim gates.

These controls improved reliability and reduced hallucination, but they do not by themselves create:
- new representational capacity,
- new invariant-discovery ability,
- or stronger theorem-space exploration geometry.

## 4. Candidate directions to shift the boundary

These were out of scope for this sprint but are plausible boundary-shifting directions.

### 4.1 Domain-adaptive fine-tuning

Fine-tune on adjacent theorem families and foundational corpora to:
- increase density of relevant structural patterns,
- improve invariant recognition,
- reduce definition drift in niche domains.

Target classes of problems, not single benchmark items.

### 4.2 Formal verifier coupling

Integrate Lean/Coq/SMT in loop to:
- enforce quantifier discipline,
- expose hidden circular dependencies,
- turn proof-check failures into search guidance.

### 4.3 Theorem retrieval with structural matching

Move beyond keyword retrieval to structure-aware matching on:
- hypothesis templates,
- operator algebra form,
- categorical signatures.

### 4.4 Process-level verifier fine-tuning

Train on audit/failure corpora:
- recurring quantifier errors,
- patch cycles,
- dependency-ledger failures,
- theorem-misapplication patterns.

### 4.5 Multi-problem domain pipelines

Shift objective from one-off closure to domain colonization:
- solve adjacent families procedurally,
- build reusable invariant templates,
- compound solvable subspaces over time.

### 4.6 Architecture-level improvements

Likely helpful:
- deeper compositional inductive biases,
- neural-symbolic hybrid reasoning modules,
- stronger long-range abstraction tracking.

## 5. Why these were excluded in this run

These methods were excluded to preserve:
- comparability under general frontier-model conditions,
- strict autonomy constraints,
- clean interpretation of what orchestration alone can do.

Including heavy specialization in-sprint would confound the baseline.

## 6. Interpretation

The observed limitations do not imply "AI cannot do research mathematics."

They imply a boundary:
- some theorem-space regions are currently reachable under strict autonomy plus orchestration,
- others likely require denser domain representation or stronger abstraction mechanisms.

The likely trajectory is gradual expansion of automatically solvable subspaces, not immediate universal closure.

## 7. Practical takeaway

This sprint supports three claims:

1. General frontier models can autonomously solve nontrivial advanced problems with rigorous scaffolding.
2. Remaining blockers are not mainly promptcraft or orchestration hygiene failures.
3. Future gains will likely come from training/system architecture/verification integration, not workflow tuning alone.

## 8. Pointers

- Method protocol: `methods_extended.md`
- Limitation analysis: `docs/methods/technical_limitations.md`
- Portfolio outcomes: `RESULTS.md`
