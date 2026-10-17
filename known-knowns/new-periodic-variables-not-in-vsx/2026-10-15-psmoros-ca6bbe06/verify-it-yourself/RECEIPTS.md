# Receipts (real output, Python 3.14.2, macOS)

## sh verify-it-yourself/run_checks.sh   (run at 2026-10-15T21:07:47Z)
```
integrity: 48 files listed, 0 bad
variables: scored 80, recovered (independent agree) 77
controls: scored 400 (VSX CST 67), max control S 21.103453, S > 54.0: 0/400 overall, 0/67 CST
recovered AND S above every control: 77 (rule: >= 50)
light curves: not checked offline (run fetch_lightcurves.py DIR, then this script with --lc-dir DIR)
PASS
```

## python3 -I -B verify-it-yourself/check_gate.py --lc-dir lc   (run at 2026-10-15T21:07:48Z)
Here `lc` held the 82 scored variable-star responses exactly as saved by the run (their sha256 equal the
manifest), i.e. what verify-it-yourself/fetch_lightcurves.py writes when SNAD serves the same release.
```
integrity: 48 files listed, 0 bad
variables: scored 80, recovered (independent agree) 77
controls: scored 400 (VSX CST 67), max control S 21.103453, S > 54.0: 0/400 overall, 0/67 CST
recovered AND S above every control: 77 (rule: >= 50)
light curves: 77 recovered periods folded; worst PDM ratio to random median 0.733 (limit 0.8)
PASS
```
After this file was written, SHA256SUMS was regenerated and run_checks.sh was run again with the same output.

## Network path, run on a copy of this package at 2026-10-15T23:10:00Z-23:14:42Z
```
$ python3 -I verify-it-yourself/fetch_lightcurves.py lc
fetched 82 light curves; 82 byte-identical to the scored files
$ python3 -I -B verify-it-yourself/check_gate.py --lc-dir lc
integrity: 48 files listed, 0 bad
variables: scored 80, recovered (independent agree) 77
controls: scored 400 (VSX CST 67), max control S 21.103453, S > 54.0: 0/400 overall, 0/67 CST
recovered AND S above every control: 77 (rule: >= 50)
light curves: 77 recovered periods folded; worst PDM ratio to random median 0.733 (limit 0.8)
PASS
```
