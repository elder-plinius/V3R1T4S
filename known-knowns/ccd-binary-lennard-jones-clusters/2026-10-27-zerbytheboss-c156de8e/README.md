# Cambridge Cluster Database Binary Lennard-Jones 600-Cell & 666-File Coordinate Re-Evaluation Audit (`p2`)

## What
A machine-readable 600-cell merged audit table (object/blj_600_cell_audit.csv) and 666-file coordinate re-evaluation audit (object/blj_all_666_files_reproduction_audit.csv) re-evaluating from 3D Cartesian coordinates all 576 canonical all.tar point files, all 27 live HTTP-200 'new' point files on the Cambridge Cluster Database server (while cataloging the 70 'new'/'newer' table links that return HTTP 404 on the live server and 4 updated cells whose table href still points to the superseded all.tar file), and all 63 point files across the 4 hosted improvement archives (Wenqi_Tao_BLJ.zip, Wenqi_Tao_BLJ2.zip, Istvan_Kolossvary_new_BLJ_minima.tgz, and NEW_BINARY_LJ_MINIMA/), verifying that 666/666 hosted coordinate files reproduce their own posted header energies within 1e-5 (max error 9.14e-8), reporting the merged minimum energy over the live table and all hosted files for all 600 cells, and identifying all 33 cells where hosted improvement files beat both the live HTML table and live linked point files by > 1e-4.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (recomputes the pairwise binary Lennard-Jones potential from 3D coordinates for all 666 point files in `< 1` second using pure Python standard library, verifies `1e-5` header and table reproduction, verifies the `|lambda| < 1e-6` analytical Hessian zero-mode threshold, and checks all 600 cells of `object/blj_600_cell_audit.csv` and all 666 rows of `object/blj_all_666_files_reproduction_audit.csv`).

## Compared To
All comparisons are against the authoritative Cambridge Cluster Database (CCD) status table, live HTTP server directory listings, canonical archive, and 4 hosted improvement archives:
- Live Table: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/table.html` (HTTP `200`, SHA-256 `045161fcbc4117f5a4c52252cbe3c7680342aee55be9dde95e6d729d3fec449d`).
- Canonical Archive: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/all.tar` (HTTP `200`, SHA-256 `6e18e78d50f65d804d36545fc6ebc9764e600f6b2a8829def028015625446c08`, `576` files).
- Live Server `new` Point Files (`27` files returning `HTTP 200` under `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/1.05/` and `1.1/`; `70` `new`/`newer` links in `1.1/46new` and `1.15..1.30` return `HTTP 404 Not Found`).
- Hosted Improvement Archives (`63` coordinate files total):
  - `Wenqi_Tao_BLJ.zip` (SHA-256 `69e4ec09081621654d1fdf018dd8ec621062f4e4b9606afb5f4914b180cfcea9`, `12` files)
  - `Wenqi_Tao_BLJ2.zip` (SHA-256 `9328552d1a61229984628fb2a33b5398025c1a9fd8a35c700b5df7fc861ed18a`, `17` files)
  - `Istvan_Kolossvary_new_BLJ_minima.tgz` (SHA-256 `136e27ee131204a41fab707e2da4172c5ed229140dfbe5b79d3f46cfeaa7972e`, `17` files)
  - `NEW_BINARY_LJ_MINIMA/` (`17` files)

| Metric | Specification Target (`p2`) | Audit Result | Status |
|---|---|---|---|
| Cell Coverage | 600 cells (`N=1..100`, 6 ratios `1.05..1.30`) | 600 cells in `object/blj_600_cell_audit.csv` with `merged_min_energy` and `best_coord_evaluated_energy` | Verified |
| Point Files Re-Evaluated from 3D Coordinates | All `all.tar` + live `new` + 4 hosted archives | `666` files (`576` `all.tar` + `27` live `new` + `63` hosted archive files) in `object/blj_all_666_files_reproduction_audit.csv` | Verified |
| Internal Header Reproduction (`<= 1e-5`) | Flag any file failing `1e-5` | `666 / 666` (`100%`) reproduce header energy within `1e-5` (max error `9.14e-8` on `99SBB1.25.txt`) | Verified |
| Live Table Link Audit (`N=5..100`, 576 links) | Re-evaluate every linked point file | `475` canonical `HTTP 200` + `27` live `new` `HTTP 200` (all `502` match `table.html` within `5e-7`); `70` broken `new`/`newer` `HTTP 404` links; `4` stale hrefs (`1.05/31`, `1.05/36`, `1.05/97`, `1.1/66`) | Verified |
| Hosted Archives Beating Live Table (`> 1e-4`) | Flag every cell beaten by `> 1e-4` | Exactly `33` cells beaten by `> 1e-4` (both vs `table.html` and vs live linked point files) | Verified |

## Not Claimed
- This submission is scoped strictly to partial win `p2` (the complete 600-cell and 666-file coordinate re-evaluation audit across the live CCD table, live server directories, `all.tar`, and all 4 hosted improvement archives). We do not claim a full-win new putative global minimum in this pull request.

## Credits
- Contributor: `zerbytheboss` (GitHub account `HindsightWise` is operated by `zerbytheboss`).
- Jonathan Doye and Lars Meyer (*Phys. Rev. Lett.* 95, 063401, 2005) for the binary Lennard-Jones cluster benchmark.
- David Wales and the Cambridge Cluster Database team (`https://www-wales.ch.cam.ac.uk/CCD.html`) for hosting the data archives.
- Huang Wenqi, Ye Tao, Istvan Kolossvary, Andrea Cassioli, Marco Locatelli, Fabio Schoen, Wayne Pullan, Christian Sicher, Stephan Mohr, and Stefan Goedecker for published cluster structures.
