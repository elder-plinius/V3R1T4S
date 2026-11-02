# Run It Yourself

## Requirements

- Python 3.8+ (standard library only, no third-party packages).
- Runtime: ~2.5 seconds on a single CPU core; < 30 MB RAM.

## Verification Command

```bash
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS` (exit code 0). If any digit in `object/a182275_dissections.json` is modified, `sh verify-it-yourself/run_checks.sh` prints `FAIL` and exits with status 1.
