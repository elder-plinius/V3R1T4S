# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 accf82a6ee2089b168a50f6100f78a3b3a7edf28ca8af3bf01ed8e0386c01d5c
d = 7, n = 31, numbers: 434, fewest significant digits in a coordinate: 21
coherence mu = 0.3485093138521599189322310158935112513346
claimed      = 0.3485093138521599189322310158935112513346  difference 3.960e-41
attaining pair (0-based vectors) (5, 28)
leaderboard  = 0.34941560  leaderboard - mu = 9.062861e-04  (need >= 1e-8)
lower bound  = 0.33806170  mu - lower bound = 1.044761e-02  (need >= 0)
best pending = 0.34935941870298209437  pending - mu = 8.501049e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x31_bmea.txt 7 31 0.3485093138521599189322310158935112513346 0.34941560 0.33806170 accf82a6ee2089b168a50f6100f78a3b3a7edf28ca8af3bf01ed8e0386c01d5c 0.34935941870298209437
```

## Where it came from

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 build_job.py                          # fetches every input packing by URL, checks its sha256, writes job.json
python3 order_check.py ../../object/7x31_bmea.txt   # compares the object, in vector order, with every input; expected output: order_check.txt
```

## Rebuild

```sh
python3 run_job.py            # the full job, 20070 s on one worker; or python3 run_job.py 600 for a short run
```

It writes out/best/7x31_j0.txt and out/progress.jsonl. The original job ran on a Kaggle CPU session with numpy and scipy of that image (versions not recorded); requirements.txt pins the versions we used for the checks above. The search stops on a wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different path and need not reproduce the object digit for digit. The original job's log is how-we-built-it/src/progress.jsonl; the object is that job's final best file.
