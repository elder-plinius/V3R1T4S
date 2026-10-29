# Fewer additions for <2,5,5> at rank 40: 147 against 153

## What

claim/object/2x5x5_m40_cr147_ZT_reduced.json (sha256 62737a117df29bc9dc6194509ed47f95a6f763ea3ca21fca84f79a78c44e6e1a) is an exact ternary straight-line program for the rank-40 <2,5,5> scheme with Perminov's product set using 147 reduced additions (U 31, V 54, W 62), strictly below the 153 of his only live addition_reduced_ZT file for that format and rank, with Lille's page citing no operation count and COVERAGE.md's adds column being a naive count under another convention.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/2x5x5_m40_cr147_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 2x5x5 rank 40 | 153 (minimum over his files for this format and rank; one file) | 147 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:36Z |
| Perminov, arXiv:2512.13365, Table 1 | 2x5x5 rank 40 | 153 | 147 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 2x5x5 | rank 40 | rank 40 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:36Z |
| Lille per-format page | 2x5x5 | rank 40; no complexity variant or operation count cited | 147 | https://fmm.univ-lille.fr/2x5x5.html | 2026-10-15T22:25:36Z |
| matmulcatalog COVERAGE.md, adds column | 2x5x5 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 147 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:36Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 2x5x5 rank 40 | lowest count listed for 255-40: 154 over Z (Table 3.3); 144 over Z2 (Table 3.6, a scheme with naive count 256, not comparable; below the reference 153 and below our 147, which is over Z); author's reading of a hand-downloaded PDF | 147 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 147 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:36Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 40, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-40 ternary scheme and its 153-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 40**, cited by the Lille catalogue (https://fmm.univ-lille.fr/2x5x5.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
