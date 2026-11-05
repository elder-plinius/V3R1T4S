The shipped object is object/651.txt. The checker does not need a rebuild.

The search that produced it:

1. The warm start is a LogSumExp polish of the table's posted coordinates for (25, 651), already on disk from the 2026-10-22 run. That file had float64 maximum 0.24269127947873631.
2. From that point set, run continue_beta.py, which takes three further L-BFGS steps at inverse temperatures 1e7 (250 iterations), 3e7 (200) and 1e8 (120). kernel.py is the surrogate. Set one BLAS thread.
3. continue_beta.py writes continue_651.txt when the hard maximum drops by at least 1e-12. On this run only the beta 1e8 step dropped the float64 maximum, by 2.571617e-8, to 0.24269125376256218. That file, printed to 20 digits in scientific notation, is object/651.txt.
4. Score it with checker.py at mpmath precision 50 against the live cosine 0.245484258816. The accept rule was frozen in PREREG.md, and the object line was replaced by PREREG.v2.md before this file was scored.

Rebuilding is not required for the check.
