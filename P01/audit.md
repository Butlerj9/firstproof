# Audit: P01 — Φ⁴₃ measure quasi-invariance

## G0 Formalize

**Status**: ✅ Complete.

### Problem restatement

Let μ be the **Φ⁴₃ measure** on S'(T³) (Schwartz distributions on the 3-torus), defined formally as:

$$d\mu(\phi) = \frac{1}{Z} \exp\left(-\int_{T^3} \left(\frac{1}{4}:\!\phi^4\!: + \frac{m^2}{2}:\!\phi^2\!:\right) dx\right) d\mu_{\text{GFF}}(\phi)$$

where:
- μ\_GFF is the Gaussian free field on T³ (massive, with mass m > 0)
- :φ^k: denotes Wick-ordered (renormalized) powers
- Z is a normalization constant
- The measure exists rigorously by Hairer (2014) regularity structures or Barashkov-Gubinelli (2020) variational method

Let ψ ∈ C^∞(T³) be a smooth function, and T\_ψ : φ ↦ φ + ψ the translation operator.

**Question**: Is μ **quasi-invariant** under T\_ψ? That is, are μ and (T\_ψ)\*μ mutually absolutely continuous?

**Success criteria**:
- YES (EQUIVALENT): Exhibit a Radon-Nikodym derivative d(T\_ψ)\*μ/dμ and prove it is in L¹(μ)
- NO (SINGULAR): Prove μ ⊥ (T\_ψ)\*μ via support/energy argument

### Object glossary

| Symbol | Type | Definition |
|--------|------|------------|
| T³ | Manifold | 3-dimensional torus (R/Z)³ |
| S'(T³) | Topological vector space | Schwartz distributions on T³ |
| μ\_GFF | Gaussian measure on S'(T³) | Gaussian free field with covariance (−Δ + m²)⁻¹ |
| :φ^k: | Renormalized power | Wick-ordered product; removes UV divergences |
| μ (Φ⁴₃) | Non-Gaussian probability measure | Φ⁴₃ measure; exists rigorously |
| ψ | C^∞(T³) | Smooth test function (shift direction) |
| T\_ψ | Translation operator | T\_ψ(φ) = φ + ψ |
| Quasi-invariance | Property | μ ≪ (T\_ψ)\*μ AND (T\_ψ)\*μ ≪ μ |

### Key mathematical structure

Under the shift φ → φ − ψ:

(φ − ψ)⁴ − φ⁴ = −4φ³ψ + 6φ²ψ² − 4φψ³ + ψ⁴

With Wick ordering, the shifted potential involves:
1. :φ³:·ψ — most singular (φ ∈ C^{−1/2−ε}, so :φ³: ∈ C^{−3/2−ε}, product with ψ ∈ C^∞ is marginal)
2. :φ²:·ψ² — less singular (well-defined)
3. φ·ψ³ — distribution × smooth (well-defined)
4. ψ⁴ — smooth (deterministic constant)

**Critical integrability**: The Radon-Nikodym derivative involves exp(c ∫ :φ³: ψ dx). Whether this exponential is in L¹(μ) is the core analytic challenge.

### Truth mode

- [x] LEAN YES (70% YES / 30% NO)
- YES lean: The Gaussian part (μ\_GFF) is quasi-invariant by Cameron-Martin. The interaction :φ⁴: adds integrability requirements that seem manageable given the regularity of ψ.
- NO lean: The :φ³:ψ term might not be integrable in exponential form. In 3D, the regularity structure is at the edge of what works.

### Counterexample shape

- **NO evidence**: Show that exp(c ∫ :φ³: ψ dx) ∉ L¹(μ) for some specific ψ, using moment bounds or variational arguments.

## G1 Background

**Status**: ⚠️ BLOCKED — critical references not accessible.

### Critical external dependencies

| Reference | Status | Need | Blocking? |
|-----------|--------|------|-----------|
| Hairer (2014), "A theory of regularity structures" | ❌ Not sourced | Φ⁴₃ construction, regularity class of samples | YES |
| Barashkov-Gubinelli (2020), Duke Math J. | ❌ Not sourced | Variational construction, most accessible path | YES |
| Albeverio-Kusuoka (2021) | ❌ Not sourced | Invariant measure properties, flow | YES |
| Cameron-Martin theorem | ✅ Known | GFF quasi-invariance (baseline) | No |
| Wick ordering / renormalization | ✅ Basic concepts known | Product definitions | No |
| Besov space regularity | ✅ Basic known | Sample regularity C^{-1/2-ε} | No |

**Blocked items**: 3 of 6 (above the ≤3 threshold).

### Known facts (without references)

1. Φ⁴₃ measure exists rigorously (Hairer 2014, Barashkov-Gubinelli 2020).
2. Typical samples: φ ∈ C^{−1/2−ε}(T³) — Hölder-Besov regularity.
3. The GFF μ\_GFF IS quasi-invariant under shifts by H¹ functions (Cameron-Martin).
4. The Radon-Nikodym derivative for GFF shifts has a known explicit form (Girsanov-type).
5. For the interaction term, the shifted potential involves :φ^k: products with smooth ψ.

### Assessment

The background is partially accessible from general knowledge, but the specific integrability results (whether exp(∫ :φ³:ψ) ∈ L¹(μ)) require specialized bounds from the references listed above. Without access to Barashkov-Gubinelli or Albeverio-Kusuoka, we cannot verify the key technical claim.

## G2 Route map

**Status**: ✅ Routes identified, execution blocked.

### Route A: Cameron-Martin + perturbation (YES direction)

1. Factor the Radon-Nikodym derivative: d(T\_ψ)\*μ/dμ = (Gaussian RN) × (interaction correction)
2. The Gaussian part is standard Cameron-Martin
3. The interaction correction involves exp(difference of potentials)
4. Expand (φ−ψ)⁴ − φ⁴ with Wick ordering
5. Show the exponential of the difference is in L¹(μ) using:
   - Moment bounds for :φ³: from the Φ⁴₃ theory
   - Variational estimates (Barashkov-Gubinelli approach)

**Gap**: Step 5 requires deep results from the references.

### Route B: Singularity argument (NO direction)

1. Construct a measurable set A with μ(A) = 1 but (T\_ψ)\*μ(A) = 0
2. Use energy functional arguments: the :φ⁴: interaction penalizes certain configurations
3. Show that the shift T\_ψ moves mass to a set of μ-measure zero

**Assessment**: This route seems less likely. The :φ⁴: interaction is a "soft" perturbation, and quasi-invariance typically survives such perturbations for smooth shifts.

### Route C: Direct variational bound (YES direction, alternative)

1. Use the Barashkov-Gubinelli variational characterization
2. Show that the shifted measure satisfies the same variational principle
3. Conclude quasi-invariance from uniqueness

**Gap**: Requires detailed knowledge of the variational framework.

## Decision: PARK

**Rationale**:
- 3+ critical external dependencies blocked (Hairer, Barashkov-Gubinelli, Albeverio-Kusuoka)
- The core technical challenge (integrability of exp(∫ :φ³:ψ)) cannot be resolved without specialized bounds from these references
- Routes are identified but execution is blocked
- RED priority problem with HIGH autonomy risk
- Budget better spent on problems with higher probability of closure

**Documented routes for potential future attempt**:
- Route A (Cameron-Martin + perturbation) is most promising
- Key unresolved technical question: Is exp(c ∫ :φ³:ψ dx) in L¹(Φ⁴₃)?
- If references are sourced, Route A could potentially proceed to G3-G5

## Human interventions

| Timestamp | Type | Action | Justification |
|-----------|------|--------|---------------|
| 2026-02-10 | ADMIN | Producer instructed G0-G2 feasibility pass | Scheduling/priority |

## Metrics

| Metric | Value |
|--------|-------|
| Messages used | ~2 |
| Gate | G2 (route map) |
| Status | ❌ Parked (blocked on references) |
| Budget | 30-80 messages (GREEN — ~2 used) |
