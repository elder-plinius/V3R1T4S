#!/usr/bin/env python3
"""
Step 4: Benchmark DualTanimotoKernelEngine + Protein/Ligand descriptors +
Two-Regime (Seen-Target + Cold/Unseen-Target) LightGBM & Ridge on strictly
train_val Inner Temporal Splits (Split A: 2013-2016 -> 2017-2018, Split B: 2013-2017 -> 2018).
Never touches `test`.
"""
import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")
import time
from pathlib import Path
from numba_dual_kernel import DualTanimotoKernelEngine
import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import GroupKFold
from tdc.benchmark_group import dti_dg_group

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"


def build_protein_similarity_and_svd(all_targets: list[str], prot_feats: np.ndarray, tv_target_mask: np.ndarray):
    """
    Compute multi-scale protein similarity matrix (combining 3-mer containment,
    2..4-mer TF-IDF cosine, and CTD+AAC+DPC cosine similarity) and 64-dim SVD of protein features.
    Fitted ONLY on train_val targets (`tv_target_mask`).
    """
    vec_tf = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), sublinear_tf=True)
    vec_tf.fit([all_targets[i] for i in np.nonzero(tv_target_mask)[0]])
    X_tf = vec_tf.transform(all_targets)
    sim_tf = cosine_similarity(X_tf)

    vec_c3 = CountVectorizer(analyzer="char", ngram_range=(3, 3), binary=True)
    vec_c3.fit([all_targets[i] for i in np.nonzero(tv_target_mask)[0]])
    X_c3 = vec_c3.transform(all_targets).astype(np.float32)
    inter = (X_c3 @ X_c3.T).toarray()
    lens = np.asarray(X_c3.sum(axis=1)).ravel()
    min_lens = np.minimum(lens[:, None], lens[None, :])
    contain3 = np.divide(inter, np.maximum(min_lens, 1.0))

    # Cosine similarity on standardized AAC + DPC + CTD (first 567 features)
    pf_sub = prot_feats[:, :567].copy()
    pf_mean = pf_sub[tv_target_mask].mean(axis=0, keepdims=True)
    pf_std = pf_sub[tv_target_mask].std(axis=0, keepdims=True) + 1e-6
    pf_norm = (pf_sub - pf_mean) / pf_std
    sim_ctd = np.clip(cosine_similarity(pf_norm), 0.0, 1.0)

    prot_sim = (0.40 * sim_tf + 0.35 * contain3 + 0.25 * sim_ctd).astype(np.float32)

    svd = TruncatedSVD(n_components=48, random_state=42)
    svd.fit(X_tf[tv_target_mask])
    prot_svd = svd.transform(X_tf).astype(np.float32)

    # Combine AAC (20) + CTD (147) + PhysChem (19) + SVD (48) = 234 compact protein features
    prot_compact = np.hstack([
        prot_feats[:, :20],      # AAC (20)
        prot_feats[:, 420:567],  # CTD (147)
        prot_feats[:, 567:],     # PhysChem (19)
        prot_svd,                # 2..4-mer TF-IDF SVD (48)
    ]).astype(np.float32)

    return prot_sim, prot_compact


def unpack_ecfp4_svd(fp_ecfp4: np.ndarray, tv_lig_mask: np.ndarray, n_components: int = 64) -> np.ndarray:
    """Compute fast 256-bucket folded Morgan count/bit projection from uint64[32] ECFP4."""
    # Fold 2048 bits (32 x uint64) into 256 bytes (or 128 floats via popcount per byte/half-word)
    u8 = fp_ecfp4.view(np.uint8)  # shape (n_lig, 256)
    # Bit-count lookup table for 0..255
    lut = np.array([bin(i).count("1") for i in range(256)], dtype=np.float32)
    folded_256 = lut[u8]  # (n_lig, 256), each entry in 0..8
    return folded_256


def evaluate_inner_split(
    name: str,
    tr_df: pd.DataFrame,
    va_df: pd.DataFrame,
    engine: DualTanimotoKernelEngine,
    prot_compact: np.ndarray,
    lig_folded: np.ndarray,
):
    t0 = time.time()
    print(f"\n==================== {name} ====================")
    tr_d = tr_df["d_idx"].values
    tr_t = tr_df["t_idx"].values
    tr_yr = tr_df["Year"].values
    tr_y = tr_df["Y"].values.astype(np.float32)
    tr_rid = tr_df["row_id"].values

    va_d = va_df["d_idx"].values
    va_t = va_df["t_idx"].values
    va_yr = va_df["Year"].values
    va_y = va_df["Y"].values.astype(np.float32)
    va_rid = va_df["row_id"].values

    print(f"Computing DualTanimotoKernel features for tr ({len(tr_df)}) and va ({len(va_df)})...")
    k_tr = engine.compute(tr_d, tr_t, tr_yr, tr_y, tr_rid, tr_d, tr_t, tr_yr, tr_rid)
    k_va = engine.compute(tr_d, tr_t, tr_yr, tr_y, tr_rid, va_d, va_t, va_yr, va_rid)
    print(f"  Kernel features computed in {time.time() - t0:.2f}s!")

    seen_mask = k_va[:, 0] > 0.0
    unseen_mask = ~seen_mask
    print(f"  va rows: {len(va_df)} (seen_target: {seen_mask.sum()}, unseen_target: {unseen_mask.sum()})")

    # Check raw kernel feature PCCs on va
    for idx_f, fname in [
        (1, "t_mean_i"),
        (3, "t_rec_i"),
        (8, "knn_p2"),
        (9, "knn_p6"),
        (10, "knn_p12"),
        (11, "knn_p6_rec"),
        (17, "oos_knn_p6"),
        (25, "exact_pair_y"),
        (27, "same_t_scaf_y"),
        (30, "global_can_y"),
        (32, "global_scaf_y"),
        (38, "hom_dual_p4"),
        (40, "hom_dual_resid_p6"),
        (42, "glob_knn_y4"),
    ]:
        r_all = pearsonr(k_va[:, idx_f], va_y)[0]
        r_seen = pearsonr(k_va[seen_mask, idx_f], va_y[seen_mask])[0] if seen_mask.sum() > 10 else 0.0
        r_unseen = pearsonr(k_va[unseen_mask, idx_f], va_y[unseen_mask])[0] if unseen_mask.sum() > 10 else 0.0
        print(f"  Raw Feature [{idx_f:2d} {fname:18s}]: All PCC={r_all:.5f} | Seen PCC={r_seen:.5f} | Unseen PCC={r_unseen:.5f}")


def main():
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"].copy()

    prot_npz = np.load(CACHE_DIR / "protein_features.npz", allow_pickle=True)
    all_targets = list(prot_npz["targets"])
    prot_feats = prot_npz["prot_feats"]
    t_to_idx = {t: i for i, t in enumerate(all_targets)}

    lig_npz = np.load(CACHE_DIR / "ligand_features.npz", allow_pickle=True)
    all_smiles = list(lig_npz["smiles"])
    d_to_idx = {s: i for i, s in enumerate(all_smiles)}

    tv["t_idx"] = tv["Target"].map(t_to_idx).astype(np.int32)
    tv["d_idx"] = tv["Drug"].map(d_to_idx).astype(np.int32)
    tv["row_id"] = np.arange(len(tv), dtype=np.int32)

    tv_target_mask = np.isin(np.arange(len(all_targets)), tv["t_idx"].unique())
    tv_lig_mask = np.isin(np.arange(len(all_smiles)), tv["d_idx"].unique())

    prot_sim, prot_compact = build_protein_similarity_and_svd(all_targets, prot_feats, tv_target_mask)
    lig_folded = unpack_ecfp4_svd(lig_npz["fp_ecfp4"], tv_lig_mask)

    engine = DualTanimotoKernelEngine(CACHE_DIR, prot_sim)

    # Warmup & evaluate Split A (2013-2016 -> 2017-2018) and Split B (2013-2017 -> 2018)
    evaluate_inner_split(
        "Inner Temporal A (2013-2016 -> 2017-2018)",
        tv[tv["Year"] <= 2016],
        tv[tv["Year"] >= 2017],
        engine,
        prot_compact,
        lig_folded,
    )
    evaluate_inner_split(
        "Inner Temporal B (2013-2017 -> 2018)",
        tv[tv["Year"] <= 2017],
        tv[tv["Year"] == 2018],
        engine,
        prot_compact,
        lig_folded,
    )


if __name__ == "__main__":
    main()
