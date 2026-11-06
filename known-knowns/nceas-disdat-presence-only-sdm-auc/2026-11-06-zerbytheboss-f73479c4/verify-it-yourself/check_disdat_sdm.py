#!/usr/bin/env python3
"""Standalone pure-stdlib verifier for NCEAS disdat Presence-Only SDM benchmark (win + p1 + p2 + p3)."""

import csv
import gzip
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OBJ_CSV = ROOT / "object" / "disdat_225_species_auc.csv"
DATA_DIR = ROOT / "verify-it-yourself" / "data"
SHARDS = sorted(DATA_DIR.glob("disdat_pa_eval_*.json.gz"))

# Published per-region best ROC AUCs from known-unknowns/ecology/nceas-disdat-presence-only-sdm-auc.md
PUBLISHED_REGION_RECORDS = {
    "AWT": 0.732,  # Random Forest down-sampled (Valavi et al. 2022)
    "CAN": 0.732,  # Boosted Regression Trees (Valavi et al. 2022)
    "NSW": 0.752,  # DeepMaxent TGB (Ryckewaert et al. 2025)
    "NZ": 0.759,   # TabPFN-ens LORO fine-tuned (Doi et al. 2026 Table S2)
    "SA": 0.820,   # TabPFN-ens LORO fine-tuned (Doi et al. 2026 Table S2)
    "SWI": 0.850,  # DeepMaxent TGB (Ryckewaert et al. 2025)
}


def roc_auc_mann_whitney(y_true, y_score) -> float:
    pairs = sorted(zip(y_score, y_true), key=lambda x: x[0])
    n = len(pairs)
    n_pos = sum(y_true)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    rank_sum_pos = 0.0
    i = 0
    while i < n:
        j = i + 1
        while j < n and pairs[j][0] == pairs[i][0]:
            j += 1
        avg_rank = 0.5 * ((i + 1) + j)
        pos_in_tie = sum(pairs[k][1] for k in range(i, j))
        rank_sum_pos += pos_in_tie * avg_rank
        i = j
    u_stat = rank_sum_pos - (n_pos * (n_pos + 1)) / 2.0
    return u_stat / (n_pos * n_neg)


def main() -> int:
    if not OBJ_CSV.is_file() or not SHARDS:
        print("FAIL")
        return 1

    try:
        with OBJ_CSV.open("r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        bundle = []
        for p in SHARDS:
            with gzip.open(p, "rt", encoding="utf-8") as gz:
                bundle.extend(json.load(gz)["species"])
    except Exception:
        print("FAIL")
        return 1

    if len(rows) != 225 or len(bundle) != 225:
        print("FAIL")
        return 1

    reg_v2 = {}
    reg_v3 = {}
    aucs_217_v2 = []
    aucs_217_v3 = []

    for row, ref in zip(rows, bundle):
        try:
            r = row["region"]
            g = row["group"]
            bg = row["bio_group"]
            sp = row["spid"]
            n_po = int(row["n_po_records"])
            n_sites = int(row["n_pa_eval_sites"])
            n_pres = int(row["n_pa_presences"])
            in_217 = row["in_217_subset"].strip().lower() == "true"
            auc_cols = {
                k: float(row[k])
                for k in (
                    "auc_deepmaxent_tgb",
                    "auc_newton_bio_cell",
                    "auc_newton_reg_site",
                    "auc_sp_kde_bio",
                    "auc_tgb_base_v1",
                    "auc_tgb_hybrid_v2",
                    "auc_tgb_hybrid_v3",
                )
            }
        except Exception:
            print("FAIL")
            return 1

        if (
            r != ref["region"]
            or g != ref["group"]
            or bg != ref["bio_group"]
            or sp != ref["spid"]
            or n_po != ref["n_po_records"]
            or n_sites != len(ref["y_true"])
            or n_pres != sum(ref["y_true"])
            or in_217 != (n_po < 1000)
        ):
            print("FAIL")
            return 1

        for k, val in auc_cols.items():
            if abs(val - ref["expected_aucs"][k]) > 1e-6:
                print("FAIL")
                return 1

        recomp_v2 = roc_auc_mann_whitney(ref["y_true"], ref["pred_v2"])
        recomp_v3 = roc_auc_mann_whitney(ref["y_true"], ref["pred_v3"])
        if (
            abs(recomp_v2 - auc_cols["auc_tgb_hybrid_v2"]) > 5e-5
            or abs(recomp_v3 - auc_cols["auc_tgb_hybrid_v3"]) > 5e-5
        ):
            print("FAIL")
            return 1

        reg_v2.setdefault(r, []).append(recomp_v2)
        reg_v3.setdefault(r, []).append(recomp_v3)
        if in_217:
            aucs_217_v2.append(recomp_v2)
            aucs_217_v3.append(recomp_v3)

    reg_means_v3 = {r: sum(v) / len(v) for r, v in reg_v3.items()}
    mean6_v2 = sum(sum(v) / len(v) for v in reg_v2.values()) / 6.0
    mean6_v3 = sum(reg_means_v3.values()) / 6.0
    med217_v2 = statistics.median(aucs_217_v2)
    med217_v3 = statistics.median(aucs_217_v3)
    regions_beaten_v3 = sum(1 for r, m in reg_means_v3.items() if m > PUBLISHED_REGION_RECORDS[r])

    if not (
        len(aucs_217_v3) == 217
        and mean6_v2 > 0.773
        and med217_v2 > 0.774
        and mean6_v3 > 0.773
        and med217_v3 > 0.774
        and regions_beaten_v3 >= 3
    ):
        print("FAIL")
        return 1

    print(
        f"Verified 225 NCEAS disdat species: tgb_hybrid_v3 6-region mean AUC={mean6_v3:.5f} > 0.77300, "
        f"217-species median AUC={med217_v3:.5f} > 0.77400, regions beaten={regions_beaten_v3}/6"
    )
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
