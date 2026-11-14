# How we found it (contributor text, unverified)

**Brief.** Bank target minlplib-finance-open-instances, partial win p1 on pricing050: a machine-checkable certificate that the optimum is at most the best known primal plus 1e-6*|value|. MINLPLib still listed a large dual gap (bestdual about -1153, SCIP about -1534) against primal -1813.829078.

**What failed.** Multistart SLSQP plus high-precision KKT polish of the posted primal found no better feasible point. Float dual searches with crude grids left a dual gap of order 1e-3 or worse. A first interval branch-and-bound with loose tolerances certified only down to about -1813.82, short of the 1e-6 relative bar.

**What worked.** A short float dual search fixed nonnegative multipliers with only e5 and e6 active (lambda = (0, 0, 0, 3.04890112, 2.16775096)). Reading the posted GAMS decimals as exact decimals, an Arb-ball separable branch-and-bound on each of the 50 univariate pieces produced a deterministic 1958-leaf covering of [0,10] whose reassembled dual upper bound is -1813.829075713452, inside the bar -1813.827264171. An independent mpmath.iv path also passed. Concavity of the three univariate term types was checked as the bank's optional illustration (i); the confirmed object is the dual leaf log.
