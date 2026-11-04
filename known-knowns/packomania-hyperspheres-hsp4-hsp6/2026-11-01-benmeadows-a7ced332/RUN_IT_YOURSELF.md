# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = a7ced3321fa76c13cb6372501334593f81d9a0385864873726b3b9fb87483f3b
N = 156
half min pair distance = 0.22031378116345623392670442895924547274922886088440 (pair 81, 91)
1 - max norm = 0.22031376415231824838912701087369874594203899420566
r* = 0.22031376415231824838912701087369874594203899420566
table = 0.220308265077
gain = 0.00000549907531824838912701087369874594203899420566
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
