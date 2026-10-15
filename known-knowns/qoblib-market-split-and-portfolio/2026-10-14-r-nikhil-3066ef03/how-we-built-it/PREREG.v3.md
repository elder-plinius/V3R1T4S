# PREREG v3: run 2026-10-14-1518, lane C

Written at: Wed Oct 14 15:37:14 UTC 2026 (from `date -u`).

Why a v3: the operator raised this run's budget from light to heavy (about 480 active minutes in total) during the
run ("go deeper ... keep the current target, pour effort into the most promising live line, add lenses if useful,
and keep the kit's verification standards"). Results seen before this file: the quoter and lattice-smuggler lenses
already produced feasible portfolios below the bar on the cell (best so far −585086 in book b4, fast-model value).

What changes: more lenses and more compute on the SAME cell, and one frozen object for the panel, chosen as the best
`pf_eval.py`-verified portfolio at the freeze time (the freeze time and the object's sha256 are written in
`claim/CLAIM.md` when it is built). What does not change: the cell, the judge and the threshold.

- Cell: `po_a200_t10_orig`, B = 50, lambda = 1e-2. Bar −551385 (PR #87; the official table has no row; the bar
  is the better of the table and every open QOBLIB PR, as the operator confirmed this run). Win: `checker/pf_eval.py`
  prints FEASIBLE, exit 0, objective ≤ −551386, and `checker/zimpl_literal_eval.py` (step-5 self-check, a literal
  binary-variable evaluation of the ZIMPL model) agrees on the same integer.
- The bar is re-read (table + open PR list, one plain request each) right before the claim is built and again in the
  gate if the panel's fetch is over 6 hours old.
- Other cells (other instances or lambdas) may be searched with the same pipeline in this run, but only as live
  leads for later runs: no claim on them in this run (one cell per claim; one claim folder per run).
- null_test: not needed because every claim here is an explicit portfolio object checked by a deterministic exact
  checker against a posted value.
