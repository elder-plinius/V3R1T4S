# Receipts — output of sh verify-it-yourself/run_checks.sh

Run: 2026-11-13 (UTC), from this package folder, in a throwaway venv.

```
dataset OK: 500 rows, 7 features, sha256 matches
live table OK: LFS pointer oid matches the recorded table sha256
object integrity OK: expressions.json sha256 matches INDEX.csv
re-scored 30/30 splits: median R2 = 0.3313, median complexity = 145.5
bar check OK: median R2 0.3313 > 0.3009 and median complexity 145.5 <= 4996.5
PASS
```
