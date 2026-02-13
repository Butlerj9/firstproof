# Claude Code Checklist — P05 (From Claude Research Round 1)

Date: 2026-02-12  
Lane: P05 only  
Goal: Run one bounded cycle that converts the new structural framing into lane-usable lemmas.

---

## 0) Load context first

1. `P05/answer.md`
2. `P05/audit.md`
3. `P05/transcript.md`
4. `P05/experiments/exp1_transfer_systems.py`
5. `tools/claude-research-final/transcripts/P05_claude_research_response_2026-02-12.md`
6. `tools/claude-research-final/transcripts/P05_claude_research_breakdown_2026-02-12.md`

---

## 1) Hard constraints

1. No status upgrade without theorem-level closure.
2. Label every claim: `Proved / Cited / Empirical / Unresolved`.
3. Verify each imported external statement in primary source text before integration.
4. Log all external statements in contamination format before use.
5. Keep cycle bounded and explicitly stop if only analogy-level progress appears.

---

## 2) Route A (primary): source-verified theorem extraction

### A1) Extract exact statements needed
1. Carrick O-slice framing statement(s).
2. Smith reconstruction/conservativity statement(s).
3. MNN/Glasman detection analog statement(s).
4. Schwede–Shipley reduction statement(s).

### A2) Produce dependency map
1. Build a minimal theorem dependency graph for Class II “if” direction.
2. Mark each node:
   - usable directly,
   - needs adaptation,
   - not usable for this lane.

### A3) Artifacts
1. `P05/experiments/exp2_theorem_extraction_map.md`
2. `P05/experiments/exp2b_theorem_dependency_graph.md`

---

## 3) Route B: endomorphism-category reduction pilot

1. Write lane-specific generator set `S` for the smallest open case (`G=Z/4` class-II setup).
2. State explicit target reduction:
   - from `Loc(S)` connectivity detection
   - to a module-category t-structure detection condition.
3. List exactly which Hom-vanishing checks would be sufficient.
4. Artifacts:
   - `P05/experiments/exp3_endomorphism_reduction_pilot.md`

---

## 4) Route C: smallest-case fixed-point obstruction sharpening

1. For the `Z/4` open case, tabulate fixed-point dimensions for all relevant subgroup levels.
2. Identify the exact step where non-uniformity breaks current induction.
3. Recast that break as a precise candidate bridge lemma.
4. Artifacts:
   - `P05/experiments/exp4_z4_obstruction_sharpening.py`
   - `P05/experiments/exp4_z4_obstruction_sharpening_report.md`

---

## 5) Stop-loss gates

1. If Route A does not yield verified theorem statements, stop cycle.
2. If Route B cannot be formalized beyond analogy, mark strategic-only and stop B.
3. If Route C does not produce a precise candidate lemma, stop.
4. If all routes stop, keep P05 at `BLOCKED_WITH_FRONTIER`.

---

## 6) Required outputs after cycle

1. Lane verdict line: `CLOSEABLE_NOW` or `BLOCKED_WITH_FRONTIER`.
2. Route table A/B/C with pass/fail/strategic-only.
3. `P05/audit.md` escalation row.
4. `P05/transcript.md` entry with artifact paths.
5. `CONTAMINATION.md` updates for adopted external claims.

---

## 7) Minimal command skeleton

```powershell
git status -sb

# Optional computational aid for Route C
python P05/experiments/exp4_z4_obstruction_sharpening.py

git status -sb
```

