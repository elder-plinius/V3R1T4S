#!/usr/bin/env python3
"""
Deterministic Training, 5-Fold Cross-Validation (p2), Null-Permutation Control,
Per-Material Feature CSV Export, Standard-Operator ONNX Export, and Official Test
Prediction Script for the NIST JARVIS Small-Data Materials Benchmarks:
  1. dft_3d_exfoliation_energy (AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae)
  2. tinnet_N_ead              (AI-SinglePropertyPrediction-ead-tinnet_N-test-mae, p1)

All models are trained strictly on train U val IDs using structure-only inputs
(lattice_mat, coords, elements, cartesian) with zero target or DFT property leakage,
and exported as standard-operator ONNX graphs (opset 18, ir_version 8) evaluated
directly by onnxruntime.InferenceSession on the exported per-material feature CSVs.
"""
import csv
import hashlib
import json
import pathlib
import time
import zipfile
import numpy as np
import onnx
from onnx import helper, TensorProto, numpy_helper
from scipy.spatial.distance import cdist
from scipy.stats import wilcoxon, ttest_rel
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold
from sklearn.preprocessing import QuantileTransformer
import xgboost as xgb

from featurize_physics_clss import (
    featurize_structure,
    extract_fracture_regime_vector,
    extract_canonical_adsorbate_slab,
)

HERE = pathlib.Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
OBJ_DIR = PKG_ROOT / "object"


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


def fit_reproduced_matminer_xgboost(X_tr: np.ndarray, y_tr: np.ndarray, X_ev: np.ndarray, seed: int = 42) -> np.ndarray:
    """Reproduced matminer_xgboost baseline on canonical Magpie + CFID features (:1350)."""
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
# 1. dft_3d_exfoliation_energy: Multi-View + Griffith 3D-Covalent Fracture KRR
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
# 2. tinnet_N_ead (p1): Hammer-Norskov Adsorbate-Centered Canonical Slab KRR
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


def make_cdist_two_inputs(A_name: str, B_name: str, out_name: str, scale_val: float, prefix: str):
    inits = [
        numpy_helper.from_array(np.array([0], dtype=np.int64), name=f"{prefix}_ax0"),
        numpy_helper.from_array(np.array([1], dtype=np.int64), name=f"{prefix}_ax1"),
        numpy_helper.from_array(np.array([2], dtype=np.int64), name=f"{prefix}_ax2"),
        numpy_helper.from_array(np.array(float(scale_val), dtype=np.float64), name=f"{prefix}_scale"),
    ]
    nodes = [
        helper.make_node("Unsqueeze", [A_name, f"{prefix}_ax1"], [f"{prefix}_A3"]),
        helper.make_node("Unsqueeze", [B_name, f"{prefix}_ax0"], [f"{prefix}_B3"]),
        helper.make_node("Sub", [f"{prefix}_A3", f"{prefix}_B3"], [f"{prefix}_diff"]),
        helper.make_node("Abs", [f"{prefix}_diff"], [f"{prefix}_abs"]),
        helper.make_node("ReduceSum", [f"{prefix}_abs", f"{prefix}_ax2"], [f"{prefix}_l1"], keepdims=0),
        helper.make_node("Div", [f"{prefix}_l1", f"{prefix}_scale"], [out_name]),
    ]
    return inits, nodes
