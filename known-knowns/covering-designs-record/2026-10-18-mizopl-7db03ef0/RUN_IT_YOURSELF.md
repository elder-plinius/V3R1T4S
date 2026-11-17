# Run It Yourself: Exhaustive Verification of `C(40, 16, 7) <= 7,251`

## Requirements

- POSIX shell (`sh`)
- Python 3.8+ with `numpy` installed

## One-Line Verification Command (~4 seconds)

From the root of this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

## Optional: Rebuild the Raw Staircase Design from LJCR Ingredients

The seven La Jolla ingredient designs are not vendored; the first command downloads them (a few kB, one HTTP Range request each into the frozen Zenodo LJCR v1.2 `covers.json`) and checks each against the sha256 in `how-we-built-it/INGREDIENTS.tsv`. The builder reads those downloaded copies and refuses to run on a missing or mismatching ingredient.

```sh
python3 how-we-built-it/fetch_ingredients.py
python3 how-we-built-it/build_40_16_7.py how-we-built-it/staircase_40_16_7.txt
cc -O3 -o how-we-built-it/prune how-we-built-it/prune.c
./how-we-built-it/prune 40 16 7 how-we-built-it/staircase_40_16_7.txt how-we-built-it/pruned_40_16_7.txt 1
```
