# (6, 256) spherical code: a 256-point code in R^6 with a larger minimal angle than the table's

## What

In the claim package's saved pages, fetched 2026-10-25T06:26:36Z (index) and 06:26:38Z (/plain), 3 s before CLAIM.md was written according to the file times, the 256 vectors of object/code_6_256.txt (26 significant digits per coordinate), normalised in mpmath at 50 digits, have c* = 0.7048987224974410014733 at pair (55, 247), which is 0.00003324685455899852672 below the unstarred, unlabelled /plain row 6,256,0.704931969352 (exact-rational check: no pair above 0.704931969352 − 1e-10) and below every row with d' <= 6 and N' >= 256 in /plain, in the index and in arXiv:2610.19988's three tables; no saved arXiv feed or full text shows a (6, 256) code at or below c*, and d = 6 lies outside the kissing clause; not confirmed are the row's live state after 06:26:38Z (my timing check ran 21.8 minutes after that fetch), any arXiv paper posted after about 05:54Z or missed by the saved title and abstract feeds, and the truth of the fetch-log lines beyond their sha256 matching the saved bytes.

Note: the paragraph above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`; "my timing check" is that skeptic's).

Path note: the panel files name the panel's claim/ folder ("the claim package"):

- In this package claim/object/code_6_256.txt is object/code_6_256.txt (same sha256).
- claim/CLAIM.md's claim is this README.
- The fetch lines of claim/TABLE_RECORD.md and FETCH_RECORDS.md are in the-record-we-beat/RECORD.md.

Not shipped:

- The claim's checkers (claim/checker/check_mp.py, check_exact.py, table_row.py, propagated_bar.py, contacts.py, rows_changed.py, arxiv_read.py and the other scripts there), claim/REPRODUCE.md and expected_output.txt. verify-it-yourself/verify_code.py is a separate standalone checker of the same exact bar, and its output is verify-it-yourself/RECEIPTS.md.
- claim/inputs/: third-party pages and data, namely the table's index and /plain, the posted code /data/6/256, the arXiv feeds and full texts, and arXiv:2610.19988's Zenodo tables. Their URLs, fetch times and sha256 values are in the-record-we-beat/RECORD.md and the panel files. Also our polish logs polish_6_256_stage1/2.log, whose summary lines are in how-we-built-it/COMMANDS.md.
- claim/ARXIV_RECORD.md and claim/build/ (MANIFEST.txt, templates/, finalize.py).
- The self-break files selfbreak/verdict.md and claim_build/REPAIR1.md (panel/gate.md).
- The skeptics' working folders work-reproduce/, work-novelty/ and work-criterion/.

Also see "Named but not shipped" in RUN_IT_YOURSELF.md.

## Check it yourself

From this folder, with Python 3 (standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (under a second on a laptop; full expected output in RUN_IT_YOURSELF.md and
verify-it-yourself/RECEIPTS.md). The check is exact: it reads the coordinates as decimals and compares every one
of the 32,640 pairs with the bar 0.704931969352 - 1e-10 in integer arithmetic.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Henry Cohn's Table of Spherical Codes | d = 6, N = 256 (no `&ast;`, not labelled "needs more optimization"; Pavlos Moros, 2026) | 0.704931969352 | https://spherical-codes.org/ and https://spherical-codes.org/plain | 2026-10-25T06:26:36Z and 06:26:38Z (re-read by the panel at 06:33:58Z and 06:34:00Z: same bytes) |

This code: c* = 0.7048987224974410014733 (22 significant digits), which is 3.32469e-5 lower (a minimal angle of
45.1786374° against 45.1759518° for the table's code). No listed code with d' <= 6 and N' >= 256 (which would give
a (6, 256) code by deleting points or padding with zeros) reaches c*, in the table, in the three data tables of
arXiv:2610.19988 or in ImprovEvolve's benchmark cells. d = 6 is outside the kissing clause's 9 <= d <= 23.
Snapshot and extracted cell: the-record-we-beat/RECORD.md.

Re-read before filing (one GET each, HTTP 200): index 2026-10-28T18:23:47Z, /plain 18:23:50Z, /data/6/256 18:23:52Z. The (6, 256) row is unchanged: 0.704931969352, "Pavlos Moros, 2026.", no `&ast;`, no "needs more optimization". The posted code has the same sha256, and (6, 256) is still the lowest row with d' <= 6 and N' >= 256 in the index and in /plain (next: (6, 257) at 0.705350637779). Other rows changed after 2026-10-25, but none with d' <= 6 and N' >= 256 is at or below c*. Details and sha256 values: the-record-we-beat/RECORD.md.

## Not claimed

- Not optimality. The polish stopped at a numerically stationary point of its method (trust radius below 1e-15;
  the maximum cosine changed by 4e-16 over the last 10 steps (log lines at steps 120 and 130)), with 1,331 pairs within 1e-14 of the maximum
  and every point in such a pair; that is not a proof of local optimality.
- Not an exact (algebraic) angle: the table lists no minimal polynomial for this row, and none is claimed here.
- Not a new construction: the code is a local polish of the code posted for the row by Pavlos Moros (2026). That
  code was not at a local optimum (1 pair at its maximum cosine, 998 within 1e-8), though the row carried no
  "needs more optimization" label.
- Not uploaded to the table: an upload to spherical-codes.org/upload-code is left to the contributor.
- The table row's state after the pre-filing re-read (2026-10-28T18:23:47Z) is not checked. Neither are arXiv papers outside the saved 'spherical code' / 'Tammes' / 'kissing number' / 256 metadata searches and the full texts named in the panel files. One more arXiv API read before filing (2026-10-28T17:32:49Z, newest 25 updated entries) found nothing on (6, 256) after 2026-10-25.

## Credits

- **Pavlos Moros**: the (6, 256) code posted on the table (2026), https://spherical-codes.org/data/6/256. This
  object is a local refinement of that code (points moved by 0.023 median, 0.055 at most), so the seed is Pavlos
  Moros's work.
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
