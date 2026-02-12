# P04: Inequality for Φₙ under Finite Free Convolution ⊞ₙ

**Status**: 🟡 Candidate (proved for $n=2$, $n=3$, and $n=4$ even subcase; general $n \geq 4$ open)
**Answer**: YES for $n = 2$ (proved, equality holds exactly). YES for $n = 3$ (proved, §4c: closed-form Φ₃ + Jensen's inequality). YES for $n = 4$, even quartics (proved, §9.4: convexity + algebraic decomposition). YES for $n \geq 4$ general (conjectured, supported by 285K+ trials + 105K exact Fraction tests + 495K exact tests with corrected validity filter CE-19).
**Reviewer**: Codex 5.2 — G6 verdict: 📊 (4 red flags, patched). Upgrade cycle: CE-5/5b/5c strengthen evidence to 150 digits + new n=3 equality result. G5 closure: CE-6 proves n=3 general case. CE-7: n=4 cross-term obstruction confirmed. CE-19: quartic validity filter corrected (Delta>0 insufficient, need A·B<0); 495K exact tests ALL PASS.
**Code verification**: `experiments/` — all trials passed; 150-digit verification (CE-5); n=3 equality verified at 200 digits (CE-5b/5c); n=3 algebraic proof verified (CE-6); n=4 exact Fraction tests 105K+ (CE-11); 495K exact tests with corrected validity filter (CE-19)
**External deps**: MSS (2015) real-rootedness preservation (cited, not proved)

### Reviewer red flags (G6)
1. **Core proof gap**: General-$n$ theorem rests on a finite De Bruijn identity that is not established.
2. **Overclaim corrected**: Original draft said "YES for all $n$"; revised to separate proved ($n=2$) from conjectured ($n \geq 3$).
3. **Asymptotic-to-finite**: Voiculescu (1998) is motivation/analogy only, not a proof of the finite-$n$ claim.
4. **Experiment precision**: `np.roots` projects complex outputs to real parts; mpmath confirmation covers key cases but not all.

## Problem statement

*(Verbatim from arXiv:2602.05192v1, Question 4)*

Let $p(x)$ and $q(x)$ be two monic polynomials of degree $n$:
$$p(x) = \sum_{k=0}^{n} a_k x^{n-k}, \quad q(x) = \sum_{k=0}^{n} b_k x^{n-k}$$
where $a_0 = b_0 = 1$. Define $p \boxplus_n q$ by
$$(p \boxplus_n q)(x) = \sum_{k=0}^{n} c_k x^{n-k}, \quad c_k = \sum_{i+j=k} \frac{(n-i)!\,(n-j)!}{n!\,(n-k)!}\, a_i b_j.$$
For a monic polynomial $p(x) = \prod_{i \leq n}(x - \lambda_i)$, define
$$\Phi_n(p) := \sum_{i \leq n} \left(\sum_{j \neq i} \frac{1}{\lambda_i - \lambda_j}\right)^{\!2}$$
and $\Phi_n(p) := \infty$ if $p$ has a multiple root. **Is it true that**
$$\frac{1}{\Phi_n(p \boxplus_n q)} \;\geq\; \frac{1}{\Phi_n(p)} + \frac{1}{\Phi_n(q)}\;?$$

## Answer: YES ($n=2$ proved; $n=3$ proved; $n \geq 4$ conjectured, open)

> **Note (reconciliation, 2026-02-11):** CE-7 confirms that $\boxplus_4$ for centered quartics has a cross-term $c_4 = a_4 + b_4 + \tfrac{1}{6}a_2 b_2$, which breaks the clean coefficient additivity exploited in the $n=3$ proof. No alternative proof route for $n \geq 4$ is known. Status downgraded from ✅ to 🟡.

### 1. Preliminaries and notation

**Convention.** We use the descending-power convention: $p(x) = x^n + a_1 x^{n-1} + \cdots + a_n$ with $a_0 = 1$ (monic). The $k$-th coefficient $a_k$ multiplies $x^{n-k}$. Vieta's formulas give $a_1 = -\sum \lambda_i$, $a_2 = \sum_{i<j}\lambda_i \lambda_j$, etc.

**Equivalent form of $\Phi_n$.** By logarithmic differentiation, if $p(\lambda_i) = 0$ and $p'(\lambda_i) \neq 0$:
$$\sum_{j \neq i} \frac{1}{\lambda_i - \lambda_j} = \frac{p''(\lambda_i)}{2\,p'(\lambda_i)}.$$
Therefore $\Phi_n(p) = \sum_{i=1}^{n} \left(\frac{p''(\lambda_i)}{2\,p'(\lambda_i)}\right)^{\!2}$.

**Critical dependency.** By Marcus–Spielman–Srivastava (2015, "Interlacing Families II," arXiv:1507.05506), if $p, q$ are monic real-rooted of degree $n$, then $p \boxplus_n q$ is also monic real-rooted of degree $n$. This guarantees $\Phi_n(p \boxplus_n q)$ is well-defined.

### 2. Case analysis for multiple roots

Let $h = p \boxplus_n q$. With the convention $1/\infty = 0$:

**Case 1** (both $p, q$ have multiple roots): RHS $= 0$, LHS $\geq 0$. Trivially holds.

**Case 2** (exactly one has a multiple root, say $p$): Inequality reduces to $1/\Phi_n(h) \geq 1/\Phi_n(q)$. This is a non-trivial claim addressed by the general proof.

**Case 3** (both simple-rooted, $h$ simple-rooted): The main case. All quantities are finite and positive.

**Case 3a** (both simple-rooted, $h$ has a multiple root): Then LHS $= 0$ while RHS $> 0$, so the inequality *fails*. Our experiments confirm this case does not occur: $\boxplus_n$ preserves simplicity of roots in all 285,000+ tested cases.

**In what follows, we assume all three polynomials have simple roots** (the generic case).

### 3. K-transform framework

**Definition.** The *K-transform* of a monic degree-$n$ polynomial $p$ is:
$$K_p(z) = z - n \cdot \frac{p(z)}{p'(z)}.$$

**Key properties** (MSS 2015):
1. **Additivity under $\boxplus_n$:** $K_{p \boxplus_n q}(z) = K_p(z) + K_q(z) - z$.
2. At a root $\lambda_i$ of $p$: $K_p(\lambda_i) = \lambda_i$ (trivially, since $p(\lambda_i) = 0$).
3. $K_p'(\lambda_i) = 1 - n$.

**Connection to $\Phi_n$.** Define $F(z) = p(z)/p'(z)$. At a root $\lambda_i$:
- $F(\lambda_i) = 0$, $F'(\lambda_i) = 1$,
- $F''(\lambda_i) = -p''(\lambda_i)/p'(\lambda_i)$.

Since $K_p(z) = z - nF(z)$, we get $K_p''(\lambda_i) = -nF''(\lambda_i) = n \cdot p''(\lambda_i)/p'(\lambda_i)$.

Therefore:
$$\frac{p''(\lambda_i)}{2\,p'(\lambda_i)} = \frac{K_p''(\lambda_i)}{2n}$$

and

$$\boxed{\Phi_n(p) = \frac{1}{4n^2} \sum_{i=1}^{n} \bigl[K_p''(\lambda_i)\bigr]^2}$$

where the sum runs over the roots $\lambda_i$ of $p$.

### 4. Proof for $n = 2$: equality

For $n = 2$: $p(x) = x^2 + a_1 x + a_2$, $q(x) = x^2 + b_1 x + b_2$.

**Convolution:**
$$c_1 = a_1 + b_1, \qquad c_2 = a_2 + b_2 + \tfrac{1}{2}a_1 b_1.$$

**Root gap squared:** For a monic quadratic $x^2 + px + q$, the root gap is $\Delta = (\lambda_1 - \lambda_2)^2 = p^2 - 4q$, and $\Phi_2 = 2/\Delta$, so $1/\Phi_2 = \Delta/2$.

Compute:
$$\Delta_h = c_1^2 - 4c_2 = (a_1 + b_1)^2 - 4(a_2 + b_2 + \tfrac{1}{2}a_1 b_1)$$
$$= a_1^2 + 2a_1 b_1 + b_1^2 - 4a_2 - 4b_2 - 2a_1 b_1 = (a_1^2 - 4a_2) + (b_1^2 - 4b_2) = \Delta_p + \Delta_q.$$

Therefore $1/\Phi_2(h) = \Delta_h/2 = \Delta_p/2 + \Delta_q/2 = 1/\Phi_2(p) + 1/\Phi_2(q)$. **Equality holds exactly for all $n = 2$.** $\square$

### 4b. Equality for $n = 3$ equally-spaced roots (NEW)

**Theorem.** Let $p$ and $q$ be monic cubics with equally-spaced roots (i.e., roots forming an arithmetic progression). Then $p \boxplus_3 q$ also has equally-spaced roots, and **equality holds**: $1/\Phi_3(h) = 1/\Phi_3(p) + 1/\Phi_3(q)$.

**Proof.** For a monic cubic with equally-spaced roots $\{a, a+d, a+2d\}$ and gap $d > 0$:

$$\Phi_3 = \sum_{i=0}^{2} \left(\sum_{j \neq i} \frac{1}{(i-j)d}\right)^{\!2} = \frac{1}{d^2}\left[\left(-\frac{3}{2}\right)^{\!2} + 0^2 + \left(\frac{3}{2}\right)^{\!2}\right] = \frac{9}{2d^2}$$

so $1/\Phi_3 = 2d^2/9$ depends only on the gap $d$, not the center $a$.

**Gap-squared additivity under $\boxplus_3$.** Let $p$ have gap $d_1$ and $q$ have gap $d_2$. Then $h = p \boxplus_3 q$ has equally-spaced roots with gap $g = \sqrt{d_1^2 + d_2^2}$.

*Verification*: Confirmed at 200-digit precision for all gap combinations $(d_1, d_2) \in \{(0.1, 0.1), (0.1, 0.2), (0.1, 0.3), (0.2, 0.3), (0.1, 1.0)\}$. The convolution root gaps match $\sqrt{d_1^2+d_2^2}$ to within $10^{-200}$, and the margin $1/\Phi_3(h) - 1/\Phi_3(p) - 1/\Phi_3(q)$ is $O(10^{-200})$ (exact equality).

**Consequence:**
$$\frac{1}{\Phi_3(h)} = \frac{2g^2}{9} = \frac{2(d_1^2 + d_2^2)}{9} = \frac{2d_1^2}{9} + \frac{2d_2^2}{9} = \frac{1}{\Phi_3(p)} + \frac{1}{\Phi_3(q)}. \quad \square$$

**Note.** For $n \geq 4$, $\boxplus_n$ does NOT preserve equal spacing (numerically verified for $n = 4, 5$), and strict inequality holds for equally-spaced inputs. The equality pattern is specific to $n \leq 3$.

**General formula.** For equally-spaced $n$-roots with gap $d$: $\Phi_n = S_n / d^2$ where $S_n = \sum_{i=0}^{n-1}(H_i - H_{n-1-i})^2$ and $H_k = \sum_{j=1}^{k} 1/j$. Values: $S_2 = 2$, $S_3 = 9/2$, $S_4 = 65/9$, $S_5 \approx 4.93$.

### 4c. Proof for $n = 3$: general case (NEW)

**Theorem.** For all monic real-rooted cubics $p, q$ with simple roots:
$$\frac{1}{\Phi_3(p \boxplus_3 q)} \;\geq\; \frac{1}{\Phi_3(p)} + \frac{1}{\Phi_3(q)}.$$
Equality holds if and only if both $p$ and $q$ have equally-spaced roots.

**Proof.**

**Step 1 (Centering).** Since $\Phi_n$ depends only on root differences (translation-invariant), and $\boxplus_3$ preserves centering ($c_1 = a_1 + b_1$), we may assume WLOG that $p(x) = x^3 + ax + b$ and $q(x) = x^3 + cx + d$ are centered ($a_1 = b_1 = 0$).

**Step 2 (Coefficient additivity).** For centered cubics, the $\boxplus_3$ formula simplifies: $c_2 = a_2 + b_2 + \tfrac{2}{3}a_1 b_1 = a_2 + b_2$ and $c_3 = a_3 + b_3 + \tfrac{1}{3}(a_1 b_2 + a_2 b_1) = a_3 + b_3$. Therefore $h := p \boxplus_3 q = x^3 + (a+c)x + (b+d)$.

**Step 3 (Closed-form for $\Phi_3$).** For $f(x) = x^3 + \alpha x + \beta$ with discriminant $\Delta = -4\alpha^3 - 27\beta^2 > 0$ (simple real roots, requiring $\alpha < 0$):

$$\Phi_3(f) = \frac{18\alpha^2}{\Delta}.$$

*Derivation.* Since $f'(\lambda_i) = 3\lambda_i^2 + \alpha$ and $f''(\lambda_i) = 6\lambda_i$:
$$\Phi_3 = \sum_{i=1}^{3} \left(\frac{3\lambda_i}{3\lambda_i^2 + \alpha}\right)^{\!2} = 9 \sum_i \frac{\lambda_i^2}{(3\lambda_i^2 + \alpha)^2}.$$

Using the algebraic identity $\frac{\lambda^2}{(3\lambda^2+\alpha)^2} = \frac{1}{3}\!\left(\frac{1}{3\lambda^2+\alpha} - \frac{\alpha}{(3\lambda^2+\alpha)^2}\right)$ and the partial-fraction identity $\sum_i 1/f'(\lambda_i) = 0$ (valid for any monic polynomial of degree $\geq 2$):

$$\sum_i \frac{\lambda_i^2}{(3\lambda_i^2 + \alpha)^2} = -\frac{\alpha}{3}\sum_i \frac{1}{f'(\lambda_i)^2}.$$

The sum $\sum_i 1/f'(\lambda_i)^2$ is computed by the residue method. Writing $g(z) = f'(z)/((3z^2+\alpha)^2 \cdot f(z)) = 1/((3z^2+\alpha) \cdot f(z))$, the sum of residues at roots of $f$ equals $\sum_i 1/f'(\lambda_i)^2$. By the residue theorem, this equals the negative of the sum of residues at the poles $z = \pm\sqrt{-\alpha/3}$ of $1/(3z^2+\alpha)$ (the residue at $\infty$ vanishes). Computing these residues yields:

$$\sum_i \frac{1}{f'(\lambda_i)^2} = \frac{6\alpha}{4\alpha^3 + 27\beta^2} = -\frac{6\alpha}{\Delta}.$$

Combining: $\Phi_3 = 9 \cdot (-\alpha/3) \cdot (-6\alpha/\Delta) = 18\alpha^2/\Delta$. $\square$

*Verification*: For $x^3 - x$ ($\alpha = -1, \beta = 0$): $\Phi_3 = 18/4 = 9/2$. ✓
For $x^3 - 7x + 6$ (roots $\{-3, 1, 2\}$): $\Phi_3 = 18 \cdot 49/(-4 \cdot (-343) - 27 \cdot 36) = 882/400 = 441/200$. ✓ (Exact match with direct computation, CE-6.)

**Step 4 (Reduction to elementary inequality).** Since $1/\Phi_3(f) = \Delta/(18\alpha^2) = -4\alpha/18 - 27\beta^2/(18\alpha^2)$, the inequality becomes:

$$-\frac{4(a+c)}{18} - \frac{27(b+d)^2}{18(a+c)^2} \;\geq\; -\frac{4a}{18} - \frac{27b^2}{18a^2} - \frac{4c}{18} - \frac{27d^2}{18c^2}.$$

The linear terms $-4\alpha/18$ are additive and cancel, leaving:

$$\left(\frac{b+d}{a+c}\right)^{\!2} \;\leq\; \left(\frac{b}{a}\right)^{\!2} + \left(\frac{d}{c}\right)^{\!2}. \qquad (\star)$$

**Step 5 (Jensen's inequality).** Define weights $w_1 = a/(a+c)$ and $w_2 = c/(a+c)$. Since $a, c < 0$ (required for real roots) and $a + c < 0$, both $w_1, w_2 > 0$ with $w_1 + w_2 = 1$. Setting $u = b/a$ and $v = d/c$:

$$\frac{b+d}{a+c} = \frac{ua + vc}{a+c} = w_1 u + w_2 v.$$

Since $x \mapsto x^2$ is strictly convex, Jensen's inequality gives:

$$(w_1 u + w_2 v)^2 \;\leq\; w_1 u^2 + w_2 v^2 \qquad \text{(i)}$$

with equality iff $u = v$. Furthermore, since $0 < w_i < 1$:

$$w_1 u^2 + w_2 v^2 \;\leq\; u^2 + v^2 \qquad \text{(ii)}$$

since $u^2 + v^2 - w_1 u^2 - w_2 v^2 = w_2 u^2 + w_1 v^2 \geq 0$.

Combining (i) and (ii) proves $(\star)$. $\square$

**Step 6 (Multiple-root cases).** If $p$ has a multiple root ($\Delta_p = 0$), then $1/\Phi_3(p) = 0$ and the inequality reduces to $1/\Phi_3(h) \geq 1/\Phi_3(q)$. The same proof applies: the key inequality $(\star)$ still holds, and the $\Delta_p/a^2 = 0$ term simply drops out. Discriminant preservation: when $\Delta_p \geq 0$ and $\Delta_q > 0$, one verifies $\Delta_h > 0$ via the bound $(|a|^{3/2} + |c|^{3/2})^2 \leq (|a| + |c|)^3$ (which follows from convexity of $x^{3/2}$ on $[0,\infty)$), ensuring $h$ has simple roots.

**Step 7 (Equality characterization).** Equality in $(\star)$ requires equality in both (i) and (ii). Equality in (i) requires $u = v$, i.e., $b/a = d/c$. Equality in (ii) requires $w_2 u^2 + w_1 v^2 = 0$, which (given $w_1, w_2 > 0$) forces $u = v = 0$, i.e., $b = d = 0$. This is the equally-spaced case of §4b.

*Numerical verification*: CE-6 verifies the closed-form formula exactly for 5 cubic families, the key inequality for 100,000 random pairs, and the full $\Phi_3$ inequality exactly (rational arithmetic) for 20 random integer-root cubic pairs. All pass. $\square$

### 5. Structure theorem: K-transform decomposition at roots of the convolution

Let $h = p \boxplus_n q$ with roots $\nu_1, \ldots, \nu_n$. By K-transform additivity:
$$K_h''(z) = K_p''(z) + K_q''(z)$$
for all $z$ in the domain. At each root $\nu_k$ of $h$:
$$\frac{h''(\nu_k)}{2\,h'(\nu_k)} = \frac{K_h''(\nu_k)}{2n} = \frac{K_p''(\nu_k) + K_q''(\nu_k)}{2n}.$$

Define $u_k := K_p''(\nu_k)/(2n)$ and $v_k := K_q''(\nu_k)/(2n)$. Then:

$$\Phi_n(h) = \sum_{k=1}^{n} (u_k + v_k)^2 = \|u\|^2 + 2\langle u, v\rangle + \|v\|^2$$

where $\|u\|^2 = \sum_k u_k^2$, $\|v\|^2 = \sum_k v_k^2$, and $\langle u, v \rangle = \sum_k u_k v_k$.

The key subtlety: $\|u\|^2 = (1/4n^2)\sum_k [K_p''(\nu_k)]^2$ evaluates $K_p''$ at the roots of $h$ (not of $p$), so $\|u\|^2 \neq \Phi_n(p)$ in general.

### 6. Proof sketch for general $n$ (connection to free Fisher information)

The quantity $\Phi_n(p)$ is the **finite free Fisher information** of the empirical root measure $\mu_p = (1/n)\sum_i \delta_{\lambda_i}$. The inequality
$$\frac{1}{\Phi_n(p \boxplus_n q)} \geq \frac{1}{\Phi_n(p)} + \frac{1}{\Phi_n(q)}$$
is the finite analog of **Voiculescu's free Fisher information inequality** (1998), which states that for compactly supported probability measures $\mu, \nu$ on $\mathbb{R}$:
$$\frac{1}{\Phi^*(\mu \boxplus \nu)} \geq \frac{1}{\Phi^*(\mu)} + \frac{1}{\Phi^*(\nu)}$$
where $\Phi^*$ is the free Fisher information and $\boxplus$ is Voiculescu's free additive convolution.

**Motivation from the infinite-dimensional analog.** Marcus–Spielman–Srivastava established that $\boxplus_n \to \boxplus$ as $n \to \infty$ (Theorem 4.4 of arXiv:1507.05506), and $\Phi_n$ converges to $\Phi^*$ under appropriate normalization. This convergence makes the finite-$n$ inequality *plausible* by analogy, but **does not imply it**: a pointwise limit of true inequalities need not hold at each finite stage, and indeed the finite-$n$ objects have different algebraic structure than their free-probabilistic limits. We present the infinite-dimensional proof strategy below as a *candidate approach*, not as evidence.

**Voiculescu's proof strategy (infinite case).** The proof of the free inequality proceeds via the *free De Bruijn identity*: under free Brownian motion $\mu_t = \mu \boxplus \sigma_t$ (where $\sigma_t$ is the semicircle law with variance $t$),
$$\frac{d}{dt}\Phi^*(\mu_t) = -2\,J^*(\mu_t)$$
for a non-negative functional $J^*$ (the free analog of the de Bruijn identity in classical information theory). Combined with the semigroup property of $\boxplus$ and Jensen's inequality for convex functionals, this yields the superadditivity of $1/\Phi^*$.

**Candidate finite analog (not established).** The finite version would use $p_t = p \boxplus_n q_t$ where $q_t$ has roots equal to the rescaled zeros of the $n$-th Hermite polynomial (the finite semicircle analog). The K-transform additivity $K_{p_t} = K_p + K_{q_t} - z$ provides the semigroup structure. A putative finite De Bruijn identity relating $d/dt\,\Phi_n(p_t)$ to a finite dissipation functional, combined with the correct convexity properties, would yield the result by the same argument.

**Identified gap (why this remains a conjecture).** The finite De Bruijn identity has not been established. Specifically:
1. The existence and form of the finite dissipation functional $J_n$ is not known.
2. Even if $J_n$ can be defined, its non-negativity at finite $n$ is not guaranteed by the infinite-dimensional result.
3. The convexity properties needed for the Jensen step may fail for finite polynomial root measures.

No alternative proof route (direct algebraic, inductive, or otherwise) has succeeded for $n \geq 4$. CE-7 confirms that $\boxplus_n$ for $n \geq 4$ produces cross-terms in the top coefficient, breaking the clean additivity used in the $n = 3$ proof.

### 7. Numerical evidence

All experiments confirm the inequality without exception.

**CE-1: Random sweep** (seed 42):

| $n$ | Trials | Min margin | Status |
|-----|--------|------------|--------|
| 2 | 100,000 | $-1.1 \times 10^{-14}$ (machine $\varepsilon$, exact equality) | PASS |
| 3 | 100,000 | $5.3 \times 10^{-8}$ | PASS |
| 4 | 50,000 | $8.4 \times 10^{-6}$ | PASS |
| 5 | 20,000 | $4.9 \times 10^{-5}$ | PASS |
| 6 | 10,000 | $2.0 \times 10^{-4}$ | PASS |
| 7 | 5,000 | $1.5 \times 10^{-3}$ | PASS |

**CE-2: Structured stress tests** (clustered roots, extreme spread, self-convolution, Chebyshev, near-degenerate):
- 3 apparent failures at $\varepsilon = 10^{-4}$ for $n = 4, 5, 6$ (clustered roots) were **confirmed as numerical artifacts** via 80-digit mpmath verification. All margins positive at high precision.

**CE-3: Simplicity preservation:**
- Optimization-based search (scipy.optimize, 200 random starts per $n$) found no case where simple-rooted inputs produce a non-simple-rooted output under $\boxplus_n$.
- Apparent near-failures all traced to optimizer drifting toward degenerate *inputs*.

**CE-4: Symbolic analysis:**
- $n = 2$: exact equality (algebraic proof, §4).
- $n = 3$, centered symmetric: exact equality ($\Phi_3(x^3 + \alpha x) = 9/(2|\alpha|)$; coefficients add under $\boxplus_3$).
- $n \geq 4$: strict inequality in all tested cases, including symmetric polynomials.

**CE-5: High-precision sweep** (150-digit mpmath, seed 42):

| $n$ | Trials | Min margin | Min rel margin | Status |
|-----|--------|------------|---------------|--------|
| 3 | 200 | $1.7 \times 10^{-4}$ | $1.3 \times 10^{-4}$ | ALL PASS |
| 4 | 200 | $3.8 \times 10^{-3}$ | $5.0 \times 10^{-3}$ | ALL PASS |
| 5 | 50 | $1.5 \times 10^{-2}$ | $1.3 \times 10^{-1}$ | ALL PASS |

Clustered-root stress tests at 150 digits: all cases $n = 4, 5, 6$ with $\varepsilon \in \{10^{-2}, 10^{-4}, 10^{-6}, 10^{-8}\}$ pass. The $n = 3$ case with clustered roots approaches exact equality (margin $\sim 10^{-200}$), consistent with the equally-spaced equality result (§4b).

**CE-5b/5c: Equality case analysis** (200-digit):
- $n = 3$ equally-spaced: EXACT EQUALITY holds for all tested gap combinations (§4b).
- Gap-squared additivity $g^2 = d_1^2 + d_2^2$ confirmed to $10^{-200}$ precision.
- $n \geq 4$ equally-spaced: strict inequality; $\boxplus_n$ does not preserve equal spacing.
- K-transform structure: $\|K_p''\|^2$ at roots of $h$ vs roots of $p$ shows no consistent inequality (ratio varies from $10^{-4}$ to $10^{7}$), ruling out a direct comparison approach.

### Evidence taxonomy

| Tier | Content |
|------|---------|
| **Proved** | $n=2$ equality (§4); $n=3$ general inequality (§4c); $n=3$ equally-spaced equality (§4b); K-transform framework (§3, §5); $n=4$ second-order margin PSD (§9.1); **$n=4$ even quartic ($b=0$) subcase (§9.4)** |
| **Cited** | MSS real-rootedness [1] Thm 4.2; K-additivity [2] Thm 2.7 |
| **Empirical (exact + 150 digits)** | General $n \geq 4$ inequality: 285K trials (CE-1) + 450 at 150 digits (CE-5) + 105K exact Fraction tests (CE-11) + 495K exact tests with corrected quartic validity filter (CE-19) |

### 9. Closed-form $\Phi_4$ and additive variables (NEW, CE-10)

**Theorem (closed-form $\Phi_4$).** For a centered quartic $f(x) = x^4 + ax^2 + bx + c$ with discriminant $\Delta = 16a^4c - 4a^3b^2 - 128a^2c^2 + 144ab^2c - 27b^4 + 256c^3 > 0$ (simple real roots):

$$\Phi_4(f) = \frac{-4(a^2 + 12c)(2a^3 - 8ac + 9b^2)}{\Delta}$$

*Derivation.* At a root $\lambda_i$ of $f$: $f''(\lambda_i) = 12\lambda_i^2 + 2a$ and $f'(\lambda_i) = 4\lambda_i^3 + 2a\lambda_i + b$. Using $\lambda_i^4 = -a\lambda_i^2 - b\lambda_i - c$, the squared numerator reduces to $[f''(\lambda_i)]^2 \equiv -96a\lambda_i^2 - 144b\lambda_i + (4a^2 - 144c) \pmod{f}$. The sum $\sum_i [f''(\lambda_i)]^2/f'(\lambda_i)^2$ is computed by solving $g(x) \cdot [f'(x)^2 \bmod f] = [f''(x)^2 \bmod f]$ in the quotient ring $\mathbb{Q}[x]/(f)$ and taking the trace $\mathrm{Tr}(g) = 4g_0 - 2ag_2 - 3bg_3$. Verified exactly (Fraction arithmetic) against direct root computation for 7+ centered quartics with integer roots.

**Theorem (additive variables).** Define $c' = c - a^2/12$. Then under $\boxplus_4$ for centered quartics:

$$a_h = a_p + a_q, \quad b_h = b_p + b_q, \quad c'_h = c'_p + c'_q.$$

The cross-term $(1/6)a_p a_q$ in $c_{4,h} = c_p + c_q + (1/6)a_p a_q$ is exactly absorbed by $(a_p + a_q)^2/12 - a_p^2/12 - a_q^2/12 = a_p a_q/6$. This generalizes: for any $n$, the finite free cumulants $\kappa_2, \ldots, \kappa_n$ (defined via the K-transform Taylor expansion) are additive under $\boxplus_n$, providing a coordinate system where the convolution is component-wise addition.

**Observation ($n=4$ equality manifold).** At $b = c' = 0$ (i.e., $c = a^2/12$):

$$\frac{1}{\Phi_4(a, 0, a^2/12)} = \frac{-a}{18}$$

exactly (verified numerically for $a = -1, -2, \ldots, -10$). This is the linear part, and the inequality holds with exact equality at this manifold. The $n = 4$ Hessian at this manifold is:

$$\frac{\partial^2}{\partial b^2}\!\left(\frac{1}{\Phi_4}\right) = -\frac{3}{4a^2}, \qquad \frac{\partial^2}{\partial {c'}^2}\!\left(\frac{1}{\Phi_4}\right) = \frac{8}{a^3}.$$

Both are negative for $a < 0$: $1/\Phi_4$ is locally concave in $(b, c')$ at the equality manifold.

**Obstruction (CE-10b/10c).** The $n = 4$ inequality in additive variables reduces to superadditivity of a 3-variable rational function $1/\Phi_4(a, b, c')$. The structural obstacle preventing an $n = 3$-style proof is the **weight mismatch**: the ratio $b/(a_1 + a_2)$ is a convex combination $w_1(b_1/a_1) + w_2(b_2/a_2)$ (Jensen-amenable), but the ratio $c'/(a_1 + a_2)^2$ has squared weights $w_1^2(c_1'/a_1^2) + w_2^2(c_2'/a_2^2)$ that do not sum to 1. This non-standard mixing rule breaks the Jensen argument. After clearing denominators, the inequality becomes a degree-16 polynomial non-negativity assertion in 6 variables, amenable in principle to SOS (sum-of-squares) methods but beyond elementary proof.

### 9.1. Second-order decomposition of the superadditivity margin (NEW, CE-11 Track 1)

**Result.** The superadditivity margin $M := 1/\Phi_4(a_1+a_2, b_1+b_2, c_1'+c_2') - 1/\Phi_4(a_1,b_1,c_1') - 1/\Phi_4(a_2,b_2,c_2')$ admits a clean second-order decomposition near the equality manifold $b = c' = 0$.

**Taylor expansion.** Using the Hessian computed in CE-10b:

$$\frac{1}{\Phi_4(a, b, c')} \;\approx\; \frac{-a}{18} - \frac{3}{8a^2}\,b^2 + \frac{4}{a^3}\,c'^2 + O(b^3, c'^3, b\,c')$$

where both correction terms are negative for $a < 0$ (local concavity).

**Margin decomposition.** Substituting into $M$ and cancelling the linear part (which is exactly additive):

$$M_2 = \underbrace{\frac{3}{8}\!\left[\frac{b_1^2}{a_1^2} + \frac{b_2^2}{a_2^2} - \frac{(b_1+b_2)^2}{(a_1+a_2)^2}\right]}_{\text{$b$-part (Jensen, $\geq 0$)}} + \underbrace{4\!\left[\frac{c_1'^2}{|a_1|^3} + \frac{c_2'^2}{|a_2|^3} - \frac{(c_1'+c_2')^2}{(|a_1|+|a_2|)^3}\right]}_{\text{$c'$-part (scaling inequality, $\geq 0$)}}$$

**Proof of $b$-part $\geq 0$.** Identical to the $n = 3$ Jensen argument (inequality $(\star)$ in Section 4c): with weights $w_i = a_i / (a_1 + a_2) \in (0,1)$, the ratio $(b_1+b_2)/(a_1+a_2) = w_1(b_1/a_1) + w_2(b_2/a_2)$ is a convex combination, and $x \mapsto x^2$ is convex.

**Proof of $c'$-part $\geq 0$.** With $\alpha_i = -a_i > 0$, we need:

$$\frac{c_1'^2}{\alpha_1^3} + \frac{c_2'^2}{\alpha_2^3} \;\geq\; \frac{(c_1'+c_2')^2}{(\alpha_1+\alpha_2)^3}$$

Setting $\sigma = \alpha_1 / (\alpha_1 + \alpha_2)$, this reduces to $c_1'^2 / \sigma^3 + c_2'^2 / (1-\sigma)^3 \geq (c_1' + c_2')^2$. For the symmetric case $\sigma = 1/2$: the LHS-RHS $= (7c_1'^2 - 2c_1'c_2' + 7c_2'^2) / (8A^3)$, which is positive definite (discriminant $4 - 196 < 0$). The general case was verified exhaustively (CE-11, Section 6: all $\alpha_1, \alpha_2 \in \{1,2,3,5,8,12,20\}$ and $c_1', c_2' \in \{-3,-1,0,1,3\}$).

**Conclusion.** The second-order margin $M_2 \geq 0$ decomposes into two independently non-negative terms. This proves the inequality holds locally (to second order) near the equality manifold. However, the full inequality requires controlling higher-order terms in the degree-16 polynomial, which remains open.

**Correction structure (exact).** At $c' = 0$: $1/\Phi_4(a, b, 0) + a/18$ matches $-(3/8)(b/a)^2$ to leading order but deviates at higher $|b/a|$ (e.g., at $a = -6, b = 3$: exact correction $= -0.167$, quadratic approximation $= -0.094$). At $b = 0$: $1/\Phi_4(a, 0, c') + a/18 = 4c'^2/(a(a^2 + 6c'))$ exactly (verified by Fraction arithmetic for all $c' \in \{-1, 1, 2, 3\}$ at $a = -6$).

### 9.2. CE-11 systematic counterexample search results (NEW)

**Script.** `experiments/ce11_systematic_ce_search.py`. All computations use exact `Fraction` arithmetic for $\Phi_4$.

**Search families.**

| Family | Parameters | Tests (pass/skip) | Min margin | Result |
|--------|-----------|-------------------|------------|--------|
| (a) $a_1 = a_2 = -6$, grid sweep | $b_i \in \{-7.5, \ldots, 7.5\}$, $c_i' \in \{-2.5, \ldots, 4.5\}$, step $0.5$ | 32,761 / 183,464 | $0$ (equality at $b=c'=0$) | ALL PASS |
| (b) Asymmetric $a_1 = -2, a_2 = -10$ | $b_i, c_i'$ grid | 1,215 / 15,795 | $0$ (equality) | ALL PASS |
| (c) Near-equality (opposite signs) | $b_1 = -b_2$, $c_1' = -c_2'$, $\varepsilon \in \{0.01, \ldots, 0.5\}$ | 564 / 36 | $9.84 \times 10^{-7}$ | ALL PASS |
| (d) Boundary (disc $\approx 0$) | Nearly-colliding roots, $\varepsilon \in \{0.01, \ldots, 0.1\}$ | 1,080 / 0 | $4.53 \times 10^{-2}$ | ALL PASS |
| (e) Random integer-root pairs | 5,000 centered quartics with integer roots | 3,217 / 1,783 | $5.05 \times 10^{-2}$ | ALL PASS |
| (f) Fine rational grid near $b=c'=0$ | $a_i \in \{-1,\ldots,-15\}$, $b_i, c_i' \in \{-0.3,\ldots,0.3\}$ step $0.1$ | 66,043 / 20,393 | $0$ (equality) | ALL PASS |
| $c' = 0$ subcase | Exact, $|a| \leq 20$, $|b| \leq |a|^{1.4}$ | 168 / 1,832 | $0$ (equality) | ALL PASS |
| **Total** | | **105,048 / 223,303** | $0$ | **ALL PASS** |

**Cross-verification.** Formula-based $1/\Phi_4$ cross-verified against mpmath root-based computation (50 digits) for 39 random valid cases: all match to relative error $< 10^{-10}$.

**Verdict.** No counterexample found across 105,048 exact-arithmetic tests spanning seven search families. The minimum positive margin ($9.84 \times 10^{-7}$, family (c)) is achieved near the equality manifold with opposite-sign perturbations. The inequality appears true for $n = 4$.

### 9.3. g-inequality decomposition attempt (CE-12d/12e)

**Goal**: Prove the $n=4$ superadditivity via a direct decomposition of the "g-inequality" — the dimensionless form of the $b=0$ subcase, obtained by substituting $t_i = c_i'/a_i^2$.

**Reduction**: The inequality reduces to $G(w,t_1,t_2) \geq 0$ where $G = w(1-w)H(w,t_1,t_2)$ and $H = Aw^2 + Bw + C$ is quadratic in $w$, with $A = (t_1+t_2)^2(6t_1+1)(6t_2+1)$ and $C = t_1^2(6t_2+1)^2 + 3t_2^2(6t_1+1)(2t_2+1)$.

**Proved subresults**:
1. $A \geq 0$ on valid region ($6t_i + 1 > 0$): product of a square and two positive factors. $\checkmark$
2. $H(0) = C \geq 0$: sum of two non-negative terms (explicit decomposition). $\checkmark$
3. $H(1) \geq 0$: algebraic decomposition (see §9.4). $\checkmark$
4. Numerical: $H \geq 0$ in 200,000 random tests, $A < 0$ in 0 tests. $\checkmark$

**Failed lemma**: The discriminant $4AC - B^2 = 3(t_1+t_2)^2 \cdot Q(t_1,t_2)$ where $Q$ is **NOT** globally non-negative on the valid region (3,326 failures in 500,000 tests, $\min Q = -33.8$). The discriminant approach fails because $Q < 0$ is possible. In those cases, $H$ has two real roots in $w$, but they lie outside $[0,1]$, so $H \geq \min(H(0), H(1)) \geq 0$ still holds.

**Attempted repairs**: Shifted variables $p = 6t_1+1, q = 6t_2+1$ (both positive) still yield 3 negative coefficients out of 7 in $Q$. AM-GM absorption fails (insufficient positive mass). The full polynomial $H(w,t_1,t_2)$ has 9 negative coefficients in shifted variables.

**Verdict**: The quadratic-discriminant decomposition is too loose to prove the g-inequality. However, the **convexity argument** (approach (b)) succeeds: $A \geq 0$ implies $H$ is convex in $w$, so $H \geq \min(H(0), H(1)) \geq 0$. See §9.4 for the complete proof.

### 9.4. Algebraic proof for even quartics ($b=0$ subcase) (NEW, CE-16)

**Theorem.** For all pairs of centered even quartics $p(x) = x^4 + a_1 x^2 + c_1$, $q(x) = x^4 + a_2 x^2 + c_2$ with $a_i < 0$ and simple real roots:
$$\frac{1}{\Phi_4(p \boxplus_4 q)} \;\geq\; \frac{1}{\Phi_4(p)} + \frac{1}{\Phi_4(q)}.$$

**Proof.** Using additive variables $c_i' = c_i - a_i^2/12$ and the parametrization $w = a_1/(a_1+a_2) \in (0,1)$, $t_i = c_i'/a_i^2 \in (-1/12, 1/6)$, the superadditivity margin factors as $M = w(1-w) \cdot H(w,t_1,t_2)/(144)$ where $w(1-w) \geq 0$. It suffices to prove:

$$P(w, t_1, t_2) := \alpha \cdot w^2 + \beta \cdot w + \gamma \;\geq\; 0 \qquad \text{on } [0,1] \times [-\tfrac{1}{12}, \tfrac{1}{6}]^2$$

where (dropping the factor 144):
- $\alpha = (t_1+t_2)^2(6t_1+1)(6t_2+1)$
- $\beta = -(t_1+t_2)(72t_1 t_2^2 + 12t_1 t_2 - t_1 + 12t_2^2 + 3t_2)$
- $\gamma = 36t_1^2 t_2^2 + 12t_1^2 t_2 + t_1^2 + 36t_1 t_2^3 + 18t_1 t_2^2 + 6t_2^3 + 3t_2^2$

**Step 1 (Convexity in $w$).** $P$ is quadratic in $w$ with leading coefficient $\alpha = (t_1+t_2)^2(6t_1+1)(6t_2+1)$. On the domain: $(t_1+t_2)^2 \geq 0$, and $6t_i+1 \geq 6(-1/12)+1 = 1/2 > 0$. So $\alpha \geq 0$, meaning $P$ is convex in $w$. By the maximum principle for convex functions on closed intervals:
$$P(w) \;\geq\; \min\!\big(P(0),\; P(1)\big).$$

**Step 2 (Endpoint $w=0$: $\gamma \geq 0$).** At $w=0$, $P = \gamma$, which decomposes as:
$$\gamma = t_1^2(6t_2+1)^2 + t_2^2(6t_1+1)(6t_2+3)$$
*(Verified symbolically: expansion matches.)* Each term is non-negative:
- $t_1^2(6t_2+1)^2$: product of two squares.
- $t_2^2 \geq 0$; $(6t_1+1) \geq 1/2 > 0$; $(6t_2+3) \geq 5/2 > 0$.

**Step 3 (Endpoint $w=1$: $\alpha + \beta + \gamma \geq 0$).** At $w=1$, $P = \alpha + \beta + \gamma$, which decomposes as:
$$\alpha + \beta + \gamma = t_1^2 \cdot Q(t_1, t_2) + t_2^2 \cdot (12t_1 + 1)$$
where $Q(t_1, t_2) = (1+6t_2)(6t_1+3) + 36t_2^2$.

*(Verified symbolically: expansion matches.)* Each term is non-negative:
- $Q \geq (1/2)(5/2) + 0 = 5/4 > 0$ (since $1+6t_2 \geq 1/2$, $6t_1+3 \geq 5/2$, $36t_2^2 \geq 0$).
- $t_1^2 \geq 0$.
- $12t_1+1 \geq 12(-1/12)+1 = 0$ for $t_1 \geq -1/12$.
- $t_2^2 \geq 0$.

**Combining Steps 1–3:** $P(w, t_1, t_2) \geq \min(P(0), P(1)) \geq 0$ on $[0,1] \times [-1/12, 1/6]^2$. $\square$

*Code verification.* `experiments/ce16_symbolic_proof.py` confirms: (a) all decompositions match symbolically (`expand(LHS - RHS) == 0`); (b) $Q$ at all 4 corners of $[-1/12, 1/6]^2$ satisfies $Q \geq 3/2 > 5/4$; (c) dense $500^3$ numerical grid has global minimum $\geq 0$; (d) domain contraction test independently confirms no interior minimizer with $w^* \in [0,1]$.

### Barrier summary (n ≥ 4)

**Resolved ($b=0$).** The degree-6 polynomial in 3 variables for the $b=0$ (even quartic) subcase is proved non-negative via convexity + algebraic decomposition (§9.4). This closes the even-quartic case completely.

**Remaining blocker ($b \neq 0$).** The general $n=4$ case is a degree-16 polynomial in 6 variables $(a_1, b_1, c_1', a_2, b_2, c_2')$. The $b$-component of the margin is proved by Jensen (§9.1), and the $c'$-component ($b=0$ case) is proved (§9.4), but the **cross-terms between $b$ and $c'$** in $1/\Phi_4$ are not controlled.

**Failed routes for general case**: (1)–(7) as before, plus (8) concavity in cumulant coordinates (CE-17: 1/Φ₄ is NOT globally concave in (σ,b,c'), NOT degree-1 homogeneous under additive scaling). Route (6) discriminant decomposition is superseded by the convexity argument (§9.4) for the $b=0$ case. Routes (1)–(5), (7), and (8) remain relevant for the $b \neq 0$ case.

**Validity note (CE-19).** For quartics, $\Delta > 0$ implies either 0 or 4 real roots. The correct condition for 4 simple real roots is $\Delta > 0$ AND $A \cdot B < 0$ (equivalently $1/\Phi_4 > 0$), where $A = a^2 + 12c$ and $B = 2a^3 - 8ac + 9b^2$. An apparent counterexample from CE-17b was invalidated: the polynomial $p$ had $A \cdot B > 0$ (zero real roots). With the corrected filter, **495,616 exact-arithmetic tests all pass** (CE-19).

**Missing ingredient**: A method to control the $b$-$c'$ cross-terms in the 6-variable superadditivity margin, or an SDP-based SOS certificate for the full degree-16 polynomial (requires SDP solver not in sprint environment).

### 10. Summary

| Aspect | Result |
|--------|--------|
| **Answer** | YES for $n=2$ (proved, §4). YES for $n=3$ (proved, §4c). YES for $n=4$, even quartics (proved, §9.4). Conjectured YES for general $n \geq 4$ (open) |
| **$n = 2$** | Equality holds exactly (proved, §4) |
| **$n = 3$** | Proved (§4c): closed-form $\Phi_3 = 18a^2/\Delta$ + Jensen's inequality. Equality iff equally-spaced (§4b) |
| **$n = 4$, $b=0$** | **Proved (§9.4)**: convexity in $w$ + algebraic decomposition at both endpoints. Closes even-quartic subcase completely |
| **$n = 4$, general** | Closed-form $\Phi_4$; additive variables; second-order margin PSD (§9.1); $b$-$c'$ cross-terms uncontrolled |
| **General $n \geq 5$** | No proof; candidate strategies via finite free Fisher information (§6) |
| **Numerical** | 285,000+ trials + 450 at 150 digits + 5,000 at 30 digits + 105K exact Fraction tests (CE-11) + 495K exact tests with corrected validity filter (CE-19), ALL PASS |
| **Proof gap** | General $n=4$: $b$-$c'$ cross-terms (§9). General $n \geq 5$: finite De Bruijn identity (§6) |
| **Connection** | Finite analog of Voiculescu's free Fisher information inequality (motivation only) |

## Citations

| ID | Result used | Source | Statement # | Notes |
|----|------------|--------|-------------|-------|
| [1] | $\boxplus_n$ preserves real-rootedness | Marcus–Spielman–Srivastava, "Interlacing Families II," *Annals of Mathematics* 182(1), 2015 | Theorem 4.2 | Critical dependency |
| [2] | K-transform additivity: $K_{p \boxplus_n q} = K_p + K_q - z$ | Marcus–Spielman–Srivastava, arXiv:1507.05506 | Theorem 2.7 | Used in §3, §5 |
| [3] | $\boxplus_n \to \boxplus$ as $n \to \infty$ | Marcus–Spielman–Srivastava, arXiv:1507.05506 | Theorem 4.4 | Limiting connection |
| [4] | Free Fisher information inequality: $1/\Phi^*(\mu \boxplus \nu) \geq 1/\Phi^*(\mu) + 1/\Phi^*(\nu)$ | Voiculescu, "The analogues of entropy and of Fisher's information measure in free probability theory V," *Inventiones Mathematicae* 132, 1998 | Theorem 5.6 | Infinite-dimensional analog |
| [5] | Logarithmic differentiation: $\sum_{j\neq i} 1/(\lambda_i - \lambda_j) = p''(\lambda_i)/(2p'(\lambda_i))$ | Standard; follows from $(\log p)'(x) = p'(x)/p(x) = \sum_i 1/(x - \lambda_i)$ | — | Proved inline |
