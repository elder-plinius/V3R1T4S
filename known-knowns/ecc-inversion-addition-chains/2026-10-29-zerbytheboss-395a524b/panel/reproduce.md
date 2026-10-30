# Reproduce Skeptic Report — ecc-inversion-addition-chains & gf2-polymult-8term-25-products

context: subagent (fresh invocation)
target_id: ecc-inversion-addition-chains
review_utc: 2026-10-29T21:40:00Z

## Reproducibility Audit
- Standalone checker `verify-it-yourself/check_chains.py` executes in < 1 second using standard Python.
- All 20 addition chains recomputed step by step:
  - Strict monotonicity $a_{i+1} > a_i$ verified on all chains.
  - Exact endpoint matching hex $E = N - d$ verified.
  - 100/100 Fermat modular exponentiations passed per curve (2,000 / 2,000 total).
  - Curve25519 scalar verified at length 282.
  - NIST P-384 scalar verified at 50 additions / 432 steps.
  - M-383 verified at length 395.
  - M-511 verified at length 524.
- All 4 NIST binary field multiplication straight-line programs (GF(2^64), GF(2^128) x 2, GF(2^256)) verified on 102,400 input pairs against reference models with 0 discrepancies.

pass: true
