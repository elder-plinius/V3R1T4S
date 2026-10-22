# PREREG — frozen 2026-10-16T09:48:33Z (checker-output time; before any attack output was scored)

target: packomania-cci-equal-circles-in-circle

## Criterion (verbatim from bank/targets.json)

Success means a file of N centers (x_i, y_i) for one N listed in
https://packomania.com/cci/txt/radius.txt such that the FEASIBLE radius
r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ), computed in mpmath at 50 digits directly
from the submitted coordinates (no tolerance), is STRICTLY GREATER (direction: max) than the
30-decimal radius for that N re-fetched live immediately before claiming, by at least 1e-11, AND
the configuration is not isometric to the posted cci<N>.txt one (sorted distance multisets
differ), AND N does not appear in a History-of-updates line on the live cci.html newer than the
one the scout fetched. QUEUE RULE (Packomania, checked 2026-10-08): the N must NOT lie inside any
range listed for this category on https://packomania.com/pending-requests.html re-fetched at
verification time; a value that is already in Packomania's queue does not count as ours. The
26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be
resolved; the verdict must state this caveat and the N must be re-checked against the live table
once that bundle disappears from the pending list. Packomania coordinate files are CENTERED.
No submission (email) is ever made; the claim is for the verified construction only.

## Statistic / exact checker

r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) computed by code/checker.py (mpmath,
mp.dps = 50) directly from candidate coordinates. Search phases run in double precision (numpy);
only the mpmath-50 value of the saved coordinates counts, recomputed after the search from the
coordinates alone.

## Thresholds

- Record claim: r* - r_table(N) >= 1e-11 for a live-refetched row N, non-isometric (sorted
  distance multiset differs at 50 digits), queue and History rules satisfied.
- Partial win p2: same numeric rule for a gap row N > 2600.
- Scope this run: the 135 gap rows N > 2600 in data/radius.txt and N = 2000.
- Sub-1e-11 margins, ties, or double-precision-only evidence: NOT a win.

## Null design

null_test: not needed because the claim is an explicit object (a coordinate file) checked by a
deterministic evaluator against a live table value; no statistical "beats chance" or
cipher-strength claim is made.

## Time box

Standard run: 3-4 lenses; searches capped (timeout 600 s each); nothing new started after 80% of
the budget.
