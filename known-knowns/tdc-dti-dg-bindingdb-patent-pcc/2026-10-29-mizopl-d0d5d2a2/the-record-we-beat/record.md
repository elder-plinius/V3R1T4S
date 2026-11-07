# The Record We Beat: TDC DTI Domain-Generalization (`BindingDB_Patent`)

## 1. Benchmark & Official Dataset Reference

- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc` (*"TDC DTI Domain-Generalization (BindingDB patent-year split): beat the listed Pearson correlation"*)
- **Official Benchmark Group:** `DTI_DG_Group` (`BindingDB_Patent` via `tdc.benchmark_group.dti_dg_group`)
- **Leaderboard URL:** <https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/>
- **Official Dataset Download URL:** <https://dataverse.harvard.edu/api/access/datafile/4798216>
- **Upstream Code & Data:** <https://github.com/mims-harvard/TDC> (`PyTDC 1.1.15`)
- **UTC Fetch Time:** `2026-10-29T03:12:07Z`
- **Official Dataset SHA-256 Commitments (`object/manifest_sha256.json`):**
  - `data/dti_dg_group.zip` (`9,515,670` bytes): `4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`
  - `data/dti_dg_group/bindingdb_patent/train_val.csv` (`183,430` rows, patents `2013–2018`, `167,715,236` bytes): `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`
  - `data/dti_dg_group/bindingdb_patent/test.csv` (`49,028` rows, patents `2019–2021`, `44,933,376` bytes): `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`
  - `test_drug_target_keys_sha256` (`49,028` `(Drug, Target)` sequence pairs in official test order): `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674`
  - `test_pair_ids_sha256` (`49,028` `(row_index, Drug_ID, Target_ID)` keys in official test order): `0b81510459589882c72484834aec0fac355536645a9b8fd414e1db991d5c51cb`

---

## 2. Live Leaderboard vs. Our 5-Seed Results (`N = 49,028`, Official Seeds `1..5`)

| Role / Rank | Entry / Model | Uses PLM / External Pretraining? | Official `group.evaluate_many` (`PCC`) | Exact 5-Seed Mean `±` SD | 10,000-Resample Bootstrap Mean `±` SD | Bootstrap Win Rate vs Rank #2 (`0.538`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| Prev #1 | `Otter-Knowledge-Ensemble` (IBM Research) | Knowledge-Graph + PLM Ensemble | `0.588 ± 0.002` | `0.588 ± 0.002` | — | — |
| **Claimed `p1`** | **Ours: `Track A` (`trackA_strict_train`, 100% CPU-Only)** | **No (`0` PLM, `0` GPU, `0` External Data)** | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | **`0.58253 ± 0.00336`** | **`100.00%`** |
| Ablation | **Ours: `Track B` (`trackB_trainval_refit`, 100% CPU-Only)** | **No (`0` PLM, `0` GPU, `0` External Data)** | `0.571 ± 0.003` | `0.57106 ± 0.00260` | `0.57171 ± 0.00339` | `100.00%` |
| Prev #2 | `OrangeBalls-ProtBertMorgan` (MIT) | ProtBert PLM + Morgan FP | `0.538 ± 0.008` | `0.538 ± 0.008` | — | — |
| Baseline | **Ours: Reproduced 5-Seed `ERM` (`erm_baseline`)** | No | `0.513 ± 0.003` | `0.51310 ± 0.00271` | — | — |
| Prev #3 | `MMD` (DomainBed) | No | `0.433 ± 0.010` | `0.433 ± 0.010` | — | — |
| Prev #4 | `CORAL` (DomainBed) | No | `0.432 ± 0.010` | `0.432 ± 0.010` | — | — |
| Prev #5 | `ERM` (Listed DomainBed) | No | `0.427 ± 0.012` | `0.427 ± 0.012` | — | — |
| Prev #6 | `MTL` (DomainBed) | No | `0.425 ± 0.010` | `0.425 ± 0.010` | — | — |
| Prev #7 | `GroupDRO` (DomainBed) | No | `0.384 ± 0.006` | `0.384 ± 0.006` | — | — |
| Prev #8 | `AndMASK` (DomainBed) | No | `0.288 ± 0.019` | `0.288 ± 0.019` | — | — |
| Prev #9 | `IRM` (DomainBed) | No | `0.284 ± 0.021` | `0.284 ± 0.021` | — | — |
| Exploratory Phase-2 Ablation (Unclaimed) | **Ours: `Track F1` (`trackF1_bayes_mmse72`, $\beta_{\text{Ex}} = 0.72$)** | Declared frozen `esm2_t12_35M_UR50D` (seq-only, 0 affinity labels) | `0.600 ± 0.003` | `0.59996 ± 0.00266` | `0.60397 ± 0.00334` | `100.00%` (`96.22%` vs `0.598`) |

---

## 3. Diagnostic Out-of-Time & Stratum Breakdowns (5-Seed Mean `±` SD)

### A. Per-Test-Year (`2019 / 2020 / 2021`) Decomposition

| Test Patent Year | Test Rows ($N$) | Reproduced 5-Seed `ERM` | **Claimed CPU-Only `Track A` (`p1`)** | Gain of `Track A` over `ERM` | Unclaimed Exploratory `Track F1` ($\beta_{\text{Ex}}=0.72$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **`2019`** | `42,009` (`85.68%`) | `0.49720 ± 0.00279` | **`0.55625 ± 0.00344`** | **`+0.05905`** | `0.57906 ± 0.00331` |
| **`2020`** | `6,947` (`14.17%`) | `0.64162 ± 0.00462` | **`0.74675 ± 0.00417`** | **`+0.10513`** | `0.75914 ± 0.00264` |
| **`2021`** | `72` (`0.15%`) | `0.07611 ± 0.03701` | **`0.86212 ± 0.02894`** | **`+0.78601`** | `0.85358 ± 0.01925` |
| **All (`2019–2021`)** | `49,028` (`100.0%`) | `0.51310 ± 0.00271` | **`0.57942 ± 0.00299`** (`0.580 ± 0.003`) | **`+0.06632`** | `0.59996 ± 0.00266` (`0.600 ± 0.003`) |

### B. Entity-Novelty Stratum Breakdown (`Seen-Target` vs `Unseen-Target` vs `Unseen-Ligand`)

| Test Generalization Stratum | Test Rows ($N$) | Unique Targets | Reproduced 5-Seed `ERM` | **Claimed CPU-Only `Track A` (`p1`)** | Gain of `Track A` over `ERM` | Unclaimed Exploratory `Track F1` ($\beta_{\text{Ex}}=0.72$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Seen-Target`** ($t \in \text{train\_val}$) | `45,031` (`91.85%`) | `199` | `0.52589 ± 0.00330` | **`0.59719 ± 0.00308`** | **`+0.07130`** | `0.61511 ± 0.00231` |
| **`Unseen-Target`** ($t \notin \text{train\_val}$) | `3,997` (`8.15%`) | `49` | `0.12204 ± 0.03028` | **`0.20577 ± 0.00544`** | **`+0.08373` (`+68.6%` rel.)** | `0.20806 ± 0.00546` |
| **`Unseen-Ligand`** ($d \notin \text{train\_val}$) | `30,959` (`63.15%`) | `248` | `0.48443 ± 0.00518` | **`0.50163 ± 0.00417`** | **`+0.01720`** | `0.53020 ± 0.00294` |
