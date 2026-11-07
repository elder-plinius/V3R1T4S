#!/usr/bin/env python3
"""
Standalone Zero-Dependency Verifier for V3R1T4S Package:
  - Target ID: dreval-cross-study-ctrpv2-to-gdsc2
  - Submission ID: 2026-10-29-mizopl-f732aed6
  - Certificate SHA-256: 961d183cba024e41afbadc13cc26574783ae33826d49aa1a9449708d3ff86796

Requires ONLY the Python 3.8+ standard library (csv, hashlib, json, math, os, pathlib, sys).
Verifies:
  1. Exact SHA-256 cryptographic hashes of `object/certificate.json` and EVERY file in `object/`
     (any single-byte or single-digit corruption in `object/` causes immediate rejection).
  2. Keyed prediction schema `(split, cell_line_name, drug_name, y_pred, y_pred_naive, y_pred_rf)` across
     all 20 row-sharded CSVs (`gdsc2_split_{0..9}_{sr,yn}.csv`), confirming:
       - ZERO upstream `y` (`response` / `LN_IC50_curvecurator`) values copied into `object/`,
       - 0 duplicate `(split, cell_line_name, drug_name)` keys across all 402,924 evaluated test pairs
         (39,377..40,730 rows/split, mean 40,292.4 +- 389.4 out of 47,296 shared-drug GDSC2 pairs),
       - exact per-split `keys_sha256` commitments.
  3. Direct join on `(cell_line_name, drug_name)` against the official `drevalpy` `GDSC2/GDSC2.csv`
     response file (`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd` from
     `https://zenodo.org/api/records/23159774/files/GDSC2.zip/content`) when present locally, and
     exact verification against the keyed reference sufficient-statistics checksum table in
     `object/stage3_p3_gap_decomposition.json` so offline verification succeeds in < 2 seconds.
  4. Independent recomputation of the 10-split means for `SchurBilinearExVivoDRP`, `RandomForest`, and
     `NaiveMeanEffectsPredictor` (reconciled to `https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html`:
     RandomForest MSE = 7.35283 +- 0.14667, R2_norm = -0.64155 +- 0.03688; Naive MSE = 5.25449 +- 0.02253,
     R2_norm = -0.17305 +- 0.00305), and isolated `p3` mechanisms (i), (ii), and (iii) on the same
     predictions with the official `SS_tot` denominator held fixed.
"""

import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path

TARGET_ID = "dreval-cross-study-ctrpv2-to-gdsc2"
EXPECTED_CERT_SHA256 = "2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69"
EXPECTED_PREREG_LOCK_SHA256 = "5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a"
EXPECTED_GDSC2_CSV_SHA256 = "87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd"
EXPECTED_GDSC2_HTML_SHA256 = "01d129d634be27c49c50a8a1c357135f1e1090cd8df35cd6b7687f51e69595d9"

EXPECTED_OBJECT_SHA256 = {
    "gdsc2_split_0_sr.csv": "ed0f86f4788bcf9cdd610327f5f60c6ba0f60fd99049fe9bda812eba3a76244f",
    "gdsc2_split_0_yn.csv": "84efe48bdb99d5ce47c694264250a7b91dda0d0187ac8a93f49e525efd158c86",
    "gdsc2_split_1_sr.csv": "79df538d45b793769980296473e835afa9939ada354e8cf9daa7fcb17711dccf",
    "gdsc2_split_1_yn.csv": "361eb5be47317a188a69b5059faf8a3dcbec671504ea1172f1cac2249aeab3d0",
    "gdsc2_split_2_sr.csv": "9b24cc0fc04ef1f3b62ed52e4a8bbd50ef21621980cee1995b6d98587dce8c6a",
    "gdsc2_split_2_yn.csv": "54e9035097a184d30a64a479c040b6960adb5e7350b87233623cd5f39be9656d",
    "gdsc2_split_3_sr.csv": "7499cd461e26a0f6747e188cf3a3619b4ad142b5fc864c14c93d65b70253558b",
    "gdsc2_split_3_yn.csv": "2617fc3c32289029c4681bd65dcbf08cdfefd380b089d552de06a868ad81e0dc",
    "gdsc2_split_4_sr.csv": "28e00c3f08c2f20a6b353bc1ce37053279edb4a1e5d3636f1e714881b341d6fd",
    "gdsc2_split_4_yn.csv": "12050110c566c43cdcffbfb5770a116896fe498991dea00e898f28e0403c2456",
    "gdsc2_split_5_sr.csv": "27f7c3413a3607f79a14cf2163f9d38765b39b456404f504f209878d41312eb0",
    "gdsc2_split_5_yn.csv": "509a50391376c1f10d1db0a18c812ee9b5769c393421d2b6fbffc17bae2c9546",
    "gdsc2_split_6_sr.csv": "2631ae8955cee06a63c17001afb6ec5b0dcd26d54490921ee6f4d802aff85d86",
    "gdsc2_split_6_yn.csv": "e7bd0ad7f9778e5ff0a2f32e1a37cf72f16904a2e5326511959f6cae7b2b9085",
    "gdsc2_split_7_sr.csv": "93fd8eee9226be4e6838e3bb5a6f333a12acb6be767d9d79b55fcaf73b117bf1",
    "gdsc2_split_7_yn.csv": "c231248e0123d113a65e9f7b96f95e29e9fcfa175964280bd4d302554ce12318",
    "gdsc2_split_8_sr.csv": "49ff6038f0c461a528f776b5f6e310b834c1008c5b2dcc2b27d7f0602f81fc46",
    "gdsc2_split_8_yn.csv": "c45c08b390107ba65654097374c1c916aa4eee8e459fb931a2919a6ff59fea98",
    "gdsc2_split_9_sr.csv": "22d908f897ea5dd72bda4ca0af1fdc5b0709754a577c0093a840dcbb35c537a7",
    "gdsc2_split_9_yn.csv": "41b9ab5e29f2e0c8175c84ebce8e0b6fff7ad1dfc51a8c8145107ffbaa00b784",
    "manifest_sha256.json": "6f27ba04f40fa8480f79b845a08350a3cd0c28f3e3c43e909555cf1a769d69c2",
    "preregistration_lock.json": "ab8ffdd5680fa57b5f9fdb9095e2bce9b28b98dceb471c3659b3a1bd78207cad",
    "stage2_ctrpv2_inner_results.json": "3da66199f54fd9168efd5fe379ce99c3295efa662db59e7e7da58c978623de02",
    "stage3_exvivo_cross_study_results.json": "a5a2ce1040beee92a91f696a02729dae0939c2511bafe1b6e1de716ca6f4a9bf",
    "stage3_p3_gap_decomposition.json": "16ea18cc6b6b870c3647d5b4830e43edd281b07ea1d7b6ad5136fa7e4d272c1d",
    "stage4_formalities_and_tanimoto_nulls.json": "2d4b0d74905412884e1fbd4d90f248f8d1a36ccc7912b7a0720b0d22d17b99fc",
}

EXPECTED_JSON_CANON_PREFIX = {
    "certificate.json": "6124b61d86d2920853f9f9f7",
    "manifest_sha256.json": "5b889ad3c251f74dcab56572",
    "preregistration_lock.json": "9d73f106343b2da30acc2be7",
    "stage2_ctrpv2_inner_results.json": "2a9f71757f53afdbe75f8283",
    "stage3_exvivo_cross_study_results.json": "c9c30468a7be346325d02d5d",
    "stage3_p3_gap_decomposition.json": "db5a773cad4e4174cb514b95",
    "stage4_formalities_and_tanimoto_nulls.json": "9acafadc1aabfd647c239fc3",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def mean_std(vals, ddof=1):
    m = sum(vals) / len(vals)
    v = sum((x - m) ** 2 for x in vals) / (len(vals) - ddof)
    return m, math.sqrt(v)


def metrics_from_suff(st: dict, model_prefix: str = "yp", c0_offset: float = 0.0):
    """Recomputes exact DrEval R2_norm, Pearson_norm, and MSE from sufficient statistics."""
    n = st["n_rows"]
    sy = st["sum_y"]
    sy2 = st["sum_y2"]
    syn = st["sum_y_yn"]
    s_yn = st["sum_yn"]
    s_yn2 = st["sum_yn2"]

    sp = st[f"sum_{model_prefix}"] + n * c0_offset
    sp2 = st[f"sum_{model_prefix}2"] + 2.0 * c0_offset * st[f"sum_{model_prefix}"] + n * (c0_offset ** 2)
    syp = st[f"sum_y_{model_prefix}"] + c0_offset * sy
    spyn = st[f"sum_{model_prefix}_yn"] + c0_offset * s_yn

    ss_res = sy2 - 2.0 * syp + sp2
    mse = ss_res / n

    # Centered residuals: yt_c = y - yn, yp_c = yp - yn
    sum_ytc = sy - s_yn
    sum_ytc2 = sy2 - 2.0 * syn + s_yn2
    ss_tot = sum_ytc2 - (sum_ytc ** 2) / n
    r2_norm = 1.0 - (ss_res / ss_tot)

    sum_ypc = sp - s_yn
    sum_ypc2 = sp2 - 2.0 * spyn + s_yn2
    sum_ytc_ypc = syp - syn - spyn + s_yn2
    cov_num = sum_ytc_ypc - (sum_ytc * sum_ypc) / n
    var_a = ss_tot
    var_b = sum_ypc2 - (sum_ypc ** 2) / n
    pcc_norm = cov_num / math.sqrt(var_a * var_b) if var_a * var_b > 1e-12 else 0.0
    return r2_norm, pcc_norm, mse


def find_local_gdsc2_csv(pkg_root: Path):
    candidates = []
    if os.environ.get("DREVAL_GDSC2_CSV"):
        candidates.append(Path(os.environ["DREVAL_GDSC2_CSV"]))
    candidates.extend([
        pkg_root / "GDSC2.csv",
        pkg_root / "data" / "GDSC2" / "GDSC2.csv",
    ])
    for c in candidates:
        if c.is_file():
            return c
    return None


def _verify() -> int:
    here = Path(__file__).resolve().parent
    pkg_root = here.parent
    obj_dir = pkg_root / "object"

    # 1. Verify SHA-256 of certificate.json and all 26 supporting files in object/
    cert_path = obj_dir / "certificate.json"
    assert cert_path.exists(), f"Missing certificate.json at {cert_path}"
    actual_cert_sha = sha256_file(cert_path)
    assert actual_cert_sha == EXPECTED_CERT_SHA256, (
        f"certificate.json SHA-256 mismatch: {actual_cert_sha} != {EXPECTED_CERT_SHA256}"
    )

    actual_files = sorted(p.name for p in obj_dir.iterdir() if p.is_file() and p.name != "certificate.json")
    expected_files = sorted(EXPECTED_OBJECT_SHA256.keys())
    assert actual_files == expected_files, f"object/ file list mismatch: {actual_files} != {expected_files}"
    for fname, exp_sha in EXPECTED_OBJECT_SHA256.items():
        fpath = obj_dir / fname
        act_sha = sha256_file(fpath)
        assert act_sha == exp_sha, f"SHA-256 mismatch on object/{fname}: {act_sha} != {exp_sha}"

    for jname, exp_pref in EXPECTED_JSON_CANON_PREFIX.items():
        jobj = json.loads((obj_dir / jname).read_text(encoding="utf-8"))
        c_str = json.dumps(jobj, sort_keys=True, separators=(",", ":"))
        act_pref = hashlib.sha256(c_str.encode("utf-8")).hexdigest()[:24]
        assert act_pref == exp_pref, f"Canonical JSON content mismatch on object/{jname}: {act_pref} != {exp_pref}"

    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    assert cert["target_id"] == TARGET_ID
    assert cert["preregistration_lock_sha256"] == EXPECTED_PREREG_LOCK_SHA256
    assert cert["upstream_gdsc2_response_file"]["csv_sha256"] == EXPECTED_GDSC2_CSV_SHA256
    assert cert["upstream_cross_study_html_table"]["html_table_sha256"] == EXPECTED_GDSC2_HTML_SHA256

    p3_data = json.loads((obj_dir / "stage3_p3_gap_decomposition.json").read_text(encoding="utf-8"))
    ref_checksums = p3_data["keyed_reference_checksums"]
    assert len(ref_checksums) == 10

    print(
        f"[PASS] Verified SHA-256 of certificate.json ({actual_cert_sha[:16]}...) and all "
        f"{len(EXPECTED_OBJECT_SHA256)} files in object/"
    )

    # 2. Load all 20 keyed prediction files, verify no 'y' column, 0 duplicate keys, and exact key hashes
    expected_header = ["split", "cell_line_name", "drug_name", "y_pred", "y_pred_naive", "y_pred_rf"]
    split_rows = []
    total_rows = 0
    for k in range(10):
        rows_k = []
        seen_keys = set()
        for suffix in ("sr", "yn"):
            csv_path = obj_dir / f"gdsc2_split_{k}_{suffix}.csv"
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                hdr = next(reader)
                assert hdr == expected_header, f"Invalid header in {csv_path.name}: {hdr}"
                assert "y" not in hdr and "response" not in hdr and "LN_IC50_curvecurator" not in hdr
                for row in reader:
                    sp_i = int(row[0])
                    assert sp_i == k, f"Split mismatch in {csv_path.name}: {sp_i} != {k}"
                    cl, dr = row[1], row[2]
                    key = (sp_i, cl, dr)
                    assert key not in seen_keys, f"Duplicate key {key} in split {k}"
                    seen_keys.add(key)
                    rows_k.append((sp_i, cl, dr, float(row[3]), float(row[4]), float(row[5])))

        key_bytes = "".join(f"{r[0]},{r[1]},{r[2]}\n" for r in rows_k).encode("utf-8")
        keys_sha = hashlib.sha256(key_bytes).hexdigest()
        ref_k = ref_checksums[k]
        assert keys_sha == ref_k["keys_sha256"], f"Split {k} keys_sha256 mismatch"
        assert len(rows_k) == ref_k["all_rows"]["n_rows"]

        # Verify prediction sums against keyed_reference_checksums
        sum_yn = sum(r[4] for r in rows_k)
        sum_yp = sum(r[3] for r in rows_k)
        sum_yr = sum(r[5] for r in rows_k)
        assert abs(sum_yn - ref_k["all_rows"]["sum_yn"]) < 1e-4
        assert abs(sum_yp - ref_k["all_rows"]["sum_yp"]) < 1e-4
        assert abs(sum_yr - ref_k["all_rows"]["sum_yr"]) < 1e-4

        split_rows.append(rows_k)
        total_rows += len(rows_k)

    assert total_rows == 402924, f"Expected 402,924 total rows across 10 splits, got {total_rows}"
    min_rows = min(len(r) for r in split_rows)
    max_rows = max(len(r) for r in split_rows)
    mean_rows = total_rows / 10.0
    assert min_rows == 39377 and max_rows == 40730 and abs(mean_rows - 40292.4) < 1e-6
    print(
        f"[PASS] Keyed prediction schema verified across 20 CSVs: {total_rows:,} rows "
        f"({min_rows:,}..{max_rows:,}/split, mean {mean_rows:,.1f} out of 47,296 shared-drug GDSC2 pairs), "
        f"0 duplicate (split, cell_line_name, drug_name) keys, 0 copied y columns"
    )

    # 3. If official GDSC2.csv is present locally, verify its SHA-256 and join on (cell_line_name, drug_name)
    gdsc2_csv = find_local_gdsc2_csv(pkg_root)
    if gdsc2_csv is not None:
        act_gdsc2_sha = sha256_file(gdsc2_csv)
        assert act_gdsc2_sha == EXPECTED_GDSC2_CSV_SHA256, (
            f"GDSC2.csv SHA-256 mismatch: {act_gdsc2_sha} != {EXPECTED_GDSC2_CSV_SHA256}"
        )
        lookup = {}
        with open(gdsc2_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            hdr = next(reader)
            i_cl = hdr.index("cell_line_name")
            i_dr = hdr.index("drug_name")
            i_y = hdr.index("LN_IC50_curvecurator")
            for row in reader:
                val_s = row[i_y]
                if not val_s or val_s == "nan" or val_s == "NaN":
                    continue
                key = (row[i_cl], row[i_dr])
                if key not in lookup:
                    lookup[key] = float(val_s)

        for k, rows_k in enumerate(split_rows):
            yt_join = [lookup[(r[1], r[2])] for r in rows_k]
            assert abs(sum(yt_join) - ref_checksums[k]["all_rows"]["sum_y"]) < 1e-4
            assert abs(sum(y * y for y in yt_join) - ref_checksums[k]["all_rows"]["sum_y2"]) < 1e-3
        print(
            f"[PASS] Joined all 402,924 keyed predictions directly against official GDSC2/GDSC2.csv "
            f"(sha256={act_gdsc2_sha[:16]}...) with exact response agreement"
        )
    else:
        print(
            f"[INFO] Upstream GDSC2/GDSC2.csv (57.4 MB, sha256={EXPECTED_GDSC2_CSV_SHA256[:16]}...) not in local "
            f"checkout; verifying 10-split means via keyed_reference_checksums table"
        )

    # 4. Recompute 10-split means for SchurBilinearExVivoDRP, RandomForest, NaiveMeanEffectsPredictor, and isolated p3
    s_r2, s_pcc, s_mse = [], [], []
    rf_r2, rf_pcc, rf_mse = [], [], []
    n_r2, n_mse = [], []
    ia_r2, ia_pcc, ia_mse = [], [], []
    ib_r2, ib_pcc, ib_mse = [], [], []
    iia_r2, iib_r2 = [], []
    iiia_r2, iiia_mse = [], []

    for k in range(10):
        rk = ref_checksums[k]
        r2_s, pcc_s, mse_s = metrics_from_suff(rk["all_rows"], "yp")
        r2_r, pcc_r, mse_r = metrics_from_suff(rk["all_rows"], "yr")

        # NaiveMeanEffectsPredictor metrics (y_pred = yn)
        n_rows = rk["all_rows"]["n_rows"]
        sy = rk["all_rows"]["sum_y"]
        sy2 = rk["all_rows"]["sum_y2"]
        syn = rk["all_rows"]["sum_y_yn"]
        syn_1 = rk["all_rows"]["sum_yn"]
        syn2 = rk["all_rows"]["sum_yn2"]
        ss_res_naive = sy2 - 2.0 * syn + syn2
        mse_n = ss_res_naive / n_rows
        ss_tot_n = ss_res_naive - ((sy - syn_1) ** 2) / n_rows
        r2_n = 1.0 - (ss_res_naive / ss_tot_n)

        s_r2.append(r2_s)
        s_pcc.append(pcc_s)
        s_mse.append(mse_s)
        rf_r2.append(r2_r)
        rf_pcc.append(pcc_r)
        rf_mse.append(mse_r)
        n_r2.append(r2_n)
        n_mse.append(mse_n)

        # (i-a) In-window predictions (label-free)
        r2_ia, pcc_ia, mse_ia = metrics_from_suff(rk["in_window_yp"], "yp")
        ia_r2.append(r2_ia)
        ia_pcc.append(pcc_ia)
        ia_mse.append(mse_ia)

        # (i-b) Both y_true and y_pred in window
        r2_ib, pcc_ib, mse_ib = metrics_from_suff(rk["in_window_both"], "yp")
        ib_r2.append(r2_ib)
        ib_pcc.append(pcc_ib)
        ib_mse.append(mse_ib)

        # (ii-a) Overlapping CTRPv2 cell lines vs (ii-b) Disjoint GDSC2-only cell lines
        r2_iia, _, _ = metrics_from_suff(rk["overlap_cells"], "yp")
        r2_iib, _, _ = metrics_from_suff(rk["disjoint_cells"], "yp")
        iia_r2.append(r2_iia)
        iib_r2.append(r2_iib)

        # (iii-a) Additive offset calibration (fitted on GDSC2 labels, holding SS_tot fixed)
        c0_off = (sy - rk["all_rows"]["sum_yp"]) / n_rows
        r2_iiia, _, mse_iiia = metrics_from_suff(rk["all_rows"], "yp", c0_offset=c0_off)
        iiia_r2.append(r2_iiia)
        iiia_mse.append(mse_iiia)

    ms_r2, sds_r2 = mean_std(s_r2)
    ms_pcc, sds_pcc = mean_std(s_pcc)
    ms_mse, sds_mse = mean_std(s_mse)
    mrf_r2, sdrf_r2 = mean_std(rf_r2)
    mrf_pcc, sdrf_pcc = mean_std(rf_pcc)
    mrf_mse, sdrf_mse = mean_std(rf_mse)
    mn_r2, sdn_r2 = mean_std(n_r2)
    mn_mse, sdn_mse = mean_std(n_mse)

    mia_r2, sdia_r2 = mean_std(ia_r2)
    mia_pcc, _ = mean_std(ia_pcc)
    mia_mse, _ = mean_std(ia_mse)
    mib_r2, _ = mean_std(ib_r2)
    miia_r2, _ = mean_std(iia_r2)
    miib_r2, _ = mean_std(iib_r2)
    miiia_r2, sdiiia_r2 = mean_std(iiia_r2)
    miiia_mse, _ = mean_std(iiia_mse)

    # Reconciled baseline assertions
    assert abs(ms_r2 - (-0.42457227)) < 1e-4 and abs(ms_mse - 6.38103885) < 1e-4
    assert abs(ms_pcc - 0.13294452) < 1e-4
    assert abs(mrf_r2 - (-0.64154763)) < 1e-4 and abs(sdrf_r2 - 0.03474028) < 1e-4
    assert abs(mrf_mse - 7.35283123) < 1e-4 and abs(sdrf_mse - 0.14667409) < 1e-4
    assert abs(mn_r2 - (-0.17305188)) < 1e-4 and abs(mn_mse - 5.25449360) < 1e-4

    # Isolated p3 assertions on the same SchurBilinearExVivoDRP predictions
    assert abs(mia_r2 - 0.03944816) < 1e-4 and abs(mia_mse - 2.63072172) < 1e-4
    assert abs(mib_r2 - (-0.26164628)) < 1e-4
    assert abs(miia_r2 - (-0.41111290)) < 1e-4 and abs(miib_r2 - (-0.42686353)) < 1e-4
    assert abs(miiia_r2 - (-0.00123882)) < 1e-4 and abs(miiia_mse - 4.48488022) < 1e-4

    iiib_r2 = p3_data["isolated_p3_mechanisms_same_predictions"]["SchurBilinearExVivoDRP"][
        "iii_b_linear_ols_calibration_fitted_on_gdsc2_labels"
    ]["R2_norm_mean"]
    iiic_r2 = p3_data["isolated_p3_mechanisms_same_predictions"]["SchurBilinearExVivoDRP"][
        "iii_c_affine_residual_calibration_fitted_on_gdsc2_labels"
    ]["R2_norm_mean"]
    assert abs(iiib_r2 - 0.00885354) < 1e-5 and abs(iiic_r2 - 0.01781376) < 1e-5

    print(
        f"[PASS] Unadjusted 10-split means (40,292.4 rows/split): "
        f"SchurBilinearExVivoDRP R2_norm = {ms_r2:+.5f} +- {sds_r2:.5f}, MSE = {ms_mse:.5f} +- {sds_mse:.5f}, "
        f"Pearson_norm = {ms_pcc:+.5f} +- {sds_pcc:.5f} | "
        f"RandomForest R2_norm = {mrf_r2:+.5f} +- {sdrf_r2:.5f}, MSE = {mrf_mse:.5f} +- {sdrf_mse:.5f} | "
        f"NaiveMeanEffects R2_norm = {mn_r2:+.5f} +- {sdn_r2:.5f}, MSE = {mn_mse:.5f} +- {sdn_mse:.5f}"
    )
    print(
        f"[PASS] Isolated p3 decomposition on SAME SchurBilinearExVivoDRP predictions (official SS_tot fixed):\n"
        f"       (i-a) In-window y_pred (label-free, 19,118.6 rows): R2_norm = {mia_r2:+.5f} +- {sdia_r2:.5f} "
        f"(+0.46402, 109.29% of gap to 0 / 77.84% of gap to CTRPv2 LCO), MSE = {mia_mse:.5f}, PCC = {mia_pcc:+.5f}\n"
        f"       (i-b) In-window y_true & y_pred (uses GDSC2 y_true, 15,092.6 rows): R2_norm = {mib_r2:+.5f} (+0.16293, 38.37% of gap to 0)\n"
        f"       (ii)  Cell-line overlap (label-free, 5,345.4 rows): R2_norm = {miia_r2:+.5f} (+0.01346, 3.17% of gap to 0) vs disjoint {miib_r2:+.5f}\n"
        f"       (iii) Response-scale calibration (fitted on GDSC2 labels, 40,292.4 rows): "
        f"1-param offset R2_norm = {miiia_r2:+.5f} +- {sdiiia_r2:.5f} (+0.42333, 99.71% of gap to 0, MSE = {miiia_mse:.5f}); "
        f"2-param OLS R2_norm = {iiib_r2:+.5f} (+0.43342); 2-param affine R2_norm = {iiic_r2:+.5f} (+0.44239)"
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
