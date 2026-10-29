#!/usr/bin/env python3
"""
Step 8: Official 5-Seed Evaluation, ERM Baseline Reproduction (p2), Unseen-Target
Generalization (p3), 10,000-Resample Bootstrap, and SHA-256 Certificate Generation
for `tdc-dti-dg-bindingdb-patent-pcc` (`BindingDB_Patent` in `DTI_DG_Group`).
"""
import os
os.environ["NUMBA_THREADING_LAYER"] = "workqueue"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import hashlib
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from tdc.benchmark_group import dti_dg_group

from step07_test_full_modular_stack_splits import (
    UnifiedDTIDGFeatureEngine,
    fit_predict_two_regime_ensemble_v3,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
PRED_DIR = BASE_DIR / "predictions"
PRED_DIR.mkdir(parents=True, exist_ok=True)


def build_temporal_oof_late_years(
    engine: UnifiedDTIDGFeatureEngine,
    tr_d: np.ndarray,
    tr_p: np.ndarray,
    tr_yr: np.ndarray,
    tr_y: np.ndarray,
    tr_rid: np.ndarray,
    min_eval_yr: int = 2016,
):
    years = [yr for yr in sorted(np.unique(tr_yr).tolist()) if yr >= min_eval_yr]
    oof_X, oof_y, oof_yr = [], [], []
    for yr in years:
        hist_mask = tr_yr < yr
        curr_mask = tr_yr == yr
        if np.sum(hist_mask) < 500 or np.sum(curr_mask) < 100:
            continue
        X_yr = engine.extract_all_features(
            tr_d[hist_mask], tr_p[hist_mask], tr_yr[hist_mask], tr_y[hist_mask], tr_rid[hist_mask],
            tr_d[curr_mask], tr_p[curr_mask], tr_yr[curr_mask], tr_rid[curr_mask],
        )
        oof_X.append(X_yr)
        oof_y.append(tr_y[curr_mask])
        oof_yr.append(tr_yr[curr_mask])
    return np.vstack(oof_X), np.concatenate(oof_y), np.concatenate(oof_yr)


def train_predict_erm_baseline_5seeds(
    group,
    bm,
    engine: UnifiedDTIDGFeatureEngine,
    t_to_idx: dict,
    d_to_idx: dict,
):
    import lightgbm as lgb

    te_df = bm["test"]
    te_p = te_df["Target"].map(t_to_idx).values.astype(np.int32)
    te_d = te_df["Drug"].map(d_to_idx).values.astype(np.int32)

    X_te_erm = np.hstack([engine.U_lig_232[te_d], engine.V_prot_all[te_p]]).astype(np.float32)

    erm_preds_list = []
    erm_seed_pccs = []

    for seed in [1, 2, 3, 4, 5]:
        tr_df, va_df = group.get_train_valid_split(benchmark="BindingDB_Patent", split_type="default", seed=seed)
        tr_p = tr_df["Target"].map(t_to_idx).values.astype(np.int32)
        tr_d = tr_df["Drug"].map(d_to_idx).values.astype(np.int32)
        tr_y = tr_df["Y"].values.astype(np.float32)

        X_tr_erm = np.hstack([engine.U_lig_232[tr_d], engine.V_prot_all[tr_p]]).astype(np.float32)

        erm_model = lgb.LGBMRegressor(
            objective="regression",
            n_estimators=400,
            learning_rate=0.05,
            num_leaves=31,
            random_state=seed,
            n_jobs=1,
            verbose=-1,
        )
        erm_model.fit(X_tr_erm, tr_y)
        pred_te_erm = erm_model.predict(X_te_erm).astype(np.float32)
        erm_preds_list.append({bm["name"]: pred_te_erm})
        ev = group.evaluate({bm["name"]: pred_te_erm})
        erm_seed_pccs.append(float(pearsonr(te_df["Y"].values.astype(np.float32), pred_te_erm)[0]))

    erm_eval_many = group.evaluate_many(erm_preds_list)
    return erm_preds_list, erm_seed_pccs, erm_eval_many


def run_bootstrap_10000(y_true: np.ndarray, y_pred: np.ndarray, thresholds=(0.538, 0.588), n_boot: int = 10000, seed: int = 20261029):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    y_t = y_true.astype(np.float64)
    y_p = y_pred.astype(np.float64)

    boot_pccs = np.empty(n_boot, dtype=np.float64)
    chunk = 200
    for start in range(0, n_boot, chunk):
        end = min(n_boot, start + chunk)
        b = end - start
        idx = rng.integers(0, n, size=(b, n), dtype=np.int32)
        yt_b = y_t[idx]
        yp_b = y_p[idx]
        yt_c = yt_b - yt_b.mean(axis=1, keepdims=True)
        yp_c = yp_b - yp_b.mean(axis=1, keepdims=True)
        num = np.sum(yt_c * yp_c, axis=1)
        den = np.sqrt(np.sum(yt_c * yt_c, axis=1) * np.sum(yp_c * yp_c, axis=1))
        boot_pccs[start:end] = num / np.maximum(den, 1e-12)

    res = {
        "n_resamples": n_boot,
        "boot_mean_pcc": float(np.mean(boot_pccs)),
        "boot_std_pcc": float(np.std(boot_pccs)),
        "ci_95_lower": float(np.percentile(boot_pccs, 2.5)),
        "ci_95_upper": float(np.percentile(boot_pccs, 97.5)),
    }
    for thr in thresholds:
        res[f"win_rate_vs_{thr:.3f}"] = float(np.mean(boot_pccs > thr))
    return res


def compute_year_and_subset_breakdown(te_y, te_yr, te_seen_t_mask, te_unseen_t_mask, te_unseen_d_mask, preds_5seeds):
    """
    Computes 5-seed mean & std of per-year PCC (2019, 2020, 2021), Seen-Target PCC,
    Unseen-Target PCC (`p3`), and Unseen-Ligand PCC.
    """
    per_year = {}
    for yr in [2019, 2020, 2021]:
        m = te_yr == yr
        vals = [float(pearsonr(te_y[m], p[m])[0]) for p in preds_5seeds]
        per_year[str(yr)] = {
            "n_rows": int(np.sum(m)),
            "mean_pcc": float(np.mean(vals)),
            "std_pcc": float(np.std(vals)),
            "per_seed": vals,
        }

    seen_vals = [float(pearsonr(te_y[te_seen_t_mask], p[te_seen_t_mask])[0]) for p in preds_5seeds]
    unseen_t_vals = [float(pearsonr(te_y[te_unseen_t_mask], p[te_unseen_t_mask])[0]) for p in preds_5seeds]
    unseen_d_vals = [float(pearsonr(te_y[te_unseen_d_mask], p[te_unseen_d_mask])[0]) for p in preds_5seeds]

    return {
        "per_year": per_year,
        "seen_target": {
            "n_rows": int(np.sum(te_seen_t_mask)),
            "mean_pcc": float(np.mean(seen_vals)),
            "std_pcc": float(np.std(seen_vals)),
            "per_seed": seen_vals,
        },
        "unseen_target_p3": {
            "n_rows": int(np.sum(te_unseen_t_mask)),
            "mean_pcc": float(np.mean(unseen_t_vals)),
            "std_pcc": float(np.std(unseen_t_vals)),
            "per_seed": unseen_t_vals,
        },
        "unseen_ligand": {
            "n_rows": int(np.sum(te_unseen_d_mask)),
            "mean_pcc": float(np.mean(unseen_d_vals)),
            "std_pcc": float(np.std(unseen_d_vals)),
            "per_seed": unseen_d_vals,
        },
    }


def main():
    t0_all = time.time()
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv_df = bm["train_val"].copy()
    te_df = bm["test"].copy()

    manifest = json.loads((BASE_DIR / "manifest_sha256.json").read_text())
    key_lines = "\n".join(f"{d}\t{t}" for d, t in zip(te_df["Drug"], te_df["Target"])).encode("utf-8")
    test_keys_sha256 = hashlib.sha256(key_lines).hexdigest()
    assert test_keys_sha256 == manifest["test_drug_target_keys_sha256"], "Test key SHA-256 mismatch!"
    print(f"Verified test_drug_target_keys_sha256 = {test_keys_sha256}", flush=True)

    engine = UnifiedDTIDGFeatureEngine(CACHE_DIR)
    t_to_idx = {t: i for i, t in enumerate(engine.targets)}
    d_to_idx = {s: i for i, s in enumerate(engine.smiles)}

    tv_df["t_idx"] = tv_df["Target"].map(t_to_idx).astype(np.int32)
    tv_df["d_idx"] = tv_df["Drug"].map(d_to_idx).astype(np.int32)
    tv_df["rid"] = np.arange(len(tv_df), dtype=np.int32)

    te_p = te_df["Target"].map(t_to_idx).values.astype(np.int32)
    te_d = te_df["Drug"].map(d_to_idx).values.astype(np.int32)
    te_y = te_df["Y"].values.astype(np.float32)
    te_yr = te_df["Year"].values.astype(np.int32)
    te_rid = np.arange(10_000_000, 10_000_000 + len(te_df), dtype=np.int32)

    seen_targets_tv = set(tv_df["t_idx"].values.tolist())
    seen_drugs_tv = set(tv_df["d_idx"].values.tolist())
    te_seen_t_mask = np.array([p in seen_targets_tv for p in te_p], dtype=bool)
    te_unseen_t_mask = ~te_seen_t_mask
    te_unseen_d_mask = np.array([d not in seen_drugs_tv for d in te_d], dtype=bool)
    print(
        f"Test set: {len(te_df)} rows | Seen-Target rows: {np.sum(te_seen_t_mask)} | "
        f"Unseen-Target rows: {np.sum(te_unseen_t_mask)} ({len(set(te_p[te_unseen_t_mask]))} targets)",
        flush=True,
    )

    # 1. Reproduce ERM Baseline across Seeds 1..5 for Partial Win p2
    t_erm = time.time()
    erm_preds_list, erm_seed_pccs, erm_eval_many = train_predict_erm_baseline_5seeds(
        group, bm, engine, t_to_idx, d_to_idx
    )
    erm_vecs = [d[bm["name"]] for d in erm_preds_list]
    erm_breakdown = compute_year_and_subset_breakdown(
        te_y, te_yr, te_seen_t_mask, te_unseen_t_mask, te_unseen_d_mask, erm_vecs
    )
    print(f"Reproduced 5-seed ERM Baseline in {time.time()-t_erm:.2f}s: {erm_eval_many} (seeds={erm_seed_pccs})", flush=True)
    for yr in ["2019", "2020", "2021"]:
        yb = erm_breakdown["per_year"][yr]
        print(f"  ERM Year {yr} (n={yb['n_rows']}): PCC = {yb['mean_pcc']:.5f} +- {yb['std_pcc']:.5f}", flush=True)

    # 2. Pre-extract Track B full `train_val -> test` Level-1 features once (35s)
    t_tb = time.time()
    X_te_full_tv = engine.extract_all_features(
        tv_df["d_idx"].values, tv_df["t_idx"].values, tv_df["Year"].values.astype(np.int32),
        tv_df["Y"].values.astype(np.float32), tv_df["rid"].values,
        te_d, te_p, te_yr, te_rid,
    )
    print(f"Extracted full train_val -> test features in {time.time()-t_tb:.2f}s", flush=True)

    # 3. Run Official Seeds 1..5 for both Track A (`strict_train_s`) and Track B (`train_val_refit`)
    track_a_preds_list = []
    track_b_preds_list = []
    track_a_vecs = []
    track_b_vecs = []

    for seed in [1, 2, 3, 4, 5]:
        t_s = time.time()
        tr_df, va_df = group.get_train_valid_split(benchmark="BindingDB_Patent", split_type="default", seed=seed)
        tr_p = tr_df["Target"].map(t_to_idx).values.astype(np.int32)
        tr_d = tr_df["Drug"].map(d_to_idx).values.astype(np.int32)
        tr_yr = tr_df["Year"].values.astype(np.int32)
        tr_y = tr_df["Y"].values.astype(np.float32)
        tr_rid = np.arange(len(tr_df), dtype=np.int32)

        X_temp_s, y_temp_s, yr_temp_s = build_temporal_oof_late_years(
            engine, tr_d, tr_p, tr_yr, tr_y, tr_rid, min_eval_yr=2016
        )

        # Track A: Extract test features strictly from `train_s` (80% of train_val, zero valid_s in Level-1)
        X_te_s = engine.extract_all_features(
            tr_d, tr_p, tr_yr, tr_y, tr_rid,
            te_d, te_p, te_yr, te_rid,
        )
        pred_a_s, _, _, _, _ = fit_predict_two_regime_ensemble_v3(
            X_temp_s, y_temp_s, yr_temp_s, X_te_s, seed=seed * 100
        )

        # Track B: Same Level-2 stacker trained strictly on `X_temp_s` (from `train_s`), evaluated on `X_te_full_tv`
        pred_b_s, _, _, _, _ = fit_predict_two_regime_ensemble_v3(
            X_temp_s, y_temp_s, yr_temp_s, X_te_full_tv, seed=seed * 100
        )

        ev_a_tdc = float(group.evaluate({bm["name"]: pred_a_s})[bm["name"]]["pcc"])
        ev_b_tdc = float(group.evaluate({bm["name"]: pred_b_s})[bm["name"]]["pcc"])
        ev_a = float(pearsonr(te_y, pred_a_s)[0])
        ev_b = float(pearsonr(te_y, pred_b_s)[0])

        unseen_a = float(pearsonr(te_y[te_unseen_t_mask], pred_a_s[te_unseen_t_mask])[0])
        unseen_b = float(pearsonr(te_y[te_unseen_t_mask], pred_b_s[te_unseen_t_mask])[0])

        track_a_preds_list.append({bm["name"]: pred_a_s})
        track_b_preds_list.append({bm["name"]: pred_b_s})
        track_a_vecs.append(pred_a_s)
        track_b_vecs.append(pred_b_s)

        print(
            f"  [Seed {seed} | {time.time()-t_s:.1f}s] "
            f"Track A (strict_train_s): All PCC = {ev_a:.5f} [TDC={ev_a_tdc:.3f}] (Unseen-T = {unseen_a:.5f}) | "
            f"Track B (train_val L1): All PCC = {ev_b:.5f} [TDC={ev_b_tdc:.3f}] (Unseen-T = {unseen_b:.5f})",
            flush=True,
        )

    eval_many_a = group.evaluate_many(track_a_preds_list)
    eval_many_b = group.evaluate_many(track_b_preds_list)

    breakdown_a = compute_year_and_subset_breakdown(
        te_y, te_yr, te_seen_t_mask, te_unseen_t_mask, te_unseen_d_mask, track_a_vecs
    )
    breakdown_b = compute_year_and_subset_breakdown(
        te_y, te_yr, te_seen_t_mask, te_unseen_t_mask, te_unseen_d_mask, track_b_vecs
    )

    boot_a = run_bootstrap_10000(te_y, np.mean(track_a_vecs, axis=0))
    boot_b = run_bootstrap_10000(te_y, np.mean(track_b_vecs, axis=0))

    print(f"\n==============================================================", flush=True)
    print(f"OFFICIAL 5-SEED EVALUATION SUMMARY (total runtime {time.time()-t0_all:.1f}s)", flush=True)
    print(f"==============================================================", flush=True)
    print(f"Track A (Strict train_s only): {eval_many_a}", flush=True)
    print(f"  Bootstrap (10k): mean={boot_a['boot_mean_pcc']:.5f} +- {boot_a['boot_std_pcc']:.5f}, "
          f"win_vs_0.538={boot_a['win_rate_vs_0.538']*100:.2f}%, win_vs_0.588={boot_a['win_rate_vs_0.588']*100:.2f}%", flush=True)
    print(f"  Per-Year PCC (p2): 2019={breakdown_a['per_year']['2019']['mean_pcc']:.5f}, "
          f"2020={breakdown_a['per_year']['2020']['mean_pcc']:.5f}, 2021={breakdown_a['per_year']['2021']['mean_pcc']:.5f}", flush=True)
    print(f"  Seen-Target PCC:   {breakdown_a['seen_target']['mean_pcc']:.5f} +- {breakdown_a['seen_target']['std_pcc']:.5f}", flush=True)
    print(f"  Unseen-Target (p3): {breakdown_a['unseen_target_p3']['mean_pcc']:.5f} +- {breakdown_a['unseen_target_p3']['std_pcc']:.5f}", flush=True)

    print(f"\nTrack B (train_val L1 refit) : {eval_many_b}", flush=True)
    print(f"  Bootstrap (10k): mean={boot_b['boot_mean_pcc']:.5f} +- {boot_b['boot_std_pcc']:.5f}, "
          f"win_vs_0.538={boot_b['win_rate_vs_0.538']*100:.2f}%, win_vs_0.588={boot_b['win_rate_vs_0.588']*100:.2f}%", flush=True)
    print(f"  Per-Year PCC (p2): 2019={breakdown_b['per_year']['2019']['mean_pcc']:.5f}, "
          f"2020={breakdown_b['per_year']['2020']['mean_pcc']:.5f}, 2021={breakdown_b['per_year']['2021']['mean_pcc']:.5f}", flush=True)
    print(f"  Seen-Target PCC:   {breakdown_b['seen_target']['mean_pcc']:.5f} +- {breakdown_b['seen_target']['std_pcc']:.5f}", flush=True)
    print(f"  Unseen-Target (p3): {breakdown_b['unseen_target_p3']['mean_pcc']:.5f} +- {breakdown_b['unseen_target_p3']['std_pcc']:.5f}", flush=True)

    # Save prediction files and SHA-256 hashes
    saved_files = {}
    for s_idx, seed in enumerate([1, 2, 3, 4, 5]):
        for track_tag, vec in [("trackA_strict_train", track_a_vecs[s_idx]), ("trackB_trainval_refit", track_b_vecs[s_idx]), ("erm_baseline", erm_vecs[s_idx])]:
            npy_path = PRED_DIR / f"seed_{seed}_{track_tag}.npy"
            csv_path = PRED_DIR / f"seed_{seed}_{track_tag}.csv"
            np.save(npy_path, vec.astype(np.float32))
            pd.DataFrame({"y_pred": vec.astype(np.float32)}).to_csv(csv_path, index=False)
            saved_files[f"seed_{seed}_{track_tag}.csv"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()

    cert = {
        "benchmark_id": "tdc-dti-dg-bindingdb-patent-pcc",
        "tdc_group": "DTI_DG_Group",
        "tdc_benchmark": "BindingDB_Patent",
        "test_rows": len(te_df),
        "test_drug_target_keys_sha256": test_keys_sha256,
        "leaderboard_live_top2": {
            "rank_1_Otter_Knowledge_Ensemble": {"mean": 0.588, "std": 0.002},
            "rank_2_OrangeBalls_ProtBertMorgan": {"mean": 0.538, "std": 0.008},
            "rank_5_ERM_listed": {"mean": 0.427, "std": 0.012},
        },
        "erm_reproduced_5seed": {
            "evaluate_many": {k: [float(x) for x in v] for k, v in erm_eval_many.items()},
            "seed_pccs": erm_seed_pccs,
            "breakdown": erm_breakdown,
        },
        "track_a_strict_train_s": {
            "evaluate_many": {k: [float(x) for x in v] for k, v in eval_many_a.items()},
            "seed_pccs": [float(pearsonr(te_y, v)[0]) for v in track_a_vecs],
            "bootstrap_10000": boot_a,
            "breakdown": breakdown_a,
        },
        "track_b_train_val_refit": {
            "evaluate_many": {k: [float(x) for x in v] for k, v in eval_many_b.items()},
            "seed_pccs": [float(pearsonr(te_y, v)[0]) for v in track_b_vecs],
            "bootstrap_10000": boot_b,
            "breakdown": breakdown_b,
        },
        "prediction_files_sha256": saved_files,
        "total_runtime_seconds": float(time.time() - t0_all),
    }
    cert_path = BASE_DIR / "results_certificate.json"
    cert_path.write_text(json.dumps(cert, indent=2))
    print(f"\nSaved complete certificate to {cert_path}", flush=True)


if __name__ == "__main__":
    main()
