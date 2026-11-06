# CCD Gupta cobalt table, N = 2..200: an audit of every posted file (partial win p1 of ccd-gupta-cobalt-clusters-n200)

## What

With the Gupta potential A = 0.0950 eV, xi = 1.4880 eV, p = 11.604, q = 2.286 (r in units of r0), which reproduces all ten Co.zip energies within 4.8e-7 eV as posted and 198 of 199 table energies within 6e-8 eV after polishing (N = 102 lies 1.1e-6 eV below its posted value), object/ccd_cobalt_audit.csv correctly recomputes all 199 CCD cobalt table point files in data/points.tgz (sha256-identical to the live CCD download of 2026-10-19) and all ten Co.zip files, and the only N whose posted table energy is not reproduced within 1e-5 eV are N = 163, 175, 179, 183, 185, 188, 189 and 190 for the coordinates as posted (all within 1e-5 eV after polishing), while no posted table or Co.zip structure polishes lower than its own posted energy by more than 1e-4 eV.

The potential, stated here because the CCD page gives no parameters: E = sum_i [ sum_{j!=i} A exp(-p (r_ij - 1)) -
sqrt( sum_{j!=i} xi^2 exp(-2 q (r_ij - 1)) ) ], all pairs, no cutoff, r_ij in units of r0 (2.497 A for cobalt), energies in
eV, with the Cleri-Rosato cobalt parameters A = 0.0950 eV, xi = 1.4880 eV, p = 11.604, q = 2.286.
`object/ccd_cobalt_audit.csv` has one row per N = 2..200: the posted point group and energy, the energy of the posted
coordinates (`E_table_as_is`), the polished energy, the three flags of the partial win, the Co.zip energy (posted and
recomputed) where one exists, and `E_best` = the lower of the two CCD sources with `best_source`.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. About 20 to 40 seconds on a laptop. Needs Python 3.8+ with numpy and scipy, and either
network access to www-wales.ch.cam.ac.uk or `CCD_DATA_DIR` pointing to a folder with the three CCD files; every file is
checked against its sha256 pin. Details in RUN_IT_YOURSELF.md; real output in verify-it-yourself/RECEIPTS.md.

## Compared to

The Cambridge Cluster Database cobalt table, https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html, all 199 cells
(N = 2..200), with its point files (points.tgz) and the improved minima (Co.zip, Co/Energy.txt), fetched
2026-10-19T03:57:05Z to 03:57:10Z (HTTP 200; sizes, Last-Modified and sha256 in the-record-we-beat/README.md). The
novelty skeptic re-fetched the page at 2026-10-19T04:56:43Z: identical bytes.

## Not claimed

- No new global minimum. A one-hour search with five lenses (logs in how-we-built-it/logs/) found no structure below
  the table or Co.zip; the closest misses were N = 177 (0.00058 eV above) and N = 161 (0.0018 eV above).
- `E_best` is the lower of the two CCD sources for each N, not a literature-wide best value. J. Chem. Inf. Model. 63,
  6727 (2023) re-searched Co_N for N = 3..200; the novelty skeptic read only its abstract (no Co improvement reported).
- The target's calibration clause ("reproduce the posted energies of ten randomly chosen table point files to 1e-6 eV")
  cannot be met with the files as posted: 84 of 199 are within 1e-6 eV. After polishing, 198 of 199 are within 6e-8 eV
  and N = 102 lies 1.1e-6 eV below its posted value.
- verify-it-yourself checks the table rows (as posted and polished) and the Co.zip energies as posted; the Co.zip half
  of "no posted structure polishes lower than posted by more than 1e-4 eV" was verified by the reproduce and criterion
  skeptics (panel/), not by the shipped checker. Its polish is float64 L-BFGS to a gradient norm below 1e-4; the
  skeptics polished to about 1e-13 with Newton steps and found the same flags.
- The literature part of the novelty check is provisional; its limits are listed in panel/novelty.md.

## Credits

Submission credit: DmitrL-dev. Table: Cambridge Cluster Database (D. J. Wales and co-workers); cobalt minima from
L. Zhan, J. Z. Y. Chen, W.-K. Liu and S. K. Lai, J. Chem. Phys. 122, 244707 (2005), doi:10.1063/1.1940028; improved
minima in Co.zip from Lai Xiangjing, Huang Wenqi and Ni Hanwen. Potential: F. Cleri and V. Rosato, Phys. Rev. B 48, 22
(1993). Target and partial win p1: the V3R1T4S bank.
