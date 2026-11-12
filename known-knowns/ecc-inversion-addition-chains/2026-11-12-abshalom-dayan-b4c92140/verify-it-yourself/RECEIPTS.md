# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-12 (macOS, Python 3, standard library only, no network):

```
exponent N - 2 = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f (256 bits)
every one of the 281 steps is a sum of two earlier elements; the last element equals N - 2
length 281 = 251 doublings + 30 additions
distinct elements: 282 of 282; strictly increasing: True
strictly shorter than the lowest public length on record, 282, by 1
x * x^E = 1 (mod N) for 100 nonzero x, following the chain step by step
CHECK: PASS
PASS
```
