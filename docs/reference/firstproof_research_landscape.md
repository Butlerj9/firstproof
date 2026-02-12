# Research landscape for tackling the First Proof project

**First Proof is a small, independent, research-math evaluation: 10 recently-solved lemmas (≤~5-page solutions) released publicly on February 5, 2026, with encrypted answers revealed February 13, 2026.** It uses human expert grading and permits internet access, intentionally stressing the "proof-writing" stage of research rather than problem selection or theory invention. Under a strict one-shot protocol, the authors report that frontier models struggle on most questions; Abouzaid is quoted as saying models solved 2 of 10 in preliminary tests ([Harvard Gazette](https://news.harvard.edu/gazette/story/2026/02/when-you-do-the-math-humans-still-rule/)). This report synthesizes findings across five categories to inform a composite multi-agent plan: the project's design and community reception, mathematical domain context for each problem, multi-agent proof workflows, multi-model diversity research, and metrics infrastructure.

---

## 1. The First Proof project and its design philosophy

The paper was published on arXiv (2602.05192v1) on February 5, 2026, with encrypted solutions scheduled for release on **February 13, 2026**. Its 11 authors—including Fields Medalist **Martin Hairer**, MacArthur Fellows **Lauren Williams** (2025) and **Daniel Spielman** (2012), Breakthrough New Horizons Prize recipient **Mohammed Abouzaid**, and Kadison–Singer co-solver **Nikhil Srivastava**—held an organizational meeting at the Simons Institute (Berkeley) in early December 2025 to contribute problems they had recently solved but never published. None were employed by or consulted with AI companies during the project, a deliberate contrast with benchmarks like FrontierMath (funded by OpenAI).

The project's name comes from baking: "first proof" or bulk fermentation is the step where dough ferments as one mass before being shaped into loaves. The authors describe this as a preliminary effort to let ideas "ferment in the community" before producing a more structured evaluation. They explicitly note the question list **should not be considered a benchmark in its current form**—too few questions and no formal grading scheme. Problems span algebraic combinatorics, spectral graph theory, algebraic topology, stochastic analysis, symplectic geometry, representation theory, lattices in Lie groups, tensor analysis, and numerical linear algebra.

### Key design choices that inform any multi-agent approach

The project has several properties that constrain and inform how an AI system should approach it. Each problem has a proof of **roughly five pages or less**, deliberately chosen to fit within LLM context windows. The authors constrained problems to those with short solutions (~5 pages, "due to the technical limitations of current publicly available AI systems"). In the NYT interview, Abouzaid noted they avoided visual reasoning problems since "they are notoriously bad at visual reasoning" ([NYT](NYT via mirror, Siobhan Roberts, Feb 7 2026; original: nytimes.com/2026/02/07/science/math-ai-proofs.html)). Models are granted **unfettered access to outside resources** including internet searches, simulating real research conditions. The paper frames this as an attempt to understand **the role AI tools could play in professional mathematicians' workflows**, explicitly narrowing scope to the "final stage" (prove a well-specified statement) rather than question generation or theory building.

While the paper specifies **no formal grading scheme** and notes assessment must be by human experts, the project website states a clear criterion: an AI "answers" a question if it produces an **autonomous** proof meeting the rigor and scholarship standards of the mathematics literature, without relying on human input for any mathematical idea or content. Citations must include precise statement numbers and reference peer-reviewed journals or arXiv preprints ([1stproof.org](https://1stproof.org)). We adopt this as our submission standard.

In preliminary tests using **one-shot prompting** (no iterative interaction, no re-runs) with GPT 5.2 Pro and Gemini 3.0 Deepthink, the authors found models struggled on most problems. Abouzaid told the Harvard Gazette that AI solved 2 of 10 ([Harvard Gazette](https://news.harvard.edu/gazette/story/2026/02/when-you-do-the-math-humans-still-rule/)). In the New York Times, Hairer described the AI's output as sometimes resembling "a paper by a bad undergraduate student" who wanders around and then sticks in "'and therefore' and pray" ([NYT, Siobhan Roberts, Feb 7 2026](NYT via mirror, Siobhan Roberts, Feb 7 2026; original: nytimes.com/2026/02/07/science/math-ai-proofs.html)). Williams reported that on her problem, the model entered "an infinite loop" — repeatedly producing answers, retracting them, and modifying, never converging ([NYT](NYT via mirror, Siobhan Roberts, Feb 7 2026; original: nytimes.com/2026/02/07/science/math-ai-proofs.html)). She also described models hallucinating paper citations attributed to her that she never wrote ([Harvard Gazette](https://news.harvard.edu/gazette/story/2026/02/when-you-do-the-math-humans-still-rule/)). The problems are described as "lemmas"—not earth-shattering results, but requiring several years of postgraduate preparation in specific research areas.

**Critical distinction for our plan**: The authors' results come from a strict one-shot protocol with no iteration. The authors themselves note they "expect that through such interactions [they] would be able to coax the systems to produce better answers." Our multi-agent workflow—with iterative prompting, adversarial verification, literature sourcing, and multi-model routing—tests this hypothesis directly. We will measure the delta via pass rate and lemma-closure velocity.

### Community reception reveals both enthusiasm and methodological concerns

Andrew Sutherland (MIT) endorsed the project as "a much better experiment than any I have seen to date." On Hacker News (100+ comments), a researcher characterized the problems as "lemmas that I encountered while doing my PhD" and noted they test "whether LLMs can really synthesize results from knowledge that require a human several years of postgraduate preparation." However, ML researchers criticized the lack of formal grading rubrics, reproducibility protocols, and standardized evaluation infrastructure. Emergent Mind's automated analysis identified missing elements: no difficulty calibration, no inter-rater reliability measures, no multi-turn interaction protocols, no compute controls, and no partial-credit scheme.

A particularly informative blog post by a Northeastern CS professor documented spending **2 million tokens** exploring Problem 6 (Spielman's spectral graph theory problem) with Gemini over half a day. Though unsuccessful, he described AI as an "excellent accelerator" for learning the problem's structure—but documented the model hallucinating a nonexistent mathematical axiom and presenting it with full confidence. He self-assessed understanding only **2 of 10** problems despite holding a PhD in a relevant field, underscoring the specialized difficulty.

---

## 2. Mathematical domain context for each problem

Each of the ten problems draws on deep, specialized mathematical knowledge. The following provides high-level context sufficient to inform workflow planning—prerequisite areas, key difficulty factors, and the mathematical landscape surrounding each domain.

### P1: Φ⁴₃ measure and Cameron-Martin quasi-invariance

This problem lives at the intersection of constructive quantum field theory and infinite-dimensional probability. The **Φ⁴₃ measure** is a non-Gaussian probability measure on Schwartz distributions, constructed by perturbing a Gaussian free field with a renormalized quartic interaction. Hairer's own theory of **regularity structures** (Fields Medal 2014) and Gubinelli-Imkeller-Perkowski's paracontrolled distributions made rigorous construction possible via stochastic quantization. The Cameron-Martin theorem characterizes quasi-invariance of Gaussian measures under translation—extending this to the non-Gaussian Φ⁴₃ setting is the deep challenge. Prerequisites include Gaussian measures on Banach spaces, Wick renormalization, singular SPDEs, and Besov space analysis.

### P2: Whittaker models and Rankin-Selberg test vectors

Situated in the Langlands program, this problem involves the representation theory of GL(n) over **non-archimedean local fields**. **Whittaker models** realize representations via functions satisfying specific transformation properties; the **Multiplicity One Theorem** (Shalika) guarantees uniqueness of Whittaker functionals. Rankin-Selberg integrals produce L-functions L(s, π × π') by integrating Whittaker functions, and the "test vector problem" seeks explicit vector choices that cleanly extract L-factors. The key structural challenge is finding a single Whittaker function W for Π that works universally across all generic representations π of the smaller group. Prerequisites span smooth representations of p-adic groups, the Bernstein-Zelevinsky classification, conductor theory, and the JPSS local Rankin-Selberg integral.

### P3: Interpolation ASEP polynomials and Markov chains on partitions

This bridges algebraic combinatorics and integrable probability. **Macdonald polynomials** P_λ(x; q, t) generalize Schur, Hall-Littlewood, and Jack polynomials, with deep connections to double affine Hecke algebras and Hilbert schemes. **Interpolation Macdonald polynomials** (Knop-Sahi) are inhomogeneous deformations defined by vanishing conditions. ASEP polynomials connect to stationary measures of the asymmetric simple exclusion process through **multiline queues** (Corteel-Mandelshtam-Williams). The interplay between algebraic vanishing conditions and probabilistic Markov chain stationarity is the core difficulty.

### P4: Finite free convolution and root repulsion

The **⊞ₙ operation** (Marcus-Spielman-Srivastava) takes two real-rooted polynomials and produces the expected characteristic polynomial of A + UBU* for random unitary U. This is a finite analogue of Voiculescu's free additive convolution from free probability. The MSS "interlacing families" method resolved both the **Kadison-Singer problem** and the existence of bipartite Ramanujan graphs (Annals of Mathematics, 2015). Prerequisites include random matrix theory, the R-transform and K-transform, and polynomial interlacing theory. This is likely the most computationally accessible problem, as one blog post author noted it was one of only two problems they could understand.

### P5: Equivariant slice filtration for incomplete transfer systems

The central task is to **define a slice filtration on G-equivariant spectra adapted to an incomplete transfer system** (associated to an N∞ operad) and **characterize slice connectivity via geometric fixed points**. The classical slice filtration (Hill-Hopkins-Ravenel, from the Kervaire invariant one proof) uses all representation spheres as slice cells; with incomplete transfer systems, only those compatible with the allowed norms/transfers should appear. **N∞ operads** (Blumberg-Hill, 2015) encode which norms an equivariant algebra admits, and their homotopy types biject with **transfer systems**—purely combinatorial objects classified by Rubin (2017). Prerequisites include operads, equivariant spectra, Mackey and Tambara functors, and geometric fixed point functors. The combinatorial lattice structure may create opportunities for computational exploration, but the core question is homotopy-theoretic.

### P6: ε-light vertex subsets and Laplacian PSD domination

This problem asks whether every graph contains a large vertex subset $S$ whose induced edges are spectrally dominated by ε times the full Laplacian: $\epsilon L - L_S \succeq 0$. This is **not** the standard edge-sampling spectral sparsifier theorem (Spielman-Srivastava); it is a vertex-subset PSD domination problem that draws on related techniques—matrix concentration inequalities, effective resistances, and barrier methods—but requires genuinely different arguments. The **Batson-Spielman-Srivastava** deterministic sparsification method and its barrier/potential function approach provide the closest technical toolkit. The blog post exploring this problem found AI helpful for learning the landscape but unable to complete the proof.

### P7: Lattices in Lie groups and rational acyclicity

This draws on **Margulis's fundamental results**: the Arithmeticity and Superrigidity Theorems for lattices in semisimple Lie groups of rank ≥ 2. For rank-1 groups, non-arithmetic lattices exist and rigidity differs. Rational acyclicity and torsion in fundamental groups connect to group cohomology, rational homotopy theory (Sullivan-Quillen), and the Borel conjecture. Prerequisites include Lie theory, algebraic groups, Bruhat-Tits buildings, and Borel-Serre compactification. This is among the most abstract problems.

### P8: Polyhedral Lagrangian surfaces and Hamiltonian isotopy

**Lagrangian submanifolds** are half-dimensional submanifolds where the symplectic form vanishes—central to mirror symmetry. Polyhedral (PL) Lagrangians are relatively unexplored. While smooth Lagrangian tori can be C¹-approximated by PL ones (Jauberteau-Rollin), Moser's trick fails in the PL setting. Connections to **tropical geometry** (Hicks, Matessi) through SYZ fibrations provide another angle. Prerequisites include symplectic manifolds, Floer homology, pseudoholomorphic curves (Gromov), and the Arnold nearby Lagrangian conjecture.

### P9: Uniform-degree polynomial invariants for generic tensor families

This asks whether a polynomial map $F$ with **degrees independent of n** can detect rank-1 scalings of tensors built from Zariski-generic 3×4 matrices. The connection to **hyperdeterminants** (Cayley 1843, Gelfand-Kapranov-Zelevinsky 1992) and algebraic invariants of tensors is a possible lens, though not obviously implied by the statement. Plücker relations and torus-orbit testing via invariant theory are likely more directly relevant. Prerequisites include algebraic geometry (dual varieties, Segre embeddings), GIT quotients, and representation theory of GL and SL.

### P10: RKHS tensor decomposition and preconditioned CP-ALS

The most applied problem: extending **CP decomposition** (CANDECOMP/PARAFAC) to "quasi-tensors" with infinite-dimensional RKHS modes. The **Representer Theorem** reduces infinite-dimensional optimization to finite dimensions. CP-ALS (Alternating Least Squares) solves normal equations with Khatri-Rao structure but suffers from ill-conditioning. Preconditioned conjugate gradient methods can accelerate the linear systems. Prerequisites include RKHS theory (Mercer's theorem), tensor algebra, and numerical optimization. This problem is likely the most amenable to computational experimentation.

---

## 3. Multi-agent workflows for mathematical proof production

The field of AI-assisted mathematical reasoning has advanced rapidly through 2025-2026, with several architectural paradigms demonstrating clear effectiveness. The most successful systems share a common pattern: **separation of proof generation, verification, and refinement into distinct agent roles**, combined with formal verification as ground truth. Three archetypes dominate.

### Archetype A: Generator-verifier-refiner loops

**MALT** (COLM 2025) formalized the three-role architecture: a Generator produces initial solutions, a Verifier critiques for errors, and a Refinement Model integrates feedback. Using Llama 3.1 8B as the base, MALT achieved **57.25% on MATH** (+15.66% relative improvement). Each agent learned from both correct and incorrect trajectories via supervised fine-tuning plus DPO, with value iteration propagating reward signals. The sequential pipeline consistently outperformed single-agent approaches.

The most impressive recent result comes from **Le Duc & Liberti's prover-verifier protocol** (arXiv:2510.12829, October 2025), which solved **5 of 6 IMO 2025 problems** using multiple GPT-5 instances with role-specific system prompts. Prover instances generate proofs, verifier instances check step-by-step, and a TTVR (Test-Time Verification and Refinement) loop iterates between them. Additional "research mode" agents handle literature search. The minimal human intervention required—only checking that the formal Lean statement matches the informal one—makes this protocol directly relevant to our workflow.

**DeepSeekMath-V2** (November 2025) achieved gold on IMO 2025 (5/6 problems) and strong results on Putnam 2024 through generator-verifier co-evolution. The system trains a verifier that scores proofs on a {0, 0.5, 1} rubric for rigor, then trains a generator to satisfy the verifier. At test time, **64 proof candidates** undergo **64 independent verification passes** across up to 16 iterations, creating an adversarial dynamic.

**Implication for our workflow**: The prover-verifier architecture with iterative refinement is the backbone of our plan. The Le Duc & Liberti protocol is the closest existing template.

### Archetype B: Formal tool-in-the-loop (Lean 4)

**DeepSeek-Prover-V2** (April 2025) introduced recursive subgoal decomposition: a general LLM generates natural language proof sketches and decomposes theorems into `have` statements with `sorry` placeholders, then a specialized 7B prover solves each subgoal recursively, with Lean 4 as the verifier. This achieved **88.9% on MiniF2F-test** and 49/658 on PutnamBench.

**Hilbert** (Apple, NeurIPS MATH-AI 2025 Workshop) pushed this further with a four-component system: an informal LLM for mathematical reasoning, a specialized prover LLM for Lean 4 tactics, Lean 4 as formal verifier, and a semantic theorem retriever. This achieved the best known score on miniF2F (**99.2%**) and **462/660 (70.0%) on PutnamBench**—a 422% improvement over the prior best public baseline.

**AlphaProof** (DeepMind, Nature November 2025) couples a fine-tuned Gemini with AlphaZero-style RL, using Lean verification as the reward signal. It solved 3/5 non-geometry IMO 2024 problems, including P6 solved by only 5/609 human contestants.

However, formal verification faces a critical bottleneck for research-level problems: **autoformalization**. Converting novel research mathematics into Lean requires formalizing concepts that may not exist in mathlib. The **MASA** multi-agent system (EMNLP 2025) and **FORMAL** system (2025) address this with agentic feedback loops achieving 86-92% accuracy, but typically require 2-3 iterations. For First Proof problems involving highly specialized mathematics, autoformalization is the primary bottleneck—many required concepts likely lack mathlib coverage.

**Implication for our workflow**: Lean 4 verification is optional and scoped — use it only if the needed objects are already in mathlib. For P4, P6, P10 (computationally concrete), attempt formalization if time permits. For all other problems, rely on proof-audit plus computational sanity checks. Never burn time on autoformalization of specialized concepts.

### Archetype C: Multi-model ensemble and routing

This archetype is covered in detail in Section 4. The key systems are ReConcile (multi-round multi-model discussion), Archon (Bayesian-optimized model configurations), and MasRouter (cascaded controller networks for role allocation). Debate-based approaches (**Debate4MATH**, ACL 2025 Findings) show promise but face a known asymmetry: erroneous reasoning paths generate lengthier justifications that can overwhelm simpler correct arguments. **Free-MAD** (2025) addresses this with anti-conformity modes.

**Implication for our workflow**: Use model diversity for scout/exploration queries (see Section 4), not for debate-style consensus where the "loudest wrong answer wins" failure mode applies.

### Known failure modes that must be engineered around

Research across multiple systems identifies consistent LLM failure patterns in mathematical reasoning:

- **Hallucinated axioms and results**: Models confidently cite nonexistent theorems or attribute results to papers that don't contain them (documented in the P6 blog post and Williams's account of fabricated citations; [Harvard Gazette](https://news.harvard.edu/gazette/story/2026/02/when-you-do-the-math-humans-still-rule/))
- **Boundary neglect**: Models correctly identify general trends but fail on singular or special cases
- **Calculation drift**: Symbolic precision degrades as reasoning chains grow
- **Premature closure**: Models elaborate on easy steps, then skip the crux with hand-waving (Hairer, [NYT](NYT via mirror, Siobhan Roberts, Feb 7 2026; original: nytimes.com/2026/02/07/science/math-ai-proofs.html))
- **Infinite loops**: Models repeatedly propose and retract answers without convergence (Williams, [NYT](NYT via mirror, Siobhan Roberts, Feb 7 2026; original: nytimes.com/2026/02/07/science/math-ai-proofs.html))
- **Sensitivity to perturbation**: Minor rephrasing causes significant accuracy drops (Apple GSM-Symbolic study)

---

## 4. Multi-model diversity yields measurable mathematical gains

Strong evidence now exists that deploying diverse LLM families produces better mathematical results than scaling a single model. The key insight: **different models solve different subsets of problems**, and cross-family diversity exceeds within-model sampling diversity.

### Frontier models have distinct mathematical profiles

As of early 2026, frontier models show clear differentiation on mathematical benchmarks: GPT-5.2, Gemini 3.0 Pro, Claude Opus, DeepSeek-R1, and Qwen3-235B each demonstrate distinct strengths. GPT-5.2 leads on competition math and FrontierMath research problems. Gemini 3.0 Pro excels in long-context and exploratory reasoning via its "Deep Think" mode. Claude Opus shows documented strength in code-based mathematical approaches and maintaining structured argumentative throughlines. DeepSeek-R1 achieves strong performance through large-scale RL. Qwen3-235B shows notable strength in algorithmic reasoning (high CodeForces Elo), suggesting complementary value on constructive/computational problems.

The structural point matters more than exact scores: **different model families solve different problem subsets**. FrontierMath's Tier 4 results demonstrated that one model solved research-level problems that no other model solved, and even across different runs of the same model, different problems were solved. This is direct evidence that solution spaces differ across models and even across sampling runs.

### Quantitative evidence for ensemble gains

**ReConcile** (ACL 2024) implements multi-round discussion between models from different families with confidence-weighted voting, achieving meaningful improvement on MATH when incorporating diverse models. The paper quantified that "responses from different models in ReConcile are most diverse" compared to paraphrased responses from a single model or multiple instances of the same model.

**Archon** (Stanford, 2024-2025) uses Bayesian optimization to find optimal multi-model configurations and outperforms individual frontier models by substantial margins across benchmarks including MATH. Even open-source-only configurations surpass single-model state-of-the-art. The **A-HMAD** (Adaptive Heterogeneous Multi-Agent Debate) system achieves higher accuracy with fewer factual errors by assigning distinct expertise roles to diverse agents.

The **Multi-Model Consensus Engine** (January 2026) provides the clearest mechanistic explanation: "Mixing families (Llama, Mistral, Qwen) increases diversity of errors and makes consensus more informative. The strongest gains occurred in math reasoning and truthfulness tasks, where the structure of agreement and disagreement is particularly informative."

### Theoretical grounding in latent space geometry

Several 2025 research papers explain why model diversity helps at a fundamental level. Meta's **Coconut** framework demonstrated that LLMs reason in continuous latent space with significant diversity in reasoning paths. The **Latent-SFT** paper showed that latent reasoning "effectively captures a superposition of diverse reasoning trajectories." Research on **Selective Layer Restoration** demonstrates that RLHF induces different mode collapse patterns across model families (Llama, Qwen, Gemma), meaning combining them inherently increases reasoning diversity.

The core argument: different LLMs have different training data distributions, architectures (dense vs. MoE), optimization objectives (RLHF vs. GRPO vs. DPO), latent space geometries, and mode collapse patterns. Even when two models fail on a given problem, **they fail for different reasons and at different reasoning steps**, making ensemble approaches structurally valuable.

### Practical routing for our workflow

The paper explicitly highlights the difficulty of disentangling "problem-solving" from "search/translation" and allows web access. Our multi-model routing should exploit this:

- **Search/synthesis engines**: Deploy Gemini 3.0 Deep Think for exploratory long-context literature synthesis
- **Proof constructors**: Deploy GPT-5.2 and Claude Opus for structured proof generation
- **Anti-hallucination verifiers**: Deploy DeepSeek-R1 and Qwen3 as adversarial scouts that search for counterexamples and challenge cited results

The **MasRouter** framework (ACL 2025) provides a formal architecture for routing across collaboration modes, role allocation, and LLM selection using cascaded controller networks.

---

## 5. Metrics and instrumentation remain the weakest link

Despite rapid progress in mathematical reasoning capabilities, the measurement infrastructure for tracking AI proof attempts lags significantly. **No existing tools are purpose-built for mathematical reasoning workflows**—current platforms handle generic LLM observability but lack proof-specific step tracking, formal verification integration, or convergence detection.

### What metrics exist today

The dominant metric in formal theorem proving is **pass@K**: success rate within K attempts. For research-level problems requiring proofs rather than numerical answers, the field is moving toward structured rubrics. **IMO-ProofBench** (DeepMind, 2025) uses a 7-point grading scale per problem with partial credit for intermediate results. **IMProofBench** (ETH Zurich) proposes 100-point grading schemes with detailed rubrics, metadata on mathematical area and difficulty dimensions, and plans for AI-assisted grading.

**Process Reward Models** (PRMs) provide step-level verification. OpenAI's foundational work ("Let's Verify Step by Step," Lightman et al., 2023) demonstrated that process supervision significantly outperforms outcome supervision on MATH. **ThinkPRM** (2025) uses only 1% of PRM800K labels yet outperforms discriminative PRMs by generating verification chains-of-thought for each step. **FoVer** (2025) uses formal verification tools (Z3, Isabelle) to automatically annotate step-level error labels, with surprising cross-task generalization.

For tracking token efficiency, **OckBench** (2025) explicitly measures reasoning efficiency as the ratio of decoding tokens to accuracy, finding that models with comparable accuracy can differ **4x or more** in token consumption. This matters for First Proof, where exploration budgets must be managed across 10 problems.

### Observability platforms and logging schemas

The emerging standard for multi-agent tracing uses **OpenTelemetry-compatible** hierarchical spans. Each trace captures agent ID, role, model used, input/output, latency, token usage (prompt, completion, reasoning, cached), tool invocations, and agent-to-agent handoffs. **Langfuse** (open-source, self-hostable) offers nested traces, session grouping, and cost tracking. **LangSmith** provides deep tracing for LangChain/LangGraph ecosystems. **Weights & Biases Weave** supports hierarchical agent tracing with built-in scorers.

For a First Proof workflow, the critical gap is **proof-specific instrumentation**: tracking lemmas proved, goals remaining, proof tree depth, formal verification feedback loops, semantic similarity between proof attempts (for circularity detection), and distinct strategies explored. The **ProSEA framework** (2025) offers a promising pattern with "exploration traces" documenting reasoning including both successful paths and informative failures.

### A practical logging schema for First Proof attempts

Based on the research, a fit-for-purpose schema should capture:

- **Problem-level**: problem ID, mathematical domain, attempt number, total token budget consumed, strategies attempted (tagged by approach type), current best proof status (none / partial / candidate / verified)
- **Agent-level per interaction**: agent role (prover/verifier/researcher/decomposer), model used, reasoning token count vs. completion tokens, tool calls (web search, code execution, formal verification), confidence self-assessment
- **Proof-level**: proof tree with subgoals (open/closed/sorry), intermediate results established, citations generated and verified, verification attempts and outcomes (if using Lean/Isabelle), similarity score to previous attempts on same problem
- **Progress indicators**: number of distinct strategies attempted, proof obligation reduction rate, novel intermediate results per iteration, token efficiency (progress per 10K tokens)
- **Lemma closure velocity**: (subgoals closed) / (tokens or wall-clock), as the primary "are we making progress?" signal
- **Novelty vs. repetition detector**: embedding similarity between successive drafts to catch "infinite loop / rephrase loop" behavior—the failure mode Williams described where models become unreliable near expert level

### Transcript compliance

The paper explicitly asks participants to share **complete transcripts** of interactions. Our logging should produce sanitized transcripts (including tool calls and agent handoffs) suitable for public release, matching the project's preferred reporting format.

### Source hygiene

The paper's answers hadn't appeared publicly before release, but community discussion of specific questions has already begun ([abhvio.us](https://abhvio.us/posts/pony/)). To preserve the "novel task" premise:

- Disallow browsing anything that claims to solve a numbered First Proof question until the escalation ladder reaches "last resort"
- Log any accidental exposure as an "info hazard event" in the metrics
- Prefer textbook references over blog posts for prerequisite sourcing
- Never search for "[problem author name] + [problem keywords]" as this may surface draft solutions
- If a direct solution is found online: **freeze** that problem and mark it as contaminated

**Operational rule**: All web searches are logged in `CONTAMINATION.md` with timestamp, query, and purpose. If exposed to a direct solution: (1) freeze problem, (2) log exposure event with URL and what was seen, (3) do NOT incorporate, (4) mark status as `CONTAMINATED_EXTERNAL_SOLUTION`. This is non-negotiable for claiming autonomous ✅ status.

---

## Conclusion: what these findings mean for a multi-agent First Proof plan

Five key insights emerge from this research. First, the project's design—**≤5-page proofs, unfettered internet access, short solutions**—is well-suited to multi-agent LLM workflows, despite preliminary one-shot results showing only 2/10 solved. The authors themselves expect iterative interaction would improve results; structured systems like the Le Duc & Liberti protocol achieved 5/6 on IMO 2025 where single-shot approaches failed. Our workflow tests whether this gap extends to research-level problems.

Second, the **recursive decomposition pattern** (demonstrated by Hilbert, DeepSeek-Prover-V2, and the prover-verifier protocol) is the most promising architectural approach. Each First Proof problem should be decomposed into subgoals, with specialized agents handling generation, verification, literature search, and refinement in iterative loops.

Third, **model diversity is not optional**—it is a structural advantage. Cross-family ensembles consistently outperform single-model sampling, and evidence shows different models solve different problem subsets. Deploy at least 3-4 model families with problem-aware routing, using some models as search/synthesis engines, others as proof constructors, and at least one as an anti-hallucination verifier.

Fourth, **formal verification** via Lean 4 is optional and scoped—attempt only where needed objects exist in mathlib (primarily P4, P6, P10). For problems in areas with poor mathlib coverage (P1, P2, P5, P7, P8), informal prover-verifier loops with adversarial checking and computational sanity checks are more practical and time-efficient.

Fifth, the measurement infrastructure must be built from scratch. No existing platform handles proof-specific telemetry, and the lack of standardized partial-credit schemes means progress tracking must rely on custom instrumentation—tracking subgoal closure rates, lemma closure velocity, strategy diversity, and token efficiency as primary indicators of whether a multi-agent system is making genuine progress or spinning in circles. Source hygiene must be engineered in from the start.

### Counterexample-first principle for YES/NO problems

Four of the ten problems (P4, P6, P7, P8) ask whether something is true. A systematic bias toward proof attempts wastes time if the answer is NO. For all YES/NO problems, **allocate at least 30-50% of early budget to aggressive counterexample search** before committing to a proof route. This applies especially to P4 (adversarial root configurations) and P6 (adversarial graph families).

### Time budget realism

In a 2-3 day sprint we realistically expect ✅ only on P10 (a derivation problem). P4 and P6 may reach 🟡 (candidate proof) or 📊 (conjecture with numerical evidence). The remainder are mostly ❌ feasibility probes unless blocking dependencies (definitions for P3/P5) are sourced fast.

### Operational bridge

This background document informs the design of gates, budgets, and publication cadence specified in the canonical runbook (`firstproof.md`). When this document and the runbook disagree, the runbook wins.
