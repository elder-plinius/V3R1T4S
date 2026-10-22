# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 -I verify-it-yourself/check_fmm_fast.py object/9x11x14_m889_Z.json --expect-rank 889 --expect-class Z
```

It reads the scheme, reports the largest absolute coefficient and the class (ZT means every coefficient is -1, 0 or 1), and checks every Brent equation exactly in integer arithmetic (the method is stated in the checker's header). Index convention: for format n1 x n2 x n3, `u[i*n2+j]` is the coefficient of A[i][j], `v[j*n3+l]` of B[j][l], `w[l*n1+i]` of C[i][l].

## 2. Rebuild the object

Not possible from this package: the search code that produced this scheme is not in the snapshot (`how-we-built-it/README.md` says what is included).
