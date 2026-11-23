# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 ebfcd805697bcd8c7c10c5dc51ba1b58267aaa59162733e6d9026e8e39143bbc
d = 7, n = 29, numbers: 406, fewest significant digits in a coordinate: 21
coherence mu = 0.3400004550336341244794899860286491766629
claimed      = 0.3400004550336341244794899860286491766629  difference 1.385e-41
attaining pair (0-based vectors) (4, 19)
leaderboard  = 0.34064551  leaderboard - mu = 6.450550e-04  (need >= 1e-8)
lower bound  = 0.33502970  mu - lower bound = 4.970755e-03  (need >= 0)
best pending = 0.34054289311848036660  pending - mu = 5.424381e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/7x29_bmea.txt 7 29 0.3400004550336341244794899860286491766629 0.34064551 0.33502970 ebfcd805697bcd8c7c10c5dc51ba1b58267aaa59162733e6d9026e8e39143bbc 0.34054289311848036660
```

## Where it came from

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 build_job.py                          # fetches every input packing by URL, checks its sha256, writes job.json
python3 order_check.py ../../object/7x29_bmea.txt   # compares the object, in vector order, with every input; expected output: order_check.txt
```

## Rebuild

```sh
python3 run_job.py            # the full job, 20070 s on one worker; or python3 run_job.py 600 for a short run
```

It writes out/best/7x29_j0.txt and out/progress.jsonl. The original job ran on a Kaggle CPU session with numpy and scipy of that image (versions not recorded); requirements.txt pins the versions we used for the checks above. The search stops on a wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different path and need not reproduce the object digit for digit. The original job's log is how-we-built-it/src/progress.jsonl; the object is that job's final best file.
