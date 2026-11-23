# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 386918bcc87c79220d9738c9244850bae315e9f8f5b1bcc547f274870bbc9642
d = 5, n = 38, numbers: 380, fewest significant digits in a coordinate: 17
coherence mu = 0.4999809988399788999929898458823814612691
claimed      = 0.4999809988399788999929898458823814612691  difference 3.005e-41
attaining pair (0-based vectors) (2, 7)
leaderboard  = 0.49998890  leaderboard - mu = 7.901160e-06  (need >= 1e-8)
lower bound  = 0.48199920  mu - lower bound = 1.798180e-02  (need >= 0)
best pending = 0.49998579061709488759  pending - mu = 4.791777e-06  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/5x38_bmea.txt 5 38 0.4999809988399788999929898458823814612691 0.49998890 0.48199920 386918bcc87c79220d9738c9244850bae315e9f8f5b1bcc547f274870bbc9642 0.49998579061709488759
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/5x38.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (5x38.txt, 5x39.txt, kept from the original first run); writes out/5x38.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 1000 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/5x38.txt), converted to float64 and written with 20 decimal places for packing-records.
