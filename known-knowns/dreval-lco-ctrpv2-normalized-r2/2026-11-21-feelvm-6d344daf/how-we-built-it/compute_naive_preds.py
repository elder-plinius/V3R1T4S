"""Compute NaiveMeanEffectsPredictor test predictions independently per split.

The pipeline trains its normalization baseline (NaiveMeanEffectsPredictor) on train+validation
of each split before predicting the test fold (experiment.py: train_dataset.add_rows(
validation_dataset) before the final train_and_predict). This script reproduces exactly that
with the package's own class, reading the split CSVs drevalpy wrote, so normalized metrics can
be recomputed before the report step exists.

Usage: python compute_naive_preds.py <run_id> [results_root]
Writes: <root>/<run_id>/CTRPv2/LCO/naive_independent/predictions_split_<i>.csv
"""
import os
import sys

import numpy as np
import pandas as pd

from drevalpy.datasets.dataset import DrugResponseDataset, FeatureDataset
from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor
from drevalpy.models.utils import load_cl_ids_and_tissues_from_csv, load_drug_ids_from_csv


def main() -> None:
    run_id = sys.argv[1]
    root = sys.argv[2] if len(sys.argv) > 2 else "results"
    split_dir = os.path.join(root, run_id, "CTRPv2", "LCO", "splits")
    out_dir = os.path.join(root, run_id, "CTRPv2", "LCO", "naive_independent")
    os.makedirs(out_dir, exist_ok=True)
    cl_feats = load_cl_ids_and_tissues_from_csv(path="data", dataset_name="CTRPv2")
    drug_feats = load_drug_ids_from_csv(data_path="data", dataset_name="CTRPv2")

    idx = 0
    while True:
        tr_path = os.path.join(split_dir, f"cv_split_{idx}_train.csv")
        if not os.path.exists(tr_path):
            break
        out_path = os.path.join(out_dir, f"predictions_split_{idx}.csv")
        if os.path.exists(out_path):
            idx += 1
            continue
        parts = []
        for role in ("train", "validation"):
            p = os.path.join(split_dir, f"cv_split_{idx}_{role}.csv")
            df = pd.read_csv(p, dtype={"pubchem_id": str, "cell_line_name": str})
            parts.append(df)
        trainval = pd.concat(parts, ignore_index=True)
        # the split CSVs store response as 'response' column? check actual columns
        resp_col = "response" if "response" in trainval.columns else trainval.columns[-1]
        train_ds = DrugResponseDataset(
            response=trainval[resp_col].to_numpy(),
            cell_line_ids=trainval["cell_line_name"].to_numpy(),
            drug_ids=trainval["pubchem_id"].to_numpy(),
            dataset_name="CTRPv2",
        )
        model = NaiveMeanEffectsPredictor()
        model.train(output=train_ds, cell_line_input=cl_feats, drug_input=drug_feats)
        test = pd.read_csv(
            os.path.join(split_dir, f"cv_split_{idx}_test.csv"),
            dtype={"pubchem_id": str, "cell_line_name": str},
        )
        preds = model.predict(
            cell_line_ids=test["cell_line_name"].to_numpy(),
            drug_ids=test["pubchem_id"].to_numpy(),
            cell_line_input=cl_feats,
            drug_input=drug_feats,
        )
        out = test.copy()
        out["naive_pred"] = preds
        out.to_csv(out_path, index=False)
        print(f"split {idx}: wrote {len(out)} naive predictions")
        idx += 1


if __name__ == "__main__":
    main()
