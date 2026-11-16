# Run It Yourself (`post-tag-busy-beaver-bbpt`: Exact `BB_PT(8) = 19`)

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (~0.2–1.5 seconds, Python 3 standard library only):
```text
Calibration checks (S=7..11): OK
Exhaustive raw enumeration & conjugacy check: 19693 systems -> 1728 canonical classes OK
Verified all 19693 raw size-8 2-tag systems (1728 canonical classes):
  HALT:          17374 raw (1012 canonical), max steps = 19 (111_20_)
  CYCLE:          1404 raw ( 348 canonical)
  DFA_INVARIANT:   915 raw ( 368 canonical)
BB_PT(8) = 19 CERTIFIED EXACT.
PASS
```
