# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder at 2026-11-07T20:49:14Z (Python 3.14.7):

```text
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 28860, p = 1017279755641, Fermat quotient q_p(b) mod p = 0
PASS
```

exit status: 0

Negative control, run on a scratch copy of this package: changing the last digit of p in object/pair.json (1 to 2),
or the last digit of b (0 to 1), makes the same script end with `FAIL` and exit status 1. The restored copy passes again.
