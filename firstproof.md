# FIRSTPROOF: Single Source of Truth + Living Record

**Repo**: `firstproof` → `firstproof-<username>` → `firstproof-attempt` → `firstproof-YYYYMMDD`  
**Timezone**: America/Los_Angeles (PT)  
**Answer release (T_RELEASE)**: 2026-02-13 23:59 PT ([1stproof.org](https://1stproof.org))  
**Internal freeze (T_FREEZE)**: T_RELEASE - 12h = 2026-02-13 12:00 PT  
**Last updated**: 2026-02-10  
**Owners**: Producer (Human, logistics only) + Implementer (Claude Opus) + Reviewer (Codex) + Scouts (Gemini / DeepSeek / Qwen / Kimi)

### Canonical documents

These files initialize the project; this file (`firstproof.md`) is the ongoing runbook.

1. `firstproof.md` (THIS FILE) — canonical directives + living log. **If any doc conflicts, this file wins.**
2. `firstproof_sprint_plan.md` — time plan + publishing ops + setup scripts
3. `docs/reference/firstproof_implementation_guide.md` — gates + per-problem work orders (deep)
4. `docs/reference/firstproof_research_landscape.md` — background + citations (optional reading)

---

## 0. Canonical rules (if documents disagree, this file wins)

### Sprint parameters
- **T_NOW**: 2026-02-10 PT (update on Day 0)
- **T_DEADLINE**: 2026-02-13 23:59 PT (solutions release, verify at [1stproof.org](https://1stproof.org))
- **T_FREEZE**: 2026-02-13 12:00 PT (= T_DEADLINE - 12h; no new math after this)

### Hard invariants

- **Always publish**: push to GitHub at least every **6 hours** OR after any gate completion, whichever comes first.
- **Always log**: every agent interaction must land in `PXX/transcript.md`.
- **Never block**: any subproblem stuck >2 hours triggers escalation or parking.
- **Counterexample-first** for YES/NO problems (P4, P6, P7, P8).
- **Human provides NO mathematical ideas/content.** Human may do: repo setup, tool setup, PDF retrieval, scheduling, pushing commits, sending emails, running agent-written scripts verbatim.
- **Default status under time pressure: 🟡.** Never overclaim ✅.

---

## 1. Autonomy boundary (First Proof eligibility)

Per [1stproof.org](https://1stproof.org): "We consider that an AI model has answered one of our questions if it can produce in an *autonomous* way a proof that conforms to the levels of rigor and scholarship prevailing in the mathematics literature. In particular, the AI should not rely on human input for any mathematical idea or content, or to help it isolate the core of the problem. Citations should include precise statement numbers and should either be to articles published in peer-reviewed journals or to arXiv preprints."

### Allowed (Human = ADMIN / LOGISTICS)

- Create repo, scaffold files, manage deadlines, allocate budgets
- Choose which problem to attempt next (time/budget management only)
- Fetch PDFs/papers and provide them verbatim to agents (no interpretation)
- Quote verbatim theorem statements with citation, without explaining how to use them
- Run agent-provided scripts verbatim (no modifying parameters to steer math)
- Ensure logs are complete; ensure citations include statement numbers when claiming ✅
- Deploy scout models with prompts (framing a query is allowed; answering it is not)

### Not allowed (Human = MATHEMATICAL)

- Any hint, idea, strategy suggestion, lemma suggestion, or "focus on X theorem"
- Any interpretation/summarization of a reference that selects the "key idea"
- Isolating which subproblem is the crux
- Selecting which lemma to focus on based on mathematical judgment (vs. time/budget)
- Any manual adjustment of experiments intended to find/avoid specific results
- Steering route selection ("try the K-transform approach")

### Prompt authorship rule (safety)

Any prompt containing mathematical content must be **authored by Implementer (I) or Reviewer (R)**. Producer may dispatch Scout queries only if the query text was authored by I or R and copied verbatim. Producer may NOT edit, rephrase, or "improve" mathematical prompts — this is the most common way autonomy claims get undermined in practice.

**If violated**: mark the problem as `CONTAMINATED_HUMAN_MATH` in audit.md. Do NOT claim ✅. Be honest.

---

## 2. Repo structure (sprint mode)

Each problem uses **4-file sprint mode** in two-digit folders (`P01/` … `P10/`):

```
PXX/
├── answer.md        # Clean final proof/counterexample/conjecture. Status labeled.
│                    # Citations section at bottom with statement numbers.
├── audit.md         # All gates (G0–G7) as sections + routes + risks +
│                    # metrics summary + human intervention log (ADMIN/LOGISTICS tags).
├── experiments/     # Scripts + outputs (if used). Reproducible.
└── transcript.md    # Full prompts/responses + tool logs.
```

Root files:

```
firstproof/
├── README.md             # Public-facing overview + results table
├── RESULTS.md            # Expanded status + confidence + links
├── CONTAMINATION.md      # All web searches + exposure events + no-incorporation statement
├── firstproof.md         # THIS FILE — canonical truth
├── methodology.md        # Links to research landscape + implementation guide
└── LICENSE               # CC-BY-4.0
```

Gates G0–G7 are conceptual phases stored as **sections inside `audit.md`**, not separate files. Only `answer.md` is clean standalone output. The full 10-file-per-problem structure is available post-freeze for archival polish.

---

## 3. Status taxonomy (problem-level)

| Status | Meaning | Required |
|--------|---------|----------|
| ✅ **Submitted** | Proof complete; reviewer has **zero** unresolved red flags; all external deps resolved with statement-number citations OR proved inline | `answer.md` + reviewed `audit.md` |
| 🟡 **Candidate** | Coherent draft but unresolved dependency / edge case / reviewer flag | `answer.md` with uncertainty flags |
| 📊 **Conjecture** | Strong empirical evidence; no proof route; published as conjecture + experiments | `answer.md` labeled + `experiments/` |
| ❌ **Parked** | Explored; blocked; failure analysis published | `audit.md` with routes tried |

---

## 3A. Latent-Limit Escalation (Relaxed Pass)

Use a second-pass mode when a problem appears blocked by missing machinery, not by proof hygiene.

Observed signal from current artifacts:
- `P04`: ~76k-token transcript, repeated review cycles, unresolved finite-n theorem gap -> 📊.
- `P06`: review faults were boundary/quantifier issues and closed cleanly -> no relaxed pass needed.

### Trigger (all required)
- G6 completed with >=1 unresolved MAJOR/FATAL red flag.
- Same bottleneck persists across >=2 route attempts or >=2 patch cycles.
- Token log indicates heavy spend (>=50k tokens OR >=25% of problem budget after first full G5/G6 cycle).
- At least one independent scout pass and one high-precision/exact experiment pass already done.

### Relaxations allowed in this pass
1. Budget extension: +100 messages (GREEN) or +60 messages (YELLOW) for one additional pass.
2. Broader source search for primary references on adjacent machinery (identities, inequalities, finite analogs), while still avoiding direct-solution searches for numbered First Proof questions.
3. Scout expansion to >=3 model families, with prompts targeted at falsification and missing hypotheses (not confirmation-only prompts).
4. Stronger computation stack: exact/symbolic small-case derivations + high-precision numerics for boundary regimes.
5. Explicit dependency ledger update in `audit.md`: blocked statement, hypotheses needed, what was verified, what remains unproved.

### Exit criteria
- If blocker closes and G6 passes: upgrade status normally.
- If blocker remains: publish as 📊/❌ with explicit label "unsolved after relaxed pass."
- If contamination event occurs: freeze problem and mark `CONTAMINATED_EXTERNAL_SOLUTION`.

## 3B. Final Synthesis Pass (one-time, end-stage)

After all active tracks are complete (or parked), run one final consolidation attempt:

1. Feed GPT-5.2-pro the full artifact set for each attempted problem: `answer.md`, `audit.md`, `transcript.md`, and experiment scripts/outputs.
2. Restrict the objective to unresolved proof bottlenecks and cross-artifact consistency, not broad re-exploration.
3. Keep llm-only hygiene: no web-search for foundational lemmas during this pass unless the run is explicitly marked relaxed/non-llm-only.
4. Send any newly claimed closure through standard G6 adversarial review before status upgrade.

Interpretation rule:
- If GPT-5.2-pro still cannot close the bottleneck with full multi-agent context, record this as evidence that the remaining gap is likely not solvable with current LLM-only training/architecture.

## 3C. Out-of-Scope Upgrade Paths (not executed in this sprint)

To preserve timeline and comparability, the following upgrades were left out of current execution:

1. Fine-tuning on orthogonal-but-related proof spaces (adjacent theorem families and foundational corpora).
2. Process-level verifier fine-tuning with step supervision.
3. Formal-checker-coupled training loops (Lean/SMT-in-the-loop generation).
4. Retrieval-index tuning for foundational statement/hypothesis matching.
5. Multi-agent replay training on accumulated audit/transcript failure patterns.

These are valid follow-on research directions, but not part of the current sprint claims.

---

## 4. Gates (G0–G7) as sections inside `audit.md`

**G0 — Formalize**: Restate with explicit quantifiers and object types. Define every symbol. Describe what a counterexample would look like. *Cap: 10 messages.*

**G1 — Background**: List prerequisites, mark each: PROVE-INLINE / CITE (needs statement #) / BLOCKED (needs sourcing). If >3 BLOCKED: stop, request Producer sourcing. *Cap: 15 messages.*

**G2 — Route map**: 2–4 strategies. Bottleneck lemma for each. For YES/NO: include explicit disproof track. *Cap: 15 messages.*

**G3 — Lemma DAG**: Minimal dependency graph (inline list OK). Each lemma has acceptance test.

**G4 — Experiments** (required for P4/P6/P9/P10): Small cases + counterexample hunt. PSD checks done correctly (nullspace handling). Reproducibility: seed + version notes. *Cap: 15 messages.*

**G5 — Proof draft**: No "and therefore" gaps. Every claim proved inline or cited with statement number. *Cap: 40 messages.*

**G6 — Adversarial review**: Reviewer tries to break weakest lemma. Edge/degenerate cases checked. Max 3 patch cycles. If fatal flaw persists → downgrade to 🟡. *Cap: 20 messages.*

**G7 — Package**: `answer.md` clean standalone. `audit.md` complete. `transcript.md` complete.

### Verification stamp (required at top of `answer.md` for ✅ or 🟡)

```
**Status**: ✅ / 🟡 / 📊 / ❌
**Reviewer**: [model] — verdict: [accept / list of flags]
**Scout check**: [model] — [outcome]
**Code verification**: [script path] — [pass/fail, seed]
**External deps**: [N resolved / M unresolved]
```

### External dependency handling (binary)

- For ✅: statement-number citation required, OR proved inline. No exceptions.
- For 🟡: `NEEDS CITATION` flags allowed but enumerated in `audit.md` risk list.
- For 📊/❌: citation gaps acceptable but noted.

---

## 5. Stop-loss rules

### Per-gate caps

| Gate | Cap | If exceeded |
|------|-----|-------------|
| G0 | 10 msgs | Park → fetch references |
| G1 | 15 msgs | Block on Producer sourcing |
| G2 | 15 msgs | Deploy Scout → if fails, park |
| G4 | 15 msgs | If counterexample → switch to disprove |
| G5 | 40 msgs | Park with 🟡 or 📊 |
| G6 | 20 msgs (3 cycles) | Publish as 🟡 with flaw noted |

### Per-problem hard caps

| Class | Budget | At cap |
|-------|--------|--------|
| GREEN (P10, P4, P6) | 300 msgs | Hard park, write up whatever exists |
| YELLOW (P9, P3) | 200 msgs | Hard park |
| RED (P1, P2, P5, P7, P8) | 80 msgs | Hard park |

### Stall detection

If 10 consecutive messages yield no lemma closure, no new experiment result, and no route change → escalate to Scout (one pass) or park.

### Anti-rewrite-loop rule

If 3 successive revisions of the same proof section are >90% similar with no new lemma closures → force route change or park. No 4th revision of the same approach.

---

## 6. Multi-LLM validation minimums

Required before claiming 🟡 or ✅ on GREEN problems (P10, P4, P6):

1. **Reviewer pass** (Codex) with explicit fault list or accept
2. **At least 1 independent Scout check** (different model family) targeted at: counterexample attempt, OR "find a gap in lemma X," OR "re-derive the key identity from scratch"
3. **Code verification** where applicable:
   - P10: matvec vs explicit A·vec(W) on toy sizes
   - P4: high-precision (mpmath 50+ digit) numeric search + stability checks
   - P6: PSD checks with correct nullspace handling + adversarial graph families

If any check disagrees → publish as 🟡 with explicit disagreement documented.

---

## 7. Contamination hygiene

- **Allowed**: browsing for prerequisite definitions/theorems
- **Disallowed**: searching "solution to First Proof Problem X" or author+keywords combos
- All searches logged in `CONTAMINATION.md` (timestamp, query, purpose)
- If accidental exposure:
  1. Freeze that problem
  2. Log exposure event (timestamp, URL, what was seen)
  3. Do NOT incorporate
  4. Mark `CONTAMINATED_EXTERNAL_SOLUTION`

---

## 8. Problem triage + budget allocation

| Problem | Priority | Budget | Class | Next milestone |
|--------:|:--------:|-------:|:-----:|----------------|
| P10 | 1 | 60–120 | GREEN | G0→G7 same session |
| P4 | 2 | 180–300 | GREEN | Counterexample-first (30%+ budget) |
| P6 | 3 | 220–350 | GREEN | Counterexample-first (50% budget) |
| P9 | 4 | 180–300 | YELLOW | n=5 CAS probe; binary gate by T_FREEZE-48h |
| P3 | 5 | 120–240 | YELLOW | Blocked until definitions sourced |
| P1,P2,P5,P7,P8 | probe | 30–80 ea | RED | G0–G2 feasibility only |

After P10, run P4 and P6 counterexample hunts in parallel/interleaved.

---

## 9. Publication + notification invariants

### GitHub cadence

Push at least every 6 hours OR after any milestone. Every push updates `README.md` status table.

### Author notifications

- **Email #1 (early notice)**: within 2 hours of first public push. Repo link + "will update."
- **Email #2 (freeze notice)**: at T_FREEZE with summary + final link.
- Send to: **contact@1stproof.org**

### Social post

At freeze (or earlier if results warrant). Tag **#1stProof**. Link repo.

---

## 10. Verification stack (default)

Verification does NOT default to Lean 4.

1. **Adversarial reviewer** (Codex) — fault checklist, try to break weakest lemma
2. **Independent scout** (different model family) — re-derive key identity or find gap
3. **Code sanity checks** — numerical experiments, toy cases, edge cases
4. **Lean 4** ONLY for micro-lemmas already in mathlib. Never burn sprint time on autoformalization.

---

## 11. Living logbook (append-only below this line)

Format: `YYYY-MM-DD HH:MM PT — Action. Commit hash. Budget used. Decisions. Risks.`

Do not rewrite old entries. Append only.

### 2026-02-10
- [ ] Repo created (name: ___)
- [ ] First push done (commit: ___)
- [ ] Email #1 sent (time: ___)
- [ ] P10 started (gate: ___)

---
