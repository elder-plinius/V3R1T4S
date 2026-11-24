# Receipts (real output; same checker files and byte-identical certificate, run 2026-11-24 ~07:50-08:00 UTC on a fresh copy of the claim folder)
Package-level clean-copy and tamper results: the kit's check_run --package receipt (runs/2026-11-24-0729/check_run_package_presubmit.txt).
```
precision bits: 128
check 0: wvcount matches the definition at 2859 points <= 20000
check rho: 22 intervals use Sigma(n) at 20 levels n <= 20000 (weights certified, exact sums, identity sum_q P_q = (sum L)^2 OK)
check 1-2: 9906 intervals admissible; recomputed sups <= stated (max relative slack 5.1e-06)
check 3: A(1e10) <= 0.01070009059 <= 0.0107001
B <= 2.1257393973040676877 (sup of the ball, recomputed)
check 4: B < 2.1257395
PASS
precision bits: 256
check 0: wvcount matches the definition at 2859 points <= 20000
check rho: 22 intervals use Sigma(n) at 20 levels n <= 20000 (weights certified, exact sums, identity sum_q P_q = (sum L)^2 OK)
check 1-2: 9906 intervals admissible; recomputed sups <= stated (max relative slack 5.1e-06)
check 3: A(1e10) <= 0.01070009059 <= 0.0107001
B <= 2.1257393973040676877 (sup of the ball, recomputed)
check 4: B < 2.1257395
PASS
both precisions: PASS
PASS
```

Tamper tests (verify/tamper_tests.py, claim folder):
```
rho intervals: 22 ; tampered interval index: 11
rho term lowered by 1e-6 relative                  exit=1  FAIL reason: interval 11: recomputed 0.0025312235963600461785 exceeds stated 2.53122106513644978473e-03  -> rejected (ok)
rho term raised by 1e-4 relative                   exit=1  FAIL reason: interval 11: stated 2.53147671871968224511e-03 exceeds recomputed 0.0025312235963600461785 by more than 1e-5 relative (corrupted certific  -> rejected (ok)
'rho' flag removed (Lambda^2 used)                 exit=1  FAIL reason: interval 11: recomputed 0.0025974565391733550166 exceeds stated 0.0025312235963600462881  -> rejected (ok)
z_i of a rho interval scaled by 0.9                exit=1  FAIL reason: interval 11: recomputed 0.0025338864543669005141 exceeds stated 0.0025312235963600462881  -> rejected (ok)
'rho' flag added to an interval with z > 20000     exit=1  FAIL reason: rho flag on interval 22 with z > 20000  -> rejected (ok)
tamper tests: PASS
```
