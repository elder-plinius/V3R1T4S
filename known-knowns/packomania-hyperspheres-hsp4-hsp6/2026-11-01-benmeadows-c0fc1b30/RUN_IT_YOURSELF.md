# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = c0fc1b302af41f2cd3b2fe423c866d95d9695c4dc46705a49b55113d2694dc67
N = 214
half min pair distance = 0.20388671005401594317423175513280102983896454012892 (pair 123, 187)
1 - max norm = 0.20388671005401599825192964920919393091388638296591
r* = 0.20388671005401594317423175513280102983896454012892
table = 0.203884464476
gain = 0.00000224557801594317423175513280102983896454012892
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
