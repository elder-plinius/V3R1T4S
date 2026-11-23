# A 21-glider synthesis of the still life xs25_69ar1mkiczx643 (Catagolue lists 49) — bank target catagolue-glider-synthesis-cost-records, main success criterion

> Main success criterion only. Partial win p1 is NOT claimed: p1 needs a listed cost of at least 60, and this
> object's listed cost is 49. p2 and p3 are not claimed.

## What
A 21-glider all-glider synthesis of xs25_69ar1mkiczx643 that uses strictly fewer gliders than a live true Catagolue cost of 49 on both the object page and the xs25 synthesis-costs tabulation data meets the main success criterion of catagolue-glider-synthesis-cost-records (not partial win p1).

In plain words: object/xs25_69ar1mkiczx643.rle is a Game of Life (B3/S23) pattern made of 21 gliders and nothing else. Run forward, the
gliders collide and leave exactly the 25-cell still life xs25_69ar1mkiczx643 (from generation 3840 on), with no other live cells and
no glider escaping. Rewound, the gliders never touch each other, so they come in from infinity. Catagolue's cheapest
known synthesis of this object costs 49 gliders (true synthesis), on the object page and in the xs25 class tabulation
data, fetched live on 2026-11-19. 21 is 28 fewer.

How it is built: the published 20-glider synthesis of xs27_cikm1da4ozxd8711 (a 7-stage Shinjuku route; Catagolue also lists
it at 20, true, read live on 2026-11-19), plus one new glider that turns that 27-cell still life into the
25-cell target. The new part is that 1-glider step. No earlier V3R1T4S claim is used.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. A few seconds on a laptop. verify-it-yourself/life_check.py is a standard-library Life
checker written from the bank definition (the same file as in the merged #970 package): it checks that every
generation-0 component is a glider, rewinds every glider 7016 and 9892 generations (4 x the longer bounding-box side,
and 4 x the diagonal) and requires no interaction, runs forward to an exact repeat, compares the final cells with the
cells decoded from the apgcode under all 8 symmetries, counts the gliders and requires fewer than the recorded table
cost 49. It does not go online; re-fetch the object page yourself (URL below) to see the cost today.
RUN_IT_YOURSELF.md also gives the lifelib route and the drop-one controls.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Catagolue object page | `#CSYNTH xs25_69ar1mkiczx643 costs N gliders` | 49 (true) | https://catagolue.hatsya.com/object/xs25_69ar1mkiczx643/b3s23 | 2026-11-19T15:20:58Z |
| Catagolue xs25 synthesis-cost tabulation (CSV) | row `"xs25_69ar1mkiczx643"` | 100000000000000049 = 49 (true) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs25 | 2026-11-19T15:20:47Z |

The HTML tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs25) shows only the most expensive
objects of the class; the CSV is the full class table. Details and page sha256s: the-record-we-beat/RECORD.md.

## Not claimed
- Partial win p1 (listed cost 49 is below 60), p2 (not an oscillator) and p3 (one object only).
- That the cost is still 49 after 2026-11-19T15:20:58Z (the last live read); Catagolue tables are recomputed every few hours.
- Anything about other objects. The same search found many other savings, and some other objects can be built more
  cheaply from this one; none of those are part of this package.
- That Shinjuku or Catagolue already contains this 1-glider step (they did not list it at the last read).
- Any upload to Catagolue or Shinjuku.

## Credits
- Catagolue (Adam P. Goucher): https://catagolue.hatsya.com/syntheses
- Shinjuku synthesis database and components (Jeremy Tan, with Mark Niemiec, Martin Grant, Goldtiger997 and many others): https://gitlab.com/parclytaxel/Shinjuku ; the 20-glider route for xs27_cikm1da4ozxd8711 is built entirely from its components.
- lifelib (Adam P. Goucher): https://gitlab.com/apgoucher/lifelib , https://pypi.org/project/python-lifelib/
- Contributor: whosedreams (V3R1T4S kit).
