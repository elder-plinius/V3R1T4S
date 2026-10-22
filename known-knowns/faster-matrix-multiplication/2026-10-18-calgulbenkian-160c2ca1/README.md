# Fast matrix multiplication: format 11x12x14 in rank 1165, class Z

## What

The file object/11x12x14_m1165_Z.json is an exact integer (class Z, largest absolute coefficient 2) bilinear scheme of rank 1165 for the 11x12x14 format whose Brent equations hold over Z, and rank 1165 is strictly below the Z rank 1182 in the live Perminov README table, not below the overall best rank 1153 and not matched by any Z-class scheme file in the two named repositories at the fetch time.

Path note: the sentence above is quoted word for word from `panel/gate.md`, and it names the panel's `claim/` folder. In this package the same scheme is `object/11x12x14_m1165_Z.json`.

**Encoding.** The panel checked the original file `object/11x12x14_m1165_Z.json` (dense rows, 1082598 bytes) with sha256 `5cd673ec5425d0a2057030114643b89e7ba64d3c3a60aed4c097ca8b3a895e47`. That file is over the 1,000,000-byte limit, so this package holds a lossless re-encoding of it under the same name (`"encoding": "sparse_flat_pairs"`, 212737 bytes, sha256 `160c2ca18bd51633b189cff33b081be588caec8dd0c124f8021406df547ba053`). Entry-by-entry comparison with the original found no difference; see `verify-it-yourself/RECEIPTS.md`. `INDEX.csv` and `SHA256SUMS` carry the re-encoded file's hash, and the submission id uses it. `panel/gate.md` names the original's hash.

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
| Perminov `README.md`, table `Format \| ZT rank \| Z rank \| Q rank` | 11x12x14 | Z rank 1182 (live columns: ZT 1182, Z 1182, Q 1153) | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-18T14:20:53Z |
| Perminov `schemes/results/{ZT,Z,Q}` file names | 11x12x14 | lowest existing file rank: ZT 1182, Z no file, Q 1153 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 2026-10-18T14:20:54Z |
| Sedoglavic `fmm_sota.json` | 11x12x14 | rank 1153 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-18T14:20:59Z |
| MerlijnW70/fmm-schemes tree | 11x12x14 | no file for this format | https://github.com/MerlijnW70/fmm-schemes | 2026-10-18T14:20:59Z |
| V3R1T4S `TROPHY_CASE.md` and pull requests (pages 1 to 5) | 11x12x14 | no ZT or Z entry for this format | https://github.com/elder-plinius/V3R1T4S | 2026-10-18T14:21:00Z |

Live Perminov row, verbatim: `| `11x12x14` |  1182 (?)   |     1182     | 1153 (1182)  |   2.811853672   |`. The panel's novelty skeptic fetched every source above; its report is `panel/novelty.md`. The claim folder's own earlier fetch (2026-10-18T13:47:52Z, same README sha256) is in `the-record-we-beat/README.md`, with HTTP status and page sha256.

## Not claimed

- Only the Z (integer) column is claimed. Nothing is claimed for any other coefficient class of this format.
- The scheme does not beat the best known rank for this format over the rationals (Q rank 1153; fmm_sota 1153). It is an improvement for the Z column only.
- This is a rank bound for one format and does not improve the asymptotic exponent of matrix multiplication.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **A. I. Perminov**, *FastMatrixMultiplication* (https://github.com/dronperminov/FastMatrixMultiplication): the status table, the scheme file format, and the Q schemes and ZT base schemes this work builds on (see `how-we-built-it/README.md`).
- **A. Sedoglavic**, *Catalogue of fast matrix multiplication algorithms* (https://fmm.univ-lille.fr/ and https://github.com/sedoglavic/fmm_digest), including `fmm_sota.json`.
- **M. Kauers and J. Moosbauer**, *Flip Graphs for Matrix Multiplication*, arXiv:2212.01175, and the meta flip graph work of M. Kauers and co-authors (https://github.com/mkauers/matrix-multiplication): the reduction step in `how-we-built-it/tools/zt_flip_reduce.c` applies flips to the scheme.
- **MerlijnW70**, *fmm-schemes* (https://github.com/MerlijnW70/fmm-schemes), compared against.
- Contributor credit: `calgulbenkian`. The object was produced by the contributor's AI search agent (Gemini, "Argon").
