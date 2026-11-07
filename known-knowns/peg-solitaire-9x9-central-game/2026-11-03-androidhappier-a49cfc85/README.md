# peg-solitaire-9x9-central-game: a 31-move central-game solution on the 9x9 (81-hole) square board

Family: graphs-games-automata · target peg-solitaire-9x9-central-game

## What

object/sol31.txt is a legal 9x9 (81-hole) square-board central-game solution from e5 vacancy to a single peg at e5 using orthogonal jumps only, of 79 jumps and 31 moves (maximal same-peg runs), independently replayed, which is shorter than the 34-move Maye solution listed as best on Bell's main index page as fetched at 2026-11-03T14:09:43Z.

(In this package that file is `object/sol31.txt`, sha256 `a49cfc85ce7d20bd828fd9f168fd3beea6d4bfb0fbe90df350944a85bd60093a`.)

The board is the full 9x9 square of 81 holes (columns a..i, rows 1..9), not the 33-hole English cross. Start: every
hole filled except the centre e5. A jump moves a peg two holes orthogonally over an adjacent peg into an empty hole
and removes the jumped peg. A move is a maximal run of consecutive jumps by the same peg. Finish: one peg, at e5.
The file has one move per line, holes joined by `-`.

## Check it yourself

From this folder, in a fresh shell (needs python3; a C compiler is optional):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (a few seconds on a laptop). It checks the object's sha256, replays every jump with a
standard-library Python checker written from the definition (expects `VALID central game e5->e5 in 31 moves`,
79 jumps), rejects five illegal or unfinished fixtures, accepts a 34-move calibration solution as VALID 34, and, if
a C compiler is found, builds and runs an independently written C replay checker (expects `PASS`, 31 moves).
See RUN_IT_YOURSELF.md and verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | table value | this package | URL | fetched (UTC) |
|---|---|---|---|---|---|
| George I. Bell, Peg Solitaire (main index, section "The 9x9 Board (81 holes)") | 9x9 central game e5 -> e5, shortest known solution in moves | 34 moves (Alain Maye, 2004, by hand; listed as best, question open) | 31 moves (79 jumps) | https://www.gibell.net/pegsolitaire/ | 2026-11-03T14:09:43Z (HTTP 200) |

The dedicated 9x9 page (https://www.gibell.net/pegsolitaire/9x9/9x9index.html, re-fetched 2026-11-03T14:11:36Z,
HTTP 200, last modified November 14th, 2015) also names Maye's 34 moves as the best seen and gives a lower bound
of 24. Fetch records and hashes: the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Optimality: 31 is an upper bound only; nothing is claimed about the minimum number of moves.
- Any lower bound (Bell's published lower bound is 24; this package does not change it).
- Anything about the 33-hole English cross board or any other board; this is the 81-hole 9x9 square board only.
- Partial wins (e.g. a final sweep, loop or bound variants) and any other cell; one cell only.
- Anything about the search method beyond the record in how-we-built-it/ (re-running it is optional).

## Credits

- GitHub [CharanRayudu](https://github.com/CharanRayudu): this run, search, checkers and package.
- George I. Bell: [Peg Solitaire pages](https://www.gibell.net/pegsolitaire/) and the
  [9x9 board page](https://www.gibell.net/pegsolitaire/9x9/9x9index.html), the status source, board notation and
  the open central-game question.
- Alain Maye: the previous best, a 34-move solution found by hand in 2004, as published on
  [Bell's 9x9 page](https://www.gibell.net/pegsolitaire/9x9/9x9index.html).
