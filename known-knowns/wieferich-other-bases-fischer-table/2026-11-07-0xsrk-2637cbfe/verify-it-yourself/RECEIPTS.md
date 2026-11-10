# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder at 2026-11-07T22:55:27Z (Python 3.14.7):

```text
ok   3 <= b <= 10125
ok   b is not a perfect power
ok   p > 4.8e12 (the table's searched limit for bases 1053..10125)
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 5481, p = 4848813530161, Fermat quotient q_p(b) mod p = 0
PASS
```

exit status: 0
