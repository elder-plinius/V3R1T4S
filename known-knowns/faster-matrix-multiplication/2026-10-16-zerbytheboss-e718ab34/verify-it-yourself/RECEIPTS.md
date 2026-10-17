# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (390137202a525ecc9e2e7e3fd04ae26608e7cb6e0057d6f5423535cac0252b15)
== check_slp.py (exact tensor identity over Z, ternary coefficients, straight-line order, reduced addition count)
{"file": "2x4x7_m45_cr161_ZT_reduced.json", "format": "2x4x7", "rank": 45, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 35, "adds_V": 58, "adds_W": 68, "adds_total": 161, "naive_total": 336, "declared_reduced": 161, "VALID": true}
checker verdict: PASS (VALID=True, rank=45, adds_total=161, tensor=C^T)
== brent_check.py (all 3136 Brent equations over Z, entries in -1,0,1, rank 45, cr 161)
format 2x4x7 rank 45 equations 3136 brent_bad 0 ternary True cr 161
BRENT_OK brent_bad=0
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected by check_slp (VALID false)
negative control rejected by brent_check
ALL CHECKS PASS
```
