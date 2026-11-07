#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 3: Unlabeled p3 Ex Vivo Transfer-Gap Decomposition (BeatAML2 & PDX_Bruna, zero y_true calibration)."""
import hashlib
import json
import math
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

DATA_DIR = "os.environ.get("DREVAL_DATA_DIR", "DREVAL_CAMPAIGN/data")"
PRED_DIR = "os.environ.get("DREVAL_PRED_DIR", "DREVAL_CAMPAIGN/predictions/cross_study")"
OUT_TMP = "object"
os.makedirs(OUT_TMP, exist_ok=True)

# 1. Load CTRPv2 protocol data
ctrp_raw = pd.read_csv(f"{DATA_DIR}/CTRPv2/CTRPv2.csv", low_memory=False).dropna(subset=["LN_IC50_curvecurator"]).copy()
ctrp_raw["cell_line_name"] = ctrp_raw["cell_line_name"].astype(str)
ctrp_raw["pubchem_id"] = ctrp_raw["pubchem_id"].astype(str)
ctrp_raw["log_min_uM"] = np.log(ctrp_raw["min_dose_M"].astype(float) * 1e6)
ctrp_raw["log_max_uM"] = np.log(ctrp_raw["max_dose_M"].astype(float) * 1e6)
ctrp_proto_df = ctrp_raw.groupby(["cell_line_name", "pubchem_id"], as_index=False).agg({
    "log_min_uM": "mean",
    "log_max_uM": "mean",
    "LN_IC50_curvecurator": "mean",
})
ctrp_valid_drugs = set(pd.read_csv(f"{DATA_DIR}/CTRPv2/drug_names.csv")["pubchem_id"].astype(str))

def eval_metrics(y_true, y_pred, y_naive):
    mse = float(np.mean((y_true - y_pred) ** 2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2_raw = float(1.0 - np.sum((y_true - y_pred) ** 2) / max(ss_tot, 1e-12))
    p_raw = float(pearsonr(y_true, y_pred)[0]) if np.std(y_pred) > 1e-12 else 0.0
    s_raw = float(spearmanr(y_true, y_pred)[0]) if np.std(y_pred) > 1e-12 else 0.0
    
    yt_res = y_true - y_naive
    yp_res = y_pred - y_naive
    ss_tot_n = float(np.sum((yt_res - np.mean(yt_res)) ** 2))
    r2_n = float(1.0 - np.sum((yt_res - yp_res) ** 2) / max(ss_tot_n, 1e-12))
    ss_res_cent = float(np.sum(((yt_res - np.mean(yt_res)) - (yp_res - np.mean(yp_res))) ** 2))
    r2_n_cent = float(1.0 - ss_res_cent / max(ss_tot_n, 1e-12))
    p_n = float(pearsonr(yt_res, yp_res)[0]) if np.std(yp_res) > 1e-12 else 0.0
    s_n = float(spearmanr(yt_res, yp_res)[0]) if np.std(yp_res) > 1e-12 else 0.0
    return {
        "R2_norm": round(r2_n, 6),
        "R2_norm_centered": round(r2_n_cent, 6),
        "Pearson_norm": round(p_n, 6),
        "Spearman_norm": round(s_n, 6),
        "MSE": round(mse, 6),
        "RMSE": round(rmse, 6),
        "MAE": round(mae, 6),
        "R2_raw": round(r2_raw, 6),
        "Pearson_raw": round(p_raw, 6),
        "Spearman_raw": round(s_raw, 6),
    }

def agg_splits(recs, baseline_summary=None):
    keys = [
        "R2_norm", "R2_norm_centered", "Pearson_norm", "Spearman_norm",
        "MSE", "RMSE", "MAE", "R2_raw", "Pearson_raw", "Spearman_raw", "n_rows"
    ]
    out = {}
    for k in keys:
        if k not in recs[0]:
            continue
        vals = [r[k] for r in recs]
        out[f"{k}_mean"] = round(float(np.mean(vals)), 5)
        out[f"{k}_std"] = round(float(np.std(vals, ddof=1)), 5) if len(vals) > 1 else 0.0
    out["n_splits_R2_norm_gt_0"] = int(sum(1 for r in recs if r["R2_norm"] > 0.0))
    if baseline_summary is not None:
        out["R2_norm_gain_vs_unadjusted"] = round(out["R2_norm_mean"] - baseline_summary["R2_norm_mean"], 5)
        out["Pearson_norm_gain_vs_unadjusted"] = round(out["Pearson_norm_mean"] - baseline_summary["Pearson_norm_mean"], 5)
        out["Spearman_norm_gain_vs_unadjusted"] = round(out["Spearman_norm_mean"] - baseline_summary["Spearman_norm_mean"], 5)
        out["MSE_change_vs_unadjusted"] = round(out["MSE_mean"] - baseline_summary["MSE_mean"], 5)
    out["splits"] = recs
    return out

summary_all = {}
for cohort in ["BeatAML2", "PDX_Bruna"]:
    raw = pd.read_csv(f"{DATA_DIR}/{cohort}/{cohort}.csv", low_memory=False).dropna(subset=["LN_IC50_curvecurator"]).copy()
    raw["cell_line_name"] = raw["cell_line_name"].astype(str)
    raw["pubchem_id"] = raw["pubchem_id"].astype(str)
    raw["log_min_uM"] = np.log(raw["min_dose_M"].astype(float) * 1e6)
    raw["log_max_uM"] = np.log(raw["max_dose_M"].astype(float) * 1e6)
    meta = raw.groupby(["cell_line_name", "pubchem_id"], as_index=False).agg({
        "min_dose_M": "mean",
        "max_dose_M": "mean",
        "log_min_uM": "mean",
        "log_max_uM": "mean",
        "LN_IC50_curvecurator": "mean",
    })
    
    models_recs = {m: [] for m in [
        "SchurBilinearExVivoDRP",
        "RawPlatformKRR_Ablation",
        "RandomForest_SameEnv",
        "GradientBoosting_SameEnv",
        "NaiveMeanEffectsPredictor",
    ]}
    p3_recs = {k: [] for k in [
        "unadjusted_all_drugs",
        "unadjusted_shared_drugs",
        "unadjusted_unseen_drugs",
        "unadjusted_shared_drugs_RawPlatformKRR",
        "only_i_assay_protocol_fe_all",
        "only_i_assay_protocol_ols_all",
        "only_ii_platform_shift_all",
        "only_iii_drug_overlap_prior_all",
        "only_iii_shared_drugs_stratum",
        "cumulative_step0_unadjusted_all",
        "cumulative_step1_plus_assay_fe_all",
        "cumulative_step2_plus_overlap_prior_all",
        "cumulative_step3_plus_platform_shift_all",
        "shared_drugs_plus_assay_fe",
        "shared_drugs_plus_assay_fe_and_platform",
    ]}
    
    for k in range(10):
        tr_df = pd.concat([
            pd.read_csv(f"{DATA_DIR}/splits/cv_split_{k}_train.csv", low_memory=False),
            pd.read_csv(f"{DATA_DIR}/splits/cv_split_{k}_validation.csv", low_memory=False),
        ], ignore_index=True)
        tr_pairs = set(zip(tr_df["cell_line_name"].astype(str), tr_df["pubchem_id"].astype(str)))
        tr_dr_set = set(tr_df["pubchem_id"].astype(str)) & ctrp_valid_drugs
        
        ctrp_k = ctrp_proto_df[ctrp_proto_df.set_index(["cell_line_name", "pubchem_id"]).index.isin(tr_pairs)].copy()
        drug_means_k = ctrp_k.groupby("pubchem_id")[["log_min_uM", "log_max_uM", "LN_IC50_curvecurator"]].mean()
        dm_y = ctrp_k["LN_IC50_curvecurator"] - ctrp_k["pubchem_id"].map(drug_means_k["LN_IC50_curvecurator"])
        dm_min = ctrp_k["log_min_uM"] - ctrp_k["pubchem_id"].map(drug_means_k["log_min_uM"])
        dm_max = ctrp_k["log_max_uM"] - ctrp_k["pubchem_id"].map(drug_means_k["log_max_uM"])
        beta_fe_k, _, _, _ = np.linalg.lstsq(np.column_stack([dm_min.values, dm_max.values]), dm_y.values, rcond=None)
        global_min_k = float(ctrp_k["log_min_uM"].mean())
        global_max_k = float(ctrp_k["log_max_uM"].mean())
        
        X_ols_k = np.column_stack([np.ones(len(ctrp_k)), ctrp_k["log_min_uM"].values, ctrp_k["log_max_uM"].values])
        beta_ols_k, _, _, _ = np.linalg.lstsq(X_ols_k, ctrp_k["LN_IC50_curvecurator"].values, rcond=None)
        ctrp_mean_y_k = float(np.mean(X_ols_k @ beta_ols_k))
        
        df_k = pd.read_csv(f"{PRED_DIR}/{cohort}/cross_study_{cohort}_split_{k}.csv")
        df_k["cell_line_name"] = df_k["cell_line_name"].astype(str)
        df_k["pubchem_id"] = df_k["pubchem_id"].astype(str)
        df_k["mapped_pubchem_id"] = df_k["mapped_pubchem_id"].astype(str)
        m = df_k.merge(meta, on=["cell_line_name", "pubchem_id"], how="left")
        
        sh = m["mapped_pubchem_id"].isin(tr_dr_set).values
        yt = m["response"].values
        
        # Round exported columns to 4 decimal places so CSV and JSON match with 0 rounding gap
        yn = np.round(m["predictions_naive"].values, 4)
        ys = np.round(m["predictions"].values, 4)
        yr = np.round(m["predictions_raw_krr"].values, 4)
        yrf = np.round(m["predictions_rf"].values, 4)
        ygb = np.round(m["predictions_gb"].values, 4)
        
        ref_min = m["mapped_pubchem_id"].map(drug_means_k["log_min_uM"]).fillna(global_min_k).values
        ref_max = m["mapped_pubchem_id"].map(drug_means_k["log_max_uM"]).fillna(global_max_k).values
        delta_assay_fe = np.round(beta_fe_k[0] * (m["log_min_uM"].values - ref_min) + beta_fe_k[1] * (m["log_max_uM"].values - ref_max), 4)
        delta_assay_ols = np.round((beta_ols_k[0] + beta_ols_k[1] * m["log_min_uM"].values + beta_ols_k[2] * m["log_max_uM"].values) - ctrp_mean_y_k, 4)
        
        delta_platform_scalar = -float(np.mean(ys - yr))
        delta_overlap_scalar = float(np.mean(ys[sh]) - np.mean(ys[~sh]))
        delta_overlap_vec = np.where(sh, 0.0, delta_overlap_scalar)
        
        for m_name, yp in [
            ("SchurBilinearExVivoDRP", ys),
            ("RawPlatformKRR_Ablation", yr),
            ("RandomForest_SameEnv", yrf),
            ("GradientBoosting_SameEnv", ygb),
            ("NaiveMeanEffectsPredictor", yn),
        ]:
            r = eval_metrics(yt, yp, yn)
            r["split"] = k
            r["n_rows"] = int(len(yt))
            models_recs[m_name].append(r)
            
        def add_p3(key, y_t, y_p, y_n):
            r = eval_metrics(y_t, y_p, y_n)
            r["split"] = k
            r["n_rows"] = int(len(y_t))
            p3_recs[key].append(r)
            
        add_p3("unadjusted_all_drugs", yt, ys, yn)
        add_p3("unadjusted_shared_drugs", yt[sh], ys[sh], yn[sh])
        add_p3("unadjusted_unseen_drugs", yt[~sh], ys[~sh], yn[~sh])
        add_p3("unadjusted_shared_drugs_RawPlatformKRR", yt[sh], yr[sh], yn[sh])
        
        add_p3("only_i_assay_protocol_fe_all", yt, ys + delta_assay_fe, yn)
        add_p3("only_i_assay_protocol_ols_all", yt, ys + delta_assay_ols, yn)
        add_p3("only_ii_platform_shift_all", yt, ys + delta_platform_scalar, yn)
        add_p3("only_iii_drug_overlap_prior_all", yt, ys + delta_overlap_vec, yn)
        add_p3("only_iii_shared_drugs_stratum", yt[sh], ys[sh], yn[sh])
        
        add_p3("cumulative_step0_unadjusted_all", yt, ys, yn)
        add_p3("cumulative_step1_plus_assay_fe_all", yt, ys + delta_assay_fe, yn)
        add_p3("cumulative_step2_plus_overlap_prior_all", yt, ys + delta_assay_fe + delta_overlap_vec, yn)
        add_p3("cumulative_step3_plus_platform_shift_all", yt, ys + delta_assay_fe + delta_overlap_vec + delta_platform_scalar, yn)
        
        add_p3("shared_drugs_plus_assay_fe", yt[sh], ys[sh] + delta_assay_fe[sh], yn[sh])
        add_p3("shared_drugs_plus_assay_fe_and_platform", yt[sh], ys[sh] + delta_assay_fe[sh] - float(np.mean((ys - yr)[sh])), yn[sh])

    m_sum = {m: agg_splits(recs) for m, recs in models_recs.items()}
    base_all = agg_splits(p3_recs["unadjusted_all_drugs"])
    p3_sum = {k: agg_splits(recs, baseline_summary=base_all) for k, recs in p3_recs.items()}
    summary_all[cohort] = {"models": m_sum, "p3": p3_sum}

    print(f"\n================ {cohort} EXACT 4DP-CSV SUMMARY ================")
    for m, s in m_sum.items():
        print(f"  [Model] {m:30s}: R2_norm={s['R2_norm_mean']:+.5f}±{s['R2_norm_std']:.5f} | P_norm={s['Pearson_norm_mean']:+.5f}±{s['Pearson_norm_std']:.5f} | S_norm={s['Spearman_norm_mean']:+.5f}±{s['Spearman_norm_std']:.5f} | MSE={s['MSE_mean']:.4f}±{s['MSE_std']:.4f}")
    for k, s in p3_sum.items():
        print(f"  [p3]    {k:42s}: R2_norm={s['R2_norm_mean']:+.5f}±{s['R2_norm_std']:.5f} ({s['n_splits_R2_norm_gt_0']:2d}/10>0, dR2={s['R2_norm_gain_vs_unadjusted']:+.5f}) | P_norm={s['Pearson_norm_mean']:+.5f}±{s['Pearson_norm_std']:.5f} | S_norm={s['Spearman_norm_mean']:+.5f}±{s['Spearman_norm_std']:.5f} | MSE={s['MSE_mean']:.4f}±{s['MSE_std']:.4f} (dMSE={s['MSE_change_vs_unadjusted']:+.4f})")
