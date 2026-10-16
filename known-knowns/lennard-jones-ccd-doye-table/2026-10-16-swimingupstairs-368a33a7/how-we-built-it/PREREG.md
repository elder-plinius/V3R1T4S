# PREREG frozen 2026-10-15T21:22:41Z (before any attack output)
target: lennard-jones-ccd-doye-table, N in 562..1000 (excluding 664 and 813 unless Barron's value is beaten)
criterion: verbatim in target.md.
statistic: E of the L-BFGS-polished configuration (checker/lj_lib.py); candidates recomputed in mpmath 30 dp.
threshold: main: E_polished < table(N) - 1e-5, distinct basin (polished table file minus candidate >= 1e-5), Hessian 6 zero modes and none negative.
 p3 audit: |E_polished(table file) - table(N)| > 1e-5 flags a row (either direction) for a second, tighter polish before any mention.
null_test: not needed because every claim would be an explicit configuration checked by a deterministic energy checker against a table value.
lenses: auditor (p3, all 439 files), relaxer (surface basin hopping), swimmer (FIRE + flow moves), constructor (grow/shrink from N +- 1 sweeps).
