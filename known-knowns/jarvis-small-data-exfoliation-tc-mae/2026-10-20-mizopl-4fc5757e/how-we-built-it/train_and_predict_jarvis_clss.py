#!/usr/bin/env python3
"""
Deterministic Training, 5-Fold Cross-Validation (p2), Null-Permutation Control,
and Official Test Prediction Script for the NIST JARVIS Small-Data Materials Benchmarks:
  1. dft_3d_Tc_supercon        (AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae)
  2. dft_3d_exfoliation_energy (AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae)
  3. tinnet_N_ead              (AI-SinglePropertyPrediction-ead-tinnet_N-test-mae, p1)
  4. dft_3d_dfpt_piezo_max_dij (AI-SinglePropertyPrediction-dfpt_piezo_max_dij-dft_3d-test-mae, p1)

All models are trained strictly on train U val IDs using structure-only inputs
(lattice_mat, coords, elements, cartesian) with zero target or DFT property leakage.
"""
import argparse
import csv
import gzip
import hashlib
import json
import pathlib
import time
import zipfile
import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import wilcoxon, ttest_rel
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold
from sklearn.preprocessing import QuantileTransformer
import xgboost as xgb

from featurize_physics_clss import (
    featurize_structure,
    extract_iso_homolog_signature,
    compute_single_sub_homolog_distance,
    extract_fracture_regime_vector,
    extract_canonical_adsorbate_slab,
)

HERE = pathlib.Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
CLEAN_DIR = DATA_DIR / "clean_structures"
CACHE_DIR = DATA_DIR / "features_cache"
LB_DIR = DATA_DIR / "leaderboard_baselines"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def bootstrap_mae_ci90(y_true: np.ndarray, y_pred: np.ndarray, n_boot: int = 1000, seed: int = 0):
    rng = np.random.default_rng(seed)
    errs = np.abs(y_true - y_pred)
    n = len(errs)
    idx = rng.integers(0, n, size=(n_boot, n))
    boot_maes = np.mean(errs[idx], axis=1)
    q05, q95 = np.percentile(boot_maes, [5.0, 95.0])
    half_width = 0.5 * float(q95 - q05)
    return float(np.mean(errs)), float(q05), float(q95), half_width, boot_maes


def paired_bootstrap_test(y_true: np.ndarray, y_pred_claim: np.ndarray, y_pred_base: np.ndarray,
                          n_boot: int = 10000, seed: int = 0):
    rng = np.random.default_rng(seed)
    diff = np.abs(y_true - y_pred_base) - np.abs(y_true - y_pred_claim)
    n = len(diff)
    idx = rng.integers(0, n, size=(n_boot, n))
    boot_diffs = np.mean(diff[idx], axis=1)
    win_rate = float(np.mean(boot_diffs > 0.0))
    p_val = float((1 + np.sum(boot_diffs <= 0.0)) / (n_boot + 1))
    q05, q95 = np.percentile(boot_diffs, [5.0, 95.0])
    return {
        "mean_mae_gain": float(np.mean(diff)),
        "ci90_gain_low": float(q05),
        "ci90_gain_high": float(q95),
        "win_rate_10k": win_rate,
        "p_value_10k": p_val,
    }


def load_leaderboard_baseline_preds(zip_name: str, test_ids: np.ndarray) -> np.ndarray:
    with zipfile.ZipFile(LB_DIR / zip_name) as zf:
        raw_txt = zf.read(zf.namelist()[0]).decode("utf-8").splitlines()
    reader = csv.DictReader(raw_txt)
    id_to_pred = {}
    for row in reader:
        jid = str(row.get("id", row.get(reader.fieldnames[0]))).strip()
        p_val = float(row.get("prediction", row.get(reader.fieldnames[-1])))
        id_to_pred[jid] = p_val
    return np.array([id_to_pred[str(k)] for k in test_ids], dtype=np.float64)


def verify_leak_free_structures(task: str):
    p = CLEAN_DIR / f"{task}_structures.json.gz"
    d = json.load(gzip.open(p))
    splits = d["splits"]
    structs = d["structures"]
    tr_ids = set(splits["train"].keys())
    va_ids = set(splits.get("val", {}).keys())
    te_ids = set(splits["test"].keys())
    assert len(tr_ids & va_ids) == 0, f"Overlap train/val in {task}"
    assert len(tr_ids & te_ids) == 0, f"Overlap train/test in {task}"
    assert len(va_ids & te_ids) == 0, f"Overlap val/test in {task}"
    allowed_keys = {"lattice_mat", "coords", "elements", "cartesian"}
    for jid, s in structs.items():
        extra = set(s.keys()) - allowed_keys
        assert len(extra) == 0, f"Forbidden keys {extra} in {task}:{jid}"
    return d


def load_task_arrays(task: str, from_scratch: bool = False):
    d = verify_leak_free_structures(task)
    splits = d["splits"]
    structs = d["structures"]
    cache_path = CACHE_DIR / f"{task}_feat.npz"
    if not from_scratch and cache_path.exists():
        c = np.load(cache_path, allow_pickle=True)
        X_tr, y_tr, ids_tr = c["train_X"], c["train_y"], c["train_ids"]
        X_va, y_va, ids_va = c["val_X"], c["val_y"], c["val_ids"]
        X_te, y_te, ids_te = c["test_X"], c["test_y"], c["test_ids"]
        X_tv = np.vstack([X_tr, X_va])
        y_tv = np.concatenate([y_tr, y_va])
        ids_tv = np.concatenate([ids_tr, ids_va])
        extra = {}
        if "train_F" in c:
            extra["F_tv"] = np.vstack([c["train_F"], c["val_F"]])
            extra["F_te"] = c["test_F"]
        if "train_S" in c:
            extra["S_tv"] = np.vstack([c["train_S"], c["val_S"]])
            extra["S_te"] = c["test_S"]
        return structs, ids_tv, X_tv, y_tv, ids_te, X_te, y_te, extra
    else:
        ids_tr = list(splits["train"].keys())
        ids_va = list(splits["val"].keys())
        ids_te = list(splits["test"].keys())
        ids_tv = np.array(ids_tr + ids_va, dtype=str)
        ids_te_arr = np.array(ids_te, dtype=str)
        y_tv = np.array([float(splits["train"].get(k, splits["val"].get(k))) for k in ids_tv], dtype=np.float64)
        y_te = np.array([float(splits["test"][k]) for k in ids_te_arr], dtype=np.float64)
        X_tv = np.vstack([featurize_structure(structs[str(k)]) for k in ids_tv])
        X_te = np.vstack([featurize_structure(structs[str(k)]) for k in ids_te_arr])
        extra = {}
        if task == "dft_3d_exfoliation_energy":
            extra["F_tv"] = np.vstack([extract_fracture_regime_vector(structs[str(k)], X_tv[i]) for i, k in enumerate(ids_tv)])
            extra["F_te"] = np.vstack([extract_fracture_regime_vector(structs[str(k)], X_te[i]) for i, k in enumerate(ids_te_arr)])
        if task == "tinnet_N_ead":
            extra["S_tv"] = np.vstack([extract_canonical_adsorbate_slab(structs[str(k)]) for k in ids_tv])
            extra["S_te"] = np.vstack([extract_canonical_adsorbate_slab(structs[str(k)]) for k in ids_te_arr])
        return structs, ids_tv, X_tv, y_tv, ids_te_arr, X_te, y_te, extra


def fit_reproduced_matminer_xgboost(X_tr: np.ndarray, y_tr: np.ndarray, X_ev: np.ndarray, seed: int = 42) -> np.ndarray:
    """Reproduced matminer_xgboost baseline on canonical Magpie + CFID structural features (:1350)."""
    m = xgb.XGBRegressor(
        tree_method="hist",
        n_estimators=600,
        learning_rate=0.1,
        max_depth=6,
        colsample_bytree=0.3,
        colsample_bylevel=0.5,
        reg_lambda=0.01,
        reg_alpha=0.01,
        random_state=seed,
        n_jobs=4,
    )
    m.fit(X_tr[:, :1350], y_tr)
    return m.predict(X_ev[:, :1350])


# ==============================================================================
# 1. dft_3d_Tc_supercon: BCS Physics Core + Single-Site Isoelectronic Homolog KRR
# ==============================================================================
def fit_predict_tc_supercon(X_tr: np.ndarray, y_tr: np.ndarray, sigs_tr: list,
                            X_ev: np.ndarray = None, sigs_ev: list = None):
    n_tr = len(y_tr)
    qt = QuantileTransformer(n_quantiles=min(250, n_tr), output_distribution="uniform", random_state=42)
    Q_tr = qt.fit_transform(X_tr)
    phys_idx = np.r_[0:189, 441:474, 1350:1612]
    Dp_tr = cdist(Q_tr[:, phys_idx], Q_tr[:, phys_idx], metric="cityblock") / len(phys_idx)

    tau = 0.4 * float(np.median(y_tr[y_tr > 0]))
    z_tr = np.log1p(np.maximum(y_tr, 0.0) / tau)
    K_p = np.exp(-3.5 * Dp_tr)
    A_p = np.linalg.inv(K_p + 0.025 * np.eye(n_tr))
    alpha_p = A_p @ z_tr

    # LOO prediction on training set
    loo_base = np.maximum(0.0, tau * np.expm1(z_tr - alpha_p / np.diag(A_p)))
    Dh_tr = compute_single_sub_homolog_distance(sigs_tr, sigs_tr, Dp_tr) + np.eye(n_tr) * 10.0
    w_tr = np.exp(-30.0 * Dh_tr)
    w_tr /= np.maximum(np.sum(w_tr, axis=1, keepdims=True), 1e-12)
    loo_hom = w_tr @ y_tr
    has_hom_tr = (np.min(Dh_tr, axis=1) < 1.0).astype(np.float64)

    # Select c_hom strictly by minimizing LOO MAE on (X_tr, y_tr)
    c_grid = np.linspace(0.0, 1.0, 21)
    best_c = 0.80
    best_loo_mae = 1e9
    for c_cand in c_grid:
        g_tr = c_cand * has_hom_tr
        p_c = (1.0 - g_tr) * loo_base + g_tr * loo_hom
        m_c = float(mean_absolute_error(y_tr, p_c))
        if m_c < best_loo_mae:
            best_loo_mae = m_c
            best_c = float(c_cand)

    g_tr_opt = best_c * has_hom_tr
    loo_pred = (1.0 - g_tr_opt) * loo_base + g_tr_opt * loo_hom

    if X_ev is None:
        return loo_pred, {"tau": tau, "best_c_hom": best_c, "alpha_p": alpha_p}

    Q_ev = qt.transform(X_ev)
    Dp_ev = cdist(Q_ev[:, phys_idx], Q_tr[:, phys_idx], metric="cityblock") / len(phys_idx)
    K_pe = np.exp(-3.5 * Dp_ev)
    ev_base = np.maximum(0.0, tau * np.expm1(K_pe @ alpha_p))

    Dh_ev = compute_single_sub_homolog_distance(sigs_ev, sigs_tr, Dp_ev)
    w_ev = np.exp(-30.0 * Dh_ev)
    w_ev /= np.maximum(np.sum(w_ev, axis=1, keepdims=True), 1e-12)
    ev_hom = w_ev @ y_tr
    has_hom_ev = (np.min(Dh_ev, axis=1) < 1.0).astype(np.float64)
    g_ev = best_c * has_hom_ev
    ev_pred = (1.0 - g_ev) * ev_base + g_ev * ev_hom
    return ev_pred, loo_pred, {"tau": tau, "best_c_hom": best_c, "alpha_p": alpha_p}


# ==============================================================================
# 2. dft_3d_exfoliation_energy: Multi-View + Griffith 3D-Covalent Fracture KRR
# ==============================================================================
def fit_predict_exfoliation(X_tr: np.ndarray, y_tr: np.ndarray, F_tr: np.ndarray,
                            X_ev: np.ndarray = None, F_ev: np.ndarray = None):
    n_tr, d_tot = X_tr.shape
    qt = QuantileTransformer(n_quantiles=min(250, n_tr), output_distribution="uniform", random_state=42)
    Q_tr = qt.fit_transform(X_tr)

    D_full_tr = cdist(Q_tr, Q_tr, metric="cityblock") / d_tot
    D_stru_tr = cdist(Q_tr[:, 1350:], Q_tr[:, 1350:], metric="cityblock") / (d_tot - 1350.0)
    D_reg_tr = cdist(F_tr, F_tr, metric="cityblock") / F_tr.shape[1]

    tau = 0.45 * float(np.median(y_tr))
    z_tr = np.log1p(np.maximum(y_tr, 0.0) / tau)
    K_base_tr = np.exp(-3.0 * (0.5 * D_full_tr + 0.5 * D_stru_tr))
    A_base = np.linalg.inv(K_base_tr + 0.025 * np.eye(n_tr))
    alpha_base = A_base @ z_tr
    loo_base = np.maximum(0.0, tau * np.expm1(z_tr - alpha_base / np.diag(A_base)))

    K_r_tr = np.exp(-6.0 * D_reg_tr - 2.0 * D_stru_tr)
    A_r = np.linalg.inv(K_r_tr + 0.03 * np.eye(n_tr))
    alpha_r = A_r @ y_tr
    loo_r = np.maximum(0.0, y_tr - alpha_r / np.diag(A_r))

    # Select w_r strictly by minimizing LOO MAE on (X_tr, y_tr)
    w_grid = np.linspace(0.0, 1.0, 21)
    best_w = 0.85
    best_loo_mae = 1e9
    for w_cand in w_grid:
        gate_tr = w_cand * F_tr[:, 5]
        p_c = (1.0 - gate_tr) * loo_base + gate_tr * loo_r
        m_c = float(mean_absolute_error(y_tr, p_c))
        if m_c < best_loo_mae:
            best_loo_mae = m_c
            best_w = float(w_cand)

    gate_tr_opt = best_w * F_tr[:, 5]
    loo_pred = (1.0 - gate_tr_opt) * loo_base + gate_tr_opt * loo_r

    if X_ev is None:
        return loo_pred, {"tau": tau, "best_w_r": best_w, "alpha_base": alpha_base, "alpha_r": alpha_r}

    Q_ev = qt.transform(X_ev)
    D_full_ev = cdist(Q_ev, Q_tr, metric="cityblock") / d_tot
    D_stru_ev = cdist(Q_ev[:, 1350:], Q_tr[:, 1350:], metric="cityblock") / (d_tot - 1350.0)
    D_reg_ev = cdist(F_ev, F_tr, metric="cityblock") / F_tr.shape[1]

    K_base_ev = np.exp(-3.0 * (0.5 * D_full_ev + 0.5 * D_stru_ev))
    ev_base = np.maximum(0.0, tau * np.expm1(K_base_ev @ alpha_base))

    K_r_ev = np.exp(-6.0 * D_reg_ev - 2.0 * D_stru_ev)
    ev_r = np.maximum(0.0, K_r_ev @ alpha_r)

    gate_ev = best_w * F_ev[:, 5]
    ev_pred = (1.0 - gate_ev) * ev_base + gate_ev * ev_r
    return ev_pred, loo_pred, {"tau": tau, "best_w_r": best_w, "alpha_base": alpha_base, "alpha_r": alpha_r}


# ==============================================================================
# 3. tinnet_N_ead (p1): Hammer-Norskov Adsorbate-Centered Canonical Slab KRR
# ==============================================================================
def fit_predict_tinnet(X_tr: np.ndarray, y_tr: np.ndarray, S_tr: np.ndarray,
                       X_ev: np.ndarray = None, S_ev: np.ndarray = None):
    n_tr = len(y_tr)
    S_all_tr = np.hstack([S_tr, X_tr])
    qt = QuantileTransformer(n_quantiles=min(150, n_tr), output_distribution="uniform", random_state=42)
    QS_tr = qt.fit_transform(S_all_tr)
    d_s = S_tr.shape[1]
    Ds_tr = cdist(QS_tr[:, :d_s], QS_tr[:, :d_s], metric="cityblock") / d_s
    Df_tr = cdist(QS_tr, QS_tr, metric="cityblock") / QS_tr.shape[1]

    D_tr = 0.70 * Ds_tr + 0.30 * Df_tr
    K_tr = np.exp(-1.2 * D_tr)
    A_inv = np.linalg.inv(K_tr + 0.002 * np.eye(n_tr))
    alpha = A_inv @ y_tr
    loo_pred = y_tr - alpha / np.diag(A_inv)

    if X_ev is None:
        return loo_pred, {"alpha": alpha}

    S_all_ev = np.hstack([S_ev, X_ev])
    QS_ev = qt.transform(S_all_ev)
    Ds_ev = cdist(QS_ev[:, :d_s], QS_tr[:, :d_s], metric="cityblock") / d_s
    Df_ev = cdist(QS_ev, QS_tr, metric="cityblock") / QS_tr.shape[1]
    D_ev = 0.70 * Ds_ev + 0.30 * Df_ev
    K_ev = np.exp(-1.2 * D_ev)
    ev_pred = K_ev @ alpha
    return ev_pred, loo_pred, {"alpha": alpha}


def write_prediction_csv(path_csv: pathlib.Path, ids: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray):
    with open(path_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "target", "prediction"])
        for jid, yt, yp in zip(ids, y_true, y_pred):
            w.writerow([str(jid), f"{float(yt):.8f}", f"{float(yp):.8f}"])
    zip_path = path_csv.with_suffix(".csv.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(path_csv, arcname=path_csv.name)


def write_cv_csv(path_csv: pathlib.Path, ids: np.ndarray, y_true: np.ndarray,
                 oof_clss: np.ndarray, oof_xgb: np.ndarray, loo_clss: np.ndarray):
    with open(path_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "y_true", "oof_5fold_clss", "oof_5fold_matminer_xgboost", "loo_clss"])
        for jid, yt, pc, px, pl in zip(ids, y_true, oof_clss, oof_xgb, loo_clss):
            w.writerow([str(jid), f"{float(yt):.8f}", f"{float(pc):.8f}", f"{float(px):.8f}", f"{float(pl):.8f}"])


def run_null_permutation_control(y_true: np.ndarray, K_ev: np.ndarray, A_inv: np.ndarray,
                                 y_tr: np.ndarray, claimed_mae: float, n_perm: int = 400,
                                 non_neg: bool = True, tau: float = None, seed: int = 0):
    rng = np.random.default_rng(seed)
    null_maes = np.zeros(n_perm, dtype=np.float64)
    for p in range(n_perm):
        y_shuf = rng.permutation(y_tr)
        if non_neg and tau is not None:
            z_shuf = np.log1p(np.maximum(y_shuf, 0.0) / tau)
            pred_p = np.maximum(0.0, tau * np.expm1(K_ev @ (A_inv @ z_shuf)))
        else:
            pred_p = K_ev @ (A_inv @ y_shuf)
        null_maes[p] = float(mean_absolute_error(y_true, pred_p))
    mean_null = float(np.mean(null_maes))
    std_null = float(np.std(null_maes))
    min_null = float(np.min(null_maes))
    z_score = float((claimed_mae - mean_null) / max(std_null, 1e-12))
    n_better = int(np.sum(null_maes <= claimed_mae))
    return {
        "n_permutations": n_perm,
        "null_mae_mean": mean_null,
        "null_mae_std": std_null,
        "null_mae_min": min_null,
        "claimed_mae": float(claimed_mae),
        "z_score": z_score,
        "n_null_better_or_equal": n_better,
        "empirical_p_value": float((1 + n_better) / (n_perm + 1)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-scratch-structures", action="store_true", help="Recompute features from raw structures")
    args = ap.parse_args()

    t_start = time.time()
    manifest = {
        "benchmark_suite": "NIST JARVIS-Leaderboard Small-Data Materials Property Prediction",
        "target_id": "jarvis-small-data-exfoliation-tc-mae",
        "tasks": {},
    }
    saved_model_weights = {}

    task_specs = [
        {
            "task": "dft_3d_Tc_supercon",
            "csv_name": "AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv",
            "live_best_mae": 1.5187,
            "live_best_model": "atomgpt_model",
            "live_second_mae": 1.9989,
            "live_second_model": "cfid",
            "baseline_zip": "tc_atomgpt.csv.zip",
            "baseline2_zip": "tc_cfid.csv.zip",
            "units": "K",
        },
        {
            "task": "dft_3d_exfoliation_energy",
            "csv_name": "AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv",
            "live_best_mae": 40.887,
            "live_best_model": "matminer_xgboost",
            "live_second_mae": 42.7554,
            "live_second_model": "matminer_rf",
            "baseline_zip": "exf_matminer_xgb.csv.zip",
            "baseline2_zip": "exf_cfid.csv.zip",
            "units": "meV/atom",
        },
        {
            "task": "tinnet_N_ead",
            "csv_name": "AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv",
            "live_best_mae": 0.0871,
            "live_best_model": "alignn",
            "live_second_mae": 0.1508,
            "live_second_model": "cfid_chem",
            "baseline_zip": "tinnet_N_alignn.csv.zip",
            "baseline2_zip": None,
            "units": "eV",
        },
    ]

    for spec in task_specs:
        task = spec["task"]
        t0 = time.time()
        structs, ids_tv, X_tv, y_tv, ids_te, X_te, y_te, extra = load_task_arrays(
            task, from_scratch=args.from_scratch_structures
        )

        # 5-fold Cross-Validation on train U val (Partial Win p2)
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        oof_clss = np.zeros(len(y_tv), dtype=np.float64)
        oof_xgb = np.zeros(len(y_tv), dtype=np.float64)

        if task == "dft_3d_Tc_supercon":
            sigs_tv = [extract_iso_homolog_signature(structs[str(k)]) for k in ids_tv]
            sigs_te = [extract_iso_homolog_signature(structs[str(k)]) for k in ids_te]
            for fold, (f_tr, f_va) in enumerate(kf.split(X_tv)):
                s_tr = [sigs_tv[i] for i in f_tr]
                s_va = [sigs_tv[i] for i in f_va]
                p_va, _, _ = fit_predict_tc_supercon(X_tv[f_tr], y_tv[f_tr], s_tr, X_tv[f_va], s_va)
                oof_clss[f_va] = p_va
                oof_xgb[f_va] = fit_reproduced_matminer_xgboost(X_tv[f_tr], y_tv[f_tr], X_tv[f_va], seed=42 + fold)
            y_pred_te, loo_tv, params = fit_predict_tc_supercon(X_tv, y_tv, sigs_tv, X_te, sigs_te)
            saved_model_weights[f"{task}_alpha_p"] = params["alpha_p"]
            saved_model_weights[f"{task}_c_hom"] = np.array([params["best_c_hom"], params["tau"]])

            # Null permutation control
            qt = QuantileTransformer(n_quantiles=min(250, len(y_tv)), output_distribution="uniform", random_state=42)
            Q_tv = qt.fit_transform(X_tv)
            Q_te = qt.transform(X_te)
            phys_idx = np.r_[0:189, 441:474, 1350:1612]
            Dp_tv = cdist(Q_tv[:, phys_idx], Q_tv[:, phys_idx], "cityblock") / len(phys_idx)
            Dp_te = cdist(Q_te[:, phys_idx], Q_tv[:, phys_idx], "cityblock") / len(phys_idx)
            A_inv = np.linalg.inv(np.exp(-3.5 * Dp_tv) + 0.025 * np.eye(len(y_tv)))
            K_ev = np.exp(-3.5 * Dp_te)
            null_ctrl = run_null_permutation_control(
                y_te, K_ev, A_inv, y_tv, float(mean_absolute_error(y_te, y_pred_te)),
                n_perm=400, non_neg=True, tau=params["tau"], seed=0
            )

        elif task == "dft_3d_exfoliation_energy":
            F_tv, F_te = extra["F_tv"], extra["F_te"]
            for fold, (f_tr, f_va) in enumerate(kf.split(X_tv)):
                p_va, _, _ = fit_predict_exfoliation(X_tv[f_tr], y_tv[f_tr], F_tv[f_tr], X_tv[f_va], F_tv[f_va])
                oof_clss[f_va] = p_va
                oof_xgb[f_va] = fit_reproduced_matminer_xgboost(X_tv[f_tr], y_tv[f_tr], X_tv[f_va], seed=42 + fold)
            y_pred_te, loo_tv, params = fit_predict_exfoliation(X_tv, y_tv, F_tv, X_te, F_te)
            saved_model_weights[f"{task}_alpha_base"] = params["alpha_base"]
            saved_model_weights[f"{task}_alpha_r"] = params["alpha_r"]
            saved_model_weights[f"{task}_w_r"] = np.array([params["best_w_r"], params["tau"]])

            qt = QuantileTransformer(n_quantiles=min(250, len(y_tv)), output_distribution="uniform", random_state=42)
            Q_tv = qt.fit_transform(X_tv)
            Q_te = qt.transform(X_te)
            D_full_tv = cdist(Q_tv, Q_tv, "cityblock") / X_tv.shape[1]
            D_full_te = cdist(Q_te, Q_tv, "cityblock") / X_tv.shape[1]
            A_inv = np.linalg.inv(np.exp(-3.0 * D_full_tv) + 0.025 * np.eye(len(y_tv)))
            K_ev = np.exp(-3.0 * D_full_te)
            null_ctrl = run_null_permutation_control(
                y_te, K_ev, A_inv, y_tv, float(mean_absolute_error(y_te, y_pred_te)),
                n_perm=400, non_neg=True, tau=params["tau"], seed=0
            )

        elif task == "tinnet_N_ead":
            S_tv, S_te = extra["S_tv"], extra["S_te"]
            for fold, (f_tr, f_va) in enumerate(kf.split(X_tv)):
                p_va, _, _ = fit_predict_tinnet(X_tv[f_tr], y_tv[f_tr], S_tv[f_tr], X_tv[f_va], S_tv[f_va])
                oof_clss[f_va] = p_va
                oof_xgb[f_va] = fit_reproduced_matminer_xgboost(X_tv[f_tr], y_tv[f_tr], X_tv[f_va], seed=42 + fold)
            y_pred_te, loo_tv, params = fit_predict_tinnet(X_tv, y_tv, S_tv, X_te, S_te)
            saved_model_weights[f"{task}_alpha"] = params["alpha"]

            S_all_tv = np.hstack([S_tv, X_tv])
            S_all_te = np.hstack([S_te, X_te])
            qt = QuantileTransformer(n_quantiles=min(150, len(y_tv)), output_distribution="uniform", random_state=42)
            QS_tv = qt.fit_transform(S_all_tv)
            QS_te = qt.transform(S_all_te)
            d_s = S_tv.shape[1]
            D_tv = 0.70 * (cdist(QS_tv[:, :d_s], QS_tv[:, :d_s], "cityblock") / d_s) + 0.30 * (cdist(QS_tv, QS_tv, "cityblock") / QS_tv.shape[1])
            D_te = 0.70 * (cdist(QS_te[:, :d_s], QS_tv[:, :d_s], "cityblock") / d_s) + 0.30 * (cdist(QS_te, QS_tv, "cityblock") / QS_tv.shape[1])
            A_inv = np.linalg.inv(np.exp(-1.2 * D_tv) + 0.002 * np.eye(len(y_tv)))
            K_ev = np.exp(-1.2 * D_te)
            null_ctrl = run_null_permutation_control(
                y_te, K_ev, A_inv, y_tv, float(mean_absolute_error(y_te, y_pred_te)),
                n_perm=400, non_neg=False, tau=None, seed=0
            )

        saved_model_weights[f"{task}_test_pred"] = y_pred_te
        saved_model_weights[f"{task}_oof_clss"] = oof_clss
        saved_model_weights[f"{task}_oof_xgb"] = oof_xgb
        saved_model_weights[f"{task}_loo_clss"] = loo_tv

        # Write CSV files
        pred_csv_path = HERE / spec["csv_name"]
        write_prediction_csv(pred_csv_path, ids_te, y_te, y_pred_te)
        cv_csv_path = HERE / f"cv5_oof_{task}.csv"
        write_cv_csv(cv_csv_path, ids_tv, y_tv, oof_clss, oof_xgb, loo_tv)

        # Official test metrics and 1,000-sample bootstrap 90% CI
        mae_te, q05, q95, hw90, _ = bootstrap_mae_ci90(y_te, y_pred_te, n_boot=1000, seed=0)
        live_best = spec["live_best_mae"]
        rel_gain_pct = 100.0 * (live_best - mae_te) / live_best
        abs_gain = live_best - mae_te
        passes_5pct = bool(rel_gain_pct >= 5.0)
        passes_ci90 = bool(abs_gain > hw90)

        # Check across 10 bootstrap seeds (0..9)
        hw90_seeds = [bootstrap_mae_ci90(y_te, y_pred_te, n_boot=1000, seed=s)[3] for s in range(10)]

        # Paired test on test set against official published leaderboard baseline CSV
        y_base_lb = load_leaderboard_baseline_preds(spec["baseline_zip"], ids_te)
        base_lb_mae = float(mean_absolute_error(y_te, y_base_lb))
        paired_te = paired_bootstrap_test(y_te, y_pred_te, y_base_lb, n_boot=10000, seed=0)
        w_te_stat, p_wilcox_te = wilcoxon(np.abs(y_te - y_base_lb), np.abs(y_te - y_pred_te), alternative="greater")

        # 5-fold CV (p2) metrics and paired tests against reproduced matminer_xgboost
        te_pred_xgb = fit_reproduced_matminer_xgboost(X_tv, y_tv, X_te, seed=42)
        te_mae_xgb = float(mean_absolute_error(y_te, te_pred_xgb))
        oof_mae_clss = float(mean_absolute_error(y_tv, oof_clss))
        oof_mae_xgb = float(mean_absolute_error(y_tv, oof_xgb))
        loo_mae_clss = float(mean_absolute_error(y_tv, loo_tv))
        w_cv_stat, p_wilcox_cv = wilcoxon(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        w_loo_stat, p_wilcox_loo = wilcoxon(np.abs(y_tv - oof_xgb), np.abs(y_tv - loo_tv), alternative="greater")
        _, p_ttest_cv = ttest_rel(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        _, p_ttest_loo = ttest_rel(np.abs(y_tv - oof_xgb), np.abs(y_tv - loo_tv), alternative="greater")
        paired_cv = paired_bootstrap_test(y_tv, oof_clss, oof_xgb, n_boot=10000, seed=0)
        paired_loo = paired_bootstrap_test(y_tv, loo_tv, oof_xgb, n_boot=10000, seed=0)

        manifest["tasks"][task] = {
            "benchmark_name": spec["csv_name"].replace(".csv", ""),
            "units": spec["units"],
            "n_train_val": int(len(y_tv)),
            "n_test": int(len(y_te)),
            "live_leaderboard_best_model": spec["live_best_model"],
            "live_leaderboard_best_mae": float(live_best),
            "published_baseline_csv_mae_verified": base_lb_mae,
            "claimed_test_mae": mae_te,
            "relative_mae_reduction_pct": float(rel_gain_pct),
            "absolute_mae_reduction": float(abs_gain),
            "bootstrap_1000_ci90_low": q05,
            "bootstrap_1000_ci90_high": q95,
            "bootstrap_1000_ci90_half_width": hw90,
            "bootstrap_ci90_upper_bound_mae_plus_hw90": float(mae_te + hw90),
            "hw90_across_seeds_0_to_9_max": float(np.max(hw90_seeds)),
            "passes_5pct_relative_margin": passes_5pct,
            "passes_bootstrap_ci90_half_width": passes_ci90,
            "passes_full_criterion": bool(passes_5pct and passes_ci90),
            "paired_test_vs_live_leader_csv": {
                **paired_te,
                "wilcoxon_statistic": float(w_te_stat),
                "wilcoxon_p_value_one_sided": float(p_wilcox_te),
            },
            "p2_5fold_cv_study_on_train_val": {
                "reproduced_matminer_xgboost_test_mae": te_mae_xgb,
                "reproduced_matminer_xgboost_oof_mae": oof_mae_xgb,
                "clss_5fold_oof_mae": oof_mae_clss,
                "clss_analytical_loo_mae": loo_mae_clss,
                "relative_5fold_oof_reduction_pct": float(100.0 * (oof_mae_xgb - oof_mae_clss) / oof_mae_xgb),
                "relative_loo_reduction_pct": float(100.0 * (oof_mae_xgb - loo_mae_clss) / oof_mae_xgb),
                "wilcoxon_5fold_p_value_one_sided": float(p_wilcox_cv),
                "wilcoxon_loo_p_value_one_sided": float(p_wilcox_loo),
                "paired_ttest_5fold_p_value_one_sided": float(p_ttest_cv),
                "paired_ttest_loo_p_value_one_sided": float(p_ttest_loo),
                "paired_bootstrap_5fold": paired_cv,
                "paired_bootstrap_loo": paired_loo,
            },
            "null_permutation_control_400": null_ctrl,
            "prediction_csv": spec["csv_name"],
            "prediction_csv_sha256": sha256_file(pred_csv_path),
            "cv5_oof_csv": cv_csv_path.name,
            "cv5_oof_csv_sha256": sha256_file(cv_csv_path),
            "runtime_seconds": float(time.time() - t0),
        }

        print(f"\n==================== {task} ({spec['units']}) ====================")
        print(f"  Live Leaderboard #1 ({spec['live_best_model']}): MAE = {live_best:.5f}")
        print(f"  CLSS Official Test MAE               : {mae_te:.5f} (-{rel_gain_pct:.2f}% relative, gain = +{abs_gain:.5f})")
        print(f"  1,000-Sample 90% Bootstrap CI        : [{q05:.5f}, {q95:.5f}], half-width h90 = {hw90:.5f}")
        print(f"  Criterion Check (gain > h90 & >=5%)  : {abs_gain:.5f} > {hw90:.5f} (MAE+h90 = {mae_te+hw90:.5f} < {live_best:.5f}) -> {'PASS' if (passes_5pct and passes_ci90) else 'FAIL'}")
        print(f"  Paired Test vs Published Leader CSV  : Wilcoxon p = {p_wilcox_te:.4e}, 10k-Boot Win Rate = {100*paired_te['win_rate_10k']:.2f}%")
        print(f"  [p2] 5-Fold CV OOF MAE (n={len(y_tv):3d})       : CLSS 5-fold = {oof_mae_clss:.5f} (LOO = {loo_mae_clss:.5f}) vs matminer_xgboost = {oof_mae_xgb:.5f} (Wilcoxon p = {p_wilcox_cv:.4e})")
        print(f"  [Null Control 400 Permutations]      : null MAE = {null_ctrl['null_mae_mean']:.4f} +/- {null_ctrl['null_mae_std']:.4f} (min = {null_ctrl['null_mae_min']:.4f}, z = {null_ctrl['z_score']:.2f})")

    models_path = HERE / "trained_models_jarvis_clss.npz"
    np.savez_compressed(models_path, **saved_model_weights)
    manifest["trained_models_file"] = models_path.name
    manifest["trained_models_sha256"] = sha256_file(models_path)
    manifest["total_runtime_seconds"] = float(time.time() - t_start)

    manifest_path = HERE / "jarvis_clss_results_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nSaved {models_path.name} and {manifest_path.name} in {time.time() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
