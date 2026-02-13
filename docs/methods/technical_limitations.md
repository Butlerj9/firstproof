# Technical Limitations and Escalation Rationale

## Abstract

This note documents the principal limitation modes observed in the project and clarifies the role of escalation under strict autonomy constraints. The aim is to distinguish operational failures from structural failures, and to record which categories of unresolved lanes remain outside current closure conditions.

## 1. Study Context

The Producer role is interpreted operationally, not mathematically: gate execution, escalation control, logging, and publication hygiene are enforced under pre-defined policy rules. Correctness adjudication is delegated to adversarial review and deterministic validation artifacts.

The control stack used throughout the repository is:

- policy/workflow control,
- agent orchestration (Implementer/Reviewer/Scout),
- base LLM generation,
- opaque in-model inference dynamics.

Within this setup, unresolved lanes are not interpreted as "unsolvable in principle," but as outside reliable closure for the present system configuration.

## 2. Principal Failure Modes

### 2.1 Coverage and statement-fidelity limitations

Certain domains depend on highly specific definitions and theorem statements with delicate hypotheses. When these are weakly represented in priors, the dominant failure modes are:

- nearby-definition conflation,
- incorrect theorem-schema substitution,
- plausible but invalid analogical steps.

### 2.2 Structural-composition limitations

Other domains fail despite adequate references because closure requires:

- discovery of new invariants,
- non-local abstraction bridges,
- finite-to-uniform generalization steps,
- long compositional chains with strict hypothesis alignment.

This second class is not reducible to retrieval quality alone.

## 3. Why Escalation Is Necessary

Escalation is introduced to control overclaim risk and preserve inferential quality. In practice it provides:

- adversarial detection of hidden quantifier/hypothesis defects,
- deterministic rejection of algebraic or numerical inconsistencies,
- bounded search via stop-loss policy,
- definition-only retrieval when statement fidelity is the blocking factor.

Without escalation, difficult lanes systematically exhibit premature closure claims.

## 4. What Escalation Resolves and What It Does Not

Escalation can resolve:

- definition drift,
- missing statement-level citations,
- weak empirical validation procedures,
- artifact inconsistency across answer/audit/transcript layers.

Escalation does not directly create:

- new structural invariants,
- novel theorem-composition operators,
- robust finite-to-uniform bridge lemmas,
- domain-specific abstraction mechanisms absent from model behavior.

## 5. Repository-Level Case Pattern

Observed lane behavior supports this separation.

- `P01` closed via CITE_PLUS escalation (BG proof-chain verification) together with an independent Hairer-Steele line.
- `P09` closed after escalation to modular rank arguments and exact base-case coverage.
- `P03` closed for `n <= 4` but remains open for `n >= 5` under the documented computational/structural barrier.
- `P04` progressed from empirical evidence to SOS-certified closure at `n = 4` once solver-path issues were corrected.
- `P05` closed through iterative theorem expansion culminating in the general biconditional.

The common pattern is that escalation improved reliability and occasionally enabled closure, but unresolved frontier components were concentrated in structural-composition gaps.

## 6. On the "Not Encoded in Priors" Hypothesis

Lack of prior coverage is a necessary explanation in some lanes, but not a sufficient one. Even with stronger retrieval, closure requires:

- stable decomposition choices,
- consistent multi-layer hypothesis propagation,
- and sound recomposition across long proof chains.

Hence improved corpus coverage raises closure probability but does not guarantee theorem-level completion.

## 7. Cross-Model Coherence as a Reliability Signal

The project used cross-model structural agreement ("resonant coherence") as a triage signal:

- independent model families propose compatible decompositions,
- those decompositions survive adversarial review,
- and executable checks remain stable.

This signal improves route selection and early fault detection, but it is not a substitute for proof. Deterministic validation and adversarial gates remain mandatory.

## 8. Evidence Pattern Across the Portfolio

Closed or strongly closed lanes cluster in domains admitting:

- direct algebraic reductions,
- bounded symbolic structure,
- or transferable global obstructions.

Residual frontier lanes cluster where closure requires:

- new structural bridge lemmas,
- delicate machinery composition,
- or theorem-level upgrading from finite empirical evidence.

This pattern justifies strict claim-tier separation.

## 9. Claim-Policy Consequences

The repository therefore enforces:

- strict `proved / cited / empirical / unresolved` separation,
- explicit escalation provenance,
- and publication of candidate/parked outputs when blockers are precise and reproducible.

This is a methodological strength, not a fallback, because it preserves high-value negative and frontier evidence.

## 10. Boundary-Shift Directions

Likely mechanisms for shifting the current boundary include:

- domain-adaptive fine-tuning on adjacent theorem families,
- structure-aware theorem retrieval,
- formal-method coupling (Lean/SMT/CAS),
- and neural-symbolic planning for theorem-space exploration.

Workflow refinement alone is unlikely to resolve all frontier cases.

## 11. Conclusion

Escalation was necessary for rigor and reliability, and in several lanes it was decisive. However, unresolved frontier lanes indicate a residual structural-composition ceiling under current autonomy constraints. The central limitation is therefore not only reference availability, but missing structural glue in theorem composition.

## 12. Prompt-Equivalency Heuristic (Reporting Only)

For documentation-level effort interpretation, the repository uses:

- `1` orchestrated agent prompt ~= `10` llm-only prompts,
- with a nominal split of `8` short prompts + `2` long prompts.

This is a planning/reporting heuristic, not an empirical benchmark. Primary accounting remains token/message logs in `RESULTS.md` and per-lane artifacts.
