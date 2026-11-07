# Pre-Registered Permutation Null Test — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- `controls`: 500
- `best_control`: 0.022533
- `real`: 0.067577
- `command`: `sh verify-it-yourself/run_checks.sh`
- `real_beats_all_controls`: yes

## 1. Protocol (`B = 500` Residual Label Permutations, `seed = 20261107`)

To test whether the differential sensitivity signal on `BeatAML2` ($N = 19,823$ rows/split) and `PDX_Bruna` ($N = 1,046$ rows/split) exceeds finite-sample noise under DrEval's mean-effect normalization (`y_res = y - y_naive`), we ran $B = 500$ independent permutations of the residual vector (`seed = 20261107`) on Split 0 for both the unadjusted `SchurBilinearExVivoDRP` predictions and the cumulatively `p3`-adjusted predictions (`how-we-built-it/stage4_formalities_and_nulls.py`, stored in `object/certificate.json` under `null_permutation_tests`).

## 2. Ex Vivo Permutation Null Summary ($B = 500$ Controls, Split 0)

| Ex Vivo Cohort & Prediction Slice | Evaluated Rows ($N$) | Observed `Pearson_norm` (`real`) | Null Mean | Null SD | Max Null (`best_control`) | $Z$-Score | Controls Beaten | Empirical $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`BeatAML2` Unadjusted (`SchurBilinearExVivoDRP`, Split 0)** | `19,823` | **`+0.067577`** | `+0.000018` | `0.007155` | `+0.022533` | **`+9.44`** | **`500 / 500`** | **`0.001996`** |
| **`BeatAML2` Unlabeled `p3` Cumulative (`(i)+(ii)+(iii)`, Split 0)** | `19,823` | **`+0.228431`** | `+0.000087` | `0.007172` | `+0.031905` | **`+31.84`** | **`500 / 500`** | **`0.001996`** |
| **`PDX_Bruna` Unadjusted (`SchurBilinearExVivoDRP`, Split 0)** | `1,046` | **`+0.095517`** | `-0.001665` | `0.028535` | `+0.091245` | **`+3.41`** | **`500 / 500`** | **`0.001996`** |
| **`PDX_Bruna` Unlabeled `p3` Cumulative (`(i)+(ii)+(iii)`, Split 0)** | `1,046` | **`+0.351178`** | `-0.000737` | `0.031555` | `+0.086664` | **`+11.15`** | **`500 / 500`** | **`0.001996`** |
