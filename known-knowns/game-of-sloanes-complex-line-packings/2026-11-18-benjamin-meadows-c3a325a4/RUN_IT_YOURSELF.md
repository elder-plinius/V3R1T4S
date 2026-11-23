# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 c3a325a490a3c4a7ae4c26f80bfbe524b4f909dba875780b44f0591085da686e
d = 7, n = 30, numbers: 420, fewest significant digits in a coordinate: 17
coherence mu = 0.3452270454186593950746948641045502774133
claimed      = 0.3452270454186593950746948641045502774133  difference 1.269e-41
attaining pair (0-based vectors) (3, 15)
leaderboard  = 0.34639121  leaderboard - mu = 1.164165e-03  (need >= 1e-8)
lower bound  = 0.33660139  mu - lower bound = 8.625655e-03  (need >= 0)
best pending = 0.34596041604331477787  pending - mu = 7.333706e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x30_bmea.txt 7 30 0.3452270454186593950746948641045502774133 0.34639121 0.33660139 c3a325a490a3c4a7ae4c26f80bfbe524b4f909dba875780b44f0591085da686e 0.34596041604331477787
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/7x30.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (7x30.txt, 7x31.txt, kept from the original first run); writes out/7x30.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/7x30.txt), converted to float64 and written with 20 decimal places for packing-records.
