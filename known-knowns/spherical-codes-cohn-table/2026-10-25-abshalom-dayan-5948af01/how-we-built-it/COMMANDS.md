# How the object was built

Input: the code posted for (6, 575) on the table by Pavlos Moros (2026), https://spherical-codes.org/data/6/575
(fetched once at 2026-10-24T17:41:05Z and again at 22:56:45Z, HTTP 200, byte-identical, sha256
a0b954a28ad0af6cc8ad9307c6239a0a5ee88e8facf7a0bf009ccd9082a33340; not included here, it is the table's file; its
lines are comma-separated). Python 3.14.7 with requirements.txt; one core
(`OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1`).

```sh
# 1-2. exact-objective SLP with HiGHS dual simplex (slp_polish.py; earlier run of the same workspace)
python3 slp_polish.py 6_575.txt 6 575 0.792780236785 slp_6_575.txt 45            # 3 steps, gain 4.351e-05
python3 slp_polish.py slp_6_575.txt 6 575 0.792780236785 deep_6_575.txt 600      # 33 steps, gain 6.667e-05, not converged
# 3. the same step with HiGHS interior point (slp_v2.py; this run): converged
python3 slp_v2.py deep_6_575.txt 6 575 0.792780236785 code_6_575.txt 1500 1e-4 1e-2 60 1e9 highs-ipm
#    242 steps, every LP solved, trust radius down to 5.8e-15, 722 s, gain 1.004e-04
```

Both programs do sequential linear programming on the exact objective: at each step they take the pairs whose
cosine is within 4*rad of the current maximum, move every point in its tangent space by rad*y with |y|_inf <= 1,
linearise the normalised inner products and minimise their common upper bound with HiGHS
(scipy.optimize.linprog); a step is kept only if the true maximum cosine drops, otherwise rad shrinks by 3.
slp_v2.py adds a start radius, a radius ceiling, an optional cap on the active window (off here: 1e9) and the
choice of HiGHS method; interior point solves the large LPs (about 2,800 active pairs) about 7 times faster per
step than dual simplex, which let step 3 run to convergence. HiGHS timing can change the step count, so a rebuild
lands near, not exactly on, object/code_6_575.txt; the saved file is the claim.

PREREG_seed_run.md is the preregistration of the earlier run that made steps 1 and 2 (frozen 2026-10-24T16:47:45Z).
PREREG.md is the preregistration of this run, which made step 3 and claimed the result (frozen
2026-10-24T22:59:33Z, before any measurement).
