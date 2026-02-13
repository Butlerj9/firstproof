# Claude Research Transcript — P04 (Round 2, condensed archival)

Date captured: 2026-02-13  
Source: user-provided Claude Research response (manual paste)  
Lane: P04  
Intent: archive latest scout guidance and closure priorities for execution.

---

## Core verdict from scout

- **Lane verdict: `CLOSEABLE_NOW`** for general `n=4`.
- Claimed viable closure routes (new vs prior failed 13 routes):
  - `L1` TSSOS sparse SOS on the 837-term degree-14 polynomial.
  - `L2` Parametric SOS by fixing `w` (dimension-reduced slices).
  - `L5` Bernstein subdivision for the 3-variable sub-problem.
  - `L11` Schmudgen preordering (higher-degree constrained certificates).
  - `L13` Fiber-wise case-split + Lipschitz interpolation.
- Analytic longer-horizon routes flagged:
  - `L6` finite free score-projection analog of Blachman/Stam.
  - `L7` cumulant-coordinate convexity/superadditivity.

---

## Lane table (as reported)

| Lane | Approach | Scout status |
|---|---|---|
| L1 | TSSOS sparse SOS on 837-term `P` | CLOSEABLE_NOW |
| L2 | Parametric SOS stratification (`w` fixed) | CLOSEABLE_NOW |
| L3 | SONC/SAGE circuit certificates | BLOCKED_WITH_FRONTIER |
| L4 | SDSOS/DSOS LP/SOCP hierarchy | BLOCKED_WITH_FRONTIER |
| L5 | Bernstein subdivision (3-var sub-problem) | CLOSEABLE_NOW |
| L6 | Finite free score projection (Blachman-Zamir transfer) | BLOCKED_WITH_FRONTIER |
| L7 | Cumulant-coordinate convexity | BLOCKED_WITH_FRONTIER |
| L8 | Gribinski entropy + finite de Bruijn | BLOCKED_WITH_FRONTIER |
| L9 | Schur-Horn for hyperbolic polynomials | BLOCKED_WITH_FRONTIER |
| L10 | `phi`-subadditivity via Jensen on `F(u)` convexity | BLOCKED_WITH_FRONTIER |
| L11 | Schmudgen preordering at higher degree | CLOSEABLE_NOW |
| L12 | Entropic OT variational route | BLOCKED_WITH_FRONTIER |
| L13 | Case-split fiber-wise + Lipschitz | CLOSEABLE_NOW |
| L14 | Handelman LP on polytope approximation | BLOCKED_WITH_FRONTIER |

---

## Top 3 routes (as prioritized in response)

### 1) Parametric SOS + TSSOS (L1+L2 combined)

- Bridge idea:
  - Certify `P(w0, ...) >= eps(w0) > 0` on fibers for grid `w0 = k/N`.
  - Bound `L = max |dP/dw|` on full domain.
  - Conclude positivity if `L/N < min_k eps(wk)`.
- Kill conditions:
  - Persistent infeasible/negative fiber certs at raised degree.
  - Lipschitz bound too loose for current grid.
- Expected closure mode:
  - Computational certificate with rational rounding check.

### 2) Cumulant-coordinate convexity/superadditivity (L7)

- Bridge idea:
  - Re-express `Phi_4` in finite-free cumulants where `boxplus_4` is additive.
  - Reduce to proving superadditivity (or concavity sufficient condition) of `1/Phi_4` in cumulant variables.
- Kill conditions:
  - No tractable closed rational form in cumulants.
  - Numerical superadditivity fails in sampled valid domain.

### 3) Finite free score-projection (L6)

- Bridge idea:
  - Define finite score vectors from root-derivative formula.
  - Prove score decomposition/projection identity under `boxplus_4`.
  - Use projection contraction (`L2`) to recover Stam-type inequality.
- Kill conditions:
  - Score decomposition identity fails numerically/algebraically.
  - Projection map is not contractive in required norm.

---

## 48-hour plan (as reported)

1. **0–6h**: infrastructure + TSSOS on full polynomial/constraints.
2. **6–14h**: parametric slice SOS with margin tracking + Lipschitz test.
3. **14–24h**: cumulant-coordinate computation and numerical convexity/superadditivity checks.
4. **24–36h**: score-projection numerical probing on random pairs.
5. **36–48h**: extract certificate(s), rationalize/verify, write closure or frontier.

---

## Contamination / source notes in response

- The response listed external references used for route generation (MSS, Arizmendi-Perales, Gribinski, Shlyakhtenko-Tao, Arizmendi-Johnston, TSSOS, SONC/SAGE, DSOS/SDSOS, Schur-Horn preprint, etc.).
- It explicitly stated:
  - no direct solution found for the target question,
  - finite de Bruijn link to `Phi_n` remains a key literature gap.

---

## Integration note

This transcript is **scout guidance only**. It is not theorem-level closure evidence.
Adoption into lane claims requires independent reproducible artifacts under `P04/experiments/` and synchronized updates in `P04/answer.md` and `P04/audit.md`.

