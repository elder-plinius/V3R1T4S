# Novelty Audit (`ab-offlattice-protein-3d-best-energies`)

- Context: independent novelty audit
- Target: `ab-offlattice-protein-3d-best-energies`
- Audited UTC: `2026-11-06`

## 1. Primary Benchmark Source (`https://arxiv.org/abs/1903.01456`)

1. **Primary Benchmark Source (`https://arxiv.org/abs/1903.01456`)**:
   - **URL**: `https://arxiv.org/abs/1903.01456` (Borko Bošković and Janez Brest, *"Two-phase protein folding optimization on a three-dimensional AB off-lattice model"*, *Swarm and Evolutionary Computation* 57, 100708, 2020, `doi:10.1016/j.swevo.2020.100708`; arXiv v2 source bundle `https://arxiv.org/e-print/1903.01456v2` sha256 `c82a906c10c98416c0d6deb490985fa80845791e0cb6f9c63d345a2ffef53ae1`, `paper.tex` sha256 `997f641bd85f77f103e5d5c0c525cf47c71dad0030a25c571c22207647c0f769`, PDF `https://arxiv.org/pdf/1903.01456` sha256 `17e9dce895fe982a6a1b1578548e2dc081a4f1958d7a5de9e56c88f5fbb51fda`).
   - **Table 10 (`\label{tab:best:energies}`) Quoted As Printed**:
     Table 10 compares four columns (`DE2P`, `DElscr` from Bošković & Brest 2018 `doi:10.1016/j.ins.2018.04.072`, `SGDE` from Rakhshani et al. 2019 `doi:10.1016/j.swevo.2019.01.009`, and `BE-ABC` from Li et al. 2015 `doi:10.1109/CEC.2015.7257119`):
     - **`F89` (`L = 89`, `D = 173`, Fibonacci sequence)**: `DE2P = 86.4318`, `DElscr = 83.5761`, `SGDE = -` (none), `BE-ABC = -` (none). (Table 9 4-day run reports `DE2P = 86.4318`, `DElscr = 81.5297`; S. Y. Kim, *Chaos, Solitons & Fractals* 90, 111-117, 2016, `doi:10.1016/j.chaos.2016.04.010`, covers `F89` only and reports `-E = 73.1065` across 32,200 conformations.) Recomputed from the published 173-angle vector in Table 11: `-E = 86.431770637812`.
     - **`2EWH` (`L = 98`, `D = 191`)**: `DE2P = 257.0741`, `DElscr = 245.5193` (`245.5190` in Table 9), `SGDE = 201.0500`, `BE-ABC = 146.8231`. Recomputed from the published 191-angle vector in Table 12: `-E = 257.074143752161`.
     - **`1CRN` (`L = 46`, `D = 87`, Crambin)**: `DE2P = 95.3159`, `DElscr = 92.9853`, `SGDE = 78.2451`, `BE-ABC = 54.7253`. Recomputed from the published 87-angle vector in Table 11: `-E = 95.315913201680`.
     - **`1PCH` (`L = 87`, `D = 169`; printed in Table 2 and Table 10 as `L = 88`)**: `DE2P = 166.7194`, `DElscr = 156.5252` (`156.5250` in Table 9), `SGDE = -` (none), `BE-ABC = 91.3508`. Recomputed from the published 169-angle vector in Table 12: `-E = 166.719372689090`.

2. **Cambridge Cluster Database Archive (`https://www-wales.ch.cam.ac.uk/~wales/CCD/Protein_AB_models_by_Istvan_Kolossvary.txt`)**:
   - **URL**: `https://www-wales.ch.cam.ac.uk/~wales/CCD/Protein_AB_models_by_Istvan_Kolossvary.txt` (Istvan Kolossváry and Kevin J. Bowers, `arXiv:1205.4705v1`, 21 May 2012, SHA-256 `7886fe931fe22ba80f2d33b8abf21e7acacbd4f9ffe3a21fc7ab7d1ea3e1b0e6`).
   - **Scope Check**: Uses an incompatible modified model variant; contains no entries for `2EWH`, `1CRN`, or `1PCH`, and none of its fixed-sequence `F89` entries reach `86.4318`.

## 2. Later Papers Checked on the 3D AB Off-Lattice Model

We checked the citing literature of Bošković and Brest (`doi:10.1016/j.swevo.2020.100708` / `arXiv:1903.01456` and `doi:10.1016/j.ins.2018.04.072` / `arXiv:1710.07031`) via OpenAlex, Crossref, and arXiv through `2026-11-06`:

| Source (Authors, Year, Identifier) | Algorithm | `F89` (`L=89`) `-E` | `2EWH` (`L=98`) `-E` | `1CRN` (`L=46`) `-E` | `1PCH` (`L=87`) `-E` |
|---|---|---:|---:|---:|---:|
| S. Y. Kim (2016), *Chaos, Solitons & Fractals* 90, 111-117, `doi:10.1016/j.chaos.2016.04.010` | CSA | `73.1065` | none | none | none |
| B. Li, R. Chiong, M. Lin (2015), *IEEE CEC*, `doi:10.1109/CEC.2015.7257119` (Table 10 `BE-ABC`) | BE-ABC | none | `146.8231` | `54.7253` | `91.3508` |
| B. Bošković, J. Brest (2018), *Inf. Sci.* 454-455, 178-199, `doi:10.1016/j.ins.2018.04.072` / `arXiv:1710.07031` (Table 10 `DElscr`) | DElscr | `83.5761` | `245.5193` | `92.9853` | `156.5252` |
| H. Rakhshani et al. (2019), *Swarm Evol. Comput.* 50, 100503, `doi:10.1016/j.swevo.2019.01.009` (Table 10 `SGDE`) | SGDE | none | `201.0500` | `78.2451` | none |
| B. Bošković, J. Brest (2020), *Swarm Evol. Comput.* 57, 100708, `doi:10.1016/j.swevo.2020.100708` / `arXiv:1903.01456` (Table 10 `DE2P`) | DE2P | `86.4318` | `257.0741` | `95.3159` | `166.7194` |
| P. H. Narloch, R. S. Parpinelli (2020), *WSCAD 2020*, `doi:10.5753/wscad.2020.14080` & (2021) *Concurr. Comput. Pract. Exp.* 33(23), e6745, `doi:10.1002/cpe.6745` | cuDSMjDE | none | `257.3538` (no angles published) | `94.5862` | `164.0593` |
| B. S. Yildiz et al. (2023), *IJACSA* 14(3), 400-405, `doi:10.14569/ijacsa.2023.0140345` | ELAMO | none (`N <= 34` only) | `146.81` | none | none |
| **This package (`object/ab_3d_records_F89_2EWH_1CRN_1PCH.json`)** | **$C^2$ Homotopy + $S^2\times S^1$ Polish** | **`87.179252`** | **`257.505676`** | **`95.720530`** | **`166.978884`** |

## 3. Strict Improvement Verification Across All Four Sequences

- **Artifact**: `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json` (SHA-256 `fe7774733af39f0e5195f23d2f0255a8d7e919b007b2e50d6995c6fc6f71c124`, matching all four rows of `INDEX.csv` and `the-record-we-beat/snapshot_2026-10-17.md`).
- **Per-Sequence Strict Margins**:
  1. **`F89` (`L = 89`, `D = 173`)**:
     - Published best `-E`: `86.4318` (Table 10 `DE2P` of `arXiv:1903.01456`; `DElscr = 83.5761`; Kim 2016: `73.1065`).
     - Our conformation `-E*`: **`87.179252478342`** (`E* = -87.179252478342`, `E_bb = 3.945563924209`, `E_lj = -91.124816402551`), with `||grad E||_2 = 2.801e-12` (well below `1e-8`), `||grad E||_inf = 5.256e-13`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.747452`** (`+0.747452478342` over Table 10, `+14.072752` over Kim 2016), exceeding both the `1e-3` full-win threshold (`747.5x`) and the `0.5` partial-win `p1` threshold on `F89`.
  2. **`2EWH` (`L = 98`, `D = 191`)**:
     - Published best `-E`: `257.0741` in Table 10 of `arXiv:1903.01456` (and `257.3538` without published angles in Narloch & Parpinelli 2020 `doi:10.5753/wscad.2020.14080`).
     - Our conformation `-E*`: **`257.505676299754`** (`E* = -257.505676299754`, `E_bb = 9.236057908470`, `E_lj = -266.741734208224`), with `||grad E||_2 = 6.688e-12` (well below `1e-8`), `||grad E||_inf = 1.249e-12`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.431576`** over Table 10 (`+0.151876` over Narloch & Parpinelli 2020).
  3. **`1CRN` (`L = 46`, `D = 87`)**:
     - Published best `-E`: `95.3159` (Table 10 `DE2P` of `arXiv:1903.01456`).
     - Our conformation `-E*`: **`95.720529801173`** (`E* = -95.720529801173`, `E_bb = 1.626304826130`, `E_lj = -97.346834627302`), with `||grad E||_2 = 4.718e-12` (well below `1e-8`), `||grad E||_inf = 1.519e-12`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.404630`** (`+0.404629801173` over Table 10).
  4. **`1PCH` (`L = 87`, `D = 169`)**:
     - Published best `-E`: `166.7194` (Table 10 `DE2P` of `arXiv:1903.01456`).
     - Our conformation `-E*`: **`166.978883682418`** (`E* = -166.978883682418`, `E_bb = 5.537609970091`, `E_lj = -172.516493652509`), with `||grad E||_2 = 3.606e-12` (well below `1e-8`), `||grad E||_inf = 8.080e-13`, and max bond length error `2.22e-16`.
     - Strict gain: **`+0.259484`** (`+0.259483682418` over Table 10).

pass: true
