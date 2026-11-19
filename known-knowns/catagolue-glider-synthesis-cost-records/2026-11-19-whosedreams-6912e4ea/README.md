# A 13-glider synthesis of the still life xs26_8kk69ba952zw3453 (Catagolue lists 32) — bank target catagolue-glider-synthesis-cost-records, main success criterion

> Main success criterion only. Partial win p1 is NOT claimed: p1 needs a listed cost of at least 60, and this
> object's listed cost is 32. p2 and p3 are not claimed.

## What
A 13-glider all-glider synthesis of xs26_8kk69ba952zw3453 that uses strictly fewer gliders than a live true Catagolue cost of 32 on both the object page and the xs26 synthesis-costs tabulation data meets the main success criterion of catagolue-glider-synthesis-cost-records (not partial win p1).

In plain words: object/xs26_8kk69ba952zw3453.rle is a Game of Life (B3/S23) pattern made of 13 gliders and nothing else. Run forward, the
gliders collide and leave exactly the 26-cell still life xs26_8kk69ba952zw3453 (from generation 1786 on), with no other live cells and
no glider escaping. Rewound, the gliders never touch each other, so they come in from infinity. Catagolue's cheapest
known synthesis of this object costs 32 gliders (true synthesis), on the object page and in the xs26 class tabulation
data, fetched live on 2026-11-19. 13 is 19 fewer.

How it is built: the published 12-glider synthesis of xs27_g88ehmkia4z0178a6 (a 3-stage Shinjuku route; Catagolue also lists
it at 12, true, read live on 2026-11-19), plus one new glider that turns that 27-cell still life into the
26-cell target. The new part is that 1-glider step. No earlier V3R1T4S claim is used.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. A few seconds on a laptop. verify-it-yourself/life_check.py is a standard-library Life
checker written from the bank definition (the same file as in the merged #970 package): it checks that every
generation-0 component is a glider, rewinds every glider 2880 and 4012 generations (4 x the longer bounding-box side,
and 4 x the diagonal) and requires no interaction, runs forward to an exact repeat, compares the final cells with the
cells decoded from the apgcode under all 8 symmetries, counts the gliders and requires fewer than the recorded table
cost 32. It does not go online; re-fetch the object page yourself (URL below) to see the cost today.
RUN_IT_YOURSELF.md also gives the lifelib route and the drop-one controls.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Catagolue object page | `#CSYNTH xs26_8kk69ba952zw3453 costs N gliders` | 32 (true) | https://catagolue.hatsya.com/object/xs26_8kk69ba952zw3453/b3s23 | 2026-11-19T15:21:03Z |
| Catagolue xs26 synthesis-cost tabulation (CSV) | row `"xs26_8kk69ba952zw3453"` | 100000000000000032 = 32 (true) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 | 2026-11-19T15:20:50Z |

The HTML tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs26) shows only the most expensive
objects of the class; the CSV is the full class table. Details and page sha256s: the-record-we-beat/RECORD.md.

## Not claimed
- Partial win p1 (listed cost 32 is below 60), p2 (not an oscillator) and p3 (one object only).
- That the cost is still 32 after 2026-11-19T15:21:03Z (the last live read); Catagolue tables are recomputed every few hours.
- Anything about other objects. The same search found many other savings, and some other objects can be built more
  cheaply from this one; none of those are part of this package.
- That Shinjuku or Catagolue already contains this 1-glider step (they did not list it at the last read).
- Any upload to Catagolue or Shinjuku.

## Credits
- Catagolue (Adam P. Goucher): https://catagolue.hatsya.com/syntheses
- Shinjuku synthesis database and components (Jeremy Tan, with Mark Niemiec, Martin Grant, Goldtiger997 and many others): https://gitlab.com/parclytaxel/Shinjuku ; the 12-glider route for xs27_g88ehmkia4z0178a6 is built entirely from its components.
- lifelib (Adam P. Goucher): https://gitlab.com/apgoucher/lifelib , https://pypi.org/project/python-lifelib/
- Contributor: whosedreams (V3R1T4S kit).
