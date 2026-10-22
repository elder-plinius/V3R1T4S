# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 verify-it-yourself/check_stabilizer.py object/new_stabilizer_codes_d5.json 83 65 table-record/cell_83_65_excerpt.txt
```

Expected last line: `RESULT PASS [[83,65,5]] live [4,6]`. The object file holds ten codes (one per cell of the ten claim folders built from the same file); the checker selects the code with n = 83 and k = 65. It takes under a few seconds.

What it computes, with exact integer bit arithmetic and no sampling: the 18 generators pairwise commute under the symplectic product; their GF(2) rank is 18 = n - k; the Pauli strings in the file agree with the binary rows; all 1 + 3n + 9*C(n,2) Pauli errors of weight at most 2 (identity included) have pairwise distinct syndromes, done twice (method A from the binary rows, method B by direct commutation with the Pauli strings), so no nonidentity Pauli of weight 1 to 4 commutes with every generator and the pure distance is at least 5; a weight-5 element of the normalizer outside the stabilizer span exists, so d is exactly 5 and d = 6 is excluded. It then compares with the saved cell excerpt: lower bound below 5 and 5 at most the upper bound.

The first lines of run_checks.sh check every file in object/ against SHA256SUMS and print FAIL if one differs.

How to rebuild the object: the construction code is not part of this package (see how-we-built-it/README.md). The object is the data; the checker above needs nothing else.
