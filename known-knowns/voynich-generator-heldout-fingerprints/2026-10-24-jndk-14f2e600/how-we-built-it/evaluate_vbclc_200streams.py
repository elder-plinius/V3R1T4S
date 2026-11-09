#!/usr/bin/env python3
"""
evaluate_vbclc_200streams.py — Full evaluation of the frozen 152-entry
Hand-Executable Voynich Boundary-Coupled Lexicon Cipher (VBCLC-152) across
20 period plaintexts (10 Latin, 10 Italian) x 10 seeds = 200 streams per cell
on Currier A and Currier B across BOTH ZL3b-n.txt and IT2a-n.txt (plus RF1b-e.txt
and the 37,000-word synthetic length of Parisel 2026).
"""

import copy
import json
import os
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
JOB_OUT = Path(os.environ.get("JOB_OUT", str(ROOT / "output")))
JOB_OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(DATA))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from calibrate_and_audit import parse_ivtff_clean, get_dialect_lines, score_p2, score_p1
import verifier as vf
from vbclc import TOTAL_TABLE_ENTRIES, encrypt_vbclc_lines


def _eval_single_stream(args):
    pt_id, pt_lang, pt_text, tmpl, sigma_f, seed, ref_clean, ref_raw, do_p1 = args
    gen_lines = encrypt_vbclc_lines(pt_text, tmpl, sigma_f=sigma_f, seed=seed)
    sc_clean = score_p2(gen_lines, ref_cal=ref_clean, n_chunks=10, n_shuffles=3)
    sc_clean["plaintext"] = pt_id
    sc_clean["seed"] = seed

    # Compute adaptive checks against raw_parisel_ref on the exact same signature values
    sc_raw = copy.deepcopy(sc_clean)
    agg_proxy = {
        "es_pct_mean": sc_clean["es_pct"],
        "mi_orig_mean": sc_clean["mi_orig"],
        "bilat_frac": sc_clean["bilat_frac"],
        "shape": sc_clean["shape"],
    }
    adap_raw, _ = vf.compute_adaptive_checks(agg_proxy, sc_clean["bilat_full"], ref_raw)
    sc_raw["adaptive_checks"] = {k: bool(v) for k, v in adap_raw.items()}
    sc_raw["adaptive_pass_4"] = bool(all(adap_raw.values()))
    sc_raw["adaptive_pass_strict_zipf"] = bool(all(adap_raw.values()) and sc_clean["shape"] == "Zipfian")

    p1_sc = None
    if do_p1:
        p1_sc = score_p1(gen_lines, shuffles=30, seed=seed)["collapsed"]

    return pt_lang, sc_clean, sc_raw, p1_sc


def _eval_37k_stream(args):
    pt_text, tmpl_37k, sigma_f, seed, ref_rf = args
    gen_37k = encrypt_vbclc_lines(pt_text, tmpl_37k, sigma_f=sigma_f, seed=seed)
    return score_p2(gen_37k, ref_cal=ref_rf, n_chunks=10, n_shuffles=3)


def summarize_p2_streams(records):
    n = len(records)
    es = np.array([r["es_pct"] for r in records], dtype=float)
    mi = np.array([r["mi_orig"] for r in records], dtype=float)
    r2 = np.array([r["zipf_r2"] for r in records], dtype=float)
    cv = np.array([r["cv"] for r in records], dtype=float)
    bilat_full = np.array([r["bilat_full"] for r in records], dtype=float)
    bilat_frac = np.array([r["bilat_frac"] for r in records], dtype=float)
    shapes = dict(Counter(r["shape"] for r in records))

    adap_pass = sum(1 for r in records if r["adaptive_pass_4"])
    adap_zipf_pass = sum(1 for r in records if r["adaptive_pass_strict_zipf"])
    fixed_pass = sum(1 for r in records if r["fixed_pass_4"])
    fixed_zipf_pass = sum(1 for r in records if r["fixed_pass_strict_zipf"])
    joint_all_pass = sum(
        1 for r in records
        if r["adaptive_pass_4"] and r["adaptive_pass_strict_zipf"]
        and r["fixed_pass_4"] and r["fixed_pass_strict_zipf"]
    )

    return {
        "n_streams": n,
        "table_entries": TOTAL_TABLE_ENTRIES,
        "adaptive_pass_count": adap_pass,
        "adaptive_pass_rate": adap_pass / n,
        "adaptive_strict_zipf_pass_count": adap_zipf_pass,
        "adaptive_strict_zipf_pass_rate": adap_zipf_pass / n,
        "fixed_pass_count": fixed_pass,
        "fixed_pass_rate": fixed_pass / n,
        "fixed_strict_zipf_pass_count": fixed_zipf_pass,
        "fixed_strict_zipf_pass_rate": fixed_zipf_pass / n,
        "joint_all_criteria_pass_count": joint_all_pass,
        "joint_all_criteria_pass_rate": joint_all_pass / n,
        "es_pct": {
            "mean": float(es.mean()), "sd": float(es.std(ddof=1)),
            "min": float(es.min()), "max": float(es.max()),
        },
        "mi_orig": {
            "mean": float(mi.mean()), "sd": float(mi.std(ddof=1)),
            "min": float(mi.min()), "max": float(mi.max()),
        },
        "zipf_r2": {
            "mean": float(r2.mean()), "sd": float(r2.std(ddof=1)),
            "min": float(r2.min()), "max": float(r2.max()),
        },
        "cv": {
            "mean": float(cv.mean()), "sd": float(cv.std(ddof=1)),
            "min": float(cv.min()), "max": float(cv.max()),
        },
        "bilat_full_rate": float(bilat_full.mean()),
        "bilat_chunk_frac_mean": float(bilat_frac.mean()),
        "shapes": shapes,
    }


def main():
    t0 = time.time()
    ref_cal = json.loads((DATA / "reference_calibration.json").read_text())

    # Load templates for ZL3b-n, IT2a-n, RF1b-e
    templates = {}
    for ms_name, fname in [("ZL3b", "ZL3b-n.txt"), ("IT2a", "IT2a-n.txt"), ("RF1b-e", "RF1b-e.txt")]:
        p2_lines, p1_lines, meta = parse_ivtff_clean(DATA / fname)
        for lang in ("A", "B"):
            cell = f"{lang}/{ms_name}"
            lines_p2, _ = get_dialect_lines(p2_lines, meta, lang, use_parisel_map=True)
            lines_p1, _ = get_dialect_lines(p1_lines, meta, lang, use_parisel_map=False)
            templates[cell] = {"p2": lines_p2, "p1": lines_p1}

    # Plaintexts: 10 Latin + 10 Italian = 20 plaintexts
    plaintexts = []
    for lang_name in ("Latin", "Italian"):
        for idx in range(10):
            pt_path = DATA / "plaintexts" / f"{lang_name}-{idx:02d}.txt"
            plaintexts.append((f"{lang_name}-{idx:02d}", lang_name, pt_path.read_text(encoding="utf-8")))

    results = {
        "generator_name": "VBCLC-152",
        "total_table_entries": TOTAL_TABLE_ENTRIES,
        "per_folio_state_bits": 1,
        "cells_p2_200streams": {},
        "by_language_p2": {},
        "synthetic_37k_p2": {},
        "p1_evaluation": {},
    }

    n_workers = min(8, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        # Evaluate 200 streams (20 plaintexts x 10 seeds) per cell across all 6 cells
        for cell in ("A/ZL3b", "B/ZL3b", "A/IT2a", "B/IT2a", "A/RF1b-e", "B/RF1b-e"):
            lang = cell.split("/")[0]
            sigma_f = 1 if lang == "A" else 0
            tmpl = templates[cell]["p2"]
            ref_clean = ref_cal["reference_p2"][cell]["clean_ivtff"]
            ref_raw = ref_cal["reference_p2"][cell]["raw_parisel_parser"]

            tasks = []
            for pt_idx, (pt_id, pt_lang, pt_text) in enumerate(plaintexts):
                for s in range(10):
                    seed = 10000 * (1 if lang == "A" else 2) + 100 * pt_idx + s
                    do_p1 = (cell in ("A/ZL3b", "B/ZL3b", "A/IT2a", "B/IT2a") and s < 2)
                    tasks.append((pt_id, pt_lang, pt_text, tmpl, sigma_f, seed, ref_clean, ref_raw, do_p1))

            cell_records_clean = []
            cell_records_raw = []
            latin_records = []
            italian_records = []
            p1_records = []

            for pt_lang, sc_clean, sc_raw, p1_sc in pool.map(_eval_single_stream, tasks):
                cell_records_clean.append(sc_clean)
                cell_records_raw.append(sc_raw)
                if pt_lang == "Latin":
                    latin_records.append(sc_clean)
                else:
                    italian_records.append(sc_clean)
                if p1_sc is not None:
                    p1_records.append(p1_sc)

            sum_clean = summarize_p2_streams(cell_records_clean)
            sum_raw = summarize_p2_streams(cell_records_raw)
            results["cells_p2_200streams"][cell] = {
                "vs_clean_ivtff_ref": sum_clean,
                "vs_raw_parisel_ref": sum_raw,
            }
            results["by_language_p2"][cell] = {
                "Latin_100streams": summarize_p2_streams(latin_records),
                "Italian_100streams": summarize_p2_streams(italian_records),
            }

            print(
                f"[p2 {cell}] 200 streams: "
                f"adaptive_pass={sum_clean['adaptive_pass_count']}/200 ({100*sum_clean['adaptive_pass_rate']:.1f}%), "
                f"strict_zipf_pass={sum_clean['adaptive_strict_zipf_pass_count']}/200 ({100*sum_clean['adaptive_strict_zipf_pass_rate']:.1f}%), "
                f"raw_ref_pass={sum_raw['adaptive_pass_count']}/200 ({100*sum_raw['adaptive_pass_rate']:.1f}%), "
                f"E->S={sum_clean['es_pct']['mean']:.1f}% [{sum_clean['es_pct']['min']:.1f},{sum_clean['es_pct']['max']:.1f}], "
                f"MI={sum_clean['mi_orig']['mean']:.4f} [{sum_clean['mi_orig']['min']:.4f},{sum_clean['mi_orig']['max']:.4f}], "
                f"R2={sum_clean['zipf_r2']['mean']:.3f} (min {sum_clean['zipf_r2']['min']:.3f}), "
                f"CV={sum_clean['cv']['mean']:.2f}",
                flush=True,
            )

            if p1_records:
                ex_mi = np.array([r["excess_edge_mi"] for r in p1_records])
                sh_mi = np.array([r["edge_share"] for r in p1_records])
                sing = np.array([r["singleton_rate"] for r in p1_records])
                h2_arr = np.array([r["h2"] for r in p1_records])
                wl_arr = np.array([r["word_len_mean"] for r in p1_records])
                results["p1_evaluation"][cell] = {
                    "n_streams": len(p1_records),
                    "excess_edge_mi_mean": float(ex_mi.mean()),
                    "excess_edge_mi_sd": float(ex_mi.std(ddof=1)),
                    "edge_share_mean": float(sh_mi.mean()),
                    "singleton_rate_mean": float(sing.mean()),
                    "singleton_rate_sd": float(sing.std(ddof=1)),
                    "h2_collapsed_mean": float(h2_arr.mean()),
                    "word_len_collapsed_mean": float(wl_arr.mean()),
                }
                print(
                    f"  [p1 {cell}] excess_MI={ex_mi.mean():.4f}±{ex_mi.std(ddof=1):.4f}, "
                    f"share={100*sh_mi.mean():.2f}%, singleton={sing.mean():.4f}±{sing.std(ddof=1):.4f}, "
                    f"h2={h2_arr.mean():.4f}, len={wl_arr.mean():.2f}",
                    flush=True,
                )

        # Also evaluate 37,000-word synthetic length (Parisel default) across all 20 plaintexts x 2 seeds = 40 streams
        tmpl_37k = [["w"] * 8 for _ in range(37000 // 8)]
        for lang in ("A", "B"):
            sigma_f = 1 if lang == "A" else 0
            ref_rf = ref_cal["reference_p2"][f"{lang}/RF1b-e"]["raw_parisel_parser"]
            tasks_37k = []
            for pt_idx, (pt_id, _, pt_text) in enumerate(plaintexts):
                for s in range(2):
                    seed = 90000 + 100 * pt_idx + s
                    tasks_37k.append((pt_text, tmpl_37k, sigma_f, seed, ref_rf))
            recs_37k = list(pool.map(_eval_37k_stream, tasks_37k))
            sum_37k = summarize_p2_streams(recs_37k)
            results["synthetic_37k_p2"][lang] = sum_37k
            print(
                f"[p2 37k-words {lang}] 40 streams: "
                f"pass={sum_37k['joint_all_criteria_pass_count']}/40 ({100*sum_37k['joint_all_criteria_pass_rate']:.1f}%), "
                f"E->S={sum_37k['es_pct']['mean']:.1f}%, MI={sum_37k['mi_orig']['mean']:.4f}, R2={sum_37k['zipf_r2']['mean']:.3f}",
                flush=True,
            )

    # Save a sample generated corpus for Currier A and Currier B so standalone verifier.py can also be run on them
    sample_A = encrypt_vbclc_lines(plaintexts[0][2], templates["A/ZL3b"]["p2"], sigma_f=1, seed=10000)
    sample_B = encrypt_vbclc_lines(plaintexts[0][2], templates["B/ZL3b"]["p2"], sigma_f=0, seed=20000)
    (JOB_OUT / "sample_vbclc_A.txt").write_text("\n".join(" ".join(l) for l in sample_A) + "\n")
    (JOB_OUT / "sample_vbclc_B.txt").write_text("\n".join(" ".join(l) for l in sample_B) + "\n")

    out_path = JOB_OUT / "vbclc_200streams_evaluation.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nSaved full 200-stream evaluation to {out_path} in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
