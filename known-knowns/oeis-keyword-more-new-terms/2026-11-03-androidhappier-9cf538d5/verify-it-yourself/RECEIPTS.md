# Receipts: real output of verify-it-yourself/run_checks.sh

Run from the package folder on 2026-11-03T18:13:08Z (UTC), python3 3.13.5, cc = cc (Debian 14.2.0-19) 14.2.0. Exit status 0.

```
== 1. sha256 of object/VALUE.txt
got  9cf538d5a41058aa72a6ce79df5852e594cd1d0c0ff8c68b3354332ec38125c5
want 9cf538d5a41058aa72a6ce79df5852e594cd1d0c0ff8c68b3354332ec38125c5
sha256: match
== 2. independent exhaustive count from the definition (n = 1..21)
object claims A325786(21) = 93725
1 1
2 1
3 2
4 2
5 4
6 7
7 12
8 19
9 41
10 71
11 141
12 255
13 509
14 924
15 1882
16 3395
17 6838
18 12715
19 25233
20 47049
21 93725
a(1..20) equal OEIS DATA
computed a(21) = 93725
PASS
== 3. negative control: no necklace test
no-necklace control a(1..9): [1, 1, 3, 4, 11, 22, 48, 88, 207]
control differs from DATA: True
FAIL
control: differs from DATA as expected
== 4. Program A (C) for n = 1..21
pA 1 21 identical to the checker's a(1..21): 21 93725
summary: A325786(21) = 93725
PASS
```
