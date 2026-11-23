# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. It takes seconds. The checker alone:

```sh
python3 verify-it-yourself/check_stabilizer.py object/new_optimal_stabilizer_codes_r11_d4.json 47 36 the-record-we-beat/cell_47_36_excerpt.txt
```

Expected last line: `RESULT PASS [[47,36,4]] live [3,4]`.

The object file holds six codes (n = 37, 39, 43, 45, 47, 49; k = n - 11), one for each of six packages. The checker selects the code with n = 47 and k = 36. What it computes, with exact integer bit arithmetic and no sampling: the 11 generators pairwise commute under the symplectic product; their GF(2) rank is 11 = n - k; the Pauli strings in the file agree with the binary rows; no Pauli of weight 1, 2 or 3 commutes with every generator (done twice, by a syndrome table and by direct commutation against the strings), so the normalizer has no nonidentity element of weight 3 or less and the distance is at least 4; and a weight-4 element of the normalizer outside the stabilizer span exists, so the distance is exactly 4. It then compares with the saved cell excerpt: lower bound below 4 and 4 at most the upper bound. A negative control (one flipped bit) must be rejected.

How to rebuild the object: the construction code is not part of this package (see how-we-built-it/README.md). The object is the data; the checker above needs nothing else.
