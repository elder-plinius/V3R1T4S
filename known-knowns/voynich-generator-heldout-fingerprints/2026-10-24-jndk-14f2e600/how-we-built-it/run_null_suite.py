#!/usr/bin/env python3
"""
run_null_suite.py — Lens 4 (statistician):
Execute the pre-registered 400-control null suite (200 word-order permutations +
200 position-preserving glyph shuffles = 400 controls per cell) across all 4
dialect x transliteration cells (A/ZL3b, B/ZL3b, A/IT2a, B/IT2a) for BOTH:
  1) The real Voynich manuscript corpus, and
  2) Our 152-entry Hand-Executable Boundary-Coupled Lexicon Cipher (VBCLC-152).
"""

import functools
import json
import math
import os
import random
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

import signatures_v27 as ev
sys.modules["signatures_v26"] = ev
import verifier as vf
from calibrate_and_audit import (
    collapse_eva,
    get_dialect_lines,
    parse_ivtff_clean,
)
from vbclc import TOTAL_TABLE_ENTRIES, encrypt_vbclc_lines

TOKENIZER = functools.lru_cache(maxsize=131072)(vf.TOKENIZER)
collapse_eva_cached = functools.lru_cache(maxsize=131072)(collapse_eva)


def _edge_mi_from_collapsed_lines(c_lines):
    trans = Counter()
    cond_c = Counter()
    tgt_c = Counter()
    for c_line in c_lines:
        for i in range(len(c_line) - 1):
            l_ch, f_ch = c_line[i][-1], c_line[i + 1][0]
            trans[(l_ch, f_ch)] += 1
            cond_c[l_ch] += 1
            tgt_c[f_ch] += 1
    total_pairs = sum(trans.values())
    if total_pairs == 0:
        return 0.0
    h_t = -sum((v / total_pairs) * math.log2(v / total_pairs) for v in tgt_c.values())
    h_tc = -sum((cnt / total_pairs) * math.log2(cnt / cond_c[c]) for (c, _), cnt in trans.items())
    return max(0.0, h_t - h_tc)


def fast_p2_and_edge_metrics(sents, ref_cal, n_shuffles=1, edge_shuffles=3, seed=0):
    """
    Fast, exact computation of the 4 arXiv:2604.19762 signatures (10-chunk MI,
    shuffle-corrected delta_MI_10chunk, E->S, full-corpus Bilat, chunk Shape)
    plus collapsed-EVA excess_edge_mi (arXiv:2608.17096) on `sents`.
    """
    n_chunks = 10
    chunk_size = len(sents) // n_chunks
    es_list, mi_list, mi_shuf_list, r2_list, cv_list, bilat_list = [], [], [], [], [], []
    shapes = []

    tok_all = ev.pretokenize(sents, TOKENIZER)
    n_se_full, n_ee_full = ev.bilateral_extremity_fast(tok_all)
    bilat_full = 1 if (n_se_full > 0 and n_ee_full > 0) else 0

    for i in range(n_chunks):
        start = i * chunk_size
        end = len(sents) if i == n_chunks - 1 else (i + 1) * chunk_size
        chunk_tok = tok_all[start:end]
        es_list.append(ev.end_start_pct_fast(chunk_tok))
        mi_o, mi_s, _ = ev.mi_with_retention_fast(chunk_tok, n_shuffles=n_shuffles)
        mi_list.append(mi_o)
        mi_shuf_list.append(mi_s)
        nse_c, nee_c = ev.bilateral_extremity_fast(chunk_tok)
        bilat_list.append(1 if (nse_c > 0 and nee_c > 0) else 0)
        r2_c, cv_c, sh_c = ev.zipfian_boundary_test_fast(chunk_tok)
        r2_list.append(r2_c)
        cv_list.append(cv_c)
        shapes.append(sh_c)

    es_mean = float(np.mean(es_list))
    mi_mean = float(np.mean(mi_list))
    mi_shuf_mean = float(np.mean(mi_shuf_list))
    delta_mi_mean = float(mi_mean - mi_shuf_mean)
    es_x_delta_mi = float((es_mean / 100.0) * delta_mi_mean)
    r2_mean = float(np.mean(r2_list))
    cv_mean = float(np.mean(cv_list))
    bilat_frac = float(np.mean(bilat_list))
    maj_shape = Counter(shapes).most_common(1)[0][0]

    # Adaptive checks
    ref_es = ref_cal["es_pct"]
    ref_mi = ref_cal["mi_orig"]
    es_lo, es_hi = max(ref_es - 15.0, 50.0), min(ref_es + 15.0, 98.0)
    mi_lo, mi_hi = max(0.10, ref_mi * 0.5), ref_mi * 2.0
    adap_pass = (
        (es_lo <= es_mean <= es_hi)
        and (bilat_full == 1)
        and (mi_lo <= mi_mean <= mi_hi)
        and (maj_shape in ("Zipfian", "Intermediate"))
    )
    fixed_pass_zipf = (
        (60.0 <= es_mean <= 85.0)
        and (bilat_full == 1)
        and (0.20 <= mi_mean <= 0.65)
        and (maj_shape == "Zipfian")
    )

    # Collapsed EVA edge MI (arXiv:2608.17096) with within-line shuffle baseline
    c_lines = [[collapse_eva_cached(w) for w in line if w] for line in sents]
    c_lines = [l for l in c_lines if len(l) >= 2]
    obs_edge_mi = _edge_mi_from_collapsed_lines(c_lines)

    rng_edge = random.Random(900000 + seed)
    shuf_edge_vals = []
    for _ in range(edge_shuffles):
        shuf_c = []
        for l in c_lines:
            l_copy = list(l)
            rng_edge.shuffle(l_copy)
            shuf_c.append(l_copy)
        shuf_edge_vals.append(_edge_mi_from_collapsed_lines(shuf_c))
    shuf_edge_mean = float(np.mean(shuf_edge_vals))
    excess_edge_mi = float(obs_edge_mi - shuf_edge_mean)

    return {
        "es_pct": es_mean,
        "bilat_full": bilat_full,
        "bilat_frac": bilat_frac,
        "mi_10chunk": mi_mean,
        "mi_shuf_10chunk": mi_shuf_mean,
        "delta_mi_10chunk": delta_mi_mean,
        "es_x_delta_mi": es_x_delta_mi,
        "zipf_r2": r2_mean,
        "cv": cv_mean,
        "shape": maj_shape,
        "adaptive_pass_4": bool(adap_pass),
        "fixed_pass_strict_zipf": bool(fixed_pass_zipf),
        "obs_edge_mi": float(obs_edge_mi),
        "excess_edge_mi": excess_edge_mi,
    }


def make_word_order_shuffle(sents, rng: random.Random):
    """Permute word tokens across the entire corpus while preserving line lengths."""
    flat = [w for line in sents for w in line]
    rng.shuffle(flat)
    out = []
    idx = 0
    for line in sents:
        k = len(line)
        out.append(flat[idx:idx + k])
        idx += k
    return out


def make_glyph_shuffle(sents, rng: random.Random):
    """Permute characters across all words while preserving exact word lengths and line lengths."""
    all_chars = [ch for line in sents for w in line for ch in w]
    rng.shuffle(all_chars)
    out = []
    idx = 0
    for line in sents:
        new_line = []
        for w in line:
            lw = len(w)
            new_line.append("".join(all_chars[idx:idx + lw]))
            idx += lw
        out.append(new_line)
    return out


def _eval_one_control(args):
    kind, seed, sents, ref_cal = args
    rng = random.Random(seed)
    if kind == "word":
        ctrl_sents = make_word_order_shuffle(sents, rng)
    else:
        ctrl_sents = make_glyph_shuffle(sents, rng)
    return kind, fast_p2_and_edge_metrics(ctrl_sents, ref_cal, n_shuffles=1, edge_shuffles=3, seed=seed)


def run_400_nulls_for_corpus(sents, ref_cal, label: str, pool: ProcessPoolExecutor):
    real_m = fast_p2_and_edge_metrics(sents, ref_cal, n_shuffles=3, edge_shuffles=30, seed=42)

    tasks = []
    # 200 word-order permutations (seeds 1000..1199)
    for k in range(200):
        tasks.append(("word", 1000 + k, sents, ref_cal))
    # 200 position-preserving glyph shuffles (seeds 2000..2199)
    for k in range(200):
        tasks.append(("glyph", 2000 + k, sents, ref_cal))

    word_shuf_records = []
    glyph_shuf_records = []
    for kind, m in pool.map(_eval_one_control, tasks, chunksize=8):
        if kind == "word":
            word_shuf_records.append(m)
        else:
            glyph_shuf_records.append(m)

    all_400 = word_shuf_records + glyph_shuf_records

    def summarize_family(recs, metric_key):
        arr = np.array([r[metric_key] for r in recs], dtype=float)
        return {
            "mean": float(arr.mean()),
            "sd": float(arr.std(ddof=1)),
            "min": float(arr.min()),
            "max": float(arr.max()),
            "p95": float(np.percentile(arr, 95.0)),
            "p99": float(np.percentile(arr, 99.0)),
        }

    def summarize_full_400(metric_key):
        arr = np.array([r[metric_key] for r in all_400], dtype=float)
        w_arr = np.array([r[metric_key] for r in word_shuf_records], dtype=float)
        g_arr = np.array([r[metric_key] for r in glyph_shuf_records], dtype=float)
        real_v = float(real_m[metric_key])
        return {
            "real_val": real_v,
            "best_control_400": float(arr.max()),
            "mean_control_400": float(arr.mean()),
            "sd_control_400": float(arr.std(ddof=1)),
            "word_shuffle_200": summarize_family(word_shuf_records, metric_key),
            "glyph_shuffle_200": summarize_family(glyph_shuf_records, metric_key),
            "beats_all_400": bool(real_v > arr.max()),
            "beats_all_200_word_shuf": bool(real_v > w_arr.max()),
            "beats_all_200_glyph_shuf": bool(real_v > g_arr.max()),
            "z_score_vs_400": float((real_v - arr.mean()) / max(1e-12, arr.std(ddof=1))),
            "z_score_vs_word_shuffle": float((real_v - w_arr.mean()) / max(1e-12, w_arr.std(ddof=1))),
        }

    n_pass_adap_word = sum(1 for r in word_shuf_records if r["adaptive_pass_4"])
    n_pass_adap_glyph = sum(1 for r in glyph_shuf_records if r["adaptive_pass_4"])
    n_pass_fixed_400 = sum(1 for r in all_400 if r["fixed_pass_strict_zipf"])

    summary = {
        "label": label,
        "real": real_m,
        "n_controls_total": 400,
        "n_word_order_controls": 200,
        "n_glyph_shuffle_controls": 200,
        "delta_mi_10chunk": summarize_full_400("delta_mi_10chunk"),
        "es_x_delta_mi": summarize_full_400("es_x_delta_mi"),
        "excess_edge_mi": summarize_full_400("excess_edge_mi"),
        "mi_10chunk": summarize_full_400("mi_10chunk"),
        "es_pct": summarize_full_400("es_pct"),
        "controls_passing_adaptive_4_word_shuf": n_pass_adap_word,
        "controls_passing_adaptive_4_glyph_shuf": n_pass_adap_glyph,
        "controls_passing_fixed_strict_zipf_400": n_pass_fixed_400,
    }
    return summary


def main():
    t0 = time.time()
    ref_cal = json.loads((DATA / "reference_calibration.json").read_text())
    pt_latin0 = (DATA / "plaintexts" / "Latin-00.txt").read_text(encoding="utf-8")

    null_report = {
        "protocol": "400 controls per cell (200 word-order permutations [seeds 1000..1199] + 200 glyph-shuffled controls [seeds 2000..2199])",
        "manuscript_400_nulls": {},
        "vbclc152_400_nulls": {},
    }

    n_workers = min(8, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        for ms_name, fname in [("ZL3b", "ZL3b-n.txt"), ("IT2a", "IT2a-n.txt")]:
            p2_lines, _, meta = parse_ivtff_clean(DATA / fname)
            for lang in ("A", "B"):
                cell = f"{lang}/{ms_name}"
                sigma_f = 1 if lang == "A" else 0
                sents_ms, _ = get_dialect_lines(p2_lines, meta, lang, use_parisel_map=True)
                ref_c = ref_cal["reference_p2"][cell]["clean_ivtff"]

                print(f"[Null Suite] Running 400 controls on Manuscript {cell}...", flush=True)
                ms_res = run_400_nulls_for_corpus(sents_ms, ref_c, f"Manuscript_{cell}", pool)
                null_report["manuscript_400_nulls"][cell] = ms_res
                print(
                    f"  MS {cell}: delta_MI real={ms_res['delta_mi_10chunk']['real_val']:.4f} vs best_400={ms_res['delta_mi_10chunk']['best_control_400']:.4f} "
                    f"(beats_400={ms_res['delta_mi_10chunk']['beats_all_400']}, z={ms_res['delta_mi_10chunk']['z_score_vs_400']:.1f}) | "
                    f"exEdgeMI real={ms_res['excess_edge_mi']['real_val']:.4f} vs best_400={ms_res['excess_edge_mi']['best_control_400']:.4f} "
                    f"(beats_400={ms_res['excess_edge_mi']['beats_all_400']}) | "
                    f"nulls_passing_4/4={ms_res['controls_passing_adaptive_4_word_shuf'] + ms_res['controls_passing_adaptive_4_glyph_shuf']}/400",
                    flush=True,
                )

                print(f"[Null Suite] Running 400 controls on VBCLC-152 {cell}...", flush=True)
                sents_gen = encrypt_vbclc_lines(pt_latin0, sents_ms, sigma_f=sigma_f, seed=10000 if lang == "A" else 20000)
                gen_res = run_400_nulls_for_corpus(sents_gen, ref_c, f"VBCLC152_{cell}", pool)
                null_report["vbclc152_400_nulls"][cell] = gen_res
                print(
                    f"  VBCLC-152 {cell}: delta_MI real={gen_res['delta_mi_10chunk']['real_val']:.4f} vs best_400={gen_res['delta_mi_10chunk']['best_control_400']:.4f} "
                    f"(beats_400={gen_res['delta_mi_10chunk']['beats_all_400']}, z={gen_res['delta_mi_10chunk']['z_score_vs_400']:.1f}) | "
                    f"exEdgeMI real={gen_res['excess_edge_mi']['real_val']:.4f} vs best_400={gen_res['excess_edge_mi']['best_control_400']:.4f} "
                    f"(beats_400={gen_res['excess_edge_mi']['beats_all_400']}) | "
                    f"nulls_passing_4/4={gen_res['controls_passing_adaptive_4_word_shuf'] + gen_res['controls_passing_adaptive_4_glyph_shuf']}/400",
                    flush=True,
                )

    out_path = JOB_OUT / "null_suite_400_results.json"
    out_path.write_text(json.dumps(null_report, indent=2))
    print(f"\nSaved 400-control null suite results to {out_path} in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
