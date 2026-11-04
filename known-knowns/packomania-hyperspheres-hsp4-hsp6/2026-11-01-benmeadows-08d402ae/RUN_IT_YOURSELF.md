# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = 08d402ae2020be2bab2b33b7f3dd9846efc5ff6e7fe71f8715d4071c74238687
N = 215
half min pair distance = 0.20376854965104974669091150455497906750028585866512 (pair 112, 172)
1 - max norm = 0.20376854965104970107115404162994178816907422394072
r* = 0.20376854965104970107115404162994178816907422394072
table = 0.203682998566
gain = 0.00008555108504970107115404162994178816907422394072
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
