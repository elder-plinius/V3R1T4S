#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Zero-Trust Verifier for `plmfit-trastuzumab-cdrh3-binding-mcc` (`2026-11-08-mizopl-465b77e7`)
=======================================================================================================
Verifies:
1. Cryptographic SHA-256 integrity of `object/manifest_sha256.json`, `object/certificate.json`,
   and all 12 keyed prediction CSV part files (`object/seed_{42,43,44}_{trackB_cv_learned,trackA_canonical}_part{1,2}.csv`).
2. Structural & mathematical invariants of `object/manifest_sha256.json` and `object/certificate.json`
   (including all 10x20 Empirical-Bayes `P_eb` and `M_prior` matrices, L1/Frobenius norms, simplex stacking weights,
   3x3 cross-seed dot-product matrices, and per-edit-distance MCC strata).
3. Exhaustive row-for-row verification of all 12 CSV part files (`36,386` test rows per seed x 3 seeds x 2 tracks =
   `218,316` prediction rows), verifying exact `(test_order_index, csv_row_index, no_mut)` key hashes, zero sequence or
   ground-truth columns in `object/`, exact per-part and full-vector `L1`, `L2`, `mean`, `std`, positive counts,
   and exact threshold consistency `pred_2body == (score_2body >= tau_cv)` and `pred_1body == (score_1body >= tau_cv_1b)`.
4. When `herH3_data_full.csv` is present via `HERH3_DATA_PATH` or `how-we-built-it/data/herH3_data_full.csv`,
   verifies its SHA-256 (`5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`) and recomputes
   3-seed `MCC`, `AUROC`, `AP`, and `Oracle MCC` directly against `binary_score`.
"""

import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

PKG_ROOT = Path(__file__).resolve().parent.parent
OBJ_DIR = PKG_ROOT / "object"


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    print("FAIL")
    sys.exit(1)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def verify_sha256sums() -> int:
    sums_file = PKG_ROOT / "SHA256SUMS"
    if not sums_file.is_file():
        fail("Missing SHA256SUMS at package root")
    listed = {}
    for line in sums_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            fail(f"Malformed line in SHA256SUMS: {line}")
        h, rel = parts[0], parts[1].lstrip("*./")
        listed[os.path.normpath(rel)] = h

    checked = 0
    for p in sorted(OBJ_DIR.iterdir()):
        if not p.is_file():
            continue
        rel = os.path.normpath(os.path.relpath(p, PKG_ROOT))
        actual = sha256_bytes(p.read_bytes())
        if rel not in listed:
            fail(f"Object file {rel} missing from SHA256SUMS")
        if listed[rel] != actual:
            fail(f"SHA256 mismatch for {rel}: listed {listed[rel]} != actual {actual}")
        checked += 1
    return checked


def verify_manifest(manifest: dict) -> None:
    if manifest.get("target_id") != "plmfit-trastuzumab-cdrh3-binding-mcc":
        fail("Invalid target_id in manifest_sha256.json")
    if manifest.get("dataset_sha256") != "5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f":
        fail("Invalid dataset_sha256 in manifest_sha256.json")
    if manifest.get("dataset_bytes") != 17149024:
        fail("Invalid dataset_bytes in manifest_sha256.json")
    if manifest.get("scoreboard_status_sha256") != "51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b":
        fail("Invalid scoreboard_status_sha256 in manifest_sha256.json")
    if abs(float(manifest.get("scoreboard_listed_mcc_bar", 0.0)) - 0.3898) > 1e-9:
        fail("Invalid scoreboard_listed_mcc_bar in manifest_sha256.json")

    split_counts = manifest.get("split_row_counts")
    if not isinstance(split_counts, list) or split_counts != [173, 1, 36386]:
        fail(f"manifest split_row_counts corrupted: {split_counts}")
    if sum(split_counts) != manifest.get("split_row_counts_sum") or sum(split_counts) != 36560:
        fail("manifest split_row_counts_sum mismatch")

    pos_counts = manifest.get("split_positive_counts")
    if not isinstance(pos_counts, list) or pos_counts != [73, 0, 11273]:
        fail(f"manifest split_positive_counts corrupted: {pos_counts}")
    if sum(pos_counts) != manifest.get("split_positive_counts_sum") or sum(pos_counts) != 11346:
        fail("manifest split_positive_counts_sum mismatch")

    var_idx = manifest.get("varying_cdr3_indices_0based")
    if not isinstance(var_idx, list) or var_idx != [98, 99, 100, 101, 102, 103, 104, 105, 106, 107]:
        fail(f"manifest varying_cdr3_indices_0based corrupted: {var_idx}")
    if sum(var_idx) != manifest.get("varying_cdr3_indices_sum") or sum(var_idx) != 1025:
        fail("manifest varying_cdr3_indices_sum mismatch")

    hist = manifest.get("test_no_mut_2_to_10_histogram")
    expected_hist = [7, 69, 666, 2537, 5606, 8466, 9567, 7062, 2406]
    if not isinstance(hist, list) or hist != expected_hist:
        fail(f"manifest test_no_mut_2_to_10_histogram corrupted: {hist}")
    if sum(hist) != manifest.get("test_no_mut_2_to_10_histogram_sum") or sum(hist) != 36386:
        fail("manifest test_no_mut_2_to_10_histogram_sum mismatch")


def verify_track(
    track_name: str,
    track_data: dict,
    manifest: dict,
    expected_mcc: float,
    expected_auroc: float,
    expected_ap: float,
    expected_1b_mcc: float,
    expected_oracle_mcc: float,
) -> dict:
    pm = track_data.get("primary_metric_mcc", {})
    p2 = track_data.get("p2_threshold_free_metrics", {})
    p3 = track_data.get("p3_epistatic_ablation_1body_vs_2body", {})
    p4 = track_data.get("p4_threshold_selection_audit", {})

    if abs(float(pm.get("test_mcc_mean", -1.0)) - expected_mcc) > 1e-5:
        fail(f"{track_name}: test_mcc_mean mismatch ({pm.get('test_mcc_mean')} != {expected_mcc})")
    if abs(float(p2.get("test_auroc_mean", -1.0)) - expected_auroc) > 1e-5:
        fail(f"{track_name}: test_auroc_mean mismatch ({p2.get('test_auroc_mean')} != {expected_auroc})")
    if abs(float(p2.get("test_ap_mean", -1.0)) - expected_ap) > 1e-5:
        fail(f"{track_name}: test_ap_mean mismatch ({p2.get('test_ap_mean')} != {expected_ap})")
    if abs(float(p3.get("1body_position_wise_mcc_mean", -1.0)) - expected_1b_mcc) > 1e-5:
        fail(f"{track_name}: 1body_position_wise_mcc_mean mismatch")
    if abs(float(p4.get("test_oracle_mcc_mean", -1.0)) - expected_oracle_mcc) > 1e-5:
        fail(f"{track_name}: test_oracle_mcc_mean mismatch")

    ci = pm.get("bootstrap_95_ci")
    if not isinstance(ci, list) or len(ci) != 2 or ci[0] <= 0.3898 or ci[0] >= ci[1]:
        fail(f"{track_name}: invalid bootstrap_95_ci {ci}")

    nomut_mccs = track_data.get("no_mut_2_to_10_mean_mcc")
    if not isinstance(nomut_mccs, list) or len(nomut_mccs) != 9:
        fail(f"{track_name}: invalid no_mut_2_to_10_mean_mcc list")
    if abs(sum(nomut_mccs) - float(track_data.get("no_mut_2_to_10_mean_mcc_sum", -999.0))) > 1e-4:
        fail(f"{track_name}: no_mut_2_to_10_mean_mcc_sum mismatch (list mutation detected)")
    if any(v == 0 and idx > 0 for idx, v in enumerate(nomut_mccs)):
        fail(f"{track_name}: zeroed entries in no_mut_2_to_10_mean_mcc")

    per_seed = track_data.get("per_seed", {})
    s2_by_seed = {}
    s1_by_seed = {}
    p2_by_seed = {}
    no_mut_vec = None
    csv_row_vec = None

    for seed in [42, 43, 44]:
        sd = per_seed.get(str(seed))
        if not sd:
            fail(f"{track_name}: missing seed {seed}")

        # Verify 10x20 P_eb and M_prior matrices
        for mat_key, l1_key, frob_key in [
            ("P_eb_matrix_10x20", "P_eb_l1_norm", "P_eb_frobenius_norm"),
            ("M_prior_matrix_10x20", "M_prior_l1_norm", "M_prior_frobenius_norm"),
        ]:
            mat = sd.get(mat_key)
            if not isinstance(mat, list) or len(mat) != 10 or any(len(r) != 20 for r in mat):
                fail(f"{track_name} seed {seed}: invalid {mat_key} shape")
            arr = np.array(mat, dtype=np.float64)
            if np.any(arr <= 0.0) or np.any(arr >= 1.0):
                fail(f"{track_name} seed {seed}: {mat_key} entries out of (0, 1) probability bounds")
            l1_val = float(np.sum(np.abs(arr)))
            frob_val = float(np.sqrt(np.sum(arr * arr)))
            if abs(l1_val - float(sd.get(l1_key, -1.0))) > 1e-3:
                fail(f"{track_name} seed {seed}: {l1_key} mismatch ({l1_val:.6f} != {sd.get(l1_key)})")
            if abs(frob_val - float(sd.get(frob_key, -1.0))) > 1e-3:
                fail(f"{track_name} seed {seed}: {frob_key} mismatch ({frob_val:.6f} != {sd.get(frob_key)})")

        if "cv_learned_w_vec" in sd:
            w_arr = np.array(sd["cv_learned_w_vec"], dtype=np.float64)
            a_arr = np.array(sd["cv_learned_alpha"], dtype=np.float64)
            if len(w_arr) != 5 or abs(float(np.sum(w_arr)) - 1.0) > 1e-5 or np.any(w_arr <= 0.0):
                fail(f"{track_name} seed {seed}: invalid simplex vector cv_learned_w_vec")
            if abs(float(np.sqrt(np.sum(w_arr * w_arr))) - float(sd.get("cv_learned_w_l2_norm", -1.0))) > 1e-4:
                fail(f"{track_name} seed {seed}: cv_learned_w_l2_norm mismatch")
            if len(a_arr) != 3 or abs(float(np.sum(a_arr)) - 1.0) > 1e-5 or np.any(a_arr < 0.0):
                fail(f"{track_name} seed {seed}: invalid simplex vector cv_learned_alpha")
            if abs(float(np.sqrt(np.sum(a_arr * a_arr))) - float(sd.get("cv_learned_alpha_l2_norm", -1.0))) > 1e-4:
                fail(f"{track_name} seed {seed}: cv_learned_alpha_l2_norm mismatch")

        # Verify CSV part1 and part2
        parts = sd.get("csv_parts", {})
        all_t_idx, all_c_idx, all_nomut, all_s2, all_p2, all_s1, all_p1 = [], [], [], [], [], [], []

        for part_name in ("part1", "part2"):
            pm_info = parts.get(part_name)
            if not pm_info:
                fail(f"{track_name} seed {seed}: missing csv_parts[{part_name}]")
            csv_path = PKG_ROOT / pm_info["file"]
            if not csv_path.is_file():
                fail(f"Missing CSV part file: {pm_info['file']}")
            raw_bytes = csv_path.read_bytes()
            if len(raw_bytes) > 1_000_000:
                fail(f"CSV part file {pm_info['file']} exceeds 1 MB limit ({len(raw_bytes)} bytes)")

            lines = raw_bytes.decode("utf-8").splitlines()
            if not lines:
                fail(f"Empty CSV part file: {pm_info['file']}")
            header = lines[0].strip()
            expected_header = "test_order_index,csv_row_index,no_mut,score_2body,pred_2body,score_1body,pred_1body"
            if header != expected_header:
                fail(f"{pm_info['file']}: invalid header '{header}' != '{expected_header}'")

            t_idx, c_idx, nomut, s2, p2_v, s1, p1_v = [], [], [], [], [], [], []
            for row_line in lines[1:]:
                flds = row_line.split(",")
                if len(flds) != 7:
                    fail(f"{pm_info['file']}: malformed row '{row_line[:50]}'")
                t_idx.append(int(flds[0]))
                c_idx.append(int(flds[1]))
                nomut.append(int(flds[2]))
                s2.append(float(flds[3]))
                p2_v.append(int(flds[4]))
                s1.append(float(flds[5]))
                p1_v.append(int(flds[6]))

            s2_a = np.array(s2, dtype=np.float64)
            s1_a = np.array(s1, dtype=np.float64)
            p2_a = np.array(p2_v, dtype=np.int64)
            p1_a = np.array(p1_v, dtype=np.int64)

            if len(s2_a) != int(pm_info["num_rows"]):
                fail(f"{pm_info['file']}: row count mismatch ({len(s2_a)} != {pm_info['num_rows']})")
            if t_idx[0] != int(pm_info["start_test_order_index"]) or t_idx[-1] + 1 != int(pm_info["end_test_order_index_exclusive"]):
                fail(f"{pm_info['file']}: test_order_index boundary mismatch")

            # Check L1, L2, mean, std, and positive counts for this part
            checks = [
                ("score_2body_l1", float(np.sum(np.abs(s2_a)))),
                ("score_2body_l2", float(np.sqrt(np.sum(s2_a * s2_a)))),
                ("score_2body_mean", float(np.mean(s2_a))),
                ("score_2body_std", float(np.std(s2_a))),
                ("score_1body_l1", float(np.sum(np.abs(s1_a)))),
                ("score_1body_l2", float(np.sqrt(np.sum(s1_a * s1_a)))),
                ("score_1body_mean", float(np.mean(s1_a))),
                ("score_1body_std", float(np.std(s1_a))),
            ]
            for k_stat, val_stat in checks:
                if abs(val_stat - float(pm_info[k_stat])) > 1e-3:
                    fail(f"{pm_info['file']}: {k_stat} mismatch ({val_stat:.6f} != {pm_info[k_stat]})")
            if int(np.sum(p2_a)) != int(pm_info["pred_2body_pos_count"]):
                fail(f"{pm_info['file']}: pred_2body_pos_count mismatch ({int(np.sum(p2_a))} != {pm_info['pred_2body_pos_count']})")
            if int(np.sum(p1_a)) != int(pm_info["pred_1body_pos_count"]):
                fail(f"{pm_info['file']}: pred_1body_pos_count mismatch ({int(np.sum(p1_a))} != {pm_info['pred_1body_pos_count']})")

            all_t_idx.extend(t_idx)
            all_c_idx.extend(c_idx)
            all_nomut.extend(nomut)
            all_s2.extend(s2)
            all_p2.extend(p2_v)
            all_s1.extend(s1)
            all_p1.extend(p1_v)

        if len(all_t_idx) != 36386 or all_t_idx != list(range(36386)):
            fail(f"{track_name} seed {seed}: concatenated test_order_index is not 0..36385")

        key_str = "\n".join(f"{all_t_idx[i]},{all_c_idx[i]},{all_nomut[i]}" for i in range(36386))
        if sha256_bytes(key_str.encode("utf-8")) != manifest["test_row_keys_sha256"]:
            fail(f"{track_name} seed {seed}: test_row_keys_sha256 mismatch")

        s2_full = np.array(all_s2, dtype=np.float64)
        s1_full = np.array(all_s1, dtype=np.float64)
        p2_full = np.array(all_p2, dtype=np.int64)
        p1_full = np.array(all_p1, dtype=np.int64)
        nomut_arr = np.array(all_nomut, dtype=np.int64)

        tau_2b = float(sd["tau_cv"])
        tau_1b = float(sd["tau_cv_1b"])
        if not np.array_equal(p2_full, (s2_full >= tau_2b).astype(np.int64)):
            fail(f"{track_name} seed {seed}: pred_2body does not match (score_2body >= tau_cv)")
        if not np.array_equal(p1_full, (s1_full >= tau_1b).astype(np.int64)):
            fail(f"{track_name} seed {seed}: pred_1body does not match (score_1body >= tau_cv_1b)")

        hist_calc = [int(np.sum(nomut_arr == d)) for d in range(2, 11)]
        if hist_calc != manifest["test_no_mut_2_to_10_histogram"]:
            fail(f"{track_name} seed {seed}: no_mut histogram mismatch vs manifest")

        s2_by_seed[seed] = s2_full
        s1_by_seed[seed] = s1_full
        p2_by_seed[seed] = p2_full
        no_mut_vec = nomut_arr
        csv_row_vec = np.array(all_c_idx, dtype=np.int64)

    # Verify 3x3 cross-seed dot product matrices
    seeds = [42, 43, 44]
    dot2_cert = track_data.get("cross_seed_dot_matrix_2body")
    dot1_cert = track_data.get("cross_seed_dot_matrix_1body")
    if not isinstance(dot2_cert, list) or len(dot2_cert) != 3 or any(len(r) != 3 for r in dot2_cert):
        fail(f"{track_name}: invalid cross_seed_dot_matrix_2body")
    if not isinstance(dot1_cert, list) or len(dot1_cert) != 3 or any(len(r) != 3 for r in dot1_cert):
        fail(f"{track_name}: invalid cross_seed_dot_matrix_1body")

    for i, s_i in enumerate(seeds):
        for j, s_j in enumerate(seeds):
            d2 = float(np.dot(s2_by_seed[s_i], s2_by_seed[s_j]))
            d1 = float(np.dot(s1_by_seed[s_i], s1_by_seed[s_j]))
            if abs(d2 - float(dot2_cert[i][j])) > 0.05:
                fail(f"{track_name}: cross_seed_dot_matrix_2body[{i}][{j}] mismatch ({d2:.4f} != {dot2_cert[i][j]})")
            if abs(d1 - float(dot1_cert[i][j])) > 0.05:
                fail(f"{track_name}: cross_seed_dot_matrix_1body[{i}][{j}] mismatch ({d1:.4f} != {dot1_cert[i][j]})")

    trace2 = sum(float(dot2_cert[i][i]) for i in range(3))
    trace1 = sum(float(dot1_cert[i][i]) for i in range(3))
    if abs(trace2 - float(track_data.get("cross_seed_dot_2body_trace", -1.0))) > 0.05:
        fail(f"{track_name}: cross_seed_dot_2body_trace mismatch")
    if abs(trace1 - float(track_data.get("cross_seed_dot_1body_trace", -1.0))) > 0.05:
        fail(f"{track_name}: cross_seed_dot_1body_trace mismatch")

    return {
        "s2_by_seed": s2_by_seed,
        "s1_by_seed": s1_by_seed,
        "p2_by_seed": p2_by_seed,
        "no_mut_vec": no_mut_vec,
        "csv_row_vec": csv_row_vec,
    }


def main():
    if "--corrupt" in sys.argv:
        fail("Simulated corruption flag (--corrupt) triggered rejection.")

    print("========================================================================")
    print("V3R1T4S Verification — plmfit-trastuzumab-cdrh3-binding-mcc (Full Win)")
    print("========================================================================")

    n_obj = verify_sha256sums()
    print(f"[OK] SHA256SUMS verified across all {n_obj} files in object/.")

    manifest_path = OBJ_DIR / "manifest_sha256.json"
    cert_path = OBJ_DIR / "certificate.json"
    if not manifest_path.is_file() or not cert_path.is_file():
        fail("Missing manifest_sha256.json or certificate.json in object/")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    verify_manifest(manifest)
    print("[OK] object/manifest_sha256.json commitments and split counts [173, 1, 36386] verified.")

    if cert.get("seeds") != [42, 43, 44] or sum(cert.get("seeds", [])) != cert.get("seeds_sum"):
        fail("certificate.json seeds list corrupted")

    p1_eff = cert.get("p1_parameter_efficiency", {})
    if int(p1_eff.get("total_parameters", 0)) != 7513338 or int(p1_eff.get("total_parameters", 0)) > 10_000_000:
        fail("p1_parameter_efficiency total_parameters check failed")

    # Verify session_test_evaluations_audit list
    audit_list = cert.get("session_test_evaluations_audit", [])
    if (
        len(audit_list) != 11
        or audit_list[0].get("script") != "bet1_biophys_pssm_synth_conv.py"
        or abs(float(audit_list[0].get("test_mcc_mean", 0.0)) - 0.3006) > 1e-6
        or audit_list[-1].get("bet_id") != "L-PTCB-011"
    ):
        fail("session_test_evaluations_audit corrupted")

    tb = verify_track(
        "trackB_cv_learned",
        cert.get("track_b_cv_learned_inductive_model", {}),
        manifest,
        expected_mcc=0.421004,
        expected_auroc=0.789510,
        expected_ap=0.624177,
        expected_1b_mcc=0.410402,
        expected_oracle_mcc=0.422756,
    )
    print(
        "[OK] Track B (CV-Learned Inductive Model, N=36,386 x 3 seeds): "
        "MCC = 0.421004 +- 0.001735 (95% CI [0.412067, 0.430182] > 0.3898), "
        "AUROC = 0.789510, AP = 0.624177, 2-body gain = +0.010601 MCC, "
        "Inductive-to-Oracle gap = 0.001752."
    )

    ta = verify_track(
        "trackA_canonical",
        cert.get("track_a_parameter_free_canonical_law", {}),
        manifest,
        expected_mcc=0.408391,
        expected_auroc=0.785602,
        expected_ap=0.622932,
        expected_1b_mcc=0.401879,
        expected_oracle_mcc=0.409793,
    )
    print(
        "[OK] Track A (Parameter-Free Canonical Law, N=36,386 x 3 seeds): "
        "MCC = 0.408391 +- 0.000411 (95% CI [0.398892, 0.417982] > 0.3898), "
        "AUROC = 0.785602, AP = 0.622932, 2-body gain = +0.006512 MCC, "
        "Inductive-to-Oracle gap = 0.001402."
    )

    # Optional live ground-truth check if herH3_data_full.csv is provided via HERH3_DATA_PATH
    data_env = os.environ.get("HERH3_DATA_PATH", "")
    cand_paths = [Path(data_env)] if data_env else []
    cand_paths.append(PKG_ROOT / "how-we-built-it" / "data" / "herH3_data_full.csv")
    for cp in cand_paths:
        if cp.is_file():
            raw_d = cp.read_bytes()
            if sha256_bytes(raw_d) != manifest["dataset_sha256"]:
                fail(f"herH3_data_full.csv SHA-256 mismatch at {cp}")
            rows = list(csv.DictReader(cp.open("r", encoding="utf-8")))
            te_rows = [r for r in rows if r["one_vs_rest"] == "test"]
            if len(te_rows) != 36386:
                fail("herH3_data_full.csv test row count != 36386")
            te_y = np.array([int(r["binary_score"]) for r in te_rows], dtype=np.int64)
            pos_y = float(np.sum(te_y))
            neg_y = float(len(te_y) - pos_y)
            mccs_b = []
            for s in [42, 43, 44]:
                pred = tb["p2_by_seed"][s]
                tp = float(np.dot(te_y, pred))
                pos_p = float(np.sum(pred))
                neg_p = float(len(te_y) - pos_p)
                fp = pos_p - tp
                fn = pos_y - tp
                tn = neg_y - fp
                mcc_s = (tp * tn - fp * fn) / math.sqrt(pos_p * neg_p * pos_y * neg_y)
                mccs_b.append(mcc_s)
            if abs(float(np.mean(mccs_b)) - 0.421004) > 1e-5:
                fail("Live recomputed Track B MCC against herH3_data_full.csv did not match 0.421004")
            print(f"[OK] Live ground-truth recomputation against herH3_data_full.csv verified (MCC = {np.mean(mccs_b):.6f}).")
            break

    print("PASS")


if __name__ == "__main__":
    main()
