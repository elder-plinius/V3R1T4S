# REPRODUCE review: claim/ (three XHSTT-2014 solutions)
context: fresh subagent started for this claim only

## What I did

1. `sha256sum -c SHA256SUMS` from inside claim/: every file OK, 0 failures.
2. Before opening claim/code/, I wrote my own evaluator, panel/work-reproduce/myeval.py (Python standard library only, about 450 lines). I wrote it from data/spec/spec.html (my text extraction is in panel/work-reproduce/spec.txt) and data/spec/constraints.txt/html. It covers:
   - Archive parsing: Times with Week/Day/TimeGroup membership; resources and resource groups; events with Duration, Workload, preassigned Time, event resources (Role, ResourceType, Workload) and event ResourceGroups, which count as preassigned resources with the event's workload; event groups from Course and EventGroups.
   - Solution reading, following the spec's default rules: a missing instance event gets one unassigned solution event of full duration; total durations must equal the event duration; preassigned times and resources are filled in.
   - Rejection checks: unknown event, time, resource or role; a role given twice; wrong resource type; a changed preassigned time or resource; duration below 1; an event running past the last time.
   - Cost: Weight x CostFunction (Linear, Quadratic, Step) of the deviation; Required constraints count toward infeasibility, the others toward the objective. Points of application are repeated when an event or resource appears more than once in AppliesTo, as the spec says.

   Constraint types in the three instance files (counted from the files):
   - AU-BG-98 (172 constraints): AssignResource 21, AssignTime 1, AvoidClashes 1, AvoidSplitAssignments 23, AvoidUnavailableTimes 6, DistributeSplitEvents 8, LimitBusyTimes 3, LimitWorkload 11, LinkEvents 1, PreferResources 87, PreferTimes 2, SplitEvents 7, SpreadEvents 1.
   - DK-HG-12 (36 constraints): AssignResource 1, AssignTime 1, AvoidClashes 1, ClusterBusyTimes 6, LimitBusyTimes 1, LimitIdleTimes 2, PreferResources 15, SpreadEvents 9.
   - DK-VG-09 (21 constraints): AssignResource 1, AssignTime 1, AvoidClashes 1, ClusterBusyTimes 2, LimitBusyTimes 1, LimitIdleTimes 2, PreferResources 1, SpreadEvents 12.

   All cost functions in the three files are Linear. Quadratic and Step are implemented but not exercised. LimitWorkload uses exact fractions and rounds each amount up.
3. I validated my evaluator against every stored solution in data/inst/*.xml and compared each with its dataset page (data/pages/*.html).
4. I evaluated the three objects, with extra structure checks (panel/work-reproduce/structcheck.py), and compared them with the overview bests (data/overview.html rows: AU-BG-98 126 with lower bound 0.0; DK-HG-12 12.2330 with LB 7.0; DK-VG-09 2.2323 with LB 2.0) and the page bests.
5. Only then did I read claim/code/ (xhstt_eval.py, verify.py, validate_57.py). I ran verify.py and compared its costs with mine per constraint id (panel/work-reproduce/compare.py). I ran 183 random and targeted corruptions through both evaluators, plus 5 end-to-end corrupted files through verify.py (panel/work-reproduce/corrupt/).
6. I re-downloaded the three instance files and the overview into panel/work-reproduce/dl/ (2026-11-28T09:09Z, all HTTP 200) and compared their hashes.

## My evaluator on every stored solution (infeasibility, objective)

The first run reproduced every value, with no tuning.

| instance | solution group | mine | dataset page |
|---|---|---|---|
| AU-BG-98 | JeffKingston_KHE_2011-02-11 | (7, 433) | 7 / 433 |
| AU-BG-98 | KHE_2014_02_10 | (3, 400) | 3 / 400 |
| AU-BG-98 | KHE_2014_02_20 | (3, 311) | 3 / 311 |
| AU-BG-98 | KHE_2014_02_27 | (2, 340) | 2 / 340 |
| AU-BG-98 | KHE_2014_03_13 | (1, 386) | 1 / 386 |
| AU-BG-98 | GOAL team - Feb 12, 2015 | (1, 363) | 1 / 363 |
| AU-BG-98 | GOAL team Feb 1 2016 | (0, 334) | 0 / 334 (embedded Report says 0.340: an older evaluator, ignored as instructed) |
| AU-BG-98 | GOAL team Dec 8 2016 | (0, 128) | 0 / 128 (page best) |
| DK-HG-12 | LectioALNS | (25, 33844) | 25 / 33844 |
| DK-HG-12 | KHE_2014_08_18 | (12, 3124) | 12 / 3124 |
| DK-HG-12 | GOAL Feb 12 2015 | (12, 3056) | 12 / 3056 |
| DK-HG-12 | Sequence-basedHH | (12, 2628) | 12 / 2628 |
| DK-HG-12 | GOAL Apr 26 2015 | (12, 2611) | 12 / 2611 |
| DK-HG-12 | GOAL Dec 8 2016 | (12, 2330) | 12 / 2330 (page best) |
| DK-VG-09 | LectioALNS | (2, 18862) | 2 / 18862 |
| DK-VG-09 | KHE14-2014-08-22 | (2, 4097) | 2 / 4097 |
| DK-VG-09 | GOAL Feb 12 2015 | (2, 2881) | 2 / 2881 |
| DK-VG-09 | Sequence-basedHH | (2, 2731) | 2 / 2731 |
| DK-VG-09 | GOAL Apr 26 2015 | (2, 2718) | 2 / 2718 |
| DK-VG-09 | GOAL Dec 8 2016 | (2, 2323) | 2 / 2323 (page best) |

20 of 20 values match the dataset pages.

## My evaluator on the three objects

Structure: each object is a solution-only archive (MetaData and SolutionGroups, no Instances) holding exactly one Solution. The Solution's Reference equals the instance Id, and its only child is Events, with no Report.

- AU-BG-98: covers all 387 events with 1047 solution events (285 events split).
- DK-HG-12: 1235 events and 1235 solution events, none split.
- DK-VG-09: 918 events and 918 solution events, none split.

In all three, no event is unknown, no duration sum is wrong, and myeval's rejection checks raised nothing. Those checks cover time and resource existence, roles, resource types, preassigned times and resources, and running past the end. DK-HG-12 leaves 6 events without a Time and DK-VG-09 leaves 2; these are scored as AssignTime violations, as in the GOAL solutions.

Costs by constraint type, with the best stored solution in brackets (H = hard, S = soft; every type not listed is 0):

- **AU-BG-98 object: (0, 91)** [GOAL Dec 2016: (0, 128)]
  - AvoidSplitAssignments S 70 [110]
  - LimitBusyTimes S 10 [10]
  - SpreadEvents S 11 [8]
  - All hard types are 0.
- **DK-HG-12 object: (12, 2326)** [GOAL Dec 2016: (12, 2330)]
  - AssignResource H 5 [5]
  - AssignTime H 6 [6]
  - AvoidClashes H 1 [1]
  - ClusterBusyTimes S 742 [742]
  - LimitBusyTimes S 424 [428]
  - LimitIdleTimes S 672 [672]
  - SpreadEvents S 488 [488]
- **DK-VG-09 object: (2, 2322)** [GOAL Dec 2016: (2, 2323)]
  - AssignTime H 2 [2]
  - ClusterBusyTimes S 398 [399]
  - LimitBusyTimes S 144 [144]
  - LimitIdleTimes S 236 [236]
  - SpreadEvents S 1544 [1544]

Comparison, hierarchical (lower infeasibility first, then lower objective):

- AU-BG-98: (0, 91) is below the overview best (0, 126) and the page best (0, 128).
- DK-HG-12: (12, 2326) is below (12, 2330) on both.
- DK-VG-09: (2, 2322) is below (2, 2323) on both.

All three rows meet the criterion under my evaluator.

## Comparison with verify.py and xhstt_eval.py

`python3 code/verify.py data/inst/{instance}.xml object/{file} {overview best} {page best}` printed PASS and exited 0 for all three rows:

| row | best stored (= page best) | object |
|---|---|---|
| AU-BG-98, bests 0.126 0.128 | (0, 128) | (0, 91) |
| DK-HG-12, bests 12.2330 12.2330 | (12, 2330) | (12, 2326) |
| DK-VG-09, bests 2.2323 2.2323 | (2, 2323) | (2, 2322) |

Its per-type costs are identical to mine (listed above). For a finer check I evaluated each constraint on its own in xhstt_eval.py and compared it with my per-constraint cost:

- AU-BG-98: 0 differences over 172 constraints.
- DK-HG-12: 0 differences over 36.
- DK-VG-09: 0 differences over 21.

The same holds for the three GOAL Dec 2016 solutions (0 differences each).

Reading the code: xhstt_eval.py follows the same reading of the spec as mine. Small implementation differences have no effect here:

- It stores workloads as floats and rounds up with a 1e-9 tolerance; I use exact fractions.
- It does not remove repeated members from an event group. I checked: no event group in the three files has a repeated member.
- It ignores roles unknown to the event, but verify.py rejects them separately.

## Corruption tests

compare.py ran 61 corruptions per object (183 in total) through both evaluators: random time moves, dropped times, same-type resource swaps, wrong-type resources, duration +1, an unknown event reference, a removed solution event, a preassigned time changed (AU), and moving the first event to the last time. **All 183 agree.** Every case either gave the same (infeasibility, objective) in both or was rejected by both. Tally: 77 rejected by both, 92 changed cost, 14 left the cost unchanged.

End-to-end with verify.py:

| corrupted input | verify.py | myeval |
|---|---|---|
| DK-VG-09 with one Time removed | FAIL, (3, 2367) | (3, 2367) |
| AU-BG-98 with an extra Role 99 | FAIL, "unknown role 99 in Sport_1" | INVALID |
| AU-BG-98 with a role given twice | FAIL | INVALID |
| DK-HG-12 object with its Reference changed to DK-VG-09 | FAIL, "must hold exactly one solution for DK-HG-12" | skips it |
| true DK-VG-09 object, page best given as 2.2322 | FAIL, best stored no longer matches the page | not applicable |
| true DK-VG-09 object, overview best given as 2.2322 | FAIL | not applicable |

## Instance file provenance

My re-downloads (2026-11-28T09:09Z, HTTP 200) are byte-identical to fetch.json and to claim/data/inst:

- AustraliaBGHS98.xml: sha256 b172c3db...
- DenmarkHasserisGymnasium2012.xml: sha256 9abb1e9b...
- DenmarkVejenGymnasium2009.xml: sha256 6970f763...
- overview.html: also byte-identical (b3f6718b...), so the bests had not changed at 09:09Z.

The dataset pages' hrefs (AustraliaBGHS98.xml, DenmarkHasserisGymnasium2012.xml, DenmarkVejenGymnasium2009.xml, relative to each page URL) resolve to the URLs in fetch.json. On the DK-HG-12 page the link text reads "HasserisGymnasium2012.xml", but the href points to DenmarkHasserisGymnasium2012.xml; this is only a cosmetic difference.

## Discrepancies and weaknesses found

1. **Thin margins.** DK-VG-09 wins by 1 objective point, a single ClusterBusyTimes deviation (399 to 398). DK-HG-12 wins by 4 points (LimitBusyTimes 428 to 424). Both rows therefore depend on reading those two constraint types exactly as HSEval does. Two independent readings (mine and the claim's) agree. Both reproduce all 20 stored values on these instances exactly, including the GOAL solutions' ClusterBusyTimes 399 and LimitBusyTimes 428. So the readings are checked by HSEval's own published values on these same constraints. A cross-check with HSEval itself was not done; it is excluded by the rules and disclosed in CLAIM.md.
2. **The validate_57 result cannot be reproduced from claim/.** validate_57.py reads raw/pages and raw/inst, which are not in claim/, and 5 of its 8 instances (DK-FG-12, NL-KP-03/05/09, UK-SP-06) have no data in claim/. I could only re-check the 20 values for the three claimed instances, and all of them reproduce. Its saved output also lists stored solutions that do not appear on their pages: NL-KP-03 has an extra (0, 527), and UK-SP-06 has an extra (386000, 136). This is consistent with "57 listed values reproduced as a multiset", but it means "reproduces all 57" is a multiset statement. It does not affect the three claimed rows.
3. **verify.py takes the overview best as a command-line argument and does not read data/overview.html.** I checked the overview rows by hand (126, 12.2330, 2.2323), so this is only a usability weakness, not an error.
4. **Embedded Report elements are stale.** In AU-BG-98, GOAL Feb 2016 carries a Report of 0.340, while the page and both evaluators give 334. The other embedded reports (12.2611, 2.2718) agree. Both evaluators ignore Reports, as they should.
5. Quadratic and Step cost functions, and OrderEvents, are not exercised by these files. This is irrelevant to the claim.
6. Not a REPRODUCE issue, recorded for the panel: each object differs substantially from the best stored GOAL solution. The share of events whose start times differ is 327 of 387 (AU), 403 of 1235 (DK-HG-12) and 746 of 918 (DK-VG-09). So the objects are not trivial edits of the record holder's file, but judging novelty is the other reviewers' job.

None of these affects the claimed costs.

## Verdict

I reproduced the claim independently. An evaluator written from the spec before reading the claim's code reproduces all 20 dataset-page values for the three instances. It scores the objects at AU-BG-98 (0, 91), DK-HG-12 (12, 2326) and DK-VG-09 (2, 2322), and all three objects are structurally valid. Each cost is hierarchically strictly below the overview best and the dataset-page best. The claim's verify.py prints PASS on all three and agrees with my evaluator constraint by constraint and on 183 corruptions. The instance files are the ones the dataset pages serve today. The main caveat is the 1-point and 4-point margins on the DK rows; they are backed by exact reproduction of HSEval's published values, but not by HSEval itself.

pass: true
