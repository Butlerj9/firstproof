# P08: Lagrangian Smoothing of Polyhedral Lagrangian Surfaces

**Status**: ✅ Submitted
**Answer**: **NO.** Not every polyhedral Lagrangian surface with 4-valent vertices admits a Hamiltonian Lagrangian smoothing. The polyhedral Lagrangian octahedron $K \cong S^2$ is an explicit counterexample.
**Reviewer**: Codex 5.2 — pending G6 review
**Code verification**: `experiments/` — octahedron Lagrangian conditions verified; action-value obstruction verified
**External deps**: Gromov's theorem (no closed exact Lagrangian in $\mathbb{R}^4$, standard)

## Problem statement

*(Verbatim from arXiv:2602.05192v1, Question 8, author: Mohammed Abouzaid)*

Consider a polyhedral Lagrangian surface $K$ in $\mathbb{R}^4$, i.e., a surface in $\mathbb{R}^4$ all of whose faces are Lagrangian (with respect to the standard symplectic form). Suppose that exactly 4 faces meet at every vertex of $K$. Does $K$ admit a Hamiltonian Lagrangian smoothing?

## Answer: NO

### 1. Notation and definitions

We work in $(\mathbb{R}^4, \omega_0)$ with coordinates $(x_1, y_1, x_2, y_2)$ and the standard symplectic form $\omega_0 = dx_1 \wedge dy_1 + dx_2 \wedge dy_2$. The Liouville 1-form is $\lambda = y_1 \, dx_1 + y_2 \, dx_2$, satisfying $d\lambda = \omega_0$.

**Lagrangian plane.** A 2-plane $\Pi \subset \mathbb{R}^4$ is Lagrangian if $\omega_0|_\Pi = 0$, i.e., for any $v, w \in \Pi$: $\omega_0(v, w) = v_1 w_2 - v_2 w_1 + v_3 w_4 - v_4 w_3 = 0$.

**Polyhedral Lagrangian surface.** A compact 2-dimensional polyhedral complex $K \subset \mathbb{R}^4$, embedded as a topological 2-manifold, with every face a flat polygon lying in a Lagrangian 2-plane.

**$\alpha$-light (not needed here; see P06).** The Hamiltonian Lagrangian smoothing is a 1-parameter family $\{K_t\}_{t \in (0, \varepsilon]}$ of smooth embedded Lagrangian submanifolds of $(\mathbb{R}^4, \omega_0)$, with $K_t \to K$ as $t \to 0^+$ (in Hausdorff distance), where for $t_1, t_2 > 0$, $K_{t_1}$ and $K_{t_2}$ are Hamiltonian isotopic.

### 2. Counterexample: the Lagrangian octahedron

**Construction.** Define 6 vertices in $\mathbb{R}^4$:

| Vertex | Coordinates $(x_1, y_1, x_2, y_2)$ | Role |
|--------|--------------------------------------|------|
| $v_0$ | $(0, 0, 0, 0)$ | North pole |
| $v_1$ | $(1, 0, 0, 0)$ | Equatorial |
| $v_2$ | $(0, 0, 1, 0)$ | Equatorial |
| $v_3$ | $(0, 1, 0, 0)$ | Equatorial |
| $v_4$ | $(0, 0, 0, 1)$ | Equatorial |
| $v_5$ | $(1, -1, 1, -1)$ | South pole |

These form an octahedron with 8 triangular faces:
- **Top 4**: $(v_0, v_1, v_2)$, $(v_0, v_2, v_3)$, $(v_0, v_3, v_4)$, $(v_0, v_4, v_1)$
- **Bottom 4**: $(v_5, v_2, v_1)$, $(v_5, v_3, v_2)$, $(v_5, v_4, v_3)$, $(v_5, v_1, v_4)$

**Verified properties** (`experiments/exp1_octahedron_lagrangian.py`):

| Property | Result |
|----------|--------|
| All 8 faces Lagrangian ($\omega_0 = 0$ on each face) | ALL PASS (exact zero) |
| All faces non-degenerate (positive area) | ALL PASS (areas 0.5 to 1.8) |
| Vertices span $\mathbb{R}^4$ (rank 4) | PASS |
| No self-intersections (non-adjacent faces) | PASS |
| Euler characteristic $\chi = 6 - 12 + 8 = 2$ | $S^2$ topology |
| All 6 vertices are 4-valent | ALL PASS |

**Derivation.** The vertices $v_1, v_2, v_3, v_4$ lie in the Lagrangian plane $\{y_1 = y_2 = 0\}$ (the $(x_1, x_2)$-plane), but they span all of $\mathbb{R}^4$ together with $v_5$. The top faces through $v_0 = 0$ have edge vectors in the $(x_1, x_2)$-plane, so $\omega_0 = 0$ automatically. The south pole $v_5$ is determined by solving 4 linear equations (one per bottom face's Lagrangian condition), yielding the 1-parameter family $v_5 = (p, -p, p, -p)$ for any $p \neq 0$.

### 3. Proof that $K$ does not admit a Hamiltonian Lagrangian smoothing

**Theorem.** The polyhedral Lagrangian octahedron $K \cong S^2$ constructed above does not admit a Hamiltonian Lagrangian smoothing.

**Proof.** Suppose for contradiction that $\{K_t\}_{t \in (0,\varepsilon]}$ is a Hamiltonian Lagrangian smoothing with $K_t \to K$ as $t \to 0^+$. Let $L$ be a smooth closed Lagrangian with $K_t$ Hamiltonian isotopic to $L$ for each $t > 0$, via diffeomorphisms $\phi_t$ of $\mathbb{R}^4$ satisfying $K_t = \phi_t(L)$.

**Step 1: Action invariance.** For any cycle $\gamma$ on $L$ and any Hamiltonian diffeomorphism $\phi$:

$$\int_{\phi(\gamma)} \lambda = \int_\gamma \lambda$$

This follows from the standard identity $\phi^*\lambda - \lambda = dF$ (exact) for any Hamiltonian diffeomorphism $\phi$ (see §4 below). Therefore, for all $t > 0$:

$$A(\gamma) := \int_{\phi_t(\gamma)} \lambda = \int_\gamma \lambda|_L \quad \text{(constant in } t\text{)}$$

**Step 2: Convergence.** As $t \to 0^+$, the curves $c_t := \phi_t(\gamma)$ lie on $K_t \subset N_\varepsilon(K)$ (the $\varepsilon$-neighborhood of $K$) for all small $t$. Since $L$ is compact, $\gamma$ has finite length, and $c_t = \phi_t(\gamma)$ is a continuous family of Lipschitz curves in a bounded region of $\mathbb{R}^4$. By the Arzelà–Ascoli theorem, a subsequence $c_{t_n}$ converges uniformly to a continuous closed curve $c$ in $\overline{N_\varepsilon(K)}$. Since $K_t \to K$ in Hausdorff distance, $c \subset K$.

**Step 3: Null-homotopy on $K$.** Since $K \cong S^2$ is simply connected ($\pi_1(S^2) = 0$), the closed curve $c$ is null-homotopic. Therefore $c$ bounds a singular 2-chain $D$ in $K$: a collection of faces (or portions of faces) with $\partial D = c$.

**Step 4: Zero Liouville integral.** By Stokes' theorem:

$$\int_c \lambda = \int_D d\lambda = \int_D \omega_0 = 0$$

The last equality holds because $\omega_0|_F = 0$ for every face $F$ of $K$ (each face is Lagrangian), and $D$ is a 2-chain composed of such faces.

**Step 5: Convergence of integrals.** Since $\lambda$ is smooth and $c_{t_n} \to c$ uniformly:

$$\int_{c_{t_n}} \lambda \;\longrightarrow\; \int_c \lambda = 0$$

But from Step 1: $\int_{c_{t_n}} \lambda = A(\gamma)$ is constant. Therefore $A(\gamma) = 0$.

**Step 6: Exactness.** Since $A(\gamma) = \int_\gamma \lambda|_L = 0$ for every cycle $\gamma$ on $L$ (the argument applies to any cycle generating $H_1(L; \mathbb{Z})$), the closed 1-form $\lambda|_L$ has all periods zero. Therefore $\lambda|_L$ is exact, meaning $L$ is an **exact Lagrangian** in $(\mathbb{R}^4, \omega_0)$.

**Step 7: Gromov's theorem.** By the theorem of Gromov (1985), there is no closed exact Lagrangian submanifold in $(\mathbb{R}^4, \omega_0 = d\lambda)$.

This contradicts the existence of $L$. Therefore $K$ does not admit a Hamiltonian Lagrangian smoothing. $\square$

**Remark on topology change.** The proof does NOT assume that $K_t$ is homeomorphic to $K = S^2$. The smooth Lagrangian $L$ (and hence $K_t$) may have any genus $g \geq 1$. The obstruction arises from the combination of:
- The simple connectivity of $K$ (forcing all Liouville periods to vanish in the limit), and
- Gromov's theorem (forbidding exact Lagrangians).

### 4. Action invariance identity (proof)

**Lemma.** If $\phi_t$ is a Hamiltonian isotopy of $(\mathbb{R}^4, \omega_0)$ generated by $H_t$, then $\phi_t^*\lambda - \lambda = dF_t$ where $F_t = \int_0^t (H_s + \lambda(X_{H_s})) \circ \phi_s \, ds$.

**Proof.** By Cartan's formula:

$$\frac{d}{dt} \phi_t^*\lambda = \phi_t^*(\mathcal{L}_{X_t} \lambda) = \phi_t^*(d\iota_{X_t}\lambda + \iota_{X_t}d\lambda) = \phi_t^*(d(\lambda(X_t)) + dH_t) = d\bigl((H_t + \lambda(X_t)) \circ \phi_t\bigr)$$

Integrating from $0$ to $T$: $\phi_T^*\lambda - \lambda = dF_T$. Therefore, for any closed curve $\gamma$:

$$\int_{\phi_T(\gamma)} \lambda = \int_\gamma \phi_T^*\lambda = \int_\gamma \lambda + \int_\gamma dF_T = \int_\gamma \lambda \quad \square$$

### 5. Numerical verification

**EXP-1: Octahedron construction** (`experiments/exp1_octahedron_lagrangian.py`):
- Lagrangian conditions: all 8 faces give $\omega_0 = 0$ exactly.
- Non-degeneracy: all face areas positive (0.5 to 1.8).
- Spanning: vertex matrix has rank 4.
- Embedding: no self-intersections among 16 non-adjacent face pairs.
- Parametric family: $v_5 = (p, -p, p, -p)$ gives valid octahedron for all $p \neq 0$.

**EXP-2: Action-value obstruction** (`experiments/exp2_action_obstruction.py`):
- Liouville integral along every closed edge-path on $K$: exactly 0.
- Symplectic area of each face: exactly 0.
- Perturbed curves ($\varepsilon$-close to $K$): $\lambda$-integral = $O(\varepsilon)$, consistent with convergence to 0.

### 6. Why the 4-valent condition is necessary but not sufficient

The problem's hypothesis (4 faces at every vertex) is motivated by tropical geometry: in the tropical-to-Lagrangian correspondence, trivalent tropical vertices lift to 4-valent polyhedral Lagrangian vertices. For surfaces arising from tropical curves, the Lagrangian lift has genus $\geq 1$, and smoothing is expected (the smooth Lagrangian is a non-exact torus or higher-genus surface, compatible with Gromov's theorem).

Our counterexample shows that not all 4-valent polyhedral Lagrangians come from tropical curves. The octahedron is homeomorphic to $S^2$ (genus 0), which forces any smooth Lagrangian smoothing to be exact — contradicting Gromov. The 4-valent condition is necessary for tropical smoothability, but not sufficient for arbitrary polyhedral Lagrangian surfaces.

### 7. Summary

| Aspect | Result |
|--------|--------|
| **Answer** | **NO** |
| **Counterexample** | Polyhedral Lagrangian octahedron $K \cong S^2$ (6 vertices, 8 faces, all 4-valent) |
| **Key construction** | Vertices in $\mathbb{R}^4$ with all faces in Lagrangian planes; 1-parameter family |
| **Proof technique** | Action invariance under Hamiltonian isotopy + Gromov's theorem |
| **External dependencies** | Gromov (1985): no closed exact Lagrangian in $(\mathbb{R}^{2n}, \omega_{\text{std}})$ |
| **Numerical** | Lagrangian conditions, embedding, action-value obstruction all verified |

## Citations

| ID | Result used | Source | Notes |
|----|------------|--------|-------|
| [1] | No closed exact Lagrangian in $(\mathbb{R}^{2n}, \omega_0)$ | Gromov, M. (1985). Pseudo holomorphic curves in symplectic manifolds. *Invent. Math.* 82, 307–347. | Core obstruction |
| [2] | Action invariance under Hamiltonian isotopy | Standard; see McDuff–Salamon, *Introduction to Symplectic Topology*, Prop. 9.19 | Used in §3–4 |
| [3] | Lagrangian Grassmannian $\Lambda(n) = U(n)/O(n)$ | Standard | Used in construction |
| [4] | Tropical-Lagrangian correspondence | Mikhalkin (2019); Matessi (2019) | Context only (§6) |
