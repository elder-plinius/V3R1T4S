# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (aee2afd0dd35ce54d64786b5439fc37101e55a8a758cfd2a8e572e4431396c8c)
== check_slp.py on object/4x5x6_m90_cr348_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x5x6_m90_cr348_ZT_reduced.json", "format": "4x5x6", "rank": 90, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 81, "adds_V": 104, "adds_W": 163, "adds_total": 348, "naive_total": 1023, "declared_reduced": 348, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=348, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```
