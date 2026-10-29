#!/usr/bin/env python3
"""
Step 0 & 1: Download TDC DTI_DG_Group ('BindingDB_Patent'), verify SHA-256 manifest,
and run comprehensive structural & temporal domain-shift EDA across seeds 1..5.
"""
import hashlib
import json
import os
import time
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import requests

# Ensure Harvard Dataverse does not block default python-requests User-Agent (403 Forbidden)
_orig_requests_get = requests.get
def _patched_requests_get(*args, **kwargs):
    headers = dict(kwargs.get("headers") or {})
    headers.setdefault(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    )
    kwargs["headers"] = headers
    return _orig_requests_get(*args, **kwargs)
requests.get = _patched_requests_get

import tdc
from tdc.benchmark_group import dti_dg_group

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main():
    t0 = time.time()
    print("=== Step 0: Downloading / Loading DTI_DG_Group ('BindingDB_Patent') ===")
    group = dti_dg_group(path=str(DATA_DIR))
    benchmark = group.get("BindingDB_Patent")
    name = benchmark["name"]
    train_val = benchmark["train_val"]
    test = benchmark["test"]

    print(f"Benchmark name: {name} (loaded in {time.time() - t0:.2f}s)")
    print(f"train_val shape: {train_val.shape}, columns: {list(train_val.columns)}")
    print(f"test shape:      {test.shape}, columns: {list(test.columns)}")
    print("\ntrain_val head(3):")
    print(train_val.head(3))
    print("\ntest head(3):")
    print(test.head(3))

    # Compute SHA-256 of all files in DATA_DIR
    file_hashes = {}
    for root, _, files in os.walk(DATA_DIR):
        for fn in sorted(files):
            fpath = Path(root) / fn
            rel = str(fpath.relative_to(BASE_DIR))
            file_hashes[rel] = {
                "sha256": sha256_file(fpath),
                "size_bytes": fpath.stat().st_size,
            }

    # Official test (Drug, Target) key list hash
    # Let's check exact column names for Drug SMILES and Target sequence
    drug_col = "Drug" if "Drug" in test.columns else test.columns[1]
    target_col = "Target" if "Target" in test.columns else test.columns[2]
    y_col = "Y" if "Y" in test.columns else "y"
    year_col = "Year" if "Year" in test.columns else [c for c in test.columns if "year" in c.lower()][0]

    test_keys_str = "\n".join(f"{d}\t{t}" for d, t in zip(test[drug_col], test[target_col]))
    test_keys_sha256 = sha256_bytes(test_keys_str.encode("utf-8"))

    test_full_str = "\n".join(
        f"{i}\t{d}\t{t}\t{y:.8f}\t{yr}"
        for i, (d, t, y, yr) in enumerate(zip(test[drug_col], test[target_col], test[y_col], test[year_col]))
    )
    test_full_sha256 = sha256_bytes(test_full_str.encode("utf-8"))

    # Inspect seeds 1..5 splits
    seed_summaries = {}
    for seed in [1, 2, 3, 4, 5]:
        train_df, valid_df = group.get_train_valid_split(benchmark=name, split_type="default", seed=seed)
        seed_summaries[str(seed)] = {
            "train_rows": int(len(train_df)),
            "valid_rows": int(len(valid_df)),
            "train_years": train_df[year_col].value_counts().sort_index().to_dict(),
            "valid_years": valid_df[year_col].value_counts().sort_index().to_dict(),
            "train_unique_targets": int(train_df[target_col].nunique()),
            "valid_unique_targets": int(valid_df[target_col].nunique()),
            "valid_unseen_targets_in_train": int((~valid_df[target_col].isin(set(train_df[target_col]))).sum()),
            "valid_unseen_drugs_in_train": int((~valid_df[drug_col].isin(set(train_df[drug_col]))).sum()),
        }
        print(f"Seed {seed}: train={len(train_df)}, valid={len(valid_df)}, "
              f"valid_years={seed_summaries[str(seed)]['valid_years']}, "
              f"valid_unseen_targets={seed_summaries[str(seed)]['valid_unseen_targets_in_train']}")

    # Structural & Temporal EDA on train_val vs test
    tv_targets = set(train_val[target_col])
    test_targets = set(test[target_col])
    tv_drugs = set(train_val[drug_col])
    test_drugs = set(test[drug_col])
    tv_pairs = set(zip(train_val[drug_col], train_val[target_col]))
    test_pairs = list(zip(test[drug_col], test[target_col]))

    test_seen_target_mask = test[target_col].isin(tv_targets)
    test_seen_drug_mask = test[drug_col].isin(tv_drugs)
    test_exact_pair_in_tv = sum(1 for p in test_pairs if p in tv_pairs)

    eda = {
        "train_val_rows": int(len(train_val)),
        "test_rows": int(len(test)),
        "columns": list(train_val.columns),
        "train_val_years": {str(k): int(v) for k, v in train_val[year_col].value_counts().sort_index().items()},
        "test_years": {str(k): int(v) for k, v in test[year_col].value_counts().sort_index().items()},
        "train_val_y_stats": {
            "mean": float(train_val[y_col].mean()),
            "std": float(train_val[y_col].std()),
            "min": float(train_val[y_col].min()),
            "q25": float(train_val[y_col].quantile(0.25)),
            "median": float(train_val[y_col].median()),
            "q75": float(train_val[y_col].quantile(0.75)),
            "max": float(train_val[y_col].max()),
        },
        "test_y_stats": {
            "mean": float(test[y_col].mean()),
            "std": float(test[y_col].std()),
            "min": float(test[y_col].min()),
            "q25": float(test[y_col].quantile(0.25)),
            "median": float(test[y_col].median()),
            "q75": float(test[y_col].quantile(0.75)),
            "max": float(test[y_col].max()),
        },
        "train_val_y_by_year": {
            str(yr): {
                "count": int(len(sub)),
                "mean": float(sub[y_col].mean()),
                "std": float(sub[y_col].std()),
                "median": float(sub[y_col].median()),
            }
            for yr, sub in train_val.groupby(year_col)
        },
        "test_y_by_year": {
            str(yr): {
                "count": int(len(sub)),
                "mean": float(sub[y_col].mean()),
                "std": float(sub[y_col].std()),
                "median": float(sub[y_col].median()),
            }
            for yr, sub in test.groupby(year_col)
        },
        "unique_targets_train_val": int(len(tv_targets)),
        "unique_targets_test": int(len(test_targets)),
        "unique_targets_overlap": int(len(tv_targets & test_targets)),
        "unique_targets_test_unseen": int(len(test_targets - tv_targets)),
        "test_rows_seen_target": int(test_seen_target_mask.sum()),
        "test_rows_unseen_target": int((~test_seen_target_mask).sum()),
        "unique_drugs_train_val": int(len(tv_drugs)),
        "unique_drugs_test": int(len(test_drugs)),
        "unique_drugs_overlap": int(len(tv_drugs & test_drugs)),
        "test_rows_seen_drug": int(test_seen_drug_mask.sum()),
        "test_rows_unseen_drug": int((~test_seen_drug_mask).sum()),
        "test_rows_both_seen": int((test_seen_target_mask & test_seen_drug_mask).sum()),
        "test_rows_seen_target_unseen_drug": int((test_seen_target_mask & ~test_seen_drug_mask).sum()),
        "test_rows_unseen_target_seen_drug": int((~test_seen_target_mask & test_seen_drug_mask).sum()),
        "test_rows_both_unseen": int((~test_seen_target_mask & ~test_seen_drug_mask).sum()),
        "test_exact_pair_in_train_val": int(test_exact_pair_in_tv),
        "train_val_unique_pairs": int(len(tv_pairs)),
        "test_unique_pairs": int(len(set(test_pairs))),
    }

    manifest = {
        "benchmark_group": "DTI_DG_Group",
        "benchmark_name": name,
        "pytdc_version": getattr(tdc, "__version__", "1.1.15"),
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": file_hashes,
        "test_drug_target_keys_sha256": test_keys_sha256,
        "test_full_table_sha256": test_full_sha256,
        "eda": eda,
        "seeds_1_to_5": seed_summaries,
    }

    manifest_path = BASE_DIR / "manifest_sha256.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("\n=== EDA Summary ===")
    print(json.dumps(eda, indent=2))
    print(f"\nSaved manifest to {manifest_path}")


if __name__ == "__main__":
    main()
