# GPT-pro Breakdown — P04 (Round 3)

Date: 2026-02-13  
Source: User-provided GPT-pro response + pro-thinking dump  
Lane: P04  
Purpose: Distill actionable signal for immediate Claude Code continuation after P05.

---

## 1) High-value signal

1. Recast blocker as normalized compact-domain inequality (`P04-B1`).
2. Prioritize rigorous certification routes over new symbolic ad hoc expansion.
3. Keep verdict `BLOCKED_WITH_FRONTIER` unless certification succeeds.

---

## 2) Canonical blocker statement

Prove nonnegativity of normalized margin:

`Mar(w,u1,t1,u2,t2) = psi(uh,th) - w psi(u1,t1) - (1-w) psi(u2,t2) >= 0`

with:

- `uh = w^(3/2) u1 + (1-w)^(3/2) u2`
- `th = w^2 t1 + (1-w)^2 t2`
- `(u1,t1), (u2,t2), (uh,th)` in normalized real-rooted quartic domain.

This is the exact frontier equivalent for general n=4 `(b != 0, c' != 0)`.

---

## 3) Recommended route order from intake

1. Interval-certified positivity on compact normalized domain.
2. CAD/exact elimination on reduced boundary families.
3. KKT/boundary minimum reduction only if route 1 stalls.

---

## 4) Immediate caveats

1. Route-count metadata in intake is stale (`9` vs current `13`).
2. No theorem-level closure in intake; only route reframing + planning.
3. Existing proved subcases remain unchanged (`b=0`, `c'=0`).

---

## 5) Suggested cycle objective

Either:

1. Produce a rigorous positivity certificate for `Mar` on full domain, or
2. Produce a reduced irreducible blocker with exact uncertified remainder and why current tooling cannot close it.

