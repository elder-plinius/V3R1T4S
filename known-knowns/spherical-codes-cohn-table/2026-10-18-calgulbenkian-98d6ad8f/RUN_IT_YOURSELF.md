# Run it yourself

Needs python3 (3.8 or later), standard library only, and curl. From this package folder, fetch the two table pages yourself, then run the checks against them:

```sh
curl -s -o plain.csv https://spherical-codes.org/plain
curl -s -o index.html https://spherical-codes.org/          # about 4.6 MB
sh verify-it-yourself/run_checks.sh plain.csv index.html
```

Expected: one `sha256 ok` line per object, then one line per object of the form
`(d,N) c*=... table=... gain=... star=False needs_opt=False ref=... index_cos=... OK`, then the assertion line, and last `ALL CHECKS PASS`.

The checker alone:

```sh
python3 -I verify-it-yourself/check_sc.py index.html plain.csv object/*.txt
```

**What it does.** For each object file it reads N points in R^d, normalises each to unit length at 50 significant digits, computes every pairwise inner product (all N(N-1)/2 pairs, no sampling), and takes the maximum c*. It subtracts c* from the table's 12-decimal cosine in your copy of `/plain` (the gain must be at least 1e-10), and reads the row in your copy of the index for a proven-optimal mark and for the text "needs more optimization" (both must be absent for a full claim).

The sha256 values of the pages as compared are in `the-record-we-beat/README.md`. The table is maintained, so a later fetch can differ; the check then compares with the row as it is when you fetch it.

**Rebuilding the object.** The solver is `how-we-built-it/sc_opt.c` (`cc -O3 -o sc_opt sc_opt.c -lm`). The exact commands and seeds that produced the shipped files were not recorded; see `how-we-built-it/README.md`. The shipped object files are the artefact being claimed.
