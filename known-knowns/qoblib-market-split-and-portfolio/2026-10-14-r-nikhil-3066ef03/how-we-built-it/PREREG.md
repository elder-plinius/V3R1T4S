# PREREG: run 2026-10-14-1518, lane C (written before any attack output exists)

Written at: Wed Oct 14 15:21:37 UTC 2026 (from `date -u`, taken just before writing this file).

## Criterion (charter.md, verbatim, sub-aim (b))

> (b) class 06 portfolio optimisation (multi-period, transaction costs, short selling): a feasible solution strictly
> better than the listed best-known objective of an instance, in the objective sense the class defines.

## What will judge it

- The judge is `checker/pf_eval.py` (copied unchanged from run 2026-10-14-1428; exact rational arithmetic, written
  from the QOBLIB reference model `bqp_u3_c10.zpl` + `parameter_u3_c10.zpl`). It is not the search code. A candidate
  counts only if `pf_eval.py INSTANCE_DIR SOLUTION` prints `FEASIBLE` with exit 0 and its `objective = <int>` line is
  strictly below the bar. Any fast evaluator inside a search is only a guide.
- Objective sense: minimisation (the class minimises). Statistic: the exact integer objective.
- Thresholds (bars = best of the official table and every open QOBLIB PR, as fetched in this run at 15:20:01 UTC;
  table unchanged since run 2026-10-14-1428, PR #64 and #87 heads unchanged):
  - Lens quoter, cell `a200_t10_orig`, B = 50, lambda = 1e-2: bar −551385 (PR #87). Win: objective ≤ −551386.
  - Lens solver, the lambda = 0 cells of a200/a400 (budget 50 for a200, 100 for a400): bar per cell = column `best`
    of `../2026-10-14-1428/checker/bar_table.csv` (e.g. `a200_t10_orig` B = 50: −1360298). Win: objective ≤ bar − 1.
    An objective equal to the bar is a tie (an optimality certificate at most), never a record.
- One cell per claim. The live table and PR list are re-fetched once right before any claim (kit/LESSONS.md 8).

## Null design

null_test: not needed because every claim here is an explicit portfolio object checked by a deterministic exact
checker against a posted value; nothing is a search-for-signal or "beats chance" statistic.

## Not changed after results

If any threshold or cell changes after a result exists, it goes in a new timestamped `PREREG.v2.md` and the report
says so.
