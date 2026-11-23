# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 8f47404a6ab8b0baa40e1a24d3a9fc5a968aa21da1bafc97ed89bb2bdfa69896
d = 5, n = 36, numbers: 360, fewest significant digits in a coordinate: 21
coherence mu = 0.4992008036545907036093659314091692481845
claimed      = 0.4992008036545907036093659314091692481845  difference 3.736e-41
attaining pair (0-based vectors) (23, 27)
leaderboard  = 0.49998890  leaderboard - mu = 7.880963e-04  (need >= 1e-8)
lower bound  = 0.47519096  mu - lower bound = 2.400984e-02  (need >= 0)
best pending = 0.49931760537131485881  pending - mu = 1.168017e-04  (need >= 1e-7)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_gos.py object/5x36_bmea.txt 5 36 0.4992008036545907036093659314091692481845 0.49998890 0.47519096 8f47404a6ab8b0baa40e1a24d3a9fc5a968aa21da1bafc97ed89bb2bdfa69896 0.49931760537131485881
```

## Where it came from

```sh
cd how-we-built-it/src
python3 -m venv .venv && . .venv/bin/activate && pip install -r ../requirements.txt
python3 build_job.py                          # fetches every input packing by URL, checks its sha256, writes job.json
python3 order_check.py ../../object/5x36_bmea.txt   # compares the object, in vector order, with every input; expected output: order_check.txt
```

## Rebuild

```sh
python3 run_job.py            # the full job, 20070 s on one worker; or python3 run_job.py 600 for a short run
```

It writes out/best/5x36_j0.txt and out/progress.jsonl. The original job ran on a Kaggle CPU session with numpy and scipy of that image (versions not recorded); requirements.txt pins the versions we used for the checks above. The search stops on a wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different path and need not reproduce the object digit for digit. The original job's log is how-we-built-it/src/progress.jsonl; the object is that job's final best file.
