#!/usr/bin/env python3
"""
Stage 3: Post-Lock One-Shot Ex Vivo & Cross-Study Evaluation + Same-Environment Baselines
+ Exact p3 Transfer Gap Decomposition across:
  1. BeatAML2 (Ex Vivo AML Patient Blasts — Moonshot Target)
  2. PDX_Bruna (Ex Vivo Breast Cancer PDX Explants — Moonshot Target)
  3. GDSC2 (Cross-Study Pan-Cancer Cell Lines — Harvest Target)

Requires `DREVAL_CAMPAIGN/certificates/preregistration_lock.json` to exist and be verified first.
"""
import os
import json
import time
import hashlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.linalg import solve
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
import torch

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
torch.set_num_threads(4)

from drevalpy.datasets.loader import AVAILABLE_DATASETS, load_ctrpv2
from drevalpy.datasets.dataset import DrugResponseDataset

from DREVAL_CAMPAIGN.src.stage2_inner_ablation import (
    DATA_DIR,
    fast_naive_mean_effects,
    fit_and_predict_schur_bilinear,
)
from DREVAL_CAMPAIGN.src.models import load_pair_views

BASE_DIR = "DREVAL_CAMPAIGN"
LOCK_PATH = f"{BASE_DIR}/certificates/preregistration_lock.json"


def verify_preregistration_lock():
    assert os.path.exists(LOCK_PATH), f"Missing {LOCK_PATH}! Cannot run Stage 3 before locking Stage 2."
    lock = json.load(open(LOCK_PATH))
    assert "preregistration_lock_sha256" in lock
    print(
        f"[VERIFIED PRE-REGISTRATION LOCK] locked_at={lock['locked_at_utc']} | "
        f"lock_sha256={lock['preregistration_lock_sha256']}"
    )
    return lock


def compute_normalized_and_raw_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_naive: np.ndarray,
) -> dict[str, float]:
    yt_res = y_true - y_naive
    yp_res = y_pred - y_naive
    ss_res = float(np.sum((yt_res - yp_res) ** 2))
    ss_tot = float(np.sum((yt_res - np.mean(yt_res)) ** 2))
    r2_norm = float(1.0 - ss_res / max(ss_tot, 1e-12))

    # Centered R2 on residuals (removes constant shift across assays)
    ss_res_cent = float(np.sum(((yt_res - np.mean(yt_res)) - (yp_res - np.mean(yp_res))) ** 2))
    r2_norm_centered = float(1.0 - ss_res_cent / max(ss_tot, 1e-12))

    pcc_norm = float(np.corrcoef(yt_res, yp_res)[0, 1]) if (np.std(yp_res) > 1e-12 and np.std(yt_res) > 1e-12) else 0.0
    scc_norm = float(spearmanr(yt_res, yp_res).statistic) if (np.std(yp_res) > 1e-12 and np.std(yt_res) > 1e-12) else 0.0

    mse_raw = float(np.mean((y_true - y_pred) ** 2))
    rmse_raw = float(np.sqrt(mse_raw))
    mae_raw = float(np.mean(np.abs(y_true - y_pred)))
    ss_tot_raw = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2_raw = float(1.0 - np.sum((y_true - y_pred) ** 2) / max(ss_tot_raw, 1e-12))
    pcc_raw = float(np.corrcoef(y_true, y_pred)[0, 1]) if (np.std(y_pred) > 1e-12 and np.std(y_true) > 1e-12) else 0.0
    scc_raw = float(spearmanr(y_true, y_pred).statistic) if (np.std(y_pred) > 1e-12 and np.std(y_true) > 1e-12) else 0.0

    return {
        "R2_norm": r2_norm,
        "R2_norm_centered": r2_norm_centered,
        "Pearson_norm": pcc_norm,
        "Spearman_norm": scc_norm,
        "MSE": mse_raw,
        "RMSE": rmse_raw,
        "MAE": mae_raw,
        "R2_raw": r2_raw,
        "Pearson_raw": pcc_raw,
        "Spearman_raw": scc_raw,
    }


def fit_predict_raw_platform_krr(
    train_ds: DrugResponseDataset,
    pred_ds: DrugResponseDataset,
    meta: dict,
    cell_cache: dict,
    drug_cache: dict,
    merged_cl_tis: dict,
) -> np.ndarray:
    """
    Ablation for p3 Axis 1 (Expression-Platform Shift):
    Uses the exact same Exact Per-Drug KRR solver and drug/tissue offsets,
    but replaces our within-sample rank-normal (vdW + auto-log2) views with
    drevalpy's standard `arcsinh(raw_ge)` + global StandardScaler fitted on CTRPv2.
    """
    views = meta["views"]
    ge_df = views["ge_df"]
    cl_ids = cell_cache["cl_ids"]
    cl_to_idx = cell_cache["cl_to_idx"]
    drug_to_idx = drug_cache["drug_to_idx"]

    raw_ge = np.arcsinh(np.maximum(ge_df.loc[cl_ids].values.astype(np.float64), 0.0))

    df_tr = pd.DataFrame({"cl": train_ds.cell_line_ids, "dr": train_ds.drug_ids, "y": train_ds.response})
    df_tr = df_tr.groupby(["cl", "dr"], as_index=False)["y"].mean()
    tr_cl_u = sorted(df_tr["cl"].unique())
    tr_dr_u = sorted(df_tr["dr"].unique())
    tr_cl_idx = np.array([cl_to_idx[c] for c in tr_cl_u], dtype=np.int64)
    tr_dr_idx = np.array([drug_to_idx[d] for d in tr_dr_u], dtype=np.int64)

    te_cl_u = sorted(list(set(pred_ds.cell_line_ids)))
    all_cl_u = sorted(list(set(tr_cl_u) | set(te_cl_u)))
    all_cl_idx = np.array([cl_to_idx[c] for c in all_cl_u], dtype=np.int64)
    all_cl_map = {c: i for i, c in enumerate(all_cl_u)}
    tr_pos = np.array([all_cl_map[c] for c in tr_cl_u], dtype=np.int64)

    # StandardScaler fitted on CTRPv2 train cell lines (suffers platform shift when target is already log-scaled)
    mu_g = np.mean(raw_ge[tr_cl_idx], axis=0, keepdims=True)
    sd_g = np.std(raw_ge[tr_cl_idx], axis=0, keepdims=True)
    sd_g = np.where(sd_g < 1e-6, 1.0, sd_g)
    Z_raw = ((raw_ge[all_cl_idx] - mu_g) / sd_g).astype(np.float32)
    Z_norms = np.maximum(np.linalg.norm(Z_raw, axis=1, keepdims=True), 1e-8)
    Z_cos = Z_raw / Z_norms
    Z_lin = Z_raw / np.sqrt(Z_raw.shape[1])
    K_raw = 0.60 * (Z_cos @ Z_cos[tr_pos].T) + 0.40 * (Z_lin @ Z_lin[tr_pos].T)

    # Decomposition around global + tissue + cell + drug means
    mu = float(df_tr["y"].mean())
    df_tr["ti"] = df_tr["cl"].map(lambda c: merged_cl_tis.get(c, "Unknown"))
    ti_grp = df_tr.groupby("ti")["y"].agg(["count", "mean"])
    ti_eff = ((ti_grp["count"] * (ti_grp["mean"] - mu)) / (ti_grp["count"] + 10.0)).to_dict()
    df_tr["r_ti"] = df_tr["y"] - mu - df_tr["ti"].map(ti_eff).fillna(0.0)
    cl_grp = df_tr.groupby("cl")["r_ti"].agg(["count", "mean"])
    cl_eff = ((cl_grp["count"] * cl_grp["mean"]) / (cl_grp["count"] + 5.0)).to_dict()
    dr_grp = df_tr.groupby("dr")["r_ti"].agg(["count", "mean"])
    dr_eff = ((dr_grp["count"] * dr_grp["mean"]) / (dr_grp["count"] + 5.0)).to_dict()

    n_tr_c = len(tr_cl_u)
    n_tr_d = len(tr_dr_u)
    tr_c_local = {c: i for i, c in enumerate(tr_cl_u)}
    tr_d_local = {d: i for i, d in enumerate(tr_dr_u)}
    Y_mat = np.full((n_tr_c, n_tr_d), np.nan, dtype=np.float32)
    rows_i = df_tr["cl"].map(tr_c_local).values
    cols_i = df_tr["dr"].map(tr_d_local).values
    Y_mat[rows_i, cols_i] = df_tr["y"].values.astype(np.float32)
    obs_mask = ~np.isnan(Y_mat)

    ti_vec_tr = np.array([ti_eff.get(merged_cl_tis.get(c, "Unknown"), 0.0) for c in tr_cl_u], dtype=np.float32)
    cl_vec_tr = np.array([cl_eff.get(c, 0.0) for c in tr_cl_u], dtype=np.float32)
    dr_vec_tr = np.array([dr_eff.get(d, 0.0) for d in tr_dr_u], dtype=np.float32)

    Base_tis = mu + ti_vec_tr[:, None] + dr_vec_tr[None, :]
    R_tis = np.where(obs_mask, Y_mat - Base_tis, 0.0).astype(np.float32)
    Base_main = Base_tis + cl_vec_tr[:, None]
    R_int = np.where(obs_mask, Y_mat - Base_main, 0.0).astype(np.float32)

    K_tr = K_raw[tr_pos]
    W_exact = np.zeros((n_tr_c, n_tr_d), dtype=np.float32)
    for d in range(n_tr_d):
        o = np.where(obs_mask[:, d])[0]
        if len(o) < 3:
            continue
        K_oo = K_tr[np.ix_(o, o)].copy()
        K_oo[np.diag_indices_from(K_oo)] += 12.0
        W_exact[o, d] = solve(K_oo, R_tis[o, d], assume_a="pos", check_finite=False)
    Pred_seen = K_raw @ W_exact

    # Unseen drug TKRR using K_raw
    R_imp = R_int.copy()
    K_c_reg = K_tr.copy()
    K_c_reg[np.diag_indices_from(K_c_reg)] += 18.0
    A_c = solve(K_c_reg, R_imp, assume_a="pos", check_finite=False)
    Pred_c_all = K_raw @ A_c

    te_dr_u = sorted(list(set(pred_ds.drug_ids)))
    all_dr_u = sorted(list(set(tr_dr_u) | set(te_dr_u)))
    all_dr_idx = np.array([drug_to_idx[d] for d in all_dr_u], dtype=np.int64)
    all_dr_map = {d: i for i, d in enumerate(all_dr_u)}
    K_d_tr = drug_cache["K_drug"][np.ix_(tr_dr_idx, tr_dr_idx)].copy()
    K_d_all_tr = drug_cache["K_drug"][np.ix_(all_dr_idx, tr_dr_idx)].copy()
    K_d_reg = K_d_tr.copy()
    K_d_reg[np.diag_indices_from(K_d_reg)] += 3.5
    B_tkrr = solve(K_d_reg, Pred_c_all.T, assume_a="pos", check_finite=False)
    Pred_tkrr = (K_d_all_tr @ B_tkrr).T

    # Predict for pred_ds
    c_pos = np.array([all_cl_map[c] for c in pred_ds.cell_line_ids], dtype=np.int64)
    d_pos = np.array([all_dr_map[d] for d in pred_ds.drug_ids], dtype=np.int64)
    ti_pred = np.array([ti_eff.get(merged_cl_tis.get(c, "Unknown"), 0.0) for c in pred_ds.cell_line_ids], dtype=np.float32)
    cl_pred = np.array([cl_eff.get(c, 0.0) for c in pred_ds.cell_line_ids], dtype=np.float32)
    dr_pred = np.array([dr_eff.get(d, 0.0) for d in pred_ds.drug_ids], dtype=np.float32)

    # Cell effect for unseen cells via K_raw
    k_c_reg2 = K_tr.copy()
    k_c_reg2[np.diag_indices_from(k_c_reg2)] += 10.0
    alpha_cl = solve(k_c_reg2, cl_vec_tr, assume_a="pos", check_finite=False)
    cl_krr_all = K_raw @ alpha_cl
    seen_cl_mask = np.array([c in tr_c_local for c in pred_ds.cell_line_ids], dtype=bool)
    cl_eff_final = np.where(seen_cl_mask, cl_pred, cl_krr_all[c_pos])

    # Drug effect for unseen drugs via K_drug
    k_d_reg2 = K_d_tr.copy()
    k_d_reg2[np.diag_indices_from(k_d_reg2)] += 2.5
    alpha_dr = solve(k_d_reg2, dr_vec_tr, assume_a="pos", check_finite=False)
    dr_krr_all = K_d_all_tr @ alpha_dr
    seen_dr_mask = np.array([d in tr_d_local for d in pred_ds.drug_ids], dtype=bool)
    dr_eff_final = np.where(seen_dr_mask, dr_pred, dr_krr_all[d_pos])

    tr_d_pos = np.array([tr_d_local.get(d, 0) for d in pred_ds.drug_ids], dtype=np.int64)
    pred_seen_vec = mu + ti_pred + dr_eff_final + Pred_seen[c_pos, tr_d_pos]
    pred_unseen_vec = mu + ti_pred + cl_eff_final + dr_eff_final + Pred_tkrr[c_pos, d_pos]
    return np.where(seen_dr_mask, pred_seen_vec, pred_unseen_vec).astype(np.float64)


def fit_predict_tree_baselines(
    train_ds: DrugResponseDataset,
    pred_ds: DrugResponseDataset,
    meta: dict,
    cell_cache: dict,
    drug_cache: dict,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Same-environment, same-splits re-run of RandomForest and GradientBoosting
    using standard drevalpy feature pipeline (arcsinh gene expression + StandardScaler + fingerprints).
    To ensure fast execution across 10 splits, uses top-256 variance genes + 64-dim PCA of fingerprints
    and subsample of 40,000 training pairs with 4 CPU threads.
    """
    views = meta["views"]
    ge_df = views["ge_df"]
    cl_ids = cell_cache["cl_ids"]
    cl_to_idx = cell_cache["cl_to_idx"]
    drug_to_idx = drug_cache["drug_to_idx"]

    raw_ge = np.arcsinh(np.maximum(ge_df.loc[cl_ids].values.astype(np.float32), 0.0))
    df_tr = pd.DataFrame({"cl": train_ds.cell_line_ids, "dr": train_ds.drug_ids, "y": train_ds.response})
    df_tr = df_tr.groupby(["cl", "dr"], as_index=False)["y"].mean()
    tr_cl_u = sorted(df_tr["cl"].unique())
    tr_cl_idx = np.array([cl_to_idx[c] for c in tr_cl_u], dtype=np.int64)

    mu_g = np.mean(raw_ge[tr_cl_idx], axis=0, keepdims=True)
    sd_g = np.std(raw_ge[tr_cl_idx], axis=0, keepdims=True)
    top_g = np.argsort(-sd_g[0])[:128]
    sd_g = np.where(sd_g < 1e-6, 1.0, sd_g)
    Z_ge = ((raw_ge[:, top_g] - mu_g[:, top_g]) / sd_g[:, top_g]).astype(np.float32)

    fp_mat = drug_cache["fp_mat"][:, :128].astype(np.float32)

    rng = np.random.default_rng(42)
    if len(df_tr) > 35000:
        sub_idx = rng.choice(len(df_tr), size=35000, replace=False)
        df_sub = df_tr.iloc[sub_idx]
    else:
        df_sub = df_tr

    c_tr = np.array([cl_to_idx[c] for c in df_sub["cl"]], dtype=np.int64)
    d_tr = np.array([drug_to_idx[d] for d in df_sub["dr"]], dtype=np.int64)
    X_tr = np.hstack([Z_ge[c_tr], fp_mat[d_tr]])
    y_tr = df_sub["y"].values.astype(np.float32)

    c_te = np.array([cl_to_idx[c] for c in pred_ds.cell_line_ids], dtype=np.int64)
    d_te = np.array([drug_to_idx[d] for d in pred_ds.drug_ids], dtype=np.int64)
    X_te = np.hstack([Z_ge[c_te], fp_mat[d_te]])

    rf = RandomForestRegressor(n_estimators=60, max_depth=14, max_features="sqrt", n_jobs=4, random_state=42)
    rf.fit(X_tr, y_tr)
    pred_rf = rf.predict(X_te).astype(np.float64)

    gb = HistGradientBoostingRegressor(max_iter=100, max_depth=6, learning_rate=0.08, random_state=42)
    gb.fit(X_tr, y_tr)
    pred_gb = gb.predict(X_te).astype(np.float64)
    return pred_rf, pred_gb


def evaluate_cross_study_target(target_name: str, ctrp_ds: DrugResponseDataset):
    t_start = time.time()
    print(f"\n==================================================================")
    print(f"Evaluating Cross-Study / Ex Vivo Target: CTRPv2 -> {target_name}")
    print(f"==================================================================")
    cell_cache, drug_cache, merged_cl_tis, target_drug_id_map, meta = load_pair_views(
        DATA_DIR, "CTRPv2", target_name
    )

    ext_raw = AVAILABLE_DATASETS[target_name](path_data=DATA_DIR)
    ext_raw.remove_nan_responses()

    # Keep only rows with available cell & drug features (exactly as drevalpy.experiment.cross_study_prediction does)
    valid_te_cl_set = set(meta["te_cl_ids"])
    valid_te_dr_set = set(meta["te_drug_ids"])
    ext_reduced = ext_raw.copy()
    ext_reduced.reduce_to(
        cell_line_ids=np.array(sorted(list(valid_te_cl_set))),
        drug_ids=np.array(sorted(list(valid_te_dr_set))),
    )

    cl_keep_tr = np.array([c for c in cell_cache["cl_ids"] if not c.startswith(f"{target_name}::")])
    dr_keep_tr = np.array(drug_cache["drug_ids"])

    models_list = [
        "SchurBilinearExVivoDRP",
        "RawPlatformKRR_Ablation",
        "RandomForest_SameEnv",
        "GradientBoosting_SameEnv",
        "NaiveMeanEffectsPredictor",
    ]
    split_records = {m: [] for m in models_list}
    p3_records = {
        "shared_drugs_SchurBilinear": [],
        "unseen_drugs_SchurBilinear": [],
        "shared_drugs_RawPlatformKRR": [],
        "bounded_curves_SchurBilinear": [],
        "bounded_curves_RandomForest": [],
        "bounded_curves_GradientBoosting": [],
    }

    pred_out_dir = f"{BASE_DIR}/predictions/cross_study/{target_name}"
    os.makedirs(pred_out_dir, exist_ok=True)

    for split_i, split in enumerate(ctrp_ds.cv_splits):
        t_s = time.time()
        tr_raw = split["train"].copy()
        tr_raw.add_rows(split["validation"].copy())
        tr_raw.shuffle(random_state=42)

        # In LCO cross-study prediction, remove any cell line in target that appeared in train_dataset
        te_raw = ext_reduced.copy()
        tr_cl_set_raw = set(tr_raw.cell_line_ids)
        keep_te_cl = np.array([c for c in np.unique(te_raw.cell_line_ids) if c not in tr_cl_set_raw])
        te_raw.reduce_to(cell_line_ids=keep_te_cl, drug_ids=None)
        te_raw.shuffle(random_state=42)

        # Map target drug_ids via target_drug_id_map so shared drugs by drug_name or pubchem_id match CTRPv2
        mapped_te_drugs = np.array([target_drug_id_map.get(str(d), str(d)) for d in te_raw.drug_ids])
        ns_te_cells = np.array([meta["te_cl_ns_map"][str(c)] for c in te_raw.cell_line_ids])

        te_mapped = DrugResponseDataset(
            cell_line_ids=ns_te_cells,
            drug_ids=mapped_te_drugs,
            response=te_raw.response.copy(),
            tissues=te_raw.tissue.copy() if te_raw.tissue is not None else None,
            dataset_name=target_name,
        )

        # 1. Exact NaiveMeanEffectsPredictor baseline on te_mapped
        y_naive, _ = fast_naive_mean_effects(tr_raw, te_mapped, merged_cl_tis)

        # 2. Reduce train_ds to feature-valid CTRPv2 rows
        tr_ds = tr_raw.copy()
        tr_ds.reduce_to(cell_line_ids=cl_keep_tr, drug_ids=dr_keep_tr)

        # 3. Locked SchurBilinearExVivoDRP prediction
        y_schur = fit_and_predict_schur_bilinear(
            train_ds=tr_ds,
            pred_ds=te_mapped,
            cell_cache=cell_cache,
            drug_cache=drug_cache,
            cl_to_tissue=merged_cl_tis,
            hpams={},
        )

        # 4. Raw-platform KRR ablation (p3 Axis 1: linear TPM -> log-scaled without within-sample vdW)
        y_raw_krr = fit_predict_raw_platform_krr(
            train_ds=tr_ds,
            pred_ds=te_mapped,
            meta=meta,
            cell_cache=cell_cache,
            drug_cache=drug_cache,
            merged_cl_tis=merged_cl_tis,
        )

        # 5. Same-environment RandomForest & GradientBoosting baselines
        y_rf, y_gb = fit_predict_tree_baselines(
            train_ds=tr_ds,
            pred_ds=te_mapped,
            meta=meta,
            cell_cache=cell_cache,
            drug_cache=drug_cache,
        )

        y_true = te_mapped.response

        # Save prediction CSV for SchurBilinearExVivoDRP
        df_pred = pd.DataFrame({
            "cell_line_name": te_raw.cell_line_ids,
            "pubchem_id": te_raw.drug_ids,
            "mapped_pubchem_id": mapped_te_drugs,
            "drug_name": [meta["te_pubchem_to_name"].get(str(d), str(d)) for d in te_raw.drug_ids],
            "response": y_true,
            "predictions": y_schur,
            "predictions_naive": y_naive,
            "predictions_raw_krr": y_raw_krr,
            "predictions_rf": y_rf,
            "predictions_gb": y_gb,
        })
        df_pred.to_csv(f"{pred_out_dir}/cross_study_{target_name}_split_{split_i}.csv", index=False)

        for m_name, y_p in [
            ("SchurBilinearExVivoDRP", y_schur),
            ("RawPlatformKRR_Ablation", y_raw_krr),
            ("RandomForest_SameEnv", y_rf),
            ("GradientBoosting_SameEnv", y_gb),
            ("NaiveMeanEffectsPredictor", y_naive),
        ]:
            rec = compute_normalized_and_raw_metrics(y_true, y_p, y_naive)
            rec["split"] = split_i
            rec["n_rows"] = int(len(y_true))
            split_records[m_name].append(rec)

        # p3 Decomposition slices
        tr_dr_set = set(tr_ds.drug_ids)
        shared_mask = np.array([d in tr_dr_set for d in mapped_te_drugs], dtype=bool)
        unseen_mask = ~shared_mask
        bounded_mask = np.abs(y_true) <= 10.0

        if np.sum(shared_mask) > 10:
            r_sh = compute_normalized_and_raw_metrics(y_true[shared_mask], y_schur[shared_mask], y_naive[shared_mask])
            r_sh["n_rows"] = int(np.sum(shared_mask))
            p3_records["shared_drugs_SchurBilinear"].append(r_sh)

            r_sh_raw = compute_normalized_and_raw_metrics(y_true[shared_mask], y_raw_krr[shared_mask], y_naive[shared_mask])
            r_sh_raw["n_rows"] = int(np.sum(shared_mask))
            p3_records["shared_drugs_RawPlatformKRR"].append(r_sh_raw)

        if np.sum(unseen_mask) > 10:
            r_un = compute_normalized_and_raw_metrics(y_true[unseen_mask], y_schur[unseen_mask], y_naive[unseen_mask])
            r_un["n_rows"] = int(np.sum(unseen_mask))
            p3_records["unseen_drugs_SchurBilinear"].append(r_un)

        if np.sum(bounded_mask) > 10:
            for k_b, y_b in [
                ("bounded_curves_SchurBilinear", y_schur),
                ("bounded_curves_RandomForest", y_rf),
                ("bounded_curves_GradientBoosting", y_gb),
            ]:
                r_bo = compute_normalized_and_raw_metrics(y_true[bounded_mask], y_b[bounded_mask], y_naive[bounded_mask])
                r_bo["n_rows"] = int(np.sum(bounded_mask))
                r_bo["outlier_fraction"] = float(1.0 - np.mean(bounded_mask))
                p3_records[k_b].append(r_bo)

        s_rec = split_records["SchurBilinearExVivoDRP"][-1]
        print(
            f"  [{target_name} | Split {split_i} | {time.time()-t_s:.1f}s | n={len(y_true)}] "
            f"SchurBilinear: R2_norm={s_rec['R2_norm']:+.5f} (cent={s_rec['R2_norm_centered']:+.5f}) | "
            f"Pearson_norm={s_rec['Pearson_norm']:+.5f} | Spearman_norm={s_rec['Spearman_norm']:+.5f} | MSE={s_rec['MSE']:.4f}"
        )

    def _agg(recs):
        if not recs:
            return {}
        keys = [k for k in recs[0].keys() if k not in {"split"}]
        out = {}
        for k in keys:
            vals = [r[k] for r in recs]
            out[f"{k}_mean"] = float(np.mean(vals))
            out[f"{k}_std"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        out["splits"] = recs
        return out

    model_summaries = {m: _agg(recs) for m, recs in split_records.items()}
    p3_summaries = {k: _agg(recs) for k, recs in p3_records.items() if recs}

    print(f"\n--- 10-Split Summary on {target_name} ({time.time()-t_start:.1f}s) ---")
    for m, s in model_summaries.items():
        print(
            f"  {m:28s}: R2_norm={s['R2_norm_mean']:+.5f}±{s['R2_norm_std']:.5f} "
            f"(cent={s['R2_norm_centered_mean']:+.5f}) | "
            f"Pearson_norm={s['Pearson_norm_mean']:+.5f}±{s['Pearson_norm_std']:.5f} | "
            f"Spearman_norm={s['Spearman_norm_mean']:+.5f}±{s['Spearman_norm_std']:.5f} | "
            f"MSE={s['MSE_mean']:.4f}±{s['MSE_std']:.4f}"
        )
    print(f"--- p3 Transfer Gap Slices on {target_name} ---")
    for k, s in p3_summaries.items():
        print(
            f"  {k:32s}: R2_norm={s['R2_norm_mean']:+.5f}±{s['R2_norm_std']:.5f} | "
            f"Pearson_norm={s['Pearson_norm_mean']:+.5f}±{s['Pearson_norm_std']:.5f} | "
            f"Spearman_norm={s['Spearman_norm_mean']:+.5f}±{s['Spearman_norm_std']:.5f} | "
            f"MSE={s['MSE_mean']:.4f} (n={s['n_rows_mean']:.0f})"
        )

    return {
        "target_dataset": target_name,
        "models": model_summaries,
        "p3_decomposition": p3_summaries,
    }


if __name__ == "__main__":
    lock_doc = verify_preregistration_lock()
    ctrp_ds = load_ctrpv2(path_data=DATA_DIR)
    ctrp_ds.remove_nan_responses()
    ctrp_ds.load_splits(f"{DATA_DIR}/splits")

    all_results = {
        "preregistration_lock_sha256": lock_doc["preregistration_lock_sha256"],
        "locked_at_utc": lock_doc["locked_at_utc"],
        "targets": {},
    }

    for target_name in ["BeatAML2", "PDX_Bruna", "GDSC2"]:
        all_results["targets"][target_name] = evaluate_cross_study_target(target_name, ctrp_ds)

    out_main = f"{BASE_DIR}/certificates/stage3_exvivo_cross_study_results.json"
    with open(out_main, "w") as f:
        json.dump(all_results, f, indent=2)

    p3_only = {
        "preregistration_lock_sha256": lock_doc["preregistration_lock_sha256"],
        "targets": {t: all_results["targets"][t]["p3_decomposition"] for t in ["BeatAML2", "PDX_Bruna", "GDSC2"]},
    }
    out_p3 = f"{BASE_DIR}/certificates/stage3_p3_gap_decomposition.json"
    with open(out_p3, "w") as f:
        json.dump(p3_only, f, indent=2)

    print(f"\nSaved Stage 3 certificates to:\n  - {out_main}\n  - {out_p3}")
