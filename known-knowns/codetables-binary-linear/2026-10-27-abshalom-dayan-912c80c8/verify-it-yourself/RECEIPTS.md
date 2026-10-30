
# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run on 2026-10-27 from a read-only copy of this package folder
(copied, then chmod -R a-w; the script keeps its scratch files in a temporary folder outside the package and removes it
on exit), with the date, platform, compiler and Python version printed before it and the timing after it:

```
2026-10-27T20:41:20Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
claimed n=29 k=19 d=8; computed rank(G)=19
k=19 n=29 rank=19
W=1: no nonzero codeword of weight <= 1 (all 29 subsets)
W=2: no nonzero codeword of weight <= 2 (all 406 subsets)
W=3: no nonzero codeword of weight <= 3 (all 3654 subsets)
W=4: no nonzero codeword of weight <= 4 (all 23751 subsets)
W=5: no nonzero codeword of weight <= 5 (all 118755 subsets)
W=6: no nonzero codeword of weight <= 6 (all 475020 subsets)
W=7: no nonzero codeword of weight <= 7 (all 1560780 subsets)
W=8 complete for all W'<8; first nonzero codeword supported in a 8-set after 253 subsets
d=8 witness_weight=8 witness=2 2 2 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
m3_mindist: W=7: no nonzero codeword of weight <= 7 (all 1560780 subsets); d=8
witness: weight 8, nonzero codeword of the row space: True
computed n=29 k=19 d=8; claimed n=29 k=19 d=8
PASS
real 0.95
user 0.38
sys 0.25
```
