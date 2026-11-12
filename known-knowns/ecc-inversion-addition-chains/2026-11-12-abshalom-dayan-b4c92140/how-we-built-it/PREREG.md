# PREREG: secp256k1 scalar inversion (per-cell rule sheet)

written: 2026-11-12T18:23:15Z (date -u), before claim/ for this cell was built.

Honest order of events: the rule for this cell (strictly below the published 282, so at most 281) was written into the search folder's work log at about 2026-11-11T20:13Z, before the search that found this chain was started (20:12Z start of the queue; this dictionary was reported at 2026-11-11T21:53:28Z, the chain file written at 2026-11-11T21:54:26Z). This per-cell rule sheet itself was written afterwards, on 2026-11-12T18:23:15Z, and restates that rule. Earlier history of the cell: a first rule sheet (PREREG.original.md, 2026-11-10) named the bars then known (290, later 288); on 2026-11-10T20:32Z we found Brian Smith's 2026 chain of length 282 and withdrew a planned 284 claim before filing.

## Criterion (verbatim from bank)
Success means an explicit addition chain 1 = a_0, a_1, ..., a_L = E, where E is one of the eight exponents N - d listed in addchain's doc/results.md for Curve25519, P-256, P-384 and secp256k1 field and scalar inversion (d=3 for the P-256, P-384 and secp256k1 field entries; d=2 for the Curve25519 field entry and all four scalar entries), in which every a_i (i >= 1) equals a_j + a_k for some j, k < i (j = k is a doubling), checked with exact integer arithmetic, and whose length L is STRICTLY LESS (direction: min) than the best of: Brian Smith's live page, addchain's live doc/results.md, and any shorter chain for the same exponent published elsewhere (papers or library source such as BoringSSL, Go crypto, fiat-crypto, RustCrypto, curve25519-dalek, libsecp256k1 before its switch to safegcd), which the claimant must search for and cite. Bars on 2026-10-25 (Smith's page, last updated 3 Sep 2017, and addchain's results.md, whose own Curve25519 scalar chain of 283 beats its Best Known column of 284): Curve25519 field 265, P-256 field 266, P-384 field 396, secp256k1 field 269, secp256k1 scalar 290, P-256 scalar 292, P-384 scalar 433, Curve25519 scalar 283. Include the best valid composition of published objects for the same parameters and metric in the bar, even if it is absent from a printed table. State whether the candidate is a composition. Identify its components and composition rule. Values in unmerged pull requests are not bars.

## Checker and thresholds
- Object: a file of index pairs, one per step; a_t = a_j + a_k with j, k < t, a_0 = 1.
- Checker: a standalone Python program written from the definition (exact integers): every index refers to an earlier element, the last element equals N-2 with N derived from the standard (SEC 2 version 2.0 section 2.4.1: n = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141) and equal to the hexadecimal in addchain's results.md, and x * x^E = 1 mod N for 100 nonzero x following the chain.
- Threshold: length L strictly below every public length for this exponent: Smith's page 290, results.md 293 (Best Known 290), TTaoGaming 288, Smith 2026 on additionchains.com 282. So L <= 281.
- Composition and seed statement: say whether the chain is a composition of published chains, and name any published chain the search started from.
- Baseline for a seeded result: the best length among all one-edit neighbours of the seed's dictionary (delete one value, insert one sum, replace one value by one sum). The claim needs a length below that baseline too.
- Kill condition: any public chain of length <= ours for this exponent removes the claim.

null_test: not needed because the claim is an explicit object checked by a deterministic exact-integer checker against table values; no statistic is estimated.

## Not claimed
Optimality; any field-inversion cell; any other curve; an independent (unseeded) construction; running time of an implementation.
