# Definition-Only Reference Escalation Protocol

## Purpose

Enable re-opening of parked problems (P01, P02, P05, P07, P08) without breaking
llm-only hygiene, by ingesting only definitions, notation, and theorem statements
from primary sources.

## Scope-limited ingest rules

### ALLOWED (CITE_ONLY)
- Definitions and notation from original papers/books
- Theorem/lemma/proposition **statements** (with numbering)
- Hypothesis blocks (conditions under which a result holds)
- Object type signatures (e.g., "E*_mu is a polynomial in x1,...,xn with coefficients in Q(q,t)")

### NOT ALLOWED
- Proof sections or proof sketches
- Commentary, motivation, or "how to apply this" discussion
- Blog posts, surveys, or secondary summaries (primary-source only)
- Any text that reveals or hints at solutions to First Proof questions

## Protocol

### Step 1: Producer identifies source
- Producer locates the specific paper/book for a blocked dependency.
- Producer identifies the exact section containing the needed definition/statement.

### Step 2: Producer extracts verbatim text
- Producer copies ONLY the definition/statement text (verbatim, no paraphrasing).
- Producer does NOT read or relay proof sections.
- Producer does NOT provide interpretation or guidance on how to use the result.

### Step 3: Quarantine logging
For each imported item, log in BOTH:
- `CONTAMINATION.md`: source, section, what was extracted, exposure risk
- `PXX/audit.md`: tagged as `CITE_ONLY` or `PROVE_INLINE`

Format:
```
| Timestamp | Source | Section | Item type | Tag | Exposure risk |
|-----------|--------|---------|-----------|-----|---------------|
| YYYY-MM-DD | Author (Year), Title | Def 3.1 | Definition | CITE_ONLY | LOW |
```

### Step 4: Hypothesis-check gate
- Claude/Codex MUST explicitly verify all hypotheses before using any cited statement.
- If hypotheses cannot be verified from available information, treat as unresolved
  dependency and keep parked.
- No "well known" claims without CITE_ONLY or PROVE_INLINE tag.

### Step 5: Hard contamination fail-safe
- If proof/solution text for ANY First Proof question is accidentally seen:
  1. IMMEDIATELY freeze that problem lane
  2. Log the exposure in CONTAMINATION.md with full details
  3. Mark the problem as CONTAMINATED — do NOT incorporate any content
  4. Continue only if the exposed content is unrelated to the solution path

## Priority order for escalation

Based on tractability assessment from RED-feasibility blitz:

| Priority | Problem | What's needed | Est. definitions to ingest |
|----------|---------|---------------|---------------------------|
| 1 | P08 (Symplectic) | Polyhedral Lagrangian smoothing, tropical-Lagrangian correspondence | 3-5 definitions from Matessi, Mikhalkin |
| 2 | P07 (Lattices) | Q-Poincare duality for groups with torsion, surgery obstruction theory | 3-4 definitions from Davis, Wall, Luck |
| 3 | P01 (Stochastic) | Phi^4_3 construction, variational framework, :phi^3: integrability | 4-6 definitions from Barashkov-Gubinelli |
| 4 | P02 (Rep theory) | Essential Whittaker functions, conductor theory, modified RS integrals | 5-8 definitions from JPSS, Matringe |
| 5 | P05 (Eq. homotopy) | N-infinity operads, incomplete transfer systems, O-slice filtration | 6-10 definitions from Blumberg-Hill |

## Expected yield

- P08: HIGH — concrete objects, local smoothing construction likely follows from definitions
- P07: MEDIUM — Q-PD + surgery theory could close with 2-3 key definitions
- P01: MEDIUM — core question (exp(int :phi^3: psi) in L^1) may resolve with variational bounds
- P02: LOW-MEDIUM — deep automorphic forms; definitions alone may not suffice
- P05: LOW — open-ended formulation; definitions needed even to STATE the answer

## Human intervention classification

All definition-only ingests are classified as LOGISTICS (verbatim relay of published
definitions, no mathematical interpretation by producer).
