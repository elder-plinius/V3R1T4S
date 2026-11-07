# How We Found It: Binary Lennard-Jones Clusters 600-Cell & 666-File Coordinate Audit (`p2`)

_contributor text, unverified_

## Methodology

### 1. Complete Coordinate Harvest Across Live Server & Hosted Archives
We fetched and parsed every coordinate file linked by or hosted alongside the Cambridge Cluster Database Binary Lennard-Jones page (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/`):
1. **Canonical archive `all.tar`** (`576` coordinate point files covering `N = 5..100` across the 6 size ratios `{1.05, 1.10, 1.15, 1.20, 1.25, 1.30}`).
2. **Live server directory audit for the 97 `new`/`newer` table links**:
   - Inspecting the live Apache directory indexes (`/1.05/`, `/1.1/`, `/1.15/`, `/1.2/`, `/1.25/`, `/1.3/`) and fetching every `<A HREF="...">` target in `table.html` revealed that **27 `new` coordinate files** (`1.05/43new`, `1.05/90new`, `1.1/47new`, `1.1/62new..65new`, `1.1/67new`, `1.1/70new..81new`, `1.1/83new..89new`) are hosted live (`HTTP 200`) on the server even though they were omitted from `all.tar`.
   - The remaining **70 `new`/`newer` links** (`1.1/46new` and all 69 `new`/`newer` links in `1.15/`, `1.2/`, `1.25/`, and `1.3/`) return `HTTP 404 Not Found` on the live server, where only the un-suffixed `all.tar` coordinate file (`1.X/N`) is present.
   - In addition, **4 cells** (`1.05/31`, `1.05/36`, `1.05/97`, `1.1/66`) have updated energies in `table.html` (footnote `c`), while their `<A HREF="1.X/N">` link still points to the superseded `all.tar` file.
3. **All 4 hosted improvement archives (`63` coordinate files)**:
   - `Wenqi_Tao_BLJ.zip` (`12` structures, Huang & Ye, *JCIM* 2011)
   - `Wenqi_Tao_BLJ2.zip` (`17` structures, Huang & Ye, *JCIM* 2011)
   - `Istvan_Kolossvary_new_BLJ_minima.tgz` (`17` structures, Kolossvary, *PRE* 2010)
   - `NEW_BINARY_LJ_MINIMA/` (`17` structures, Sicher, Mohr & Goedecker, *JCP* 2011)

### 2. Exact Pairwise BLJ Coordinate Re-Evaluation & Merged Minimum Table
For all `666` coordinate point files (`576 + 27 + 63`), we evaluated the pairwise binary Lennard-Jones potential without cutoff:
$$E = \sum_{i < j} 4 \left( \left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12} - \left(\frac{\sigma_{ij}}{r_{ij}}\right)^6 \right)$$
with $\sigma_{AA} = 1.0$, $\sigma_{BB} = \text{ratio}$, and Lorentz-Berthelot arithmetic mean $\sigma_{AB} = (1 + \text{ratio}) / 2$.

- **100% Header Reproduction (`666/666`)**: Every one of the 666 hosted coordinate files reproduces its own internal header energy within $10^{-5}$ (maximum discrepancy $9.14 \times 10^{-8}$ on `Istvan_Kolossvary/99SBB1.25.txt`; maximum discrepancy across `all.tar` and the 27 live `new` files is $4.99 \times 10^{-11}$).
- **Live Table Reproduction**: All `475` unchanged canonical links and all `27` live `HTTP 200` `new` files reproduce `table.html` within $5 \times 10^{-7} < 10^{-5}$. Only the `70` broken `HTTP 404` `new`/`newer` links (when falling back to `all.tar`) and the `4` stale un-suffixed hrefs (`1.05/31`, `1.05/36`, `1.05/97`, `1.1/66`) differ from `table.html` by $> 10^{-5}$.
- **33 Cells Beaten by Hosted Improvement Archives**: Across the 600 cells, `object/blj_600_cell_audit.csv` reports both `merged_min_energy` (the minimum over `table.html`, the live linked file, `all.tar`, and all 4 hosted improvement archives) and `best_coord_evaluated_energy` (the minimum strictly over coordinate-evaluated files), identifying the 33 cells where hosted archive files beat both `table.html` and the live linked point files by $> 10^{-4}$.
