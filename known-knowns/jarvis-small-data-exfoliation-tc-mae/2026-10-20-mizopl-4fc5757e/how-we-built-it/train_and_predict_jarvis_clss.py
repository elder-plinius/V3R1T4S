#!/usr/bin/env python3
"""
Deterministic Training, 5-Fold Cross-Validation (p2), Null-Permutation Control,
Per-Material Feature CSV Export, Standard-Operator ONNX Export, and Official Test
Prediction Script for the NIST JARVIS Small-Data Materials Benchmarks:
  1. dft_3d_exfoliation_energy (AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae, claimed primary + p2)
  2. tinnet_N_ead              (AI-SinglePropertyPrediction-ead-tinnet_N-test-mae, uncredited supplementary; p1 dropped)

All models are fitted on official train U val IDs from crystal structure inputs
(lattice_mat, coords, elements, cartesian) with disjoint train/val/test ID splits,
and exported as standard-operator ONNX graphs (opset 18, ir_version 8) with named
inputs ("X_eval", "X_support") and output ("prediction") evaluated directly by
onnxruntime.InferenceSession on the exported per-material feature CSV shards.
"""
import argparse
import csv
import gzip
import hashlib
import io
import json
import pathlib
import time
import urllib.request
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
        return loo_pred, {
            "tau": tau,
            "best_w_r": best_w,
            "alpha_base": alpha_base,
            "alpha_r": alpha_r,
            "Q_tr": Q_tr,
            "loo_base": loo_base,
        }

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
    return ev_pred, loo_pred, {
        "tau": tau,
        "best_w_r": best_w,
        "alpha_base": alpha_base,
        "alpha_r": alpha_r,
        "Q_tr": Q_tr,
        "Q_ev": Q_ev,
        "ev_base": ev_base,
        "loo_base": loo_base,
    }


# ==============================================================================
# 2. tinnet_N_ead (supplementary): Hammer-Norskov Canonical Slab KRR
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
        return loo_pred, {"alpha": alpha, "QS_tr": QS_tr, "d_s": d_s}

    S_all_ev = np.hstack([S_ev, X_ev])
    QS_ev = qt.transform(S_all_ev)
    Ds_ev = cdist(QS_ev[:, :d_s], QS_tr[:, :d_s], metric="cityblock") / d_s
    Df_ev = cdist(QS_ev, QS_tr, metric="cityblock") / QS_tr.shape[1]
    D_ev = 0.70 * Ds_ev + 0.30 * Df_ev
    K_ev = np.exp(-1.2 * D_ev)
    ev_pred = K_ev @ alpha
    return ev_pred, loo_pred, {"alpha": alpha, "QS_tr": QS_tr, "QS_ev": QS_ev, "d_s": d_s}


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


def export_exfoliation_onnx(onnx_path: pathlib.Path, d_tot: int, tau: float, best_w: float,
                            alpha_base: np.ndarray, alpha_r: np.ndarray):
    inits = [
        numpy_helper.from_array(np.array([0], dtype=np.int64), name="s0"),
        numpy_helper.from_array(np.array([1350], dtype=np.int64), name="s_1350"),
        numpy_helper.from_array(np.array([d_tot], dtype=np.int64), name="s_dtot"),
        numpy_helper.from_array(np.array([d_tot + 8], dtype=np.int64), name="s_end"),
        numpy_helper.from_array(np.array([1], dtype=np.int64), name="s_ax1"),
        numpy_helper.from_array(np.array([5], dtype=np.int64), name="s_5"),
        numpy_helper.from_array(np.array([6], dtype=np.int64), name="s_6"),
        numpy_helper.from_array(np.array(-1.5, dtype=np.float64), name="c_neg15"),
        numpy_helper.from_array(np.array(-6.0, dtype=np.float64), name="c_neg6"),
        numpy_helper.from_array(np.array(-2.0, dtype=np.float64), name="c_neg2"),
        numpy_helper.from_array(np.array(float(tau), dtype=np.float64), name="c_tau"),
        numpy_helper.from_array(np.array(float(best_w), dtype=np.float64), name="c_wr"),
        numpy_helper.from_array(np.array(0.0, dtype=np.float64), name="c_zero"),
        numpy_helper.from_array(np.array(1.0, dtype=np.float64), name="c_one"),
        numpy_helper.from_array(alpha_base.reshape(-1, 1).astype(np.float64), name="alpha_base"),
        numpy_helper.from_array(alpha_r.reshape(-1, 1).astype(np.float64), name="alpha_r"),
    ]
    nodes = [
        helper.make_node("Slice", ["X_eval", "s0", "s_dtot", "s_ax1"], ["Q_ev"]),
        helper.make_node("Slice", ["X_eval", "s_1350", "s_dtot", "s_ax1"], ["Q_ev_stru"]),
        helper.make_node("Slice", ["X_eval", "s_dtot", "s_end", "s_ax1"], ["F_ev"]),
        helper.make_node("Slice", ["X_support", "s0", "s_dtot", "s_ax1"], ["Q_tr"]),
        helper.make_node("Slice", ["X_support", "s_1350", "s_dtot", "s_ax1"], ["Q_tr_stru"]),
        helper.make_node("Slice", ["X_support", "s_dtot", "s_end", "s_ax1"], ["F_tr"]),
    ]
    for a, b, out, sc, pref in [
        ("Q_ev", "Q_tr", "D_full", float(d_tot), "cd_full"),
        ("Q_ev_stru", "Q_tr_stru", "D_stru", float(d_tot - 1350), "cd_stru"),
        ("F_ev", "F_tr", "D_reg", 8.0, "cd_reg"),
    ]:
        ci, cn = make_cdist_two_inputs(a, b, out, sc, pref)
        inits.extend(ci)
        nodes.extend(cn)
    nodes.extend([
        helper.make_node("Add", ["D_full", "D_stru"], ["D_sum"]),
        helper.make_node("Mul", ["D_sum", "c_neg15"], ["arg_base"]),
        helper.make_node("Exp", ["arg_base"], ["K_base"]),
        helper.make_node("MatMul", ["K_base", "alpha_base"], ["z_pred"]),
        helper.make_node("Exp", ["z_pred"], ["exp_z"]),
        helper.make_node("Sub", ["exp_z", "c_one"], ["expm1_z"]),
        helper.make_node("Mul", ["expm1_z", "c_tau"], ["raw_base"]),
        helper.make_node("Max", ["raw_base", "c_zero"], ["ev_base"]),
        helper.make_node("Mul", ["D_reg", "c_neg6"], ["t_reg"]),
        helper.make_node("Mul", ["D_stru", "c_neg2"], ["t_stru"]),
        helper.make_node("Add", ["t_reg", "t_stru"], ["arg_r"]),
        helper.make_node("Exp", ["arg_r"], ["K_r"]),
        helper.make_node("MatMul", ["K_r", "alpha_r"], ["raw_r"]),
        helper.make_node("Max", ["raw_r", "c_zero"], ["ev_r"]),
        helper.make_node("Slice", ["F_ev", "s_5", "s_6", "s_ax1"], ["F_col5"]),
        helper.make_node("Mul", ["F_col5", "c_wr"], ["gate"]),
        helper.make_node("Sub", ["c_one", "gate"], ["one_minus_gate"]),
        helper.make_node("Mul", ["one_minus_gate", "ev_base"], ["part_base"]),
        helper.make_node("Mul", ["gate", "ev_r"], ["part_r"]),
        helper.make_node("Add", ["part_base", "part_r"], ["prediction_2d"]),
        helper.make_node("Squeeze", ["prediction_2d", "s_ax1"], ["prediction"]),
    ])
    graph = helper.make_graph(
        nodes,
        "exfoliation_clss_krr",
        [
            helper.make_tensor_value_info("X_eval", TensorProto.DOUBLE, [None, d_tot + 8]),
            helper.make_tensor_value_info("X_support", TensorProto.DOUBLE, [None, d_tot + 8]),
        ],
        [helper.make_tensor_value_info("prediction", TensorProto.DOUBLE, [None])],
        initializer=inits,
    )
    model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 18)], ir_version=8)
    onnx.save(model, str(onnx_path))


def export_tinnet_onnx(onnx_path: pathlib.Path, d_s: int, d_full: int, alpha_tin: np.ndarray):
    inits = [
        numpy_helper.from_array(np.array([0], dtype=np.int64), name="s0"),
        numpy_helper.from_array(np.array([d_s], dtype=np.int64), name="s_ds"),
        numpy_helper.from_array(np.array([1], dtype=np.int64), name="s_ax1"),
        numpy_helper.from_array(np.array(0.70, dtype=np.float64), name="c_070"),
        numpy_helper.from_array(np.array(0.30, dtype=np.float64), name="c_030"),
        numpy_helper.from_array(np.array(-1.2, dtype=np.float64), name="c_neg12"),
        numpy_helper.from_array(alpha_tin.reshape(-1, 1).astype(np.float64), name="alpha_tin"),
    ]
    nodes = [
        helper.make_node("Slice", ["X_eval", "s0", "s_ds", "s_ax1"], ["QS_ev_s"]),
        helper.make_node("Slice", ["X_support", "s0", "s_ds", "s_ax1"], ["QS_tr_s"]),
    ]
    for a, b, out, sc, pref in [
        ("QS_ev_s", "QS_tr_s", "Ds_ev", float(d_s), "cd_s"),
        ("X_eval", "X_support", "Df_ev", float(d_full), "cd_f"),
    ]:
        ci, cn = make_cdist_two_inputs(a, b, out, sc, pref)
        inits.extend(ci)
        nodes.extend(cn)
    nodes.extend([
        helper.make_node("Mul", ["Ds_ev", "c_070"], ["part_s"]),
        helper.make_node("Mul", ["Df_ev", "c_030"], ["part_f"]),
        helper.make_node("Add", ["part_s", "part_f"], ["D_ev"]),
        helper.make_node("Mul", ["D_ev", "c_neg12"], ["arg_tin"]),
        helper.make_node("Exp", ["arg_tin"], ["K_ev"]),
        helper.make_node("MatMul", ["K_ev", "alpha_tin"], ["pred_2d"]),
        helper.make_node("Squeeze", ["pred_2d", "s_ax1"], ["prediction"]),
    ])
    graph = helper.make_graph(
        nodes,
        "tinnet_clss_krr",
        [
            helper.make_tensor_value_info("X_eval", TensorProto.DOUBLE, [None, d_full]),
            helper.make_tensor_value_info("X_support", TensorProto.DOUBLE, [None, d_full]),
        ],
        [helper.make_tensor_value_info("prediction", TensorProto.DOUBLE, [None])],
        initializer=inits,
    )
    model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 18)], ir_version=8)
    onnx.save(model, str(onnx_path))


def write_feature_shards(task: str, ids_tr: list, ids_va: list, ids_te: list,
                         X_tv: np.ndarray, X_te: np.ndarray, chunk_size: int = 30) -> list:
    n_tr = len(ids_tr)
    n_va = len(ids_va)
    all_rows = []
    for i, jid in enumerate(ids_tr):
        all_rows.append((str(jid), "train", X_tv[i]))
    for i, jid in enumerate(ids_va):
        all_rows.append((str(jid), "val", X_tv[n_tr + i]))
    for i, jid in enumerate(ids_te):
        all_rows.append((str(jid), "test", X_te[i]))

    n_feat = X_tv.shape[1]
    header = ["id", "split"] + [f"f_{j}" for j in range(n_feat)]
    shards = []
    part_idx = 1
    for start in range(0, len(all_rows), chunk_size):
        chunk = all_rows[start:start + chunk_size]
        rel_file = f"object/features_{task}_part{part_idx}.csv"
        out_path = PKG_ROOT / rel_file
        with open(out_path, "w", newline="\n", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            for jid, sp, vec in chunk:
                w.writerow([jid, sp] + [f"{float(v):.10f}" for v in vec])
        shards.append({
            "file": rel_file,
            "rows": len(chunk),
            "bytes": out_path.stat().st_size,
            "sha256": sha256_file(out_path),
        })
        part_idx += 1
    return shards


def write_prediction_csv(path_csv: pathlib.Path, ids: np.ndarray, y_pred: np.ndarray):
    """Write jarvis_leaderboard prediction CSV with exact columns ['id', 'prediction']."""
    with open(path_csv, "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "prediction"])
        for jid, yp in zip(ids, y_pred):
            w.writerow([str(jid), f"{float(yp):.8f}"])


def write_cv_csv(path_csv: pathlib.Path, ids: np.ndarray, y_true: np.ndarray,
                 oof_clss: np.ndarray, oof_xgb: np.ndarray, loo_clss: np.ndarray):
    with open(path_csv, "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
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


def fetch_upstream_zip_json(url: str, expected_sha256: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-Trainer/1.0"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, f"SHA-256 mismatch for {url}: {actual} != {expected_sha256}"
    with zipfile.ZipFile(io.BytesIO(raw), "r") as zf:
        return json.loads(zf.read(zf.namelist()[0]).decode("utf-8"))


def fetch_upstream_leader_csv(url: str, expected_sha256: str, test_ids: np.ndarray) -> np.ndarray:
    req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-Trainer/1.0"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, f"SHA-256 mismatch for {url}: {actual} != {expected_sha256}"
    with zipfile.ZipFile(io.BytesIO(raw), "r") as zf:
        lines = zf.read(zf.namelist()[0]).decode("utf-8").splitlines()
    reader = csv.DictReader(lines)
    id_to_pred = {}
    for row in reader:
        jid = str(row.get("id", row.get(reader.fieldnames[0]))).strip()
        p_val = float(row.get("prediction", row.get(reader.fieldnames[-1])))
        id_to_pred[jid] = p_val
    return np.array([id_to_pred[str(k)] for k in test_ids], dtype=np.float64)


def load_structures_for_task(task: str, structures_dir: pathlib.Path = None) -> dict:
    if structures_dir is not None:
        gz_path = structures_dir / f"{task}_structures.json.gz"
        if gz_path.exists():
            d = json.load(gzip.open(gz_path, "rt", encoding="utf-8"))
            return d["structures"]
    # Fallback to jarvis-tools dataset lookup if installed locally
    from jarvis.db.figshare import data as jdata
    ds_name = "dft_3d" if task.startswith("dft_3d") else "tinnet_N"
    records = jdata(ds_name)
    id_key = "jid" if ds_name == "dft_3d" else "id"
    return {str(r[id_key]): r["atoms"] for r in records}


def main():
    ap = argparse.ArgumentParser(
        description="Train CLSS kernel models, run 5-fold CV (p2) and 400-permutation null controls, and export ONNX + CSVs."
    )
    ap.add_argument(
        "--structures-dir",
        type=pathlib.Path,
        default=None,
        help="Optional directory containing <task>_structures.json.gz (falls back to jarvis-tools figshare dataset).",
    )
    args = ap.parse_args()

    t_start = time.time()
    manifest = {
        "benchmark_suite": "NIST JARVIS-Leaderboard Small-Data Materials Property Prediction",
        "target_id": "jarvis-small-data-exfoliation-tc-mae",
        "tasks": {},
    }

    task_specs = [
        {
            "task": "dft_3d_exfoliation_energy",
            "claim_status": "claimed_primary_and_p2_5fold_cv",
            "csv_name": "AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv",
            "onnx_file": "object/model_dft_3d_exfoliation_energy.onnx",
            "live_best_mae": 40.887,
            "live_best_model": "matminer_xgboost",
            "units": "meV/atom",
            "upstream_benchmark_json_zip_url": "https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy.json.zip",
            "upstream_benchmark_json_zip_sha256": "d7a3127002098c3da40292bee8d78de0e45ca42bef81adc73a07bc47e900a9a4",
            "upstream_leader_csv_zip_url": "https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/contributions/matminer_xgboost/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv.zip",
            "upstream_leader_csv_zip_sha256": "e89262451215f98da0eddf327a082787461edfa5f73426baf6c4fd745acacb78",
        },
        {
            "task": "tinnet_N_ead",
            "claim_status": "uncredited_supplementary_p1_dropped_no_pre_run_dated_file",
            "csv_name": "AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv",
            "onnx_file": "object/model_tinnet_N_ead.onnx",
            "live_best_mae": 0.0871,
            "live_best_model": "alignn",
            "units": "eV",
            "upstream_benchmark_json_zip_url": "https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/tinnet_N_ead.json.zip",
            "upstream_benchmark_json_zip_sha256": "14da9466b46ccd69aea116c6d6ef456da2c2cfe955b45b89105bb9f21acdfc49",
            "upstream_leader_csv_zip_url": "https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/contributions/alignn_model/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv.zip",
            "upstream_leader_csv_zip_sha256": "5bc9f63e3016343afc3a5719611ec9335442305a5d752fd5c44fb66ff857ac59",
        },
    ]

    for spec in task_specs:
        task = spec["task"]
        t0 = time.time()
        bench = fetch_upstream_zip_json(
            spec["upstream_benchmark_json_zip_url"],
            spec["upstream_benchmark_json_zip_sha256"],
        )
        ids_tr = list(bench["train"].keys())
        ids_va = list(bench["val"].keys())
        ids_te = list(bench["test"].keys())
        assert len(set(ids_tr) & set(ids_va)) == 0
        assert len(set(ids_tr) & set(ids_te)) == 0
        assert len(set(ids_va) & set(ids_te)) == 0

        ids_tv = np.array(ids_tr + ids_va, dtype=str)
        ids_te_arr = np.array(ids_te, dtype=str)
        y_tv = np.array(
            [float(bench["train"][k]) if k in bench["train"] else float(bench["val"][k]) for k in ids_tv],
            dtype=np.float64,
        )
        y_te = np.array([float(bench["test"][k]) for k in ids_te_arr], dtype=np.float64)

        structs = load_structures_for_task(task, args.structures_dir)
        X_tv = np.vstack([featurize_structure(structs[str(k)]) for k in ids_tv])
        X_te = np.vstack([featurize_structure(structs[str(k)]) for k in ids_te_arr])

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        oof_clss = np.zeros(len(y_tv), dtype=np.float64)
        oof_xgb = np.zeros(len(y_tv), dtype=np.float64)
        onnx_path = PKG_ROOT / spec["onnx_file"]

        if task == "dft_3d_exfoliation_energy":
            F_tv = np.vstack([extract_fracture_regime_vector(structs[str(k)], X_tv[i]) for i, k in enumerate(ids_tv)])
            F_te = np.vstack([extract_fracture_regime_vector(structs[str(k)], X_te[i]) for i, k in enumerate(ids_te_arr)])
            for fold, (f_tr, f_va) in enumerate(kf.split(X_tv)):
                p_va, _, _ = fit_predict_exfoliation(X_tv[f_tr], y_tv[f_tr], F_tv[f_tr], X_tv[f_va], F_tv[f_va])
                oof_clss[f_va] = p_va
                oof_xgb[f_va] = fit_reproduced_matminer_xgboost(X_tv[f_tr], y_tv[f_tr], X_tv[f_va], seed=42 + fold)
            y_pred_te, loo_tv, params = fit_predict_exfoliation(X_tv, y_tv, F_tv, X_te, F_te)

            Q_tv, Q_te = params["Q_tr"], params["Q_ev"]
            X_tv_export = np.hstack([Q_tv, F_tv])
            X_te_export = np.hstack([Q_te, F_te])
            shards = write_feature_shards(task, ids_tr, ids_va, ids_te, X_tv_export, X_te_export, chunk_size=30)
            export_exfoliation_onnx(
                onnx_path, X_tv.shape[1], params["tau"], params["best_w_r"],
                params["alpha_base"], params["alpha_r"],
            )

            D_full_tv = cdist(Q_tv, Q_tv, "cityblock") / X_tv.shape[1]
            D_full_te = cdist(Q_te, Q_tv, "cityblock") / X_tv.shape[1]
            A_inv = np.linalg.inv(np.exp(-3.0 * D_full_tv) + 0.025 * np.eye(len(y_tv)))
            K_ev = np.exp(-3.0 * D_full_te)
            null_ctrl = run_null_permutation_control(
                y_te, K_ev, A_inv, y_tv, float(mean_absolute_error(y_te, y_pred_te)),
                n_perm=400, non_neg=True, tau=params["tau"], seed=0,
            )
            base_mae_te, _, _, base_hw90, _ = bootstrap_mae_ci90(y_te, params["ev_base"], n_boot=1000, seed=0)
            base_ablation = {
                "test_mae": base_mae_te,
                "bootstrap_1000_ci90_half_width": base_hw90,
                "analytical_loo_mae": float(mean_absolute_error(y_tv, params["loo_base"])),
            }
            onnx_inputs_meta = {
                "X_eval": [int(len(ids_te)), int(X_te_export.shape[1])],
                "X_support": [int(len(ids_tv)), int(X_tv_export.shape[1])],
            }

        elif task == "tinnet_N_ead":
            S_tv = np.vstack([extract_canonical_adsorbate_slab(structs[str(k)]) for k in ids_tv])
            S_te = np.vstack([extract_canonical_adsorbate_slab(structs[str(k)]) for k in ids_te_arr])
            for fold, (f_tr, f_va) in enumerate(kf.split(X_tv)):
                p_va, _, _ = fit_predict_tinnet(X_tv[f_tr], y_tv[f_tr], S_tv[f_tr], X_tv[f_va], S_tv[f_va])
                oof_clss[f_va] = p_va
                oof_xgb[f_va] = fit_reproduced_matminer_xgboost(X_tv[f_tr], y_tv[f_tr], X_tv[f_va], seed=42 + fold)
            y_pred_te, loo_tv, params = fit_predict_tinnet(X_tv, y_tv, S_tv, X_te, S_te)

            QS_tv, QS_te, d_s = params["QS_tr"], params["QS_ev"], params["d_s"]
            shards = write_feature_shards(task, ids_tr, ids_va, ids_te, QS_tv, QS_te, chunk_size=30)
            export_tinnet_onnx(onnx_path, d_s, QS_tv.shape[1], params["alpha"])

            D_tv = 0.70 * (cdist(QS_tv[:, :d_s], QS_tv[:, :d_s], "cityblock") / d_s) + 0.30 * (cdist(QS_tv, QS_tv, "cityblock") / QS_tv.shape[1])
            D_te = 0.70 * (cdist(QS_te[:, :d_s], QS_tv[:, :d_s], "cityblock") / d_s) + 0.30 * (cdist(QS_te, QS_tv, "cityblock") / QS_tv.shape[1])
            A_inv = np.linalg.inv(np.exp(-1.2 * D_tv) + 0.002 * np.eye(len(y_tv)))
            K_ev = np.exp(-1.2 * D_te)
            null_ctrl = run_null_permutation_control(
                y_te, K_ev, A_inv, y_tv, float(mean_absolute_error(y_te, y_pred_te)),
                n_perm=400, non_neg=False, tau=None, seed=0,
            )
            base_ablation = None
            onnx_inputs_meta = {
                "X_eval": [int(len(ids_te)), int(QS_te.shape[1])],
                "X_support": [int(len(ids_tv)), int(QS_tv.shape[1])],
            }

        pred_csv_path = OBJ_DIR / spec["csv_name"]
        write_prediction_csv(pred_csv_path, ids_te_arr, y_pred_te)
        cv_csv_path = OBJ_DIR / f"cv5_oof_{task}.csv"
        write_cv_csv(cv_csv_path, ids_tv, y_tv, oof_clss, oof_xgb, loo_tv)

        mae_te, q05, q95, hw90, _ = bootstrap_mae_ci90(y_te, y_pred_te, n_boot=1000, seed=0)
        live_best = spec["live_best_mae"]
        rel_gain_pct = 100.0 * (live_best - mae_te) / live_best
        abs_gain = live_best - mae_te
        passes_5pct = bool(rel_gain_pct >= 5.0)
        passes_ci90 = bool(abs_gain > hw90)
        hw90_seeds = [bootstrap_mae_ci90(y_te, y_pred_te, n_boot=1000, seed=s)[3] for s in range(10)]

        y_base_lb = fetch_upstream_leader_csv(
            spec["upstream_leader_csv_zip_url"],
            spec["upstream_leader_csv_zip_sha256"],
            ids_te_arr,
        )
        base_lb_mae = float(mean_absolute_error(y_te, y_base_lb))
        paired_te = paired_bootstrap_test(y_te, y_pred_te, y_base_lb, n_boot=10000, seed=0)
        w_te_stat, p_wilcox_te = wilcoxon(np.abs(y_te - y_base_lb), np.abs(y_te - y_pred_te), alternative="greater")

        te_pred_xgb = fit_reproduced_matminer_xgboost(X_tv, y_tv, X_te, seed=42)
        te_mae_xgb = float(mean_absolute_error(y_te, te_pred_xgb))
        oof_mae_clss = float(mean_absolute_error(y_tv, oof_clss))
        oof_mae_xgb = float(mean_absolute_error(y_tv, oof_xgb))
        loo_mae_clss = float(mean_absolute_error(y_tv, loo_tv))
        _, p_wilcox_cv = wilcoxon(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        _, p_wilcox_loo = wilcoxon(np.abs(y_tv - oof_xgb), np.abs(y_tv - loo_tv), alternative="greater")
        _, p_ttest_cv = ttest_rel(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        _, p_ttest_loo = ttest_rel(np.abs(y_tv - oof_xgb), np.abs(y_tv - loo_tv), alternative="greater")
        paired_cv = paired_bootstrap_test(y_tv, oof_clss, oof_xgb, n_boot=10000, seed=0)
        paired_loo = paired_bootstrap_test(y_tv, loo_tv, oof_xgb, n_boot=10000, seed=0)

        entry = {
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
            "onnx_model_file": spec["onnx_file"],
            "onnx_model_bytes": onnx_path.stat().st_size,
            "onnx_model_sha256": sha256_file(onnx_path),
            "feature_csv_shards": shards,
            "upstream_benchmark_json_zip_url": spec["upstream_benchmark_json_zip_url"],
            "upstream_benchmark_json_zip_sha256": spec["upstream_benchmark_json_zip_sha256"],
            "upstream_leader_csv_zip_url": spec["upstream_leader_csv_zip_url"],
            "upstream_leader_csv_zip_sha256": spec["upstream_leader_csv_zip_sha256"],
            "claim_status": spec["claim_status"],
            "prediction_csv_columns": ["id", "prediction"],
            "onnx_graph_inputs": onnx_inputs_meta,
            "onnx_graph_output": "prediction",
        }
        if base_ablation is not None:
            entry["base_only_ablation_w_r_0"] = base_ablation
        manifest["tasks"][task] = entry

        print(
            f"[DONE] {task}: Test MAE = {mae_te:.6f} ({spec['units']}) vs {live_best:.5f}, "
            f"h90 = {hw90:.6f}, 5-fold CV = {oof_mae_clss:.6f} vs {oof_mae_xgb:.6f} (Wilcoxon p = {p_wilcox_cv:.2e})"
        )

    manifest["total_runtime_seconds"] = float(time.time() - t_start)
    manifest_path = OBJ_DIR / "jarvis_clss_results_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {manifest_path} in {time.time() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
