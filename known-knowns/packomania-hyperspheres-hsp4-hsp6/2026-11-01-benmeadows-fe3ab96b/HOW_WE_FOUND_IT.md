# How we found it (contributor text, unverified)

The brief: one search lane over hsp4 N = 120..210 (N = 170 skipped, already claimed), four cores, about 3.5 hours,
with the 2026-10-31 snapshot of radius.txt as the target values. Packomania's posted coordinates were not available
offline, so no search started from them.

What failed: D4 and A4 lattice cuts, outer-shell/inner-core splits and hard-sphere Monte Carlo compression, all 3e-3 to
2e-2 below the table in tests at N = 100 and 150; 600-cell shell seeds reproduce the table at N = 120..128 (ties, not
wins); seeding from neighbouring N (pass 2) had low yield; long basin hopping from one fixed basin gained only about 1e-6.

What worked: many independent random starts annealed with a Riesz energy (pair and wall terms, exponent 4 rising to 64,
L-BFGS), each followed by penalty descent of -r + k/2 * sum(overlap^2) with k from 1e2 to 1e11, monotonic basin hopping
(Gaussian jitter of 0.05 to 0.2 r), and a final sequential-LP polish of the near-active contact set (HiGHS, trust
region). Seven of the 90 cells ended above the table (N = 136, 141, 152, 156, 160, 163, 188); this package is N = 160.
