# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 80cabc361c4f9c454bb1f6578825472fd9d3f22d8b985a9eed43623f135072e6
objects: 61  expected: 61  fewest significant digits in a coordinate: 27
computed = 4.1039483024343148952606505611268790536707
claimed  = 4.1039483024343148952606505611244132633712  difference = 2.466e-30
smallest pairwise distance 1.287268541234
table min E - E* = 1.521742836568510e-2  (need >= 1.000e-9)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_cohn.py harmonic object/61-21.txt 61 21 4.1039483024343148952606505611244132633712 4.1191657308 80cabc361c4f9c454bb1f6578825472fd9d3f22d8b985a9eed43623f135072e6
```

## Basin test (needs numpy, scipy and mpmath)

The criterion also asks that a polish of the 2021 data set's configuration stays above E* + max(1e-9, 1e-12 E*). Download data.txt (78263492 bytes, sha256 in the-record-we-beat/RECORD.md) from https://hdl.handle.net/1721.1/130937 and run, with the object copied to a folder `cells/` as `61-21.txt`:

```sh
python3 how-we-built-it/harmonic_floor.py data.txt cells 61-21
```

It polishes the posted configuration by L-BFGS-B on row-normalised coordinates and prints one CSV line; on our run the polished posted energy was 4.119165730787241162410779, above E* by 0.0152174, and `ok` was True. The three panel skeptics ran their own polishes of the same file and agree (panel/).

## Rebuild

The search code is in how-we-built-it/src/ (pinned requirements: how-we-built-it/requirements.txt). It ran in a sandbox whose workspace was `/work`, with the 2021 data set's configurations as starting points. The producing run:

```sh
OMP_NUM_THREADS=1 python3 -u worker3.py 21 44 64 run2/w2 25 31 1 0
```

(n = 21, N from 44 to 64, 25 s of hops per row, rng seed 31, one round, no two-point deletion); harvest.py wrote the cell.

Both scripts use wall-clock budgets, so an exact rerun can take a different path. Exact log lines: how-we-built-it/src/hit.log; file:line references: how-we-built-it/src/PROVENANCE.md.
