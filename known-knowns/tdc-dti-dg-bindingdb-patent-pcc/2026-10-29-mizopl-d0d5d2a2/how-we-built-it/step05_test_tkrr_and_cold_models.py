#!/usr/bin/env python3
"""
Step 5: Test Per-Target Tanimoto Kernel Ridge Regression (TKRR: RKHS Kriging on
ECFP4 + ECFP6 + FCFP4 + MACCS) and Cold/Unseen-Target Specialist models on:
  - Inner Temporal Split A (2013-2016 -> 2017-2018)
  - Inner Temporal Split B (2013-2017 -> 2018)
  - Official Seed 1 Split (train -> valid)
Never touches `test`.
"""
import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")
import time
from pathlib import Path
import numba as nb
import numpy as np
import pandas as pd
from scipy.linalg import cho_factor, cho_solve
from scipy.stats import pearsonr
from numba_dual_kernel import DualTanimotoKernelEngine, popcnt_u64, tanimoto_32, tanimoto_16, tanimoto_3
from tdc.benchmark_group import dti_dg_group

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"


@nb.njit(parallel=True, fastmath=True, cache=True)
def compute_pairwise_tanimoto_matrix(
    d_idx_a: np.ndarray,
    d_idx_b: np.ndarray,
    fp_ecfp4: np.ndarray,
    fp_ecfp6: np.ndarray,
    fp_fcfp4: np.ndarray,
    fp_maccs: np.ndarray,
    pop_e4: np.ndarray,
    pop_e6: np.ndarray,
    pop_f4: np.ndarray,
    pop_mc: np.ndarray,
) -> np.ndarray:
    na = d_idx_a.shape[0]
    nb_len = d_idx_b.shape[0]
    K = np.zeros((na, nb_len), dtype=np.float32)
    for i in nb.prange(na):
        da = d_idx_a[i]
        a_e4 = fp_ecfp4[da]
        a_e6 = fp_ecfp6[da]
        a_f4 = fp_fcfp4[da]
        a_mc = fp_maccs[da]
        pa4 = pop_e4[da]
        pa6 = pop_e6[da]
        paf = pop_f4[da]
        pam = pop_mc[da]
        for j in range(nb_len):
            db = d_idx_b[j]
            if da == db:
                K[i, j] = 1.0
                continue
            s4 = tanimoto_32(a_e4, fp_ecfp4[db], pa4, pop_e4[db])
            s6 = tanimoto_16(a_e6, fp_ecfp6[db], pa6, pop_e6[db])
            sf = tanimoto_16(a_f4, fp_fcfp4[db], paf, pop_f4[db])
            sm = tanimoto_3(a_mc, fp_maccs[db], pam, pop_mc[db])
            K[i, j] = 0.45 * s4 + 0.25 * s6 + 0.20 * sf + 0.10 * sm
    return K


def fit_predict_per_target_tkrr(
    engine: DualTanimotoKernelEngine,
    tr_d: np.ndarray,
    tr_t: np.ndarray,
    tr_yr: np.ndarray,
    tr_y: np.ndarray,
    va_d: np.ndarray,
    va_t: np.ndarray,
) -> np.ndarray:
    """
    For each target t present in both tr and va:
      - Deduplicate training ligands on target t (with recency-weighted average Y and count weight)
      - Compute exact multi-fingerprint Tanimoto Gram matrix K_tt (n_u x n_u) and cross-matrix K_vt (n_v x n_u)
      - Solve weighted Tanimoto Kernel Ridge Regression (TKRR) for:
          (0) K^1 with alpha=0.3
          (1) K^2 with alpha=0.2
          (2) (0.5 K^1 + 0.5 K^3) with alpha=0.15
          (3) Recency-weighted K^2 with alpha=0.2
          (4) GP predictive variance: 1 - diag(K_vt (K_tt + 0.2 I)^-1 K_vt^T)
    Returns va_tkrr_preds of shape (len(va_d), 5).
    """
    global_mean = float(tr_y.mean())
    max_yr = int(tr_yr.max())
    n_va = len(va_d)
    out = np.zeros((n_va, 5), dtype=np.float32)
    out[:, :4] = global_mean
    out[:, 4] = 1.0  # predictive variance = 1.0 when unseen

    # Group tr and va indices by target
    tr_by_t = {}
    for idx, t in enumerate(tr_t):
        tr_by_t.setdefault(int(t), []).append(idx)

    va_by_t = {}
    for idx, t in enumerate(va_t):
        va_by_t.setdefault(int(t), []).append(idx)

    for t, va_rows in va_by_t.items():
        va_idx = np.array(va_rows, dtype=np.int32)
        if t not in tr_by_t:
            continue
        tr_idx = np.array(tr_by_t[t], dtype=np.int32)
        d_tr = tr_d[tr_idx]
        y_tr = tr_y[tr_idx]
        yr_tr = tr_yr[tr_idx]

        # Collapse duplicate d_idx on target t
        order = np.argsort(d_idx_tr := d_tr, kind="mergesort")
        sd = d_idx_tr[order]
        sy = y_tr[order]
        syr = yr_tr[order]
        w_rec = np.exp(0.35 * (syr - max_yr)).astype(np.float32)

        uniq_d, idx_start, counts = np.unique(sd, return_index=True, return_counts=True)
        u_mean_y = (np.add.reduceat(sy, idx_start) / counts).astype(np.float32)
        u_rec_y = (np.add.reduceat(sy * w_rec, idx_start) / np.add.reduceat(w_rec, idx_start)).astype(np.float32)
        u_rec_w = (np.add.reduceat(w_rec, idx_start) / counts).astype(np.float32)

        n_u = len(uniq_d)
        t_prior = float((y_tr.sum() + 5.0 * global_mean) / (len(y_tr) + 5.0))
        t_rec_prior = float(((y_tr * np.exp(0.35 * (yr_tr - max_yr))).sum() + 2.0 * global_mean) / (np.exp(0.35 * (yr_tr - max_yr)).sum() + 2.0))

        y_cent = u_mean_y - t_prior
        y_rec_cent = u_rec_y - t_rec_prior

        K_tt = compute_pairwise_tanimoto_matrix(
            uniq_d, uniq_d,
            engine.fp_ecfp4, engine.fp_ecfp6, engine.fp_fcfp4, engine.fp_maccs,
            engine.pop_e4, engine.pop_e6, engine.pop_f4, engine.pop_mc,
        )
        d_va = va_d[va_idx]
        K_vt = compute_pairwise_tanimoto_matrix(
            d_va, uniq_d,
            engine.fp_ecfp4, engine.fp_ecfp6, engine.fp_fcfp4, engine.fp_maccs,
            engine.pop_e4, engine.pop_e6, engine.pop_f4, engine.pop_mc,
        )

        idx_diag = np.arange(n_u)

        # (0) K^1, alpha = 0.30
        A1 = K_tt.copy()
        A1[idx_diag, idx_diag] += 0.30 / np.sqrt(counts.astype(np.float32))
        c1, low1 = cho_factor(A1, lower=True, check_finite=False)
        w1 = cho_solve((c1, low1), y_cent, check_finite=False)
        out[va_idx, 0] = t_prior + K_vt @ w1

        # (1) K^2, alpha = 0.15
        K2_tt = K_tt * K_tt
        K2_vt = K_vt * K_vt
        A2 = K2_tt.copy()
        A2[idx_diag, idx_diag] += 0.15 / np.sqrt(counts.astype(np.float32))
        c2, low2 = cho_factor(A2, lower=True, check_finite=False)
        w2 = cho_solve((c2, low2), y_cent, check_finite=False)
        out[va_idx, 1] = t_prior + K2_vt @ w2

        # (2) Mixed Polynomial Tanimoto Kernel (0.4 K + 0.4 K^2 + 0.2 K^4), alpha = 0.12
        K4_tt = K2_tt * K2_tt
        K4_vt = K2_vt * K2_vt
        Km_tt = 0.40 * K_tt + 0.40 * K2_tt + 0.20 * K4_tt
        Km_vt = 0.40 * K_vt + 0.40 * K2_vt + 0.20 * K4_vt
        Am = Km_tt.copy()
        Am[idx_diag, idx_diag] += 0.12 / np.sqrt(counts.astype(np.float32))
        cm, lowm = cho_factor(Am, lower=True, check_finite=False)
        wm = cho_solve((cm, lowm), y_cent, check_finite=False)
        out[va_idx, 2] = t_prior + Km_vt @ wm

        # (3) Recency-weighted Mixed Tanimoto Kernel
        Ar = Km_tt.copy()
        Ar[idx_diag, idx_diag] += 0.12 / (u_rec_w * np.sqrt(counts.astype(np.float32)))
        cr, lowr = cho_factor(Ar, lower=True, check_finite=False)
        wr = cho_solve((cr, lowr), y_rec_cent, check_finite=False)
        out[va_idx, 3] = t_rec_prior + Km_vt @ wr

        # (4) Max similarity on target t as proxy for GP confidence
        out[va_idx, 4] = K_vt.max(axis=1)

    return out


def main():
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"].copy()

    prot_npz = np.load(CACHE_DIR / "protein_features.npz", allow_pickle=True)
    all_targets = list(prot_npz["targets"])
    t_to_idx = {t: i for i, t in enumerate(all_targets)}

    lig_npz = np.load(CACHE_DIR / "ligand_features.npz", allow_pickle=True)
    all_smiles = list(lig_npz["smiles"])
    d_to_idx = {s: i for i, s in enumerate(all_smiles)}

    tv["t_idx"] = tv["Target"].map(t_to_idx).astype(np.int32)
    tv["d_idx"] = tv["Drug"].map(d_to_idx).astype(np.int32)
    tv["row_id"] = np.arange(len(tv), dtype=np.int32)

    prot_sim = np.eye(len(all_targets), dtype=np.float32)
    engine = DualTanimotoKernelEngine(CACHE_DIR, prot_sim)

    for name, tr_df, va_df in [
        ("Inner Temporal A (2013-2016 -> 2017-2018)", tv[tv["Year"] <= 2016], tv[tv["Year"] >= 2017]),
        ("Inner Temporal B (2013-2017 -> 2018)", tv[tv["Year"] <= 2017], tv[tv["Year"] == 2018]),
    ]:
        t0 = time.time()
        tkrr_va = fit_predict_per_target_tkrr(
            engine,
            tr_df["d_idx"].values, tr_df["t_idx"].values, tr_df["Year"].values, tr_df["Y"].values.astype(np.float32),
            va_df["d_idx"].values, va_df["t_idx"].values,
        )
        dt = time.time() - t0
        va_y = va_df["Y"].values.astype(np.float32)
        seen_mask = va_df["t_idx"].isin(set(tr_df["t_idx"])).values
        print(f"\n=== {name} (TKRR solved in {dt:.2f}s) ===")
        for k, kname in enumerate(["TKRR-K1", "TKRR-K2", "TKRR-Mix(1,2,4)", "TKRR-RecencyMix"]):
            r_all = pearsonr(tkrr_va[:, k], va_y)[0]
            r_seen = pearsonr(tkrr_va[seen_mask, k], va_y[seen_mask])[0]
            print(f"  {kname:18s}: All PCC = {r_all:.5f} | Seen-Target PCC = {r_seen:.5f}")


if __name__ == "__main__":
    main()
