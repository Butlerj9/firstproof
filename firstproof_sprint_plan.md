# FIRSTPROOF-10: Sprint Plan & Publication Pipeline v2

**Hard deadline**: Feb 13, 2026 11:59 PM PT (encrypted answers released)  
**Internal freeze**: Feb 13, 12:00 PM PT (no new math after this; polish/publish only)  
**Goal**: Solve as many as possible, publish ALL attempts (solved, partial, failed) with full transcripts  
**Publication**: GitHub repo → email authors → social post with #1stProof  
**Repo name**: `firstproof` (preferred) → `firstproof-<username>` → `firstproof-attempt` → `firstproof-YYYYMMDD`  
**Canonical runbook**: `firstproof.md` in repo root (when documents disagree, it wins)  

### Always-publish invariant

Push to GitHub at least every **6 hours** OR after any gate completion, whichever comes first. Every push updates the `README.md` status table. This cadence is a hard rule, not a suggestion — it ensures work-to-date is always publicly available regardless of whether the deadline shifts.

---

## 1. Priority stack

| Priority | Problem | Budget (msgs) | Triage | Confidence | Key risk |
|----------|---------|---------------|--------|------------|----------|
| **1** | **P10** | 60-120 | GREEN | HIGH | Low — pure derivation |
| **2** | **P4** | 180-300 | GREEN | MEDIUM | "Experiments pass but no proof" trap |
| **3** | **P6** | 220-350 | GREEN | MEDIUM | Statement might be FALSE — need counterexample search |
| **4** | **P9** | 180-300 | YELLOW | LOW-MEDIUM | CAS exploration can diverge infinitely |
| **5** | **P3** | 120-240 | YELLOW | LOW-MEDIUM | Blocked on definition sourcing |
| **6+** | P1-P8 | 30-80 each | RED | LOW | Feasibility probe only |

**Total budget**: ~900-1200 messages across all problems + ~100 for overhead (repo/logging/publishing).

**Hard rule**: Never block. If stuck >2 hours on a subproblem, park it, advance to the next problem, return later.

---

## 2. Status definitions (do not overclaim)

| Status | Meaning | Required |
|--------|---------|----------|
| ✅ **Submitted** | Proof complete, adversarially reviewed, all citations resolved with statement numbers | Complete `answer.md` + reviewed `audit.md` |
| 🟡 **Candidate** | Coherent proof draft BUT one or more of: unresolved external dependency, unpatched adversarial failure, missing edge case, relies on numerics for a logically necessary step | `answer.md` with explicit uncertainty flags |
| 📊 **Conjecture** | Empirically supported but no proof. Publish as "conjecture + evidence + partial lemmas" | `answer.md` labeled as conjecture + `experiments/` |
| ❌ **Parked** | Explored, blocked, failure analysis published | `audit.md` with routes tried + why they failed |
| ⬜ **Not started** | Not attempted | — |

**Rule**: Never label something ✅ unless a Reviewer pass with zero unresolved red flags has completed. Default to 🟡 under time pressure.

---

## 3. Stop-loss rules

Hard caps that prevent burning budget on dead ends.

### Per-gate caps

| Gate | Cap | If exceeded |
|------|-----|-------------|
| G0 (formalize) | 10 messages | Park. Definitions unclear → Producer fetches references. |
| G1 (background) | 15 messages | If >3 unresolved EDs → block on Producer sourcing. |
| G2 (route map) | 15 messages | If no credible route → deploy Scout. If Scout fails → park. |
| Experiments | 15 messages | If counterexample found → switch to disprove. |
| G5 (proof draft) | 40 messages | If no complete draft → park with 🟡 or 📊 status. |
| G6 (review) | 20 messages (3 cycles) | If fatal flaw persists → publish as 🟡 with flaw noted. |

### Per-problem hard caps

| Class | Total messages | Action at cap |
|-------|---------------|---------------|
| GREEN | 300 | Hard park. Write up whatever you have. |
| YELLOW | 200 | Hard park. |
| RED | 80 | Hard park. |

### Stall detection

If **10 consecutive messages** produce no new lemma closure, no new experiment result, and no route change → automatic escalation to Scout or park. 

### Progress KPIs (check every 20 messages)

- **Lemma closure velocity**: subgoals closed per 20-message window. If zero for 2 windows → stalling.
- **New lemma rate**: new falsifiable lemmas generated per window. If zero → looping.
- **Convergence score**: if successive drafts are substantively identical for 3 iterations → paraphrasing, not progressing. Switch route or park.

### Anti-rewrite-loop rule

If 3 successive revisions of the same proof section are >90% similar (by inspection or embedding) with no new lemma closures, **force a route change or park**. Do not allow a 4th revision of the same approach.

### Multi-LLM validation minimums (required for 🟡/✅ on GREEN problems)

Before claiming 🟡 or ✅ on P10, P4, or P6:
1. **Reviewer pass** (Codex) with explicit fault list or accept
2. **At least 1 independent Scout check** (different model family) targeted at: counterexample attempt, OR "find a gap in lemma X," OR "re-derive the key identity from scratch"
3. **Code verification** where applicable (P10: matvec check; P4: high-precision numerics; P6: PSD checks with nullspace handling)

If any check produces a substantive disagreement → publish as 🟡 with disagreement documented, not ✅.

---

## 4. YES/NO problems: counterexample-first protocol

P4, P6, P7, P8 are YES/NO. The sprint plan MUST avoid the trap of spending days on a proof when the answer is NO.

### For P6 and P4 specifically:

**First 30% of budget = aggressive counterexample hunting.**

P6 counterexample families to test:
- Complete bipartite graphs $K_{a,b}$ with $a \ll b$
- Barbell graphs (two cliques connected by a path)
- Star graphs with cliques glued to leaves
- Lollipop graphs
- Two expanders connected by a thin cut
- Blow-ups of small graphs

P4 counterexample search:
- Adversarial root configurations (near-confluent, extreme spread, alternating signs)
- High-precision arithmetic (mpmath, 50+ digits) to catch floating-point false positives
- Structured polynomials: Chebyshev, Hermite, Laguerre roots

**Decision gate**: After counterexample phase, if no counterexample found AND a credible proof route exists → proceed to proof. If no counterexample AND no proof route → publish as 📊 conjecture.

**Experimental correctness requirements for P6:**
- All PSD checks must be done on the orthogonal complement of ker(L) (the all-ones vector)
- Handle disconnected graphs (multiple zero eigenvalues)
- Use exact rational arithmetic for small graphs, high-precision floating point for larger ones

---

## 5. Compressed artifact set (sprint mode)

Full 10-file pipeline is too heavy for a 4-day sprint. Each `PXX/` folder contains exactly 4 items:

```
PXX/
├── answer.md          # Clean statement + final proof/counterexample/conjecture
│                      # Labeled: ✅ / 🟡 / 📊 / ❌
│                      # Includes: route map, lemma structure, all citations with statement numbers
├── audit.md           # What changed, what failed, what's uncertain
│                      # Sections: routes tried, risk list, human interventions log,
│                      #           lemma DAG (inline), review notes, metrics summary
├── experiments/       # Reproducible scripts + outputs (for P4/P6/P9/P10)
│   ├── verify.py
│   └── output.txt
└── transcript.md      # Full prompts/responses + tool logs (per First Proof request)
```

Route maps, lemma DAGs, background notes, and review notes are **sections inside `audit.md`**, not separate files. This cuts documentation overhead by ~60%.

---

## 6. Timeline (absolute timestamps, PT)

### Phase 1: Pipeline validation + parallel experiments
**T_NOW → T_NOW + 18h** (target: Feb 10 evening → Feb 11 midday)

| When (PT) | Action | Owner |
|-----------|--------|-------|
| T_NOW | Create GitHub repo + scaffold (Section 8) | Producer |
| T_NOW +1hr | **P10: Full solve** (G0 → G7). Pipeline validation run. | Agent I → R |
| T_NOW +6hr | **P10 → COMMIT & PUSH** (expect ✅) | Producer |
| T_NOW +6hr | **P04: Counterexample search** (30% budget). High-precision numerics n=2..8. | Agent I |
| T_NOW +6hr | **P06: Counterexample search** (30% budget). Graph families. | Agent I (parallel) |
| Feb 10, 06:00 | P4 + P6 experiment results ready | — |
| Feb 10, 08:00 | **Decision gate**: For each of P4/P6 — counterexample found? Proof route credible? | Agent R |

### Phase 2: Proof attempts on GREEN problems
**Feb 10 midday → Feb 11 evening**

| When (PT) | Action | Owner |
|-----------|--------|-------|
| Feb 10, 12:00 | P4: If proof route viable → G2-G5. If not → 📊 conjecture writeup. | Agent I |
| Feb 10, 12:00 | P6: If proof route viable → G2-G5. If not → 📊 conjecture writeup. | Agent I |
| Feb 10, 18:00 | P4 or P6: adversarial review | Agent R |
| Feb 11, 00:00 | **P4 → COMMIT & PUSH** (✅ or 🟡 or 📊) | Producer |
| Feb 11, 06:00 | **P6 → COMMIT & PUSH** (✅ or 🟡 or 📊) | Producer |
| **Feb 11, 12:00** | **CHECKPOINT**: ≥2 problems committed. If not, compress remaining scope. Human checks logging completeness + source hygiene compliance only. | Producer |

### Phase 3: YELLOW problems (only if budget remains)
**Feb 11 evening → Feb 12 evening**

| When (PT) | Action | Owner |
|-----------|--------|-------|
| Feb 11, 12:00 | **P9: Begin** — formalize, CAS experiments for n=5, deploy scouts | Agent I |
| Feb 11, 18:00 | P9 binary decision gate: candidate F with bounded degree? OR degree lower bound? | Agent R |
| Feb 11, 18:00 | If P3 definitions sourced: **P3: Begin** | Agent I |
| Feb 12, 06:00 | **P9 → COMMIT & PUSH** (🟡 or 📊 or ❌) | Producer |
| Feb 12, 12:00 | P3 → COMMIT & PUSH if attempted | Producer |

### Phase 4: Final review + publication
**Feb 12 evening → Feb 13 noon PT**

| When (PT) | Action | Owner |
|-----------|--------|-------|
| Feb 12, 18:00 | **Final adversarial review** on all committed proofs | Agent R |
| Feb 12, 22:00 | Tighten any 🟡 → ✅ if review passes. Downgrade if not. | Agent I |
| Feb 13, 06:00 | Write `RESULTS.md` summary + polish README | Agent I + Producer |
| Feb 13, 08:00 | Last fixes from overnight review | Agent I |
| **Feb 13, 12:00 PT** | **INTERNAL FREEZE** — no more math. Polish/publish only. | Producer |
| Feb 13, 14:00 | Email contact@1stproof.org (Section 9.1) | Producer |
| Feb 13, 14:00 | Post to X/social with #1stProof (Section 9.2) | Producer |
| **Feb 13, 23:59 PT** | Encrypted answers released at 1stproof.org | — |
| Feb 14+ | Compare, post-mortem, update repo | Producer + Agent I |

---

## 7. Per-problem tactical notes

### P10 (GREEN — pipeline validation)
- Should take 4-8 hours. Mostly derivation + pseudocode.
- Add explicit **indexing specification**: how observed entries map to `(i_ℓ, j_ℓ)` pairs. Without this, the "matrix-free" claim hides an O(N) gather/scatter.
- Verification: toy dimensions (n=3, r=2, q=5), compare matrix-free matvec to explicit A·vec(W).
- **Expected status: ✅**

### P4 (GREEN — counterexample-first)
- **Track 1 (disproof, 40% budget)**: Adversarial root configs, high-precision (mpmath 50+ digits), structured polynomial families, n=2..8+.
- **Track 2 (proof, 60% budget)**: Express Φₙ via K-transform, seek convexity/monotonicity argument. The n=2 equality gives a template.
- **Proof route checkpoint**: If you can't express the inequality as a known functional inequality under ⊞ₙ by end of Day 1, downgrade to 📊.
- **Expected status: 🟡 or 📊** (proof is hard; conjecture + evidence is the realistic floor)

### P6 (GREEN — counterexample-first)
- **Track 1 (counterexample, 50% budget)**: Test adversarial graph families. PSD checks must use orthogonal complement of ker(L).
- **Track 2 (proof, 50% budget)**: Random vertex sampling with p = cε, concentration argument.
- **Graph generators to implement**: K_n, K_{a,b}, star, cycle, barbell, lollipop, expander+hub, random d-regular.
- Handle disconnected graphs and Laplacian nullspace correctly.
- **Expected status: 🟡** (concentration argument is the bottleneck)

### P9 (YELLOW — park aggressively)
- **Binary decision gate by Feb 11 18:00 PT**: Either (a) concrete candidate F with bounded degree + genericity skeleton, or (b) plausible degree lower bound strategy. If neither → ❌.
- Start with n=5 (minimal case). Try degree D ≤ 4 first.
- Deploy scout to Kimi 2.5: "What polynomial relations exist among 4×4 minors formed by selecting one row from each of n generic 3×4 matrices?"
- **Expected status: ❌ or 📊** (this is a stretch goal)

### P3 (YELLOW — definition-blocked)
- Cannot start until Producer sources definitions (Corteel-Mandelshtam-Williams paper).
- **Cutoff**: If definitions not in hand by Feb 11 12:00 PT → skip entirely.
- If sourced: make definition extraction itself agent-driven (Scout extracts verbatim from PDF).
- **Expected status: ❌ or 🟡 if reached**

### P1, P2, P5, P7, P8 (RED — feasibility probe only)
- Budget: 30-80 messages max per problem.
- Goal: clean formalization (G0) + dependency list (G1) + "is there a credible route?" (G2).
- Publish whatever you have as ❌ with routes explored.
- Only escalate if GREEN problems finish early with budget remaining.

---

## 8. Repository structure + setup script

```
firstproof/
├── README.md
├── RESULTS.md                    # Summary table updated with each commit
├── CONTAMINATION.md              # Search log + exposure log + no-incorporation statement
├── firstproof.md                 # Canonical runbook (this wins all conflicts)
├── methodology.md                # Links to research landscape + implementation guide
├── LICENSE                       # CC-BY-4.0
│
├── P01/ ... P10/                 # Two-digit folders, each with:
│   ├── answer.md                 #   Clean answer (or best attempt)
│   ├── audit.md                  #   Gates + decisions + human intervention log
│   ├── experiments/              #   Scripts + outputs
│   └── transcript.md             #   Full interaction log
│
└── common/                       # Shared utilities
    ├── publish.sh                #   Commit + push + update RESULTS.md
    └── experiment_harness.py     #   Shared experiment runner
```

### Setup script (Producer, do NOW)

```bash
# Create repo (prefer 'firstproof'; fallbacks: firstproof-<username>, firstproof-attempt, firstproof-YYYYMMDD)
gh repo create firstproof --public --description \
  "Multi-agent AI attempt at First Proof (arXiv:2602.05192). Full transcripts."

git clone https://github.com/YOUR_USERNAME/firstproof.git
cd firstproof

# Scaffold all 10 problem folders (two-digit, P01..P10)
for i in $(seq -w 1 10); do
  mkdir -p "P${i}/experiments"
  echo "# Answer: P${i}\n\n**Status**: ⬜ Not started" > "P${i}/answer.md"
  echo "# Audit: P${i}\n\n## G0 Formalize\n\n## G1 Background\n\n## G2 Route map\n\n## G3 Lemma DAG\n\n## G4 Experiments\n\n## G5 Proof draft\n\n## G6 Review\n\n## G7 Package\n\n## Human interventions\n\n## Metrics" > "P${i}/audit.md"
  echo "# Transcript: P${i}" > "P${i}/transcript.md"
done
mkdir -p common

# README
cat > README.md << 'READMEEOF'
# First Proof — Multi-Agent AI Attempt

**Sprint**: Feb 10-13, 2026 | **Answers release**: Feb 13 11:59 PM PT  
**Agents**: Claude Opus (Implementer) + Codex (Reviewer) + multi-model scouts  
**Human role**: Logistics only (no mathematical ideas or content)  
**Paper**: [arXiv:2602.05192](https://arxiv.org/abs/2602.05192) | [1stproof.org](https://1stproof.org)  

## Autonomy statement

Per [1stproof.org](https://1stproof.org): "We consider that an AI model has
answered one of our questions if it can produce in an *autonomous* way a proof
that conforms to the levels of rigor and scholarship prevailing in the
mathematics literature. In particular, the AI should not rely on human input
for any mathematical idea or content, or to help it isolate the core of the
problem."

All mathematical content in this repository was generated by AI agents.
The human producer provided: repository setup, reference PDF sourcing
(without interpretation), Python/CAS environment setup, scheduling decisions,
and logging compliance checks. Every human intervention is logged in each
problem's `audit.md` with classification (ADMIN/LOGISTICS).

## Results

| Problem | Domain | Status | Confidence | Budget used |
|---------|--------|--------|------------|-------------|
| P01 | Algebraic geometry | ⬜ | — | 0 |
| P02 | Combinatorics / algebraic | ⬜ | — | 0 |
| P03 | Markov chain / ASEP | ⬜ | — | 0 |
| P04 | Finite free convolution | ⬜ | — | 0 |
| P05 | TBD | ⬜ | — | 0 |
| P06 | ε-light subsets | ⬜ | — | 0 |
| P07 | TBD | ⬜ | — | 0 |
| P08 | TBD | ⬜ | — | 0 |
| P09 | Tensor polynomial map | ⬜ | — | 0 |
| P10 | RKHS CP-ALS | ⬜ | — | 0 |

Status: ⬜ Not started · 🔄 In progress · 📊 Conjecture · 🟡 Candidate · ✅ Submitted · ❌ Parked

## How to read this repo

- `PXX/answer.md` — the actual answer (start here)
- `PXX/audit.md` — what worked, what failed, routes tried, human intervention log
- `PXX/experiments/` — verification scripts and outputs
- `PXX/transcript.md` — complete AI interaction log
- `CONTAMINATION.md` — search log and exposure declarations

## License

CC-BY-4.0

#1stProof
READMEEOF

# Contamination log
cat > CONTAMINATION.md << 'CONTEOF'
# Contamination Log

## Policy
- No browsing of claimed solutions to numbered First Proof questions
- No searching "[author name] + [problem keywords]"
- All web searches logged below
- If accidental exposure occurs: freeze problem, log here, do NOT incorporate

## Search log
| Timestamp | Query | Purpose | Exposure risk |
|-----------|-------|---------|--------------|
| | | | |

## Exposure events
None.

## Statement
We did not incorporate any externally found solutions into our proofs.
CONTEOF

# Initial commit
git add -A
git commit -m "Initial scaffold for First Proof sprint (Feb 10-13, 2026)"
git push origin main
```

### Per-problem commit protocol

```bash
# When a problem reaches any publishable state:
git add -A
git commit -m "P10: ✅ Submitted — matrix-free PCG with Gram preconditioner

- O(n²r + qr) matvec, 3 preconditioner candidates with SPD proofs
- Verified on toy dimensions
- Adversarial review: clean
- Messages used: 87/120 budget"

git push origin main

# Status updates at minimum every 6 hours:
git add -A
git commit -m "Status: P10 ✅, P04 🔄 (counterexample search, 45/300 msgs)"
git push origin main
```

---

## 9. Notification plan

### Author notification invariant (two emails)

**Email #1 (early notice)**: Within 2 hours of first public push. Brief.

Send to **contact@1stproof.org**:
```
Subject: First Proof community attempt — repo link (will update)

Dear First Proof team,

Per your invitation to share results and transcripts, we are publishing
a multi-agent AI attempt on your ten questions:

https://github.com/YOUR_USERNAME/firstproof

Methodology: Claude Opus (implementer) + Codex (reviewer) + scouts.
Human role: logistics only. Full transcripts included.
We will push updates continuously. Summary to follow at freeze.

Best, [Your name]
```

**Email #2 (freeze notice)**: At internal freeze with summary.
```
Subject: First Proof community attempt — final results

Dear First Proof team,

Final results: https://github.com/YOUR_USERNAME/firstproof

- Attempted: [N] | ✅: [list] | 🟡/📊: [list] | ❌: [list]
- Total agent messages: [N]
- Human: logistics only (all interventions logged)

Full transcripts, experiments, and failure analysis in repo.

Best, [Your name] / catalypt.ai
```

### Social post (at freeze or earlier)
```
Multi-agent AI attempt at #1stProof (arXiv:2602.05192):

🔬 [N] attempted | ✅ [M] proofs | 📊 [K] conjectures
🤖 Claude Opus + Codex, adversarial prover-verifier
📝 Full transcripts, no human mathematical input

Repo: [link]
Answers: tonight 11:59 PM PT
```

---

## 10. Autonomy boundary (CRITICAL — read before starting)

### ALLOWED (LOGISTICS / ADMIN)
- Download PDFs, provide to agents as files (no interpretation)
- Quote verbatim theorem statements with citation (do not explain how to use them)
- Set up Python/CAS environments, run agent-written code verbatim (do not modify parameters to steer math)
- Choose problem order, time allocation, when to park (budget management is ADMIN)
- Deploy scout models with prompts (framing a query is allowed; answering it is not)
- Write commit messages, manage repo
- Check logging completeness + source hygiene compliance at gates
- Select which problem to work on next (time/budget management = ADMIN)

### NOT ALLOWED (MATHEMATICAL — any of these invalidates autonomy claim)
- Suggest proof strategies, reductions, key lemmas, counterexamples
- Explain how to use a sourced theorem ("try Theorem 3.2 on X")
- Isolate which subproblem is the crux ("the key issue is the concentration bound")
- Provide mathematical intuition ("this should be true because...")
- Interpret or summarize reference papers (provide verbatim only)
- Steer route selection ("you should try the K-transform approach")
- Select which lemma to focus on based on mathematical judgment (vs. time/budget)
- Modify agent-written experiment parameters to help find/avoid specific results

### Prompt authorship rule (safety)
Any prompt containing mathematical content must be **authored by I or R**. Producer may dispatch Scout queries only if the query text was authored by I or R and copied verbatim. Do NOT edit, rephrase, or "improve" math prompts.

### Logging
Every human action logged in `audit.md` as:
- **ADMIN**: scheduling, repo management, deploy decisions
- **LOGISTICS**: PDF fetching, environment setup, verbatim theorem provision
- **MATHEMATICAL**: ⚠️ disqualifying — flag immediately if borderline

**If uncertain whether an action is LOGISTICS or MATHEMATICAL, classify it as MATHEMATICAL and flag it.**

**If violated**: Mark the problem as `CONTAMINATED_HUMAN_MATH` in `audit.md`. Do NOT claim ✅. Be honest in the README.

### Contamination escalation ladder

If a direct solution to a First Proof problem is found online during research:
1. **FREEZE** that problem immediately
2. Log the exposure in `CONTAMINATION.md` (timestamp, URL, what was seen)
3. Do NOT incorporate any part of the found solution
4. Mark status as `CONTAMINATED_EXTERNAL_SOLUTION`
5. You may publish a separate "Contaminated appendix" post-reveal comparing your work to the found solution, but it cannot count as autonomous

---

## 11. Quick-start checklist (do NOW)

- [ ] Create GitHub repo (run script from Section 8)
- [ ] Verify API access: Claude Opus, Codex, + ≥1 scout model (Gemini / DeepSeek / Qwen / Kimi)
- [ ] Install: Python with numpy, scipy, sympy, mpmath, networkx, matplotlib
- [ ] Clone Codeberg: `git clone https://codeberg.org/tgkolda/1stproof.git`
- [ ] Copy problem statements (LaTeX) into each `PXX/answer.md` as "Problem statement" section
- [ ] **Start P10 immediately** — this is pipeline validation
- [ ] Set reminders:
  - **Feb 10, 08:00 PT**: P4/P6 counterexample decision gate
  - **Feb 11, 12:00 PT**: ≥2 problems committed checkpoint
  - **Feb 11, 18:00 PT**: P9 binary decision gate
  - **Feb 12, 18:00 PT**: Final adversarial review begins
  - **Feb 13, 12:00 PT**: INTERNAL FREEZE
  - **Feb 13, 14:00 PT**: Email + social post
  - **Feb 13, 23:59 PT**: Answers released

---

## 12. Contingency table

| Scenario | Action |
|----------|--------|
| P10 takes >8 hours | Skip to P4/P6 counterexample search (can run in parallel) |
| No problem fully solved by Feb 11 noon | Publish 📊 conjecture + evidence for P4/P6. This is still valuable. |
| Counterexample found for P4 or P6 | Major win. Write up immediately as ✅. |
| Solution found online during research | FREEZE that problem. Log in CONTAMINATION.md. Do NOT use. |
| Adversarial review finds fatal flaw late | Publish as 🟡 with flaw documented. More useful than hiding it. |
| P9 diverges without converging | Park by Feb 11 18:00 PT. Publish as ❌ with routes explored. |
| P3 definitions never sourced | Skip entirely. Note in RESULTS.md. |
| Budget exhausted before all GREEN done | Commit whatever exists. Partial > nothing. |
| Human accidentally provides math insight | Log as MATHEMATICAL in audit.md. Flag in README. Be honest. |
