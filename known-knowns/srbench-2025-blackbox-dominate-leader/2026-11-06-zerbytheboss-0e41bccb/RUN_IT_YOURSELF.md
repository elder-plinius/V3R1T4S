# Run It Yourself

## Requirements

- Python 3.8+ (standard library only).
- Runtime: < 2 seconds on a single CPU core; < 25 MB RAM.

## Verification Command

```bash
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS` (exit code 0). Modifying any digit in `object/srbench2025_verified_splits.csv` causes `sh verify-it-yourself/run_checks.sh` to print `FAIL` and exit with status 1.
