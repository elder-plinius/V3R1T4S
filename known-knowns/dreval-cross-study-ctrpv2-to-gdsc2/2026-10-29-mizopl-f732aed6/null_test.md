# Permutation Null Control Report (`dreval-cross-study-ctrpv2-to-gdsc2`)

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Certificate (`object/certificate.json`) SHA-256:** `2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69`
- **Supporting Null File (`object/stage4_formalities_and_tanimoto_nulls.json`) SHA-256:** `2d4b0d74905412884e1fbd4d90f248f8d1a36ccc7912b7a0720b0d22d17b99fc`

---

## 1. `B = 500` Label-Permutation Null Controls on `GDSC2` (`seed = 20261029`)

To confirm that the cross-study differential sensitivity signal of `SchurBilinearExVivoDRP` on `GDSC2` (`40,292.4 ± 389.4` evaluated rows/split across splits `0..9`) is not an artifact of drug-mean or cell-line-mean structure, we ran $B = 500$ deterministic label-permutation controls (`seed = 20261029`):

| Metric on `GDSC2` (10-Split Mean) | Observed (`SchurBilinearExVivoDRP`) | Null Mean ($B = 500$) | Null SD ($B = 500$) | Null Max ($B = 500$) | $Z$-Score | Empirical $p$-Value | Controls Beaten |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Pearson_norm`** | **`+0.13294 ± 0.01253`** | `-0.00018` | `0.00482` | `+0.01491` | **`+27.59`** | **`0.001996` (`1 / 501`)** | **`500 / 500` (`100%`)** |
| **Within-Drug Cell-Line `Pearson`** | **`+0.35148 ± 0.00525`** | `+0.00004` | `0.00511` | `+0.01618` | **`+68.77`** | **`0.001996` (`1 / 501`)** | **`500 / 500` (`100%`)** |
