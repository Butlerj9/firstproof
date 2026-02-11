# Transcript: P07

## Session 1 — 2026-02-10 PT: RED-feasibility blitz

### G0-G2 (feasibility assessment)
- Problem formalized: given a uniform lattice Gamma in a connected semisimple Lie group G (with Gamma containing elements of order 2), does there exist a compact topological manifold M with pi_1(M) = Gamma and universal cover rationally acyclic?
- Dependencies triaged: Raghunathan (uniform lattice definition, known); Borel (existence of uniform lattices with torsion, known); Shapiro's lemma for Q-coefficients (standard, can prove inline); surgery realization for Q-PD groups (NEEDS_SOURCE).
- Route map: Route A (Borel construction — fails, produces contractible not Q-acyclic); Route B (Q-Poincare duality + surgery realization).
- Decision: Route B selected. Initially parked due to RED classification.

### Budget at park: ~2 messages used of 80.

---

## Session 2 — 2026-02-11 PT: Definition-only escalation + G3-G6

### G3-G5 (proof draft via escalation)
- **Q-PD argument (proved)**: Gamma acts properly and cocompactly on G/K (contractible, finite stabilizers). By Shapiro's lemma with Q-coefficients: H^i(Gamma; Q[Gamma]) = H^i_c(G/K; Q). Poincare duality for the manifold G/K gives H^i_c(G/K; Q) = Q if i = dim(G/K), 0 otherwise. Therefore Gamma is a Q-Poincare duality group of dimension n = dim(G/K).
- **FH(Q) confirmation**: Fowler (2012) confirms that uniform lattices in connected semisimple Lie groups satisfy the Farrell-Hsiang condition FH(Q), needed for surgery-theoretic realization.
- **Surgery realization step (gap)**: The argument requires: "If Gamma is Q-PD of dimension n >= 5 and satisfies FH(Q), then Gamma = pi_1(M) for some compact n-manifold M with universal cover Q-acyclic." This is expected to follow from Wall's surgery exact sequence over Q, but no precise statement-number citation has been provided.
- Verification script `exp1_qpd_verification.py` confirms algebraic checks.

### G6 self-review
- Q-PD component: ACCEPT (Shapiro's lemma argument is rigorous and self-contained).
- Surgery realization: CONDITIONAL ACCEPT (the statement is widely believed in the surgery theory community but needs a precise published reference for First Proof standards).
- Overall: CONDITIONAL ACCEPT — lane kept at Candidate.

### Budget: ~4 messages used of 80 (RED class).

### Methodological note for researchers

The Q-PD direction illustrates a pattern seen across this sprint: the algebraic/homological step can often be proved rigorously by LLM agents using standard tools (Shapiro's lemma, Poincare duality), but the "last mile" — connecting the algebraic result to a geometric realization — requires citing specific surgery-theoretic machinery that the agents cannot verify from first principles without reference access. This is a characteristic failure mode: the agent can prove the algebra but cannot close the geometry without external citations.

### Surgery gap: precise statement needed

The following would close the gap (any one suffices):
1. Wall (1970/1999), "Surgery on Compact Manifolds": a theorem stating that Q-PD groups of dimension >= 5 with appropriate finiteness conditions are realized as fundamental groups of compact manifolds with Q-acyclic universal covers.
2. Quinn (1972/1979), "Surgery on Poincare and normal spaces": extended surgery to more general Poincare duality settings.
3. Ranicki (2002), "Algebraic and Geometric Surgery": modern treatment with explicit obstruction groups.
4. Luck (2005), "Survey on classifying spaces for families of subgroups": may contain the precise statement in the context of groups with torsion.

### Reconstruction note

This file combines a compact session summary with methodological annotations. Detailed message-by-message logs were not reconstructed into this artifact.
