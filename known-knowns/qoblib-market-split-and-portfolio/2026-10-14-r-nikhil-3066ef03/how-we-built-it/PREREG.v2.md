# PREREG v2: run 2026-10-14-1518, lane C

Written at: Wed Oct 14 15:27:16 UTC 2026 (from `date -u`).

Why a v2: after the quoter smoke test (PR #87's solution is a local optimum for single and pair block moves) and a
spectrum check (every period's risk matrix has rank 29 of 200; `attempts/lattice-smuggler/spectrum_output.txt`),
the second lens changes from "solver on the lambda = 0 cells" to the charter's lattice-smuggler lens on the SAME cell
as the quoter. Nothing about the criterion, the judge or the threshold changes:

- Cell: `po_a200_t10_orig`, B = 50, lambda = 1e-2. Bar −551385 (PR #87). Win: `checker/pf_eval.py` prints FEASIBLE,
  exit 0, objective ≤ −551386.
- The lambda = 0 solver line from PREREG.md is not run in this run (deferred, listed as a next-run angle); its
  thresholds in PREREG.md stay as written if it is ever run.
- null_test: not needed because every claim here is an explicit portfolio object checked by a deterministic exact
  checker against a posted value.
