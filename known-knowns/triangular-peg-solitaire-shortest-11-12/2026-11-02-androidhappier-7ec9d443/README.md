# A127500(12) <= 25: a 25-move solution of triangular peg solitaire on Triangle(12) (published bound: 29)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> The 25-move sequence in result/T12_25moves.txt is a legal Triangle(12) peg solitaire solution from single vacancy a3 to single peg j12, verified by two simulators, giving a(12) <= 25, strictly below the upper bound 29 in OEIS A127500 and on Bell's page as fetched 2026-11-02T17:31:50Z.

OEIS A127500 (George I. Bell, 2007) is the length of the shortest solution of triangular peg solitaire on the board
of side n, "beginning with one peg missing and ending with one peg", where "a move is one or more jumps by the same
peg". Bell computed a(n) up to n = 10 and gave 21 <= a(12) <= 29. This folder lowers the upper bound:

    A127500(12) <= 25

The object is object/T12_25moves.txt (sha256 7ec9d443efe7b234fb31c6d427820f067f3815e99dea8750a547bc1b53a6c78b), in
Bell's notation (a1 is the top corner, row r holds holes a..(r-th letter)). Each comma-separated item is one move:
one peg making the listed consecutive jumps. Start: every hole of Triangle(12) (78 holes) filled except a3. After
25 moves (76 jumps) a single peg is left at j12. object/BOUND.txt states the bound and pins the solution's sha256;
the checker recomputes every number in it from the solution.

In the panel files, result/T12_25moves.txt is this folder's object/T12_25moves.txt (byte-identical), and code/ and
fixtures/ are this folder's verify-it-yourself/ and verify-it-yourself/fixtures/ (see panel/REDACTIONS.md).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: under one second. Requirements: Python 3 (standard library only),
and a C compiler for the third simulator (skipped without one). The script checks the object's hash against
INDEX.csv and recomputes object/BOUND.txt. It replays the solution in three simulators: a standalone checker written
from the definition with the start vacancy given explicitly (check_peg.py), a second Python simulator (pegcheck.py),
and a C simulator in cube coordinates (pegsim2.c). It calibrates all three on Bell's published T9 (16), T10 (18),
T11 (28) and T12 (29) solutions and expects two corrupted T11 solutions to be rejected. Real output:
verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A127500 (%I #12, Sep 07 2015), comment | a(12) | 21 <= a(12) <= 29 (no pending draft) | a(12) <= 25 | 2026-11-02T17:31:50Z (scout); 2026-11-02T18:19:57Z (novelty panel) |
| G. I. Bell, Large Triangular Boards (last modified March 4th, 2007) | S(12) | 21 <= S(12) <= 29; shortest known T12 solution 29 moves, e11 to a3 | 25 moves, a3 to j12 | 2026-11-02T17:31:50Z; 2026-11-02T18:19:57Z (byte-identical) |

URLs: https://oeis.org/A127500 and https://www.gibell.net/pegsolitaire/LargeTriangular/index.html. Fetch records
and hashes: the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell: the upper bound for A127500(12). The exact value of a(12) is not claimed, and nothing is claimed
  about lower bounds (21 stands). The beam search is capped and heuristic; it proves nothing about shorter solutions.
- Triangle(11) is not part of this package (the same run's Triangle(11) result is a separate submission).
- Only this start/finish pair (a3 to j12) is shown; no claim is made about other vacancy/finish pairs.
- The fixtures in verify-it-yourself/fixtures/ are Bell's published solutions, transcribed for calibration, and two
  deliberately corrupted orders; they are test data, not results of this run.

## Credits

- George I. Bell: the sequence A127500, its terms and the bounds 21 <= a(12) <= 29, the 29-move Triangle(12)
  solution and the board notation; https://oeis.org/A127500,
  https://www.gibell.net/pegsolitaire/LargeTriangular/index.html, https://www.gibell.net/pegsolitaire/tindex.html,
  and "Solving Triangular Peg Solitaire", Journal of Integer Sequences 11 (2008), Article 08.4.8,
  https://cs.uwaterloo.ca/journals/JIS/VOL11/Bell/bell2.html (arXiv:math/0703865).
- Martin Gardner, "Penny Puzzles", in Mathematical Carnival (1975), cited by A127500.
- The OEIS Foundation, https://oeis.org.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
