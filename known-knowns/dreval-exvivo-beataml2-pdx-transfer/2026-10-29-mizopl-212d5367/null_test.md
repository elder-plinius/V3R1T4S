# Pre-Registered Permutation Null Test — `dreval-exvivo-beataml2-pdx-transfer`

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- `controls`: 500
- `best_control`: 0.019002
- `real`: 0.067582
- `command`: `sh verify-it-yourself/run_checks.sh`
- `real_beats_all_controls`: yes

## 1. Protocol (`B = 500` Residual Label Permutations, `seed = 20261029`)

To verify that the differential sensitivity signal captured by `SchurBilinearExVivoDRP` is not a finite-sample or normalization artifact, we executed $B = 500$ independent permutations of the residual response $y_{\text{true}} - y_{\text{naive}}$ (`seed = 20261029`) through the exact DrEval `_normalize_metrics_by_mean_effects` evaluation pipeline (`object/stage4_formalities_and_tanimoto_nulls.json`).

- **Summary for `dreval-exvivo-beataml2-pdx-transfer`:** BeatAML2 all-drugs Pearson_norm = +0.067582 vs max null +0.019002 (Z = +9.93, 500/500 controls); BeatAML2 shared-drugs R2_norm = +0.011860 +- 0.005503 (10/10 splits > 0, Pearson_norm = +0.185192); PDX_Bruna Spearman_norm = +0.209123 (500/500 controls) and unseen-drug Pearson_norm = +0.347380

## 2. Full Campaign Null Distribution Table ($B = 500$ Controls)

| Dataset / Mode | Observed `Pearson_norm` | Null Mean | Null SD | Max Null (`best_control`) | $Z$-Score | Controls Beaten | Empirical $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`CTRPv2 LCO` (Split 0, $N=22,119$)** | **`+0.474509`** (`10-split: +0.414604`) | `-0.000105` | `0.002083` | `+0.005945` | **`+199.13`** | **`500 / 500`** | **`0.001996`** |
| **`CTRPv2 LTO` (`p1`, Split 0, $N=21,496$)** | **`+0.391065`** (`10-split: +0.369581`) | `-0.000041` | `0.002139` | `+0.007473` | **`+172.81`** | **`500 / 500`** | **`0.001996`** |
| **`CTRPv2 LDO` (`seed=42`, Split 0, $N=21,981$)** | **`+0.440812`** (`10-split: +0.346633`) | `-0.000038` | `0.002190` | `+0.007319` | **`+158.34`** | **`500 / 500`** | **`0.001996`** |
| **`CTRPv2 LDO` (`seed=1337`, Split 0, $N=21,815$)** | **`+0.371264`** (`10-split: +0.352715`) | `+0.000051` | `0.002249` | `+0.006236` | **`+156.79`** | **`500 / 500`** | **`0.001996`** |
| **`BeatAML2` (Ex Vivo AML, $N=23,040$)** | **`+0.067582`** (`shared: +0.185192`) | `-0.000049` | `0.006811` | `+0.019002` | **`+9.93`** | **`500 / 500`** | **`0.001996`** |
| **`GDSC2` (Cross-Study, $N=47,296$)** | **`+0.140331`** (`10-split: +0.132939`) | `-0.000047` | `0.005088` | `+0.014744` | **`+27.59`** | **`500 / 500`** | **`0.001996`** |
