# Fast matrix multiplication: format 11x14x16 in rank 1547, class ZT

## What

The file `object/11x14x16_m1547_ZT.json` is an exact integer (class ZT, largest absolute coefficient 1) bilinear scheme of rank 1547 for the 11x14x16 format whose Brent equations hold over Z. Rank 1547 is strictly below the ZT rank 1550 in Perminov's live rank table (`docs/ranks.md`, fetched 2026-10-26T16:55:46Z) and not below the overall best rank 1520. No ZT-class scheme file for this format below 1550 was in the two named repositories when they were fetched on 2026-10-18.

**Route.** The scheme is the block composition of #410 (rank 1540, class Z), split mechanically into ternary terms (rank 1548), then lowered by one term by a ternary flip-graph search (rank 1547). The claim is that one-term saving below the composition-plus-split value 1548. `HOW_WE_FOUND_IT.md` gives the steps, and `how-we-built-it/rebuild.sh` reruns the split and the search and reproduces the object exactly.

**Encoding.** The panel checked the original file `object/11x14x16_m1547_ZT.json` (dense rows, 1743002 bytes) with sha256 `2a7d22e9c0e1881aeedfe29f53a8d2423673ca7dbf827f4eece7a598d2a93da7`. That file is over the 1,000,000-byte limit, so this package holds a lossless re-encoding of it under the same name (`"encoding": "sparse_flat_pairs"`, 249977 bytes, sha256 `8a3529b5faa6980bfd9cfa355ead52b93efec2cb36f6d6f2ab076a43e1215922`). Entry-by-entry comparison with the original found no difference; see `verify-it-yourself/RECEIPTS.md`. `INDEX.csv` and `SHA256SUMS` carry the re-encoded file's hash, and the submission id uses it. `panel/gate.md` names the original's hash.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: under one minute.
- **Expected last line**: `ALL CHECKS PASS`

The run checks the object's sha256 against `INDEX.csv`, the Brent equations exactly over the integers (no floating point, no sampling), the coefficient class, and that a copy with one sign flipped is rejected.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Perminov `docs/ranks.md` (live rank table) | 11x14x16 | ZT rank 1550 (live columns: ZT 1550, Z 1540, Q 1520) | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-26T16:55:46Z |
| Perminov `README.md` (dated note: it carried the same table on 2026-10-18; the table now lives in `docs/ranks.md`) | 11x14x16 | ZT rank 1550 (columns then: ZT 1550, Z 1550, Q 1520) | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-18T14:20:53Z |
| Composition bar: #410's block composition (rank 1540, class Z) split into ternary terms | 11x14x16 | ZT rank 1548 | `how-we-built-it/rebuild.sh`, step 2 | 2026-10-25 |
| Second composition bar: Perminov's own rank-1540 Z scheme (`CHANGELOG.md`, 25/10/2026) split into ternary terms | 11x14x16 | ZT rank 1553 (13 of its terms have a coefficient of 2) | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/Z/11x14x16_m1540_Z.json | 2026-10-26T16:56:03Z |
| Perminov `schemes/results/{ZT,Z,Q}` file names | 11x14x16 | lowest existing file rank: ZT 1550, Z no file, Q 1520 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-18T14:20:54Z |
| Perminov `schemes/results/{ZT,Z,Q}` file names, again | 11x14x16 | lowest existing file rank: ZT 1550, Z 1540, Q 1520 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-26T16:56:59Z |
| Sedoglavic `fmm_sota.json` | 11x14x16 | rank 1520 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-18T14:20:59Z |
| MerlijnW70/fmm-schemes tree | 11x14x16 | no file for this format | https://github.com/MerlijnW70/fmm-schemes | 2026-10-18T14:20:59Z |
| V3R1T4S `TROPHY_CASE.md` and pull requests (pages 1 to 5) | 11x14x16 | no ZT or Z entry for this format | https://github.com/elder-plinius/V3R1T4S | 2026-10-18T14:21:00Z |

Live row in `docs/ranks.md`, verbatim (2026-10-26T16:55:46Z): `| `11x14x16` |  1550 (?)   |   1540 (?)   | 1520 (1571)  |   2.814428649   |`. The Z cell went from 1550 to 1540 on 25/10/2026, when Perminov published his own rank-1540 integer scheme. It is a different scheme from #410's (13 of 1540 terms in common). The ZT cell is unchanged. On 2026-10-18 the row, then with Z 1550, was in Perminov's `README.md`. The panel's novelty skeptic fetched every 2026-10-18 source above; its report is `panel/novelty.md`. The claim folder's own earlier fetch (2026-10-18T13:47:52Z, same README sha256) is in `the-record-we-beat/README.md`, with HTTP status and page sha256.

## Not claimed

- Only the ZT (ternary) column is claimed. Nothing is claimed for any other coefficient class of this format.
- The block composition (rank 1540, class Z; #410, closed) and its ternary split (rank 1548) are not claimed, and neither is the Z column, where Perminov now lists his own 1540. They are compositions of published instances. Only the search step from 1548 to 1547 is new.
- The scheme does not beat the best known rank for this format over the rationals (Q rank 1520; fmm_sota 1520). It is an improvement for the ZT column only.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the rank status table (`docs/ranks.md`), the scheme file format, and the published schemes `11x14x16_m1520_Q` and `3x4x7_m64_ZT` from which the composition in step 1 of `HOW_WE_FOUND_IT.md` is built.
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest), including `fmm_sota.json`.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175, and the meta flip graph work of M. Kauers and co-authors (https://github.com/mkauers/matrix-multiplication): the reduction step in `how-we-built-it/tools/zt_flip_reduce.c` applies flips to the scheme.
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes), compared against.
- Contributor credit: `calgulbenkian`. The object was produced by the contributor's AI search agent (Gemini, "Argon").
