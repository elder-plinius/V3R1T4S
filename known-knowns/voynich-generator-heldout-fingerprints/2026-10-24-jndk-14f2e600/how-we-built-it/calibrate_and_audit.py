#!/usr/bin/env python3
"""
calibrate_and_audit.py — Lens 1 (reader):
1. Calibrate arXiv:2604.19762 (p2) and arXiv:2608.17096 (p1) reference metrics
   and 2,000-draw page-bootstrap 95% envelopes across Currier A and B on
   ZL3b-n.txt, IT2a-n.txt, and RF1b-e.txt.
2. Score the published Slot-based generator (signatures_v27.py), published
   Cardan-grille generator (grille.py), and unmodified Naibbe cipher (naibbe.py,
   20 plaintexts x 10 seeds) against p2 and p1 across all 4 cells.
3. Audit the line-823 pair_strength bug in signatures_v27.py and chunk-size
   finite-sample plug-in MI scaling.
"""

import csv
import hashlib
import importlib.util
import json
import math
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
JOB_OUT = Path(os.environ.get("JOB_OUT", str(ROOT / "output")))
JOB_OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(DATA))
import signatures_v27 as ev
sys.modules["signatures_v26"] = ev
import grille as gr
import verifier as vf

TOKENIZER = vf.TOKENIZER

# ============================================================================
# 1. Clean IVTFF Parser (supporting both RF1b-e and ZL3b-n / IT2a-n)
# ============================================================================

HEADER_RE = re.compile(r"^<([^>.]+)>\s+<!([^\n]+)>")
LOCUS_RE = re.compile(r"^<([^>.]+)\.([^,>]+),([@+*=~&])([A-Za-z0-9]+)[^>]*>\s*(.*)$")
SUBS = [
    ("cth", "T"), ("ckh", "K"), ("cph", "P"), ("cfh", "F"),
    ("ch", "C"), ("sh", "S"), ("iin", "N"), ("in", "I"), ("ee", "E"),
]


def collapse_eva(w: str) -> str:
    w = w.lower().strip()
    for a, b in SUBS:
        w = w.replace(a, b)
    return w


def strip_ivtff_markup(s: str) -> str:
    s = s.replace("<->", ".")
    s = re.sub(r"<!.*?>", "", s)
    s = re.sub(r"<[^>]*>", "", s)
    s = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", s)
    s = re.sub(r"\{([^}]*)\}", r"\1", s)
    s = re.sub(r"@[0-9]+;", "", s)
    s = s.replace("'", "")
    return s


def parse_ivtff_clean(filepath: Path, paragraph_only: bool = False):
    """
    Parse an IVTFF file into:
      - folio_lines_p2: {folio: [[tok, ...], ...]} (len(tok)>1, len(line)>=2, matching Parisel)
      - folio_lines_p1: {folio: [[tok, ...], ...]} (paragraph lines P, len(tok)>=1, len(line)>=2, matching Rozanova)
      - folio_meta: {folio: {'L': 'A'|'B'|'?', 'Q': ...}}
    """
    text = filepath.read_text(encoding="utf-8", errors="replace")
    folio_meta = {}
    folio_lines_p2 = defaultdict(list)
    folio_lines_p1 = defaultdict(list)
    current_folio = None

    for raw_line in text.splitlines():
        raw_line = raw_line.rstrip("\n")
        hm = HEADER_RE.match(raw_line)
        if hm:
            raw_f = hm.group(1)
            norm_f = re.sub(r"(\d+[rv])\d*$", r"\1", raw_f)
            tags = dict(re.findall(r"\$([A-Z])=([^ $>]+)", hm.group(2)))
            folio_meta[norm_f] = tags
            folio_meta[raw_f] = tags
            current_folio = norm_f
            continue
        if raw_line.startswith("#") or not raw_line.strip():
            continue
        lm = LOCUS_RE.match(raw_line)
        if lm:
            raw_f = lm.group(1)
            norm_f = re.sub(r"(\d+[rv])\d*$", r"\1", raw_f)
            current_folio = norm_f
            locus_type = lm.group(4)
            content = lm.group(5)
        else:
            continue

        cleaned_str = strip_ivtff_markup(content)
        raw_tokens = re.split(r"[.,\s]+", cleaned_str)

        # Parisel convention: alpha tokens with len > 1, lines with >= 2 tokens
        toks_p2 = []
        for t in raw_tokens:
            t = re.sub(r"[^a-zA-Z?]", "", t).lower()
            if t and "?" not in t and len(t) > 1 and t.isalpha():
                toks_p2.append(t)
        if len(toks_p2) >= 2:
            folio_lines_p2[current_folio].append(toks_p2)

        # Rozanova & Temerev convention: paragraph lines (locus_type startswith P), all tokens a-z
        if locus_type.startswith("P"):
            toks_p1 = []
            usable = True
            for t in [x for x in raw_tokens if x]:
                t_clean = t.strip().lower()
                if not re.fullmatch(r"[a-z]+", t_clean):
                    usable = False
                    break
                toks_p1.append(t_clean)
            if usable and len(toks_p1) >= 2:
                folio_lines_p1[current_folio].append(toks_p1)

    return folio_lines_p2, folio_lines_p1, folio_meta


def get_dialect_lines(folio_lines, folio_meta, lang: str, use_parisel_map: bool = True):
    """Return list of lines and dict of {folio: lines} for dialect A or B."""
    lines = []
    by_folio = {}
    if use_parisel_map:
        target_folios = vf.SIGMA_1_FOLIOS if lang == "A" else vf.SIGMA_0_FOLIOS
        for f in sorted(target_folios):
            if f in folio_lines and folio_lines[f]:
                by_folio[f] = folio_lines[f]
                lines.extend(folio_lines[f])
    else:
        for f in sorted(folio_lines.keys()):
            l_tag = folio_meta.get(f, {}).get("L", vf.FOLIO_LANG_MAP.get(f, "?"))
            if l_tag == lang and folio_lines[f]:
                by_folio[f] = folio_lines[f]
                lines.extend(folio_lines[f])
    return lines, by_folio


# ============================================================================
# 2. Scorers for p2 (arXiv:2604.19762) and p1 (arXiv:2608.17096)
# ============================================================================

def score_p2(sentences, ref_cal=None, n_chunks=10, n_shuffles=3):
    """Evaluate 4 Currier signatures of arXiv:2604.19762 on a list of sentences."""
    sents = [ [w for w in s if len(w) > 1 and w.isalpha()] for s in sentences ]
    sents = [ s for s in sents if len(s) >= 2 ]
    if len(sents) < 10:
        return {"error": "too_few_sentences"}

    chunk_res = vf.evaluate_chunked(sents, n_chunks, n_shuffles, "cand")
    agg = ev.aggregate(chunk_res, label="cand")
    full_res = vf.evaluate_full(sents, n_shuffles, "cand-full")
    bilat_full = 1 if (full_res and full_res["n_start_extreme"] > 0 and full_res["n_end_extreme"] > 0) else 0

    out = {
        "es_pct": float(agg["es_pct_mean"]),
        "es_pct_lo": float(agg["es_pct_lo"]),
        "es_pct_hi": float(agg["es_pct_hi"]),
        "bilat_full": int(bilat_full),
        "n_se_full": int(full_res["n_start_extreme"]) if full_res else 0,
        "n_ee_full": int(full_res["n_end_extreme"]) if full_res else 0,
        "bilat_frac": float(agg["bilat_frac"]),
        "mi_orig": float(agg["mi_orig_mean"]),
        "mi_orig_lo": float(agg["mi_orig_lo"]),
        "mi_orig_hi": float(agg["mi_orig_hi"]),
        "mi_shuf": float(agg.get("mi_shuf_mean", 0.0)),
        "mi_retention_pct": float(agg.get("mi_retention_pct_mean", 0.0)),
        "shape": str(agg["shape"]),
        "zipf_r2": float(agg.get("zipf_r2_mean", 0.0)),
        "cv": float(agg.get("cv_mean", 0.0)),
        "n_words": int(sum(len(s) for s in sents)),
        "n_sents": int(len(sents)),
    }

    # Fixed canonical verifier checks
    fixed_checks = {
        "E->S": 60.0 <= out["es_pct"] <= 85.0,
        "Bilat": out["bilat_full"] == 1,
        "MI": 0.20 <= out["mi_orig"] <= 0.65,
        "Shape_nonPlateau": out["shape"] in ("Zipfian", "Intermediate"),
        "Shape_strictZipf": out["shape"] == "Zipfian",
    }
    out["fixed_pass_4"] = bool(
        fixed_checks["E->S"] and fixed_checks["Bilat"] and fixed_checks["MI"] and fixed_checks["Shape_nonPlateau"]
    )
    out["fixed_pass_strict_zipf"] = bool(
        fixed_checks["E->S"] and fixed_checks["Bilat"] and fixed_checks["MI"] and fixed_checks["Shape_strictZipf"]
    )

    if ref_cal is not None:
        adap_checks, _ = vf.compute_adaptive_checks(agg, bilat_full, ref_cal)
        out["adaptive_checks"] = {k: bool(v) for k, v in adap_checks.items()}
        out["adaptive_pass_4"] = bool(all(adap_checks.values()))
        out["adaptive_pass_strict_zipf"] = bool(all(adap_checks.values()) and out["shape"] == "Zipfian")
    return out


def compute_h2_and_lengths(lines):
    """Compute within-word conditional character entropy h2 and word-length stats."""
    unigram = Counter()
    bigram = Counter()
    lengths = []
    for line in lines:
        for w in line:
            if not w:
                continue
            lengths.append(len(w))
            for ch in w[:-1]:
                unigram[ch] += 1
            for a, b in zip(w, w[1:]):
                bigram[(a, b)] += 1
    total_bi = sum(bigram.values())
    if total_bi == 0:
        return 0.0, 0.0, 0.0
    h2 = 0.0
    for (a, b), cnt in bigram.items():
        p_ab = cnt / total_bi
        p_b_given_a = cnt / unigram[a]
        h2 -= p_ab * math.log2(p_b_given_a)
    arr = np.array(lengths, dtype=float)
    return float(h2), float(arr.mean()), float(arr.std(ddof=1))


def score_p1(lines, shuffles=100, seed=20260816):
    """
    Compute arXiv:2608.17096 edge-glyph coupling MI, entropy share,
    singleton-type rate, within-word h2, and word-length distribution.
    Evaluates both collapsed EVA (primary per Rozanova & Temerev) and raw EVA.
    """
    res = {}
    for mode in ("collapsed", "raw"):
        proc_lines = [
            [collapse_eva(w) if mode == "collapsed" else w.lower() for w in line if w]
            for line in lines
        ]
        proc_lines = [l for l in proc_lines if len(l) >= 2]
        flat = [w for l in proc_lines for w in l]
        freq = Counter(flat)
        n_tokens = len(flat)
        n_types = len(freq)
        n_hapax = sum(1 for c in freq.values() if c == 1)
        singleton_rate = n_hapax / n_types if n_types > 0 else 0.0

        # Feature encoding for last1 -> first1
        line_ids = np.repeat(np.arange(len(proc_lines)), [len(l) for l in proc_lines])
        same_line = line_ids[:-1] == line_ids[1:]

        last_vocab = {}
        first_vocab = {}
        last_codes = np.empty(n_tokens, dtype=np.int64)
        first_codes = np.empty(n_tokens, dtype=np.int64)
        for idx, w in enumerate(flat):
            last_codes[idx] = last_vocab.setdefault(w[-1], len(last_vocab))
            first_codes[idx] = first_vocab.setdefault(w[0], len(first_vocab))
        ny = len(first_vocab)

        def calc_mi(l_idx, r_idx):
            x = last_codes[l_idx]
            y = first_codes[r_idx]
            _, joint = np.unique(x * ny + y, return_counts=True)
            _, cx = np.unique(x, return_counts=True)
            _, cy = np.unique(y, return_counts=True)
            def ent(c):
                p = c.astype(float) / c.sum()
                return float(-(p * np.log2(p)).sum())
            return ent(cx) + ent(cy) - ent(joint)

        positions = np.arange(n_tokens)
        obs_l = positions[:-1][same_line]
        obs_r = positions[1:][same_line]
        obs_mi = calc_mi(obs_l, obs_r)

        # Marginal entropy H(first1) over all tokens
        c_first = np.bincount(first_codes).astype(float)
        c_first = c_first[c_first > 0]
        p_first = c_first / c_first.sum()
        h_first = float(-(p_first * np.log2(p_first)).sum())

        rng = np.random.default_rng(seed)
        null_mis = np.empty(shuffles)
        for s in range(shuffles):
            keys = rng.random(n_tokens)
            perm = np.lexsort((keys, line_ids))
            null_mis[s] = calc_mi(perm[:-1][same_line], perm[1:][same_line])

        shuf_mean = float(null_mis.mean())
        excess_mi = obs_mi - shuf_mean
        share = excess_mi / h_first if h_first > 0 else 0.0
        h2, wl_mean, wl_sd = compute_h2_and_lengths(proc_lines)

        res[mode] = {
            "n_tokens": int(n_tokens),
            "n_types": int(n_types),
            "singleton_rate": float(singleton_rate),
            "obs_edge_mi": float(obs_mi),
            "shuf_edge_mi": float(shuf_mean),
            "excess_edge_mi": float(excess_mi),
            "edge_share": float(share),
            "h_first": float(h_first),
            "h2": float(h2),
            "word_len_mean": float(wl_mean),
            "word_len_sd": float(wl_sd),
        }
    return res


def page_bootstrap_envelopes(by_folio, n_boot=2000, seed=20261023):
    """Compute 95% and 99.9% page-level bootstrap envelopes for p1 metrics."""
    folios = sorted(by_folio.keys())
    n_folios = len(folios)
    rng = np.random.default_rng(seed)

    # Precompute per-folio token statistics to speed up 2,000 bootstrap draws
    # For each folio, store its lines (collapsed and raw)
    folio_collapsed = {}
    folio_raw = {}
    for f in folios:
        folio_collapsed[f] = [[collapse_eva(w) for w in line if w] for line in by_folio[f]]
        folio_raw[f] = [[w.lower() for w in line if w] for line in by_folio[f]]

    metrics = defaultdict(list)
    for b in range(n_boot):
        sampled = rng.choice(folios, size=n_folios, replace=True)
        lines_c = [line for f in sampled for line in folio_collapsed[f]]
        lines_r = [line for f in sampled for line in folio_raw[f]]

        # Fast excess MI & singleton on collapsed
        flat_c = [w for l in lines_c for w in l]
        freq_c = Counter(flat_c)
        sing_c = sum(1 for v in freq_c.values() if v == 1) / len(freq_c)

        # Fast edge MI with analytical/5-shuffle mean
        sc = score_p1(lines_r, shuffles=10, seed=seed + b)
        for mode in ("collapsed", "raw"):
            for k in ("excess_edge_mi", "edge_share", "singleton_rate", "h2", "word_len_mean", "word_len_sd"):
                metrics[f"{mode}_{k}"].append(sc[mode][k])

    envelopes = {}
    for k, vals in metrics.items():
        arr = np.array(vals, dtype=float)
        envelopes[k] = {
            "mean": float(arr.mean()),
            "sd": float(arr.std(ddof=1)),
            "p2.5": float(np.percentile(arr, 2.5)),
            "p50": float(np.percentile(arr, 50.0)),
            "p97.5": float(np.percentile(arr, 97.5)),
            "p0.05": float(np.percentile(arr, 0.05)),
            "p99.95": float(np.percentile(arr, 99.95)),
        }
    return envelopes


def wrap_words_to_template(words, template_lines):
    """Wrap a flat list of words to match the exact line lengths of template_lines."""
    needed = sum(len(l) for l in template_lines)
    if len(words) < needed:
        # Cycle if shorter
        reps = (needed // max(len(words), 1)) + 2
        words = (words * reps)[:needed]
    out = []
    idx = 0
    for l in template_lines:
        k = len(l)
        out.append(words[idx:idx + k])
        idx += k
    return out


# ============================================================================
# 3. Main Calibration & Audit Routine
# ============================================================================

def main():
    t0 = time.time()
    report = {
        "reference_p2": {},
        "reference_p1": {},
        "envelopes_p1": {},
        "published_generators_audit": {},
        "s5_bug_audit": {},
        "chunk_size_audit": {},
    }

    # --- Step 1: Calibrate Reference Manuscripts on p2 and p1 ---
    for ms_name, ms_file in [
        ("RF1b-e", DATA / "RF1b-e.txt"),
        ("ZL3b", DATA / "ZL3b-n.txt"),
        ("IT2a", DATA / "IT2a-n.txt"),
    ]:
        print(f"[1] Calibrating {ms_name} ({ms_file.name})...", flush=True)
        # Raw parse_manuscript from Parisel
        raw_folios, raw_all = vf.parse_manuscript(str(ms_file))
        # Clean IVTFF parser (strips <%> and <$> so ZL3b/IT2a don't lose para edges)
        clean_p2, clean_p1, meta = parse_ivtff_clean(ms_file)

        for lang in ("A", "B"):
            cell = f"{lang}/{ms_name}"
            raw_sents = vf.get_sentences_for_language(raw_folios, raw_all, lang)
            clean_sents_p2, by_folio_p2 = get_dialect_lines(clean_p2, meta, lang, use_parisel_map=True)
            clean_sents_p1, by_folio_p1 = get_dialect_lines(clean_p1, meta, lang, use_parisel_map=False)

            ref_raw = score_p2(raw_sents)
            ref_clean = score_p2(clean_sents_p2)
            # Self-check adaptive thresholds
            ref_clean = score_p2(clean_sents_p2, ref_cal=ref_clean)
            ref_raw = score_p2(raw_sents, ref_cal=ref_raw)

            report["reference_p2"][cell] = {
                "clean_ivtff": ref_clean,
                "raw_parisel_parser": ref_raw,
            }
            print(
                f"  {cell} (clean): words={ref_clean['n_words']}, E->S={ref_clean['es_pct']:.1f}%, "
                f"Bilat={ref_clean['bilat_full']} ({ref_clean['n_se_full']}/{ref_clean['n_ee_full']}), "
                f"MI={ref_clean['mi_orig']:.4f}, Shape={ref_clean['shape']} "
                f"(R2={ref_clean['zipf_r2']:.3f}, CV={ref_clean['cv']:.2f})",
                flush=True,
            )

            if ms_name in ("ZL3b", "IT2a"):
                p1_val = score_p1(clean_sents_p1, shuffles=100)
                report["reference_p1"][cell] = p1_val
                print(
                    f"  {cell} (p1 collapsed): tokens={p1_val['collapsed']['n_tokens']}, "
                    f"excess_MI={p1_val['collapsed']['excess_edge_mi']:.4f} "
                    f"(share={100*p1_val['collapsed']['edge_share']:.2f}%), "
                    f"singleton={p1_val['collapsed']['singleton_rate']:.4f}, "
                    f"h2={p1_val['collapsed']['h2']:.4f}, len={p1_val['collapsed']['word_len_mean']:.2f}",
                    flush=True,
                )
                # 500-draw fast page bootstrap for reference envelopes in reader (2000 in full gate)
                env = page_bootstrap_envelopes(by_folio_p1, n_boot=500, seed=20261023)
                report["envelopes_p1"][cell] = env

    # --- Step 2: Audit Published Slot Generator (signatures_v27.py) ---
    print("\n[2] Auditing published Slot-Based Generator (signatures_v27.py)...", flush=True)
    slot_audit = {}
    for n_words_mode in ("37000", "template_A_ZL3b", "template_B_ZL3b"):
        sents_list = []
        p2_scores_A_ZL = []
        p2_scores_B_ZL = []
        p2_scores_A_IT = []
        p2_scores_B_IT = []
        p1_scores_A_ZL = []
        for s in range(10):
            cfg = ev.cfg_baseline(n_words=37000)
            sents = cfg.generate(seed=42 + s)
            if n_words_mode == "template_A_ZL3b":
                clean_p2, _, meta = parse_ivtff_clean(DATA / "ZL3b-n.txt")
                tmpl, _ = get_dialect_lines(clean_p2, meta, "A")
                flat_w = [w for line in sents for w in line]
                sents = wrap_words_to_template(flat_w, tmpl)
            elif n_words_mode == "template_B_ZL3b":
                clean_p2, _, meta = parse_ivtff_clean(DATA / "ZL3b-n.txt")
                tmpl, _ = get_dialect_lines(clean_p2, meta, "B")
                flat_w = [w for line in sents for w in line]
                sents = wrap_words_to_template(flat_w, tmpl)

            p2_scores_A_ZL.append(score_p2(sents, ref_cal=report["reference_p2"]["A/ZL3b"]["clean_ivtff"]))
            p2_scores_B_ZL.append(score_p2(sents, ref_cal=report["reference_p2"]["B/ZL3b"]["clean_ivtff"]))
            p2_scores_A_IT.append(score_p2(sents, ref_cal=report["reference_p2"]["A/IT2a"]["clean_ivtff"]))
            p2_scores_B_IT.append(score_p2(sents, ref_cal=report["reference_p2"]["B/IT2a"]["clean_ivtff"]))
            if s < 3:
                p1_scores_A_ZL.append(score_p1(sents, shuffles=20)["collapsed"])

        slot_audit[n_words_mode] = {
            "es_pct_mean": float(np.mean([x["es_pct"] for x in p2_scores_A_ZL])),
            "mi_orig_mean": float(np.mean([x["mi_orig"] for x in p2_scores_A_ZL])),
            "bilat_full_rate": float(np.mean([x["bilat_full"] for x in p2_scores_A_ZL])),
            "shapes": dict(Counter(x["shape"] for x in p2_scores_A_ZL)),
            "pass_rate_A_ZL3b_adaptive": float(np.mean([x["adaptive_pass_4"] for x in p2_scores_A_ZL])),
            "pass_rate_B_ZL3b_adaptive": float(np.mean([x["adaptive_pass_4"] for x in p2_scores_B_ZL])),
            "pass_rate_A_IT2a_adaptive": float(np.mean([x["adaptive_pass_4"] for x in p2_scores_A_IT])),
            "pass_rate_B_IT2a_adaptive": float(np.mean([x["adaptive_pass_4"] for x in p2_scores_B_IT])),
            "pass_rate_fixed_strict_zipf": float(np.mean([x["fixed_pass_strict_zipf"] for x in p2_scores_A_ZL])),
            "p1_singleton_mean": float(np.mean([x["singleton_rate"] for x in p1_scores_A_ZL])),
            "p1_excess_mi_mean": float(np.mean([x["excess_edge_mi"] for x in p1_scores_A_ZL])),
        }
        print(f"  Slot ({n_words_mode}): E->S={slot_audit[n_words_mode]['es_pct_mean']:.1f}%, "
              f"MI={slot_audit[n_words_mode]['mi_orig_mean']:.4f}, "
              f"pass_A_ZL={slot_audit[n_words_mode]['pass_rate_A_ZL3b_adaptive']*100:.0f}%, "
              f"pass_B_ZL={slot_audit[n_words_mode]['pass_rate_B_ZL3b_adaptive']*100:.0f}%, "
              f"pass_fixed={slot_audit[n_words_mode]['pass_rate_fixed_strict_zipf']*100:.0f}%", flush=True)
    report["published_generators_audit"]["slot_generator"] = slot_audit

    # --- Step 3: Audit Published Cardan Grille Generator (grille.py) ---
    print("\n[3] Auditing published Cardan-Grille Generator (grille.py)...", flush=True)
    grille_audit = {}
    for g_mode in ("G0_SPLIT_RANDOM", "G1_SPLIT_SHIFT", "G2_SPLIT_ROTATE", "G6_WEIGHTED_ROWS"):
        scores = []
        for s in range(10):
            rng = random.Random(100 + s)
            table = gr.build_table(36, 9, specialisation="SPLIT", blank_prob=0.2, col_skew=1.2, rng=rng)
            if g_mode == "G0_SPLIT_RANDOM":
                words = gr.generate_corpus_random(table, 9, 3, 15000, rng)
            elif g_mode == "G1_SPLIT_SHIFT":
                words = gr.generate_corpus_shift(table, 9, 3, 15000, rng)
            elif g_mode == "G2_SPLIT_ROTATE":
                words = gr.generate_corpus_rotate(table, 9, 3, 15000, rng)
            else:
                words = gr.generate_corpus_weighted_rows(
                    table, 9, 3, 15000, rng, boundary_pairs=ev.DEFAULT_BOUNDARY_PAIRS, pair_strength=5.0
                )
            sents = vf.words_to_sentences(words, seed=100 + s)
            scores.append(score_p2(sents, ref_cal=report["reference_p2"]["A/ZL3b"]["clean_ivtff"]))
        grille_audit[g_mode] = {
            "es_pct_mean": float(np.mean([x["es_pct"] for x in scores])),
            "mi_orig_mean": float(np.mean([x["mi_orig"] for x in scores])),
            "cv_mean": float(np.mean([x["cv"] for x in scores])),
            "r2_mean": float(np.mean([x["zipf_r2"] for x in scores])),
            "shapes": dict(Counter(x["shape"] for x in scores)),
            "pass_rate_A_ZL3b_adaptive": float(np.mean([x["adaptive_pass_4"] for x in scores])),
            "pass_rate_fixed_strict_zipf": float(np.mean([x["fixed_pass_strict_zipf"] for x in scores])),
        }
        print(f"  Grille ({g_mode}): E->S={grille_audit[g_mode]['es_pct_mean']:.1f}%, "
              f"MI={grille_audit[g_mode]['mi_orig_mean']:.4f}, CV={grille_audit[g_mode]['cv_mean']:.3f}, "
              f"shapes={grille_audit[g_mode]['shapes']}, pass={grille_audit[g_mode]['pass_rate_A_ZL3b_adaptive']*100:.0f}%",
              flush=True)
    report["published_generators_audit"]["cardan_grille"] = grille_audit

    # --- Step 4: Audit Unmodified Naibbe (naibbe.py) on p2 and p1 ---
    print("\n[4] Auditing Unmodified Naibbe Cipher (naibbe.py)...", flush=True)
    orig_cwd = Path.cwd()
    os.chdir(DATA / "author")
    spec = importlib.util.spec_from_file_location("naibbe_author", DATA / "author" / "naibbe.py")
    naibbe_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(naibbe_mod)
    os.chdir(orig_cwd)

    clean_p2_zl, clean_p1_zl, meta_zl = parse_ivtff_clean(DATA / "ZL3b-n.txt")
    tmpl_A_zl, _ = get_dialect_lines(clean_p2_zl, meta_zl, "A")
    tmpl_B_zl, _ = get_dialect_lines(clean_p2_zl, meta_zl, "B")

    pt_files = [DATA / "plaintexts" / f"{lang}-{i:02d}.txt" for lang in ("Latin", "Italian") for i in range(10)]
    naibbe_p2_A = []
    naibbe_p2_B = []
    naibbe_p1_A = []
    for i, ptf in enumerate(pt_files):
        text = ptf.read_text(encoding="utf-8")
        cleaned = naibbe_mod.clean_line(text)
        # Run 2 seeds per plaintext in reader audit (40 streams) for fast calibration; full 200 in statistician/cipher
        for s in range(2):
            random.seed(202610190000 + 100 * i + s)
            toks = naibbe_mod.encrypt_naibbe(
                cleaned, naibbe_mod.naibbe_tables, naibbe_mod.placeholder_to_glyph, use_78=False
            )
            respaced_line = naibbe_mod.respace_line(" ".join(toks), naibbe_mod.SPACE_REMOVAL_RATE)
            resp_toks = respaced_line.split()
            sents_A = wrap_words_to_template(resp_toks, tmpl_A_zl)
            sents_B = wrap_words_to_template(resp_toks, tmpl_B_zl)
            naibbe_p2_A.append(score_p2(sents_A, ref_cal=report["reference_p2"]["A/ZL3b"]["clean_ivtff"]))
            naibbe_p2_B.append(score_p2(sents_B, ref_cal=report["reference_p2"]["B/ZL3b"]["clean_ivtff"]))
            if s == 0 and i < 6:
                naibbe_p1_A.append(score_p1(sents_A, shuffles=20)["collapsed"])

    report["published_generators_audit"]["naibbe_unmodified"] = {
        "n_streams_tested": len(naibbe_p2_A),
        "A_ZL3b": {
            "es_pct_mean": float(np.mean([x["es_pct"] for x in naibbe_p2_A])),
            "mi_orig_mean": float(np.mean([x["mi_orig"] for x in naibbe_p2_A])),
            "bilat_full_rate": float(np.mean([x["bilat_full"] for x in naibbe_p2_A])),
            "shapes": dict(Counter(x["shape"] for x in naibbe_p2_A)),
            "pass_rate_adaptive": float(np.mean([x["adaptive_pass_4"] for x in naibbe_p2_A])),
            "pass_rate_fixed": float(np.mean([x["fixed_pass_strict_zipf"] for x in naibbe_p2_A])),
        },
        "B_ZL3b": {
            "es_pct_mean": float(np.mean([x["es_pct"] for x in naibbe_p2_B])),
            "mi_orig_mean": float(np.mean([x["mi_orig"] for x in naibbe_p2_B])),
            "bilat_full_rate": float(np.mean([x["bilat_full"] for x in naibbe_p2_B])),
            "shapes": dict(Counter(x["shape"] for x in naibbe_p2_B)),
            "pass_rate_adaptive": float(np.mean([x["adaptive_pass_4"] for x in naibbe_p2_B])),
            "pass_rate_fixed": float(np.mean([x["fixed_pass_strict_zipf"] for x in naibbe_p2_B])),
        },
        "p1_A_ZL3b_sample": {
            "excess_edge_mi_mean": float(np.mean([x["excess_edge_mi"] for x in naibbe_p1_A])),
            "singleton_rate_mean": float(np.mean([x["singleton_rate"] for x in naibbe_p1_A])),
            "h2_mean": float(np.mean([x["h2"] for x in naibbe_p1_A])),
        },
    }
    print(f"  Naibbe (A/ZL3b): E->S={report['published_generators_audit']['naibbe_unmodified']['A_ZL3b']['es_pct_mean']:.1f}%, "
          f"MI={report['published_generators_audit']['naibbe_unmodified']['A_ZL3b']['mi_orig_mean']:.4f}, "
          f"pass={report['published_generators_audit']['naibbe_unmodified']['A_ZL3b']['pass_rate_adaptive']*100:.0f}%",
          flush=True)

    # --- Step 5: Audit S5 Bug in signatures_v27.py ---
    print("\n[5] Auditing S5 boundary pair_strength override bug in signatures_v27.py...", flush=True)
    s5_buggy = {}
    s5_fixed = {}
    pairs_2tuple = [(e, s) for (e, s, _) in ev.DEFAULT_BOUNDARY_PAIRS]
    for ps in (1.0, 5.0, 10.0, 20.0, 50.0):
        cfg_b = ev.cfg_baseline(n_words=15000)
        cfg_b.pair_strength = ps  # overridden by 3-tuples in DEFAULT_BOUNDARY_PAIRS!
        sents_b = cfg_b.generate(seed=42)
        sc_b = score_p2(sents_b)
        s5_buggy[str(ps)] = {"es_pct": sc_b["es_pct"], "mi_orig": sc_b["mi_orig"]}

        cfg_f = ev.cfg_baseline(n_words=15000)
        cfg_f.boundary_pairs = pairs_2tuple
        cfg_f.pair_strength = ps
        sents_f = cfg_f.generate(seed=42)
        sc_f = score_p2(sents_f)
        s5_fixed[str(ps)] = {"es_pct": sc_f["es_pct"], "mi_orig": sc_f["mi_orig"]}
    report["s5_bug_audit"] = {"buggy_3tuple_override": s5_buggy, "fixed_2tuple_sweep": s5_fixed}
    print("  S5 buggy MI across ps=(1,5,10,20,50):", [v["mi_orig"] for v in s5_buggy.values()], flush=True)
    print("  S5 fixed MI across ps=(1,5,10,20,50):", [round(v["mi_orig"], 4) for v in s5_fixed.values()], flush=True)

    out_path = JOB_OUT / "reference_calibration.json"
    out_path.write_text(json.dumps(report, indent=2))
    print(f"\nSaved calibration and audit to {out_path} in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
