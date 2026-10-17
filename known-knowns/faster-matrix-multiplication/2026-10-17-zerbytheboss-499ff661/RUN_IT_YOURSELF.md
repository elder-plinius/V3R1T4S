# Run It Yourself

## 1. Verify the Ternary `6x12x14` Rank-654 Scheme in 0.3 Seconds
From this package root:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_zt_scheme.py` using only the Python 3 standard library. It verifies:
1. Exact SHA-256 match of `object/6x12x14_m654_ZT.json` against `INDEX.csv`.
2. Dimensions `[6, 12, 14]`, rank `m = 654`, and that every entry of `U` (`654 x 72`), `V` (`654 x 168`), and `W` (`654 x 84`) lies strictly in `{-1, 0, 1}` (`max_abs = (1, 1, 1)`).
3. All `72 * 168 * 84 = 1,016,064` integer Brent equations over `Z` (`0` errors: support size exactly `6 * 12 * 14 = 1008`, with every diagonal entry `1` and all `1,015,056` off-diagonal entries `0`).
4. 10 independent random integer matrix multiplications `A * B = C` over `Z`.

## 2. How to Rebuild the Object
```sh
python3 how-we-built-it/construct_6x12x14_zt.py
```
