# A 14-glider synthesis of the still life xs31_g8e1ugmmzd553w643 (Catagolue lists 60) — bank target catagolue-glider-synthesis-cost-records, partial win p1

> Partial win p1 only (a strictly cheaper true synthesis of an object whose listed cost is at least 60). The main success criterion is also met on these numbers, but p1 is the intended claim. p2 and p3 are not claimed.

## What
A 14-glider all-glider synthesis of xs31_g8e1ugmmzd553w643 that is strictly cheaper than a live true Catagolue cost of 60 meets partial win p1 (listed cost at least 60) of catagolue-glider-synthesis-cost-records.

In plain words: object/xs31_g8e1ugmmzd553w643.rle is a Game of Life (B3/S23) pattern made of 14 gliders and nothing else. Run forward, the
gliders collide and leave exactly the 31-cell still life xs31_g8e1ugmmzd553w643 (from generation 1819 on), with no other live cells and
no glider escaping. Rewound, the gliders never touch each other, so they come in from infinity. Catagolue's cheapest
known synthesis of this object costs 60 gliders (true synthesis), on the object page and in the xs31 class tabulation
data, fetched live on 2026-11-19 (18 November 2026 evening, America/New_York). 14 is 46 fewer, and 60 is at least 60, as p1 requires.

How it is built: this is a downstream still life. The all-glider pattern is the cheaper synthesis of the seed
xs26_08ehmkk8z6a87066 (12 gliders; V3R1T4S PR #969 (package 2026-11-06-whosedreams-a855292d), merged upstream as 1209b9b; Catagolue still lists 58 (true) at this refetch) stitched with published Shinjuku components that add 2 gliders.
The RLE is self-contained: every one of the 14 gliders is in the file, and the checker does not assume the seed's
Catagolue cost. Using only Catagolue's still-listed 58-glider cost for that seed, plus the same 2 extra gliders, would cost 60. That ties the live cost of 60, so the strict saving of 46 is entirely downstream of the cheaper seed. If the cheaper seed is later ingested by Shinjuku, Catagolue will recompute and this object's listed cost will drop.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. About a minute or less on a laptop. verify-it-yourself/life_check.py is a standard-library Life
checker written from the bank definition: it checks that every generation-0 component is a glider, rewinds every glider
3612 and 4624 generations (4 x the longer bounding-box side, and 4 x the diagonal) and requires no interaction, runs
forward to an exact repeat, compares the final cells with the cells decoded from the apgcode under all 8 symmetries,
counts the gliders and requires fewer than the recorded table cost 60. It does not go online; re-fetch the object page
yourself (URL below) to see the cost today. RUN_IT_YOURSELF.md also gives the lifelib route.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Catagolue object page | `#CSYNTH xs31_g8e1ugmmzd553w643 costs N gliders` | 60 (true) | https://catagolue.hatsya.com/object/xs31_g8e1ugmmzd553w643/b3s23 | 2026-11-19T00:29:14Z |
| Catagolue xs31 synthesis-cost tabulation (CSV) | row `"xs31_g8e1ugmmzd553w643"` | 100000000000000060 = 60 (true) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs31 | 2026-11-19T00:29:09Z |

The HTML tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs31) shows only the most expensive
objects of the class and may not list this one; the CSV is the full class table. Details and page sha256s:
the-record-we-beat/RECORD.md.

## Not claimed
- The main success criterion as a confirmed status (the intended claim is p1), p2 (not an oscillator) and p3 (one object only).
- That the cost is still 60 after 2026-11-19T00:29:14Z (the last live read); Catagolue tables are recomputed every few hours.
- Anything about other objects; the harvest that found this one also found other cheaper syntheses, which are not part of this package.
- That the converter steps themselves are new; the new work is the cheaper seed (named above) used inside a self-contained all-glider RLE.
- Any upload to Catagolue or Shinjuku.

## Credits
- Catagolue (Adam P. Goucher): https://catagolue.hatsya.com/syntheses
- Shinjuku synthesis database and components (Jeremy Tan, with Mark Niemiec, Martin Grant, Goldtiger997 and many others): https://gitlab.com/parclytaxel/Shinjuku
- lifelib (Adam P. Goucher): https://gitlab.com/apgoucher/lifelib , https://pypi.org/project/python-lifelib/
- The cheaper seed xs26_08ehmkk8z6a87066 (V3R1T4S PR #969 (package 2026-11-06-whosedreams-a855292d), merged upstream as 1209b9b; Catagolue still lists 58 (true) at this refetch).
- Contributor: whosedreams (V3R1T4S kit).
