# Run it yourself

From this folder, in a fresh shell (python3 only, standard library, no network):

    sh verify-it-yourself/run_checks.sh

It joins `object/u.part1.txt` and `object/u.part2.txt` into u.txt (the 1 MB per-file limit forced the split), prints
the sha256 of u.txt, v.txt and w.txt, and runs two checkers. Expected output (a real run is in
verify-it-yourself/RECEIPTS.md), about 45 seconds on a laptop:

```
47419363a41b203879fe8ae93035fe231852f01eb3081ad15c306a91d1e3298a u.txt
dbf5c154ad97f11abdefd3d7d9ff1fda723a49710e881124bc547299308a93fa v.txt
797187bb905b8ee0dd22f321b802a1009938e2b4905517c1ffa7c576749bfacb w.txt
== exact Brent-equation check (check_scheme.py)
format <18,19,19>, 3424 terms, every term with three nonzero factors, common denominator 352800, 42224004 Brent equations checked, 0 wrong
rank 3424 scheme for <18,19,19> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 342 entries of C differ from AB
trial 2: 0 of 342 entries of C differ from AB
trial 3: 0 of 342 entries of C differ from AB
PASS
PASS
```

File format: each factor file has the header lines `# format 18 19 19` and `# rank 3424`, then one line per term
k = 0..3423 with the nonzero entries `index:coefficient` (integer or p/q). Convention: for A 18x19 and B 19x19,
m_k = (sum u_k[i*19+j] A[i][j]) * (sum v_k[j*19+l] B[j][l]) and C[i][l] = sum_k w_k[i*19+l] m_k.

The 352800 printed as "common denominator" is the checker's scaling factor (the lcm over terms of the product of
each term's three factor denominators), not the least common denominator of the coefficients (8400 for U, 84 for V
and W).

`check_scheme.py` clears denominators and expands every term exactly, so all 342 * 361 * 342 = 42,224,004 Brent
equations are checked; `check_random_eval.py` is an extra spot check (exact rational A and B).

To rebuild the object from LITA's published 19x19x19 rank-3633 scheme (numpy and python-flint), follow
how-we-built-it/COMMANDS.md; the rebuild prints `rank 3425`, then `absorbed 1 -> rank 3424`, then SAME.
