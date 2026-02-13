# GPT-pro Transcript — P04 (Round 2, condensed archival)

Date captured: 2026-02-13  
Source: user-provided GPT-pro response (manual paste)  
Lane: P04  
Intent: archive latest scout route-map and execution bridge lemmas.

---

## Topline map from scout

- Open target remains: general `n=4` case (`b != 0`, `c' != 0`).
- Exact blocker remains certificate-level nonnegativity (CE-30/SOS gap).
- New bridge: invariant reduction + `sqrt(sigma)` reparameterization.
- Verdict in response: `BLOCKED_WITH_FRONTIER`, but with a much sharper frontier object.

---

## SECTION A (as reported)

| Lane | StatusBefore | BestNewBridgeLemma | KillTest | Verdict | Why |
|---|---|---|---|---|---|
| P04 | BLOCKED_WITH_FRONTIER | Reduce to two degree-22 polynomials `P_+`, `P_-` in reduced variables with explicit semialgebraic constraints; numerator quadratic in sign bit `r`, with fully factored `r^2` coefficient | Construct `P_±`; reject if degree/term explosion or true interior negative found | BLOCKED_WITH_FRONTIER | Problem now concentrated into two explicit constrained positivity certificates |

---

## Core new algebraic reduction (as reported)

1. Use centered-quartic invariants (`I, J, K`) in `(sigma, b, c')` coordinates.
2. Normalize scale with `t = I/sigma^2`, `s = J/sigma^3`.
3. Use `sigma_i = alpha_i^2`, `alpha^2 + beta^2 = 1` to remove fractional mixing weights.
4. Parameterize `b_i` via `x_i^2 = 27 b_i^2 / sigma_i^3`.
5. Margin becomes `g_h >= alpha^2 g_1 + beta^2 g_2` with explicit reduced formulas.
6. Cleared numerator is quadratic in sign parameter `r in {+1,-1}`; check both `P_+`, `P_-`.

Scout claim: this materially shrinks the frontier versus the prior raw degree-34 object.

---

## Top 3 routes prioritized in response

1. **Approach 1 (fastest)**: invariant reduction + `P_±` + constrained SOS/Positivstellensatz.
2. **Approach 2**: trig/resolvent-cubic angle parameterization (`cos(3theta)`).
3. **Approach 3**: Ferrari two-quadratic decomposition as domain simplifier.

---

## Claude Code handoff block in response (high-level)

Script intent from scout:

1. `p04_reduce_invariants.py`  
   - Build reduced margin symbolically, confirm degree/terms, extract/factor `[r^2]`.
2. `p04_numeric_killtest.py`  
   - Random + local feasible-domain search for sign violations in `P_±`.
3. `p04_sos_poscert.py`  
   - Attempt constrained SOS/Positivstellensatz with reduced constraints.

Stop-loss in scout:

- If reduced object still explodes, abandon this route.
- If robust interior negative appears, escalate as potential counterexample.
- If SOS fails at low multipliers, switch to boundary-minimizer/CAD route instead of blind degree escalation.

---

## Integration note

This transcript is scout guidance only, not closure evidence.
Any theorem-level claim still requires reproducible lane artifacts in `P04/experiments/` and synchronized updates in `P04/answer.md` + `P04/audit.md`.

