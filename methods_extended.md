# Methods: Agentic LLM Orchestration for Research-Grade Proof Attempts

## Abstract

This repository evaluates a tool-augmented, multi-model agentic LLM system applied to advanced mathematics problems under a strict "no human mathematical content" boundary. The human administrator ("Producer") performs workflow operations only (scheduling, budgeting, repo/logging hygiene, tool execution, publication cadence, and contamination enforcement). Models generate essentially all mathematical content: formalizations, route selection, lemma decomposition, proof/counterexample construction, experiments, and writeups.

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
- execution of model-authored scripts/commands (verbatim)
- enforcement of logging, status taxonomy, and contamination policy

The Producer does not add mathematical ideas, proof strategy, or domain interpretation.

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
- human role restricted to operational continuity and integrity enforcement

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
