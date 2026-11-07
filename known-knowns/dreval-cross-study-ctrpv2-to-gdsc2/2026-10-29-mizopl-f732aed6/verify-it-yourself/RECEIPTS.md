# Verification Receipts & Cryptographic Manifest (`dreval-cross-study-ctrpv2-to-gdsc2`)

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Certificate (`object/certificate.json`) SHA-256:** `2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69`
- **Pre-Registration Lock (`object/preregistration_lock.json`) SHA-256:** `ab8ffdd5680fa57b5f9fdb9095e2bce9b28b98dceb471c3659b3a1bd78207cad` (lock ID `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`)

---

## 1. Upstream `drevalpy` Response File & HTML Table Receipts

| Upstream Resource | URL | Size (Bytes) | `SHA-256` Checksum |
| :--- | :--- | :---: | :--- |
| **`GDSC2.zip` (`Zenodo 23159774`)** | <https://zenodo.org/api/records/23159774/files/GDSC2.zip/content> | `521,509,357` | `4b0230cfcf7a670aba386d4af559eebabf3f13190517d9eb0dc67596b84ac031` (`md5: 49dc16929c6baa2b5d75c508429fa11f`) |
| **Extracted `GDSC2/GDSC2.csv` (`LN_IC50_curvecurator`)** | <https://zenodo.org/api/records/23159774/files/GDSC2.zip/content> (`GDSC2/GDSC2.csv`) | `57,384,361` | **`87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`** |
| **`CTRPv2.zip` (`Zenodo 23159774`)** | <https://zenodo.org/api/records/23159774/files/CTRPv2.zip/content> | `518,522,899` | `5ad3e867d3eda55595a981fd3f6426cb0a6a59218f109e9df68af50ffe2673bd` |
| **Extracted `CTRPv2/CTRPv2.csv` (`LN_IC50_curvecurator`)** | <https://zenodo.org/api/records/23159774/files/CTRPv2.zip/content> (`CTRPv2/CTRPv2.csv`) | `143,722,503` | **`14488de3ecff0a7499eddbc10d22cdec389549c8506a93516a547e619f90b412`** |
| **Cross-Study HTML Table (`table_cross_study_GDSC2_LCO.html`)** | <https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html> (Solo: <https://dilis-lab.github.io/drevalpy-report/all_runs/Solo/tables/table_cross_study_GDSC2_LCO.html>) | `4,664,819` | **`01d129d634be27c49c50a8a1c357135f1e1090cd8df35cd6b7687f51e69595d9`** |

---

## 2. Keyed Per-Split Prediction Files (`object/gdsc2_split_{0..9}_{sr,yn}.csv`)

Every file in `object/gdsc2_split_{0..9}_{sr,yn}.csv` has header:
```text
split,cell_line_name,drug_name,y_pred,y_pred_naive,y_pred_rf
```
- **Zero copied upstream `y` values:** The upstream `GDSC2/GDSC2.csv` response column (`LN_IC50_curvecurator`) is **not** copied into `object/`. Instead, `verify-it-yourself/verify.py` joins `(cell_line_name, drug_name)` directly against `GDSC2/GDSC2.csv` (`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`) when present locally (via `DREVAL_GDSC2_CSV` or default cache paths) and verifies against the keyed sufficient-statistics checksum table (`keyed_reference_checksums` in `object/stage3_p3_gap_decomposition.json`) when running offline.
- **One row per `(split, cell_line_name, drug_name)` test pair:** Each split $k \in \{0,\dots,9\}$ is partitioned row-wise into `gdsc2_split_{k}_sr.csv` (first half `0..N//2-1`) and `gdsc2_split_{k}_yn.csv` (second half `N//2..N-1`) so every file stays `< 1 MB`. Concatenating all 20 CSV files yields **`402,924` unique `(split, cell_line_name, drug_name)` rows** (`39,377–40,730` rows/split, mean `40,292.4 ± 389.4` out of `47,296` shared-drug pairs in `GDSC2/GDSC2.csv`) with **0 duplicate keys**.

| File Path | `SHA-256` | Size |
| :--- | :--- | :---: |
| `object/gdsc2_split_0_sr.csv` | `ed0f86f4788bcf9cdd610327f5f60c6ba0f60fd99049fe9bda812eba3a76244f` | `900,906` bytes |
| `object/gdsc2_split_0_yn.csv` | `84efe48bdb99d5ce47c694264250a7b91dda0d0187ac8a93f49e525efd158c86` | `901,686` bytes |
| `object/gdsc2_split_1_sr.csv` | `79df538d45b793769980296473e835afa9939ada354e8cf9daa7fcb17711dccf` | `894,761` bytes |
| `object/gdsc2_split_1_yn.csv` | `361eb5be47317a188a69b5059faf8a3dcbec671504ea1172f1cac2249aeab3d0` | `895,236` bytes |
| `object/gdsc2_split_2_sr.csv` | `9b24cc0fc04ef1f3b62ed52e4a8bbd50ef21621980cee1995b6d98587dce8c6a` | `896,836` bytes |
| `object/gdsc2_split_2_yn.csv` | `54e9035097a184d30a64a479c040b6960adb5e7350b87233623cd5f39be9656d` | `897,606` bytes |
| `object/gdsc2_split_3_sr.csv` | `7499cd461e26a0f6747e188cf3a3619b4ad142b5fc864c14c93d65b70253558b` | `896,859` bytes |
| `object/gdsc2_split_3_yn.csv` | `2617fc3c32289029c4681bd65dcbf08cdfefd380b089d552de06a868ad81e0dc` | `896,399` bytes |
| `object/gdsc2_split_4_sr.csv` | `28e00c3f08c2f20a6b353bc1ce37053279edb4a1e5d3636f1e714881b341d6fd` | `901,066` bytes |
| `object/gdsc2_split_4_yn.csv` | `12050110c566c43cdcffbfb5770a116896fe498991dea00e898f28e0403c2456` | `901,639` bytes |
| `object/gdsc2_split_5_sr.csv` | `27f7c3413a3607f79a14cf2163f9d38765b39b456404f504f209878d41312eb0` | `904,277` bytes |
| `object/gdsc2_split_5_yn.csv` | `509a50391376c1f10d1db0a18c812ee9b5769c393421d2b6fbffc17bae2c9546` | `904,630` bytes |
| `object/gdsc2_split_6_sr.csv` | `2631ae8955cee06a63c17001afb6ec5b0dcd26d54490921ee6f4d802aff85d86` | `886,982` bytes |
| `object/gdsc2_split_6_yn.csv` | `e7bd0ad7f9778e5ff0a2f32e1a37cf72f16904a2e5326511959f6cae7b2b9085` | `888,098` bytes |
| `object/gdsc2_split_7_sr.csv` | `93fd8eee9226be4e6838e3bb5a6f333a12acb6be767d9d79b55fcaf73b117bf1` | `891,270` bytes |
| `object/gdsc2_split_7_yn.csv` | `c231248e0123d113a65e9f7b96f95e29e9fcfa175964280bd4d302554ce12318` | `892,621` bytes |
| `object/gdsc2_split_8_sr.csv` | `49ff6038f0c461a528f776b5f6e310b834c1008c5b2dcc2b27d7f0602f81fc46` | `905,085` bytes |
| `object/gdsc2_split_8_yn.csv` | `c45c08b390107ba65654097374c1c916aa4eee8e459fb931a2919a6ff59fea98` | `904,721` bytes |
| `object/gdsc2_split_9_sr.csv` | `22d908f897ea5dd72bda4ca0af1fdc5b0709754a577c0093a840dcbb35c537a7` | `875,485` bytes |
| `object/gdsc2_split_9_yn.csv` | `41b9ab5e29f2e0c8175c84ebce8e0b6fff7ad1dfc51a8c8145107ffbaa00b784` | `875,259` bytes |
