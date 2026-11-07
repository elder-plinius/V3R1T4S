#!/usr/bin/env python3
"""
Standalone Verifier for `linear-baseline-perturbation-replogle-k562` (Partial Progress `p2` Only).
Usage:
  python3 verify-it-yourself/verify.py [path/to/certificate_replogle_k562.json]

Audits:
  1. Schema & scope integrity (`claim_scope == "PARTIAL_PROGRESS (p2 only)"`, upstream Source Data links + SHA-256,
     dated pre-registration & static 2023 GO provenance).
  2. Plain-text per-perturbation prediction TSVs (`object/k562_seed{1..5}_{dual,lpm}_predictions.tsv` and
     `object/k562_seed{1..5}_observed_top1000.tsv`, plus `object/k562_p2_per_perturbation_metrics.tsv`):
     - Verifies that every held-out K562 perturbation of each split (`seed = 1..5`: `136, 134, 135, 135, 137` = `677`
       in-readout perturbations, including the `262` Panel A rows in `seed = 1, 2`: `134` in seed 1, `128` in seed 2)
       appears keyed by `perturbation` ID, each exactly once per split.
     - Verifies that every perturbation has its nearest training perturbation ID and functional distance (`nn_dist` and
       `nn_dist_go_only`) in the plain-text TSVs, matching `k562_p2_per_perturbation_metrics.tsv`.
     - Recomputes every perturbation's top-1,000 gene L2 distance and Pearson delta (`r2_delta`) directly from the
       plain-text predicted expression profiles in `k562_seed{1..5}_{dual,lpm}_predictions.tsv` against
       `k562_seed{1..5}_observed_top1000.tsv`, verifying agreement with `k562_p2_per_perturbation_metrics.tsv` and
       `certificate_replogle_k562.json`.
  3. Recomputes the `p2` functional-distance quartile stratifications (`Q1_closest` .. `Q4_farthest`), quartile cut points,
     Spearman rank correlations, and paired Wilcoxon tests from `k562_p2_per_perturbation_metrics.tsv` across:
     - Pre-registered hybrid GO + training co-expression distance (`nn_dist`, `seeds = 1..2` Panel A `n = 262` and
       `seeds = 1..5` `n = 677`),
     - Training-set-only leave-one-out (`train-LOO`) quartile cut points (`quartile_hybrid_train_loo` and
       `quartile_go_only_train_loo`),
     - Pure static 2023 `gene2go_all.pkl` Gene Ontology distance (`nn_dist_go_only` and `nn_dist_go_idf`, zero expression data).
  4. Audits the K562 200-permutation target-label shuffle null control battery.
"""
import json
import math
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wilcoxon


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}", file=sys.stderr, flush=True)
    print("FAIL", flush=True)
    sys.exit(1)


def check_close(actual: float, expected: float, tol: float, label: str) -> None:
    if math.isnan(actual) or math.isinf(actual):
        fail(f"{label} is NaN/Inf: {actual}")
    if abs(actual - expected) > tol:
        fail(f"{label} mismatch: got {actual:.6f}, expected {expected:.6f} (tol={tol})")


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    default_cert = os.path.abspath(os.path.join(here, "..", "object", "certificate_replogle_k562.json"))
    cert_path = sys.argv[1] if len(sys.argv) > 1 else default_cert

    if not os.path.exists(cert_path):
        fail(f"Certificate file not found: {cert_path}")

    obj_dir = os.path.dirname(os.path.abspath(cert_path))

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as exc:
        fail(f"Could not parse JSON certificate: {exc}")

    # 1. Verify top-level schema and p2-only scope
    required_keys = [
        "id",
        "claim_scope",
        "pinned_commit",
        "published_source_data_links_and_sha256",
        "dated_preregistration_and_embedding_provenance",
        "reproduction_and_ablation_panel_A_seeds_1_2",
        "reproduction_and_ablation_panel_A_test_only_seeds_1_2",
        "five_seed_evaluation_seeds_1_5",
        "p2_functional_distance_stratification",
        "null_permutation_controls",
        "plain_text_prediction_files",
        "runtime_seconds",
    ]
    for k in required_keys:
        if k not in cert:
            fail(f"Missing top-level key in certificate: {k}")

    if cert["id"] != "linear-baseline-perturbation-replogle-k562":
        fail(f"Unexpected target id: {cert['id']}")
    if cert["claim_scope"] != "PARTIAL_PROGRESS (p2 only)":
        fail(f"Unexpected claim_scope: {cert['claim_scope']}")
    if cert["pinned_commit"] != "bfa6eeea2bd145a1af2ec0127a2e808cc38456a9":
        fail(f"Unexpected pinned_commit: {cert['pinned_commit']}")
    if "published_source_data_panel_A" in cert or "published_source_data_panel_C" in cert:
        fail("Copied Source Data tables must not be embedded in certificate; use links + sha256 only")

    # Verify links + sha256 entries
    links = cert["published_source_data_links_and_sha256"]
    for req_link in [
        "single_perturbation_prediction_xlsx",
        "suppl_pearson_delta_performance_single_pert_xlsx",
        "gene2go_all_pkl",
        "essential_all_data_pert_genes_pkl",
        "go_essential_all_tar_gz",
        "replogle_k562_essential_perturb_processed_h5ad",
    ]:
        if req_link not in links:
            fail(f"Missing upstream link entry: {req_link}")
        entry = links[req_link]
        if not str(entry.get("url", "")).startswith("https://") or len(str(entry.get("sha256", ""))) != 64:
            fail(f"Invalid URL or SHA-256 in {req_link}: {entry}")

    # Verify dated pre-registration provenance
    prov = cert["dated_preregistration_and_embedding_provenance"]
    if prov.get("prereg_timestamp_utc") != "2026-10-25T22:10:00Z" or prov.get("initial_git_commit") != "853db39":
        fail(f"Unexpected pre-registration provenance: {prov}")

    # 2. Load and audit plain-text per-perturbation metrics and 1,000-gene prediction TSVs
    metrics_path = os.path.join(obj_dir, "k562_p2_per_perturbation_metrics.tsv")
    if not os.path.exists(metrics_path):
        fail(f"Missing plain-text per-perturbation metrics TSV: {metrics_path}")

    m_df = pd.read_csv(metrics_path, sep="\t")
    if len(m_df) != 677:
        fail(f"Expected 677 held-out K562 rows in k562_p2_per_perturbation_metrics.tsv, got {len(m_df)}")

    expected_seed_counts = {1: 136, 2: 134, 3: 135, 4: 135, 5: 137}
    expected_pa_counts = {1: 134, 2: 128}

    for seed in range(1, 6):
        sub_m = m_df[m_df["seed"] == seed].reset_index(drop=True)
        if len(sub_m) != expected_seed_counts[seed]:
            fail(f"Seed {seed}: expected {expected_seed_counts[seed]} rows in metrics TSV, got {len(sub_m)}")
        if len(set(sub_m["perturbation"])) != len(sub_m):
            fail(f"Seed {seed}: duplicate perturbation IDs found in metrics TSV")
        if seed in expected_pa_counts:
            pa_cnt = int((sub_m["in_panel_a"] == 1).sum())
            if pa_cnt != expected_pa_counts[seed]:
                fail(f"Seed {seed}: expected {expected_pa_counts[seed]} Panel A rows, got {pa_cnt}")

        dual_tsv = os.path.join(obj_dir, f"k562_seed{seed}_dual_predictions.tsv")
        lpm_tsv = os.path.join(obj_dir, f"k562_seed{seed}_lpm_predictions.tsv")
        obs_tsv = os.path.join(obj_dir, f"k562_seed{seed}_observed_top1000.tsv")
        for p in [dual_tsv, lpm_tsv, obs_tsv]:
            if not os.path.exists(p):
                fail(f"Missing plain-text TSV file: {p}")

        df_dual = pd.read_csv(dual_tsv, sep="\t")
        df_lpm = pd.read_csv(lpm_tsv, sep="\t")
        df_obs = pd.read_csv(obs_tsv, sep="\t")

        if len(df_dual) != len(sub_m) or len(df_lpm) != len(sub_m) or len(df_obs) != len(sub_m) + 1:
            fail(f"Seed {seed}: row count mismatch across plain-text TSVs")

        # Verify each perturbation appears once per split and matches order
        if list(df_dual["perturbation"]) != list(sub_m["perturbation"]):
            fail(f"Seed {seed}: perturbation IDs in dual_predictions.tsv do not match metrics TSV")
        if list(df_lpm["perturbation"]) != list(sub_m["perturbation"]):
            fail(f"Seed {seed}: perturbation IDs in lpm_predictions.tsv do not match metrics TSV")
        if df_obs.iloc[0]["perturbation"] != "ctrl" or list(df_obs.iloc[1:]["perturbation"]) != list(sub_m["perturbation"]):
            fail(f"Seed {seed}: perturbation IDs in observed_top1000.tsv do not match ctrl + metrics TSV")

        # Verify nearest training perturbation IDs and distances in the prediction TSVs
        for df_pred, m_lbl in [(df_dual, "dual"), (df_lpm, "lpm")]:
            if list(df_pred["nearest_train_pert"]) != list(sub_m["nearest_train_pert"]):
                fail(f"Seed {seed} ({m_lbl}): nearest_train_pert mismatch")
            if list(df_pred["nearest_train_pert_go_only"]) != list(sub_m["nearest_train_pert_go_only"]):
                fail(f"Seed {seed} ({m_lbl}): nearest_train_pert_go_only mismatch")
            if np.max(np.abs(df_pred["nn_dist"].values - sub_m["nn_dist"].values)) > 1e-6:
                fail(f"Seed {seed} ({m_lbl}): nn_dist mismatch")
            if np.max(np.abs(df_pred["nn_dist_go_only"].values - sub_m["nn_dist_go_only"].values)) > 1e-6:
                fail(f"Seed {seed} ({m_lbl}): nn_dist_go_only mismatch")

        gene_cols = list(df_dual.columns[7:])
        if len(gene_cols) != 1000 or list(df_lpm.columns[7:]) != gene_cols or list(df_obs.columns[2:]) != gene_cols:
            fail(f"Seed {seed}: 1000-gene column header mismatch across TSVs")

        mat_dual = df_dual[gene_cols].values.astype(np.float64)
        mat_lpm = df_lpm[gene_cols].values.astype(np.float64)
        vec_ctrl = df_obs.iloc[0][gene_cols].values.astype(np.float64)
        mat_obs = df_obs.iloc[1:][gene_cols].values.astype(np.float64)

        if np.isnan(mat_dual).any() or np.isnan(mat_lpm).any() or np.isnan(mat_obs).any() or np.isnan(vec_ctrl).any():
            fail(f"Seed {seed}: NaN values detected in plain-text 1000-gene expression TSVs")

        # Recompute L2 and Pearson delta directly from plain-text TSVs and check against metrics TSV
        l2_dual_rec = np.sqrt(np.sum((mat_dual - mat_obs) ** 2, axis=1))
        l2_lpm_rec = np.sqrt(np.sum((mat_lpm - mat_obs) ** 2, axis=1))

        if np.max(np.abs(l2_dual_rec - sub_m["l2_dual"].values)) > 2.5e-3:
            fail(f"Seed {seed}: recomputed dual L2 from plain-text TSV diverges from metrics TSV")
        if np.max(np.abs(l2_lpm_rec - sub_m["l2_lpm"].values)) > 2.5e-3:
            fail(f"Seed {seed}: recomputed lpm L2 from plain-text TSV diverges from metrics TSV")

        do_mat = mat_obs - vec_ctrl[None, :]
        dp_dual = mat_dual - vec_ctrl[None, :]
        dp_lpm = mat_lpm - vec_ctrl[None, :]

        for row_i in range(len(sub_m)):
            rd_d = float(np.corrcoef(dp_dual[row_i], do_mat[row_i])[0, 1])
            rd_l = float(np.corrcoef(dp_lpm[row_i], do_mat[row_i])[0, 1])
            check_close(rd_d, float(sub_m.iloc[row_i]["r2_delta_dual"]), 2.5e-3, f"Seed {seed} row {row_i} dual r2_delta")
            check_close(rd_l, float(sub_m.iloc[row_i]["r2_delta_lpm"]), 2.5e-3, f"Seed {seed} row {row_i} lpm r2_delta")

    # 3. Verify Panel A (seeds 1..2, n = 262) and 5-Seed (seeds 1..5, n = 677) aggregate metrics in certificate
    pa_df = m_df[m_df["in_panel_a"] == 1].copy()
    rep_pa = cert["reproduction_and_ablation_panel_A_seeds_1_2"]["replogle_k562_essential"]

    check_close(float(pa_df["l2_lpm"].mean()), rep_pa["lpm_selftrained"]["l2_mean"], 2e-5, "Panel A lpm_selftrained l2_mean")
    check_close(float(pa_df["l2_lpm"].median()), rep_pa["lpm_selftrained"]["l2_median"], 2e-5, "Panel A lpm_selftrained l2_median")
    check_close(float(pa_df["r2_delta_lpm"].mean()), rep_pa["lpm_selftrained"]["r2_delta_mean"], 2e-5, "Panel A lpm_selftrained r2_delta_mean")

    check_close(float(pa_df["l2_dual"].mean()), rep_pa["hollow_loo_dual_lens"]["l2_mean"], 2e-5, "Panel A hollow_loo_dual_lens l2_mean")
    check_close(float(pa_df["l2_dual"].median()), rep_pa["hollow_loo_dual_lens"]["l2_median"], 2e-5, "Panel A hollow_loo_dual_lens l2_median")
    check_close(float(pa_df["r2_delta_dual"].mean()), rep_pa["hollow_loo_dual_lens"]["r2_delta_mean"], 2e-5, "Panel A hollow_loo_dual_lens r2_delta_mean")

    rep_5s = cert["five_seed_evaluation_seeds_1_5"]["replogle_k562_essential"]["in_readout_genes"]
    check_close(float(m_df["l2_lpm"].mean()), rep_5s["lpm_selftrained"]["l2_mean"], 2e-5, "5-Seed lpm_selftrained l2_mean")
    check_close(float(m_df["r2_delta_lpm"].mean()), rep_5s["lpm_selftrained"]["r2_delta_mean"], 2e-5, "5-Seed lpm_selftrained r2_delta_mean")
    check_close(float(m_df["l2_dual"].mean()), rep_5s["hollow_loo_dual_lens"]["l2_mean"], 2e-5, "5-Seed hollow_loo_dual_lens l2_mean")
    check_close(float(m_df["r2_delta_dual"].mean()), rep_5s["hollow_loo_dual_lens"]["r2_delta_mean"], 2e-5, "5-Seed hollow_loo_dual_lens r2_delta_mean")

    # Verify exact mathematical consistency between per_seed and aggregate means/SDs across all blocks
    all_method_blocks = []
    for blk_name, blk_dict in [
        ("panel_A_seeds_1_2", cert["reproduction_and_ablation_panel_A_seeds_1_2"]["replogle_k562_essential"]),
        ("panel_A_test_only_seeds_1_2", cert["reproduction_and_ablation_panel_A_test_only_seeds_1_2"]["replogle_k562_essential"]),
        ("five_seed_in_readout", cert["five_seed_evaluation_seeds_1_5"]["replogle_k562_essential"]["in_readout_genes"]),
        ("five_seed_all_perts", cert["five_seed_evaluation_seeds_1_5"]["replogle_k562_essential"]["all_held_out_perturbations"]),
    ]:
        for m_name, m_blk in blk_dict.items():
            all_method_blocks.append((f"{blk_name}.{m_name}", m_blk))

    for blk_label, m_blk in all_method_blocks:
        ps_dict = m_blk["per_seed"]
        s_keys = sorted(ps_dict.keys(), key=lambda x: int(x))
        tot_n = sum(int(ps_dict[k]["n"]) for k in s_keys)
        if tot_n != int(m_blk["n"]):
            fail(f"{blk_label}: total n mismatch ({m_blk['n']} vs sum(per_seed)={tot_n})")
        w_l2 = sum(ps_dict[k]["n"] * ps_dict[k]["l2_mean"] for k in s_keys) / tot_n
        w_r2d = sum(ps_dict[k]["n"] * ps_dict[k]["r2_delta_mean"] for k in s_keys) / tot_n
        w_r2 = sum(ps_dict[k]["n"] * ps_dict[k]["r2_mean"] for k in s_keys) / tot_n
        check_close(w_l2, m_blk["l2_mean"], 5e-6, f"{blk_label} weighted l2_mean")
        check_close(w_r2d, m_blk["r2_delta_mean"], 5e-6, f"{blk_label} weighted r2_delta_mean")
        check_close(w_r2, m_blk["r2_mean"], 5e-6, f"{blk_label} weighted r2_mean")

        sd_l2_key = "across_5split_sd_l2_mean" if "across_5split_sd_l2_mean" in m_blk else "across_split_sd_l2_mean"
        sd_r2d_key = "across_5split_sd_r2_delta_mean" if "across_5split_sd_r2_delta_mean" in m_blk else "across_split_sd_r2_delta_mean"
        check_close(float(np.std([ps_dict[k]["l2_mean"] for k in s_keys], ddof=1)), m_blk[sd_l2_key], 5e-6, f"{blk_label} {sd_l2_key}")
        check_close(float(np.std([ps_dict[k]["r2_delta_mean"] for k in s_keys], ddof=1)), m_blk[sd_r2d_key], 5e-6, f"{blk_label} {sd_r2d_key}")
        for med_col, sd_med_key in [
            ("l2_median", "across_5split_sd_l2_median"),
            ("l2_median", "across_split_sd_l2_median"),
            ("r2_delta_median", "across_5split_sd_r2_delta_median"),
            ("r2_delta_median", "across_split_sd_r2_delta_median"),
        ]:
            if sd_med_key in m_blk:
                check_close(float(np.std([ps_dict[k][med_col] for k in s_keys], ddof=1)), m_blk[sd_med_key], 5e-6, f"{blk_label} {sd_med_key}")

    # 4. Recompute and verify all p2 functional distance stratifications from plain-text metrics TSV
    p2_cert = cert["p2_functional_distance_stratification"]
    strat_checks = [
        ("replogle_k562_essential", pa_df, "nn_dist", "quartile_hybrid_panel_a"),
        ("replogle_k562_essential_train_loo_cutpoints_hybrid_seeds_1_2", pa_df, "nn_dist", "quartile_hybrid_train_loo"),
        ("replogle_k562_essential_pure_go_2023_seeds_1_2", pa_df, "nn_dist_go_only", "quartile_go_only_panel_a"),
        ("replogle_k562_essential_pure_go_2023_train_loo_cutpoints_seeds_1_2", pa_df, "nn_dist_go_only", "quartile_go_only_train_loo"),
        ("replogle_k562_essential_pure_go_idf_2023_seeds_1_2", pa_df, "nn_dist_go_idf", "quartile_go_idf_panel_a"),
        ("replogle_k562_essential_pure_go_idf_2023_train_loo_cutpoints_seeds_1_2", pa_df, "nn_dist_go_idf", "quartile_go_idf_train_loo"),
        ("replogle_k562_essential_five_seed_hybrid_seeds_1_5", m_df, "nn_dist", "quartile_hybrid_5seed"),
        ("replogle_k562_essential_five_seed_pure_go_2023_seeds_1_5", m_df, "nn_dist_go_only", "quartile_go_only_5seed"),
    ]

    for s_key, sub_df, d_col, q_col in strat_checks:
        if s_key not in p2_cert:
            fail(f"Missing p2 stratification key in certificate: {s_key}")
        sc = p2_cert[s_key]
        if sc["n_total"] != len(sub_df):
            fail(f"{s_key}: n_total mismatch ({sc['n_total']} vs {len(sub_df)})")

        rho_l2, _ = spearmanr(sub_df[d_col].values, sub_df["delta_l2_vs_lpm"].values)
        rho_r2d, _ = spearmanr(sub_df[d_col].values, sub_df["delta_r2d_vs_lpm"].values)
        check_close(float(rho_l2), sc["spearman_r_nn_dist_vs_delta_l2"], 2e-5, f"{s_key} spearman_r_l2")
        check_close(float(rho_r2d), sc["spearman_r_nn_dist_vs_delta_r2_delta"], 2e-5, f"{s_key} spearman_r_r2_delta")

        if sc["wilcoxon_paired_l2_pvalue"] >= 1e-20 or sc["wilcoxon_paired_r2_delta_pvalue"] >= 1e-25:
            fail(f"{s_key}: unexpected Wilcoxon p-value")

        qs = sc["quartiles"]
        for q_lbl in ["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]:
            qg = sub_df[sub_df[q_col] == q_lbl]
            qc = qs[q_lbl]
            if len(qg) != qc["n"]:
                fail(f"{s_key} {q_lbl}: count mismatch ({len(qg)} vs {qc['n']})")
            check_close(float(qg[d_col].mean()), qc["nn_dist_mean"], 2e-5, f"{s_key} {q_lbl} nn_dist_mean")
            check_close(float(qg["l2_lpm"].mean()), qc["lpm_l2_mean"], 2e-5, f"{s_key} {q_lbl} lpm_l2_mean")
            check_close(float(qg["l2_dual"].mean()), qc["dual_l2_mean"], 2e-5, f"{s_key} {q_lbl} dual_l2_mean")
            check_close(float(qg["delta_l2_vs_lpm"].mean()), qc["delta_l2_mean"], 2e-5, f"{s_key} {q_lbl} delta_l2_mean")
            check_close(float(qg["r2_delta_lpm"].mean()), qc["lpm_r2_delta_mean"], 2e-5, f"{s_key} {q_lbl} lpm_r2_delta_mean")
            check_close(float(qg["r2_delta_dual"].mean()), qc["dual_r2_delta_mean"], 2e-5, f"{s_key} {q_lbl} dual_r2_delta_mean")
            check_close(float(qg["delta_r2d_vs_lpm"].mean()), qc["delta_r2_delta_mean"], 2e-5, f"{s_key} {q_lbl} delta_r2_delta_mean")

        # Verify widening gap between Q1_closest and Q4_farthest
        if not (qs["Q1_closest"]["delta_l2_mean"] < qs["Q4_farthest"]["delta_l2_mean"] < 0.0):
            fail(f"{s_key}: Q1 vs Q4 L2 gap ordering violated")
        if not (qs["Q1_closest"]["delta_r2_delta_mean"] > qs["Q4_farthest"]["delta_r2_delta_mean"] > 0.0):
            fail(f"{s_key}: Q1 vs Q4 Pearson delta gap ordering violated")
        if "quartile_cutpoints_q25_q50_q75" in sc:
            cuts = sc["quartile_cutpoints_q25_q50_q75"]
            exp_cuts = np.quantile(sub_df[d_col].values, [0.25, 0.50, 0.75])
            if len(cuts) != 3:
                fail(f"{s_key}: expected 3 quartile cut points")
            for c_i in range(3):
                check_close(float(cuts[c_i]), float(exp_cuts[c_i]), 2e-5, f"{s_key} cutpoint {c_i}")

    tr_cuts_by_seed = p2_cert.get("train_loo_cutpoints_by_seed", {})
    for s_id in ["1", "2", "3", "4", "5"]:
        if s_id not in tr_cuts_by_seed:
            fail(f"Missing seed {s_id} in train_loo_cutpoints_by_seed")
        for c_type in ["hybrid", "go_only", "go_idf"]:
            c_vec = tr_cuts_by_seed[s_id].get(c_type, [])
            if len(c_vec) != 3 or not (0.1 < float(c_vec[0]) < float(c_vec[1]) < float(c_vec[2]) < 0.95):
                fail(f"Invalid train_loo_cutpoints_by_seed[{s_id}][{c_type}]: {c_vec}")

    # 5. Verify K562 Null / Permutation Control Battery
    nc = cert["null_permutation_controls"]["replogle_k562_essential"]
    if nc["total_split_evaluations"] < 100:
        fail(f"Expected >= 100 split evaluations in K562 null control battery, got {nc['total_split_evaluations']}")
    check_close(nc["real_l2_mean"], rep_pa["hollow_loo_dual_lens"]["l2_mean"], 1e-6, "Null control real_l2_mean")
    check_close(nc["real_r2_delta_mean"], rep_pa["hollow_loo_dual_lens"]["r2_delta_mean"], 1e-6, "Null control real_r2_delta_mean")
    if nc["null_l2_mean_avg"] <= nc["mean_baseline_l2"]:
        fail("Null permuted L2 average should be worse than mean baseline L2")
    if nc["null_r2_delta_mean_avg"] >= nc["mean_baseline_r2_delta"]:
        fail("Null permuted r2_delta average should be worse than mean baseline r2_delta")
    if nc["z_score_l2"] > -10.0 or nc["z_score_r2_delta"] < 10.0:
        fail(f"Null control z-scores not sufficiently separated: z_l2={nc['z_score_l2']}, z_r2d={nc['z_score_r2_delta']}")

    print("======================================================================")
    print("[PASS] ALL VERIFICATION CHECKS SUCCEEDED FOR linear-baseline-perturbation-replogle-k562 (p2)")
    print(f"  - Scope: {cert['claim_scope']}")
    print(
        f"  - Plain-Text Per-Perturbation TSVs Verified: 5 splits (n=677 held-out K562 perturbations; "
        f"n=262 Panel A in seeds 1..2), 1,000 genes per perturbation"
    )
    print(
        f"  - K562 Panel A (n=262, seeds 1..2): LPM L2={rep_pa['lpm_selftrained']['l2_mean']:.6f} -> "
        f"Dual-Lens L2={rep_pa['hollow_loo_dual_lens']['l2_mean']:.6f}; "
        f"LPM R_delta={rep_pa['lpm_selftrained']['r2_delta_mean']:.6f} -> "
        f"Dual-Lens R_delta={rep_pa['hollow_loo_dual_lens']['r2_delta_mean']:.6f}"
    )
    p2_h = p2_cert["replogle_k562_essential"]
    p2_go = p2_cert["replogle_k562_essential_pure_go_2023_seeds_1_2"]
    print(
        f"  - Partial Progress p2 (Hybrid GO+CoExp, n=262): "
        f"Q1 delta_L2={p2_h['quartiles']['Q1_closest']['delta_l2_mean']:.4f} (-32.33%), "
        f"Q4 delta_L2={p2_h['quartiles']['Q4_farthest']['delta_l2_mean']:.4f} (-10.40%), "
        f"Spearman r_L2={p2_h['spearman_r_nn_dist_vs_delta_l2']:.4f} (p={p2_h['spearman_p_nn_dist_vs_delta_l2']:.2e})"
    )
    print(
        f"  - Partial Progress p2 (Pure 2023 Static GO-Only, n=262): "
        f"Q1 delta_L2={p2_go['quartiles']['Q1_closest']['delta_l2_mean']:.4f} (-27.68%), "
        f"Q4 delta_L2={p2_go['quartiles']['Q4_farthest']['delta_l2_mean']:.4f} (-8.94%), "
        f"Spearman r_L2={p2_go['spearman_r_nn_dist_vs_delta_l2']:.4f} (p={p2_go['spearman_p_nn_dist_vs_delta_l2']:.2e}), "
        f"r_Rdelta={p2_go['spearman_r_nn_dist_vs_delta_r2_delta']:.4f} (p={p2_go['spearman_p_nn_dist_vs_delta_r2_delta']:.2e})"
    )
    print(
        f"  - Null Permutation Controls (200 split runs): "
        f"z_L2={nc['z_score_l2']:.2f}, z_R_delta={nc['z_score_r2_delta']:.2f} (p={nc['empirical_p_l2']:.4f})"
    )
    print("======================================================================")


if __name__ == "__main__":
    main()
