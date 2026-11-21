"""Compute NaiveMeanEffectsPredictor test predictions with the REPORT's (v1.3.1) semantics.

drevalpy v1.3.1 (the version that generated the public report) defines:
    prediction = overall_mean + cell_line_effect + drug_effect
with cell_line_effect = (cell line mean - overall_mean) fitted on the training rows, and NO
tissue fallback: a test cell line (unseen in LCO) contributes 0. drevalpy v1.6.0 changed the
class to overall_mean + tissue_effect + cell_line_residual_effect + drug_effect (tissue
fallback), which changes the normalized metric's ruler. To compare against the published
heatmap values we reproduce the v1.3.1 ruler exactly (same class semantics, fitted on the
same train+validation rows the pipeline used for its final models).

Usage: python compute_naive_preds_v131.py <run_id> [results_root]
Writes: <root>/<run_id>/CTRPv2/LCO/naive_v131/predictions_split_<i>.csv (column naive_pred)
"""
import os
import sys

import numpy as np
import pandas as pd


def main() -> None:
    run_id = sys.argv[1]
    root = sys.argv[2] if len(sys.argv) > 2 else "results"
    split_dir = os.path.join(root, run_id, "CTRPv2", "LCO", "splits")
    out_dir = os.path.join(root, run_id, "CTRPv2", "LCO", "naive_v131")
    os.makedirs(out_dir, exist_ok=True)

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
            parts.append(pd.read_csv(p, dtype={"pubchem_id": str, "cell_line_name": str}))
        trainval = pd.concat(parts, ignore_index=True)
        overall = float(trainval["response"].mean())
        cl_means = trainval.groupby("cell_line_name")["response"].mean()
        drug_means = trainval.groupby("pubchem_id")["response"].mean()
        cl_effect = cl_means - overall
        drug_effect = drug_means - overall

        test = pd.read_csv(
            os.path.join(split_dir, f"cv_split_{idx}_test.csv"),
            dtype={"pubchem_id": str, "cell_line_name": str},
        )
        pred = (
            overall
            + test["cell_line_name"].map(cl_effect).fillna(0.0).to_numpy()
            + test["pubchem_id"].map(drug_effect).fillna(0.0).to_numpy()
        )
        out = test.copy()
        out["naive_pred"] = pred
        out.to_csv(out_path, index=False)
        print(f"split {idx}: wrote {len(out)} v1.3.1-ruler naive predictions")
        idx += 1


if __name__ == "__main__":
    main()
