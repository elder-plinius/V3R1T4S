# PREREG (frozen 2026-11-02T17:34:07Z per date -u, before any attack program for this run has been written or run)

Target: triangular-peg-solitaire-shortest-11-12. Cells: Triangle(11) (primary), Triangle(12) (secondary). One cell per claim.

Criterion (bank, verbatim): A legal solution on Triangle(11) in at most 27 moves, or on Triangle(12) in at most 28 moves, starting from a single vacancy and ending with a single peg, verified by a simulator; or an exact value of a(11) or a(12) with a re-runnable exhaustive certificate. The result must be strictly better than the bounds in the live OEIS A127500 entry and Bell's triangular page at claim time.

Checker / statistic: checker/pegcheck.py (written from the A127500 definition, tested on Bell's T9/T10/T11/T12
solutions and two corrupted ones, checker/fixtures_out.txt). It simulates every jump on the full board minus the
first landing hole, counts moves as maximal runs of consecutive jumps by the same peg, and requires one final peg
after T(n)-2 jumps. A second, independently written simulator (different language/representation) must agree on
legality and move count before any claim.
Thresholds: claim T11 only if moves <= 27 (strictly below 28); T12 only if moves <= 28 (strictly below 29); the live
OEIS entry and Bell's large-triangular page, re-fetched right before claiming, must still show 28 / 29 or worse.
No lower-bound claim will be made from any capped or heuristic search.

null_test: not needed because the claim is an explicit object (a move list) checked by a deterministic simulator against a published table bound, not a search score or a "beats chance" statistic.
