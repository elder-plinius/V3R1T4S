# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 b197df4be95fd38c4ea50cfb785eb5dfc8d218f9ad10196443da19d098b5c990
d = 6, n = 45, numbers: 540, fewest significant digits in a coordinate: 21
coherence mu = 0.4503506341028972582490163551176797481320
claimed      = 0.4503506341028972582490163551176797481320  difference 2.848e-41
attaining pair (0-based vectors) (13, 23)
leaderboard  = 0.45132430  leaderboard - mu = 9.736659e-04  (need >= 1e-8)
lower bound  = 0.41931393  mu - lower bound = 3.103670e-02  (need >= 0)
best pending = 0.45112660942111073749  pending - mu = 7.759753e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/6x45_bmea.txt 6 45 0.4503506341028972582490163551176797481320 0.45132430 0.41931393 b197df4be95fd38c4ea50cfb785eb5dfc8d218f9ad10196443da19d098b5c990 0.45112660942111073749
```

## Where it came from

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 build_job.py                          # fetches every input packing by URL, checks its sha256, writes job.json
python3 order_check.py ../../object/6x45_bmea.txt   # compares the object, in vector order, with every input; expected output: order_check.txt
```

## Rebuild

```sh
python3 run_job.py            # the full job, 20070 s on one worker; or python3 run_job.py 600 for a short run
```

It writes out/best/6x45_j0.txt and out/progress.jsonl. The original job ran on a Kaggle CPU session with numpy and scipy of that image (versions not recorded); requirements.txt pins the versions we used for the checks above. The search stops on a wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different path and need not reproduce the object digit for digit. The original job's log is how-we-built-it/src/progress.jsonl; the object is that job's final best file.
