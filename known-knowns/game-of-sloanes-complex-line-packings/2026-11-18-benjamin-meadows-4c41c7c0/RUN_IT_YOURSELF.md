# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 4c41c7c0e9e16eed48aef8079a6c5026221bbc3864fe2bf0c4e988b60efca4a6
d = 3, n = 49, numbers: 294, fewest significant digits in a coordinate: 16
coherence mu = 0.8014002929078314485491951592004713189248
claimed      = 0.8014002929078314485491951592004713189248  difference 2.462e-41
attaining pair (0-based vectors) (12, 29)
leaderboard  = 0.80155093  leaderboard - mu = 1.506371e-04  (need >= 1e-8)
lower bound  = 0.71428571  mu - lower bound = 8.711458e-02  (need >= 0)
best pending = 0.80143721449743558115  pending - mu = 3.692159e-05  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/3x49_bmea.txt 3 49 0.8014002929078314485491951592004713189248 0.80155093 0.71428571 4c41c7c0e9e16eed48aef8079a6c5026221bbc3864fe2bf0c4e988b60efca4a6 0.80143721449743558115
```

## Rebuild

The search code is in how-we-built-it/src/, with pinned requirements in how-we-built-it/requirements.txt (we re-ran it with Python 3.13.18, numpy 2.5.4 and scipy 1.18.1 on 2026-11-18; the versions of the original 2026-11-01 runs were not recorded). From a fresh shell:

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 driver.py 1 0          # first run: random starts for the cell in slice.json; writes out/3x49.txt and results.jsonl
python3 reopt.py job_second.json 1   # second run: starts from the packing files in prev/out/ (3x49.txt, kept from the original first run); writes out/3x49.txt only if it improves on the file there
```

Run reopt.py from how-we-built-it/src/, because the start paths in job_second.json are relative to the working folder. driver.py runs the cell in slice.json with the budget formula in driver.py and seed 0; the original first run also used seeds 1 to 4 for cells near the table. Both scripts stop on wall-clock budgets (the second run used 673 s for this cell, and the original runs shared 4 cores with other cells), so a rerun can take a different path and need not reproduce the object digit for digit. The logged runs for this cell are in how-we-built-it/src/runs-first.jsonl and runs-second.jsonl. The object itself is the output of the second run (out/3x49.txt), converted to float64 and written with 20 decimal places for packing-records.
