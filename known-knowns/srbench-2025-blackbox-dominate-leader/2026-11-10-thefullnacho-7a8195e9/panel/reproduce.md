# REPRODUCE skeptic verdict

context: subagent

## Definition quoted (success criterion, from claim.md)

> For a named dataset D among the 12 SRBench 2025 black-box datasets: a
> symbolic regression procedure run on each of the 30 splits used in
> results.feather (train_test_split with train_size 0.75 and random_state
> equal to each listed seed, as in experiment/evaluate_model.py on the
> srbench_2025 branch, including its training subsampling rule) that returns
> one closed-form expression per split, such that (a) the median test R^2
> over the 30 splits is STRICTLY GREATER (direction: max) than the highest
> median r2_test of any algorithm for D in
> https://github.com/cavalab/srbench/tree/srbench_2025/results/black-box-tuning
> (results.feather, re-fetched live immediately before claiming), and (b) the
> median complexity of the 30 expressions, computed with SRBench's own
> symbolic_utils.complexity, is less than or equal to that leading
> algorithm's median model_size. The procedure must be fixed before scoring
> (no per-split hand edits).
>
> Bar (from the live table, see table_record.txt): median test R^2 > 0.3800
> (PS-Tree, highest median r2_test for 1028_SWD) and median complexity <= 3270
> (PS-Tree's median model_size).

## Method

I wrote my own checker from that definition before reading the author's
checker (check_srbench.py was not opened). The checker, run with the
provided venv python, independently:

- hashes data/1028_SWD.tsv.gz and compares to the recorded sha256;
- loads the dataset (1000 rows, 10 features In1..In10, target in {2,3,4,5});
- checks the 30 seeds in expressions.json against the `random_state`
  values for 1028_SWD in data/results.feather;
- recomputes the bar from data/results.feather (leader = highest median
  r2_test; median model_size excluding -1 rows);
- parses each expression with sympy over x_1..x_10, evaluates it on its
  seed's test split (sklearn train_test_split, train_size=0.75,
  test_size=0.25, random_state=seed over the 1000 row indices), computes
  R^2 = 1 - SS_res/SS_tot on the raw test target, and computes complexity
  with SRBench's own symbolic_utils.complexity from data/symbolic_utils.py.

The checker was run three times end to end; all runs gave identical
medians (deterministic).

## Results

- Dataset sha256: matches recorded
  b0526495039ad62169c52a9cf34a957f16b1d02cab995746d3098bbdbfa951cc. No NaN;
  feature range [1.0, 4.0]; target values {2,3,4,5}.
- 30 expressions, 30 distinct seeds, exactly the 30 `random_state` values
  for 1028_SWD in data/results.feather.
- Bar recomputed from data/results.feather: leader PS-Tree, median r2_test
  0.380003, median model_size 3270 (n=30) — matches table_record.txt.
- All 30 expressions parse, use only x_1..x_10, and produce finite
  predictions on all 250 test rows of their split.
- Per-split recomputed test R^2 vs recorded: worst deviation 8.62e-05
  (consistent with the 4-decimal coefficient rounding in the saved strings).
  Per-split complexity: exact match on all 30 (worst deviation 0).
- Median test R^2 recomputed = 0.391051 (rounds to 0.3911). Claim states
  0.3910; difference 0.000051, within the 0.001 tolerance. Strictly greater
  than the 0.3800 bar.
- Median complexity recomputed = 75.5, exactly the claimed value, and
  <= 3270 bar.

108 individual checks, 0 failures.

## Caveats (not blocking)

- The claim's 0.3910 vs recomputed 0.3911 difference is explained by the
  saved strings being rounded to 4 decimals after the author's scoring;
  per-split deviations are all < 1e-4, so this is rounding, not a scoring
  discrepancy.
- This verdict verifies the scored expressions against the saved dataset
  and table only. It does not re-run the author's procedure (teacher/student
  fit) and does not verify the "fixed procedure, no per-split hand edits"
  condition from the run itself; that is a provenance question outside the
  saved claim folder.
- I did not re-fetch results.feather or the dataset live; the bar and
  dataset were verified against the saved copies and their recorded hashes.

pass: true
