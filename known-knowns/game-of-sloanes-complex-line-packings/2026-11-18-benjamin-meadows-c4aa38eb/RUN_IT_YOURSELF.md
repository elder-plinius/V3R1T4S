# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 c4aa38eb11e27923235073314ff87c88ac79524317ff5b9a7fee611869361a6e
d = 4, n = 29, numbers: 232, fewest significant digits in a coordinate: 17
coherence mu = 0.5773298205869567615435893703751987156369
claimed      = 0.5773298205869567615435893703751987156369  difference 1.819e-41
attaining pair (0-based vectors) (12, 17)
leaderboard  = 0.57733882  leaderboard - mu = 8.999413e-06  (need >= 1e-8)
lower bound  = 0.55136195  mu - lower bound = 2.596787e-02  (need >= 0)
best pending = 0.57733739938918767426  pending - mu = 7.578802e-06  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/4x29_bmea.txt 4 29 0.5773298205869567615435893703751987156369 0.57733882 0.55136195 c4aa38eb11e27923235073314ff87c88ac79524317ff5b9a7fee611869361a6e 0.57733739938918767426
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/4x29.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (4x29.txt, 4x30.txt, kept from the original first run); writes out/4x29.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/4x29.txt), converted to float64 and written with 20 decimal places for packing-records.
