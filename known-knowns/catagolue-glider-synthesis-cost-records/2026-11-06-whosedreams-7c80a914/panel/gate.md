# Honesty gate: run 2026-11-06-xs27-confirm, catagolue-glider-synthesis-cost-records, xs27_0ca1ugmicz651346, partial win p1

context: written 2026-11-06T16:36:04Z (date -u), after reading panel/reproduce.md, panel/novelty.md and
panel/criterion.md in full. It carries over the reading of the earlier gate written when the panel ran (2026-11-06
10:23 ET); no vote was changed, re-run or written here.

## Panel files (written 2026-11-06, each in a fresh subagent context; edited 2026-11-17 only as noted at the end)
- reproduce.md: pass: true. Own checker: 32 generation-0 gliders only (160 cells); rewind T=10916 (4 x bounding-box
  diagonal 2729); settles by about generation 4333 into the 27-cell still life xs27_0ca1ugmicz651346, period 1, no debris.
- novelty.md: pass: true. Live fetch 2026-11-06 10:20:34 ET: object page `#CSYNTH xs27_0ca1ugmicz651346 costs 66 gliders (true).`;
  xs27 tabulation CSV 100000000000000066 (66 true). Seed: the published 31-glider xs27_8ehf8bbgz6430321 plus one new
  glider. No match in TROPHY_CASE, known-knowns or kit PRs.
- criterion.md: pass: true. The claim asserts p1; listed true cost 66 is at least 60 and 32 is strictly below it. The
  panelist notes the same facts would also meet the main criterion, but its confirmed_scope is the p1 sentence, so this
  gate records p1 only.

## This run's own checks
- Independent checker (verify-it-yourself/life_check.py), standard library only: PASS (32 gliders, rewind ok at 8004
  and 10916, still life from generation 4332, exact match, 32 < 66); 32 drop-one negatives fail; the 31-glider
  sub-pattern builds xs27_8ehf8bbgz6430321 (output in verify-it-yourself/RECEIPTS.md).
- Author's verifier (how-we-built-it/code/verify_synthesis.py) re-run 2026-11-06T16:16:21Z: ok true, live_csynth 66 true
  (how-we-built-it/data/verify_xs27_rerun.json).
- Live table (the-record-we-beat/RECORD.md, 2026-11-06T16:15:00Z): object page 66 true; xs27 textcensus row 100000000000000066 (66 true).

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no; all three pass outright.
- Reproduction mismatch: none (three simulators agree: the reviewer's, life_check.py, lifelib).
- Value strictly better than the live table: yes, 32 < 66 on the object page and in the class tabulation data, read
  2026-11-06 at 10:20 ET, 11:15 ET and 11:16 ET (UTC-5), all under 6 hours old at this gate; 66 >= 60 for p1.
- Stretched criterion or hidden quantifier: no; "at least 60" and "strictly fewer" both hold on the live numbers.
- Scope wider than reproduced: no; one object, one synthesis; the main-criterion reading is not claimed.
- Several objects bundled: no.
- Plan frozen after the search: yes, disclosed in PREREG.md; the claim was built in the earlier search before any
  PREREG existed. This run froze its plan before copying the claim in, and judged only the already-built object.
Result: no downgrade.

## Edits after the gate (2026-11-17, at the maintainer's request)
The internal filing note and private workspace path were removed from this file, and the checks above now point to
the package files holding their results; private workspace references were removed from how-we-built-it/PREREG.md;
a dated layout note was added atop panel/criterion.md, panel/reproduce.md and panel/novelty.md. No vote, verdict,
status or confirmed_scope was changed.

status: CONFIRMED_PARTIAL
partial win: p1
confirmed_scope: A 32-glider all-glider synthesis of xs27_0ca1ugmicz651346 that is strictly cheaper than a package-stated live true Catagolue cost of 66 meets partial win p1 (listed cost at least 60) of catagolue-glider-synthesis-cost-records.
