# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = 7c6a8a80df2a86665a9af3715802976054a9223efa6181be86d745d1264299c6
N = 163
half min pair distance = 0.21713800790564662267198811760796925587706949908556 (pair 134, 143)
1 - max norm = 0.21713800642461929882694315132625607157010627576977
r* = 0.21713800642461929882694315132625607157010627576977
table = 0.217115168538
gain = 0.00002283788661929882694315132625607157010627576977
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
