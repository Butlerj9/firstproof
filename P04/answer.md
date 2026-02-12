# P04: Inequality for Φₙ under Finite Free Convolution ⊞ₙ

**Status**: 🟡 Candidate (proved for $n=2$ and $n=3$; conjectured for $n \geq 4$ — no proof technique available)
**Answer**: YES for $n = 2$ (proved, equality holds exactly). YES for $n = 3$ (proved, §4c: closed-form Φ₃ + Jensen's inequality). YES for $n \geq 4$ (conjectured, supported by 285K+ trials + 450 trials at 150 digits; CE-7 confirms n=3 technique does not extend).
**Reviewer**: Codex 5.2 — G6 verdict: 📊 (4 red flags, patched). Upgrade cycle: CE-5/5b/5c strengthen evidence to 150 digits + new n=3 equality result. G5 closure: CE-6 proves n=3 general case. CE-7: n=4 cross-term obstruction confirmed.
**Code verification**: `experiments/` — all trials passed; 150-digit verification (CE-5); n=3 equality verified at 200 digits (CE-5b/5c); n=3 algebraic proof verified (CE-6)
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
| **Proved** | $n=2$ equality (§4); $n=3$ general inequality (§4c); $n=3$ equally-spaced equality (§4b); K-transform framework (§3, §5) |
| **Cited** | MSS real-rootedness [1] Thm 4.2; K-additivity [2] Thm 2.7 |
| **Empirical (150 digits)** | General $n \geq 4$ inequality: 285K trials (CE-1) + 450 trials at 150 digits (CE-5) |

### 8. Summary

| Aspect | Result |
|--------|--------|
| **Answer** | YES for $n=2$ (proved, §4). YES for $n=3$ (proved, §4c). Conjectured YES for $n \geq 4$ (open; CE-7 obstruction) |
| **$n = 2$** | Equality holds exactly (proved, §4) |
| **$n = 3$** | Proved (§4c): closed-form $\Phi_3 = 18a^2/\Delta$ + Jensen's inequality. Equality iff equally-spaced (§4b) |
| **General $n \geq 4$** | No proof; candidate strategy via finite free Fisher information (§6) |
| **Numerical** | 285,000+ trials + 450 at 150 digits, ALL PASS |
| **Proof gap ($n \geq 4$)** | Finite De Bruijn identity not established (§6); K-transform comparison approach ruled out (CE-5, Phase 3) |
| **Connection** | Finite analog of Voiculescu's free Fisher information inequality (motivation only) |

## Citations

| ID | Result used | Source | Statement # | Notes |
|----|------------|--------|-------------|-------|
| [1] | $\boxplus_n$ preserves real-rootedness | Marcus–Spielman–Srivastava, "Interlacing Families II," *Annals of Mathematics* 182(1), 2015 | Theorem 4.2 | Critical dependency |
| [2] | K-transform additivity: $K_{p \boxplus_n q} = K_p + K_q - z$ | Marcus–Spielman–Srivastava, arXiv:1507.05506 | Theorem 2.7 | Used in §3, §5 |
| [3] | $\boxplus_n \to \boxplus$ as $n \to \infty$ | Marcus–Spielman–Srivastava, arXiv:1507.05506 | Theorem 4.4 | Limiting connection |
| [4] | Free Fisher information inequality: $1/\Phi^*(\mu \boxplus \nu) \geq 1/\Phi^*(\mu) + 1/\Phi^*(\nu)$ | Voiculescu, "The analogues of entropy and of Fisher's information measure in free probability theory V," *Inventiones Mathematicae* 132, 1998 | Theorem 5.6 | Infinite-dimensional analog |
| [5] | Logarithmic differentiation: $\sum_{j\neq i} 1/(\lambda_i - \lambda_j) = p''(\lambda_i)/(2p'(\lambda_i))$ | Standard; follows from $(\log p)'(x) = p'(x)/p(x) = \sum_i 1/(x - \lambda_i)$ | — | Proved inline |
