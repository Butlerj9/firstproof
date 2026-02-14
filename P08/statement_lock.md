# Statement Lock (Retrospective)

- Problem: `P08`
- Date locked: 2026-02-14
- Locked by: Codex (retrospective control pass)

## Canonical statement

Determine whether every 4-valent polyhedral Lagrangian surface in `R^4` admits a Hamiltonian Lagrangian smoothing under the definition used in the problem statement.

## Definition lock

The smoothing notion must be fixed once and not changed during patch cycles.

Acceptable lock fields:

1. Parameter family domain (`t in (0,1]` vs `t in [0,1]`).
2. Convergence mode at `t->0` (topological isotopy, Hausdorff, or stronger).
3. Compatibility requirements between local charts/edge-vertex neighborhoods.

## Forbidden drift

1. Replacing the statement definition by a stronger variant solely to close a proof gap.
2. Treating "local smoothing near each vertex" as sufficient without explicit global compatibility argument.

## Contradiction trigger

If an external proof is affirmative under one definition while lane disproof is under another, lane cannot be `Submitted` until both definitions are compared and adjudicated explicitly.

