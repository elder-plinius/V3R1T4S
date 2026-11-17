# Receipts: real output of `sh verify-it-yourself/run_checks.sh`, run 2026-11-08T17:48:36Z from this folder

```
annual: RMSE 0.996243 n=1065 | published 1.00 n=1065 | |diff| 0.0038 <= 0.01: True | count ok: True | equals printed 0.9962432770: True
winter: RMSE 0.588143 n=999 | published 0.59 n=999 | |diff| 0.0019 <= 0.01: True | count ok: True | equals printed 0.5881431289: True
summer: RMSE 0.700051 n=1028 | published 0.70 n=1028 | |diff| 0.0001 <= 0.01: True | count ok: True | equals printed 0.7000514609: True
object sha256 a44c189b3573a67eb555cc473444fb7c09e6a87d719d986de96c38a0d3db1164 equals the recorded a44c189b3573a67eb555cc473444fb7c09e6a87d719d986de96c38a0d3db1164: True
PASS
```

exit status: 0 with the first working Python on PATH; 0 again with PYTHON set to a Python 3.11.15 virtual environment (standard library only is used).
A copy with one digit of the object changed printed 'object sha256 ... : False' and FAIL.
