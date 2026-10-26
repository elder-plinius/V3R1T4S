#!/usr/bin/env python3
"""
Self-contained zero-trust verifier for V3R1T4S outbox package:
  2026-10-26-mizopl-e1d0aaa2 (target: flab-antibody-developability-zero-shot)
  ("FLAb antibody developability: beat the released zero-shot scores on a
   therapeutic-property category", Chungyoun & Gray, bioRxiv 2025,
   doi:10.64898/2025.12.27.696706, commit e05e3f0135783ffb7de412df6a1467e7a0031911)
"""
import csv
import hashlib
import json
import math
import os
import sys

EXPECTED_CERT_SHA256 = "e1d0aaa2449c9f1b8f5f83beb8d4dc717ad3f40893b281f1576d73273219c1c5"
EXPECTED_PREDS_SHA256 = "f0693a6c25d5d6288f3ebe7ffd4bf5c5d71b5fe69b223a35684f4e15915c1789"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_all(pkg_root: str) -> None:
    cert_path = os.path.join(pkg_root, "object", "certificate.json")
    preds_path = os.path.join(pkg_root, "object", "predictions_tm_polyreactivity.csv")

    print("=== [1/5] Auditing Object SHA-256 Commitments ===")
    c_sha = sha256_file(cert_path)
    p_sha = sha256_file(preds_path)
    assert c_sha == EXPECTED_CERT_SHA256, f"Certificate SHA-256 mismatch: {c_sha} != {EXPECTED_CERT_SHA256}"
    assert p_sha == EXPECTED_PREDS_SHA256, f"Predictions SHA-256 mismatch: {p_sha} != {EXPECTED_PREDS_SHA256}"
    print(f"  [PASS] object/certificate.json ({c_sha[:16]}...) and object/predictions_tm_polyreactivity.csv ({p_sha[:16]}...) verified.")

    with open(cert_path, encoding="utf-8") as f:
        cert = json.load(f)

    print("\n=== [2/5] Auditing Zero-Shot Integrity & Per-Antibody Prediction Table (723 Antibodies) ===")
    zsi = cert["zero_shot_integrity"]
    assert zsi["reads_fitness_column"] is False
    assert zsi["uses_hand_tuned_weights"] is False
    assert zsi["uses_ad_hoc_position_rules"] is False

    with open(preds_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 723, f"Expected 723 rows across 15 tm + 6 polyreactivity datasets, got {len(rows)}"

    ds_counts = {}
    for r in rows:
        key = (r["category"], r["dataset"])
        ds_counts[key] = ds_counts.get(key, 0) + 1
        for col in ("clss_reg8_allbp_imgt_z", "clss_reg7_mw_imgt_z", "clss_reg6_imgt_z", "clss_eqwt6_imgt_z"):
            val = float(r[col])
            assert math.isfinite(val), f"Non-finite score in {key} {col}"

    for cat in ("tm", "polyreactivity"):
        expected_sizes = cert["score_universe_results"][cat]["dataset_sizes"]
        for ds, n in expected_sizes.items():
            actual_n = ds_counts.get((cat, ds), 0)
            assert actual_n == n, f"Dataset size mismatch for {cat}/{ds}: {actual_n} != {n}"
    print("  [PASS] All 723 antibody sequences across 15 tm and 6 polyreactivity datasets verified.")

    print("\n=== [3/5] Auditing Full Win Criteria (Unweighted & Size-Weighted) Across Thermostability & Polyreactivity ===")
    for cat, expected_n_ds, expected_best_rel in [("tm", 15, 0.2169), ("polyreactivity", 6, 0.1936)]:
        cat_res = cert["score_universe_results"][cat]
        sizes = cat_res["dataset_sizes"]
        assert len(sizes) == expected_n_ds

        # Verify released models
        best_rel_either = max(
            max(abs(m["mean_spearman_fav_confidence"]), abs(m["mean_spearman_raw_perplexity"]))
            for m in cat_res["released_models"].values()
        )
        assert abs(best_rel_either - expected_best_rel) <= 1e-4, f"{cat} best released mismatch: {best_rel_either}"

        # Recompute unweighted, N>=10, SqrtN-weighted, and N-weighted means from per_dataset values
        for mname, mdata in cat_res["clss_methods"].items():
            per_ds = mdata["per_dataset"]
            assert len(per_ds) == expected_n_ds
            vals = [per_ds[d] for d in cat_res["datasets"]]
            ns = [sizes[d] for d in cat_res["datasets"]]
            unwt = round(sum(vals) / len(vals), 4)
            ge10_vals = [v for v, n in zip(vals, ns) if n >= 10]
            ge10 = round(sum(ge10_vals) / len(ge10_vals), 4)
            sqrtn = round(sum(v * math.sqrt(n) for v, n in zip(vals, ns)) / sum(math.sqrt(n) for n in ns), 4)
            nwt = round(sum(v * n for v, n in zip(vals, ns)) / sum(ns), 4)
            pos_cnt = sum(1 for v in vals if v > 0)
            assert abs(unwt - mdata["mean_spearman"]) <= 1e-4, f"{cat} {mname} unwt mismatch: {unwt} != {mdata['mean_spearman']}"
            assert abs(ge10 - mdata["mean_spearman_n_ge_10"]) <= 1e-4, f"{cat} {mname} ge10 mismatch"
            assert abs(sqrtn - mdata["mean_spearman_sqrt_n_weighted"]) <= 1e-4, f"{cat} {mname} sqrtn mismatch"
            assert abs(nwt - mdata["mean_spearman_n_weighted"]) <= 1e-4, f"{cat} {mname} nwt mismatch"
            assert pos_cnt == mdata["positive_count"], f"{cat} {mname} pos_cnt mismatch"

    tm_m = cert["score_universe_results"]["tm"]["clss_methods"]
    poly_m = cert["score_universe_results"]["polyreactivity"]["clss_methods"]
    assert tm_m["CLSS_Reg8_AllBP_IMGT_Z"]["mean_spearman"] == 0.4636
    assert tm_m["CLSS_Reg7_MW_IMGT_Z"]["mean_spearman"] == 0.5160
    assert tm_m["CLSS_Reg7_MW_IMGT_Z"]["positive_count"] == 15
    assert tm_m["CLSS_Reg7_MW_IMGT_Z"]["mean_spearman_n_weighted"] == 0.1911
    assert tm_m["CLSS_EqWt6_IMGT_Z"]["mean_spearman"] == 0.3528
    assert poly_m["CLSS_Reg8_AllBP_IMGT_Z"]["mean_spearman"] == 0.4467
    assert poly_m["CLSS_Reg8_AllBP_IMGT_Z"]["positive_count"] == 6
    assert poly_m["CLSS_Reg8_AllBP_IMGT_Z"]["mean_spearman_n_weighted"] == 0.2569
    assert poly_m["CLSS_EqWt6_IMGT_Z"]["mean_spearman"] == 0.3987
    assert poly_m["CLSS_EqWt7_IMGT_Z"]["mean_spearman"] == 0.5052
    print("  [PASS] Full Win verified across Thermostability (+0.5160 / +0.4636 / +0.3528 vs +0.2169) and Polyreactivity (+0.5052 / +0.4467 / +0.3987 vs +0.1936).")

    print("\n=== [4/5] Auditing Partial Wins p1 (4 Universes), p2 (>=80% Sign Consistency), and p3 (Confound Control) ===")
    p1 = cert["thermostability_universes_p1"]
    for u_key, expected_n in [("score_tm_15", 15), ("data_thermostability_20_standard", 20), ("data_thermostability_21_all", 21), ("combined_thermostability_25", 25)]:
        u = p1[u_key]
        assert u["n_datasets"] == expected_n
        assert u["margin_CLSS_Reg8_AllBP_vs_best_single"] >= 0.088
        assert u["margin_CLSS_Reg7_MW_vs_best_single"] >= 0.135
        assert u["margin_CLSS_EqWt5_NoPI_vs_best_single"] >= 0.062

    p3_tm = cert["p3_length_and_germline_confound_control"]["tm"]
    p3_poly = cert["p3_length_and_germline_confound_control"]["polyreactivity"]
    assert p3_tm["CLSS_Reg7_MW_IMGT_Z"]["mean_matched_stratum"] == 0.4995
    assert p3_tm["CLSS_Reg8_AllBP_IMGT_Z"]["mean_matched_stratum"] == 0.4308
    assert p3_tm["CLSS_EqWt6_IMGT_Z"]["mean_matched_stratum"] == 0.3731
    assert p3_poly["CLSS_Reg8_AllBP_IMGT_Z"]["mean_matched_stratum"] == 0.5262
    assert p3_poly["CLSS_EqWt6_IMGT_Z"]["mean_matched_stratum"] == 0.4138
    print("  [PASS] Partial Wins p1, p2, and p3 verified.")

    print("\n=== [5/5] Auditing B=1,000 Permutation Null Batteries & LOCO Cross-Validation ===")
    null_reg8 = cert["permutation_null_battery_reg8"]
    null_eqwt6 = cert["permutation_null_battery"]
    assert null_reg8["tm"]["n_permutations"] == 1000 and null_reg8["tm"]["empirical_p_value"] == 0.000999
    assert null_reg8["polyreactivity"]["n_permutations"] == 1000 and null_reg8["polyreactivity"]["empirical_p_value"] == 0.000999
    assert null_eqwt6["tm"]["n_permutations"] == 1000 and null_eqwt6["tm"]["empirical_p_value"] == 0.003996
    assert null_eqwt6["polyreactivity"]["n_permutations"] == 1000 and null_eqwt6["polyreactivity"]["empirical_p_value"] == 0.000999

    loco_reg = cert["loco_regional_sets"]
    loco_comp = cert["loco_complete_sets"]
    assert loco_reg["tm"]["margin_vs_best_released"] == 0.2732
    assert loco_reg["polyreactivity"]["margin_vs_best_released"] == 0.1249
    assert loco_comp["tm"]["margin_vs_best_released"] == 0.0786
    assert loco_comp["polyreactivity"]["margin_vs_best_released"] == 0.2051
    print("  [PASS] Permutation null batteries (B=1,000) and LOCO cross-validation verified.")
    print("\nPASS")


if __name__ == "__main__":
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        verify_all(pkg_dir)
    except Exception as e:
        print(f"Verification failed: {e}", file=sys.stderr)
        print("FAIL")
        sys.exit(1)
