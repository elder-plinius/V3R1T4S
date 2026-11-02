# Run it yourself

Needs python3 (3.8 or later), standard library only. From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: one `sha256 ok` line per object, then one line per object of the form
`(d,N) c*=... table=... gain=... star=False needs_opt=False ref=... index_cos=... OK`, then the assertion line, and last `ALL CHECKS PASS`.

The checker alone:

```sh
python3 -I verify-it-yourself/check_sc.py the-record-we-beat/index_rows.html the-record-we-beat/plain_rows.csv object/*.txt
```

**What it does.** For each object file it reads N points in R^d, normalises each to unit length at 50 significant digits, computes every pairwise inner product (all N(N-1)/2 pairs, no sampling), and takes the maximum c*. It subtracts c* from the table's 12-decimal cosine in `the-record-we-beat/plain_rows.csv` (the gain must be at least 1e-10), and reads the saved index row for a proven-optimal mark and for the text "needs more optimization" (both must be absent for a full claim).

**Against the live table instead of the saved rows.** Fetch https://spherical-codes.org/plain and https://spherical-codes.org/ yourself, one plain request each, and pass those two files in place of the two files in `the-record-we-beat/` (the checker reads the same formats; the index file is large, about 4.7 MB).

**Rebuilding the object.** The solver is `how-we-built-it/sc_opt.c` (`cc -O3 -o sc_opt sc_opt.c -lm`). The exact commands and seeds that produced the shipped files were not recorded; see `how-we-built-it/README.md`. The shipped object files are the artefact being claimed.
