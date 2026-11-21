"""Post-hoc ensemble scorer: average two completed models' per-split predictions and
evaluate the mean under the chosen ruler. Used to ESTIMATE whether a combined model class
is worth running through the pipeline; the claim vehicle itself would be the model class.

Usage: python ensemble_score.py <run_a> <model_a> <run_b> <model_b> [ruler]
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute_normalized import pearson, r2  # noqa: E402


def load_preds(run: str, model: str, ruler: str):
    base = os.path.join("results", run, "CTRPv2", "LCO")
    pdir = os.path.join(base, model, "predictions")
    naive_dir = os.path.join(base, "naive_v131" if ruler == "v131" else "naive_independent")
    out = {}
    for f in sorted(os.listdir(pdir)):
        if f.startswith("predictions_split_") and f.endswith(".csv"):
            idx = int(f.split("_")[-1].split(".")[0])
            att = pd.read_csv(os.path.join(pdir, f))
            n = pd.read_csv(os.path.join(naive_dir, f"predictions_split_{idx}.csv"))
            n = n.rename(columns={"naive_pred": "predictions"}) if "naive_pred" in n.columns else n
            merged = att[["cell_line_name", "pubchem_id", "response", "predictions"]].merge(
                n[["cell_line_name", "pubchem_id", "predictions"]],
                on=["cell_line_name", "pubchem_id"],
                how="left",
                suffixes=("", "_naive"),
            )
            assert merged["predictions_naive"].notna().all()
            out[idx] = merged
    return out


def main() -> None:
    run_a, model_a, run_b, model_b = sys.argv[1:5]
    ruler = sys.argv[5] if len(sys.argv) > 5 else "v131"
    a = load_preds(run_a, model_a, ruler)
    b = load_preds(run_b, model_b, ruler)
    common = sorted(set(a) & set(b))
    print(f"common splits: {common}")
    rows = []
    for idx in common:
        ma = a[idx][["cell_line_name", "pubchem_id", "response", "predictions_naive", "predictions"]].copy()
        ma = ma.rename(columns={"predictions": "pred_a"})
        mb = b[idx].drop_duplicates(subset=["cell_line_name", "pubchem_id"])[
            ["cell_line_name", "pubchem_id", "predictions"]
        ].copy()
        mb = mb.rename(columns={"predictions": "pred_b"})
        m = ma.merge(mb, on=["cell_line_name", "pubchem_id"], how="left")
        assert len(m) == len(a[idx]) and m["pred_b"].notna().all()
        pred = (m["pred_a"].to_numpy() + m["pred_b"].to_numpy()) / 2.0
        yt = m["response"].to_numpy() - m["predictions_naive"].to_numpy()
        yp = pred - m["predictions_naive"].to_numpy()
        rows.append(
            dict(
                split=idx,
                r2=r2(yt, yp),
                pearson=pearson(yt, yp),
                spearman=float(stats.spearmanr(yt, yp).statistic),
            )
        )
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    se = df["r2"].std(ddof=1) / np.sqrt(len(df))
    print(
        f"ENSEMBLE MEAN normR2={df['r2'].mean():.4f} (SE {se:.4f}, 2xSE {2*se:.4f})"
        f"  Pearson={df['pearson'].mean():.4f}  Spearman={df['spearman'].mean():.4f}"
    )


if __name__ == "__main__":
    main()
