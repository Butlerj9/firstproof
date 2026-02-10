# Audit: P06 — Alpha-light sets in spectral graph theory

## G0 Formalize

**Status**: ✅ ACCEPTED (Cycle 2, 0 faults).

**Original G0**: Exact quantified statement, truth mode (90% NO), counterexample identified (K_n family), symbol glossary, edge-case analysis, 3-phase experiment plan, CE-1 verification complete.

**Codex Review**: REJECT — 2 faults:
- F1 (MAJOR): Disproof doesn't handle c≥2 (α=c/2 escapes (0,1))
- F2 (MINOR): Truncated matrix-type glossary lines

**Patch Cycle 1**: Both faults addressed. Case split for c≥1 (size impossibility) and c∈(0,1) (K_n counterexample). Full explicit dimensions/PSD in glossary. See transcript.md Session 2.

## G1-G3 Background, Route Map, Lemma DAG

Fast-tracked: counterexample is self-contained standard linear algebra.

**Background**: Combinatorial Laplacian, PSD ordering, vertex-transitive eigenvalue decomposition.

**Route map**: Single route — counterexample via K_n.

**Lemma DAG**:
- L1: Eigenspace decomposition of αL_{K_n} - L_S [proved in answer.md §2]
- L2: Case split over c [proved in answer.md §3]

## G4 Experiments

**Status**: ✅ Complete — all phases passed.

**Scripts**: `experiments/ce1_complete_graph_verify.py`, `experiments/ce2_other_graphs.py`

| Phase | Scope | Result | Notes |
|-------|-------|--------|-------|
| CE-1: K_n eigenvalue verification | n=3–24, all α | ALL PASS | Eigenvalue formula + boundary + exhaustive |
| CE-2: Non-complete graphs | cycles, paths, stars, grids, Erdos-Renyi | Greedy lower bounds | Sparse graphs admit larger α-light sets at small α; greedy is not exact |

## G5 Proof draft

**Status**: ✅ Complete — answer.md written as 🟡 Candidate.

**Key results**:
- Answer: NO
- Counterexample: K_n family with α = c/2
- Key lemma: eigenspace decomposition of αL_{K_n} - L_S
- Proof is self-contained (no external dependencies)
- No proof gaps

## G6 Review

**Status**: ✅ Complete — Codex verdict: 🟡 Candidate (3 red flags).

**Codex red flags**:
1. **Boundary k=n** (RF1): 4-subspace decomposition invalid at k=n (W_{S^c} dimension -1). Fixed: k=n handled as separate boundary case with direct computation.
2. **c≥1 logic** (RF2): Original Case 1 conflated c=1 (S=V forced) with c>1 (size impossible). Fixed: explicit three-way case split (c>1, c=1, c∈(0,1)).
3. **"K_n hardest" overclaim** (RF3): CE-2 greedy search is not exact; claim withdrawn. Proof only uses K_n as one sufficient counterexample family.

**Patch Cycle 1**: All 3 red flags addressed in answer.md:
- §2: k=n boundary case added before 4-subspace decomposition
- §2: dimension check now states "requires 2≤k≤n-1"
- §3: three-way case split (c>1 vacuous, c=1 S=V fails, c∈(0,1) K_n)
- §4 CE-2: greedy caveat added, "hardest" claim removed
- Header: reviewer red flags section added

## G7 Package

**Status**: ✅ Complete.

**Final status**: 🟡 Candidate — Answer: NO.

**Deliverables**:
- `answer.md` — Full proof: eigenspace decomposition of αL_{K_n} - L_S, three-way case split, numerical verification
- `audit.md` — Gate history G0–G7, metrics, human intervention log
- `transcript.md` — Complete interaction log with token accounting
- `experiments/ce1_complete_graph_verify.py` — Eigenvalue formula verification (n=3–24, exhaustive n≤8)
- `experiments/ce2_other_graphs.py` — Greedy comparison on non-complete graphs
- `README.md` — Updated with P06 status

**What was achieved**:
- Complete proof that no universal c>0 exists
- Counterexample: K_n family with α=c/2
- Key lemma: eigenspace decomposition with full boundary handling (k=0,1,...,n)
- Self-contained (no external dependencies)
- Numerical verification across all tested parameters

## Human interventions

| Timestamp | Type | Action | Justification |
|-----------|------|--------|---------------|
| 2026-02-10 | ADMIN | Producer instructed start of P06 | Scheduling/priority |

## Metrics

| Metric | Value |
|--------|-------|
| Messages used | ~14 |
| Gate | G7 (Package complete) |
| Status | In progress |
| Budget | 300 messages (GREEN) |

### Token estimates (synced with transcript.md)

| Category | Est. tokens |
|----------|-------------|
| Implementer input | ~16,000 |
| Implementer output | ~20,000 |
| Reviewer input | ~14,000 |
| Reviewer output | ~3,600 |
| **Running total** | **~53,600** |

*Updated: 2026-02-10 — after G6 review + patch.*
