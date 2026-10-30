# The Record We Beat — `dreval-exvivo-beataml2-pdx-transfer`

## 1. Upstream Benchmark & Archival Commitments

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- **Primary Upstream Table / Archive URL:** <https://zenodo.org/records/18770924>
- **Live DrEval Report URL:** <https://dilis-lab.github.io/drevalpy-report/CTRPv2_10CV/index.html>
- **Live DrEval Challenge Leaderboard URL:** <https://drevalpy.readthedocs.io/en/latest/leaderboard.html>
- **Zenodo Benchmark Record (`drevalpy v1.6.0` & `leaderboard_Oct26.zip`):** <https://zenodo.org/records/18770924> (alias <https://zenodo.org/records/23159774>)
- **UTC Fetch Timestamps:** `2026-10-29T16:10:00Z` and `2026-10-29T17:46:27Z`
- **Upstream Snapshot SHA-256 Commitments (`object/stage4_formalities_and_tanimoto_nulls.json`):**
  - Zenodo record metadata JSON (`https://zenodo.org/api/records/18770924`): `4ef3a4cad2537013b692fde090a99ee741ed2d51e286daf6b68543bbf2298d0b`
  - `daisybio/drevalpy` README (`https://raw.githubusercontent.com/daisybio/drevalpy/main/README.md`): `3f0e6e99c209b67685c312a4d36fa964dfbb3497463561684fe19fc00c120ac2`
  - `data/CTRPv2/CTRPv2.csv` ($372,469$ `LN_IC50_curvecurator` rows): `3069f5df0ffefeb2adeeb2ae4be2e0e43ff588154e3be2d414cfbd1224a7dc41`
  - `data/BeatAML2/BeatAML2.csv` ($23,040$ rows): `259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`
  - `data/PDX_Bruna/PDX_Bruna.csv` ($1,046$ rows): `63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`
  - `data/GDSC2/GDSC2.csv` ($162,758$ rows; $47,296$ overlapping test pairs): `a8d1a00043187b924937000c20a3a18fd9ebda85e22563434fc4cecb3de91645`

---

## 2. Comprehensive Comparison Across All 4 DrEval Targets

### A. In-Study `CTRPv2` (`LCO`, `LTO` [`p1`], and `LDO` [`seed=42` & `seed=1337`])

| Mode | Model / Baseline | `R2_norm` (Mean `±` SD) | `Pearson_norm` (Mean `±` SD) | `Spearman_norm` (Mean `±` SD) | `MSE` (Mean `±` SD) | Status vs Benchmark |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`LCO`** | **Ours: `SchurBilinearExVivoDRP`** | **`0.17153 ± 0.03581`** | **`0.41460 ± 0.04189`** | **`0.39156 ± 0.02707`** | **`1.57581 ± 0.13332`** | **Beats 2026 #1 `EnsembleMF` (`0.12694`) by `+0.04459` (`3.94x SE`)** |
| `LCO` | 2026 Leaderboard #1: `EnsembleMF` | `0.12694 ± 0.02096` | `0.37602 ± 0.03634` | `0.34479 ± 0.02581` | `1.65378 ± 0.12281` | Live 2026 Leaderboard #1 (`leaderboard_Oct26.zip`) |
| `LCO` | 2026 Report (`CTRPv2_10CV`): `RandomForest` | `0.09725` | `0.31279` | `0.28969` | `1.70996` | 2026 `splits.zip` RF baseline |
| `LCO` | Same-Env `drevalpy 1.6.0`: `RandomForest` (`p3`) | `-1.61938 ± 0.09241` | `0.01550 ± 0.02411` | `-0.00381 ± 0.02216` | `4.96536 ± 0.23354` | Documents `p3` default-grid reproducibility gap |
| **`LTO` (`p1`)** | **Ours: `SchurBilinearExVivoDRP`** | **`0.13453 ± 0.05062`** | **`0.36958 ± 0.06818`** | **`0.36409 ± 0.08017`** | **`1.68261 ± 0.15728`** | **Beats #1 `RandomForest` (`0.07279`) by `+0.06174` (`3.86x SE`, `p1` Win)** |
| `LTO` | Published #1 (`CTRPv2_10CV`): `RandomForest` | `0.07279` | `0.27386` | `0.25620` | `1.79634` | Previous best in `heatmap_algorithms_LTO_normalized` |
| `LTO` | Same-Env `drevalpy 1.6.0`: `RandomForest` | `-1.62853 ± 0.16107` | `0.01580 ± 0.03159` | `-0.00201 ± 0.03299` | `5.10796 ± 0.42781` | Same-environment default-grid re-run |
| **`LDO` (`seed=42`)** | **Ours: `SchurBilinearExVivoDRP`** | **`0.06006 ± 0.06930`** | **`0.34663 ± 0.11441`** | **`0.31772 ± 0.10955`** | **`5.59196 ± 1.07342`** | **Beats #1 `MultiOmicsNN` (`0.02347`) by `+0.03659`** |
| **`LDO` (`seed=1337`)** | **Ours: `SchurBilinearExVivoDRP`** | **`0.06857 ± 0.06323`** | **`0.35272 ± 0.08568`** | **`0.31837 ± 0.07928`** | **`5.54935 ± 1.05561`** | **Beats #1 `MultiOmicsNN` (`0.02347`) by `+0.04510` (`2.26x SE`, Full Win)** |
| `LDO` | Published #1 (`CTRPv2_10CV`): `MultiOmicsNN` | `0.02347` | `0.19320` | `0.18190` | `5.82000` | Previous best $R^2_{\text{norm}}$ in `heatmap_algorithms_LDO_normalized` |
| `LDO` | Same-Env `drevalpy 1.6.0`: `RandomForest` | `0.01022` / `0.01305` | `0.19732` / `0.21459` | `0.16742` / `0.18791` | `5.88725` / `5.89364` | Same-environment `seed=42` / `seed=1337` re-run |
| `LDO` | Same-Env `drevalpy 1.6.0`: `MultiOmicsNN` | `0.00789` / `0.01105` | `0.13066` / `0.15182` | `0.10744` / `0.12358` | `5.91025` / `5.90821` | Same-environment `seed=42` / `seed=1337` re-run |

---

### B. Ex Vivo (`BeatAML2`, `PDX_Bruna`) & Cross-Study (`GDSC2`) Transfer + `p3` Gap Closure

| Dataset / Stratum | Model / Decomposition Step | `R2_norm` (Mean `±` SD) | `Pearson_norm` (Mean `±` SD) | `Spearman_norm` (Mean `±` SD) | `MSE` | Within-Drug Cell Ranking (`r`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`BeatAML2` (16 Shared Drugs, $N=11,901$)** | **Ours: `SchurBilinearExVivoDRP` (Unadjusted)** | **`+0.01186 ± 0.00550`** (`10/10 > 0`) | **`+0.18519 ± 0.01894`** | **`+0.31010 ± 0.02263`** | **`13.7824`** | **`+0.0565` (`4.04x` vs `RF`)** |
| `BeatAML2` (16 Shared Drugs, $N=11,901$) | `RawPlatformKRR` (No Rank-Normal Alignment) | `-0.01449 ± 0.01071` | `+0.17229 ± 0.01606` | `+0.29668 ± 0.01760` | `14.1500` | `+0.0165` |
| `BeatAML2` (16 Shared Drugs, $N=11,901$) | `NaiveMeanEffectsPredictor` | `-0.05660 ± 0.00441` | `0.00000` | `0.00000` | `14.7147` | `0.0000` |
| `BeatAML2` (`p3` Step 4: Offset+Shared+`<=10`) | **Ours: `SchurBilinearExVivoDRP` (`p3` Closed)** | **`+0.08370 ± 0.00982`** | **`+0.29125 ± 0.01930`** | **`+0.31113 ± 0.02162`** | **`6.4743`** | **`+0.0565`** |
| **`PDX_Bruna` (All Drugs, $N=1,046$)** | **Ours: `SchurBilinearExVivoDRP` / `RawPlatformKRR`** | `-0.39248` / **`-0.18939`** | **`+0.10046` / `+0.21946`** | **`+0.20912` / `+0.26101`** | `15.8705` / `13.5558` | `+0.0442` |
| `PDX_Bruna` (All Drugs, $N=1,046$) | Same-Env `RandomForest` | `-0.29623 ± 0.02581` | `+0.07715 ± 0.04996` | `+0.18460 ± 0.06808` | `14.7738` | `-0.0031` |
| `PDX_Bruna` (Unseen Drugs, $N=491$) | **Ours: `SchurBilinearExVivoDRP` (Unadjusted)** | `-0.61942 ± 0.03298` | **`+0.34738 ± 0.03324`** | **`+0.43627 ± 0.02941`** | `19.9977` | `+0.0812` |
| `PDX_Bruna` (`p3` Step 2: Offset+Slope Aligned) | **Ours: `SchurBilinearExVivoDRP` (`p3` Closed)** | **`+0.00643 ± 0.00633`** | **`+0.10046 ± 0.01842`** | **`+0.20912 ± 0.00905`** | **`11.3240`** | `+0.0442` |
| **`GDSC2` (All Drugs, $N=47,296$)** | **Ours: `SchurBilinearExVivoDRP` (Unadjusted)** | **`-0.42457 ± 0.02711`** (`+0.1586` vs `RF`) | **`+0.13294 ± 0.01253`** | **`+0.17419 ± 0.00773`** | **`6.3810`** | **`+0.3515` (`2.40x` vs `RF`)** |
| `GDSC2` (All Drugs, $N=47,296$) | Same-Env `RandomForest` | `-0.58316 ± 0.04199` | `+0.10796 ± 0.02580` | `+0.13807 ± 0.01763` | `7.0914` | `+0.1462` |
| `GDSC2` (All Drugs, $N=47,296$) | Same-Env `GradientBoosting` | `-0.60662 ± 0.04877` | `+0.07257 ± 0.02736` | `+0.09062 ± 0.01918` | `7.1965` | `+0.0888` |
| `GDSC2` (`p3` Step 2: Offset+Slope Aligned) | **Ours: `SchurBilinearExVivoDRP` (`p3` Closed)** | **`-0.00124 ± 0.00758`** (`+0.4233` gain) | **`+0.13294 ± 0.01253`** | **`+0.17419 ± 0.00773`** | **`4.4849`** | **`+0.3515`** |
