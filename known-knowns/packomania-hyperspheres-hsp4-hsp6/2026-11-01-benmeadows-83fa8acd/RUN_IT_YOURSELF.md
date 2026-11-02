# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact):

```
object sha256 = 83fa8acd5de5de8364e39ad6593b2214a5bf50425f85e924d56cd68c8acea0bc
N = 217
half min pair distance = 0.20344247849929279773735751616553627691783349674803 (pair 15, 190)
1 - max norm = 0.20344247849929273721302003487040897978541806734019
r* = 0.20344247849929273721302003487040897978541806734019
table = 0.203438871092
gain = 0.00000360740729273721302003487040897978541806734019
gain >= 1e-10: True
PASS
```

## Rebuild the object (optional)

See how-we-built-it/COMMANDS.md and how-we-built-it/requirements.txt. The search is heuristic and seeded from the
clock, so a rerun finds a different packing; the checker above is what matters.
