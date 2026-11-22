# REPRODUCE skeptic verdict: instance 80 (80_14_10_2) at penalty 0

context: fresh subagent started for this claim only

Scope: only claim/ was read. All work was done in a scratch copy; claim/ was not modified. I wrote my own checker from the definition before reading claim/code/.

## Success criterion (quoted from target.md)
"A solution in the site's XML solution format for one instance listed on https://www.schedulingbenchmarks.org/matsp/ with a positive 'Best known' value, such that an independent checker written from the published ProblemDefinition.pdf (which first reproduces penalty 889 on the site's example file 8_7_20_2.Solution.889.xml) reports all hard constraints satisfied and a total penalty strictly below that instance's 'Best known' value, with the table and https://www.schedulingbenchmarks.org/changes.html re-fetched live immediately before claiming."

## Definition used (quoted from data/ProblemDefinition.txt)
- "Shifts must start at 00:00 or 06:00-10:00 or 14:00-18:00 or 20:00-23:45. A shift cannot start at 00:00 on the first day ... The only start time on the last day that is within the planning horizon is 00:00."
- "The minimum shift duration is six hours and the maximum duration is ten hours. The shift lengths are in 15-minute intervals i.e. {24…40}."
- C1 "An employee can only have one shift each day"; C2 "Shifts must finish within the planning horizon"; C3 "There must be at least 14 hours rest after a shift"; C4 "b_e ≤ Σ n_ed*15 ≤ c_e"; C5 "Maximum five consecutive shifts ... Σ_{j=d}^{d+5} z_ej ≤ 5"; C6 "Employees must be assigned to an activity for a minimum of one hour"; C7 activities exactly on on-duty intervals, at most one per interval; C8 "v_ia ≤ Σ_e x_eia − y_ia ≤ w_ia".
- Objective: "Minimise Σ_i Σ_a y_ia y_ia", y_ia "total number of assigned staff above the preferred maximum cover level" (y ∈ Z*, non-negative).

## Conventions decided from the example
The example solution data/8_7_20_2.Solution.889.xml uses <Day> 0..7 with the only Day-7 shift starting at 00:00, matching D = {0..h} (0-based calendar days). Cover lines in data/8_7_20_2.txt run from "1,06:00" to "8,05:45", i.e. 1-based calendar days. Time = minutes from 06:00 of calendar day 0; solution shift start = d*1440 + start − 360; cover line = (day−1)*1440 + time − 360. Cover table completeness asserted (h*96*|A| distinct entries for both instances).

## My checker (independent; scratch copy, not in claim/)
Checks: known/unique employees, absent employees vs minimum minutes; one shift per calendar day; allowed start times (15-min steps, day-0 restriction, last day 00:00 only); shift length 360-600 min; task IDs in range, task lengths positive multiples of 15; shift inside [0, h*1440]; 14 h rest between every successive pair of shifts (stricter than C3's next-day form); min/max total minutes; at most 5 working days in every window d..d+5, d = 0..h−5; every maximal same-task run of intervals (merged across adjacent blocks) ≥ 4 intervals; no double-booked interval; cover ≥ min for every interval and task (hard); penalty Σ max(0, count − max)².

## Results
- Example data/8_7_20_2.Solution.889.xml on data/8_7_20_2.txt: violations 0, penalty 889 (= declared 889). Evaluator reproduced.
- Claimed object/80_14_10_2.Solution.0.xml on data/80_14_10_2.txt: violations 0, penalty 0 (declared 0). All 10 employees present; no adjacent same-ID task blocks. object/80_14_10_2.Solution.0.xml is byte-identical to data/selected_solution.xml (sha256 a1398787…a972, as preregistered).
- Best known for instance 80 in data/matsp.html: row ['80','14','10','2','6','TRA26']; 0 < 6.
- Deterministic: pure function of the two files, no randomness; repeated runs identical.

## Corruption tests (all rejected by my checker)
remove a shift (employee 1; employee 4) -> min-minutes and under-cover violations; task block shortened to 45 min -> "run of 45min"; shift moved to break 14 h rest -> rest 735 min; start 12:00 -> bad start; shift 615 min -> bad length; shift past horizon end -> outside horizon; six shifts in days 0..5 -> C5 violation; two shifts on one day -> rejected; task ID 3 -> rejected; task ID switched -> under cover. The author's code/verify_claim.py also FAILs the three corruptions I fed it (45-min block, rest break, removed shift).

## REPRODUCE.md steps 1-2
- `sha256sum -c SHA256SUMS` and `sha256sum -c PREREG.sha256`: all OK.
- `code/verify_claim.py` on the example: violations 0, penalty 889, PASS. On the claim: violations 0, penalty 0, PASS. Matches my checker exactly.
- Step 3 (optional CP-SAT re-solve) not run; not needed, since a feasible roster at penalty 0 is checked directly.

## Optimality of 0
y_ia ≥ 0 (non-negative integers, and in any case y² ≥ 0), so the objective is a sum of squares and cannot be negative; penalty 0 is optimal for instance 80.

## Caveats
- I used the provided text extract data/ProblemDefinition.txt (no PDF text tool was available to re-extract data/ProblemDefinition.pdf); the quoted rules are consistent with the example reproducing 889.
- The live re-fetch of the table and changes page right before claiming is the lead's step (PREREG check 3), not reproduced here; the saved data/matsp.html (fetched 2026-11-22T08:03:12Z) lists 6.
- Cross-check with the official closed-source verifier is optional and left to the human.

pass: true
