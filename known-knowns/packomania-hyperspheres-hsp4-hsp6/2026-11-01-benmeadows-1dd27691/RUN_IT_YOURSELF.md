# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = 1dd2769172958fa1083d9614660de9dfb4e262f6235d897100991024b4839e8c
N = 213
half min pair distance = 0.20405661952173256609552697629056316349631247455091 (pair 75, 161)
1 - max norm = 0.20405661952173254773567268004122093725499478795627
r* = 0.20405661952173254773567268004122093725499478795627
table = 0.204053178162
gain = 0.00000344135973254773567268004122093725499478795627
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
