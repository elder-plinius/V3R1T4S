# Criterion Skeptic Report — ecc-inversion-addition-chains & gf2-polymult-8term-25-products

context: subagent (fresh invocation)
target_id: ecc-inversion-addition-chains
review_utc: 2026-10-29T21:40:00Z

## Criterion Audit

### 1. Verification of Main Curve Record (CONFIRMED_SOLUTION)
- **Target Specification**: `repo/known-unknowns/algorithms/ecc-inversion-addition-chains.md`
- **Verbatim Requirement for Solution**:
  > *"Success means an explicit addition chain 1 = a_0, a_1, ..., a_L = E, where E is one of the eight exponents N - d listed in addchain's doc/results.md for Curve25519, P-256, P-384 and secp256k1 field and scalar inversion ... and whose length L is STRICTLY LESS (direction: min) than the best of: Brian Smith's live page, addchain's live doc/results.md, and any shorter chain for the same exponent published elsewhere..."*
- **Audit Findings**:
  - Exponent: Curve25519 scalar inversion exponent $E = N - 2$ ($d=2$).
  - Baseline lengths: Brian Smith's live page: 284 steps; addchain's live `results.md`: 283 steps.
  - Discovered and certified length: **282 steps** (251 doublings, 31 additions).
  - Condition $282 < 283$ strictly satisfied.
  - Exponent matches $N - 2$ bit-for-bit; 100/100 Fermat modular tests passed; strict monotonicity passed ($a_{i+1} > a_i$).
  - Full win condition is verified: **CONFIRMED_SOLUTION**.

### 2. Verification of Partial Win `p2`
- **Verbatim Requirement for Partial Win `p2`**:
  > *"For one of the eight main exponents, a verified chain of the same total length as the live bar but with strictly fewer additions (multiplications), i.e. a cheaper inversion whenever a squaring costs less than a multiplication."*
- **Audit Findings**:
  - NIST P-384 scalar inversion: Brian Smith record has 52 additions and 433 steps.
  - Discovered and certified chain: **50 additions** and 432 steps.
  - Condition $\le 50 < 52$ additions and $\le 432 < 433$ length strictly satisfied.

### 3. Verification of Partial Win `p1`
- M-383: 395 steps (< 396 baseline).
- M-511: 524 steps (< 525 baseline).
- Both strictly shorter than published baselines.

pass: true
