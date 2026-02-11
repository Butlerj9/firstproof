# Audit: P05 — O-slice connectivity characterization via geometric fixed points

## G0 Formalize

**Status**: ✅ Complete.

### Problem restatement

Fix a finite group G. Let O denote an **incomplete transfer system** associated to an N∞ operad.

**Tasks**:
1. **Define** the slice filtration on the G-equivariant stable category adapted to O.
2. **State and prove** a characterization of the O-slice connectivity of a connective G-spectrum in terms of the geometric fixed points.

### Object glossary

| Symbol | Type | Definition |
|--------|------|------------|
| G | Finite group | Fixed throughout |
| N∞ operad | G-equivariant operad | Encodes which norms/transfers are available; interpolates between naive and genuine equivariant structure |
| O | Incomplete transfer system | Indexing category for an N∞ operad: specifies which transfer maps H → G/K exist |
| G-equivariant stable category | Stable ∞-category | G-spectra; objects have genuine fixed points Φ^H for all H ≤ G |
| Slice filtration | Filtration on G-spectra | Tower P^n → P^{n-1} → ⋯ with slices P^n_n capturing "dimension n" information |
| O-slice connectivity | Connectivity notion | Adapted connectivity measuring when a G-spectrum is "n-connected" relative to the transfer system O |
| Geometric fixed points Φ^H | Functor | For H ≤ G: Φ^H(X) = (X ∧ ẼP[H])^H where ẼP[H] is a universal space |
| Connective G-spectrum | Object in equivariant stable category | Underlying homotopy groups π_n^H(X) = 0 for n < 0, for all H ≤ G |

### Key mathematical structure

The classical (non-equivariant) slice filtration is well-understood: for an ordinary spectrum X, the slices correspond to Eilenberg–MacLane spectra, and connectivity is determined by homotopy groups.

In the G-equivariant setting, the slice filtration (Hill–Hopkins–Ravenel) uses representations of G to grade the filtration. The "regular slice filtration" uses the regular representation. The problem asks for:
1. An **O-adapted** variant that only uses transfers/norms from the incomplete transfer system O.
2. A characterization of the resulting connectivity notion in terms of geometric fixed points Φ^H for appropriate subgroups H.

The expected answer likely has the form: "X is O-slice n-connected iff Φ^H(X) is f(n,H)-connected for all H in some class determined by O."

### Truth mode

- [x] EXPLORE BOTH (50% YES / 50% — this is a "state and prove" problem, so the answer must exist by design)

**Note**: This problem is unusual in that it asks to **state** a characterization (not just prove one). The characterization itself is part of the answer. The problem has a known answer (the authors have a proof ≤ 5 pages).

### Counterexample shape

Not applicable — the problem asks to produce a characterization, not to determine YES/NO. However, a wrong characterization could be falsified by explicit G-spectra.

### Experiment plan

| Phase | Task | Pass/Fail |
|-------|------|-----------|
| EXP-1 | For G = Z/2 and O = complete transfer system, recover the standard slice filtration characterization | Matches known → PASS |
| EXP-2 | For G = Z/2 and O = trivial (no nontrivial transfers), determine what the characterization should reduce to | Consistent → PASS |
| EXP-3 | Attempt to state the characterization for G = Z/p (cyclic, prime order) and verify against known results | Consistent → PASS |

## G1 Background

**Status**: ⚠️ BLOCKED — critical references not accessible.

### Critical external dependencies

| Reference | Status | Need | Blocking? |
|-----------|--------|------|-----------|
| Hill–Hopkins–Ravenel (HHR), "On the nonexistence of elements of Kervaire invariant one" | ⚠️ Statement-level known | Regular slice filtration definition, slice connectivity characterization | Partially |
| Blumberg–Hill (2015), "Operadic multiplications in equivariant spectra, norms, and transfers" | ❌ Not sourced | N∞ operads, incomplete transfer systems | YES |
| Blumberg–Hill (2016), "Incomplete Tambara functors" | ❌ Not sourced | Incomplete transfer systems, algebraic structure | YES |
| Hill (2012), "The equivariant slice filtration: a primer" | ❌ Not sourced | Slice filtration foundations | YES |
| Ullman (2013), "On the slice spectral sequence" | ❌ Not sourced | Slice filtration details | Partially |
| Rubin (2021), "Characterizations of equivariant Steiner and linear isometries operads" | ❌ Not sourced | Transfer system classification | Partially |

### Known facts (without references)

1. **HHR slice filtration**: For a G-spectrum X, the slice filtration is a tower of localizations. The n-th slice P^n_n X is the "fiber" of P^n X → P^{n-1} X. For the regular slice filtration, X is slice n-connected iff all slices below n vanish.

2. **Geometric fixed points characterization (HHR)**: In the complete transfer system case (all norms available), X is slice n-connected iff Φ^H(X) is (n·|G/H| − 1)-connected for all H ≤ G.

3. **N∞ operads**: These parametrize "incomplete" equivariant commutative ring structures. An N∞ operad O specifies which norm maps N_H^K exist.

4. **Transfer systems**: A transfer system is a sub-poset of the subgroup lattice of G equipped with certain transfer maps. Blumberg–Hill showed these classify N∞ operads.

5. **Geometric fixed points**: Φ^H(X) is a non-equivariant spectrum that captures the "purely H-equivariant" information in X. For X = Σ^V S^0 (representation sphere), Φ^H(Σ^V S^0) = Σ^{V^H} S^0.

### Assessment

This problem requires deep equivariant homotopy theory. The key ingredients are:
1. Understanding how incomplete transfer systems modify the slice filtration.
2. The relationship between the modified slice connectivity and geometric fixed points.

The expected characterization likely replaces the factor |G/H| in the classical formula with something determined by O. For instance, if O only allows transfers along certain subgroup inclusions, the connectivity bound for Φ^H may involve the "O-dimension" of G/H.

**However**: Without access to Blumberg–Hill's papers on N∞ operads and incomplete transfer systems, I cannot formalize the O-adapted slice filtration precisely. The definition itself is part of the problem, and getting it right requires understanding the existing framework.

**Blocked items**: 3+ critical references not sourced (Blumberg–Hill N∞ operads, Blumberg–Hill incomplete Tambara functors, Hill slice filtration primer).

## G2 Route Map

**Status**: ✅ Routes identified; execution blocked.

### Route A: Representation-graded filtration (most likely approach)

1. Define the O-slice filtration by restricting which representation spheres S^V appear as "dimension V" cells, using only those V whose associated norms are in O.
2. The O-dimension of a representation V at a subgroup H should count dim(V^H) weighted by the O-structure.
3. Characterization: X is O-slice n-connected iff Φ^H(X) is (n·d_O(H) − 1)-connected for all H in the "O-essential" subgroups, where d_O(H) is an O-dependent dimension function.

**Bottleneck**: Defining d_O(H) correctly.

### Route B: Categorical localization approach

1. Define the O-slice filtration as a Bousfield-type localization using O-cells.
2. The O-cells are equivariant cells G/H_+ ∧ S^n where H → G is an O-admissible transfer.
3. Connectivity follows from the cellular structure.

**Bottleneck**: Making the cell structure precise without reference access.

### Route C: Direct construction for cyclic groups

1. Work out the complete answer for G = Z/p (only nontrivial subgroup is G itself).
2. There are exactly 2 transfer systems: complete (both transfers) and trivial (no nontrivial transfers).
3. Compare the characterizations in both cases to extract the pattern.

**Bottleneck**: Even this requires knowing the precise slice filtration definitions.

## Decision: ❌ PARK

**Rationale**:
- 3+ critical external dependencies blocked (Blumberg–Hill × 2, Hill primer).
- The problem asks to **state** a characterization (not just prove one), meaning the formulation itself requires deep familiarity with the O-adapted slice filtration which is only defined in unpublished/inaccessible work.
- Note: One of the paper's authors (Andrew Blumberg) is also an author of the key references needed. This problem likely arose from his own research program.
- Experimental verification would require implementing equivariant homotopy computations, which is beyond reasonable scope.
- The problem is the most "open-ended" of the ten: it asks for a statement + proof, not YES/NO.

**Documented routes for potential future attempt**:
- Route C (cyclic group case) is most tractable if references become available.
- The characterization likely has the form: "O-slice n-connected iff Φ^H(X) is (n·d_O(H)−1)-connected" where d_O(H) depends on O's structure at H.

## Human interventions

| Timestamp | Type | Action | Justification |
|-----------|------|--------|---------------|
| 2026-02-10 | ADMIN | RED-feasibility blitz | Scheduling/priority |

## Metrics

| Metric | Value |
|--------|-------|
| Messages used | ~2 |
| Gate | G2 (route map) |
| Status | ❌ Parked (blocked on references + open-ended formulation) |
| Budget | 80 messages (RED — ~2 used) |
