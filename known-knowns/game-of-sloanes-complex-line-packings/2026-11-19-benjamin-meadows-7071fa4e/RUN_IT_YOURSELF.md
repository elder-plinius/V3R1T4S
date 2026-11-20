# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 7071fa4e349c69da093b420911b015c646429c1afd746930b1088f6296da6353
d = 7, n = 24, numbers: 336, fewest significant digits in a coordinate: 21
coherence mu = 0.3290360584555490631522006857841459090217
claimed      = 0.3290360584555490631522006857841459090217  difference 2.914e-41
attaining pair (0-based vectors) (10, 19)
leaderboard  = 0.32959971  leaderboard - mu = 5.636515e-04  (need >= 1e-8)
lower bound  = 0.32494624  mu - lower bound = 4.089818e-03  (need >= 0)
best pending = 0.32934295752156057206  pending - mu = 3.068991e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x24_bmea.txt 7 24 0.3290360584555490631522006857841459090217 0.32959971 0.32494624 7071fa4e349c69da093b420911b015c646429c1afd746930b1088f6296da6353 0.32934295752156057206
```

## Where it came from

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 build_job.py                          # fetches every input packing by URL, checks its sha256, writes job.json
python3 order_check.py ../../object/7x24_bmea.txt   # compares the object, in vector order, with every input; expected output: order_check.txt
```

## Rebuild

```sh
python3 run_job.py            # the full job, 20070 s on one worker; or python3 run_job.py 600 for a short run
```

It writes out/best/7x24_j0.txt and out/progress.jsonl. The original job ran on a Kaggle CPU session with numpy and scipy of that image (versions not recorded); requirements.txt pins the versions we used for the checks above. The search stops on a wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different path and need not reproduce the object digit for digit. The original job's log is how-we-built-it/src/progress.jsonl; the object is that job's final best file.
