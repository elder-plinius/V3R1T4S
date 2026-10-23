# Run It Yourself: Exhaustive Verification of `C(68, 14, 5) <= 15,675`

## Requirements

- POSIX shell (`sh`)
- Python 3.8+ with `numpy` installed

## One-Line Verification Command (~3 seconds)

From the root of this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

## What `run_checks.sh` Does

1. Runs a positive control on the $7$-block Fano plane $C(7, 3, 2) = 7$ (`uncovered = 0`) and a negative control on a $6$-block incomplete design (`uncovered = 3 > 0`, rejected).
2. Reads `object/design_68_14_5.txt` (`sha256: 2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`, $632,514$ bytes).
3. Verifies:
   - Exact block count $b = 15,675$
   - Every block contains $k = 14$ distinct integers in $\{1, \dots, 68\}$
   - All $15,675$ blocks are distinct
   - Schonheim lower bound $L(68, 14, 5) = 5,785 \le 15,675$
   - Strictly improves on the Covering Repository record ($16,004$) and La Jolla Covering Repository record ($16,004$) by $329$ blocks
   - Exhaustively checks all $\binom{68}{5} = 10,424,128$ $5$-subsets of $\{1, \dots, 68\}$ via colexicographic ranking and confirms `uncovered = 0`.
4. Prints `PASS` on the final line and exits with status `0` (or prints `FAIL` and exits `1` if any check fails or if a single digit in `object/design_68_14_5.txt` is corrupted).

## Optional: Rebuild the Raw Staircase Design from LJCR Ingredients

The six La Jolla ingredient designs are not vendored; the first command downloads them (a few kB, one HTTP Range request each into the frozen Zenodo LJCR v1.2 `covers.json`) and checks each against the sha256 in `how-we-built-it/INGREDIENTS.tsv`. The builder refuses to run on a missing or mismatching ingredient.

```sh
python3 how-we-built-it/fetch_ingredients.py
python3 how-we-built-it/build_68_14_5.py how-we-built-it/staircase_68_14_5.txt
cc -O3 -o how-we-built-it/prune how-we-built-it/prune.c
./how-we-built-it/prune 68 14 5 how-we-built-it/staircase_68_14_5.txt how-we-built-it/pruned_68_14_5.txt 1
```
