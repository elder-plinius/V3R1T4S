"""Independent recomputation of normalized metrics from drevalpy prediction CSVs.

Reads the per-split prediction files the pipeline writes for a model and for
NaiveMeanEffectsPredictor, merges on (cell_line, drug, split), subtracts the naive
predictions from true and predicted values (exactly what visualization/utils.py
_normalize_metrics_by_mean_effects does), and computes normalized R^2 / Pearson /
Spearman per split plus the mean and SE across splits.

Usage:
  python recompute_normalized.py <run_id> [model_name] [results_root]

Example:
  python recompute_normalized.py att_v1 ResidualOmics
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats


def pearson(y, yp):
    if np.std(y) == 0 or np.std(yp) == 0:
        return float("nan")
    return float(np.corrcoef(y, yp)[0, 1])


def r2(y, yp):
    ss_res = float(((y - yp) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def main() -> None:
    run_id = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else None
    root = sys.argv[3] if len(sys.argv) > 3 else "results"
    base = os.path.join(root, run_id, "CTRPv2", "LCO")
    ruler = sys.argv[4] if len(sys.argv) > 4 else "v16"
    cand = {
        "v131": os.path.join(base, "naive_v131"),
        "v16": os.path.join(base, "NaiveMeanEffectsPredictor", "predictions"),
        "v16ind": os.path.join(base, "naive_independent"),
    }
    naive_dir = cand[ruler]
    print(f"ruler={ruler} naive_dir={naive_dir}")
    models = [model] if model else [
        d for d in sorted(os.listdir(base))
        if os.path.isdir(os.path.join(base, d, "predictions")) and d != "NaiveMeanEffectsPredictor"
    ]
    naive = {}
    for f in sorted(os.listdir(naive_dir)):
        if f.startswith("predictions_split_") and f.endswith(".csv"):
            idx = int(f.split("_")[-1].split(".")[0])
            dfn = pd.read_csv(os.path.join(naive_dir, f))
            if "naive_pred" in dfn.columns and "predictions" not in dfn.columns:
                dfn = dfn.rename(columns={"naive_pred": "predictions"})
            naive[idx] = dfn
    print(f"run_id={run_id} naive splits={sorted(naive)}")
    for m in models:
        pdir = os.path.join(base, m, "predictions")
        rows = []
        for f in sorted(os.listdir(pdir)):
            if not (f.startswith("predictions_split_") and f.endswith(".csv")):
                continue
            idx = int(f.split("_")[-1].split(".")[0])
            att = pd.read_csv(os.path.join(pdir, f))
            n = naive[idx]
            # mirror the package's _normalize_metrics_by_mean_effects merge exactly
            # (how="left" on the model rows; duplicate (cl, drug) replicate keys inflate
            # the frame exactly as the package's evaluation does)
            merged = att[["cell_line_name", "pubchem_id", "response", "predictions"]].merge(
                n[["cell_line_name", "pubchem_id", "predictions"]],
                on=["cell_line_name", "pubchem_id"],
                how="left",
                suffixes=("_att", "_naive"),
            )
            assert len(merged) >= len(att) and merged["predictions_att"].notna().all(), (
                f"{m} split {idx}: merge lost rows"
            )
            yt = merged["response"].to_numpy() - merged["predictions_naive"].to_numpy()
            yp = merged["predictions_att"].to_numpy() - merged["predictions_naive"].to_numpy()
            rows.append(
                dict(
                    split=idx,
                    n=len(merged),
                    r2=r2(yt, yp),
                    pearson=pearson(yt, yp),
                    spearman=float(stats.spearmanr(yt, yp).statistic),
                )
            )
            # dedup variant (one naive value per pair; replicate-weighted honestly)
            nd = n.drop_duplicates(subset=["cell_line_name", "pubchem_id"])
            md = att.merge(
                nd[["cell_line_name", "pubchem_id", "response", "predictions"]],
                on=["cell_line_name", "pubchem_id"],
                how="left",
                suffixes=("", "_naive"),
            )
            assert len(md) == len(att)
            ytd = md["response"].to_numpy() - md["predictions_naive"].to_numpy()
            ypd = md["predictions"].to_numpy() - md["predictions_naive"].to_numpy()
            rows[-1]["r2_dedup"] = r2(ytd, ypd)
            rows[-1]["pearson_dedup"] = pearson(ytd, ypd)
        df = pd.DataFrame(rows).sort_values("split")
        print(f"\n{m}:")
        print(df.to_string(index=False))
        print(
            f"  MEAN normR2={df['r2'].mean():.4f} (SE {df['r2'].std(ddof=1)/np.sqrt(len(df)):.4f})"
            f"  normPearson={df['pearson'].mean():.4f}"
            f"  normSpearman={df['spearman'].mean():.4f}"
        )


if __name__ == "__main__":
    main()
