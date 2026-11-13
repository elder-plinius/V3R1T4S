# Receipts

Command (from the package folder): `sh verify-it-yourself/run_checks.sh` (online: fetches the pinned hub files)
Run at 2026-11-13T02:25:09Z (date -u), Python 3.11.15 with pyarrow 26.0.1.

```
scored tasks 3065 over 14 reference dates
season-average WIS ours 72.2386 hub-ensemble 99.7021 relative -0.2755
stationary bootstrap (mean block 3, 4000 resamples) 90% interval [-0.3609, -0.2001]
criterion: rel <= -0.03 and interval below 0 -> True
PASS
```
