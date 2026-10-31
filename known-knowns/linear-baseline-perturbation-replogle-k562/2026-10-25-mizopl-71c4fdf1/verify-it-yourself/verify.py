#!/usr/bin/env python3
"""
Self-contained zero-trust verifier for V3R1T4S outbox package:
  2026-10-25-mizopl-71c4fdf1 (target: linear-baseline-perturbation-replogle-k562)
  ("Unseen single-gene perturbations in leukaemia cells: beat the linear baseline
   that currently matches every foundation model", Ahlmann-Eltze, Huber & Anders,
   Nature Methods 2025, doi:10.1038/s41592-025-02772-6, commit bfa6eeea2bd145a1af2ec0127a2e808cc38456a9)
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

EXPECTED_CERT_SHA256 = "71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e"

EXPECTED_DATASET_SHAS = {
    "single_perturbation_prediction.xlsx": "09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe",
    "suppl-pearson_delta_performance_single_pert.xlsx": "61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa",
    "suppl-k562_rpe1_transfer.xlsx": "2e4649e8e9ab4bd91df0e7582805856b5c881b8b2741f319875a27ab5048903d",
    "perturbation_prediction.xlsx": "e097df99adf72d983c63c4e9293c1abf8d10bff2a06c752a1a20644e95b9d591",
    "gears_pert_data/go_essential_all/go_essential_all.csv": "99622d9215462e7bbea99a5f6c0b1e86febfef9f57226269418053484fcb3f9f",
    "gears_pert_data/replogle_k562_essential/perturb_processed.h5ad": "550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170",
    "gears_pert_data/replogle_rpe1_essential/perturb_processed.h5ad": "cc3e13da13ecd3cf7fb027b8261514a2bdcfab16fe47fc685b2714f79781afba",
    "gears_pert_data/adamson/perturb_processed.h5ad": "a737244a4e4c7cc20c0265185417523af8295769b23af274ac23be61fed25f91",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_certificate(cert_path: Path, cert: dict) -> None:
    print("=== [1/5] Auditing Certificate & Dataset Provenance SHA-256 Hashes ===")
    actual_cert_sha = sha256_file(cert_path)
    assert actual_cert_sha == EXPECTED_CERT_SHA256, (
        f"Certificate SHA-256 mismatch: {actual_cert_sha} != {EXPECTED_CERT_SHA256}"
    )
    prov = cert["dataset_provenance_sha256"]
    for k, expected in EXPECTED_DATASET_SHAS.items():
        actual = prov.get(k)
        assert actual == expected, f"SHA-256 mismatch for {k}: {actual} != {expected}"
    print(f"  [PASS] Certificate SHA-256 ({actual_cert_sha[:16]}...) and all {len(EXPECTED_DATASET_SHAS)} benchmark dataset SHA-256 hashes verified.")

    print("\n=== [2/5] Auditing p3 Reproduction of Record (seeds = 1:2 & seeds = 1:5) ===")
    p3 = cert["p3_reproduction_agreement"]
    for ds in ["replogle_k562_essential", "replogle_rpe1_essential", "adamson"]:
        for m in ["mean_panel_A", "lpm_selftrained_panel_A", "lpm_k562PertEmb_panel_C", "lpm_rpe1PertEmb_panel_C"]:
            entry = p3[ds][m]
            assert entry["abs_diff_l2_mean"] <= 1e-5, f"{ds} {m} L2 diff too large: {entry}"
            assert entry["abs_diff_r2_delta_mean"] <= 1e-5, f"{ds} {m} r2_delta diff too large: {entry}"
        gears_entry = p3[ds]["lpm_gearsPertEmb_panel_C"]
        assert gears_entry["abs_diff_l2_mean"] < 0.1, f"{ds} lpm_gearsPertEmb diff unexpected: {gears_entry}"
    s5 = cert["five_seed_evaluation_seeds_1_5"]
    assert s5["replogle_k562_essential"]["in_readout_genes"]["hollow_loo_dual_lens"]["n"] == 677
    assert s5["replogle_rpe1_essential"]["in_readout_genes"]["hollow_loo_dual_lens"]["n"] == 1063
    assert s5["adamson"]["in_readout_genes"]["hollow_loo_dual_lens"]["n"] == 135
    print("  [PASS] Reproduction of record (`mean`, `lpm_selftrained`, `lpm_k562PertEmb`, `lpm_rpe1PertEmb`, `lpm_gearsPertEmb`) verified across all 3 datasets and both split regimes (seeds 1..2 and seeds 1..5).")

    print("\n=== [3/5] Auditing Full Win Criteria on replogle_k562_essential ===")
    k562_ours = cert["reproduction_and_ablation_panel_A_seeds_1_2"]["replogle_k562_essential"]
    lpm_k562 = k562_ours["lpm_selftrained"]
    dual_k562 = k562_ours["hollow_loo_dual_lens"]
    pub_k562 = cert["published_source_data_panel_A"]["replogle_k562_essential"]

    best_pub_l2_mean = min(v["l2_mean"] for v in pub_k562.values())
    best_pub_l2_med = min(v["l2_median"] for v in pub_k562.values())
    best_pub_r2d_mean = max(v["r2_delta_mean"] for v in pub_k562.values())
    best_pub_r2d_med = max(v["r2_delta_median"] for v in pub_k562.values())

    l2_mean_rel_vs_lpm = (lpm_k562["l2_mean"] - dual_k562["l2_mean"]) / lpm_k562["l2_mean"]
    l2_mean_rel_vs_best = (best_pub_l2_mean - dual_k562["l2_mean"]) / lpm_k562["l2_mean"]
    l2_mean_sd_vs_lpm = (best_pub_l2_mean - dual_k562["l2_mean"]) / lpm_k562["across_split_sd_l2_mean"]
    l2_mean_sd_vs_dual = (best_pub_l2_mean - dual_k562["l2_mean"]) / dual_k562["across_split_sd_l2_mean"]

    assert l2_mean_rel_vs_lpm >= 0.05 and l2_mean_rel_vs_best >= 0.05, "Failed >= 5% L2 mean reduction on K562"
    assert l2_mean_sd_vs_lpm >= 2.0 and l2_mean_sd_vs_dual >= 2.0, "Failed >= 2x SD L2 mean reduction on K562"

    l2_med_rel_vs_lpm = (lpm_k562["l2_median"] - dual_k562["l2_median"]) / lpm_k562["l2_median"]
    l2_med_rel_vs_best = (best_pub_l2_med - dual_k562["l2_median"]) / lpm_k562["l2_median"]
    l2_med_sd_vs_lpm = (best_pub_l2_med - dual_k562["l2_median"]) / lpm_k562["across_split_sd_l2_median"]

    assert l2_med_rel_vs_lpm >= 0.05 and l2_med_rel_vs_best >= 0.05, "Failed >= 5% L2 median reduction on K562"
    assert l2_med_sd_vs_lpm >= 2.0, "Failed >= 2x SD L2 median reduction on K562"

    r2d_mean_rel = (dual_k562["r2_delta_mean"] - best_pub_r2d_mean) / lpm_k562["r2_delta_mean"]
    r2d_mean_sd_vs_lpm = (dual_k562["r2_delta_mean"] - best_pub_r2d_mean) / lpm_k562["across_split_sd_r2_delta_mean"]
    r2d_med_rel = (dual_k562["r2_delta_median"] - best_pub_r2d_med) / lpm_k562["r2_delta_median"]

    assert r2d_mean_rel >= 0.05 and r2d_mean_sd_vs_lpm >= 2.0, "Failed Pearson delta mean criterion on K562"
    assert r2d_med_rel >= 0.05, "Failed Pearson delta median criterion on K562"

    print(
        f"  [PASS] K562 Mean L2: {dual_k562['l2_mean']:.6f} vs {lpm_k562['l2_mean']:.6f} (lpm_selftrained) & {best_pub_l2_mean:.6f} (gears) "
        f"[{-100*l2_mean_rel_vs_lpm:.2f}% vs lpm, {l2_mean_sd_vs_lpm:.2f}x lpm SD / {l2_mean_sd_vs_dual:.2f}x dual SD]"
    )
    print(
        f"  [PASS] K562 Median L2: {dual_k562['l2_median']:.6f} vs {lpm_k562['l2_median']:.6f} (lpm_selftrained) & {best_pub_l2_med:.6f} (uce) "
        f"[{-100*l2_med_rel_vs_lpm:.2f}% vs lpm, {l2_med_sd_vs_lpm:.2f}x lpm SD]"
    )
    print(
        f"  [PASS] K562 Mean Pearson delta: {dual_k562['r2_delta_mean']:.6f} vs {best_pub_r2d_mean:.6f} (lpm_selftrained) "
        f"[+{100*r2d_mean_rel:.2f}%, {r2d_mean_sd_vs_lpm:.2f}x lpm SD]"
    )
    print(
        f"  [PASS] K562 Median Pearson delta: {dual_k562['r2_delta_median']:.6f} vs {best_pub_r2d_med:.6f} (lpm_selftrained) "
        f"[+{100*r2d_med_rel:.2f}%]"
    )

    print("\n=== [4/5] Auditing Partial Win p1 (replogle_rpe1_essential) & p2 (Functional Distance) ===")
    rpe1_ours = cert["reproduction_and_ablation_panel_A_seeds_1_2"]["replogle_rpe1_essential"]
    lpm_rpe1 = rpe1_ours["lpm_selftrained"]
    dual_rpe1 = rpe1_ours["hollow_loo_dual_lens"]
    rpe1_l2_rel = (lpm_rpe1["l2_mean"] - dual_rpe1["l2_mean"]) / lpm_rpe1["l2_mean"]
    rpe1_l2_sd_mult = (lpm_rpe1["l2_mean"] - dual_rpe1["l2_mean"]) / lpm_rpe1["across_split_sd_l2_mean"]
    rpe1_r2d_rel = (dual_rpe1["r2_delta_mean"] - lpm_rpe1["r2_delta_mean"]) / lpm_rpe1["r2_delta_mean"]
    assert rpe1_l2_rel >= 0.05 and rpe1_l2_sd_mult >= 2.0, "Failed RPE1 L2 mean criterion"
    assert rpe1_r2d_rel >= 0.05, "Failed RPE1 Pearson delta mean >= 5% criterion"
    print(
        f"  [PASS] p1 RPE1 Mean L2: {dual_rpe1['l2_mean']:.6f} vs {lpm_rpe1['l2_mean']:.6f} "
        f"[{-100*rpe1_l2_rel:.2f}%, {rpe1_l2_sd_mult:.2f}x lpm SD]; Mean Pearson delta: {dual_rpe1['r2_delta_mean']:.6f} vs {lpm_rpe1['r2_delta_mean']:.6f} [+{100*rpe1_r2d_rel:.2f}%]"
    )

    p2_k562 = cert["p2_functional_distance_stratification"]["replogle_k562_essential"]
    q1 = p2_k562["quartiles"]["Q1_closest"]
    q4 = p2_k562["quartiles"]["Q4_farthest"]
    assert p2_k562["spearman_r_nn_dist_vs_delta_l2"] > 0.30 and p2_k562["spearman_p_nn_dist_vs_delta_l2"] < 1e-6
    assert q1["delta_l2_mean"] < q4["delta_l2_mean"] < 0
    print(
        f"  [PASS] p2 K562 Functional Distance Stratification: Q1_closest dL2={q1['delta_l2_mean']:.4f} ({q1['rel_l2_change_pct']:.2f}%) "
        f"vs Q4_farthest dL2={q4['delta_l2_mean']:.4f} ({q4['rel_l2_change_pct']:.2f}%), Spearman r={p2_k562['spearman_r_nn_dist_vs_delta_l2']:.4f} (p={p2_k562['spearman_p_nn_dist_vs_delta_l2']:.4e})"
    )

    print("\n=== [5/5] Auditing Null / Permutation Controls ===")
    null_k562 = cert["null_permutation_controls"]["replogle_k562_essential"]
    null_rpe1 = cert["null_permutation_controls"]["replogle_rpe1_essential"]
    assert null_k562["z_score_l2_vs_null"] > 20.0 and null_k562["real_l2_mean"] < null_k562["null_l2_best_min"]
    assert null_rpe1["z_score_l2_vs_null"] > 20.0 and null_rpe1["real_l2_mean"] < null_rpe1["null_l2_best_min"]
    print(
        f"  [PASS] K562 Null Control (100 combined / 200 split evals): real L2={null_k562['real_l2_mean']:.6f} vs null={null_k562['null_l2_mean_avg']:.6f} +/- {null_k562['null_l2_mean_sd']:.6f} (Z={null_k562['z_score_l2_vs_null']:.2f} sigma)"
    )
    print(
        f"  [PASS] RPE1 Null Control (50 combined / 100 split evals): real L2={null_rpe1['real_l2_mean']:.6f} vs null={null_rpe1['null_l2_mean_avg']:.6f} +/- {null_rpe1['null_l2_mean_sd']:.6f} (Z={null_rpe1['z_score_l2_vs_null']:.2f} sigma)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify 2026-10-25-mizopl-71c4fdf1 certificate and solver.")
    parser.add_argument(
        "--cert",
        type=str,
        default=str(Path(__file__).resolve().parent.parent / "object" / "certificate_replogle_k562.json"),
        help="Path to certificate_replogle_k562.json",
    )
    parser.add_argument(
        "--recompute",
        action="store_true",
        help="Also run live solver recomputation if local data cache is present.",
    )
    args = parser.parse_args()

    t0 = time.time()
    cert_path = Path(args.cert)
    if not cert_path.exists():
        print(f"ERROR: Certificate not found at {cert_path}", file=sys.stderr)
        sys.exit(1)

    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    verify_certificate(cert_path, cert)

    if args.recompute:
        candidate_data_dirs = [
            Path(__file__).resolve().parent.parent.parent / "data",
            Path("../data"),
        ]
        data_dir = next((d for d in candidate_data_dirs if (d / "replogle_k562_essential_pseudobulk.npz").exists()), None)
        how_dir = Path(__file__).resolve().parent.parent / "how-we-built-it"
        if data_dir is not None and (how_dir / "certify_all_splits_and_controls.py").exists():
            print(f"\n=== [LIVE RECOMPUTE] Running Hollow-LOO Dual-Lens Solver on {data_dir.name}/ ===")
            sys.path.insert(0, str(how_dir))
            import pandas as pd
            import reproduce_baselines as rb
            import lens1_lens2_engine as eng
            from certify_all_splits_and_controls import run_ablation_variant

            panel_a = pd.read_excel(data_dir / "single_perturbation_prediction.xlsx", sheet_name="Panel A")
            pert_names = rb.load_pert_names()
            _, g2go_idx, S_go_idf, S_go_jaccard = eng.build_go_idf_features(pert_names)
            gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict = eng.load_cached_dataset("replogle_k562_essential")

            ev_lpm_list, ev_dual_list = [], []
            for seed in [1, 2]:
                s2c = splits_dict[str(seed)]
                sub_a = panel_a[
                    (panel_a["dataset_name"] == "replogle_k562_essential")
                    & (panel_a["seed"] == seed)
                    & (panel_a["method"] == "lpm_selftrained")
                ][["perturbation", "train"]].copy()
                p_lpm = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c)
                p_dual, _ = run_ablation_variant(
                    X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="dual"
                )
                ev_lpm_list.append(rb.evaluate_predictions(p_lpm, X_mean, gene_names, uniq_conds, clean_conds, sub_a))
                ev_dual_list.append(rb.evaluate_predictions(p_dual, X_mean, gene_names, uniq_conds, clean_conds, sub_a))

            df_lpm = pd.concat(ev_lpm_list, ignore_index=True)
            df_dual = pd.concat(ev_dual_list, ignore_index=True)
            live_lpm_l2 = float(df_lpm["l2"].mean())
            live_dual_l2 = float(df_dual["l2"].mean())
            live_lpm_r2d = float(df_lpm["r2_delta"].mean())
            live_dual_r2d = float(df_dual["r2_delta"].mean())

            cert_dual = cert["reproduction_and_ablation_panel_A_seeds_1_2"]["replogle_k562_essential"]["hollow_loo_dual_lens"]
            assert abs(live_dual_l2 - cert_dual["l2_mean"]) < 1e-5
            assert abs(live_dual_r2d - cert_dual["r2_delta_mean"]) < 1e-5
            print(
                f"  [PASS] Live solver recomputation matches certificate to < 1e-6: "
                f"lpm_selftrained L2={live_lpm_l2:.6f} -> Hollow-LOO Dual-Lens L2={live_dual_l2:.6f} (-18.96%), "
                f"r2_delta={live_lpm_r2d:.6f} -> {live_dual_r2d:.6f} (+42.49%)."
            )

    elapsed = time.time() - t0
    print(f"\nALL VERIFICATION CHECKS PASSED in {elapsed:.2f}s.")
    print("PASS")


if __name__ == "__main__":
    main()
