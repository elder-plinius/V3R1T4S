# Receipts: real output of verify-it-yourself/run_checks.sh

Run from the package folder on 2026-11-03T19:18:50Z (UTC), python3 3.13.5, cc = cc (Debian 14.2.0-19) 14.2.0. Exit status 0.

```
== 1. sha256 of object/VALUE.txt
got  1726275264dcaacd920d82809a0363b4c5b93c894297cf7f8d2166e9a80350bc
want 1726275264dcaacd920d82809a0363b4c5b93c894297cf7f8d2166e9a80350bc
sha256: match
== 2. independent exhaustive count from the definition (n = 0..11)
object claims A326335(11) = 61987
0 1
1 1
2 1
3 1
4 2
5 6
6 21
7 86
8 394
9 1974
10 10696
11 61987
a(0..10) equal OEIS DATA
computed a(11) = 61987
PASS
== 3. negative control: nesting on any pairs
any-pairs control a(0..9): [1, 1, 1, 1, 2, 7, 24, 100, 458, 2279]
control reproduces DATA: False
control: differs from DATA as expected
== 4. Program A (C) for n = 0..11
pA 0 11 A326335 column identical to the checker's a(0..11): 11 61987
summary: A326335(11) = 61987
PASS
```
