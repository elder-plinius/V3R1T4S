#!/usr/bin/env python3
"""
Stage 1A: Strict Air-Gapped Audit of CTRPv2 Response, Omics, Drug Features, and
Comparison of Zenodo `splits.zip` vs `drevalpy.split_dataset` (n_cv_splits=10).
Strictly does NOT touch any response values from BeatAML2, PDX_Bruna, or GDSC2.
Only inspects feature headers/shapes and CTRPv2 training data.
"""
import os
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"

from pathlib import Path
import numpy as np
import pandas as pd
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor
from drevalpy.evaluation import evaluate, AVAILABLE_METRICS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def standalone_normalize_metrics(
    df_model: pd.DataFrame,
    df_naive: pd.DataFrame,
    drug_metadata: dict[str, str],
) -> dict[str, float]:
    """
    Exact standalone reproduction of drevalpy.visualization.utils._normalize_metrics_by_mean_effects
    including the merge on ['drug_name', 'cell_line_name'] mapped via drug_metadata.
    """
    from drevalpy.datasets.dataset import DrugResponseDataset
    m = df_model.copy()
    n = df_naive.copy()
    m["drug_name"] = [drug_metadata[str(d)] for d in m["pubchem_id"]]
    n["drug_name"] = [drug_metadata[str(d)] for d in n["pubchem_id"]]
    n_sub = n[["drug_name", "cell_line_name", "predictions"]].rename(columns={"predictions": "y_pred_naive"})
    m_sub = m[["drug_name", "cell_line_name", "response", "predictions"]].rename(
        columns={"response": "y_true", "predictions": "y_pred"}
    )
    merged = m_sub.merge(n_sub, on=["drug_name", "cell_line_name"], how="left")
    dt = DrugResponseDataset(
        response=(merged["y_true"] - merged["y_pred_naive"]).to_numpy(),
        cell_line_ids=merged["cell_line_name"].to_numpy(),
        drug_ids=merged["drug_name"].to_numpy(),
        predictions=(merged["y_pred"] - merged["y_pred_naive"]).to_numpy(),
    )
    res = evaluate(dataset=dt, metric=list(AVAILABLE_METRICS.keys() - {"MAE", "MSE", "RMSE"}))
    return {f"{k}: normalized": v for k, v in res.items()}


def main():
    print("=== 1. Inspecting CTRPv2 Response Table Columns ===", flush=True)
    df_head = pd.read_csv(DATA_DIR / "CTRPv2" / "CTRPv2.csv", nrows=5)
    print("CTRPv2.csv columns:", list(df_head.columns), flush=True)
    print(df_head[["cell_line_name", "pubchem_id", "tissue", "LN_IC50_curvecurator"]], flush=True)

    print("\n=== 2. Comparing Zenodo splits/cv_split_0_test.csv vs load_ctrpv2 measures ===", flush=True)
    s0_test = pd.read_csv(DATA_DIR / "splits" / "cv_split_0_test.csv")
    print("splits/cv_split_0_test.csv shape:", s0_test.shape, "columns:", list(s0_test.columns), flush=True)
    print(s0_test.head(3), flush=True)

    for measure in ["LN_IC50_curvecurator"]:
        ds = load_ctrpv2(path_data=str(DATA_DIR), measure=measure)
        ds.remove_nan_responses()
        print(f"load_ctrpv2(measure={measure}): len={len(ds)}, n_cl={len(np.unique(ds.cell_line_ids))}, n_drugs={len(np.unique(ds.drug_ids))}, n_tissues={len(np.unique(ds.tissue))}", flush=True)
        print("  Tissues:", np.unique(ds.tissue, return_counts=True), flush=True)
        splits = ds.split_dataset(n_cv_splits=10, mode="LCO", split_validation=True, split_early_stopping=True, validation_ratio=0.1, random_state=42)
        t0 = splits[0]["test"]
        match_len = len(t0) == len(s0_test)
        match_vals = False
        if match_len:
            match_vals = np.allclose(t0.response, s0_test["response"].values, equal_nan=True) and np.array_equal(t0.cell_line_ids, s0_test["cell_line_name"].astype(str).values)
        print(f"  Matches Zenodo splits/cv_split_0_test.csv? len_match={match_len}, exact_match={match_vals}", flush=True)

    print("\n=== 3. Inspecting Feature Views in CTRPv2 and Unlabelled Feature Headers Across Datasets ===", flush=True)
    for gname in sorted((DATA_DIR / "meta" / "gene_lists").glob("*.csv")):
        gdf = pd.read_csv(gname)
        print(f"  gene_list {gname.name}: {len(gdf)} genes (cols={list(gdf.columns)})", flush=True)

    for ds_name in ["CTRPv2", "GDSC2", "BeatAML2", "PDX_Bruna"]:
        dpath = DATA_DIR / ds_name
        ge_cols = pd.read_csv(dpath / "gene_expression.csv", nrows=1).columns.tolist()
        pw_cols = pd.read_csv(dpath / "pathway_features.csv", nrows=1).columns.tolist()
        cb_cols = pd.read_csv(dpath / "drug_chemberta_embeddings.csv", nrows=1).columns.tolist()
        sv_cols = pd.read_csv(dpath / "drug_smilesvec.csv", nrows=1).columns.tolist()
        dn_df = pd.read_csv(dpath / "drug_names.csv", dtype=str)
        cl_df = pd.read_csv(dpath / "cell_line_names.csv", dtype=str)
        print(
            f"  [{ds_name}] n_cl_meta={len(cl_df)} (tissues={cl_df['tissue'].unique().tolist() if 'tissue' in cl_df.columns else 'N/A'}), "
            f"n_drugs_meta={len(dn_df)}, ge_cols={len(ge_cols)}, pathway_cols={len(pw_cols)}, "
            f"chemberta_cols={len(cb_cols)}, smilesvec_cols={len(sv_cols)}",
            flush=True,
        )

    ctrp_drugs = set(pd.read_csv(DATA_DIR / "CTRPv2" / "drug_names.csv", dtype=str)["pubchem_id"].str.replace(",", ""))
    for ds_name in ["GDSC2", "BeatAML2", "PDX_Bruna"]:
        ext_drugs = set(pd.read_csv(DATA_DIR / ds_name / "drug_names.csv", dtype=str)["pubchem_id"].str.replace(",", ""))
        print(f"  Drug ID overlap CTRPv2 vs {ds_name}: {len(ctrp_drugs & ext_drugs)} / {len(ext_drugs)} external drugs", flush=True)

    print("\n=== 4. Verifying NaiveMeanEffectsPredictor & Standalone Metric Normalization on CTRPv2 Fold 0 ===", flush=True)
    ds_cc = load_ctrpv2(path_data=str(DATA_DIR), measure="LN_IC50_curvecurator")
    ds_cc.load_splits(str(DATA_DIR / "splits"))
    fold0 = ds_cc.cv_splits[0]
    tr0 = fold0["train"].copy()
    tr0.add_rows(fold0["validation"])
    tr0.shuffle(random_state=42)
    te0 = fold0["test"].copy()

    nme = NaiveMeanEffectsPredictor()
    cl_feat = nme.load_cell_line_features(str(DATA_DIR), "CTRPv2")
    dr_feat = nme.load_drug_features(str(DATA_DIR), "CTRPv2")
    nme.train(output=tr0, cell_line_input=cl_feat, drug_input=dr_feat)
    y_naive = nme.predict(cell_line_ids=te0.cell_line_ids, drug_ids=te0.drug_ids, cell_line_input=cl_feat, drug_input=dr_feat)

    # Check our standalone formula against drevalpy's _normalize_metrics_by_mean_effects
    from drevalpy.visualization.utils import _normalize_metrics_by_mean_effects
    rng = np.random.default_rng(123)
    y_dummy = y_naive + 0.2 * (te0.response - y_naive) + rng.normal(0, 0.5, size=len(y_naive))

    drug_metadata: dict[str, str] = {}
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file == "drug_names.csv":
                dn = pd.read_csv(os.path.join(root, file))
                dn["pubchem_id"] = dn["pubchem_id"].astype(str)
                drug_metadata.update(zip(dn["pubchem_id"], dn["drug_name"]))

    eval_df = pd.DataFrame(
        {
            "algorithm": ["NaiveMeanEffectsPredictor", "DummyModel"],
            "rand_setting": ["predictions", "predictions"],
            "test_mode": ["LCO", "LCO"],
            "CV_split": ["0", "0"],
            "MSE": [0.0, 0.0],
        },
        index=[
            "NaiveMeanEffectsPredictor_predictions_LCO_split_0",
            "DummyModel_predictions_LCO_split_0",
        ],
    )
    all_drug_names = [drug_metadata[str(d)] for d in te0.drug_ids]
    tvp_df = pd.DataFrame(
        {
            "algorithm": ["NaiveMeanEffectsPredictor"] * len(y_naive) + ["DummyModel"] * len(y_naive),
            "rand_setting": ["predictions"] * (2 * len(y_naive)),
            "test_mode": ["LCO"] * (2 * len(y_naive)),
            "CV_split": ["0"] * (2 * len(y_naive)),
            "drug_name": all_drug_names + all_drug_names,
            "cell_line_name": np.concatenate([te0.cell_line_ids, te0.cell_line_ids]),
            "y_true": np.concatenate([te0.response, te0.response]),
            "y_pred": np.concatenate([y_naive, y_dummy]),
        }
    )
    drev_norm = _normalize_metrics_by_mean_effects(eval_df, tvp_df)
    df_model = pd.DataFrame({
        "cell_line_name": te0.cell_line_ids,
        "pubchem_id": te0.drug_ids,
        "response": te0.response,
        "predictions": y_dummy,
    })
    df_naive = pd.DataFrame({
        "cell_line_name": te0.cell_line_ids,
        "pubchem_id": te0.drug_ids,
        "response": te0.response,
        "predictions": y_naive,
    })
    our_norm = standalone_normalize_metrics(df_model, df_naive, drug_metadata)

    max_diff = 0.0
    for k, v in our_norm.items():
        dv = float(drev_norm.loc["DummyModel_predictions_LCO_split_0", k])
        diff = abs(v - dv)
        max_diff = max(max_diff, diff)
        print(f"  {k}: standalone={v:.15f} | drevalpy={dv:.15f} | diff={diff:.2e}", flush=True)
    assert max_diff < 1e-12, f"Standalone verifier mismatch: {max_diff}"
    print(f"  [PASS] Standalone metric verifier matches drevalpy to max_diff = {max_diff:.2e} (< 1e-12)!", flush=True)


if __name__ == "__main__":
    main()
