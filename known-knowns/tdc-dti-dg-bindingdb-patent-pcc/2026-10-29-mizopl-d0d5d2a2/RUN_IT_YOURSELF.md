# Run It Yourself: TDC DTI Domain-Generalization (`BindingDB_Patent`)

## 1. Standalone Package Verification (`~5 seconds` on CPU)

From the root of this submission package (`2026-10-29-mizopl-d0d5d2a2/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

What `verify-it-yourself/verify.py` verifies:
1. Checks `object/manifest_sha256.json`, `object/certificate.json`, and `object/certificate_phase1_cpu_p1_p2.json` for official TDC dataset SHA-256 commitments (`dti_dg_group.zip`: `4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`; `train_val.csv`: `1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6`; `test.csv`: `3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31`; download URL: <https://dataverse.harvard.edu/api/access/datafile/4798216>), pre-test `train_val` inner temporal validation progression (`step02`–`step07`), and the 6-run test-evaluation audit.
2. Reassembles all `40` keyed prediction CSV part files (`object/seed_{1..5}_{track}_part1.csv` rows `0..24,513` + `_part2.csv` rows `24,514..49,027`) for `trackA_strict_train` (claimed primary `p1` model: `0.580 ± 0.003` [`0.57942 ± 0.00299`]), `trackB_trainval_refit` (`0.57106 ± 0.00260`), `erm_baseline` (`0.51310 ± 0.00271`), and `trackF1_bayes_mmse72` (unclaimed exploratory Phase-2 ablation: `0.59996 ± 0.00266`), verifying that every row is keyed by `row_index,Drug_ID,Target_ID,y_pred` in exact official test order (`test_pair_ids_sha256: 0b81510459589882c72484834aec0fac355536645a9b8fd414e1db991d5c51cb`) and verifying per-part SHA-256s, L1/L2 norms, means, standard deviations, and 5x5 cross-seed dot-product matrices.
3. When official TDC `test.csv` and `train_val.csv` are staged in `TDC_DATA_DIR`, `verify.py` also verifies their SHA-256 hashes and recomputes all 5-seed Pearson correlations (`PCC`), per-year (`2019 / 2020 / 2021`) PCCs, and `Seen-Target` / `Unseen-Target` / `Unseen-Ligand` PCCs directly against `test.csv["Y"]`.

### Reassembling a Single 49,028-Row Keyed CSV in Python

Each 49,028-row keyed table (`row_index,Drug_ID,Target_ID,y_pred`) is split into `_part1.csv` (`24,514` rows, `0..24,513`) and `_part2.csv` (`24,514` rows, `24,514..49,027`) so every file stays under `1,000,000` bytes:

```python
import pandas as pd
df_seed1 = pd.concat([
    pd.read_csv("object/seed_1_trackA_strict_train_part1.csv"),
    pd.read_csv("object/seed_1_trackA_strict_train_part2.csv"),
], ignore_index=True)
```

---

## 2. Reproducing the Pre-Test `train_val` Validation & 5-Seed Pipeline (`how-we-built-it/`)

```sh
cd how-we-built-it
python3 step01_download_manifest_and_eda.py
python3 step02_inner_temporal_anatomy.py
python3 step03_precompute_features.py
python3 step03_test_target_ligand_kernel_on_temporal_val.py
python3 step04_test_dual_kernel_splits.py
python3 step05_test_tkrr_and_cold_models.py
python3 step05b_test_homology_tkrr.py
python3 step06b_inspect_unseen_target_homology.py
python3 step06_test_universal_kriging_and_unseen.py
python3 step07_test_full_modular_stack_splits.py
python3 step08_run_5seeds_and_verify.py
```
