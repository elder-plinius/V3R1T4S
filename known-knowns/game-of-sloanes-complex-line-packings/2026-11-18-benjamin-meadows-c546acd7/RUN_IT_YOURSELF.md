# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 c546acd73014a01099f3b54379f86edd3ee81eb54a002df6398f0a8d4332fcb6
d = 7, n = 26, numbers: 364, fewest significant digits in a coordinate: 18
coherence mu = 0.3330718743753158294795952214297664426535
claimed      = 0.3330718743753158294795952214297664426535  difference 3.657e-42
attaining pair (0-based vectors) (15, 21)
leaderboard  = 0.33315439  leaderboard - mu = 8.251562e-05  (need >= 1e-8)
lower bound  = 0.32950179  mu - lower bound = 3.570084e-03  (need >= 0)
best pending = 0.33312151374622208506  pending - mu = 4.963937e-05  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x26_bmea.txt 7 26 0.3330718743753158294795952214297664426535 0.33315439 0.32950179 c546acd73014a01099f3b54379f86edd3ee81eb54a002df6398f0a8d4332fcb6 0.33312151374622208506
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/7x26.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (7x26.txt, 7x27.txt, kept from the original first run); writes out/7x26.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 240 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/7x26.txt), converted to float64 and written with 20 decimal places for packing-records.
