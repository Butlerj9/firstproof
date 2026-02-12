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

## What is established

- G0 formalization completed.
- G1 dependency map completed.
- G2 route map completed.
- E3 dependency ledger completed (this update).

## What is unresolved

- Statement-level closure of exponential moment bounds (step A4).
- Wick calculus under translation in 3D renormalized regime (step A3).
- Any proof-level closure of quasi-invariance or singularity.
