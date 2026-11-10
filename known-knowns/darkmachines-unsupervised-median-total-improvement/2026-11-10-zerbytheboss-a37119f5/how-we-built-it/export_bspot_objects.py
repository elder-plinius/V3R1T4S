#!/usr/bin/env python3
"""Deterministically export sorted BS-POT object CSV and 19-signal summary TSV from dm_bsp_eval raw output."""
import csv
import gzip
import json
import math
import sys

MODELS = ["BSPOT_MaxSec", "BSPOT_Bayes_Full", "BSPOT_Union_OR", "BSPOT_FloorGuard"]
M_ORDER = {m: idx for idx, m in enumerate(MODELS)}
C_ORDER = {"1": 0, "2a": 1, "2b": 2, "3": 3}


def main():
    if len(sys.argv) != 5:
        sys.stderr.write(
            "Usage: python3 export_bspot_objects.py <bspot_raw_counts.csv> <bspot_eval_ref.json.gz> <out_results.csv> <out_summary.tsv>\n"
        )
        sys.exit(1)

    raw_csv_path, ref_gz_path, out_csv_path, out_tsv_path = sys.argv[1:5]
    with open(raw_csv_path, "r", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))
    if len(raw_rows) != 136:
        raise ValueError(f"Expected 136 rows, got {len(raw_rows)}")

    with gzip.open(ref_gz_path, "rt", encoding="utf-8") as gz:
        ref = json.load(gz)
    best_1040 = ref["best_1040"]
    best_1040_model = ref["best_1040_model"]
    flow_eff = ref["flow_eff"]
    prior_strata_ti = ref["prior_strata_ti"]

    raw_rows.sort(key=lambda r: (C_ORDER[r["Chan"]], r["Signal"], M_ORDER[r["Model"]]))

    obj_csv_lines = ["Signal,Model,Chan,AUC,1e-2,1e-3,1e-4,SI_1e-2,SI_1e-3,SI_1e-4,SI_All"]
    ti_by_mod_sig = {m: {} for m in MODELS}

    for r in raw_rows:
        sig = r["Signal"]
        mod = r["Model"]
        chan = r["Chan"]
        n_sig = int(r["n_sig"])
        p2 = int(r["pass_1e-2"])
        p3 = int(r["pass_1e-3"])
        p4 = int(r["pass_1e-4"])
        auc = round(float(r["AUC"]), 4)

        e2 = round(p2 / float(n_sig), 2)
        e3 = round(p3 / float(n_sig), 2)
        e4 = round(p4 / float(n_sig), 2)
        si2 = round(e2 / math.sqrt(1e-2), 4)
        si3 = round(e3 / math.sqrt(1e-3), 4)
        si4 = round(e4 / math.sqrt(1e-4), 4)
        si_all = round(max(si2, si3, si4), 4)

        ti_by_mod_sig[mod][sig] = max(ti_by_mod_sig[mod].get(sig, 0.0), si_all)
        obj_csv_lines.append(
            f"{sig},{mod},{chan},{auc:.4f},{e2:.2f},{e3:.2f},{e4:.2f},{si2:.4f},{si3:.4f},{si4:.4f},{si_all:.4f}"
        )

    with open(out_csv_path, "wb") as f:
        f.write(("\n".join(obj_csv_lines) + "\n").encode("utf-8"))

    tsv_hdr = [
        "Signal",
        "BSPOT_MaxSec_TI",
        "BSPOT_Bayes_Full_TI",
        "BSPOT_Union_OR_TI",
        "BSPOT_FloorGuard_TI",
        "Prior_PotStrataZ_TI",
        "Flow_Efficient_Likelihood_TI",
        "Best_1040_TI",
        "Best_1040_Model",
        "MaxSec_Beats_All_1040",
    ]
    tsv_lines = ["\t".join(tsv_hdr)]
    for sig in sorted(best_1040.keys()):
        t_ms = ti_by_mod_sig["BSPOT_MaxSec"][sig]
        t_bf = ti_by_mod_sig["BSPOT_Bayes_Full"][sig]
        t_uo = ti_by_mod_sig["BSPOT_Union_OR"][sig]
        t_fg = ti_by_mod_sig["BSPOT_FloorGuard"][sig]
        t_pr = float(prior_strata_ti[sig])
        t_fe = float(flow_eff[sig])
        t_b = float(best_1040[sig])
        bm = str(best_1040_model[sig])
        beats = "YES" if t_ms > t_b + 1e-9 else "NO"
        tsv_lines.append(
            f"{sig}\t{t_ms:.4f}\t{t_bf:.4f}\t{t_uo:.4f}\t{t_fg:.4f}\t{t_pr:.4f}\t{t_fe:.4f}\t{t_b:.4f}\t{bm}\t{beats}"
        )

    with open(out_tsv_path, "wb") as f:
        f.write(("\n".join(tsv_lines) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
