# Run it yourself (fresh shell, from this folder)
1. Onsets of every minimiser: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (~1 s; needs python3).
2. Completeness, method 1 (fsearch, DFS over first reads with a 104-phase completion test):
   `cd how-we-built-it/fsearch && cc -O2 -o fsearch fsearch.c && ./fsearch 3 126` -> `RESULT K=3 best_t=126 minimisers=1 ...`
   and `./fsearch 3 125` -> `RESULT K=3 NONE t<=125 ...`. drive.sh runs the iterative deepening for every k
   (outputs as saved in k*.txt).
3. Completeness, method 2 (lcone, light-cone DFS with a turn-word test, written separately):
   `cd how-we-built-it/lcone && cc -O2 -o lcone lcone.c && ./lcone 3 126 1 0` (args K T workers worker-id; single worker) -> 0 violations at 125,
   1 minimiser at 126 (last line `DONE K=3 T=126 wid=0 leaves=40515 viol=0 mins=1`); drive2.sh "K T" runs 5 workers per k. RESULTS.md lists every k.
4. Geometry behind fsearch's far-cell bound: `python3 how-we-built-it/fsearch/dmin_radius.py` (matches dmin_radius.out).
Rebuild the object: object/minimisers.txt is lcone's all-minimiser output; TABLE.txt is the table above.
