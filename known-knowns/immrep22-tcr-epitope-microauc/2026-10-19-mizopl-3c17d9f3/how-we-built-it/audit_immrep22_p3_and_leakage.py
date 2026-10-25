#!/opt/homebrew/bin/python3
"""
Comprehensive Audit for IMMREP22 TCR-Epitope Specificity (Run 2026-10-19-1826):
1. SHA-256 manifest of all benchmark files (training_data, test_set, true_set, negativeData_controls, evaluation).
2. Negative-sampling provenance audit (partial win p3): swapped-epitope VDJdb negatives vs healthy-donor control negatives (TCR_COV*.tsv).
3. Control-repertoire and train/test leakage audit.
4. Minimum Levenshtein distance (CDR3a + CDR3b) stratification audit.
5. Paired bootstrap (10,000 resamples) and Wilcoxon signed-rank test vs published baselines.
"""
import os, sys, glob, json, hashlib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from scipy.stats import wilcoxon

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = BASE_DIR

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def lev_dist(s1, s2):
    if s1 == s2:
        return 0
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[-1]

def main():
    pub_micro = pd.read_csv(os.path.join(BASE_DIR, "evaluation/microaucs.csv"), index_col=0)
    pub_rank = pd.read_csv(os.path.join(BASE_DIR, "evaluation/epitoperank.csv"), index_col=0)
    epitopes = [c for c in pub_micro.columns if c not in ("Unnamed: 1", "_Average", "ab", "cdr", "cluster")]

    # 1. Load healthy-donor control repertoire pool (TCR_COV*.tsv)
    ctrl_pairs = set()
    ctrl_trb = set()
    for f in sorted(glob.glob(os.path.join(BASE_DIR, "negativeData_controls/TCR_COV*.tsv"))):
        df_c = pd.read_csv(f, sep="\t")
        for a, b in zip(df_c["TRA_CDR3"], df_c["TRB_CDR3"]):
            ctrl_pairs.add((str(a), str(b)))
            ctrl_trb.add(str(b))

    # Positive VDJdb pool across all 17 epitopes (train + test positives)
    vdjdb_pos_by_ep = {}
    all_vdjdb_pos = set()
    for ep in epitopes:
        tr = pd.read_csv(os.path.join(BASE_DIR, f"training_data/{ep}.txt"), sep="\t")
        tu = pd.read_csv(os.path.join(BASE_DIR, f"true_set/{ep}.txt"), sep="\t")
        s = set()
        for a, b in zip(tr[tr["Label"] == 1]["TRA_CDR3"], tr[tr["Label"] == 1]["TRB_CDR3"]):
            s.add((str(a), str(b)))
            all_vdjdb_pos.add((str(a), str(b)))
        for a, b in zip(tu[tu["Label"] == 1]["TRA_CDR3"], tu[tu["Label"] == 1]["TRB_CDR3"]):
            s.add((str(a), str(b)))
            all_vdjdb_pos.add((str(a), str(b)))
        vdjdb_pos_by_ep[ep] = s

    # 2. Score directories to audit
    methods = {
        "clss_tcr": os.path.join(WORK_DIR, "clss_tcr_scores"),
        "tcrexab": os.path.join(WORK_DIR, "baseline_tcrexab"),
        "tcrexb": os.path.join(WORK_DIR, "baseline_tcrexb"),
        "tcrexa": os.path.join(WORK_DIR, "baseline_tcrexa"),
    }

    p3_table = {m: [] for m in methods}
    leakage_audit = []
    lev_strata_records = []

    for ep in epitopes:
        tr_df = pd.read_csv(os.path.join(BASE_DIR, f"training_data/{ep}.txt"), sep="\t")
        tu_df = pd.read_csv(os.path.join(BASE_DIR, f"true_set/{ep}.txt"), sep="\t")
        y_true = (tu_df["Label"].values == 1).astype(int)

        tr_pairs = set(zip(tr_df["TRA_CDR3"].astype(str), tr_df["TRB_CDR3"].astype(str)))
        tr_pos_pairs = set(zip(tr_df[tr_df["Label"] == 1]["TRA_CDR3"].astype(str), tr_df[tr_df["Label"] == 1]["TRB_CDR3"].astype(str)))
        tr_neg_pairs = set(zip(tr_df[tr_df["Label"] != 1]["TRA_CDR3"].astype(str), tr_df[tr_df["Label"] != 1]["TRB_CDR3"].astype(str)))
        te_pairs = list(zip(tu_df["TRA_CDR3"].astype(str), tu_df["TRB_CDR3"].astype(str)))

        # Provenance of each test row
        is_pos = (y_true == 1)
        is_ctrl_neg = np.array([(not p) and ((pair in ctrl_pairs) or (pair[1] in ctrl_trb and pair not in all_vdjdb_pos)) for p, pair in zip(is_pos, te_pairs)], dtype=bool)
        is_swap_neg = (~is_pos) & (~is_ctrl_neg)

        # Check train-test overlap for this epitope
        exact_overlap = len(tr_pairs.intersection(set(te_pairs)))
        ctrl_overlap = len(tr_neg_pairs.intersection(set([pair for pair, c in zip(te_pairs, is_ctrl_neg) if c])))

        # Minimum Levenshtein distance from each test TCR to any training positive TCR of this epitope
        tr_pos_list = list(tr_pos_pairs)
        min_lev_ab = []
        min_lev_b = []
        for a_te, b_te in te_pairs:
            d_ab = min(lev_dist(a_te, a_tr) + lev_dist(b_te, b_tr) for a_tr, b_tr in tr_pos_list)
            d_b = min(lev_dist(b_te, b_tr) for _, b_tr in tr_pos_list)
            min_lev_ab.append(d_ab)
            min_lev_b.append(d_b)
        min_lev_ab = np.array(min_lev_ab)
        min_lev_b = np.array(min_lev_b)

        leakage_audit.append({
            "epitope": ep,
            "n_train": int(len(tr_df)),
            "n_train_pos": int((tr_df["Label"] == 1).sum()),
            "n_train_neg": int((tr_df["Label"] != 1).sum()),
            "n_test": int(len(tu_df)),
            "n_test_pos": int(is_pos.sum()),
            "n_test_swap_neg": int(is_swap_neg.sum()),
            "n_test_ctrl_neg": int(is_ctrl_neg.sum()),
            "exact_train_test_pair_overlap": int(exact_overlap),
            "control_neg_train_test_overlap": int(ctrl_overlap),
            "test_pos_min_lev_ab_eq_0": int((min_lev_ab[is_pos] == 0).sum()),
            "test_pos_min_lev_ab_le_1": int((min_lev_ab[is_pos] <= 1).sum()),
            "test_pos_min_lev_ab_ge_2": int((min_lev_ab[is_pos] >= 2).sum()),
        })

        for m_name, m_dir in methods.items():
            sc_df = pd.read_csv(os.path.join(m_dir, f"{ep}.txt"), sep="\t")
            scores = sc_df["score"].values
            merged_eval = pd.merge(sc_df, tu_df, how="left", left_on=["TRA_CDR3", "TRB_CDR3"], right_on=["TRA_CDR3", "TRB_CDR3"])
            auc_all = float(roc_auc_score(merged_eval["Label"] == 1, merged_eval["score"]))
            auc_all_rowwise = float(roc_auc_score(y_true, scores))
            m_swap = is_pos | is_swap_neg
            m_ctrl = is_pos | is_ctrl_neg
            auc_swap = float(roc_auc_score(y_true[m_swap], scores[m_swap]))
            auc_ctrl = float(roc_auc_score(y_true[m_ctrl], scores[m_ctrl]))

            # Also compute AUC excluding near-duplicates (min_lev_ab >= 2)
            m_ge2 = (min_lev_ab >= 2)
            auc_ge2 = float(roc_auc_score(y_true[m_ge2], scores[m_ge2])) if (y_true[m_ge2].sum() > 0 and (1 - y_true[m_ge2]).sum() > 0) else float("nan")

            p3_table[m_name].append({
                "epitope": ep,
                "auc_all_neg": auc_all,
                "auc_all_neg_rowwise": auc_all_rowwise,
                "auc_swapped_neg_only": auc_swap,
                "auc_control_neg_only": auc_ctrl,
                "diff_ctrl_minus_swap": auc_ctrl - auc_swap,
                "auc_min_lev_ab_ge_2": auc_ge2,
            })

    # Summarize p3 and statistical tests
    summary_p3 = {}
    for m_name, rows in p3_table.items():
        df_m = pd.DataFrame(rows)
        summary_p3[m_name] = {
            "mean_auc_all_neg": float(df_m["auc_all_neg"].mean()),
            "mean_auc_swapped_neg_only": float(df_m["auc_swapped_neg_only"].mean()),
            "mean_auc_control_neg_only": float(df_m["auc_control_neg_only"].mean()),
            "mean_diff_ctrl_minus_swap": float(df_m["diff_ctrl_minus_swap"].mean()),
            "mean_auc_min_lev_ab_ge_2": float(df_m["auc_min_lev_ab_ge_2"].dropna().mean()),
            "per_epitope": rows,
        }

    # Paired bootstrap & Wilcoxon signed-rank test: clss_tcr vs tcrexab (re-run and published)
    clss_aucs = np.array([r["auc_all_neg"] for r in p3_table["clss_tcr"]])
    tcrexab_rerun_aucs = np.array([r["auc_all_neg"] for r in p3_table["tcrexab"]])
    tcrexab_pub_aucs = np.array([float(pub_micro.loc["tcrexab", ep]) for ep in epitopes])
    col_max_pub_aucs = np.array([float(pub_micro[ep].max()) for ep in epitopes])

    rng = np.random.default_rng(20261019)
    n_boot = 10000
    idx = rng.integers(0, len(epitopes), size=(n_boot, len(epitopes)))
    boot_diffs_pub = (clss_aucs[idx] - tcrexab_pub_aucs[idx]).mean(axis=1)
    boot_diffs_rerun = (clss_aucs[idx] - tcrexab_rerun_aucs[idx]).mean(axis=1)

    w_stat_pub, w_pval_pub = wilcoxon(clss_aucs - tcrexab_pub_aucs, alternative="greater")
    w_stat_rerun, w_pval_rerun = wilcoxon(clss_aucs - tcrexab_rerun_aucs, alternative="greater")

    # Single-epitope gains over all 22 published methods
    single_ep_vs_max = []
    for i, ep in enumerate(epitopes):
        best_m = str(pub_micro[ep].idxmax())
        best_v = float(pub_micro[ep].max())
        single_ep_vs_max.append({
            "epitope": ep,
            "clss_auc": float(clss_aucs[i]),
            "published_max_auc": best_v,
            "published_max_method": best_m,
            "gain_over_published_max": float(clss_aucs[i] - best_v),
            "tcrexab_published_auc": float(tcrexab_pub_aucs[i]),
            "gain_over_tcrexab_published": float(clss_aucs[i] - tcrexab_pub_aucs[i]),
        })

    out = {
        "benchmark_commit": "8942484a902a4694628f0e4f828012884f76382e",
        "microaucs_csv_sha256": sha256_file(os.path.join(BASE_DIR, "evaluation/microaucs.csv")),
        "epitoperank_csv_sha256": sha256_file(os.path.join(BASE_DIR, "evaluation/epitoperank.csv")),
        "evaluate_py_sha256": sha256_file(os.path.join(BASE_DIR, "evaluation/evaluate.py")),
        "clss_mean_microauc": float(clss_aucs.mean()),
        "published_best_mean_microauc": float(pub_micro["_Average"].max()),
        "published_best_method": str(pub_micro["_Average"].idxmax()),
        "mean_microauc_gain_over_published_best": float(clss_aucs.mean() - pub_micro["_Average"].max()),
        "mean_microauc_gain_over_tcrexab_rerun": float(clss_aucs.mean() - tcrexab_rerun_aucs.mean()),
        "epitopes_beating_tcrexab_published": int((clss_aucs > tcrexab_pub_aucs).sum()),
        "epitopes_beating_all_22_published_max": int((clss_aucs > col_max_pub_aucs).sum()),
        "epitopes_beating_all_22_published_max_by_0_03": [
            r for r in single_ep_vs_max if r["gain_over_published_max"] >= 0.03
        ],
        "statistical_tests": {
            "n_bootstrap": n_boot,
            "paired_bootstrap_win_rate_vs_tcrexab_published": float((boot_diffs_pub > 0).mean()),
            "paired_bootstrap_prob_gain_ge_0_02": float((boot_diffs_pub >= 0.02).mean()),
            "paired_bootstrap_ci95_gain_vs_tcrexab_published": [
                float(np.percentile(boot_diffs_pub, 2.5)),
                float(np.percentile(boot_diffs_pub, 97.5)),
            ],
            "wilcoxon_signed_rank_stat_vs_tcrexab_published": float(w_stat_pub),
            "wilcoxon_signed_rank_pval_one_sided_vs_tcrexab_published": float(w_pval_pub),
            "wilcoxon_signed_rank_pval_one_sided_vs_tcrexab_rerun": float(w_pval_rerun),
        },
        "single_epitope_comparison": single_ep_vs_max,
        "p3_negative_sampling_provenance_audit": summary_p3,
        "leakage_and_levenshtein_audit": leakage_audit,
    }

    manifest_path = os.path.join(WORK_DIR, "immrep22_audit_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(out, f, indent=2)
    print("Saved audit manifest to:", manifest_path)
    print(f"CLSS Mean MicroAUC:          {out['clss_mean_microauc']:.6f} (gain vs published best: {out['mean_microauc_gain_over_published_best']:+.6f})")
    print(f"Epitopes > tcrexab:          {out['epitopes_beating_tcrexab_published']}/17")
    print(f"Epitopes > all 22 pub max:   {out['epitopes_beating_all_22_published_max']}/17")
    print(f"Epitopes >= +0.03 over max:  {[r['epitope'] for r in out['epitopes_beating_all_22_published_max_by_0_03']]}")
    print(f"Wilcoxon p-val (1-sided):    {w_pval_pub:.6e}, Bootstrap win rate: {(boot_diffs_pub > 0).mean()*100:.2f}%, P(gain >= 0.02): {(boot_diffs_pub >= 0.02).mean()*100:.2f}%")
    for m_name, s in summary_p3.items():
        print(f"p3 [{m_name:8s}]: all_neg={s['mean_auc_all_neg']:.6f} | swapped_only={s['mean_auc_swapped_neg_only']:.6f} | ctrl_only={s['mean_auc_control_neg_only']:.6f} | diff(ctrl-swap)={s['mean_diff_ctrl_minus_swap']:+.6f} | min_lev>=2={s['mean_auc_min_lev_ab_ge_2']:.6f}")

if __name__ == "__main__":
    main()
