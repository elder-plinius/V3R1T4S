# How We Built It (`ghz-nonlocality-robustness-below-049143`)

## Pinned Requirements
- `python3 >= 3.8` with `mpmath >= 1.3.0` (`mpmath.iv`) and `scipy` (for LP discovery in `generate_18x24x72.py`; `scipy` is not needed to run `verify-it-yourself/run_checks.sh`)
- C++17 compiler (`clang++` or `g++`)

## Exact Commands to Rebuild and Verify
```sh
python3 how-we-built-it/generate_18x24x72.py
sh verify-it-yourself/run_checks.sh
```
