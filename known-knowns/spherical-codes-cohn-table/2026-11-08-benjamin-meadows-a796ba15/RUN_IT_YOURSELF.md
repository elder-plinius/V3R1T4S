# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 a796ba15c620c062792f104ee416a92acba3ab77cabe80ceedcf97f67e233ddc
objects: 727  expected: 727  fewest significant digits in a coordinate: 21
computed = 0.2365029694576581825515416687051581290107
claimed  = 0.2365029694576581825515416687051581290107  difference = 4.709e-41
closest pair (0-based rows) (696, 721)
table cos - c* = 3.551075773341817e-3  (need >= 1e-10)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_cohn.py spherical object/29_727.txt 29 727 0.2365029694576581825515416687051581290107 0.240054045231 a796ba15c620c062792f104ee416a92acba3ab77cabe80ceedcf97f67e233ddc
```

## Rebuild

The search code is in how-we-built-it/src/ (pinned requirements: how-we-built-it/requirements.txt; sph.py needs numba). The scripts use paths relative to the container's working directory. The producing run was `TP=tpM14 python3 chain3.py qRetp.txt` with the queue row in mode `add:cells/29-725.txt`; that queue file was overwritten during the run, so its trials and iters fields are not recorded (defaults 4 and 160). The donor chain and the logged lines are in how-we-built-it/src/hit.log. The run used wall-clock budgets, so a rerun can take a different path.
