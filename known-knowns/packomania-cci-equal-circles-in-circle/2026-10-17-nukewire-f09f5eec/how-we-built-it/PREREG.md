# PREREG — frozen 2026-10-17T09:47:10Z (before the panel scored anything; the object itself was
# found and first verified in run 2026-10-16-0945 under that run's frozen PREREG)

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

r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) computed at >= 50 significant digits
directly from the submitted coordinate strings (code/verify_N3307.py decimal-60; the standalone
claim checker uses the same two-pass scheme). Search phases may run double; only the exact value
of the saved coordinates counts.

## Thresholds

- Claim (p2, cell N = 3307): r* - r_table(3307) >= 1e-11 against the live-refetched row
  (0.016314899796158766989004378524 as fetched 2026-10-17T09:45:15Z), non-isometric to the
  posted cci3307.txt, queue and History rules satisfied.
- Lenses on rows 2611/2773/3901/5000: no claim unless >= 1e-11 over the live row.
- Sub-threshold margins, ties, double-only evidence: NOT a win.

## Null design

null_test: not needed because the claim is an explicit object (a coordinate file) checked by a
deterministic evaluator against a live table value; no statistical "beats chance" or
cipher-strength claim is made.

## Time box

Standard run; panel first (three fresh contexts), then lenses, each search capped (timeout 600 s);
nothing new started after 80% of the budget.
