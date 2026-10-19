#!/usr/bin/env python3
"""Standalone verification script for immrep22-tcr-epitope-microauc (outbox package)."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from decimal import Decimal, getcontext

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.metrics import roc_auc_score

getcontext().prec = 50

PKG_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

EXPECTED_SCORE_MOMENTS = {
    'ATDALMTGF.txt': (155, '222.9255181978038053552'),
    'CINGVCWTV.txt': (275, '6364.627140830605318955'),
    'GILGFVFTL.txt': (812, '31342.50313209057611274755'),
    'GLCTLVAML.txt': (220, '1393.591518034902209545578'),
    'GPRLGVRAT.txt': (62, '310.7875334274392411680'),
    'HPVTKYIM.txt': (72, '172.8444608409399961100'),
    'KSKRTPMGF.txt': (129, '717.026867319707999677'),
    'LLWNGPMAV.txt': (282, '3105.41014980831796028022'),
    'LTDEMIAQY.txt': (150, '114.0193294921308157240'),
    'NLVPMVATV.txt': (411, '12066.9503750036344162870'),
    'NQKLIANQF.txt': (86, '143.386092953062946140'),
    'NYNYLYRLF.txt': (68, '317.3827760468736123190'),
    'RAQAPPPSW.txt': (54, '121.3050275445762911103'),
    'SPRWYFYYL.txt': (140, '2153.6867208473588328597'),
    'TPRVTGGGAM.txt': (69, '-39.2285397868833862540'),
    'TTDPSFLGRY.txt': (291, '8522.9248807277638882726'),
    'YLQPRTFLL.txt': (399, '7802.25727179338505770308'),
    'testSet_Global.txt': (10523, '-7012607.545003242025322690705'),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Verify IMMREP22 CLSS TCR-epitope predictions and audit.")
    parser.add_argument("--scores-dir", default=os.path.join(PKG_ROOT, "object", "clss_tcr_scores"))
    parser.add_argument("--stats-file", default=os.path.join(PKG_ROOT, "object", "clss_tcr_stats.txt"))
    parser.add_argument("--manifest", default=os.path.join(PKG_ROOT, "object", "immrep22_audit_manifest.json"))
    args = parser.parse_args()

    eval_py = os.path.join(PKG_ROOT, "the-record-we-beat", "evaluate.py")
    true_dir = os.path.join(PKG_ROOT, "the-record-we-beat", "true_set_labels")
    micro_csv = os.path.join(PKG_ROOT, "the-record-we-beat", "microaucs.csv")
    rank_csv = os.path.join(PKG_ROOT, "the-record-we-beat", "epitoperank.csv")

    assert sha256_file(eval_py) == "04fa0346aa914bab770f9adbd6326581026e0fa9b94ad734f3957c54be6778ed", "evaluate.py hash mismatch"
    assert sha256_file(micro_csv) == "28321870009bf2f122907da498ed912d227d8ad74b6f92d37d9ddfb9d043bec5", "microaucs.csv hash mismatch"
    assert sha256_file(rank_csv) == "286e0acde8a47fd0197ff1a4d4b0715fab8869c7b51374df3ecd1a406381c2f8", "epitoperank.csv hash mismatch"

    pub_micro = pd.read_csv(micro_csv, index_col=0)
    pub_rank = pd.read_csv(rank_csv, index_col=0)
    epitopes = list(pub_micro.columns[1:18])

    default_scores_dir = os.path.abspath(args.scores_dir) == os.path.abspath(os.path.join(PKG_ROOT, "object", "clss_tcr_scores"))

    # 1. Verify exact TCR row sequence alignment & 50-digit Decimal score moments
    for fn, (exp_n, exp_dot_str) in EXPECTED_SCORE_MOMENTS.items():
        fpath = os.path.join(args.scores_dir, fn)
        assert os.path.isfile(fpath), f"Missing score file: {fn}"
        with open(fpath, encoding="utf-8") as f:
            lines = [l.rstrip("\r\n").split("\t") for l in f if l.strip()]
        rows = lines[1:]
        assert len(rows) == exp_n, f"Row count mismatch in {fn}: {len(rows)} != {exp_n}"
        if default_scores_dir:
            dot = sum((i + 1) * Decimal(r[-1]) for i, r in enumerate(rows))
            assert dot == Decimal(exp_dot_str), f"Score moment mismatch in {fn}: {dot} != {exp_dot_str}"

    # Verify positive test TCR score identity between {ep}.txt and testSet_Global.txt
    g_df = pd.read_csv(os.path.join(args.scores_dir, "testSet_Global.txt"), sep="\t")
    g_lookup = {(r["TRA_CDR3"], r["TRB_CDR3"], r["epitope"]): float(r["score"]) for _, r in g_df.iterrows()}

    for ep in epitopes:
        pred_df = pd.read_csv(os.path.join(args.scores_dir, f"{ep}.txt"), sep="\t")
        true_df = pd.read_csv(os.path.join(true_dir, f"{ep}.txt"), sep="\t")
        assert (pred_df["TRA_CDR3"].values == true_df["TRA_CDR3"].values).all(), f"TRA_CDR3 mismatch on {ep}"
        assert (pred_df["TRB_CDR3"].values == true_df["TRB_CDR3"].values).all(), f"TRB_CDR3 mismatch on {ep}"
        for idx, r in true_df.iterrows():
            if int(r["Label"]) == 1:
                key = (r["TRA_CDR3"], r["TRB_CDR3"], ep)
                assert key in g_lookup, f"Missing positive TCR {key} in testSet_Global.txt"
                if default_scores_dir:
                    assert abs(float(pred_df.loc[idx, "score"]) - g_lookup[key]) <= 1e-13, f"Pointwise score mismatch on {key}"

    # 2. Run unmodified official evaluate.py
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
        tmp_stats = tf.name
    try:
        subprocess.run(
            [sys.executable, eval_py, "-i", args.scores_dir, "-t", true_dir, "-o", tmp_stats],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        fresh_st = pd.read_csv(tmp_stats, sep="\t", index_col=0)
        if default_scores_dir:
            with open(tmp_stats, "rb") as f1, open(args.stats_file, "rb") as f2:
                assert f1.read() == f2.read(), "Saved clss_tcr_stats.txt byte mismatch vs fresh evaluate.py"
    finally:
        if os.path.exists(tmp_stats):
            os.remove(tmp_stats)

    if default_scores_dir:
        saved_st = pd.read_csv(args.stats_file, sep="\t", index_col=0)
        max_diff = float(np.max(np.abs(fresh_st.values - saved_st.values)))
        assert max_diff == 0.0, f"Saved stats mismatch fresh evaluate.py: max_diff={max_diff}"

    avg_micro = float(fresh_st.loc["_Average", "MicroAUC"])
    best_pub_micro = float(pub_micro["_Average"].max())
    best_pub_method = str(pub_micro["_Average"].idxmax())
    gain_micro = avg_micro - best_pub_micro

    tcrexab_ep = np.array([float(pub_micro.loc["tcrexab", ep]) for ep in epitopes])
    clss_ep = np.array([float(fresh_st.loc[ep, "MicroAUC"]) for ep in epitopes])
    diffs = clss_ep - tcrexab_ep
    n_wins_tcrexab = int(np.sum(diffs > 0))
    n_col_max_wins = int(sum(float(fresh_st.loc[ep, "MicroAUC"]) > float(pub_micro[ep].max()) for ep in epitopes))

    _, p_wilcoxon = wilcoxon(clss_ep, tcrexab_ep, alternative="greater")
    rng = np.random.default_rng(0)
    idx_boot = rng.integers(0, len(epitopes), size=(10000, len(epitopes)))
    boot_gains = diffs[idx_boot].mean(axis=1)
    boot_win_rate = float(np.mean(boot_gains > 0.0))

    spr_auc = float(fresh_st.loc["SPRWYFYYL", "MicroAUC"])
    spr_col_max = float(pub_micro["SPRWYFYYL"].max())
    spr_gain = spr_auc - spr_col_max

    avg_rank = float(fresh_st.loc["_Average", "Average Rank"])
    best_pub_rank = float(pub_rank["_Average"].min())
    rank_diff = avg_rank - best_pub_rank

    print(f"[Task 1] _Average MicroAUC: {avg_micro:.6f} vs {best_pub_method} {best_pub_micro:.6f} (gain = {gain_micro:+.6f})")
    print(f"[Task 1] Epitope wins vs tcrexab: {n_wins_tcrexab}/17 | Wilcoxon p = {p_wilcoxon:.6e} | Bootstrap win rate = {boot_win_rate*100:.2f}%")
    print(f"[Task 1] Column-maximum wins across all 22 methods: {n_col_max_wins}/17")
    print(f"[p1]     SPRWYFYYL MicroAUC: {spr_auc:.6f} vs column max {spr_col_max:.6f} (gain = {spr_gain:+.6f})")
    print(f"[p2]     _Average Rank:      {avg_rank:.6f} vs tcrexab {best_pub_rank:.6f} (diff = {rank_diff:+.6f})")

    assert gain_micro >= 0.0200, f"MicroAUC gain {gain_micro:+.6f} < +0.0200"
    assert n_wins_tcrexab >= 12, f"Epitope wins {n_wins_tcrexab}/17 < 12/17"
    assert p_wilcoxon < 0.01, f"Wilcoxon p {p_wilcoxon:.6e} >= 0.01"
    assert boot_win_rate >= 0.95, f"Bootstrap win rate {boot_win_rate:.4f} < 0.95"
    assert spr_gain >= 0.0300, f"SPRWYFYYL gain {spr_gain:+.6f} < +0.0300"
    assert rank_diff <= -0.2500, f"Average Rank diff {rank_diff:+.6f} > -0.2500"

    # 3. Verify audit manifest (p3 negative provenance, Levenshtein >= 2, baselines, null model)
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)

    assert abs(float(manifest["clss_mean_microauc"]) - avg_micro) <= 1e-12, "Manifest avg_micro mismatch"
    assert abs(float(manifest["epitopes_beating_all_22_published_max_by_0_03"][0]["clss_auc"]) - spr_auc) <= 1e-12, "Manifest SPRWYFYYL mismatch"

    p3 = manifest["p3_negative_sampling_provenance_audit"]
    for m_name in ["tcrexab", "tcrexb", "tcrexa"]:
        repro_auc = float(p3[m_name]["mean_auc_all_neg"])
        pub_auc = float(pub_micro.loc[m_name, "_Average"])
        assert abs(repro_auc - pub_auc) <= 0.0100, f"Baseline {m_name} diff > 0.01"

    leak_rows = manifest["leakage_and_levenshtein_audit"]
    ctrl_overlaps = sum(int(r["control_neg_train_test_overlap"]) for r in leak_rows)
    assert ctrl_overlaps == 0, f"Nonzero control repertoire overlap: {ctrl_overlaps}"

    lev2_clss = float(p3["clss_tcr"]["mean_auc_min_lev_ab_ge_2"])
    lev2_tcrexab = float(p3["tcrexab"]["mean_auc_min_lev_ab_ge_2"])
    assert lev2_clss - lev2_tcrexab >= 0.0200, "Levenshtein >= 2 gain < +0.0200"
    assert lev2_clss - best_pub_micro >= 0.0200, "Levenshtein >= 2 gain vs full-set best < +0.0200"

    # 4. Live 400-permutation null model across all 17 epitopes
    rng_null = np.random.default_rng(0)
    ep_labels_scores = []
    for ep in epitopes:
        pred_df = pd.read_csv(os.path.join(args.scores_dir, f"{ep}.txt"), sep="\t")
        true_df = pd.read_csv(os.path.join(true_dir, f"{ep}.txt"), sep="\t")
        ep_labels_scores.append((true_df["Label"].to_numpy(dtype=np.int32), pred_df["score"].to_numpy(dtype=np.float64)))

    null_means = np.zeros(400, dtype=np.float64)
    for b in range(400):
        aucs = [roc_auc_score(rng_null.permutation(y), s) for y, s in ep_labels_scores]
        null_means[b] = np.mean(aucs)
    null_mu = float(null_means.mean())
    null_sd = float(null_means.std())
    null_max = float(null_means.max())
    z_null = (avg_micro - null_mu) / null_sd
    assert avg_micro > null_max and z_null >= 15.0, f"Null model check failed: z={z_null}"

    print(f"[p3]     Control overlap: 0/17 | Levenshtein>=2 MicroAUC: {lev2_clss:.6f} vs {lev2_tcrexab:.6f} ({lev2_clss - lev2_tcrexab:+.6f}) | 400-perm Null max = {null_max:.6f} (z = {z_null:+.2f})")
    print("PASS: ALL IMMREP22 CLSS CHECKS SUCCEEDED")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"VERIFICATION ERROR: {e}", file=sys.stderr)
        print("FAIL")
        sys.exit(1)
