# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2)
== check_slp.py on object/5x5x5_m93_cr332_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "5x5x5_m93_cr332_ZT_reduced.json", "format": "5x5x5", "rank": 93, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 87, "adds_V": 88, "adds_W": 157, "adds_total": 332, "naive_total": 843, "declared_reduced": 332, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=332, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
