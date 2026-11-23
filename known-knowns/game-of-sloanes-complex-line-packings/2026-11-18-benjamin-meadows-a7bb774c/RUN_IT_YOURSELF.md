# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 a7bb774c95dff1a9b33b464e8d898037621da74deaff699814f20fe77b350902
d = 3, n = 46, numbers: 276, fewest significant digits in a coordinate: 18
coherence mu = 0.7942836704171085550436983788218595937488
claimed      = 0.7942836704171085550436983788218595937488  difference 2.654e-41
attaining pair (0-based vectors) (12, 26)
leaderboard  = 0.79435710  leaderboard - mu = 7.342958e-05  (need >= 1e-8)
lower bound  = 0.70511609  mu - lower bound = 8.916758e-02  (need >= 0)
best pending = 0.79431158972980451695  pending - mu = 2.791931e-05  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/3x46_bmea.txt 3 46 0.7942836704171085550436983788218595937488 0.79435710 0.70511609 a7bb774c95dff1a9b33b464e8d898037621da74deaff699814f20fe77b350902 0.79431158972980451695
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/3x46.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (3x46.txt, 3x47.txt, kept from the original first run); writes out/3x46.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/3x46.txt), converted to float64 and written with 20 decimal places for packing-records.
