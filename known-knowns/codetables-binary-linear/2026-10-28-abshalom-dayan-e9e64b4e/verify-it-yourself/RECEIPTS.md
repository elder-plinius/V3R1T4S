# Receipts

Output of `sh verify-it-yourself/run_checks.sh` from this package folder on 2026-10-28 (macOS, one core;
`/usr/bin/time -p` lines at the end):

```
claimed n=32 k=19 d=10; computed rank(G)=19
k=19 n=32 rank=19
W=1: no nonzero codeword of weight <= 1 (all 32 subsets)
W=2: no nonzero codeword of weight <= 2 (all 496 subsets)
W=3: no nonzero codeword of weight <= 3 (all 4960 subsets)
W=4: no nonzero codeword of weight <= 4 (all 35960 subsets)
W=5: no nonzero codeword of weight <= 5 (all 201376 subsets)
W=6: no nonzero codeword of weight <= 6 (all 906192 subsets)
W=7: no nonzero codeword of weight <= 7 (all 3365856 subsets)
W=8: no nonzero codeword of weight <= 8 (all 10518300 subsets)
W=9: no nonzero codeword of weight <= 9 (all 28048800 subsets)
W=10 complete for all W'<10; first nonzero codeword supported in a 10-set after 23 subsets
d=10 witness_weight=10 witness=1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
m3_mindist: W=9: no nonzero codeword of weight <= 9 (all 28048800 subsets); d=10
witness: weight 10, nonzero codeword of the row space: True
computed n=32 k=19 d=10; claimed n=32 k=19 d=10
PASS
real 8.06
user 7.34
sys 0.45
```
