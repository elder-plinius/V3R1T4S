# ecc-inversion-addition-chains: secp256k1 scalar inversion, addition chain of length 281

## What
object/chain.txt (sha256 b4c92140602faf399a6aad09073210f46b902351a6b7db3bfa1c848e06d4ce9b) is an addition chain, valid in exact integer arithmetic, of length 281 = 251 doublings + 30 other additions for E = N - 2 = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f (the secp256k1 scalar inversion exponent, d = 2), one step shorter than the shortest published chain for that exponent in the saved copies fetched on 2026-11-10 and 2026-11-12 (Brian Smith's 2026 chain of length 282 = 251 + 31 on additionchains.com; the other saved bars are Smith's 2017 page at 290, addchain results.md at Length 293 and Best Known 290, and TTaoGaming at 288), found by a search seeded from the dictionary of that published 282 chain, with which it shares 173 of its 282 values, and not shown to be optimal or independent of that chain.

Path note: this package was assembled from a run folder, and the panel files use its names. claim/object/ = object/; CLAIM.md = this README.md; REPRODUCE.md = RUN_IT_YOURSELF.md; checkers/ = verify-it-yourself/; rebuild/ = how-we-built-it/; baseline/ = how-we-built-it/baseline/; table/ = the-record-we-beat/ (table/RECORD.md = the-record-we-beat/RECORD.md, table/COMPARATORS.md = the "Compared to" section below). Not shipped: the fetched pages and comparator files (table/smith.html, table/results.md, table/LargeChains.html, table/secp256k1-scalar-inverse-example.txt, table/tt_secp256k1_288.json, table/FETCHES.txt; their URLs, fetch times and hashes are in the-record-we-beat/RECORD.md), and the run's work folders attempts/ and data/.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Python 3 standard library only, no network, under a second on a laptop. The checker rebuilds every chain element with exact integers, checks that each is the sum of two earlier ones and that the last is N-2, and follows the chain to compute x^(N-2) mod N for 100 values of x.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Brian Smith, page at briansmith.org/ecc-inversion-addition-chains-01 (status source) | secp256k1 scalar inversion | 290 = 253 squarings + 37 multiplications | https://briansmith.org/ecc-inversion-addition-chains-01 | 2026-11-10T20:09:02Z; 2026-11-12T18:19:13Z |
| addchain doc/results.md | secp256k1 (Bitcoin) Scalar Inversion | Length 293, Best Known 290 | https://raw.githubusercontent.com/mmcloughlin/addchain/master/doc/results.md | 2026-11-10T20:09:02Z; 2026-11-12T18:20:02Z |
| TTaoGaming/addition-chain-search | chain file for the same exponent | 288 = 253 + 35 | https://raw.githubusercontent.com/TTaoGaming/addition-chain-search/main/review-candidates/certificates/secp256k1_288.json | 2026-11-10T20:09:03Z; 2026-11-12T18:20:02Z |
| Brian Smith (2026), on Neill Clift's "Short Addition Chains for Cryptographic Exponents" | secp256k1 scalar inversion | 282 = 251 doublings + 31 additions | https://additionchains.com/secp256k1-scalar-inverse-example.txt | 2026-11-10T20:32:35Z; 2026-11-12T18:19:13Z |
| this package | object/chain.txt | 281 = 251 doublings + 30 additions | | |

The bar is the lowest public value found, 282 (Brian Smith's 2026 chain, published on additionchains.com on 2 Nov 2026). This chain is 1 shorter: the same number of doublings and one addition fewer.

This chain is seeded from that published chain. The search started from the dictionary of Smith's 282 chain (the 27 values below 2^21 in his file). The final dictionary has 30 values, 24 of them in common with the seed; the seed's 139552, 419427, 1398106 are gone and 289, 70033, 559236, 699062, 1258297, 1817533 are new. The top of the chain (runs of 21, 42, 84 and 126 ones) is the same ladder as in the seed, and so are the last 21 steps; in all, 173 of the chain's 282 values also occur in the seed chain. Trivial edits do not give this length: how-we-built-it/baseline/one_edit.txt scores the seed dictionary and all 662 dictionaries one edit away from it (delete one value, insert one sum of two values, replace one value by such a sum), and none gives less than 282.

Other public values found for this exponent:

Novelty searches of 2026-11-10 (two passes) and a re-check of the bar pages on 2026-11-12. "Length" counts every step.

| source | where | length | how read |
|---|---|---|---|
| Brian Smith 2026, on Neill Clift's "Short Addition Chains for Cryptographic Exponents" | https://additionchains.com/LargeChains.html, file secp256k1-scalar-inverse-example.txt | 282 = 251 + 31 | replayed (the bar) |
| TTaoGaming/addition-chain-search | review-candidates/certificates/secp256k1_288.json, main 88948a7; all branches and open pull requests looked at | 288 = 253 + 35 | replayed |
| Brian Smith's 2017 page; libsecp256k1 before its switch to safegcd; RustCrypto k256; bcoin-org/libtorsion (commit 64eb3cb7b2, src/fields/scalar.h); chjj/mako (92174c30a5); matter-labs/zksync-os (128f90a6cc); mikelodder7/curvey; DanTehrani/secq256k1 | library source | 290 = 253 + 37 | read or replayed by script |
| addchain doc/results.md; Yawning/secp256k1-voi (afa636b3aa); bytemare/secp256k1 (4396377c4f); evmone | addchain-generated code | 293 = 253 + 40 | stated in source |
| gnark-crypto, Zig standard library, fiat-crypto, firedancer, halo2curves | library source | no fixed chain for this exponent (big-integer inverse, divstep, or generic exponentiation) | read |
| mmcloughlin/addchain issue 156 (Neill Clift, 2026-10-22) | GitHub issue | field inversions only | read |
| elder-plinius/V3R1T4S | TROPHY_CASE.md, known-knowns, pull requests (upstream main fb51644, 2026-11-12) | no trophy or known-knowns entry for this target; the open, unmerged pull request 833 lists 293 for this cell (values in unmerged pull requests are not bars) | read |
| GitHub code search for the hexadecimal of n - 2, its limbs, and "secp256k1_scalar_inversion" | default branches only, hits sampled | nothing below 290 other than the two chains above | search |
| arXiv and IACR ePrint, 2024 to 2026 (general web search) | | no paper with a chain for this exponent found | search |

## Not checked, or checked only in part
- Clift's page says Smith supplied a collection of chains and that each downloadable example "has the lowest weighted cost among the supplied chains of the shortest supplied length for that curve" (table/LargeChains.html). So 282 is the shortest length in Smith's supplied collection for this exponent; only that one example can be downloaded.
- NSS upstream (Mercurial) and the BearSSL source tree were not opened (BearSSL does not implement secp256k1).
- mbedTLS, AWS-LC, s2n-bignum, Intel ipp-crypto: code search only.
- Private code, mailing lists, chat servers and social media were not searched.
- GitHub code search covers default branches only.

## Not claimed
- Not a shortest possible chain. No lower bound is shown here.
- Not an independent construction. It is a one-step improvement found by local search from Brian Smith's published 282 chain, as described above. The same program without the seed reached 283 at best.
- Not the only chain of this length: other dictionaries may give 281.
- Nothing about the other exponents of the target (field inversions, or the Curve25519, P-256 and P-384 scalars).
- Not a new method. The construction (a dictionary that is itself an addition chain, a double-and-add main line with overlapping additions, a ladder for the top run of ones) is the one Smith's chain and addchain's dictionary method use; what is new is the dictionary and the resulting length.
- Not a complete survey: the comparison covers the sources listed above. Private code, and public code we did not find, could hold a shorter chain.
- No speed or constant-time claim for any implementation. The length counts group operations only; 251 of the 281 are doublings (squarings).
- Order of work: the rule for this cell (strictly below the published 282, so at most 281) was written into the search folder's work log at about 2026-11-11T20:13Z, before the search that found this chain was started (the queue started at 20:12Z with other jobs; the job that found this chain, seed 1009, started at about 21:13Z; this dictionary was reported at 2026-11-11T21:53:28Z, the chain file written at 2026-11-11T21:54:26Z). This per-cell rule sheet itself was written afterwards, on 2026-11-12T18:23:15Z, and restates that rule. Earlier history of the cell: a first rule sheet (PREREG.original.md, 2026-11-10) named the bars then known (290, later 288); on 2026-11-10T20:32Z we found Brian Smith's 2026 chain of length 282 and withdrew a planned 284 claim before filing. See how-we-built-it/PREREG.md.
- Composition: the chain is not a composition of published chains (nothing is glued or concatenated). It is seeded from one, named above.

## Credits
- Brian Smith: the 282 chain this result was grown from (2026, published on additionchains.com), and the 2017 page "ECC inversion addition chains" that the target tracks, https://briansmith.org/ecc-inversion-addition-chains-01.
- Neill Clift: "Short Addition Chains for Cryptographic Exponents", https://additionchains.com/LargeChains.html, where the 2026 chains are published and checked.
- Michael McLoughlin: addchain and its results table, https://github.com/mmcloughlin/addchain. The dictionary method used here is the family addchain implements.
- TTaoGaming/addition-chain-search, https://github.com/TTaoGaming/addition-chain-search: the 288 chain for this exponent.
- Earlier work on these chains named by the target: Bernstein, Gueron, Krasnov, Dettman, Wuille.
- The V3R1T4S bank entry ecc-inversion-addition-chains, whose suggested angles (joint choice of windows and dictionary, annealing over dictionary terms) this search follows. No earlier V3R1T4S package for this target was found (TROPHY_CASE.md and known-knowns at upstream main fb51644).
- What is new here: a dictionary of 30 values and a chain of length 281 for this exponent, one step below the shortest published chain.
- Contributor: Abshalom Dayan (V3R1T4S run).
