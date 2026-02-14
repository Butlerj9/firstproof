# Statement Lock Template

Use this file at `PXX/statement_lock.md` and freeze it at first G0 acceptance.

## Metadata

- Problem: `PXX`
- Date locked:
- Locked by (agent role/model):
- Source text hash or citation:

## Canonical Statement (verbatim or normalized)

Paste the authoritative problem statement verbatim, then normalized form below.

## Quantifier Normal Form

Write explicitly in logic order:

- `exists/for all` variables:
- Domains:
- Conclusion:

Example structure:

`for all G ... for all alpha in (0,1) ... exists S subset V ... such that ...`

## Symbol and Scale Lock

List symbols and scaling semantics that must not drift.

| Symbol | Meaning | Allowed range | Notes |
|---|---|---|---|
| | | | |

## Equivalent Restatements (approved)

List only restatements proven equivalent to canonical statement.

1.
2.

## Non-Equivalent Restatements (forbidden)

List common near-miss formulations that are not equivalent.

1.
2.

## Decision Polarity Target

- Expected final form: `YES` / `NO` / `UNKNOWN`
- What would count as a disproof:
- What would count as a proof:

## Contradiction Triggers

If any trigger fires, do not upgrade to `Submitted` until reconciled.

1. A primary-source theorem statement has opposite sign/polarity.
2. A proof route relies on a changed definition not in this lock.
3. A quantifier or scaling term differs from this lock.

## Change Control

Changes after lock require:

1. `LOCK_CHANGE_REQUEST` section in `audit.md`.
2. Reviewer sign-off.
3. Explicit statement whether the problem changed or only notation changed.

Without this, treat any change as invalid for status upgrades.

