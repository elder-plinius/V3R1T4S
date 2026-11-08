# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 18ce522b9988706b958025d21a9c807f3b487f5e10610d86d4f25406fa058532
objects: 66  expected: 66  fewest significant digits in a coordinate: 27
computed = 2.5777695524773071434134196517154616989223
claimed  = 2.5777695524773071434134196517154616989222  difference = 6.393e-41
closest pair (0-based subspaces) (31, 42)
value - table = 4.173277730714341e-5  (need >= 1e-9)
bound - value = 6.845832222692857e-3  (need >= -1e-10)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_cohn.py grassmannian object/11-4-66.txt 11 4 66 2.5777695524773071434134196517154616989222 2.5777278197 2.5846153847 18ce522b9988706b958025d21a9c807f3b487f5e10610d86d4f25406fa058532
```

## Rebuild

The search code is in how-we-built-it/src/ (pinned requirements: how-we-built-it/requirements.txt). It ran in a container, with Sloane's file `grassc.11.4.66` from https://neilsloane.com/grass/ under `grass/txts/`. The producing command, from the queue driver run14.sh:

```sh
timeout 410 python3 refix6.py 11 4 66 320
```

then harvest14.py wrote the cell with an mpmath re-orthonormalisation (mkcell.py). Exact log lines: how-we-built-it/src/hit.log; the scripts are the versions that ran.
