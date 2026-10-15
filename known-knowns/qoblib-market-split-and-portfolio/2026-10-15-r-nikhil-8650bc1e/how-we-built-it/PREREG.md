# PREREG: run 2026-10-15-0312, lane C

Written at: Thu Oct 15 03:17:11 UTC 2026 (from `date -u`), before any attack job of this run was started.

- Criterion (charter, verbatim): "a feasible solution strictly better than the best known objective of an instance
  in class 06 (portfolio optimisation: multi-period, transaction costs, short selling) of the Quantum Optimization
  Benchmarking Library, in the objective sense the class defines, where the bar is the better of the library's
  best-known table and any value posted in an open pull request to the library (#44, #64 and #87 when this was
  written)." Applied with the operator's wider bar: best value posted anywhere public.
- Cell: `po_a200_t10_s00`, B = 50, lambda = 1e-2. Bar −401535 (PR #87; no table row; PR #64 −192428; no third-party
  value found at 03:13–03:15 UTC).
- Claim object: ONE portfolio, the best `checker/pf_eval.py`-verified portfolio for this cell at the freeze time
  (planned 04:35 UTC, recorded with the object's sha256 in `claim/CLAIM.md`). Candidates: the lead from run
  2026-10-14-1518 (−618978) and anything the extender lens produces before the freeze.
- Statistic and threshold: `checker/pf_eval.py` (exact rationals, written from the ZIMPL model) prints FEASIBLE,
  exits 0, and reports objective ≤ −401536; `checker/zimpl_literal_eval.py` (literal binary-variable evaluation)
  reports the same integer.
- The bar is re-read (table + open PR list, one plain request each) right before the claim is built and in the gate
  if the panel's fetch is more than 6 hours old.
- Other cells searched in this run are live leads only: no claim on them in this run.
- null_test: not needed because the claim is an explicit portfolio object checked by a deterministic exact checker
  against a posted value.
