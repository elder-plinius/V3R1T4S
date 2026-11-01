# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = fe3ab96bf8a15a69dce5665ad60f28d88aa23ccb85c1239f2761375074d6e394
N = 160
half min pair distance = 0.21857935361515588853679380518513370498615336585768 (pair 7, 103)
1 - max norm = 0.21857935352324099278067051097225436236904613091590
r* = 0.21857935352324099278067051097225436236904613091590
table = 0.218358476129
gain = 0.00022087739424099278067051097225436236904613091590
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
