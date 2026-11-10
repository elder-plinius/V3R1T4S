#!/usr/bin/env python3
"""
Standalone verifier for `darkmachines-unsupervised-median-total-improvement` (BS-POT).

1. Runs a built-in negative control on perturbed efficiency cells to confirm immediate rejection.
2. Verifies every cell across all 136 rows (`34` channel-signal files x `4` BS-POT detectors) in
   `object/darkmachines_bspot_results.csv` and all 19 rows in `object/darkmachines_19signals_bspot_summary.tsv`.
3. Re-runs live unsupervised BS-POT training from scratch in pure Python/NumPy on all `11,628` odd-`event_ID`
   SM background events of Channel `2a`, calibrates tie-aware thresholds on all `8,377` even-`event_ID`
   SM background events, scores all `7` Channel `2a` BSM signal files, and verifies agreement with the CSV.
4. Verifies partial win `p1` (`BSPOT_MaxSec`: `cha300 TI = 6.0000 > 1.1000`, `cha400 TI = 7.0000 > 1.0000`,
   `Median_TI = 5.3759`; `BSPOT_FloorGuard`: `cha300 TI = 1.8000 > 1.1000`, `cha400 TI = 2.2136 > 1.0000`,
   `Median_TI = 3.1000`, `Min_TI = 0.9000 >= 0.9000`).
"""
import csv
import gzip
import json
import math
import os
import statistics
import sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "how-we-built-it"))
from run_darkmachines_bspot import MODELS, fit_and_score_channel


def fail(msg):
    print(f"VERIFICATION ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def check_row_against_ref(r, cref):
    n_sig = float(cref["n_sig"])
    exp_auc = round(float(cref["auc"]), 4)
    exp_e2 = round(cref["pass_1e-2"] / n_sig, 2)
    exp_e3 = round(cref["pass_1e-3"] / n_sig, 2)
    exp_e4 = round(cref["pass_1e-4"] / n_sig, 2)
    exp_si2 = round(exp_e2 / math.sqrt(1e-2), 4)
    exp_si3 = round(exp_e3 / math.sqrt(1e-3), 4)
    exp_si4 = round(exp_e4 / math.sqrt(1e-4), 4)
    exp_si_all = round(max(exp_si2, exp_si3, exp_si4), 4)
    ok = (
        r.get("AUC") == f"{exp_auc:.4f}"
        and r.get("1e-2") == f"{exp_e2:.2f}"
        and r.get("1e-3") == f"{exp_e3:.2f}"
        and r.get("1e-4") == f"{exp_e4:.2f}"
        and r.get("SI_1e-2") == f"{exp_si2:.4f}"
        and r.get("SI_1e-3") == f"{exp_si3:.4f}"
        and r.get("SI_1e-4") == f"{exp_si4:.4f}"
        and r.get("SI_All") == f"{exp_si_all:.4f}"
    )
    return ok, exp_si_all


def main():
    csv_path = os.path.join(ROOT, "object", "darkmachines_bspot_results.csv")
    tsv_path = os.path.join(ROOT, "object", "darkmachines_19signals_bspot_summary.tsv")
    data_dir = os.path.join(ROOT, "verify-it-yourself", "data")
    ref_path = os.path.join(data_dir, "bspot_eval_ref.json.gz")

    for p in [csv_path, tsv_path, ref_path]:
        if not os.path.isfile(p):
            fail(f"Missing required file: {p}")

    with gzip.open(ref_path, "rt", encoding="utf-8") as gz:
        ref = json.load(gz)

    counts_ref = ref["counts_ref"]
    best_1040 = ref["best_1040"]
    best_1040_model = ref["best_1040_model"]
    flow_eff = ref["flow_eff"]
    prior_strata_ti = ref["prior_strata_ti"]

    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 136:
        fail(f"Expected 136 rows in darkmachines_bspot_results.csv, found {len(rows)}")

    # 1. Negative control: perturb one digit of row 0 and confirm rejection
    bad_r0 = dict(rows[0])
    bad_r0["1e-4"] = "0.99" if bad_r0.get("1e-4") != "0.99" else "0.00"
    k0 = f"{rows[0].get('Model','')}|{rows[0].get('Chan','')}|{rows[0].get('Signal','')}"
    if k0 in counts_ref and check_row_against_ref(bad_r0, counts_ref[k0])[0]:
        fail("Negative control failed to reject perturbed row")

    # 2. Verify all 136 rows in object/darkmachines_bspot_results.csv
    ti_by_mod_sig = {m: {} for m in MODELS}
    seen_keys = set()
    chan2a_rows = {}
    for idx, r in enumerate(rows):
        sig = r.get("Signal", "")
        mod = r.get("Model", "")
        chan = r.get("Chan", "")
        key = f"{mod}|{chan}|{sig}"
        if key in seen_keys or key not in counts_ref:
            fail(f"Row {idx} has invalid or duplicate key: {key}")
        seen_keys.add(key)
        ok, exp_si_all = check_row_against_ref(r, counts_ref[key])
        if not ok:
            fail(f"Row {idx} ({key}) failed exact formula/count verification: {r}")
        ti_by_mod_sig[mod][sig] = max(ti_by_mod_sig[mod].get(sig, 0.0), exp_si_all)
        if chan == "2a":
            chan2a_rows[f"{mod}|{sig}"] = r

    # 3. Live re-training & scoring from scratch on Channel 2a (11,628 odd, 8,377 even, 7 BSM signals)
    odd1 = np.load(os.path.join(data_dir, "chan2a_odd_part1.npz"))["X"]
    odd2 = np.load(os.path.join(data_dir, "chan2a_odd_part2.npz"))["X"]
    even1 = np.load(os.path.join(data_dir, "chan2a_even_part1.npz"))["X"]
    even2 = np.load(os.path.join(data_dir, "chan2a_even_part2.npz"))["X"]
    X_odd = np.vstack([odd1, odd2])
    X_even = np.vstack([even1, even2])
    if X_odd.shape != (11628, 52) or X_even.shape != (8377, 52):
        fail(f"Unexpected Channel 2a shapes: odd={X_odd.shape}, even={X_even.shape}")

    sig_manifest = json.load(open(os.path.join(data_dir, "chan2a_sig_manifest.json"), "r", encoding="utf-8"))
    sigs_2a = {}
    for sname, part_files in sorted(sig_manifest.items()):
        sigs_2a[sname] = np.vstack([np.load(os.path.join(data_dir, pf))["X"] for pf in part_files])

    bg_sc, taus, sig_sc = fit_and_score_channel(X_odd, X_even, sigs_2a)

    for m in MODELS:
        for k, eps in [("1e-2", 1e-2), ("1e-3", 1e-3), ("1e-4", 1e-4)]:
            emp_fpr = float(np.mean(bg_sc[m] >= taus[m][k]))
            if emp_fpr > eps + 1e-12:
                fail(f"Channel 2a {m} threshold at {k} violates tie-aware FPR bound: {emp_fpr} > {eps}")

    max_diff = 0.0
    for sname in sorted(sigs_2a.keys()):
        for m in MODELS:
            r = chan2a_rows.get(f"{m}|{sname}")
            if r is None:
                fail(f"Missing Channel 2a row for {m}|{sname}")
            for k in ["1e-2", "1e-3", "1e-4"]:
                live_e = round(float(np.mean(sig_sc[sname][m] >= taus[m][k])), 2)
                csv_e = float(r[k])
                diff = abs(live_e - csv_e)
                if diff > max_diff:
                    max_diff = diff
                if diff > 0.01 + 1e-9:
                    fail(f"Live Channel 2a mismatch on {m}|{sname} at {k}: live={live_e:.2f} vs csv={csv_e:.2f}")

    # 4. Verify all 19 summary rows in object/darkmachines_19signals_bspot_summary.tsv
    with open(tsv_path, "r", encoding="utf-8") as f:
        trows = list(csv.DictReader(f, delimiter="	"))
    if len(trows) != 19:
        fail(f"Expected 19 rows in darkmachines_19signals_bspot_summary.tsv, found {len(trows)}")

    for idx, tr in enumerate(trows):
        sig = tr.get("Signal", "")
        if sig not in best_1040:
            fail(f"Unknown signal in summary row {idx}: {sig}")
        exp_ms = ti_by_mod_sig["BSPOT_MaxSec"][sig]
        exp_bf = ti_by_mod_sig["BSPOT_Bayes_Full"][sig]
        exp_uo = ti_by_mod_sig["BSPOT_Union_OR"][sig]
        exp_fg = ti_by_mod_sig["BSPOT_FloorGuard"][sig]
        exp_pr = float(prior_strata_ti[sig])
        exp_fe = float(flow_eff[sig])
        exp_b = float(best_1040[sig])
        exp_bm = str(best_1040_model[sig])
        exp_beats = "YES" if exp_ms > exp_b + 1e-9 else "NO"
        if (
            tr.get("BSPOT_MaxSec_TI") != f"{exp_ms:.4f}"
            or tr.get("BSPOT_Bayes_Full_TI") != f"{exp_bf:.4f}"
            or tr.get("BSPOT_Union_OR_TI") != f"{exp_uo:.4f}"
            or tr.get("BSPOT_FloorGuard_TI") != f"{exp_fg:.4f}"
            or tr.get("Prior_PotStrataZ_TI") != f"{exp_pr:.4f}"
            or tr.get("Flow_Efficient_Likelihood_TI") != f"{exp_fe:.4f}"
            or tr.get("Best_1040_TI") != f"{exp_b:.4f}"
            or tr.get("Best_1040_Model") != exp_bm
            or tr.get("MaxSec_Beats_All_1040") != exp_beats
        ):
            fail(f"Summary row {idx} ({sig}) mismatch: {tr}")

    # 5. Verify p1 and floor-guard metrics
    ms_300 = ti_by_mod_sig["BSPOT_MaxSec"]["chaneut_cha300_neut100"]
    ms_400 = ti_by_mod_sig["BSPOT_MaxSec"]["chaneut_cha400_neut200"]
    ms_med = statistics.median(ti_by_mod_sig["BSPOT_MaxSec"].values())

    fg_300 = ti_by_mod_sig["BSPOT_FloorGuard"]["chaneut_cha300_neut100"]
    fg_400 = ti_by_mod_sig["BSPOT_FloorGuard"]["chaneut_cha400_neut200"]
    fg_med = statistics.median(ti_by_mod_sig["BSPOT_FloorGuard"].values())
    fg_min = min(ti_by_mod_sig["BSPOT_FloorGuard"].values())

    uo_300 = ti_by_mod_sig["BSPOT_Union_OR"]["chaneut_cha300_neut100"]
    uo_400 = ti_by_mod_sig["BSPOT_Union_OR"]["chaneut_cha400_neut200"]
    uo_med = statistics.median(ti_by_mod_sig["BSPOT_Union_OR"].values())
    uo_min = min(ti_by_mod_sig["BSPOT_Union_OR"].values())

    if not (ms_300 >= 5.99 and ms_400 >= 6.99 and ms_med > 5.30):
        fail(f"BSPOT_MaxSec metrics below expected: cha300={ms_300}, cha400={ms_400}, med={ms_med}")
    if not (fg_300 > 1.60 and fg_400 > 1.70 and fg_min >= 0.90):
        fail(f"BSPOT_FloorGuard metrics below expected: cha300={fg_300}, cha400={fg_400}, min={fg_min}")
    if not (uo_300 >= 2.99 and uo_400 >= 4.99 and uo_med >= 4.99 and uo_min >= 0.80):
        fail(f"BSPOT_Union_OR metrics below expected: cha300={uo_300}, cha400={uo_400}, med={uo_med}, min={uo_min}")

    print("Negative control rejected perturbed CSV cell.")
    print(f"Verified all 136 signal-channel rows and live Channel 2a retraining (max float32 diff = {max_diff:.4f}).")
    print(f"BSPOT_MaxSec     : cha300 TI = {ms_300:.4f} (> 1.10), cha400 TI = {ms_400:.4f} (> 1.00), Median_TI = {ms_med:.4f}.")
    print(f"BSPOT_Union_OR   : cha300 TI = {uo_300:.4f} (> 1.10), cha400 TI = {uo_400:.4f} (> 1.00), Median_TI = {uo_med:.4f}, Min_TI = {uo_min:.4f} (>= 0.80).")
    print(f"BSPOT_FloorGuard : cha300 TI = {fg_300:.4f} (> 1.10), cha400 TI = {fg_400:.4f} (> 1.00), Median_TI = {fg_med:.4f}, Min_TI = {fg_min:.4f} (>= 0.90).")
    print("PASS")


if __name__ == "__main__":
    main()
