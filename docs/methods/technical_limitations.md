# Technical Limitations and Escalation Rationale

## Purpose

This document explains why escalation was necessary in this project, what escalation can and cannot fix, and why some lanes stalled despite strong workflow controls.

The short version:
- A lane like `P01` is not "unsolvable in principle."
- Under the current autonomy and training constraints, it sits outside reliable closure for a general frontier LLM stack.

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

## 4. Why P01/P04/P09-type gaps persisted

Observed in this project:
- `P01` depends on deep renormalization/infinite-dimensional measure machinery with strict hypothesis handling.
- `P04` and `P09` reached strong empirical/formal partial structure but stalled at final symbolic closure steps.

Inference:
- workflow quality improved substantially,
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

## 7. Repo-level evidence pattern

Closed or strongly closed lanes clustered in domains with:
- direct algebraic reductions,
- bounded symbolic structure,
- or known global obstructions that can be applied cleanly.

Stalled lanes clustered where closure required:
- a new structural bridge,
- heavy machinery composition with subtle quantifiers,
- or theorem-level upgrades from high-quality finite evidence.

This pattern supports the need for escalation and strict claim-tier separation.

## 8. Implication for claim policy

The correct policy is:
- keep `proved / cited / empirical` separation strict,
- keep escalation logs explicit,
- treat parked/candidate states as valid scientific outputs when blockers are precise and reproducible.

This is a strength, not a weakness: it avoids result laundering and preserves high-value failure information.

## 9. If pushing beyond the current boundary

Likely required improvements include:
- domain-adaptive fine-tuning on adjacent theorem families,
- stronger theorem-retrieval with structural matching,
- symbolic search/formal-method coupling (Lean/SMT/CAS),
- or neural-symbolic hybrid planning for theorem-space exploration.

Workflow improvements alone are unlikely to close every remaining lane.

## 10. Takeaway

For this project, escalation was necessary for reliability and rigor, but insufficient for full closure in all domains.

The key finding is not "some references were missing." The stronger finding is:
- current general LLM orchestration handles deep application of known structure well,
- but remains limited on problems requiring new structural glue under strict autonomy constraints.
