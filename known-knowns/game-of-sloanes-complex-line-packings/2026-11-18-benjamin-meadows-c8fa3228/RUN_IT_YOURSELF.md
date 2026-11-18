# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 c8fa32286e01682d603e52dd8146c7f8ed6b01be7f3e1a171344c74a643ff8eb
d = 6, n = 47, numbers: 564, fewest significant digits in a coordinate: 17
coherence mu = 0.4590478477175000934777023914688782554201
claimed      = 0.4590478477175000934777023914688782554201  difference 1.509e-41
attaining pair (0-based vectors) (18, 24)
leaderboard  = 0.45924802  leaderboard - mu = 2.001723e-04  (need >= 1e-8)
lower bound  = 0.42565792  mu - lower bound = 3.338993e-02  (need >= 0)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/6x47_bmea.txt 6 47 0.4590478477175000934777023914688782554201 0.45924802 0.42565792 c8fa32286e01682d603e52dd8146c7f8ed6b01be7f3e1a171344c74a643ff8eb
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/6x47.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (6x47.txt, 6x48.txt, kept from the original first run); writes out/6x47.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 853 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/6x47.txt), converted to float64 and written with 20 decimal places for packing-records.
