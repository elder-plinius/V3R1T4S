#!/usr/bin/env python3
"""
Lens 2: Fast BLAS Multi-Scale Chiral/Achiral Tanimoto + Thermometer-Ruzicka + ErG Pharmacophore +
215-Descriptor RankGauss Kernel/Tree Ensemble with CLSS Matched-Molecular-Pair (MMP) Seam Surgery.

All feature scalers, quantile transformers, kernel weights, and MMP residual operators are fit
strictly on each target's InChIKey[:14]-disjoint training split (split == 'train') via exact
Leave-One-Out (LOO) and 5-fold Stratified Out-of-Fold (OOF) cross-validation (zero test-label access).

Supports:
  python3 run_lens2_clss_fast.py                     # runs all 30 targets in parallel (n_jobs=8)
  python3 run_lens2_clss_fast.py --dataset CHEMBL287_Ki  # runs a single target in ~20s
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from joblib import Parallel, delayed
from scipy.optimize import minimize
from scipy.spatial.distance import cdist
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, QuantileTransformer
from sklearn.svm import SVR
from sklearn.ensemble import ExtraTreesRegressor
import lightgbm as lgb
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, MACCSkeys, Descriptors, rdMolDescriptors, ReducedGraphs

RDLogger.DisableLog('rdApp.*')

RUN_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = RUN_ROOT / "data" / "benchmark_data"
CONFIG_DIR = RUN_ROOT / "data" / "configures" / "benchmark"
BASELINE_JSON = RUN_ROOT / "attempts" / "lens1_baseline_reproduction_and_multiscale_ruzicka_kernel" / "baseline_and_inchikey_audit.json"
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


def thermometer_encode(C: np.ndarray, thresholds=(1.0, 2.0, 3.0, 4.0, 6.0, 8.0)) -> np.ndarray:
    """
    Unary thermometer encoding of nonnegative integer count matrix C:
    Turns float32 BLAS SGEMM inner products into exact L1 MinMax (Ruzicka) intersections!
    """
    planes = []
    prev = 0.0
    for t in thresholds:
        w = np.sqrt(t - prev)
        planes.append(((C >= t).astype(np.float32)) * w)
        prev = t
    return np.hstack(planes)


def extract_fast_views(smiles_list):
    fast_descs = [(name, fn) for name, fn in Descriptors._descList if name not in ("Ipc", "AvgIpc")]
    n = len(smiles_list)
    ecfp_b1024_achiral = np.zeros((n, 1024), dtype=np.float32)
    ecfp_b2048_chiral_r1 = np.zeros((n, 2048), dtype=np.float32)
    ecfp_b2048_chiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    ecfp_b2048_chiral_r3 = np.zeros((n, 2048), dtype=np.float32)
    mc_c2048_chiral_r1 = np.zeros((n, 2048), dtype=np.float32)
    mc_c2048_chiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    mc_c2048_chiral_r3 = np.zeros((n, 2048), dtype=np.float32)
    mc_c2048_achiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    fcfp_c2048_chiral_r2 = np.zeros((n, 2048), dtype=np.float32)
    fcfp_c2048_chiral_r3 = np.zeros((n, 2048), dtype=np.float32)
    ap_c2048 = np.zeros((n, 2048), dtype=np.float32)
    tt_c2048 = np.zeros((n, 2048), dtype=np.float32)
    rdk_b2048 = np.zeros((n, 2048), dtype=np.float32)
    maccs_b167 = np.zeros((n, 167), dtype=np.float32)
    physchem = np.zeros((n, 24), dtype=np.float32)
    erg_fp = np.zeros((n, 315), dtype=np.float32)
    desc215 = np.zeros((n, len(fast_descs)), dtype=np.float32)

    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        ecfp_b1024_achiral[i] = bitvect_to_array(
            AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024, useChirality=False), 1024
        )
        ecfp_b2048_chiral_r1[i] = bitvect_to_array(
            AllChem.GetMorganFingerprintAsBitVect(mol, 1, nBits=2048, useChirality=True), 2048
        )
        ecfp_b2048_chiral_r2[i] = bitvect_to_array(
            AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048, useChirality=True), 2048
        )
        ecfp_b2048_chiral_r3[i] = bitvect_to_array(
            AllChem.GetMorganFingerprintAsBitVect(mol, 3, nBits=2048, useChirality=True), 2048
        )
        mc_c2048_chiral_r1[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 1, nBits=2048, useChirality=True), 2048
        )
        mc_c2048_chiral_r2[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 2, nBits=2048, useChirality=True), 2048
        )
        mc_c2048_chiral_r3[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 3, nBits=2048, useChirality=True), 2048
        )
        mc_c2048_achiral_r2[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 2, nBits=2048, useChirality=False), 2048
        )
        fcfp_c2048_chiral_r2[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 2, nBits=2048, useChirality=True, useFeatures=True), 2048
        )
        fcfp_c2048_chiral_r3[i] = hashed_int_fp_to_array(
            AllChem.GetHashedMorganFingerprint(mol, 3, nBits=2048, useChirality=True, useFeatures=True), 2048
        )
        ap_c2048[i] = hashed_int_fp_to_array(
            rdMolDescriptors.GetHashedAtomPairFingerprint(mol, nBits=2048, includeChirality=True), 2048
        )
        tt_c2048[i] = hashed_int_fp_to_array(
            rdMolDescriptors.GetHashedTopologicalTorsionFingerprint(mol, nBits=2048, includeChirality=True), 2048
        )
        rdk_b2048[i] = bitvect_to_array(Chem.RDKFingerprint(mol, minPath=1, maxPath=7, fpSize=2048), 2048)
        maccs_b167[i] = bitvect_to_array(MACCSkeys.GenMACCSKeys(mol), 167)
        erg_fp[i] = np.asarray(ReducedGraphs.GetErGFingerprint(mol), dtype=np.float32)
        desc215[i] = [fn(mol) for _, fn in fast_descs]

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
    desc215 = np.nan_to_num(desc215, nan=0.0, posinf=0.0, neginf=0.0)

    mc_multi = np.hstack([mc_c2048_chiral_r1, mc_c2048_chiral_r2, 0.85 * mc_c2048_chiral_r3])
    ecfp_multi = np.hstack([ecfp_b2048_chiral_r1, ecfp_b2048_chiral_r2, 0.85 * ecfp_b2048_chiral_r3])
    fcfp_multi = np.hstack([fcfp_c2048_chiral_r2, 0.85 * fcfp_c2048_chiral_r3])
    ap_tt = np.hstack([ap_c2048, tt_c2048])

    return {
        "ecfp_b1024_achiral": ecfp_b1024_achiral,
        "ecfp_multi_bit": ecfp_multi,
        "mc_multi_sqrt": np.sqrt(mc_multi),
        "mc_multi_log": np.log1p(mc_multi),
        "mc_r2_raw": mc_c2048_chiral_r2,
        "mc_achiral_sqrt": np.sqrt(mc_c2048_achiral_r2),
        "fcfp_multi_sqrt": np.sqrt(fcfp_multi),
        "ap_tt_sqrt": np.sqrt(ap_tt),
        "rdk_maccs": np.hstack([rdk_b2048, maccs_b167]),
        "maccs": maccs_b167,
        "physchem": physchem,
        "erg_fp": erg_fp,
        "desc215": desc215,
    }


def continuous_tanimoto_blas(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    A32 = np.ascontiguousarray(A, dtype=np.float32)
    B32 = np.ascontiguousarray(B, dtype=np.float32)
    dot = (A32 @ B32.T).astype(np.float64)
    na = np.sum(A32 * A32, axis=1, keepdims=True, dtype=np.float64)
    nb = np.sum(B32 * B32, axis=1, keepdims=True, dtype=np.float64).T
    denom = na + nb - dot
    sim = np.where(denom > 1e-12, dot / np.maximum(denom, 1e-12), 1.0)
    return np.clip(sim, 0.0, 1.0)


def loo_krr_and_predict(K_tr: np.ndarray, y_tr: np.ndarray, K_tr_te: np.ndarray, alphas):
    y_mean = float(np.mean(y_tr))
    yc = y_tr - y_mean
    evals, evecs = np.linalg.eigh(K_tr)
    evals = np.maximum(evals, 0.0)
    Qt_y = evecs.T @ yc
    V_sq = evecs ** 2

    loo_list = []
    te_list = []
    for alpha in alphas:
        inv_eig = 1.0 / (evals + alpha)
        w = evecs @ (inv_eig * Qt_y)
        diag_Ainv = V_sq @ inv_eig
        loo_pred = y_tr - (w / np.maximum(diag_Ainv, 1e-12))
        te_pred = y_mean + K_tr_te.T @ w
        loo_list.append(loo_pred)
        te_list.append(te_pred)
    return loo_list, te_list


def clss_mmp_directional_seam_corrector(views_tr, y_tr, base_oof, views_te, base_te, S_tr_tr, S_tr_te, S_ac_tr_tr, S_ac_tr_te):
    n_tr = len(y_tr)
    res_oof = y_tr - base_oof

    S_tr_zero = S_tr_tr.copy()
    np.fill_diagonal(S_tr_zero, 0.0)

    nw_oof_list = []
    nw_te_list = []
    for power in [4, 8, 14]:
        W_tr = (S_tr_zero ** power) * (S_tr_zero >= 0.35)
        W_te = (S_tr_te.T ** power) * (S_tr_te.T >= 0.35)
        denom_tr = np.sum(W_tr, axis=1) + 1e-4
        denom_te = np.sum(W_te, axis=1) + 1e-4
        nw_oof_list.append(base_oof + (W_tr @ res_oof) / denom_tr)
        nw_te_list.append(base_te + (W_te @ (y_tr - base_oof)) / denom_te)

    scaler = StandardScaler().fit(views_tr["physchem"])
    phi_tr = np.hstack([
        0.25 * views_tr["mc_r2_raw"],
        0.25 * views_tr["fcfp_multi_sqrt"],
        0.25 * views_tr["maccs"],
        0.25 * scaler.transform(views_tr["physchem"]),
    ]).astype(np.float64)
    phi_te = np.hstack([
        0.25 * views_te["mc_r2_raw"],
        0.25 * views_te["fcfp_multi_sqrt"],
        0.25 * views_te["maccs"],
        0.25 * scaler.transform(views_te["physchem"]),
    ]).astype(np.float64)

    S_pair = S_ac_tr_tr.copy()
    np.fill_diagonal(S_pair, 0.0)
    pair_i, pair_j, pair_w = [], [], []
    for i in range(n_tr):
        top_j = np.argsort(S_pair[i])[-5:]
        for j in top_j:
            if S_pair[i, j] >= 0.45 and i < j:
                pair_i.append(i)
                pair_j.append(j)
                pair_w.append(float(S_pair[i, j] ** 2))

    mmp_oof = np.copy(base_oof)
    mmp_te = np.copy(base_te)
    if len(pair_i) >= 25:
        pair_i = np.array(pair_i, dtype=np.int32)
        pair_j = np.array(pair_j, dtype=np.int32)
        pair_w = np.sqrt(np.array(pair_w, dtype=np.float64))[:, None]
        dX = (phi_tr[pair_i] - phi_tr[pair_j]) * pair_w
        dy_res = (res_oof[pair_i] - res_oof[pair_j]) * pair_w[:, 0]
        m_pairs, d_dim = dX.shape
        lam_mmp = 25.0 * m_pairs
        if m_pairs < d_dim:
            G = dX @ dX.T + lam_mmp * np.eye(m_pairs)
            beta_diff = dX.T @ np.linalg.solve(G, dy_res)
        else:
            G = dX.T @ dX + lam_mmp * np.eye(d_dim)
            beta_diff = np.linalg.solve(G, dX.T @ dy_res)

        shift_tr = phi_tr @ beta_diff
        shift_te = phi_te @ beta_diff

        W_tr = (S_tr_zero ** 6) * (S_tr_zero >= 0.45)
        W_te = (S_tr_te.T ** 6) * (S_tr_te.T >= 0.45)
        w_sum_tr = np.sum(W_tr, axis=1)
        w_sum_te = np.sum(W_te, axis=1)
        anchor_corr_tr = (W_tr @ (res_oof - shift_tr) + w_sum_tr * shift_tr) / (w_sum_tr + 1e-2)
        anchor_corr_te = (W_te @ (res_oof - shift_tr) + w_sum_te * shift_te) / (w_sum_te + 1e-2)
        mmp_oof = base_oof + anchor_corr_tr
        mmp_te = base_te + anchor_corr_te

    return nw_oof_list + [mmp_oof], nw_te_list + [mmp_te]


def fit_simplex_weights(oof_mat: np.ndarray, y_tr: np.ndarray, l2_reg: float = 1e-4) -> np.ndarray:
    m = oof_mat.shape[1]
    w0 = np.ones(m, dtype=np.float64) / m

    def loss_and_grad(w):
        r = oof_mat @ w - y_tr
        mse = np.mean(r * r) + l2_reg * np.sum((w - w0) ** 2)
        grad = (2.0 / len(y_tr)) * (oof_mat.T @ r) + 2.0 * l2_reg * (w - w0)
        return mse, grad

    res = minimize(
        loss_and_grad,
        w0,
        method="SLSQP",
        jac=True,
        bounds=[(0.0, 1.0)] * m,
        constraints=[{"type": "eq", "fun": lambda w: np.sum(w) - 1.0, "jac": lambda w: np.ones(m)}],
        options={"ftol": 1e-10, "maxiter": 300},
    )
    w = np.clip(res.x, 0.0, 1.0)
    return w / np.sum(w)


def fit_predict_clss_universal(views_tr, y_tr, views_te, seed=42):
    n_tr = len(y_tr)
    n_te = views_te["physchem"].shape[0]

    raw_keys = [
        "ecfp_b1024_achiral",
        "ecfp_multi_bit",
        "mc_multi_sqrt",
        "mc_multi_log",
        "mc_r2_raw",
        "mc_achiral_sqrt",
        "fcfp_multi_sqrt",
        "ap_tt_sqrt",
        "rdk_maccs",
        "maccs",
    ]
    sims_tr = {k: continuous_tanimoto_blas(views_tr[k], views_tr[k]) for k in raw_keys}
    sims_te = {k: continuous_tanimoto_blas(views_tr[k], views_te[k]) for k in raw_keys}

    scaler_phys = StandardScaler().fit(views_tr["physchem"])
    Z_tr = scaler_phys.transform(views_tr["physchem"])
    Z_te = scaler_phys.transform(views_te["physchem"])
    d1_tr = cdist(Z_tr, Z_tr, metric="cityblock") / Z_tr.shape[1]
    d1_te = cdist(Z_tr, Z_te, metric="cityblock") / Z_tr.shape[1]
    d2_tr = cdist(Z_tr, Z_tr, metric="sqeuclidean") / Z_tr.shape[1]
    d2_te = cdist(Z_tr, Z_te, metric="sqeuclidean") / Z_tr.shape[1]
    sims_tr["phys_lap"] = np.exp(-0.8 * d1_tr)
    sims_te["phys_lap"] = np.exp(-0.8 * d1_te)
    sims_tr["phys_rbf"] = np.exp(-0.5 * d2_tr)
    sims_te["phys_rbf"] = np.exp(-0.5 * d2_te)

    S_comp_tr = (
        0.22 * sims_tr["mc_multi_sqrt"]
        + 0.16 * sims_tr["ecfp_multi_bit"]
        + 0.14 * sims_tr["mc_multi_log"]
        + 0.12 * sims_tr["fcfp_multi_sqrt"]
        + 0.10 * sims_tr["ap_tt_sqrt"]
        + 0.08 * sims_tr["mc_achiral_sqrt"]
        + 0.08 * sims_tr["ecfp_b1024_achiral"]
        + 0.06 * sims_tr["rdk_maccs"]
        + 0.04 * sims_tr["phys_lap"]
    )
    S_comp_te = (
        0.22 * sims_te["mc_multi_sqrt"]
        + 0.16 * sims_te["ecfp_multi_bit"]
        + 0.14 * sims_te["mc_multi_log"]
        + 0.12 * sims_te["fcfp_multi_sqrt"]
        + 0.10 * sims_te["ap_tt_sqrt"]
        + 0.08 * sims_te["mc_achiral_sqrt"]
        + 0.08 * sims_te["ecfp_b1024_achiral"]
        + 0.06 * sims_te["rdk_maccs"]
        + 0.04 * sims_te["phys_lap"]
    )

    S_chiral_tr = 0.40 * sims_tr["mc_multi_sqrt"] + 0.25 * sims_tr["ecfp_multi_bit"] + 0.20 * sims_tr["fcfp_multi_sqrt"] + 0.15 * sims_tr["ap_tt_sqrt"]
    S_chiral_te = 0.40 * sims_te["mc_multi_sqrt"] + 0.25 * sims_te["ecfp_multi_bit"] + 0.20 * sims_te["fcfp_multi_sqrt"] + 0.15 * sims_te["ap_tt_sqrt"]

    kernel_pairs = [
        ("comp_g1", np.exp(-1.0 * (1.0 - S_comp_tr)) * S_comp_tr, np.exp(-1.0 * (1.0 - S_comp_te)) * S_comp_te),
        ("comp_g2.5", np.exp(-2.5 * (1.0 - S_comp_tr)) * S_comp_tr, np.exp(-2.5 * (1.0 - S_comp_te)) * S_comp_te),
        ("comp_g5", np.exp(-5.0 * (1.0 - S_comp_tr)) * S_comp_tr, np.exp(-5.0 * (1.0 - S_comp_te)) * S_comp_te),
        ("comp_g9", np.exp(-9.0 * (1.0 - S_comp_tr)) * S_comp_tr, np.exp(-9.0 * (1.0 - S_comp_te)) * S_comp_te),
        ("chiral_g2.5", np.exp(-2.5 * (1.0 - S_chiral_tr)) * S_chiral_tr, np.exp(-2.5 * (1.0 - S_chiral_te)) * S_chiral_te),
        ("chiral_g5", np.exp(-5.0 * (1.0 - S_chiral_tr)) * S_chiral_tr, np.exp(-5.0 * (1.0 - S_chiral_te)) * S_chiral_te),
        ("mc_sqrt_g3", np.exp(-3.0 * (1.0 - sims_tr["mc_multi_sqrt"])) * sims_tr["mc_multi_sqrt"], np.exp(-3.0 * (1.0 - sims_te["mc_multi_sqrt"])) * sims_te["mc_multi_sqrt"]),
        ("ecfp_multi_g3", np.exp(-3.0 * (1.0 - sims_tr["ecfp_multi_bit"])) * sims_tr["ecfp_multi_bit"], np.exp(-3.0 * (1.0 - sims_te["ecfp_multi_bit"])) * sims_te["ecfp_multi_bit"]),
        ("ecfp1024_g2.5", np.exp(-2.5 * (1.0 - sims_tr["ecfp_b1024_achiral"])) * sims_tr["ecfp_b1024_achiral"], np.exp(-2.5 * (1.0 - sims_te["ecfp_b1024_achiral"])) * sims_te["ecfp_b1024_achiral"]),
        ("fcfp_g3", np.exp(-3.0 * (1.0 - sims_tr["fcfp_multi_sqrt"])) * sims_tr["fcfp_multi_sqrt"], np.exp(-3.0 * (1.0 - sims_te["fcfp_multi_sqrt"])) * sims_te["fcfp_multi_sqrt"]),
        ("ap_tt_g3", np.exp(-3.0 * (1.0 - sims_tr["ap_tt_sqrt"])) * sims_tr["ap_tt_sqrt"], np.exp(-3.0 * (1.0 - sims_te["ap_tt_sqrt"])) * sims_te["ap_tt_sqrt"]),
        ("rdk_g2.5", np.exp(-2.5 * (1.0 - sims_tr["rdk_maccs"])) * sims_tr["rdk_maccs"], np.exp(-2.5 * (1.0 - sims_te["rdk_maccs"])) * sims_te["rdk_maccs"]),
        ("phys_lap", sims_tr["phys_lap"], sims_te["phys_lap"]),
    ]

    oof_cols, te_cols = [], []
    alphas = [0.015, 0.04, 0.10, 0.25, 0.60]
    for _, K_tr, K_te in kernel_pairs:
        loo_l, te_l = loo_krr_and_predict(K_tr, y_tr, K_te, alphas)
        oof_cols.extend(loo_l)
        te_cols.extend(te_l)

    n_bins = min(10, max(2, n_tr // 40))
    bins = pd.qcut(y_tr, q=n_bins, labels=False, duplicates="drop")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    folds = list(skf.split(np.zeros(n_tr), bins))

    svr_configs = [
        (kernel_pairs[1][1], kernel_pairs[1][2], 2.0, 0.05),
        (kernel_pairs[1][1], kernel_pairs[1][2], 5.0, 0.02),
        (kernel_pairs[2][1], kernel_pairs[2][2], 3.0, 0.03),
        (kernel_pairs[4][1], kernel_pairs[4][2], 3.0, 0.05),
        (kernel_pairs[8][1], kernel_pairs[8][2], 3.0, 0.05),
    ]
    svr_oof = np.zeros((n_tr, len(svr_configs)), dtype=np.float64)
    svr_te = np.zeros((n_te, len(svr_configs)), dtype=np.float64)

    anchor_idx = np.linspace(0, n_tr - 1, min(128, n_tr), dtype=int)
    X_tree_tr = np.hstack([S_comp_tr[:, anchor_idx], S_chiral_tr[:, anchor_idx], views_tr["maccs"], Z_tr])
    X_tree_te = np.hstack([S_comp_te[anchor_idx, :].T, S_chiral_te[anchor_idx, :].T, views_te["maccs"], Z_te])
    lgb_oof = np.zeros(n_tr, dtype=np.float64)
    et_oof = np.zeros(n_tr, dtype=np.float64)

    for tr_idx, val_idx in folds:
        y_f = y_tr[tr_idx]
        for j, (K_tr, _, C_val, eps_val) in enumerate(svr_configs):
            m = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
            m.fit(K_tr[np.ix_(tr_idx, tr_idx)], y_f)
            svr_oof[val_idx, j] = m.predict(K_tr[np.ix_(tr_idx, val_idx)].T)

        lgbm = lgb.LGBMRegressor(
            n_estimators=250, learning_rate=0.04, num_leaves=31,
            subsample_for_bin=500, colsample_bytree=0.7, subsample=0.8,
            random_state=seed, n_jobs=1, verbose=-1
        )
        lgbm.fit(X_tree_tr[tr_idx], y_f)
        lgb_oof[val_idx] = lgbm.predict(X_tree_tr[val_idx])

        et = ExtraTreesRegressor(n_estimators=200, max_features=0.5, random_state=seed, n_jobs=1)
        et.fit(X_tree_tr[tr_idx], y_f)
        et_oof[val_idx] = et.predict(X_tree_tr[val_idx])

    for j, (K_tr, K_te, C_val, eps_val) in enumerate(svr_configs):
        m = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
        m.fit(K_tr, y_tr)
        svr_te[:, j] = m.predict(K_te.T)
        oof_cols.append(svr_oof[:, j])
        te_cols.append(svr_te[:, j])

    lgbm_full = lgb.LGBMRegressor(
        n_estimators=250, learning_rate=0.04, num_leaves=31,
        subsample_for_bin=500, colsample_bytree=0.7, subsample=0.8,
        random_state=seed, n_jobs=1, verbose=-1
    )
    lgbm_full.fit(X_tree_tr, y_tr)
    oof_cols.append(lgb_oof)
    te_cols.append(lgbm_full.predict(X_tree_te))

    et_full = ExtraTreesRegressor(n_estimators=200, max_features=0.5, random_state=seed, n_jobs=1)
    et_full.fit(X_tree_tr, y_tr)
    oof_cols.append(et_oof)
    te_cols.append(et_full.predict(X_tree_te))

    oof_mat_stage1 = np.column_stack(oof_cols)
    te_mat_stage1 = np.column_stack(te_cols)
    w_stage1 = fit_simplex_weights(oof_mat_stage1, y_tr, l2_reg=2e-3)
    base_oof = oof_mat_stage1 @ w_stage1
    base_te = te_mat_stage1 @ w_stage1

    # Stage 2: CLSS Matched-Molecular-Pair (MMP) Directional Seam Surgery Correctors
    mmp_oof_list, mmp_te_list = clss_mmp_directional_seam_corrector(
        views_tr, y_tr, base_oof, views_te, base_te,
        S_comp_tr, S_comp_te, sims_tr["mc_achiral_sqrt"], sims_te["mc_achiral_sqrt"]
    )
    oof_mat_stage2 = np.column_stack([base_oof] + mmp_oof_list + oof_cols[:20])
    te_mat_stage2 = np.column_stack([base_te] + mmp_te_list + te_cols[:20])
    w_stage2 = fit_simplex_weights(oof_mat_stage2, y_tr, l2_reg=1e-3)
    stage2_oof = oof_mat_stage2 @ w_stage2
    stage2_te = te_mat_stage2 @ w_stage2

    # Stage 3: Exact Thermometer-BLAS Ruzicka + ErG Pharmacophore + 215-Descriptor RankGauss LOO KRR
    u_mc_tr = thermometer_encode(views_tr["mc_r2_raw"])
    u_mc_te = thermometer_encode(views_te["mc_r2_raw"])
    S_ruz_mc_tr = continuous_tanimoto_blas(u_mc_tr, u_mc_tr)
    S_ruz_mc_te = continuous_tanimoto_blas(u_mc_tr, u_mc_te)

    erg_tr_s = np.sqrt(np.maximum(views_tr["erg_fp"], 0.0))
    erg_te_s = np.sqrt(np.maximum(views_te["erg_fp"], 0.0))
    S_erg_tr = continuous_tanimoto_blas(erg_tr_s, erg_tr_s)
    S_erg_te = continuous_tanimoto_blas(erg_tr_s, erg_te_s)

    qt = QuantileTransformer(n_quantiles=min(200, n_tr), output_distribution="normal", random_state=seed)
    Z_d_tr = qt.fit_transform(views_tr["desc215"])
    Z_d_te = qt.transform(views_te["desc215"])
    S_d215_tr = np.exp(-0.6 * cdist(Z_d_tr, Z_d_tr, metric="cityblock") / Z_d_tr.shape[1])
    S_d215_te = np.exp(-0.6 * cdist(Z_d_tr, Z_d_te, metric="cityblock") / Z_d_tr.shape[1])

    loo_r1, te_r1 = loo_krr_and_predict(np.exp(-3.0 * (1.0 - S_ruz_mc_tr)) * S_ruz_mc_tr, y_tr, np.exp(-3.0 * (1.0 - S_ruz_mc_te)) * S_ruz_mc_te, [0.03, 0.08, 0.20])
    loo_r2, te_r2 = loo_krr_and_predict(np.exp(-2.5 * (1.0 - S_erg_tr)) * S_erg_tr, y_tr, np.exp(-2.5 * (1.0 - S_erg_te)) * S_erg_te, [0.05, 0.15, 0.40])
    loo_r3, te_r3 = loo_krr_and_predict(S_d215_tr, y_tr, S_d215_te, [0.05, 0.15, 0.40])

    oof_mat_stage3 = np.column_stack([stage2_oof] + loo_r1 + loo_r2 + loo_r3)
    te_mat_stage3 = np.column_stack([stage2_te] + te_r1 + te_r2 + te_r3)
    w_stage3 = fit_simplex_weights(oof_mat_stage3, y_tr, l2_reg=5e-3)

    final_oof = oof_mat_stage3 @ w_stage3
    final_te = te_mat_stage3 @ w_stage3
    return final_te, final_oof, stage2_te, stage2_oof


def paired_bootstrap_win_rate(y_true, pred_model, pred_base, ref_mse, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    err_model = (y_true - pred_model) ** 2
    err_base = (y_true - pred_base) ** 2
    idx = rng.integers(0, n, size=(n_boot, n))
    boot_mse_model = np.mean(err_model[idx], axis=1)
    boot_mse_base = np.mean(err_base[idx], axis=1)
    win_vs_base = float(np.mean(boot_mse_model < boot_mse_base))
    win_vs_ref = float(np.mean(boot_mse_model < ref_mse))
    return win_vs_base, win_vs_ref


def run_single_dataset(ds_name: str, b_info: dict, preds_dir: Path):
    t_ds = time.time()
    df = pd.read_csv(DATA_DIR / f"{ds_name}.csv")
    tr_df = df[df["split"] == "train"].reset_index(drop=True)
    te_df = df[df["split"] == "test"].reset_index(drop=True)

    te_ik14 = {Chem.MolToInchiKey(Chem.MolFromSmiles(s))[:14] for s in te_df["smiles"]}
    keep_mask = [Chem.MolToInchiKey(Chem.MolFromSmiles(s))[:14] not in te_ik14 for s in tr_df["smiles"]]
    tr_clean_df = tr_df[keep_mask].reset_index(drop=True)

    views_tr = extract_fast_views(tr_clean_df["smiles"].tolist())
    views_te = extract_fast_views(te_df["smiles"].tolist())
    y_tr = tr_clean_df["y"].to_numpy(dtype=np.float64)
    y_te = te_df["y"].to_numpy(dtype=np.float64)
    cliff_te = te_df["cliff_mol"].to_numpy(dtype=np.int32) == 1

    pred_te, oof_pred, _, _ = fit_predict_clss_universal(views_tr, y_tr, views_te)

    svm_cfg = yaml.safe_load((CONFIG_DIR / ds_name / "SVM_ECFP.yml").read_text())
    svm_base = SVR(**svm_cfg)
    svm_base.fit(views_tr["ecfp_b1024_achiral"], y_tr)
    pred_svm_base = svm_base.predict(views_te["ecfp_b1024_achiral"])

    mse_oof = float(np.mean((y_tr - oof_pred) ** 2))
    mse_te = float(np.mean((y_te - pred_te) ** 2))
    mse_cliff = float(np.mean((y_te[cliff_te] - pred_te[cliff_te]) ** 2))
    mse_noncliff = float(np.mean((y_te[~cliff_te] - pred_te[~cliff_te]) ** 2))

    pol_mse = b_info["polaris_best_mse"]
    pap_mse = b_info["paper_best_mse"]
    pap_cliff_mse = b_info["paper_best_cliff_mse"]
    repro_best_cliff_mse = b_info["repro_best_classical_cliff_mse"]

    rel_pol = 100.0 * (pol_mse - mse_te) / pol_mse
    rel_pap = 100.0 * (pap_mse - mse_te) / pap_mse
    rel_cliff_pap = 100.0 * (pap_cliff_mse - mse_cliff) / pap_cliff_mse
    rel_cliff_repro = 100.0 * (repro_best_cliff_mse - mse_cliff) / repro_best_cliff_mse

    boot_vs_svm, boot_vs_pol = paired_bootstrap_win_rate(y_te, pred_te, pred_svm_base, pol_mse, n_boot=10000, seed=0)
    boot_cliff_vs_svm, _ = paired_bootstrap_win_rate(y_te[cliff_te], pred_te[cliff_te], pred_svm_base[cliff_te], pap_cliff_mse, n_boot=10000, seed=0)

    test_global_indices = df.index[df["split"] == "test"].to_numpy(dtype=np.int32)
    pred_df = pd.DataFrame({
        "test_row_index": np.arange(len(te_df)),
        "csv_row_index": test_global_indices,
        "smiles": te_df["smiles"],
        "cliff_mol": te_df["cliff_mol"],
        "y_true": y_te,
        "y_pred_clss": pred_te,
        "y_pred_svm_ecfp_baseline": pred_svm_base,
    })
    pred_df.to_csv(preds_dir / f"{ds_name}_test_predictions.csv", index=False)

    row = {
        "dataset": ds_name,
        "slug": b_info["slug"],
        "csv_sha256": b_info["csv_sha256"],
        "n_train_used": len(tr_clean_df),
        "n_test": len(te_df),
        "n_test_cliff": int(np.sum(cliff_te)),
        "oof_mse": mse_oof,
        "clss_mse": mse_te,
        "clss_rmse": float(np.sqrt(mse_te)),
        "clss_cliff_mse": mse_cliff,
        "clss_cliff_rmse": float(np.sqrt(mse_cliff)),
        "clss_noncliff_mse": mse_noncliff,
        "clss_noncliff_rmse": float(np.sqrt(mse_noncliff)),
        "polaris_best_mse": pol_mse,
        "paper_best_mse": pap_mse,
        "paper_best_cliff_mse": pap_cliff_mse,
        "repro_svm_ecfp_mse": b_info["repro_svm_ecfp_mse"],
        "repro_svm_ecfp_cliff_mse": b_info["repro_svm_ecfp_cliff_mse"],
        "repro_best_classical_mse": b_info["repro_best_classical_mse"],
        "repro_best_classical_cliff_mse": repro_best_cliff_mse,
        "rel_impr_vs_polaris_pct": rel_pol,
        "rel_impr_vs_paper_pct": rel_pap,
        "rel_impr_cliff_vs_paper_pct": rel_cliff_pap,
        "rel_impr_cliff_vs_repro_best_pct": rel_cliff_repro,
        "boot_win_rate_vs_svm": boot_vs_svm,
        "boot_win_rate_vs_polaris_val": boot_vs_pol,
        "boot_cliff_win_rate_vs_svm": boot_cliff_vs_svm,
        "elapsed_sec": round(time.time() - t_ds, 2),
    }
    print(
        f"{ds_name:16s} | Pol={pol_mse:.4f} Pap={pap_mse:.4f} -> CLSS={mse_te:.4f} ({rel_pol:+6.2f}% Pol, {rel_pap:+6.2f}% Pap, boot_svm={100*boot_vs_svm:5.1f}%, boot_pol={100*boot_vs_pol:5.1f}%) "
        f"| Cliff: Pap={pap_cliff_mse:.4f} -> {mse_cliff:.4f} ({rel_cliff_pap:+6.2f}%) [{time.time()-t_ds:.1f}s]",
        flush=True,
    )
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default=None, help="Run a single dataset (e.g. CHEMBL287_Ki)")
    parser.add_argument("--n_jobs", type=int, default=6, help="Number of parallel workers for 30-dataset sweep")
    args = parser.parse_args()

    t0 = time.time()
    baseline_rows = json.loads(BASELINE_JSON.read_text())
    base_by_ds = {r["dataset"]: r for r in baseline_rows}

    preds_dir = OUT_DIR / "predictions"
    preds_dir.mkdir(parents=True, exist_ok=True)

    if args.dataset is not None:
        run_single_dataset(args.dataset, base_by_ds[args.dataset], preds_dir)
        return

    ds_names = sorted(base_by_ds.keys())
    lens2_results = Parallel(n_jobs=args.n_jobs, prefer="processes")(
        delayed(run_single_dataset)(ds_name, base_by_ds[ds_name], preds_dir) for ds_name in ds_names
    )
    lens2_results = sorted(lens2_results, key=lambda r: r["dataset"])

    wins_polaris = sum(1 for r in lens2_results if r["clss_mse"] < r["polaris_best_mse"])
    wins_polaris_5pct = sum(1 for r in lens2_results if r["rel_impr_vs_polaris_pct"] >= 5.0)
    wins_polaris_boot95 = sum(
        1 for r in lens2_results
        if r["rel_impr_vs_polaris_pct"] >= 5.0 and r["boot_win_rate_vs_svm"] >= 0.95 and r["clss_mse"] < r["paper_best_mse"]
    )
    wins_paper = sum(1 for r in lens2_results if r["clss_mse"] < r["paper_best_mse"])
    wins_cliff = sum(1 for r in lens2_results if r["clss_cliff_mse"] < r["paper_best_cliff_mse"])

    macro_rmse = float(np.mean([r["clss_rmse"] for r in lens2_results]))
    macro_cliff_rmse = float(np.mean([r["clss_cliff_rmse"] for r in lens2_results]))
    macro_noncliff_rmse = float(np.mean([r["clss_noncliff_rmse"] for r in lens2_results]))
    macro_mse = float(np.mean([r["clss_mse"] for r in lens2_results]))
    macro_cliff_mse = float(np.mean([r["clss_cliff_mse"] for r in lens2_results]))

    print("-" * 115, flush=True)
    print(f"LENS 2 CLSS UNIVERSAL RECIPE SUMMARY ({time.time() - t0:.1f}s):", flush=True)
    print(f"  Wins vs Polaris Best MSE:                  {wins_polaris}/30 (>=5% rel margin: {wins_polaris_5pct}/30)", flush=True)
    print(f"  Wins >=5% rel + >=95% bootstrap + <Paper:  {wins_polaris_boot95}/30", flush=True)
    print(f"  Wins vs Paper Best MSE:                    {wins_paper}/30", flush=True)
    print(f"  Wins vs Paper Best Cliff MSE:              {wins_cliff}/30", flush=True)
    print(f"  Macro-Average MSE / RMSE:                  {macro_mse:.4f} / {macro_rmse:.4f} (Monroe 2026: 0.629, GraphCliff: 0.665, SVM: 0.671)", flush=True)
    print(f"  Macro-Average Cliff MSE / RMSE:            {macro_cliff_mse:.4f} / {macro_cliff_rmse:.4f} (Monroe 2026: 0.737, SVM: 0.751, GraphCliff: 0.757)", flush=True)
    print(f"  Macro-Average Non-Cliff RMSE:              {macro_noncliff_rmse:.4f}", flush=True)

    out_path = OUT_DIR / "lens2_clss_universal_results.json"
    out_path.write_text(json.dumps(lens2_results, indent=2))


if __name__ == "__main__":
    main()
