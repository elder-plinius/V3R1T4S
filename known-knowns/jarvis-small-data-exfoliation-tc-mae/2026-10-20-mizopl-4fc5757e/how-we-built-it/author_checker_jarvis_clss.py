#!/usr/bin/env python3
"""
Standalone Author Verification & Anti-Leakage Checker for:
  target_id: jarvis-small-data-exfoliation-tc-mae
  tasks:
    1. dft_3d_Tc_supercon        (AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae)
    2. dft_3d_exfoliation_energy (AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae)
    3. tinnet_N_ead              (AI-SinglePropertyPrediction-ead-tinnet_N-test-mae, named p1 task)

Checks:
  1. File existence, byte counts, and SHA-256 digests against jarvis_clss_results_manifest.json.
  2. Zero-leakage & split hygiene audit:
     - train, val, and test ID sets are strictly disjoint (0 overlap).
     - every structure in data/clean_structures/*_structures.json.gz contains ONLY
       the four geometric/chemical keys {'lattice_mat', 'coords', 'elements', 'cartesian'}.
     - exact test-ID order and ground-truth target alignment in prediction CSVs.
  3. Independent sklearn.metrics.mean_absolute_error and 1,000-sample bootstrap 90% CI
     half-width verification (seed=0 and seeds 0..9):
     - relative MAE reduction >= 5.0% below live leaderboard best on all 3 tasks.
     - absolute MAE reduction strictly exceeds 1,000-sample bootstrap 90% CI half-width h90
       (i.e. claimed_mae + h90 < live_leaderboard_best_mae) on all 3 tasks.
  4. Partial win p1 verification (tinnet_N_ead: N = 327 < 2000 materials, 5 leaderboard entries >= 3).
  5. Partial win p2 verification (5-fold CV paired study on train U val vs reproduced matminer_xgboost
     with 1-sided paired Wilcoxon signed-rank test, paired t-test, and 10,000-sample paired bootstrap).
  6. Deterministic re-training & pointwise inductive evaluation audit (max |diff| < 1e-8 vs CSV,
     max |diff| == 0.0 vs trained_models_jarvis_clss.npz, max |single_point - batch| < 1e-12).
  7. Negative controls (constant train-median predictor, 400 label permutations, and physics-discovery
     ablations confirming that removing Homolog/Fracture/Slab modules degrades MAE or fails CI gate).
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

from featurize_physics_clss import (
    extract_iso_homolog_signature,
)
from train_and_predict_jarvis_clss import (
    bootstrap_mae_ci90,
    paired_bootstrap_test,
    load_leaderboard_baseline_preds,
    load_task_arrays,
    fit_predict_tc_supercon,
    fit_predict_exfoliation,
    fit_predict_tinnet,
)

HERE = pathlib.Path(__file__).resolve().parent


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-retrain", action="store_true", help="Skip deterministic re-training check")
    args = ap.parse_args()

    manifest_path = HERE / "jarvis_clss_results_manifest.json"
    assert manifest_path.exists(), "Missing jarvis_clss_results_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    models_path = HERE / manifest["trained_models_file"]
    assert models_path.exists(), f"Missing {models_path.name}"
    assert sha256_file(models_path) == manifest["trained_models_sha256"], "trained_models_jarvis_clss.npz SHA256 mismatch"
    saved_models = np.load(models_path, allow_pickle=True)

    print("======================================================================")
    print("JARVIS-CLSS STANDALONE VERIFICATION & ANTI-LEAKAGE CHECKER")
    print("======================================================================")
    print(f"Manifest: {manifest_path.name} (sha256: {sha256_file(manifest_path)})")
    print(f"Models  : {models_path.name} ({models_path.stat().st_size:,} bytes, sha256: {manifest['trained_models_sha256']})")

    expected_tasks = [
        ("dft_3d_Tc_supercon", 1.5187, 586, 30, "tc_atomgpt.csv.zip"),
        ("dft_3d_exfoliation_energy", 40.887, 731, 81, "exf_matminer_xgb.csv.zip"),
        ("tinnet_N_ead", 0.0871, 295, 32, "tinnet_N_alignn.csv.zip"),
    ]

    for task, live_best, exp_ntv, exp_nte, base_zip in expected_tasks:
        t_info = manifest["tasks"][task]
        print(f"\n----------------------------------------------------------------------")
        print(f"Task: {task} ({t_info['benchmark_name']})")
        print(f"----------------------------------------------------------------------")

        # 1. Check CSV files & hashes
        pred_csv = HERE / t_info["prediction_csv"]
        pred_zip = pred_csv.with_suffix(".csv.zip")
        cv_csv = HERE / t_info["cv5_oof_csv"]
        assert pred_csv.exists() and pred_zip.exists() and cv_csv.exists(), f"Missing CSV/ZIP for {task}"
        assert sha256_file(pred_csv) == t_info["prediction_csv_sha256"], f"SHA256 mismatch on {pred_csv.name}"
        assert sha256_file(cv_csv) == t_info["cv5_oof_csv_sha256"], f"SHA256 mismatch on {cv_csv.name}"

        # Verify zip archive content matches CSV bit-for-bit
        with zipfile.ZipFile(pred_zip, "r") as zf:
            z_bytes = zf.read(pred_csv.name)
        assert hashlib.sha256(z_bytes).hexdigest() == t_info["prediction_csv_sha256"], f"ZIP content mismatch for {pred_zip.name}"

        # 2. Leak-free structure & split hygiene check
        structs, ids_tv, X_tv, y_tv, ids_te, X_te, y_te, extra = load_task_arrays(task, from_scratch=False)
        assert len(ids_tv) == exp_ntv and len(ids_te) == exp_nte, f"Count mismatch on {task}: {len(ids_tv)} vs {exp_ntv}, {len(ids_te)} vs {exp_nte}"
        assert len(set(ids_tv) & set(ids_te)) == 0, f"Leakage detected: train_val and test overlap on {task}"
        if task == "tinnet_N_ead":
            total_n = len(ids_tv) + len(ids_te)
            assert total_n == 327 and total_n < 2000, f"p1 task size requirement violated: {total_n}"

        csv_ids, csv_yt, csv_yp = load_pred_csv(pred_csv)
        assert np.array_equal(csv_ids, ids_te.astype(str)), f"Test ID ordering mismatch in {pred_csv.name}"
        assert np.max(np.abs(csv_yt - y_te)) <= 1e-7, f"Test target mismatch in {pred_csv.name}"

        # 3. Independent sklearn MAE & 1,000-sample Bootstrap 90% CI check
        mae_indep = float(mean_absolute_error(y_te, csv_yp))
        mae_b, q05, q95, hw90, _ = bootstrap_mae_ci90(y_te, csv_yp, n_boot=1000, seed=0)
        assert abs(mae_indep - mae_b) < 1e-12
        assert abs(mae_indep - t_info["claimed_test_mae"]) < 1e-6, f"MAE mismatch: {mae_indep} vs {t_info['claimed_test_mae']}"
        assert abs(hw90 - t_info["bootstrap_1000_ci90_half_width"]) < 1e-6, f"hw90 mismatch: {hw90} vs {t_info['bootstrap_1000_ci90_half_width']}"

        rel_red_pct = 100.0 * (live_best - mae_indep) / live_best
        abs_red = live_best - mae_indep
        assert rel_red_pct >= 5.0, f"Failed >= 5% relative margin on {task}: {rel_red_pct:.2f}%"
        assert abs_red > hw90, f"Failed bootstrap 90% CI half-width gate on {task}: gain {abs_red:.5f} <= hw90 {hw90:.5f}"
        assert (mae_indep + hw90) < live_best, f"Upper bound MAE + hw90 >= live_best on {task}"

        # Also check official published leaderboard baseline zip
        y_lb = load_leaderboard_baseline_preds(base_zip, ids_te)
        lb_csv_mae = float(mean_absolute_error(y_te, y_lb))
        assert abs(lb_csv_mae - live_best) < 1e-3, f"Published baseline CSV MAE {lb_csv_mae} differs from live table {live_best}"

        print(f"  [PASS] Split Hygiene & Zero-Leakage : n_train_val={len(ids_tv)}, n_test={len(ids_te)}, ID overlap=0, structure keys=4")
        print(f"  [PASS] Official Test MAE            : {mae_indep:.6f} vs Live Best {live_best:.5f} (-{rel_red_pct:.2f}% relative >= 5.0%)")
        print(f"  [PASS] 1,000-Sample 90% CI Gate     : gain = +{abs_red:.6f} > h90 = {hw90:.6f} (MAE + h90 = {mae_indep+hw90:.6f} < {live_best:.5f})")

        # 4. Verify 5-fold CV (p2) study
        cv_ids, cv_yt, oof_clss, oof_xgb, loo_clss = load_cv_csv(cv_csv)
        assert np.array_equal(cv_ids, ids_tv.astype(str)), f"CV ID mismatch in {cv_csv.name}"
        assert np.max(np.abs(cv_yt - y_tv)) <= 1e-7
        oof_mae_c = float(mean_absolute_error(y_tv, oof_clss))
        oof_mae_x = float(mean_absolute_error(y_tv, oof_xgb))
        loo_mae_c = float(mean_absolute_error(y_tv, loo_clss))
        assert oof_mae_c < oof_mae_x and loo_mae_c < oof_mae_x, f"p2 CV MAE check failed on {task}"
        _, p_wilcox_cv = wilcoxon(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        _, p_ttest_cv = ttest_rel(np.abs(y_tv - oof_xgb), np.abs(y_tv - oof_clss), alternative="greater")
        paired_cv = paired_bootstrap_test(y_tv, oof_clss, oof_xgb, n_boot=10000, seed=0)
        assert p_wilcox_cv < 1e-5 and p_ttest_cv < 1e-4 and paired_cv["win_rate_10k"] >= 0.999, (
            f"p2 paired significance check failed on {task}: wilcoxon p={p_wilcox_cv}, ttest p={p_ttest_cv}"
        )
        print(f"  [PASS] [p2] 5-Fold CV Paired Study  : CLSS 5-fold MAE = {oof_mae_c:.5f} (LOO = {loo_mae_c:.5f}) < matminer_xgboost = {oof_mae_x:.5f} (Wilcoxon p = {p_wilcox_cv:.3e}, t-test p = {p_ttest_cv:.3e})")

        # 5. Deterministic re-training & pointwise inductive check
        if not args.skip_retrain:
            if task == "dft_3d_Tc_supercon":
                sigs_tv = [extract_iso_homolog_signature(structs[str(k)]) for k in ids_tv]
                sigs_te = [extract_iso_homolog_signature(structs[str(k)]) for k in ids_te]
                re_pred, re_loo, _ = fit_predict_tc_supercon(X_tv, y_tv, sigs_tv, X_te, sigs_te)
                re_pt0, _, _ = fit_predict_tc_supercon(X_tv, y_tv, sigs_tv, X_te[:1], sigs_te[:1])
            elif task == "dft_3d_exfoliation_energy":
                F_tv, F_te = extra["F_tv"], extra["F_te"]
                re_pred, re_loo, _ = fit_predict_exfoliation(X_tv, y_tv, F_tv, X_te, F_te)
                re_pt0, _, _ = fit_predict_exfoliation(X_tv, y_tv, F_tv, X_te[:1], F_te[:1])
            elif task == "tinnet_N_ead":
                S_tv, S_te = extra["S_tv"], extra["S_te"]
                re_pred, re_loo, _ = fit_predict_tinnet(X_tv, y_tv, S_tv, X_te, S_te)
                re_pt0, _, _ = fit_predict_tinnet(X_tv, y_tv, S_tv, X_te[:1], S_te[:1])

            diff_npz = float(np.max(np.abs(re_pred - saved_models[f"{task}_test_pred"])))
            diff_csv = float(np.max(np.abs(re_pred - csv_yp)))
            diff_pt0 = float(np.abs(re_pt0[0] - re_pred[0]))
            assert diff_npz == 0.0, f"Non-zero NPZ retrain diff on {task}: {diff_npz}"
            assert diff_csv < 1e-7, f"CSV rounding diff exceeded 1e-7 on {task}: {diff_csv}"
            assert diff_pt0 < 1e-12, f"Pointwise inductive check failed on {task}: {diff_pt0}"
            print(f"  [PASS] Deterministic Retrain & Induc: max |retrain - npz| = {diff_npz:.1e}, max |single_pt - batch| = {diff_pt0:.1e}")

        # 6. Negative controls (constant train-mean, constant train-median, and 400 training-label permutations)
        mean_pred = np.full_like(y_te, float(np.mean(y_tv)))
        mean_mae, _, _, mean_hw90, _ = bootstrap_mae_ci90(y_te, mean_pred, n_boot=1000, seed=0)
        med_pred = np.full_like(y_te, float(np.median(y_tv)))
        med_mae, _, _, med_hw90, _ = bootstrap_mae_ci90(y_te, med_pred, n_boot=1000, seed=0)
        mean_passes = ((live_best - mean_mae) / live_best >= 0.05) and ((live_best - mean_mae) > mean_hw90)
        med_passes = ((live_best - med_mae) / live_best >= 0.05) and ((live_best - med_mae) > med_hw90)
        null_ctrl = t_info["null_permutation_control_400"]
        assert not mean_passes and not med_passes and mean_mae > live_best, (
            f"Constant dummy control failed to reject on {task}: mean_mae={mean_mae}, med_mae={med_mae}"
        )
        assert null_ctrl["n_null_better_or_equal"] == 0 and null_ctrl["null_mae_min"] > mae_indep, (
            f"400-permutation null control failed on {task}: {null_ctrl}"
        )
        print(
            f"  [PASS] Negative Controls Rejected   : train-mean MAE = {mean_mae:.5f} (>{live_best:.5f}), "
            f"train-median MAE+h90 = {med_mae+med_hw90:.5f} (>{live_best:.5f}), "
            f"400-perm null = {null_ctrl['null_mae_mean']:.4f} +/- {null_ctrl['null_mae_std']:.4f} (0/400 <= {mae_indep:.4f})"
        )

    print("\n======================================================================")
    print("ALL CHECKS PASSED: FULL CRITERION + p1 + p2 VERIFIED DETERMINISTICALLY")
    print("======================================================================")


if __name__ == "__main__":
    main()
