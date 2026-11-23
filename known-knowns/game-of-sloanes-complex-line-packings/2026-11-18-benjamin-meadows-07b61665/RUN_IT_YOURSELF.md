# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 07b61665a7df72affdb89b3bc1770541c6ad1e57b0fd95aadb476f8cf215bbfd
d = 3, n = 41, numbers: 246, fewest significant digits in a coordinate: 21
coherence mu = 0.7784778326431421360698299495495172055667
claimed      = 0.7784778326431421360698299495495172055667  difference 2.876e-41
attaining pair (0-based vectors) (22, 29)
leaderboard  = 0.77848806  leaderboard - mu = 1.022736e-05  (need >= 1e-8)
lower bound  = 0.68765248  mu - lower bound = 9.082535e-02  (need >= 0)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/3x41_bmea.txt 3 41 0.7784778326431421360698299495495172055667 0.77848806 0.68765248 07b61665a7df72affdb89b3bc1770541c6ad1e57b0fd95aadb476f8cf215bbfd
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/3x41.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (3x41.txt, 3x42.txt, kept from the original first run); writes out/3x41.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 626 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/3x41.txt), unrounded.
