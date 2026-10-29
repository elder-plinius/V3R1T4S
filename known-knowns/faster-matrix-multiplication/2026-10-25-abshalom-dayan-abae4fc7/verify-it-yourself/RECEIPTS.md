# RECEIPTS: real output of sh verify-it-yourself/run_checks.sh

Note added at filing: this run was recorded before run_checks.sh compared the sha256 values; the script now prints "matches" after each of the three hash lines and stops with FAIL on a mismatch.

run from a clean copy of this package on 2026-10-25 (start 10:21:33Z, end 10:27:01Z, UTC), 5 min 27 s wall clock
(270 s of CPU) on a laptop (Apple M4 Pro, Python 3.14) while it was shared with other jobs and run at low priority
(`nice -n 10`); an earlier run of the same checkers on the unshared machine took 3 min 55 s

```
abae4fc7429a9c3b715405717c52e2dfcd36ab0f41cd137f3e1327252b1ff56e u.txt
a05bcf35e2018bde9600457e4776483969b8b6c0de6c3a1463847f8ca3ae08bb v.txt
041992e80c316daa766acecffae71c0c7839fa5f189c77365109f2e63fe7c32d w.txt
== exact Brent-equation check (check_scheme.py)
format <14,14,15>, 1709 terms, every term with three nonzero factors, common denominator 2121600, 8643600 Brent equations checked, 0 wrong
rank 1709 scheme for <14,14,15> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 210 entries of C differ from AB
trial 2: 0 of 210 entries of C differ from AB
trial 3: 0 of 210 entries of C differ from AB
PASS
PASS
```
