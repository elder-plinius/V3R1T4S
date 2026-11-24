# Receipts (real output, copied from the terminal)

## `sh verify-it-yourself/run_checks.sh` (started 2026-11-23T17:43:10Z, 8-core Linux box, Python 3.13.5, gcc 14.2.0, python-flint 0.9.0 in verify-it-yourself/.venv)

```
check 0: vcount matches the definition at 2859 points <= 20000
check 1-2: 9906 intervals admissible; stated terms match recomputation (max rel diff 4.8e-20)
sum of interval bounds <= 0.313373392366251; pi_2(z) correction <= 1.03e-15
check 3: A(1e10) <= 0.01070009059 <= 0.0107001
B <= 2.1569669355299588530 (sup of the ball)
check 4: B < 2.156967
PASS

real	0m16.991s
user	1m39.773s
sys	0m0.339s
```

A copy with one digit of object/a_bound_certificate.json changed (the middle digit, as kit/check_run.py does) printed:

```
check 0: vcount matches the definition at 2859 points <= 20000
FAIL reason: interval 4943: stated term 9.2265006329156680408e-7 != recomputed 9.7678450318103538523e-7
FAIL
```
