# Fewer additions for <2,4,8> at rank 51: 181 against 188

## What

claim/object/2x4x8_m51_cr181_ZT_reduced.json (sha256 e5f0f3807baaa5f00a76f606bd33199db83dfd83ef82c21abbcb0fbc79c02d95) is a ternary straight-line program that exactly computes the full 2x4 times 4x8 product over Z with Perminov's own 51 products, using 181 additions under the reduced convention (U 37, V 67, W 77), against 188 for his only live 2x4x8 file, with no lower addition count on the Lille page, in reduced_known.json, or in COVERAGE.md, as fetched on 2026-10-15.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same file, with identical bytes, is `object/2x4x8_m51_cr181_ZT_reduced.json`.

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
| Perminov, FastMatrixMultiplication, addition_reduced_ZT (live repository) | 2x4x8 rank 51 | 188 (minimum over his files for this format and rank; one file) | 181 | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-15T22:25:32Z |
| Perminov, arXiv:2512.13365, Table 1 | 2x4x8 rank 51 | 188 | 181 | https://arxiv.org/abs/2512.13365 | 2026-10-15 |
| fmm_sota.json (Sedoglavic), best known rank | 2x4x8 | rank 51 | rank 51 (same scheme rank; eligibility) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-15T22:25:32Z |
| Lille per-format page | 2x4x8 | rank 51; no complexity variant or operation count cited | 181 | https://fmm.univ-lille.fr/2x4x8.html | 2026-10-15T22:25:32Z |
| matmulcatalog COVERAGE.md, adds column | 2x4x8 | naive count nz(U)+nz(V)+nz(W)-2r-np, not comparable | 181 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-15T22:25:32Z |
| Martensson and Stankovski Wagner, IACR ePrint 2026/849 | 2x4x8 rank 51 | lowest count listed for 248-51: 190 over Z (Table 3.3); 183 over Z2 (Table 3.6, not comparable; below the reference 188, above our 181); author's reading of a hand-downloaded PDF | 181 | https://eprint.iacr.org/2026/849 | 2026-10-15 (hand download) |
| V3R1T4S TROPHY_CASE.md and open pull requests | this target | none | 181 | https://github.com/elder-plinius/V3R1T4S | 2026-10-15T22:25:32Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; nothing is known about the minimum number of additions for this format and rank.
- No new rank: the scheme has rank 51, the best known rank, and the claim is the number of additions only.
- Counts after a change of basis (the Karstadt-Schwartz framework) or over other rings are a different quantity and are not compared.
- Other formats improved in the same sweep are separate packages, one cell each.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, FastMatrixMultiplication (https://github.com/dronperminov/FastMatrixMultiplication), arXiv:2512.13365 and arXiv:2511.20317: the rank-51 ternary scheme and its 188-addition program, the reduced-scheme JSON layout, the counting convention, and the table value compared against.
- **the Lille catalogue entry for rank 51**, cited by the Lille catalogue (https://fmm.univ-lille.fr/2x4x8.html) for the rank.
- **J. Boyar and R. Peralta**, "A new combinational logic minimization technique with applications to cryptology", SEA 2010: the distance-guided heuristic our search extends.
- **E. Martensson and P. Stankovski Wagner**, IACR ePrint 2026/849 (and ACDA25): addition reduction without change of basis, compared against.
- **A. Bostan, G. Lecerf and E. Schost**, "Tellegen's principle into practice", ISSAC 2003: the transposition principle used for the W map.
- **DrZuzzjen**, pull request #149 on this repository (<4,6,7> at 503 additions), whose use of the transposition principle on the W map prompted our W^T search.
- **solven-eu/matmulcatalog** (COVERAGE.md) and **A. Sedoglavic** (fmm_digest, fmm_sota.json): the catalogues compared against.
- Contributor credit: `calgulbenkian`.
