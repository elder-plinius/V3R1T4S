# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from this folder on 2026-10-19 (builder run, python3 standard library only):

```
sha256 matches INDEX.csv (2de9ef5264ea4bbbe334bf590f12f5ce89cb8f8ce30a464b4112e55f66a2927f)
== check_stabilizer.py on [[91,73]]
code [[91,73]] r=18
generators pairwise commute: True
GF(2) rank of generators: 18 (need 18 = n-k = 18): True
Pauli strings agree with HX, HZ: True
errors of weight 0..2 enumerated: 37129; syndrome collisions: method A 0, method B 0
pure distance >= 5: True
weight-5 element of N(S) outside span(S) (logical of weight 5, so d = 5 and d = 6 excluded): XYXIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIZZIIIIIIIIIIIIIIIII  verified: True
live codetables.de cell: lower bound 4, upper bound 6; d = 5; strictly above lower and within upper: True
RESULT PASS [[91,73,5]] live [4,6]
== negative control: a copy with one bit of the first X row flipped must FAIL
negative control rejected as expected: RESULT FAIL [[91,73,None]] live [4,6]
ALL CHECKS PASS
```
