# Verification Receipts — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- **Package ID:** `2026-11-07-mizopl-d1d47e16`
- **Verified UTC Timestamp:** `2026-11-07T16:25:00Z`
- **Verification Command:** `sh verify-it-yourself/run_checks.sh`

## 1. Upstream Dataset Citations & SHA-256 Digests (Replacing Copied `y` Columns in `object/*.csv`)

Per reviewer guidance, no ground-truth response column (`y` / `LN_IC50_curvecurator`) is copied into `object/*.csv`. Instead, all 30 per-split prediction CSVs (`object/beataml2_split_{0..9}_{schur,base}.csv` and `object/pdx_bruna_split_{0..9}.csv`) are keyed by `(split, cell_line_name, drug_name, pubchem_id)` against the official `drevalpy` benchmark archive on Zenodo (`https://zenodo.org/records/14974099`):

| Upstream File | Official Zenodo Download URL | SHA-256 Digest | Evaluated Rows / Split |
| :--- | :--- | :--- | :--- |
| `BeatAML2/BeatAML2.csv` | `https://zenodo.org/records/14974099/files/BeatAML2.zip?download=1` | `259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9` | `19,823` (`484` AML patients $\times$ `154` drugs: `79` shared [`11,901` rows], `75` unseen [`7,922` rows]) |
| `PDX_Bruna/PDX_Bruna.csv` | `https://zenodo.org/records/14974099/files/PDX_Bruna.zip?download=1` | `63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4` | `1,046` (`25` breast PDX models $\times$ `100` drugs: `49` shared [`555` rows], `51` unseen [`491` rows]) |
| `CTRPv2/CTRPv2.csv` | `https://zenodo.org/records/14974099/files/CTRPv2.zip?download=1` | `3069f5df0ffefeb2adeeb2ae4be2e0e43ff588154e3be2d414cfbd1224a7dc41` | `372,469` training response rows across `776` cell lines and `545` drugs |
| `CTRPv2/splits.zip` | `https://zenodo.org/records/14974099/files/CTRPv2.zip?download=1` | `28dfdd7dca4ea5d2ca7da1ea0f53bb2eb149bd150bfabbf47cd9f1f145fd5839` | `10` official cross-validation splits (`cv_split_0` .. `cv_split_9`) |

## 2. Primary Object Digests

- `object/certificate.json`: `d1d47e161a4d025e732817e75adbcc7a06bf258e1695c2d5800ed781e74e2025` (`255609` bytes)
- `object/stage3_p3_gap_decomposition.json`: `d29f8337f60ef6a9d372a3b744892547c66f35071ce20016a297fe6f6d013542` (`178104` bytes)

## 3. Verifier Execution Transcript

```text
$ sh verify-it-yourself/run_checks.sh
========================================================================
V3R1T4S Verification — dreval-exvivo-beataml2-pdx-transfer (p3)
========================================================================
[OK] SHA256SUMS manifest verified (53 files).
[OK] Zero ground-truth response (`y`) columns copied into `object/*.csv`.
[OK] BeatAML2 (N=19,823/split, 484 AML patients, 154 drugs [79 shared, 75 unseen]): unadjusted R2_norm=-0.09514+-0.00706, Pearson_norm=+0.08461+-0.00873, MSE=15.2230; shared drugs (N=11,901) R2_norm=+0.01186.
[OK] BeatAML2 p3 single-factor (each on its own, zero y_true): (i) Assay FE R2_norm=+0.01286 (dMSE=-1.5013), (ii) Platform R2_norm=-0.08088 (dMSE=-0.1982), (iii) Overlap R2_norm=-0.00075 (dMSE=-1.3121); cumulative (i)+(ii)+(iii) R2_norm=+0.05710+-0.00305 (10/10 splits > 0).
[OK] PDX_Bruna (N=1,046/split, 25 PDX models, 100 drugs [49 shared, 51 unseen]): unadjusted R2_norm=-0.39248+-0.02784, Pearson_norm=+0.10046+-0.01842, MSE=15.8705.
[OK] PDX_Bruna p3 single-factor (each on its own, zero y_true): (i) Assay FE R2_norm=-0.02490 (dMSE=-4.1895), (ii) Platform R2_norm=-0.22024 (dMSE=-1.9630), (iii) Overlap R2_norm=-0.26516 (dMSE=-1.4511); cumulative (i)+(ii)+(iii) R2_norm=+0.10159+-0.00598 (10/10 splits > 0).
PASS
```
