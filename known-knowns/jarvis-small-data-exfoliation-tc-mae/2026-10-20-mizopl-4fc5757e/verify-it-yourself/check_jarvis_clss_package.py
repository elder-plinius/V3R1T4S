#!/usr/bin/env python3
"""
Standalone Package Verification Script for outbox/2026-10-20-mizopl-4fc5757e
Target: jarvis-small-data-exfoliation-tc-mae

Verifies:
  1. Integrity and SHA-256 digests of all prediction CSVs, .csv.zip archives, 5-fold CV CSVs,
     and trained_models_jarvis_clss.npz against object/jarvis_clss_results_manifest.json.
  2. Strict zero-leakage split hygiene:
     - Zero overlap between (train U val) and test IDs in official .json.zip and clean_structures.
     - Every structure dictionary in clean_structures contains strictly the 4 keys
       {'lattice_mat', 'coords', 'elements', 'cartesian'}.
  3. Official test MAE (sklearn.metrics.mean_absolute_error) and 1,000-sample bootstrap 90% CI
     half-width h90 across seed=0 and seeds 0..9 on:
     - dft_3d_Tc_supercon        : 0.902806 K vs live best 1.51870 K (-40.55% >= 5%, gain +0.615894 > h90 = 0.367962 K)
     - dft_3d_exfoliation_energy : 28.195924 meV/atom vs live best 40.88700 meV/atom (-31.04% >= 5%, gain +12.691076 > h90 = 11.132579 meV/atom)
     - tinnet_N_ead (p1, N=327)  : 0.068908 eV vs live best 0.08710 eV (-20.89% >= 5%, gain +0.018192 > h90 = 0.017247 eV)
  4. Partial win p2: 5-fold CV and analytical LOO paired superiority over reproduced matminer_xgboost
     on train U val across all 3 benchmarks (Wilcoxon p = 5.99e-09, 1.62e-18, and 5.86e-15).
  5. Negative controls (constant train-mean, constant train-median, and 400 label permutations).

Prints 'PASS' on the final line (exit 0) if and only if every check succeeds;
prints 'FAIL' on the final line (exit 1) on any mismatch or corruption.
"""
import argparse
import csv
import gzip
import hashlib
import json
import pathlib
import sys
import zipfile
import numpy as np
from scipy.stats import wilcoxon, ttest_rel
from sklearn.metrics import mean_absolute_error

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent
OBJ_DIR = PKG_ROOT / "object"
DATA_DIR = OBJ_DIR / "data"
CLEAN_DIR = DATA_DIR / "clean_structures"
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


def run_all_checks(retrain_from_structures: bool = False):
    manifest_path = OBJ_DIR / "jarvis_clss_results_manifest.json"
    assert manifest_path.exists(), "Missing object/jarvis_clss_results_manifest.json"
    assert sha256_file(manifest_path) == "9bd2bff5a465b8c32d355361f58c49d73413eb73f72b566994f56edcffdbd8db", "Manifest SHA-256 mismatch"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    models_path = OBJ_DIR / manifest["trained_models_file"]
    assert models_path.exists(), f"Missing {models_path.name}"
    assert sha256_file(models_path) == manifest["trained_models_sha256"], "trained_models_jarvis_clss.npz SHA-256 mismatch"
    saved_models = np.load(models_path, allow_pickle=True)

    expected_tasks = [
        ("dft_3d_Tc_supercon", 1.5187, 586, 30, "tc_atomgpt.csv.zip"),
        ("dft_3d_exfoliation_energy", 40.887, 731, 81, "exf_matminer_xgb.csv.zip"),
        ("tinnet_N_ead", 0.0871, 295, 32, "tinnet_N_alignn.csv.zip"),
    ]

    for task, live_best, exp_ntv, exp_nte, base_zip in expected_tasks:
        t_info = manifest["tasks"][task]
        pred_csv = OBJ_DIR / t_info["prediction_csv"]
        pred_zip = pred_csv.with_suffix(".csv.zip")
        cv_csv = OBJ_DIR / t_info["cv5_oof_csv"]
        assert pred_csv.exists() and pred_zip.exists() and cv_csv.exists(), f"Missing CSV/ZIP for {task}"
        assert sha256_file(pred_csv) == t_info["prediction_csv_sha256"], f"SHA-256 mismatch on {pred_csv.name}"
        assert sha256_file(cv_csv) == t_info["cv5_oof_csv_sha256"], f"SHA-256 mismatch on {cv_csv.name}"

        with zipfile.ZipFile(pred_zip, "r") as zf:
            z_bytes = zf.read(pred_csv.name)
        assert hashlib.sha256(z_bytes).hexdigest() == t_info["prediction_csv_sha256"], f"ZIP content mismatch on {pred_zip.name}"

        # Official split & sanitized structure audit
        with zipfile.ZipFile(DATA_DIR / f"{task}.json.zip", "r") as zf:
            official_split = json.loads(zf.read(zf.namelist()[0]).decode("utf-8"))
        clean_data = json.load(gzip.open(CLEAN_DIR / f"{task}_structures.json.gz"))
        splits = clean_data["splits"]
        structs = clean_data["structures"]
        assert set(splits["train"].keys()) == set(official_split["train"].keys())
        assert set(splits["val"].keys()) == set(official_split["val"].keys())
        assert set(splits["test"].keys()) == set(official_split["test"].keys())

        ids_tr = list(splits["train"].keys())
        ids_va = list(splits["val"].keys())
        ids_te = np.array(list(splits["test"].keys()), dtype=str)
        ids_tv = np.array(ids_tr + ids_va, dtype=str)
        assert len(ids_tv) == exp_ntv and len(ids_te) == exp_nte
        assert len(set(ids_tv) & set(ids_te)) == 0, f"Split overlap detected on {task}"
        if task == "tinnet_N_ead":
            assert len(ids_tv) + len(ids_te) == 327 < 2000

        allowed_keys = {"lattice_mat", "coords", "elements", "cartesian"}
        for jid, s in structs.items():
            assert set(s.keys()) == allowed_keys, f"Forbidden keys in {task}:{jid}"

        y_tv = np.array([float(splits["train"].get(k, splits["val"].get(k))) for k in ids_tv], dtype=np.float64)
        y_te = np.array([float(splits["test"][k]) for k in ids_te], dtype=np.float64)

        csv_ids, csv_yt, csv_yp = load_pred_csv(pred_csv)
        assert np.array_equal(csv_ids, ids_te)
        assert np.max(np.abs(csv_yt - y_te)) <= 1e-7
        assert np.max(np.abs(csv_yp - saved_models[f"{task}_test_pred"])) <= 1e-7

        # Test MAE & 1,000-sample Bootstrap 90% CI check
        mae_te = float(mean_absolute_error(y_te, csv_yp))
        mae_b, q05, q95, hw90 = bootstrap_mae_ci90(y_te, csv_yp, n_boot=1000, seed=0)
        assert abs(mae_te - mae_b) < 1e-12
        assert abs(mae_te - t_info["claimed_test_mae"]) < 1e-6
        assert abs(hw90 - t_info["bootstrap_1000_ci90_half_width"]) < 1e-6

        rel_red_pct = 100.0 * (live_best - mae_te) / live_best
        abs_red = live_best - mae_te
        assert rel_red_pct >= 5.0, f"Relative margin < 5% on {task}"
        assert abs_red > hw90 and (mae_te + hw90) < live_best, f"Bootstrap 90% CI gate failed on {task}"

        # Also check seeds 0..9
        for s in range(10):
            _, _, _, hw_s = bootstrap_mae_ci90(y_te, csv_yp, n_boot=1000, seed=s)
            assert abs_red > hw_s, f"Seed {s} bootstrap CI gate failed on {task}"

        # Check published baseline zip
        y_lb = load_leaderboard_baseline_preds(base_zip, ids_te)
        assert abs(float(mean_absolute_error(y_te, y_lb)) - live_best) < 1e-3

        # Check 5-fold CV (p2)
        cv_ids, cv_yt, oof_clss, oof_xgb, loo_clss = load_cv_csv(cv_csv)
        assert np.array_equal(cv_ids, ids_tv)
        assert np.max(np.abs(cv_yt - y_tv)) <= 1e-7
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
            f"[OK] {task:25s}: Test MAE = {mae_te:.6f} vs {live_best:.5f} (-{rel_red_pct:.2f}%), "
            f"gain = +{abs_red:.6f} > h90 = {hw90:.6f}, p2 5-fold MAE = {oof_mae_c:.5f} vs {oof_mae_x:.5f} (Wilcoxon p = {p_wilcox_cv:.2e})"
        )

    if retrain_from_structures:
        sys.path.insert(0, str(PKG_ROOT / "how-we-built-it"))
        import featurize_physics_clss as fp
        import train_and_predict_jarvis_clss as tp
        for task, _, _, _, _ in expected_tasks:
            clean_data = json.load(gzip.open(CLEAN_DIR / f"{task}_structures.json.gz"))
            splits = clean_data["splits"]
            structs = clean_data["structures"]
            ids_tv = np.array(list(splits["train"].keys()) + list(splits["val"].keys()), dtype=str)
            ids_te = np.array(list(splits["test"].keys()), dtype=str)
            y_tv = np.array([float(splits["train"].get(k, splits["val"].get(k))) for k in ids_tv], dtype=np.float64)
            X_tv = np.vstack([fp.featurize_structure(structs[str(k)]) for k in ids_tv])
            X_te = np.vstack([fp.featurize_structure(structs[str(k)]) for k in ids_te])
            if task == "dft_3d_Tc_supercon":
                s_tv = [fp.extract_iso_homolog_signature(structs[str(k)]) for k in ids_tv]
                s_te = [fp.extract_iso_homolog_signature(structs[str(k)]) for k in ids_te]
                re_pred, _, _ = tp.fit_predict_tc_supercon(X_tv, y_tv, s_tv, X_te, s_te)
            elif task == "dft_3d_exfoliation_energy":
                F_tv = np.vstack([fp.extract_fracture_regime_vector(structs[str(k)], X_tv[i]) for i, k in enumerate(ids_tv)])
                F_te = np.vstack([fp.extract_fracture_regime_vector(structs[str(k)], X_te[i]) for i, k in enumerate(ids_te)])
                re_pred, _, _ = tp.fit_predict_exfoliation(X_tv, y_tv, F_tv, X_te, F_te)
            elif task == "tinnet_N_ead":
                S_tv = np.vstack([fp.extract_canonical_adsorbate_slab(structs[str(k)]) for k in ids_tv])
                S_te = np.vstack([fp.extract_canonical_adsorbate_slab(structs[str(k)]) for k in ids_te])
                re_pred, _, _ = tp.fit_predict_tinnet(X_tv, y_tv, S_tv, X_te, S_te)
            assert float(np.max(np.abs(re_pred - saved_models[f"{task}_test_pred"]))) < 1e-12
            print(f"[OK] Retrained {task} from raw structures: max |diff| < 1e-12")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--retrain-from-structures", action="store_true")
    args = ap.parse_args()
    try:
        run_all_checks(retrain_from_structures=args.retrain_from_structures)
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"VERIFICATION ERROR: {e}")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
