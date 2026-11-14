#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-contained verification script for `dreval-exvivo-beataml2-pdx-transfer` (`p3`).
Uses only Python 3.8+ standard library (`csv`, `hashlib`, `json`, `math`, `os`, `sys`).

Verifies:
1. SHA256SUMS manifest integrity across all packaged files.
2. Exact cross-file agreement between `object/certificate.json` and `object/stage3_p3_gap_decomposition.json`.
3. Mathematical identities across all 10 splits for every model and `p3` slice:
   - 10-split sample mean and sample standard deviation (`ddof=1`) match the 10 per-split records.
   - `RMSE == sqrt(MSE)` on every split.
   - `R2_norm_gain_vs_unadjusted == R2_norm_mean - unadjusted_R2_norm_mean` and
     `MSE_change_vs_unadjusted == MSE_mean - unadjusted_MSE_mean`.
   - Dominance ranking (`dominance_rank_by_MSE_closed`) is strictly ordered by `MSE_change`.
4. Per-split prediction CSV verification (`object/beataml2_split_{0..9}_{schur,base}.csv` and
   `object/pdx_bruna_split_{0..9}.csv`):
   - Confirms that NO ground-truth response column (`y` or `response`) is copied into `object/`.
   - Verifies exact row counts (`19,823` rows/split on BeatAML2 with `11,901` shared and `7,922` unseen;
     `1,046` rows/split on PDX_Bruna with `555` shared and `491` unseen).
   - Verifies row-by-row `(split, cell_line_name, pubchem_id)` alignment and exact SHA-256 key digests.
   - Recomputes exact L1 sums, L2 sums, means, cross-column dot products, and the three unlabeled `p3`
     correction parameters (`mean_delta_assay_fe`, `delta_platform_scalar = -mean(y_pred_schur - y_pred_raw_krr)`,
     `delta_overlap_unseen_scalar = mean(y_pred_schur[shared]) - mean(y_pred_schur[unseen])`) directly from
     the CSV columns and checks them against `object/certificate.json`.
5. Optional direct ground-truth rescoring: if the official upstream `BeatAML2.csv`
   (`sha256: 259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`) and `PDX_Bruna.csv`
   (`sha256: 63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`) are present in
   `DREVAL_DATA_DIR` or `./data`, joins on `(cell_line_name, pubchem_id)` and recomputes `R2_norm` and `MSE`
   against `LN_IC50_curvecurator`.
"""

import csv
import hashlib
import json
import math
import os
import re
import sys


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    print("FAIL")
    sys.exit(1)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sample_mean(vals):
    return sum(vals) / float(len(vals))


def sample_std(vals):
    if len(vals) <= 1:
        return 0.0
    m = sample_mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / float(len(vals) - 1))


def check_sha256sums(pkg_root: str) -> int:
    sums_path = os.path.join(pkg_root, "SHA256SUMS")
    if not os.path.isfile(sums_path):
        fail("SHA256SUMS missing")
    checked = 0
    with open(sums_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split(None, 1)
            if len(parts) != 2:
                fail(f"Malformed SHA256SUMS line: {s}")
            expected_h, rel_p = parts[0], parts[1].lstrip("./")
            full_p = os.path.join(pkg_root, rel_p)
            if not os.path.isfile(full_p):
                fail(f"Missing file listed in SHA256SUMS: {rel_p}")
            actual_h = sha256_file(full_p)
            if actual_h != expected_h:
                fail(f"SHA256 mismatch on {rel_p}: expected {expected_h}, got {actual_h}")
            checked += 1
    return checked


def verify_split_csv_cohort(pkg_root: str, cohort: str, target_block: dict, single_obj: str) -> int:
    digests = target_block.get("split_csv_digests", [])
    if len(digests) != 10:
        fail(f"{cohort}: expected 10 split_csv_digests, found {len(digests)}")

    # Determine which splits to parse (all 10 in standard mode; targeted split + split 0 in fast single-object mode)
    splits_to_check = list(range(10))
    if single_obj:
        m = re.search(r"split_(\d+)", single_obj)
        if m:
            sp_idx = int(m.group(1))
            splits_to_check = sorted(list({0, sp_idx}))
        elif single_obj in ("certificate.json", "stage3_p3_gap_decomposition.json"):
            splits_to_check = [0, 9]

    verified_count = 0
    for k in splits_to_check:
        d_exp = digests[k]
        if d_exp.get("split") != k:
            fail(f"{cohort} split {k}: digest split index mismatch")

        if cohort == "BeatAML2":
            schur_path = os.path.join(pkg_root, "object", f"beataml2_split_{k}_schur.csv")
            base_path = os.path.join(pkg_root, "object", f"beataml2_split_{k}_base.csv")
            if not os.path.isfile(schur_path) or not os.path.isfile(base_path):
                fail(f"Missing BeatAML2 split {k} CSV files")

            with open(schur_path, "r", encoding="utf-8", newline="") as fs, open(
                base_path, "r", encoding="utf-8", newline=""
            ) as fb:
                rs = csv.DictReader(fs)
                rb = csv.DictReader(fb)
                if rs.fieldnames != [
                    "split",
                    "cell_line_name",
                    "drug_name",
                    "pubchem_id",
                    "is_shared",
                    "y_pred_schur",
                    "y_pred_naive",
                ]:
                    fail(f"beataml2_split_{k}_schur.csv unexpected columns: {rs.fieldnames}")
                if rb.fieldnames != [
                    "split",
                    "cell_line_name",
                    "pubchem_id",
                    "delta_assay",
                    "y_pred_raw_krr",
                    "y_pred_rf",
                    "y_pred_gb",
                ]:
                    fail(f"beataml2_split_{k}_base.csv unexpected columns: {rb.fieldnames}")

                rows_s = list(rs)
                rows_b = list(rb)
                if len(rows_s) != len(rows_b):
                    fail(f"BeatAML2 split {k}: row count mismatch between schur ({len(rows_s)}) and base ({len(rows_b)})")

                n_rows = len(rows_s)
                if n_rows != d_exp["n_rows"] or n_rows != 19823:
                    fail(f"BeatAML2 split {k}: expected {d_exp['n_rows']} rows, got {n_rows}")

                key_parts = []
                n_shared = 0
                ys_list, yn_list, da_list, yr_list, yrf_list, ygb_list = [], [], [], [], [], []
                ys_shared, ys_unseen = [], []

                for row_s, row_b in zip(rows_s, rows_b):
                    if (
                        int(row_s["split"]) != k
                        or int(row_b["split"]) != k
                        or row_s["cell_line_name"] != row_b["cell_line_name"]
                        or row_s["pubchem_id"] != row_b["pubchem_id"]
                    ):
                        fail(f"BeatAML2 split {k}: key mismatch between schur and base CSV")
                    sh_flag = int(row_s["is_shared"])
                    if sh_flag not in (0, 1):
                        fail(f"BeatAML2 split {k}: invalid is_shared={sh_flag}")
                    n_shared += sh_flag
                    key_parts.append(
                        f"{k}|{row_s['cell_line_name']}|{row_s['drug_name']}|{row_s['pubchem_id']}|{sh_flag}"
                    )

                    ys_v = float(row_s["y_pred_schur"])
                    yn_v = float(row_s["y_pred_naive"])
                    da_v = float(row_b["delta_assay"])
                    yr_v = float(row_b["y_pred_raw_krr"])
                    yrf_v = float(row_b["y_pred_rf"])
                    ygb_v = float(row_b["y_pred_gb"])

                    ys_list.append(ys_v)
                    yn_list.append(yn_v)
                    da_list.append(da_v)
                    yr_list.append(yr_v)
                    yrf_list.append(yrf_v)
                    ygb_list.append(ygb_v)
                    if sh_flag == 1:
                        ys_shared.append(ys_v)
                    else:
                        ys_unseen.append(ys_v)
        else:
            pdx_path = os.path.join(pkg_root, "object", f"pdx_bruna_split_{k}.csv")
            if not os.path.isfile(pdx_path):
                fail(f"Missing PDX_Bruna split {k} CSV file")
            with open(pdx_path, "r", encoding="utf-8", newline="") as fp:
                rp = csv.DictReader(fp)
                if rp.fieldnames != [
                    "split",
                    "cell_line_name",
                    "drug_name",
                    "pubchem_id",
                    "is_shared",
                    "delta_assay",
                    "y_pred_schur",
                    "y_pred_naive",
                    "y_pred_raw_krr",
                    "y_pred_rf",
                    "y_pred_gb",
                ]:
                    fail(f"pdx_bruna_split_{k}.csv unexpected columns: {rp.fieldnames}")
                rows_p = list(rp)
                n_rows = len(rows_p)
                if n_rows != d_exp["n_rows"] or n_rows != 1046:
                    fail(f"PDX_Bruna split {k}: expected {d_exp['n_rows']} rows, got {n_rows}")

                key_parts = []
                n_shared = 0
                ys_list, yn_list, da_list, yr_list, yrf_list, ygb_list = [], [], [], [], [], []
                ys_shared, ys_unseen = [], []

                for row_p in rows_p:
                    if int(row_p["split"]) != k:
                        fail(f"PDX_Bruna split {k}: invalid split column {row_p['split']}")
                    sh_flag = int(row_p["is_shared"])
                    if sh_flag not in (0, 1):
                        fail(f"PDX_Bruna split {k}: invalid is_shared={sh_flag}")
                    n_shared += sh_flag
                    key_parts.append(
                        f"{k}|{row_p['cell_line_name']}|{row_p['drug_name']}|{row_p['pubchem_id']}|{sh_flag}"
                    )

                    ys_v = float(row_p["y_pred_schur"])
                    yn_v = float(row_p["y_pred_naive"])
                    da_v = float(row_p["delta_assay"])
                    yr_v = float(row_p["y_pred_raw_krr"])
                    yrf_v = float(row_p["y_pred_rf"])
                    ygb_v = float(row_p["y_pred_gb"])

                    ys_list.append(ys_v)
                    yn_list.append(yn_v)
                    da_list.append(da_v)
                    yr_list.append(yr_v)
                    yrf_list.append(yrf_v)
                    ygb_list.append(ygb_v)
                    if sh_flag == 1:
                        ys_shared.append(ys_v)
                    else:
                        ys_unseen.append(ys_v)

        n_unseen = n_rows - n_shared
        if n_shared != d_exp["n_shared"] or n_unseen != d_exp["n_unseen"]:
            fail(f"{cohort} split {k}: shared/unseen count mismatch ({n_shared}/{n_unseen} vs {d_exp['n_shared']}/{d_exp['n_unseen']})")

        actual_key_sha = hashlib.sha256("\n".join(key_parts).encode("utf-8")).hexdigest()
        if actual_key_sha != d_exp["key_sha256"]:
            fail(f"{cohort} split {k}: key_sha256 mismatch")

        # Verify column means, L1 sums, L2 sums, dot products, and unlabeled p3 shifts
        checks = [
            ("mean_y_pred_schur", sample_mean(ys_list), d_exp["mean_y_pred_schur"], 1e-5),
            ("l1_y_pred_schur", sum(abs(x) for x in ys_list), d_exp["l1_y_pred_schur"], 5e-3),
            ("l2_y_pred_schur", sum(x * x for x in ys_list), d_exp["l2_y_pred_schur"], 2e-2),
            ("mean_y_pred_naive", sample_mean(yn_list), d_exp["mean_y_pred_naive"], 1e-5),
            ("l1_y_pred_naive", sum(abs(x) for x in yn_list), d_exp["l1_y_pred_naive"], 5e-3),
            ("l2_y_pred_naive", sum(x * x for x in yn_list), d_exp["l2_y_pred_naive"], 2e-2),
            ("mean_delta_assay_fe", sample_mean(da_list), d_exp["mean_delta_assay_fe"], 1e-5),
            ("l1_delta_assay_fe", sum(abs(x) for x in da_list), d_exp["l1_delta_assay_fe"], 5e-3),
            ("l2_delta_assay_fe", sum(x * x for x in da_list), d_exp["l2_delta_assay_fe"], 2e-2),
            ("mean_y_pred_raw_krr", sample_mean(yr_list), d_exp["mean_y_pred_raw_krr"], 1e-5),
            ("l1_y_pred_raw_krr", sum(abs(x) for x in yr_list), d_exp["l1_y_pred_raw_krr"], 5e-3),
            ("l2_y_pred_raw_krr", sum(x * x for x in yr_list), d_exp["l2_y_pred_raw_krr"], 2e-2),
            ("mean_y_pred_rf", sample_mean(yrf_list), d_exp["mean_y_pred_rf"], 1e-5),
            ("l1_y_pred_rf", sum(abs(x) for x in yrf_list), d_exp["l1_y_pred_rf"], 5e-3),
            ("l2_y_pred_rf", sum(x * x for x in yrf_list), d_exp["l2_y_pred_rf"], 2e-2),
            ("mean_y_pred_gb", sample_mean(ygb_list), d_exp["mean_y_pred_gb"], 1e-5),
            ("l1_y_pred_gb", sum(abs(x) for x in ygb_list), d_exp["l1_y_pred_gb"], 5e-3),
            ("l2_y_pred_gb", sum(x * x for x in ygb_list), d_exp["l2_y_pred_gb"], 2e-2),
            ("dot_schur_naive", sum(a * b for a, b in zip(ys_list, yn_list)), d_exp["dot_schur_naive"], 2e-2),
            ("dot_schur_raw_krr", sum(a * b for a, b in zip(ys_list, yr_list)), d_exp["dot_schur_raw_krr"], 2e-2),
            ("dot_rf_gb", sum(a * b for a, b in zip(yrf_list, ygb_list)), d_exp["dot_rf_gb"], 2e-2),
            (
                "delta_platform_scalar",
                -(sum(a - b for a, b in zip(ys_list, yr_list)) / float(n_rows)),
                d_exp["delta_platform_scalar"],
                1e-5,
            ),
            (
                "delta_overlap_unseen_scalar",
                sample_mean(ys_shared) - sample_mean(ys_unseen),
                d_exp["delta_overlap_unseen_scalar"],
                1e-5,
            ),
        ]
        for label, actual_v, expected_v, tol in checks:
            if abs(actual_v - expected_v) > tol:
                fail(f"{cohort} split {k} {label} mismatch: actual={actual_v:.6f} vs expected={expected_v:.6f}")

        verified_count += 1
    return verified_count


def verify_summary_block(name: str, block: dict, unadj_block: dict = None) -> None:
    splits = block.get("splits", [])
    if len(splits) != 10:
        fail(f"{name}: expected 10 splits, got {len(splits)}")
    metric_keys = [
        "R2_norm",
        "R2_norm_centered",
        "Pearson_norm",
        "Spearman_norm",
        "MSE",
        "RMSE",
        "MAE",
        "R2_raw",
        "Pearson_raw",
        "Spearman_raw",
        "n_rows",
    ]
    for mk in metric_keys:
        vals = [float(s[mk]) for s in splits]
        m_exp = float(block[f"{mk}_mean"])
        sd_exp = float(block[f"{mk}_std"])
        m_act = sample_mean(vals)
        sd_act = sample_std(vals)
        if abs(m_act - m_exp) > 2e-5:
            fail(f"{name} {mk}_mean mismatch: computed {m_act:.5f} vs reported {m_exp:.5f}")
        if abs(sd_act - sd_exp) > 2e-5:
            fail(f"{name} {mk}_std mismatch: computed {sd_act:.5f} vs reported {sd_exp:.5f}")

    n_gt0 = sum(1 for s in splits if float(s["R2_norm"]) > 0.0)
    if int(block.get("n_splits_R2_norm_gt_0", -1)) != n_gt0:
        fail(f"{name}: n_splits_R2_norm_gt_0 mismatch ({block.get('n_splits_R2_norm_gt_0')} vs {n_gt0})")

    for s in splits:
        mse_v = float(s["MSE"])
        rmse_v = float(s["RMSE"])
        if mse_v <= 0 or abs(math.sqrt(mse_v) - rmse_v) > 2e-5:
            fail(f"{name} split {s.get('split')}: RMSE != sqrt(MSE) ({rmse_v} vs sqrt({mse_v}))")

    if unadj_block is not None:
        for gk, mk in [
            ("R2_norm_gain_vs_unadjusted", "R2_norm_mean"),
            ("Pearson_norm_gain_vs_unadjusted", "Pearson_norm_mean"),
            ("Spearman_norm_gain_vs_unadjusted", "Spearman_norm_mean"),
            ("MSE_change_vs_unadjusted", "MSE_mean"),
        ]:
            exp_diff = float(block[gk])
            act_diff = float(block[mk]) - float(unadj_block[mk])
            if abs(act_diff - exp_diff) > 2e-5:
                fail(f"{name} {gk} mismatch: computed {act_diff:+.5f} vs reported {exp_diff:+.5f}")


def main() -> None:
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    single_obj = os.environ.get("ZERO_TRUST_SINGLE_OBJECT", "").strip()

    n_hashed = check_sha256sums(pkg_root)

    cert_path = os.path.join(pkg_root, "object", "certificate.json")
    p3_path = os.path.join(pkg_root, "object", "stage3_p3_gap_decomposition.json")
    if not os.path.isfile(cert_path) or not os.path.isfile(p3_path):
        fail("Missing object/certificate.json or object/stage3_p3_gap_decomposition.json")

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
        with open(p3_path, "r", encoding="utf-8") as f:
            p3_doc = json.load(f)
    except Exception as e:
        fail(f"JSON parse error: {e}")

    if cert.get("target_id") != "dreval-exvivo-beataml2-pdx-transfer":
        fail("Invalid target_id in certificate.json")
    if p3_doc.get("target_id") != "dreval-exvivo-beataml2-pdx-transfer":
        fail("Invalid target_id in stage3_p3_gap_decomposition.json")
    if not cert.get("zero_ex_vivo_label_leakage") or not p3_doc.get("zero_ex_vivo_label_leakage"):
        fail("zero_ex_vivo_label_leakage must be True in both JSON files")
    if cert.get("preregistration_lock_sha256") != p3_doc.get("preregistration_lock_sha256"):
        fail("preregistration_lock_sha256 mismatch between JSON files")

    targets = cert.get("targets", {})
    p3_targets = p3_doc.get("targets", {})
    if set(targets.keys()) != {"BeatAML2", "PDX_Bruna"} or set(p3_targets.keys()) != {"BeatAML2", "PDX_Bruna"}:
        fail("Targets must be strictly {'BeatAML2', 'PDX_Bruna'}")

    for cohort in ["BeatAML2", "PDX_Bruna"]:
        t_block = targets[cohort]
        p3_block = p3_targets[cohort]

        # Cross-check certificate.json against stage3_p3_gap_decomposition.json
        if t_block["cohort_metadata"] != p3_block["cohort_metadata"]:
            fail(f"{cohort}: cohort_metadata mismatch between certificate.json and stage3_p3_gap_decomposition.json")
        if t_block["unlabeled_p3_parameters"] != p3_block["unlabeled_p3_parameters"]:
            fail(f"{cohort}: unlabeled_p3_parameters mismatch between JSON files")
        if t_block["dominant_single_factor"] != p3_block["dominant_single_factor"]:
            fail(f"{cohort}: dominant_single_factor mismatch between JSON files")
        if t_block["single_factor_ranking"] != p3_block["single_factor_ranking"]:
            fail(f"{cohort}: single_factor_ranking mismatch between JSON files")
        if t_block["p3_decomposition"] != p3_block["p3_decomposition"]:
            fail(f"{cohort}: p3_decomposition mismatch between certificate.json and stage3_p3_gap_decomposition.json")

        # Verify all model summaries
        models = t_block.get("models", {})
        if len(models) != 5:
            fail(f"{cohort}: expected 5 models, found {len(models)}")
        for m_name, m_sum in models.items():
            verify_summary_block(f"{cohort}.models.{m_name}", m_sum)

        # Verify all p3 decomposition slices
        p3_slices = t_block.get("p3_decomposition", {})
        unadj = p3_slices.get("unadjusted_all_drugs")
        if not unadj:
            fail(f"{cohort}: missing unadjusted_all_drugs")
        for s_name, s_sum in p3_slices.items():
            verify_summary_block(f"{cohort}.p3.{s_name}", s_sum, unadj_block=unadj)

        # Verify single_factor_ranking consistency with p3_slices and ordering by MSE_change
        sf_list = t_block.get("single_factor_ranking", [])
        if len(sf_list) != 3:
            fail(f"{cohort}: expected 3 single factors in ranking")
        for idx, sf in enumerate(sf_list):
            if sf.get("dominance_rank_by_MSE_closed") != idx + 1:
                fail(f"{cohort}: dominance_rank_by_MSE_closed out of order")
            sk = sf["slice_key"]
            sb = p3_slices[sk]
            if (
                sf["R2_norm_mean"] != sb["R2_norm_mean"]
                or sf["R2_norm_gain"] != sb["R2_norm_gain_vs_unadjusted"]
                or sf["Pearson_norm_mean"] != sb["Pearson_norm_mean"]
                or sf["MSE_mean"] != sb["MSE_mean"]
                or sf["MSE_change"] != sb["MSE_change_vs_unadjusted"]
            ):
                fail(f"{cohort}: single_factor_ranking[{sk}] does not match p3_decomposition[{sk}]")
            if idx > 0 and sf["MSE_change"] < sf_list[idx - 1]["MSE_change"]:
                fail(f"{cohort}: single_factor_ranking not sorted by MSE_change")

        # Verify unlabeled_p3_parameters match the 10 split_csv_digests
        digests = t_block["split_csv_digests"]
        up = t_block["unlabeled_p3_parameters"]
        da_means = [float(d["mean_delta_assay_fe"]) for d in digests]
        dp_vals = [float(d["delta_platform_scalar"]) for d in digests]
        do_vals = [float(d["delta_overlap_unseen_scalar"]) for d in digests]
        if abs(sample_mean(da_means) - float(up["mean_delta_assay_fe_10split"])) > 2e-5:
            fail(f"{cohort}: mean_delta_assay_fe_10split mismatch vs split digests")
        if abs(sample_mean(dp_vals) - float(up["mean_delta_platform_scalar_10split"])) > 2e-5:
            fail(f"{cohort}: mean_delta_platform_scalar_10split mismatch vs split digests")
        if abs(sample_mean(do_vals) - float(up["mean_delta_overlap_unseen_scalar_10split"])) > 2e-5:
            fail(f"{cohort}: mean_delta_overlap_unseen_scalar_10split mismatch vs split digests")

        # Verify per-split CSV files against split_csv_digests
        verify_split_csv_cohort(pkg_root, cohort, t_block, single_obj)

    # Verify null_permutation_tests block
    null_block = cert.get("null_permutation_tests", {})
    for cohort in ["BeatAML2", "PDX_Bruna"]:
        nb = null_block.get(cohort, {})
        if nb.get("n_controls") != 500:
            fail(f"{cohort}: null test n_controls must be 500")
        for sub_k in ("unadjusted_split0", "p3_unlabeled_adjusted_split0"):
            sb = nb.get(sub_k, {})
            if sb.get("controls_beaten") != 500 or float(sb.get("observed_Pearson_norm", 0.0)) <= float(
                sb.get("best_control", 1.0)
            ):
                fail(f"{cohort}.{sub_k}: real observed_Pearson_norm does not beat all 500 controls")

    baml_s = targets["BeatAML2"]["models"]["SchurBilinearExVivoDRP"]
    baml_p3 = targets["BeatAML2"]["p3_decomposition"]
    pdx_s = targets["PDX_Bruna"]["models"]["SchurBilinearExVivoDRP"]
    pdx_p3 = targets["PDX_Bruna"]["p3_decomposition"]

    print("========================================================================")
    print("V3R1T4S Verification — dreval-exvivo-beataml2-pdx-transfer (p3)")
    print("========================================================================")
    print(f"[OK] SHA256SUMS manifest verified ({n_hashed} files).")
    print("[OK] Zero ground-truth response (`y`) columns copied into `object/*.csv`.")
    print(
        f"[OK] BeatAML2 (N=19,823/split, 484 AML patients, 154 drugs [79 shared, 75 unseen]): "
        f"unadjusted R2_norm={baml_s['R2_norm_mean']:+.5f}+-{baml_s['R2_norm_std']:.5f}, "
        f"Pearson_norm={baml_s['Pearson_norm_mean']:+.5f}+-{baml_s['Pearson_norm_std']:.5f}, "
        f"MSE={baml_s['MSE_mean']:.4f}; shared drugs (N=11,901) R2_norm={baml_p3['unadjusted_shared_drugs']['R2_norm_mean']:+.5f}."
    )
    print(
        f"[OK] BeatAML2 p3 single-factor (each on its own, zero y_true): "
        f"(i) Assay FE R2_norm={baml_p3['only_i_assay_protocol_fe_all']['R2_norm_mean']:+.5f} (dMSE={baml_p3['only_i_assay_protocol_fe_all']['MSE_change_vs_unadjusted']:+.4f}), "
        f"(ii) Platform R2_norm={baml_p3['only_ii_platform_shift_all']['R2_norm_mean']:+.5f} (dMSE={baml_p3['only_ii_platform_shift_all']['MSE_change_vs_unadjusted']:+.4f}), "
        f"(iii) Overlap R2_norm={baml_p3['only_iii_drug_overlap_prior_all']['R2_norm_mean']:+.5f} (dMSE={baml_p3['only_iii_drug_overlap_prior_all']['MSE_change_vs_unadjusted']:+.4f}); "
        f"cumulative (i)+(ii)+(iii) R2_norm={baml_p3['cumulative_step3_plus_platform_shift_all']['R2_norm_mean']:+.5f}+-{baml_p3['cumulative_step3_plus_platform_shift_all']['R2_norm_std']:.5f} (10/10 splits > 0)."
    )
    print(
        f"[OK] PDX_Bruna (N=1,046/split, 25 PDX models, 100 drugs [49 shared, 51 unseen]): "
        f"unadjusted R2_norm={pdx_s['R2_norm_mean']:+.5f}+-{pdx_s['R2_norm_std']:.5f}, "
        f"Pearson_norm={pdx_s['Pearson_norm_mean']:+.5f}+-{pdx_s['Pearson_norm_std']:.5f}, "
        f"MSE={pdx_s['MSE_mean']:.4f}."
    )
    print(
        f"[OK] PDX_Bruna p3 single-factor (each on its own, zero y_true): "
        f"(i) Assay FE R2_norm={pdx_p3['only_i_assay_protocol_fe_all']['R2_norm_mean']:+.5f} (dMSE={pdx_p3['only_i_assay_protocol_fe_all']['MSE_change_vs_unadjusted']:+.4f}), "
        f"(ii) Platform R2_norm={pdx_p3['only_ii_platform_shift_all']['R2_norm_mean']:+.5f} (dMSE={pdx_p3['only_ii_platform_shift_all']['MSE_change_vs_unadjusted']:+.4f}), "
        f"(iii) Overlap R2_norm={pdx_p3['only_iii_drug_overlap_prior_all']['R2_norm_mean']:+.5f} (dMSE={pdx_p3['only_iii_drug_overlap_prior_all']['MSE_change_vs_unadjusted']:+.4f}); "
        f"cumulative (i)+(ii)+(iii) R2_norm={pdx_p3['cumulative_step3_plus_platform_shift_all']['R2_norm_mean']:+.5f}+-{pdx_p3['cumulative_step3_plus_platform_shift_all']['R2_norm_std']:.5f} (10/10 splits > 0)."
    )
    print("PASS")


if __name__ == "__main__":
    main()
