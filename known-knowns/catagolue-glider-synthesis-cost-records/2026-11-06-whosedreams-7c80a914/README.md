# A 32-glider synthesis of the still life xs27_0ca1ugmicz651346 (Catagolue lists 66) — bank target catagolue-glider-synthesis-cost-records, partial win p1

> Partial win p1 only (a strictly cheaper true synthesis of an object whose listed cost is at least 60). The main
> success criterion is not what the panel confirmed, and p2 and p3 are not claimed.

## What
Confirmed scope (from panel/gate.md, verbatim): A 32-glider all-glider synthesis of xs27_0ca1ugmicz651346 that is strictly cheaper than a package-stated live true Catagolue cost of 66 meets partial win p1 (listed cost at least 60) of catagolue-glider-synthesis-cost-records.

In plain words: object/xs27_0ca1ugmicz651346.rle is a Game of Life (B3/S23) pattern made of 32 gliders and nothing else. Run forward, the
gliders collide and leave exactly the 27-cell still life xs27_0ca1ugmicz651346 (from generation 4332 on), with no other live cells and
no glider escaping. Rewound, the gliders never touch each other, so they come in from infinity. Catagolue's cheapest
known synthesis of this object costs 66 gliders (true synthesis), on the object page and in the xs27 class tabulation
data, fetched live on 2026-11-06. 32 is 34 fewer, and 66 is at least 60, as p1 requires.

How it is built: the published 31-glider synthesis of xs27_8ehf8bbgz6430321 (an 8-stage Shinjuku route), plus one new glider that
turns that 27-cell still life into the target. The new part is that 1-glider step.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. About 10 seconds on a laptop. verify-it-yourself/life_check.py is a standard-library Life
checker written from the bank definition: it checks that every generation-0 component is a glider, rewinds every glider
8004 and 10916 generations (4 x the longer bounding-box side, and 4 x the diagonal) and requires no interaction, runs
forward to an exact repeat, compares the final cells with the cells decoded from the apgcode under all 8 symmetries,
counts the gliders and requires fewer than the recorded table cost 66. It does not go online; re-fetch the object page
yourself (URL below) to see the cost today. RUN_IT_YOURSELF.md also gives the lifelib route.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Catagolue object page | `#CSYNTH xs27_0ca1ugmicz651346 costs N gliders` | 66 (true) | https://catagolue.hatsya.com/object/xs27_0ca1ugmicz651346/b3s23 | 2026-11-06T16:15:00Z |
| Catagolue xs27 synthesis-cost tabulation (CSV) | row `"xs27_0ca1ugmicz651346"` | 100000000000000066 = 66 (true) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs27 | 2026-11-06T16:15:01Z |

The HTML tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs27) shows only the most expensive
objects of the class and does not list this one; the CSV is the full class table. Details and page sha256s:
the-record-we-beat/RECORD.md.

## Not claimed
- The main success criterion as a confirmed status (the criterion panelist's confirmed scope is p1), p2 (not an
  oscillator) and p3 (one object only).
- That the cost is still 66 after 2026-11-06T16:16:21Z (the last live read); Catagolue tables are recomputed every few hours.
- Anything about other objects; the run that found this one also found many smaller savings, which are not part of this package.
- Any upload to Catagolue or Shinjuku.

## Credits
- Catagolue (Adam P. Goucher): https://catagolue.hatsya.com/syntheses
- Shinjuku synthesis database and components (Jeremy Tan, with Mark Niemiec, Martin Grant, Goldtiger997 and many others): https://gitlab.com/parclytaxel/Shinjuku ; the 31-glider seed route for xs27_8ehf8bbgz6430321 is built entirely from its components.
- lifelib (Adam P. Goucher): https://gitlab.com/apgoucher/lifelib , https://pypi.org/project/python-lifelib/
- Contributor: whosedreams (V3R1T4S kit).
