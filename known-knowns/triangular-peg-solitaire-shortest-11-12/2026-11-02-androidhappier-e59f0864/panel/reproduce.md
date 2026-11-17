# REPRODUCE skeptic verdict: claim 2026-11-02-1731

context: subagent (reproduce skeptic, isolated claim copy)

Scope: I read only the claim copy. All paths below are relative to claim/. I wrote my own checker before I opened code/pegcheck.py or code/pegsim2.c.

## Definition used (quoted from data/A127500.txt)
- %N: "On the triangular peg solitaire board of side n, the shortest solution to any problem beginning with one peg missing and ending with one peg."
- %C: "Shortest means the minimum number of moves, where a move is one or more jumps by the same peg. The reference calculates a(n) up to n=10 and gives the bounds 19<=a(11)<=28, 21<=a(12)<=29, ..."

Notation (from claim.md, Bell): a hole is a column letter plus a row number, and a1 is the top corner. Row r holes are a..(r-th letter). Jumps run along the three lattice directions.

## My checker (independent; saved beside this file as reproduce_mycheck.py)
- Board: holes (r,c) with 1<=c<=r<=n. Letter = column c, number = row r. That gives 66 holes for n=11.
- A jump goes from p over the middle hole to p+2d, where d is one of (0,+-1), (+-1,0), (+1,+1) or (-1,-1). Each jump must stay on the board, start on a peg, pass over a peg and land in an empty hole. It then empties p and the middle hole and fills the landing hole.
- A move is one comma-separated item. It is a chain x1-x2-...-xk, so every jump in it is made by the same peg. Square brackets in the fixtures are removed and a trailing "(N)" is ignored.
- Start: a full board minus the given vacancy. Finish: list the holes that still have pegs.
- I also counted adjacent items where the next move starts at the hole where the previous one ended. These are moves by the same peg that could be merged into one. The count is 0 for the result, so 22 is a true move count under the definition.

## What I verified
- result/T11_22moves.txt has sha256 e59f0864e5e9fc3034f2ee6815a92a2fa05775d4b1e2f6f3515082553a6ef6f4, matching claim.md.
- My checker on n=11 with vacancy a2: every jump is legal. The result is 22 moves and 64 jumps (64 = 66-2). Exactly one peg is left, at j11. No two adjacent moves use the same peg.
- The run is deterministic: a second run gave identical output (22, 64, ['j11'], 0).
- Calibration: I tried every possible vacancy on Bell's fixtures. Each one is valid for exactly one vacancy:
  - T9 is 16 moves from a2 to i9.
  - T10 is 18 moves from a3 to c6.
  - T11 is 28 moves from a4 to a1.
  - T12 is 29 moves from e11 to a3.
  - Each published count matches. fixtures/neg_T11_swapped.txt and fixtures/neg_T11_order.txt are rejected for every vacancy.
- The author's tools agree, checked only after my own run:
  - code/pegcheck.py reports "start_vacancy=a2 pegs_left=1 finish=j11 jumps=64 moves=22 VALID".
  - code/pegsim2.c, compiled with gcc -O2, reports "jumps=64 moves=22 pegs_left=1 VALID".
  - Both give the same calibration results as mine. The negatives are ILLEGAL (b2-d4, a6-a4).
- This is a witness claim, not an exhaustive search. A single legal solution is enough to show A127500(11) <= 22. I did not re-run code/beam3.c, and the claim does not depend on it.
- The comparison with the published bound of 28 (data/A127500.txt) belongs to the criterion and novelty reviewers. Here I only confirm that 22 < 28 is consistent with the saved data file.

## Conclusion
The claim reproduces. The saved file is a legal 22-move solution on Triangle(11), starting with a2 empty and ending with one peg on j11.

pass: true
