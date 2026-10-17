# Receipts: real output of verify-it-yourself/run_checks.sh

Run from a clean copy of this package on a 4-core Linux server (Python 3 with sympy 1.14.0, gcc), 2026-10-17:

```
symbolic proofs: 7 of 7 PROVED
all controls rejected: True
parser test pass: True
all real pass: True
all mutants caught: True
BB(5) champion: 47176869 defined transitions, then halt
TOTAL scheduled=8365935 passed=8365935 failures=0
replay controls (steps+1, flipped bit): passed=0, passed=0
PASS
```

Wall time: 0m48.667s. Exit code 0.

Same script on a copy with one digit of object/rules.json changed (byte 940, inside the even_drain rule): last line FAIL, exit code 1 ('symbolic proofs: 6 of 7 PROVED', 'all real pass: False').
