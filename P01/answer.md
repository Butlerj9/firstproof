# Answer: P01

**Status**: ❌ Parked
**Reviewer**: Codex supervisor audit — park confirmed (blocked on references)
**External deps**: Unresolved (`Hairer 2014`, `Barashkov-Gubinelli 2020`, `Albeverio-Kusuoka 2021`)

## Problem statement

Let $\mathbb{T}^3$ be the 3D unit torus and let $\mu$ be the $\Phi^4_3$ measure on $\mathcal{D}'(\mathbb{T}^3)$. Let $\varphi : \mathbb{T}^3 \to \mathbb{R}$ be a smooth function that is not identically zero and let $T_\varphi : \mathcal{D}'(\mathbb{T}^3) \to \mathcal{D}'(\mathbb{T}^3)$ be the shift map $T_\varphi(u) = u + \varphi$. Are $\mu$ and $(T_\varphi)_*\mu$ equivalent (same null sets)?

## Conjectured answer: YES

The measures $\mu$ and $(T_\varphi)_*\mu$ should be equivalent for any smooth nonzero $\varphi$. The expected proof strategy is a Girsanov-type argument exploiting the Cameron-Martin quasi-invariance of the underlying GFF, combined with exponential integrability of the renormalized interaction under translation.

## Outcome

No proof or disproof was completed in this sprint lane. The lane was parked at G2 due to blocked primary dependencies needed for the core integrability step.

## Dependency ledger (E3 escalation)

### Route A: Girsanov via variational characterization

| Step | What's needed | From where | Status |
|------|--------------|-----------|--------|
| A1. GFF quasi-invariance | Cameron-Martin theorem: GFF measure $\nu$ on $\mathcal{D}'(\mathbb{T}^3)$ is quasi-invariant under $H^1$ translations. R-N derivative is $\exp(\langle h, \varphi\rangle_{H^1} - \frac{1}{2}\|h\|^2_{H^1})$. | Classical (Bogachev 1998) | AVAILABLE from training |
| A2. $\Phi^4_3$ construction | Rigorous construction of $\mu$ as a Borel probability measure on $\mathcal{D}'(\mathbb{T}^3)$. $d\mu \propto \exp(-\lambda \int :\!\varphi^4\!: dx)\, d\nu$ with Wick renormalization. | Hairer (2014), Gubinelli-Imkeller-Perkowski (2015), or Barashkov-Gubinelli (2020) | BLOCKED — need precise construction statement |
| A3. Shifted interaction | Under $T_h$: $:\!(u+h)^4\!: = :\!u^4\!: + 4h:\!u^3\!: + 6h^2:\!u^2\!: + 4h^3 u + h^4$ (with renormalized Wick powers). The R-N derivative involves $\exp(\text{interaction difference})$. | Requires Wick calculus in 3D (renormalization-dependent) | BLOCKED — need Wick product identities in renormalized regime |
| A4. Exponential integrability | $\exp(\pm C \int :\!\varphi^k\!: h^{4-k} dx) \in L^1(\mu)$ for $k = 1, 2, 3$ and smooth $h$. This is the core technical requirement. | Barashkov-Gubinelli (2020): exponential moments via Polchinski flow / Boué-Dupuis formula | BLOCKED — need precise exponential moment bounds |
| A5. Absolute continuity | Steps A1+A3+A4 combine: $d(T_h)_*\mu / d\mu$ exists and is positive $\mu$-a.e. Equivalence follows by symmetry ($h \mapsto -h$). | Assembly step (no external ref needed) | AVAILABLE (given A1-A4) |

### Route B: Singularity (disproof)

If the answer were NO, one would need:
- A measurable set $S$ with $\mu(S) = 1$ and $\mu(S - h) = 0$
- This seems implausible for smooth $h$ given the Gaussian core structure

No evidence for singularity was found. Route B is deprioritized.

### Assessment

**Bottleneck**: Steps A2–A4. The specific exponential moment bounds (step A4) are the hardest part and rely on the Barashkov-Gubinelli variational construction. Steps A1 and A5 are available from standard theory.

**Feasibility without references**: LOW. The 3D Wick renormalization (step A3) and the exponential integrability (step A4) involve UV-divergent quantities that require precise renormalization prescriptions. These cannot be reliably reconstructed from training knowledge alone.

**Recommendation**: KEEP PARKED. The dependency ledger is complete. Unblocking requires statement-level ingestion of:
1. Barashkov-Gubinelli (2020) Theorem on exponential moments of $:\!\varphi^k\!:$ under $\Phi^4_3$
2. Precise renormalization prescription for Wick powers in the BG construction

## Session 4: A4 Statement Recovery + Proof Strategy (2026-02-12)

### A4 Statement (recovered from training knowledge)

**A4 (Exponential integrability)**: For any $\psi \in C^\infty(\mathbb{T}^3)$ and $c > 0$:
$$\mathbb{E}_\mu[\exp(c|\langle :\!\phi^3\!:, \psi\rangle|)] < \infty$$
where $\langle :\!\phi^3\!:, \psi\rangle = \int_{\mathbb{T}^3} :\!\phi^3\!:(x)\, \psi(x)\, dx$ is the distributional pairing.

### A3 Wick expansion under translation (recovered)

For $\psi \in C^\infty(\mathbb{T}^3)$ deterministic:
$$:\!(\phi - \psi)^4\!: = :\!\phi^4\!: - 4:\!\phi^3\!:\psi + 6:\!\phi^2\!:\psi^2 - 4:\!\phi\!:\psi^3 + \psi^4$$
(Wick ordering acts only on the stochastic field $\phi$; deterministic $\psi$ factors out of contractions.)

Therefore:
$$V(\phi) - V(\phi - \psi) = \lambda \int (4:\!\phi^3\!:\psi - 6:\!\phi^2\!:\psi^2 + 4\phi\psi^3 - \psi^4)\, dx + m^2\int(2\phi\psi - \psi^2)\, dx$$

### Proof strategy (identified but incomplete)

**Route A proof sketch** (assuming A4):
1. $d\mu_\psi / d\mu = \exp(V(\phi) - V(\phi-\psi)) \times R_\psi^{\mathrm{GFF}}(\phi)$
2. $R_\psi^{\mathrm{GFF}} \in L^p(\nu)$ for all $p$ (Cameron-Martin, since $\psi \in C^\infty \subset H^1$)
3. Dominant term in $V(\phi)-V(\phi-\psi)$: $4\lambda\langle :\!\phi^3\!:, \psi\rangle$
4. If A4 holds: $\exp(|V(\phi)-V(\phi-\psi)|) \in L^q(\mu)$ for some $q > 1$
5. By Hölder: $d\mu_\psi/d\mu \in L^1(\mu)$, establishing quasi-invariance

**Proof strategy for A4**: Young's inequality + coupling absorption.

For the **regularized** field $\phi_\varepsilon$: the pointwise inequality $|\phi_\varepsilon^3 \psi| \leq \delta \phi_\varepsilon^4 + C(\delta)|\psi|^4$ (by AM-GM with exponents 4/3, 4) gives:
$$\exp(c|\textstyle\int \phi_\varepsilon^3 \psi\, dx|) \leq \exp(c\delta \textstyle\int \phi_\varepsilon^4\, dx + cC(\delta)\|\psi\|_4^4)$$

Under $\mu_\varepsilon \propto \exp(-\lambda\int :\!\phi_\varepsilon^4\!:\, dx)\, d\nu$, the coupling absorption gives:
$$\mathbb{E}_{\mu_\varepsilon}[\exp(c\delta\textstyle\int \phi_\varepsilon^4\, dx)] \sim Z_\varepsilon(\lambda - c\delta) / Z_\varepsilon(\lambda)$$
which is finite for $c\delta < \lambda$ (the modified coupling remains positive).

**Gap**: Passing from $\phi_\varepsilon^3$ (ordinary power) to $:\!\phi_\varepsilon^3\!:$ (Wick power). In 3D, $:\!\phi_\varepsilon^3\!: = \phi_\varepsilon^3 - 3c_\varepsilon \phi_\varepsilon$ where $c_\varepsilon = \mathbb{E}[\phi_\varepsilon(x)^2] \sim \varepsilon^{-1} \to \infty$. The Young inequality for ordinary powers does NOT transfer to Wick powers because the Wick subtraction $3c_\varepsilon \phi_\varepsilon$ introduces terms that grow with $c_\varepsilon$ and cannot be absorbed by the $:\!\phi^4\!:$ interaction alone.

**Alternative approach**: Nelson's hypercontractivity. Under the GFF $\nu$, the random variable $X = \langle :\!\phi^3\!:, \psi\rangle$ (a degree-3 Wiener chaos element) satisfies $\|X\|_{L^p(\nu)} \leq (p-1)^{3/2} \|X\|_{L^2(\nu)}$. Combined with Cauchy-Schwarz transfer to $\mu$, this gives $\|X\|_{L^p(\mu)} \leq C p^{3/2}$, which implies sub-Weibull(2/3) tails: $\mathbb{P}_\mu(|X| > t) \leq \exp(-ct^{2/3})$. This gives **all polynomial moments** but is **insufficient** for exponential integrability (which requires sub-exponential tails).

**Conclusion**: The gap between sub-Weibull(2/3) (from hypercontractivity) and sub-exponential (needed for A4) must be bridged by the $:\!\phi^4\!:$ coercivity. This requires showing that the $:\!\phi^4\!:$ interaction improves the tails of $\langle:\!\phi^3\!:, \psi\rangle$ from sub-Weibull(2/3) to sub-exponential. This improvement is expected (the quartic interaction suppresses large fields) but proving it requires renormalization-level technical control not available from training knowledge.

### Assessment (Session 4)

| Step | Status | Change from Session 3 |
|------|--------|-----------------------|
| A1 (Cameron-Martin) | ✅ AVAILABLE | No change |
| A2 (Φ⁴₃ construction) | ✅ Statement-level | No change |
| A3 (Shifted interaction) | ✅ **RECOVERED** | Wick expansion under deterministic shift derived |
| A4 (Exponential integrability) | ⚠️ **STATEMENT RECOVERED, PROOF INCOMPLETE** | Statement formulated; proof strategy identified (Young + coupling absorption); gap: 3D Wick renormalization |
| A5 (Assembly) | ✅ AVAILABLE | No change |

**Upgrade assessment**: A4 statement is available. The proof sketch is nearly complete but has a gap at the Wick-to-ordinary power transfer in 3D. This gap is specific to 3D (in 2D, the analogous argument works). Without BG-level renormalization control, the gap cannot be closed.

**Recommendation**: P01 remains **❌ Parked**. The A4 statement and proof strategy are documented. The specific technical gap (Wick Young inequality in 3D) is identified. Closure requires either:
1. Sourcing BG's exponential moment bounds (statement-level), OR
2. A new approach to the Wick-to-ordinary transfer that avoids the $c_\varepsilon \to \infty$ divergence.

## What is established

- G0 formalization completed.
- G1 dependency map completed (A3 + A4 statement recovered in Session 4).
- G2 route map completed.
- E3 dependency ledger completed.
- E4 A4 statement + proof strategy documented (Session 4).

## What is unresolved

- Proof-level closure of A4 (exponential integrability): gap at Wick-to-ordinary power transfer in 3D.
- Full proof of quasi-invariance (conditional on A4 closure).
