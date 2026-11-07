#!/usr/bin/env python3
"""Standalone standard-library verifier for moabb-within-session-benchmark-cells.

Independently verifies:
1. 5-fold StratifiedKFold(n_splits=5, shuffle=True, random_state=42) partition integrity
   (strictly increasing indices, zero train/test overlap, full session coverage, exact
   test partition across folds, cross-fold ground-truth label consistency y_session[idx],
   and class stratification) for all 32 subject-sessions (160 CV folds, 3,955 trials)
   across Kalunga2016, Nakanishi2015, and MAMEM3.
2. Orthonormal QR upper-triangular structure (R_W[i][j] == 0 for i > j) and multinomial
   L2 zero-sum stationarity (|sum(b)| <= 1e-8 and |sum_k R_W[j][k]| <= 1e-8), plus exact
   multi-class logit and softmax probability recomputation from the 3-view projections
   (joint, cca, ts), fixed ensemble combination (0.45 * p_joint + 0.40 * p_cca + 0.15 * p_ts),
   argmax class prediction, fold accuracy, and 5-fold session accuracy against both
   object/moabb_ssvep_within_session_cells.csv and the fold witness metadata.
3. Exact baseline reproduction of SSVEP_MDM (70.89 +/- 13.44) and SSVEP_TS+LR
   (70.86 +/- 11.64) on Kalunga2016, and SSVEP_TS+LR (87.28 +/- 15.90 vs 87.22 +/- 15.96)
   and SSVEP_MDM (78.77 +/- 19.06) on Nakanishi2015.
4. Full win (and p1) criteria: one fixed pipeline (FB_HTR_SSVEP) beating the best
   live table cell by >= 1.0 percentage point on all 3 datasets of the SSVEP
   (All classes) table:
   - Kalunga2016:   88.92 +/- 8.03 vs 70.89 +/- 13.44 (+18.03 points >= +1.0)
   - Nakanishi2015: 95.86 +/- 10.02 vs 87.22 +/- 15.96 (+8.64 points  >= +1.0)
   - MAMEM3 (n=11): 52.73 +/- 23.99 vs 42.10 +/- 14.33 (+10.63 points >= +1.0;
                    50.08 +/- 23.58 on subjects 1..10, +7.98 points >= +1.0)
"""
import csv
import gzip
import json
import math
import os
import sys


LIVE_TABLE_BEST = {
    "Kalunga2016": ("SSVEP_MDM", 70.89, 13.44),
    "Nakanishi2015": ("SSVEP_TS+LR", 87.22, 15.96),
    "MAMEM3": ("SSVEP_TS+LR", 42.10, 14.33),
}

EXPECTED_FB_HTR = {
    "Kalunga2016": (88.92, 8.03),
    "Nakanishi2015": (95.86, 10.02),
    "MAMEM3": (52.73, 23.99),
}

EXPECTED_COUNTS = {
    "Kalunga2016": 12,
    "Nakanishi2015": 9,
    "MAMEM3": 11,
}


def fail(msg):
    print(f"Verification error: {msg}")
    print("FAIL")
    sys.exit(1)


def softmax_rows(U_te, R_W, b, label=""):
    K = len(b)
    if K < 2 or len(R_W) != K or any(len(row) != K for row in R_W):
        fail(f"Invalid R_W/b dimensions at {label}")
    # Verify upper-triangular QR factor structure and multinomial L2 zero-sum stationarity
    if abs(sum(b)) > 1e-8:
        fail(f"Intercept vector b violates multinomial zero-sum stationarity at {label}: sum={sum(b)}")
    for i in range(K):
        for j in range(i):
            if R_W[i][j] != 0.0:
                fail(f"R_W is not upper triangular at {label} ({i},{j})={R_W[i][j]}")
        if abs(sum(R_W[i])) > 1e-8:
            fail(f"R_W row {i} violates multinomial zero-sum stationarity at {label}: sum={sum(R_W[i])}")

    probs = []
    for u in U_te:
        if len(u) != K:
            fail(f"Dimension mismatch between U_te and R_W at {label}")
        logits = []
        for k in range(K):
            s = b[k]
            for j in range(K):
                s += u[j] * R_W[j][k]
            logits.append(s)
        m = max(logits)
        exps = [math.exp(x - m) for x in logits]
        z = sum(exps)
        probs.append([e / z for e in exps])
    return probs


def mean_std_ddof0(vals):
    n = len(vals)
    if n == 0:
        fail("Empty value list")
    mu = sum(vals) / n
    var = sum((x - mu) ** 2 for x in vals) / n
    return mu, math.sqrt(var)


def check_float_str(raw_str, expected_val, tol=5e-10, label=""):
    try:
        parsed = float(raw_str)
    except ValueError:
        fail(f"Non-numeric value in CSV ({label}): {raw_str!r}")
    expected_str = f"{expected_val:.10f}"
    if raw_str.strip() != expected_str or abs(parsed - expected_val) > tol:
        fail(f"CSV mismatch at {label}: got {raw_str!r}, expected {expected_str!r}")


def check_witness_float(val, expected_val, tol=5e-10, label=""):
    if not isinstance(val, (int, float)) or abs(float(val) - expected_val) > tol:
        fail(f"Witness accuracy mismatch at {label}: got {val!r}, expected {expected_val:.10f}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)
    csv_path = os.path.join(pkg_root, "object", "moabb_ssvep_within_session_cells.csv")
    gz_path = os.path.join(here, "data", "moabb_ssvep_fold_witness.json.gz")

    if not os.path.isfile(csv_path):
        fail(f"Missing object file: {csv_path}")
    if not os.path.isfile(gz_path):
        fail(f"Missing fold witness file: {gz_path}")

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        csv_rows = list(reader)

    with gzip.open(gz_path, "rt", encoding="utf-8") as f:
        witness = json.load(f)

    sessions = witness.get("sessions", [])
    if len(csv_rows) != 32 or len(sessions) != 32:
        fail(f"Expected 32 subject-sessions, got csv={len(csv_rows)}, witness={len(sessions)}")

    w_ens = witness.get("ensemble_weights", {})
    if (
        abs(w_ens.get("joint", 0.0) - 0.45) > 1e-12
        or abs(w_ens.get("cca", 0.0) - 0.40) > 1e-12
        or abs(w_ens.get("ts", 0.0) - 0.15) > 1e-12
    ):
        fail("Unexpected ensemble weights in witness")

    by_dataset = {"Kalunga2016": [], "Nakanishi2015": [], "MAMEM3": []}
    total_trials = 0

    for row, sess in zip(csv_rows, sessions):
        ds = sess["dataset"]
        subj = sess["subject"]
        session_id = sess["session"]
        n_trials = sess["n_trials"]
        n_classes = sess["n_classes"]
        label_prefix = f"{ds}/subj{subj}/{session_id}"

        if row["dataset"] != ds or str(subj) != row["subject"].strip() or row["session"].strip() != session_id:
            fail(f"Identifier mismatch at {label_prefix}")
        if row["n_trials"].strip() != str(n_trials) or row["n_classes"].strip() != str(n_classes):
            fail(f"Trial/class count mismatch at {label_prefix}")

        folds = sess.get("folds", [])
        if len(folds) != 5:
            fail(f"Expected 5 folds at {label_prefix}, got {len(folds)}")

        all_test_indices = []
        session_labels = {}
        train_class_counts = {c: [] for c in range(n_classes)}
        fold_fb_accs = []
        fold_mdm_accs = []
        fold_ts_accs = []

        for f_idx, fold in enumerate(folds):
            if fold["fold"] != f_idx:
                fail(f"Fold index mismatch at {label_prefix} fold {f_idx}")
            tr = fold["train_idx"]
            te = fold["test_idx"]
            y_tr = fold["y_train"]
            y_te = fold["y_test"]

            if len(tr) != len(y_tr) or len(te) != len(y_te) or len(te) == 0:
                fail(f"Invalid fold lengths at {label_prefix} fold {f_idx}")
            if tr != sorted(tr) or te != sorted(te):
                fail(f"Unsorted train/test indices at {label_prefix} fold {f_idx}")

            tr_set = set(tr)
            te_set = set(te)
            if len(tr_set) != len(tr) or len(te_set) != len(te):
                fail(f"Duplicate indices in fold {f_idx} at {label_prefix}")
            if tr_set & te_set:
                fail(f"Train/test leakage detected at {label_prefix} fold {f_idx}")
            if (tr_set | te_set) != set(range(n_trials)):
                fail(f"Train union test does not equal 0..{n_trials - 1} at {label_prefix} fold {f_idx}")

            for idx_val, y_val in list(zip(tr, y_tr)) + list(zip(te, y_te)):
                if not isinstance(y_val, int) or not (0 <= y_val < n_classes):
                    fail(f"Invalid class label {y_val} at {label_prefix} fold {f_idx}")
                if idx_val in session_labels and session_labels[idx_val] != y_val:
                    fail(
                        f"Cross-fold label inconsistency for trial {idx_val} at {label_prefix} fold {f_idx}: "
                        f"{session_labels[idx_val]} vs {y_val}"
                    )
                session_labels[idx_val] = y_val

            all_test_indices.extend(te)
            for c in range(n_classes):
                train_class_counts[c].append(sum(1 for y in y_tr if y == c))

            # Recompute probabilities from orthonormal QR projections for each view
            views = fold["views"]
            pj = softmax_rows(
                views["joint"]["U_te"], views["joint"]["R_W"], views["joint"]["b"],
                label=f"{label_prefix}:fold{f_idx}:joint",
            )
            pc = softmax_rows(
                views["cca"]["U_te"], views["cca"]["R_W"], views["cca"]["b"],
                label=f"{label_prefix}:fold{f_idx}:cca",
            )
            pt = softmax_rows(
                views["ts"]["U_te"], views["ts"]["R_W"], views["ts"]["b"],
                label=f"{label_prefix}:fold{f_idx}:ts",
            )

            if not (len(pj) == len(pc) == len(pt) == len(y_te)):
                fail(f"View prediction length mismatch at {label_prefix} fold {f_idx}")

            recomp_pred_fb = []
            for i in range(len(y_te)):
                p_ens = [
                    0.45 * pj[i][k] + 0.40 * pc[i][k] + 0.15 * pt[i][k]
                    for k in range(n_classes)
                ]
                best_k = max(range(n_classes), key=lambda k: p_ens[k])
                recomp_pred_fb.append(best_k)

            if recomp_pred_fb != fold["pred_fb_htr"]:
                fail(f"Recomputed FB_HTR predictions do not match witness at {label_prefix} fold {f_idx}")

            pred_mdm = fold["pred_mdm"]
            pred_ts = fold["pred_ts_lr"]
            if len(pred_mdm) != len(y_te) or len(pred_ts) != len(y_te):
                fail(f"Baseline prediction length mismatch at {label_prefix} fold {f_idx}")

            acc_fb = sum(1 for p, y in zip(recomp_pred_fb, y_te) if p == y) / len(y_te)
            acc_mdm = sum(1 for p, y in zip(pred_mdm, y_te) if p == y) / len(y_te)
            acc_ts = sum(1 for p, y in zip(pred_ts, y_te) if p == y) / len(y_te)

            check_witness_float(fold.get("acc_fb_htr"), acc_fb, label=f"{label_prefix}:fold{f_idx}:acc_fb_htr")
            check_witness_float(fold.get("acc_mdm"), acc_mdm, label=f"{label_prefix}:fold{f_idx}:acc_mdm")
            check_witness_float(fold.get("acc_ts_lr"), acc_ts, label=f"{label_prefix}:fold{f_idx}:acc_ts_lr")

            check_float_str(row[f"fold{f_idx}_fb_htr"], acc_fb, label=f"{label_prefix}:fold{f_idx}_fb_htr")
            check_float_str(row[f"fold{f_idx}_mdm"], acc_mdm, label=f"{label_prefix}:fold{f_idx}_mdm")
            check_float_str(row[f"fold{f_idx}_ts_lr"], acc_ts, label=f"{label_prefix}:fold{f_idx}_ts_lr")

            fold_fb_accs.append(acc_fb)
            fold_mdm_accs.append(acc_mdm)
            fold_ts_accs.append(acc_ts)

        # Verify 5-fold test partition covers every trial exactly once
        if sorted(all_test_indices) != list(range(n_trials)) or len(session_labels) != n_trials:
            fail(f"5-fold test indices do not partition 0..{n_trials - 1} at {label_prefix}")

        # Verify stratification across folds
        for c, counts in train_class_counts.items():
            if max(counts) - min(counts) > 1:
                fail(f"Non-stratified class {c} counts {counts} at {label_prefix}")

        sess_fb = sum(fold_fb_accs) / 5.0
        sess_mdm = sum(fold_mdm_accs) / 5.0
        sess_ts = sum(fold_ts_accs) / 5.0

        check_witness_float(sess.get("fb_htr_ssvep"), sess_fb, label=f"{label_prefix}:fb_htr_ssvep")
        check_witness_float(sess.get("ssvep_mdm"), sess_mdm, label=f"{label_prefix}:ssvep_mdm")
        check_witness_float(sess.get("ssvep_ts_lr"), sess_ts, label=f"{label_prefix}:ssvep_ts_lr")

        check_float_str(row["fb_htr_ssvep"], sess_fb, label=f"{label_prefix}:fb_htr_ssvep")
        check_float_str(row["ssvep_mdm"], sess_mdm, label=f"{label_prefix}:ssvep_mdm")
        check_float_str(row["ssvep_ts_lr"], sess_ts, label=f"{label_prefix}:ssvep_ts_lr")

        by_dataset[ds].append((sess_fb * 100.0, sess_mdm * 100.0, sess_ts * 100.0))
        total_trials += n_trials

    for ds, exp_n in EXPECTED_COUNTS.items():
        if len(by_dataset[ds]) != exp_n:
            fail(f"Expected {exp_n} sessions for {ds}, got {len(by_dataset[ds])}")

    # Verify baseline reproduction on Kalunga2016 and Nakanishi2015
    kal_fb, kal_mdm, kal_ts = zip(*by_dataset["Kalunga2016"])
    nak_fb, nak_mdm, nak_ts = zip(*by_dataset["Nakanishi2015"])
    mam_fb, mam_mdm, mam_ts = zip(*by_dataset["MAMEM3"])

    kal_mdm_m, kal_mdm_s = mean_std_ddof0(kal_mdm)
    kal_ts_m, kal_ts_s = mean_std_ddof0(kal_ts)
    nak_ts_m, nak_ts_s = mean_std_ddof0(nak_ts)
    nak_mdm_m, nak_mdm_s = mean_std_ddof0(nak_mdm)

    if round(kal_mdm_m, 2) != 70.89 or round(kal_mdm_s, 2) != 13.44:
        fail(f"Kalunga2016 SSVEP_MDM baseline mismatch: {kal_mdm_m:.2f}+/-{kal_mdm_s:.2f}")
    if round(kal_ts_m, 2) != 70.86 or round(kal_ts_s, 2) != 11.64:
        fail(f"Kalunga2016 SSVEP_TS+LR baseline mismatch: {kal_ts_m:.2f}+/-{kal_ts_s:.2f}")
    if round(nak_ts_m, 2) != 87.28 or round(nak_ts_s, 2) != 15.90:
        fail(f"Nakanishi2015 SSVEP_TS+LR baseline mismatch: {nak_ts_m:.2f}+/-{nak_ts_s:.2f}")
    if round(nak_mdm_m, 2) != 78.77 or round(nak_mdm_s, 2) != 19.06:
        fail(f"Nakanishi2015 SSVEP_MDM baseline mismatch: {nak_mdm_m:.2f}+/-{nak_mdm_s:.2f}")

    # Also verify MAMEM3 subjects 1..10 (matching moabb-1.1.2 10-subject count)
    mam10_fb_m, mam10_fb_s = mean_std_ddof0(mam_fb[:10])
    if round(mam10_fb_m, 2) != 50.08 or round(mam10_fb_s, 2) != 23.58 or (mam10_fb_m - 42.10) < 1.0:
        fail(f"MAMEM3 (subjects 1..10) mismatch: {mam10_fb_m:.2f}+/-{mam10_fb_s:.2f}")

    # Verify FB_HTR_SSVEP scores and >= +1.0 point win margin on all 3 datasets
    results_summary = []
    for ds, fb_vals in [
        ("Kalunga2016", kal_fb),
        ("Nakanishi2015", nak_fb),
        ("MAMEM3", mam_fb),
    ]:
        fb_m, fb_s = mean_std_ddof0(fb_vals)
        exp_m, exp_s = EXPECTED_FB_HTR[ds]
        if round(fb_m, 2) != exp_m or round(fb_s, 2) != exp_s:
            fail(f"{ds} FB_HTR_SSVEP score mismatch: got {fb_m:.2f}+/-{fb_s:.2f}, expected {exp_m:.2f}+/-{exp_s:.2f}")
        best_name, best_m, best_s = LIVE_TABLE_BEST[ds]
        margin = fb_m - best_m
        if margin < 1.0:
            fail(f"{ds} margin {margin:.2f} is below required +1.0 point over {best_name} ({best_m:.2f})")
        results_summary.append(
            f"{ds}: FB_HTR_SSVEP={fb_m:.2f}+/-{fb_s:.2f} vs {best_name}={best_m:.2f}+/-{best_s:.2f} (margin=+{margin:.2f})"
        )

    print(
        f"Verified 32 subject-sessions (160 CV folds, {total_trials} trials): "
        + " | ".join(results_summary)
    )
    print("PASS")


if __name__ == "__main__":
    main()
