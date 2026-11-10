# RECEIPTS

Real output of `sh verify-it-yourself/run_checks.sh` run from this package folder (staging copy, same files), started 2026-11-09T08:59:15Z, PYTHON set to a python-flint 0.9.0 interpreter; the interpreter path line is shown as <python>.

```
using: <python>
tables 8.7s
residual: head [1.4041e-842 +/- 3.38e-847] tail [2.3711e-1271 +/- 3.40e-1276] eta [2.7644e-843 +/- 4.18e-848]  (63.6s)
eps: a [1.64e-7 +/- 1.82e-10]  b_rows [0.000147 +/- 2.92e-7]  b_tail [4.34e-51 +/- 2.37e-54]  total [0.000147 +/- 4.56e-7]  (65.2s)
A_K: 1 eigenvalues in Gamma_2, 2 with |z|>rho: ['[1.00000000000 +/- 3e-17] + [+/- 7.85e-639]j', '[-0.303663002899 +/- 2.68e-13] + [+/- 7.85e-639]j']
resolvent: M_K(G2) [160.7 +/- 0.0380]  M_K(rho) [55.70 +/- 2.56e-3]  gains [0.0237 +/- 9.57e-6] [0.00821 +/- 2.88e-6] (152.2s)
RESULT: |lambda - mu| <= [4.5490e-843 +/- 4.25e-848]  ->  D = 842 certified decimals; isolation/counting ok = True
certified: |lambda_2 - mu| <= [4.54904e-843 +/- 2.41e-849], D = 842; endpoints match object/C83_enclosure.txt; Nisoli centre agrees
PASS
rc=0
2026-11-09T09:01:48Z
```
