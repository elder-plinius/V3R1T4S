# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9
d = 7, n = 25, numbers: 350, fewest significant digits in a coordinate: 18
coherence mu = 0.3320683282539935095931558778760380236073
claimed      = 0.3320683282539935095931558778760380236073  difference 7.691e-42
attaining pair (0-based vectors) (13, 19)
leaderboard  = 0.33247138  leaderboard - mu = 4.030517e-04  (need >= 1e-8)
lower bound  = 0.32732684  mu - lower bound = 4.741488e-03  (need >= 0)
best pending = 0.33211991135920991668  pending - mu = 5.158311e-05  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x25_bmea.txt 7 25 0.3320683282539935095931558778760380236073 0.33247138 0.32732684 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9 0.33211991135920991668
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/7x25.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (7x25.txt, 7x26.txt, kept from the original first run); writes out/7x25.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/7x25.txt), converted to float64 and written with 20 decimal places for packing-records.
