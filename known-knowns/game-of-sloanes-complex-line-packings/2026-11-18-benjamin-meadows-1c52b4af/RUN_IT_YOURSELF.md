# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 1c52b4afe1001f0b48df54d0650a323ac00bafbeb3d9643cf175895950d61c88
d = 3, n = 24, numbers: 144, fewest significant digits in a coordinate: 18
coherence mu = 0.7190647707373806963227094589931320020145
claimed      = 0.7190647707373806963227094589931320020145  difference 1.372e-41
attaining pair (0-based vectors) (0, 10)
leaderboard  = 0.71909565  leaderboard - mu = 3.087926e-05  (need >= 1e-8)
lower bound  = 0.65465367  mu - lower bound = 6.441110e-02  (need >= 0)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/3x24_bmea.txt 3 24 0.7190647707373806963227094589931320020145 0.71909565 0.65465367 1c52b4afe1001f0b48df54d0650a323ac00bafbeb3d9643cf175895950d61c88
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/3x24.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (3x24.txt, 3x25.txt, kept from the original first run); writes out/3x24.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/3x24.txt), converted to float64 and written with 20 decimal places for packing-records.
