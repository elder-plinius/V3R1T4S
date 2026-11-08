# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 c9da55b9f9cfe7a4711ded4bae4c1f46700366b616fa820fd31e794eba3bb9d2
objects: 62  expected: 62  fewest significant digits in a coordinate: 28
computed = 0.8891705545504745639782620838840554149827
claimed  = 0.8891705545504745639782620838840554149826  difference = 7.615e-41
closest pair (0-based subspaces) (11, 36)
value - table = 5.531105047456398e-5  (need >= 1e-9)
bound - value = 3.482348424952544e-2  (need >= -1e-10)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_cohn.py grassmannian object/11-1-62.txt 11 1 62 0.8891705545504745639782620838840554149826 0.8891152435 0.9239940388 c9da55b9f9cfe7a4711ded4bae4c1f46700366b616fa820fd31e794eba3bb9d2
```

## Rebuild

The search code is in how-we-built-it/src/ (pinned requirements: how-we-built-it/requirements.txt). It ran in a container, with Sloane's file `grassc.11.1.62` from https://neilsloane.com/grass/ under `grass/txts/`. The producing command, from the queue driver run11w.sh:

```sh
timeout 180 python3 refix5.py 11 1 62 120
```

then harvest2.py wrote the cell with an mpmath re-orthonormalisation (mkcell.py). Exact log lines: how-we-built-it/src/hit.log; the scripts are the versions that ran.
