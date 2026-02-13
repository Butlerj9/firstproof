# Claude Research Response — P03 (Round 2)

Date captured: 2026-02-13  
Source: User-provided Claude Research response (manual paste)  
Lane: P03  
Integration intent: Archive the "P03 Frontier Certificate v2" response for reproducible lane history.

---

## Raw Response (as provided by user)

# P03 Frontier Certificate v2: Interpolation Macdonald Symmetry Conjecture (n >= 5)

## Critical Structural Constraint (R1 Correction)

**EXP-5b finding**: At exact q=1, the symmetric vanishing space has dimension **14** (not 1). The vanishing conditions at q=1 are far too weak to uniquely determine E*_{lambda^-}. The Symmetry Conjecture is true because the **q->1 limit selects** the symmetric element from this 14-dimensional space — not because the q=1 vanishing conditions force it.

**Filter**: Any approach that works purely at the q=1 point, without engaging the limit-selection mechanism, is structurally incompatible with the known proof mechanism and must be killed.

---

## Status Summary

| n | Status | Method | Reference |
|---|--------|--------|-----------|
| 2 | **PROVED** | Exact symbolic | section 3 |
| 3 | **PROVED** | Perturbation order 4, rank 49/49, 82-zero FTA | section 7 |
| 4 | **PROVED** | Modular perturbation order 8, 90-value sweep x 2 primes | section 7b |
| >=5 | **BLOCKED** | 12 failed routes + 7 killed R1 routes; 7 surviving routes | this response |

---

## Blocking Claim

For n>=5, the Symmetry Conjecture — that the inhomogeneous lower-degree corrections in E*_{lambda^-}(x; q=1, t) are symmetric — cannot be verified computationally (247+ days for n=5) or proved inductively (branching fails with 4 independent obstructions: partition mismatch, lost Hecke condition, vanishing of antidominant, limit-vs-specialization gap), and no algebraic shortcut has been found across 12 failed routes and 14 R1 approach families (7 killed by limit-selection filter).

---

## 12 Previously Failed Routes (Sessions 2-15)

1. Symbolic-t perturbation (SymPy too slow at order >=4)
2. Rational Richardson extrapolation (insufficient convergence)
3. Thiele continued fraction (poles in reciprocal differences)
4. S_n equivariance quotient (11K->324 blocks, per-block cost still prohibitive)
5. Spectral vector collapse at q=1 (vectors remain distinct at generic t)
6. Restriction x_n->0 (wrong implication direction)
7. Hecke algebra degeneration (symmetry emergent, not structural)
8. Null space structure (explains but no computational shortcut)
9. AS leading-term factorization (closes leading term only, not corrections)
10. Branching rule induction (EXP-20: 4 independent obstructions)
11. Kimi's "Degree Reduction + Spectral Vanishing" (spectral collision deficit: -35 for n=3)
12. Direct computation for n=5 (247 days, O(N^3) Gaussian elimination, N=11,627)

---

## 7 Killed R1 Routes (Limit-Selection Filter)

| # | Route | Kill Reason |
|---|-------|-------------|
| 4 | Multispecies SSEP symmetry transfer | Vertex model formulated only at q=1; no q-dependent framework to track limit selection |
| 9 | Nonsymmetric plethysm extension | Designed for homogeneous polynomials; no interpolation extension exists; static q=1 |
| 10 | Dimension-counting in symmetric vanishing space | Directly killed: EXP-5b shows dim = 14, not 1 |
| 11 | Inhomogeneous Dunkl operator symmetry | Eigenspace analysis at static q=1; does not engage limit |
| 12 | Knop-Sahi creation operator at q=1 | Recursion at static q=1; intermediate steps pass through non-partition compositions |
| 13 | Integrable vertex model at q=1 | Transfer matrix commutativity at static q=1; signs prevent clean formulation |
| 14 | Sahi Jordan algebra / Capelli eigenvalue | Classical Jordan algebra at q=1; limit mechanism unresolved |

---

## 7 Surviving Routes

### Route S1: Signed Multiline Queue q->1 Analysis
Source: Ben Dali-Williams (arXiv:2510.02587, Oct 2025)

### Route S2: Signed Tableaux Formula at q->1
Source: Ben Dali-Williams (arXiv:2510.02587, section 6)

### Route S3: Interpolation PushTASEP Reversibility
Source: Ayyer-Martin-Williams (arXiv:2403.10485), forthcoming [BDW]

### Route S4: Rational KZ Monodromy
Source: Kasatani-Takeyama (arXiv:0810.2581), Lascoux-Rains-Warnaar (arXiv:0807.1351)

### Route S5: Sahi's Binomial Theorem at q->1
Source: Sahi (1998), Chen-Sahi (arXiv:2403.02490)

### Route S6: Yang-Baxter Eigenvalue Degeneracy
Source: arXiv:2601.12881 (Jan 2026)

### Route S7: Rains' Elliptic Degeneration Path
Source: Rains (2005/2018), Lascoux-Rains-Warnaar (arXiv:0807.1351)

---

## Unlock Theorems (as listed in response)

1. Signed multiline queue column-swap symmetry at q=1.
2. Interpolation PushTASEP detailed balance at q=1.
3. Rational KZ monodromy triviality.
4. Binomial coefficient partition-vanishing at q=1.

---

## 48-Hour Lane Plan (as listed in response)

0-12h:
- Implement signed multiline queue enumeration for n=3 at q=1.
- Cross-check with signed tableaux formula.

12-24h:
- If S1/S2 succeeds, attempt column-swap pairing structure.
- Begin eigenvalue analysis for Route S6 at n=5.

24-48h:
- Monitor arXiv for [BDW].
- If pairing pattern appears, test n=4 and formulate bridge lemma.
- Start Sahi binomial coefficient q=1 limit checks.

---

## Contamination Log (as listed in response)

The response lists statement-level extraction from:
- arXiv:2510.02587
- arXiv:2403.10485
- arXiv:0810.2581
- arXiv:2601.12881
- arXiv:2403.02490
- arXiv:0807.1351
- arXiv:1801.04550

Risk level stated: LOW (statement-level extraction only).

---

## Verdict (as listed in response)

Lane status: BLOCKED_WITH_FRONTIER  
Escalation level: L5  
Next action: execute 48-hour plan starting with Route S1 (signed multiline queue computational test).

