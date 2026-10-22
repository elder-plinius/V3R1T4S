# Receipts (real output, 2026-10-22, from the package folder)
$ sh verify-it-yourself/run_checks.sh
```
n=16 k=2 m=102 stray_chars=[] lengths_ok=True distinct=True clash=None
VALID
n=16 m=102 pairs=5151 distinct_unions=5151
PASS
m=102 > OEIS bound 91
PASS
```
Checker self-test (small inputs written for this check; expected VALID|PASS, then INVALID|FAIL three times):
```
pos_n8: VALID | PASS
neg_n8: INVALID | FAIL
stray_n8: INVALID | FAIL
space_n8: INVALID | FAIL
```
