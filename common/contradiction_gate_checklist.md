# Contradiction Gate Checklist

Run this checklist before any lane upgrades to `✅ Submitted`.

## Purpose

Prevent false closure from statement drift, polarity inversion, or unresolved source contradictions.

## Inputs

- `PXX/answer.md`
- `PXX/audit.md`
- `PXX/statement_lock.md`
- `PXX/transcript.md`
- Primary-source theorem statements (if cited)

## Gate Criteria

Mark each item `PASS` or `FAIL`.

1. Statement lock exists and is current.
2. Final claim in `answer.md` matches statement-lock quantifiers exactly.
3. Final claim matches statement-lock scaling semantics exactly.
4. No definition used in proof differs from statement lock.
5. Every external theorem used for closure has statement-level citation.
6. No cited theorem has opposite polarity to final claim.
7. If opposite-polarity source exists, a reconciliation section is present and reviewer-approved.
8. Reviewer explicitly checked for "solved a stronger/weaker problem" drift.
9. Counterexample track and proof track were both evaluated for sign-critical lanes.
10. Status labels are consistent across `answer.md`, `audit.md`, and `RESULTS.md`.

## Required Artifacts

Add this block to `PXX/audit.md`:

```
## Contradiction Gate

Date:
Reviewer:
Result: PASS/FAIL
Failed items:
Remediation:
```

## Hard Rule

If any item fails, lane cannot be upgraded to `✅ Submitted`.

