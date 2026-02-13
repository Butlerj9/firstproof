# EXP-29: Scout Conflict Audit — P03

Date: 2026-02-13
Purpose: Test scout claims against established lane facts

---

## Lane Facts (ground truth)

| Fact ID | Source | Statement |
|---------|--------|-----------|
| F1 | EXP-5b | At q=1, vanishing system has 50-dim null space (n=3); symmetric subspace: 14-dim. Vanishing alone does NOT determine E*. |
| F2 | EXP-20 | Branching rule induction blocked by 4 independent obstructions (partition mismatch, lost T_{n-2}, antidominant vanishes, limit≠specialization). |
| F3 | EXP-3b | f*_{(0,2)}/f*_{(2,0)} = 1/t EXACTLY at q=1 limit (n=2). x-INDEPENDENT. |
| F4 | EXP-4 | (T_i − t)E*_{λ⁻} = O(1−q) as q→1 (numerical, n=3, multiple t). |
| F5 | EXP-20 #4 | E*_μ from Hecke ops at q=1 ≠ f*_μ = lim_{q→1} E*(q). Specialization ≠ limit. |
| F6 | Session 11 | Leading term E_{λ⁻}(x;1,t) is symmetric for all n (AS 2019 + Hecke extension). Lower-degree corrections NOT covered. |
| F7 | Memory | Spectral vectors collapse at q=1: C(D+n,n) → n! distinct. Interpolation uniqueness requires generic q. |

---

## Conflict Audit

### GPT-pro R2 Claims

| GPT-pro Claim | Compatible with Lane Facts? | Verdict |
|--------------|---------------------------|---------|
| (T_i − t)E* divisible by (1−q) | **COMPATIBLE** with F4 (numerical O(1−q) convergence observed). Not proved. | **KEEP** — testable, consistent with evidence |
| LRW/Sahi binomial expansion collapses at q=1 | **NEEDS TEST** — at q=1 spectral collision (F7) may cause coefficient divergence. Not directly contradicted but F7 is a risk factor. | **KEEP with caution** |
| BDW queue factorization at q=1 | **COMPATIBLE** — does not conflict with any known fact. Requires BDW formula implementation. | **KEEP** — dependency-blocked |
| "Fastest closure = divisibility lemma" | **COMPATIBLE** — divisibility is the most testable claim with existing tools. | **KEEP** |

### Claude Research R3 Claims

| Claude Research Claim | Compatible with Lane Facts? | Verdict |
|----------------------|---------------------------|---------|
| Sahi-Knop integrality ⟹ limit = specialization | **CONTRADICTED by F5** (EXP-20 finding #4). At q=1 the Hecke specialization gives DIFFERENT objects from the q→1 limit. The "integrality" claim needs careful scoping — it may hold for the polynomial coefficients (which are in Z[q,t]) but does NOT mean the q=1 specialization equals the q→1 limit. | **QUARANTINE** — do not adopt without independent verification |
| D1 BinAS: Moebius inversion on Knop poset + AS termwise | **COMPATIBLE with F6** (AS leading term symmetric). Risk: Moebius coefficients involve Knop partial order which depends on spectral vectors → F7 collision risk. | **KEEP with caution** |
| D2 SMLQ: adjacent-transposition involution at q=1 | **COMPATIBLE** — no direct conflict. Independent of F1-F7. | **KEEP** |
| D3 SSD: Sahi-Stokman evaluation duality at q=1 | **AT RISK from F7** — evaluation duality uses spectral vectors η_σ. At q=1 these collapse (F7), making the duality potentially trivial or undefined. | **KEEP with strong caution** |
| "14 novel candidate families" | Most are compatible. Approaches 10 (vanishing dimension count) is **CONTRADICTED by F1** (vanishing space is 14-dim, not 1-dim). Previously assessed and dropped (Session 22 audit). | **Approach 10: QUARANTINE** (confirmed incompatible) |

---

## Quarantined Claims

| Claim | Source | Conflict | Status |
|-------|--------|----------|--------|
| Sahi-Knop integrality ⟹ limit = specialization (unconditionally) | Claude Research R3 | F5: specialization ≠ limit at q=1 | **QUARANTINE** — may be a scoping issue, not wholesale wrong. Integrality ensures limit exists; does NOT ensure limit = specialization. |
| Approach 10: vanishing dimension count forces symmetry | Claude Research R3 (inherited from R1) | F1: symmetric null space is 14-dim, not 1-dim | **QUARANTINE** — confirmed incompatible (Session 22 audit already dropped this) |
| GPT-pro R1: x-dependent Mallows claim | GPT-pro R1 (NOT R2) | F3: x-independent proved exactly for n=2 | **QUARANTINE** — corrected in R2 |

---

## Summary

- **No fatal conflicts** in the R2/R3 routes that survive de-dup.
- **One quarantined claim** (integrality⟹limit=specialization) — important to scope correctly but does not kill any route.
- **All proposed routes are testable** without adopting quarantined claims.
- **Spectral collision (F7)** is the main risk factor for BinAS, SSD, and any Knop-poset-based approach.
