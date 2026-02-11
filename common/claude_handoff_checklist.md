# Producer -> Claude Checklist (Standard Handoff)

Use this checklist at the start of every new problem and at each gate transition.
Goal: maximize throughput, prevent rewrite loops, and keep artifacts publishable.

## 0) Handoff Header (always include)

- Problem ID and domain.
- Current date/time (PT) and remaining sprint window.
- Message budget for this problem (hard cap).
- Current gate target (start at G0 unless resuming).
- Current status target options: `✅` / `🟡` / `📊` / `❌`.
- Contamination mode reminder (llm-only unless explicitly relaxed).

## 1) Immediate Work Plan Request

Ask Claude to return a compact execution plan before deep work:

- Gate sequence to run now.
- Expected message spend per gate.
- Stop-loss trigger for each gate.
- Exact artifacts to update (`answer.md`, `audit.md`, `transcript.md`, `experiments/`).

## 2) Gate-by-Gate Execution Checklist

## G0 Formalize (hard cap: 10 messages)

- Explicit quantifiers (`forall`, `exists`, order).
- Full symbol/type glossary.
- Precise YES/NO restatement.
- Counterexample shape (concrete falsifier template).
- Truth mode selected (`PROVE`, `DISPROVE`, or `EXPLORE BOTH`) with rationale.

Pass condition:
- No hidden assumptions.
- Ambiguities listed as open dependencies.

## G1 Background (hard cap: 15 messages)

- Prerequisite list complete.
- Each dependency tagged:
  - `PROVE_INLINE`
  - `CITE(statement number required)`
  - `NEEDS_SOURCE`
- If `NEEDS_SOURCE > 3`, stop and park or switch problem.

Pass condition:
- No "well known" claims without source or proof.

## G2 Route Map (hard cap: 15 messages)

- At least 2 distinct routes (not cosmetic variants).
- Each route includes:
  - lemma chain
  - bottleneck lemma
  - failure conditions
- YES/NO problems must include a counterexample track.

Pass condition:
- Chosen route is justified against alternatives.

## G3 Lemma DAG

- Every lemma has precise statement + acceptance test.
- No circular dependencies.
- Explicit map from lemmas -> final claim.

Pass condition:
- No "then result follows" gap.

## G4 Experiments (hard cap: 15 messages)

- Reproducible scripts (seed/version/tolerance).
- Adversarial test cases, not only random easy cases.
- Numerical stability checks (precision escalation near boundary).
- Edge-case coverage (degenerate/nullspace/disconnected/etc. as relevant).

Pass condition:
- Experiments test the exact claim, not a proxy.

## G5 Proof Draft (hard cap: 40 messages)

- Every nontrivial step justified.
- All theorem hypotheses checked explicitly.
- Quantifier scope verified line-by-line.
- Boundary cases handled explicitly.
- Claim level matches evidence level (do not overclaim).

Pass condition:
- Draft is internally coherent and citation-complete.

## G6 Reviewer Readiness Package

- Prepare concise relay summary for reviewer:
  - what is fully proved
  - what is only empirical
  - known gaps and risk flags
- Include explicit "key questions for reviewer to attack".

Pass condition:
- Reviewer can falsify/test quickly without extra context hunting.

## G7 Package

- `answer.md` self-contained.
- `audit.md` includes full gate history and patch cycles.
- `transcript.md` complete enough for reconstruction.
- `README.md` and `RESULTS.md` status rows updated.
- Commit with clear status label in message.

Pass condition:
- Repo reflects true state without overclaim.

## 3) Stall / Park Rules (always enforce)

- If no new lemma closure or experimental signal in 10 messages:
  - force route change once.
- If still stalled after route change:
  - park as `📊` or `❌` and move on.
- Never spend more than cap trying to "polish" a stuck proof.

## 4) Token + Prompt Logging Requirement

Require Claude to append/update in `audit.md` at every gate:

- Estimated messages used / budget.
- Estimated token usage so far.
- New scripts run and outputs produced.
- Net progress since last checkpoint (what closed, what remains).

If logging is missing, pause progression until logs are updated.

## 5) Standard Closing Ask to Claude

At the end of each working block, require:

- Current status recommendation (`✅` / `🟡` / `📊` / `❌`).
- Top 3 unresolved risks.
- Exact next action with estimated message cost.
