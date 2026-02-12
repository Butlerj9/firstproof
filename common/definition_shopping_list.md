# Definition-Only Unblocking Queue (Claude Prep)

Generated: 2026-02-11  
Protocol: `common/definition_only_escalation.md`

This file is the single low-noise prep artifact for unsolved lanes.
Use it to dispatch Claude immediately when available.

## 0. Hygiene rules (mandatory)

- Ingest **statements only**: definitions, theorem statements, hypotheses, notation.
- Do **not** ingest proof text, proof sketches, survey commentary, or blog summaries.
- Primary sources only (journal/arXiv/book originals).
- Every ingest must be logged in both:
  - `CONTAMINATION.md` (row with source/section/tag/risk)
  - `PXX/audit.md` (Escalation Ledger event + dependency tag)
- If accidental direct-solution exposure occurs: freeze lane and log contamination.

## 1. Current unsolved lanes (canonical)

| Problem | Status | Bottleneck type | Priority |
|---------|--------|-----------------|----------|
| P05 | 🟡 Candidate | Proof gap (orbit-counting "only if"); definitions resolved | 5 (done this cycle) |
| P01 | ❌ Parked | Definition/theorem dependency block | 2 |
| P09 | 📊 Conjecture | Algebraic formalization gap | 3 |
| P04 | 🟡 Candidate | n>=4 theorem gap | 4 |
| P03 | 🟡 Candidate | n>=4 closure still open | 5 |

## 2. Immediate queue for Claude (gate-scoped)

### Q1. P05 re-open (G1 only, definition unlock)

- Cap: 25 messages.
- Goal: produce a precise candidate definition of O-adapted slice filtration with explicit dependency tags.
- Must output:
  - `P05/audit.md`: G1 refresh + Escalation row with citations.
  - `P05/transcript.md`: ingest provenance and rejected/accepted statements.
  - `P05/answer.md`: no theorem claim; definition candidates only unless fully closed.
- Stop condition:
  - If canonical O-adapted definition remains ambiguous after two candidate formulations, keep `❌ Parked`.

### Q2. P01 re-open (G1->G2 dependency closure check)

- Cap: 20 messages.
- Goal: resolve whether existing primary statements suffice to advance Route A without overclaim.
- Must output:
  - `P01/audit.md`: updated dependency ledger (resolved/unresolved).
  - `P01/transcript.md`: exact statement references used.
  - `P01/answer.md`: keep uncertainty explicit if any core theorem is still unresolved.
- Stop condition:
  - If deterministic shift quasi-invariance statement is still missing, keep `❌ Parked`.

### Q3. P09 closure prep (no new docs, no status upgrade by numerics alone)

- Cap: 30 messages.
- Goal: target only algebraic formalization tasks from existing experiments.
- Must output:
  - `P09/audit.md`: exact remaining formalization claims and pass/fail checks.
  - `P09/transcript.md`: independent check record.
- Stop condition:
  - If only empirical strengthening is added, status remains `📊`.

### Q4. P04 closure prep (n>=4 triage)

- Cap: 35 messages.
- Goal: bounded route test for n>=4 only; no rewrite loops.
- Must output:
  - `P04/audit.md`: route verdict with explicit blocker theorem.
  - `P04/transcript.md`: verification scripts and outcomes.
- Stop condition:
  - If no theorem closure and no verified counterexample, remain `🟡`.

### Q5. P03 monitoring prep (n>=4 hygiene checks)

- Cap: 15 messages for review cycle.
- Goal: enforce theorem-vs-empirical separation for n>=4 claims.
- Must output:
  - `P03/audit.md`: checklist results (degree-bound applicability, pole safety, modular consistency).

## 3. Minimal-contamination reference packet (statement targets only)

## P05 core references

1. Blumberg-Hill (2015), *Operadic multiplications in equivariant spectra, norms, and transfers*  
   URL: https://arxiv.org/abs/1309.1750  
   Extract only:
   - `Definition` of N-infinity operad (`def:geinfop`)
   - `Definition` of indexing system
   - `Definition` of admissible H-set
   - Main theorem mapping operads to indexing systems

2. Rubin (2019), *Characterizations of equivariant Steiner and linear isometries operads*  
   URL: https://arxiv.org/abs/1903.08723  
   Extract only:
   - `defn:indsys` (indexing system)
   - `defn:transys` (transfer system)
   - `thm:transys` (equivalence indexing systems <-> transfer systems)
   - `cor:transysBH2` (transfer systems <-> indexing categories)

3. Hill-Yarnall (2017), *A new formulation of the equivariant slice filtration...*  
   URL: https://arxiv.org/abs/1703.10526  
   Extract only:
   - theorem characterizing slice n-connectivity via geometric fixed points (`thm:GeomFPVersion`)
   - statement-level definitions of slice-connective categories used by that theorem

## P01 core references

1. Barashkov-Gubinelli (2018), *A variational method for Phi^4_3*  
   URL: https://arxiv.org/abs/1805.10814  
   Extract only:
   - main variational theorem (`th:main`)
   - Boue-Dupuis variational theorem statement (`th:variational`)
   - statement defining the limiting measure / Laplace transform characterization

2. Barashkov-Gubinelli (2020), *The Phi^4_3 measure via Girsanov's theorem*  
   URL: https://arxiv.org/abs/2004.01513  
   Extract only:
   - theorem giving variational/Girsanov representation (`eq:th1`)
   - coercivity / integrability theorem (`thm:equicoerc`)
   - statement-level absolute-continuity result wrt drift measure
   - statement-level singularity result wrt Gaussian free field (for route sanity check)

## 4. Dispatch-ready checklist (paste into Claude handoff)

1. Run `G0/G1` for target lane with stop-loss cap from Section 2.
2. Use only references in Section 3 and extract statement-level text only.
3. Update artifacts: `answer.md`, `audit.md`, `transcript.md`.
4. Add message/token delta and escalation event row in `audit.md`.
5. Return one of: `proceed`, `park`, `escalate`.

## 5. Required logging row format

Use this row format in `CONTAMINATION.md` and in `PXX/audit.md`:

`| timestamp | source | section/label | item_type | tag(CITE_ONLY) | exposure_risk | used_for |`
