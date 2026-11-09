#!/usr/bin/env python3
"""
Self-contained verification script for `darkmachines-unsupervised-median-total-improvement`.

Checks:
1. Validates `object/darkmachines_27invariant_pot_results.csv` (102 rows = 34 signal-channel pairs x 3 models)
   and `object/darkmachines_19signals_summary.tsv` (19 signals) against `verify-it-yourself/data/other_channels_eval_ref.json.gz`.
2. Re-runs live unsupervised training from scratch on `verify-it-yourself/data/chan2a_bg_odd.npz` (11,628 odd-event_ID
   SM background events in Channel 2a), calibrates exact non-tie thresholds on `chan2a_bg_even.npz` (8,377 even-event_ID
   SM background events), and scores all 7 Channel 2a signal datasets in `chan2a_signals.npz`.
3. Confirms live recomputed Channel 2a metrics match `object/darkmachines_27invariant_pot_results.csv` and
   confirms partial win `p1` (`chaneut_cha300_neut100` TI = 1.4000 / 1.6000 > 1.1000 and
   `chaneut_cha400_neut200` TI = 1.6000 / 1.7000 > 1.0000) plus `Min_TI = 1.0000 >= 0.9000` across all 19 signals.
4. Any corruption of any numeric cell or text field in `object/` triggers an immediate non-zero exit with `FAIL`.
"""
import csv
import gzip
import json
import math
import os
import sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "how-we-built-it"))
from run_darkmachines_pot import fit_and_score_matrix


def fail(msg):
    print(f"VERIFICATION ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def main():
    csv_path = os.path.join(ROOT, "object", "darkmachines_27invariant_pot_results.csv")
    tsv_path = os.path.join(ROOT, "object", "darkmachines_19signals_summary.tsv")
    ref_path = os.path.join(ROOT, "verify-it-yourself", "data", "other_channels_eval_ref.json.gz")

    for p in [csv_path, tsv_path, ref_path]:
        if not os.path.exists(p):
            fail(f"Missing required file: {p}")

    with gzip.open(ref_path, "rt", encoding="utf-8") as gz:
        ref = json.load(gz)

    counts_ref = ref["counts_ref"]
    best_1040 = ref["best_1040"]
    best_1040_model = ref["best_1040_model"]
    flow_eff = ref["flow_eff"]

    # 1. Parse and verify every cell of object/darkmachines_27invariant_pot_results.csv
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if len(rows) != 102:
        fail(f"Expected 102 rows in darkmachines_27invariant_pot_results.csv, found {len(rows)}")

    models = ["PotHull_Hybrid_Lp3", "PotStrataZ_Lp3", "PotHull_L1_L2_Hull"]
    ti_by_mod_sig = {m: {} for m in models}
    chan2a_rows = {}

    for idx, r in enumerate(rows):
        sig = r.get("Signal", "")
        mod = r.get("Model", "")
        chan = r.get("Chan", "")
        key = f"{mod}|{chan}|{sig}"
        if key not in counts_ref:
            fail(f"Row {idx} has unexpected key {key}")
        cref = counts_ref[key]
        n_sig = float(cref["n_sig"])

        try:
            _ = (
                float(r["AUC"]),
                float(r["1e-2"]),
                float(r["1e-3"]),
                float(r["1e-4"]),
                float(r["SI_1e-2"]),
                float(r["SI_1e-3"]),
                float(r["SI_1e-4"]),
                float(r["SI_All"]),
            )
        except Exception as exc:
            fail(f"Row {idx} ({key}) contains non-float value: {exc}")

        exp_auc = round(float(cref["auc"]), 4)
        exp_e2 = round(cref["pass_1e-2"] / n_sig, 2)
        exp_e3 = round(cref["pass_1e-3"] / n_sig, 2)
        exp_e4 = round(cref["pass_1e-4"] / n_sig, 2)
        exp_si2 = round(exp_e2 / math.sqrt(1e-2), 4)
        exp_si3 = round(exp_e3 / math.sqrt(1e-3), 4)
        exp_si4 = round(exp_e4 / math.sqrt(1e-4), 4)
        exp_si_all = round(max(exp_si2, exp_si3, exp_si4), 4)

        if (
            r["AUC"] != f"{exp_auc:.4f}"
            or r["1e-2"] != f"{exp_e2:.2f}"
            or r["1e-3"] != f"{exp_e3:.2f}"
            or r["1e-4"] != f"{exp_e4:.2f}"
            or r["SI_1e-2"] != f"{exp_si2:.4f}"
            or r["SI_1e-3"] != f"{exp_si3:.4f}"
            or r["SI_1e-4"] != f"{exp_si4:.4f}"
            or r["SI_All"] != f"{exp_si_all:.4f}"
        ):
            fail(f"Row {idx} ({key}) mismatch against verified counts/formulas: got {r}")

        ti_by_mod_sig[mod][sig] = max(ti_by_mod_sig[mod].get(sig, 0.0), exp_si_all)
        if chan == "2a":
            chan2a_rows[f"{mod}|{sig}"] = r

    # 2. Live re-training & scoring on Channel 2a odd/even background and 7 signals
    odd_npz = np.load(os.path.join(ROOT, "verify-it-yourself", "data", "chan2a_bg_odd.npz"))["X"]
    even_npz = np.load(os.path.join(ROOT, "verify-it-yourself", "data", "chan2a_bg_even.npz"))["X"]
    sigs_npz = dict(np.load(os.path.join(ROOT, "verify-it-yourself", "data", "chan2a_signals.npz")))

    if len(odd_npz) != 11628 or len(even_npz) != 8377:
        fail(f"Unexpected Channel 2a split sizes: odd={len(odd_npz)}, even={len(even_npz)}")

    bg_sc, taus, sig_sc = fit_and_score_matrix(odd_npz, even_npz, sigs_npz)

    for m in models:
        for k, eps in [("1e-2", 1e-2), ("1e-3", 1e-3), ("1e-4", 1e-4)]:
            emp_fpr = float(np.mean(bg_sc[m] >= taus[m][k]))
            if emp_fpr > eps + 1e-12:
                fail(f"Channel 2a {m} threshold at {k} violates tie-aware FPR bound: {emp_fpr} > {eps}")

    for sname, X_s in sorted(sigs_npz.items()):
        for m in models:
            r = chan2a_rows.get(f"{m}|{sname}")
            if r is None:
                fail(f"Missing Channel 2a row for {m}|{sname}")
            live_e2 = round(float(np.mean(sig_sc[sname][m] >= taus[m]["1e-2"])), 2)
            live_e3 = round(float(np.mean(sig_sc[sname][m] >= taus[m]["1e-3"])), 2)
            live_e4 = round(float(np.mean(sig_sc[sname][m] >= taus[m]["1e-4"])), 2)
            if (
                abs(live_e2 - float(r["1e-2"])) > 0.01 + 1e-9
                or abs(live_e3 - float(r["1e-3"])) > 0.01 + 1e-9
                or abs(live_e4 - float(r["1e-4"])) > 0.01 + 1e-9
            ):
                fail(
                    f"Live Channel 2a {m}|{sname} efficiency mismatch: live=({live_e2:.2f},{live_e3:.2f},{live_e4:.2f}) vs csv=({r['1e-2']},{r['1e-3']},{r['1e-4']})"
                )

    # 3. Verify every row of object/darkmachines_19signals_summary.tsv
    with open(tsv_path, "r", encoding="utf-8") as f:
        treader = csv.DictReader(f, delimiter="	")
        trows = list(treader)

    if len(trows) != 19:
        fail(f"Expected 19 rows in darkmachines_19signals_summary.tsv, found {len(trows)}")

    for idx, tr in enumerate(trows):
        sig = tr.get("Signal", "")
        if sig not in best_1040:
            fail(f"Summary row {idx} has unknown signal {sig}")
        exp_h = ti_by_mod_sig["PotHull_Hybrid_Lp3"][sig]
        exp_s = ti_by_mod_sig["PotStrataZ_Lp3"][sig]
        exp_l = ti_by_mod_sig["PotHull_L1_L2_Hull"][sig]
        exp_fe = float(flow_eff[sig])
        exp_b = float(best_1040[sig])
        exp_bm = str(best_1040_model[sig])
        exp_beats = "YES" if (exp_h > exp_b + 1e-9 or exp_s > exp_b + 1e-9) else "NO"

        if (
            tr["PotHull_Hybrid_Lp3_TI"] != f"{exp_h:.4f}"
            or tr["PotStrataZ_Lp3_TI"] != f"{exp_s:.4f}"
            or tr["PotHull_L1_L2_Hull_TI"] != f"{exp_l:.4f}"
            or tr["Flow_Efficient_Likelihood_TI"] != f"{exp_fe:.4f}"
            or tr["Best_1040_TI"] != f"{exp_b:.4f}"
            or tr["Best_1040_Model"] != exp_bm
            or tr["Beats_All_1040"] != exp_beats
        ):
            fail(f"Summary row {idx} ({sig}) mismatch: got {tr}")

    # 4. Verify partial win p1 and minimum-TI floor
    cha300_h = ti_by_mod_sig["PotHull_Hybrid_Lp3"]["chaneut_cha300_neut100"]
    cha300_s = ti_by_mod_sig["PotStrataZ_Lp3"]["chaneut_cha300_neut100"]
    cha400_h = ti_by_mod_sig["PotHull_Hybrid_Lp3"]["chaneut_cha400_neut200"]
    cha400_s = ti_by_mod_sig["PotStrataZ_Lp3"]["chaneut_cha400_neut200"]
    min_ti_h = min(ti_by_mod_sig["PotHull_Hybrid_Lp3"].values())
    min_ti_l = min(ti_by_mod_sig["PotHull_L1_L2_Hull"].values())

    if not (cha300_h > 1.10 and cha300_s > 1.10 and cha400_h > 1.00 and cha400_s > 1.00):
        fail("Partial win p1 thresholds not satisfied")
    if not (min_ti_h >= 0.90 and min_ti_l >= 0.90):
        fail(f"Minimum TI floor >= 0.90 not satisfied: min_ti_h={min_ti_h}, min_ti_l={min_ti_l}")

    print(
        f"Verified 102 signal-channel evaluations and live Channel 2a retraining: "
        f"cha300 TI = {cha300_h:.2f} / {cha300_s:.2f} (> 1.10), "
        f"cha400 TI = {cha400_h:.2f} / {cha400_s:.2f} (> 1.00), "
        f"Min_TI = {min_ti_h:.2f} (>= 0.90)."
    )
    print("PASS")


if __name__ == "__main__":
    main()
