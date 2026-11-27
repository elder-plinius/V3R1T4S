# CHANGES: claim_v2/ (judged by panel_v2/; left untouched) -> claim_v3/

Panel v2 (runs/2026-11-24-0728/panel_v2/): REPRODUCE pass: true, NOVELTY pass: true, CRITERION pass: false.
panel_v2/gate.md: status PROMISING, p1 not confirmed. Wording-only fix; no certified number is changed
(result/p1_certified_values.json is byte-identical to v1/v2).

1. Dropped the premise "The paper rounds, it does not truncate" (CRITERION, decisive). The paper mixes rounding
   and truncation, including in its y+sqrt(y) column (rounded at Table 1 row 4 and Table 2 rows 2, 10, 12, 13;
   truncated at Table 2 rows 7, 9, 14; checked by check/compare_printed.py on the published y values and the
   excerpt). v3 reports the 19-row h comparison under both conventions.
2. Counts, verified on the shipped balls and the printed excerpt: 8 mismatches under rounding (Table 2 rows
   1, 2, 4, 7, 9, 10, 12, 14) and 6 under truncation (Table 1 row 4 and Table 2 rows 1, 4, 6, 12, 14); 0
   ambiguous under either. v2 had reported only the rounding column and called all 8 "corrections".
3. Only Table 2 rows 1, 4, 12 and 14 are listed as corrections (wrong at printed precision under either
   convention). Table 2 rows 2, 7, 9 and 10 are marked convention-dependent (mismatch under rounding, match
   under truncation). Table 1 row 4 and Table 2 row 6, which mismatch only under truncation, are described
   the same way and are not called corrections.
4. At 3 decimals: rows 7 (printed 1.025; certified 1.026 rounded / 1.025 truncated) and 9 (printed 0.997;
   certified 0.998 / 0.997) are convention-dependent, as is row 4 (certified -0.995 under both; the printed
   -0.9949 is -0.995 rounded to 3 decimals and -0.994 truncated). v2's 3-decimal "corrections" of rows 7 and 9
   are withdrawn.
5. The p1 deliverable is narrowed to the 19 certified values to 3 decimals, plus the full balls (a table of
   both 3-decimal renderings is in CLAIM.md). The partial-win sentence and the headline were narrowed to match.
   Table 2 row 5 remains a 2-decimal match under both conventions; its 3-decimal rendering is -1.021 (rounding)
   or -1.020 (truncation), which v2 had stated only as -1.021.
6. Credits added (NOVELTY, pass with notes): the bzyzz authors are named, Zhenyu Bi and Enze Hou, with HAL
   hal-05838582 alongside github.com/bzyzz/mertens_bound. Their "Peak1" is noted as a different polished point
   near Table 2 row 2 (about -0.99590, uncertified), not a re-evaluation of that row. The HAL copy of
   Kim-Nguyen (hal-05016898) is cited as printing identical digits for all 19 pairs. The Gallego credit is
   unchanged.
7. Caveats kept: same Arb library (independent computation, not an independent method); journal tables
   paywalled (the HAL copy is the available post-referee print). The note that the values were not recomputed
   after the zero-writer change is kept; the v2 REPRODUCE skeptic's independent zeros overlapped all 19 balls.
8. check/compare_printed.py now parses the excerpt, reports both conventions and the y+sqrt(y) column, and
   does not depend on flint (ball strings are parsed as mid +/- radius). SHA256SUMS.txt regenerated; the
   bytecode file that had been in v2's sums is not included.
