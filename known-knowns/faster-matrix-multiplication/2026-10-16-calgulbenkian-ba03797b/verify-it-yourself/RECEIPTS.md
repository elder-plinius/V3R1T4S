# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (ba03797bb02013423a43e98b27ac46c6897018e12f9e90f0761e874c402070d7)
== check_slp.py on object/2x4x7_m45_cr169_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x4x7_m45_cr169_ZT_reduced.json", "format": "2x4x7", "rank": 45, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 35, "adds_V": 67, "adds_W": 67, "adds_total": 169, "naive_total": 308, "declared_reduced": 169, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=169, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
