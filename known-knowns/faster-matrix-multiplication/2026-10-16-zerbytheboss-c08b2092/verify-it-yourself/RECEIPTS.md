# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (c08b2092f9e0ec767e9eaa7b7293e2b928463bad843e7d24d8e2b272355f5cc0)
== check_slp.py (exact tensor identity over Z, ternary coefficients, straight-line order, reduced addition count)
{"file": "2x5x6_m47_cr177_ZT_reduced.json", "format": "2x5x6", "rank": 47, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 38, "adds_V": 64, "adds_W": 75, "adds_total": 177, "naive_total": 347, "declared_reduced": 177, "VALID": true}
checker verdict: PASS (VALID=True, rank=47, adds_total=177, tensor=C^T)
== brent_check.py (all 3600 Brent equations over Z, entries in -1,0,1, rank 47, cr 177)
format 2x5x6 rank 47 equations 3600 brent_bad 0 ternary True cr 177
BRENT_OK brent_bad=0
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected by check_slp (VALID false)
negative control rejected by brent_check
ALL CHECKS PASS
```
