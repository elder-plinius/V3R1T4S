# Panel Skeptic Audit: NOVELTY (`ccd-finnis-sinclair-mo-fe-clusters`)

- `role`: novelty
- `context`: subagent (fresh invocation)
- `target_id`: `ccd-finnis-sinclair-mo-fe-clusters`
- `audited_utc`: `2026-10-17T22:55:19Z`

## 1. Single Honest HTTP Fetch of Primary Sources (No Retries)

Using Python `urllib.request.urlopen` (single request per URL, zero retries) at `2026-10-17T22:55:19Z`:

1. **Cambridge Cluster Database — Finnis-Sinclair Molybdenum (`https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/moly_fs.html`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/moly_fs.html` (J. A. Elliott, Y. Shibuta, and D. J. Wales, *"Global minima of transition metal clusters described by Finnis-Sinclair potentials: a comparison with semi-empirical molecular orbital theory"*, *Philosophical Magazine* 89, 3311-3332, 2009)
   - **HTTP Status**: `200` (`27606` bytes, `Last-Modified: Mon, 26 Feb 2018 16:57:00 GMT`, SHA-256 `86a26ce8f81f7762f5d2bf85980416090a84b7ad2c2c838dd5a2d6bcb9658473`)
   - **Fetched UTC**: `2026-10-17T22:55:19Z` (identical SHA-256 to the `2026-10-17T20:27:05Z` snapshot in `the-record-we-beat/snapshot_2026-10-17.md`)
   - **Quoted Live Table Values**:
     - `Mo_75` (`N = 75`): `-439.4197932305 eV` (polished posted structure: `-439.4197932305 eV`)
     - `Mo_90` (`N = 90`): `-532.7899433214 eV` (polished posted structure: `-532.7899433215 eV`)

2. **Cambridge Cluster Database — Finnis-Sinclair Iron (`https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Fe/iron_fs.html`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Fe/iron_fs.html` (J. A. Elliott, Y. Shibuta, and D. J. Wales, *Philosophical Magazine* 89, 3311-3332, 2009)
   - **HTTP Status**: `200` (`27714` bytes, `Last-Modified: Mon, 26 Feb 2018 16:57:00 GMT`, SHA-256 `0f1edac7ef2bccbe49a73dcbc95886b8683995c9648e4fd7fe25eef8afab79e6`)
   - **Fetched UTC**: `2026-10-17T22:55:19Z` (identical SHA-256 to the `2026-10-17T20:27:05Z` snapshot in `the-record-we-beat/snapshot_2026-10-17.md`)
   - **Quoted Live Table Values**:
     - `Fe_86` (`N = 86`): `-312.6006513052 eV` (polished posted structure: `-312.6006513052 eV`)
     - `Fe_87` (`N = 87`): `-316.4759023549 eV` (polished posted structure: `-316.4759023549 eV`)
     - `Fe_90` (`N = 90`): `-327.8503707653 eV` (polished posted structure: `-327.8503707653 eV`)
     - `Fe_91` (`N = 91`): `-331.9072022873 eV` (polished posted structure: `-331.9072022874 eV`)
     - `Fe_92` (`N = 92`): `-335.9034309081 eV` (polished posted structure: `-335.9034309082 eV`)
     - `Fe_96` (`N = 96`): `-351.2027399452 eV` (polished posted structure: `-351.2027399452 eV`)
     - `Fe_97` (`N = 97`): `-354.9919830214 eV` (polished posted structure: `-354.9919830215 eV`)
     - `Fe_98` (`N = 98`): `-358.8031191667 eV` (polished posted structure: `-358.8031191668 eV`)
     - `Fe_100` (`N = 100`): `-366.5806583336 eV` (polished posted structure: `-366.5806583337 eV`)

3. **Force-Biased Monte Carlo Reference (`https://arxiv.org/abs/1708.00096`)**:
   - **URL**: `https://arxiv.org/abs/1708.00096` (Dil K. Limbu and Parthapratim Biswas, *"Structure of transition metal clusters: A force-biased Monte Carlo approach"*, 2017)
   - **HTTP Status**: `200` (`42900` bytes, SHA-256 `eafe2d886829a1570e0b9a40dba72ca2563188091cb53c4813498f8e4f82ae14`)
   - **Fetched UTC**: `2026-10-17T22:55:19Z`
   - **Scope Check**: Models `Fe_N` for `N = 5..60` and benchmarks against the CCD `FS_Fe` table (with energies within `0.05 eV` above the CCD values and none lower than the CCD entries; does not cover `N = 75..100`).

## 2. Literature, Trophy Case, and Pull Request Audit

1. **Last 24 Months of Literature (2024-2026)**:
   - Searched 2024-2026 literature and citations of Elliott, Shibuta, and Wales (2009), Finnis and Sinclair (1984, 1986), and the Cambridge Cluster Database `FS_Mo` and `FS_Fe` tables.
   - No publication in the last 24 months (or any prior work) reports Finnis-Sinclair `Mo_N` or `Fe_N` energies for `N = 3..100` below the live CCD values for `Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, or `Fe_100`.

2. **Repository `TROPHY_CASE.md`**:
   - Inspected `TROPHY_CASE.md`: confirmed zero existing entries for `ccd-finnis-sinclair-mo-fe-clusters`.

3. **Open and Merged Pull Requests on `elder-plinius/V3R1T4S`**:
   - Queried `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` across pages 1 to 3 (300 total open/closed/merged PRs).
   - Confirmed `0` open, closed, or merged pull requests targeting `ccd-finnis-sinclair-mo-fe-clusters` or Finnis-Sinclair `Mo`/`Fe` clusters.

## 3. Strict Improvement Verification Across All 11 Structures

- **Artifact**: `object/fs_mo_fe_11_records_and_196_audit.json` (SHA-256 `215c879357f5bbbcc335e6dece2dc7ad12248abd428ef6b1c5ff9a4ba23af249`, matching all 11 rows of `INDEX.csv`).
- **Per-Cluster Strict Margins (all strictly beating the live CCD table and polished CCD coordinates by `-0.027627 eV` to `-0.424275 eV`, well beyond the `1e-4 eV` threshold)**:
  1. **`Mo_75` (`N = 75`)**: `E* = -439.5640256673 eV` vs CCD `-439.4197932305 eV`, change **`-0.144232 eV`** (`-0.1442324368 eV`, `1442x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 1.23e-13`, Decimal50 `||grad E||_2 = 9.18e-28`).
  2. **`Mo_90` (`N = 90`)**: `E* = -533.2142178271 eV` vs CCD `-532.7899433214 eV`, change **`-0.424275 eV`** (`-0.4242745057 eV`, `4242x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 1.26e-13`, Decimal50 `||grad E||_2 = 1.20e-27`).
  3. **`Fe_86` (`N = 86`)**: `E* = -312.7609188697 eV` vs CCD `-312.6006513052 eV`, change **`-0.160268 eV`** (`-0.1602675645 eV`; float64 `||grad E||_2 = 2.36e-14`, Decimal50 `||grad E||_2 = 1.10e-28`).
  4. **`Fe_87` (`N = 87`)**: `E* = -316.6115843892 eV` vs CCD `-316.4759023549 eV`, change **`-0.135682 eV`** (`-0.1356820343 eV`; float64 `||grad E||_2 = 2.30e-14`, Decimal50 `||grad E||_2 = 9.84e-29`).
  5. **`Fe_90` (`N = 90`)**: `E* = -327.9864583540 eV` vs CCD `-327.8503707653 eV`, change **`-0.136088 eV`** (`-0.1360875887 eV`; float64 `||grad E||_2 = 2.86e-14`, Decimal50 `||grad E||_2 = 1.01e-28`).
  6. **`Fe_91` (`N = 91`)**: `E* = -332.0252838865 eV` vs CCD `-331.9072022873 eV`, change **`-0.118082 eV`** (`-0.1180815992 eV`; float64 `||grad E||_2 = 2.36e-14`, Decimal50 `||grad E||_2 = 1.01e-28`).
  7. **`Fe_92` (`N = 92`)**: `E* = -335.9470373457 eV` vs CCD `-335.9034309081 eV`, change **`-0.043606 eV`** (`-0.0436064376 eV`; float64 `||grad E||_2 = 2.76e-14`, Decimal50 `||grad E||_2 = 1.07e-28`).
  8. **`Fe_96` (`N = 96`)**: `E* = -351.2401491626 eV` vs CCD `-351.2027399452 eV`, change **`-0.037409 eV`** (`-0.0374092174 eV`; float64 `||grad E||_2 = 2.38e-14`, Decimal50 `||grad E||_2 = 1.14e-28`).
  9. **`Fe_97` (`N = 97`)**: `E* = -355.1385265715 eV` vs CCD `-354.9919830214 eV`, change **`-0.146544 eV`** (`-0.1465435501 eV`; float64 `||grad E||_2 = 2.76e-14`, Decimal50 `||grad E||_2 = 1.18e-28`).
  10. **`Fe_98` (`N = 98`)**: `E* = -359.0082985625 eV` vs CCD `-358.8031191667 eV`, change **`-0.205179 eV`** (`-0.2051793958 eV`; float64 `||grad E||_2 = 2.26e-14`, Decimal50 `||grad E||_2 = 1.00e-28`).
  11. **`Fe_100` (`N = 100`)**: `E* = -366.6082856510 eV` vs CCD `-366.5806583336 eV`, change **`-0.027627 eV`** (`-0.0276273174 eV`, `276x` the `1e-4 eV` threshold; float64 `||grad E||_2 = 2.64e-14`, Decimal50 `||grad E||_2 = 1.14e-28`).
- **Complete 196-Point-File Audit (`p1`)**: All 196 posted `FS_Mo` (`N = 3..100`) and `FS_Fe` (`N = 3..100`) point files are reproduced to 10 decimal places (within `9.77e-11 eV`) and Newton-polished in `object/fs_mo_fe_11_records_and_196_audit.json`, confirming that every posted CCD structure is already stationary within `1.9e-10 eV` and that all 11 new minima occupy genuinely distinct lower-energy basins.

pass: true
