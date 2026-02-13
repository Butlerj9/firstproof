# EXP-30: Selected Route Plan — P03

Date: 2026-02-13
Selected route: **R1-DIV** ((1-q)-divisibility kill-test)

---

## Target Statement

**Divisibility Lemma**: For each simple reflection s_i (i=0,...,n-2), the quantity (T_i − t)E*_{λ⁻}(x; q, t) is divisible by (1−q) in Q(t)[q,x].

**Consequence**: If true, then at q=1: (T_i − t)(lim_{q→1} E*_{λ⁻}) = 0, i.e., T_i g = tg for all i, i.e., g is symmetric. This proves the Symmetry Conjecture for all n simultaneously (if the divisibility holds for all n).

---

## Implementation Plan

### Step 1: Compute (T_i − t)E*_{λ⁻} at exact q values (n=3)

**Script**: `exp32_divisibility_test.py`

1. For n=3, λ⁻=(0,2,3), compute E*_{λ⁻}(x; q, t) at ~15 exact rational q values using existing Fraction perturbation infrastructure (order-4, adapted from exp13b).
2. At each q, compute T_0 E*_{λ⁻} and T_1 E*_{λ⁻} using the Hecke operator formula.
3. Form D_i(q) = (T_i − t)E*_{λ⁻} — this is a polynomial in x with coefficients depending on q,t.
4. Divide each coefficient of D_i(q) by (1−q) using exact Fraction arithmetic.
5. Check: is the quotient well-defined (no remainder)? Is it bounded?

**Stop-loss**: If at any q value the division has nonzero remainder, the divisibility hypothesis fails → stop, report, fall back to R2-BinAS.

### Step 2: Characterize R_i(q,t) (if Step 1 passes)

1. Compute R_i(q) = D_i(q)/(1−q) at all 15 q values.
2. Apply rational interpolation (Padé) to determine the degree of R_i as a rational function of q.
3. Evaluate R_i(1) (either by interpolation or direct limit).
4. If R_i(1) = 0: the divisibility is of order ≥ 2 (even stronger). Verify.

### Step 3: Test at n=4 (if Step 2 succeeds)

1. Adapt the n=4 modular perturbation solver (exp15g) to compute (T_i − t)E*_{λ⁻} mod primes.
2. Check divisibility by (1−q) mod p at several q values.
3. If passes: strong structural evidence for general n.

### Step 4: Structural proof attempt (if Steps 1-3 pass)

Look for an algebraic identity explaining WHY the divisibility holds:
- Knop-Sahi characterization + Hecke operator calculus
- Leading term is a Hecke eigenvector (AS result); the correction terms satisfy recursion relations that force divisibility
- Connection to the (1-q) factor in the spectral vector formula ν̃_i = q^{ν_i} · t^{-k_i}

---

## Kill-test Criteria

| Test | PASS | FAIL |
|------|------|------|
| Step 1: (1-q) divides D_i(q) exactly | All 15 q-values, both T_0 and T_1, zero remainder | Any nonzero remainder at any q |
| Step 2: R_i(q) bounded at q=1 | R_i(1) finite (determined by interpolation) | Pole at q=1 |
| Step 3: n=4 divisibility | Holds mod both primes at ≥5 q-values | Any failure |

---

## Stop-loss Gates

1. Step 1 failure → fall back to R2-BinAS (Rank 2 route)
2. Step 2 pole → fall back to R2-BinAS
3. Step 3 failure → report n=3-only phenomenon, reassess
4. Step 4 stalls after one bounded cycle → report frontier delta, no symbolic sprawl

---

## Resource Estimate

- Step 1: ~5 minutes (n=3 Fraction computation, 15 q-values × 2 operators)
- Step 2: ~2 minutes (rational interpolation)
- Step 3: ~30-60 minutes (n=4 modular, ~5 q-values × 2 primes)
- Step 4: unbounded (capped at one cycle by stop-loss)
