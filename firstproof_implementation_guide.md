# FIRSTPROOF-10: Operational Implementation Guide

**Version**: 2.0 — Sprint Mode  
**Date**: 2026-02-09  
**Deadline**: Answers released 2026-02-13 23:59 PT  
**Canonical runbook**: `firstproof.md` (when documents disagree, the runbook wins)  

---

## 0. How to use this document

This is a **directly agent-actionable** implementation plan. Each problem section contains:

1. **Success criteria** — what "solved" means, concretely
2. **Subproblem decomposition** — the actual mathematical lemmas needed
3. **Candidate methods** — ranked by feasibility for LLM agents
4. **Fine details** — the specific technical points that determine correctness
5. **LLM capability gaps** — where models will fail and why
6. **External dependencies** — papers/theorems to source, with exact references
7. **Verification plan** — how to confirm the proof is correct
8. **Agent task sequence** — ordered steps for Implementer and Reviewer

Agents should treat each problem section as a self-contained work order. The Producer (human) provides logistics only — sourcing references, managing tooling, scheduling — never mathematical ideas or content.

### Sprint mode (default)

In sprint mode, all G0–G7 gate artifacts live as **sections inside `audit.md`**; only `answer.md` is the clean output. The full 10-file-per-problem structure is available post-freeze for archival polish but is NOT required during the sprint. See `firstproof.md` for the canonical 4-file structure.

### Status taxonomy

| Status | Meaning |
|--------|---------|
| ✅ **Submitted** | Proof complete, reviewer zero red flags, all citations resolved with statement numbers |
| 🟡 **Candidate** | Coherent draft but unresolved dependency / edge case / reviewer flag |
| 📊 **Conjecture** | Strong empirical evidence, no proof. Publish as conjecture + experiments |
| ❌ **Parked** | Explored, blocked. Publish failure analysis |

Default under time pressure: 🟡. Never overclaim ✅.

### Counterexample-first principle (global)

For all YES/NO problems (P4, P6, P7, P8): allocate **at least 30-50% of early budget** to aggressive counterexample search BEFORE committing to a proof route. If a counterexample is found, that's a ✅ — write it up immediately.

### Verification stack (default, not Lean)

Verification does NOT mean "formal proof assistant" unless explicitly scoped:
1. **Adversarial reviewer** (Codex) — fault checklist, try to break weakest lemma
2. **Independent scout check** (different model family) — re-derive key identity or find gap
3. **Code sanity checks** — numerical experiments, toy cases, edge cases
4. Lean 4 ONLY for micro-lemmas already in mathlib. Never burn sprint time on autoformalization.

---

## 1. Architecture: Who does what

### 1.1 Agent roles

| Role | Model | Function | Output format |
|------|-------|----------|---------------|
| **Implementer (I)** | Claude Code Opus-4.6 | Deep mathematical work, derivations, experiments, proof drafts | Structured artifacts: lemma ledger, proof.tex, experiments/ |
| **Reviewer (R)** | Codex-5.2 | Gate enforcement, adversarial verification, hallucination detection | Accept/reject + specific fault list + required patches |
| **Scout (S)** | Kimi 2.5 / Qwen3 / DeepSeek-R1 / Gemini Deep Think | Alternative perspectives, counterexample search, literature angles | Candidate approaches, counterexamples, or "no novel insight" |
| **Producer (H)** | Human | Logistics ONLY: reference fetching, tool plumbing, admin routing | Fetched papers (verbatim, no interpretation), admin decisions |

### 1.2 Autonomy boundary (CRITICAL)

The 1stproof.org criterion states: "the AI should not rely on human input for **any mathematical idea or content**, or to help it **isolate the core of the problem**." ([1stproof.org](https://1stproof.org))

**ALLOWED human actions (LOGISTICS / ADMIN):**
- Downloading PDFs, providing verbatim theorem statements (with citation, no interpretation)
- Setting up Python/CAS environments, running code
- Choosing problem order, time allocation, when to park
- Deploying scout models with queries (framing the query is allowed; answering it is not)
- Writing commit messages, managing the repo

**DISALLOWED human actions (MATHEMATICAL CONTENT):**
- Suggesting proof strategies, reductions, key lemmas, counterexamples
- Explaining how to use a sourced theorem ("try applying Theorem 3.2 to X")
- Isolating which subproblem is the crux
- Providing mathematical intuition ("this should be true because...")
- Interpreting or summarizing reference papers beyond quoting verbatim

**Prompt authorship rule:** Any prompt containing mathematical content must be authored by I or R. Producer may dispatch Scout queries only if the query text was authored by I or R and copied verbatim.

Every human intervention is logged in the audit trail with classification: `ADMIN`, `LOGISTICS`, or `MATHEMATICAL` (the last is disqualifying). If a human action is borderline, classify it as MATHEMATICAL and flag it.

All web searches are logged in `CONTAMINATION.md` (timestamp, query, purpose). If a direct solution to a numbered problem is found: freeze that problem, log exposure, do NOT incorporate, mark as `CONTAMINATED_EXTERNAL_SOLUTION`. See `firstproof.md` Section 7 for full contamination protocol.

### 1.3 Interaction protocol

```
For each problem, for each gate:
  1. I produces artifact update
  2. R reviews: accept / reject with specific faults
  3. If reject: I patches (max 3 cycles per gate)
  4. If still failing: deploy Scout for alternative perspective
  5. If still failing: escalate to H for logistics (fetch specific paper, run tool)
  6. If still failing after scout + logistics: run latent-limit trigger check (firstproof.md §3A)
  7. If trigger met: execute one relaxed pass (expanded sources + multi-scout + exact/symbolic checks)
  8. If still failing after relaxed pass: park problem, advance curriculum, return later
```

### 1.3A Relaxed-pass checklist (for latent-limit problems)

Run this only when firstproof.md §3A trigger conditions are all satisfied.

- Confirm unresolved blocker is theorem-level (not notation/boundary hygiene).
- Log trigger evidence in `audit.md`: unresolved red flag IDs + token/budget burn.
- Expand source search to primary references for the blocked machinery; keep contamination rules.
- Run >=3 scout model families with falsification-focused prompts.
- Add exact/symbolic small-case checks and high-precision numeric boundary checks.
- End with explicit status: resolved / unresolved / contaminated.

### 1.4 Scout deployment strategy

Scouts are deployed for **latent space diversity**, not redundancy. Each model family encodes different mathematical training distributions:

- **DeepSeek-R1/V3**: Strong on algebraic manipulation, combinatorics, competition-style reductions. Deploy on P4, P6, P9, P10.
- **Kimi 2.5**: Extended context window, strong Chinese mathematical corpus (algebraic geometry, number theory traditions). Deploy on P2, P9.
- **Qwen3-235B**: High CodeForces Elo suggests strength in algorithmic/constructive problems. Deploy on P3, P6, P10.
- **Gemini 3.0 Deep Think**: Extended reasoning, strong on exploratory domains. Deploy on P1, P5, P7, P8.

Scout queries should be **structured differently** from Implementer queries to maximize diversity:
- Ask for the "simplest possible counterexample" (even when you expect truth)
- Ask "what is the one-line intuition for why this should be true/false?"
- Ask for connections to other areas the Scout might know better
- Ask for the proof strategy they would use if limited to 1 page

---

## 2. Global gate definitions

Every problem passes through these gates sequentially. A gate is passed when the Reviewer explicitly accepts.

### G0 — FORMALIZE (hard gate)
**Artifacts**: `00_formalization.md`
- [ ] Problem restated in agent's own words with all quantifiers explicit
- [ ] Every symbol defined; every object's type/space specified
- [ ] Truth mode determined: prove / disprove / explore both
- [ ] Glossary of all mathematical objects with their properties
- [ ] "What would a counterexample look like?" description

**Acceptance**: Reviewer confirms restatement is equivalent to original. No ambiguous symbols.

### G1 — BACKGROUND (hard gate)
**Artifacts**: `01_background.md`, `01_references.bib`
- [ ] 10-20 prerequisite concepts/theorems listed
- [ ] Each marked: KNOWN (agent can prove) / ED (external dependency, needs source) / SKIP (not needed)
- [ ] For each ED: exact reference with theorem number, or "NEEDS SOURCING" for Producer
- [ ] 1-2 page "toolkit notes" with the key results that will be used

**Acceptance**: Every ED has either a source or a sourcing plan. No "it is well known" without citation.

### G2 — ROUTE MAP (hard gate)
**Artifacts**: `02_route_map.md`
- [ ] 2-4 candidate solution strategies, each with:
  - One-sentence summary
  - Key lemma chain (what needs proving)
  - Expected difficulty bottleneck
  - "This fails if..." condition
- [ ] Primary route selected with justification
- [ ] Backup route identified
- [ ] Scout consultation results (if deployed)

**Acceptance**: Selected route has a plausible lemma chain. Backup route is genuinely different (not a minor variant).

### G3 — LEMMA DAG (hard gate)
**Artifacts**: `03_lemma_dag.md`, `03_lemma_dag.json`
- [ ] Every lemma has: ID, statement, role, dependencies, status (TODO/SKETCH/PROVEN/CITED/BLOCKED)
- [ ] DAG is complete: proving all lemmas implies the main result
- [ ] Each lemma has an acceptance test: "this lemma is verified if..."
- [ ] External dependencies fully resolved or marked BLOCKED with sourcing request

**Acceptance**: DAG is logically complete. No circular dependencies. Critical path identified.

### G4 — EXPERIMENTS (soft gate, strongly recommended)
**Artifacts**: `04_experiments/` directory with scripts and outputs
- [ ] Small cases computed (n=2,3,4 or equivalent)
- [ ] Counterexample search attempted (even if expecting truth)
- [ ] Sanity checks on intermediate results
- [ ] Results logged with reproducibility info (seeds, versions)

**Acceptance**: No immediate counterexample found. Experiments consistent with proposed route (or route pivoted).

### G5 — PROOF DRAFT (hard gate)
**Artifacts**: `05_proof.tex` or `05_proof.md`
- [ ] Complete proof with no gaps, handwaves, or "clearly"
- [ ] Every lemma from DAG either proven inline or cited
- [ ] All assumptions explicit
- [ ] Compiles/renders correctly

**Acceptance**: Every step is justifiable. No uncited claims. No missing cases.

### G6 — ADVERSARIAL REVIEW (hard gate)
**Artifacts**: `06_review.md`
- [ ] Reviewer attempts to break proof at weakest lemma
- [ ] Edge cases / degeneracies / boundary conditions checked
- [ ] Counterexample attempts documented
- [ ] Hidden assumptions surfaced and addressed
- [ ] "Proof stress test": rewrite as explicit implication chain

**Acceptance**: No unresolved red flags. Remaining risks explicitly enumerated with severity.

### G7 — PACKAGE (hard gate)
**Artifacts**: `07_final_answer.md`, `07_audit_trail.md`, `07_metrics.json`
- [ ] Clean final answer (proof or counterexample)
- [ ] Audit trail (what changed and why at each gate)
- [ ] Metrics summary (prompts, tokens, tool calls, human interventions)
- [ ] All external dependencies verified or explicitly listed as assumptions

**Acceptance**: A third party can follow the reasoning from problem to solution.

### External dependency handling (binary rule)

For **✅ Submitted**: every external result must have a statement-number citation (journal or arXiv) OR be proved inline. No exceptions.

For **🟡 Candidate**: `NEEDS CITATION` flags are allowed but must be enumerated in `audit.md` risk list with the exact claim that depends on them.

For **📊 Conjecture / ❌ Parked**: citation gaps are acceptable but should be noted.

### Sprint mode note

In sprint mode, G0–G7 artifacts are **sections inside `audit.md`**, not separate files. Only `answer.md` is a clean standalone output. The artifact filenames listed above (e.g., `00_formalization.md`) are conceptual labels, not required files. See `firstproof.md` for the canonical 4-file structure.

---

## 3. Metrics collection schema

Every agent interaction generates an event record:

```json
{
  "timestamp": "ISO8601",
  "problem_id": "P06",
  "gate": "G3",
  "agent": "implementer|reviewer|scout|human",
  "model": "opus-4.6|codex-5.2|deepseek-r1|kimi-2.5|qwen3|gemini-3.0",
  "mode": "direct|agentic|tool_assisted",
  "prompt_tokens": 0,
  "response_tokens": 0,
  "reasoning_tokens": 0,
  "tools_used": ["python", "sympy", "web_search"],
  "abstraction_level": "A0|A1|A2|A3|A4",
  "artifact_written": ["lemma_dag.md"],
  "confidence_self_report": 0.0,
  "risk_flags": ["uncited_theorem", "quantifier_gap", "missing_edge_case"],
  "human_intervention": null,
  "outcome": "accepted|rejected|partial|escalated",
  "notes": ""
}
```

**Abstraction levels**:
- A0: Concrete computation / numerical check
- A1: Named lemma application / definition work
- A2: New lemma with proof within known framework
- A3: Strategic reduction / equivalence / reframing
- A4: New definition or framework introduction

**Aggregates to compute per problem**:
- Total prompts per agent, total tokens
- Gate cycle counts (iterations to pass each gate)
- Human intervention count + category breakdown
- Tool call distribution
- Abstraction level distribution
- Time from G0 to G7 (or parking)
- External dependency count (cited vs. sourced vs. unresolved)

---

## 4. Problem ordering rationale

The curriculum builds reusable tooling early:

| Order | Problem | Why now | Builds |
|-------|---------|---------|--------|
| 1 | **P10** | Most concrete; validates pipeline | Matrix-free reasoning, complexity analysis, experiment harness |
| 2 | **P6** | Spectral/PSD; computational | PSD certificate toolkit, counterexample search, matrix concentration |
| 3 | **P4** | Inequality + computation | Symbolic algebra, root analysis, numeric verification discipline |
| 4 | **P9** | Algebraic invariants | Genericity reasoning, invariant theory, CAS integration |
| 5 | **P3** | Combinatorial + probabilistic | Markov chain design, detailed balance, definition precision |
| 6 | **P2** | Representation theory | Hypothesis management, "named results" discipline, analytic convergence |
| 7 | **P1** | Measure theory (infinite dim) | Quasi-invariance logic, Cameron-Martin reasoning |
| 8 | **P7** | Group theory + topology | Lattice theory, torsion handling, cohomological arguments |
| 9 | **P8** | Symplectic geometry | Local-to-global obstruction reasoning |
| 10 | **P5** | Equivariant homotopy | Most specialized; needs hardened process |

---

## 4A. Triage scoring

| Problem | Def risk | Ref load | Falsifiable? | Search space | Autonomy risk | Triage class |
|---------|----------|----------|-------------|--------------|---------------|-------------|
| **P10** | LOW (standard LA) | LOW | YES (toy dims) | NARROW (derivation) | LOW | **GREEN** |
| **P4** | LOW (explicit formula) | LOW-MED | YES (numerics) | MEDIUM (generalize n=2) | LOW | **GREEN** |
| **P6** | LOW (Laplacian PSD) | MEDIUM | YES (graph experiments) | MEDIUM (concentration) | LOW | **GREEN** |
| **P9** | MEDIUM (tensor indices) | MEDIUM | YES (CAS, n=5) | WIDE (invariant theory) | MEDIUM | **YELLOW** |
| **P3** | HIGH (niche polynomials) | HIGH | PARTIAL (small n) | MEDIUM (Markov design) | LOW | **YELLOW** |
| **P2** | MEDIUM (GL(n) reps) | VERY HIGH | LOW | WIDE (test vectors) | MEDIUM | **YELLOW** |
| **P1** | HIGH (Φ⁴₃ renormalization) | HIGH | LOW | MEDIUM (known techniques?) | HIGH | **RED** |
| **P7** | MEDIUM | HIGH | LOW | WIDE | HIGH | **RED** |
| **P8** | HIGH (Lagrangian smoothing) | HIGH | LOW | WIDE | HIGH | **RED** |
| **P5** | VERY HIGH (equivariant) | VERY HIGH | LOW | NARROW (definition work) | HIGH | **RED** |

**Budget allocation:**

Per-problem message budgets (from `firstproof.md`) are the **primary caps**. Triage class determines priority ordering and default aggressiveness:
- **GREEN** (P10, P04, P06): Full solve attempt. See `firstproof.md` for per-problem budgets.
- **YELLOW** (P09, P03, P02): Attempt after GREEN complete. Park aggressively.
- **RED** (P01, P07, P08, P05): Feasibility probe only (G0–G2). 30–80 messages max.

## 4B. Stop-loss rules

Hard caps that prevent burning budget on dead ends. Per-gate caps are **secondary safety rails** — the per-problem budget from `firstproof.md` is the primary cap.

| Gate | Cap | If exceeded |
|------|-----|-------------|
| **G0 (formalize)** | 10 messages | Park. Definitions unclear → fetch references first. |
| **G1 (background)** | 15 messages | If >3 unresolved EDs → block on Producer sourcing. |
| **G2 (route map)** | 15 messages | If no credible route → deploy Scout. If Scout fails → park. |
| **G3 (lemma DAG)** | 20 messages | If DAG incomplete after 20 → route is wrong. Return to G2. |
| **G4 (experiments)** | 15 messages | If counterexample found → switch to disprove mode. |
| **G5 (proof)** | 40 messages | If no complete draft → park with 🟡 or 📊 status. |
| **G6 (review)** | 20 messages (3 cycles max) | If fatal flaw persists → publish as 🟡 with flaw noted. |

**Stall detection**: If 10 consecutive messages produce no new lemma closure, no new experiment result, and no route change → automatic escalation to Scout or park.

## 4C. Multi-model convergence protocol

### Diverge phase (maximize idea diversity)
Deploy 3-5 scouts with **different** prompts per problem:
- Scout A: "What is the simplest counterexample to [claim]?"
- Scout B: "What is the one-line intuition for why [claim] should be true?"
- Scout C: "If you had to prove [claim] in one page, what strategy would you use?"
- Scout D: "What connections exist between [claim] and [adjacent domain]?"

Each scout produces: 2 candidate routes, 1 suspected failure mode, 5 external dependencies with confidence.

### Converge phase (single canonical artifact)
- **One owner proof document per problem** — the Implementer. No multi-author chaos.
- Reviewer runs a **fault checklist** (not debate):
  - Undefined symbols?
  - Quantifier slips?
  - Uncited named results?
  - Hidden regularity assumptions?
  - Boundary cases / degeneracies?
  - Does the proof actually use the hypotheses?
- If Reviewer and Scout disagree: require a **concrete falsifier** (counterexample, missing hypothesis, explicit lemma gap). Abstract "I'm not convinced" is not actionable — must point to a specific step.
- **No debate mode.** The "loud wrong answer wins" failure mode is well-documented. Disagreements resolved by evidence, not argument.

---

## 5. Per-problem implementation plans

---

# P10 — RKHS CP-ALS: Matrix-free PCG with preconditioner

## Success criteria

A complete answer consists of:
1. **Matrix-free matvec**: Algorithm to compute $y = A\,\text{vec}(W)$ where $A = (Z \otimes K)^T S S^T (Z \otimes K) + \lambda(I_r \otimes K)$ without forming any $O(N)$ object
2. **Preconditioner**: At least one SPD preconditioner with efficient apply, with justification
3. **Complexity analysis**: All operations expressed in $O(\cdot)$ with parameters $n, r, q, M, N, d$, with $n, r < q \ll N$
4. **PCG algorithm**: Complete pseudocode for the iterative solve

The answer is an **explanation**, not a proof of a theorem. Quality is judged on correctness, clarity, and avoiding $O(N)$ costs.

## Subproblem decomposition

### SP10.1: Unpack the linear system
**Task**: Write $A\,\text{vec}(W) = b$ explicitly, identifying all dimensions.
- $W \in \mathbb{R}^{n \times r}$, so $\text{vec}(W) \in \mathbb{R}^{nr}$
- $Z \in \mathbb{R}^{M \times r}$ (Khatri-Rao product of all other factor matrices)
- $K \in \mathbb{R}^{n \times n}$ (RKHS kernel matrix, SPD)
- $S \in \mathbb{R}^{N \times q}$ (selection matrix, $q$ columns of $I_N$)
- $B = TZ \in \mathbb{R}^{n \times r}$ (MTTKRP)
- LHS matrix: $(Z \otimes K)^T S S^T (Z \otimes K) + \lambda(I_r \otimes K)$, size $nr \times nr$
- RHS: $(I_r \otimes K)\text{vec}(B)$, size $nr$

**Key identity**: $\text{vec}(KWD) = (D^T \otimes K)\text{vec}(W)$ for any matrices of compatible size.

**Status**: Straightforward linear algebra. LLM should handle.

### SP10.2: Derive the matrix-free matvec
**Task**: Given $\text{vec}(W)$, compute $(Z \otimes K)^T S S^T (Z \otimes K)\text{vec}(W)$ without forming $N \times N$ or $N \times q$ matrices.

**Decomposition of the matvec into steps**:
1. Reshape $\text{vec}(W) \to W \in \mathbb{R}^{n \times r}$
2. Compute $\hat{W} = KW \in \mathbb{R}^{n \times r}$ — cost $O(n^2 r)$
3. Form the Khatri-Rao product applied columnwise: $\text{vec}(\hat{W} \cdot Z^T)$... **NO**, this gives an $n \times M$ matrix which has $nM$ entries, potentially $O(N)$.

**The critical insight**: $(Z \otimes K)\text{vec}(W) = \text{vec}(KWZ^T)$ where $KWZ^T$ is $n \times M$. Forming this is $O(nM)$ which could be $O(N/n \cdot n) = O(N)$. **This is the trap.**

**Resolution**: The selection matrix $S$ selects $q \ll N$ entries. So:
1. Compute $\text{vec}(V) = (Z \otimes K)\text{vec}(W)$ — but DON'T form the full $nM$-vector
2. Instead: $S^T \text{vec}(V)$ selects $q$ entries from the mode-$k$ unfolding
3. Key: Each selected entry $(i, j)$ corresponds to specific row $i$ of $K$ and row $j$ of $Z$
4. So $[S^T(Z \otimes K)\text{vec}(W)]_\ell = (K_{i_\ell,:} W)(Z_{j_\ell,:})^T$ for the $\ell$-th observed entry at position $(i_\ell, j_\ell)$

**The efficient matvec**:
1. $\hat{W} = KW$ — $O(n^2 r)$
2. For each observed entry $\ell = 1, \ldots, q$: compute $v_\ell = \hat{W}_{i_\ell,:} \cdot Z_{j_\ell,:}^T$ — $O(r)$ per entry, $O(qr)$ total
3. Multiply $S \cdot v$ where $v \in \mathbb{R}^q$ — this scatters back to $\mathbb{R}^N$ but we only need $(Z \otimes K)^T$ applied to it
4. $(Z \otimes K)^T S v$: for each observed entry $\ell$, accumulate $v_\ell \cdot (Z_{j_\ell,:} \otimes K_{i_\ell,:})$ into $\text{vec}(W')$ — which means $W'_{:,p} \mathrel{+}= v_\ell \cdot Z_{j_\ell, p} \cdot K_{:, i_\ell}$ for each $p$
5. Actually: reshape as $W' \in \mathbb{R}^{n \times r}$ where $W'$ accumulates contributions

**Total matvec cost**: $O(n^2 r + qr + qnr)$ — but $qnr$ might be too much. Need to check if the scatter step can be done in $O(qr + n^2r)$.

**Fine detail**: The scatter step computes $W'_{:,p} = K^T \sum_{\ell: j_\ell \text{ maps to column}} v_\ell \cdot Z_{j_\ell,p} \cdot e_{i_\ell}$. Group by row index $i$: for each row $i$, sum $v_\ell Z_{j_\ell,p}$ over entries with that row, giving an intermediate $n \times r$ matrix, then multiply by $K$. Total: $O(qr + n^2 r)$.

**Regularization term**: $\lambda(I_r \otimes K)\text{vec}(W) = \lambda \text{vec}(KW)$ — cost $O(n^2 r)$.

**Total matvec**: $O(n^2 r + qr)$.

### SP10.3: Preconditioner selection
**Task**: Find an SPD matrix $P$ that approximates $A$ and is cheap to apply $P^{-1}$.

**Candidate 1: Block diagonal** — Use $\lambda(I_r \otimes K)$ as preconditioner.
- Apply cost: $O(n^2 r)$ (solve $r$ systems with $K$, or use Cholesky of $K$ precomputed in $O(n^3)$)
- Good when $\lambda$ dominates (strong regularization)
- SPD since $K$ is SPD

**Candidate 2: Diagonal + regularization** — Use diagonal of $A$ plus $\lambda(I_r \otimes K)$
- Requires computing diagonal of $(Z \otimes K)^T SS^T(Z \otimes K)$: for each diagonal entry $(i,p)$, sum $K_{i,i} Z_{j_\ell,p}^2$ over observed entries $\ell$ with row $i$. Cost $O(qr)$.
- Apply: $O(nr)$
- SPD by construction

**Candidate 3: Gram-based** — Use $(Z^T Z) \otimes K + \lambda(I_r \otimes K) = ((Z^T Z + \lambda I_r) \otimes K)$
- This ignores the selection/masking $SS^T$ but captures the Khatri-Rao structure
- Apply: Cholesky of $(Z^T Z + \lambda I_r)$ in $O(r^3)$, then $r$ solves with $K$ in $O(n^2 r)$
- Total apply: $O(n^2 r + r^3)$
- SPD: yes (Kronecker product of SPD matrices)

### SP10.4: PCG pseudocode and convergence
**Task**: Standard PCG with the above matvec and preconditioner.
- Initialization: $r_0 = b - A\text{vec}(W_0)$, $z_0 = P^{-1}r_0$, $p_0 = z_0$
- Iterate: $\alpha_k, W_{k+1}, r_{k+1}, z_{k+1}, p_{k+1}$ per standard PCG
- Convergence depends on condition number of $P^{-1}A$

### SP10.5: RHS computation
**Task**: Compute $b = (I_r \otimes K)\text{vec}(B) = \text{vec}(KB)$.
- $B = TZ$ (MTTKRP): depends on tensor format, but given as precomputed. Cost $O(n^2 r)$ for $KB$.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Kronecker/vec identity errors | HIGH | Verify every identity on 2×2 example |
| Missing that naive approach is $O(N)$ | HIGH | Explicit dimension tracking at every step |
| Confusing $S$ semantics (rows vs columns) | MEDIUM | Force explicit index-set notation |
| Preconditioner not SPD | MEDIUM | Require SPD proof for each candidate |
| Forgetting the regularization term | LOW | Checklist |

## External dependencies

- **Kronecker product identities**: $(A \otimes B)(C \otimes D) = AC \otimes BD$; $\text{vec}(AXB^T) = (B \otimes A)\text{vec}(X)$. Standard linear algebra — agent should prove inline.
- **PCG convergence theory**: Golub & Van Loan or Trefethen & Bau. Producer should have available but agent likely knows this.
- **CP-ALS with missing data**: Kolda & Bader, "Tensor Decompositions and Applications," SIAM Review 2009. The specific RKHS extension: arXiv:2408.05677 (Kileel, Ward, et al.).

## Verification plan

1. **Dimension check**: Every matrix/vector operation has compatible dimensions (automated)
2. **Toy example**: Set $n=3, r=2, q=5, M=10$. Form $A$ explicitly. Verify matvec matches $A \cdot \text{vec}(W)$ entry-by-entry.
3. **Complexity audit**: Count FLOPs for each step; confirm no $O(N)$ or $O(M)$ terms (since $M = N/n$)
4. **SPD check**: For each preconditioner, verify positive definiteness argument

## Agent task sequence

```
I: G0 — Write formal problem restatement with all dimensions explicit
R: Verify dimensions and notation consistency
I: G1 — List Kronecker identities needed; prove each on 2×2
R: Check each identity
I: G2 — Propose 2 matvec strategies: (A) entry-wise via observed indices, (B) block-sparse approach
R: Select based on complexity; reject any with O(N)
I: G3 — Lemma DAG: matvec lemma, preconditioner SPD lemma, complexity lemma, RHS lemma
R: Verify DAG completeness
I: G4 — Python verification script on toy dimensions
R: Check script output matches explicit computation
I: G5 — Full writeup: algorithm, pseudocode, complexity, preconditioner analysis
R: Line-by-line complexity audit
I: G7 — Package
```

---

# P6 — Existence of large ε-light subset

## Success criteria

Either:
- **YES + proof**: Prove there exists $c > 0$ such that for every graph $G = (V, E)$ and every $\epsilon \in (0, 1)$, $V$ contains an $\epsilon$-light subset $S$ with $|S| \geq c\epsilon|V|$
- **NO + counterexample family**: Construct a family of graphs where no such $c$ exists

An $\epsilon$-light set $S$ satisfies $\epsilon L - L_S \succeq 0$ where $L$ is the Laplacian of $G$ and $L_S$ is the Laplacian of $G_S = (V, E(S,S))$ (the graph with same vertex set but only edges between vertices in $S$).

## Key mathematical translation

**What does $\epsilon L - L_S \succeq 0$ mean?**

For any vector $x \in \mathbb{R}^V$:
$$\epsilon \sum_{\{u,v\} \in E} (x_u - x_v)^2 \geq \sum_{\{u,v\} \in E(S,S)} (x_u - x_v)^2$$

So $S$ is $\epsilon$-light if the edges within $S$ contribute at most $\epsilon$ fraction of the total Laplacian energy **for every test vector simultaneously**. This is much stronger than just having $|E(S,S)| \leq \epsilon |E|$.

## Subproblem decomposition

### SP6.1: Reformulate the PSD condition
**Task**: Express $\epsilon L - L_S \succeq 0$ in terms of edge sets and eigenvalues.

Note: $L = \sum_{e \in E} L_e$ where $L_e$ is the Laplacian of edge $e$ (rank-1 PSD matrix). Similarly $L_S = \sum_{e \in E(S,S)} L_e$.

So: $\epsilon L - L_S = \epsilon \sum_{e \in E} L_e - \sum_{e \in E(S,S)} L_e = \sum_{e \in E(S,S)} (\epsilon - 1) L_e + \epsilon \sum_{e \in E \setminus E(S,S)} L_e$.

Since $\epsilon < 1$, edges inside $S$ contribute negatively (with coefficient $\epsilon - 1 < 0$) and edges not inside $S$ contribute positively (with coefficient $\epsilon > 0$). For PSD, the positive contributions must dominate.

**Alternative formulation**: $\epsilon L - L_S \succeq 0$ iff $L_S \preceq \epsilon L$ iff the quadratic form of $L_S$ is dominated by $\epsilon$ times the quadratic form of $L$.

### SP6.2: Try random sampling
**Task**: Select each vertex independently with probability $p$. Let $S$ be the selected set. Show $\mathbb{E}[L_S] \preceq \epsilon L$ and concentrate.

If each vertex is selected independently with probability $p$, an edge $\{u,v\}$ is in $E(S,S)$ iff both $u, v \in S$, with probability $p^2$.

$\mathbb{E}[L_S] = p^2 L$. For this to satisfy $p^2 L \preceq \epsilon L$, need $p^2 \leq \epsilon$, so $p \leq \sqrt{\epsilon}$.

Expected size: $|S| = p|V| = \sqrt{\epsilon}|V|$. But we need $c\epsilon|V|$, and $\sqrt{\epsilon} \gg \epsilon$ for small $\epsilon$. So random sampling **gives a better bound than needed** in expectation!

**But**: We need concentration, not just expectation. The matrix $L_S$ is a random matrix, and we need $L_S \preceq \epsilon L$ with high probability, not just in expectation.

### SP6.3: Matrix concentration for dependent random matrices
**Task**: If $S$ is a random set of vertices, bound $\|L^{-1/2} L_S L^{-1/2}\|$ (or the appropriate restricted operator).

**Key complication**: The edge indicators $\mathbf{1}[\{u,v\} \in E(S,S)]$ are **not independent** — they share vertices. Standard matrix Chernoff (Tropp) requires independence.

**Possible approaches**:
- **Matrix Chernoff with bounded dependence**: If the dependency graph has bounded chromatic number, adapt.
- **Matrix Freedman inequality**: For martingale-based arguments.
- **Vertex-by-vertex peeling**: Add vertices to $S$ one at a time; track the spectral condition.
- **Pessimistic estimator / derandomization**: Use the method of conditional expectations with a matrix-valued potential.

### SP6.4: What bound on $|S|$ can we achieve?
**Task**: Determine the optimal relationship between $|S|$ and $\epsilon$.

With $p = \sqrt{\epsilon}$ we get $|S| \approx \sqrt{\epsilon}|V|$, which is $\gg c\epsilon|V|$. Even $p = c\epsilon$ for some constant $c$ gives $\mathbb{E}[L_S] = c^2\epsilon^2 L \preceq \epsilon L$ for $c \leq 1/\sqrt{\epsilon}$... wait, that's not a constant.

Let me reconsider. With $p = c\epsilon$, $\mathbb{E}[L_S] = c^2\epsilon^2 L$. Need $c^2\epsilon^2 \leq \epsilon$, so $c^2\epsilon \leq 1$, meaning $c \leq 1/\sqrt{\epsilon}$. For small $\epsilon$, this allows $c$ to be large, so $|S| = c\epsilon|V|$ with $c$ up to $1/\sqrt{\epsilon}$ gives $|S|$ up to $\sqrt{\epsilon}|V|$.

Actually the question asks: does there exist a **universal constant** $c > 0$ such that for every graph and every $\epsilon$, there's an $\epsilon$-light $S$ with $|S| \geq c\epsilon|V|$?

So we need $|S| \geq c\epsilon|V|$ for a constant $c$ independent of $\epsilon$ and $G$.

Take $p = c\epsilon$ for some constant $c$. Then $\mathbb{E}[L_S] = p^2 L = c^2 \epsilon^2 L$. For $\epsilon \leq 1$, we have $c^2\epsilon^2 \leq c^2\epsilon \leq \epsilon$ if $c \leq 1$. So the expectation bound works!

**Key question**: Can we concentrate? $\mathbb{E}[|S|] = c\epsilon|V|$, and we need $L_S \preceq \epsilon L$ not just in expectation but actually.

### SP6.5: Concentration argument
**Task**: Prove that random vertex sampling with $p = c\epsilon$ yields $L_S \preceq \epsilon L$ with positive probability.

**Approach via effective resistance**: The effective resistance $R_{\text{eff}}(e) = (L^{+})_{uu} + (L^{+})_{vv} - 2(L^{+})_{uv}$ for edge $e = \{u,v\}$ is the key quantity in spectral sparsification.

$L^{-1/2} L_e L^{-1/2}$ has operator norm equal to $R_{\text{eff}}(e) \cdot w_e$ for edge weight $w_e$.

For the matrix $L^{-1/2} L_S L^{-1/2} = \sum_{e \in E(S,S)} L^{-1/2} L_e L^{-1/2}$, each term has norm at most $R_{\text{eff}}(e)$ (for unweighted graphs).

**Matrix Bernstein / Chernoff** (Tropp): If the summands were independent...

But the edge indicators $\mathbf{1}[u \in S]\mathbf{1}[v \in S]$ have dependencies through shared vertices. The total effective resistance $\sum_e R_{\text{eff}}(e) = n - 1$ (number of vertices minus one, for connected graphs).

### SP6.6: Alternative approach — greedy / deterministic
**Task**: Instead of random sampling, build $S$ greedily.
- Add vertices one by one
- At each step, check if adding vertex $v$ maintains $L_S \preceq \epsilon L$
- Use a potential function (e.g., $\text{tr}[(\epsilon L - L_S)^{-1}]$ or a log-determinant barrier)

This mirrors the Batson-Spielman-Srivastava barrier method.

### SP6.7: Connection to spectral sparsification literature
**Key insight**: This problem is essentially **dual to spectral sparsification**. In sparsification, you select edges to approximate $L$. Here, you select vertices, and the induced edges must be spectrally dominated by $\epsilon L$.

The closest results:
- **Spielman-Srivastava** (2011): Edge sampling by effective resistance gives spectral sparsification
- **Batson-Spielman-Srivastava** (2012): Deterministic spectral sparsification via barrier method
- **Lee-Sun** (2018): Constructive spectral sparsification via random walks

The vertex selection version is less studied. Spielman (the problem's author) likely knows the spectral sparsification literature intimately and designed this as a variant that requires new ideas.

## Fine details that determine correctness

1. **Laplacian of $G_S$**: $G_S = (V, E(S,S))$ has the SAME vertex set $V$ but only edges between vertices in $S$. So $L_S$ is an $|V| \times |V|$ matrix (not $|S| \times |S|$). Vertices not in $S$ are isolated in $G_S$.
2. **PSD ordering**: $\epsilon L - L_S \succeq 0$ means for ALL vectors $x$, not just those supported on $S$.
3. **Connected components**: If $G$ is disconnected, $L$ has nullity > 1. The PSD condition still makes sense (both sides have the same null space containing the all-ones vector).
4. **The constant $c$**: Must be universal — independent of $|V|$, $|E|$, and $\epsilon$.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Confusing $L_S$ (same vertex set, induced edges) with principal submatrix | CRITICAL | Force explicit definition check at G0 |
| Ignoring dependency structure in random sampling | HIGH | Require explicit handling of vertex correlations |
| Misapplying matrix Chernoff without checking independence | HIGH | Demand exact hypotheses of any concentration inequality |
| Missing that $\sqrt{\epsilon} \gg c\epsilon$ so random sampling may be overkill | MEDIUM | Note this explicitly in route map |
| Hallucinating spectral sparsification results | HIGH | Require exact citation for any named result |

## External dependencies

- **Matrix Chernoff bound** (Tropp, 2012): "User-Friendly Tail Bounds for Sums of Random Matrices." *Foundations of Computational Mathematics*. Exact statement of Theorem 1.1.
- **Effective resistance identity**: $\sum_e R_{\text{eff}}(e) = n - 1$ for connected unweighted graphs. Standard — appears in Spielman's lecture notes.
- **Batson-Spielman-Srivastava barrier method**: "Twice-Ramanujan Sparsifiers." *SIAM Journal on Computing*, 2012. The potential function / barrier approach.
- **Matrix Bernstein inequality**: For bounded summands with dependencies.

**Producer action**: Source Tropp 2012 (exact theorem statement with conditions) and BSS 2012 (barrier method details).

## Verification plan

1. **Complete graph $K_n$**: $L = nI - J$. Choose $S$ of size $k$. Compute $L_S$ explicitly. Check when $\epsilon L - L_S \succeq 0$.
2. **Star graph $S_n$**: Hub + $n-1$ leaves. Interesting because $L$ has very different eigenvalue structure.
3. **Cycle $C_n$**: Check for $S$ being every other vertex.
4. **Random $d$-regular graphs**: Numerical experiments for $n = 50, 100$ with various $\epsilon$.
5. **Expander graphs**: Where spectral gap is large.

## Agent task sequence

```
I: G0 — Formalize: restate PSD condition as quadratic form bound. Verify L_S definition.
R: Confirm L_S is Laplacian of (V, E(S,S)) not principal submatrix.
I: G1 — List: spectral sparsification results, matrix concentration, effective resistance.
   Source request to H (LOGISTICS): fetch Tropp 2012 PDF, BSS 2012 PDF. Provide verbatim theorem statements.
I: G2 — Route map:
   (A) Random vertex sampling with p = cε, concentration via adapted matrix Chernoff
   (B) Deterministic greedy via barrier/potential function
   (C) Counterexample search on extreme graphs
I: G4 — Run experiments EARLY: test random sampling on K_n, star, cycle, expander
   Compute smallest eigenvalue of εL - L_S for random S of various sizes
R: Evaluate experiment results; determine if approach (A) or (B) is more promising
I: G3 — Lemma DAG based on selected route
I: G5 — Full proof
R: G6 — Adversarial review: try to find graph where the bound fails
I: G7 — Package
```

**Scout deployment**: Send to DeepSeek-R1 with prompt: "Find a family of graphs where no subset $S$ with $|S| \geq c\epsilon|V|$ satisfies $\epsilon L - L_S \succeq 0$. Try expanders, complete bipartite graphs, and stars."

---

# P4 — Inequality for Φₙ under ⊞ₙ convolution

## Success criteria

Either:
- **YES + proof**: Prove that for all monic real-rooted degree-$n$ polynomials $p, q$:
$$\frac{1}{\Phi_n(p \boxplus_n q)} \geq \frac{1}{\Phi_n(p)} + \frac{1}{\Phi_n(q)}$$
- **NO + counterexample**: Specific $p, q$ (with roots) where the inequality fails.

Where:
- $(p \boxplus_n q)(x) = \sum_{k=0}^n c_k x^{n-k}$ with $c_k = \sum_{i+j=k} \frac{(n-i)!(n-j)!}{n!(n-k)!} a_i b_j$
- $\Phi_n(p) = \sum_{i \leq n} \left(\sum_{j \neq i} \frac{1}{\lambda_i - \lambda_j}\right)^2$ where $\lambda_1, \ldots, \lambda_n$ are roots of $p$

## Key mathematical insights

### What is $\Phi_n$?
$\Phi_n(p) = \sum_i \left(\frac{p'(\lambda_i)}{p''(\lambda_i)} \cdot \text{[something]}\right)^2$... actually let's compute directly.

If $p(x) = \prod_i (x - \lambda_i)$, then $p'(\lambda_i) = \prod_{j \neq i}(\lambda_i - \lambda_j)$.

The quantity $\sum_{j \neq i} \frac{1}{\lambda_i - \lambda_j} = \frac{p''(\lambda_i)}{2p'(\lambda_i)}$ (by logarithmic differentiation).

So $\Phi_n(p) = \sum_i \left(\frac{p''(\lambda_i)}{2p'(\lambda_i)}\right)^2$.

This is the **sum of squares of the logarithmic second derivatives** at the roots. It measures "root repulsion strength" — how much the roots push each other apart.

**Connection**: $1/\Phi_n$ is an inverse measure of repulsion. The inequality says $1/\Phi_n$ is **superadditive** under $\boxplus_n$. Equivalently, $\boxplus_n$ reduces root repulsion (or increases the spacing between roots).

### What is $\boxplus_n$?
This is the **finite free additive convolution** (Marcus-Spielman-Srivastava). For degree $n$ polynomials:
$(p \boxplus_n q)(x) = \mathbb{E}[\det(xI - (A + UBU^*))]$
where $A, B$ have characteristic polynomials $p, q$ and $U$ is Haar-random unitary.

**Key properties**:
- $\boxplus_n$ preserves real-rootedness (MSS 2015)
- In the $n \to \infty$ limit, $\boxplus_n \to \boxplus$ (Voiculescu's free convolution)
- The coefficient formula given matches the "finite R-transform" or "K-transform" approach

### Why the inequality should be true (heuristic)
Free convolution spreads out the roots (adds independent randomness). More spread → smaller $\Phi_n$ → larger $1/\Phi_n$. The superadditivity of $1/\Phi_n$ says the "spreading" from combining two polynomials is at least as much as the sum of their individual spreads.

This is analogous to: if $X, Y$ are free random variables, $\text{Var}(X + Y) \geq \text{Var}(X) + \text{Var}(Y)$ (which is actually equality for free independence). The $\Phi_n$ version is a "local" analogue.

## Subproblem decomposition

### SP4.1: Compute $\Phi_n$ for small cases
**Task**: Derive closed-form $\Phi_n$ for $n = 2, 3$.

For $n = 2$: $p(x) = (x - \lambda_1)(x - \lambda_2)$.
$\Phi_2(p) = \left(\frac{1}{\lambda_1 - \lambda_2}\right)^2 + \left(\frac{1}{\lambda_2 - \lambda_1}\right)^2 = \frac{2}{(\lambda_1 - \lambda_2)^2}$

So $1/\Phi_2(p) = (\lambda_1 - \lambda_2)^2 / 2$.

For $n = 2$, the inequality becomes:
$\frac{(\mu_1 - \mu_2)^2}{2} \geq \frac{(\lambda_1 - \lambda_2)^2}{2} + \frac{(\rho_1 - \rho_2)^2}{2}$

where $\mu_i$ are roots of $p \boxplus_2 q$.

### SP4.2: Compute $\boxplus_2$ explicitly
**Task**: For $n = 2$, $p(x) = x^2 + a_1 x + a_2$, $q(x) = x^2 + b_1 x + b_2$.

$c_0 = 1$, $c_1 = a_1 + b_1$ (using the formula with $k=1$: $\frac{1!1!}{2!1!}a_0 b_1 + \frac{1!1!}{2!1!}a_1 b_0 = \frac{1}{2}b_1 + \frac{1}{2}a_1$... wait, let me recompute.

$c_k = \sum_{i+j=k} \frac{(n-i)!(n-j)!}{n!(n-k)!} a_i b_j$

For $n = 2, k = 1$: $c_1 = \frac{2! \cdot 1!}{2! \cdot 1!} a_0 b_1 + \frac{1! \cdot 2!}{2! \cdot 1!} a_1 b_0 = b_1 + a_1$.

For $n = 2, k = 2$: $c_2 = \frac{2! \cdot 0!}{2! \cdot 0!} a_0 b_2 + \frac{1! \cdot 1!}{2! \cdot 0!} a_1 b_1 + \frac{0! \cdot 2!}{2! \cdot 0!} a_2 b_0 = b_2 + \frac{1}{2}a_1 b_1 + a_2$.

So $(p \boxplus_2 q)(x) = x^2 + (a_1 + b_1)x + (a_2 + b_2 + \frac{1}{2}a_1 b_1)$.

Roots of $p$: $\lambda_{1,2} = \frac{-a_1 \pm \sqrt{a_1^2 - 4a_2}}{2}$, so $(\lambda_1 - \lambda_2)^2 = a_1^2 - 4a_2$.

Roots of $p \boxplus_2 q$: $(\mu_1 - \mu_2)^2 = (a_1 + b_1)^2 - 4(a_2 + b_2 + \frac{1}{2}a_1 b_1) = a_1^2 + 2a_1 b_1 + b_1^2 - 4a_2 - 4b_2 - 2a_1 b_1 = (a_1^2 - 4a_2) + (b_1^2 - 4b_2)$.

So $(\mu_1 - \mu_2)^2 = (\lambda_1 - \lambda_2)^2 + (\rho_1 - \rho_2)^2$. **Equality holds for $n = 2$!**

This means $1/\Phi_2(p \boxplus_2 q) = 1/\Phi_2(p) + 1/\Phi_2(q)$ exactly.

### SP4.3: Check $n = 3$ numerically
**Task**: Sample random real-rooted cubics, compute $\boxplus_3$, verify inequality.

Need: Python script that:
1. Generates random real-rooted monic cubics (sample 3 roots, form polynomial)
2. Computes $\boxplus_3$ via the coefficient formula
3. Finds roots of the result (numpy.roots)
4. Computes $\Phi_3$ for input and output
5. Checks inequality

### SP4.4: Prove the inequality for general $n$
**Candidate methods**:

**Method A: Connection to variance/energy**
If $\Phi_n$ relates to a trace of some operator, and $\boxplus_n$ preserves some algebraic structure, then maybe the inequality follows from a Cauchy-Schwarz or convexity argument.

**Method B: Differential operator / K-transform approach**
MSS define finite free convolution via the "K-transform": $K_p(z) = z - n \cdot \frac{p(z)}{p'(z)}$. Under $\boxplus_n$: $K_{p \boxplus_n q}(z) = K_p(z) + K_q(z) - z$.

Can $\Phi_n$ be expressed in terms of $K_p$? Since $\Phi_n$ involves $p''/p'$ at roots, and $K_p$ involves $p/p'$...

**Method C: Cauchy transform / Stieltjes transform**
The Cauchy transform $G_p(z) = \frac{1}{n}\sum_i \frac{1}{z - \lambda_i}$. Note $G_p'(z) = -\frac{1}{n}\sum_i \frac{1}{(z - \lambda_i)^2}$.

$\Phi_n(p) = \sum_i (G_p'(\lambda_i) \cdot n)^2$... not quite, need to be more careful since $G_p$ has poles at $\lambda_i$.

**Method D: Interlacing / barrier approach**
If $p \boxplus_n q$ has roots that interlace or separate from those of $p$ and $q$ in a controlled way, the inequality might follow from root separation estimates.

### SP4.5: Express $\Phi_n$ in terms of coefficients (not just roots)
**Task**: Write $\Phi_n(p)$ as a rational function of the coefficients $a_0, \ldots, a_n$.

$\Phi_n(p) = \sum_i (p''(\lambda_i)/(2p'(\lambda_i)))^2$.

Using the identity: $\sum_i \frac{f(\lambda_i)}{p'(\lambda_i)} = \text{[coefficient extraction from } f/p \text{]}$ (partial fractions), we can write:

$\sum_i \frac{(p''(\lambda_i))^2}{(p'(\lambda_i))^2} = \sum_i \frac{(p''(\lambda_i))^2}{(p'(\lambda_i))^2}$

This is harder to simplify. May need the resultant or subresultant of $p'$ and $p''$.

### SP4.6: Prove $n = 2$ case as template
Already done in SP4.2: equality holds. This gives the base case and suggests the inequality might be tight.

## Fine details that determine correctness

1. **Multiple roots**: $\Phi_n(p) = \infty$ if $p$ has a multiple root. The inequality trivially holds if either input has a multiple root ($1/\infty = 0$). But does $\boxplus_n$ preserve simplicity of roots?
2. **Real-rootedness of $\boxplus_n$**: MSS proved $\boxplus_n$ preserves real-rootedness. Must be cited, not assumed.
3. **Sign of $\Phi_n$**: Always non-negative (sum of squares). Actually always positive for simple roots.
4. **Convention**: The inequality is about $1/\Phi_n$, not $\Phi_n$. Superadditivity of $1/\Phi_n$ = subadditivity of $\Phi_n$... no, it's the harmonic-mean-type inequality.
5. **Coefficient formula**: Double-check the formula $c_k = \sum_{i+j=k} \frac{(n-i)!(n-j)!}{n!(n-k)!} a_i b_j$. Verify it matches the MSS definition.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Symbolic manipulation errors in coefficient formulas | HIGH | Verify all formulas on $n = 2$ case where answer is known |
| Assuming $\boxplus_n$ preserves real-rootedness without proof | HIGH | Require explicit citation of MSS result |
| Root-finding instability for numerical checks | MEDIUM | Use high-precision arithmetic (mpmath), perturbation analysis |
| Flipping inequality direction | MEDIUM | Verify with $n = 2$ closed form |
| Missing multiple-root edge case | LOW | Note $\Phi_n = \infty$ convention makes inequality trivial for multiple roots |

## External dependencies

- **MSS (2015)**: "Interlacing Families I: Bipartite Ramanujan Graphs of All Degrees." *Annals of Mathematics*. Theorem establishing real-rootedness of $\boxplus_n$.
- **MSS (2015)**: "Interlacing Families II: Mixed Characteristic Polynomials and the Kadison-Singer Problem." Finite free convolution properties.
- **K-transform**: Exact definition and additive property. Check Marcus's survey or arXiv:1507.05506.
- **Srivastava** (the problem author): Recent papers on polynomial convolutions may contain relevant machinery.

**Producer action**: Source MSS papers for exact $\boxplus_n$ definition, K-transform properties, and real-rootedness theorem.

## Verification plan

1. **$n = 2$**: Closed-form verification (already done: equality holds)
2. **$n = 3$**: Numerical experiments with 10,000+ random real-rooted cubics
3. **$n = 4, 5, 6$**: Numerical experiments with decreasing sample sizes
4. **Edge cases**: Polynomials with roots very close together (near-multiple roots)
5. **Structured cases**: $p = q$ (self-convolution), $p = (x-a)^n$ approaches

## Agent task sequence

```
I: G0 — Formalize: rewrite Φₙ in terms of roots and in terms of p'/p''.
   Verify coefficient formula on n = 2.
R: Confirm formula matches MSS definition.
I: G4 — EARLY EXPERIMENTS: Python script for n = 2,3,4,5,6.
   Generate random real-rooted polynomials, compute both sides, check inequality.
   Report: does equality hold for n = 2? Does inequality hold for all tested cases?
R: Verify numerical methodology (precision, root-finding stability).
I: G1 — Background: K-transform, finite free convolution properties.
   Source request: MSS papers.
I: G2 — Route map:
   (A) Express Φₙ via K-transform, prove superadditivity from K-transform additivity
   (B) Direct algebraic proof via coefficient formula + root-coefficient relations
   (C) Barrier/convexity argument on root configurations
R: Select route based on n = 2 template and experiment patterns.
I: G3 — Lemma DAG
Scout: Send to DeepSeek-R1: "Is 1/Φₙ concave/superadditive on real-rooted polynomials
   under finite free convolution? What's the connection to free probability?"
I: G5 — Full proof
R: G6 — Adversarial: try polynomials with extreme root configurations
I: G7 — Package
```

---

# P9 — Polynomial map F characterizing rank-1 tensor scalings

## Success criteria

Either:
- **YES + construction**: Construct a polynomial map $F: \mathbb{R}^{81n^4} \to \mathbb{R}^N$ satisfying all three properties (independent of $A^{(i)}$, degrees independent of $n$, characterizes rank-1 scalings)
- **NO + obstruction**: Prove no such $F$ exists (e.g., degree must grow with $n$)

## Key mathematical translation

### Setup
Given $n \geq 5$ Zariski-generic matrices $A^{(1)}, \ldots, A^{(n)} \in \mathbb{R}^{3 \times 4}$, form tensors:
$$Q^{(\alpha\beta\gamma\delta)}_{ijkl} = \det\begin{pmatrix} A^{(\alpha)}_{i,:} \\ A^{(\beta)}_{j,:} \\ A^{(\gamma)}_{k,:} \\ A^{(\delta)}_{l,:} \end{pmatrix}$$

So $Q^{(\alpha\beta\gamma\delta)}$ is a $3 \times 3 \times 3 \times 3$ tensor (81 entries) for each 4-tuple $(\alpha,\beta,\gamma,\delta)$.

There are $n^4$ such tensors (with repetitions from index permutations), giving the input space $\mathbb{R}^{81n^4}$.

### The scaling condition
Given $\lambda \in \mathbb{R}^{n \times n \times n \times n}$ with $\lambda_{\alpha\beta\gamma\delta} \neq 0$ when $\alpha, \beta, \gamma, \delta$ are not all identical, we form:
$$\lambda_{\alpha\beta\gamma\delta} Q^{(\alpha\beta\gamma\delta)} \in \mathbb{R}^{81n^4}$$

$F$ should vanish on this collection iff $\lambda_{\alpha\beta\gamma\delta} = u_\alpha v_\beta w_\gamma x_\delta$ for some $(u, v, w, x) \in (\mathbb{R}^*)^n \times (\mathbb{R}^*)^n \times (\mathbb{R}^*)^n \times (\mathbb{R}^*)^n$.

### What this means
The rank-1 condition on $\lambda$ means $\lambda$ is a rank-1 tensor in $\mathbb{R}^{n \times n \times n \times n}$. So $F$ should test whether scaling the $Q$ tensors by $\lambda$ is equivalent to scaling each index independently.

## Subproblem decomposition

### SP9.1: Understand the group action
**Task**: The scaling group $(\mathbb{R}^*)^{4n}$ acts on the collection $\{Q^{(\alpha\beta\gamma\delta)}\}$ by:
$(u, v, w, x) \cdot Q^{(\alpha\beta\gamma\delta)} = u_\alpha v_\beta w_\gamma x_\delta \cdot Q^{(\alpha\beta\gamma\delta)}$

$F$ should detect the orbit of this action, i.e., $F(\lambda \cdot Q) = 0$ iff $\lambda$ is in the orbit of the trivial scaling.

This is a **membership test for a torus orbit** in a polynomial way.

### SP9.2: Find polynomial invariants for the torus action
**Task**: Identify polynomial functions of the scaled tensors $\{\lambda_{\alpha\beta\gamma\delta} Q^{(\alpha\beta\gamma\delta)}\}$ that vanish iff $\lambda$ is rank-1.

**Key observation**: For rank-1 $\lambda$, $\lambda_{\alpha\beta\gamma\delta} \cdot \lambda_{\alpha'\beta'\gamma'\delta'} = \lambda_{\alpha\beta'\gamma\delta'} \cdot \lambda_{\alpha'\beta\gamma'\delta}$ (and all such "swaps"). These are the $2 \times 2$ minors of the unfoldings of $\lambda$.

So candidate invariants: for any two 4-tuples $(\alpha\beta\gamma\delta)$ and $(\alpha'\beta'\gamma'\delta')$ and any "swap" of indices:
$$(\lambda_{\alpha\beta\gamma\delta} Q^{(\alpha\beta\gamma\delta)}) \otimes (\lambda_{\alpha'\beta'\gamma'\delta'} Q^{(\alpha'\beta'\gamma'\delta')}) - (\lambda_{\alpha\beta'\gamma\delta'} Q^{(\alpha\beta'\gamma\delta')}) \otimes (\lambda_{\alpha'\beta\gamma'\delta} Q^{(\alpha'\beta\gamma'\delta)}) = 0$$

But $F$ must be a function of the SCALED tensors $\lambda \cdot Q$, not of $\lambda$ and $Q$ separately. So we need to extract $\lambda$ ratios from the scaled tensors.

### SP9.3: Extract scaling ratios from $Q$ tensors
**Task**: Given $\lambda_{\alpha\beta\gamma\delta} Q^{(\alpha\beta\gamma\delta)}$, can we recover $\lambda_{\alpha\beta\gamma\delta}$ (up to the rank-1 ambiguity)?

Since $A^{(i)}$ are generic, $Q^{(\alpha\beta\gamma\delta)}$ are generically nonzero (for distinct indices). We can form ratios:
$$\frac{[\lambda_{\alpha\beta\gamma\delta} Q^{(\alpha\beta\gamma\delta)}]_{ijkl}}{[\lambda_{\alpha'\beta'\gamma'\delta'} Q^{(\alpha'\beta'\gamma'\delta')}]_{i'j'k'l'}} = \frac{\lambda_{\alpha\beta\gamma\delta}}{\lambda_{\alpha'\beta'\gamma'\delta'}} \cdot \frac{Q^{(\alpha\beta\gamma\delta)}_{ijkl}}{Q^{(\alpha'\beta'\gamma'\delta')}_{i'j'k'l'}}$$

For generic $A$, the $Q$ values are known (they're determinants of known matrices). So the ratios $\lambda_{\alpha\beta\gamma\delta}/\lambda_{\alpha'\beta'\gamma'\delta'}$ are determined.

**But $F$ must not depend on $A$!** So we cannot use specific $Q$ values.

### SP9.4: Use the $Q$ tensors' algebraic structure
**Task**: Find polynomial relations among $\{Q^{(\alpha\beta\gamma\delta)}\}$ that are universal (hold for all generic $A$).

The $Q$ tensors satisfy Plücker-like relations: they are $4 \times 4$ minors of a $3n \times 4$ matrix (stacking all $A^{(i)}$). Wait — each $Q$ is a $4 \times 4$ determinant of 4 rows from different $A^{(i)}$'s, but also involves choosing which row (1, 2, or 3) from each $A^{(i)}$.

The degree-2 relations: for fixed $\alpha, \beta, \gamma, \delta, \epsilon$ (5 indices), there are linear relations among the 81-entry tensors $Q^{(\alpha\beta\gamma\delta)}$ — these come from the fact that 5 rows in $\mathbb{R}^4$ are linearly dependent.

### SP9.5: Construct $F$ from cross-ratios
**Task**: Form polynomial expressions in $\lambda \cdot Q$ that cancel the $A$-dependence.

Consider:
$$R(\alpha\beta\gamma\delta; \alpha'\beta'\gamma'\delta'; i,j,k,l; i',j',k',l') = (\lambda Q)^{(\alpha\beta\gamma\delta)}_{ijkl} \cdot (\lambda Q)^{(\alpha'\beta'\gamma'\delta')}_{i'j'k'l'} - (\lambda Q)^{(\alpha\beta'\gamma\delta')}_{ijkl} \cdot (\lambda Q)^{(\alpha'\beta\gamma'\delta)}_{i'j'k'l'}$$

Wait, this doesn't work because the tensor indices $(i,j,k,l)$ are for the 3×3×3×3 tensor, not the combinatorial indices $(\alpha, \beta, \gamma, \delta)$.

**Better approach**: Fix tensor positions $(i,j,k,l)$ and form ratios:
$$\frac{(\lambda Q)^{(\alpha\beta\gamma\delta)}_{ijkl}}{(\lambda Q)^{(\alpha'\beta'\gamma'\delta')}_{ijkl}} = \frac{\lambda_{\alpha\beta\gamma\delta}}{\lambda_{\alpha'\beta'\gamma'\delta'}} \cdot \frac{Q^{(\alpha\beta\gamma\delta)}_{ijkl}}{Q^{(\alpha'\beta'\gamma'\delta')}_{ijkl}}$$

For this to be independent of $A$, we need $Q^{(\alpha\beta\gamma\delta)}_{ijkl} / Q^{(\alpha'\beta'\gamma'\delta')}_{ijkl}$ to be an algebraic function of the other $Q$ entries — which requires algebraic relations among the $Q$'s.

### SP9.6: The fundamental question
Does there exist an $A$-independent polynomial test for rank-1-ness of $\lambda$, using only the scaled tensors $\lambda \cdot Q$?

**Positive argument sketch**: The 2×2 minors of the "unfoldings" of $\lambda$ can be tested using degree-2 polynomials in the scaled tensors, IF we can cancel the $Q$-factors. Since we have $81$ entries per tensor and $3$ rows per matrix, there should be enough "cross-ratio" type identities.

**Negative argument sketch**: The degrees of the coordinate functions of $F$ might necessarily grow with $n$ because the number of scaling parameters grows.

## Fine details that determine correctness

1. **"Does not depend on $A^{(i)}$"**: $F$ is a fixed polynomial map applied to the 81$n^4$-dimensional input. The SAME $F$ works for ALL generic $A$.
2. **"Degrees independent of $n$"**: Each coordinate of $F$ is a polynomial of degree $\leq D$ for some fixed $D$ (not depending on $n$). But the NUMBER $N$ of coordinates can depend on $n$.
3. **"Zariski generic"**: The characterization holds for $A$ outside a proper algebraic subset. Need to track where genericity is used.
4. **$\lambda_{\alpha\beta\gamma\delta} = 0$ when all indices equal**: This is a support condition, not a rank condition.
5. **"If and only if"**: Both directions must hold. The "only if" (rank-1 ⟹ $F = 0$) is usually easier; the "if" ($F = 0$ ⟹ rank-1) requires genericity.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Confusing "generic" with "for all" | CRITICAL | Force quantifier-normal-form rewrite |
| Degree bound arguments are subtle | HIGH | Require explicit degree tracking |
| Invariant theory is specialized | HIGH | Source references; don't trust agent's "known results" |
| Confusing the tensor index structure | HIGH | Force explicit notation: $(α,β,γ,δ)$ vs $(i,j,k,l)$ |
| Missing the support condition on $\lambda$ | MEDIUM | Note at G0 |

## External dependencies

- **Finite free resolution / syzygies**: For understanding polynomial relations among determinants.
- **GKZ hyperdeterminant**: For background on tensor invariants. Gelfand-Kapranov-Zelevinsky, *Discriminants, Resultants, and Multidimensional Determinants*.
- **Plücker relations**: For algebraic relations among minors.
- **Kileel's work**: The problem author likely has relevant papers on algebraic statistics and tensor decomposition. Check arXiv for recent Kileel papers.

**Producer action**: Source Kileel's recent papers on tensor algebra. Source GKZ book chapter on hyperdeterminants.

## Verification plan

1. **$n = 5$ (minimal case)**: Attempt explicit construction of $F$ for $n = 5$.
2. **Symbolic computation**: Use Macaulay2 or Singular to compute relations among $Q$ tensors.
3. **Numerical verification**: Generate random $A^{(i)}$, random rank-1 $\lambda$, verify $F = 0$. Generate non-rank-1 $\lambda$, verify $F \neq 0$.

## Agent task sequence

```
I: G0 — Formalize all dimensions, index ranges, and the three conditions on F.
R: Verify: F maps R^{81n^4} → R^N, N can depend on n, degrees cannot.
I: G1 — Background on Plücker relations, tensor invariants, torus orbit testing.
   Source request: Kileel papers, GKZ book.
I: G2 — Route map:
   (A) Construct F from cross-ratio / Plücker-type identities (degree ≤ 4?)
   (B) Prove impossibility via degree lower bound (representation-theoretic)
   (C) Reduce to known invariant-theory results
Scout: Send to Kimi 2.5: "For generic 3×4 matrices, what polynomial relations exist
   among 4×4 minors formed by selecting one row from each matrix?"
I: G4 — Symbolic experiments for n = 5 with CAS
I: G3-G5-G6-G7 per standard
```

---

# P3 — Markov chain on Sn(λ) with interpolation polynomial stationary distribution

## Success criteria

**Constructive**: Define a Markov chain on the state space $S_n(\lambda)$ such that:
1. The chain is **nontrivial** (transitions not described using $F^*_\mu$ polynomials)
2. The **stationary distribution** is proportional to $F^*_\mu(x_1, \ldots, x_n; q=1, t) / P^*_\lambda(x_1, \ldots, x_n; q=1, t)$ for $\mu \in S_n(\lambda)$
3. **Proof of stationarity** (via detailed balance, global balance, or intertwining)

Note: The question is "does there exist" — so the answer is YES + construction, or NO + impossibility argument.

## Key mathematical background

### What is $S_n(\lambda)$?
For a partition $\lambda = (\lambda_1 > \cdots > \lambda_n \geq 0)$ with distinct parts, restricted (unique part of size 0, no part of size 1):

$S_n(\lambda)$ is a set of compositions/permutations of $\lambda$. Most likely: $S_n(\lambda) = \{\mu = (\mu_1, \ldots, \mu_n) : \mu \text{ is a permutation of } \lambda\}$, i.e., the $S_n$-orbit of $\lambda$ as a composition.

**Critical**: This definition needs verification from the interpolation polynomial literature. The "$S_n(\lambda)$" notation may refer to the orbit of $\lambda$ under the symmetric group acting on parts.

### What are $F^*_\mu$ and $P^*_\lambda$?
- $P^*_\lambda(x; q, t)$: **Interpolation Macdonald polynomial** (Knop-Sahi). Defined by vanishing conditions: $P^*_\lambda(\mu; q, t) = 0$ for $\mu \neq \lambda$ in a specified set, with specific normalization.
- $F^*_\mu(x; q, t)$: **Interpolation ASEP polynomial**. Related to stationary measures of the asymmetric simple exclusion process via multiline queues (Corteel-Mandelshtam-Williams).

At $q = 1$: specialization simplifies significantly. Need to compute what happens.

### What does "nontrivial" mean?
Transition probabilities cannot be described using $F^*_\mu$. So you can't just define $P(\mu \to \nu) \propto F^*_\nu / \text{something}$. The chain must arise from combinatorial/structural moves on the state space.

## Subproblem decomposition

### SP3.1: Pin down definitions exactly
**Task**: From the literature, determine:
1. Exact definition of $S_n(\lambda)$ for restricted partitions with distinct parts
2. Exact formulas for $F^*_\mu(x; q=1, t)$ and $P^*_\lambda(x; q=1, t)$
3. What the ratio $F^*_\mu / P^*_\lambda$ simplifies to at $q=1$

**This is the most critical subproblem.** Without exact definitions, everything downstream is wrong.

**Source**: Lauren Williams's recent papers on ASEP and Macdonald polynomials. Corteel-Mandelshtam-Williams (arXiv:2209.09859 or similar). Knop's original paper on interpolation Macdonald polynomials.

### SP3.2: Compute the stationary distribution for small cases
**Task**: For $n = 3$, $\lambda = (3, 2, 0)$ (the smallest restricted partition with distinct parts and a unique 0):
- $S_3(\lambda) = \{(3,2,0), (3,0,2), (2,3,0), (2,0,3), (0,3,2), (0,2,3)\}$ — 6 states (all permutations)
- Compute $F^*_\mu / P^*_\lambda$ at $q = 1$ for each $\mu$
- This gives the target distribution on 6 states

### SP3.3: Design candidate Markov chains
**Task**: Propose transition rules based on combinatorial moves:

**Candidate A: Adjacent transpositions**
- From $\mu = (\mu_1, \ldots, \mu_n)$, swap $\mu_i$ and $\mu_{i+1}$ for some $i$ with probability depending on $\mu_i, \mu_{i+1}, t, x$.
- This is the standard approach for Markov chains on $S_n$-orbits.

**Candidate B: ASEP-like moves**
- Particles at positions $\lambda_1 > \cdots > \lambda_n \geq 0$, with labels $1, \ldots, n$.
- Each pair of adjacent labeled particles swaps with rate depending on positions and parameter $t$.

**Candidate C: Growth/projection chain**
- Project from an $n+1$-state chain to an $n$-state chain via an intertwining relation.

### SP3.4: Prove stationarity
**Task**: For the selected chain, prove the target distribution is stationary.

**Method 1: Detailed balance**
Show $\pi(\mu) P(\mu \to \nu) = \pi(\nu) P(\nu \to \mu)$ for all $\mu, \nu$.

**Method 2: Global balance**
Show $\sum_\nu \pi(\nu) P(\nu \to \mu) = \pi(\mu)$ for all $\mu$.

**Method 3: Intertwining**
Find a "link" kernel $\Lambda$ from a larger chain $\hat{X}$ to this chain $X$ such that $\Lambda \hat{P} = P \Lambda$ and the stationary distribution projects correctly.

### SP3.5: Verify the chain is nontrivial
**Task**: Confirm that the transition probabilities can be written without $F^*_\mu$.

## Fine details that determine correctness

1. **$q = 1$ specialization**: This is crucial and might simplify the polynomials dramatically. Interpolation Macdonald polynomials at $q = 1$ may reduce to interpolation Jack polynomials or simpler objects.
2. **Normalization**: The distribution is $\pi(\mu) \propto F^*_\mu / P^*_\lambda$. Must verify this is positive for all $\mu \in S_n(\lambda)$ and sums to something finite.
3. **"Restricted" partition**: Unique part of size 0, no part of size 1. Why these conditions? They may ensure certain non-degeneracy.
4. **The $x$ and $t$ parameters**: The distribution depends on $x_1, \ldots, x_n$ and $t$. The chain may also depend on these.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Definitions of $F^*_\mu$ and $P^*_\lambda$ are niche | CRITICAL | Must source from exact reference before proceeding |
| $q=1$ specialization effects unknown to models | HIGH | Compute explicitly for small cases |
| "Nontrivial" constraint hard to verify formally | MEDIUM | Require transitions to be described purely combinatorially |
| Stationarity proof requires exact identity | HIGH | Verify numerically on small cases first |

## External dependencies (CRITICAL)

- **Corteel-Mandelshtam-Williams**: ASEP polynomials definition. Check arXiv:2209.09859 and related.
- **Knop (1997)**: "Symmetric and non-symmetric quantum group analogs of the Macdonald polynomials." Interpolation Macdonald polynomial definition.
- **Sahi (1996)**: Interpolation Jack polynomials.
- **Williams's lecture notes or survey**: For the connection between ASEP and Macdonald polynomials.

**Producer action (LOGISTICS)**: This problem CANNOT proceed without exact definitions. Source the Corteel-Mandelshtam-Williams paper and the relevant Williams survey. Provide verbatim: definition of $S_n(\lambda)$, formula for $F^*_\mu$ at $q = 1$, formula for $P^*_\lambda$ at $q = 1$. Do NOT interpret or summarize — copy the definitions exactly as stated.

## Agent task sequence

```
H: SOURCE definitions before anything else. This is the blocking dependency.
I: G0 — Formalize state space and distribution using sourced definitions.
R: Verify definitions match the problem statement exactly.
I: SP3.2 — Compute distribution for n = 3, λ = (3,2,0).
R: Verify computation.
I: G2 — Propose 2-3 chain constructions (adjacent transpositions, ASEP-like, intertwining).
R: Check each for nontriviality constraint.
I: G4 — Implement chains in Python; verify stationarity numerically for n = 3.
I: G5 — Prove stationarity for selected chain.
R: G6 — Check proof; try to find state where detailed balance fails.
I: G7 — Package.
```

---

# P2 — Whittaker function with nonvanishing Rankin-Selberg integral

## Success criteria

**YES + existence proof**: Prove that for any generic irreducible admissible $\Pi$ of $GL_{n+1}(F)$, there exists $W \in \mathcal{W}(\Pi, \psi^{-1})$ such that for every generic irreducible admissible $\pi$ of $GL_n(F)$, there exists $V \in \mathcal{W}(\pi, \psi)$ such that the Rankin-Selberg integral is finite and nonzero for all $s \in \mathbb{C}$.

Or **NO + counterexample**: A specific $\Pi$ where no such $W$ exists.

## Key mathematical translation

The local Rankin-Selberg integral:
$$\Psi(s, W, V) = \int_{N_n \backslash GL_n(F)} W\left(\begin{pmatrix} g & \\ & 1 \end{pmatrix} u_Q\right) V(g) |\det g|^{s - 1/2} \, dg$$

where $u_Q = I_{n+1} + Q E_{n,n+1}$, $Q$ generates $\mathfrak{q}^{-1}$ (inverse of conductor of $\pi$).

**Note the quantifier structure**: $\exists W$ (independent of $\pi$!) such that $\forall \pi$, $\exists V$, the integral is finite and nonzero $\forall s$.

The $W$ must work uniformly across all $\pi$. This is the hard part.

## Subproblem decomposition

### SP2.1: Understand the test vector problem
**Task**: Survey known results on choosing $W$ and $V$ for Rankin-Selberg integrals.

Key results:
- **Jacquet-Piatetski-Shapiro-Shalika (JPSS)**: The local Rankin-Selberg integral computes $L(s, \Pi \times \pi)$ for suitable choices of $W, V$.
- **Test vector results**: Miyauchi, Matringe, Humphries-Jo — explicit test vectors for specific representations.
- **Newvector theory**: For $GL_n$ over non-archimedean fields, the newvector (essential vector) has special properties.

### SP2.2: Analyze the $u_Q$ shift
**Task**: Understand the role of $u_Q = I_{n+1} + QE_{n,n+1}$.

This shifts the $(n, n+1)$ entry by $Q$, where $Q$ generates the inverse conductor of $\pi$. This is a "conductor-adjusted" integral.

**Key**: The shift by $u_Q$ normalizes the integral so that the answer is insensitive to the conductor of $\pi$. This is what allows a single $W$ to work for all $\pi$.

### SP2.3: Analyze convergence
**Task**: Determine for which $s$ the integral converges absolutely.

Standard: The integral converges absolutely for $\text{Re}(s) \gg 0$ and has meromorphic continuation. The question asks for it to be **finite for all $s$**, meaning no poles.

### SP2.4: Analyze nonvanishing
**Task**: Show the integral is nonzero for all $s$.

The integral, as a function of $s$, is a ratio of L-functions times exponential factors. Nonvanishing for all $s$ requires understanding the zeros and poles of $L(s, \Pi \times \pi)$.

### SP2.5: Construct $W$
**Task**: Propose a specific $W$ (likely the newvector or a translate of it) and verify the properties.

**Candidate**: $W = W_{\Pi}^{\text{new}}$, the newvector of $\Pi$. Then $W(g \cdot u_Q)$ involves shifting the newvector by a specific unipotent element.

## Fine details

1. **Conductor normalization**: $\mathfrak{q}$ is the conductor ideal of $\pi$; $Q$ generates $\mathfrak{q}^{-1}$. The exact normalization matters.
2. **"For all $s \in \mathbb{C}$"**: Not just $\text{Re}(s) \gg 0$. Need analytic continuation + no poles.
3. **Measure normalization**: The Haar measure on $N_n \backslash GL_n(F)$ must be specified.
4. **"Generic"**: Both $\Pi$ and $\pi$ are generic (have Whittaker models).

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Hallucinating "standard facts" about GL(n) newforms | CRITICAL | Every invoked theorem must be cited with exact statement |
| Conductor normalization errors | HIGH | Force explicit tracking of all normalizations |
| Confusing "for all $s$" with "for $\text{Re}(s) \gg 0$" | HIGH | Check analytic continuation explicitly |
| Missing the universality of $W$ over all $\pi$ | HIGH | Highlight quantifier structure repeatedly |

## External dependencies (HEAVY)

- **JPSS**: Jacquet-Piatetski-Shapiro-Shalika, local Rankin-Selberg theory.
- **Cogdell-Piatetski-Shapiro**: "Remarks on Rankin-Selberg convolutions."
- **Miyauchi (2014)**: "Whittaker functions associated to newforms for GL(n)."
- **Matringe**: Test vectors for Rankin-Selberg integrals.
- **Humphries-Jo**: "Test vectors for Rankin-Selberg L-functions."
- **Nelson** (problem author): Recent work on subconvexity likely uses this machinery.

**Producer action**: Source Miyauchi 2014, Matringe papers, and Humphries-Jo for exact test vector statements.

## Agent task sequence

```
H: Source references (blocking). This is the most reference-heavy problem.
I: G0 — Formalize: write out quantifiers explicitly. Note W is universal over π.
R: Verify quantifier structure.
I: G1 — Extensive background assembly. Many EDs.
I: G2 — Route map:
   (A) W = newvector, prove universality via newvector properties
   (B) W = specific Kirillov function, use explicit Kirillov model computation
   (C) Existence via functional equation / gamma factor analysis
I: G3-G5-G6-G7 per standard
Scout: Send to Gemini Deep Think: "In local Rankin-Selberg theory for GL(n+1) × GL(n),
   what is the relationship between the newvector of Π and the test vector for the integral?"
```

---

# P1 — Φ⁴₃ measure quasi-invariance under smooth shift

## Success criteria

Either:
- **EQUIVALENT**: Prove $\mu$ and $T^*_\psi \mu$ are equivalent (same null sets), likely by exhibiting a Radon-Nikodym derivative
- **SINGULAR**: Prove $\mu \perp T^*_\psi \mu$ (mutually singular), likely via a support/energy argument

## Key mathematical insight

The Φ⁴₃ measure is the probability measure on $\mathcal{D}'(\mathbb{T}^3)$ formally given by:
$$d\mu(\phi) = \frac{1}{Z} \exp\left(-\int_{\mathbb{T}^3} \left(\frac{1}{4}\phi^4 + \frac{m^2}{2}\phi^2\right) dx\right) d\mu_{\text{GFF}}(\phi)$$

where $\mu_{\text{GFF}}$ is the Gaussian free field on $\mathbb{T}^3$ and the expression requires renormalization (Wick ordering).

**For Gaussian measures**: The Cameron-Martin theorem says $\mu_{\text{GFF}}$ and $T^*_\psi \mu_{\text{GFF}}$ are equivalent iff $\psi$ is in the Cameron-Martin space $H^1(\mathbb{T}^3)$. Since smooth $\psi$ is certainly in $H^1$, the Gaussian measures are equivalent.

**For Φ⁴₃**: The non-Gaussian perturbation changes things. The question is whether the Girsanov/Cameron-Martin mechanism survives the $\phi^4$ interaction.

## Subproblem decomposition

### SP1.1: Cameron-Martin for the Gaussian part
**Task**: Verify that for $\mu_{\text{GFF}}$, shift by smooth $\psi$ gives equivalent measures.

The GFF on $\mathbb{T}^3$ has Cameron-Martin space $H^1(\mathbb{T}^3)$. Smooth functions are in $H^1$. By Cameron-Martin theorem, $\mu_{\text{GFF}} \sim T^*_\psi \mu_{\text{GFF}}$ with explicit Radon-Nikodym derivative.

### SP1.2: Analyze the shift of the interaction term
**Task**: Compute $T^*_\psi \mu$ in terms of $\mu$.

$$\frac{dT^*_\psi \mu}{d\mu_{\text{GFF}}}(\phi) \propto \exp\left(-\int \frac{1}{4}(\phi - \psi)^4 + \frac{m^2}{2}(\phi - \psi)^2 \, dx\right)$$

vs.

$$\frac{d\mu}{d\mu_{\text{GFF}}}(\phi) \propto \exp\left(-\int \frac{1}{4}\phi^4 + \frac{m^2}{2}\phi^2 \, dx\right)$$

The ratio:
$$\frac{dT^*_\psi \mu}{d\mu}(\phi) \propto \frac{\exp(-\int \frac{1}{4}(\phi-\psi)^4 + \frac{m^2}{2}(\phi-\psi)^2)}{\exp(-\int \frac{1}{4}\phi^4 + \frac{m^2}{2}\phi^2)} \cdot \frac{dT^*_\psi \mu_{\text{GFF}}}{d\mu_{\text{GFF}}}(\phi)$$

**The key question**: Is this ratio well-defined (measurable, a.e. finite and nonzero) under $\mu$?

### SP1.3: Expand the interaction difference
**Task**: Compute $(\phi - \psi)^4 - \phi^4$ (and similarly for the $\phi^2$ terms).

$(\phi - \psi)^4 - \phi^4 = -4\phi^3\psi + 6\phi^2\psi^2 - 4\phi\psi^3 + \psi^4$

**Renormalization issue**: $\phi^3$ and $\phi^2$ require Wick ordering in 3D. The terms $\phi^3\psi$ and $\phi^2\psi^2$ are products of distributions with smooth functions, but the renormalization must be handled carefully.

Since $\psi$ is smooth and $\phi \in \mathcal{C}^{-1/2-\epsilon}(\mathbb{T}^3)$ (typical regularity of Φ⁴₃ samples), the products $\phi^k \cdot \psi^{4-k}$ for $k \leq 3$ require analysis:
- $\phi \cdot \psi^3$: distribution × smooth = well-defined
- $\phi^2 \cdot \psi^2$: Wick-ordered $:\!\phi^2\!: \cdot \psi^2$ is well-defined (smooth × Wick power)
- $\phi^3 \cdot \psi$: Wick-ordered $:\!\phi^3\!: \cdot \psi$ — this is the most singular term but still involves a distribution tested against smooth $\psi$

### SP1.4: Show the Radon-Nikodym derivative is well-defined
**Task**: Prove the exponential of the interaction difference is $\mu$-integrable.

The Radon-Nikodym derivative involves $\exp(\text{terms involving } :\!\phi^3\!:\psi, :\!\phi^2\!:\psi^2, \ldots)$. These are exponential moments of Wick powers, which ARE known to be finite under $\Phi^4_3$ (or at least under the Gaussian part, with the interaction providing additional decay).

### SP1.5: Determine the answer
**Likely answer**: **YES, equivalent.** The smooth shift is "mild" enough that the Cameron-Martin mechanism plus the integrability of Wick powers ensures equivalence.

**Why it might be singular**: If the interaction creates a support constraint that's broken by the shift. But smooth shifts shouldn't break support constraints (the Φ⁴₃ measure is supported on $\mathcal{C}^{-1/2-\epsilon}$, and shifting by smooth $\psi$ stays in this space).

## Fine details

1. **Renormalization**: All products involving $\phi^k$ for $k \geq 2$ require Wick ordering. The exact renormalization constants depend on the UV cutoff and must be tracked.
2. **Which construction of Φ⁴₃?**: Hairer (regularity structures), Gubinelli-Imkeller-Perkowski (paracontrolled), or Barashkov-Gubinelli (variational). The variational approach may be most useful for quasi-invariance.
3. **$\mu$-integrability of exponential moments**: Need to cite/prove that $\exp(c\int :\!\phi^3\!: \psi)$ is $\mu$-integrable for smooth $\psi$.
4. **Measurability of the shift**: $T_\psi$ maps $\mathcal{D}'(\mathbb{T}^3) \to \mathcal{D}'(\mathbb{T}^3)$ and is continuous, hence measurable.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Treating Φ⁴₃ as Gaussian | CRITICAL | Reviewer must reject any unqualified Gaussian analogy |
| Ignoring renormalization / Wick ordering | CRITICAL | Force explicit discussion of all products |
| Hallucinating measure theory results | HIGH | Every invoked fact about Φ⁴₃ must be ED with citation |
| Missing the regularity class of typical samples | HIGH | Must state: $\phi \in \mathcal{C}^{-1/2-\epsilon}$ |

## External dependencies (HEAVY)

- **Hairer (2014)**: "A theory of regularity structures." *Inventiones Mathematicae*. For Φ⁴₃ construction and regularity.
- **Barashkov-Gubinelli (2020)**: "A variational method for Φ⁴₃." *Duke Math Journal*. Variational construction — most useful for shift analysis.
- **Albeverio-Kusuoka (2021)**: "The invariant measure and the flow associated to the Φ⁴₃ quantum field model." For properties of the measure.
- **Cameron-Martin theorem**: Standard (e.g., Bogachev, *Gaussian Measures*).

**Producer action**: Source Barashkov-Gubinelli 2020 (key for variational characterization). Source any results on exponential moments of Wick powers under Φ⁴₃.

## Agent task sequence

```
H: Source Barashkov-Gubinelli 2020 and Albeverio-Kusuoka 2021.
I: G0 — Formalize: state measure, shift, equivalence definition.
   Explicitly note: this is NOT a Gaussian measure.
R: Verify formalization; confirm no Gaussian assumptions snuck in.
I: G1 — Background: Cameron-Martin, Wick powers, Φ⁴₃ regularity, Girsanov.
   Heavy ED list — most items need sourcing.
I: G2 — Route map:
   (A) Equivalence via explicit Radon-Nikodym derivative (expand interaction difference)
   (B) Singularity via support/energy argument
   (C) Equivalence via variational characterization (Barashkov-Gubinelli)
I: SP1.2 — Compute interaction difference explicitly
R: Check renormalization handling
I: G5 — Proof
R: G6 — Adversarial: challenge every use of "by analogy with Gaussian"
I: G7 — Package
```

---

# P7 — Uniform lattice with 2-torsion as π₁ of Q-acyclic compact manifold

## Success criteria

Either:
- **YES**: Construct a compact manifold $M$ (without boundary) with $\pi_1(M) = \Gamma$ (a uniform lattice in a real semisimple group with 2-torsion) whose universal cover $\tilde{M}$ is acyclic over $\mathbb{Q}$
- **NO**: Prove this is impossible (obstruction from torsion + acyclicity)

## Key mathematical concepts

- **Uniform lattice**: A discrete subgroup $\Gamma$ of a semisimple Lie group $G$ such that $G/\Gamma$ is compact.
- **2-torsion**: $\Gamma$ contains elements of order 2.
- **Q-acyclic universal cover**: $H_i(\tilde{M}; \mathbb{Q}) = 0$ for $i > 0$ (rational homology of a point).
- **Without boundary**: $M$ is a closed manifold.

## Subproblem decomposition

### SP7.1: Understand the constraints from lattice theory
- By **Selberg's Lemma**, every finitely generated subgroup of $GL_n(\mathbb{C})$ has a torsion-free subgroup of finite index. So $\Gamma$ has a finite-index torsion-free normal subgroup $\Gamma' \trianglelefteq \Gamma$.
- $\Gamma'$ acts freely on $G/K$ ($K$ = maximal compact), giving a manifold $M' = \Gamma' \backslash G/K$.
- $\Gamma$ acts on $G/K$ with fixed points from torsion elements, giving an orbifold $\Gamma \backslash G/K$, NOT a manifold.

### SP7.2: Can $\Gamma$ be the fundamental group of a manifold (not an orbifold)?
- **Key distinction**: $\Gamma \backslash G/K$ is an orbifold, but the question asks for $\Gamma$ to be $\pi_1$ of SOME manifold $M$, not necessarily $\Gamma \backslash G/K$.
- By a theorem of Eilenberg-Ganea and Wall: every finitely presented group is $\pi_1$ of a closed manifold (in dimension $\geq 4$). But can we additionally require Q-acyclicity of the universal cover?

### SP7.3: Q-acyclicity constraints
- If $\tilde{M}$ is Q-acyclic and $\Gamma = \pi_1(M)$ acts freely, then $H_i(M; \mathbb{Q}) = H_i(\Gamma; \mathbb{Q})$ (group cohomology).
- For uniform lattices in semisimple groups, $H^i(\Gamma; \mathbb{Q})$ is known in many cases (Borel, Matsushima formula).
- **Euler characteristic**: If $M$ is even-dimensional with Q-acyclic universal cover, $\chi(M) = \chi(\Gamma) = 1$ (since $\chi(\tilde{M}) = 1$).

### SP7.4: The role of 2-torsion
- 2-torsion in $\Gamma$ means $\Gamma$ cannot act freely on any contractible manifold of dimension equal to $\text{vcd}(\Gamma)$ (virtual cohomological dimension).
- But it CAN act freely on OTHER manifolds.
- **Davis construction**: Davis's reflection group trick can produce aspherical manifolds with prescribed fundamental groups, but these have contractible (not just Q-acyclic) covers.

### SP7.5: Obstruction vs construction
**Obstruction direction**: Perhaps the Euler characteristic or L²-Betti numbers provide constraints. If $\tilde{M}$ is Q-acyclic:
- $\chi(M) = 1$ (if $\tilde{M}$ is acyclic)... actually $\chi(\tilde{M})$ = Euler char of a Q-acyclic space = 1.
- By multiplicativity: $\chi(M) = [\Gamma : \Gamma'] \cdot \chi(M')$ for finite-index... not quite, need careful accounting for orbifold vs manifold.

**Construction direction**: Find a specific lattice and construct the manifold.

## Fine details

1. **"Acyclic over Q"**: $H_i(\tilde{M}; \mathbb{Q}) = 0$ for $i > 0$, AND $H_0(\tilde{M}; \mathbb{Q}) = \mathbb{Q}$ (connected). NOT contractible (integral homology may have torsion).
2. **"Compact manifold without boundary"**: Closed manifold. Not orbifold.
3. **"Uniform lattice"**: Cocompact discrete subgroup of a real semisimple group.
4. **Which semisimple group?**: The answer may depend on the ambient group.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Conflating acyclic with contractible | CRITICAL | Force definition check: Q-acyclic ≠ contractible |
| Confusing orbifolds with manifolds | CRITICAL | Reviewer must enforce manifold (free action) |
| Hallucinating theorems about lattices | HIGH | All lattice/group theory facts must be ED |
| Missing Selberg's lemma implications | MEDIUM | Include in G1 background |

## External dependencies

- **Selberg's lemma**: Standard, but state precisely.
- **Davis's reflection group trick**: Davis, *The Geometry and Topology of Coxeter Groups*. For aspherical manifold constructions.
- **Borel-Serre**: Compactification of locally symmetric spaces. Virtual cohomological dimension of arithmetic groups.
- **L²-Betti numbers**: Lück, *L²-Invariants: Theory and Applications to Geometry and K-Theory*.
- **Weinberger** (problem author): Likely has relevant papers on group actions and manifold rigidity.

**Producer action**: Source Davis's book (relevant chapters on aspherical manifolds), Lück's book (L²-Betti numbers of lattices).

---

# P8 — Polyhedral Lagrangian smoothing (4 faces per vertex)

## Success criteria

Either:
- **YES**: Prove every polyhedral Lagrangian surface with 4 faces per vertex has a Lagrangian smoothing
- **NO**: Construct a counterexample (a specific polyhedral Lagrangian surface with 4 faces per vertex but no Lagrangian smoothing)

Where a **Lagrangian smoothing** is a Hamiltonian isotopy $K_t$ ($t \in (0,1]$) of smooth Lagrangians extending continuously to $K_0 = K$.

## Key mathematical concepts

- **Polyhedral Lagrangian surface**: A 2-dimensional polyhedral complex in $\mathbb{R}^4$ where each face (2-cell) is a Lagrangian plane (symplectic form $\omega = dx_1 \wedge dx_2 + dx_3 \wedge dx_4$ vanishes on it).
- **4 faces per vertex**: Local combinatorial constraint — at each vertex, exactly 4 Lagrangian faces meet.
- **Hamiltonian isotopy**: The smoothing must be through Hamiltonian diffeomorphisms, not arbitrary isotopies. This is a much stronger constraint.

## Subproblem decomposition

### SP8.1: Local model analysis
**Task**: Classify the possible local models at a vertex where 4 Lagrangian planes meet in $\mathbb{R}^4$.

A Lagrangian plane in $\mathbb{R}^4$ is a 2-plane $V$ with $\omega|_V = 0$. The Lagrangian Grassmannian $\Lambda(2) \cong U(2)/O(2)$ parametrizes these.

At a vertex, 4 Lagrangian planes meet along edges. The combinatorial type is a cone over a graph (4 faces, some edges).

**Key constraints**: The symplectic form restricts which configurations of Lagrangian planes can meet.

### SP8.2: Local smoothing construction
**Task**: For each local model, determine if a local Lagrangian smoothing exists.

Replace the polyhedral neighborhood of each vertex with a smooth Lagrangian piece. This requires solving a local ODE/PDE while maintaining the Lagrangian condition.

### SP8.3: Global patching
**Task**: Show local smoothings can be glued into a global Hamiltonian isotopy.

**Obstruction**: Hamiltonian isotopy is a global constraint. Local pieces might not be compatible. The Maslov class and exactness of the Lagrangian provide potential obstructions.

### SP8.4: Topological constraints
**Task**: Determine what topology the polyhedral surface $K$ can have (given 4 faces per vertex).

4 faces per vertex gives an Euler characteristic constraint: if $V, E, F$ are vertices, edges, faces, then $4V = 2E$ (each edge borders 2 faces, each vertex has 4 faces implies each vertex has some number of edges), and $\chi = V - E + F$.

## Fine details

1. **"Faces are Lagrangians"**: Each 2-cell is contained in a Lagrangian plane. Edges and vertices automatically satisfy the Lagrangian condition (lower-dimensional).
2. **"Topological submanifold"**: $K$ is homeomorphic to a surface (no self-intersections as a topological submanifold).
3. **Hamiltonian isotopy, not just smooth isotopy**: The Lagrangian condition must be preserved by HAMILTONIAN diffeomorphisms.
4. **"Exactly 4 faces"**: Not "at least 4". This is a specific combinatorial constraint.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Confusing Lagrangian smoothing with topological smoothing | CRITICAL | Force explicit symplectic form check in every construction |
| Symplectic geometry is extremely specialized | HIGH | Heavy ED sourcing; don't trust agent claims |
| Local-to-global obstructions are subtle | HIGH | Require explicit gluing argument |
| Hamiltonian vs symplectic isotopy distinction | HIGH | Precise definitions at G0 |

## External dependencies

- **Abouzaid** (problem author): Papers on Lagrangian topology, Floer homology.
- **Hicks (2019)**: "Tropical Lagrangian hypersurfaces are unobstructed." For PL Lagrangian constructions.
- **Matessi (2021)**: Smoothing of tropical Lagrangians. Key reference.
- **Jauberteau-Rollin**: PL approximation of Lagrangians.

**Producer action**: Source Matessi 2021 and Hicks 2019 for tropical Lagrangian smoothing techniques.

---

# P5 — O-slice filtration for N∞ operad transfer systems

## Success criteria

1. **Define** the slice filtration on the $G$-equivariant stable category adapted to the incomplete transfer system $O$ associated to an $N_\infty$ operad
2. **State** a characterization of $O$-slice connectivity of a connective $G$-spectrum in terms of geometric fixed points
3. **Prove** the characterization

## Key mathematical concepts

- **$N_\infty$ operad**: Encodes "which norms are allowed" in equivariant algebra. Between $E_\infty$ (all norms) and naive $E_\infty$ (no norms).
- **Incomplete transfer system $O$**: The combinatorial data extracted from an $N_\infty$ operad. Specifies which transfers $G/H \to G/K$ are available.
- **Slice filtration**: A filtration on $G$-spectra by "slice connectivity" — measures equivariant connectivity subgroup-by-subgroup.
- **Geometric fixed points**: $\Phi^H(X)$ for a $G$-spectrum $X$ — the "honest" fixed points (vs. categorical fixed points $X^H$).

## Subproblem decomposition

### SP5.1: Pin down all definitions
**Task**: Precisely define:
1. $N_\infty$ operad and associated transfer system $O$
2. $O$-slice cells (the "building blocks" of the $O$-slice filtration)
3. $O$-slice connectivity ($X$ is $O$-slice $\geq n$ if...)
4. How geometric fixed points interact with $O$-structure

**This requires sourcing.** Definitions are in Hill-Hopkins-Ravenel (for the full transfer system case) and Blumberg-Hill (for the $N_\infty$ generalization).

### SP5.2: Recall the classical (full transfer) case
**Task**: State the classical result: $X$ is slice $\geq n$ iff $\Phi^H(X)$ is $(\lfloor n/|G/H| \rfloor)$-connected for all $H \leq G$ (or whatever the exact statement is).

This is in HHR. The $O$-version should modify this by restricting which subgroups $H$ are relevant (based on which transfers $O$ allows).

### SP5.3: Identify what changes with incomplete transfers
**Task**: The classical slice filtration uses ALL representation spheres $S^V$ for $V$ running over all representations. With incomplete transfers, only SOME representation spheres are "allowed" as slice cells.

The $O$-slice cells should be indexed by representations that are "compatible" with $O$.

### SP5.4: State and prove the characterization
**Task**: The characterization should take the form:

"$X$ is $O$-slice $\geq n$ if and only if for all subgroups $H$ in a specified family (depending on $O$), $\Phi^H(X)$ is $f(n, H, O)$-connected."

The function $f$ and the family of subgroups are what need to be determined.

## Fine details

1. **"Connective"**: $X$ is connective ($\pi_k(X^H) = 0$ for $k < 0$ and all $H$, or some variant).
2. **Geometric vs categorical fixed points**: $\Phi^H(X) \neq X^H$ in general. Geometric fixed points kill transfer information.
3. **The group $G$ is finite**: Fixed throughout.
4. **"Adapted to $O$"**: The filtration changes based on which norms/transfers are available.

## LLM capability gaps

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Definitions are extremely specialized | CRITICAL | Cannot proceed without exact sourced definitions |
| Models will hallucinate equivariant homotopy facts | CRITICAL | Every claim must be ED with citation |
| Confusing geometric and categorical fixed points | HIGH | Definition check at every use |
| Importing full-transfer results into incomplete setting | HIGH | Reviewer must catch this |

## External dependencies (CRITICAL)

- **Hill-Hopkins-Ravenel (2016)**: "On the nonexistence of elements of Kervaire invariant one." *Annals of Mathematics*. Section on slice filtration.
- **Blumberg-Hill (2015)**: "Operadic multiplications in equivariant spectra, norms, and transfers." $N_\infty$ operad definition.
- **Rubin (2017)**: "Combinatorial $N_\infty$ operads." Classification of $N_\infty$ operads via transfer systems.
- **Hill-Yarnall**: "A new formulation of the equivariant slice filtration with applications."
- **Blumberg** (problem author): Will have relevant recent/forthcoming work.

**Producer action**: Source HHR (slice filtration sections), Blumberg-Hill 2015, Rubin 2017. This problem CANNOT proceed without these.

---

## 6. Cross-problem reuse map

```
P10 ──builds──→ [Experiment harness, complexity analysis template]
   │                    │
   ▼                    ▼
P6  ──builds──→ [PSD toolkit, matrix concentration, counterexample search]
   │                    │
   ▼                    ▼
P4  ──builds──→ [Symbolic algebra, root analysis, numerical verification]
   │                    │
   ▼                    ▼
P9  ──builds──→ [Genericity reasoning, invariant theory, CAS pipelines]
   │                    │
   ▼                    ▼
P3  ──builds──→ [Definition sourcing discipline, combinatorial chain design]
   │                    │
   ▼                    ▼
P2  ──builds──→ [Heavy reference management, analytic continuation reasoning]
   │                    │
   ▼                    ▼
P1  ──builds──→ [Infinite-dimensional measure theory, renormalization tracking]
   │
   ▼
P7, P8, P5 ── [Full process maturity required; heavy external dependencies]
```

## 7. Global risk register

| Risk | Problems affected | Detection | Mitigation |
|------|------------------|-----------|------------|
| **Hallucinated theorems** | ALL, esp. P2, P5, P7 | Named Results Rule at every gate | ED ledger + human sourcing |
| **Quantifier errors** | P2, P6, P9 | Quantifier-normal-form rewrite at G0 | Reviewer enforces |
| **Gaussian analogy misapplied** | P1 | Reviewer rejects any unqualified analogy | Explicit non-Gaussian treatment |
| **Genericity ≠ universality** | P9 | Track "generic" vs "for all" at every lemma | Explicit Zariski-open sets |
| **Definition gaps** | P3, P5 | Cannot proceed without sourced definitions | Producer sources BEFORE agents start |
| **Numerical instability** | P4, P6 | High-precision (mpmath) + perturbation analysis | Multiple precision levels |
| **False confidence from experiments** | P4, P6, P10 | Require perturbation and edge-case testing | Not just random sampling |
| **Infinite loops / no convergence** | ALL | Gate cycle cap (k=3) | Pivot route or park problem |

## 8. Contamination hygiene

- Literature search allowed ONLY for prerequisites, not "the question itself"
- Log ALL search queries + URLs
- If a direct solution is found online: FREEZE that problem, mark as contaminated
- Prefer textbook references over blog posts
- Never search for "[problem author name] + [problem keywords]" as this may find the author's draft solution

## 9. Deliverable artifacts per problem

### Sprint deliverables (required)

During the sprint, each `PXX/` folder contains exactly 4 items:
1. `answer.md` — Clean answer (proof, counterexample, conjecture, or failure analysis). Status labeled (✅/🟡/📊/❌). Citations with statement numbers at bottom.
2. `audit.md` — All G0–G7 gate outputs as sections + routes tried + risks + human intervention log + metrics summary.
3. `experiments/` — Reproducible scripts + outputs (required for P04/P06/P09/P10).
4. `transcript.md` — Full prompts/responses + tool logs.

### Post-freeze archival expansion (optional)

If time permits after T_FREEZE, split `audit.md` into the 10-file canonical artifact set:
1. `00_formalization.md` — Precise restatement
2. `01_background.md` + `01_references.bib` — Prerequisites + sources
3. `02_route_map.md` — Solution strategies considered
4. `03_lemma_dag.md` + `.json` — Proof structure
5. `04_experiments/` — Scripts, outputs, analysis
6. `05_proof.md` or `.tex` — Complete proof
7. `06_review.md` — Adversarial review notes
8. `07_final_answer.md` — Clean answer
9. `07_audit_trail.md` — Full history of what changed and why
10. `07_metrics.json` — All collected metrics for this problem

This expansion is NOT required for the sprint. Do not spend sprint time on it.

## 10. Human admin checklist (do first)

- [ ] Repository created with folder scaffold (P01-P10 + common/ + metrics/)
- [ ] Logging pipeline operational (audit trail with ADMIN/LOGISTICS/MATHEMATICAL classification)
- [ ] Model access configured: Opus, Codex, + at least 2 scout models
- [ ] Gate cycle cap set (k=3 per gate; per-problem budgets from firstproof.md are primary caps)
- [ ] Reference sourcing for P3 and P5 (BLOCKING — agents cannot start these without definitions)
- [ ] Reference sourcing for P2 (SEMI-BLOCKING — agents can start G0 but not G1 without sources)
- [ ] Reference sourcing for P1 (Barashkov-Gubinelli 2020)
- [ ] Python environment with sympy, numpy, scipy, networkx, mpmath
- [ ] Optional: SageMath / Macaulay2 for P9
- [ ] Contamination hygiene rules communicated to all agents
- [ ] Autonomy boundary rules posted (Section 1.2) — no mathematical content from human
- [ ] All reference papers provided as verbatim PDFs, not human-summarized
