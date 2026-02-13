# Claude Research Response — P03

Date captured: 2026-02-12  
Source: User-provided Claude Research Mode response (manual paste)  
Lane: P03  
Integration intent: Archive response for downstream review and reproducible escalation tracking.

---

## Raw Response (verbatim)

# New mathematical routes to the interpolation Macdonald symmetry conjecture

**The most promising path to proving that E\*_{λ⁻}(x; 1, t) is symmetric for all n runs through the October 2025 signed multiline queue formula of Ben Dali–Williams, combined with the probabilistic t-PushTASEP framework of Ayyer–Martin–Williams.** These two recent results provide, for the first time, explicit combinatorial and probabilistic descriptions of the full inhomogeneous interpolation polynomial — the exact object whose lower-degree corrections must be shown symmetric. Fourteen genuinely new approach families emerge from this research, spanning algebraic combinatorics, integrable probability, rational KZ theory, elliptic degeneration, and nonsymmetric plethysm. At least five of these are cross-domain, and none reduces to the twelve previously killed routes.

The conjecture (P03) asserts that E\*_{λ⁻}(x; q=1, t) is a symmetric polynomial in x₁,…,xₙ. Alexandersson–Sawhney (2019) closed the leading-term gap: E_{λ⁻}(x; 1, t) is symmetric and t-independent when λ⁻ is anti-dominant. What remains is showing the inhomogeneous lower-degree correction terms — forced by vanishing at spectral vectors — are also symmetric. Every approach below is evaluated specifically on whether it can close this correction-term gap.

---

## The signed multiline queue formula opens a direct combinatorial attack

Ben Dali and Williams (arXiv:2510.02587, October 2025) proved the first combinatorial formula for nonsymmetric interpolation Macdonald polynomials E\*_μ, expressing them as weighted sums over **signed multiline queues**. This generalizes the Corteel–Mandelshtam–Williams formula for ordinary Macdonald polynomials. The key structural advance: each signed multiline queue encodes both the leading-degree Macdonald contribution and the lower-degree correction terms simultaneously, via sign assignments on ball labels in the queue.

**Approach 1 — Signed multiline queue q=1 analysis.** At q=1, the weighting on multiline queues simplifies dramatically: the q^{maj} statistic collapses to 1 for all fillings, and the queue dynamics lose their asymmetry. The signed layers that generate lower-degree corrections should exhibit enhanced cancellation symmetry at q=1. The concrete strategy: show that at q=1 the signed multiline queue partition function Z\*_λ(x; 1, t) is invariant under permutation of x-variables. This requires proving that for each transposition s_i, the contributions of queues related by permuting columns i and i+1 pair up with matching weights. **Bridge lemma needed**: a signed-queue analog of the "column-swap involution" that Corteel–Mandelshtam–Williams used for the homogeneous case. **Failure mode**: the signs in the interpolation formula may not pair cleanly under column swaps, since interpolation ASEP polynomials lack the circular symmetry that homogeneous ASEP polynomials enjoy — Ben Dali–Williams explicitly note this obstruction. **Viability: HIGH** — this is the most explicit formula available for E\*_μ with all correction terms, and q=1 is precisely where combinatorial simplifications are maximal.

**Approach 2 — Signed tableaux formula at q=1.** Ben Dali–Williams also give a **tableaux formula** (their Section 6) for interpolation Macdonald polynomials. At q=1, fillings lose their descent-statistic dependence, and the tableaux formula may reduce to a manifestly symmetric sum. This is distinct from Approach 1: multiline queues and tableaux are different combinatorial models with different symmetry-breaking patterns. **Bridge lemma**: show the q=1 tableaux weights are invariant under content permutation. **Failure mode**: tableaux formulas tend to be column-strict, which breaks manifest symmetry. **Viability: MEDIUM-HIGH.**

---

## Probabilistic reversibility via the t-PushTASEP provides a physics-based proof strategy

Ayyer, Martin, and Williams (arXiv:2403.10485, 2024) proved that stationary probabilities of the **inhomogeneous multispecies t-PushTASEP** are proportional to ASEP polynomials F_η(x; q, t) at q=1, with partition function equal to P_λ(x; 1, t). The t-PushTASEP is a Markov chain on a ring where particles hop with site-dependent rates x₁,…,xₙ.

**Approach 3 — Interpolation PushTASEP reversibility.** Ben Dali–Williams promise a forthcoming paper [BDW] giving an **interpolation analogue** of the t-PushTASEP probabilistic interpretation at q=1. The key physical insight: at q=1 (symmetric hopping), particle systems generically satisfy **detailed balance**, making the stationary distribution invariant under relabeling of sites. If E\*_{λ⁻}(x; 1, t) arises as a partition function or observable of such a reversible system, its symmetry in x₁,…,xₙ would follow from the interchangeability of site rates. **Bridge lemma**: construct an explicit Markov chain whose stationary distribution encodes E\*_{λ⁻} (including corrections), and prove detailed balance or time-reversibility at q=1. **Failure mode**: the interpolation version may correspond to a process that is NOT reversible even at q=1 — the inhomogeneous corrections could break detailed balance. **Not a variant of any failed approach** — this is genuinely probabilistic, not algebraic. **Viability: HIGH** (contingent on [BDW] results).

**Approach 4 — Multispecies SSEP symmetry transfer.** When q=1, the multispecies ASEP becomes the SSEP (symmetric simple exclusion process), which possesses a powerful **Sₙ symmetry** acting on species labels. Aggarwal–Nicoletti–Petrov (arXiv:2309.11865) give a unified vertex-model framework for colored particle systems; at q=1, the vertex weights become symmetric. If one can formulate the interpolation polynomial as an observable in this symmetric vertex model, the Sₙ-invariance is automatic. **Bridge lemma**: embed the interpolation vanishing conditions into the vertex model framework. **Failure mode**: the vertex model naturally produces homogeneous Macdonald polynomials; inhomogeneous corrections may require boundary conditions that break vertex-model symmetry. **Viability: MEDIUM.**

---

## Rational KZ equations directly involve interpolation polynomials at q=1

**Approach 5 — Kasatani–Takeyama rational KZ connection.** Kasatani and Takeyama (arXiv:0810.2581, 2008) proved that **shifted nonsymmetric Jack polynomials** — which are precisely the q→1 limits of Knop–Sahi interpolation polynomials — arise as solutions to the **rational quantum KZ equation** associated to gl_N. This is a direct, published connection between interpolation polynomials at q=1 and the KZ framework. The rational KZ equation has **monodromy representation** valued in the Hecke algebra. If the monodromy representation acts on the relevant solution component via the trivial (symmetric) character, the polynomial solution must be symmetric. **Bridge lemma**: compute the monodromy representation for the specific KZ solution corresponding to E\*_{λ⁻}(x; 1, t) and show it factors through the sign/trivial representation of Sₙ. **This is NOT the same as the failed "Hecke algebra degeneration" approach** (Route 7 in the killed list), which attempted to use the Hecke algebra structure directly; the KZ approach uses the *monodromy* of a differential equation, which is a fundamentally different invariant. **Failure mode**: the monodromy representation may be non-trivial (reducible but not scalar), so the solution components are vector-valued and the scalar projection need not be symmetric. **Viability: MEDIUM-HIGH** — this is the most mathematically rigorous of the analytic approaches, with a direct published theorem linking the right objects.

---

## Sahi's nonsymmetric binomial theorem offers an algebraic expansion route

**Approach 6 — Binomial expansion at q=1.** Sahi (Duke Math. J. 94, 1998) proved a **nonsymmetric binomial theorem**: E\*_u(ax) = Σ_v E_{u/v}(a) · E\*_v(x), where E_{u/v}(a) are generalized (q,t)-binomial coefficients defined via evaluations at spectral vectors. At q=1, the spectral vectors collapse (from ~C(D+n,n) to n! distinct), and many binomial coefficients E_{u/v}(1,t) should vanish or simplify dramatically. The strategy: show that the q=1 binomial expansion of E\*_{λ⁻} is a linear combination of interpolation polynomials E\*_v(x; 1, t) that is manifestly Sₙ-invariant. **Bridge lemma**: prove that the q=1 binomial coefficients E_{λ⁻/v}(1, t) vanish unless v⁺ = v (i.e., v is itself a partition), and then E\*_v(x; 1, t) is symmetric by induction on degree. **Failure mode**: the denominators M_v(⟨v⟩) in the binomial coefficients may have poles at q=1 due to spectral collision, requiring delicate limiting analysis. The Chen–Sahi paper (arXiv:2403.02490, 2024) proves positivity and monotonicity results for interpolation binomial coefficients that could help control this limit. **Viability: MEDIUM.**

---

## Yang-Baxter eigenvalue degeneracy forces partial symmetry at q=1

**Approach 7 — Cherednik eigenvalue collapse and Yang-Baxter symmetry propagation.** The Cherednik operators Y_i have eigenvalue q^{μ_i} · t^{ρ_i} on E_μ. At q=1, **all eigenvalues become t^{ρ_i}**, depending only on the rank of position i in μ — not on the actual values μ_i. The paper "Hunting the Poles in the Staircases" (arXiv:2601.12881, January 2026) proves a key lemma: when eigenvalues of Y_i and Y_{i+1} coincide, the Yang-Baxter operator forces **M_v to be symmetric in x_i, x_{i+1}**. At q=1 for a partition λ⁻, many pairs of Cherednik eigenvalues coincide. The strategy: show that enough pairwise symmetries (s_i-invariances) are forced by eigenvalue degeneracy to generate the full Sₙ. **Bridge lemma**: for generic t and λ⁻ anti-dominant, show that the pattern of coinciding Cherednik eigenvalues at q=1 generates all of Sₙ (not just a proper subgroup). **Failure mode**: for partitions with all distinct parts, positions i with distinct λ-values may have different ρ-values, so eigenvalues t^{ρ_i} ≠ t^{ρ_j}, and the pairwise symmetry is not forced. The approach would prove symmetry only for partitions with repeated parts, not all partitions. **This is distinct from the killed Hecke algebra degeneration** (Route 7): it uses the Yang-Baxter graph recursion and eigenvalue degeneracy, not the algebraic structure of the degenerate Hecke algebra. **Viability: MEDIUM** for partitions with many repeated parts; **LOW** for partitions with all distinct parts.

---

## Rains' elliptic interpolation framework naturally encodes lower-degree corrections

**Approach 8 — Elliptic degeneration path.** Rains developed BCₙ-symmetric elliptic interpolation functions (Transform. Groups 2005; SIGMA 2018) at the elliptic level, with the trigonometric interpolation Macdonald polynomials as a degeneration. The Lascoux–Rains–Warnaar paper (Transform. Groups 2009, arXiv:0807.1351) works directly with **nonsymmetric interpolation Macdonald polynomials** and develops glₙ basic hypergeometric series. The elliptic level has an additional parameter (the nome p), and the interpolation polynomials are the p→0 limit. The strategy: at the elliptic level, there may be additional symmetry identities (e.g., Rains' transformation formulas for elliptic hypergeometric integrals) that, upon taking q→1 and then p→0, yield the symmetry of E\*_{λ⁻}(x; 1, t). **Bridge lemma**: find an elliptic identity (transformation or evaluation formula) that specializes to the symmetry statement at q=1. **Failure mode**: the q=1 limit from the elliptic level is a deep degeneration that may destroy the relevant elliptic structure. **Viability: MEDIUM** — Rains' framework is the only one where interpolation polynomials (with their inhomogeneous corrections) are native objects at every level of the hierarchy.

---

## Nonsymmetric plethysm and the Blasiak–Haiman program

**Approach 9 — Nonsymmetric plethysm extension to interpolation polynomials.** Blasiak–Haiman–Morse–Pun–Seelinger (arXiv:2506.09015, June 2025) introduce a **nonsymmetric plethysm operator** Π_{t,x} and show that modified nonsymmetric Macdonald polynomials H_{η|λ} are positive sums of flagged LLT polynomials. Their nonsymmetric shuffle theorem (arXiv:2509.24040, September 2025) extends this to the double Dyck path algebra. The strategy: extend the nonsymmetric plethysm to interpolation polynomials. If E\*_{λ⁻} can be expressed as Π_{t,x} applied to a symmetric LLT polynomial, and if Π_{t,x} preserves symmetry at q=1 (because the plethysm simplifies when q=1), then symmetry follows. **Bridge lemma**: construct an interpolation analog of the nonsymmetric plethysm. **Failure mode**: the plethysm framework is designed for homogeneous polynomials; the inhomogeneous corrections in E\*_μ may not fit. **Viability: MEDIUM** — very new tools, but extending to the interpolation setting is non-trivial.

---

## Extra vanishing and uniqueness characterization at q=1

**Approach 10 — Dimension-counting in the symmetric vanishing space.** E\*_{λ⁻}(x; q, t) is the unique polynomial of degree ≤ |λ| satisfying E\*_{λ⁻}(⟨ν⟩) = 0 for all compositions ν with |ν| ≤ |λ|, ν ≠ λ⁻, plus a normalization. At q=1, spectral vectors collapse from ~C(D+n, n) to **n!** distinct points. The strategy: show that within the space of **symmetric** polynomials of degree ≤ |λ|, the collapsed vanishing conditions at q=1 still uniquely determine a polynomial. If the dimension of the symmetric vanishing space is exactly 1, then the unique polynomial satisfying these conditions must be symmetric (since the symmetrization of E\*_{λ⁻} also satisfies the same vanishing conditions, by Sₙ-invariance of the collapsed spectral set). **Bridge lemma**: prove that dim{f ∈ Sym[x]_{≤|λ|} : f vanishes at all collapsed spectral points except ⟨λ⁻⟩} = 1. **Failure mode**: the collapsed spectral points may not impose enough independent conditions on symmetric polynomials, leaving the vanishing space dimension > 1. Koornwinder–Stokman (2021) report computational evidence of "extra vanishing" in rank 2 for BC-type interpolation polynomials, which suggests additional vanishing may help. **Viability: MEDIUM-HIGH** — this is a clean linear-algebra argument that could potentially be verified computationally for n=5 before attempting a general proof.

---

## Dunkl operator eigenspace confinement at q=1

**Approach 11 — Inhomogeneous Dunkl operator symmetry.** The interpolation polynomials E\*_μ are eigenfunctions of inhomogeneous Cherednik operators Ξ_i (Knop's notation). At q=1, these degenerate to **inhomogeneous Dunkl operators** D̃_i = D_i + (correction). Dunkl's theory (1989) shows that the rational Dunkl operators generate a representation of the rational Cherednik algebra. The strategy: at q=1, show that the eigenspace of D̃_i corresponding to the eigenvalue of E\*_{λ⁻} lies entirely within the symmetric polynomial subspace. Dunkl's classification of singular polynomials (Axioms, 2022) shows that at special parameter values, the Dunkl operator structure can force polynomials into specific Sₙ-isotypic components. **Bridge lemma**: for anti-dominant λ⁻, show the inhomogeneous Dunkl eigenvalue is "generic enough" (at generic t) that its eigenspace is one-dimensional within symmetric polynomials. **Failure mode**: the inhomogeneous Dunkl operators at q=1 may not be well-studied enough for this eigenspace analysis to be tractable. **Viability: MEDIUM.**

---

## Knop–Sahi creation operator at q=1

**Approach 12 — Creation operator symmetry preservation.** The Knop–Sahi recursion builds E\*_μ from E\*_0 = 1 using two operations: Hecke operators T_i and a creation operator Φ: f(x₁,…,xₙ) → x_n · q⁻¹ · f(x₁/q, x₂,…, xₙ) composed with cyclic shift. At q=1, **Φ degenerates**: the q-shift becomes trivial, so Φ|_{q=1}: f → x_n · f(x₁, x₂,…, xₙ) composed with cyclic permutation. This simplified operator may preserve symmetry in ways the general Φ does not. Strategy: track symmetry through the full Knop–Sahi recursion at q=1 — start from the symmetric E\*_0 = 1 and show each application of T_i or Φ|_{q=1} preserves the property "E\*_{λ⁻} is symmetric" when the target index is anti-dominant. **Bridge lemma**: show Φ|_{q=1} maps symmetric interpolation polynomials indexed by partitions to symmetric ones. **Failure mode**: the recursion passes through non-partition compositions (non-anti-dominant indices) where symmetry is not expected, making it impossible to maintain the symmetry invariant throughout the recursion. **This overlaps with but is not identical to the failed Hecke degeneration** — the focus here is on the creation operator's specific q=1 behavior, not the Hecke algebra structure. **Viability: LOW-MEDIUM.**

---

## Two cross-domain approaches from vertex models and Jordan algebras

**Approach 13 — Integrable vertex model at q=1.** Borodin–Wheeler (arXiv:1904.06804) construct nonsymmetric Macdonald polynomials as partition functions of colored lattice paths in integrable vertex models satisfying the Yang-Baxter equation. At q=1, the vertex weights simplify (the asymmetry disappears). The strategy: extend the Borodin–Wheeler construction to interpolation polynomials (which Ben Dali–Williams' signed multiline queues essentially do for the combinatorial side), and then exploit the enhanced integrability at q=1 to prove the partition function is symmetric. In integrable systems, **transfer matrix commutativity** often forces symmetry of observables. **Bridge lemma**: construct a transfer matrix whose trace gives E\*_{λ⁻}(x; 1, t), and show transfer matrices commute at q=1. **Failure mode**: the signs in the interpolation formula may prevent a clean transfer-matrix formulation. **Viability: MEDIUM.**

**Approach 14 — Sahi's Jordan algebra / Capelli eigenvalue approach.** Knop originally titled his paper "Symmetric and nonsymmetric quantum Capelli polynomials" — the interpolation polynomials arise as eigenvalues of quantum Capelli operators in Jordan algebra theory. Sahi's recent work (2024 IISc talk, Chen–Sahi arXiv:2403.02490) continues developing this connection. The Jordan algebra approach provides a **representation-theoretic meaning** for the interpolation polynomials that is independent of the Hecke algebra: they are central characters of certain modules. At q=1, the quantum Jordan algebra becomes a classical Jordan algebra, and central characters are automatically invariant under the Weyl group (= Sₙ for type A). **Bridge lemma**: show that E\*_{λ⁻}(x; 1, t) equals a central character of a module over the type-A Jordan algebra at appropriate parameters. **Failure mode**: the "quantum" vs. "classical" Jordan algebra distinction may be more subtle than a simple q=1 limit; the interpolation polynomial may not literally be a central character at q=1 with generic t. **Viability: MEDIUM** — conceptually elegant and potentially powerful, but the precise connection needs development.

---

## How these fourteen approaches map against the twelve killed routes

The critical test for each new approach is whether it is genuinely new or a disguised variant of a previously killed route. Here is the differentiation:

- **Approaches 1–2 (signed multiline queues/tableaux)**: Entirely new — the Ben Dali–Williams formula did not exist when Routes 1–12 were attempted. The combinatorial objects (signed queues with ball labels) are fundamentally different from the symbolic-t perturbation, Richardson extrapolation, or direct computation approaches.
- **Approach 3 (PushTASEP reversibility)**: Cross-domain (probability → algebra). Not a variant of any killed route. The Ayyer–Martin–Williams paper is from 2024, and [BDW] is forthcoming.
- **Approach 5 (rational KZ monodromy)**: Distinct from killed Route 7 (Hecke algebra degeneration), which used algebraic structure of the Hecke algebra. The KZ approach uses analytic continuation and monodromy of differential equations — a different mathematical technology.
- **Approach 7 (Yang-Baxter eigenvalue degeneracy)**: Uses the 2026 "Hunting the Poles" techniques. Related to but distinct from killed Route 4 (Sₙ equivariance quotient), which tried to reduce the quotient space dimension rather than exploit eigenvalue coincidences.
- **Approach 10 (dimension counting)**: A variant of killed Route 5 (spectral vector collapse), but with a crucial difference: it counts dimensions **within the symmetric polynomial subspace**, not in the full polynomial space. The collapse is a feature, not a bug, because it reduces the space of symmetric solutions.
- **Approaches 8, 9, 13, 14**: Entirely new frameworks (elliptic, plethysm, vertex models, Jordan algebras) with no overlap with any killed route.

---

## Synthesis: a prioritized research program

The most actionable path combines three complementary strategies:

**Tier 1 (immediate, highest probability of success)**:  
The Ben Dali–Williams signed multiline queue formula (Approach 1) specialized to q=1, combined with the forthcoming [BDW] probabilistic interpretation (Approach 3). These two results, when they appear together, may directly resolve the conjecture. The signed multiline queue formula is explicit enough for computer verification at n=5, which would itself be a significant advance. Meanwhile, the dimension-counting approach (Approach 10) can be tested computationally: enumerate the collapsed spectral points at q=1 for n=5 and check whether the symmetric vanishing space is one-dimensional.

**Tier 2 (medium-term, requires new bridge lemmas)**:  
The Kasatani–Takeyama rational KZ monodromy approach (Approach 5) and the Sahi binomial expansion at q=1 (Approach 6) are mathematically rigorous routes that require proving specific bridge lemmas but rest on established theory. The Yang-Baxter eigenvalue degeneracy (Approach 7) can provide partial results immediately (symmetry for partitions with repeated parts).

**Tier 3 (longer-term, potentially most powerful)**:  
The Rains elliptic degeneration (Approach 8), the Sahi–Knop Jordan algebra connection (Approach 14), and the Blasiak–Haiman nonsymmetric plethysm (Approach 9) could yield the most conceptual and general proofs, but each requires developing substantial new theory before the conjecture can be reached.

The field has shifted significantly since the twelve previous approaches were killed. The October 2025 Ben Dali–Williams formula and the 2024 Ayyer–Martin–Williams PushTASEP framework have created **genuinely new entry points** that did not previously exist. The fact that interpolation Macdonald polynomials now have both a combinatorial formula (signed multiline queues) and a probabilistic interpretation (PushTASEP at q=1) means that the conjecture is, for the first time, accessible to tools from integrable probability — a domain entirely outside the twelve failed algebraic and computational approaches.

