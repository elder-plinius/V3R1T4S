"""
SchurBilinearExVivoDRP: Domain-Invariant Multi-Subspace Kernel & Bilinear Drug Response Predictor.
Engineered under Strict Air-Gap (Stage 2) on CTRPv2 inner validation (LCO, LTO, LDO).
"""
import os
import time
from typing import Any
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from drevalpy.datasets.dataset import DrugResponseDataset, FeatureDataset
from drevalpy.models.drp_model import DRPModel

from DREVAL_CAMPAIGN.src.stage2_inner_ablation import (
    within_sample_vdw,
    within_sample_log_zscore,
    _FullMatrixBilinearNet,
    fit_and_predict_schur_bilinear,
    precompute_cell_views,
    precompute_drug_views,
    fast_naive_mean_effects,
)


def load_pair_views(data_dir: str, train_name: str, target_name: str) -> tuple[dict, dict, dict, dict, dict]:
    """
    Loads and aligns all cell-line and drug views for (train_name, target_name) using the exact
    Stage 2 multi-view representation (intersecting gene subsets across train and target so zero
    missing-gene imputation is needed before within-sample van der Waerden normal scores).
    Target cell lines are namespaced as `{target_name}::{cl_id}` in `cell_cache` so target predictions
    always use the target study's own omics profiles.
    """
    t0 = time.time()
    ge_inter_raw = pd.read_csv(f"{data_dir}/meta/gene_lists/gene_expression_intersection.csv")["Symbol"].tolist()
    lm_genes_raw = pd.read_csv(f"{data_dir}/meta/gene_lists/landmark_genes.csv")["Symbol"].tolist()
    dt_genes_raw = pd.read_csv(f"{data_dir}/meta/gene_lists/drug_target_genes_all_drugs.csv")["Symbol"].tolist()
    pm_genes_raw = pd.read_csv(f"{data_dir}/meta/gene_lists/gene_list_paccmann_network_prop.csv")["Symbol"].tolist()

    with open(f"{data_dir}/{train_name}/DIPK_features/gene_list_sel.txt", encoding="gbk") as f:
        bionic_sel = [line.strip() for line in f if line.strip()]
    ppi_df = pd.read_csv(f"{data_dir}/{train_name}/DIPK_features/human_ppi_features.tsv", index_col=0, sep="\t")

    tr_ge_path = f"{data_dir}/{train_name}/gene_expression.csv"
    te_ge_path = f"{data_dir}/{target_name}/gene_expression.csv"
    tr_header = set(pd.read_csv(tr_ge_path, nrows=0).columns.tolist()) - {"cell_line_name"}
    te_header = set(pd.read_csv(te_ge_path, nrows=0).columns.tolist()) - {"cell_line_name"}
    common_header = tr_header & te_header

    ge_inter = [g for g in ge_inter_raw if g in common_header]
    valid_bionic_genes = [g for g in bionic_sel if g in ppi_df.index and g in common_header]
    lm_genes = [g for g in lm_genes_raw if g in common_header]
    dt_genes = [g for g in dt_genes_raw if g in common_header]
    pm_genes = [g for g in pm_genes_raw if g in common_header]

    union_genes = sorted(list(set(ge_inter) | set(valid_bionic_genes) | set(lm_genes) | set(dt_genes) | set(pm_genes)))

    def _read_ds_cell_views(ds_name: str):
        ge_full = pd.read_csv(f"{data_dir}/{ds_name}/gene_expression.csv", usecols=["cell_line_name"] + union_genes)
        ge_full["cell_line_name"] = ge_full["cell_line_name"].astype(str)
        ge_full = ge_full.groupby("cell_line_name", sort=False).mean()

        ge_df = ge_full[ge_inter].astype(np.float32)
        ge_lm_df = ge_full[lm_genes].astype(np.float32)
        ge_dt_df = ge_full[dt_genes].astype(np.float32)

        ge_b_vals = ge_full[valid_bionic_genes].values
        ppi_mat = ppi_df.loc[valid_bionic_genes].values.astype(np.float32)
        top256_idx = np.argpartition(-ge_b_vals, kth=min(256, ge_b_vals.shape[1] - 1), axis=1)[:, :256]
        bionic_mat = np.mean(ppi_mat[top256_idx], axis=1)
        bionic_df = pd.DataFrame(bionic_mat, index=ge_full.index)

        pw_df = pd.read_csv(f"{data_dir}/{ds_name}/pathway_features.csv", index_col=0)
        pw_df.index = pw_df.index.astype(str)
        pw_df = pw_df.groupby(level=0, sort=False).mean().astype(np.float32)

        cl_names = pd.read_csv(f"{data_dir}/{ds_name}/cell_line_names.csv", dtype=str).drop_duplicates("cell_line_name")
        cl_to_tissue = dict(zip(cl_names["cell_line_name"], cl_names["tissue"]))
        return ge_df, ge_lm_df, ge_dt_df, pw_df, bionic_df, cl_to_tissue

    def _read_ds_drug_views(ds_name: str):
        fp2048 = pd.read_csv(f"{data_dir}/{ds_name}/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv", index_col=None).T
        fp2048.index = fp2048.index.astype(str)
        has_fp = np.ones(len(fp2048), dtype=bool)
        for idx_i, drug in enumerate(fp2048.index):
            if fp2048.loc[drug].isna().all():
                has_fp[idx_i] = False
                rng = np.random.default_rng(hash(drug) % (2**32))
                fp2048.loc[drug] = rng.integers(0, 2, size=fp2048.shape[1])
        fp2048 = fp2048.astype(np.float32)
        has_fp_series = pd.Series(has_fp, index=fp2048.index)

        cb_df = pd.read_csv(f"{data_dir}/{ds_name}/drug_chemberta_embeddings.csv", dtype={"pubchem_id": str}).set_index("pubchem_id")
        cb_df = cb_df.groupby(level=0, sort=False).mean().astype(np.float32)

        sv_df = pd.read_csv(f"{data_dir}/{ds_name}/drug_smilesvec.csv", dtype={"pubchem_id": str}).set_index("pubchem_id")
        sv_df = sv_df.groupby(level=0, sort=False).mean().astype(np.float32)

        dn_df = pd.read_csv(f"{data_dir}/{ds_name}/drug_names.csv", dtype=str)
        pubchem_to_name = dict(zip(dn_df["pubchem_id"], dn_df["drug_name"]))
        return fp2048, has_fp_series, cb_df, sv_df, pubchem_to_name

    tr_ge, tr_lm, tr_dt, tr_pw, tr_bio, tr_cl_tis = _read_ds_cell_views(train_name)
    tr_fp, tr_has_fp, tr_cb, tr_sv, tr_pub2name = _read_ds_drug_views(train_name)

    dt_set, lm_set, pm_set = set(dt_genes), set(lm_genes), set(pm_genes)
    gene_weights = np.ones(len(ge_inter), dtype=np.float32)
    for i, g in enumerate(ge_inter):
        if g in dt_set:
            gene_weights[i] += 0.6
        if g in lm_set:
            gene_weights[i] += 0.3
        if g in pm_set:
            gene_weights[i] += 0.15

    if train_name == target_name:
        views = {
            "ge_df": tr_ge,
            "ge_lm_df": tr_lm,
            "ge_dt_df": tr_dt,
            "pw_df": tr_pw,
            "bionic_df": tr_bio,
            "cl_to_tissue": tr_cl_tis,
            "fp2048": tr_fp,
            "has_fp": tr_has_fp,
            "cb_df": tr_cb,
            "sv_df": tr_sv,
            "pubchem_to_name": tr_pub2name,
            "gene_weights": gene_weights,
        }
        cell_cache = precompute_cell_views(views)
        drug_cache = precompute_drug_views(views)
        target_drug_id_map = {d: d for d in drug_cache["drug_ids"]}
        return cell_cache, drug_cache, tr_cl_tis, target_drug_id_map, {
            "tr_pubchem_to_name": tr_pub2name,
            "te_pubchem_to_name": tr_pub2name,
            "te_cl_ids": sorted(list(set(tr_ge.index) & set(tr_pw.index) & set(tr_cl_tis.keys()))),
            "te_drug_ids": sorted(list(tr_fp.index)),
            "te_cl_to_tissue": tr_cl_tis,
            "views": views,
        }

    te_ge, te_lm, te_dt, te_pw, te_bio, te_cl_tis = _read_ds_cell_views(target_name)
    te_fp, te_has_fp, te_cb, te_sv, te_pub2name = _read_ds_drug_views(target_name)

    valid_te_cl = sorted(list(set(te_ge.index) & set(te_pw.index) & set(te_cl_tis.keys())))
    ns_map = {c: f"{target_name}::{c}" for c in valid_te_cl}

    te_ge_ns = te_ge.loc[valid_te_cl].copy()
    te_ge_ns.index = [ns_map[c] for c in valid_te_cl]
    te_lm_ns = te_lm.loc[valid_te_cl].copy()
    te_lm_ns.index = [ns_map[c] for c in valid_te_cl]
    te_dt_ns = te_dt.loc[valid_te_cl].copy()
    te_dt_ns.index = [ns_map[c] for c in valid_te_cl]
    te_pw_ns = te_pw.loc[valid_te_cl].reindex(columns=tr_pw.columns, fill_value=0.0).copy()
    te_pw_ns.index = [ns_map[c] for c in valid_te_cl]
    te_bio_ns = te_bio.loc[valid_te_cl].copy()
    te_bio_ns.index = [ns_map[c] for c in valid_te_cl]

    ge_df = pd.concat([tr_ge, te_ge_ns], axis=0)
    ge_lm_df = pd.concat([tr_lm, te_lm_ns], axis=0)
    ge_dt_df = pd.concat([tr_dt, te_dt_ns], axis=0)
    pw_df = pd.concat([tr_pw, te_pw_ns], axis=0)
    bionic_df = pd.concat([tr_bio, te_bio_ns], axis=0)

    merged_cl_tis = dict(tr_cl_tis)
    for c in valid_te_cl:
        merged_cl_tis[ns_map[c]] = te_cl_tis[c]

    # Merge drugs: map target drug to training pubchem_id if pubchem_id OR normalized drug_name matches
    tr_drug_set = set(tr_fp.index)
    tr_name_to_id = {}
    for d_id in tr_fp.index:
        nm = tr_pub2name.get(d_id, "").strip().lower()
        if nm:
            tr_name_to_id[nm] = d_id

    target_drug_id_map = {}
    new_dr = []
    for d_id in te_fp.index:
        if d_id in tr_drug_set:
            target_drug_id_map[d_id] = d_id
        else:
            nm = te_pub2name.get(d_id, "").strip().lower()
            if nm and nm in tr_name_to_id:
                target_drug_id_map[d_id] = tr_name_to_id[nm]
            else:
                target_drug_id_map[d_id] = d_id
                new_dr.append(d_id)

    fp2048 = pd.concat([tr_fp, te_fp.loc[new_dr]], axis=0)
    has_fp_series = pd.concat([tr_has_fp, te_has_fp.loc[new_dr]], axis=0)
    cb_df = pd.concat([tr_cb, te_cb.loc[[d for d in new_dr if d in te_cb.index]]], axis=0)
    sv_df = pd.concat([tr_sv, te_sv.loc[[d for d in new_dr if d in te_sv.index]]], axis=0)

    merged_pub2name = dict(tr_pub2name)
    merged_pub2name.update(te_pub2name)

    views = {
        "ge_df": ge_df,
        "ge_lm_df": ge_lm_df,
        "ge_dt_df": ge_dt_df,
        "pw_df": pw_df,
        "bionic_df": bionic_df,
        "cl_to_tissue": merged_cl_tis,
        "fp2048": fp2048,
        "has_fp": has_fp_series,
        "cb_df": cb_df,
        "sv_df": sv_df,
        "pubchem_to_name": merged_pub2name,
        "gene_weights": gene_weights,
    }
    cell_cache = precompute_cell_views(views)
    drug_cache = precompute_drug_views(views)
    shared_dr = sum(1 for d in te_fp.index if target_drug_id_map[d] in tr_drug_set)
    print(
        f"Loaded & aligned ({train_name} -> {target_name}) views in {time.time()-t0:.2f}s "
        f"(te_cl={len(valid_te_cl)}, te_dr={len(te_fp)}, shared_dr={shared_dr}, unseen_dr={len(new_dr)})"
    )
    return cell_cache, drug_cache, merged_cl_tis, target_drug_id_map, {
        "tr_pubchem_to_name": tr_pub2name,
        "te_pubchem_to_name": te_pub2name,
        "te_cl_ids": valid_te_cl,
        "te_cl_ns_map": ns_map,
        "te_drug_ids": sorted(list(te_fp.index)),
        "te_cl_to_tissue": te_cl_tis,
        "tr_drug_set": tr_drug_set,
        "views": views,
    }


class SchurBilinearExVivoDRP(DRPModel):
    """
    drevalpy-compatible wrapper for SchurBilinearExVivoDRP.
    """

    cell_line_views = ["gene_expression", "pathway_features", "bionic_features"]
    drug_views = ["fingerprints", "chemberta_features", "molgnet_features"]
    is_single_drug_model = False

    def __init__(self) -> None:
        super().__init__()
        self.hpams: dict[str, Any] = {}
        self.train_ds: DrugResponseDataset | None = None

    @classmethod
    def get_model_name(cls) -> str:
        return "SchurBilinearExVivoDRP"

    def build_model(self, hyperparameters: dict[str, Any]) -> None:
        self.hpams = dict(hyperparameters) if hyperparameters else {}

    def train(
        self,
        output: DrugResponseDataset,
        cell_line_input: FeatureDataset,
        drug_input: FeatureDataset | None = None,
        output_earlystopping: DrugResponseDataset | None = None,
        model_checkpoint_dir: str = "checkpoints",
    ) -> None:
        self.train_ds = output.copy()
        if output_earlystopping is not None and len(output_earlystopping) > 0:
            self.train_ds.add_rows(output_earlystopping.copy())

    def predict(
        self,
        cell_line_ids: np.ndarray,
        drug_ids: np.ndarray,
        cell_line_input: FeatureDataset,
        drug_input: FeatureDataset | None = None,
    ) -> np.ndarray:
        raise NotImplementedError("Use fit_and_predict_schur_bilinear with precomputed caches.")
