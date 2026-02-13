# EXP-28: Scout Route Ranking — P03

Date: 2026-02-13
Input: EXP-27 (reconciliation matrix), EXP-29 (conflict audit)

---

## De-duplication

| Merged Route | GPT-pro R2 Source | Claude Research R3 Source | Label |
|-------------|------------------|--------------------------|-------|
| **(1-q)-divisibility** | Route 2 (primary bridge) | — (unique to GPT-pro) | **R1-DIV** |
| **Sahi binomial + AS collapse** | Route 1 (LRW/Sahi) | D1 (BinAS) | **R2-BinAS** |
| **Signed MLQ at q=1** | Route 3 (BDW queue) | D2 (SMLQ) | **R3-SMLQ** |
| **Sahi-Stokman duality** | — | D3 (SSD) | R4-SSD (below cutoff) |

---

## Ranked Shortlist (max 3)

### Rank 1: R1-DIV — (1-q)-divisibility kill-test

**Bridge lemma**: (T_i − t)E*_{λ⁻}(x; q, t) = (1−q) · R_i(x; q, t) where R_i is a polynomial/rational function regular at q=1.

**Kill-test**: Compute (T_i − t)E*_{λ⁻} at several exact rational q values for n=3 (where we have full Fraction infrastructure). Divide by (1−q). Check:
1. Is the quotient R_i(q) bounded as q→1?
2. Does R_i(1) = 0? (If so, symmetry follows since (T_i−t)g = 0 ⟹ T_i g = tg.)
3. Can the rational-function degree of R_i in q be bounded?

**Earliest fail-point**: If R_i(q) has a pole at q=1 (i.e., (T_i−t)E* = O((1−q)^0)), the divisibility hypothesis fails immediately.

**Why Rank 1**:
- Directly testable with existing n=3 infrastructure (Fraction arithmetic, order-4 perturbation)
- Already supported by numerical evidence (F4: O(1−q) convergence in EXP-4)
- Does NOT require implementing new external formulas (BDW, Sahi binomial)
- Clean bridge lemma → clean proof if it works
- Structural: if divisibility holds for general n (not just n=3), it immediately proves the Symmetry Conjecture

### Rank 2: R2-BinAS — Binomial inversion + AS factorization

**Bridge lemma**: Write E*_{λ⁻} = Σ_{μ ≤ λ⁻} c_μ(q,t) · E_μ via Sahi binomial formula on Knop poset. At q=1, each E_μ is symmetric (AS 2019). If the coefficients c_μ(1,t) are well-defined, E*_{λ⁻}(q=1) is automatically symmetric as a finite sum of symmetric functions.

**Kill-test**: For n=3, compute the Sahi binomial coefficients c_μ(q,t) symbolically and check their behavior at q=1:
1. Do the coefficients have poles at q=1? (Spectral collision risk from F7)
2. If poles exist, do they cancel in the sum?

**Earliest fail-point**: If c_μ(q,t) has uncancellable poles at q=1, the binomial expansion approach fails (the sum diverges).

**Why Rank 2**:
- Has convergent support from both scouts (highest cross-scout confidence)
- Clean structural mechanism (symmetric basis → symmetric sum)
- F7 spectral collision is a genuine risk → must test before committing
- Requires implementing Sahi binomial formula (moderate effort)

### Rank 3: R3-SMLQ — Signed multiline queue at q=1

**Bridge lemma**: Use the BDW signed MLQ formula for E*_{λ⁻}. At q=1, construct an adjacent-transposition involution on signed queue configurations that preserves signed weights and swaps monomial content → coefficient symmetry.

**Kill-test**: For n=3, enumerate all signed MLQ configurations, compute weights at q=1, and check:
1. Can configurations be paired under s_i with equal signed weight?
2. Are there unpaired configurations (which must cancel)?

**Earliest fail-point**: If the sign structure prevents clean pairing (unpaired configurations with nonzero net weight), the involution approach fails.

**Why Rank 3**:
- Supported by both scouts
- Requires implementing BDW signed MLQ formula (substantial effort — need formula details from arXiv:2510.02587)
- Most dependency-blocked of the three (formula access needed)
- Kill-test is combinatorial, bounded, but labor-intensive

---

## Below cutoff

**R4-SSD**: Sahi-Stokman evaluation duality. Dropped because:
1. Unique to Claude Research (no cross-scout validation)
2. F7 spectral collision is particularly dangerous for evaluation duality (spectral vectors ARE the evaluation points)
3. Higher theoretical overhead, lower testability

---

## Execution order

**R1-DIV → R2-BinAS → R3-SMLQ**

If R1-DIV passes kill-test at n=3: extend to n=4,5 and attempt structural proof.
If R1-DIV fails: fall back to R2-BinAS (requires Sahi binomial implementation).
If R2-BinAS fails: fall back to R3-SMLQ (requires BDW formula access).
If all three fail: HOLD — no further progress possible; park at 🟡 with updated barrier.
