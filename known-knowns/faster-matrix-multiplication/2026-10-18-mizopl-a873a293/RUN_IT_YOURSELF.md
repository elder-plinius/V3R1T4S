# Run It Yourself: Exhaustive Verification of `9x12x14` Rank 954 in `ZT = {-1, 0, 1}`

## Requirements

- POSIX shell (`sh`)
- Python 3.8+ with `numpy` installed

## One-Line Verification Command (~0.2 seconds)

From the root of this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

## What `run_checks.sh` Does

1. Runs a positive control on Strassen's `2x2x2` rank-7 ternary scheme (`64/64` Brent equations satisfied) and two negative controls (corrupted `W` entry and non-ternary coefficient `2`, both rejected).
2. Reads `object/9x12x14_m954_ZT.json` (`sha256: a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02`, `915,296` bytes).
3. Verifies:
   - Exact format `(9, 12, 14)` and rank `m = 954`
   - Every entry of `u` (`954 x 108`), `v` (`954 x 168`), and `w` (`954 x 126`) lies in `{-1, 0, 1}` (`max_abs = 1`)
   - No rank-1 term has an all-zero `u_q`, `v_q`, or `w_q` vector (`zero_terms = 0`)
   - Exhaustively checks all `108 * 168 * 126 = 2,286,144` Brent equations over `Z` in exact `int64` arithmetic (`mismatches = 0`).
4. Prints `PASS` on the final line and exits with status `0` (or prints `FAIL` and exits `1` if any check fails or if a single digit in `object/9x12x14_m954_ZT.json` is corrupted).
