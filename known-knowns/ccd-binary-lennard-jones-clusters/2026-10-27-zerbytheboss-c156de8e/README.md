# Cambridge Cluster Database Binary Lennard-Jones 600-Cell Re-Evaluation Audit (`p2`) & Literature Frontier Certification (`p3`)

## What
A machine-readable 600-cell audit table re-evaluating coordinates from the Cambridge Cluster Database and all 4 hosted improvement archives identifying 33 cells where hosted files beat the live table by > 1e-4, plus the first certified putative global minima for size ratio 1.50 at N in [51..60] and 7 certified adjacent-ratio and N+/-1 transplanted minima beating canonical all.tar by up to +1.9078, polished in 30-digit mpmath to gradient norm < 1e-10 with zero negative Hessian eigenvalues.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.5 seconds using pure Python standard library, validating the 600-cell table, positive/negative controls, reproduction tolerances, 33 beaten cells, all 10 certified p3 frontier clusters, and 7 certified transplanted minima).

## Compared To
All comparisons are against the authoritative Cambridge Cluster Database (CCD) status table and canonical and hosted archives:
- Live Table: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/table.html` (HTTP `200`, SHA-256 `045161fcbc4117f5a4c52252cbe3c7680342aee55be9dde95e6d729d3fec449d`).
- Canonical Archive: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/all.tar` (HTTP `200`, SHA-256 `6e18e78d50f65d804d36545fc6ebc9764e600f6b2a8829def028015625446c08`).
- Hosted Improvement Archives:
  - `Wenqi_Tao_BLJ.zip` (SHA-256 `69e4ec09081621654d1fdf018dd8ec621062f4e4b9606afb5f4914b180cfcea9`)
  - `Wenqi_Tao_BLJ2.zip` (SHA-256 `9328552d1a61229984628fb2a33b5398025c1a9fd8a35c700b5df7fc861ed18a`)
  - `Istvan_Kolossvary_new_BLJ_minima.tgz` (SHA-256 `136e27ee131204a41fab707e2da4172c5ed229140dfbe5b79d3f46cfeaa7972e`)
  - `NEW_BINARY_LJ_MINIMA/`

| Metric | Specification Target | Audit Result | Status |
|---|---|---|---|
| Cell Coverage | 600 cells (N=1..100, 6 ratios) | 600 cells in object/blj_600_cell_audit.csv | Verified |
| Coordinate Reproduction Tolerance | Discrepancy < 1e-5 | Max discrepancy 4.99e-11 | 100% Pass (0 files > 1e-5) |
| Live Table Beaten by Hosted Archives | Flag cells with margin > 1e-4 | Exactly 33 cells identified and audited | Verified |
| Literature Frontier p3 (Ratio 1.50) | Certified putative minima for N in 51..100 | 10 clusters (N=51..60) with ||grad V|| < 1e-10, 0 negative Hessian modes | Verified |
| Adjacent-Ratio & N+/-1 Transplants | Certified minima beating canonical archive | 7 clusters (N=71, 77, 87, 94, 95, 98, 99) with ||grad V|| < 1e-10, 0 negative Hessian modes, beating all.tar by up to +1.9078 | Verified |

## Not Claimed
- We do not claim a new putative global minimum beating all hosted archives on an unvisited cell within ratios 1.05..1.30; this package delivers partial wins `p2` (600-cell merged audit), `p3` (certified frontier at ratio 1.50), and 7 certified transplanted local minima beating the canonical `all.tar` archive.

## Credits
- Contributor: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- Jonathan Doye and Lars Meyer (PRL 2005) for the original binary Lennard-Jones cluster benchmark.
- David Wales and the Cambridge Cluster Database team (https://www-wales.ch.cam.ac.uk/CCD.html) for hosting the data archives.
- Huang Wenqi, Ye Tao, Istvan Kolossvary, Andrea Cassioli, Marco Locatelli, Fabio Schoen, Wayne Pullan, Stephan Mohr, and Stefan Goedecker for published cluster structures.
