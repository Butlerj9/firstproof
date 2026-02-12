# PRODUCER CHEAT SHEET
# Keep this open while running the sprint. It tells you what to copy-paste where.

## The loop

```
┌─────────────┐     paste artifact     ┌─────────────┐
│ IMPLEMENTER │ ───────────────────────→│  REVIEWER    │
│  (Claude)   │                         │  (Codex)     │
│             │←─────────────────────── │              │
└─────────────┘   paste verdict back    └─────────────┘
       │                                       │
       │  ACCEPT → next gate                   │
       │  REJECT → I patches, resubmit         │
       │  PARK   → write up, commit, move on   │
       │                                       │
       ▼                                       ▼
   SCOUT (if requested)               SCOUT (if requested)
   Copy-paste the query               Copy-paste the query
   written by I or R                  written by I or R
   VERBATIM — do not edit             VERBATIM — do not edit
```

## Step by step for each problem

### 1. Start Implementer
Paste into the Implementer session:
```
Here is Problem [N] from the First Proof challenge.

[Paste the LaTeX problem statement verbatim from the Codeberg repo]

Begin with G0 (Formalization).
Your per-problem message budget is [X]. Current gate: G0.
```

### 2. Implementer produces G0 artifact
Copy the ENTIRE G0 output from Implementer.

### 3. Paste to Reviewer
```
The Implementer has submitted G0 for P[N]. Review it.

[Paste I's G0 output here]
```

### 4. Reviewer produces verdict
- If `ACCEPT`: go back to Implementer with:
  ```
  G0 ACCEPTED by Reviewer. Proceed to G1 (Background).
  Budget remaining: [X - messages used so far].
  ```
- If `REJECT`: go back to Implementer with:
  ```
  G0 REJECTED by Reviewer. Fault list below. Patch and resubmit.
  Cycle: [1/2/3] of 3. Budget remaining: [X].

  [Paste R's full fault list here]
  ```

### 5. Repeat through G1 → G2 → G3 → G4 → G5 → G6 → G7

### 6. At G6 (Adversarial Review)
This is special — the REVIEWER generates the attack report (not I).
Paste the G5 proof to Reviewer with:
```
The Implementer has submitted G5 (Proof Draft) for P[N].
Perform G6: full adversarial review. Run all attacks and produce the structured G6 report.

[Paste I's G5 output here]
```

### 7. Package (G7)
Tell Implementer:
```
G6 complete. Reviewer verdict: [ACCEPT/REJECT + flags].
Produce G7: final answer.md for P[N].
Status to assign: [✅/🟡/📊] based on review.

[Paste R's G6 report if there are residual risks to acknowledge]
```

### 8. Commit
```bash
cd firstproof
# Copy answer.md, audit.md, transcript.md into P[XX]/
git add -A
git commit -m "P[XX]: [STATUS] — [one-line summary]"
git push origin main
```

---

## Scout deployment (when I or R requests it)

1. I or R writes a query in their output under "Scout query" or "SCOUT REQUEST"
2. You copy that query **exactly as written** — do NOT rephrase
3. Open a session with the target scout model
4. Paste the query
5. Copy the scout's response back to whoever requested it:
   ```
   Scout response ([model name]):

   [Paste scout's full response here]
   ```

**NEVER** edit the scout query. **NEVER** add your own mathematical context. If you need to add the problem statement for context, copy it verbatim from the Codeberg repo.

---

## What you CAN say to agents

✅ "G0 accepted. Proceed to G1."
✅ "G2 rejected. Faults below. Cycle 2 of 3."
✅ "Budget update: 45 of 120 messages used."
✅ "Here is the PDF of [paper]. Use it as needed." [attach PDF, no commentary]
✅ "Parking this problem. Produce best-available writeup."
✅ "Here is the scout response:" [paste verbatim]
✅ "Time check: 6 hours to freeze."

## What you CANNOT say to agents

❌ "Try using the K-transform" (math strategy)
❌ "The key insight is..." (math content)
❌ "Focus on Lemma L3, that's the crux" (isolating the core)
❌ "I think the answer is TRUE" (math judgment)
❌ "The scout's response means you should..." (interpretation)
❌ "This paper says [summary]" (interpreting literature — provide the PDF only)
❌ Any edit to a scout query before pasting it

---

## Logging

After every interaction, append to `P[XX]/audit.md`:

```
### Human intervention [timestamp]
- **Type**: ADMIN / LOGISTICS
- **Action**: [what you did]
- **Justification**: [why]
```

If you catch yourself doing something that might be MATHEMATICAL, STOP. Log it as:
```
### Human intervention [timestamp] ⚠️
- **Type**: MATHEMATICAL (FLAGGED)
- **Action**: [what happened]
- **Impact**: [which problem/gate this affects]
```

---

## Quick budget tracker

| Problem | Budget | Used | Remaining | Status |
|---------|--------|------|-----------|--------|
| P10 | 120 | | | ⬜ |
| P04 | 300 | | | ⬜ |
| P06 | 350 | | | ⬜ |
| P09 | 300 | | | ⬜ |
| P03 | 240 | | | ⬜ |

---

## Emergency rules

- **Stall (10 msgs no progress)**: If I is spinning, paste: "STALL DETECTED. You have spent [N] messages with no lemma closure. Produce a stall report OR park."
- **Budget >80%**: Paste: "BUDGET WARNING: [X] of [Y] messages used. Produce best-available output at current status."
- **3 reject cycles**: Paste: "3 reject cycles on G[N]. ROUTE_CHANGE or PARK. Do not attempt a 4th revision of the same approach."
- **Latent-limit trigger**: If G6 still has unresolved MAJOR/FATAL faults and transcript token burn is high, paste: "LATENT-LIMIT ESCALATION: run one relaxed pass per firstproof.md §3A (expanded primary-source search, >=3 scouts, exact/symbolic + high-precision checks), then re-review."
- **Accidental math input**: If you accidentally said something mathematical, immediately paste: "RETRACT: My previous message contained mathematical content. Disregard it. Logging as CONTAMINATED_HUMAN_MATH."
