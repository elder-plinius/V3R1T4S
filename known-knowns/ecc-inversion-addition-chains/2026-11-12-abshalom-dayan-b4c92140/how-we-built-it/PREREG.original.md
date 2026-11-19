# PREREG: shorter addition chains for ECC scalar inversion exponents

Written 2026-11-10 19:50 CET. Honest timing note: the search code and a 4-minute test run
existed before this file; the test already produced sub-bar chains (logged in FINDINGS.md).
The success rule below is the target file's own rule and was not tuned to those results.

Target: known-unknowns/algorithms/ecc-inversion-addition-chains.md (V3R1T4S).
Cells: scalar inversion exponent N-2 for Curve25519, P-256, secp256k1, P-384.
Bars (addchain doc/results.md and B. Smith's page, fetched 2026-11-10, in sources/):
283, 292, 290, 433. Open unmerged PR #833 claims 282 (Curve25519) and 432 (P-384).

Success rule (frozen): an explicit sequence a_0 = 1, ..., a_L = N-2 with every a_t = a_i + a_j,
i, j < t, and L strictly below the bar (and strictly below #833's numbers where it has one).
L counts every step, doublings included. Check: src/build_chain.py check_chain(), exact
integers, plus x * x^(N-2) == 1 mod N on 100 seeded x.

Not claimed: optimality; anything about field exponents; constant-time or performance wins
beyond the operation count.

Kill conditions: a public chain of equal or shorter length for a cell (novelty search over
library sources and literature) removes that cell from any claim.

Amendment 2026-11-10 20:30 CET (before any claim): the novelty search found shorter public
chains (TTaoGaming/addition-chain-search): 279, 284, 288, 421. A cell is claimable only if
strictly shorter than these too: <= 278, <= 283, <= 287, <= 420.
