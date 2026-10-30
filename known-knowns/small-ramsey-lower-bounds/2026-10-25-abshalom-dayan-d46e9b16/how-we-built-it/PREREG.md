# PREREG (frozen 2026-10-25T06:25:30Z, from date -u at 06:25:09Z; before any split or search output exists)

Target: small-ramsey-lower-bounds, partial win p1.

## Criterion (verbatim, repo/bank/targets.json, p1)
"A multicolour classical Ramsey record: an explicit edge colouring of K_N with no monochromatic forbidden clique in each
colour (e.g. a 4-colouring of K_51 with no monochromatic triangle, giving R(3,3,3,3) >= 52), verified exhaustively, with
N+1 strictly above the best lower bound in DS1 and any newer arXiv paper for that multicolour cell."

## Statistic and checker
- The object: an explicit r-colouring of K_N (matrix or circulant file) for one cell R(k_1, ..., k_r).
- Validity: every edge has exactly one colour in 1..r; for each colour c, no clique of size k_c, decided on the
  expanded K_N by two independent exact methods that must agree: (A) exhaustive bitset branch and bound,
  (B) a SAT encoding ("is there a K_{k_c} in colour c?") that must be UNSAT. RUN/checker/mcheck.py implements both
  (tested: RUN/checker/checker_tests.out); a faster exact implementation may replace either method only if it gives the
  same verdicts as mcheck.py on the four test files and on at least one valid Kuznetsov source graph.
- Score: N. Threshold: N + 1 > B, where B is the cell's best lower bound, read live before claiming as the maximum of
  DS1 (latest revision) and any newer paper or repository found by a fresh search. Bars on 2026-10-25 (DS1 Apr 24, 2026,
  Table XIb): R(3,3,11) 174, R(3,3,12) 194, R(3,3,13) 217, R(3,3,14) 242, R(3,3,15) 269, R(3,3,16) 291, R(3,4,7) 152,
  R(3,4,8) 193, R(3,4,9) 242, R(3,5,5) 139, R(3,5,6) 181, R(3,5,7) 241. A tie (N + 1 = B) is not a win.
- Cells outside DS1 Table XIb and 6.1.h (e.g. R(3,4,10), R(3,5,8)) are not claimed in this run: their DS1 bar is only
  implicit in general constructions.
- Several winning cells: each is a separate claim (one cell per claim). Panel order: largest (N + 1 - B) / B first;
  cells that cannot be panelled before the deadline stay at PROMISING (single-context, unpanelled) in the run folder.

null_test: not needed because every claim is an explicit colouring checked by deterministic exact checkers against a
table value; there is no search statistic or "beats chance" claim.

## Negative results
"No circulant split exists" or "no cyclic colouring exists on Z_N" is reported only when the SAT search finished
(UNSAT, uncapped) for exactly the stated graph and family; capped runs are reported as undecided.
