# RECEIPTS: real output of verify-it-yourself/run_checks.sh

Run from this folder on the contributor's machine (Python 3.11, numpy 2.4.6): started 2026-10-31T19:49:29Z, ended 2026-10-31T19:49:31Z (date -u).

```
$ sh verify-it-yourself/run_checks.sh
sha256 object/N38_Ne.xyz = 31155172b650ba08dc63be96d76a7f189e754612e2d6e7183a744ac6c1270fe1
sha256 matches INDEX.csv: ok
N = 38
min significant digits = 18 (need >= 12): ok
E_LJ (50-digit decimal) = -168.984987247422   (double: -168.984987247422)
gradient norm (decimal) = 1.641e-13   (double: 1.827e-13)  need < 1e-9: ok
Hessian: 6 eigenvalues with |lambda| < 1e-6 (need exactly 6), lowest eigenvalue -7.611891e-14 (need >= -1e-6), max |zero mode| 7.612e-14, lowest nonzero 8.097800e-01: ok
certified classical minimum: YES
E_Xe = E_LJ + (0.01/2) * sum sqrt(lambda) = -162.663403
E_Ar = E_LJ + (0.03/2) * sum sqrt(lambda) = -150.020234
E_Ne = E_LJ + (0.095/2) * sum sqrt(lambda) = -108.929936
record test Ne: bar -107.42431, E_sp -108.929936, bar - E_sp = 1.505626 (need >= 5e-04 on a certified minimum): BEATS BAR
RESULT: PASS
PASS
exit 0
```
