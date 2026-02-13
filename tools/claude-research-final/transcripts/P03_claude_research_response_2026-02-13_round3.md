# Claude Research Response — P03 (Round 3)

Date captured: 2026-02-13  
Source: User-provided Claude Research response (manual paste)  
Lane: P03  
Integration intent: Archive the additional P03 frontier response for lane history and checklist generation.

---

## Raw response (archival capture)

# Symmetry of interpolation Macdonald corrections at q = 1

The conjecture that `f* = lim_{q->1} E*_{lambda^-}(x; q, t)` is symmetric for all `n` remains open for `n >= 5`.

Verdict in response: `BLOCKED_WITH_FRONTIER`.

Core response claims:

1. Sahi-Knop integrality is cited to assert the `q->1` limit equals direct specialization (object well-defined).
2. `n <= 4` remains in the proved tier; `n >= 5` remains blocked.
3. 14 novel candidate families are listed across 6 domains.
4. 3 routes are developed to bridge-lemma + kill-test level:
   - D1: Binomial inversion + Alexandersson-Sawhney factorization (BinAS)
   - D2: Signed multiline queue analysis at `q=1` (SMLQ)
   - D3: Sahi-Stokman duality leveraging (SSD)
5. A 48-hour plan is provided with kill-test order D1 -> D2 -> D3.

---

## A) Lane verdict table (as provided)

| Field | Value |
|-------|-------|
| Status | BLOCKED_WITH_FRONTIER |
| Blocker | No structural characterization of lower-degree correction terms in `M_{lambda^-}(x;1,t)` forcing `S_n` symmetry for general `n` |
| Evidence tier | Proved `n<=4`; numerical/high-precision support in small cases |
| Failed routes | 10 prior + 3 Kimi scout proposals evaluated |
| New candidate routes | 14 |
| Cross-domain coverage | 6 domains |

---

## B) Failure map (as provided)

Exact unresolved statement in response:

For all `n >= 5`, prove symmetry of `M_{(0,1,...,n-1)}(x;1,t)` (equivalently the lane `q->1` object under the stated integrality assumption).

Minimal blocker in response:

No known identity controlling lower-degree homogeneous components in the Moebius inversion expansion strongly enough to force full `S_n` symmetry.

---

## C) 14 approach families (as provided; abbreviated labels)

1. Signed multiline queue weight collapse (BDW 2025).
2. Signed tableaux formula at `q=1` (BDW section 6).
3. Interpolation PushTASEP reversibility.
4. Bar monomial expansion via glissade.
5. Rational qKZ / monodromy constraint.
6. Free probability / cumulant asymptotics.
7. Integrable vertex model R-matrix degeneration.
8. Shifted Dunkl operator commutant.
9. Binomial inversion + AS factorization.
10. Yang-Baxter graph pole cancellation extension.
11. Hilbert scheme degeneration route.
12. Tropical Newton polytope invariance.
13. Plethystic lambda-ring route.
14. Categorification via Soergel bimodules.

---

## D) Top 3 actionable approaches from response

### D1) BinAS

Bridge idea:
- invert Sahi binomial formula on Knop poset,
- apply AS `q=1` factorization termwise,
- show non-symmetric permutation factors cancel under Moebius-weighted sums.

Kill-test in response:
- implement `n=3` symbolic extraction and inspect cancellation structure in coefficients.

Likely failure mode in response:
- cancellation may be compositional/fragile, not structural.

### D2) SMLQ

Bridge idea:
- use BDW signed multiline queue formula,
- construct adjacent-transposition involution at `q=1` that preserves signed weights and swaps monomial content.

Kill-test in response:
- full `n=3` signed queue enumeration and coefficient pairing checks.

Likely failure mode in response:
- sign structure may obstruct clean involution.

### D3) SSD

Bridge idea:
- leverage Sahi-Stokman evaluation duality at `q=1`,
- derive permutation-invariant evaluation constraints at staircase spectral points.

Kill-test in response:
- evaluate `n=3` staircase-permuted spectral points and test sigma-independence.

Likely failure mode in response:
- correction factors may remain sigma-dependent.

---

## E) Escalation/contamination block (as provided)

The response lists statement-level use of sources including:
- arXiv:1801.04550
- arXiv:1609.09686
- arXiv:2510.02587
- arXiv:2601.12881
- arXiv:1901.04852
- arXiv:0807.1351
- arXiv:2104.08598
- arXiv:0810.2581
- Knop/Sahi foundational interpolation sources

Response-level risk statement: low, statement-level extraction.

---

## F) Claude Code handoff payload in response

The response includes 3 executable-test blocks aligned to D1/D2/D3 with stop-loss gates:
1. BinAS kill-test script scaffold.
2. SMLQ kill-test scaffold.
3. SSD kill-test scaffold.

---

## G) Response verdict (as provided)

`BLOCKED_WITH_FRONTIER` with recommendation to run kill-tests in order:

`D1 -> D2 -> D3`, then promote whichever survives to `n=4` and `n=5` extension attempts.

