# Post-Mortem: First Proof Sprint — Root Cause Analysis

**Date**: 2026-02-14
**Scope**: All 10 problems (P01–P10), with deep focus on the 4 sign conflicts
**Alignment score**: 47.5% risk-adjusted (3A + 1B + 2C + 4F)

---

## Executive Summary

Of 10 research-level mathematics problems attempted in a ~4-day sprint:
- **3 correct** (P02, P09, P10) — all theorem-level aligned with external solutions
- **1 directionally correct** (P05) — same characterization, internal documentation issues
- **2 partial** (P03, P04) — correct answer (YES) but proved only for small n; external solutions prove all n
- **4 wrong sign** (P01, P06, P07, P08) — repo answer is the OPPOSITE of the external solution

The 4 sign conflicts represent the most serious failures. This document traces each to root causes across model capability, agent design, tooling, orchestration, workflow, and time constraints.

---

## Part I: Problem-by-Problem Root Cause Analysis

### P01: We said YES, external says NO

**Our claim**: The Phi-4-3 measure is quasi-invariant under smooth translations. Proved via Girsanov factorization + BG stability extension + Hairer-Steele independent path.

**External answer (Martin Hairer)**: The measures are MUTUALLY SINGULAR. The shift creates a distinguishing event B_gamma using regularity structures (Wick powers, paraproducts), with a logarithmically divergent renormalization constant c_{N,2} that causes the distinguishing functional to diverge.

**Root causes (ranked by severity)**:

1. **Model: Initial bias never challenged (CRITICAL)**. Truth mode was set to 70% YES / 30% NO in Session 1. This prior was NEVER updated despite 7 failed proof approaches (Sessions 3-9). The model kept looking for YES evidence and never seriously explored the singularity direction (Route B was "deprioritized" in G2 as "implausible"). The external comments packet confirms: this is the exact opposite of the correct answer.

2. **Model: Misapplication of cited results (CRITICAL)**. We cited Hairer's own co-authored work to reach the OPPOSITE conclusion from Hairer himself. The key errors:
   - **Young's inequality for Wick powers**: The argument `|:phi^3: psi| <= delta :phi^4: + C(delta)` is FALSE for Wick-ordered products. The Wick subtraction terms (3 c_epsilon phi_epsilon with c_epsilon -> infinity) cannot be absorbed. This is not a technical gap — it is the REASON the measures are singular.
   - **BG Theorem 3 "routine extension"**: We spent 20+ tool calls convincing ourselves that BG's proof extends to V_c. But BG's construction specifically handles the standard Phi-4-3 potential; the :phi^3:psi perturbation is qualitatively different (it changes the renormalization structure in a way that makes the shifted measure singular).
   - **Hairer-Steele misapplication**: We claimed their sub-Gaussian tail bound + Young gives exponential integrability. But Young's inequality for Wick powers is invalid in 3D.

3. **Agent: Self-review echo chamber**. P01's G6 review was "self-adversarial" (Claude reviewing Claude) — the audit explicitly notes "no external Codex available for this lane." The scout cross-check (E8) was also Claude. No genuinely independent review ever examined the proof.

4. **Agent: Sunk-cost escalation**. The problem was correctly PARKED in Sessions 1-4 (3+ critical references blocked). It was then UNPARKED when the partition function approach was found (Session 5). After 10 sessions and 20+ messages, the agent was deeply invested in YES and couldn't reverse course.

5. **Workflow: No singularity test**. The agent never constructed a candidate distinguishing event or computed the divergence rate of renormalization constants under the shift. A single computation of c_{N,2} ~ log N under the shift would have revealed the mechanism for singularity.

**External commentary match**: "The answer given by GPT-Pro simply quotes that note, claiming that it contains a detailed proof... This is incorrect." Also: "the LLM would take as a premise the (wrong!) statement that the Phi-4-3 measure is equivalent to the free field measure." Our error is structurally identical — assuming the interaction is "soft enough" to preserve quasi-invariance.

**Fault allocation**: 60% model capability (Wick power confusion), 25% agent design (self-review, no direction reversal), 15% workflow (no singularity test).

---

### P06: We said NO, external says YES

**Our claim**: No universal constant c > 0 exists. K_n provides a counterexample family: max alpha-light set in K_n has size max(1, floor(alpha*n)), so choosing alpha = c/2 gives size < c*n.

**External answer (Dan Spielman)**: YES — epsilon-light sets of size >= epsilon*n/42 always exist, proved via BSS barrier function adaptation.

**Root causes — NOTE: This case may be a false positive in the comparison**:

The external comparison document classifies this as a "Critical Mismatch." However, careful analysis reveals that Spielman's bound |S| >= alpha*n/42 does NOT give a universal constant c independent of alpha. As alpha -> 0, the guaranteed set size also -> 0. Our K_n counterexample shows: for K_n at alpha = c/2, max alpha-light = floor(cn/2) < cn. This is numerically consistent with Spielman's bound (cn/84 < cn/2) — there is no contradiction between the two results.

**Possible resolutions**:
- **Quantifier interpretation difference**: If "constant c" is meant to be universal over both G AND alpha, our answer (NO) appears correct. If c is allowed to depend on alpha (c = alpha/42), Spielman's answer (YES) is correct. The problem statement's quantifier structure (exists c, forall G, forall alpha) supports our reading.
- **Weighted vs unweighted**: Spielman's lemma is for weighted graphs; our counterexample is unweighted. But unweighted is a special case, so a counterexample in the unweighted case disproves the general claim.
- **External comparison error**: The Codex analysis may have mischaracterized Spielman's result as answering the exact question posed.

**If our answer is indeed wrong**, the root causes would be:
1. **Model: Problem misinterpretation**. Possible confusion about the quantifier structure or a definition we missed.
2. **Tooling: No engagement with BSS barrier functions**. We never explored Spielman's own prior work on barrier functions, which might have revealed the correct approach.

**External commentary match**: "ChatGPT 5.2 Pro asserted that it could not answer the question. So, it instead offered a correct upper bound of 1/2 on the constant, if it exists." This suggests even ChatGPT Pro found this problem difficult and couldn't determine the sign.

**Fault allocation**: UNCERTAIN. If wrong: 50% model (problem interpretation), 30% agent (no literature engagement), 20% time. If correct: 0% — comparison error.

**Recommendation**: This problem needs manual verification by the competition organizers.

---

### P07: We said YES, external says NO

**Our claim**: YES — a uniform lattice Gamma in SO_0(5,1) with 2-torsion is pi_1(M) for a closed 5-manifold M with Q-acyclic universal cover. Proof via Q-PD_5 (Shapiro) + surgery realization + Borel existence.

**External answer (Cappell, Weinberger, Yan)**: NO — the same impossibility as Fowler's theorem (odd torsion) extends to 2-torsion. Proof uses symmetric signatures over R, the Novikov conjecture, and a cobordism argument comparing [Y] to [M] in group homology.

**Root causes (ranked by severity)**:

1. **Model: Fabricated surgery argument (CRITICAL)**. Our Part (b) claims to prove surgery realization: "Kill H_2 by surgery on embedded 2-spheres (below middle dimension, no obstruction in dim 5)." This argument is FALSE for groups with torsion. The error: surgery below the middle dimension CAN change pi_1 when the fundamental group has torsion, and the surgery obstruction groups L_*(Q Gamma) are non-trivial for groups with torsion. The model generated a plausible-sounding but mathematically wrong proof.

2. **Model: Ignored known obstructions (CRITICAL)**. The external comments are devastating: "All proofs by AI's I've seen only use finite complex and Poincaré duality. However, Fowler's paper shows that... the product M^3 x (K\G/Gamma_0 x E Delta)/Delta... has the rational type of a finite complex, and satisfies Rational Poincaré duality. It has fundamental group pi_1(M^3) x Gamma... This shows that all such proofs must fail." The model's proof is EXACTLY the type that Weinberger says "must fail."

3. **Model: False intermediate lemma**. The comments specifically identify: "Theorem 4 and Lemma 5 are false. The counterexample is R^1 and f is a translation." Our proof likely contains an equivalent false intermediate result.

4. **Agent: Self-review loop again**. G6 was "self-review" that initially flagged a "surgery gap" but then "closed" it with the same flawed argument. The fix was: "A self-contained surgery proof was found." But the "fix" introduced the same error in a different disguise.

5. **Time/budget constraint (SEVERE)**. Only ~6 messages were used for P07 — the least of any submitted problem. The problem was initially PARKED, then "solved" in a single escalation session (E2-E4). A problem requiring deep surgery theory expertise cannot be reliably solved in 6 messages.

6. **Workflow: No disproof attempt**. Despite the truth mode being 50/50, the agent never seriously attempted the NO direction (Route B: cohomological obstruction). All effort went into the YES construction.

**External commentary match**: "Some proofs try to use 'multiplicativity of Euler characteristic in finite covers'. This is false for infinite complexes with finitely generated homology over Q." Our proof doesn't use this specific error, but uses an equally invalid surgery argument.

**Fault allocation**: 50% model (fabricated proof), 20% agent (self-review), 20% time (6 messages), 10% workflow (no disproof attempt).

---

### P08: We said NO, external says YES

**Our claim**: NO — the polyhedral Lagrangian octahedron (K ~ S^2) is a counterexample. Any topology-preserving smoothing would produce a smooth exact Lagrangian S^2, contradicting Gromov's theorem.

**External answer (Mohammed Abouzaid)**: YES — smoothing exists. Proof via conormal fibrations (Lemmas 1-8), smoothing functions (partition of unity), Weinstein tubular neighborhood theorem. The smooth Lagrangians are constructed as graphs of closed 1-forms in the conormal fibration.

**Root causes (ranked by severity)**:

1. **Model: Constructed a counterexample that may contradict established mathematics (CRITICAL)**. Our octahedron is a polyhedral Lagrangian S^2 with 4-valent vertices in R^4. If valid AND if Abouzaid's proposition is correct, then there would exist a smooth exact Lagrangian S^2 in R^4, contradicting Gromov. The resolution is likely:
   - Our octahedron has a subtle embedding failure (self-intersection in R^4) that our numerical check missed, OR
   - Abouzaid's smoothing does not actually preserve the S^2 topology (despite the statement saying "topological isotopy"), OR
   - There is a geometric constraint we violated (e.g., the octahedron's link at each vertex may not satisfy Abouzaid's Lemma 1 conditions).

2. **Agent: Quick counterexample bias**. We spent only ~10 messages on P08 and immediately went for a counterexample (Route C: obstruction search). Finding a clean counterexample + invoking Gromov felt elegant and complete. We never attempted the YES direction (constructing a smoothing).

3. **Agent: Failed to apply the "trivial problem" test**. If the answer were NO via such a simple argument (Gromov + S^2 topology), the problem would be trivially solvable and not worthy of a competition question authored by a leading symplectic topologist. This should have been a red flag suggesting our approach was wrong.

4. **Workflow: No engagement with the problem's mathematical framework**. Abouzaid's solution uses conormal fibrations, smoothing functions, partition of unity, and Weinstein neighborhoods — the core tools of symplectic geometry. We never engaged with any of these. Instead, we used a topological obstruction (Gromov) that bypasses the entire framework.

5. **Tooling: Numerical verification was insufficient**. Our EXP-1 checked Lagrangian conditions and non-intersection of faces. But checking non-intersection of 2D surfaces in R^4 via a simple pairwise face test may miss subtle intersections or near-intersections that affect the topology.

**External commentary match**: "The best two solutions produced during testing both correctly identified the existence of a local smoothing near every vertex... The proof then proceeds to perform a local-to-global gluing argument. It was a priori clear that there must be a gap in this argument." The AI solutions that attempted YES were on the right track but had gluing gaps. Our approach (going for NO) was the outlier.

**Fault allocation**: 40% model (invalid counterexample), 25% agent (counterexample bias, no trivial-problem check), 20% workflow (no framework engagement), 15% time (10 messages).

---

### P03: Partial mismatch (we proved n <= 4, external proved all n)

**Our claim**: YES for n <= 4 (proved). YES for n >= 5 (conditional on Symmetry Conjecture, verified to 48+ digits).

**External answer (Ben Dali, Williams)**: YES for all n. Constructs the "interpolation t-Push TASEP" — a Markov chain with explicitly defined multi-step transition probabilities involving signed two-line queues. Complete proof using combinatorial weight decomposition.

**Root causes**:

1. **Methodology gap**: The external solution uses a DIFFERENT Markov chain than ours (interpolation t-Push TASEP vs ASEP with rates (t,1)). The external chain has more complex transitions (multi-step: bell-ringing, clockwise travel, push dynamics) but the combinatorial framework makes it tractable for all n. We identified a correct but simpler chain and couldn't prove it works universally.

2. **Computational limitation**: Our degree-bound + interpolation approach for proving the Symmetry Conjecture scales as O(n^n). At n=5, the system is ~11K x 11K, computationally infeasible within the sprint timeframe.

3. **Missing combinatorial insight**: The two-line queue framework (from prior work: CMW22, BDW25) provides the key algebraic machinery. We never discovered this connection.

**Fault allocation**: 40% model (missed combinatorial framework), 30% tooling (computational limits), 30% time.

---

### P04: Partial mismatch (we proved n <= 4, external proved all n)

**Our claim**: YES for n <= 4 (proved). YES for n >= 5 (conjectured, strongly supported by numerical evidence).

**External answer (Garza Vargas, Srivastava, Stier)**: YES for all n. Elegant 6-page proof using the Blachman approach: score vectors as derivatives under the heat flow, Jacobian analysis of the free convolution map, Hessian convexity via Bauschke-et-al's theorem on hyperbolic polynomials.

**Root causes**:

1. **Methodology gap (CRITICAL)**: The external solution uses the Blachman approach — well-known in classical information theory for the Shannon-Stam inequality. The key insight (score vectors as derivatives, Jacobian contraction) makes the proof short and elegant. We NEVER tried this approach, despite the problem being explicitly titled "Stam inequality."

2. **Bottom-up vs top-down**: We went bottom-up (compute Phi_n explicitly for n=2,3,4 and try to prove the inequality directly), consuming ~977K tokens. The external solution goes top-down (abstract the classical proof technique and verify the analogous steps). The top-down approach is vastly more efficient.

3. **Scout failure**: None of our scout models (GPT-Pro, Kimi, DeepSeek-R1, Qwen) found the correct approach. The comments packet reveals ChatGPT Pro 5.2 DID try the Blachman approach but got the details wrong. The approach was discoverable but incorrectly executed by all tested AI systems.

4. **High resource concentration**: P04 consumed the most resources of any lane (~142 messages, ~3.4M estimated compute tokens, ~$133). Most effort went into n=4 SOS certification — valuable for that lane, but not directly transferable to all-`n` closure.

**Fault allocation**: 50% model (missed Blachman connection despite "Stam" in problem name), 25% workflow (bottom-up instead of top-down), 15% time (but we actually spent the MOST time here), 10% scout limitation.

---

### P05: Directionally aligned, internal consistency issues

**Our claim**: Full biconditional characterization proved (11 theorems, Thm 10 closes the "if" direction for all G and all O).

**External answer (Blumberg)**: Characterization by geometric fixed-point connectivity.

**Status**: Directionally aligned (grade B). The mathematical content appears to match, but the answer.md contains numerous superseded status statements ("open," "frontier," "blocked") from the chronological development. A historical note at line 7 explains this, but the document reads as internally contradictory.

**Root cause**: Pure documentation issue. The answer was written incrementally over 21 sessions and accumulated status language from each session. Needs editorial cleanup, not mathematical correction.

---

### P02, P09, P10: Aligned (grade A)

These three problems are strongly aligned with external solutions:
- **P02**: Both prove YES (fixed W, then V). High-level theorem target matches.
- **P09**: Both prove YES (polynomial relations exist). Comments say the best LLM answer was "essentially correct."
- **P10**: Both construct matrix-free iterative methods. Comments say the best LLM answer was "correct and better than the solution I provided."

P09 and P10 received the strongest external validation. P10 was the only problem where the AI solution was BETTER than the human solution.

---

## Part II: Cross-Cutting Failure Invariants

### Invariant 1: Initial Direction Bias (affects P01, P07, P08)

Three of the four sign-conflict problems show a pattern: the model formed an initial directional hypothesis and never reversed it, even when evidence mounted against it.

| Problem | Initial lean | Final answer | Correct answer | Bias reversal attempted? |
|---------|-------------|-------------|----------------|-------------------------|
| P01 | 70% YES | YES | NO | Never — 7 failed approaches, still committed to YES |
| P07 | 50/50 | YES | NO | Never — only YES direction explored seriously |
| P08 | 50/50 | NO | YES | Never — counterexample found quickly, no YES attempt |

**Structural cause**: The agent architecture has no mechanism for systematically exploring BOTH directions of a binary question. Once a direction shows initial promise, confirmation bias takes over. The "truth mode" assessment (G0) should have been a living hypothesis, updated after each session, not a fixed prior.

### Invariant 2: Self-Review Is Not Adversarial (affects P01, P07)

Both P01 and P07 had "self-review" G6 gates (Claude reviewing Claude). In both cases, the self-review ACCEPTED proofs that are mathematically wrong. The self-review consistently found superficial issues (notation, edge cases) while missing fundamental logical errors.

Contrast with problems where EXTERNAL Codex review was used:
- P06: Codex found 3 red flags (boundary, case split, overclaim) — all real issues
- P08: Codex found 2 MAJOR issues (regularity gap, definition mismatch) — both real

External review was effective at finding issues; self-review was not. But even external review didn't catch sign errors — Codex reviewed the proof internals, not whether the answer direction was correct.

### Invariant 3: Counterexample Construction Without Verification Against Expert Expectations (affects P06, P08)

Both P06 and P08 constructed counterexamples to disprove claims that the problem authors expected to be true. In both cases, the "counterexample" appeared rigorous on its face but conflicted with expert-authored solutions.

**Missing check**: Before submitting a counterexample that contradicts the expected answer direction, the agent should have asked: "If this counterexample is correct, would the problem be trivially solvable? If so, why would an expert pose it as a competition problem?"

### Invariant 4: Methodology Lock-In (affects P03, P04)

Both P03 and P04 show the agent committing to a bottom-up algebraic methodology early and never pivoting to the correct top-down approach.

| Problem | Our approach | External approach | Discovery difficulty |
|---------|-------------|------------------|---------------------|
| P03 | Degree-bound + interpolation | Two-line queue combinatorics | Required knowing BDW25 |
| P04 | Explicit Phi_n computation + SOS | Blachman score-vector method | Required connecting "Stam" to Blachman (1965) |

The external approaches required specific mathematical connections (BDW25 paper, Blachman's classical proof). These were not in the model's training data or discoverable via web search within the sprint timeline. However, for P04, the problem is literally called "Stam inequality" and the Blachman approach to the classical Stam inequality is well-known. The model should have explored this connection.

### Invariant 5: Budget Mis-Allocation

| Problem | Messages used | Outcome | Correct? |
|---------|-------------|---------|----------|
| P04 | ~142 | Submitted (n<=4 + computational n=4 certification) | Partial vs external-all-n |
| P03 | ~83 | Candidate (n<=4) | Partial |
| P05 | ~57 | Submitted (full) | Likely correct |
| P01 | ~20 | Submitted (YES) | WRONG |
| P09 | ~58 | Submitted (YES) | Correct |
| P10 | ~12 | Submitted | Correct |
| P06 | ~14 | Submitted (NO) | Disputed |
| P08 | ~10 | Submitted (NO) | WRONG |
| P07 | ~6 | Submitted (YES) | WRONG |
| P02 | ~12 | Submitted (YES) | Correct |

P04 and P03 jointly consumed the largest share of effort and ended as partial-vs-external closures. Meanwhile, P07 and P08 were given minimal budgets (6 and 10 messages) and both landed on wrong-sign outcomes. This suggests under-allocation to high-risk sign lanes and over-allocation to technically deep but low-polarity-risk lanes.

**Optimal reallocation signal**: Once P04 entered solver-friction loops, part of that budget should have been diverted to sign-validation audits on P01/P06/P07/P08.

---

## Part III: Fault Attribution Matrix

| Factor | Weight | Problems affected | Description |
|--------|--------|------------------|-------------|
| **Agent design** | 35% | P01, P06, P07, P08 | Failed at its core job: catching model errors. Self-review echo chamber, no direction reversal, no opposition pass, no "trivial problem" check, budget mis-allocation |
| **Operator oversight** | 20% | ALL | Set sprint parameters that forced speed over depth; didn't spot-check answer signs; didn't intervene on budget allocation; trusted agent's "Submitted" status without independent verification; didn't require red-team pass |
| **Model capability** | 15% | P01, P04, P07 | Fabricated proofs (P07), misapplied results (P01), missed key connections (P04) — but model errors are EXPECTED; the agent and operator exist to catch them |
| **Methodology/workflow** | 15% | P03, P04, P06, P08 | Bottom-up vs top-down, no framework engagement, counterexample bias |
| **Time/budget** | 10% | P07, P08, P03 | Insufficient messages for hard problems, over-allocation to P04 — but budget was jointly the agent's and operator's to allocate |
| **Tooling** | 5% | P03, P04 | Computational limits (11K x 11K systems), SDP solver wrestling |

### Who's Fault?

**It's a shared failure across three layers — agent, operator, and model — but the agent and operator bear the most responsibility because their entire purpose is to catch model errors.**

The model producing wrong mathematical reasoning is expected behavior. LLMs generate plausible-but-wrong proofs routinely. That's why the agent architecture (gates, reviews, escalation) and the human operator exist: to be the CHECK on the model. When neither the agent nor the operator pushed back, the errors went straight to submission.

1. **Agent design** (35%): The agent's job is to be skeptical of the model's output, and it failed at this core function across all 4 sign-conflict problems:
   - **No opposition pass**: The agent never required the model to seriously attempt the opposite direction before committing. In P01, after 7 failed YES approaches, the agent should have FORCED a NO exploration. It didn't.
   - **Self-review accepted without challenge**: In P01 and P07, the agent ran self-review (Claude reviewing Claude) instead of demanding external adversarial review. Self-review consistently rubber-stamped the model's reasoning.
   - **No "trivial problem" sanity check**: In P08, the agent accepted a counterexample that would make a competition problem trivially solvable. The agent should have flagged: "If this is correct, why would an expert symplectic topologist pose it?"
   - **Budget mis-allocation unchallenged**: The agent let P04 consume 142 messages while allocating 6 to P07. It should have recognized diminishing returns and reallocated.
   - **No direction-reversal trigger**: The agent had no mechanism to flip the model's hypothesis when evidence mounted against it. Seven failed approaches in one direction (P01) should have triggered a mandatory direction switch.

2. **Operator oversight** (20%): The human operator is the last line of defense and also failed to catch the errors:
   - **No independent sign verification**: The operator accepted "Submitted" status without independently checking whether the YES/NO direction was even plausible. A 5-minute sanity check per problem ("Does this direction make sense given what I know about the problem author's expertise?") could have flagged P07 and P08.
   - **Sprint parameters forced speed over depth**: 10 research-level problems in 4 days with ~$400 budget made depth impossible. The operator set these constraints knowing they would force shortcuts.
   - **No budget intervention**: The operator watched P04 consume the majority of messages without redirecting resources to underserved problems (P07: 6 messages, P08: 10 messages).
   - **No red-team requirement**: The operator didn't build a mandatory "try to disprove your own answer" pass into the workflow. This is an operator design decision, not an agent limitation.
   - **Trusted the gate system**: The G0-G7 gates were designed to catch proof-level errors, but the operator never asked: "Do these gates actually catch DIRECTION errors?" They don't — and the operator should have recognized this gap.

3. **Model capability** (15%): The model produced wrong proofs — this is expected and the least actionable factor. The specific errors (Wick power confusion in P01, fabricated surgery in P07, invalid counterexample in P08) are the kind of mistakes that adversarial review is designed to catch. The model's errors are the INPUT to the system; the agent's and operator's failure to detect them is the OUTPUT failure.

4. **Workflow** (15%): The sprint's "submit early, submit often" culture incentivized committing to a direction quickly rather than spending time verifying the direction first. Problems like P08 were "solved" in 10 messages because the counterexample seemed clean. A workflow that required explicit consideration of both directions before committing would have caught some errors.

5. **Time** (10%): The 4-day sprint was insufficient for 10 research-level problems, but time allocation was itself a joint agent/operator decision. More time would not have helped without better skepticism — P01 received 20 messages and was still wrong because nobody challenged the direction.

6. **Tooling** (5%): Computational limits blocked P03 n>=5 closure. SDP solver issues consumed sessions of P04 time. But these are partial-closure problems, not sign errors.

---

## Part IV: Recommendations

### R1: Mandatory Bidirectional Exploration
For every binary (YES/NO) problem, require the agent to spend at least 30% of its budget exploring the LESS-favored direction before committing. Specifically:
- If leaning YES: construct a candidate distinguishing event/counterexample for NO
- If leaning NO: attempt a proof of YES using standard techniques
- Only commit to a direction after both have been explored

### R2: External Adversarial Review for All Submissions
Self-review (Claude reviewing Claude) must be replaced by EXTERNAL adversarial review for all submitted answers. The G6 gate should be mandatory-external, not optional.

### R3: "Trivial Problem" Test for Counterexamples
Before submitting a counterexample that makes a competition problem trivially solvable, explicitly check: "Is this counterexample so simple that the problem author would have noticed it?" If yes, re-examine the counterexample's validity.

### R4: Budget Caps Per Problem
No single problem should consume more than 25% of the total budget. Implement hard caps with mandatory pivot-or-park decisions at budget thresholds.

### R5: Methodology Diversity
For each problem, generate at least 3 distinct proof strategies before committing to one. Use scouts specifically for strategy discovery, not just for verification.

### R6: Living Truth Mode
The G0 truth-mode assessment should be updated after each session based on evidence accumulated. If 5+ approaches fail in one direction, the truth-mode probability should shift significantly toward the other direction.

---

## Appendix: External Commentary Crosswalk

| Problem | External comment on AI solutions | Our failure mode |
|---------|--------------------------------|-----------------|
| P01 | "LLM quotes unpublished note as proof; takes wrong premise (Phi43 ~ GFF)" | Same class: assumed interaction "soft enough" to preserve quasi-invariance |
| P02 | "LLM constructed W depending on pi (wrong)" | We avoided this error |
| P03 | "Metropolis-Hastings trivial construction" | We avoided this error (found ASEP chain) |
| P04 | "ChatGPT tried Blachman but got score function wrong" | We never tried Blachman at all |
| P05 | "Details sketched or slightly garbled" | Our details may have similar issues |
| P06 | "ChatGPT couldn't answer; offered upper bound of 1/2" | We gave an answer (NO) but it may be disputed |
| P07 | "Theorem 4/Lemma 5 are false; counterexample: R^1" | Our surgery argument contains equivalent false lemma |
| P08 | "Local smoothing correct; local-to-global gluing gap" | We went the wrong direction entirely (NO instead of YES) |
| P09 | "Essentially correct answer" | Our answer is correct |
| P10 | "Correct and better than human solution" | Our answer is correct |

The external comments show that ALL tested AI systems struggle with the same problems (P01, P04, P07, P08). The failure modes are consistent across model families, suggesting these are fundamental limitations of current LLM mathematical reasoning rather than implementation-specific issues.

---

## Part V: Retry and Logging Forensics (What should have been retried earlier)

This section answers: when did we fail, what should have been retried, and what should have been logged more clearly for later diagnosis.

| Lane | Event window | What failed | What should have been retried | Logging gap |
|---|---|---|---|---|
| P04 | Session 25 -> 26 | "Solver-limited" diagnosis from cvxpy behavior was wrong | Direct sparse API runs (SCS/CLARABEL) should have been retried immediately after first cvxpy stall | Need mandatory "frontend vs solver" benchmark log before declaring tooling infeasible |
| P03 | After n=4 closure milestone | n=5 left as infeasible in-sprint though parallel route was known | Launch cloud-parallel pilot (5-10 t-values) as soon as n=4 pipeline stabilized | Need explicit "deferred compute launch" decision record with timestamped reasons |
| P08 | External review reject -> patch | Definition mismatch was patched by tightening definition | Re-run both directions under locked original definition before status upgrade | Need definition-change control block in audit for every semantic change |
| P06 | Initial formalization | Potential quantifier mismatch vs external interpretation | Re-formalize quantifiers with lock + independent reviewer pass before proof route | Need mandatory quantifier-normal-form artifact (`statement_lock.md`) |
| P05 | Final packaging | Chronological sections left stale status lines in final artifact | Final normalization pass should have been rerun after each major merge | Need scripted final-form lint gate prior to release |

### Failure-analysis logging quality issues

1. Route failures were logged, but the "retry decision rationale" was often implicit.
2. Tool failures lacked a two-layer diagnosis (frontend compile vs backend solver).
3. Definition mutations were documented narratively, not as controlled semantic deltas.
4. Closure claims were not always paired with a contradiction checklist artifact.

---

## Part VI: More Time/Tooling Counterfactual and Theoretical Best

### What likely improves with more time and tooling

1. `P03`: materially improvable by parallel compute execution (known embarrassingly parallel path).
2. `P04`: already improved once tooling diagnosis was corrected; more time would likely improve formalization of the continuity gap.
3. Sign-conflict lanes (`P01/P07/P08`): extra time helps only if paired with stronger contradiction controls; extra time alone does not guarantee reversal.

### Counterfactual outcome bands (under same premise constraints)

- **Observed**: strict alignment `3/10`, directional `6/10`.
- **With full time + existing stack only**: likely strict `5-7/10`, directional `7-9/10`.
- **With full time + new checks/balances (statement lock + contradiction gate + opposition pass)**: likely strict `6-8/10`, directional `8-9/10`.
- **Practical ceiling in this run architecture**: about `8/10` strict, with `P03` and one sign-critical lane remaining uncertain.

### Theoretical best (upper bound estimate)

If all premise-safe controls were in place from day 1, parallel compute was launched on schedule, and all disputed sign lanes were adjudicated correctly, a `9/10` strict-alignment outcome was plausible. A true `10/10` required one additional favorable event: either full P03 closure in-window or perfect sign adjudication on every disputed lane.

---

## Part VII: Technical Debt from Wrong Answers

Wrong-sign submissions create debt beyond correctness:

| Debt type | Description | Lanes | Estimated remediation effort |
|---|---|---|---:|
| Semantic debt | Statement/quantifier/definition contracts not frozen | P06, P07, P08 | 20-40 hours |
| Proof debt | Deep proof-route replacement after polarity reversal | P01, P07, P08 | 80-160 hours |
| Validation debt | Rebuilding contradiction checks and dual-route reviews | P01, P06, P07, P08 | 30-60 hours |
| Documentation debt | Status conflicts and stale narrative cleanup | P05 (and cross-doc references) | 10-25 hours |
| Governance debt | New gates, templates, and enforcement integration | Portfolio-wide | 15-30 hours |

**Total estimated debt from wrong/contested lanes**: roughly `155-315 hours` of focused follow-up work.

---

## Part VIII: Is the Workflow Worth the Cost? (ROI and Time Saved)

### Direct sprint cost

- Compute/API spend: approximately `$400`.
- Human operator time: comparatively low and mostly logistical.

### Counterfactual from-scratch baseline

For 10 heterogeneous research problems, producing the same volume of artifacts (formalizations, experiments, audits, transcripts, route maps) from scratch without the workflow likely requires several hundred expert hours.

### Estimated net effect

- **Speedup for first-pass research triage and artifact production**: substantial (roughly `3x-8x` depending on baseline assumptions).
- **Penalty from correction debt on wrong-sign lanes**: meaningful (`155-315` hours estimated).
- **Net**: still positive for rapid exploration and structured evidence generation, but only if contradiction controls prevent expensive wrong-sign closures.

Conclusion: the workflow is worth the effort for discovery and triage, but value collapses without stronger polarity/statement controls.

---

## Part IX: Disputed External Answer (Claude Code dispute)

One disputed lane is `P06`. The dispute is likely a quantifier-form mismatch, not necessarily a pure mathematical contradiction.

### Competing forms

- Form A: `exists c>0` independent of `alpha` (strong form).
- Form B: bound scales with `alpha` (e.g., `|S| >= alpha*n/C`) (weaker form).

These are not equivalent. A proof of Form B does not prove Form A.

### Required adjudication protocol

1. Freeze canonical quantifiers in `statement_lock.md`.
2. Prove/disprove only that frozen statement.
3. Add a reconciliation note if external solution addresses a different quantifier form.
4. Mark lane as `DISPUTED_QUANTIFIER_FORM` until adjudicated.

This can be done without violating the premise (no human math injection, no direct-solution dependence), because it is a logic/statement-governance step.

---

## Part X: Systems-Level Improvements and Fine-Tuning Paths

### A. Systems-level improvements (process)

1. Mandatory statement lock at G0.
2. Mandatory contradiction gate before `✅`.
3. Mandatory opposition pass for binary-sign problems.
4. Mandatory final-form normalization lint.
5. Mandatory frontend-vs-backend solver diagnostics before tooling infeasibility claims.
6. Budget controller that reallocates when marginal closure probability drops.

### B. Training and adaptation methods (out of sprint scope, high leverage)

To populate related-lemma capability without violating run-time premise constraints, use offline training on adjacent theorem corpora:

1. **Supervised fine-tuning (SFT)** on structured proof traces:
   - theorem statement
   - lemma DAG
   - proof skeleton
   - failure labels

2. **Preference optimization** (DPO/ORPO-like) on reviewer outcomes:
   - prefer proofs that pass contradiction gates
   - penalize proofs with statement drift or polarity conflict

3. **Process reward models (PRM)**:
   - step-level scoring for quantifier correctness, citation validity, and closure integrity

4. **Tool-use trajectory fine-tuning**:
   - train on successful solver diagnosis traces (frontend vs backend)
   - train on compute-planning traces (when to parallelize)

5. **Synthetic lemma curriculum generation**:
   - perturb known lemmas into near-miss variants
   - label as valid/invalid with machine checks
   - improve discrimination at the "almost right but wrong" boundary

6. **Hard-negative replay from this repo**:
   - use failed lanes (wrong sign, stale status, drift) as explicit anti-pattern data

### C. Expected effect of training improvements

These methods are most likely to reduce:

- quantifier/polarity errors,
- citation-extension overreach,
- false closure under partial evidence,
- repeated toolchain misdiagnosis.

They are less likely to fully solve deep novel-invariant discovery (e.g., hardest remaining frontier-type gaps), but they should materially improve correctness and calibration.

---

## Part XI: Throughput Accelerators, Closure-Cost Model, and Upgrade Economics

This section consolidates the operational conclusion of the post-mortem: in this run, the dominant residual error was a **harness/orchestration problem** (control-plane quality), not a pure "model cannot reason" condition.

### XI.A Closure-cost model (portfolio level)

Let

- `S` = number of lanes closed at theorem level,
- `T` = operational throughput (closure-grade artifacts per unit time),
- `C_setup` = fixed setup cost (runbook, templates, tooling),
- `C_exec` = lane execution cost (tokens/compute + operator effort),
- `C_debt` = correction debt from wrong-sign or drifted submissions.

Then a practical budget model is:

`C_total = C_setup + C_exec + C_debt`.

Empirically, `C_debt` is the principal destabilizer once wrong-sign closure enters the system. This explains why contradiction controls have unusually high ROI: they reduce the highest-variance term in the cost model.

### XI.B Throughput accelerators and expected effect

| Accelerator | Mechanism | Throughput effect | Strict-accuracy effect | Cost profile |
|---|---|---:|---:|---|
| Statement lock (`G0`) | Freezes quantifiers/definitions before route search | +10% to +25% | +10 to +20 pts | Very low (policy + template) |
| Contradiction gate (`G6/G7`) | Blocks closure unless opposite-sign challenge is cleared | +0% to +10% | +10 to +20 pts | Low (checklist + reviewer time) |
| Independent opposition pass | Forces explicit disproof/proof of opposite polarity | -5% to +10% | +10 to +25 pts | Low-medium |
| Final-form normalization lint | Prevents stale mixed-status merges | +5% to +15% | +0 to +5 pts | Very low (scripted) |
| Solver preflight diagnostics | Separates frontend bottlenecks from solver limits | +10% to +30% on compute lanes | +0 to +10 pts | Low-medium |
| Parallel compute scheduler | Auto-scales embarrassingly parallel sweeps | +20% to +200% on targeted lanes | +0 to +10 pts | Medium (cloud + orchestration) |
| Curated lemma/first-principles retrieval layer | Reduces theorem-selection drift | +20% to +100% | +10 to +30 pts | Medium-high (corpus curation) |
| Verifier-tuned training loop (offline) | Process-level calibration on proof failures | +10% to +50% | +10 to +30 pts | High (training program) |

Interpretation: accuracy gains are driven mostly by control-plane safeguards, while large throughput gains come from compute scheduling and curated retrieval.

### XI.C Upgrade economics toward a reliable high-throughput research accelerator

Order-of-magnitude estimates (portfolio scale):

| Upgrade package | Scope | One-time engineering cost | Run-time cost | Expected performance band |
|---|---|---:|---:|---|
| Package A: Governance hardening | Statement lock + contradiction gate + opposition pass + normalization lint | ~40-120 hours | Negligible | Strict alignment uplift: +10 to +30 pts |
| Package B: Compute orchestration | Solver preflight + parallel scheduler + automatic retry policy | ~80-200 hours | ~$300-$3,000 per heavy run | Throughput uplift on hard lanes: +20% to +200% |
| Package C: Corpus-enhanced accelerator | Curated lemma retrieval + failure replay + process scoring | ~200-600 hours | ~$1,000-$10,000/month (ops/inference) | Throughput: ~10x-30x over unaided baseline; strict closure: ~3x-10x |
| Package D: Training-enhanced system (out of sprint scope) | SFT + preference/process optimization + tool-use tuning | ~300-1,200 hours + training budget | Scenario dependent | Throughput: ~20x-50x possible in scoped domains; strict closure: ~5x-15x |

These estimates are scenario-dependent and should be treated as planning ranges, not guaranteed outcomes.

### XI.D Marginal closure cost near frontier

Observed pattern: the first set of lanes closes at low marginal cost, while the final one or two lanes absorb disproportionate effort. This is consistent with superlinear marginal closure cost:

`m_k = C(close lane k | k unresolved lanes remain)` increasing as `k -> 1`.

Operational consequence: budget and schedule policy must optimize for **expected portfolio value**, not "all lanes to closure at any cost."

### XI.E Practical conclusion

Within the autonomy premise, the main bottleneck is best characterized as **agent/model harnessing and orchestration optimization**:

1. Control-plane rigor determines correctness stability.
2. Compute and solver orchestration determine closure speed on heavy lanes.
3. Model capability matters, but gains are amplified or suppressed by pipeline quality.

Accordingly, the highest-ROI strategy is: deploy Package A immediately, Package B for compute-heavy lanes, and Package C as the medium-term architecture target.

---

## Part XII: Minimum Viable Operator Review

A careful operator review — requiring no deep mathematical expertise — would have caught 3 of 4 sign conflicts in approximately 30 minutes total.

### The protocol (per submitted problem)

1. Read the 1-line answer (YES/NO).
2. Ask: "Does this direction feel too easy for a research competition?"
3. Ask: "Did the agent try the opposite direction seriously?"
4. For any problem where the agent flipped direction, demand the exact moment of the flip and what evidence drove it.

### Per-problem application

| Problem | Check | Catch? | Effort |
|---------|-------|--------|--------|
| P07 | Agent flagged "surgery gap" in G6, then "closed" it with same flawed argument. Ask: "You flagged this gap, then closed it with no new evidence — show me the actual construction." | YES — forces honest downgrade or real fix | 5 min |
| P08 | Problem authored by Abouzaid (Fields-adjacent symplectologist). Ask: "Would a world expert pose a question whose answer is a 3-step argument using only Gromov 1985?" | YES — triggers deeper investigation | 5 min |
| P01 | 7 failed approaches before "breakthrough" on attempt 8. Ask: "7 failures followed by a breakthrough — is the breakthrough real or did we lower our standards?" | LIKELY — reviewing BG extension requires some effort, but the pattern is a red flag | 10 min |
| P06 | Genuinely disputed quantifier interpretation. Operator review would be inconclusive — which is correct (should stay Candidate, not Submitted). | AMBIGUOUS — correct outcome is to flag, not resolve | 5 min |

**Result**: 3 of 4 sign conflicts caught or flagged, ~25-30 minutes total. The review doesn't require the operator to do math — only to ask skeptical questions about the agent's own process.

---

## Part XIII: MCP Servers and Custom Agent Architecture

### MCP servers: specific impact mapping

**1. Formal verifier MCP (Lean4/Coq wrapper)**

Single highest-ROI tool not available during the sprint. A server that takes a proof sketch and attempts to formalize the key lemma would have caught:

- **P07**: Surgery realization claim fails to typecheck. Lean's `sorry` flags exactly where the fabrication sits.
- **P01**: Wick power Young's inequality claim requires a proof term that doesn't exist in 3D. Formalization stalls at the critical step.
- **P08**: Less clear — the counterexample construction is computationally valid (EXP-1/EXP-2 pass), but the *interpretation* error (valid octahedron, wrong conclusion) may not be caught by a verifier.

Build cost: ~40-80 hours. Expected catch rate on fabricated proofs: high.

**2. Literature retrieval MCP (arXiv/MathSciNet/zbMATH)**

Authenticated access to mathematical databases with semantic search:

- **P04**: "Stam inequality" + "finite convolution" retrieves Blachman (1965) and Bauschke et al. (2001). The 6-page external proof becomes reproducible. Saves ~130 messages.
- **P01**: "quasi-invariance" + "Phi^4_3" retrieves BDW25 results showing mutual singularity (correct answer: NO).
- **P03**: Surfaces Williams interpolation/t-Push TASEP framework as a competing approach.

Build cost: ~20-40 hours. Impact: likely flips P04 from partial to complete, possibly flips P01 direction.

**3. Contradiction oracle MCP**

Takes proposed answer (YES/NO), runs a second model instance with instruction "prove the opposite":

- **P07**: "Prove NO lattice with 2-torsion exists in SO(5,1)" — second model likely finds the R^1 counterexample.
- **P08**: "Prove smoothing DOES exist" — forces engagement with conormal fibration framework.

Build cost: ~20-40 hours (prompt wrapper + model call). Impact: catches 1-2 sign conflicts.

### Custom fine-tuned models

| Model type | Training data | Build cost | Expected impact |
|-----------|--------------|-----------|----------------|
| Direction prediction | ~10K competition problems with known YES/NO | 100-200 hrs | Flags low-confidence directions before proof attempt |
| Process reward model (PRM) | Correct vs incorrect proof traces, step-level | 200-500 hrs | Scores P07 surgery step as "unsupported", P01 BG extension as "unverified" |
| Theorem retrieval embedding | ~100K theorems, structured by concept | 200-400 hrs | Matches "Stam inequality" → "Blachman approach" without explicit search |

### Combined architecture impact estimate

| Tool combination | Build cost | Problems likely flipped | Expected strict alignment |
|-----------------|-----------|------------------------|--------------------------|
| 3 MCP servers only (verifier + retrieval + contradiction) | 80-160 hrs | P04 (complete), P07 (flip), possibly P01/P08 | 5-6/10 |
| MCP servers + fine-tuned models | 500-1500 hrs | Above + better P01/P03 orientation | 6-8/10 |
| Full stack + governance (Package A+C+D) | 700-2000 hrs | All of above + sign-conflict prevention | 7-9/10 |

---

## Part XIV: Cold Start vs Lemma Database vs Lemma-Trained Model

### The enabling lemma map

Every external solution depends on a critical connection that bridges problem statement to proof:

| Problem | Enabling connection | Source | Published? | In standard corpus? |
|---------|-------------------|--------|-----------|---------------------|
| P01 | BDW25 mutual singularity | Barashkov-De Vecchi-Worn (2025) | Preprint | No |
| P03 | t-Push TASEP / interpolation polynomials | Williams (2026, this competition) | Novel | No |
| P04 | Blachman score-vector technique | Blachman (1965), Bauschke et al. (2001) | Yes, 60 years old | **Yes** |
| P07 | Surgery impossibility for groups with torsion | Weinberger + classical surgery theory | Yes | Specialized |
| P08 | Conormal fibrations for polyhedral Lagrangians | Abouzaid (2026, this competition) | Novel | No |

### Three tiers of discoverability

**Tier 1 — Standard corpus** (P04): Blachman (1965) and Bauschke et al. (2001) are in any reasonable mathematical database. A retrieval system indexing "Stam inequality" → "Blachman approach" → "score function contraction" finds this in seconds. Clearest case where a lemma database changes outcome from partial to complete.

**Tier 2 — Specialized corpus** (P07): Surgery-theoretic obstructions for groups with torsion are published. A research-level topology corpus surfaces "surgery realization fails for groups with torsion" when queried appropriately.

**Tier 3 — Novel techniques** (P01 preprint, P03 novel construction, P08 novel technique): No database or fine-tuned model contains these because they didn't exist before the competition. This is the hard ceiling of any retrieval-based approach.

### Starting condition comparison

| Condition | Build cost | Expected strict alignment | Key wins | Hard ceiling |
|-----------|-----------|--------------------------|----------|-------------|
| Cold start (actual run) | 0 | 3/10 | P02, P09, P10 | Everything else |
| Warm start (database + retrieval MCP) | 200-600 hrs | 5-7/10 | + P04 (full), P07 (flip) | P01 preprint, P03/P08 novel |
| Hot start (fine-tuned model) | 500-1500 hrs | 6-8/10 | + better P01/P03 orientation | P08 novel technique |
| Hot start + governance (Package A+C) | 700-2000 hrs | 7-9/10 | + sign-conflict prevention | P03 full, P08 novel |

### The irreducible gap

The Tier 3 problems (novel techniques by problem authors/competitors) represent 1-2 problems per 10. No retrieval system or fine-tuned model solves them because the techniques are genuinely new. This is the boundary between "research acceleration" and "research replacement."

A well-trained model could get *closer* — recognizing "this problem has the shape of a conormal bundle problem" without knowing Abouzaid's specific technique — but closing the gap requires genuine mathematical creativity that no current system reliably produces.

### Highest-leverage single intervention

The warm-start lemma database is the single highest-ROI intervention:
- Cheaper than fine-tuning (200-600 hrs vs 500-1500 hrs)
- Catches the most embarrassing failure (P04: 142 messages to partially solve a problem whose answer is in a 60-year-old paper)
- Provides foundation for the fine-tuning pipeline (the database becomes training data)
- Immediately available at run-time via MCP without model retraining

---

## Part XV: Executive Synthesis — Review, Tooling, and Compensation Capacity

A disciplined operator review could likely have corrected 2-3 of the 4 sign-conflict lanes before submission (P07, P08, and likely P01; P06 remains quantifier-disputed).

Practical effect of stronger controls:

1. **Human red-team pass** (opposite-sign challenge on each binary lane): biggest immediate gain.
2. **MCP tooling** (theorem retrieval, contradiction oracle, formal-check gate): strong gain.
3. **Lemma database / lemma-trained model**: large compounding gain, especially on methodology selection.

### Consolidated impact model

| Setup | Expected strict alignment (of 10) | Main reason |
|---|---:|---|
| From scratch (current-style cold start) | ~3/10 | Direction errors + missed bridge lemmas |
| + Governance controls only | ~5-6/10 | Fewer wrong-sign promotions |
| + Lemma DB + retrieval MCP | ~5-7/10 | Faster access to enabling known methods |
| + Lemma-trained model + strong harness | ~6-8/10 (sometimes ~7-9/10) | Better theorem/strategy priors + fewer false closures |

Careful review and better tooling could have compensated substantially. The remaining hard ceiling is novel-invariant discovery (typically the last 1-2 frontier lanes).

### Domain-weighted priority

These gains are not uniform across mathematical domains. Governance hardening (Package A) helps all lanes roughly equally, but compute/retrieval tooling should be domain-weighted:

- **Computational/numerical lanes** (P09, P10): already correct; highest multiplier from compute orchestration.
- **Algebraic-combinatorial lanes** (P02, P03, P04): highest multiplier from lemma retrieval (Blachman for P04).
- **High-abstraction geometry/topology/SPDE lanes** (P01, P05, P07, P08): highest multiplier from the formal verifier MCP — catching fabrications matters more than finding references when the domain requires deep conceptual reasoning.

Detailed per-lane domain-normalized multiplier tables: see `workflow_adjustment_impact_2026-02-14.md`.
