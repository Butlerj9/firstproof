# Audit: P09 — Tensor polynomial map

## G0 Formalize

**Status**: ✅ ACCEPTED (Cycle 2, 0 faults).

**Original G0**: Exact quantified statement, truth mode EXPLORE BOTH (55% YES / 45% NO), symbol glossary with 14 entries, edge-case analysis (6 cases), 5-phase experiment plan (EXP-1 through EXP-5), falsification criteria, precision policy.

**Codex Review (Cycle 1)**: REJECT — 4 faults:
- F1 (FATAL): Restatement appeared to separate F(τ,Q) instead of F(R) where R = τ·Q
- F2 (MAJOR): Quantifier order not explicit — single F can't serve all n (domain changes)
- F3 (MAJOR): "not identical" vs "pairwise distinct" ambiguity in index condition
- F4 (MAJOR): Counterexample/falsifier shape not explicit enough

**Patch Cycle 1**: All 4 faults addressed:
- F1: Rewrote statement with F_n acting on R = (τ_{αβγδ} · Q^{αβγδ}_{ijkl}) as single flattened input
- F2: Explicit schema: ∃D ∈ N, ∀n≥5, ∃F_n with coordinate degrees ≤ D
- F3: Defined D_n = {pairwise distinct 4-tuples} and D_n^c explicitly; all conditions use D_n
- F4: Added explicit NO-type-1 (false positive) and NO-type-2 (false negative) falsifier templates
- Added: flattening convention (lex order), Zariski-generic convention (over R)

**Key structural insight**: The input R^{αβγδ} = τ_{αβγδ} · Q^{αβγδ} is a scalar multiple of Q for each Greek 4-tuple. The 81 Latin-index components provide redundancy. Cross-ratio constructions within a single Greek tuple cancel τ; cross-ratio constructions across Greek tuples may cancel Q via determinantal identities.

## G1-G3 Background, Route Map, Lemma DAG

**Status**: ✅ Complete (fast-tracked with G4-G5).

**Background**: Q tensor structure from 4×4 determinants, Plücker coordinates, rank-1 tensor varieties, Frobenius inner products on Latin indices, Cauchy-Binet decomposition of Q-Gram matrices.

**Route map**: Single route — YES via degree-4 Frobenius-product polynomial construction.

**Route evolution**: Initially explored both YES and NO directions. EXP-2/EXP-4 suggested NO (Plücker degree grows with n), but EXP-5/5b discovered YES via a fundamentally different polynomial type.

**Lemma DAG**:
- L1: Frobenius inner product structure — ⟨R^T1,R^T2⟩ = τ_T1·τ_T2·K_{T1,T2}(A) [verified EXP-1,3]
- L2: Rank-1 τ ⟹ 2×2 minor vanishing in (a,b) block with fixed (γ,δ) [standard]
- L3: K-compatibility — degree-4 Frobenius products admit 9-dim A-independent vanishing [verified EXP-5b]
- L4: Separation — vanishing polynomials are nonzero on generic non-rank-1 τ [verified EXP-5b]

## G4 Experiments

**Status**: ✅ Complete — all phases passed.

**Scripts**:
- `experiments/exp1_build_Q_tensors.py` — Q tensor construction and verification
- `experiments/exp2_rank_flattening_test.py` — Rank flattening tests
- `experiments/exp3_polynomial_search.py` — Cross-ratio and polynomial separator search
- `experiments/exp4_degree_scaling.py` — Plücker rank scaling with n
- `experiments/exp5_vanishing_search.py` — Degree-4 vanishing polynomial existence
- `experiments/exp5b_verify_separation.py` — Separation verification and universality

| Phase | Scope | Result | Notes |
|-------|-------|--------|-------|
| EXP-1: Q tensor | n=5, 7 tests | ALL PASS | Q rank=71/81, Plücker verified, scalar multiple confirmed |
| EXP-2: Rank flattening | n=5,7, multiple flattenings | PARTIAL | Small flattenings don't separate; Plücker does but degree ∝ n |
| EXP-3: Cross-ratio | n=5,6, multiple A/τ | PASS | ⟨R^T1,R^T4⟩/⟨R^T2,R^T3⟩ constant for rank-1 (std~10⁻¹⁶) |
| EXP-4: Degree scaling | n=5,6,7 | KEY | Plücker rank = 3n(n-1), grows O(n²); K-ratio varies with A |
| EXP-5: Vanishing search | n=6, degree 2 and 4 | KEY | Degree-2: null dim=0. Degree-4: null dim=9 (stabilized at 20 A) |
| EXP-5b: Separation | n=6, 20 A, 10 τ, 4 (γ,δ) | PASS | rank-1: |f|~10⁻⁷; random: |f|~10⁶; universal across (γ,δ) |

## G5 Proof draft

**Status**: ✅ Complete — answer.md written as 🟡 Candidate.

**Answer**: YES, D = 4

**Key construction**: Degree-4 Frobenius-product polynomials f_c(R) = Σ c_{pq} ⟨R^{T_{p1}},R^{T_{p2}}⟩ · ⟨R^{T_{q1}},R^{T_{q2}}⟩ with A-independent coefficient vectors c in the 9-dimensional kernel of the rank-1 vanishing constraint.

**Proof gaps**:
1. Algebraic proof of K-compatibility (numerical evidence only)
2. Sufficiency of combined index-pair constructions for full 4-way rank-1 detection
3. Zariski-genericity of separation (tested probabilistically)

## G6 Review

**Status**: ✅ ACCEPTED (Cycle 2b, 0 faults).

**Codex Review (Cycle 1)**: REJECT — 5 faults. Patch Cycle 1 applied by Implementer.

**Codex Re-review (Cycle 2a)**: REJECT — 5 remaining faults:
- F1 (FATAL): The artifact still claims theorem-level YES while explicitly admitting proof-critical gaps.
- F2 (MAJOR): Quantifier gap remains (`forall n >= 5`, A-independent coefficients, and uniform degree proof not established).
- F3 (MAJOR): Masked-domain implication from block tests to full 4-way rank-1 is still unproved.
- F4 (MAJOR): Numerical claims in text remain stronger than what scripts certify (approximate vanishing only).
- F5 (MINOR): Experiment narrative inconsistencies across scripts vs prose still need cleanup.

**Patch Cycle 2**: Implementer addressed remaining concerns — further softened all claims, ensured 📊 Conjecture throughout.

**Codex Re-review (Cycle 2b)**: ACCEPT — 0 faults. All checklist items passing. Recommendation: PROCEED to G7, keep 📊 Conjecture.

## G7 Package

**Status**: ✅ Complete.

All deliverables finalized:
- `answer.md`: 📊 Conjecture — YES, D = 4. Three proof gaps explicitly documented.
- `audit.md`: Full gate history G0–G7.
- `transcript.md`: Complete interaction log with token accounting.
- `experiments/`: 6 scripts (exp1–exp5b), runnable, results consistent with answer.md.

## Human interventions

| Timestamp | Type | Action | Justification |
|-----------|------|--------|---------------|
| 2026-02-10 | ADMIN | Producer instructed start of P09 | Scheduling/priority |

## Metrics

| Metric | Value |
|--------|-------|
| Messages used | ~21 |
| Gate | G7 (Package) |
| Status | 📊 Conjecture (YES, D=4) |
| Budget | 200 messages (YELLOW — ~21 used) |

### Token estimates (synced with transcript.md)

| Category | Est. tokens |
|----------|-------------|
| Implementer input | ~18,300 |
| Implementer output | ~32,000 |
| Reviewer input | ~14,500 |
| Reviewer output | ~6,600 |
| **Running total** | **~70,600** |

*Updated: 2026-02-10 — after G7 Package.*
