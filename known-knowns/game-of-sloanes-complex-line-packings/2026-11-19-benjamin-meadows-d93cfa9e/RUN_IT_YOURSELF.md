# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 d93cfa9e4a52fe04c0bfea5a4894577ae9a7a699a27ed8ba93098d44926feb1e
d = 6, n = 44, numbers: 528, fewest significant digits in a coordinate: 21
coherence mu = 0.4454997364686413214894167613702234492231
claimed      = 0.4454997364686413214894167613702234492231  difference 2.962e-41
attaining pair (0-based vectors) (3, 21)
leaderboard  = 0.44643020  leaderboard - mu = 9.304635e-04  (need >= 1e-8)
lower bound  = 0.41585133  mu - lower bound = 2.964841e-02  (need >= 0)
best pending = 0.44589711067290106763  pending - mu = 3.973742e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/6x44_bmea.txt 6 44 0.4454997364686413214894167613702234492231 0.44643020 0.41585133 d93cfa9e4a52fe04c0bfea5a4894577ae9a7a699a27ed8ba93098d44926feb1e 0.44589711067290106763
```

## Where it came from

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 build_job.py                          # fetches every input packing by URL, checks its sha256, writes job.json
python3 order_check.py ../../object/6x44_bmea.txt   # compares the object, in vector order, with every input; expected output: order_check.txt
```

## Rebuild

```sh
python3 run_job.py            # the full job, 20070 s on one worker; or python3 run_job.py 600 for a short run
```

It writes out/best/6x44_j1.txt and out/progress.jsonl. The original job ran on a Kaggle CPU session with numpy and scipy of that image (versions not recorded); requirements.txt pins the versions we used for the checks above. The search stops on a wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different path and need not reproduce the object digit for digit. The original job's log is how-we-built-it/src/progress.jsonl; the object is that job's final best file.
