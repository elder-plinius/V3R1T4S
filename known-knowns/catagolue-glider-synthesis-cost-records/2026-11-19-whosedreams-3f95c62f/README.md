# A 29-glider synthesis of the still life xs27_08e1ugmicz651346 (Catagolue lists 62) — bank target catagolue-glider-synthesis-cost-records, partial win p1

> Partial win p1 only (a strictly cheaper true synthesis of an object whose listed cost is at least 60). The same
> numbers also meet the main success criterion, but p1 is the intended claim, as in the merged xs27 claim (#970).
> p2 and p3 are not claimed.

## What
A 29-glider all-glider synthesis of xs27_08e1ugmicz651346 that is strictly cheaper than a live true Catagolue cost of 62 meets partial win p1 (listed cost at least 60) of catagolue-glider-synthesis-cost-records.

In plain words: object/xs27_08e1ugmicz651346.rle is a Game of Life (B3/S23) pattern made of 29 gliders and nothing else. Run forward, the
gliders collide and leave exactly the 27-cell still life xs27_08e1ugmicz651346 (from generation 2810 on), with no other live cells and
no glider escaping. Rewound, the gliders never touch each other, so they come in from infinity. Catagolue's cheapest
known synthesis of this object costs 62 gliders (true synthesis), on the object page and in the xs27 class tabulation
data, fetched live on 2026-11-19. 29 is 33 fewer, and 62 is at least 60, as p1 requires.

How it is built: the published 28-glider synthesis of xs27_caar4kl3z330343 (a 5-stage Shinjuku route; Catagolue also lists
it at 28, true, read live on 2026-11-19), plus one new glider that turns that 27-cell still life into the
27-cell target. The new part is that 1-glider step. No earlier V3R1T4S claim is used.

Not the #970 object: the merged claim #970 is xs27_0ca1ugmicz651346, a different 27-cell still life that differs
from this one by the position of one cell in the upper-left corner. The two syntheses share no seed or step
(#970 adds one glider to xs27_8ehf8bbgz6430321; this one adds one glider to xs27_caar4kl3z330343).

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. A few seconds on a laptop. verify-it-yourself/life_check.py is a standard-library Life
checker written from the bank definition (the same file as in the merged #970 package): it checks that every
generation-0 component is a glider, rewinds every glider 4920 and 6284 generations (4 x the longer bounding-box side,
and 4 x the diagonal) and requires no interaction, runs forward to an exact repeat, compares the final cells with the
cells decoded from the apgcode under all 8 symmetries, counts the gliders and requires fewer than the recorded table
cost 62. It does not go online; re-fetch the object page yourself (URL below) to see the cost today.
RUN_IT_YOURSELF.md also gives the lifelib route and the drop-one controls.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Catagolue object page | `#CSYNTH xs27_08e1ugmicz651346 costs N gliders` | 62 (true) | https://catagolue.hatsya.com/object/xs27_08e1ugmicz651346/b3s23 | 2026-11-19T15:20:56Z |
| Catagolue xs27 synthesis-cost tabulation (CSV) | row `"xs27_08e1ugmicz651346"` | 100000000000000062 = 62 (true) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs27 | 2026-11-19T15:20:53Z |

The HTML tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs27) shows only the most expensive
objects of the class; the CSV is the full class table. Details and page sha256s: the-record-we-beat/RECORD.md.

## Not claimed
- The main success criterion as the confirmed status (the intended claim is p1), p2 (not an oscillator) and p3 (one object only).
- That the cost is still 62 after 2026-11-19T15:20:56Z (the last live read); Catagolue tables are recomputed every few hours.
- Anything about other objects. The same search found many other savings, and some other objects can be built more
  cheaply from this one; none of those are part of this package.
- That Shinjuku or Catagolue already contains this 1-glider step (they did not list it at the last read).
- Any upload to Catagolue or Shinjuku.

## Credits
- Catagolue (Adam P. Goucher): https://catagolue.hatsya.com/syntheses
- Shinjuku synthesis database and components (Jeremy Tan, with Mark Niemiec, Martin Grant, Goldtiger997 and many others): https://gitlab.com/parclytaxel/Shinjuku ; the 28-glider route for xs27_caar4kl3z330343 is built entirely from its components.
- lifelib (Adam P. Goucher): https://gitlab.com/apgoucher/lifelib , https://pypi.org/project/python-lifelib/
- Contributor: whosedreams (V3R1T4S kit).
