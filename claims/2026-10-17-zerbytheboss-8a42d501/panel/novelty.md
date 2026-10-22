# Panel Skeptic Audit: NOVELTY (`ccd-gupta-murrell-mottram-metal-clusters`)

- `role`: novelty
- `context`: subagent (fresh invocation)
- `target_id`: `ccd-gupta-murrell-mottram-metal-clusters`
- `audited_utc`: `2026-10-18T04:03:59Z`

## 1. Single Honest HTTP Fetch of Primary Sources (No Retries)

Using Python `urllib.request.urlopen` (single request per URL, zero retries) at `2026-10-18T04:03:59Z`:

1. **Cambridge Cluster Database — Gupta Metal Clusters Index (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta.html` / `Gupta.html`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta.html`
   - **HTTP Status**: `200` (`2696` bytes, `Last-Modified: Mon, 23 Feb 2026 08:30:25 GMT`, SHA-256 `519a73cbf87cf7dc6ddcb814ea35754c61fadd3873e302b7985e8c4f12a862ca`, matching `the-record-we-beat/snapshot_2026-10-17.md`)
   - **Fetched UTC**: `2026-10-18T04:03:59Z`

2. **Cambridge Cluster Database — Zinc Gupta Table (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Zn/table.html` / `Zn/zn.html`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Zn/table.html` (J. P. K. Doye, *"Everything you wanted to know about Zn and Cd clusters (if they are described by a Gupta potential)"*, *Physical Review B* 68, 195418, 2003; `https://arxiv.org/abs/cond-mat/0306225`)
   - **HTTP Status**: `200` (`19989` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:26 GMT`, SHA-256 `965d83b51b85fe897e0c5e5ee4a549ac32775c6e201bb59ede030d389b59c601`, matching `the-record-we-beat/snapshot_2026-10-17.md`)
   - **Fetched UTC**: `2026-10-18T04:03:59Z`
   - **Quoted Live Table Value**:
     - `Zn_106` (`N = 106`, point group `C_1`): `-141.928489 eV` (recomputed from posted point file `points/106`: `-141.9284893514 eV`, Newton-polished: `-141.9284893514 eV`)

3. **Cambridge Cluster Database — Cadmium Gupta Table (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/table.html` / `Cd/cd.html`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/table.html` (J. P. K. Doye, *Physical Review B* 68, 195418, 2003)
   - **HTTP Status**: `200` (`19925` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:29 GMT`, SHA-256 `6d1b3e7f245d38a4c9170b98dcda6ff52d8cc2b2ac7a4b93de52ced3ceb3b1ae`, matching `the-record-we-beat/snapshot_2026-10-17.md`)
   - **Fetched UTC**: `2026-10-18T04:03:59Z`
   - **Quoted Live Table Values**:
     - `Cd_71` (`N = 71`, point group `C_1`): `-82.302019 eV` (recomputed and polished from posted `points/71`: `-82.3020188326 eV`)
     - `Cd_84` (`N = 84`, point group `C_s`): `-97.415006 eV` (recomputed and polished from posted `points/84`: `-97.4150057630 eV`)
     - `Cd_94` (`N = 94`, point group `C_1`): `-109.048698 eV` (recomputed and polished from posted `points/94`: `-109.0486983843 eV`)
     - `Cd_106` (`N = 106`, point group `C_1`): `-123.000416 eV` (recomputed and polished from posted `points/106`: `-123.0004155585 eV`)

4. **Cambridge Cluster Database — Lead (`Pb`) & Sodium (`Na_Gupta`) Tables and arXiv Sources**:
   - **Lead (`Pb`, `N = 3..150`)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Pb/table.html` (`Pb/pb.html`), HTTP `200`, `24073` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:24 GMT`, SHA-256 `0e565f399bb9c9ec29ba7fba60ad07008352c7e3d87b1fc2fc3af2116f0f3f73`.
   - **Sodium (`Na_Gupta`, `N = 3..379`)**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Na/table.html` (`Na_Gupta/na_gupta.html`), HTTP `200`, `59281` bytes, `Last-Modified: Thu, 25 Jul 2024 14:43:20 GMT`, SHA-256 `0c87fb16135bb2cdbab33c3848af87bfb042d1fcedbf560e374035a134652afe`.
   - **arXiv Sources**: `https://arxiv.org/abs/cond-mat/0306225` (HTTP `200`, `41603` bytes, SHA-256 `7fd51ecf93846b82df6679b44c4e4009dfbea1d92749733b366790fb0f3db234`) and `https://arxiv.org/abs/2505.05989` (HTTP `200`, `42453` bytes, SHA-256 `fc0e01ee942b304b27bac2048da6d828039339b4143038bcf42cd7b47fc0aa88`), fetched at `2026-10-18T04:02:45Z`–`2026-10-18T04:03:59Z`.

## 2. Literature, Trophy Case, and Pull Request Audit

1. **Last 24 Months of Literature (2024-2026)**:
   - Searched 2024-2026 literature and citations of Doye (2003, *Phys. Rev. B* 68, 195418), Cleri and Rosato (1993), and the Cambridge Cluster Database `Zn` and `Cd` Gupta tables.
   - Note that Aguado et al. (*Nanoscale* 2018, *PCCP* 2019) use cluster-refitted Gupta parameters that are non-comparable with the bulk-fitted Cleri-Rosato Doye tables (`p = 9.689, q = 4.602, A = 0.1477 eV, xi = 0.8900 eV` for `Zn`; `p = 10.612, q = 5.206, A = 0.1420 eV, xi = 0.8117 eV` for `Cd`), and Lai et al. (2025) study `Ag` (`N = 141..310`) and binary nanoalloys rather than pure `Zn` or `Cd` clusters.
   - No publication in the last 24 months (or any prior work under the Doye / Cleri-Rosato Gupta parameter sets) reports energies lower than the live CCD table values for `Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, or `Cd_106`.

2. **Repository `TROPHY_CASE.md`**:
   - Inspected all 53 rows of `TROPHY_CASE.md` across the existing result families (`degree-diameter`, `constant-weight-codes`, `lehmer`, `fast-matrix-multiplication`, `sealed-envelopes/bouchaudy-cipher-machines`, `vnncomp-2026`, `robustbench-cifar100`).
   - Confirmed `0` existing entries for `ccd-gupta-murrell-mottram-metal-clusters` or Gupta `Zn`/`Cd` nanoclusters.

3. **Open and Merged Pull Requests on `elder-plinius/V3R1T4S`**:
   - Queried `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` across pages 1 to 3 (300 total open/closed/merged PRs).
   - Confirmed `0` open, closed, or merged pull requests targeting `ccd-gupta-murrell-mottram-metal-clusters` or Gupta `Zn`/`Cd` clusters.

## 3. Strict Improvement Verification Across All 5 Structures

- **Artifact**: `object/gupta_zn_cd_5_records_and_780_audit.json` (SHA-256 `a9e11a5c5563c428f65acad059f7b585b2d7ef3985936feeea3c148657fda05c`, matching all 5 rows of `INDEX.csv`).
- **Per-Cluster Strict Margins (all strictly beating the live 6-decimal CCD table and polished CCD coordinates by `-0.000207 eV` to `-0.004692 eV`, exceeding the `1e-4 eV` threshold by `2.07x` to `46.9x`)**:
  1. **`Zn_106` (`N = 106`)**: `E* = -141.9309047390 eV` vs CCD `-141.928489 eV` (polished CCD: `-141.9284893514 eV`), change **`-0.002416 eV`** (`-0.0024157390 eV` vs table, `-0.0024153876 eV` vs polished CCD, `24.2x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 1.91e-14`, Decimal50 `||grad E||_2 = 6.50e-35`, `312/312` positive vibrational Hessian modes).
  2. **`Cd_71` (`N = 71`)**: `E* = -82.3022257380 eV` vs CCD `-82.302019 eV` (polished CCD: `-82.3020188326 eV`), change **`-0.000207 eV`** (`-0.0002067380 eV` vs table, `-0.0002069054 eV` vs polished CCD, `2.07x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 2.04e-14`, Decimal50 `||grad E||_2 = 6.58e-35`, `207/207` positive vibrational Hessian modes).
  3. **`Cd_84` (`N = 84`)**: `E* = -97.4196981104 eV` vs CCD `-97.415006 eV` (polished CCD: `-97.4150057630 eV`), change **`-0.004692 eV`** (`-0.0046921104 eV` vs table, `-0.0046923474 eV` vs polished CCD, `46.9x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 2.22e-14`, Decimal50 `||grad E||_2 = 5.63e-35`, `246/246` positive vibrational Hessian modes).
  4. **`Cd_94` (`N = 94`)**: `E* = -109.0494558230 eV` vs CCD `-109.048698 eV` (polished CCD: `-109.0486983843 eV`), change **`-0.000758 eV`** (`-0.0007578230 eV` vs table, `-0.0007574386 eV` vs polished CCD, `7.58x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 1.95e-14`, Decimal50 `||grad E||_2 = 5.68e-35`, `276/276` positive vibrational Hessian modes).
  5. **`Cd_106` (`N = 106`)**: `E* = -123.0018760970 eV` vs CCD `-123.000416 eV` (polished CCD: `-123.0004155585 eV`), change **`-0.001460 eV`** (`-0.0014600970 eV` vs table, `-0.0014605385 eV` vs polished CCD, `14.6x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 2.43e-14`, Decimal50 `||grad E||_2 = 6.02e-35`, `312/312` positive vibrational Hessian modes).
- **Complete 780-Point-File Calibration & Reproduction Audit**: All 780 posted point files (`Zn` `N = 3..125`, `Cd` `N = 3..125`, `Pb` `N = 3..150` plus 9 `Pb_Gupta.rar` files, and `Na_Gupta` `N = 3..379`) reproduce their posted 6-decimal CCD table energies within `7.17e-7 eV` (well below `1e-5 eV`) and polish by less than `5e-7 eV` on the 5 target sizes, confirming that all 5 new structures lie in distinct lower-energy basins.

pass: true
