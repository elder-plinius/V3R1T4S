# A 12-glider synthesis of the still life xs26_08ehmkk8z6a87066 (Catagolue lists 58) — bank target catagolue-glider-synthesis-cost-records, main success criterion

> Main success criterion only. Partial win p1 is NOT claimed: p1 needs a listed cost of at least 60, and this
> object's listed cost is 58.

## What
Confirmed scope (from panel/gate.md, verbatim): A package-stated 12-glider all-glider synthesis of xs26_08ehmkk8z6a87066 uses strictly fewer gliders than the claimed live true cost of 58 on both the object page and the xs26 synthesis-costs tabulation data, meeting the main success criterion of catagolue-glider-synthesis-cost-records (not partial win p1).

In plain words: object/xs26_08ehmkk8z6a87066.rle is a Game of Life (B3/S23) pattern made of 12 gliders and nothing else. Run forward, the
gliders collide and leave exactly the 26-cell still life xs26_08ehmkk8z6a87066 (from generation 1774 on), with no other live cells and
no glider escaping. Rewound, the gliders never touch each other, so they come in from infinity. Catagolue's cheapest
known synthesis of this object costs 58 gliders (true synthesis), on the object page and in the xs26 class tabulation
data, fetched live on 2026-11-06. 12 is 46 fewer.

How it is built: the published 11-glider synthesis of xs28_651ugmmz69706221 (a 3-stage Shinjuku route), plus one new
glider that turns that 28-cell still life into the 26-cell target. The new part is that 1-glider transfer.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3 3.8+, no other packages).
Expected last line: `PASS`. About 2 seconds on a laptop. verify-it-yourself/life_check.py is a standard-library Life
checker written from the bank definition: it checks that every generation-0 component is a glider, rewinds every glider
2860 and 4040 generations (4 x the longer bounding-box side, and 4 x the diagonal) and requires no interaction, runs
forward to an exact repeat, compares the final cells with the cells decoded from the apgcode under all 8 symmetries,
counts the gliders and requires fewer than the recorded table cost 58. It does not go online; re-fetch the object page
yourself (URL below) to see the cost today. RUN_IT_YOURSELF.md also gives the lifelib route.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Catagolue object page | `#CSYNTH xs26_08ehmkk8z6a87066 costs N gliders` | 58 (true) | https://catagolue.hatsya.com/object/xs26_08ehmkk8z6a87066/b3s23 | 2026-11-06T16:05:53Z |
| Catagolue xs26 synthesis-cost tabulation (CSV) | row `"xs26_08ehmkk8z6a87066"` | 100000000000000058 = 58 (true) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 | 2026-11-06T16:05:53Z |

The HTML tabulation (https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs26) shows only the most expensive
objects of the class and does not list this one; the CSV is the full class table. Details and page sha256s:
the-record-we-beat/RECORD.md.

## Not claimed
- Partial win p1 (listed cost 58 is below 60), p2 (not an oscillator) and p3 (one object only).
- That the cost is still 58 after 2026-11-06T16:10:54Z (the last live read); Catagolue tables are recomputed every few hours.
- Anything about other objects; the run that found this one also found many smaller savings, which are not part of this package.
- Any upload to Catagolue or Shinjuku.

## Credits
- Catagolue (Adam P. Goucher): https://catagolue.hatsya.com/syntheses
- Shinjuku synthesis database and components (Jeremy Tan, with Mark Niemiec, Martin Grant, Goldtiger997 and many others): https://gitlab.com/parclytaxel/Shinjuku ; the 11-glider seed route for xs28_651ugmmz69706221 is theirs (components in transfer_20210826.sjk and contrib_20260923.sjk, and the route into xs20_6s1v0rrzw1).
- lifelib (Adam P. Goucher): https://gitlab.com/apgoucher/lifelib , https://pypi.org/project/python-lifelib/
- Contributor: whosedreams (V3R1T4S kit).
