# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
sha256 968ebd541209b17fcf58284178aa4a81b6e3562ef520328e8520e250625e9c71
objects: 64  expected: 64  fewest significant digits in a coordinate: 27
computed = 6.6854636813572274909833858385394136557102
claimed  = 6.6854636813572274909833858385404135959869  difference = 9.999e-31
smallest pairwise distance 1.323663877827
table min E - E* = 3.778582244277251e-2  (need >= 1.000e-9)
PASS
```

The script runs:

```sh
python3 verify-it-yourself/check_cohn.py harmonic object/64-20.txt 64 20 6.6854636813572274909833858385404135959869 6.7232495038 968ebd541209b17fcf58284178aa4a81b6e3562ef520328e8520e250625e9c71
```

## Basin test (needs numpy, scipy and mpmath)

The criterion also asks that a polish of the 2021 data set's configuration stays above E* + max(1e-9, 1e-12 E*). Download data.txt (78263492 bytes, sha256 in the-record-we-beat/RECORD.md) from https://hdl.handle.net/1721.1/130937 and run, with the object copied to a folder `cells/` as `64-20.txt`:

```sh
python3 how-we-built-it/harmonic_floor.py data.txt cells 64-20
```

It polishes the posted configuration by L-BFGS-B on row-normalised coordinates and prints one CSV line; on our run the polished posted energy was 6.723249503773814233455731, above E* by 0.0377858, and `ok` was True. The three panel skeptics ran their own polishes of the same file and agree (panel/).

## Rebuild

The search code is in how-we-built-it/src/ (pinned requirements: how-we-built-it/requirements.txt). It ran in a container with the 2021 data set's configurations as starting points. The producing run:

```sh
OMP_NUM_THREADS=1 python3 -u liftseed.py run4/w9 18 555 <row list>
```

(18 s per row, rng seed 555; 64-20 is one row of the list), seeded from the (64, 19) file made by `OMP_NUM_THREADS=1 python3 -u worker3.py 19 44 64 run2/w0 25 5 1 0`; harvest.py wrote the cell.

Both scripts use wall-clock budgets, so an exact rerun can take a different path. Exact log lines: how-we-built-it/src/hit.log; file:line references: the scripts are the versions that ran.
