# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder at 2026-11-07T22:17:17Z (Python 3.14.7):

```text
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 56350, p = 1024048960667, Fermat quotient q_p(b) mod p = 0
PASS
```

exit status: 0
