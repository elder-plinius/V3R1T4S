# Receipts: real output of verify-it-yourself/run_checks.sh

Run from a clean copy of this package (no cache; date -u before: Mon Nov 23 07:53:07 UTC 2026), python3 with numpy, scipy, mpmath; exit code 0.

```
inputs sha256 ok
calibration N=35: E_posted - E_table = 9.34e-08
calibration N=42: E_posted - E_table = 3.46e-07
calibration N=57: E_posted - E_table = -1.38e-08
calibration N=63: E_posted - E_table = 3.96e-07
calibration N=89: E_posted - E_table = -3.82e-07
calibration N=90: E_posted - E_table = 3.18e-07
calibration N=149: E_posted - E_table = 1.05e-08
calibration N=155: E_posted - E_table = -1.05e-07
calibration N=158: E_posted - E_table = -1.12e-07
calibration N=159: E_posted - E_table = 2.53e-07
calibration N=121: E_posted - E_table = 4.24e-07
object sha256 matches INDEX.csv
object as given: E = -198.47902916627 eV (claimed -198.47902916627226), float64 |grad| = 4.72e-14
mpmath iteration 0: E = -198.4790291662722464899116  |grad| = 5.0725e-14
mpmath iteration 1: E = -198.4790291662722464899116  |grad| = 1.3892e-23
object: E = -198.4790291663 eV; table N=121 -198.211397; margin -0.267632 eV
Hessian: near-zero modes 6, negative 0, lowest nonzero 0.1490
posted N=121 polished: -198.2113965759 eV; object lower by 0.267633 eV
problems: []
PASS
```
