#!/usr/bin/env python3
"""
Step 3: Fast prototype of Target-Conditioned Ligand Tanimoto Transfer +
Homology-Transfer Cross-Target Kernel on strictly train_val Inner Temporal Splits:
  - Split A: 2013-2016 -> 2017-2018
  - Split B: 2013-2017 -> 2018
Never touches `test`.
"""
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, MACCSkeys
from tdc.benchmark_group import dti_dg_group

RDLogger.DisableLog("rdApp.*")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def compute_protein_sim_matrix(unique_targets: list[str]) -> np.ndarray:
    """Compute multi-scale k-mer (1,2,3,4-mer) TF-IDF + char cosine similarity between proteins."""
    vec3 = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), sublinear_tf=True)
    X3 = vec3.fit_transform(unique_targets)
    sim3 = cosine_similarity(X3)

    vec_cnt = CountVectorizer(analyzer="char", ngram_range=(3, 3), binary=True)
    X_bin = vec_cnt.fit_transform(unique_targets).astype(np.float32)
    inter = (X_bin @ X_bin.T).toarray()
    norms = np.asarray(X_bin.sum(axis=1)).ravel()
    union = norms[:, None] + norms[None, :] - inter
    jaccard3 = np.divide(inter, np.maximum(union, 1.0))

    return 0.5 * sim3 + 0.5 * jaccard3


def main():
    t0 = time.time()
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"].copy()

    # Check protein similarity on Inner Temporal A (2013-2016 -> 2017-2018)
    unique_targets = sorted(tv["Target"].unique())
    t_to_idx = {t: i for i, t in enumerate(unique_targets)}
    tv["t_idx"] = tv["Target"].map(t_to_idx)

    sim_prot = compute_protein_sim_matrix(unique_targets)
    print(f"Computed {len(unique_targets)}x{len(unique_targets)} protein similarity matrix in {time.time()-t0:.2f}s")

    # Inspect unseen targets in 2017-2018 vs 2013-2016: what is their max similarity to 2013-2016 targets?
    trA = tv[tv["Year"] <= 2016]
    vaA = tv[tv["Year"] >= 2017]
    trA_t_idxs = sorted(trA["t_idx"].unique())
    vaA_t_idxs = sorted(vaA["t_idx"].unique())
    unseenA_t_idxs = sorted(set(vaA_t_idxs) - set(trA_t_idxs))

    sub_sim = sim_prot[np.ix_(unseenA_t_idxs, trA_t_idxs)]
    max_sims = sub_sim.max(axis=1)
    print(f"Split A (2013-2016 -> 2017-2018): {len(unseenA_t_idxs)} unseen targets.")
    print(f"  Max protein sim to seen targets: min={max_sims.min():.3f}, median={np.median(max_sims):.3f}, "
          f"mean={max_sims.mean():.3f}, >0.8: {(max_sims > 0.8).sum()}/{len(max_sims)}, >0.5: {(max_sims > 0.5).sum()}/{len(max_sims)}")

    # Test pure Homology Transfer of Target Mean on Unseen Targets in Split A!
    t_mean_trA = trA.groupby("t_idx")["Y"].mean()
    t_cnt_trA = trA.groupby("t_idx")["Y"].count()
    global_mean_A = trA["Y"].mean()
    t_smooth_A = (t_mean_trA * t_cnt_trA + global_mean_A * 5.0) / (t_cnt_trA + 5.0)

    trA_t_arr = np.array(trA_t_idxs)
    trA_y_arr = np.array([t_smooth_A[i] for i in trA_t_idxs])

    vaA_unseen = vaA[~vaA["t_idx"].isin(set(trA_t_idxs))]
    for power in [2, 4, 8, 16, 32]:
        pred_unseen_t = {}
        for u_idx in unseenA_t_idxs:
            s = sim_prot[u_idx, trA_t_arr]
            w = np.power(np.maximum(s - 0.15, 0.0), power)
            if w.sum() > 1e-12:
                pred_unseen_t[u_idx] = float(np.dot(w, trA_y_arr) / w.sum())
            else:
                pred_unseen_t[u_idx] = global_mean_A
        preds = vaA_unseen["t_idx"].map(pred_unseen_t).values
        r_u, _ = pearsonr(preds, vaA_unseen["Y"].values)
        print(f"  Unseen Targets (n={len(vaA_unseen)}) Homology-Transferred Target Mean (power={power:2d}): PCC = {r_u:.5f}")


if __name__ == "__main__":
    main()
