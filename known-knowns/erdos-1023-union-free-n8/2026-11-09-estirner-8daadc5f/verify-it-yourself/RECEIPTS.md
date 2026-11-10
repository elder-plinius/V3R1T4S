# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this folder at 2026-11-09T13:42:53Z (date -u), Python 3.14.8:

```
0. sha256 8daadc5f6c94a0b0e2364d01cfb9db7931fff7e815d182b329dc4b5cd3293560 matches expected_sha256.txt
1. calibration a(1..4) by exhaustive search: [1, 2, 4, 7] (expected [1, 2, 4, 7])
2. 80 members, all distinct sets of distinct elements of {1..8}: True
3. union-free: maximal-union test True, per-element test True
   size profile: {2: 2, 3: 15, 4: 63}
4. size 80 >= 80: True
PASS
```
