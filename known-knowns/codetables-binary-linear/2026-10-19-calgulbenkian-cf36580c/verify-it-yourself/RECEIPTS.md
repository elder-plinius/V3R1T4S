# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-19 (python3 standard library only):

```
sha256 matches INDEX.csv (3e9858a143b751d715399b3dc8248129a522c4d2628dfb3bc074f09c0930b9c0)
== check_stabilizer.py on [[45,34]]
code [[45,34]] r=11
generators pairwise commute: True
GF(2) rank of generators: 11 (need 11 = n-k = 11): True
Pauli strings agree with HX, HZ: True
weight 1..3 Paulis commuting with every generator: method A 0, method B 0
weight-4 element of N(S) outside span(S) (logical of weight 4): XXIIIYYIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII  verified: True
live codetables.de cell: lower bound 3, upper bound 4; d = 4; strictly above lower and within upper: True
RESULT PASS [[45,34,4]] live [3,4]
== negative control: a copy with one bit of the first X row flipped must FAIL
negative control rejected as expected: RESULT FAIL [[45,34,None]] live [3,4]
ALL CHECKS PASS
```
