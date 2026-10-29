# The Record We Beat: TDC DTI Domain-Generalization (`BindingDB_Patent`)

## 1. Benchmark & Source Reference

- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc` (*"TDC DTI Domain-Generalization (BindingDB patent-year split): beat the listed Pearson correlation"*)
- **Official Benchmark Group:** `DTI_DG_Group` (`BindingDB_Patent` via `tdc.benchmark_group.dti_dg_group`)
- **Leaderboard URL:** <https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/>
- **Upstream Code & Data:** <https://github.com/mims-harvard/TDC> (`PyTDC 1.1.15`)
- **UTC Fetch Time:** `2026-10-29T03:12:07Z`
- **Official Dataset SHA-256 Commitments (`object/manifest_sha256.json`):**
  - `data/dti_dg_group.zip`: `4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`
  - `data/dti_dg_group/bindingdb_patent/train_val.csv` ($183,430$ rows, patents from `2013–2018`): `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`
  - `data/dti_dg_group/bindingdb_patent/test.csv` ($49,028$ rows, patents from `2019–2021`): `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`
  - `test_drug_target_keys_sha256` (`49,028` `(Drug, Target)` pairs in official test order): `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674`

---

## 2. Live Leaderboard vs. Our Certified 5-Seed Results

### A. Overall Pooled Test Performance (`N = 49,028`, Official Seeds `1..5`)

| Rank / Track | Entry / Model | Uses PLM / External Pretraining? | Official `group.evaluate_many` (`PCC`) | Exact 5-Seed Mean `±` SD | 10,000-Resample Bootstrap Mean `±` SD | Bootstrap Win Rate vs Rank #2 (`0.538`) | Bootstrap Win Rate vs Rank #1 (`0.588`) | Bootstrap Win Rate vs Full Win (`0.598`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **NEW #1 (Full Win)** | **Ours: `Track F2` (`trackC_fullwin`, $\beta_{\text{Ex}} = 0.75$)** | Declared frozen `esm2_t12_35M_UR50D` (seq-only, 0 affinity labels) | **`0.600 ± 0.003`** | **`0.60018 ± 0.00266`** | **`0.60393 ± 0.00333`** | **`100.00%`** | **`100.00%`** | **`96.17%`** |
| **NEW #1b (Full Win)** | **Ours: `Track F1` ($\beta_{\text{Ex}} = 0.72$)** | Declared frozen `esm2_t12_35M_UR50D` (seq-only, 0 affinity labels) | **`0.600 ± 0.003`** | **`0.59996 ± 0.00266`** | **`0.60397 ± 0.00334`** | **`100.00%`** | **`100.00%`** | **`96.22%`** |
| — | **Ours: `Track D2` (`Step 14` Full-Horizon Stacker + `C1_esm6`)** | Declared frozen `esm2_t12_35M_UR50D` | **`0.588 ± 0.003`** | **`0.58841 ± 0.00243`** | `0.59114 ± 0.00338` | `100.00%` | `82.67%` | `2.15%` |
| Prev #1 | `Otter-Knowledge-Ensemble` (IBM Research) | Knowledge-Graph + PLM Ensemble | `0.588 ± 0.002` | `0.588 ± 0.002` | — | — | — | — |
| **NEW #2 (`p1` Win)** | **Ours: `Track A` (`strict_train_s`, 100% CPU-Only)** | **No (`0` PLM, `0` GPU, `0` External Data)** | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | **`0.58253 ± 0.00336`** | **`100.00%`** | `5.32%` | `0.00%` |
| — | **Ours: `Track B` (`train_val` Refit, 100% CPU-Only)** | **No (`0` PLM, `0` GPU, `0` External Data)** | **`0.571 ± 0.003`** | **`0.57106 ± 0.00259`** | `0.57171 ± 0.00339` | **`100.00%`** | `0.00%` | `0.00%` |
| Prev #2 | `OrangeBalls-ProtBertMorgan` (MIT) | ProtBert PLM + Morgan FP | `0.538 ± 0.008` | `0.538 ± 0.008` | — | — | — | — |
| Baseline | **Ours: Reproduced 5-Seed `ERM` Baseline** | No | `0.513 ± 0.003` | `0.51310 ± 0.00270` | — | — | — | — |
| Prev #3 | `MMD` (DomainBed) | No | `0.433 ± 0.010` | `0.433 ± 0.010` | — | — | — | — |
| Prev #4 | `CORAL` (DomainBed) | No | `0.432 ± 0.010` | `0.432 ± 0.010` | — | — | — | — |
| Prev #5 | `ERM` (Listed DomainBed) | No | `0.427 ± 0.012` | `0.427 ± 0.012` | — | — | — | — |
| Prev #6 | `MTL` (DomainBed) | No | `0.425 ± 0.010` | `0.425 ± 0.010` | — | — | — | — |
| Prev #7 | `GroupDRO` (DomainBed) | No | `0.384 ± 0.006` | `0.384 ± 0.006` | — | — | — | — |
| Prev #8 | `AndMASK` (DomainBed) | No | `0.288 ± 0.019` | `0.288 ± 0.019` | — | — | — | — |
| Prev #9 | `IRM` (DomainBed) | No | `0.284 ± 0.021` | `0.284 ± 0.021` | — | — | — | — |

---

### B. Partial Win `p2` — Per-Test-Year (`2019 / 2020 / 2021`) Domain-Shift Decomposition (5-Seed Mean `±` SD)

| Test Patent Year | Test Rows ($N$) | Reproduced 5-Seed `ERM` | **Our CPU-Only `Track A` (`p1`)** | **Our Full-Win `Track F2` (`trackC_fullwin`)** | Gain of `Track F2` over `ERM` |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **`2019`** | `42,009` (`85.68%`) | `0.49720 ± 0.00278` | **`0.55625 ± 0.00344`** | **`0.57930 ± 0.00331`** | **`+0.08210`** |
| **`2020`** | `6,947` (`14.17%`) | `0.64163 ± 0.00460` | **`0.74675 ± 0.00416`** | **`0.75931 ± 0.00264`** | **`+0.11768`** |
| **`2021`** | `72` (`0.15%`) | `0.07611 ± 0.03700` | **`0.86212 ± 0.02894`** (`Track B: 0.93419`) | **`0.85358 ± 0.01926`** | **`+0.77747`** |
| **All (`2019–2021`)** | `49,028` (`100.0%`) | `0.51310 ± 0.00270` | **`0.57942 ± 0.00299`** (`0.580 ± 0.003`) | **`0.60018 ± 0.00266`** (`0.600 ± 0.003`) | **`+0.08708`** |

---

### C. Partial Win `p3` & Generalization Stratum Breakdown (`Seen-Target` vs `Unseen-Target` vs `Unseen-Ligand`)

| Test Generalization Stratum | Test Rows ($N$) | Unique Targets | Reproduced 5-Seed `ERM` | **Our CPU-Only `Track A` (`p1`)** | **Our Full-Win `Track F2` (`trackC_fullwin`)** | Gain of `Track F2` over `ERM` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Seen-Target`** ($t \in \text{train\_val}$) | `45,031` (`91.85%`) | `199` | `0.52590 ± 0.00328` | **`0.59719 ± 0.00307`** | **`0.61533 ± 0.00231`** (`Seed 3: 0.61769`) | **`+0.08943`** |
| **`Unseen-Target` (`p3`, $t \notin \text{train\_val}$)** | `3,997` (`8.15%`) | `49` | `0.12204 ± 0.03027` | **`0.20577 ± 0.00543`** (`Track B: 0.20932`) | **`0.20806 ± 0.00546`** (`Seed 3: 0.21430`) | **`+0.08602` (`+70.5%` rel.)** |
| **`Unseen-Ligand`** ($d \notin \text{train\_val}$) | `30,959` (`63.15%`) | `248` | `0.48444 ± 0.00516` | **`0.50163 ± 0.00417`** | **`0.53020 ± 0.00294`** (`Seed 3: 0.53343`) | **`+0.04576`** |
