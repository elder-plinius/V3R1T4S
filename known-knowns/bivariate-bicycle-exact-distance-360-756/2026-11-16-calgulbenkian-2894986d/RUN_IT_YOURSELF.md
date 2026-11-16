# Run It Yourself (`bivariate-bicycle-exact-distance-360-756` `p1`, `n = 504`)

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Code parameters: n=504 (l=42, m=6), rank(H_X)=246, rank(H_Z)=246, k=12
Witness file: object/bb504_logical_wt28.txt
Support size (Hamming weight): 28 (left=12, right=16)
CSS commutativity H_X * H_Z^T = 0: OK
Syndrome H_X * u = 0 (mod 2): OK
Logical non-triviality rank([H_Z; u]) = 247 > 246: OK
Dual X-logical weight = 28, H_Z * v_X = 0, rank([H_X; v_X]) = 247 > 246: OK
PASS
```
