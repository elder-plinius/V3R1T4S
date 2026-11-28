# Run It Yourself

## Requirements

- Python 3.8+ (standard library only) and a standard C99 compiler (`cc`, `gcc`, or `clang`).
- Runtime: ~11 seconds on a single CPU core; < 15 MB RAM.

## Verification Command

```bash
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS` (exit code 0). Modifying any digit in `object/a000229_qnr_census.json` causes `sh verify-it-yourself/run_checks.sh` to print `FAIL` and exit with status 1.
