# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 d5a09fe3e86bd33f50a94280aa07b4da5c260a9c2591b61ca0427d630289b268
d = 7, n = 23, numbers: 322, fewest significant digits in a coordinate: 17
coherence mu = 0.3253417037456465537231361928662624148246
claimed      = 0.3253417037456465537231361928662624148246  difference 1.372e-41
attaining pair (0-based vectors) (7, 13)
leaderboard  = 0.32539307  leaderboard - mu = 5.136625e-05  (need >= 1e-8)
lower bound  = 0.32232919  mu - lower bound = 3.012514e-03  (need >= 0)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x23_bmea.txt 7 23 0.3253417037456465537231361928662624148246 0.32539307 0.32232919 d5a09fe3e86bd33f50a94280aa07b4da5c260a9c2591b61ca0427d630289b268
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/7x23.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (7x23.txt, 7x24.txt, kept from the original first run); writes out/7x23.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 290 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/7x23.txt), converted to float64 and written with 20 decimal places for packing-records.
