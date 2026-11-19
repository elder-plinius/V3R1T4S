# PREREG.v2: site-percolation-2-uniform-lattices-thresholds

frozen: 2026-10-16T17:25:39Z (date -u), before any Monte Carlo block beyond
block 20 exists and before any new transfer-matrix series is run.

PREREG.md (byte copy of runs/2026-10-16-0447/PREREG.md, frozen 2026-10-16T05:22:16Z) stays in force unchanged: the
criterion, cells, both methods, the fit, the thresholds and decision rules (a)-(d). This file only adds a stopping
rule for the Monte Carlo, a pipeline test, and calibration lattices. It changes no threshold.

null_test: not needed because the claim is a measured constant checked against calibration lattices with exactly known or published high-precision thresholds (unchanged from PREREG.md)

## What was already seen before this freeze (interim, decides nothing)

At 20 blocks per size (runs/2026-10-16-1714/attempts/timeline-aligner/out/): kagome site p_MC 0.652707020(1637),
exact 0.6527036447, +2.06 sigma, stable; #23 site p_MC 0.571771431(2262), stable; #23 bond p_MC 0.458442891(2599).
Transfer matrix at n_max = 15 (attempts/exact-polynomial/out/extrapolate_rows.txt): #23 site 0.5717645628(1080),
#22 0.5646354181(1660), #21 0.5342770535(1440), #20 0.5260053225(1590); #23 bond (n_max 12) 0.4584460446(2090).
Rule (a) for #23 site at 20 blocks: |TM - MC| = 6.87e-6 against 3 combined sigma 6.79e-6 (3.04 sigma). This
interim value is reported as it stands and is not the decision: the MC sigma (2.26e-6) does not yet meet the
PREREG.md requirement sigma_MC <= 2e-6, so no claim and no refutation can be made from it.

## Addition 1: Monte Carlo stopping rule (fixed budget, one look)

- Datasets kagome site, #23 site, #23 bond: every size with L2 >= 16 is extended to exactly 60 blocks (blocks 20..59),
  by the same nzwrap.exe (sha256 44c3b4612db4dc5d1df8c79b2de25f04522ddde9730d356071d4bda6d70e78f3), the same lattice
  files, sizes, samples per block and seeds, continuing each size's xoshiro256** stream from its .state file.
  L2 = 8 and 12 stay at 20 blocks (the primary fit does not use them).
- The PREREG.md fit (fss_mc.py, primary L2 >= 16, stability L2 >= 24) and decision rules (a) and (b) are evaluated
  once, when every size of the dataset has exactly 60 blocks. That evaluation is the decision. Progress checks
  before then count blocks only; no fit is run on a partly extended dataset except to report "in progress".
- New Monte Carlo datasets for #20, #21, #22 site (aspect ratios of PREREG.md): L2 = 8, 12 with 20 blocks,
  L2 = 16..128 with 60 blocks, seeds seed0 + L2 with seed0 = 20000 + 1000 * (lattice number), the same one-look rule.
- Kill rule added (kill criterion 5, made concrete): if the 60-block kagome site fit is more than 3 sigma from the
  exact value, the whole MC line stops until the cause is found and a new prereg is written.

## Addition 2: estimator test on the triangular lattice (pipeline test, kill criterion 5)

Triangular site percolation is self-matching, so on every L x L torus the microcanonical curves satisfy
R_0D(n) = R_2D(M - n) and the crossing R_2D(p) = R_0D(p) lies at p = 1/2 exactly for every L. Test: nzwrap with
mc_worker on the triangular lattice, L = 16, 32, 64 (L1 = L2), 10 blocks each, seed0 = 7000. Pass: every
|p_L - 1/2| <= 3 sigma_L (jackknife over the 10 blocks). Fail: the MC line stops (kill criterion 5).

## Addition 3: calibration lattice for the row geometry (transfer matrix, decides no claim)

Elongated triangular (3^3,4^2) = rows "ST" (lattices.py, tiling check 1 orbit, zbar 5). tmcrit site n = 1..15 and bond
n = 1..12 (13 if memory allows), extrapolated by the frozen rule. Published values (live Wikipedia, 17:16Z):
bond 0.41964035886369(2) (Scullard and Jacobsen 2019), site 0.550213(3) (Suding and Ziff 1999).
Pass for the bond: |p_TM - published| <= max(3 sigma_TM, 1e-7) with sigma_TM <= 1e-7 (the PREREG.md (c) standard).
Site: reported as a comparison only (the published error is 3e-6). A failed bond calibration means the
transfer-matrix error bars on row lattices are not trusted for any claim until explained.

## Addition 4: transfer-matrix bond series for #20, #21, #22

tmcrit bond n = 1..12 for #20, #21, #22, extrapolated by the frozen rule, compared with the Wikipedia bond column
(criterion (c) and partial win p2, rules exactly as in PREREG.md).
