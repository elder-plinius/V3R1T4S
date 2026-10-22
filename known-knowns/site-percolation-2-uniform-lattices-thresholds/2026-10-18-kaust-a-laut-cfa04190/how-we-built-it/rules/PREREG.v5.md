# PREREG.v5: site-percolation-2-uniform-lattices-thresholds

frozen: 2026-10-17T00:11:11Z (date -u), before any Monte Carlo data exist for #20, #21, #22, the square lattice or
(3^3,4^2), before any block of the PREREG.v2 extension is fitted, and before any transfer-matrix root with n = 16
exists. PREREG.md, PREREG.v2.md, PREREG.v3.md and PREREG.v4.md (byte copies in this run folder, sha256 in scout.md)
stay in force unchanged. This file changes no threshold and no decision rule of those files; it fixes one
inexecutable size list and adds one stricter kill rule.

null_test: not needed because the claim is a measured constant checked against calibration lattices with exactly known or published high-precision thresholds (unchanged from PREREG.md)

## Already seen before this freeze (decides nothing by itself)

The PREREG.v2 triangular estimator test ran at 2026-10-17T00:03:58Z (attempts/evaluator-first/out/
triangular_test_output.txt): PASS at all three sizes, p_L - 1/2 = +1.83, +0.12 and +1.40 sigma. All three are
positive; their inverse-variance mean, computed after seeing them, is about +2 sigma. Together with kagome site
(+2.06 sigma at 20 blocks) and #23 site (Monte Carlo above the transfer matrix by 3.04 combined sigma at 20 blocks),
this is the pattern Addition 2 below tests on data not yet seen.

## Addition 1: #21 site Monte Carlo sizes (replaces the PREREG.v2 size list for #21 only)

PREREG.md fixes the #21 aspect ratio L2 = 3 L1 / 8, so L2 must be a multiple of 3; the PREREG.v2 sizes 8, 16, 32, 64
and 128 are not, and mc_worker.py refuses them. For #21 the sizes are L2 in {6, 12} with 20 blocks and
L2 in {18, 24, 36, 48, 72, 144} with 60 blocks (L1 = 8 L2 / 3), seeds seed0 + L2 with seed0 = 41000
(PREREG.v2: 20000 + 1000 x 21). Everything else as PREREG.md and PREREG.v2: the primary fit uses L2 >= 16
(here 18 .. 144), the stability fit L2 >= 24, one look when every size has its blocks.

## Addition 2: common-offset kill rule for the site Monte Carlo (stricter; kill criterion 5)

At the PREREG.v2 one look, with PREREG.v3 Addition A complete, compute over the three site calibrations with exactly
known thresholds: kagome site (the 60-block primary fit, exact 1 - 2 sin(pi/18)), square site (Addition A primary fit,
exact 0.59274605079210) and triangular site (p_L at L = 16, 32, 64, 10 blocks each, exact 1/2, no fit):
offsets d_i = p_MC,i - p_exact,i with sigma_i, D = sum(d_i / sigma_i^2) / sum(1 / sigma_i^2),
sigma_D = 1 / sqrt(sum(1 / sigma_i^2)). If |D| > 3 sigma_D, the Monte Carlo line stops for every lattice (no claim
uses a Monte Carlo value) until the cause is found and a new prereg is written. This adds to, and never relaxes, the
per-lattice kagome and square rules. The triangular inputs are already seen (above); including them can only make
the rule stricter.

## Addition 3: scheduling (no rule change)

From this run, the remaining sizes of queues QC and QD of run 2026-10-16-1714 (kagome site L2 = 24, #23 bond
L2 = 24, PREREG.v3 A and B) and the new datasets #20, #21 (Addition 1) and #22 site run on a pool of parallel slots
(attempts/timeline-aligner/code/pool_runner.py of this run), one size per task, through the same mc_worker.py with the
same executables, lattice files, sizes, samples per block and seeds. A size's xoshiro256** stream continues from its
.state file, so the histograms are byte-identical to those the queues would have written.

## Addition 4: transfer-matrix site series beyond n = 15

#23 site n = 16 (PREREG.v3 Addition D) and #22, #21, #20 site n = 16 (PREREG.v4: each series as far as disk, memory
and time allow) run with tmcrit_stream.exe, one at a time. At the one look of a lattice, its series is extrapolated by
the frozen rule with every n then present in its file. Availability decides, not the value.
