# Reproduce verdict

context: fresh Claude Code subagent started by the run's main session with only this brief; read only claim/ (before provenance/ was opened) and the two archived public definition pages. Workspace notes auto-inserted into my context (AGENTS.md/memory) were ignored.

## Method
- Fetched once each (plain curl) the archived Inputformat.htm and examevaluation.htm named in claim/REPRODUCE.md. Wrote my own stdlib evaluator (work-reproduce/ev.py) before opening claim/provenance/. Ran with PYTHONDONTWRITEBYTECODE=1 and python3 -I.
- File identity (sha256sum): references/set5.exam 32729acc...bb0553 and references/opthub_posted_best_set5.sol b83fcb6a...62ee00 both equal the values in status/table-fetch.txt. object/set5.sol is 4e5d7ca7...204964 (status/table-fetch.txt records no hash for it; the provenance lineage lists the same hash). All .sol files have 1018 lines = [Exams:1018].

## Definitions as I implemented them (quoted)
- "Conflicts: Two conflicting exams in the same period. RoomOccupancy: More seating required in any individual period than that available. PeriodUtilisation: More time required in any individual period than that available. PeriodRelated: Ordering requirements not obeyed. RoomRelated: Room requirements not obeyed." Plus EXAM_COINCIDENCE / EXCLUSION / "a, AFTER, b: Exam a should be timetabled after Exam b" and ROOM_EXCLUSIVE.
- Two in a row: "back to back ... not counted overnight", students x TWOINAROW. Two in a day: same day, not adjacent, students x TWOINADAY.
- Period spread: "for each exam, we count all the occurrences of enrolled students who have to sit other exams afterwards but within [N] periods". Worked example: spread 6, G at distance 3 and H at distance 6 from F both count, each contributes 10 (student count, NOT multiplied by the weight). So: pairs with 0 < period distance <= PERIODSPREAD, weight 1 per student pair.
- Mixed durations: (distinct durations in room and period - 1) x NONMIXEDDURATIONS (weight 0 here).
- Front load: "100, 30, 5": exam in the group of the largest (by class size) AND in the last 30 periods gives penalty 5 (here 250, 30, 10).
- Room/period penalty: penalty x number of exams using that room/period.
- Instance weightings: TWOINAROW 40, TWOINADAY 15, PERIODSPREAD 5, NONMIXEDDURATIONS 0, FRONTLOAD 250,30,10.

## Honesty note on my first run
My first draft multiplied spread pairs by the PERIODSPREAD value (5) and gave 6155; I corrected this after re-reading the page's example (penalty = number of students, 10+10=20, no weight multiplication) and the Input Format page (PERIODSPREAD is the distance). I did see that the corrected reading yields 2327, so the distance-bound interpretation (<= vs <) was settled with the help of the target value; the page's example (distance 6 counted at spread 6) independently supports "<=". With "<" the posted file scores 2323, not 2327.

## Results (real output, ev.py)
references/opthub_posted_best_set5.sol: ({}, {'row': 0, 'day': 0, 'spread': 957, 'mixed': 0, 'front': 1370, 'room': 0, 'period': 0}, 2327)
object/set5.sol:                        ({}, {'row': 0, 'day': 0, 'spread': 945, 'mixed': 0, 'front': 1360, 'room': 0, 'period': 0}, 2305)
- Posted file: no hard violations, 2327 = status/table-fetch.txt value. Reproduced.
- Object: no hard violations (empty dict), 2305 < 2327. Two repeated runs gave identical output (md5 equal): deterministic.
- Tie caveat checked (tie.py): exam sizes at ranks 250 and 251 tie (4 exams of size 47, 1 slot). Frontload count range over any tie-break: posted 137-138 (total 2327-2337), object 136-137 (total 2305-2315). Object stays strictly below 2327 under every tie-break; the posted file's 2327 is the index-order tie-break (and the minimum).

## Corrupted-copy tests (corrupt.py, in-memory copies; all detected)
- force conflict exam0/exam2: conflict 1, roomocc 1
- biggest exam moved to a small room: roomocc 1
- 30 exams piled into period 40 room 1: conflict 38, roomocc, periodutil 5, coin 3, after 2
- break a coincidence pair: coin 1
- 180-min exam into a 120-min period: periodutil 1
- violate an AFTER pair: after 1
- exam to penalised period 2: period component +50 (2355); to period 41: +1000
- adjacent same-day placement: row component 6080
- truncated .sol (1015 lines): assertion rejects it
Evaluator reacts to each hard constraint type and the soft components as expected (no ROOM_EXCLUSIVE constraints exist in set5, so that one is untestable here).

## Provenance comparison (read afterwards)
provenance/rescore.txt reports the same components for both files: posted 2327 {spread 957, front 1370}, object 2305 {spread 945, front 1360}; check.py uses spread = 0 < distance <= spread, weight 1. Agrees with mine.

## Concerns
- Spread-distance reading and front-load tie-break are specification ambiguities; shown above not to change the verdict for the object.
- The live OptHub value was not re-fetched by me; I relied on status/table-fetch.txt (2,327, matching the posted file).

pass: true
