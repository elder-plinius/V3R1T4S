# PREREG.v6: site-percolation-2-uniform-lattices-thresholds

frozen: 2026-10-17T00:34:14Z (date -u); one edit at 2026-10-17T00:34:53Z, before any bond data of these lattices existed, replaced
a combined-sigma form of rule (c) by the stricter wording of PREREG.md. Frozen before any Monte Carlo bond data exist for #20, #21 or #22. PREREG.md and
PREREG.v2-v5 stay in force unchanged; this file adds three datasets that criterion (c) requires for any claim on
#20, #21 or #22, and changes no threshold and no decision rule.

null_test: not needed because the claim is a measured constant checked against calibration lattices with exactly known or published high-precision thresholds (unchanged from PREREG.md)

## Why

PREREG.md rule (c), Monte Carlo part: "the lattice's Wikipedia bond value within 3 sigma with sigma <= 2e-6". Only #23
has a bond Monte Carlo dataset. Without these, no claim on #20, #21 or #22 can meet (c), and partial win p1 (all 20
lattices) cannot either. Already seen, before this freeze: the transfer-matrix bond values of #20 and #22 differ from
the table by about 1e-6 (2.4-2.6 combined sigma, interim), #21 and #23 agree within 0.5 sigma.

## Datasets

Bond mode, mc_worker.py with the frozen evaluator (nzwrap.exe at the two smallest sizes, nzwrap2.exe above, byte-
identical by PREREG.v3), the PREREG.md aspect ratios and the same size lists as the site datasets:
- #22 bond: L2 = L1 / 3; L2 in {8, 12} with 20 blocks, {16, 24, 32, 48, 64, 128} with 60 blocks; seed0 = 52000.
- #21 bond: L2 = 3 L1 / 8; L2 in {6, 12} with 20 blocks, {18, 24, 36, 48, 72, 144} with 60 blocks (PREREG.v5
  addition 1); seed0 = 51000.
- #20 bond: L2 = 2 L1 / 7; L2 in {8, 12} with 20 blocks, {16, 24, 32, 48, 64, 128} with 60 blocks; seed0 = 50000.
Seeds are seed0 + L2; samples per block as mc_worker.py (max(1000, round(4.5e9 / M, -3)), M = number of bonds).

## Start condition

These datasets start only after the PREREG.v2 one look has been made and the Monte Carlo line survived it: kagome
site within 3 sigma of exact (PREREG.v2), square site within 3 sigma (PREREG.v3 A) and the PREREG.v5 common-offset
rule passed. If the Monte Carlo line stops there, these datasets are not started until a new prereg says so.

## Decision (one look per dataset, as PREREG.v2)

When every size of a dataset has its blocks: fss_mc.py primary fit (L2 >= 16, one-term L^-4) and stability fit
(L2 >= 24), exactly as PREREG.md method B. Rule (c), Monte Carlo part, as PREREG.md words it ("within 3 sigma with
sigma <= 2e-6"): |p_MC,bond - p_table,bond| <= 3 sigma_MC with sigma_MC <= 2e-6 (the table's own error is not added;
the stricter reading). Reported next to it, deciding nothing on its own: |p_MC,bond - p_TM,bond|
against 3 combined sigma (the partial win p2 sanity check of PREREG.md).
