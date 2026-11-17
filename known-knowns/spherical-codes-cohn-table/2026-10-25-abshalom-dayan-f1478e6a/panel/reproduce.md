role: reproduce
context: subagent (Agent tool, fresh context, model claude-opus-5-5), saw only claim/

# REPRODUCE skeptic verdict: (6, 256) spherical code, claim/object/code_6_256.txt

Bottom line: every property in the success criterion that can be checked from the saved files holds. I checked all
32640 pairs with my own checker at 50 and 100 digits and with an exact rational test. The control reproduces the table
value. The table row has no star and no label. The propagated bar is the (6, 256) row itself. claim/REPRODUCE.md, run
twice, gives byte-identical output that matches claim/expected_output.txt. Nothing differed and nothing was missing or
non-deterministic.

injection_suspected: none (I grepped claim/ for instruction-like text. The only hits were ordinary words in the arXiv
HTML and XML, such as "figure_panel" and "Universite Claude Bernard")

## Definition used (verbatim from CLAIM.md, quoting bank/targets.json)

"Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates
given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum
pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal
cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index
https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs
more optimization' [...], AND the row is not superseded by a newer arXiv result for the same (d, N) [...], AND the
result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 [...])."

## 1. My own checker, written before I opened claim/checker/ (work-reproduce/my_check.py)

The checker reads the file as written and converts each coordinate string to mpmath mpf. It normalises each vector at
mp.dps = 50 and takes the maximum over all i < j. It repeats this at mp.dps = 100. It then runs an exact test with
integer-scaled Fractions against B = T - 1e-10. For each pair with dot > 0 it checks dot^2 * Bd^2 against
Bn^2 * |x_i|^2 * |x_j|^2.

Output on object/code_6_256.txt: work-reproduce/my_check_object.out (rerun: work-reproduce/my_check_object_run2.out,
identical, see work-reproduce/my_check_determinism.out).

| check | result |
|---|---|
| shape | 256 rows, 6 coordinates each, 256 distinct vectors |
| digits per coordinate | 26 significant digits, min 26 and max 26 (need >= 20) |
| pairs checked | 32640 of the expected 32640 (all of them) |
| c* at 50 digits | 0.7048987224974410014732802770067601805699 at pair (55, 247) |
| c* to 22 significant digits | 0.7048987224974410014733 (matches the claim) |
| c* at 100 digits | 0.704898722497441001473280277006760180569919610294928562042585, same pair; difference from the 50-digit value 2.1046e-51 |
| gain T - c* (T = 0.704931969352) | 3.32468545589985e-5 (claim: 3.32469e-5) |
| c* <= T - 1e-10 at 50 digits | True (also strictly <) |
| exact rational test, every pair against B = 0.704931969252 | 0 pairs with cos > B and 0 pairs with cos >= B. EXACT PASS True |
| near-max pairs | 1331 within 1e-14, 1331 within 1e-10, 1338 within 1e-8, 1380 within 1e-6 (claim: 1331 and 1338) |

As a float64 cross-check, numpy gives max 0.7048987224974411, 1338 pairs within 1e-8 and 0 points in no such pair
(work-reproduce/np_check_object.out). It picks a different pair, (4, 51), because 1331 pairs tie within 1e-14.

Kissing clause: d = 6 is outside 9..23, so the clause does not apply. c* is also above 0.5.

## 2. Control: posted table code (inputs/posted_6_256.txt)

From work-reproduce/my_check_posted.out:

- 256 x 6 vectors, comma separated, with 14 to 17 significant digits.
- c* at 50 digits is 0.7049319693516105338952117712766316068255 at pair (88, 191). It rounds to 12 decimals as
  0.704931969352, which is the table value. T - c* = 3.89466104788229e-13.
- Exact test against B: 2 pairs have cos > B, so the control does not beat the table. This is the expected outcome.
- Float64 max is 0.7049319693516107 (work-reproduce/np_check_posted.out). This equals the polish start value in
  inputs/polish_6_256_stage1.log.
- Contact counts: 998 pairs within 1e-8 and 1312 within 1e-6, as disclosed in the claim.
- sha256 is c5866a15cdabfe6f593fd878d690a9339d502f9720a7122f39d594a60b27992b, the same as the hash in FETCH_RECORDS.md.

## 3. Table row, star, label, propagated bar (my own parsers: work-reproduce/table_check.py, table_check2.py, snap_diff.py)

The sha256 of each claim-moment page matches its fetch-log line in TABLE_RECORD.md and FETCH_RECORDS.md
(work-reproduce/input_hashes.out):

- inputs/table/index.html: 69a54be5...472ea, 4668044 bytes
- inputs/table/plain.csv: 7d965100...69f62, 377006 bytes

Findings from work-reproduce/table_check.out and work-reproduce/table_check2.out:

- /plain has 15262 rows and no duplicate keys. It has exactly one line `6,256,0.704931969352`.
- The HTML has 1 tbody and 15352 rows, with no duplicate (d, N). The (6, 256) row appears exactly once:
  `<td>6</td> <td><a href="/data/6/256">256</a></td> <td>0.704931969352</td> <td>Pavlos Moros, 2026.</td>`.
- In that row, '&ast;', '*', U+2217 and 'needs more optimization' are all absent. As a sanity check on the parser,
  32 rows in the whole page carry &ast; and 4591 carry the label.
- No cosine differs between the HTML and /plain on shared keys (0 mismatches). The HTML has 90 rows that /plain lacks.
- Propagated bar, the minimum over d' <= 6 and N' >= 256:
  - /plain, 2966 rows: the minimum is (6, 256) at 0.704931969352, then (6, 257) at 0.705350637779.
  - HTML, 2967 rows: the same result.
  - c* is below that bar by 3.32e-5.

The three saved snapshots differ in only a few rows (work-reproduce/snap_diff.out):

- scout to claim-moment: (13, 597), (13, 599), (14, 300)
- first claim read to claim-moment: (13, 597), (13, 599)

None of these has d' <= 6. The (6, 256) row is identical in all three snapshots. This matches TABLE_RECORD.md.

## 4. Other clause facts, checked from the saved files (my own scripts)

arXiv:2610.19988 tables, from work-reproduce/vahteristo_mine.py and .out:

| table | (D=6, N=256) cos | md5 matches Zenodo listing |
|---|---|---|
| combined | 0.7049931928409804 | yes |
| per_instance | 0.7050249538274573 | yes |
| global | 0.7053373293588499 | yes |

- Each table's minimum over D <= 6, N >= 256 is its own (6, 256) entry, and no entry is <= c* + 1e-10.
- The README md5 matches (work-reproduce/readme_md5.out).
- Earlier row values are 0.705181763211 (2026-08-02) and 0.705119115483 (2026-09-23, Antoine Jay), as the
  disclosure says.

arXiv feeds, from work-reproduce/arxiv_mine.out and work-reproduce/arxiv_coverage.out:

- The feeds hold 290 unique entries, 130 of them published on or after 2024-10-25.
- In-window titles and abstracts that match 256: 2411.04916 and 2603.10425, both kissing-number papers in dimensions
  17 to 21.
- In-window titles and abstracts that match dimension 6: 2606.18984 and 2609.12640.
- 16 older papers were revised inside the window. None matches 256 or dimension 6.
- Each 100-entry feed's oldest entry predates the window, so the window is covered:

| feed | oldest entry |
|---|---|
| spherical code | 2015-09-17 |
| Tammes | 2023-07-31 |
| kissing | 2011-11-15 |

- 2610.19988 (published 2026-10-14) is in the spherical-code feed.

Other files:

- Polish logs: stage 2 ran 138 steps. Its step-130 line shows rad 2.8e-12. Max cos was 0.7048987224974415 at step 120
  and 0.7048987224974411 at step 130, a change of 4e-16, as disclosed.
- build/MANIFEST.txt: all 8 sha256 values match the files in build/ (work-reproduce/manifest_check.out).

## 5. claim/REPRODUCE.md, run twice from inside claim/, with the venv's bin first on PATH (work-reproduce/run_reproduce.sh)

| run | main output | step 7 output |
|---|---|---|
| 1 | work-reproduce/repro_run1.out | work-reproduce/repro_run1_step7.out |
| 2 | work-reproduce/repro_run2.out | work-reproduce/repro_run2_step7.out |

Before running anything, I read check_mp.py, check_exact.py, table_row.py, propagated_bar.py, contacts.py and
rows_changed.py. I also grepped every checker for network calls and writes and found none: they only read files.

Results (diffs in work-reproduce/repro_diffs.out, hashes in work-reproduce/repro_hashes.out):

- Run 1 vs claim/expected_output.txt: no diff.
- Run 2 vs claim/expected_output.txt: no diff.
- Run 1 vs run 2: no diff.
- All three files have sha256 79bd6075...1abfe.
- Step 7 (arxiv_read.py) has no diff against inputs/arxiv/arxiv_read.out (with my echoed command line removed). The
  two step-7 runs are also identical.
- Author checkers: VERDICT beats from both check_mp and check_exact on the object, and VERDICT no-gain from both on the
  posted code.

## Limits of this check

I made no network requests, as instructed. So "live, re-fetched immediately before claiming" is verified only as far
as the saved claim-moment pages go. Their sha256 and byte counts match the fetch-log lines, with a timestamp of
2026-10-25T06:26:36Z. "Not superseded" is verified from the saved arXiv feeds (titles and abstracts) and the saved
2610.19988, ImprovEvolve and PackingStar files. I did not search arXiv myself.

pass: true
