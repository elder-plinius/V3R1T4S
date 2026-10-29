# PREREG: spherical-codes-cohn-table, run 2026-10-24-1639

frozen: 2026-10-24T16:47:45Z (date -u), before any attack output was scored.

## Criterion (verbatim, bank/targets.json)

Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

## Statistic and checker

- c* = max over pairs of the normalised inner product, computed from the saved coordinate file (>= 20 significant
  digits per coordinate) by checker/check_mp.py (mpmath, 50 digits) and independently by checker/check_exact.py
  (exact Fractions, squared comparison against the bar). Both must say "beats".
- Bar: c_table - 1e-10, with c_table the 12-decimal /plain cosine re-fetched live (one honest request) right before
  claiming. Until that fetch succeeds the comparison uses the 2026-10-24T16:28:44Z snapshot and any candidate stays
  PENDING TABLE CHECK.
- Eligibility, literally: row present in live /plain; live index row has no &ast; and no "needs more optimization";
  not (9 <= d <= 23 and c* <= 0.5); no newer arXiv result for the cell; not claimed in this repo's open PRs,
  TROPHY_CASE.md, known-knowns/, or sibling workspaces' runs/ and outbox/.
- One cell per claim. A tie (gain < 1e-10) is not a record. Float search results count for nothing until both
  checkers pass on the saved file.

## Thresholds

- gain = c_table - c* >= 1e-10 in both checkers (check_exact.py tests the exact bar c_table - 1e-10).

## Null design

null_test: not needed because each claim is an explicit object (a coordinate file) checked by two deterministic checkers against a fixed table value; no search statistic or "beats chance" claim is made.

## Plan of lenses (may grow; any change of rule goes in a new PREREG.v2.md)

optimizer (from-scratch multi-start + exact active-set polish on small d >= 24 cells; warm start impossible while
the site is unreachable), object-as-data (cross-cell scan, contact structure), constructor (structured seeds:
orbits, embeddings of structured codes), already-settled (skeptic lens on any candidate), and others as budget allows.
