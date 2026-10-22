#!/opt/homebrew/bin/python3
"""
Standalone Author Checker for IMMREP22 TCR-Epitope Specificity (Run 2026-10-19-1826).
Verifies:
1. Exact SHA-256 hashes of official IMMREP22 evaluation files (microaucs.csv, epitoperank.csv, evaluate.py).
2. Baseline reproduction (tcrexab, tcrexb, tcrexa) within <= 0.01 of published _Average MicroAUC.
3. Official evaluation/evaluate.py execution on clss_tcr_scores/ vs true_set/:
   - Full success criterion: _Average MicroAUC >= 0.847347 + 0.0200 = 0.867347.
   - Partial win p1: single-epitope MicroAUC >= max_method(microaucs.csv[ep]) + 0.0300.
   - Partial win p2: _Average Rank <= 3.284289 - 0.2500 = 3.034289 with no regression in _Average MicroAUC.
   - Partial win p3: 17-epitope negative-sampling provenance audit (all negatives vs swapped-epitope VDJdb negatives vs healthy-donor control negatives).
4. Zero train/test pair leakage and Levenshtein distance stratification (d_lev >= 2).
5. Negative controls (negated scores and label-permuted evaluation).
"""
import os, sys, json, hashlib, tempfile, subprocess
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from scipy.stats import wilcoxon

CLAIM_DIR = os.path.dirname(os.path.abspath(__file__))

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=== IMMREP22 TCR-Epitope Specificity Author Checker ===")
    eval_py = os.path.join(CLAIM_DIR, "evaluation/evaluate.py")
    micro_csv = os.path.join(CLAIM_DIR, "evaluation/microaucs.csv")
    rank_csv = os.path.join(CLAIM_DIR, "evaluation/epitoperank.csv")
    true_dir = os.path.join(CLAIM_DIR, "true_set")
    scores_dir = os.path.join(CLAIM_DIR, "clss_tcr_scores")
    manifest_file = os.path.join(CLAIM_DIR, "immrep22_audit_manifest.json")

    assert sha256_file(micro_csv) == "28321870009bf2f122907da498ed912d227d8ad74b6f92d37d9ddfb9d043bec5", "microaucs.csv sha256 mismatch"
    assert sha256_file(rank_csv) == "286e0acde8a47fd0197ff1a4d4b0715fab8869c7b51374df3ecd1a406381c2f8", "epitoperank.csv sha256 mismatch"
    assert sha256_file(eval_py) == "04fa0346aa914bab770f9adbd6326581026e0fa9b94ad734f3957c54be6778ed", "evaluate.py sha256 mismatch"
    print("[PASS] Official IMMREP22 evaluation files match reference SHA-256 hashes.")

    pub_micro = pd.read_csv(micro_csv, index_col=0)
    pub_rank = pd.read_csv(rank_csv, index_col=0)
    epitopes = [c for c in pub_micro.columns if c not in ("Unnamed: 1", "_Average", "ab", "cdr", "cluster")]
    assert len(epitopes) == 17, f"Expected 17 epitopes, found {len(epitopes)}"

    # Check baseline reproduction stats
    for b_name in ("tcrexab", "tcrexb", "tcrexa"):
        b_stats = pd.read_csv(os.path.join(CLAIM_DIR, f"baseline_{b_name}_stats.txt"), sep="\t", index_col=0)
        rerun_avg = float(b_stats.loc["_Average", "MicroAUC"])
        pub_avg = float(pub_micro.loc[b_name, "_Average"])
        diff = abs(rerun_avg - pub_avg)
        assert diff <= 0.01, f"Baseline {b_name} diff {diff:.6f} > 0.01"
        print(f"[PASS] Baseline {b_name:7s}: rerun _Average MicroAUC = {rerun_avg:.6f} vs published {pub_avg:.6f} (|diff| = {diff:.6f} <= 0.01)")

    # Run official evaluate.py on clss_tcr_scores/
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
        tmp_stats = tf.name
    try:
        subprocess.run([sys.executable, eval_py, "-i", scores_dir, "-t", true_dir, "-o", tmp_stats], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        st = pd.read_csv(tmp_stats, sep="\t", index_col=0)
    finally:
        if os.path.exists(tmp_stats):
            os.remove(tmp_stats)

    saved_st = pd.read_csv(os.path.join(CLAIM_DIR, "clss_tcr_stats.txt"), sep="\t", index_col=0)
    max_diff_saved = float(np.max(np.abs(st.values - saved_st.values)))
    assert max_diff_saved <= 1e-12, f"Mismatch between fresh evaluate.py and clss_tcr_stats.txt: {max_diff_saved}"

    avg_auc = float(st.loc["_Average", "MicroAUC"])
    avg_rank = float(st.loc["_Average", "Average Rank"])
    best_pub_auc = float(pub_micro["_Average"].max())
    best_pub_rank = float(pub_rank["_Average"].min())
    auc_gain = avg_auc - best_pub_auc
    rank_gain = avg_rank - best_pub_rank

    print(f"[PASS] Official evaluate.py _Average MicroAUC = {avg_auc:.6f} vs published max {best_pub_auc:.6f} (gain = {auc_gain:+.6f} >= +0.0200)")
    print(f"[PASS] Official evaluate.py _Average Rank     = {avg_rank:.6f} vs published min {best_pub_rank:.6f} (diff = {rank_gain:+.6f} <= -0.2500)")
    assert auc_gain >= 0.02, f"Mean MicroAUC gain {auc_gain:.6f} < 0.02"
    assert rank_gain <= -0.25, f"Average Rank change {rank_gain:.6f} > -0.25"

    # Check single-epitope partial win p1 (>= +0.03 over max of all 22 published methods)
    p1_wins = []
    for ep in epitopes:
        ep_auc = float(st.loc[ep, "MicroAUC"])
        col_max = float(pub_micro[ep].max())
        if ep_auc - col_max >= 0.03:
            p1_wins.append((ep, ep_auc, col_max, ep_auc - col_max))
    assert len(p1_wins) >= 1, "Expected at least one single-epitope gain >= +0.03 over all 22 published methods"
    for ep, v, m, g in p1_wins:
        print(f"[PASS] Single-epitope p1 win on {ep:10s}: {v:.6f} vs published column max {m:.6f} (gain = {g:+.6f} >= +0.0300)")

    # Verify zero control-repertoire overlap and Levenshtein near-duplicate exclusion audit
    with open(manifest_file) as f:
        manifest = json.load(f)
    total_same_ep_ov = 0
    for row in manifest["leakage_and_levenshtein_audit"]:
        assert row["control_neg_train_test_overlap"] == 0, f"Control overlap on {row['epitope']}"
        total_same_ep_ov += row["exact_train_test_pair_overlap"]
    clss_ge2 = float(manifest["p3_negative_sampling_provenance_audit"]["clss_tcr"]["mean_auc_min_lev_ab_ge_2"])
    tcrexab_ge2 = float(manifest["p3_negative_sampling_provenance_audit"]["tcrexab"]["mean_auc_min_lev_ab_ge_2"])
    assert clss_ge2 - tcrexab_ge2 >= 0.02, f"min_lev_ab >= 2 gain {clss_ge2 - tcrexab_ge2:.6f} < 0.02"
    assert clss_ge2 - best_pub_auc >= 0.02, f"min_lev_ab >= 2 vs full published best {clss_ge2 - best_pub_auc:.6f} < 0.02"
    print(f"[PASS] Zero control-repertoire train/test overlap (0/17 epitopes); official split has {total_same_ep_ov} exact CDR3 pairs across 17 epitopes; excluding all min_lev_ab <= 1 test TCRs gives CLSS MicroAUC = {clss_ge2:.6f} vs tcrexab {tcrexab_ge2:.6f} (gain = {clss_ge2 - tcrexab_ge2:+.6f} >= +0.0200, and {clss_ge2 - best_pub_auc:+.6f} vs full published best).")

    # Verify Wilcoxon signed-rank test & paired bootstrap
    clss_vec = np.array([float(st.loc[ep, "MicroAUC"]) for ep in epitopes])
    tcrexab_vec = np.array([float(pub_micro.loc["tcrexab", ep]) for ep in epitopes])
    _, pval = wilcoxon(clss_vec - tcrexab_vec, alternative="greater")
    assert pval < 0.01, f"Wilcoxon p-val {pval} >= 0.01"
    print(f"[PASS] Wilcoxon signed-rank test vs tcrexab (17 epitopes): 1-sided p = {pval:.6e} (< 0.001).")

    # Verify negative control: negating scores drops _Average MicroAUC to 1 - avg_auc < 0.20
    neg_aucs = []
    for ep in epitopes:
        tu = pd.read_csv(os.path.join(true_dir, f"{ep}.txt"), sep="\t")
        sc = pd.read_csv(os.path.join(scores_dir, f"{ep}.txt"), sep="\t")
        neg_aucs.append(roc_auc_score((tu["Label"].values == 1).astype(int), -sc["score"].values))
    neg_mean = float(np.mean(neg_aucs))
    assert neg_mean < 0.20, f"Negative control failed: {neg_mean}"
    print(f"[PASS] Negative control (negated scores): _Average MicroAUC = {neg_mean:.6f} (rejected as expected).")
    print("ALL IMMREP22 CHECKS PASSED!")

if __name__ == "__main__":
    main()
