# How we built it

- search/: warm defect-kick Metropolis basin hopping (hunt.py, T = 2e-3, about 200 hops per chain, 8 workers), seeded from the posted CCD Riesz s=1 N = 1382 file, with a float64 L-BFGS polisher (fastpol.py, Numba) and deep.py (long float64 gradient descent to max gradient < 1e-10). thomson_check.py parses table pages. Typical commands, run from search/ with the table page saved as riesz.html and the seed file in data/:
  `python3 hunt.py --table riesz.html --data data ...` (see `python3 hunt.py -h` for the job options), then `python3 deep.py best_1382_fine.txt cand_1382_deep.txt`.
  Requirements: numpy, scipy, numba.
- cand_1382_deep.txt: the float64 search output (the object before high-precision repair).
- certify/: hp.py (MPFR 170-bit tangent Newton, mpmath dps-30 energy, Weyl-bounded Hessian certificate), fastpol.py, ptload.py. Requirements: numpy, scipy, numba, mpmath, gmpy2.
  `python3 certify/hp.py cand_1382_deep.txt cand_1382 --prepolish --hessian` produced object/cand_1382.txt.
- expected/: the JSON records of the certificate runs (object and both posted files).
- PREREG.md, PREREG.v2.md: this run's pre-registration (statistic, checker, thresholds), frozen before the hunt. PREREG.run-0716.md: the pre-registration of the earlier run whose search found the basin.
- null_test.md is not needed: the claim is one explicit configuration checked deterministically against table values.
