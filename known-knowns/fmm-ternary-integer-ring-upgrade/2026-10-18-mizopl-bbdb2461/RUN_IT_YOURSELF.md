# Run It Yourself: Exhaustive Verification of `14x15x15` Rank 1,894 in `ZT = {-1, 0, 1}`

## Requirements

- POSIX shell (`sh`)
- Python 3.8+ with `numpy` installed

## One-Line Verification Command (~0.4 seconds)

From the root of this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

## What `run_checks.sh` Does

1. Runs a positive control on Strassen's `2x2x2` rank-7 ternary scheme (`64/64` Brent equations satisfied) and two negative controls (corrupted `W` entry and non-ternary coefficient `2`, both rejected).
2. Reads `object/14x15x15_m1894_ZT.json` (`sha256: bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`, `944,884` bytes).
3. Verifies:
   - Exact format `(14, 15, 15)` and rank `m = 1,894`
   - Every entry of `u` (`1894 x 210`), `v` (`1894 x 225`), and `w` (`1894 x 210`) lies in `{-1, 0, 1}` (`max_abs = 1`)
   - No rank-1 term has an all-zero `u_q`, `v_q`, or `w_q` vector (`zero_terms = 0`)
   - Exhaustively checks all `210 * 225 * 210 = 9,922,500` Brent equations over `Z` in exact `int64` arithmetic (`mismatches = 0`).
4. Prints `PASS` on the final line and exits with status `0` (or prints `FAIL` and exits `1` if any check fails or if a single digit in `object/14x15x15_m1894_ZT.json` is corrupted).
