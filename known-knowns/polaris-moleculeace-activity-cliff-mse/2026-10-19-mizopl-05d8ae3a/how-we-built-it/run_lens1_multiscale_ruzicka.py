#!/usr/bin/env python3
"""
Lens 1 Step 2: Multi-Scale Chiral & Achiral Ruzicka (MinMax) + Tanimoto Kernel Ensemble.
Evaluates a single fixed multi-scale kernel & tree ensemble (all weights fit via 5-fold OOF CV on train only,
with strict stereo-stripped InChIKey[:14] train/test disjointness enforced) across all 30 MoleculeACE datasets.
"""
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.linalg import solve
from scipy.optimize import nnls
from scipy.spatial.distance import cdist
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, MACCSkeys, Descriptors, rdMolDescriptors

RDLogger.DisableLog('rdApp.*')

RUN_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = RUN_ROOT / "data" / "benchmark_data"
AUDIT_JSON = RUN_ROOT / "polaris_moleculeace_30_audit.json"
BASELINE_JSON = Path(__file__).resolve().parent / "baseline_and_inchikey_audit.json"
OUT_DIR = Path(__file__).resolve().parent


def hashed_int_fp_to_array(fp, n_bits: int) -> np.ndarray:
    arr = np.zeros((n_bits,), dtype=np.float32)
    for k, v in fp.GetNonzeroElements().items():
        arr[k % n_bits] += float(v)
    return arr


def bitvect_to_array(bv, n_bits: int) -> np.ndarray:
    arr = np.zeros((n_bits,), dtype=np.float32)
    Chem.DataStructs.ConvertToNumpyArray(bv, arr)
    return arr


def extract_molecule_views(smiles_list):
    """
    Extract multi-scale chiral and achiral structural views from SMILES strings.
    Returns dict of feature matrices (N, D_view).
    """
    n = len(smiles_list)
    mc_chiral_r1 = np.zeros((n, 2048), dtype=np.float32)
    mc_chiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    mc_chiral_r3 = np.zeros((n, 2048), dtype=np.float32)
    mc_achiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    fcfp_chiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    fcfp_chiral_r3 = np.zeros((n, 2048), dtype=np.float32)
    ap_chiral = np.zeros((n, 2048), dtype=np.float32)
    tt_chiral = np.zeros((n, 2048), dtype=np.float32)
    rdk_bits = np.zeros((n, 2048), dtype=np.float32)
    maccs_bits = np.zeros((n, 167), dtype=np.float32)
    physchem = np.zeros((n, 24), dtype=np.float32)

    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        mc_chiral_r1[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 1, nBits=2048, useChirality=True), 2048
        )
        mc_chiral_r2[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 2, nBits=2048, useChirality=True), 2048
        )
        mc_chiral_r3[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 3, nBits=2048, useChirality=True), 2048
        )
        mc_achiral_r2[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 2, nBits=2048, useChirality=False), 2048
        )
        fcfp_chiral_r2[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 2, nBits=2048, useChirality=True, useFeatures=True), 2048
        )
        fcfp_chiral_r3[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 3, nBits=2048, useChirality=True, useFeatures=True), 2048
        )
        ap_chiral[i] = hashed_int_fp_to_array(
            rdMolDescriptors.GetHashedAtomPairFingerprint(mol, nBits=2048, includeChirality=True), 2048
        )
        tt_chiral[i] = hashed_int_fp_to_array(
            rdMolDescriptors.GetHashedTopologicalTorsionFingerprint(mol, nBits=2048, includeChirality=True), 2048
        )
        rdk_bits[i] = bitvect_to_array(Chem.RDKFingerprint(mol, minPath=1, maxPath=7, fpSize=2048), 2048)
        maccs_bits[i] = bitvect_to_array(MACCSkeys.GenMACCSKeys(mol), 167)

        # Stereochemical + 2D physicochemical descriptors
        chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
        n_chiral = len(chiral_centers)
        n_R = sum(1 for _, lab in chiral_centers if lab == 'R')
        n_S = sum(1 for _, lab in chiral_centers if lab == 'S')
        n_EZ = sum(
            1 for b in mol.GetBonds()
            if b.GetStereo() in (Chem.BondStereo.STEREOE, Chem.BondStereo.STEREOZ,
                                 Chem.BondStereo.STEREOCIS, Chem.BondStereo.STEREOTRANS)
        )
        physchem[i] = [
            Descriptors.MolWt(mol) / 500.0,
            Descriptors.MolLogP(mol),
            Descriptors.MolMR(mol) / 100.0,
            Descriptors.TPSA(mol) / 100.0,
            Descriptors.NumHDonors(mol),
            Descriptors.NumHAcceptors(mol),
            Descriptors.NumRotatableBonds(mol),
            Descriptors.RingCount(mol),
            Descriptors.NumAromaticRings(mol),
            Descriptors.NumAliphaticRings(mol),
            Descriptors.FractionCSP3(mol),
            Descriptors.HeavyAtomCount(mol) / 30.0,
            Descriptors.NumHeteroatoms(mol) / 10.0,
            Descriptors.LabuteASA(mol) / 200.0,
            Descriptors.BalabanJ(mol),
            np.log1p(max(0.0, Descriptors.BertzCT(mol))),
            Descriptors.HallKierAlpha(mol),
            Descriptors.Chi0v(mol) / 20.0,
            Descriptors.Chi1v(mol) / 10.0,
            Descriptors.Kappa1(mol) / 20.0,
            Descriptors.Kappa2(mol) / 10.0,
            float(n_chiral),
            float(n_R - n_S),
            float(n_EZ),
        ]
    physchem = np.nan_to_num(physchem, nan=0.0, posinf=0.0, neginf=0.0)

    mc_chiral_multi = np.hstack([mc_chiral_r1, mc_chiral_r2, 0.85 * mc_chiral_r3])
    fcfp_multi = np.hstack([fcfp_chiral_r2, 0.85 * fcfp_chiral_r3])
    ap_tt = np.hstack([ap_chiral, tt_chiral])

    return {
        "mc_chiral_multi_sqrt": np.sqrt(mc_chiral_multi),
        "mc_chiral_multi_log": np.log1p(mc_chiral_multi),
        "mc_chiral_r2_raw": mc_chiral_r2,
        "mc_achiral_r2_sqrt": np.sqrt(mc_achiral_r2),
        "fcfp_multi_sqrt": np.sqrt(fcfp_multi),
        "ap_tt_sqrt": np.sqrt(ap_tt),
        "rdk_maccs_bits": np.hstack([rdk_bits, maccs_bits]),
        "physchem": physchem,
    }


def ruzicka_similarity(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Fast BLAS Generalized Ruzicka / Tanimoto similarity matrix in float32 SGEMM."""
    A32 = np.ascontiguousarray(A, dtype=np.float32)
    B32 = np.ascontiguousarray(B, dtype=np.float32)
    dot = (A32 @ B32.T).astype(np.float64)
    na = np.sum(A32 * A32, axis=1, keepdims=True, dtype=np.float64)
    nb = np.sum(B32 * B32, axis=1, keepdims=True, dtype=np.float64).T
    denom = na + nb - dot
    sim = np.where(denom > 1e-12, dot / np.maximum(denom, 1e-12), 1.0)
    return np.clip(sim, 0.0, 1.0)


def compute_view_similarities(views_A, views_B, scaler_phys=None, fit_scaler=False):
    sims = {}
    for k in [
        "mc_chiral_multi_sqrt",
        "mc_chiral_multi_log",
        "mc_chiral_r2_raw",
        "mc_achiral_r2_sqrt",
        "fcfp_multi_sqrt",
        "ap_tt_sqrt",
        "rdk_maccs_bits",
    ]:
        sims[k] = ruzicka_similarity(views_A[k], views_B[k])

    if fit_scaler:
        scaler_phys = StandardScaler().fit(views_A["physchem"])
    Z_A = scaler_phys.transform(views_A["physchem"])
    Z_B = scaler_phys.transform(views_B["physchem"])
    d_l1 = cdist(Z_A, Z_B, metric="cityblock") / Z_A.shape[1]
    d_l2 = cdist(Z_A, Z_B, metric="sqeuclidean") / Z_A.shape[1]
    sims["phys_lap"] = np.exp(-0.8 * d_l1)
    sims["phys_rbf"] = np.exp(-0.5 * d_l2)
    return sims, scaler_phys


def build_kernel_bank(sims_dict):
    """
    Build a bank of positive-definite Mercer kernels from the multi-view Ruzicka/Tanimoto similarity matrices.
    """
    S_c1 = sims_dict["mc_chiral_multi_sqrt"]
    S_c2 = sims_dict["mc_chiral_multi_log"]
    S_cr2 = sims_dict["mc_chiral_r2_raw"]
    S_ac = sims_dict["mc_achiral_r2_sqrt"]
    S_fc = sims_dict["fcfp_multi_sqrt"]
    S_ap = sims_dict["ap_tt_sqrt"]
    S_rdk = sims_dict["rdk_maccs_bits"]
    S_pl = sims_dict["phys_lap"]
    S_pr = sims_dict["phys_rbf"]

    # Composite multi-scale similarity (convex combination of Mercer kernels)
    S_comp = (
        0.28 * S_c1
        + 0.16 * S_c2
        + 0.12 * S_cr2
        + 0.10 * S_ac
        + 0.14 * S_fc
        + 0.10 * S_ap
        + 0.06 * S_rdk
        + 0.04 * S_pl
    )
    S_chiral_focus = 0.45 * S_c1 + 0.25 * S_fc + 0.20 * S_ap + 0.10 * S_rdk

    kernels = {}
    # Sharp exponential-on-Ruzicka kernels (ideal for activity cliffs)
    for gamma in [1.5, 3.0, 5.0, 8.0]:
        kernels[f"comp_exp_g{gamma}"] = np.exp(-gamma * (1.0 - S_comp)) * S_comp
        kernels[f"chiral_exp_g{gamma}"] = np.exp(-gamma * (1.0 - S_chiral_focus)) * S_chiral_focus

    # Individual view exponential kernels
    for name, S in [
        ("mc_sqrt", S_c1),
        ("mc_log", S_c2),
        ("mc_raw", S_cr2),
        ("achiral", S_ac),
        ("fcfp", S_fc),
        ("ap_tt", S_ap),
        ("rdk", S_rdk),
    ]:
        kernels[f"{name}_exp3"] = np.exp(-3.0 * (1.0 - S)) * S
        kernels[f"{name}_pow2"] = S ** 2

    kernels["phys_lap"] = S_pl
    kernels["phys_rbf"] = S_pr
    kernels["S_comp_raw"] = S_comp
    return kernels


def solve_krr(K_tr, y_tr, K_eval, alpha):
    n = K_tr.shape[0]
    y_mean = float(np.mean(y_tr))
    A = K_tr + alpha * np.eye(n, dtype=np.float64)
    w = solve(A, y_tr - y_mean, assume_a="pos")
    return y_mean + K_eval.T @ w


def fit_predict_multiscale_ruzicka(views_tr, y_tr, views_te, seed=42):
    """
    Fit Multi-Scale Ruzicka Kernel Ridge + SVR ensemble strictly using 5-fold Stratified OOF on train.
    Zero test-set access during training or weighting.
    """
    n_tr = len(y_tr)
    n_te = views_te["physchem"].shape[0]

    # 5-fold stratified split on y_tr deciles/quartiles
    n_bins = min(10, max(2, n_tr // 40))
    bins = pd.qcut(y_tr, q=n_bins, labels=False, duplicates="drop")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    folds = list(skf.split(np.zeros(n_tr), bins))

    # Precompute full train-train and train-test raw fingerprint similarities (physchem scaled inside folds!)
    raw_keys = [
        "mc_chiral_multi_sqrt",
        "mc_chiral_multi_log",
        "mc_chiral_r2_raw",
        "mc_achiral_r2_sqrt",
        "fcfp_multi_sqrt",
        "ap_tt_sqrt",
        "rdk_maccs_bits",
    ]
    raw_sims_tr = {k: ruzicka_similarity(views_tr[k], views_tr[k]) for k in raw_keys}
    raw_sims_te = {k: ruzicka_similarity(views_tr[k], views_te[k]) for k in raw_keys}

    # Define candidate base models: (kernel_name, model_type, param)
    krr_Specs = [
        ("comp_exp_g1.5", 0.03),
        ("comp_exp_g1.5", 0.10),
        ("comp_exp_g3.0", 0.02),
        ("comp_exp_g3.0", 0.06),
        ("comp_exp_g3.0", 0.18),
        ("comp_exp_g5.0", 0.03),
        ("comp_exp_g5.0", 0.10),
        ("comp_exp_g8.0", 0.05),
        ("chiral_exp_g3.0", 0.03),
        ("chiral_exp_g3.0", 0.10),
        ("chiral_exp_g5.0", 0.05),
        ("mc_sqrt_exp3", 0.04),
        ("mc_sqrt_exp3", 0.12),
        ("mc_log_exp3", 0.05),
        ("mc_raw_exp3", 0.05),
        ("achiral_exp3", 0.05),
        ("fcfp_exp3", 0.05),
        ("fcfp_exp3", 0.15),
        ("ap_tt_exp3", 0.05),
        ("ap_tt_exp3", 0.15),
        ("rdk_exp3", 0.08),
        ("mc_sqrt_pow2", 0.05),
        ("fcfp_pow2", 0.08),
        ("phys_lap", 0.10),
        ("phys_rbf", 0.15),
    ]
    svr_Specs = [
        ("comp_exp_g3.0", 3.0, 0.05),
        ("comp_exp_g5.0", 5.0, 0.03),
        ("chiral_exp_g3.0", 3.0, 0.05),
        ("mc_sqrt_exp3", 3.0, 0.05),
        ("fcfp_exp3", 3.0, 0.05),
        ("ap_tt_exp3", 3.0, 0.05),
    ]

    n_models = len(krr_Specs) + len(svr_Specs)
    oof_preds = np.zeros((n_tr, n_models), dtype=np.float64)

    for tr_idx, val_idx in folds:
        sims_fold_tr = {k: raw_sims_tr[k][np.ix_(tr_idx, tr_idx)] for k in raw_keys}
        sims_fold_val = {k: raw_sims_tr[k][np.ix_(tr_idx, val_idx)] for k in raw_keys}

        scaler_f = StandardScaler().fit(views_tr["physchem"][tr_idx])
        Z_tr = scaler_f.transform(views_tr["physchem"][tr_idx])
        Z_val = scaler_f.transform(views_tr["physchem"][val_idx])
        d_l1_tr = cdist(Z_tr, Z_tr, metric="cityblock") / Z_tr.shape[1]
        d_l2_tr = cdist(Z_tr, Z_tr, metric="sqeuclidean") / Z_tr.shape[1]
        d_l1_val = cdist(Z_tr, Z_val, metric="cityblock") / Z_tr.shape[1]
        d_l2_val = cdist(Z_tr, Z_val, metric="sqeuclidean") / Z_tr.shape[1]

        sims_fold_tr["phys_lap"] = np.exp(-0.8 * d_l1_tr)
        sims_fold_tr["phys_rbf"] = np.exp(-0.5 * d_l2_tr)
        sims_fold_val["phys_lap"] = np.exp(-0.8 * d_l1_val)
        sims_fold_val["phys_rbf"] = np.exp(-0.5 * d_l2_val)

        kb_tr = build_kernel_bank(sims_fold_tr)
        kb_val = build_kernel_bank(sims_fold_val)
        y_f_tr = y_tr[tr_idx]

        m_idx = 0
        for k_name, alpha in krr_Specs:
            oof_preds[val_idx, m_idx] = solve_krr(kb_tr[k_name], y_f_tr, kb_val[k_name], alpha)
            m_idx += 1

        for k_name, C_val, eps_val in svr_Specs:
            svr = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
            svr.fit(kb_tr[k_name], y_f_tr)
            oof_preds[val_idx, m_idx] = svr.predict(kb_val[k_name].T)
            m_idx += 1

    # Fit non-negative Ridge-regularized stacking weights strictly on OOF predictions
    # Minimize ||oof_preds @ w - y_tr||^2 + lambda_w ||w - 1/M||^2 subject to w >= 0
    reg_lambda = 0.05 * np.var(y_tr) * np.sqrt(n_tr)
    A_stack = np.vstack([oof_preds, np.sqrt(reg_lambda) * np.eye(n_models)])
    b_stack = np.concatenate([y_tr, np.full(n_models, np.sqrt(reg_lambda) / n_models)])
    weights, _ = nnls(A_stack, b_stack)
    if np.sum(weights) > 0:
        weights = weights / np.sum(weights)
    else:
        weights = np.ones(n_models) / n_models

    oof_ens = oof_preds @ weights
    oof_mse = float(np.mean((y_tr - oof_ens) ** 2))

    # Fit full models on all train data and predict test
    sims_full_tr = dict(raw_sims_tr)
    sims_full_te = dict(raw_sims_te)
    scaler_full = StandardScaler().fit(views_tr["physchem"])
    Z_full_tr = scaler_full.transform(views_tr["physchem"])
    Z_full_te = scaler_full.transform(views_te["physchem"])
    sims_full_tr["phys_lap"] = np.exp(-0.8 * cdist(Z_full_tr, Z_full_tr, metric="cityblock") / Z_full_tr.shape[1])
    sims_full_tr["phys_rbf"] = np.exp(-0.5 * cdist(Z_full_tr, Z_full_tr, metric="sqeuclidean") / Z_full_tr.shape[1])
    sims_full_te["phys_lap"] = np.exp(-0.8 * cdist(Z_full_tr, Z_full_te, metric="cityblock") / Z_full_tr.shape[1])
    sims_full_te["phys_rbf"] = np.exp(-0.5 * cdist(Z_full_tr, Z_full_te, metric="sqeuclidean") / Z_full_tr.shape[1])

    kb_full_tr = build_kernel_bank(sims_full_tr)
    kb_full_te = build_kernel_bank(sims_full_te)

    te_preds = np.zeros((n_te, n_models), dtype=np.float64)
    m_idx = 0
    for k_name, alpha in krr_Specs:
        te_preds[:, m_idx] = solve_krr(kb_full_tr[k_name], y_tr, kb_full_te[k_name], alpha)
        m_idx += 1

    for k_name, C_val, eps_val in svr_Specs:
        svr = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
        svr.fit(kb_full_tr[k_name], y_tr)
        te_preds[:, m_idx] = svr.predict(kb_full_te[k_name].T)
        m_idx += 1

    pred_te = te_preds @ weights
    return pred_te, oof_ens, oof_mse, oof_preds, te_preds, kb_full_tr, kb_full_te, raw_sims_tr, raw_sims_te


def main():
    t0 = time.time()
    baseline_rows = json.loads(BASELINE_JSON.read_text())
    base_by_ds = {r["dataset"]: r for r in baseline_rows}

    lens1_results = []
    wins_polaris = 0
    wins_polaris_5pct = 0
    wins_paper = 0
    wins_cliff = 0

    for ds_name in sorted(base_by_ds.keys()):
        b_info = base_by_ds[ds_name]
        df = pd.read_csv(DATA_DIR / f"{ds_name}.csv")
        tr_df = df[df["split"] == "train"].reset_index(drop=True)
        te_df = df[df["split"] == "test"].reset_index(drop=True)

        # Enforce strict stereo-stripped InChIKey[:14] disjointness against test
        te_ik14 = {Chem.MolToInchiKey(Chem.MolFromSmiles(s))[:14] for s in te_df["smiles"]}
        keep_mask = [Chem.MolToInchiKey(Chem.MolFromSmiles(s))[:14] not in te_ik14 for s in tr_df["smiles"]]
        tr_clean_df = tr_df[keep_mask].reset_index(drop=True)

        views_tr = extract_molecule_views(tr_clean_df["smiles"].tolist())
        views_te = extract_molecule_views(te_df["smiles"].tolist())
        y_tr = tr_clean_df["y"].to_numpy(dtype=np.float64)
        y_te = te_df["y"].to_numpy(dtype=np.float64)
        cliff_te = te_df["cliff_mol"].to_numpy(dtype=np.int32) == 1

        pred_te, oof_ens, oof_mse, _, _, _, _, _, _ = fit_predict_multiscale_ruzicka(views_tr, y_tr, views_te)

        mse_te = float(np.mean((y_te - pred_te) ** 2))
        mse_cliff = float(np.mean((y_te[cliff_te] - pred_te[cliff_te]) ** 2))
        mse_noncliff = float(np.mean((y_te[~cliff_te] - pred_te[~cliff_te]) ** 2))

        pol_mse = b_info["polaris_best_mse"]
        pap_mse = b_info["paper_best_mse"]
        pap_cliff_mse = b_info["paper_best_cliff_mse"]
        rel_pol = 100.0 * (pol_mse - mse_te) / pol_mse
        rel_pap = 100.0 * (pap_mse - mse_te) / pap_mse
        rel_cliff = 100.0 * (pap_cliff_mse - mse_cliff) / pap_cliff_mse

        if mse_te < pol_mse:
            wins_polaris += 1
        if rel_pol >= 5.0:
            wins_polaris_5pct += 1
        if mse_te < pap_mse:
            wins_paper += 1
        if mse_cliff < pap_cliff_mse:
            wins_cliff += 1

        row = {
            "dataset": ds_name,
            "slug": b_info["slug"],
            "n_train_used": len(tr_clean_df),
            "n_test": len(te_df),
            "n_test_cliff": int(np.sum(cliff_te)),
            "oof_mse": oof_mse,
            "lens1_mse": mse_te,
            "lens1_rmse": float(np.sqrt(mse_te)),
            "lens1_cliff_mse": mse_cliff,
            "lens1_cliff_rmse": float(np.sqrt(mse_cliff)),
            "lens1_noncliff_mse": mse_noncliff,
            "lens1_noncliff_rmse": float(np.sqrt(mse_noncliff)),
            "polaris_best_mse": pol_mse,
            "paper_best_mse": pap_mse,
            "paper_best_cliff_mse": pap_cliff_mse,
            "rel_impr_vs_polaris_pct": rel_pol,
            "rel_impr_vs_paper_pct": rel_pap,
            "rel_impr_cliff_vs_paper_pct": rel_cliff,
        }
        lens1_results.append(row)
        print(
            f"{ds_name:16s} | Pol={pol_mse:.4f} Pap={pap_mse:.4f} -> L1={mse_te:.4f} ({rel_pol:+6.2f}% vs Pol) "
            f"| Cliff: Pap={pap_cliff_mse:.4f} -> L1={mse_cliff:.4f} ({rel_cliff:+6.2f}%)"
        )

    macro_rmse = float(np.mean([r["lens1_rmse"] for r in lens1_results]))
    macro_cliff_rmse = float(np.mean([r["lens1_cliff_rmse"] for r in lens1_results]))
    macro_noncliff_rmse = float(np.mean([r["lens1_noncliff_rmse"] for r in lens1_results]))
    print("-" * 100)
    print(f"LENS 1 SUMMARY ({time.time() - t0:.1f}s):")
    print(f"  Wins vs Polaris Best MSE:       {wins_polaris}/30 (>=5% rel margin: {wins_polaris_5pct}/30)")
    print(f"  Wins vs Paper Best MSE:         {wins_paper}/30")
    print(f"  Wins vs Paper Best Cliff MSE:   {wins_cliff}/30")
    print(f"  Macro-Average RMSE:             {macro_rmse:.4f} (Monroe 2026: 0.629, GraphCliff: 0.665, SVM: 0.671)")
    print(f"  Macro-Average Cliff RMSE:       {macro_cliff_rmse:.4f} (Monroe 2026: 0.737, SVM: 0.751, GraphCliff: 0.757)")
    print(f"  Macro-Average Non-Cliff RMSE:   {macro_noncliff_rmse:.4f}")

    out_path = OUT_DIR / "lens1_multiscale_ruzicka_results.json"
    out_path.write_text(json.dumps(lens1_results, indent=2))


if __name__ == "__main__":
    main()
