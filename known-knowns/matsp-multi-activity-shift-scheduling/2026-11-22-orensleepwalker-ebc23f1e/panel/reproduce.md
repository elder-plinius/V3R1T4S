# REPRODUCE skeptic verdict: matsp instance 155 at penalty 0

context: fresh subagent started for this claim only

Inputs read: CLAIM.md, target.md, PREREG.md, REPRODUCE.md, data/ProblemDefinition.txt, data/*.txt, data/*.ros, data/*.xml, data/matsp.html, object/155_28_10_2.Solution.0.xml. I wrote my own evaluator before opening code/. All work was done on a scratch copy; claim/ was not modified.

## Success criterion (quoted from target.md)
"A solution in the site's XML solution format for one instance listed on https://www.schedulingbenchmarks.org/matsp/ with a positive 'Best known' value, such that an independent checker written from the published ProblemDefinition.pdf (which first reproduces penalty 889 on the site's example file 8_7_20_2.Solution.889.xml) reports all hard constraints satisfied and a total penalty strictly below that instance's 'Best known' value"

## Definition used (quoted from data/ProblemDefinition.txt)
- "Shifts must start at 00:00 or 06:00-10:00 or 14:00-18:00 or 20:00-23:45. A shift cannot start at 00:00 on the first day ... The only start time on the last day that is within the planning horizon is 00:00."
- "The minimum shift duration is six hours and the maximum duration is ten hours." L = {0, 24..40} intervals.
- C1: at most one shift per day. C2: "Shifts must finish within the planning horizon" (u_ed <= h*96). C3: "There must be at least 14 hours rest after a shift." C4: b_e <= sum n_ed*15 <= c_e. C5: "The maximum number of shifts an employee can work without a day off is five. A day is considered as a working day if a shift starts on that day" (sum z over d..d+5 <= 5). C6: "Employees must be assigned to an activity for a minimum of one hour." C7: activities are assigned exactly on on-duty intervals, with one activity per interval. C8: v_ia <= sum_e x_eia - y_ia <= w_ia.
- Objective: "Minimise sum_i sum_a y_ia * y_ia". Here y_ia is a non-negative integer (y in Z*), so the objective is a sum of squares and is >= 0. With y at its optimum, max(0, cover - max), C8 is the hard rule cover >= min.

## My evaluator
Time is counted in minutes from 00:00 on calendar day 0, and the horizon is [06:00 day 0, 06:00 day h). The cover file's "Day k" means calendar day k-1. I chose this because the example's cover runs from Day 1 06:00 to Day 8 06:00 for h=7. I set the solution `<Day>` offset from the example. Offset 0 (Day 0 = first calendar day) gives **violations 0, penalty 889**. Offset 1 gives 456 violations and penalty 920. So solution days count from 0.

The evaluator checks every hard rule:
- start-time windows, no 00:00 start on day 0, and only 00:00 on day h;
- shift length 360-600 min in multiples of 15, with the task lengths summing to the shift length;
- each shift lies inside the horizon;
- rest of at least 840 min between consecutive shifts;
- min/max total minutes for every employee, including employees with no shifts;
- at most 5 working days in any 6-day window d..d+5, d=0..h-5;
- every contiguous same-task block lasts at least 60 min. I apply this strictly, including blocks at the horizon edges;
- one task per interval, and no assignment outside the cover table;
- cover >= min for every (interval, task).
The penalty is the sum of max(0, cover-max)^2.

I also cross-checked data/155_28_10_2.txt against data/155_28_10_2.ros. The cover tables are identical (5376 entries), and so are the staff min/max values for all 10 employees. The .ros contract (MinRestTime 840, MaxSeq 5, task min length 60, shift 360-600, the same start ranges) matches the definition.

## Claimed roster (object/155_28_10_2.Solution.0.xml)
- Byte-identical to data/selected_solution.xml (sha256 ebc23f1e..., as in PREREG.md).
- My evaluator: **violations 0, penalty 0**. It covers 10 employees, 99 shifts and 430 task entries.
- On the stricter readings it still has 0 violations. No two adjacent task entries share an ID, and the shortest raw task entry is 60 min, so the C6 result does not depend on merging same-task blocks.
- The table in data/matsp.html (fetched 2026-11-22T08:03:12Z) lists row "155 28 10 2 24 TRA26". 0 < 24.
- Optimality: the objective is a sum of squares of non-negative integers, so it cannot be negative, and 0 is optimal.

## Corruption tests (my evaluator rejects every infeasible copy)
| copy | detected |
|---|---|
| remove a shift | min minutes + undercover |
| task block 60 -> 45 (next block +15) | block 45 min + undercover |
| move a start so rest is 825 min | rest violation |
| start at 11:00 | start not allowed |
| shift 615 min | length violation |
| shift 345 min | length + block + min minutes |
| swap a task ID | undercover |
| 6 working days in a row (clean rest) | >5 in 6 |
| two shifts on one day | >1 shift per day + rest + max minutes |
| 00:00 start on day 0 | start rule + outside horizon |
| day 28 00:00 for 375 min | outside horizon |
| drop an employee | absent with positive min + undercover |
A control copy adds a day-28 00:00 shift of 360 min, ending exactly at 06:00. It is correctly feasible and only adds penalty 24. The author's code/verify_claim.py also reports FAIL on every corrupted copy.

## REPRODUCE.md steps 1-2
- Step 1: `sha256sum -c SHA256SUMS` passes for all 20 files, and `sha256sum -c PREREG.sha256` passes.
- Step 2: code/verify_claim.py gives "violations 0, penalty 889 ... PASS" on the example and "violations 0, penalty 0 ... PASS" on the claim. Two runs gave identical output (deterministic). This agrees with my independent evaluator.
- Step 3 (optional CP-SAT re-solve) was not run. It is not needed to verify a feasible roster.

## Caveats (do not block the pass)
- pdftotext was not available, so I worked from the sha-checked text extract data/ProblemDefinition.txt rather than the PDF itself.
- The closed-source official verifier was not run, per the target rules. Any later disagreement from the human's cross-check would withdraw the claim.
- PREREG check 3 (re-fetch the table and the changes page before filing) is a lead-agent step and was not done here.
- A best known value of 24 with a feasible 0 available is surprising, but the roster checks out under my independent reading of the definition.

pass: true
