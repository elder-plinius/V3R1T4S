# (6, 256) spherical code: a 256-point code in R^6 with a larger minimal angle than the table's

## What

As of 2026-11-07T00:08:29Z, the 256 vectors of object/code_6_256.txt (26 significant digits per coordinate) have maximum pairwise cosine c* = 0.7048987224974410014733 (a minimal angle of 45.1786374 degrees), at pair (55, 247) (0-based lines), computed in mpmath at 50 digits. The live Table of Spherical Codes row for d = 6, N = 256 reads 0.704931961199 (Christopher Smolen, 2026), with no `&ast;` and no "needs more optimization" label, so c* is 3.32387e-5 below it. An exact-rational check finds no pair with cosine above 0.704931961199 - 1e-10. No row with d' <= 6 and N' >= 256 in the table, and none in the three data tables of arXiv:2610.19988, reaches c*. d = 6 is outside the kissing clause (9 <= d <= 23).

## Check it yourself

From this folder, with Python 3 (standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (under a second on a laptop; full expected output in RUN_IT_YOURSELF.md and
verify-it-yourself/RECEIPTS.md). The check is exact: it reads the coordinates as decimals and compares every one
of the 32,640 pairs with the bar 0.704931961199 - 1e-10 in integer arithmetic.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Henry Cohn's Table of Spherical Codes | d = 6, N = 256 (no `&ast;`, not labelled "needs more optimization"; Christopher Smolen, 2026) | 0.704931961199 | https://spherical-codes.org/ | 2026-11-07T00:08:29Z (HTTP 200) |

This code: c* = 0.7048987224974410014733 (22 significant digits), which is 3.32387e-5 lower (a minimal angle of
45.1786374 degrees against 45.1759518 degrees for the table's code). The bar is the lowest public value among the
comparators: no listed code with d' <= 6 and N' >= 256 (which would give a (6, 256) code by deleting points or
padding with zeros) reaches c*, in the table, in the three data tables of arXiv:2610.19988 or in ImprovEvolve's
benchmark cells. d = 6 is outside the kissing clause's 9 <= d <= 23. Snapshot and extracted cell:
the-record-we-beat/RECORD.md.

History of the row: it read 0.705181763211 on 2026-08-02 and 0.705119115483 on 2026-09-23 (credited to Antoine Jay). From 2026-10-24 to at least 2026-10-28T18:23:47Z it read 0.704931969352 (Pavlos Moros, 2026), and the code behind that value is the seed of this object (see Credits). By 2026-11-07T00:08:29Z it read 0.704931961199 (Christopher Smolen, 2026). Against the earlier 0.704931969352, c* was 3.32469e-5 lower.

## Not claimed

- Not optimality. The polish stopped at a numerically stationary point of its method (trust radius below 1e-15;
  the maximum cosine changed by 4e-16 over the last 10 steps (log lines at steps 120 and 130)), with 1,331 pairs within 1e-14 of the maximum
  and every point in such a pair; that is not a proof of local optimality.
- Not an exact (algebraic) angle: the table lists no minimal polynomial for this row, and none is claimed here.
- Not a new construction: the code is a local polish of the code Pavlos Moros posted for the row (as served on
  2026-10-24 and 2026-10-28). That code was not at a local optimum (1 pair at its maximum cosine, 998 within 1e-8), though the row carried no
  "needs more optimization" label.
- Not uploaded to the table: an upload to spherical-codes.org/upload-code is left to the contributor.
- The table row's state after 2026-11-07T00:08:29Z is not checked. Neither are arXiv papers outside the saved 'spherical code' / 'Tammes' / 'kissing number' / 256 metadata searches and the full texts named in the panel files. One more arXiv API read before filing (2026-10-28T17:32:49Z, newest 25 updated entries) found nothing on (6, 256) after 2026-10-25.

## Credits

- **Pavlos Moros**: the (6, 256) code posted on the table (2026) as served at https://spherical-codes.org/data/6/256
  on 2026-10-24 and 2026-10-28 (sha256 c5866a15cdabfe6f593fd878d690a9339d502f9720a7122f39d594a60b27992b). That URL
  now serves different code, so the seed is identified by this hash. This object is a local refinement of that code
  (points moved by 0.023 median, 0.055 at most), so the seed is Pavlos Moros's work.
- **Christopher Smolen**: the current table row for (6, 256), 0.704931961199 (2026), the bar this package is compared
  against.
- **Henry Cohn**: the Table of Spherical Codes, https://spherical-codes.org/ (archived data set
  https://hdl.handle.net/1721.1/153543).
- **Ilmari Vahteristo**: "New spherical codes by tuning an annealing solver", https://arxiv.org/abs/2610.19988,
  data at https://zenodo.org/records/23270586 (compared against).
- **Alexey Kravatskiy, Valentin Khrulkov, Ivan Oseledets**: "ImprovEvolve", https://arxiv.org/abs/2602.10233
  (compared against; no cell in d <= 7).
- Also checked: Chengdong Ma et al. (PackingStar, https://arxiv.org/abs/2511.13391), S. V. Borodachov,
  P. G. Boyvalenkov, P. D. Dragnev, D. P. Hardin, E. B. Saff, M. M. Stoyanova (https://arxiv.org/abs/2512.25037),
  Rustem Takhanov, Zhenisbek Assylbekov, Stanislav Yun (https://arxiv.org/abs/2606.18984), Yanlu Lian, Qun Mo,
  Yu Xia (https://arxiv.org/abs/2411.16038), and the other arXiv papers named in panel/criterion.md and
  panel/novelty.md (each at https://arxiv.org/abs/ followed by its identifier).
- HiGHS (Q. Huangfu and J. A. J. Hall, https://highs.dev/, https://doi.org/10.1007/s12532-017-0130-5), via SciPy's linprog (https://scipy.org/), solves the linear programs of the polish.
- Contributed by Abshalom Dayan. Found by an AI agent run using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S) (method:
  how-we-built-it/ and HOW_WE_FOUND_IT.md; panel: panel/).
