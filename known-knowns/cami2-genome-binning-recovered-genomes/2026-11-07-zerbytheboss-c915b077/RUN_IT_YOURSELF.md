# Run It Yourself

## Requirements

- Python 3.8+ (standard library only).
- Runtime: < 3 seconds on a single CPU core; < 50 MB RAM.

## Verification Command

```bash
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS` (exit code 0). Modifying any digit in `object/amber_cami2_per_bin_metrics.tsv` causes `sh verify-it-yourself/run_checks.sh` to print `FAIL` and exit with status 1.
