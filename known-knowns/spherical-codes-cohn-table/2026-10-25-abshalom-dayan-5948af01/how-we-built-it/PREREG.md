# PREREG (frozen 2026-10-24T22:59:33Z, from date -u, before this run's claim folder exists)

Honest note on timing: the (6, 575) polished object and its float64 c* come from run 2026-10-24-1639 (frozen there
in its own PREREG.md); this run's scout re-screened the 73-cell queue at 22:54Z (attempts/already-settled/
rescreen_scout.out) before this file. No other lens output of this run existed when it was written.

## Criterion (verbatim from bank/targets.json, as in target.md)

Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

Partial wins p1, p2, p3: verbatim in target.md (lines starting "- **p1**", "- **p2**", "- **p3**").

## Statistic and checkers

- c* = max over pairs i < j of <x_i, x_j> / (|x_i| |x_j|), computed from the saved coordinate file by
  checker/check_mp.py (mpmath, 50 significant digits) and checker/check_exact.py (exact rationals: decides
  c* < bar by comparing squared quantities with signs, no floating point). Both must print "beats" for a claim.
  Both were tested on a known negative (posted (6, 575) code against its own table value), a seeded flaw and a
  synthetic positive (checker/test_checkers.out).
- The bar for (d, N) is the 12-decimal cosine of the (d, N) row in the live /plain fetched at the claim moment
  (checker/fetch_live.sh claim<k>, as the very last step after the last text edit), with the HTML row checked for
  no '&ast;' and no "needs more optimization".

## Thresholds

- Claim (full criterion, one cell): c* <= bar - 1e-10 by both checkers; row unstarred, unlabelled, present in
  /plain at the claim-moment fetch; no arXiv result of the last 24 months for the same (d, N) at or below c* + 1e-10
  (arXiv API searches plus the per-instance data of every arXiv paper that covers the cell, read, not inferred);
  propagated bar min over listed d' <= d and N' >= N (live /plain, live index, and the three 2610.19988 tables)
  above c* by >= 1e-10; not (9 <= d <= 23 and c* <= 0.5). This run's claim cell is (6, 575). One cell per claim;
  a second cell, if time remains after this claim's gate, gets its own run folder, prereg and panel.
- Lens outputs for other cells are screens, not claims: a cell enters the ready queue only if float64 c* is below
  the table read the lens used by >= 1e-9 (a 10x float margin), the row is unstarred and unlabelled in that read,
  not in an open PR (data/lit/pulls_open_p*.json), not an ImprovEvolve cell, and below the propagated bar over
  d' <= d and N' >= N from the table and the three 2610.19988 tables (attempts/already-settled/code/rescreen.py).
- Author-level kill rule for sweeps: an uploader's rows are called converged for the SLP when 10 sampled rows
  whose first LP finished (iteration count above the cap test) give no gain >= 1e-9.
- p2 (prepared, not claimed in this run): >= 20 rows in one d that are labelled at this run's index fetch, each
  "beats" by both checkers with margin 1e-10 against that fetch.

null_test: not needed because every result here is an explicit coordinate file judged by two deterministic checkers against a table value (no search statistic, key, period or "beats chance" claim).

## Kill rules for lenses

A lens line dies when three seeds or three cells give no gain >= 1e-9 over the table, or when its structural
premise is shown false.
