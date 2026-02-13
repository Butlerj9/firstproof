# Claude Research Response — P04

Date captured: 2026-02-12  
Source: User-provided Claude Research Mode response (manual paste)  
Lane: P04  
Integration intent: Archive response for downstream lane execution and escalation tracking.

---

## Raw Response (verbatim)

Josh, let me read through all three uploaded files to fully understand the P04 problem state before proceeding.Synthesized P04 framework and examined blocking constraints thoroughlyRead the problem context file for P04Let me continue reading the truncated portion and the other files.Read truncated portion of problem contextLet me continue reading the files.Continue reading problem context - the general n=4 blocker sectionLet me continue reading the remaining files to understand the full picture.Read the experiments bundleLet me now read the lane packet file which likely has the most important information about the current state and failed routes.Read the lane packet fileNow I have a thorough understanding of P04. Let me read a key section of the lane packet - the failure routes and the specific blocker details.DoneLet me read the key middle section of the lane packet for the specific failure routes and current barrier analysis.Synthesized mathematical research strategy for polynomial inequality proof problemRead the lane packet middle section with failure routes and analysisNow I have a comprehensive understanding of the P04 problem. Let me synthesize what I know:
P04 Problem: Finite free convolution Fisher information inequality

For monic real-rooted degree-n polynomials p, q: Is 1/Φ_n(p ⊞_n q) ≥ 1/Φ_n(p) + 1/Φ_n(q)?

What's proved:

n=2: Equality holds exactly
n=3: General case proved (closed-form Φ₃ + Jensen)
n=4, b=0 (even quartics): Proved via convexity + algebraic decomposition (CE-16)
n=4 with b≠0 remains the main obstacle—the cross-terms between b and c' parameters create a degree-16 polynomial in 6 variables that resists standard approaches like Jensen's inequality, K-transform comparison, and induction strategies.

Now I'm mapping out why each route failed: weight mismatches between components, non-monotonicity issues, negative SOS coefficients, and lack of global concavity in the cumulant space. I need to generate at least 12 fundamentally different approach families—pulling from optimization theory, algebraic geometry, probabilistic methods, and potentially harmonic analysis or representation theory—then filter through a novelty gate to identify the three most promising candidates for detailed proof sketches.Show moreDoneI've now fully internalized all three files. This is a well-defined mathematical research task with a precise blocker. Let me launch a deep research dive to explore whether any existing mathematical tools or results could help close the general n=4 (b≠0) case or provide new approach families.Finite free Fisher information inequalityResearch complete•Creating my research plan...481 sources•8m 23sYour research report on finite free Fisher information for the general n=4 case is ready. It covers the computational feasibility of sparse SOS certification via TSSOS on the 31-term degree-16 polynomial, the theoretical path of discretizing the Shlyakhtenko-Tao projection argument using finite free score functions, and the algebraic strategy of Schur complement lifting to handle b-c' cross-terms. The report also details connections to heat flow dynamics, finite free cumulants, and SAGE/SONC alternative certification frameworks, concluding that no published result currently implies the inequality and identifying three ranked proof strategies.

# Finite free Fisher information: tools for the general n=4 case

**No published result directly implies the general n=4 case.** The inequality 1/Φ_n(p ⊞_n q) ≥ 1/Φ_n(p) + 1/Φ_n(q) appears in Problem 4 of the "First Proof" benchmark (arXiv:2602.05192), posed by a team including Spielman and Srivastava, with encrypted solutions scheduled for release on February 13, 2026. The literature on finite free probability extensively develops the algebraic framework of ⊞_n but has not addressed Fisher-information-type functionals. Three concrete proof strategies emerge from this research, ranked by likely feasibility: (1) sparse SOS certification via TSSOS on the degree-16 polynomial, (2) discretizing the Shlyakhtenko-Tao projection argument, and (3) a score-function decomposition inspired by Madiman-Barron. The extreme sparsity of the target polynomial—**31 terms out of ~74,613 possible**—makes computational certification surprisingly tractable.

## The computational path: TSSOS and sparse SOS on the 31-term polynomial

The degree-16 polynomial in 6 variables with only 31 nonzero terms is an ideal target for **sparsity-exploiting SOS hierarchies**, particularly TSSOS (Wang, Magron, Lasserre, 2021). Standard SOS for degree-16 in 6 variables requires a Gram matrix of size **3,003 × 3,003** with ~4.5 million entries—intractable with conventional SDP solvers. TSSOS constructs adjacency graphs based on which monomials interact, then performs chordal completion to obtain block-diagonal SDP matrices with dramatically smaller blocks. For a 31-term polynomial, most monomials do not interact, yielding blocks likely of size 10-50 rather than 3,003.

The critical insight is that **standard SOS failure does not preclude Putinar certificates on the semi-algebraic set**. The semi-algebraic constraint (real-rootedness of both input polynomials) defines a compact domain on which Putinar's Positivstellensatz guarantees a decomposition M = σ₀ + Σᵢ σᵢ · gᵢ where each σᵢ is SOS and gᵢ encodes a constraint. TSSOS directly supports this via the `add_psatz!` function, which accepts inequality constraints, equality constraints, and a relaxation order. The Julia code pattern is:

```julia
using TSSOS, DynamicPolynomials
@polyvar a1 b1 c1p a2 b2 c2p
# M = the degree-16 margin polynomial
# g = [g1, g2, ...] real-rootedness constraints (discriminant ≥ 0, etc.)
info = add_psatz!(model, M, vars, g, [], order, TS="MD")
```

Three alternative computational frameworks also merit testing. **SAGE certificates** (sageopt, Python) scale with number of terms rather than degree, making the 31-term polynomial very favorable; they use relative entropy programming rather than SDP. **SONC certificates** (Sums of Nonnegative Circuit Polynomials) are equivalent to SAGE for global non-negativity and admit second-order cone representations (Magron & Wang, 2023). Finally, **DSOS/SDSOS** (Ahmadi & Majumdar, 2019) reduce SOS to LP/SOCP but are more restrictive than SOS—they would only succeed if the polynomial has a diagonally dominant decomposition, which is unlikely given the 12 negative coefficients.

A key gap from Blekherman's work: for degree 16 in 6 variables, there exist non-negative polynomials that are not globally SOS. However, the constrained (Putinar) version circumvents this—the polynomial only needs to be non-negative on the real-rootedness domain, not everywhere.

## Discretizing the Shlyakhtenko-Tao projection argument

The **most theoretically promising route** is to discretize the proof of the infinite-dimensional analog. Shlyakhtenko and Tao (arXiv:2009.01882, 2020) proved that free Fisher information Φ*(μ^{⊞k}/√k) is non-increasing in k, which implies 1/Φ* is superadditive under ⊞. Their proof method uses the **free score function** ξ_μ (the conjugate variable in Voiculescu's sense) and a Pythagorean inequality: the score of a free convolution is a conditional expectation of the joint score, and conditional expectations are contractions in L².

The finite analog proceeds as follows. The quantity Σ_{j≠i} 1/(λ_i - λ_j) at each root λ_i is precisely the **finite free score**—it equals p''(λ_i)/(2p'(λ_i)) by L'Hôpital's rule, and converges to the Hilbert transform of the limiting spectral measure. Since p ⊞_n q = E[det(xI - A - UBU*)] where U is Haar-random unitary, the roots of p ⊞_n q arise from averaging over random rotations. If one could show that the score function of p ⊞_n q is (in some sense) a "projection" of the joint score, the Pythagorean inequality Φ_n(p ⊞_n q) ≤ Φ_n(p) + Φ_n(q) would follow, giving the desired superadditivity of 1/Φ_n.

The key obstacle is that the MSS expected characteristic polynomial is an *expectation of determinants*, not the determinant of an expectation. The roots of E[det(xI - M)] are not expectations of eigenvalues. Nevertheless, Jekel and Pi (arXiv:2305.02574, 2024) showed that free Fisher information Φ* is exactly the N→∞ limit of (1/N) times the expectation of Φ_N for random matrix models, providing the bridge between finite and infinite settings.

## The heat flow connection and a candidate finite De Bruijn identity

Hall and Ho (arXiv:2202.09660, published in Letters in Mathematical Physics, 2025) discovered that roots of degree-N polynomials under the heat flow ∂_t P = ∂_z² P satisfy the ODE system **dλ_i/dt = -2Σ_{j≠i} 1/(λ_i - λ_j)**. The drift term is precisely the negative of the score function whose squared sum defines Φ_n. This means the heat flow on polynomials is the **natural finite analog of free Brownian motion**.

Steinerberger (2020) and Kiselev-Tan (2022) rigorously established that differentiation of polynomials acts as a discrete semigroup on root distributions, converging to the free fractional convolution semigroup of Shlyakhtenko-Tao. The PDE governing root densities under differentiation is ∂_t ρ + ∂_x(ρ Hρ) = 0, a nonlinear fractional heat equation. This connection suggests a finite De Bruijn identity: define a finite entropy H_n(p_t) = -(1/n)Σ_{i<j} log|λ_i(t) - λ_j(t)| along the heat flow, and compute dH_n/dt using the root dynamics. The result should involve Φ_n(p_t), yielding a relation of the form dH_n/dt ∝ Φ_n. However, no paper has established this identity, and the heat flow pushes roots off the real line for forward time, complicating analysis.

The gradient structure is the deepest connection: **Φ_n(p) = ||∇ log |Δ(λ)||²** where Δ(λ) = Π_{i<j}(λ_i - λ_j) is the Vandermonde determinant. The heat flow moves roots along -∇ log|Δ|, while Dyson Brownian motion has drift +∇ log|Δ|. This links Φ_n to the Coulomb/log-gas energy functional, where Fisher information inequalities correspond to energy estimates for interacting particle systems.

## Finite free cumulants and the algebraic framework

The cumulant machinery developed by Arizmendi and Perales (2018) provides the algebraic backbone: **finite free cumulants κ_k^(d) are additive under ⊞_d**, meaning κ_k^(d)(p ⊞_d q) = κ_k^(d)(p) + κ_k^(d)(q). For n=4, the cumulants κ_1, κ_2, κ_3, κ_4 linearize the convolution, and the coordinates (a, b, c') used in the problem statement are essentially cumulant coordinates (with c' = c - a²/12 being the "corrected" fourth parameter).

The difficulty is that **Φ_n is a highly nonlinear functional of the cumulants**. For n=4 centered quartics, expressing Φ₄ in terms of (a, b, c') yields a rational function where the denominator involves the discriminant (a degree-6 polynomial in a, b, c'). The inverse 1/Φ₄ has cross-terms between b and c' because the discriminant couples them nonlinearly, even though the convolution acts additively on each coordinate separately.

Recent work by Arizmendi, Fujie, Perales, and Ueda (arXiv:2408.09337, 2024) defines a finite S-transform with multiplicativity and monotonicity properties and relates finite free cumulant behavior under differentiation to free fractional convolution powers. While this extends the algebraic toolkit, it does not address information-theoretic functionals.

## Strategies for the b-c' cross-terms in n=4

For the specific n=4 blocker, four approaches emerge from the literature:

**Schur complement lifting.** Write 1/Φ₄ = N/D as a ratio of polynomials. The superadditivity condition becomes N(sum)·D₁·D₂ - N₁·D(sum)·D₂ - N₂·D(sum)·D₁ ≥ 0 after clearing denominators. If the cross-terms between b and c' can be isolated into off-diagonal blocks of a 2×2 matrix, PSD-ness of the matrix (verified by the Schur complement A - BC⁻¹Bᵀ ≥ 0) would imply the scalar inequality. This converts the single polynomial inequality into a matrix inequality where cross-terms live naturally in off-diagonal positions.

**Parametric weight decomposition.** The even subcase succeeds by parameterizing (a₁,a₂) = (wa, (1-w)a) and showing convexity in w. For the general case, introduce **two weight variables**: w for the a-component and u for the (b,c')-component. If the margin can be shown convex in (w,u) jointly on [0,1]², the endpoint analysis extends. The cross-terms manifest as mixed w·u terms that need absorption.

**Convexity of the real-rootedness domain.** The set of coefficients (a,b,c) for which x⁴+ax²+bx+c has all real roots is semi-algebraic but NOT convex. However, the set of non-negative quartics IS a convex cone (Qi, Song, Zhang, 2020). If the problem can be reformulated in terms of non-negative polynomials rather than real-rooted ones, domain convexity provides leverage. The discriminant Δ ≥ 0 condition for real-rootedness is a polynomial inequality that defines the constraint in the Putinar framework.

**SAGE/SONC for structured sparsity.** Since the margin polynomial has only 31 terms, the Newton polytope is a low-dimensional object in the 6-variable monomial lattice. SAGE certificates decompose the polynomial into "AGE" components certified non-negative via AM/GM, and their complexity scales with terms, not degree. The 12 negative coefficients can potentially be absorbed by adjacent positive terms through the AM/GM structure of the Newton polytope faces.

## Conclusion

The finite free Fisher information inequality occupies a genuine gap in the literature—between the well-established infinite free probability result (Voiculescu, Shlyakhtenko-Tao) and the fully developed finite algebraic framework (Marcus-Spielman-Srivastava, Arizmendi-Perales). No existing theorem implies it. Three actionable paths forward stand out. First, **TSSOS with Putinar certificates** offers the most concrete and immediately executable strategy: the extreme sparsity (31/74,613 terms) and the semi-algebraic constraint formulation make this computationally feasible, likely requiring only moderate relaxation orders. Second, **discretizing the Shlyakhtenko-Tao projection argument** via the random matrix representation p ⊞_n q = E[det(xI - A - UBU*)] is the most natural theoretical approach—the finite score function Σ_{j≠i}1/(λ_i - λ_j) is exactly the right object, and the Pythagorean/contraction inequality for conditional expectations should transfer if the right conditioning structure can be identified. Third, the **Schur complement reformulation** of the cross-term problem directly addresses the b-c' coupling by lifting the scalar inequality to a matrix PSD condition where cross-terms belong naturally in off-diagonal blocks. The solutions release on February 13, 2026 at 11:59pm PT will reveal the intended approach.

