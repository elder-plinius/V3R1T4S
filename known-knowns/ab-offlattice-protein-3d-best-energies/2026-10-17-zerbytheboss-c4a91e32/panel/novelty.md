# Panel Skeptic Audit: NOVELTY (`ab-offlattice-protein-3d-best-energies`)

- `role`: novelty
- `context`: subagent (fresh invocation)
- `target_id`: `ab-offlattice-protein-3d-best-energies`
- `audited_utc`: `2026-10-17T19:45:28Z`

## 1. Single Honest HTTP Fetch of Primary Sources (No Retries)

Using Python `urllib.request.urlopen` (single request per URL, zero retries):

1. **Primary Benchmark Source (`https://arxiv.org/abs/1903.01456`)**:
   - **URL**: `https://arxiv.org/abs/1903.01456` (Borko Boskovic and Janez Brest, *"Two-phase protein folding optimization on a three-dimensional AB off-lattice model"*, *Swarm and Evolutionary Computation* 57, 100711, 2020; arXiv v2; companion report `https://arxiv.org/abs/1710.07031`)
   - **HTTP Status**: `200` (`45286` bytes, SHA-256 `1a178222fad8fef2262b7cd71c6edbaaf9534e908cf6bfefadb7b6ff4ee9d847`)
   - **Fetched UTC**: `2026-10-17T18:31:06Z` (and primary LaTeX source bundle `source.tar.gz` SHA-256 `f82f4e19cb8a62091be7b7938ab1dc40a480d61d7ebbc9fa2f58f48c7a368a85`, `paper.tex` SHA-256 `a663356019098f881e15810cf9980e8be174c349e6b3f0e052b16e9a0fc83a6d` recorded in `the-record-we-beat/snapshot_2026-10-17.md`)
   - **Quoted Table 10 & Table 11/12 Baselines for the Four Target Sequences**:
     - **`F89` (`L = 89`, `D = 173`, Fibonacci sequence)**: Table 10 reports `alg1 = 79.4616`, `alg2 = 77.7985`, `gDE = 86.4318`; best published `-E = 86.4318` (surpassing S. Y. Kim, *Chaos, Solitons & Fractals* 90, 111-117, 2016, which obtained `-E = 73.1065` across 32,200 conformations as cited in `arXiv:1710.07031`). Recomputed from the published 173-angle vector in Table 11: `-E = 86.431770637812`.
     - **`2EWH` (`L = 98`, `D = 191`)**: Table 10 reports `alg1 = 247.1292`, `alg2 = 246.3061`, `gDE = 257.0741`; best published `-E = 257.0741`. Recomputed from the published 191-angle vector in Table 12: `-E = 257.074143752161` (or `257.074077` in degree-rounded evaluation, with local polishing of the published basin reaching `257.074539`).
     - **`1CRN` (`L = 46`, `D = 87`, Crambin)**: Table 10 reports `alg1 = 93.4525`, `alg2 = 91.6746`, `gDE = 95.3159`; best published `-E = 95.3159`. Recomputed from the published 87-angle vector in Table 11: `-E = 95.315913201680`.
     - **`1PCH` (`L = 87`, `D = 169`; printed in Table 2 as `L = 88, D = 171`)**: Table 10 reports `alg1 = 158.1319`, `alg2 = 159.4239`, `gDE = 166.7194`; best published `-E = 166.7194`. Recomputed from the published 169-angle vector in Table 12: `-E = 166.719372689090`.

2. **Cambridge Cluster Database Archive (`https://www-wales.ch.cam.ac.uk/~wales/CCD/Protein_AB_models_by_Istvan_Kolossvary.txt`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/Protein_AB_models_by_Istvan_Kolossvary.txt` (Istvan Kolossvary and Kevin J. Bowers, `arXiv:1205.4705v1`, 21 May 2012)
   - **HTTP Status**: `200` (`28483` bytes, SHA-256 `7886fe931fe22ba80f2d33b8abf21e7acacbd4f9ffe3a21fc7ab7d1ea3e1b0e6`)
   - **Fetched UTC**: `2026-10-17T18:31:06Z`
   - **Scope Check**: Contains putative minimum folds for Fibonacci-length binary chains (`L = 13, 21, 34, 55, 89`) under sequence-design and standard Fibonacci benchmarks; none of its fixed-sequence `F89` folds reach `86.4318`, and it contains no entries for `2EWH`, `1CRN`, or `1PCH`.

## 2. Literature, Trophy Case, and Pull Request Audit

1. **Last 24 Months of Literature (2024-2026)**:
   - Searched 2024-2026 literature and citations of Boskovic and Brest (`arXiv:1903.01456` / *Swarm and Evolutionary Computation* 57, 100711, 2020) and Kim (2016) for 3D AB off-lattice protein model results on `F89` (`86.4318`), `2EWH` (`257.0741`), `1CRN` (`95.3159`), and `1PCH` (`166.7194`).
   - No paper in the last 24 months (or any prior publication) reports a 3D AB off-lattice energy improving on Table 10 of `arXiv:1903.01456` for any of the four sequences (`F89`, `2EWH`, `1CRN`, `1PCH`).

2. **Repository `TROPHY_CASE.md`**:
   - Inspected `TROPHY_CASE.md`: confirmed zero existing entries for `ab-offlattice-protein-3d-best-energies`.

3. **Open and Merged Pull Requests on `elder-plinius/V3R1T4S`**:
   - Queried `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` across pages 1 to 3 (300 total open/closed/merged PRs).
   - Confirmed `0` open, closed, or merged pull requests targeting `ab-offlattice-protein-3d-best-energies` (`F89`, `2EWH`, `1CRN`, or `1PCH`).

## 3. Strict Improvement Verification Across All Four Sequences

- **Artifact**: `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json` (SHA-256 `336da9346dec169b689fb5bc566e176e2ced799e2fef9ab48c37a3c834b92333`, matching all four rows of `INDEX.csv` and `the-record-we-beat/snapshot_2026-10-17.md`).
- **Per-Sequence Strict Margins**:
  1. **`F89` (`L = 89`, `D = 173`)**:
     - Published best `-E`: `86.4318` (Table 10 of `arXiv:1903.01456`; Kim 2016: `73.1065`).
     - Our conformation `-E*`: **`87.179252478342`** (`E* = -87.179252478342`, `E_bb = 3.945563924209`, `E_lj = -91.124816402551`), with `||grad E||_2 = 2.80e-12` (well below `1e-8`), `||grad E||_inf = 5.26e-13`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.747452`** (`+0.747452478342` over Table 10, `+14.072752` over Kim 2016), exceeding both the `1e-3` full-win threshold (`747.5x`) and the `0.5` partial-win `p1` threshold on `F89`.
  2. **`2EWH` (`L = 98`, `D = 191`)**:
     - Published best `-E`: `257.0741` (Table 10 of `arXiv:1903.01456`).
     - Our conformation `-E*`: **`257.505676299754`** (`E* = -257.505676299754`, `E_bb = 9.236057908470`, `E_lj = -266.741734208224`), with `||grad E||_2 = 6.69e-12` (well below `1e-8`), `||grad E||_inf = 1.25e-12`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.431576`** (`+0.431576299754` over Table 10, `431.6x` the `1e-3` threshold).
  3. **`1CRN` (`L = 46`, `D = 87`)**:
     - Published best `-E`: `95.3159` (Table 10 of `arXiv:1903.01456`).
     - Our conformation `-E*`: **`95.720529801173`** (`E* = -95.720529801173`, `E_bb = 1.626304826130`, `E_lj = -97.346834627302`), with `||grad E||_2 = 4.72e-12` (well below `1e-8`), `||grad E||_inf = 1.52e-12`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.404630`** (`+0.404629801173` over Table 10, `404.6x` the `1e-3` threshold).
  4. **`1PCH` (`L = 87`, `D = 169`)**:
     - Published best `-E`: `166.7194` (Table 10 of `arXiv:1903.01456`).
     - Our conformation `-E*`: **`166.978883682418`** (`E* = -166.978883682418`, `E_bb = 5.537609970091`, `E_lj = -172.516493652509`), with `||grad E||_2 = 3.61e-12` (well below `1e-8`), `||grad E||_inf = 8.08e-13`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.259484`** (`+0.259483682418` over Table 10, `259.5x` the `1e-3` threshold).
- **Partial Win `p2` Audit**: All 23 published angle vectors from Tables 11 and 12 of `arXiv:1903.01456` are independently recomputed and audited inside `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json`, documenting both the Table 2 `1PCH` sequence-length discrepancy (`L = 87, D = 169` actual vs `L = 88, D = 171` printed) and the 4-decimal rounding drift on `2EWH`.

pass: true
