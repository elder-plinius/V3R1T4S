# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 -I verify-it-yourself/check_fmm_fast.py object/11x14x16_m1547_ZT.json --expect-rank 1547 --expect-class ZT
```

It reads the scheme, reports the largest absolute coefficient and the class (ZT means every coefficient is -1, 0 or 1), and checks every Brent equation exactly in integer arithmetic (the method is stated in the checker's header). Index convention: for format n1 x n2 x n3, `u[i*n2+j]` is the coefficient of A[i][j], `v[j*n3+l]` of B[j][l], `w[l*n1+i]` of C[i][l].

## The encoding

`object/11x14x16_m1547_ZT.json` is stored as `"encoding": "sparse_flat_pairs"` (rows are `[index, value, index, value, ...]` into the dense row; `n` and `m` are kept). To get the dense file and compare it with the original that the panel checked (sha256 `2a7d22e9c0e1881aeedfe29f53a8d2423673ca7dbf827f4eece7a598d2a93da7`; the original is not shipped because of the size limit):

```sh
python3 -I verify-it-yourself/convert_sparse.py to-dense object/11x14x16_m1547_ZT.json dense.json
sha256sum dense.json   # equals 2a7d22e9c0e1881aeedfe29f53a8d2423673ca7dbf827f4eece7a598d2a93da7
```

The dense output is the original's exact bytes (the conversion writes compact JSON in the original key order). `python3 -I verify-it-yourself/convert_sparse.py compare A.json B.json` compares two scheme files entry by entry in either encoding.

## 2. Rebuild the object

`how-we-built-it/README.md` names the parent file (URL and sha256), the base schemes and the script. The construction was not rerun while packaging, no run log exists and the agent's verifier is not included, so a rebuild is a reconstruction, not a recorded recipe.
