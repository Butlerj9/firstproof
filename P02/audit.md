# Audit: P02 — Rankin–Selberg integral nonvanishing in Whittaker models

## G0 Formalize

**Status**: ✅ Complete.

### Problem restatement

Let F be a non-archimedean local field with ring of integers o. Let:
- N_r = upper-triangular unipotent subgroup of GL_r(F)
- ψ : F → C× a nontrivial additive character of conductor o, identified with a generic character of N_r
- Π a generic irreducible admissible representation of GL_{n+1}(F), realized in its ψ⁻¹-Whittaker model W(Π, ψ⁻¹)
- π a generic irreducible admissible representation of GL_n(F), realized in its ψ-Whittaker model W(π, ψ)
- q the conductor ideal of π, Q ∈ F× a generator of q⁻¹
- u_Q := I_{n+1} + Q · E_{n,n+1} ∈ GL_{n+1}(F)

**Question**: Must there exist W ∈ W(Π, ψ⁻¹) such that for some V ∈ W(π, ψ), the local Rankin–Selberg integral

∫_{N_n\GL_n(F)} W(diag(g,1) · u_Q) · V(g) · |det g|^{s-1/2} dg

is finite and nonzero for all s ∈ C?

**Quantifier structure**: ∃W ∈ W(Π,ψ⁻¹) such that ∀ generic irreducible admissible π of GL_n(F), ∃V ∈ W(π,ψ) such that the integral is finite and nonzero for all s ∈ C.

**Note on interpretation**: The problem statement is slightly ambiguous about the quantifier order for π. Two readings:
- (A) ∃W such that ∀π ∃V: the integral converges and is nonzero ∀s.
- (B) For each π, ∃W (possibly depending on π) ∃V: the integral converges and is nonzero ∀s.

The problem says "Must there exist W ∈ W(Π,ψ⁻¹) with the following property?" then defines the property involving π,V. The most natural reading is (A): a single W works for all π.

### Object glossary

| Symbol | Type | Definition |
|--------|------|------------|
| F | Non-archimedean local field | e.g. Q_p or F_q((t)) |
| o | Ring of integers in F | Maximal compact subring |
| ψ : F → C× | Additive character | Conductor o (i.e. ψ trivial on o, nontrivial on ϖ⁻¹o) |
| N_r | Unipotent subgroup of GL_r(F) | Upper-triangular unipotent matrices |
| Π | Smooth representation of GL_{n+1}(F) | Generic, irreducible, admissible |
| W(Π,ψ⁻¹) | Whittaker model | Realization of Π as functions W : GL_{n+1}(F) → C with W(ng) = ψ⁻¹(n)W(g) |
| π | Smooth representation of GL_n(F) | Generic, irreducible, admissible |
| q | Conductor ideal of π | Measures ramification |
| u_Q | Matrix in GL_{n+1}(F) | I_{n+1} + Q·E_{n,n+1} where Q generates q⁻¹ |
| Rankin–Selberg integral | Zeta integral | Standard local RS integral with modification by u_Q |

### Key mathematical structure

The standard local Rankin–Selberg integral (Jacquet–Piatetski-Shapiro–Shalika) is

Ψ(s, W, V) = ∫_{N_n\GL_n(F)} W(diag(g,1)) · V(g) · |det g|^{s-1/2} dg

This integral converges for Re(s) >> 0 and has meromorphic continuation. The L-factor L(s, Π × π) is the GCD of such integrals.

The modification here is W(diag(g,1) · u_Q) instead of W(diag(g,1)). The element u_Q is a "conductor-dependent" unipotent perturbation. This is related to:
1. The theory of newforms/essential vectors in GL_n Whittaker models
2. The conductor exponent and ε-factor of pairs
3. Possibly the "local converse theorem" or "stability of γ-factors"

The question asks whether a SINGLE W can make the integral entire (no poles) and nonzero for ALL s, uniformly in π.

### Truth mode

- [x] EXPLORE BOTH (55% YES / 45% NO)
- YES lean: For the standard RS integral (without u_Q), it's known that suitable choices of W, V can make the integral equal to L(s, Π×π). The modification by u_Q likely relates to newform theory and may simplify the integral. A "new vector" W might work universally.
- NO lean: The requirement that the integral is nonzero for ALL s ∈ C (not just convergent and nonzero in a half-plane) is very strong. The integral typically has poles related to L(s, Π×π). Achieving entirety AND nonvanishing for all s with a single W seems demanding.

### Counterexample shape

- **NO evidence**: Exhibit specific Π (e.g., principal series of GL_3(Q_p)) and specific π (e.g., with particular conductor) such that for every W ∈ W(Π,ψ⁻¹), the modified RS integral either has a pole or vanishes at some s₀ ∈ C.

### Experiment plan

| Phase | Task | Pass/Fail |
|-------|------|-----------|
| EXP-1 | For GL_2 × GL_1 (n=1), compute the modified integral explicitly for principal series | Tractable → PASS |
| EXP-2 | Check the u_Q modification for conductor-1 (unramified) π: does u_Q = I restore the standard integral? | Consistent → PASS |
| EXP-3 | Literature check: connection to Jacquet–Shalika newform theory, essential vectors | Found → helps route selection |

## G1 Background

**Status**: ⚠️ Partially accessible.

### Critical external dependencies

| Reference | Status | Need | Blocking? |
|-----------|--------|------|-----------|
| Jacquet–Piatetski-Shapiro–Shalika (JPSS), local RS integrals | ✅ Known (basic theory) | Standard integral, meromorphic continuation, L-factor as GCD | No |
| Jacquet–Shalika, newforms for GL_n | ⚠️ Partial knowledge | Essential vector, conductor | Partially |
| Cogdell–Piatetski-Shapiro, local converse theorem | ⚠️ Statement known, details not | Stability of γ-factors | Partially |
| Matringe (2013), essential Whittaker functions | ❌ Not sourced | May contain the key construction | YES |
| Jacquet (2009), archimedean RS theory | ❌ Not sourced | Comparison point | No |
| JPSS (1981), Conducteur des représentations du groupe linéaire | ❌ Not sourced | Conductor theory, ε-factors | YES |

### Known facts (without references)

1. **Standard RS integral**: For Re(s) >> 0, Ψ(s,W,V) converges absolutely. It has meromorphic continuation to all s as a rational function in q^{-s}.
2. **L-factor**: L(s, Π×π) = GCD of {Ψ(s,W,V) : W ∈ W(Π), V ∈ W(π)}.
3. **Essential vector**: For GL_n, there exists a distinguished "new vector" W₀ in the Whittaker model, characterized by invariance under a specific congruence subgroup.
4. **Conductor of a pair**: The conductor of Π × π measures the ramification of the pair.
5. **ε-factor**: The functional equation involves ε(s, Π×π, ψ) which depends on the conductor.

### Known difficulty: interpretation of u_Q

The element u_Q = I_{n+1} + Q·E_{n,n+1} is a specific unipotent element depending on the conductor of π. This suggests:
- The integral W(diag(g,1)·u_Q) is a "twisted" evaluation of W.
- This may be related to evaluating W at a point determined by π's conductor.
- In newform theory, such evaluations appear in explicit formulas for ε-factors and local integrals at the conductor level.

### Assessment

The problem lives in deep analytic number theory / automorphic forms territory. While the basic framework (RS integrals, Whittaker models) is known to me at a structural level, the specific technical question about the u_Q modification and the entirety/nonvanishing condition requires specialized knowledge from Jacquet–Shalika conductor theory and possibly Matringe's work on essential Whittaker functions. Without access to these references, completing a proof seems unlikely.

**Blocked items**: 2 of 6 references critically needed (Matringe, JPSS conductor theory).

## G2 Route Map

**Status**: ✅ Routes identified; execution blocked.

### Route A: New vector approach (YES direction)

1. Take W = W₀ (new vector / essential vector) for Π.
2. For each π, choose V = V₀ (new vector for π).
3. Show that the modified integral Ψ(s, W₀, V₀, u_Q) simplifies (perhaps to 1 or to a known nonvanishing expression).
4. The u_Q factor may be precisely what's needed to cancel the L-factor poles.

**Key lemma**: W₀(diag(g,1)·u_Q) has a specific factorization or decay property that makes the integral entire.

**Bottleneck**: Step 3 requires explicit computation of the modified integral for specific representations.

**Gap**: We don't have the explicit formulas for W₀ evaluated at unipotent-translated elements.

### Route B: Analytic continuation argument (YES direction)

1. Show that the standard integral Ψ(s,W,V) equals L(s,Π×π) for suitable W,V.
2. Show that the u_Q modification divides out the L-factor (or its poles).
3. Conclude that the modified integral is entire and nonzero.

**Key lemma**: The u_Q twist corresponds to dividing by L(s,Π×π) at the integral level.

**Gap**: This is plausible but requires deep knowledge of the integral's dependence on u_Q.

### Route C: Explicit computation for small n (YES or NO direction)

1. For n=1 (GL_2 × GL_1): compute everything explicitly.
2. For n=2 (GL_3 × GL_2): attempt computation for principal series.
3. Look for patterns or counterexamples.

**Bottleneck**: Even n=1 requires careful Whittaker function computations.

### Route D: Counterexample search (NO direction)

1. For specific Π, π where L(s,Π×π) has a known pole, check if u_Q can neutralize it.
2. If u_Q cannot neutralize all poles simultaneously for varying π, the answer is NO.

**Gap**: This requires understanding how u_Q interacts with L-factor poles.

## G3–G5: Proof development (re-opened after scout escalation)

**Status**: ✅ Complete (n=1 proved; general n structural argument).

### Escalation trigger

P02 was re-opened after P07/P08 resolution freed budget. Scout briefs from the definition-only escalation provided JPSS conductor definition (K₁ congruence subgroup characterization) and Whittaker model structure.

### Route taken: Route A (new vector) + Route C (explicit n=1)

The key breakthrough was the **unipotent absorption identity**:

$$W(\mathrm{diag}(g,1) \cdot u_Q) = \psi^{-1}(Q \cdot g_{nn}) \cdot W(\mathrm{diag}(g,1))$$

This shows the u_Q modification simply introduces an additive character twist in the (n,n)-entry. For n=1, this collapses the integral to a Gauss sum.

**Construction (n=1)**: Choose W via the Kirillov model with φ = 1_{o×} (indicator of units). The integral becomes:

∫_{o×} ψ⁻¹(uQ) · χ(u) d×u = G(χ, ψ_{-c})

This is a conductor-matched Gauss sum, which is always nonzero (|G| = q^{c/2}).

### Experiment results

| Experiment | Description | Result |
|-----------|-------------|--------|
| EXP-1 | Classical Gauss sums |G|² = p for p = 3,5,7,11,13 | ALL PASS |
| EXP-1 | Conductor-matched sums nonzero (p=3,5,7; c=0,1,2,3) | ALL PASS |
| EXP-1 | Mismatched conductors give zero (confirms u_Q essential) | PASS (3/3 zeros) |

### Answer

**YES.** For n=1: proved via Kirillov model + Gauss sum nonvanishing. For general n: structural argument via JPSS ideal theory.

## G6: Self-Review

### G6: CONDITIONAL ACCEPT (general n gap flagged)

1. **n=1 proof (PASS).** Complete and rigorous. Key identity + Kirillov model + Gauss sum nonvanishing. No gaps.

2. **General n argument (GAP).** Steps A-B are rigorous (right-translate invertibility, RS non-degeneracy). Steps C-E rely on the claim that the "partial ideal" (V varying, W' fixed) equals the full L-ideal for generic W'. This is plausible by multiplicity-one but not self-contained.

3. **Direction confirmed.** YES is correct (supported by n=1 proof + structural argument + experiments).

### Current verdict: 🟡 Candidate

The n=1 proof is complete. The general n argument requires the JPSS partial ideal claim. Status is 🟡 (not ✅) because the full generality is not self-contained.

## Decision: 🟡 Candidate

**Rationale**:
- Key identity proved for all n (rigorous). ✓
- n=1 proof complete (Kirillov + Gauss sums). ✓
- General n: structural argument, not fully self-contained. ⚠️
- Experiments: all pass. ✓
- Answer: YES.

## Human interventions

| Timestamp | Type | Action | Justification |
|-----------|------|--------|---------------|
| 2026-02-10 | ADMIN | RED-feasibility blitz | Scheduling/priority |
| 2026-02-11 | ADMIN | Definition-only escalation (scout briefs) | P02 re-opened after P07/P08 resolution |

## Metrics

| Metric | Value |
|--------|-------|
| Messages used | ~8 (2 blitz + 6 proof) |
| Gate | G6 (conditional accept) |
| Status | 🟡 Candidate — YES via Kirillov + Gauss sums (n=1 proved) |
| Tokens (est.) | ~25,000 |
| Budget | 80 messages (RED — ~8 used) |
