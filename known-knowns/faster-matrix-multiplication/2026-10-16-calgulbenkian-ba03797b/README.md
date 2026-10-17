# Fewer additions for <2,4,7> at rank 45: 169 against 174

## What

claim/object/2x4x7_m45_cr169_ZT_reduced.json (sha256 ba03797bb02013423a43e98b27ac46c6897018e12f9e90f0761e874c402070d7) is a ternary straight-line program over the inputs that exactly computes the 2x4 times 4x7 product with the 45 products of Perminov's rank-45 scheme (same U, V, W rows as his file), using 169 reduced additions (U 35, V 67, W 67) against his only 2x4x7 rank-45 count of 174, with no lower count on the Lille page or in the COVERAGE.md adds column (naive 308) as fetched 2026-10-15.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/2x4x7_m45_cr169_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 2x4x7 rank 45 | 174 (minimum over his files for this format and rank; one file) | 169 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:39Z |
| Perminov, arXiv:2512.13365, Table 1 | 2x4x7 rank 45 | 174 | 169 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 2x4x7 | rank 45 | rank 45 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:39Z |
| Lille per-format page | 2x4x7 | rank 45; no complexity variant or operation count cited | 169 | https://fmm.univ-lille.fr/2x4x7.html | 2026-10-15T22:25:39Z |
| matmulcatalog COVERAGE.md, adds column | 2x4x7 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 169 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:39Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 2x4x7 rank 45 | rows for this scheme code appear in the paper's tables (over Z and/or Z2); every listed count is above the reference, see panel/novelty.md: 247-45       308         181        177          0, 0.26, 0           - / 247-45         308       180       176     132   42.9       0, 0.21, 0 | 169 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 169 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:39Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 45, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-45 ternary scheme and its 174-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 45**, cited by the Lille catalogue (https://fmm.univ-lille.fr/2x4x7.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
