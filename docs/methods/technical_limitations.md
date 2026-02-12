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
