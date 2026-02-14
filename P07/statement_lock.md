# Statement Lock (Retrospective)

- Problem: `P07`
- Date locked: 2026-02-14
- Locked by: Codex (retrospective control pass)

## Canonical statement (ambiguity noted)

Given a uniform lattice `Gamma` in a real semisimple Lie group with an element of order `2`, ask whether `Gamma` can be the fundamental group of a closed manifold whose universal cover is rationally acyclic.

## Ambiguity requiring explicit adjudication

Two non-equivalent readings exist:

1. Universal reading: `for all such Gamma`, existence of such a manifold.
2. Existential reading: `there exists at least one such Gamma`.

This lock requires the lane to declare one reading explicitly before closure.

## Quantifier lock requirement

No `Submitted` status is allowed unless `answer.md` includes an explicit quantifier declaration block.

## Forbidden drift

1. Switching between universal and existential reading mid-proof.
2. Using an existential construction to claim a universal theorem.

## Contradiction trigger

If any authoritative source proves universal impossibility while lane claims existential possibility (or vice versa), the lane must include a reconciliation section identifying the quantifier mismatch.

