# Run it yourself

All commands run from this package folder in a fresh shell.

## Quick check (standard library only)

```sh
sh verify-it-yourself/run_checks.sh
```

Needs python3 3.9 or later only; a few seconds and negligible memory. Expected: lines beginning `ok`, then `failed checks: 0`, and the last line `PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`.

The checker (a) verifies the sha256 of every file in `object/` against `verify-it-yourself/object_files.csv` (the full per-file index of the object folder), (b) recomputes the Wynn epsilon extrapolation from the 27 open-strip files at 80 digits and compares with the shipped results, (c) counts the decimals shared by the last four rungs of each corner transfer matrix ladder and by the two methods, (d) checks the value against Kong's bracket, and (e) counts matchings of small grids against OEIS A028420.

## Recompute the data (optional, heavy)

See `how-we-built-it/README.md`. In short, the open-strip eigenvalues come from `mdtm.c` and `hprun.py`, the extrapolation from `wynnB3.py`, and the corner transfer matrix ladder from `ctmchain.py` and `ctmchain_ext.py`. Widths up to 14 take seconds; width 28 needs about 13 GB and width 29 about 26 GB of memory. Do not share a machine with another large job for those.

## Layout note

This package differs from the contributor's claim folder in two places only: the per-file index of `object/` is `verify-it-yourself/object_files.csv` (the top-level `INDEX.csv` has the single row the package format requires), and `check_md.py` reads Kong's value from `the-record-we-beat/README.md`. Both are recorded in `verify-it-yourself/RECEIPTS.md`.
