# Claude Code Checklist — P05 (From Claude Research Round 2)

Date: 2026-02-12  
Lane: P05 only  
Goal: Convert round-2 local-lemma progress into a single global testable proposition.

---

## 0) Load context first

1. `P05/answer.md`
2. `P05/audit.md`
3. `P05/transcript.md`
4. `P05/experiments/exp1_transfer_systems.py`
5. `claude-research-final/transcripts/P05_claude_research_response_2026-02-12_round2.md`
6. `claude-research-final/transcripts/P05_claude_research_breakdown_2026-02-12_round2.md`
7. `claude-research-final/P05/99_claude_code_checklist_from_claude_research_round1.md`

---

## 1) Hard constraints

1. No status upgrade without theorem-level closure.
2. Claims must be tagged: `Proved / Cited / Empirical / Unresolved`.
3. Preserve distinction:
   - local geometric lemma (now proved),
   - global Class II “if” statement (still unresolved).
4. Avoid noisy/unverified external sources for theorem claims.

---

## 2) Route A (mandatory): formalize local lemma and corollary

1. Write precise lemma:
   - if `W^H=0` then `S^W ∧ ~E P_H ≃ ~E P_H`.
2. Write corollary for permutation cells:
   - `S^{k ind_K^H(1)} ∧ ~E P_H ≃ Σ^k ~E P_H`.
3. Insert in lane artifact with exact hypotheses/notation alignment.
4. Artifacts:
   - `P05/experiments/exp5_geometric_triviality_lemma.md`

---

## 3) Route B (mandatory): isolate the single remaining global proposition

1. Define explicit “proper-piece lifting proposition”:
   - from subgroupwise connectivity bounds,
   - deduce `E P_{G,+} ∧ E ∈ τ_{≥n}^O`.
2. Express it as a finite family of statements/checks (family tower or double-coset formulas).
3. Artifacts:
   - `P05/experiments/exp6_proper_piece_target_proposition.md`

---

## 4) Route C (bounded): one proof attempt on the target proposition

Choose one:
1. Family-filtration proof skeleton, or
2. double-coset weighted-connectivity proof skeleton.

Deliver either:
1. a complete proposition proof, or
2. an exact first-failure step with a candidate bridge lemma.

Artifacts:
- `P05/experiments/exp7_proper_piece_attempt.md`

---

## 5) Stop-loss gates

1. If Route B does not yield a single sharply testable proposition, stop cycle.
2. If Route C cannot advance beyond framework-level prose, stop cycle.
3. If no bridge lemma/proof is produced, keep P05 at `BLOCKED_WITH_FRONTIER`.

---

## 6) Required outputs after cycle

1. Lane verdict line: `CLOSEABLE_NOW` or `BLOCKED_WITH_FRONTIER`.
2. Route table A/B/C with pass/fail.
3. `P05/audit.md` escalation row.
4. `P05/transcript.md` entry with artifact paths.
5. `CONTAMINATION.md` updates (adopted vs discarded sources).

---

## 7) Minimal command skeleton

```powershell
git status -sb

# (if any script is added for finite-case checks)
python P05/experiments/exp1_transfer_systems.py

git status -sb
```

