# Run it yourself

From this package folder:

```
sh verify-it-yourself/run_checks.sh
```

Last line must be PASS. That re-simulates the blank grid and every listed seed
(k=1..6) with the standalone Python checker and checks the object SHA-256.

To re-run the exhaustive searches (hours of CPU):

```
# A (one of 84 pieces; TMAX=140):
cc -O3 -o hsearch how-we-built-it/code/hsearch/hsearch.c
./hsearch LLRL 6 140 84 <piece>

# B (one of 400 pieces; T=139):
cc -O3 -o lcb how-we-built-it/code/lcone4/lcb_fast.c
LCB_SPLITD=60 ./lcb LLRL 6 139 400 <piece>
```

Merge rules and expected digests are in how-we-built-it/METHOD.md and
how-we-built-it/data/audit/COVERAGE_AUDIT.md.
