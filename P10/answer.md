# P10: RKHS CP-ALS — Matrix-free Preconditioned Conjugate Gradient Solver

**Status**: ✅ Submitted
**Reviewer**: Codex 5.2 — verdict: ACCEPT (0 faults, 3 minor residual risks acknowledged)
**Scout check**: GPT Pro — consistent with our derivation
**Code verification**: `experiments/verify_matvec.py` — ALL TESTS PASSED (seed=42, n=4, r=2, q=8)
**External deps**: 0 unresolved (all results are standard linear algebra, proved inline)

## Problem statement

*(Verbatim from arXiv:2602.05192v1, Question 10)*

Given a $d$-way tensor $T \in \mathbb{R}^{n_1 \times n_2 \times \cdots \times n_d}$ with missing entries, we consider the problem of computing a CP decomposition of rank $r$ where some modes are infinite-dimensional and constrained to be in a Reproducing Kernel Hilbert Space (RKHS). We use an alternating optimization approach, and our question is focused on the mode-$k$ subproblem for an infinite-dimensional mode.

The system to be solved is:

$$\left[(Z \otimes K)^T S S^T (Z \otimes K) + \lambda(I_r \otimes K)\right] \operatorname{vec}(W) = (I_r \otimes K) \operatorname{vec}(B)$$

where $N = \prod_i n_i$, $n \equiv n_k$, $M = \prod_{i \neq k} n_i$, $K \in \mathbb{R}^{n \times n}$ is the PSD RKHS kernel matrix, $Z \in \mathbb{R}^{M \times r}$ is the Khatri-Rao product of all other factor matrices, $S \in \mathbb{R}^{N \times q}$ is a selection matrix ($q$ columns of $I_N$), $B = TZ \in \mathbb{R}^{n \times r}$ is the MTTKRP, and $W \in \mathbb{R}^{n \times r}$ is the unknown. Regime: $n, r < q \ll N$. Avoid any computation of order $N$.

## Answer

### 1. Notation and setup

We define the system matrix and right-hand side:

$$A := (Z \otimes K)^T S S^T (Z \otimes K) + \lambda(I_r \otimes K), \qquad b := (I_r \otimes K)\operatorname{vec}(B) = \operatorname{vec}(KB).$$

The system $A\operatorname{vec}(W) = b$ has size $nr \times nr$. A direct solve costs $O(n^3 r^3)$. We describe an iterative solver that avoids this and, critically, avoids any $O(N)$ operations.

Each observed tensor entry $p \in \{1, \ldots, q\}$ corresponds to a position in the mode-$k$ unfolding of $T$: a row index $i_p \in [n]$ (the mode-$k$ index) and a column index $j_p \in [M]$ (the flattened multi-index over all other modes, obtained by mapping the multi-index $(i_1^{(p)}, \ldots, i_{k-1}^{(p)}, i_{k+1}^{(p)}, \ldots, i_d^{(p)})$ to a single column index via the standard column-major convention). The row of $Z$ at position $j_p$ can be computed from the factor matrices as:

$$z^{(p)} := Z(j_p, :) = \bigodot_{\ell \neq k} A_\ell(i_\ell^{(p)}, :) \in \mathbb{R}^r$$

where $\odot$ denotes the Hadamard (element-wise) product and $i_\ell^{(p)}$ is the mode-$\ell$ index of observation $p$. This costs $O((d-1)r)$ per observation and avoids ever forming $Z$ explicitly.

### 2. The system matrix $A$ is symmetric positive semidefinite; CG applicability

The problem states that $K$ is PSD (positive semidefinite). We analyze both the PSD and SPD cases.

**Claim.** $A$ is always PSD. If $K$ is SPD (positive definite), then $A$ is SPD.

*Proof.* Write $C := S^T(Z \otimes K) \in \mathbb{R}^{q \times nr}$. Then $(Z \otimes K)^T S S^T (Z \otimes K) = C^T C \succeq 0$ (positive semidefinite, as a Gram matrix). The regularization term $\lambda(I_r \otimes K)$ is PSD when $K$ is PSD: for any $v \in \mathbb{R}^{nr}$, reshape $v$ as $V \in \mathbb{R}^{n \times r}$ and note $v^T(\lambda I_r \otimes K)v = \lambda \sum_{j=1}^r V_{:,j}^T K V_{:,j} \geq 0$. Therefore $A = C^TC + \lambda(I_r \otimes K) \succeq 0$.

If additionally $K \succ 0$ (SPD), then $\lambda(I_r \otimes K) \succ 0$, so $A \succ 0$ (SPD), and the standard conjugate gradient method applies directly. $\square$

**Remark (PSD case).** If $K$ is only PSD with $\operatorname{null}(K) \neq \{0\}$, then $A$ is singular. In this case, define $\hat{K} := K + \delta I_n$ for a small $\delta > 0$ (jitter regularization), which is standard practice for RKHS kernel matrices. Replacing $K$ by $\hat{K}$ makes $A$ SPD and CG applies. The jitter $\delta$ can be chosen as small as machine precision times $\|K\|$ without affecting the mathematical structure. Alternatively, one may restrict the system to $\operatorname{range}(I_r \otimes K)$ and solve the reduced SPD system there. **In what follows, we assume $K$ is SPD** (either inherently or after jitter), which is the standard numerical setup for RKHS kernel methods.

### 3. Matrix-free matvec: computing $y = A\operatorname{vec}(V)$

The key to an efficient iterative solver is computing $y = A\operatorname{vec}(V)$ for arbitrary $V \in \mathbb{R}^{n \times r}$ without forming any $N$-dimensional object. We use two standard Kronecker product identities.

**Identity 1.** For matrices $P \in \mathbb{R}^{m_1 \times m_2}$, $X \in \mathbb{R}^{m_2 \times m_3}$, $Q \in \mathbb{R}^{m_4 \times m_3}$:

$$\operatorname{vec}(PXQ^T) = (Q \otimes P)\operatorname{vec}(X).$$

*Proof.* This is the standard vec-Kronecker identity. It follows from the bilinearity of the Kronecker product and the definition of vectorization. Specifically, $(Q \otimes P)\operatorname{vec}(X) = \sum_{j} (Q_{:,j} \otimes P X_{:,j})$, which upon rearranging gives $\operatorname{vec}(PXQ^T)$. $\square$

**Identity 2 (Transpose).** Since $K = K^T$ (symmetric):

$$(Z \otimes K)^T = Z^T \otimes K, \qquad (Z^T \otimes K)\operatorname{vec}(Y) = \operatorname{vec}(KYZ).$$

*Proof.* $(Z \otimes K)^T = Z^T \otimes K^T = Z^T \otimes K$. Apply Identity 1 with $P = K$, $X = Y$, $Q = Z$. $\square$

**The matvec decomposition.** We want to compute:

$$A\operatorname{vec}(V) = \underbrace{(Z \otimes K)^T S S^T (Z \otimes K)\operatorname{vec}(V)}_{\text{data-fit term}} + \underbrace{\lambda(I_r \otimes K)\operatorname{vec}(V)}_{\text{regularization term}}$$

The **regularization term** is simply $\lambda \operatorname{vec}(KV)$, computed by a single dense matrix multiply $KV$ at cost $O(n^2 r)$.

For the **data-fit term**, we proceed in stages:

**Stage 1: Forward map.** By Identity 1, $(Z \otimes K)\operatorname{vec}(V) = \operatorname{vec}(KVZ^T)$. This is a vector of length $N = nM$, which we must **not form explicitly**. Instead, we observe that $SS^T$ is the $N \times N$ diagonal matrix with 1s at the $q$ observed positions. So $SS^T \operatorname{vec}(KVZ^T)$ selects exactly the $q$ entries of $KVZ^T$ at observed positions. For observation $p$ at unfolding position $(i_p, j_p)$:

$$[KVZ^T]_{i_p, j_p} = (KV)(i_p, :) \cdot Z(j_p, :)^T = U(i_p, :) \cdot z^{(p)}$$

where $U := KV \in \mathbb{R}^{n \times r}$ and $z^{(p)} = Z(j_p, :) \in \mathbb{R}^r$. Call this scalar $y_p$.

**Stage 2: Backward map.** We need $(Z^T \otimes K)$ applied to the sparse vector $\sum_p y_p \, e_{(i_p, j_p)}$ where $e_{(i_p, j_p)}$ is the standard basis vector at the observed position. By linearity and Identity 2:

$$(Z^T \otimes K) \sum_p y_p \, e_{(i_p, j_p)} = \sum_p y_p \operatorname{vec}(K \, E_{i_p j_p} \, Z) = \operatorname{vec}\left(K \left[\sum_p y_p \, e_{i_p} (z^{(p)})^T\right]\right)$$

where $E_{ij}$ is the matrix with a single 1 at position $(i,j)$. Define the accumulator:

$$C := \sum_{p=1}^{q} y_p \, e_{i_p} (z^{(p)})^T \in \mathbb{R}^{n \times r}$$

which is computed by: for each observation $p$, add $y_p \cdot z^{(p)}$ to row $i_p$ of $C$. Then the backward map gives $\operatorname{vec}(KC)$.

**Complete algorithm:**

> **Input:** $V \in \mathbb{R}^{n \times r}$
>
> 1. $U \leftarrow KV$ $\hfill O(n^2 r)$
> 2. $C \leftarrow 0 \in \mathbb{R}^{n \times r}$
> 3. **For** $p = 1, \ldots, q$:
>    - Compute $z^{(p)} = \bigodot_{\ell \neq k} A_\ell(i_\ell^{(p)}, :)$ $\hfill O((d-1)r)$
>    - $y_p \leftarrow U(i_p, :) \cdot z^{(p)}$ $\hfill O(r)$
>    - $C(i_p, :) \mathrel{+}= y_p \cdot z^{(p)}$ $\hfill O(r)$
> 4. $D \leftarrow KC$ $\hfill O(n^2 r)$
> 5. **Return** $\operatorname{vec}(D + \lambda U)$

**Total matvec cost:** $O(n^2 r + qdr)$.

No array of size $N$, $M$, or $nM$ is ever formed. The $Z$ matrix is never stored; each row $z^{(p)}$ is computed on-the-fly from the factor matrices.

### 4. Right-hand side computation

The RHS is $b = \operatorname{vec}(KB)$ where $B = TZ$ is the MTTKRP. Since $T$ has missing entries set to zero, $B$ can be computed from the observations alone:

> 1. $B \leftarrow 0 \in \mathbb{R}^{n \times r}$
> 2. **For** $p = 1, \ldots, q$:
>    - Compute $z^{(p)}$ as above $\hfill O((d-1)r)$
>    - $B(i_p, :) \mathrel{+}= t_p \cdot z^{(p)}$ $\hfill O(r)$
> 3. $b \leftarrow \operatorname{vec}(KB)$ $\hfill O(n^2 r)$

where $t_p$ is the observed tensor value at entry $p$. **Cost:** $O(qdr + n^2 r)$, computed once.

### 5. PCG algorithm

The preconditioned conjugate gradient method solves $Ax = b$ iteratively given:
- A matvec routine $v \mapsto Av$ (Section 3)
- A preconditioner solve routine $v \mapsto M^{-1}v$ (Section 6)

> **PCG Algorithm:**
>
> 1. $W_0 \leftarrow 0$, $\; r_0 \leftarrow b - A\operatorname{vec}(W_0)$, $\; z_0 \leftarrow M^{-1} r_0$, $\; p_0 \leftarrow z_0$
> 2. **For** $k = 0, 1, 2, \ldots$ until $\|r_k\| < \varepsilon \|b\|$:
>    - $\alpha_k \leftarrow \frac{r_k^T z_k}{p_k^T A p_k}$
>    - $x_{k+1} \leftarrow x_k + \alpha_k p_k$
>    - $r_{k+1} \leftarrow r_k - \alpha_k A p_k$
>    - $z_{k+1} \leftarrow M^{-1} r_{k+1}$
>    - $\beta_k \leftarrow \frac{r_{k+1}^T z_{k+1}}{r_k^T z_k}$
>    - $p_{k+1} \leftarrow z_{k+1} + \beta_k p_k$

Each iteration requires one matvec ($O(n^2 r + qdr)$) and one preconditioner apply.

### 6. Preconditioner selection

We propose two preconditioners, both SPD and efficient to apply.

#### Preconditioner A: Regularization-based (block-Cholesky)

$$M_A := \lambda(I_r \otimes K)$$

**SPD proof.** $K$ is SPD and $\lambda > 0$, so $\lambda(I_r \otimes K)$ is SPD (same argument as Section 2). $\square$

**Apply $M_A^{-1}$:** Reshape $v$ as $V \in \mathbb{R}^{n \times r}$, solve $K Y_{:,j} = V_{:,j}$ for $j = 1, \ldots, r$ using a precomputed Cholesky factorization of $K$, return $\operatorname{vec}(Y/\lambda)$.

**Costs:**
- Precomputation: Cholesky of $K$ in $O(n^3)$ (one-time).
- Apply: $O(n^2 r)$ per PCG iteration ($r$ triangular solves of size $n$).

**When it works well:** When $\lambda$ is large relative to the data-fit term (strong regularization), $M_A \approx A$ and PCG converges in few iterations.

#### Preconditioner B: Kronecker approximation

Approximate the diagonal mask $SS^T \approx \rho I_N$ where $\rho := q/N$ is the observation density. Then:

$$(Z \otimes K)^T (\rho I_N)(Z \otimes K) = \rho(Z^TZ \otimes K^2)$$

and the preconditioner is:

$$M_B := \rho(G \otimes K^2) + \lambda(I_r \otimes K)$$

where $G := Z^TZ \in \mathbb{R}^{r \times r}$.

**Computing $G$ without forming $Z$:** By the Khatri-Rao Gram identity,

$$Z^TZ = \bigodot_{\ell \neq k} (A_\ell^T A_\ell) \in \mathbb{R}^{r \times r}$$

where $\odot$ denotes the Hadamard product. Each $A_\ell^T A_\ell$ costs $O(n_\ell r^2)$, and the Hadamard products cost $O(r^2)$ each, giving total $O((\sum_{\ell \neq k} n_\ell) r^2)$.

*Proof of the Gram identity.* Recall $Z = \bigodot_{\ell \neq k} A_\ell \in \mathbb{R}^{M \times r}$ (Khatri-Rao product over all modes except $k$). Each row of $Z$ is a Hadamard product of the corresponding factor rows: $Z(j,:) = \bigodot_{\ell \neq k} A_\ell(i_\ell,:)$ where $(i_\ell)_{\ell \neq k}$ is the multi-index corresponding to column $j$. Then $(Z^TZ)_{ab} = \sum_j Z(j,a)Z(j,b) = \sum_j \prod_{\ell \neq k} A_\ell(i_\ell,a)A_\ell(i_\ell,b)$. Since the sum over $j$ ranges over all multi-indices $(i_\ell)_{\ell \neq k}$, it factors as $\prod_{\ell \neq k} \sum_{i_\ell=1}^{n_\ell} A_\ell(i_\ell,a)A_\ell(i_\ell,b) = \prod_{\ell \neq k} (A_\ell^T A_\ell)_{ab}$. $\square$

**SPD proof.** $K^2$ is SPD ($K$ SPD implies $K^2$ SPD). $G$ is PSD (Gram matrix). The Kronecker product of PSD matrices is PSD. Since $\rho > 0$ and $\lambda > 0$, $M_B$ is SPD by the same argument as Section 2. $\square$

**Apply $M_B^{-1}$ via simultaneous diagonalization:** Compute eigendecompositions $K = V_K \Lambda_K V_K^T$ and $G = U_G \Sigma_G U_G^T$. Then:

$$M_B = (U_G \otimes V_K) \operatorname{diag}\left(\rho \sigma_j \lambda_i^2 + \lambda \lambda_i\right) (U_G \otimes V_K)^T$$

Apply $M_B^{-1}v$:
1. Reshape $v$ as $X \in \mathbb{R}^{n \times r}$
2. $\tilde{X} \leftarrow V_K^T X U_G$ $\hfill O(n^2 r + nr^2)$
3. $\tilde{X}_{ij} \leftarrow \tilde{X}_{ij} / (\rho \sigma_j \lambda_i^2 + \lambda \lambda_i)$ $\hfill O(nr)$
4. Return $\operatorname{vec}(V_K \tilde{X} U_G^T)$ $\hfill O(n^2 r + nr^2)$

**Costs:**
- Precomputation: $O(n^3 + r^3)$ for the two eigendecompositions.
- Apply: $O(n^2 r + nr^2)$ per PCG iteration.

**When it works well:** When the observation pattern is approximately uniform across the tensor. The Kronecker structure captures the interaction between the kernel ($K$) and the factor coupling ($G$).

### 7. Complexity summary

| Operation | Cost | When |
|-----------|------|------|
| Matvec $A\operatorname{vec}(V)$ | $O(n^2 r + qdr)$ | Each PCG iteration |
| RHS $b = \operatorname{vec}(KB)$ | $O(qdr + n^2 r)$ | Once |
| Gram $G = Z^TZ$ via Hadamard | $O((\sum_{\ell \neq k} n_\ell)r^2)$ | Once (for Preconditioner B) |
| Cholesky of $K$ | $O(n^3)$ | Once (for Preconditioner A) |
| Eigendecomp of $K, G$ | $O(n^3 + r^3)$ | Once (for Preconditioner B) |
| Preconditioner A apply | $O(n^2 r)$ | Each PCG iteration |
| Preconditioner B apply | $O(n^2 r + nr^2)$ | Each PCG iteration |

**Total solve cost with Preconditioner A:** $O\bigl(m(n^2 r + qdr + n^2 r) + n^3\bigr) = O\bigl(m(n^2 r + qdr) + n^3\bigr)$, where $m$ is the number of PCG iterations and $O(n^3)$ accounts for the one-time Cholesky factorization.

**Total solve cost with Preconditioner B:** $O\bigl(m(n^2 r + qdr + n^2 r + nr^2) + n^3 + r^3\bigr) = O\bigl(m(n^2 r + nr^2 + qdr) + n^3 + r^3\bigr)$, where the additional $O(n^3 + r^3)$ accounts for eigendecompositions and $O(nr^2)$ per iteration accounts for the eigenbasis transforms.

**Memory:** $O(n^2 + nr + qd + r^2)$ — kernel matrix ($n^2$), factor/accumulator matrices ($nr$), observation indices ($qd$), and Gram matrix $G$ ($r^2$) for Preconditioner B. No $O(N)$ memory.

**Comparison to direct solve:** Direct factorization of the $nr \times nr$ system matrix costs $O(n^3 r^3)$, and explicitly forming that matrix requires computing entries of $(Z \otimes K)^T SS^T(Z \otimes K)$, which involves $O(N)$ work. The PCG approach costs $O(m(n^2 r + qdr))$ per solve with no $O(N)$ operations. Standard CG convergence theory gives $\|x_k - x^*\|_A \leq 2\left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^k \|x_0 - x^*\|_A$ where $\kappa = \kappa(M^{-1}A)$ is the condition number of the preconditioned system (Golub & Van Loan, *Matrix Computations*, 4th ed., Theorem 11.3.3). Since $n, r$ are small, $n^2 r \ll n^3 r^3$, and $qdr \ll N$, this is a substantial improvement.

### 8. Why this works: summary of the key idea

The linear system matrix $A$ is $nr \times nr$ but is defined via the $N \times N$ diagonal mask $SS^T$ and the $N \times nr$ Kronecker product $Z \otimes K$. The naive approach of forming $A$ explicitly requires $O(N)$ operations. The matrix-free approach exploits three facts:

1. **Kronecker structure**: $(Z \otimes K)\operatorname{vec}(V) = \operatorname{vec}(KVZ^T)$, so the forward map factors into an $n \times n$ kernel multiply and a matrix multiply with $Z^T$.

2. **Sparsity of $SS^T$**: Only $q \ll N$ entries are observed. Instead of forming the full $n \times M$ matrix $KVZ^T$, we compute only its $q$ observed entries, each via an inner product $U(i_p, :) \cdot z^{(p)}$ costing $O(r)$.

3. **On-the-fly Khatri-Rao rows**: Each row $z^{(p)}$ of $Z$ is the Hadamard product of $d-1$ factor matrix rows, computed in $O((d-1)r)$ without storing $Z$.

The backward map $(Z^T \otimes K)$ applied to the sparse result accumulates into an $n \times r$ matrix $C$ (one rank-1 update per observation) followed by a single kernel multiply $KC$. The total per-matvec cost is $O(n^2 r + qdr)$, with no $O(N)$ operations.

## Citations

| ID | Result used | Source | Statement # | Notes |
|----|------------|--------|-------------|-------|
| [1] | Kronecker-vec identity: $\operatorname{vec}(AXB^T) = (B \otimes A)\operatorname{vec}(X)$ | Standard linear algebra; e.g., Horn & Johnson, *Matrix Analysis*, 2nd ed., Cambridge, 2012 | Theorem 4.2.10 | Proved inline |
| [2] | Khatri-Rao Gram identity: $(A \odot B)^T(A \odot B) = (A^TA) * (B^TB)$ | Kolda & Bader, "Tensor Decompositions and Applications," *SIAM Review* 51(3), 2009 | Property 2 (Section 2.6) | Proved inline |
| [3] | CP-ALS with missing data (RKHS extension) | Kileel, Trager, Ward, "Subspace power method for symmetric tensor decomposition and generalized PCA," arXiv:2408.05677 | Context for the problem formulation | |
| [4] | PCG algorithm | Golub & Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins, 2013 | Algorithm 11.5.1 | Standard algorithm |
