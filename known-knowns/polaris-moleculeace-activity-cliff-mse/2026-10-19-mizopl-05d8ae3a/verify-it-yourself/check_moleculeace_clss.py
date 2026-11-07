#!/usr/bin/env python3
"""
Standalone verifier for polaris-moleculeace-activity-cliff-mse in outbox package.
Fetches upstream MoleculeACE CSVs from https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/
(caching in ${MOLECULEACE_UPSTREAM_CACHE:-tempfile.gettempdir()/moleculeace_upstream_cache}) and fails cleanly if any
SHA-256 does not match the recorded digest in the-record-we-beat/polaris_moleculeace_30_audit.json.
"""
import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from sklearn.metrics import mean_squared_error

RDLogger.DisableLog("rdApp.*")

PKG_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_BASE = "https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data"
RESULTS_CSV_URL = f"{UPSTREAM_BASE}/results/MoleculeACE_results.csv"
RESULTS_CSV_SHA256 = "6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ensure_upstream_file(rel_path: str, url: str, expected_sha256: str, cache_root: Path) -> Path:
    dest = cache_root / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-verifier/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch upstream CSV {url}: {exc}") from exc
        actual_sha = hashlib.sha256(data).hexdigest()
        if actual_sha != expected_sha256:
            raise AssertionError(
                f"Upstream SHA-256 mismatch for {url}: expected {expected_sha256}, got {actual_sha}"
            )
        dest.write_bytes(data)
    actual_sha = sha256_file(dest)
    if actual_sha != expected_sha256:
        raise AssertionError(
            f"SHA-256 mismatch for {dest} ({url}): expected {expected_sha256}, got {actual_sha}"
        )
    return dest


def paired_and_scalar_bootstrap(y_true, pred_model, pred_base, ref_mse, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    err_model = (y_true - pred_model) ** 2
    err_base = (y_true - pred_base) ** 2
    idx = rng.integers(0, n, size=(n_boot, n))
    boot_m = np.mean(err_model[idx], axis=1)
    boot_b = np.mean(err_base[idx], axis=1)
    return float(np.mean(boot_m < boot_b)), float(np.mean(boot_m < ref_mse))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=str, default=None, help="Optional path to primary prediction CSV")
    parser.add_argument(
        "--upstream-cache",
        type=str,
        default=os.environ.get(
            "MOLECULEACE_UPSTREAM_CACHE",
            os.path.join(tempfile.gettempdir(), "moleculeace_upstream_cache"),
        ),
        help="Directory for fetched upstream MoleculeACE CSVs",
    )
    args = parser.parse_args()
    cache_root = Path(args.upstream_cache)

    try:
        m287_path = PKG_ROOT / "object" / "CHEMBL287_Ki_manifest.json"
        sweep_path = PKG_ROOT / "object" / "moleculeace_30_sweep_manifest.json"
        pol_path = PKG_ROOT / "the-record-we-beat" / "polaris_moleculeace_30_audit.json"
        p287_file = Path(args.predictions) if args.predictions else (PKG_ROOT / "object" / "CHEMBL287_Ki_test_predictions.csv")

        for p in [m287_path, sweep_path, pol_path, p287_file]:
            assert p.exists(), f"Missing file {p}"

        res_csv_path = ensure_upstream_file(
            "MoleculeACE_results.csv",
            RESULTS_CSV_URL,
            RESULTS_CSV_SHA256,
            cache_root,
        )
        assert sha256_file(res_csv_path) == RESULTS_CSV_SHA256, "MoleculeACE_results.csv sha256 mismatch"

        m287 = json.loads(m287_path.read_text())
        sweep = json.loads(sweep_path.read_text())
        pol_list = json.loads(pol_path.read_text())
        pol_by_ds = {r["dataset"]: r for r in pol_list}
        assert len(sweep) == 30 and len(pol_by_ds) == 30, f"Expected 30 datasets in sweep, got {len(sweep)}"

        for r in pol_list:
            assert r.get("polaris_benchmark_url", "").startswith("https://polarishub.io/benchmarks/molecularml/"), f"Missing polaris_benchmark_url for {r['dataset']}"
            assert r.get("utc_fetched_at", "").endswith("Z"), f"Missing utc_fetched_at for {r['dataset']}"

        if args.predictions is None:
            assert sha256_file(p287_file) == m287["prediction_csv_sha256"] == "37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38", "Primary prediction sha256 mismatch"
            assert len(p287_file.read_bytes()) == m287["prediction_csv_bytes"] == 28516, "Primary prediction byte size mismatch"

        # 1. Verify Primary Headline Target (CHEMBL287_Ki) & every field of m287
        raw_287 = ensure_upstream_file(
            "benchmark_data/CHEMBL287_Ki.csv",
            f"{UPSTREAM_BASE}/benchmark_data/CHEMBL287_Ki.csv",
            m287["moleculeace_csv_sha256"],
            cache_root,
        )
        assert sha256_file(raw_287) == m287["moleculeace_csv_sha256"], "CHEMBL287_Ki.csv sha256 mismatch"
        df_raw_287 = pd.read_csv(raw_287)
        df_tr_287 = df_raw_287[df_raw_287["split"] == "train"].reset_index(drop=True)
        df_te_287 = df_raw_287[df_raw_287["split"] == "test"].reset_index(drop=True)
        df287 = pd.read_csv(p287_file)

        for forbidden_col in ("smiles", "cliff_mol", "y_true", "y"):
            assert forbidden_col not in df287.columns, f"df287 contains copied third-party column {forbidden_col}"

        expected_idx_287 = df_raw_287.index[df_raw_287["split"] == "test"].tolist()
        assert m287["test_csv_row_indices"] == expected_idx_287, "m287 test_csv_row_indices mismatch"
        assert df287["csv_row_index"].tolist() == expected_idx_287, "df287 csv_row_index mismatch"
        assert df287["test_row_index"].tolist() == list(range(len(df_te_287))), "df287 test_row_index mismatch"
        assert m287["n_train"] == m287["n_train_used"] == len(df_tr_287) == 1061, "m287 n_train mismatch"
        assert m287["n_test"] == len(df_te_287) == 267, "m287 n_test mismatch"
        assert m287["n_test_cliff"] == 103 and m287["n_test_noncliff"] == 164, "m287 cliff count mismatch"
        assert m287["stereo_stripped_inchikey14_overlap"] == 0 and m287["canonical_smiles_overlap"] == 0, "m287 overlap field mismatch"

        y287 = df_te_287["y"].to_numpy(dtype=np.float64)
        p287 = df287["y_pred_clss"].to_numpy(dtype=np.float64)
        s287 = df287["y_pred_svm_ecfp_baseline"].to_numpy(dtype=np.float64)
        c287 = df_te_287["cliff_mol"].to_numpy(dtype=np.int32) == 1

        # Also verify pre-test-scoring Stage 1, Stage 1+2, and Lens 1 predictions against m287["stage_progression_audit"]
        sp_audit = m287["stage_progression_audit"]
        for col_name, audit_key in [
            ("y_pred_lens1", "lens1_frozen_2026_10_19T115831Z_zero_prior_test_evals"),
            ("y_pred_stage1", "stage1_frozen_2026_10_19T121856Z_zero_prior_chembl287_test_evals"),
            ("y_pred_stage2", "stage1_plus_stage2_frozen_2026_10_19T121856Z_zero_prior_chembl287_test_evals"),
        ]:
            pred_stage = df287[col_name].to_numpy(dtype=np.float64)
            st_mse = float(mean_squared_error(y287, pred_stage))
            st_cmse = float(mean_squared_error(y287[c287], pred_stage[c287]))
            st_ncmse = float(mean_squared_error(y287[~c287], pred_stage[~c287]))
            st_b_svm, st_b_pol = paired_and_scalar_bootstrap(y287, pred_stage, s287, m287["polaris_listed_best_mse"], n_boot=10000, seed=0)
            info = sp_audit[audit_key]
            assert abs(round(st_mse, 8) - info["test_mse"]) < 1e-8, f"{col_name} test_mse mismatch"
            assert abs(round(st_cmse, 8) - info["test_cliff_mse"]) < 1e-8, f"{col_name} test_cliff_mse mismatch"
            assert abs(round(st_ncmse, 8) - info["test_noncliff_mse"]) < 1e-8, f"{col_name} test_noncliff_mse mismatch"
            assert abs(st_b_svm - info["paired_bootstrap_win_rate_vs_svm"]) < 1e-12, f"{col_name} paired bootstrap mismatch"
            assert abs(st_b_pol - info["scalar_bootstrap_win_rate_vs_polaris"]) < 1e-12, f"{col_name} scalar bootstrap mismatch"

        mse287 = float(mean_squared_error(y287, p287))
        mse287_cliff = float(mean_squared_error(y287[c287], p287[c287]))
        mse287_noncliff = float(mean_squared_error(y287[~c287], p287[~c287]))
        svm287 = float(mean_squared_error(y287, s287))
        svm287_cliff = float(mean_squared_error(y287[c287], s287[c287]))
        svm287_noncliff = float(mean_squared_error(y287[~c287], s287[~c287]))
        b_svm_287, b_pol_287 = paired_and_scalar_bootstrap(y287, p287, s287, m287["polaris_listed_best_mse"], n_boot=10000, seed=0)

        assert abs(mse287 - m287["clss_test_mse"]) < 1e-12, "m287 clss_test_mse mismatch"
        assert abs(np.sqrt(mse287) - m287["clss_test_rmse"]) < 1e-12, "m287 clss_test_rmse mismatch"
        assert abs(mse287_cliff - m287["clss_cliff_mse"]) < 1e-12, "m287 clss_cliff_mse mismatch"
        assert abs(np.sqrt(mse287_cliff) - m287["clss_cliff_rmse"]) < 1e-12, "m287 clss_cliff_rmse mismatch"
        assert abs(mse287_noncliff - m287["clss_noncliff_mse"]) < 1e-12, "m287 clss_noncliff_mse mismatch"
        assert abs(np.sqrt(mse287_noncliff) - m287["clss_noncliff_rmse"]) < 1e-12, "m287 clss_noncliff_rmse mismatch"
        assert abs(svm287 - m287["reproduced_svm_ecfp_mse"]) < 1e-12, "m287 reproduced_svm_ecfp_mse mismatch"
        assert abs(svm287_cliff - m287["reproduced_svm_ecfp_cliff_mse"]) < 1e-12, "m287 reproduced_svm_ecfp_cliff_mse mismatch"
        assert abs(svm287_noncliff - m287["reproduced_svm_ecfp_noncliff_mse"]) < 1e-12, "m287 reproduced_svm_ecfp_noncliff_mse mismatch"
        assert abs(b_svm_287 - m287["paired_bootstrap_10000_win_rate_vs_svm"]) < 1e-12, "m287 paired_bootstrap mismatch"
        assert abs(b_pol_287 - m287["scalar_bootstrap_10000_win_rate_vs_polaris"]) < 1e-12, "m287 scalar_bootstrap mismatch"

        assert mse287 < m287["polaris_listed_best_mse"] * 0.95, "Did not beat Polaris by >=5%"
        assert mse287 < m287["moleculeace_paper_best_mse"], "Did not beat MoleculeACE paper best"
        assert b_svm_287 >= 0.95 and b_pol_287 >= 0.95, "Bootstrap win rate below 95%"
        assert int(np.sum(c287)) >= 40 and mse287_cliff < m287["moleculeace_paper_best_cliff_mse"] and mse287_noncliff < svm287_noncliff, "Failed p2 cliff criterion"

        # 2. Verify All 30 Benchmarks (check all 30 prediction CSV SHA-256s upfront before RDKit molecular parsing)
        for r in sweep:
            ds = r["dataset"]
            pred_csv = PKG_ROOT / "object" / r["pred_csv_relpath"]
            assert pred_csv.exists(), f"Missing prediction CSV on {ds}: {pred_csv}"
            assert sha256_file(pred_csv) == r["pred_csv_sha256"], f"Prediction CSV sha256 mismatch on {ds}"

        wins_polaris = 0
        wins_5pct_boot95_paper = 0
        wins_paper = 0
        wins_cliff_paper = 0
        rmses, cliff_rmses, noncliff_rmses = [], [], []

        for r in sweep:
            ds = r["dataset"]
            pol_info = pol_by_ds[ds]
            assert r["csv_sha256"] == pol_info["csv_sha256"], f"CSV sha256 mismatch in manifests on {ds}"
            raw_csv = ensure_upstream_file(
                f"benchmark_data/{ds}.csv",
                pol_info.get("upstream_csv_url", f"{UPSTREAM_BASE}/benchmark_data/{ds}.csv"),
                r["csv_sha256"],
                cache_root,
            )
            pred_csv = PKG_ROOT / "object" / r["pred_csv_relpath"]

            assert sha256_file(raw_csv) == r["csv_sha256"] == pol_info["csv_sha256"], f"CSV sha256 mismatch on {ds}"
            assert sha256_file(pred_csv) == r["pred_csv_sha256"], f"Prediction CSV sha256 mismatch on {ds}"

            df_raw = pd.read_csv(raw_csv)
            df_tr = df_raw[df_raw["split"] == "train"].reset_index(drop=True)
            df_te = df_raw[df_raw["split"] == "test"].reset_index(drop=True)
            df_pred = pd.read_csv(pred_csv)

            assert len(df_tr) == pol_info["n_train"], f"Train count mismatch on {ds}"
            assert len(df_te) == pol_info["n_test"] == len(df_pred) == r["n_test"], f"Test count mismatch on {ds}"

            for forbidden_col in ("smiles", "cliff_mol", "y_true", "y"):
                assert forbidden_col not in df_pred.columns, f"df_pred on {ds} contains copied third-party column {forbidden_col}"

            expected_csv_idx = df_raw.index[df_raw["split"] == "test"].to_numpy(dtype=np.int32)
            assert np.array_equal(df_pred["csv_row_index"].to_numpy(dtype=np.int32), expected_csv_idx), f"Row index mismatch on {ds}"
            assert np.array_equal(df_pred["test_row_index"].to_numpy(dtype=np.int32), np.arange(len(df_te), dtype=np.int32)), f"test_row_index mismatch on {ds}"

            te_mols = [Chem.MolFromSmiles(s) for s in df_te["smiles"]]
            te_ik14 = {Chem.MolToInchiKey(m)[:14] for m in te_mols}
            te_can = {Chem.MolToSmiles(m, isomericSmiles=True) for m in te_mols}

            tr_mols_all = [Chem.MolFromSmiles(s) for s in df_tr["smiles"]]
            tr_used_mols = [m for m in tr_mols_all if Chem.MolToInchiKey(m)[:14] not in te_ik14]
            assert len(tr_used_mols) == r["n_train_used"], f"n_train_used mismatch on {ds}"
            tr_used_ik14 = {Chem.MolToInchiKey(m)[:14] for m in tr_used_mols}
            tr_used_can = {Chem.MolToSmiles(m, isomericSmiles=True) for m in tr_used_mols}
            assert len(tr_used_ik14 & te_ik14) == 0, f"InChIKey[:14] overlap on {ds}"
            assert len(tr_used_can & te_can) == 0, f"Canonical SMILES overlap on {ds}"

            y_true = df_te["y"].to_numpy(dtype=np.float64)
            y_clss = df_pred["y_pred_clss"].to_numpy(dtype=np.float64)
            y_svm = df_pred["y_pred_svm_ecfp_baseline"].to_numpy(dtype=np.float64)
            cliff = df_te["cliff_mol"].to_numpy(dtype=np.int32) == 1

            mse_all = float(mean_squared_error(y_true, y_clss))
            mse_cliff = float(mean_squared_error(y_true[cliff], y_clss[cliff]))
            mse_noncliff = float(mean_squared_error(y_true[~cliff], y_clss[~cliff]))
            assert abs(mse_all - r["clss_mse"]) < 1e-12, f"MSE mismatch on {ds}"
            assert abs(mse_cliff - r["clss_cliff_mse"]) < 1e-12, f"Cliff MSE mismatch on {ds}"
            assert abs(mse_noncliff - r["clss_noncliff_mse"]) < 1e-12, f"Non-cliff MSE mismatch on {ds}"

            b_svm, b_pol = paired_and_scalar_bootstrap(y_true, y_clss, y_svm, r["polaris_best_mse"], n_boot=10000, seed=0)
            assert abs(b_svm - r["boot_win_rate_vs_svm"]) < 1e-12, f"Paired bootstrap mismatch on {ds}"
            assert abs(b_pol - r["boot_win_rate_vs_polaris_val"]) < 1e-12, f"Scalar bootstrap mismatch on {ds}"

            rel_pol = 100.0 * (r["polaris_best_mse"] - mse_all) / r["polaris_best_mse"]
            if mse_all < r["polaris_best_mse"]:
                wins_polaris += 1
            if rel_pol >= 5.0 and b_svm >= 0.95 and mse_all < r["paper_best_mse"]:
                wins_5pct_boot95_paper += 1
            if mse_all < r["paper_best_mse"]:
                wins_paper += 1
            if mse_cliff < r["paper_best_cliff_mse"]:
                wins_cliff_paper += 1

            rmses.append(np.sqrt(mse_all))
            cliff_rmses.append(np.sqrt(mse_cliff))
            noncliff_rmses.append(np.sqrt(mse_noncliff))

        assert wins_polaris == 29 and wins_5pct_boot95_paper == 21 and wins_paper == 28 and wins_cliff_paper == 21, "Sweep win counts mismatch"

        # 3. 400 Permutation Null Controls on CHEMBL287_Ki
        rng_null = np.random.default_rng(42)
        null_mses = [float(mean_squared_error(rng_null.permutation(y287), p287)) for _ in range(400)]
        z_score = (mse287 - float(np.mean(null_mses))) / float(np.std(null_mses))
        assert mse287 < float(np.min(null_mses)), "Failed 400-permutation null control"

        print(
            f"Verified polaris-moleculeace-activity-cliff-mse: "
            f"CHEMBL287_Ki MSE={mse287:.8f} (-{m287['relative_improvement_vs_polaris_pct']:.2f}% vs Polaris {m287['polaris_listed_best_mse']:.8f}, "
            f"-{m287['relative_improvement_vs_paper_pct']:.2f}% vs Paper {m287['moleculeace_paper_best_mse']:.8f}, "
            f"boot_paired={b_svm_287*100:.2f}%, boot_scalar={b_pol_287*100:.2f}%, "
            f"cliff_MSE={mse287_cliff:.8f} -{m287['relative_improvement_cliff_vs_paper_pct']:.2f}%, "
            f"null_400_z={z_score:.2f}); 30-target sweep: {wins_polaris}/30 Polaris wins, "
            f"{wins_5pct_boot95_paper}/30 full-gate wins, macro_cliff_RMSE={np.mean(cliff_rmses):.4f}"
        )
        print("PASS")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
