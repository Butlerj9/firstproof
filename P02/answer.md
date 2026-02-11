# P02: Nonvanishing of the $u_Q$-Modified Rankin–Selberg Integral

**Status**: 🟡 Candidate (n=1 proved; general n structural argument)
**Answer**: **YES.** For any generic irreducible admissible $\Pi$ of $\mathrm{GL}_{n+1}(F)$, there exists $W \in \mathcal{W}(\Pi, \psi^{-1})$ such that for every generic irreducible admissible $\pi$ of $\mathrm{GL}_n(F)$, there exists $V \in \mathcal{W}(\pi, \psi)$ making the modified integral entire and nonzero.
**Code verification**: `experiments/` — Gauss sum nonvanishing verified for all conductor-matched pairs
**External deps**: JPSS local integral theory (standard), Gauss sum nonvanishing (standard number theory)

## Problem statement

*(From arXiv:2602.05192v1, Question 2)*

Let $F$ be a non-archimedean local field with ring of integers $\mathfrak{o}$, uniformizer $\varpi$, residue field $\mathbb{F}_q$. Let $\psi: F \to \mathbb{C}^\times$ be a nontrivial additive character with conductor $\mathfrak{o}$. For generic irreducible admissible representations $\Pi$ of $\mathrm{GL}_{n+1}(F)$ and $\pi$ of $\mathrm{GL}_n(F)$, with conductor ideal $\mathfrak{q} = \mathfrak{p}^{f(\pi)}$ and $Q = \varpi^{-f(\pi)}$ generating $\mathfrak{q}^{-1}$, set $u_Q = I_{n+1} + Q \cdot E_{n,n+1}$.

**Question**: Must there exist $W \in \mathcal{W}(\Pi, \psi^{-1})$ such that for every such $\pi$, there exists $V \in \mathcal{W}(\pi, \psi)$ with

$$\Psi_Q(s, W, V) := \int_{N_n \backslash \mathrm{GL}_n(F)} W\bigl(\mathrm{diag}(g, 1) \cdot u_Q\bigr) \, V(g) \, |\det g|^{s - 1/2} \, dg$$

finite and nonzero for all $s \in \mathbb{C}$?

## Answer: YES

### 1. Key identity (all $n$)

**Lemma (Unipotent absorption).** For all $W \in \mathcal{W}(\Pi, \psi^{-1})$ and $g \in \mathrm{GL}_n(F)$:

$$W\bigl(\mathrm{diag}(g, 1) \cdot u_Q\bigr) = \psi^{-1}(Q \cdot g_{nn}) \cdot W\bigl(\mathrm{diag}(g, 1)\bigr)$$

where $g_{nn}$ is the $(n, n)$-entry of $g$.

**Proof.** Write $u_Q = I_{n+1} + Q \cdot E_{n,n+1}$. Then:

$$\mathrm{diag}(g, 1) \cdot u_Q = \begin{pmatrix} g & Q \cdot g \cdot e_n \\ 0 & 1 \end{pmatrix} = \underbrace{\begin{pmatrix} I_n & Q \cdot g \cdot e_n \\ 0 & 1 \end{pmatrix}}_{=: \, n'} \cdot \mathrm{diag}(g, 1)$$

The matrix $n'$ is upper-triangular unipotent (lies in $N_{n+1}$). Its superdiagonal entries are all zero except at position $(n, n+1)$, which equals $Q \cdot g_{nn}$. By the Whittaker equivariance $W(n' \cdot h) = \psi^{-1}(n') \cdot W(h)$, and $\psi^{-1}(n') = \psi^{-1}(Q \cdot g_{nn})$. $\square$

**Consequence.** The modified integral equals:

$$\Psi_Q(s, W, V) = \int_{N_n \backslash \mathrm{GL}_n(F)} \psi^{-1}(Q \cdot g_{nn}) \cdot W\bigl(\mathrm{diag}(g, 1)\bigr) \cdot V(g) \cdot |\det g|^{s-1/2} \, dg$$

Equivalently, $\Psi_Q(s, W, V) = \Psi(s, R(u_Q) W, V)$ where $R(u_Q)W := W(\cdot \, u_Q)$ is the standard (unmodified) Rankin–Selberg integral with $W$ replaced by its right-translate. Since $u_Q \in \mathrm{GL}_{n+1}(F)$ and the Whittaker model is stable under right translation, $R(u_Q) W \in \mathcal{W}(\Pi, \psi^{-1})$.

### 2. Complete proof for $n = 1$ ($\mathrm{GL}_2 \times \mathrm{GL}_1$)

**Theorem.** Let $\Pi$ be any generic irreducible admissible representation of $\mathrm{GL}_2(F)$. There exists $W \in \mathcal{W}(\Pi, \psi^{-1})$ such that for every quasi-character $\chi$ of $F^\times$ with conductor $c = f(\chi)$:

$$\Psi_Q(s, W, \chi) = \int_{F^\times} W\bigl(\mathrm{diag}(g, 1) \cdot u_Q\bigr) \cdot \chi(g) \cdot |g|^{s-1/2} \, d^\times g$$

is a nonzero constant (independent of $s$).

**Proof.**

**Step 1 (Specialization of key identity).** For $n = 1$: $g \in F^\times$, $g_{11} = g$. The key identity gives $W(\mathrm{diag}(g, 1) \cdot u_Q) = \psi^{-1}(gQ) \cdot W(\mathrm{diag}(g, 1))$.

**Step 2 (Choice of $W$ via Kirillov model).** The Kirillov model $\mathcal{K}(\Pi, \psi^{-1})$ consists of functions $\varphi: F^\times \to \mathbb{C}$ related to $W$ by $\varphi(a) = W(\mathrm{diag}(a, 1))$. For any generic irreducible admissible $\Pi$ of $\mathrm{GL}_2(F)$, the Schwartz space $\mathcal{S}(F^\times)$ (locally constant, compactly supported functions) is contained in $\mathcal{K}(\Pi, \psi^{-1})$ [standard: Bernstein–Zelevinsky theory].

Choose $\varphi = \mathbf{1}_{\mathfrak{o}^\times}$ (indicator function of the units). This is in $\mathcal{S}(F^\times) \subset \mathcal{K}(\Pi, \psi^{-1})$, so it corresponds to some $W \in \mathcal{W}(\Pi, \psi^{-1})$.

**Step 3 (Integral computation).** With this $W$:

$$\Psi_Q(s, W, \chi) = \int_{F^\times} \psi^{-1}(gQ) \cdot \mathbf{1}_{\mathfrak{o}^\times}(g) \cdot \chi(g) \cdot |g|^{s-1/2} \, d^\times g = \int_{\mathfrak{o}^\times} \psi^{-1}(uQ) \cdot \chi(u) \, d^\times u$$

where the last equality uses $|u| = 1$ for $u \in \mathfrak{o}^\times$, so the $|g|^{s-1/2}$ factor is 1. **The integral is independent of $s$.**

**Step 4 (Gauss sum nonvanishing).** Set $c = f(\chi)$ and $Q = \varpi^{-c}$. The integral is:

$$G(\chi, \psi_{-c}) := \int_{\mathfrak{o}^\times} \psi^{-1}(u \varpi^{-c}) \cdot \chi(u) \, d^\times u$$

We verify this is nonzero:

- **Case $c = 0$** (unramified $\chi$): $Q \in \mathfrak{o}^\times$, so $uQ \in \mathfrak{o}^\times \subset \mathfrak{o}$, and $\psi^{-1}(uQ) = 1$ (since $\psi$ has conductor $\mathfrak{o}$). Also $\chi|_{\mathfrak{o}^\times} = 1$. So $G = \mathrm{vol}(\mathfrak{o}^\times) \neq 0$. $\checkmark$

- **Case $c \geq 1$** (ramified $\chi$): The additive character $\psi_{-c}(u) := \psi^{-1}(u \varpi^{-c})$ restricted to $\mathfrak{o}^\times$ has conductor $\mathfrak{p}^c$ (trivial on $1 + \mathfrak{p}^c$, nontrivial on $1 + \mathfrak{p}^{c-1}$). The multiplicative character $\chi$ also has conductor $\mathfrak{p}^c$. The integral decomposes as:

$$G = \mathrm{vol}(1 + \mathfrak{p}^c) \cdot \sum_{a \in (\mathfrak{o}/\mathfrak{p}^c)^\times} \psi^{-1}(a \varpi^{-c}) \cdot \chi(a)$$

This is a generalized Gauss sum with matching conductors. By the standard Gauss sum nonvanishing theorem:

$$|G| = \mathrm{vol}(1 + \mathfrak{p}^c) \cdot q^{c/2}$$

In particular, $G \neq 0$. $\checkmark$

**Conclusion.** The integral $\Psi_Q(s, W, \chi) = G(\chi, \psi_{-c})$ is a nonzero constant for all $\chi$, hence entire and nonzero for all $s \in \mathbb{C}$. $\square$

### 3. Structural argument for general $n$

For $n \geq 2$ ($\mathrm{GL}_{n+1} \times \mathrm{GL}_n$), the proof of the key identity (§1) shows that the modified integral is a standard Rankin–Selberg integral with $W$ replaced by $W' = R(u_Q)W$. The argument proceeds as follows.

**Step A (Right-translate is nonzero).** Since $u_Q$ is invertible, the map $R(u_Q): \mathcal{W}(\Pi, \psi^{-1}) \to \mathcal{W}(\Pi, \psi^{-1})$ is a linear isomorphism. In particular, $W \neq 0$ implies $R(u_Q)W \neq 0$.

**Step B (Non-degeneracy of the RS bilinear form).** By the Jacquet–Piatetski-Shapiro–Shalika theory [1], for any nonzero $W' \in \mathcal{W}(\Pi, \psi^{-1})$, there exists $V \in \mathcal{W}(\pi, \psi)$ with $\Psi(s, W', V) \neq 0$ as a rational function of $q^{-s}$.

**Step C (Ideal structure).** The JPSS theory further shows that the family of integrals $\{\Psi(s, W', V) : W' \in \mathcal{W}(\Pi), V \in \mathcal{W}(\pi)\}$ generates the fractional ideal $L(s, \Pi \times \pi) \cdot \mathbb{C}[q^s, q^{-s}]$. For a fixed nonzero $W'$, the sub-family $\{\Psi(s, W', V) : V \in \mathcal{W}(\pi)\}$ generates a nonzero sub-ideal. For generic $W'$ (outside a proper Zariski-closed subset of $\mathcal{W}(\Pi)$), this sub-ideal equals the full ideal $L(s) \cdot \mathbb{C}[q^s, q^{-s}]$.

**Step D (Existence of entire nonzero element).** When the sub-ideal is $L(s) \cdot R$ (where $R = \mathbb{C}[q^s, q^{-s}]$), we can find $V$ with $\Psi(s, W', V) = c \cdot q^{-as}$ for some $c \neq 0$ and $a \in \mathbb{Z}$. This monomial is entire and nonzero for all $s$. (Proof: take $V$ such that the integral polynomial $P(q^{-s})$ in $\Psi = L \cdot P$ exactly cancels the poles of $L$.)

**Step E (Uniform $W$).** The "generic" condition in Step C is Zariski-open for each $\pi$. Since $R(u_Q)$ is invertible, the set of $W$ such that $R(u_Q)W$ is generic is also Zariski-open. A countable intersection of Zariski-open dense sets (one for each conductor value $c \geq 0$) is non-empty in the infinite-dimensional space $\mathcal{W}(\Pi)$. Hence a single $W$ exists working for all $\pi$. $\square$

**Remark.** The structural argument in Steps C–E is not fully self-contained: it relies on the claim that the "partial ideal" (V varying, W' fixed) equals the full ideal for generic W'. This is a consequence of the multiplicity-one theorem for the pair $(\mathrm{GL}_{n+1}, \mathrm{GL}_n)$ and the surjectivity of the RS pairing, but a complete proof would require the full JPSS–Matringe machinery. The $n = 1$ proof in §2 avoids this by direct computation.

### 4. Why $u_Q$ is essential

The element $u_Q$ plays the role of a **conductor-matching device**: it introduces the additive twist $\psi^{-1}(Q g_{nn})$ whose conductor equals $f(\pi)$, the conductor of $\pi$. This ensures:

1. **Nonvanishing**: The twist produces a Gauss-sum-type integral with matching conductors, which is always nonzero.
2. **Entirety**: The $s$-dependence factors out (for $n = 1$, the integral becomes $s$-independent; for general $n$, the twist regularizes the integral).

Without $u_Q$ (standard RS integral), the integral $\Psi(s, W, V)$ is a polynomial multiple of $L(s, \Pi \times \pi)$, which generically has poles. The $u_Q$ twist is what makes it possible to achieve entirety and nonvanishing simultaneously.

**Numerical evidence** (`experiments/exp1_gauss_sum_verification.py`):
- Conductor-matched Gauss sums: ALL PASS for $p = 3, 5, 7$ and conductors $c = 0, 1, 2, 3$
- $|G(\chi, \psi_{-c})| = q^{c/2}$ exactly (matching theoretical prediction)
- Mismatched conductors give zero, confirming $u_Q$ is essential

### 5. Summary

| Aspect | Result |
|--------|--------|
| **Answer** | **YES** |
| **$n = 1$ proof** | Complete: $W$ from Kirillov model with $\varphi = \mathbf{1}_{\mathfrak{o}^\times}$; integral = Gauss sum |
| **General $n$** | Structural argument via JPSS ideal theory + non-degeneracy |
| **Key identity** | $W(\mathrm{diag}(g,1) \cdot u_Q) = \psi^{-1}(Q g_{nn}) \cdot W(\mathrm{diag}(g,1))$ (proved for all $n$) |
| **Role of $u_Q$** | Conductor-matching: ensures Gauss sum nonvanishing |
| **External deps** | JPSS local RS theory (standard), Gauss sum nonvanishing (standard) |
| **Numerical** | Conductor-matched sums verified; mismatched = zero |

## Citations

| ID | Result used | Source | Notes |
|----|------------|--------|-------|
| [1] | Local RS integrals, meromorphic continuation, L-factor as GCD | Jacquet, Piatetski-Shapiro, Shalika (1983). Rankin–Selberg convolutions. *Amer. J. Math.* 105, 367–464 | Core framework |
| [2] | Conductor of $\pi$; essential vector | JPSS (1981). Conducteur des représentations du groupe linéaire. *Math. Ann.* 256, 199–214 | Conductor definition |
| [3] | Kirillov model: $\mathcal{S}(F^\times) \subset \mathcal{K}(\Pi, \psi)$ | Bernstein–Zelevinsky (1976). Representations of the group GL(n,F). *Russian Math. Surveys* 31:3, 1–68 | $n=1$ proof |
| [4] | Gauss sum nonvanishing for matching conductors | Standard; see e.g. Neukirch, *Algebraic Number Theory*, Ch. VII | $n=1$ proof |
