# Receipts
Output of `sh verify-it-yourself/run_checks.sh` from this folder, 2026-11-02T19:04:53Z UTC (python3 3.13.5):

```
cover ('tcnf', 5, 8, 4) cubes 32 of 32 OK
cover ('mcnf', 5, 8, 4) cubes 32 of 32 OK
cover ('tcnf', 5, 7, 4) cubes 32 of 32 OK
cover ('mcnf', 5, 7, 4) cubes 32 of 32 OK
cover ('tcnf', 5, 6, 3) cubes 32 of 32 OK
cover ('tcnf', 5, 4, 2) cubes 32 of 32 OK
mcnf (4, 6) clause counts ['1577060']
mcnf (5, 7) clause counts ['14696677']
mcnf (5, 8) clause counts ['16793861']
control B64/S1 (masks) height 2 up to width 6: first orphan width 2, expected 2
control B17/S1 (masks) height 2 up to width 6: first orphan width 5, expected 5
control B64/S4 (masks) height 2 up to width 7: first orphan width 6, expected 6
control B8/S0 (masks) height 2 up to width 7: first orphan width 6, expected 6
control B8/S12 (masks) height 2 up to width 8: first orphan width None, expected None
control B8/S12 (masks) height 3 up to width 5: first orphan width None, expected None
verify.py OK
PASS
```
