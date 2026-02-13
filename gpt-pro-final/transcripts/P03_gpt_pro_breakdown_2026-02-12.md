# GPT-pro Breakdown — P03

Date: 2026-02-12  
Source: User-provided GPT-pro response  
Lane: P03  
Purpose: Extract execution-ready signal and hard constraints.

---

## 1) High-value correction

### New hard constraint
- Under standard interpolation definitions, the old route
  - `f^*_mu(x;1,t) ∝ t^{inv(mu)}` (x-independent Mallows reduction)
  is not compatible with the cited q=1 interpolation framework (already breaks in smallest restricted case).

### Practical implication
- P03 should now target construction of an explicit **x-dependent** chain or an equivalent local-relations proof, not x-independent Mallows proportionality.

---

## 2) Frontier reformulation

### Minimal missing component
- A polynomial-free local generator on `S_n(lambda)` with rates `r(mu -> nu)` such that
  - `L^T w = 0`, where `w(mu)=f^*_mu(x;1,t)`.

### Best proposed bridge
- Derive q=1 local exchange / qKZ-type relations and read them as stationarity equations.

---

## 3) Route gate summary

### Top routes from this GPT round
1. qKZ/exchange-relations -> generator extraction.
2. Markov chain on signed MLQs + lumping to bottom row.
3. Vertex-model transfer matrix normalization.

### Fast falsifiers
1. n=2 exact check vs cited q=1 formula.
2. n=3 closure under proposed local moves.
3. nonnegativity of candidate rates on natural `(x,t)` domain.

---

## 4) Recommended bounded next cycle

1. Rebuild n=2 exactly and record explicit two-state detailed-balance rates.
2. Implement n=3 signed-MLQ enumerator at q=1.
3. Fit a local move family (adjacent swap + push candidates).
4. Validate `L^T w=0` numerically/symbolically in n=2,3.
5. Stop if no local move family survives positivity + closure.

---

## 5) Integration notes

1. Treat this as **frontier sharpening**, not closure.
2. Update `P03/audit.md` with one escalation row (if adopting).
3. Maintain P03 status unless a proof/certificate is produced.
4. Log source contamination metadata before importing claims into lane proof text.

