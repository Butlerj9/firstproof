# Claude Research Breakdown — P04

Date: 2026-02-12  
Source: User-provided Claude research response  
Lane: P04  
Purpose: Extract practical, bounded next actions from the research report.

---

## 1) High-value signal

### Proposed top routes
1. **Sparse constrained SOS** (TSSOS + Putinar) on the existing degree-16 margin polynomial.
2. **Finite score/projection route** as a discretized Shlyakhtenko–Tao analog.
3. **Schur complement lifting** to isolate and control `b-c'` cross terms.

### Why relevant
- All three target the exact unresolved structure (`b!=0` general n=4).
- They are distinct from already exhausted Jensen-only or naive global SOS routes.

---

## 2) Evidence-tier extraction

### Proved in lane context (unchanged)
- n=2 equality.
- n=3 theorem-level proof.
- n=4 `b=0` subcase closure.

### Cited/proposed by new report (needs verification before integration)
- TSSOS/Putinar sparse certificate feasibility.
- Score/projection analogy via free Fisher information literature.
- Schur complement PSD lifting concept.

### Empirical/proposed
- 31-term sparsity is emphasized as computational leverage.
- Suggestion that constrained certificates may succeed where unconstrained SOS fails.

### Unresolved
- No theorem-level closure for full n=4 delivered.
- Solver/tool availability and certificate extraction remain open execution risks.

---

## 3) Bounded route gate for next cycle

### Route A (primary): constrained sparse certificate
1. Verify actual tool availability (Julia + TSSOS + SDP backend).
2. Reconstruct exact margin + exact semialgebraic constraints.
3. Run low-order sparse Putinar attempts.
4. Require machine-verifiable certificate output; otherwise route remains unresolved.

### Route B: Schur-complement decomposition
1. Algebraically lift margin into block matrix form.
2. Check if cross terms isolate into off-diagonal blocks.
3. Attempt PSD conditions reduction.

### Route C: finite-score bridge memo
1. Formalize finite score identity precisely in lane notation.
2. Identify minimal lemma needed for projection contraction.
3. Stop if no exact conditional-expectation structure is derivable.

---

## 4) Stop-loss policy

1. If Route A fails at environment gate (no solver/toolchain), do not spend cycle budget on pseudo-SOS claims.
2. If Route B does not produce explicit algebraic decomposition in bounded steps, stop.
3. If Route C remains analogy-level without exact finite identity, mark as strategic only.
4. Keep P04 status unchanged unless a checkable proof/certificate appears.

---

## 5) Integration guidance

1. Add one P04 escalation row in `P04/audit.md` summarizing this research round.
2. Keep theorem statements untouched unless independently verified.
3. Log all adopted external claims in contamination tracking before integration.

