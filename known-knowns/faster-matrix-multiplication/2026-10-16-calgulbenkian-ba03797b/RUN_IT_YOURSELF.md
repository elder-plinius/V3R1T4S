# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: the object's sha256 matches INDEX.csv; `check_slp.py` prints a JSON line with `"VALID": true`,
`"adds_total": 169` and `"tensor_exact": "C^T"`; a copy with one coefficient flipped is rejected; last line `ALL CHECKS PASS`.

The checker alone:

```sh
python3 verify-it-yourself/check_slp.py object/2x4x7_m45_cr169_ZT_reduced.json
```

It expands every form of the program over Z, checks that every expanded intermediate and output has coefficients in
-1, 0, 1, checks the full tensor identity of the 45 products against the 2x4x7 matrix multiplication tensor
(outputs in the C-transposed layout Perminov uses: output k*n+i is C[i][k]), evaluates the program on random integer
matrices, and counts the additions under the reduced convention. With sympy installed:

```sh
python3 verify-it-yourself/sym_check.py object/2x4x7_m45_cr169_ZT_reduced.json
```

To recount the reference, download Perminov's file named in `the-record-we-beat/README.md` and run `check_slp.py` on it;
it reports 174.

Rebuilding the object means rerunning the randomized search in `how-we-built-it/` (compile the C programs with
`cc -O2`, then follow `COMMANDS.md` or `SEARCH_REPORT.md`); runs differ by seed, so a rerun gives a program of similar
cost, not this exact file.
