# Fewer additions for <5,5,5> at rank 93: 332 against 383

## What

The file claim/object/5x5x5_m93_cr332_ZT_reduced.json (sha256 9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2) is a ternary straight-line program that exactly computes the 5x5 by 5x5 product with Perminov's 93 products using 332 reduced additions (U 87, V 88, W 157), against 383 for the only 5x5x5 file in his live addition_reduced_ZT directory (recounted by me), with no count for this rank on the Lille 5x5x5 page and a naive +846 in COVERAGE.md.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/5x5x5_m93_cr332_ZT_reduced.json`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (`sym_check.py`, optional, needs sympy).
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 5x5x5 rank 93 | 383 (minimum over his files for this format and rank; one file) | 332 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:14Z |
| Perminov, arXiv:2512.13365, Table 1 | 5x5x5 rank 93 | 383 | 332 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 5x5x5 | rank 93 | rank 93 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:14Z |
| Lille per-format page | 5x5x5 | rank 93; no complexity variant or operation count cited | 332 | https://fmm.univ-lille.fr/5x5x5.html | 2026-10-15T22:25:14Z |
| matmulcatalog COVERAGE.md, adds column | 5x5x5 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 332 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:14Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 5x5x5 rank 93 | lowest count listed for 555-93: 387 over Z (Table 3.3); 384 over Z2 (Table 3.6, not comparable); author's reading of a hand-downloaded PDF | 332 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | PR #186 (Gutierrez and DrZuzzjen, merged 2026-10-15): 358 under the same convention | 332 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:14Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 93, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- This supersedes merged PR #186 (Gutierrez and DrZuzzjen, 358 additions), which is not ours and is listed in the table above.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-93 ternary scheme and its 383-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 93**, cited by the Lille catalogue (https://fmm.univ-lille.fr/5x5x5.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- **Gutierrez and DrZuzzjen**, pull request #186 on this repository (5x5x5 rank 93 at 358 additions), the 5x5x5 result this improves on.
- Contributor credit: `calgulbenkian`.
