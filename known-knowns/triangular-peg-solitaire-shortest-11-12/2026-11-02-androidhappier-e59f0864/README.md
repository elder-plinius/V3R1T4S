# A127500(11) <= 22: a 22-move solution of triangular peg solitaire on Triangle(11)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> The 22-move sequence in result/T11_22moves.txt is a legal Triangle(11) peg solitaire solution from the single vacancy a2 to the single peg j11 (64 jumps), checked by two included simulators and an independent re-check, so a(11) <= 22, strictly below the upper bound 28 in the OEIS A127500 and Bell page snapshots in data/; this is an upper bound only, not an exact value of a(11).

OEIS A127500 is the length of the shortest solution of triangular peg solitaire on the board of side n, over every
problem that starts with one peg missing and ends with one peg, where a move is one or more consecutive jumps by the
same peg. a(4..10) = 5, 9, 9, 12, 13, 16, 18 are known exactly. For n = 11 the entry, and George I. Bell's page on
large triangular boards, give 19 <= a(11) <= 28; the best published Triangle(11) solution has 28 moves (a4 to a1).
This folder gives a solution in 22 moves:

    Triangle(11), start: every hole filled except a2; finish: one peg on j11; 64 jumps in 22 moves.
    So A127500(11) <= 22.

The object is object/T11_22moves.txt (sha256 e59f0864e5e9fc3034f2ee6815a92a2fa05775d4b1e2f6f3515082553a6ef6f4), one
line in Bell's notation (hole = column letter + row number, a1 = the top corner; each comma-separated item is one
move, the hole names of one peg's jump chain). It is the file the panel read as result/T11_22moves.txt, byte for byte.
The "data/" snapshots that the confirmed scope names are the run's copies of the OEIS and Bell pages. They are not
shipped (third-party pages); their URLs, fetch times and sha256 are in the-record-we-beat/TABLE_SNAPSHOT.md, and a
fresh fetch while packaging returned the same bytes.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: under 2 seconds. Requirements: Python 3 (standard library only), plus
a C compiler for the third simulator (skipped without one). The script checks the object's hash against INDEX.csv,
then replays the solution with three simulators: check_peg.py (written for this package from the definition; the
start vacancy is given, not inferred, and it also checks that no two listed moves could merge into one), pegcheck.py
and pegsim2.c (the run's two checkers; the C one uses cube coordinates). The original run calibrated all three against Bell's published solutions, but those third-party move lists and their
modified copies are not included here; the current script skips that calibration. Historical and current checks are
distinguished in verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A127500 (DATA 5,9,9,12,13,16,18 for n = 4..10; comment) | a(11) | 19 <= a(11) <= 28 | a(11) <= 22 | 2026-11-02T17:31:50Z (scout); 18:17:50Z (novelty panel); 18:20:55Z (packaging) |
| G. I. Bell, Large Triangular Boards ("Last modified March 4th, 2007") | S(11) | 19 <= S(11) <= 28; shortest known solution 28 moves (a4 to a1) | 22 moves (a2 to j11) | 2026-11-02T17:31:50Z (scout); 18:17:51Z (novelty panel); 18:20:55Z (packaging) |

URLs: https://oeis.org/A127500 (text form https://oeis.org/search?q=id:A127500&fmt=text),
https://www.gibell.net/pegsolitaire/LargeTriangular/index.html. Fetch record: the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only an upper bound for one cell, A127500(11). It is not an exact value: no lower bound above the published 19 is
  claimed, and nothing shows that 21 or fewer moves are impossible. Bell writes that he believes S(11) is 20, 21 or
  22; this result is consistent with that belief and does not settle it.
- Nothing about Triangle(12) (A127500(12)) is claimed here.
- The solution came from a heuristic beam search (how-we-built-it/beam3.c). The search is not exhaustive and is not
  needed to check the claim; only the replay of the object by the simulators is.
- The three simulators were written in the same project from the same definition; they share no code, and they agree
  with every published solution used for calibration.

## Credits

- George I. Bell: the triangular-board problem as studied here, the bounds 19 <= S(11) <= 28, and the published
  solutions used for the original calibration (not shipped),
  https://www.gibell.net/pegsolitaire/LargeTriangular/index.html, https://www.gibell.net/pegsolitaire/tindex.html,
  and "Solving triangular peg solitaire", Journal of Integer Sequences 11 (2008), arXiv math/0703865.
- The OEIS Foundation and the authors of A127500, https://oeis.org/A127500.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
