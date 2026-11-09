# PREREG.md (frozen before any attack output is scored)

frozen_at: Wed Oct 28 00:38:30 UTC 2026
target: risk-or-safety-exact-optimal-play
run: runs/2026-10-27-1710

## Criterion (verbatim from the bank entry)

Exact reduced rationals A387261(n)/A387262(n) - the starting player's win probability from (0 open, 0 banked, 0 banked) under optimal play by both players - for EVERY n from 31 through 45 (direction: new terms), each with a certificate: the claimed value P(a, b, c) for every position (a open and b banked points of the player to move, c banked by the opponent) and the claimed action, satisfying exactly P(a, b, c) = max(continue, stop) for a >= 1 and the forced toss for a = 0, where continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c) and stop = 1 - P(0, c, a + b), with P = 1 when a + b >= n (equations of Sections 3-4 of arXiv:2603.01002), all checked in exact arithmetic. The same code must reproduce the published terms (n <= 15) and the terms in known-knowns/risk-or-safety-exact-optimal-play/ (n = 16..30), or certify a correction (see p1). Check the OEIS entries, b-files, edit histories and the repository's known-knowns before claiming; terms already established there do not count as new terms.

Partial wins (verbatim):
- **p1:** A certified correction: an exact Bellman certificate showing that a published value (A387261/A387262 for n <= 15, or the repository's terms for n = 16..30) or a published optimal action (paper Table 1 / A394776, n <= 20) is not optimal.
- **p2:** Certified exact terms for every n = 31..35 with complete independently checked Bellman value/action tables, after calibration on the published and repository terms through n = 30.

## Statistic / checker that will judge it

`verify-it-yourself/ros_cert_check.py` and `verify-it-yourself/my_verify.py` tested on positive and negative cases. Run as `python3 -I verify-it-yourself/ros_cert_check.py` and `python3 -I verify-it-yourself/my_verify.py --oeis data` on all certificates n = 31..45 and calibration n = 1..30. Decisive output: "PASS" / "FAIL" per certificate (every position's Bellman equation holds exactly in rational arithmetic, every position listed exactly once, the claimed action attains the max, forced toss at a = 0), "oeis_match=yes" for n = 1..15, known-knowns match for n = 16..30, and the final line "ALL_PASS".

## Thresholds (decision rule, fixed now)

- solution_claim iff (a) all 15 certificates n = 31..45 print PASS; (b) all 15 published OEIS terms n = 1..15 and all 15 repository terms n = 16..30 match exactly; (c) a second, independently written solver (contrarian lens, pure-turn-plan exact minimax) produces identical values and action plan sets; (d) the step-5 self-break finds no flaw; (e) independent integer cross-multiplication verifier confirms all certificates and coprime reduction.
- partial_win_claim p2 iff (a)-(e) hold for every n = 31..35.
- partial_win_claim p1 iff a certificate that passes the checker shows a published term (n <= 15) or a repository term (n = 16..30) to be non-optimal, confirmed by both solvers with exact ties excluded.
- otherwise: progress or negative. A certificate that fails at any position is a failure for that n; no rounding, no tolerance, no partial credit per position.

## Null design

null_test: not needed because the result is an explicit object (a value-and-action table over every position of the game) checked by a deterministic exact-rational checker against the Bellman equations and against the published OEIS terms; no search statistic, key, period, language or "beats chance" claim is involved.
