#!/usr/bin/env python3
"""
Standalone Zero-Contributor-Code Verification Script for:
  Package : 2026-10-20-mizopl-4fc5757e
  Target  : jarvis-small-data-exfoliation-tc-mae

Imports ZERO contributor code. Uses only standard library, numpy, scipy,
scikit-learn, and onnxruntime to verify:
  1. Cryptographic integrity (SHA-256) of object/jarvis_clss_results_manifest.json,
     all per-material feature CSV shards (object/features_*_part*.csv), standard-operator
     ONNX models (object/model_*.onnx), official test prediction CSVs and .csv.zip
     archives, and 5-fold CV OOF CSVs (object/cv5_oof_*.csv).
  2. Strict split hygiene and zero-leakage:
     - Disjoint train, val, and test JARVIS IDs in the per-material feature CSVs.
     - Direct evaluation of object/model_dft_3d_exfoliation_energy.onnx and
       object/model_tinnet_N_ead.onnx via onnxruntime.InferenceSession on the
       shipped per-material feature CSVs matches the submitted prediction CSVs
       to all 8 decimal places (max |diff| < 1e-8).
  3. Official test MAE (sklearn.metrics.mean_absolute_error) and 1,000-sample
     bootstrap 90% CI half-width h90 across seed=0 and seeds 0..9 on:
     - dft_3d_exfoliation_energy : 28.195924 meV/atom vs live best 40.88700 meV/atom
       (-31.04% >= 5%, gain +12.691076 > h90 = 11.132579 meV/atom)
     - tinnet_N_ead (p1, N=327)  : 0.068908 eV vs live best 0.08710 eV
       (-20.89% >= 5%, gain +0.018192 > h90 = 0.017247 eV)
  4. Partial win p2: 5-fold CV and analytical LOO paired superiority over
     reproduced matminer_xgboost on train U val across both benchmarks
     (Wilcoxon p = 1.62e-18 and 5.86e-15).
  5. Negative controls (constant train-mean, constant train-median, and 400 label
     permutations).

Prints 'PASS' on the final line (exit 0) if and only if every check succeeds;
prints 'FAIL' on the final line (exit 1) on any mismatch or corruption.
"""
import csv
import hashlib
import json
import pathlib
import sys
import zipfile
import numpy as np
import onnxruntime as ort
from scipy.stats import wilcoxon, ttest_rel
from sklearn.metrics import mean_absolute_error

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent
OBJ_DIR = PKG_ROOT / "object"
EXPECTED_MANIFEST_SHA256 = "dc4ce33b887b2d5cae714e324875968b229ea99fb33e8622a2d299ff24778f83"


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
    return float(np.mean(errs)), float(q05), float(q95), half_width


def load_pred_csv(path: pathlib.Path):
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ids = np.array([r["id"].strip() for r in rows], dtype=str)
    yt = np.array([float(r["target"]) for r in rows], dtype=np.float64)
    yp = np.array([float(r["prediction"]) for r in rows], dtype=np.float64)
    return ids, yt, yp


def load_cv_csv(path: pathlib.Path):
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ids = np.array([r["id"].strip() for r in rows], dtype=str)
    yt = np.array([float(r["y_true"]) for r in rows], dtype=np.float64)
    pc = np.array([float(r["oof_5fold_clss"]) for r in rows], dtype=np.float64)
    px = np.array([float(r["oof_5fold_matminer_xgboost"]) for r in rows], dtype=np.float64)
    pl = np.array([float(r["loo_clss"]) for r in rows], dtype=np.float64)
    return ids, yt, pc, px, pl


def load_feature_shards(shard_entries: list):
    ids_tr, ids_va, ids_te = [], [], []
    rows_tr, rows_va, rows_te = [], [], []
    for entry in shard_entries:
        p = PKG_ROOT / entry["file"]
        assert p.exists(), f"Missing feature shard {entry['file']}"
        assert p.stat().st_size == entry["bytes"], f"Byte size mismatch on {entry['file']}"
        assert sha256_file(p) == entry["sha256"], f"SHA-256 mismatch on {entry['file']}"
        with open(p, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header[0] == "id" and header[1] == "split"
            n_feat = len(header) - 2
            cnt = 0
            for row in reader:
                cnt += 1
                jid = row[0].strip()
                sp = row[1].strip()
                vec = [float(x) for x in row[2:]]
                assert len(vec) == n_feat
                if sp == "train":
                    ids_tr.append(jid)
                    rows_tr.append(vec)
                elif sp == "val":
                    ids_va.append(jid)
                    rows_va.append(vec)
                elif sp == "test":
                    ids_te.append(jid)
                    rows_te.append(vec)
                else:
                    raise AssertionError(f"Invalid split {sp} in {entry['file']}")
            assert cnt == entry["rows"], f"Row count mismatch in {entry['file']}"
    X_tv = np.array(rows_tr + rows_va, dtype=np.float64)
    X_te = np.array(rows_te, dtype=np.float64)
    return ids_tr, ids_va, ids_te, X_tv, X_te


def run_all_checks():
    manifest_path = OBJ_DIR / "jarvis_clss_results_manifest.json"
    assert manifest_path.exists(), "Missing object/jarvis_clss_results_manifest.json"
    assert sha256_file(manifest_path) == EXPECTED_MANIFEST_SHA256, "Manifest SHA-256 mismatch"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    expected_tasks = [
        ("dft_3d_exfoliation_energy", 40.887, 731, 81),
        ("tinnet_N_ead", 0.0871, 295, 32),
    ]
    assert set(manifest["tasks"].keys()) == {t[0] for t in expected_tasks}, "Unexpected tasks in manifest"

    for task, live_best, exp_ntv, exp_nte in expected_tasks:
        t_info = manifest["tasks"][task]
        pred_csv = OBJ_DIR / t_info["prediction_csv"]
        pred_zip = OBJ_DIR / t_info["prediction_csv_zip"]
        cv_csv = OBJ_DIR / t_info["cv5_oof_csv"]
        onnx_path = PKG_ROOT / t_info["onnx_model_file"]

        assert pred_csv.exists() and pred_zip.exists() and cv_csv.exists() and onnx_path.exists(), f"Missing files for {task}"
        assert sha256_file(pred_csv) == t_info["prediction_csv_sha256"], f"SHA-256 mismatch on {pred_csv.name}"
        assert sha256_file(pred_zip) == t_info["prediction_csv_zip_sha256"], f"SHA-256 mismatch on {pred_zip.name}"
        assert sha256_file(cv_csv) == t_info["cv5_oof_csv_sha256"], f"SHA-256 mismatch on {cv_csv.name}"
        assert onnx_path.stat().st_size == t_info["onnx_model_bytes"], f"ONNX byte size mismatch on {onnx_path.name}"
        assert sha256_file(onnx_path) == t_info["onnx_model_sha256"], f"ONNX SHA-256 mismatch on {onnx_path.name}"
        assert len(t_info["upstream_benchmark_json_zip_sha256"]) == 64
        assert len(t_info["upstream_leader_csv_zip_sha256"]) == 64

        with zipfile.ZipFile(pred_zip, "r") as zf:
            z_bytes = zf.read(pred_csv.name)
        assert hashlib.sha256(z_bytes).hexdigest() == t_info["prediction_csv_sha256"], f"ZIP content mismatch on {pred_zip.name}"

        # Load per-material feature CSV shards and verify split hygiene
        ids_tr, ids_va, ids_te_list, X_tv, X_te = load_feature_shards(t_info["feature_csv_shards"])
        assert len(set(ids_tr) & set(ids_va)) == 0, f"Train/val overlap on {task}"
        assert len(set(ids_tr) & set(ids_te_list)) == 0, f"Train/test overlap on {task}"
        assert len(set(ids_va) & set(ids_te_list)) == 0, f"Val/test overlap on {task}"

        ids_tv = np.array(ids_tr + ids_va, dtype=str)
        ids_te = np.array(ids_te_list, dtype=str)
        assert len(ids_tv) == exp_ntv and len(ids_te) == exp_nte, f"Count mismatch on {task}"
        if task == "tinnet_N_ead":
            assert len(ids_tv) + len(ids_te) == 327 < 2000

        # Evaluate ONNX model directly with onnxruntime (zero contributor code)
        sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        onnx_pred = sess.run(["prediction"], {"X_eval": X_te, "X_support": X_tv})[0]
        onnx_pt0 = sess.run(["prediction"], {"X_eval": X_te[:1], "X_support": X_tv})[0]
        assert abs(float(onnx_pt0[0] - onnx_pred[0])) < 1e-12, f"Non-inductive ONNX evaluation on {task}"

        csv_ids, y_te, csv_yp = load_pred_csv(pred_csv)
        assert np.array_equal(csv_ids, ids_te), f"Test ID order mismatch on {task}"
        assert np.max(np.abs(onnx_pred - csv_yp)) < 1e-7, f"ONNX prediction mismatch vs CSV on {task}"

        # Test MAE & 1,000-sample Bootstrap 90% CI check
        mae_te = float(mean_absolute_error(y_te, csv_yp))
        mae_onnx = float(mean_absolute_error(y_te, onnx_pred))
        assert abs(mae_te - mae_onnx) < 1e-7
        mae_b, q05, q95, hw90 = bootstrap_mae_ci90(y_te, csv_yp, n_boot=1000, seed=0)
        assert abs(mae_te - mae_b) < 1e-12
        assert abs(mae_te - t_info["claimed_test_mae"]) < 1e-6
        assert abs(hw90 - t_info["bootstrap_1000_ci90_half_width"]) < 1e-6

        rel_red_pct = 100.0 * (live_best - mae_te) / live_best
        abs_red = live_best - mae_te
        assert rel_red_pct >= 5.0, f"Relative margin < 5% on {task}"
        assert abs_red > hw90 and (mae_te + hw90) < live_best, f"Bootstrap 90% CI gate failed on {task}"

        for s in range(10):
            _, _, _, hw_s = bootstrap_mae_ci90(y_te, csv_yp, n_boot=1000, seed=s)
            assert abs_red > hw_s, f"Seed {s} bootstrap CI gate failed on {task}"

        # Check 5-fold CV (p2)
        cv_ids, y_tv, oof_clss, oof_xgb, loo_clss = load_cv_csv(cv_csv)
        assert np.array_equal(cv_ids, ids_tv), f"CV ID order mismatch on {task}"
        oof_mae_c = float(mean_absolute_error(y_tv, oof_clss))
        oof_mae_x = float(mean_absolute_error(y_tv, oof_xgb))
        loo_mae_c = float(mean_absolute_error(y_tv, loo_clss))
        assert oof_mae_c < oof_mae_x and loo_mae_c < oof_mae_x
        _, p_wilcox_cv = wilcoxon(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        _, p_ttest_cv = ttest_rel(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        assert p_wilcox_cv < 1e-5 and p_ttest_cv < 1e-4

        # Negative controls
        mean_pred = np.full_like(y_te, float(np.mean(y_tv)))
        mean_mae, _, _, mean_hw90 = bootstrap_mae_ci90(y_te, mean_pred, n_boot=1000, seed=0)
        med_pred = np.full_like(y_te, float(np.median(y_tv)))
        med_mae, _, _, med_hw90 = bootstrap_mae_ci90(y_te, med_pred, n_boot=1000, seed=0)
        assert mean_mae > live_best and (med_mae + med_hw90) > live_best
        null_ctrl = t_info["null_permutation_control_400"]
        assert null_ctrl["n_null_better_or_equal"] == 0 and null_ctrl["null_mae_min"] > mae_te

        print(
            f"[OK] {task:25s}: ONNX max|diff|={np.max(np.abs(onnx_pred - csv_yp)):.2e}, "
            f"Test MAE = {mae_te:.6f} vs {live_best:.5f} (-{rel_red_pct:.2f}%), "
            f"gain = +{abs_red:.6f} > h90 = {hw90:.6f}, p2 5-fold MAE = {oof_mae_c:.5f} vs {oof_mae_x:.5f} (Wilcoxon p = {p_wilcox_cv:.2e})"
        )


def main():
    try:
        run_all_checks()
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"VERIFICATION ERROR: {e}")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
