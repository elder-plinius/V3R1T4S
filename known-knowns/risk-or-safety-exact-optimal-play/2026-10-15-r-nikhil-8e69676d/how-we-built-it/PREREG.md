# PREREG.md (frozen before any attack output is scored)

frozen_at: Thu Oct 15 03:25:44 UTC 2026
target: risk-or-safety-exact-optimal-play
run: runs/2026-10-15-0312

## Criterion (verbatim from the bank entry)

Exact reduced rationals A387261(n)/A387262(n) - the starting player's win probability from (0 open, 0 banked, 0 banked) under optimal play by both players - for EVERY n from 16 through 30 (direction: new terms), each with a certificate: the claimed value P(a, b, c) for every position (a open and b banked points of the player to move, c banked by the opponent) and the claimed action, satisfying exactly P(a, b, c) = max(continue, stop) for a >= 1 and the forced toss for a = 0, where continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c) and stop = 1 - P(0, c, a + b), with P = 1 when a + b >= n (equations of Sections 3-4 of arXiv:2603.01002), all checked in exact arithmetic. The same code must reproduce the published terms for n <= 15 (or certify a correction, see p1).

Partial wins (verbatim): p1: A certified correction: an exact Bellman certificate showing that a published value (A387261/A387262, n <= 15) or a published optimal action (paper Table 1 / A394776, n <= 20) is not optimal. p2: Certified exact terms for n = 16..20 only (the range where the paper gives strategies but no exact probabilities).

## Statistic / checker that will judge it

code/ros_cert_check.py (sha256 f4ea640f567f9c790038c5a04c5a3e293c7fc906ae2bcc6ec482bb1121c3cbf9; tested on one positive and
five negative cases, checker_tests/test_output.log), written from the bank definition before any solver ran. It is run
as `python3 -I code/ros_cert_check.py --oeis data cert/n<k>.json` on every certificate n = 1..30 produced by the
extender lens. Decisive output: "PASS"/"FAIL" per certificate (every position's Bellman equation holds exactly in
rational arithmetic, every position listed exactly once, the claimed action attains the max, forced toss at a = 0),
"oeis_match=yes" for n = 1..15 (P(0,0,0) equals the b-file term exactly), and the final line "ALL_PASS".

## Thresholds (decision rule, fixed now)

- solution_claim iff (a) all 30 certificates n = 1..30 print PASS; (b) all 15 published terms match exactly
  (oeis_match=yes for every n = 1..15); (c) a second, independently written solver (contrarian lens, different
  formulation) returns the same 30 values of P(0,0,0); (d) the step-5 self-break (checker re-run on the saved
  certificates plus an audit of the lens code against the definition) finds no flaw.
- partial_win_claim p2 iff (a)-(d) hold for n = 1..20 but not for all of 21..30.
- partial_win_claim p1 iff a certificate that passes the checker shows a published term (n <= 15) or a published
  optimal toss count (Table 1 / A394776, i, j <= 20) to be non-optimal, confirmed by both solvers, with the index
  encoding re-derived and exact ties excluded (a tie is not a correction).
- otherwise: progress or negative. A certificate that fails at any position is a failure for that n; no rounding, no
  tolerance, no partial credit per position.

## Null design

null_test: not needed because the result is an explicit object (a value-and-action table over every position of the
game) checked by a deterministic exact-rational checker against the Bellman equations and against the published
OEIS terms; no search statistic, key, period, language or "beats chance" claim is involved.

## Informational comparisons (not part of the decision rule)

The cross-model worker's candidate values recorded in the dossier are compared with the lenses' values afterwards
and reported as data; agreement or disagreement there changes nothing above.
