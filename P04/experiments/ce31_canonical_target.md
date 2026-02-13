# CE-31: Canonical Target Memo — P04 General n=4 Closure

Date: 2026-02-12
Status: ACTIVE

---

## 1. Notation (FROZEN)

| Symbol | Definition | Domain |
|--------|-----------|--------|
| σ₁, σ₂ | σᵢ = -aᵢ > 0, where aᵢ is the x² coefficient of centered quartic pᵢ | (0, ∞) |
| σₕ | σₕ = σ₁ + σ₂ (additive under ⊞₄) | (0, ∞) |
| w | w = σ₁/σₕ ∈ (0, 1), weight parameter | (0, 1) |
| b₁, b₂ | x¹ coefficients of p₁, p₂ (additive: bₕ = b₁ + b₂) | ℝ |
| c'₁, c'₂ | Shifted x⁰ coefficients: c'ᵢ = cᵢ - aᵢ²/12 = cᵢ - σᵢ²/12 (additive: c'ₕ = c'₁ + c'₂) | ℝ |
| βᵢ | βᵢ = bᵢ²/σᵢ³, dimensionless b-parameter | [0, 4/27) |
| uᵢ | uᵢ = 27bᵢ²/(4σᵢ³) = (27/4)βᵢ, normalized | [0, 1) |

**Quartic form**: pᵢ(x) = x⁴ - σᵢx² + bᵢx + (σᵢ²/12 + c'ᵢ)

**Convolution**: h = p₁ ⊞₄ p₂ has (σₕ, bₕ, c'ₕ) = (σ₁+σ₂, b₁+b₂, c'₁+c'₂).

---

## 2. Closed-form Φ₄

For f(x) = x⁴ + ax² + bx + c with discriminant Δ > 0 and A·B < 0:

$$\Phi_4(f) = \frac{-4(a² + 12c)(2a³ - 8ac + 9b²)}{\Delta}$$

Equivalently: 1/Φ₄ = -Δ/(4AB) where A = a²+12c, B = 2a³-8ac+9b².

In additive variables (σ, b, c'):
- a = -σ, c = σ²/12 + c'
- A = σ² + 12(σ²/12 + c') = 2σ² + 12c'
- B = -2σ³ + 8σ(σ²/12 + c') + 9b² = -2σ³ + 2σ³/3 + 8σc' + 9b² = -(4σ³/3) + 8σc' + 9b²

**Validity domain** (real-rooted with simple roots):
- Δ > 0 (0 or 4 real roots)
- A·B < 0 (selects 4 real roots; equivalently 1/Φ₄ > 0)

---

## 3. Target inequality — Two equivalent forms

### Form A: Superadditivity of 1/Φ₄

$$M(w, b_1, b_2, c'_1, c'_2) := \frac{1}{\Phi_4(\sigma_h, b_h, c'_h)} - \frac{1}{\Phi_4(\sigma_1, b_1, c'_1)} - \frac{1}{\Phi_4(\sigma_2, b_2, c'_2)} \geq 0$$

where σ₁ = w, σ₂ = 1-w (WLOG σₕ = 1 by scale invariance).

### Form B: Parametric margin

$$M(\theta) := M(w, b_1, b_2, \theta c'_1, \theta c'_2) \geq 0 \quad \forall \theta \in [0, 1]$$

### Equivalence proof

Form A at general (c'₁, c'₂) ⟺ Form B at θ = 1.

Form B is stronger: it asserts M ≥ 0 along the entire ray from the c'=0 hyperplane (θ=0) to the target point (θ=1). By the proof chain below, Form B follows from:
1. M(0) ≥ 0 — **PROVED** (§9.6 of answer.md: c'=0 subcase)
2. M''(θ) ≥ κ > 0 — parametric c'-convexity
3. 2κ·M(0) ≥ M'(0)² — discriminant bound

Steps (1)+(2)+(3) ⟹ M(θ) ≥ M(0) + M'(0)θ + ½κθ² ≥ 0, since the quadratic lower bound has non-positive discriminant (M'(0)² - 4·(κ/2)·M(0) = M'(0)² - 2κM(0) ≤ 0).

---

## 4. Domain constraints (FROZEN)

For each component (σᵢ, bᵢ, c'ᵢ) and the sum (σₕ, bₕ, c'ₕ), we require:

1. **Discriminant positive**: Δ(σ, b, c') > 0
2. **Real-rootedness selector**: A(σ, c')·B(σ, b, c') < 0

At c' = 0:
- A₀ = 2σ² > 0
- B₀ = -(4σ³/3) + 9b² = -(4σ³)(1 - 27b²/(4σ³))/3
- B₀ < 0 iff 27b² < 4σ³ (i.e., β < 4/27)
- Δ₀ > 0 iff β < 4/27 (coincides)

So at c' = 0: validity ⟺ β = b²/σ³ < 4/27 for each component and the sum.

For general c': the validity region is more complex but fully characterized by the two conditions above.

---

## 5. Proved subcases

| Subcase | Status | Reference |
|---------|--------|-----------|
| n = 2 | PROVED (equality) | §4 |
| n = 3 general | PROVED | §4c (Φ₃ closed-form + Jensen) |
| n = 4, b = 0 (even quartics) | PROVED | §9.4 (convexity in w + algebraic decomposition) |
| n = 4, c' = 0 | PROVED | §9.6 (g(β) concave + weighted Jensen + gap lemma) |
| n = 4, general | **OPEN** — this memo's target | |

---

## 6. Proof chain target (symbolic)

### Step 1: M(0) ≥ 0 — PROVED
The c'=0 superadditivity (§9.6).

### Step 2: M''(θ) ≥ κ(w,b₁,b₂) > 0 for all valid θ
Compute M''(θ) = (c'₁+c'₂)²·f''_h(θ) - c'₁²·f''₁(θ) - c'₂²·f''₂(θ)
where f''ᵢ(θ) = d²(1/Φ₄)/dc'² evaluated at c' = θ·c'ᵢ.

Each f''ᵢ < 0 (individual concavity in c', CE-29d: 95K tests).
Need: "parts more concave than whole" — superadditivity of |f''|.

At θ=0: reduces to φ-subadditivity (CE-30b, 153K tests, 0 violations).
At general θ: M''(θ) not monotone in θ (CE-30b), but always > 0 (122K tests).

### Step 3: 2κ·M(0) ≥ M'(0)²
60K tests, 0 violations (CE-29c). min slack = 6.88e-9.

### Assembly: Steps 1+2+3 ⟹ M(θ) ≥ 0 for all valid θ.

---

## 7. Known obstructions to symbolic proof

1. **M''(θ) structure**: At θ=0, M''(0) reduces via Titu's lemma to φ-subadditivity. The φ-subadditivity polynomial has 1612 terms, total degree 34 (CE-30c).
2. **M''(θ) at θ>0**: Not monotone or convex in θ (CE-30b). Cannot reduce to θ=0 case.
3. **Full polynomial P**: 837 terms, degree 14, 5 variables (CE-29). Negative outside validity domain → constrained SOS.
4. **Joint concavity**: ψ(u,v) NOT jointly concave (CE-27, 5028 violations).
5. **13 failed routes**: See answer.md barrier summary.

---

## 8. This cycle's approach priority

1. **Symbolic M''(θ) ≥ 0**: Factor and decompose M''(θ) as function of (w, b₁, b₂, θ, c'₁, c'₂). Look for structural decomposition (Cauchy-Schwarz, trace inequalities, matrix PSD).
2. **Symbolic discriminant bound**: Prove 2·min_θ(M'')·M(0) ≥ M'(0)² by expressing both sides in canonical form.
3. **Interval certification fallback**: If symbolic proof stalls, certify M ≥ 0 on compact normalized domain using rigorous interval arithmetic with outward rounding.
