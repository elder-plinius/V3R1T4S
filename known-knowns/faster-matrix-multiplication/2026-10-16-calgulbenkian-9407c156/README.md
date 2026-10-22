# Fewer additions for <3,5,5> at rank 58: 211 against 221

## What

The program claim/object/3x5x5_m58_cr211_ZT_reduced.json (sha256 9407c156647ed8a24fbd9e29d7f644e1fd6281aabc4eaa317bb5cb3a3a9b5b23) is, on my checks, a ternary straight-line program for the rank-58 scheme for <3,5,5> (the same 58 products as Perminov's cr221 file) that exactly computes A*B over Z and uses 211 reduced additions (U 48, V 69, W 94), below 221, the only addition_reduced_ZT count for this format and rank in his live tree on 2026-10-15, and below the +413 naive adds in matmulcatalog COVERAGE.md; the Lille 3x5x5 page cites no operation count.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/3x5x5_m58_cr211_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 3x5x5 rank 58 | 221 (minimum over his files for this format and rank; one file) | 211 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:31Z |
| Perminov, arXiv:2512.13365, Table 1 | 3x5x5 rank 58 | 221 | 211 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 3x5x5 | rank 58 | rank 58 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:31Z |
| Lille per-format page | 3x5x5 | rank 58; no complexity variant or operation count cited | 211 | https://fmm.univ-lille.fr/3x5x5.html | 2026-10-15T22:25:31Z |
| matmulcatalog COVERAGE.md, adds column | 3x5x5 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 211 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:31Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 3x5x5 rank 58 | lowest count listed for 355-58: 222 over Z (Table 3.3); 220 over Z2 (Table 3.6, not comparable; below the reference 221, above our 211); author's reading of a hand-downloaded PDF | 211 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 211 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:31Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 58, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-58 ternary scheme and its 221-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 58**, cited by the Lille catalogue (https://fmm.univ-lille.fr/3x5x5.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
