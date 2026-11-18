# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 8456e23556911891ea6d3ccc7c3095bda2bd3d96b3f7ddd4bfd6fec8636f67ee
d = 6, n = 24, numbers: 288, fewest significant digits in a coordinate: 18
coherence mu = 0.3696053676390931559939761664514415115511
claimed      = 0.3696053676390931559939761664514415115511  difference 2.313e-41
attaining pair (0-based vectors) (6, 21)
leaderboard  = 0.36998252  leaderboard - mu = 3.771524e-04  (need >= 1e-8)
lower bound  = 0.36115756  mu - lower bound = 8.447808e-03  (need >= 0)
best pending = 0.36970275367722819048  pending - mu = 9.738604e-05  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/6x24_bmea.txt 6 24 0.3696053676390931559939761664514415115511 0.36998252 0.36115756 8456e23556911891ea6d3ccc7c3095bda2bd3d96b3f7ddd4bfd6fec8636f67ee 0.36970275367722819048
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/6x24.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (6x24.txt, 6x25.txt, kept from the original first run); writes out/6x24.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/6x24.txt), converted to float64 and written with 20 decimal places for packing-records.
