# How the object was built

Input: the code posted for (6, 256) on the table by Pavlos Moros (2026), https://spherical-codes.org/data/6/256
(fetched 2026-10-24T17:37:11Z, HTTP 200, sha256 c5866a15cdabfe6f593fd878d690a9339d502f9720a7122f39d594a60b27992b,
and again 2026-10-25T05:52:42Z with the same sha256; not included here, it is the table's file). Python 3.14.7 with
requirements.txt; one core (`OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1`). Two steps, both in
the run that made the object; each line gives the program's own summary line.

```sh
# 1. exact-objective SLP with HiGHS (scipy.optimize.linprog, method="highs", which picks the HiGHS simplex or interior-point solver itself), 45 s budget (a sweep over 371 posted codes)
python3 slp_polish.py 6_256.txt 6 256 0.704931969352 slp_6_256.txt 45
#    25 steps, max cosine 0.7049319693516107 -> 0.7049204633911365 (gain 1.151e-05)
# 2. the same program from step 1's result, 600 s budget (a deep queue of the six largest sweep gains)
python3 slp_polish.py slp_6_256.txt 6 256 0.704931969352 code_6_256.txt 600
#    138 steps in 218 s, -> 0.7048987224974411 (gain 3.325e-05); stopped because the trust radius fell
#    below 1e-15 (2.8e-12 at the last logged step, max cosine changing by 4e-16 over the last 10 steps)
```

slp_polish.py does sequential linear programming on the exact objective: at each step it takes the pairs whose
cosine is within 4*rad of the current maximum, moves every point in its tangent space by rad*y with |y|_inf <= 1,
linearises the normalised inner products and minimises their common upper bound with HiGHS
(scipy.optimize.linprog); a step is kept only if the true maximum cosine drops, otherwise rad shrinks by 3. It
stops when rad falls below 1e-15 or the time budget runs out. HiGHS timing changes the step count, so a rebuild
lands near, not exactly on, object/code_6_256.txt; the saved file is the claim (its sha256 equals the step-2 output
of the run that made the object). Two wording notes on files kept as they were run: PREREG.md's "interior-point SLP polish" is this same program, and slp_polish.py's docstring says "25 significant digits" while its %.25e format writes 26 (as in object/code_6_256.txt).

PREREG_seed_run.md is the preregistration of the run that made both steps (frozen 2026-10-24T16:47:45Z), and
PREREG.md that of this run, which froze the object unchanged and claimed it (frozen 2026-10-25T05:54:46Z).
