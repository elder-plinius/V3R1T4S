# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (4cedfb0300d6174d108b33526e0559d6429a50ab606727d728fa933501cc7118)
== check_slp.py (exact tensor identity over Z, ternary coefficients, straight-line order, reduced addition count)
{"file": "3x4x4_m38_cr124_ZT_reduced.json", "format": "3x4x4", "rank": 38, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 32, "adds_V": 36, "adds_W": 56, "adds_total": 124, "naive_total": 240, "declared_reduced": 124, "VALID": true}
checker verdict: PASS (VALID=True, rank=38, adds_total=124, tensor=C^T)
== brent_check.py (all 2304 Brent equations over Z, entries in -1,0,1, rank 38, cr 124)
format 3x4x4 rank 38 equations 2304 brent_bad 0 ternary True cr 124
BRENT_OK brent_bad=0
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected by check_slp (VALID false)
negative control rejected by brent_check
ALL CHECKS PASS
```
