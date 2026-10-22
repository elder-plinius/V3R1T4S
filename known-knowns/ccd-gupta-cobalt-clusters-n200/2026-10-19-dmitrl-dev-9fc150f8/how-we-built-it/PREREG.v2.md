# PREREG.v2 (changed plan after part A; the original PREREG.md is unchanged)

## Addendum A1 (written 2026-10-19T04:00:23Z, after part A, before any part-B run)
Part A results (audit_table.csv):
- Cleri-Rosato cobalt parameters (A 0.0950, xi 1.4880, p 11.604, q 2.286, reduced units r/r0) reproduce all ten Co.zip
  energies (Co/Energy.txt, 6 decimals) to < 5e-7 eV: PASS of the Co.zip half of the calibration rule.
- The table half as written ("posted energies of the 10 sampled files to 1e-6 eV") FAILS on the files as posted: max
  2.19e-5 eV on the sample (2.94e-5 eV at N = 175 over all 199; 115 files > 1e-6, 8 > 1e-5). The posted coordinates are
  not stationary points (gradient norms 2e-3..2.2e-2, median 6.7e-3); they carry 6 decimals.
- After L-BFGS polishing every table energy is reproduced: median |d| 2.0e-8 eV, max 1.11e-6 eV (N = 102, polished
  lower); sample max 4.1e-8 eV. No posted structure polishes lower by more than 1e-4 eV.
CHANGE MADE AFTER SEEING THE RESULT (recorded as such): the parameter set is accepted for part B on the Co.zip match plus
the polished-table match (both pass). The as-is failure is reported as an audit finding, not hidden. Part B's validity
depends only on the parameter set, which the Co.zip files pin; this change does not touch any part-B criterion.
Part B plan (unchanged rules): reference E_best(N) = min(table, Co.zip). First pass = neighbour seeding (remove one
atom from the best N+1 structure; add one atom above each convex-hull facet of the best N-1 structure; relax all),
cascading to N +- 1 on any gain; sizes ordered: neighbours of the ten Co.zip sizes, then N = 200 down to 80, then the rest.
