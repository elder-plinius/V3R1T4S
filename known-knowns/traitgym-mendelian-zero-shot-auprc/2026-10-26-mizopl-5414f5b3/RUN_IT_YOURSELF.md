# Run It Yourself (`2026-10-26-mizopl-5414f5b3`)

## Option 1: Instant Zero-Dependency Verification (`< 1 second`)

Requires **only Python 3.8+ standard library** (`json`, `csv`, `math`, `hashlib`, `pathlib`, `sys`). Recomputes exact step-function Average Precision (`AUPRC`) across all 19 Mendelian chromosomes ($N = 3,380$ variants) and all 22 Complex chromosomes ($N = 11,400$ variants) directly from `object/mendelian_zero_shot_predictions.csv` and `object/complex_zero_shot_predictions.csv`, and verifies all `object/certificate.json` invariants:

```bash
sh verify-it-yourself/run_checks.sh
```

## Option 2: Full End-to-End Reproduction from Raw TraitGym Parquet Files (`~10 minutes`)

To recompute every baseline, every zero-shot score (`Track A` and `Track B`), every by-chromosome `GridSearchCV` Ridge logistic regression probe (`Track C`), all $1,000$-iteration chromosome block bootstraps (`seed = 42`), and all $1,000$-iteration within-chromosome label permutation null tests directly from the official Hugging Face `songlab/TraitGym` parquet files:

```bash
pip install numpy pandas pyarrow scikit-learn
git clone https://huggingface.co/datasets/songlab/TraitGym data/TraitGym
python3 how-we-built-it/verify_full_benchmark.py
```
