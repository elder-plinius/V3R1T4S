# REPRODUCE skeptic: T12 in 25 moves

context: subagent (reproduce skeptic, isolated claim copy)

Scope: I read only the isolated copy of claim/. All paths below are relative to claim/. My own checker lives outside panel/, in a private /tmp scratch dir, and I wrote it before opening code/.

## Definition (quoted from data/A127500.txt)
"On the triangular peg solitaire board of side n, the shortest solution to any problem beginning with one peg missing and ending with one peg."
"Shortest means the minimum number of moves, where a move is one or more jumps by the same peg."
Board notation (claim.md, Bell): hole = column letter + row number, a1 = top corner, row r has holes a..(r-th letter). Jumps run along the three lattice directions.

## Independent checker (written from the definition)
- Holes are (c,r) with 1<=c<=r<=12, giving 78 holes. Every named hole is checked to be on the board.
- A jump goes from p over q=p+d into t=p+2d, with d in {(±1,0),(0,±1),±(1,1)}. It needs p and q to have pegs and t to be empty.
- Every hole starts with a peg except one. The vacancy is taken from the landing hole of the first jump, and the checker then confirms that all later jumps are legal from that state.
- A move is one comma-separated item, which is a chain of jumps by the same peg. I also merged any consecutive items where the same peg keeps jumping. The merged count is still 25, so no item was double-counted and nothing would shrink further.
- At the end it counts the pegs left on the board.

## Results
- result/T12_25moves.txt (sha256 7ec9d443…c78b, same as claim.md): n=12, holes=78, start=a3, moves=25 (merged 25), jumps=76 (=78-2), pegs left=1, finish=j12, VALID. I ran it twice and got identical output both times, so the result is deterministic.
- Calibration on Bell's published fixtures: T9 gives 16 moves VALID, T10 gives 18 VALID, T11 gives 28 VALID (a4 to a1), and T12 gives 29 VALID (e11 to a3, matching Bell's page).
- Negative controls: fixtures/neg_T11_swapped.txt fails as illegal at b2-d4, and fixtures/neg_T11_order.txt fails as illegal at a6-a4. My checker rejected both.
- Author tools agree: code/pegcheck.py reports "start_vacancy=a3 pegs_left=1 finish=j12 jumps=76 moves=25 VALID". code/pegsim2.c (compiled to /tmp) reports "jumps=76 moves=25 pegs_left=1 VALID". Both get the same fixture results as mine (16/18/28/29 VALID, both negative controls ILLEGAL).
- Published bound: data/A127500.txt says "21<=a(12)<=29", and data/bell_large_triangular.html says "S(12)&le;29". 25 < 29, so this beats the bank criterion of at most 28 for T12.

## Verdict
Every property checks out: legal jumps on Triangle(12), a single starting vacancy at a3, a single survivor at j12, 25 moves, deterministic output. A solution with 25 moves means A127500(12) <= 25. This is an upper bound only, not an exact value, and the claim only asserts the upper bound.

pass: true
