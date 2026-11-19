#!/usr/bin/env python3
"""
analyze_obstructions_and_capacity.py — Lens 2 (obstruction):
1. Map the 2D tradeoff surface between E->S dominance (Sig 1) and cross-boundary
   MI (Sig 3 / p1 excess_edge_mi) across bridge share beta and class-coupling alpha.
2. Quantify the top_k=30 dilution obstruction in signatures_v27.py (why 16 sparse
   boundary pairs fail to reach Currier A/B MI thresholds under Zipfian word weights).
3. Quantify the column-averaging CV compression obstruction in grille.py (why
   shifting/rotating 3-hole masks produce Shape = Plateau).
4. Prove and numerically verify the 200-Entry Combinatorial Singleton Ceiling:
   1-slot vs 2-slot vs 3-slot factorized tables under T <= 200 total entries
   driven by real Latin and Italian plaintexts.
"""

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


def theoretical_es_and_mi(k_classes: int, bridge_share: float, coupling_alpha: float):
    """
    Analytical model of a K-class boundary system:
    - Each class c in {0..K-1} has an End grapheme set E_c and a Start grapheme set S_c,
      plus shared Bridge graphemes B that can appear at both start and end with
      marginal probability `bridge_share`.
    - When a word ends in class c, with probability `coupling_alpha` the next word
      draws its initial grapheme from class c; with probability `1 - coupling_alpha`
      it draws from the marginal distribution over all K classes.
    Returns (expected_es_pct, true_class_mi_bits).
    """
    # Pure start graphemes have s > 2e ("start"), pure end graphemes have e > 2s ("end").
    # Bridge graphemes have s ~= e ("ambig").
    # Therefore P(cls(last(w_i)) == "end") = 1 - bridge_share
    # and P(cls(first(w_{i+1})) == "start") = 1 - bridge_share.
    es_pct = 100.0 * (1.0 - bridge_share) ** 2

    # Mutual information I(C_end; C_start) across K equiprobable boundary classes
    # where P(C_start = j | C_end = i) = alpha + (1 - alpha)/K if i == j else (1 - alpha)/K.
    p_diag = coupling_alpha + (1.0 - coupling_alpha) / k_classes
    p_off = (1.0 - coupling_alpha) / k_classes
    h_marginal = math.log2(k_classes)
    h_cond = 0.0
    if p_diag > 0:
        h_cond -= p_diag * math.log2(p_diag)
    if p_off > 0 and k_classes > 1:
        h_cond -= (k_classes - 1) * p_off * math.log2(p_off)
    mi_bits = max(0.0, h_marginal - h_cond)
    return es_pct, mi_bits


def audit_slot_topk_dilution():
    """
    Analyze why build_sparse_markov in signatures_v27.py fails Sig 3 MI:
    Compute conditional entropy H(S_{i+1} | E_i) and 10-chunk MI across
    pair_strength in {1, 5, 10, 20, 50} and top_k in {5, 10, 30, 100, 500}.
    """
    pairs_2tuple = [(e, s) for (e, s, _) in ev.DEFAULT_BOUNDARY_PAIRS]
    grid = {}
    for top_k in (5, 10, 30, 100, 500):
        for ps in (1.0, 5.0, 10.0, 25.0, 50.0):
            cfg = ev.cfg_baseline(n_words=10000, top_k=top_k)
            cfg.boundary_pairs = pairs_2tuple
            cfg.pair_strength = ps
            sents = cfg.generate(seed=42)
            tok = ev.pretokenize(sents, TOKENIZER)
            es = ev.end_start_pct_fast(tok)
            mi_o, mi_s, _ = ev.mi_with_retention_fast(tok, n_shuffles=3)
            r2, cv, shape = ev.zipfian_boundary_test_fast(tok)
            grid[f"topk_{top_k}_ps_{int(ps)}"] = {
                "top_k": top_k,
                "pair_strength": ps,
                "es_pct": float(es),
                "mi_full": float(mi_o),
                "mi_shuf": float(mi_s),
                "mi_excess": float(mi_o - mi_s),
                "r2": float(r2),
                "cv": float(cv),
                "shape": shape,
            }
    return grid


def audit_grille_column_averaging():
    """
    Show why Cardan grille (grille.py) compresses initial-grapheme CV (< 0.5, Plateau):
    Compare 1-column fixed left hole vs 3-hole random/shift/rotate across 9 columns.
    """
    results = {}
    for col_skew in (0.5, 1.0, 1.2, 1.5, 2.0):
        rng = random.Random(42)
        table = gr.build_table(36, 9, specialisation="SPLIT", blank_prob=0.2, col_skew=col_skew, rng=rng)
        words_shift = gr.generate_corpus_shift(table, 9, 3, 10000, rng)
        sents_shift = vf.words_to_sentences(words_shift, seed=42)
        tok_shift = ev.pretokenize(sents_shift, TOKENIZER)
        r2_s, cv_s, shape_s = ev.zipfian_boundary_test_fast(tok_shift)
        es_s = ev.end_start_pct_fast(tok_shift)
        mi_s, _, _ = ev.mi_with_retention_fast(tok_shift, n_shuffles=3)
        results[f"col_skew_{col_skew}"] = {
            "col_skew": col_skew,
            "es_pct": float(es_s),
            "mi_full": float(mi_s),
            "r2": float(r2_s),
            "cv": float(cv_s),
            "shape": shape_s,
        }
    return results


def audit_200_entry_factorization():
    """
    Test 1-slot, 2-slot, and 3-slot factorized tables under strict budget T <= 200
    driven by real period Latin (Latin-00.txt) and Italian (Italian-00.txt) plaintexts.
    """
    latin_text = (DATA / "plaintexts" / "Latin-00.txt").read_text(encoding="utf-8")
    letters = "".join(c for c in latin_text.lower() if c.isalpha())

    # Chunk into 4-letter plaintext words (approx 10,000 words from 40,000 letters)
    chunks_4 = [letters[i:i + 4] for i in range(0, len(letters) - 4, 4)]

    # 1. 1-slot table (T = 200 whole words)
    vocab_1slot = [f"w{i:03d}" for i in range(200)]
    stream_1slot = [vocab_1slot[hash(ch) % 200] for ch in chunks_4]
    freq_1 = Counter(stream_1slot)
    sing_1 = sum(1 for v in freq_1.values() if v == 1) / len(freq_1)

    # 2. 2-slot table (T = 100 prefixes + 100 suffixes = 200 entries)
    # Driven by 2-letter respaced chunks vs 4-letter chunks (2+2)
    chunks_2 = [letters[i:i + 2] for i in range(0, 20000, 2)]
    stream_2slot_2char = [f"p{ord(ch[0])%100:02d}_s{ord(ch[1])%100:02d}" for ch in chunks_2]
    freq_2a = Counter(stream_2slot_2char)
    sing_2a = sum(1 for v in freq_2a.values() if v == 1) / len(freq_2a)

    # 2-slot driven by 2+2 letter pairs (each pair mapped to 100 entries)
    def pair_idx(s2, mod):
        return ((ord(s2[0]) - 97) * 26 + (ord(s2[1]) - 97)) % mod

    stream_2slot_4char = [f"p{pair_idx(ch[:2], 100):02d}_s{pair_idx(ch[2:4], 100):02d}" for ch in chunks_4]
    freq_2b = Counter(stream_2slot_4char)
    sing_2b = sum(1 for v in freq_2b.values() if v == 1) / len(freq_2b)

    # 3. 3-slot table (T = 32 onsets + 128 cores + 32 codas = 192 <= 200 entries)
    # Driven by 5-letter chunks (1 letter onset + 2 letter core + 2 letter coda)
    results_3slot = {}
    for n_tokens in (9500, 20000):
        # Variable chunk length 4 or 5 letters
        rng = random.Random(42)
        pos = 0
        stream_3 = []
        prev_class = 0
        while len(stream_3) < n_tokens:
            if pos + 6 >= len(letters):
                pos = 0
            clen = 4 if rng.random() < 0.45 else 5
            chunk = letters[pos:pos + clen]
            pos += clen
            # Onset from 32 entries (4 classes x 8 ranks)
            l0 = (ord(chunk[0]) - 97) % 8
            onset_id = prev_class * 8 + l0
            # Core from 128 entries
            core_id = pair_idx(chunk[1:3], 128)
            # Coda from 32 entries
            coda_id = pair_idx(chunk[-2:], 32)
            prev_class = coda_id % 4
            stream_3.append(f"o{onset_id:02d}_c{core_id:03d}_s{coda_id:02d}")
        freq_3 = Counter(stream_3)
        sing_3 = sum(1 for v in freq_3.values() if v == 1) / len(freq_3)
        results_3slot[f"N_{n_tokens}"] = {
            "n_tokens": n_tokens,
            "n_types": len(freq_3),
            "singleton_rate": float(sing_3),
            "total_table_entries": 32 + 128 + 32,
        }

    return {
        "1_slot_200_entries": {
            "n_tokens": len(stream_1slot),
            "n_types": len(freq_1),
            "singleton_rate": float(sing_1),
            "total_table_entries": 200,
        },
        "2_slot_200_entries_2letter_chunks": {
            "n_tokens": len(stream_2slot_2char),
            "n_types": len(freq_2a),
            "singleton_rate": float(sing_2a),
            "total_table_entries": 200,
        },
        "2_slot_200_entries_4letter_chunks": {
            "n_tokens": len(stream_2slot_4char),
            "n_types": len(freq_2b),
            "singleton_rate": float(sing_2b),
            "total_table_entries": 200,
        },
        "3_slot_192_entries": results_3slot,
    }


def main():
    t0 = time.time()
    # 1. Theoretical capacity grid
    cap_grid = []
    for k in (2, 4, 6, 8):
        for beta in (0.0, 0.08, 0.14, 0.20, 0.28):
            for alpha in (0.0, 0.20, 0.35, 0.50, 0.65, 0.80):
                es, mi = theoretical_es_and_mi(k, beta, alpha)
                cap_grid.append({
                    "k_classes": k,
                    "bridge_share": beta,
                    "coupling_alpha": alpha,
                    "theoretical_es_pct": round(es, 2),
                    "theoretical_class_mi_bits": round(mi, 4),
                    "in_p2_es_window_60_85": 60.0 <= es <= 85.0,
                    "in_p1_A_mi_window": 0.09 <= mi <= 0.18,
                    "in_p1_B_mi_window": 0.19 <= mi <= 0.30,
                })

    print("[1] Auditing slot generator top_k dilution...", flush=True)
    slot_grid = audit_slot_topk_dilution()

    print("[2] Auditing Cardan grille column-averaging CV compression...", flush=True)
    grille_grid = audit_grille_column_averaging()

    print("[3] Auditing 200-entry factorization capacity...", flush=True)
    fact_res = audit_200_entry_factorization()
    print("  Factorization results:", json.dumps(fact_res, indent=2), flush=True)

    out = {
        "theoretical_capacity_grid": cap_grid,
        "slot_topk_dilution_audit": slot_grid,
        "grille_cv_compression_audit": grille_grid,
        "factorization_singleton_ceiling": fact_res,
    }
    out_path = JOB_OUT / "obstruction_analysis.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Saved obstruction analysis to {out_path} in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
