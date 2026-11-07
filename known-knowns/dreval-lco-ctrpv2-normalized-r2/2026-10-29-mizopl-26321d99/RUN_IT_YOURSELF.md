# Run It Yourself (`2026-10-29-mizopl-26321d99`)

## Option 1: Instant Zero-Dependency Verification (`< 3 seconds`)

Requires **only the Python 3.8+ standard library** (`csv`, `hashlib`, `json`, `math`, `pathlib`, `sys`). Verifies the SHA-256 cryptographic hashes of `object/certificate.json`, `object/preregistration_lock.json`, and all `46` files in `object/`, and independently recomputes the 10-split normalized metrics (`R2_norm`, `Pearson_norm`, `MSE`, `RMSE`, `MAE`), Tanimoto strata, and `p3` transfer-gap decompositions directly from `object/*.csv`:

```bash
sh verify-it-yourself/run_checks.sh
```

## Option 2: Full End-to-End Campaign Reproduction (`drevalpy==1.6.0`)

To reproduce the entire pipeline from the official Zenodo `drevalpy==1.6.0` benchmark archive (`record 18770924` / `23159774` + `leaderboard_Oct26.zip`) on a laptop (`OMP_NUM_THREADS=4`):

```bash
python3 -m venv .venv
.venv/bin/pip install drevalpy==1.6.0 rdkit scikit-learn scipy pandas numpy
OMP_NUM_THREADS=4 .venv/bin/python how-we-built-it/stage0_download_and_manifest.py
OMP_NUM_THREADS=4 .venv/bin/python how-we-built-it/stage1_inspect_and_verify_metrics.py
OMP_NUM_THREADS=4 .venv/bin/python how-we-built-it/stage2_inner_ablation.py
OMP_NUM_THREADS=4 .venv/bin/python how-we-built-it/stage3_exvivo_and_cross_study_eval.py
OMP_NUM_THREADS=4 .venv/bin/python how-we-built-it/stage3_p3_gap_decomposition.py
OMP_NUM_THREADS=4 .venv/bin/python how-we-built-it/stage4_formalities_and_nulls.py
```
