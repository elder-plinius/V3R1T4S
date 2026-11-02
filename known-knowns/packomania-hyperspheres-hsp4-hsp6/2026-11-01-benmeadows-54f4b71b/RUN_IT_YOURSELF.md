# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = 54f4b71bb63ae5ba84e04efa6555129c96d9d1d72f79a3c05c4fc24c98c0f1d3
N = 141
half min pair distance = 0.22405439466669082726689145543227317971281842763576 (pair 99, 125)
1 - max norm = 0.22405439455945332450808207248104094869170633838734
r* = 0.22405439455945332450808207248104094869170633838734
table = 0.224016561889
gain = 0.00003783267045332450808207248104094869170633838734
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
