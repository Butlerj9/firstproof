# EXP-27: Scout Reconciliation Matrix — P03

Date: 2026-02-13
Sources: GPT-pro R2 (2026-02-13), Claude Research R3 (2026-02-13)
Lane: P03 (Symmetry Conjecture n≥5)

---

## Claim Compatibility Matrix

| Claim Category | GPT-pro R2 | Claude Research R3 | Relation |
|---------------|-----------|-------------------|----------|
| **Lane verdict** | BLOCKED_WITH_FRONTIER | BLOCKED_WITH_FRONTIER | **COMPATIBLE** |
| **Blocker statement** | No theorem for lower-degree interpolation correction symmetry at n≥5 | No structural characterization of lower-degree correction terms forcing S_n symmetry for general n | **COMPATIBLE** (same gap, different phrasing) |
| **Minimal bridge lemma** | (T_i − t)E*_{λ⁻} divisible by (1−q), so q→1 limit satisfies Hecke eigenrelation | Moebius-weighted cancellation of non-symmetric permutation factors under Sahi binomial inversion | **COMPLEMENTARY** (different mechanisms toward same goal) |
| **Route family 1** | LRW/Sahi binomial expansion + AS q=1 structure | D1: BinAS (Sahi binomial inversion + AS factorization) | **OVERLAPPING** (same ingredients: Sahi formula + AS result) |
| **Route family 2** | Direct (1−q)-divisibility of (T_i − t)E* | (no direct analog; closest is D3 SSD duality) | **UNIQUE to GPT-pro** |
| **Route family 3** | BDW signed multiline queue factorization at q=1 | D2: SMLQ (signed multiline queue involution at q=1) | **OVERLAPPING** (same BDW formula, different exploitation) |
| **Route family 4** | — | D3: SSD (Sahi-Stokman evaluation duality at q=1) | **UNIQUE to Claude Research** |
| **Kill-test 1** | R_i(q) = ((T_i−t)E*)/(1−q) bounded near q=1 | D1: n=3 symbolic BinAS coefficient cancellation | **COMPLEMENTARY** |
| **Kill-test 2** | LRW support-collapse at q=1 | D2: n=3 signed queue enumeration + coefficient pairing | **COMPLEMENTARY** |
| **Kill-test 3** | BDW queue-normalized inversion normalization | D3: n=3 staircase-permuted spectral evaluation σ-independence | **COMPLEMENTARY** |
| **Stop-loss** | If divisibility shows blow-up → deprioritize | If D1-D3 all fail kill-tests → park remaining 11 routes | **COMPATIBLE** |
| **Prior x-dependence claim** | CORRECTED in R2 (R1 had misunderstanding; R2 focuses on divisibility) | Not present (never made this error) | **RESOLVED** |

## Key Observations

1. **Convergent assessment**: Both scouts agree the blocker is the same (lower-degree correction symmetry) and no closure route is immediately available. This is consistent with our own Session 22 assessment.

2. **Complementary bridge lemmas**: GPT-pro's divisibility lemma ((T_i−t)E* ∈ (1−q)·R) and Claude Research's BinAS Moebius cancellation are structurally different approaches to the same target. Neither has been tested against lane data.

3. **Shared ingredient**: Both scouts invoke the Sahi binomial formula and AS q=1 structure (GPT-pro Route 1 ≈ Claude Research D1). This is the highest-confidence overlapping signal.

4. **Unique routes**: GPT-pro's (1−q)-divisibility is unique and directly testable with existing infrastructure. Claude Research's SSD duality is unique but has spectral collision risk.

5. **No closure claim**: Neither scout claims closure. Both provide route suggestions with explicit kill-tests. This is appropriate given the L5 barrier.
