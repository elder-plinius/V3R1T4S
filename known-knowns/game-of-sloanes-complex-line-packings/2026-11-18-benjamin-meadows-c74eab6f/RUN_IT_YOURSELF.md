# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 c74eab6fe1a84859d0f3ff0027bddbc084891b8fe4a6c5689e3065e9017a169e
d = 6, n = 38, numbers: 456, fewest significant digits in a coordinate: 17
coherence mu = 0.4167504373839113168478658238006318809803
claimed      = 0.4167504373839113168478658238006318809803  difference 4.482e-41
attaining pair (0-based vectors) (11, 12)
leaderboard  = 0.41682055  leaderboard - mu = 7.011262e-05  (need >= 1e-8)
lower bound  = 0.40824829  mu - lower bound = 8.502147e-03  (need >= 0)
best pending = 0.41680962925949597288  pending - mu = 5.919188e-05  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/6x38_bmea.txt 6 38 0.4167504373839113168478658238006318809803 0.41682055 0.40824829 c74eab6fe1a84859d0f3ff0027bddbc084891b8fe4a6c5689e3065e9017a169e 0.41680962925949597288
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/6x38.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (6x38.txt, 6x39.txt, kept from the original first run); writes out/6x38.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/6x38.txt), converted to float64 and written with 20 decimal places for packing-records.
