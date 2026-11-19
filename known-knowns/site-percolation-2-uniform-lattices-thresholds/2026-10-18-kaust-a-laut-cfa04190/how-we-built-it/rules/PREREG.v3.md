# PREREG.v3: site-percolation-2-uniform-lattices-thresholds

frozen: 2026-10-16T17:42:16Z (date -u), before any data of the datasets below exist. PREREG.md and PREREG.v2.md stay in force
unchanged; this file adds calibration datasets, one check torus, one transfer-matrix cell and the n_max rule. It
changes no threshold and no decision rule.

null_test: not needed because the claim is a measured constant checked against calibration lattices with exactly known or published high-precision thresholds (unchanged from PREREG.md)

## Evaluator for the new MC datasets

nzwrap2.exe (attempts/evaluator-first/code/nzwrap2.c). It writes byte-identical .hist and .state files to the
frozen nzwrap.exe for the same arguments: test_nzwrap2.py, 16 of 16 cases (11 lattices, site and bond, resume after
a stop), and bench_nzwrap.py on #23 at 512 x 128 (site and bond), all byte-identical (test_nzwrap2_output.txt,
bench_output.txt). For speed, nzwrap.exe may be used instead at small sizes; the output is the same either way.
Block sizing and seeds as mc_worker.py (samples per block = max(1000, round(4.5e9 / M, -3)), seed = seed0 + L2).

## Addition A: square site MC calibration (kill criterion 5)

Square lattice, L1 = L2 in {8, 12, 16, 24, 32, 48, 64}; 20 blocks at L = 8, 12 and 60 blocks at L = 16..64;
seed0 = 4000. One look when all sizes are complete: fss_mc.py primary fit (L2 >= 16, one-term L^-4, PREREG.md).
Pass: |p_MC - 0.59274605079210| <= 3 sigma_MC (Jacobsen 2015; Mertens 2022 gives 0.592746050786(3)).
Fail: the MC line stops for every lattice until the cause is found and a new prereg is written.

## Addition B: elongated triangular (3^3,4^2) site MC (row-lattice calibration, decides no claim)

Rows "ST", L1 = 2 L2, L2 in {8, 12, 16, 24, 32, 48, 64}; 20 blocks at L2 = 8, 12, 60 at L2 = 16..64; seed0 = 3000.
One look when complete: fss_mc.py primary fit; reported against the transfer-matrix ST site extrapolation
(rule (a) form: |p_TM - p_MC| <= 3 combined sigma) and against Suding and Ziff 0.550213(3).
A failure of rule (a) here, together with a pass of Addition A, means a row-lattice-specific MC or TM problem:
no claim on #20-#23 until explained.

## Addition C: #23 site check torus with L1 >= 2048 (the low-statistics torus of PREREG.md)

#23 site, L1 = 2048, L2 = 512, seed 23512, 20 blocks of 200 samples each (fixed). Statistic: p_L (analyze_mc.py,
jackknife over the 20 blocks). Check, at the PREREG.v2 one look for #23 site: |p_L - p_MC| <= 3 sqrt(sigma_L^2 +
sigma_MC^2). Outside means the one-term fit misses a large-L drift: the MC value of #23 is then not used for a claim.
It is not part of the fit.

## Addition D: transfer-matrix n_max for the decision

For #23 site the one-look evaluation uses n_max = 16 if the n = 16 root exists in out/r23_site_series.txt at that
time, otherwise n_max = 15. Availability decides, not the value.

## Addition E: lattice #15 for method A (progress only, not a claim cell)

#15 = (2/3)(3^2,6^2) + (1/3)(3,6,3,6), built by oldest-entry/code/new_lattices.py (2 orbits, fractions and zbar of
the Wikipedia row), cylinder circumference = the shortest period vector (length sqrt(3)). tmcrit site n = 1..n_max as
memory allows (one lattice at a time when above 4 GB), extrapolated by the frozen rule. It becomes a claim cell
only through a later prereg that adds its MC design before any MC data exist.
