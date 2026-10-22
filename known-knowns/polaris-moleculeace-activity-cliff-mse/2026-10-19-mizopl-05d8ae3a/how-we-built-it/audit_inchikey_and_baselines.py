#!/usr/bin/env python3
"""
Lens 1 Step 1: Audit all 30 MoleculeACE datasets for:
1. Exact CSV sha256, train/test/cliff counts matching Polaris API.
2. Canonical SMILES, full InChIKey, and stereo-stripped InChIKey[:14] overlap between train and test.
3. Faithful reproduction of the MoleculeACE paper classical baselines (SVM_ECFP, RF_ECFP, GBM_ECFP, KNN_ECFP)
   using the official benchmark YAML configs in data/configures/benchmark/<dataset>/.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, MACCSkeys
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor

RDLogger.DisableLog('rdApp.*')

RUN_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = RUN_ROOT / "data" / "benchmark_data"
CONFIG_DIR = RUN_ROOT / "data" / "configures" / "benchmark"
RESULTS_CSV = RUN_ROOT / "data" / "results" / "MoleculeACE_results.csv"
AUDIT_JSON = RUN_ROOT / "polaris_moleculeace_30_audit.json"
OUT_DIR = Path(__file__).resolve().parent


def ecfp_1024_achiral(smiles_list):
    fps = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        bv = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
        arr = np.zeros((1024,), dtype=np.float32)
        Chem.DataStructs.ConvertToNumpyArray(bv, arr)
        fps.append(arr)
    return np.asarray(fps, dtype=np.float32)


def main():
    polaris_audit = json.loads(AUDIT_JSON.read_text())
    polaris_by_ds = {row["dataset"]: row for row in polaris_audit}

    summary_rows = []
    for ds_name in sorted(polaris_by_ds.keys()):
        csv_path = DATA_DIR / f"{ds_name}.csv"
        sha256 = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        df = pd.read_csv(csv_path)
        tr_df = df[df["split"] == "train"].reset_index(drop=True)
        te_df = df[df["split"] == "test"].reset_index(drop=True)

        tr_mols = [Chem.MolFromSmiles(s) for s in tr_df["smiles"]]
        te_mols = [Chem.MolFromSmiles(s) for s in te_df["smiles"]]

        tr_can = {Chem.MolToSmiles(m, isomericSmiles=True) for m in tr_mols}
        te_can = {Chem.MolToSmiles(m, isomericSmiles=True) for m in te_mols}
        tr_ik_full = {Chem.MolToInchiKey(m) for m in tr_mols}
        te_ik_full = {Chem.MolToInchiKey(m) for m in te_mols}
        tr_ik14 = [Chem.MolToInchiKey(m)[:14] for m in tr_mols]
        te_ik14_set = {Chem.MolToInchiKey(m)[:14] for m in te_mols}

        overlap_can = len(tr_can & te_can)
        overlap_ik_full = len(tr_ik_full & te_ik_full)
        overlap_ik14_rows = sum(1 for ik in tr_ik14 if ik in te_ik14_set)

        # Reproduce SVM_ECFP, RF_ECFP, GBM_ECFP, KNN_ECFP using official YAML configs
        X_tr = ecfp_1024_achiral(tr_df["smiles"].tolist())
        X_te = ecfp_1024_achiral(te_df["smiles"].tolist())
        y_tr = tr_df["y"].to_numpy(dtype=np.float64)
        y_te = te_df["y"].to_numpy(dtype=np.float64)
        cliff_te = te_df["cliff_mol"].to_numpy(dtype=np.int32) == 1

        # SVM_ECFP
        svm_cfg = yaml.safe_load((CONFIG_DIR / ds_name / "SVM_ECFP.yml").read_text())
        svm = SVR(**svm_cfg)
        svm.fit(X_tr, y_tr)
        pred_svm = svm.predict(X_te)
        mse_svm = float(np.mean((y_te - pred_svm) ** 2))
        mse_svm_cliff = float(np.mean((y_te[cliff_te] - pred_svm[cliff_te]) ** 2))

        # Also fit SVM_ECFP on ik14-clean train set (if any overlap_ik14_rows > 0)
        clean_mask = np.array([ik not in te_ik14_set for ik in tr_ik14], dtype=bool)
        svm_clean = SVR(**svm_cfg)
        svm_clean.fit(X_tr[clean_mask], y_tr[clean_mask])
        pred_svm_clean = svm_clean.predict(X_te)
        mse_svm_clean = float(np.mean((y_te - pred_svm_clean) ** 2))
        mse_svm_clean_cliff = float(np.mean((y_te[cliff_te] - pred_svm_clean[cliff_te]) ** 2))

        # RF_ECFP
        rf_cfg = yaml.safe_load((CONFIG_DIR / ds_name / "RF_ECFP.yml").read_text())
        rf = RandomForestRegressor(random_state=42, n_jobs=-1, **rf_cfg)
        rf.fit(X_tr, y_tr)
        pred_rf = rf.predict(X_te)
        mse_rf = float(np.mean((y_te - pred_rf) ** 2))
        mse_rf_cliff = float(np.mean((y_te[cliff_te] - pred_rf[cliff_te]) ** 2))

        # GBM_ECFP
        gbm_cfg = yaml.safe_load((CONFIG_DIR / ds_name / "GBM_ECFP.yml").read_text())
        gbm = GradientBoostingRegressor(random_state=42, **gbm_cfg)
        gbm.fit(X_tr, y_tr)
        pred_gbm = gbm.predict(X_te)
        mse_gbm = float(np.mean((y_te - pred_gbm) ** 2))
        mse_gbm_cliff = float(np.mean((y_te[cliff_te] - pred_gbm[cliff_te]) ** 2))

        # KNN_ECFP
        knn_cfg = yaml.safe_load((CONFIG_DIR / ds_name / "KNN_ECFP.yml").read_text())
        knn = KNeighborsRegressor(**knn_cfg)
        knn.fit(X_tr, y_tr)
        pred_knn = knn.predict(X_te)
        mse_knn = float(np.mean((y_te - pred_knn) ** 2))
        mse_knn_cliff = float(np.mean((y_te[cliff_te] - pred_knn[cliff_te]) ** 2))

        p_info = polaris_by_ds[ds_name]
        row = {
            "dataset": ds_name,
            "slug": p_info["slug"],
            "csv_sha256": sha256,
            "n_train": len(tr_df),
            "n_train_clean_ik14": int(np.sum(clean_mask)),
            "n_test": len(te_df),
            "n_test_cliff": int(np.sum(cliff_te)),
            "overlap_can_smiles": overlap_can,
            "overlap_full_inchikey": overlap_ik_full,
            "overlap_ik14_train_rows": overlap_ik14_rows,
            "polaris_best_mse": p_info["best_lb_mse"],
            "paper_best_mse": p_info["paper_best_mse"],
            "paper_best_cliff_mse": p_info["paper_best_cliff_mse"],
            "repro_svm_ecfp_mse": mse_svm,
            "repro_svm_ecfp_cliff_mse": mse_svm_cliff,
            "repro_svm_clean_mse": mse_svm_clean,
            "repro_svm_clean_cliff_mse": mse_svm_clean_cliff,
            "repro_rf_ecfp_mse": mse_rf,
            "repro_rf_ecfp_cliff_mse": mse_rf_cliff,
            "repro_gbm_ecfp_mse": mse_gbm,
            "repro_gbm_ecfp_cliff_mse": mse_gbm_cliff,
            "repro_knn_ecfp_mse": mse_knn,
            "repro_knn_ecfp_cliff_mse": mse_knn_cliff,
            "repro_best_classical_mse": min(mse_svm, mse_rf, mse_gbm, mse_knn),
            "repro_best_classical_cliff_mse": min(mse_svm_cliff, mse_rf_cliff, mse_gbm_cliff, mse_knn_cliff),
        }
        summary_rows.append(row)
        print(
            f"{ds_name:18s} | n_tr={len(tr_df):4d} (clean={int(np.sum(clean_mask)):4d}) n_te={len(te_df):3d} (cliff={int(np.sum(cliff_te)):3d}) "
            f"| ik14_ov={overlap_ik14_rows:2d} | PolMSE={p_info['best_lb_mse']:.4f} | SVM={mse_svm:.4f} (cliff={mse_svm_cliff:.4f})"
        )

    out_json = OUT_DIR / "baseline_and_inchikey_audit.json"
    out_json.write_text(json.dumps(summary_rows, indent=2))
    print(f"\nSaved 30-dataset audit to {out_json.name}")


if __name__ == "__main__":
    main()
