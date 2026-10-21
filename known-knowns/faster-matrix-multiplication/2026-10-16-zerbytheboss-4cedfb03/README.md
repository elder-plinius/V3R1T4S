# Fewer additions for <3,4,4> at rank 38: 124 against 125

## What

The ternary straight-line program object/3x4x4_m38_cr124_ZT_reduced.json computes the <3,4,4> matrix product exactly over Z at rank 38 (the best rank in fmm_sota.json) using 124 additions/subtractions under Perminov's reduced convention, strictly fewer than the 125 of the best file for 3x4x4 at rank 38 in Perminov's live addition_reduced_ZT directory on 2026-10-16, with no lower count on the Lille page or in COVERAGE.md; no claim of optimality or of other formats.

The output C is indexed transposed (k,i), matching Perminov's cyclic layout; the checkers use the same convention.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library only.
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Perminov, FastMatrixMultiplication, addition_reduced_ZT | 3x4x4 rank 38 | 125 (minimum over two files: 125, 133) | 124 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-16T17:43:11Z |
| fmm_sota.json (Sedoglavic) | 3x4x4 | rank 38 | rank 38 (eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-16T17:43:15Z |
| Lille per-format page | 3x4x4 | rank 38; no operation count | 124 | https://fmm.univ-lille.fr/3x4x4.html | 2026-10-16T17:43:13Z |
| matmulcatalog COVERAGE.md, adds column | 3x4x4 | naive count +216, not comparable | 124 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-16T17:43:14Z |
| V3R1T4S open and closed pull requests | this target | none | 124 | https://github.com/elder-plinius/V3R1T4S | 2026-10-16 |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- The margin is a single addition (124 vs 125). IACR ePrint 2026/849 (Mårtensson and Stankovski Wagner) lists a 344-38 scheme that neither our panel nor the repository reviewers could read (the PDF is behind a challenge page, and their repository includes a Moosbauer <3,4,4>:38 scheme); the comparison here stands against Perminov, Lille and COVERAGE.md.
- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: rank 38 is the best known rank; the claim is the number of additions only.
- Counts after a change of basis (Karstadt-Schwartz) or over other rings are a different quantity and are not compared.
- The Perminov "Z" figure in reduced_known.json (198) is a different measure and is not compared.
- Not peer reviewed. Checked by the standalone checkers shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the reduced-scheme JSON layout, the counting convention, the ternary addition reducer used inside the search, the schemes used as starting points, and the value compared against.
- **A. V. Smirnov** (2013, *Computational Mathematics and Mathematical Physics* 53(12), 1781–1795): the <3,4,4> rank-38 algorithm cited by the Lille catalogue (`https://fmm.univ-lille.fr/3x4x4.html`).
- **A. Sedoglavic**, the Lille catalogue and fmm_digest (fmm_sota.json): best-known ranks.
- **solven-eu/matmulcatalog** (COVERAGE.md): catalogue compared against.
- **Kauers and Moosbauer** and the flip-graph literature (arXiv:2212.01175): the flip-graph walk idea used to move between schemes of equal rank.
- **V3R1T4S** contributors whose packages set the layout and checkers (check_slp.py is adapted from an existing package in this repository).
- Contributor credit: Zerbytheboss (the `HindsightWise` GitHub account is operated by Zerbytheboss).
