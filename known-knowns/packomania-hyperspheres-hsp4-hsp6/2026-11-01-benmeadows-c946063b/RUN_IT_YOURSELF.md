# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = c946063bd7e626150c1b0ba69415fbd774a3519ff87470f73d55372119481d6d
N = 152
half min pair distance = 0.22097502706448427281871869298721922443651297250190 (pair 7, 88)
1 - max norm = 0.22097502706448416408815908921357097646062824532483
r* = 0.22097502706448416408815908921357097646062824532483
table = 0.220960306508
gain = 0.00001472055648416408815908921357097646062824532483
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
