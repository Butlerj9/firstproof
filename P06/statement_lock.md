# Statement Lock (Retrospective)

- Problem: `P06`
- Date locked: 2026-02-14
- Locked by: Codex (retrospective control pass)

## Canonical statement

For every graph `G=(V,E)` and every `alpha in (0,1)`, does there exist a universal constant `c>0` and an `alpha`-light subset `S` with `|S| >= c|V|`?

## Quantifier normal form

`exists c>0, for all G, for all alpha in (0,1), exists S subseteq V such that S is alpha-light and |S| >= c|V|.`

## Symbol/scale lock

| Symbol | Meaning | Lock |
|---|---|---|
| `c` | global constant | must be independent of both `G` and `alpha` |
| `alpha` | lightness parameter | quantified universally over `(0,1)` |
| `|S| >= c|V|` | size target | linear-in-`|V|`, not `alpha`-scaled |

## Forbidden non-equivalent restatements

1. `exists C such that |S| >= alpha*n/C` (depends on `alpha`).
2. Any formulation where the constant depends on `alpha`.

## Contradiction trigger

If external authoritative source states a theorem for an `alpha`-scaled bound while this lock asserts `alpha`-independent `c`, status cannot be `Submitted` until this mismatch is reconciled in `audit.md`.

