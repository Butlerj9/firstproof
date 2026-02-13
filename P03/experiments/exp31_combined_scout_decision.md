# EXP-31: Combined Scout Decision Memo — P03

Date: 2026-02-13
Scouts reviewed: GPT-pro R2 (2026-02-13), Claude Research R3 (2026-02-13)
Prior scout intakes: GPT-pro R1 (Session 22), Claude Research R1 (Session 22)

---

## Executive Summary

Two independent scouts (GPT-pro R2, Claude Research R3) both confirm BLOCKED_WITH_FRONTIER for P03 n≥5. No closure route is immediately available. Both scouts propose testable bridge lemmas and kill-tests that are compatible with existing lane facts (with one quarantined claim).

After reconciliation, de-duplication, and conflict audit:
- **4 merged route families** identified (from 12 GPT-pro + 14 Claude Research)
- **1 quarantined claim** (integrality ⟹ limit=specialization — scoping issue)
- **3 ranked routes** selected for bounded execution
- **1 immediate execution pick**: R1-DIV (divisibility kill-test)

---

## Decision: Execute R1-DIV First

**Rationale**:
1. Directly testable with existing Fraction arithmetic infrastructure (n=3)
2. Already supported by numerical evidence (EXP-4: O(1−q) convergence)
3. No dependency on external formulas (BDW, Sahi binomial)
4. Clean bridge: if (T_i−t)E* ∈ (1−q)·R, then symmetry follows immediately
5. Generalizable: if divisibility holds for all n, closes the conjecture completely
6. Cross-scout endorsement: GPT-pro R2 explicitly identifies this as "fastest closure path"

**Fallback chain**: R1-DIV → R2-BinAS → R3-SMLQ → HOLD

---

## Deliverables Produced

| Artifact | Content | Path |
|----------|---------|------|
| EXP-27 | Scout reconciliation matrix | `P03/experiments/exp27_scout_reconciliation_matrix.md` |
| EXP-28 | Route de-dup and ranking | `P03/experiments/exp28_scout_route_rank.md` |
| EXP-29 | Conflict audit | `P03/experiments/exp29_scout_conflict_audit.md` |
| EXP-30 | Selected route plan (R1-DIV) | `P03/experiments/exp30_selected_route_plan.md` |
| EXP-31 | This memo | `P03/experiments/exp31_combined_scout_decision.md` |

---

## Lane State After This Review

- **Status**: 🟡 Candidate (unchanged)
- **Messages used**: ~71 + ~4 (this review) = ~75
- **Next action**: Implement exp32_divisibility_test.py (R1-DIV kill-test at n=3)
- **Stop-loss**: If R1-DIV fails kill-test → R2-BinAS. If all 3 fail → HOLD.
- **No answer.md status change** unless a checkable proof artifact appears.
