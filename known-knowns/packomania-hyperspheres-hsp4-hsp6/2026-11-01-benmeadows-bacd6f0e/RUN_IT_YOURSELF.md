# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = bacd6f0e9c0c6e94c1b7a2afea1b4872922c1cdd2f69e69c07d06d35b9f5e968
N = 216
half min pair distance = 0.20362333097990603045221346248297173127882114674642 (pair 54, 75)
1 - max norm = 0.20362333097990599275220577366244339625411531997264
r* = 0.20362333097990599275220577366244339625411531997264
table = 0.203582040585
gain = 0.00004129039490599275220577366244339625411531997264
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
