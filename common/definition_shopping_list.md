# Definition-Only Shopping List for Producer

Generated: 2026-02-11 (after P07+P08 resolution)
Protocol: `common/definition_only_escalation.md`

## Summary

P08 has been RESOLVED without needing external definitions (octahedron counterexample + Gromov). P07 has been RESOLVED via Q-PD (Shapiro's lemma) + Wall surgery in dim 5 (answer: YES). The remaining parked problems that could benefit from definition-only escalation are listed below in priority order.

## ~~P07 — Lattices in Lie Groups~~ (RESOLVED)

**Route**: Q-Poincaré duality for lattices with torsion → surgery theory → manifold construction.

### Definitions needed (3-4 items)

1. **Q-Poincaré duality group** (or "Poincaré duality group over Q")
   - Likely source: Brown, "Cohomology of Groups", Ch. VIII; or Bieri, "Homological Dimension of Discrete Groups"
   - What we need: Formal definition of a group Γ being PD_n over Q. Specifically: Ext^i_{QΓ}(Q, QΓ) = Q if i = n, 0 otherwise.
   - Why critical: The proof route requires showing uniform lattices with torsion ARE Q-PD groups.

2. **Virtual cohomological dimension (vcd)**
   - Likely source: Brown, "Cohomology of Groups", §VIII.11; Serre, "Cohomologie des groupes discrets"
   - What we need: vcd(Γ) = cd(Γ₀) for any torsion-free finite-index Γ₀ ≤ Γ.
   - Why critical: Need vcd(Γ) = dim(G/K) for uniform lattices.

3. **Surgery exact sequence for Q-PD groups** (or "Wall realization theorem over Q")
   - Likely source: Wall, "Surgery on Compact Manifolds", 2nd ed.; or Ranicki, "Algebraic and Geometric Surgery"
   - What we need: Statement-only: if Γ is Q-PD of dimension n ≥ 5, then Γ = π₁(M) for some compact n-manifold M with M̃ Q-acyclic. Or the relevant obstruction theorem.
   - Why critical: This is the second half of the proof (from Q-PD to manifold existence).

4. **(Optional) Proper cocompact action → Q-PD**
   - Likely source: Lück, "Survey on classifying spaces for families of subgroups"; or Brown-Davis, "Lattices and proper Q-PD"
   - What we need: Statement: if Γ acts properly and cocompactly on a contractible manifold X with finite stabilizers, then Γ is Q-PD of dimension dim(X).
   - Why critical: This gives Q-PD for all uniform lattices (with or without torsion), since Γ acts on G/K.

### Scout-identified sources (cross-model consensus)
- Raghunathan 1972, Def. 1.1/1.8 — uniform lattice (known; not needed)
- Knapp 2002, §I.8 / Helgason 1978, Ch. II §6 — semisimple Lie groups (known; not needed)
- Davis 2008, "Geometry and Topology of Coxeter Groups" — aspherical manifold constructions
- Lück, "Survey on classifying spaces" — classifying spaces EΓ for groups with torsion
- Browder-Novikov-Sullivan-Wall surgery program — manifold realization

### Ambiguity flags (from scouts)
- Does "rationally acyclic" require vanishing rational homotopy groups? → NO, just H̃_*(−; Q) = 0.
- Is M smooth or topological? → Either works for the question (topological suffices).
- Must M̃ be contractible? → NO, only Q-acyclic.

## P01 — Stochastic Analysis (LOW PRIORITY)

### Definitions needed (4-6 items)
1. Φ⁴₃ measure and its construction (Hairer, Barashkov-Gubinelli)
2. Quasi-invariance of Gaussian measures under nonlinear maps
3. Cameron-Martin space for the Φ⁴₃ model
4. Regularity structures framework (statement level only)

### Scout status: NOT queried (no scout briefs for P01)

## P02 — Representation Theory (LOW PRIORITY)

### Definitions needed (5-8 items)
1. Conductor ideal q and its generator Q (JPSS)
2. Essential Whittaker function (Matringe)
3. Rankin-Selberg integral for GL_{n+1} × GL_n (JPSS)
4. Non-vanishing at s = 1/2 for the local zeta integral
5. u_Q = I_{n+1} + Q E_{n,n+1} transformation

### Scout-identified sources (cross-model consensus)
- JPSS 1981/1983 — Conducteur des représentations, Rankin-Selberg convolutions
- Matringe — essential Whittaker functions (exact source uncertain)
- Cogdell-Piatetski-Shapiro — L-functions for GL_n
- Bump, "Automorphic Forms and Representations" — general reference

## P05 — Equivariant Homotopy (LOWEST PRIORITY)

### Definitions needed: 5+ just to STATE the answer
The problem is open-ended ("state and prove"), and the scouts flagged:
- "No primary source explicitly defines O-adapted slice filtration"
- "No published theorem explicitly characterizes O-slice connectivity via geometric fixed points"

**Recommendation**: Skip unless all other escalation targets are exhausted.

## Action items for producer

| Priority | Problem | Action | Estimated effort |
|----------|---------|--------|-----------------|
| ~~1~~ | ~~P07~~ | ~~RESOLVED: Q-PD via Shapiro + surgery~~ | — |
| 2 | P02 | Source JPSS conductor definition (Def/Thm numbers) | 15 min |
| — | P01, P05 | Skip unless time permits | — |

**Note**: P08 is RESOLVED. No further reference sourcing needed for P08.
