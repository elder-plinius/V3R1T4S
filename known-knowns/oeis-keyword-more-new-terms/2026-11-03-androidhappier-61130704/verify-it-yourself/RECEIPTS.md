# Receipts: real output of `sh verify-it-yourself/run_checks.sh` (run 2026-11-03T17:45:01Z to 17:45:42Z, 41 s, box under load ~135)

```
== 1. object/VALUE.txt: hash vs INDEX.csv, and the claimed value
sha256 61130704e05eb2819cbd23604b090802da6409ae924ed4239a2658f992ec1a55 ok
claimed a(12) = 2092816
== 2. definition-level exhaustive count, n = 1..12 (Python, exact Fractions)
1 1
2 0
3 3
4 6
5 30
6 96
7 461
8 2000
9 10727
10 57092
11 342348
12 2092816
a(1..11) = OEIS DATA ok
a(12) = 2092816 = claim ok
== 3. Program A (C, restricted growth strings), if a C compiler is present
C output identical to the Python count ok
summary: A361864(12) = 2092816
PASS
```
