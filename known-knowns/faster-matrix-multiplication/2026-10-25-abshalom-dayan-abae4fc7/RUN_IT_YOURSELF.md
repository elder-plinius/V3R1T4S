# Run it yourself

From this folder, in a fresh shell (python3 only, standard library, no network):

    sh verify-it-yourself/run_checks.sh

It joins `object/u.part1.txt` + `object/u.part2.txt` into u.txt and `object/v.part1.txt` + `object/v.part2.txt` into
v.txt (the 1 MB per-file limit forced the splits), checks the sha256 of u.txt, v.txt and w.txt against the files the panel checked (FAIL on
any other file), and runs two checkers (about 1.4 GB peak memory). Expected output (a real run is in verify-it-yourself/RECEIPTS.md); it took 5 min 27 s on a shared laptop at
low priority (about 4 minutes unshared):

```
abae4fc7429a9c3b715405717c52e2dfcd36ab0f41cd137f3e1327252b1ff56e u.txt matches
a05bcf35e2018bde9600457e4776483969b8b6c0de6c3a1463847f8ca3ae08bb v.txt matches
041992e80c316daa766acecffae71c0c7839fa5f189c77365109f2e63fe7c32d w.txt matches
== exact Brent-equation check (check_scheme.py)
format <14,14,15>, 1709 terms, every term with three nonzero factors, common denominator 2121600, 8643600 Brent equations checked, 0 wrong
rank 1709 scheme for <14,14,15> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 210 entries of C differ from AB
trial 2: 0 of 210 entries of C differ from AB
trial 3: 0 of 210 entries of C differ from AB
PASS
PASS
```

File format: each factor file has the header lines `# format 14 14 15` and `# rank 1709` (plus a comment line with
the convention), then one line per term k = 0..1708 with the nonzero entries `index:coefficient` (integer or p/q).
Convention: for A 14x14 and B 14x15, m_k = (sum u_k[i*14+j] A[i][j]) * (sum v_k[j*15+l] B[j][l]) and
C[i][l] = sum_k w_k[i*15+l] m_k.

`check_scheme.py` clears denominators and expands every term exactly, so all 196 * 210 * 210 = 8,643,600 Brent
equations are checked; `check_random_eval.py` is an extra spot check (exact rational A and B).

To rebuild the object from LITA's published 15x15x15 rank-1977 scheme (numpy and python-flint), follow
how-we-built-it/COMMANDS.md; the rebuild prints `parent <15,15,15> rank 1977`, `... -> rank 1865`, `removed 29 ->
rank 1836`, `... -> rank 1731`, `removed 22 -> rank 1709`, and the comparison prints SAME.
