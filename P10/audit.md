# Audit: P10 — RKHS CP-ALS: Matrix-free PCG with preconditioner

## G0 Formalize

### Problem restatement

We are given a $d$-way tensor $T \in \mathbb{R}^{n_1 \times n_2 \times \cdots \times n_d}$ with missing entries. We seek a CP decomposition of rank $r$ where mode $k$ is infinite-dimensional and constrained to a Reproducing Kernel Hilbert Space (RKHS). We use alternating optimization, and the question focuses on the **mode-$k$ subproblem** where all other CP factor matrices $A_1, \ldots, A_{k-1}, A_{k+1}, \ldots, A_d$ are fixed.

**Given quantities and their types:**

| Symbol | Type / Space | Definition |
|--------|-------------|------------|
| $d$ | $\mathbb{Z}_{>0}$ | Number of tensor modes (ways) |
| $n_i$ | $\mathbb{Z}_{>0}$ | Size of mode $i$, for $i = 1, \ldots, d$ |
| $N$ | $\mathbb{Z}_{>0}$ | $N = \prod_i n_i$, product of all mode sizes |
| $n \equiv n_k$ | $\mathbb{Z}_{>0}$ | Size of mode $k$ (the mode being solved) |
| $M$ | $\mathbb{Z}_{>0}$ | $M = \prod_{i \neq k} n_i = N/n$, product of all dimensions except mode $k$ |
| $r$ | $\mathbb{Z}_{>0}$ | CP rank; $r < q \ll N$ and $n, r < q$ |
| $q$ | $\mathbb{Z}_{>0}$ | Number of observed entries; $q \ll N$ |
| $T \in \mathbb{R}^{n \times M}$ | Matrix | Mode-$k$ unfolding of tensor $T$ (missing entries set to zero) |
| $S \in \mathbb{R}^{N \times q}$ | Matrix | Selection matrix: $q$ columns of the $N \times N$ identity; $S^T \operatorname{vec}(T)$ selects the $q$ known entries |
| $Z \in \mathbb{R}^{M \times r}$ | Matrix | Khatri-Rao product $A_d \odot \cdots \odot A_{k+1} \odot A_{k-1} \odot \cdots \odot A_1$ |
| $K \in \mathbb{R}^{n \times n}$ | Matrix (SPD) | RKHS kernel matrix for mode $k$ |
| $W \in \mathbb{R}^{n \times r}$ | Matrix (unknown) | The unknown; factor matrix is $A_k = KW$ |
| $B \in \mathbb{R}^{n \times r}$ | Matrix | $B = TZ$, the MTTKRP (Matricized Tensor Times Khatri-Rao Product) |
| $\lambda > 0$ | Scalar | Regularization parameter |
| $I_r$ | $\mathbb{R}^{r \times r}$ | Identity matrix of size $r$ |

**The linear system to solve:**

$$\left[(Z \otimes K)^T S S^T (Z \otimes K) + \lambda(I_r \otimes K)\right] \operatorname{vec}(W) = (I_r \otimes K) \operatorname{vec}(B)$$

This is a system of size $nr \times nr$ in the unknown $\operatorname{vec}(W) \in \mathbb{R}^{nr}$.

**What is asked:**

1. Explain how an iterative preconditioned conjugate gradient (PCG) solver can solve this more efficiently than the $O(n^3 r^3)$ direct solve.
2. Explain the method and choice of preconditioner.
3. Explain in detail how the matrix-vector products are computed and why this works.
4. Provide complexity analysis.
5. **Constraint**: $n, r < q \ll N$. Avoid any computation of order $N$.

### Object glossary

| Symbol | Type / Space | Definition |
|--------|-------------|------------|
| $\otimes$ | Operator | Kronecker product |
| $\odot$ | Operator | Khatri-Rao (column-wise Kronecker) product |
| $\operatorname{vec}(\cdot)$ | Operator | Vectorization (stacks columns) |
| $A$ (system matrix) | $\mathbb{R}^{nr \times nr}$ (SPD) | $A = (Z \otimes K)^T S S^T (Z \otimes K) + \lambda(I_r \otimes K)$ |
| $b$ (RHS) | $\mathbb{R}^{nr}$ | $b = (I_r \otimes K) \operatorname{vec}(B)$ |
| $S S^T$ | $\mathbb{R}^{N \times N}$ | Diagonal 0/1 matrix indicating observed entries (since $S$ has orthonormal columns, $SS^T$ is an orthogonal projector onto observed entries) |

**Key size regime**: $n, r \ll q \ll N = nM$. The matrix $A$ is $nr \times nr$ — small enough to iterate over but we must never form $N$-dimensional objects. The "trap" is that intermediate computations in the Kronecker product $(Z \otimes K)$ naively produce vectors of size $nM = N$.

### Truth mode
- [x] EXPLAIN (this is a derivation/explanation problem, not a YES/NO theorem)

### Counterexample shape
Not applicable — this is an explanation/derivation problem, not a true/false question.

### Equivalence check

The restatement is faithful to the original. Key observations:
- The problem statement says "$S \in \mathbb{R}^{N \times q}$ denotes the selection matrix (a subset of the $N \times N$ identity matrix) such that $S^T \operatorname{vec}(T)$ selects the $q$ known entries." This means $S$ consists of $q$ columns of $I_N$, so $S^T$ is $q \times N$ and $S^T \operatorname{vec}(T) \in \mathbb{R}^q$.
- The product $SS^T$ is $N \times N$ but has rank $q$ — it is the diagonal matrix with 1s at observed positions. **We must never form this explicitly** since it is $N \times N$.
- The problem says "This is a system of size $nr \times nr$. Using a standard linear solver costs $O(n^3 r^3)$". This is the cost of directly factoring the $nr \times nr$ system matrix.
- The regime $n, r < q \ll N$ means $q$ can be much larger than $nr$ but much smaller than $N$.

**Ambiguity resolved**: The selection matrix $S$ selects entries from $\operatorname{vec}(T)$ which is the vectorization of the mode-$k$ unfolding. Each observed entry corresponds to a position $(i, j)$ in the $n \times M$ unfolding, i.e., row $i \in [n]$ and column $j \in [M]$. The vectorized index is $(j-1)n + i$ (column-major). This mapping is critical for the matrix-free matvec.

## G1 Background

*Pending.*

## G2 Route map

*Pending.*

## G3 Lemma DAG

*Pending.*

## G1-G3 Background, Route Map, Lemma DAG

Fast-tracked: P10 is a derivation problem using standard linear algebra (Kronecker identities, CG theory). No external dependencies requiring sourcing. Single route: matrix-free matvec via Kronecker structure + observation-wise loop.

**Lemma DAG:**
- L1: Kronecker-vec identity → used for forward/backward maps
- L2: SPD of system matrix → justifies CG
- L3: Accumulator trick correctness → core of matvec
- L4: Khatri-Rao Gram identity → used for Preconditioner B
- L5: Preconditioner SPD → justifies PCG

All proved inline. No external dependencies.

## G4 Experiments

**Script**: `experiments/verify_matvec.py` | **Seed**: 42 | **Dims**: n=4, r=2, q=8, M=6

| Test | Result | Error |
|------|--------|-------|
| Matvec match | PASS | 1.6e-16 |
| RHS match | PASS | 1.7e-16 |
| Gram identity | PASS | 9.9e-17 |
| CG (no precond) | PASS | 7.8e-11 |
| PCG (Precond A) | PASS | 6.5e-14 |
| PCG (Precond B) | PASS | 2.1e-15 |

**Verdict**: All 6 tests passed. Proceed to G5.

## G5 Proof draft

Complete answer.md produced. See answer.md for full content.

## G6 Review

### Cycle 1: Codex adversarial review — REJECT (4 red flags)

1. **SPD claim fails for PSD K** (FATAL): Problem says K is PSD, not SPD. Counterexample: K=diag(1,0).
2. **Gram identity proof drops ℓ≠k**: Inline proof text inconsistent with displayed formula.
3. **Complexity table undercounts Precond B**: Missing O(r³) setup and O(nr²) per-iteration.
4. **j_p undefined**: Minor notation gap.

### Patch Cycle 1 response

All 4 faults patched in answer.md:
- P1: Added PSD/SPD distinction, jitter regularization discussion, explicit SPD assumption
- P2: Fixed Gram identity proof to use ℓ≠k throughout
- P3: Split complexity table per-preconditioner, added all missing terms
- P4: Added explicit definition of j_p

### Cycle 2: Codex re-review — ACCEPT (0 faults)

Residual risks acknowledged (all minor/expected):
1. Preconditioner B is heuristic; no conditioning-improvement guarantee
2. Jitter perturbs the original singular-kernel system
3. G1-G3 sourcing was fast-tracked

**Verdict**: ACCEPT → proceed to G7.

## G7 Package

**Status**: ✅ Submitted
- `answer.md`: Complete, self-contained answer with inline proofs, pseudocode, complexity analysis
- `audit.md`: Full gate history, review cycles, metrics
- `transcript.md`: Complete interaction log with all agent messages
- `experiments/verify_matvec.py`: Reproducible verification script (seed=42)
- `experiments/output.txt`: Test results

All criteria met:
- [x] Reviewer pass with zero unresolved faults
- [x] Independent Scout check (GPT Pro)
- [x] Code verification (all 6 tests passed)
- [x] All external dependencies resolved with statement-number citations or proved inline
- [x] No human mathematical input

## Escalation Ledger

| event_id | date | level | trigger | blocking claim | action taken | tools/models/scripts | artifact updates | validation gate/result | msg/token delta | decision |
|----------|------|-------|---------|---------------|-------------|---------------------|-----------------|----------------------|----------------|----------|
| E1 | 2026-02-10 | L4 | Sprint kickoff | — | Scout candidate ingested + independent verification | GPT-5.2-pro (scout), Claude Opus 4.6 (implementer) | answer.md drafted from scout candidate | G0 ACCEPT | ~2 msgs | proceed |
| E2 | 2026-02-10 | L3 | G0 complete | Matvec correctness, RHS match, Gram identity | Experiment-first validation (6 tests) | verify_matvec.py (seed=42) | experiments/ output | G4: ALL 6 PASS | ~2 msgs | proceed |
| E3 | 2026-02-10 | L1 | G5 complete | SPD claim fails for PSD K; Gram identity proof inconsistency; complexity undercounting | G6 adversarial review Cycle 1 | Codex 5.2 (reviewer) | — | G6 C1: REJECT (4 flags) | ~2 msgs | patch |
| E4 | 2026-02-10 | L1 | G6 C1 REJECT | SPD/PSD, Gram proof, complexity, notation | Patch all 4 faults | Claude Opus 4.6 | answer.md patched (4 sections) | G6 C2: ACCEPT (0 faults) | ~4 msgs | proceed |
| E5 | 2026-02-10 | L0 | G6 C2 ACCEPT | — | G7 package finalized | Claude Opus 4.6 | All deliverables finalized | G7 ACCEPT | ~2 msgs | **SUBMITTED** |

**Escalation summary**: Level reached: L4 (scout). Closure level: L0. Validation: G6 C2 ACCEPT + L4 scout. CONTAM: none (scout generated independently, no web search).

## Human interventions

| Timestamp | Type | Action | Justification |
|-----------|------|--------|---------------|
| 2026-02-10 | LOGISTICS | Producer provided problem PDF and markdown reference files | Providing source materials |
| 2026-02-10 | LOGISTICS | Producer provided GPT-5.2-pro initial candidate solution for P10, generated during solvability evaluation of all 10 problems | Scout deployment — initial candidate was produced by GPT-5.2-pro before the Implementer session began; Implementer then independently verified, corrected, and extended it through the full gate pipeline |
| 2026-02-10 | LOGISTICS | Producer relayed Codex G6 review verbatim | Review relay |

## Metrics

| Metric | Value |
|--------|-------|
| Messages used | ~12 of 120 budget |
| Gates completed | G0-G7 (all) |
| Status | ✅ Submitted |
| G6 cycles | 1 reject + 1 accept = 2 cycles |
| Estimated tokens (Implementer input) | ~100,000 |
| Estimated tokens (Implementer output) | ~30,000 |
| Estimated tokens (Reviewer input) | ~15,000 |
| Estimated tokens (Reviewer output) | ~4,000 |
| Scout deployments | 1 (GPT-5.2-pro initial candidate, generated during solvability evaluation) |
| Human interventions | 3 (all LOGISTICS) |
| Abstraction levels | A0 (experiments), A1 (identity application), A2 (inline proofs) |
| Wall clock time | ~2 hours |

## Orientation Note (2026-02-12)

- Method/provenance policy source: `methods_extended.md`.
- Docs organization source: `docs/README.md`.
- Detailed governance session logs: `P03/audit.md`, `P05/audit.md`, and `P09/audit.md`.
- Classification: ADMIN/LOGISTICS only. No mathematical status, proof content, or experiment claims changed in this lane.
