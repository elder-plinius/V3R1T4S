# drevalpy's own generated evaluation output

The success criterion lists "the generated report directory" among its deliverables. drevalpy's report is a
multi-megabyte HTML tree of Plotly plots, which `kit/SUBMIT.md` forbids copying into a submission (no
third-party pages; files at most 1 MB). What is shipped instead is the **substantive content** of that
report: the evaluation table drevalpy's own `parse_results` -> `prep_results` pipeline writes, from which
every plot in the report is drawn.

| file | what it is |
|---|---|
| `seed42_evaluation_results.csv` | drevalpy's own per-split metrics for PotencyTransfer and the reference baseline on the official splits, including the `R^2: normalized` column that defines the claim |
| `independent_evaluation_results.csv` | the same for the independent split generation |
| `*_summary.json` | the per-algorithm means, SDs, SEs and per-split values read off those tables |

Regenerate the full HTML report with drevalpy's own entry point after reproducing a run
(`../../RUN_IT_YOURSELF.md` Level 2):

```sh
"$ENV/bin/drevalpy-report" --run_id RUN_ID --dataset CTRPv2 --path_data "$DATA" --result_path "$RESULTS"
```

The claim's numbers are the `R^2: normalized` values in these tables; `verify-it-yourself/check_claim.py`
recomputes them from the raw predictions in `object/` without needing drevalpy at all.
