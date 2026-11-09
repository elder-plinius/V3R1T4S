# PREREG (frozen 2026-11-03T13:28:07Z, from date -u)

target: peg-solitaire-9x9-central-game

## Criterion (verbatim from bank)
A legal central-game solution on the 9x9 board (centre vacancy to one peg in the centre, orthogonal jumps only) using at most 33 moves, where a move is a maximal run of consecutive jumps by the same peg, verified by a simulator that replays every jump and counts moves. It must be strictly shorter than the best solution on Bell's page at claim time (34 moves as of 2026-10-30).

## Statistic / checker
- checker/check9.py (written from the definition, this run) replays every jump from the start position (all 81 holes
  filled except e5), rejects any non-orthogonal, off-board, no-peg, no-jumped-peg or occupied-landing jump, counts
  moves as maximal runs of consecutive jumps by the same peg (a jump starting where the previous one landed continues
  the move), and requires the final position to be exactly one peg at e5.
- A second, independently written checker (C, attempts/self-break/) must agree on legality, jump count (79) and move count.
- Threshold: moves <= 33 AND moves strictly less than the best value on Bell's page re-fetched at claim time
  (34 at scout, data/bell_index.html).
- Fixtures: three negatives in checker/ (diagonal jump, jump over empty hole, unfinished game) must be rejected; a
  34-move beam solution (attempts/exact-eval-first/code/sol34.txt) is the positive calibration (ties Maye, not a win).

null_test: not needed because the claim is an explicit move sequence checked by a deterministic replay checker against a table value (34); no statistical or search-significance claim is made.

## Partial wins
p1 / p2 are not targeted for packaging this run (instruction: package ONLY a full CONFIRMED_SOLUTION).
