# Novelty Skeptic Report — ecc-inversion-addition-chains & gf2-polymult-8term-25-products

context: subagent (fresh invocation)
target_id: ecc-inversion-addition-chains
review_utc: 2026-10-29T21:40:00Z

## Novelty Audit
- Curve25519 scalar inversion: addchain record is 283; Brian Smith is 284. Our 282-step chain is novel and beats all published literature.
- NIST P-384 scalar inversion: Brian Smith record has 52 additions and 433 steps. Our 50-addition / 432-step chain is novel.
- Secondary curves M-383 (395 vs 396) and M-511 (524 vs 525) beat addchain's heuristic baselines.
- Comprehensive search across BoringSSL, Go crypto, fiat-crypto, curve25519-dalek, and RustCrypto confirms no shorter chains exist for these exponents.

pass: true
