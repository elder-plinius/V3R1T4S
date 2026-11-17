# CRITERION skeptic — claim 2026-11-02-1731 (Triangle(11))
context: subagent (criterion skeptic, isolated claim copy)

## What was read
Only claim/: claim.md, table_record.md, REPRODUCE.md, result/T11_22moves.txt, code/pegcheck.py, code/pegsim2.c, fixtures/, data/.

## Checks
- result/T11_22moves.txt sha256 e59f0864...6ef6f4 matches claim.md.
- code/pegcheck.py 11 result/T11_22moves.txt: start_vacancy=a2, pegs_left=1, finish=j11, jumps=64, moves=22, VALID.
- code/pegsim2.c (compiled fresh): jumps=64 moves=22 pegs_left=1 VALID.
- My own throwaway re-implementation (skew coords, six lattice directions, peg/mid/landing checks): all 64 jumps legal, one peg left at j11, 22 comma-separated moves, 0 adjacent items where one ends at the hole the next starts from (so no two listed items merge into one move; 22 is the A127500 move count, not an undercount or overcount).
- Calibration: fixtures/bell_T9_16, bell_T10_18, bell_T11_28, bell_T12_29 VALID at 16/18/28/29; fixtures/neg_T11_swapped and neg_T11_order ILLEGAL. The checker does reject bad input and does reproduce Bell's counts.
- Jumps = 64 = T(11) - 2: a single vacancy at the start and a single peg at the end, as required.

## Hidden quantifiers / definitions
- "Shortest solution to any problem beginning with one peg missing and ending with one peg" (data/A127500.txt) is a minimum over every start and finish pair. So one legal a2 -> j11 solution in 22 moves is enough to show a(11) <= 22. The finish can be anywhere, and the solution does not have to be a complement problem.
- "Move = one or more jumps by the same peg": counted as maximal runs. The file matches this, with no merges (see above).
- The criterion's "at most 27 moves" is met: 22 <= 27.
- "Strictly better than the bounds in the live OEIS A127500 entry and Bell's page at claim time": data/A127500.txt (fetched 2026-11-02T17:31:50Z) says 19<=a(11)<=28. data/A127500_draft.html shows no pending edit. data/bell_large_triangular.html says 19<=S(11)<=28, and its shortest known T11 is 28. 22 < 28 on both. I could not re-fetch the live pages under isolation, so "at claim time" rests on these snapshots, which are hash-recorded in table_record.md.
- Bell's page says "it is believed that S(11) is 20, 21, or 22". That is a conjecture, not a published bound. 22 fits it and still beats the published upper bound of 28. The claim does not show a(11) = 22, and it claims no exact value or lower bound (p2 is not claimed).
- Null models: the trivial bound T(11)-2 = 64 and the published 28 are both far above 22. 22 >= 19 (the published lower bound), so there is no contradiction that would suggest a checker bug.

## Classification
This is the first improvement past the published upper bound of 28 for Triangle(11). That makes it the FULL success criterion (first alternative: a Triangle(11) solution in <= 27 moves, verified by a simulator, strictly better than OEIS and Bell). It is not p1, because there was no earlier published improvement to go beyond. Nothing about T(12) is claimed or checked.

confirmed_scope: The 22-move sequence in result/T11_22moves.txt is a legal Triangle(11) peg solitaire solution from the single vacancy a2 to the single peg j11 (64 jumps), checked by two included simulators and an independent re-check, so a(11) <= 22, strictly below the upper bound 28 in the OEIS A127500 and Bell page snapshots in data/; this is an upper bound only, not an exact value of a(11).
pass: true
