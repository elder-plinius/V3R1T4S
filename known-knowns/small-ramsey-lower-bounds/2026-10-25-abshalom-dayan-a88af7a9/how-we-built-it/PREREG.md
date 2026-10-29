# PREREG (frozen 2026-10-25T07:32:47Z, from date -u; before any output of this run's lenses exists)

Target: small-ramsey-lower-bounds, partial win p1. Weekend run 5 (runs/2026-10-25-0719).

## Criterion (verbatim, repo/bank/targets.json, p1)
"A multicolour classical Ramsey record: an explicit edge colouring of K_N with no monochromatic forbidden clique in each
colour (e.g. a 4-colouring of K_51 with no monochromatic triangle, giving R(3,3,3,3) >= 52), verified exhaustively, with
N+1 strictly above the best lower bound in DS1 and any newer arXiv paper for that multicolour cell."

## Statistic and checker (same rule as runs/2026-10-25-0610/PREREG.md, frozen 06:25:30Z, extended to more cells)
- The object: an explicit 3-colouring of K_N (circulant file or matrix) for one cell R(3,k,m) of DS1 Table XIb.
- Validity: every edge has exactly one colour; for each colour c, no clique of size k_c, decided on the expanded K_N by
  two independent exact methods that must agree: (A) exhaustive bitset branch and bound, (B) a SAT encoding that must be
  UNSAT. Tools: runs/2026-10-25-0610/attempts/constructor/code/check_fast.py (alpha.c B&B + CaDiCaL), which gave the
  same verdicts as runs/2026-10-25-0610/checker/mcheck.py on the four checker tests and on two Kuznetsov source graphs
  (runs/2026-10-25-0610/mainchk/source_agree.out), plus runs/2026-10-25-0610/checker/verify_circ.py (stdlib) as a
  third opinion for circulant objects.
- Score: N. Threshold: N + 1 > B, where B is the cell's best lower bound read live before claiming, as the maximum of
  DS1 (latest revision) and any newer paper or repository found by a fresh search. Bars on 2026-10-25 (DS1 Apr 24, 2026,
  Table XIb): R(3,3,m) for m = 4..16: 30 45 61 85 103 129 150 174 194 217 242 269 291; R(3,4,m) for m = 4..9:
  55 89 117 152 193 242; R(3,5,m) for m = 4..7: 89 139 181 241. A tie (N + 1 = B) is not a win.
- Cells outside DS1 Table XIb (e.g. R(3,4,10), R(3,5,8)) and four-colour cells are not claimed in this run.
- One cell per claim. For a cell already claimed by run 4 (R(3,3,11), R(3,3,12), R(3,3,14), R(3,4,7), R(3,5,6),
  R(3,5,7)), a new object counts only if its N is strictly larger than run 4's; the larger object replaces run 4's
  for that cell before its panel.
- Panel order: largest (N + 1 - B) / B first; cells not panelled before the deadline stay PROMISING
  (single-context, unpanelled) in their run folder.

null_test: not needed because every claim is an explicit colouring checked by deterministic exact checkers against a
table value; there is no search statistic or "beats chance" claim.

## Negative results
"No circulant split exists" is reported only when the SAT search finished UNSAT, uncapped, for exactly the stated
source graph, colour and split type; capped runs are reported as undecided.
