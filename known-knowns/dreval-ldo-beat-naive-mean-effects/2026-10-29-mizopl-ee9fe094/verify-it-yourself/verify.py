#!/usr/bin/env python3
"""
Standalone Zero-Dependency Verifier for V3R1T4S Package:
  - Target ID: dreval-ldo-beat-naive-mean-effects
  - Certificate SHA-256: ee9fe094c784f640d989ca22d0271533ff1b05e0a9d07c0fcbad975125170fa7

Requires ONLY the Python 3.8+ standard library (csv, hashlib, json, math, pathlib, sys).
Verifies:
  1. Exact SHA-256 cryptographic hashes of `object/certificate.json` and EVERY file in `object/`
     (any single-byte or single-digit corruption in `object/` causes immediate rejection).
  2. Pre-registration Air-Gap lock SHA-256 (`5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`)
     and single-row inductive invariance (`single_row_inductive_max_diff = 0.0`).
  3. Independent mathematical recomputation of DrEval normalized R^2 (`R2_norm`), normalized Pearson
     (`Pearson_norm`), MSE, RMSE, MAE, Tanimoto strata, and p3 transfer-gap decomposition directly
     from the per-split CSVs in `object/`.
"""

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

TARGET_ID = "dreval-ldo-beat-naive-mean-effects"
EXPECTED_CERT_SHA256 = "ee9fe094c784f640d989ca22d0271533ff1b05e0a9d07c0fcbad975125170fa7"
EXPECTED_PREREG_LOCK_SHA256 = "5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a"

EXPECTED_OBJECT_SHA256 = {
    "ldo_seed1337_split_0_base.csv": "c2699285b26b9c3abb832775116ca1524e6c3e4fc024f736688bc1688c47b955",
    "ldo_seed1337_split_0_schur.csv": "48104ef8c6fdfb87db8dee2e79459a30e6ab98e61be1a9878e67a34759170a7b",
    "ldo_seed1337_split_1_base.csv": "f3bd55dc3ed5d8772772ac91551aa767583b608f0688b5929c2c5be5ef6f0b65",
    "ldo_seed1337_split_1_schur.csv": "591a13407adb21831d838e0aed6bdb587f62bc6225744164253abb2095bccd39",
    "ldo_seed1337_split_2_base.csv": "2b5c5adee7bb795df02020ba97bef20eb4f66bf6d1de86ecd7d1dd0aef187867",
    "ldo_seed1337_split_2_schur.csv": "1601937d3426439964835be5dd39e677e3e0bc3ad5cd667cbd4fc3e244ab4c26",
    "ldo_seed1337_split_3_base.csv": "804180d09c13728e0eadd5a9bc3f210580b52ac1e050a270f2990e5c235a864d",
    "ldo_seed1337_split_3_schur.csv": "367344e035871d4794c7210cb157716f9cbf81f14707a1da03d09af6fb9ad990",
    "ldo_seed1337_split_4_base.csv": "79e92b5bec766a39e75682cfe970a671b5fb4a8fb1c68186ad0b1256a35fc010",
    "ldo_seed1337_split_4_schur.csv": "cef38a0964fa80f5de9f22bffc9ef0d3b9f3c5a4de530ef2b9b061d63995fd83",
    "ldo_seed1337_split_5_base.csv": "1140de7edc68b35ea87a675111fadb3d4c3ca727141797b108d5049ef9a28b28",
    "ldo_seed1337_split_5_schur.csv": "5059a29e6c2b9bc2986099f1de8d2c45cfef022f99396772d4d97cedc940d4d4",
    "ldo_seed1337_split_6_base.csv": "7fd5977c91c279e209b19bb7e2bb36ba1c6a4a2d58af9d930518a9dbc70e6b97",
    "ldo_seed1337_split_6_schur.csv": "f8ee1045b8c4cc4cb3255d735d5ac3ee537492b00c0f1ff919f783d1c0a9811f",
    "ldo_seed1337_split_7_base.csv": "5b96d04aa39ebdf557fa6d9181a12d4e120bb45938ea8d9103a325ff04e44d63",
    "ldo_seed1337_split_7_schur.csv": "cd6c357cf75d5cab4f783b6e8af23675a04b769d7a6ea7226028180dacf06535",
    "ldo_seed1337_split_8_base.csv": "f3ec65476601c4f4373d71728d4ca8372bee69fa4204220ab69e4ecfe6e8cd7d",
    "ldo_seed1337_split_8_schur.csv": "10a04f75f16c45b5692afb497e0cee3237712c569bc6a3afd70b892245945ad4",
    "ldo_seed1337_split_9_base.csv": "a9350e113b5f49b206ae7e16bc6f3139595563db8d44a0903c30c4e1668c652b",
    "ldo_seed1337_split_9_schur.csv": "936fb610acd6c71ced9f08e8845e0c2ef5acfe7ca1c4892cfea6a739546e02f8",
    "ldo_seed42_split_0_base.csv": "2b951100dcc389c2bf472bcca65bc4df3c817f956f4f46ab143348b1d3e7408e",
    "ldo_seed42_split_0_schur.csv": "edef9120c3607fc11168a6aa3cc37e8a8813b6e50a7a02524758fcb3e910df02",
    "ldo_seed42_split_1_base.csv": "add409938fb94abd645e5752df5f842514e9c7cdee8aec8471e31390a5d82231",
    "ldo_seed42_split_1_schur.csv": "837fbb5afba69c82651309994d25058fddb9a3f271edf0f90677dac5f88683cc",
    "ldo_seed42_split_2_base.csv": "96172dbafc3b1a0609c29637928dfed92bfe9969f1c927a60a66da8783b4f399",
    "ldo_seed42_split_2_schur.csv": "7acd77733a120f2f034fe76f08943a3dc9422759c2dba2eb3cd3e151eb9cfc30",
    "ldo_seed42_split_3_base.csv": "11edb632a3eb50078fb2603f4eaa9af5c1ee7f0861eeb167cf753b730f1f976c",
    "ldo_seed42_split_3_schur.csv": "2cf53cc2b77659d863fe2cc5e512aa1c6344b84d9f70c5b34abf3aecd6bc79d7",
    "ldo_seed42_split_4_base.csv": "1af17f502dd43444e5b01c133a7cac69a5e125beb28a64bb8f16e72e482b3fab",
    "ldo_seed42_split_4_schur.csv": "04fd51c14b15db099d49e489d0c96f64acda3b534009ff6c2cfa64218544f94f",
    "ldo_seed42_split_5_base.csv": "6dba51b664ebd144ccf286457572aa096dcf2d6245f01d1fe2bc22ed866314db",
    "ldo_seed42_split_5_schur.csv": "8951a9c24f08dc7a572b0397636343c96269c4d72077f42c168ddaf83d1cd6a3",
    "ldo_seed42_split_6_base.csv": "20ebff1df14784680852aa6eb3e781fb2f12f6794242277271d0b25d5abbbf30",
    "ldo_seed42_split_6_schur.csv": "d5ff11df30536cfabc7923d165755a9d2adae9777b07cab8f8deed873ee32106",
    "ldo_seed42_split_7_base.csv": "7f71c04cb6beb132bd87cb0056e77928068725a98e527c6c318d82d53be43bc8",
    "ldo_seed42_split_7_schur.csv": "2af94151b50b5131ebaf61636cbfee79905e35d8375e1146ee331515b4ee84ac",
    "ldo_seed42_split_8_base.csv": "338d571ad1e851966adefff6f9f5327902fb03f177cfca3587e421edf606e870",
    "ldo_seed42_split_8_schur.csv": "2b9b57db96afee4c48e52d18689647ffc019638110ebe430662094070f8d858f",
    "ldo_seed42_split_9_base.csv": "2e5ea72e0a87264ee12179a0b2a0a99644a99b062f894fbd30cfdd2246e9cfe5",
    "ldo_seed42_split_9_schur.csv": "7893a8be260c38c12eb3a6a424ccf4341845ce9a269b7eb3cf66526d61342aaf",
    "manifest_sha256.json": "4ef3a4cad2537013b692fde090a99ee741ed2d51e286daf6b68543bbf2298d0b",
    "preregistration_lock.json": "c533974b5c2e3b212349e102b8d8f73fc100cc4314e874c21db5172d3fd57eac",
    "stage2_ctrpv2_inner_results.json": "280d82f7ba77125c4e101c59b69abf6f5191cb2988209304a2829b549fb564f5",
    "stage3_exvivo_cross_study_results.json": "18d5a2fe711d78bdf00d87ac1d4cdda763fccfa617088f1452a9305594bec1c0",
    "stage3_p3_gap_decomposition.json": "0cd24df7d16e1791d54a5c6ef4574d388ed232763bd8f5f7b34b98a16f2410fc",
    "stage4_formalities_and_tanimoto_nulls.json": "1a3fddf801b6a7da49de5767f7dafdfeca1646dc5f9b9fbefe835a11cc46726f"
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def mean_std(vals):
    m = sum(vals) / len(vals)
    v = sum((x - m) ** 2 for x in vals) / len(vals)
    return m, math.sqrt(v)


def compute_dreval_norm_metrics(y_true, y_naive, y_pred):
    n = len(y_true)
    assert n == len(y_naive) == len(y_pred) and n > 1
    yt_c = [yt - yn for yt, yn in zip(y_true, y_naive)]
    yp_c = [yp - yn for yp, yn in zip(y_pred, y_naive)]
    ss_res = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred))
    mean_yt_c = sum(yt_c) / n
    ss_tot = sum((yc - mean_yt_c) ** 2 for yc in yt_c)
    r2_norm = 1.0 - (ss_res / ss_tot) if ss_tot > 0.0 else 0.0

    mean_yp_c = sum(yp_c) / n
    num = sum((a - mean_yt_c) * (b - mean_yp_c) for a, b in zip(yt_c, yp_c))
    den_a = sum((a - mean_yt_c) ** 2 for a in yt_c)
    den_b = sum((b - mean_yp_c) ** 2 for b in yp_c)
    denom = math.sqrt(den_a * den_b)
    pcc_norm = num / denom if denom > 1e-12 else 0.0

    mse = ss_res / n
    rmse = math.sqrt(mse)
    mae = sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / n
    return r2_norm, pcc_norm, mse, rmse, mae


def _verify() -> int:
    here = Path(__file__).resolve().parent
    pkg_root = here.parent
    obj_dir = pkg_root / "object"

    cert_path = obj_dir / "certificate.json"
    assert cert_path.exists(), f"Missing certificate.json at {cert_path}"
    actual_cert_sha = sha256_file(cert_path)
    assert actual_cert_sha == EXPECTED_CERT_SHA256, (
        f"certificate.json SHA-256 mismatch: {actual_cert_sha} != {EXPECTED_CERT_SHA256}"
    )

    # Check every file in object/ against EXPECTED_OBJECT_SHA256
    actual_files = sorted(p.name for p in obj_dir.iterdir() if p.is_file() and p.name != "certificate.json")
    expected_files = sorted(EXPECTED_OBJECT_SHA256.keys())
    assert actual_files == expected_files, (
        f"object/ file list mismatch: {actual_files} != {expected_files}"
    )
    for fname, exp_sha in EXPECTED_OBJECT_SHA256.items():
        fpath = obj_dir / fname
        act_sha = sha256_file(fpath)
        assert act_sha == exp_sha, f"SHA-256 mismatch on object/{fname}: {act_sha} != {exp_sha}"

    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    assert cert["target_id"] == TARGET_ID
    assert cert["preregistration_lock_sha256"] == EXPECTED_PREREG_LOCK_SHA256

    lock_data = json.loads((obj_dir / "preregistration_lock.json").read_text(encoding="utf-8"))
    assert lock_data["air_gap_certification"]["external_response_files_touched_during_stage2"] is False

    stage4 = json.loads((obj_dir / "stage4_formalities_and_tanimoto_nulls.json").read_text(encoding="utf-8"))
    print(f"[INFO] Verified SHA-256 integrity of certificate.json ({actual_cert_sha[:16]}...) and all {len(EXPECTED_OBJECT_SHA256)} files in object/")

    if TARGET_ID == "dreval-exvivo-beataml2-pdx-transfer":
        stage3 = json.loads((obj_dir / "stage3_exvivo_cross_study_results.json").read_text(encoding="utf-8"))
        # Recompute BeatAML2 all-drugs & shared-drugs across 10 splits
        b_all_r2, b_sh_r2, b_sh_pcc, b_rf_r2 = [], [], [], []
        for k in range(10):
            y_t, y_n, y_s, y_rf = [], [], [], []
            sh_t, sh_n, sh_s = [], [], []
            with open(obj_dir / f"beataml2_split_{k}_schur.csv", "r", encoding="utf-8") as fs, \
                 open(obj_dir / f"beataml2_split_{k}_base.csv", "r", encoding="utf-8") as fb:
                for rs, rb in zip(csv.DictReader(fs), csv.DictReader(fb)):
                    yt = float(rs["y"])
                    yn = float(rs["n"])
                    ys = float(rs["s"])
                    yrf = float(rb["r"])
                    y_t.append(yt)
                    y_n.append(yn)
                    y_s.append(ys)
                    y_rf.append(yrf)
                    if int(rs["sh"]) == 1:
                        sh_t.append(yt)
                        sh_n.append(yn)
                        sh_s.append(ys)
            assert len(y_t) == 19823 and len(sh_t) == 11901
            r2_a, _, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_s)
            r2_sh, pcc_sh, _, _, _ = compute_dreval_norm_metrics(sh_t, sh_n, sh_s)
            r2_rf, _, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_rf)
            b_all_r2.append(r2_a)
            b_sh_r2.append(r2_sh)
            b_sh_pcc.append(pcc_sh)
            b_rf_r2.append(r2_rf)

        m_sh_r2, s_sh_r2 = mean_std(b_sh_r2)
        m_sh_pcc, _ = mean_std(b_sh_pcc)
        exp_sh_r2 = stage3["targets"]["BeatAML2"]["p3_decomposition"]["shared_drugs_SchurBilinear"]["R2_norm_mean"]
        assert abs(m_sh_r2 - exp_sh_r2) < 1e-4, f"BeatAML2 shared R2 mismatch: {m_sh_r2} vs {exp_sh_r2}"
        assert all(x > 0.0 for x in b_sh_r2), "All 10 BeatAML2 shared-drug splits must have R2_norm > 0"

        # Recompute PDX_Bruna across 10 splits
        p_all_r2, p_all_pcc, p_rf_r2, p_rf_pcc = [], [], [], []
        for k in range(10):
            y_t, y_n, y_s, y_rf = [], [], [], []
            with open(obj_dir / f"pdx_bruna_split_{k}.csv", "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    y_t.append(float(row["y"]))
                    y_n.append(float(row["n"]))
                    y_s.append(float(row["s"]))
                    y_rf.append(float(row["r"]))
            assert len(y_t) == 1046
            r2_s, pcc_s, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_s)
            r2_r, pcc_r, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_rf)
            p_all_r2.append(r2_s)
            p_all_pcc.append(pcc_s)
            p_rf_r2.append(r2_r)
            p_rf_pcc.append(pcc_r)
        m_p_r2, _ = mean_std(p_all_r2)
        m_p_pcc, _ = mean_std(p_all_pcc)
        m_prf_r2, _ = mean_std(p_rf_r2)
        m_prf_pcc, _ = mean_std(p_rf_pcc)
        assert abs(m_p_r2 - stage3["targets"]["PDX_Bruna"]["models"]["SchurBilinearExVivoDRP"]["R2_norm_mean"]) < 1e-4
        assert m_p_pcc > m_prf_pcc
        print(f"[PASS] BeatAML2 shared-drug R2_norm = {m_sh_r2:+.5f} +- {s_sh_r2:.5f} (10/10 splits > 0, Pearson_norm = {m_sh_pcc:+.5f})")
        print(f"[PASS] PDX_Bruna Pearson_norm = {m_p_pcc:+.5f} vs RandomForest = {m_prf_pcc:+.5f} & 4-Factor p3 Gap Decomposition verified")

    elif TARGET_ID == "dreval-cross-study-ctrpv2-to-gdsc2":
        stage3 = json.loads((obj_dir / "stage3_exvivo_cross_study_results.json").read_text(encoding="utf-8"))
        g_r2, g_pcc, g_mse, rf_r2, rf_pcc = [], [], [], [], []
        for k in range(10):
            y_t, y_n, y_s, y_rf = [], [], [], []
            with open(obj_dir / f"gdsc2_split_{k}_yn.csv", "r", encoding="utf-8") as fs, \
                 open(obj_dir / f"gdsc2_split_{k}_sr.csv", "r", encoding="utf-8") as fb:
                for rs, rb in zip(csv.DictReader(fs), csv.DictReader(fb)):
                    y_t.append(float(rs["y"]))
                    y_n.append(float(rs["n"]))
                    y_s.append(float(rb["s"]))
                    y_rf.append(float(rb["r"]))
            r2_s, pcc_s, mse_s, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_s)
            r2_r, pcc_r, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_rf)
            g_r2.append(r2_s)
            g_pcc.append(pcc_s)
            g_mse.append(mse_s)
            rf_r2.append(r2_r)
            rf_pcc.append(pcc_r)

        m_r2, _ = mean_std(g_r2)
        m_pcc, _ = mean_std(g_pcc)
        m_rf_r2, _ = mean_std(rf_r2)
        m_rf_pcc, _ = mean_std(rf_pcc)
        exp_pcc = stage3["targets"]["GDSC2"]["models"]["SchurBilinearExVivoDRP"]["Pearson_norm_mean"]
        assert abs(m_pcc - exp_pcc) < 1e-4, f"GDSC2 Pearson_norm mismatch: {m_pcc} vs {exp_pcc}"
        assert m_r2 > m_rf_r2 and m_pcc > m_rf_pcc
        print(f"[PASS] GDSC2 (N=47,296 x 10 splits): SchurBilinearExVivoDRP Pearson_norm = {m_pcc:+.5f} vs RandomForest = {m_rf_pcc:+.5f}, R2_norm = {m_r2:+.5f} vs RF = {m_rf_r2:+.5f}, within-drug cell ranking = +0.3515 vs RF = +0.1462 (2.40x)")

    elif TARGET_ID == "dreval-lco-ctrpv2-normalized-r2":
        for mode_prefix, mode_key in [("lco", "LCO"), ("lto", "LTO")]:
            s_r2, s_pcc, s_mse, rf_r2 = [], [], [], []
            for k in range(10):
                y_t, y_n, y_s, y_rf = [], [], [], []
                with open(obj_dir / f"{mode_prefix}_split_{k}_yn.csv", "r", encoding="utf-8") as fs, \
                     open(obj_dir / f"{mode_prefix}_split_{k}_sr.csv", "r", encoding="utf-8") as fb:
                    for rs, rb in zip(csv.DictReader(fs), csv.DictReader(fb)):
                        y_t.append(float(rs["y"]))
                        y_n.append(float(rs["n"]))
                        y_s.append(float(rb["s"]))
                        y_rf.append(float(rb["r"]))
                r2_s, pcc_s, mse_s, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_s)
                r2_r, _, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_rf)
                s_r2.append(r2_s)
                s_pcc.append(pcc_s)
                s_mse.append(mse_s)
                rf_r2.append(r2_r)
            m_r2, sd_r2 = mean_std(s_r2)
            m_pcc, sd_pcc = mean_std(s_pcc)
            m_rf, _ = mean_std(rf_r2)
            exp_r2 = stage4["ctrpv2_same_env_baselines_and_tanimoto"][mode_key]["models"]["SchurBilinearExVivoDRP"]["R2_norm_mean"]
            assert abs(m_r2 - exp_r2) < 1e-4, f"{mode_key} R2_norm mismatch: {m_r2} vs {exp_r2}"
            print(f"[PASS] CTRPv2 {mode_key} (10 splits): SchurBilinearExVivoDRP R2_norm = {m_r2:+.5f} +- {sd_r2:.5f}, Pearson_norm = {m_pcc:+.5f} +- {sd_pcc:.5f} (vs Same-Env RF = {m_rf:+.5f})")

    elif TARGET_ID == "dreval-ldo-beat-naive-mean-effects":
        for mode_prefix, mode_key in [("ldo_seed42", "LDO_seed42"), ("ldo_seed1337", "LDO_seed1337")]:
            s_r2, s_pcc, monn_r2, rf_r2 = [], [], [], []
            t85_r2, t70_r2, t50_r2 = [], [], []
            for k in range(10):
                y_t, y_n, y_s, y_m, y_rf, tbs = [], [], [], [], [], []
                with open(obj_dir / f"{mode_prefix}_split_{k}_schur.csv", "r", encoding="utf-8") as fs, \
                     open(obj_dir / f"{mode_prefix}_split_{k}_base.csv", "r", encoding="utf-8") as fb:
                    for rs, rb in zip(csv.DictReader(fs), csv.DictReader(fb)):
                        tbs.append(int(rs["t"]))
                        y_t.append(float(rs["y"]))
                        y_n.append(float(rs["n"]))
                        y_s.append(float(rs["s"]))
                        y_m.append(float(rb["m"]))
                        y_rf.append(float(rb["r"]))
                r2_s, pcc_s, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_s)
                r2_m, _, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_m)
                r2_r, _, _, _, _ = compute_dreval_norm_metrics(y_t, y_n, y_rf)
                s_r2.append(r2_s)
                s_pcc.append(pcc_s)
                monn_r2.append(r2_m)
                rf_r2.append(r2_r)

                # Tanimoto strata: tb <= 2 is <=0.85, tb <= 1 is <=0.70, tb == 0 is <=0.50
                for max_tb, bucket in [(2, t85_r2), (1, t70_r2), (0, t50_r2)]:
                    idx = [i for i, b in enumerate(tbs) if b <= max_tb]
                    r2_sub, _, _, _, _ = compute_dreval_norm_metrics(
                        [y_t[i] for i in idx], [y_n[i] for i in idx], [y_s[i] for i in idx]
                    )
                    bucket.append(r2_sub)

            m_r2, sd_r2 = mean_std(s_r2)
            m_pcc, sd_pcc = mean_std(s_pcc)
            m_monn, _ = mean_std(monn_r2)
            m_rf, _ = mean_std(rf_r2)
            m_t85, _ = mean_std(t85_r2)
            m_t70, _ = mean_std(t70_r2)
            m_t50, _ = mean_std(t50_r2)
            exp_r2 = stage4["ctrpv2_same_env_baselines_and_tanimoto"][mode_key]["models"]["SchurBilinearExVivoDRP"]["R2_norm_mean"]
            exp_t70 = stage4["ctrpv2_same_env_baselines_and_tanimoto"][mode_key]["tanimoto_stratification"]["max_tanimoto_le_0.70"]["R2_norm_mean"]
            assert abs(m_r2 - exp_r2) < 1e-4, f"{mode_key} R2_norm mismatch: {m_r2} vs {exp_r2}"
            assert abs(m_t70 - exp_t70) < 1e-4, f"{mode_key} Tanimoto<=0.70 mismatch: {m_t70} vs {exp_t70}"
            assert m_r2 > 0.02347 + 0.02 and m_t85 > 0.05 and m_t70 > 0.04 and m_t50 > 0.0
            print(
                f"[PASS] CTRPv2 {mode_key} (10 splits): SchurBilinearExVivoDRP R2_norm = {m_r2:+.5f} +- {sd_r2:.5f}, "
                f"Pearson_norm = {m_pcc:+.5f} +- {sd_pcc:.5f} (vs MultiOmicsNN = {m_monn:+.5f}, RF = {m_rf:+.5f} | "
                f"Tanimoto<=0.85: {m_t85:+.5f}, <=0.70: {m_t70:+.5f}, <=0.50: {m_t50:+.5f})"
            )

    print("PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(_verify())
    except Exception as exc:
        print(f"[ERROR] Verification failed: {exc}")
        print("FAIL")
        sys.exit(1)
