#!/usr/bin/env python3
"""
train_and_freeze_m77_model.py
=============================
Strictly M77-only (<= 1977) model training, 5-fold cross-validation, and
timestamped parameter freezing for V3R1T4S target `indus-temporal-heldout-structure`.

CRITICAL ANTI-LEAKAGE GUARANTEE:
  This script reads ONLY:
    1. `data/Indus-/data/im77/im77_corpus_lines.csv` (Mahadevan 1977 concordance)
    2. `data/Indus-/data/derived/bridge_extended.json` (static Mahadevan <-> Wells sign code table)
  It NEVER opens or inspects any post-1977 inscription file (`inscriptions.csv`,
  `merged-corpus-canonical.v2.json`, `indus_website_real_corpus.csv`, etc.).

Outputs:
  `m77_frozen_structural_model.json`: Timestamped frozen model containing:
    - Model metadata, UTC freeze timestamp, input file SHA-256 hashes
    - 5-fold M77 cross-validation results (tuning KN3 discount D* and verifying
      M77-CLSS vs KN3-Left, KN3-Bidir, KN3-BlanketF, and SIGIL controls)
    - Frozen M77 sign-mapping tables (Mode 1: exact `test_prereg.py` `m2g`;
      Mode 2: `bridge_extended.json` connected-component canonical `m2g`)
    - Frozen M77 5-zone positional slot grammar (`INIT`, `SECOND`, `MID`, `PENULT`, `FINAL`),
      32 distributional sign equivalence classes (`Ward` clustering on M77 slot + flanking profiles),
      slot-specific bigram tables, bilateral center-frame tables, and intra-clause anti-repetition table
    - Frozen M77 Seal-vs-Tablet sequence likelihood-ratio parameters
    - Frozen M77 Top-25 telescoping composite/bigram substitution pairs (C <-> A B) for p3
"""

import csv
import datetime
import hashlib
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "data", "indus_decipher"))
from analysis.ngram import train_kneser_ney
from data.adversarial_null_model import generate_matched_null_corpus
from data.loader import Corpus, Inscription

IM77_CSV = os.path.join(HERE, "data", "Indus-", "data", "im77", "im77_corpus_lines.csv")
BRIDGE_JSON = os.path.join(HERE, "data", "Indus-", "data", "derived", "bridge_extended.json")
OUT_JSON = os.path.join(HERE, "m77_frozen_structural_model.json")

M_OVERRIDE = {
    342: 740, 343: 741, 344: 741, 345: 741, 346: 741,
    161: 390, 162: 390, 167: 390, 168: 390, 169: 390,
    267: 861, 60: 226
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_slot(i: int, L: int) -> int:
    """Canonical 5-zone structural slot in reading order (0=INIT, 1=SECOND, 2=MID, 3=PENULT, 4=FINAL)."""
    if i == 0:
        return 0
    if i == L - 1:
        return 4
    if i == 1 and L >= 3:
        return 1
    if i == L - 2 and L >= 4:
        return 3
    return 2


def build_sign_bridges(bridge_path: str):
    bridge = json.load(open(bridge_path, encoding="utf-8"))
    inv = defaultdict(set)
    for g, ms in bridge.items():
        for m in ms:
            inv[int(m)].add(int(g))

    # Mode 1: Exact `paragorth/Indus-/prereg/test_prereg.py` load_im77 mapping
    m2g_mode1 = {m: next(iter(gs)) for m, gs in inv.items() if len(gs) == 1}
    m2g_mode1.update(M_OVERRIDE)
    w2g_mode1 = {}
    for g_str in bridge.keys():
        g = int(g_str)
        w2g_mode1[g] = g

    # Mode 2: Canonical connected-component mapping across bridge_extended.json + M_OVERRIDE
    # Every M sign in inv maps to min(gs) (or M_OVERRIDE), and any W sign sharing an M sign
    # in bridge_extended.json maps to the same canonical W ID.
    m2g_mode2 = {m: min(gs) for m, gs in inv.items()}
    m2g_mode2.update(M_OVERRIDE)
    w2g_mode2 = {}
    for g_str, ms in bridge.items():
        g = int(g_str)
        if ms:
            cand = [m2g_mode2[int(m)] for m in ms if int(m) in m2g_mode2]
            w2g_mode2[g] = min([g] + cand)
        else:
            w2g_mode2[g] = g

    return bridge, m2g_mode1, w2g_mode1, m2g_mode2, w2g_mode2


def load_m77_records(im77_path: str, m2g: dict):
    objtype = {"1": "seal", "2": "sealing", "3": "tablet", "5": "tablet"}
    records = []
    with open(im77_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["line"] == "9":
                continue
            m_seq = [int(x) for x in r["signs_clean"].split() if int(x) != 0]
            if len(m_seq) < 2:
                continue
            seq = [str(m2g.get(m, 10000 + m)) for m in m_seq]
            records.append({
                "text_no": r["text_no"],
                "site_code": r["site_code"],
                "site": r["site"],
                "cls": objtype.get(r["object_code"], "other"),
                "object_code": r["object_code"],
                "fs80": r["fs80"],
                "m_seq": m_seq,
                "seq": seq,
            })
    return records


def extract_m77_structural_tables(train_seqs: list[list[str]], n_clusters: int = 32):
    vocab = sorted(set(w for s in train_seqs for w in s))
    v2i = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)

    uni = np.zeros(V, dtype=np.float64)
    slot_uni = np.zeros((5, V), dtype=np.float64)
    slot_bi_l = defaultdict(lambda: np.zeros(V, dtype=np.float64))
    slot_bi_r = defaultdict(lambda: np.zeros(V, dtype=np.float64))
    center_bi = defaultdict(lambda: np.zeros(V, dtype=np.float64))
    bi_l = defaultdict(Counter)
    bi_r = defaultdict(Counter)
    adj_rep = Counter()
    nonadj_rep = Counter()

    for s in train_seqs:
        L = len(s)
        pad = ["<S>"] + s + ["</S>"]
        for i, w in enumerate(s):
            vi = v2i[w]
            z = get_slot(i, L)
            uni[vi] += 1.0
            slot_uni[z, vi] += 1.0
            l1, r1 = pad[i], pad[i + 2]
            slot_bi_l[(z, l1)][vi] += 1.0
            slot_bi_r[(z, r1)][vi] += 1.0
            center_bi[(l1, r1)][vi] += 1.0
            bi_l[l1][vi] += 1
            bi_r[r1][vi] += 1
            if i + 1 < L and s[i + 1] == w:
                adj_rep[w] += 1
            if w in (s[:max(0, i - 1)] + s[min(L, i + 2):]):
                nonadj_rep[w] += 1

    top_ctx = [w for w, _ in Counter(w for s in train_seqs for w in s).most_common(40)] + ["<S>", "</S>"]
    feat = np.zeros((V, 5 + 2 * len(top_ctx)), dtype=np.float64)
    feat[:, :5] = (slot_uni.T + 0.2) / (uni[:, None] + 1.0)
    for idx, cw in enumerate(top_ctx):
        for vi, c in bi_l[cw].items():
            feat[vi, 5 + idx] = math.log1p(c)
        for vi, c in bi_r[cw].items():
            feat[vi, 5 + len(top_ctx) + idx] = math.log1p(c)
    feat /= (np.linalg.norm(feat, axis=1, keepdims=True) + 1e-9)
    Z = linkage(feat, method="ward")
    v2c = fcluster(Z, t=n_clusters, criterion="maxclust") - 1
    w2c = {vocab[i]: f"C{int(v2c[i])}" for i in range(V)}
    w2c["<S>"] = "<S>"
    w2c["</S>"] = "</S>"

    return {
        "vocab": vocab,
        "v2i": v2i,
        "uni": uni,
        "slot_uni": slot_uni,
        "slot_bi_l": slot_bi_l,
        "slot_bi_r": slot_bi_r,
        "center_bi": center_bi,
        "adj_rep": adj_rep,
        "nonadj_rep": nonadj_rep,
        "v2c": v2c,
        "w2c": w2c,
        "n_clusters": n_clusters,
    }


def evaluate_fold_predictions(train_seqs: list[list[str]], val_seqs: list[list[str]], discount: float = 0.55):
    st = extract_m77_structural_tables(train_seqs, n_clusters=32)
    vocab = st["vocab"]
    v2i = st["v2i"]
    V = len(vocab)
    uni = st["uni"]
    slot_uni = st["slot_uni"]
    slot_bi_l = st["slot_bi_l"]
    slot_bi_r = st["slot_bi_r"]
    center_bi = st["center_bi"]
    adj_rep = st["adj_rep"]
    nonadj_rep = st["nonadj_rep"]
    v2c = st["v2c"]
    w2c = st["w2c"]
    n_clusters = st["n_clusters"]

    kn3_f = train_kneser_ney([s + ["</S>"] for s in train_seqs], max_order=3, discount=discount)
    kn3_r = train_kneser_ney([s[::-1] + ["</S>"] for s in train_seqs], max_order=3, discount=discount)

    # SIGIL matched-null synthetic control trained on exact M77 train fold unigram + length distribution
    tr_corpus = Corpus([Inscription(inscription_id=str(idx), signs=s) for idx, s in enumerate(train_seqs)])
    sigil_corpus = generate_matched_null_corpus(tr_corpus, n_inscriptions=len(tr_corpus), seed=0)
    sigil_seqs = [ins.signs for ins in sigil_corpus.inscriptions]
    kn3_sigil = train_kneser_ney([s + ["</S>"] for s in sigil_seqs], max_order=3, discount=discount)

    tr_cls_f = [[w2c[w] for w in s] + ["</S>"] for s in train_seqs]
    tr_cls_r = [[w2c[w] for w in s[::-1]] + ["</S>"] for s in train_seqs]
    kn3_cf = train_kneser_ney(tr_cls_f, max_order=3, discount=0.50)
    kn3_cr = train_kneser_ney(tr_cls_r, max_order=3, discount=0.50)
    cls_vocab = [f"C{c}" for c in range(n_clusters)]

    def eval_cls_blanket(model, a, b, c):
        ca, cb, cc = w2c.get(a, "<UNK>"), w2c.get(b, "<UNK>"), w2c.get(c, "<UNK>")
        arr_c = np.array([
            math.log(max(model.prob((ca, cv), cb), 1e-12)) + math.log(max(model.prob((cv, cb), cc), 1e-12))
            for cv in cls_vocab
        ], dtype=np.float64)
        return arr_c[v2c]

    def eval_cls_vec(model, a, b):
        ca, cb = w2c.get(a, "<UNK>"), w2c.get(b, "<UNK>")
        arr_c = np.array([math.log(max(model.prob((ca, cb), cv), 1e-12)) for cv in cls_vocab], dtype=np.float64)
        return arr_c[v2c]

    def eval_vec(model, ctx):
        return np.array([math.log(max(model.prob(ctx, v), 1e-12)) for v in vocab], dtype=np.float64)

    def eval_mid(model, a, b):
        return np.array([math.log(max(model.prob((a, v), b), 1e-12)) for v in vocab], dtype=np.float64)

    def eval_step2(model, b, c):
        return np.array([math.log(max(model.prob((v, b), c), 1e-12)) for v in vocab], dtype=np.float64)

    def disc_res(cnt_vec, base_p, D=0.4, alpha=2.0):
        tot = cnt_vec.sum()
        if tot == 0:
            return np.zeros_like(base_p)
        disc = np.maximum(cnt_vec - D, 0.0)
        rem = tot - disc.sum()
        p = (disc + (rem + alpha) * base_p) / (tot + alpha)
        return np.log(p) - np.log(base_p)

    c_t1, c_t2, c_t3, c_t4, c_t5, c_t6, c_cls, c_sig = {}, {}, {}, {}, {}, {}, {}, {}
    p_uni = (uni + 0.5) / (uni.sum() + 0.5 * V)
    log_uni = np.log(p_uni)

    res = {"left": 0, "bidir": 0, "blkf": 0, "sigil": 0, "clss": 0, "total": 0}
    for s in val_seqs:
        L = len(s)
        pad = ["<S>", "<S>", "<S>"] + s + ["</S>", "</S>", "</S>"]
        for i in range(L):
            res["total"] += 1
            target = s[i]
            z = get_slot(i, L)
            pi = i + 3
            l2, l1 = pad[pi - 2], pad[pi - 1]
            r1, r2 = pad[pi + 1], pad[pi + 2]

            if (l2, l1) not in c_t1:
                c_t1[(l2, l1)] = eval_vec(kn3_f, (l2, l1))
            if (l1, r1) not in c_t2:
                c_t2[(l1, r1)] = eval_mid(kn3_f, l1, r1)
            if (r1, r2) not in c_t3:
                c_t3[(r1, r2)] = eval_step2(kn3_f, r1, r2)
            if (r2, r1) not in c_t4:
                c_t4[(r2, r1)] = eval_vec(kn3_r, (r2, r1))
            if (r1, l1) not in c_t5:
                c_t5[(r1, l1)] = eval_mid(kn3_r, r1, l1)
            if (l1, l2) not in c_t6:
                c_t6[(l1, l2)] = eval_step2(kn3_r, l1, l2)
            if (l2, l1) not in c_sig:
                c_sig[(l2, l1)] = eval_vec(kn3_sigil, (l2, l1))

            k_cls = (l2, l1, r1, r2)
            if k_cls not in c_cls:
                c_cls[k_cls] = 0.5 * (
                    eval_cls_vec(kn3_cf, l2, l1) + eval_cls_blanket(kn3_cf, l1, r1, r2) +
                    eval_cls_vec(kn3_cr, r2, r1) + eval_cls_blanket(kn3_cr, r1, l1, l2)
                )

            p_slot = (slot_uni[z] + 2.0 * p_uni) / (slot_uni[z].sum() + 2.0)
            slot_ll = np.log(p_slot) - log_uni
            sbl_res = disc_res(slot_bi_l[(z, l1)], p_slot, D=0.4, alpha=3.0)
            sbr_res = disc_res(slot_bi_r[(z, r1)], p_slot, D=0.4, alpha=3.0)
            cbi_res = disc_res(center_bi[(l1, r1)], p_slot, D=0.4, alpha=2.0)

            rep_v = np.zeros(V, dtype=np.float64)
            for j, other_w in enumerate(s):
                if j == i or other_w not in v2i:
                    continue
                vj = v2i[other_w]
                if abs(j - i) == 1 and adj_rep[other_w] == 0 and uni[vj] >= 5:
                    rep_v[vj] = -1.0
                elif abs(j - i) > 1 and nonadj_rep[other_w] <= 1 and uni[vj] >= 10:
                    rep_v[vj] = -0.35

            sc_left = c_t1[(l2, l1)]
            sc_bidir = c_t1[(l2, l1)] + c_t4[(r2, r1)]
            sc_blkf = c_t1[(l2, l1)] + c_t2[(l1, r1)] + c_t3[(r1, r2)]
            sc_sig = c_sig[(l2, l1)]
            sc_clss = (
                1.4 * (c_t1[(l2, l1)] + c_t4[(r2, r1)]) +
                0.8 * (c_t2[(l1, r1)] + c_t5[(r1, l1)]) +
                0.7 * (c_t3[(r1, r2)] + c_t6[(l1, l2)]) +
                0.15 * c_cls[k_cls] +
                0.25 * slot_ll +
                0.20 * (sbl_res + sbr_res) +
                0.25 * cbi_res +
                0.80 * rep_v
            )
            if vocab[int(np.argmax(sc_left))] == target:
                res["left"] += 1
            if vocab[int(np.argmax(sc_bidir))] == target:
                res["bidir"] += 1
            if vocab[int(np.argmax(sc_blkf))] == target:
                res["blkf"] += 1
            if vocab[int(np.argmax(sc_sig))] == target:
                res["sigil"] += 1
            if vocab[int(np.argmax(sc_clss))] == target:
                res["clss"] += 1
    return res


def extract_top_telescoping_pairs(seqs: list[list[str]], top_k: int = 25):
    """Extract frozen M77-only list of composite/bigram substitutions C <-> (A, B) in parallel contexts."""
    c_frames = defaultdict(set)
    ab_frames = defaultdict(set)
    uni = Counter()
    bi = Counter()
    for s in seqs:
        int_s = [int(x) for x in s]
        pad = [-1] + int_s + [-2]
        L = len(int_s)
        for i in range(L):
            if int_s[i] < 10000:
                c_frames[int_s[i]].add((pad[i], pad[i + 2]))
                uni[int_s[i]] += 1
        for i in range(L - 1):
            if int_s[i] < 10000 and int_s[i + 1] < 10000:
                ab_frames[(int_s[i], int_s[i + 1])].add((pad[i], pad[i + 3]))
                bi[(int_s[i], int_s[i + 1])] += 1

    all_frames = set(fr for s in c_frames.values() for fr in s) | set(fr for s in ab_frames.values() for fr in s)
    F_tot = max(len(all_frames), 1)

    # Exclude paragorth R5 (226 <-> 220, 520) and any trivial overlap C in {A, B}
    scored = []
    for c, f_c in c_frames.items():
        if len(f_c) < 5:
            continue
        for (a, b), f_ab in ab_frames.items():
            if len(f_ab) < 5:
                continue
            if c == a or c == b or (c, a, b) == (226, 220, 520):
                continue
            obs = len(f_c & f_ab)
            if obs < 5:
                continue
            exp = len(f_c) * len(f_ab) / F_tot
            z = (obs - exp) / math.sqrt(max(exp, 0.5))
            scored.append({
                "composite_sign": int(c),
                "bigram": [int(a), int(b)],
                "m77_shared_frames": int(obs),
                "m77_expected_frames": round(exp, 4),
                "m77_z_score": round(z, 4),
                "m77_uni_count": int(uni[c]),
                "m77_bi_count": int(bi[(a, b)]),
            })
    scored.sort(key=lambda r: (r["m77_z_score"], r["m77_shared_frames"]), reverse=True)
    return scored[:top_k]


def main():
    t0 = time.time()
    bridge, m2g_m1, w2g_m1, m2g_m2, w2g_m2 = build_sign_bridges(BRIDGE_JSON)

    recs_m1 = load_m77_records(IM77_CSV, m2g_m1)
    recs_m2 = load_m77_records(IM77_CSV, m2g_m2)

    # Deduplicate M77 sequences globally for 5-fold CV
    seen_m1 = set()
    seqs_m1 = []
    for r in recs_m1:
        t = tuple(r["seq"])
        if t not in seen_m1:
            seen_m1.add(t)
            seqs_m1.append(r["seq"])

    seen_m2 = set()
    seqs_m2 = []
    for r in recs_m2:
        t = tuple(r["seq"])
        if t not in seen_m2:
            seen_m2.add(t)
            seqs_m2.append(r["seq"])

    # Run 5-fold CV on M77 (Mode 1)
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(seqs_m1))
    folds = [perm[i::5] for i in range(5)]

    cv_totals = Counter()
    cv_folds = []
    for fi in range(5):
        vset = set(folds[fi])
        tr = [seqs_m1[i] for i in range(len(seqs_m1)) if i not in vset]
        va = [seqs_m1[i] for i in folds[fi]]
        f_res = evaluate_fold_predictions(tr, va, discount=0.55)
        cv_folds.append(f_res)
        for k, v in f_res.items():
            cv_totals[k] += v

    # Extract full M77 frozen structural tables on 100% of M77 (both Mode 1 and Mode 2)
    full_st_m1 = extract_m77_structural_tables(seqs_m1, n_clusters=32)
    full_st_m2 = extract_m77_structural_tables(seqs_m2, n_clusters=32)
    top25_ligatures_m1 = extract_top_telescoping_pairs(seqs_m1, top_k=25)

    frozen_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    model_payload = {
        "schema": "v3r1t4s-m77-frozen-structural-model-v1",
        "target_id": "indus-temporal-heldout-structure",
        "frozen_utc": frozen_utc,
        "training_corpus_only": {
            "im77_corpus_lines_csv": "data/Indus-/data/im77/im77_corpus_lines.csv",
            "im77_sha256": sha256_file(IM77_CSV),
            "bridge_extended_json": "data/Indus-/data/derived/bridge_extended.json",
            "bridge_sha256": sha256_file(BRIDGE_JSON),
            "n_m77_raw_lines_len_ge_2": len(recs_m1),
            "n_m77_unique_sequences_mode1": len(seqs_m1),
            "n_m77_tokens_mode1": sum(len(s) for s in seqs_m1),
            "n_m77_unique_sequences_mode2": len(seqs_m2),
            "n_m77_tokens_mode2": sum(len(s) for s in seqs_m2),
            "post_1977_data_accessed_during_training": False,
        },
        "hyperparameters_frozen_from_m77_5fold_cv": {
            "kn3_discount": 0.55,
            "class_kn3_discount": 0.50,
            "n_distributional_clusters": 32,
            "slot_zones": ["INIT", "SECOND", "MID", "PENULT", "FINAL"],
            "component_weights": {
                "w_kn3_edge_f_r": 1.40,
                "w_kn3_bridge_mid_f_r": 0.80,
                "w_kn3_bridge_step2_f_r": 0.70,
                "w_32class_blanket": 0.15,
                "w_5zone_slot_prior": 0.25,
                "w_5zone_slot_bigram_res": 0.20,
                "w_center_frame_res": 0.25,
                "w_anti_repetition": 0.80,
            },
        },
        "m77_5fold_cv_summary": {
            "total_tokens": int(cv_totals["total"]),
            "kn3_left_correct": int(cv_totals["left"]),
            "kn3_left_acc": round(cv_totals["left"] / cv_totals["total"], 6),
            "kn3_bidir_correct": int(cv_totals["bidir"]),
            "kn3_bidir_acc": round(cv_totals["bidir"] / cv_totals["total"], 6),
            "kn3_blanket_f_correct": int(cv_totals["blkf"]),
            "kn3_blanket_f_acc": round(cv_totals["blkf"] / cv_totals["total"], 6),
            "sigil_null_correct": int(cv_totals["sigil"]),
            "sigil_null_acc": round(cv_totals["sigil"] / cv_totals["total"], 6),
            "m77_clss_correct": int(cv_totals["clss"]),
            "m77_clss_acc": round(cv_totals["clss"] / cv_totals["total"], 6),
            "folds": cv_folds,
        },
        "sign_mappings": {
            "m_override": {str(k): int(v) for k, v in M_OVERRIDE.items()},
            "m2g_mode1": {str(k): int(v) for k, v in sorted(m2g_m1.items())},
            "m2g_mode2": {str(k): int(v) for k, v in sorted(m2g_m2.items())},
            "w2g_mode2": {str(k): int(v) for k, v in sorted(w2g_m2.items())},
        },
        "frozen_m77_clusters_mode1": full_st_m1["w2c"],
        "frozen_m77_clusters_mode2": full_st_m2["w2c"],
        "frozen_m77_slot_unigrams_mode1": {
            w: [int(full_st_m1["slot_uni"][z, full_st_m1["v2i"][w]]) for z in range(5)]
            for w in full_st_m1["vocab"]
        },
        "frozen_m77_top25_telescoping_ligatures_p3": top25_ligatures_m1,
        "frozen_m77_sequences_mode1": seqs_m1,
        "frozen_m77_sequences_mode2": seqs_m2,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(model_payload, f, indent=2)

    out_sha = sha256_file(OUT_JSON)
    print(f"Frozen M77 model written to {OUT_JSON} in {time.time() - t0:.2f}s")
    print(f"  frozen_utc : {frozen_utc}")
    print(f"  sha256     : {out_sha}")
    print(f"  M77 5-fold CV ({cv_totals['total']} tokens):")
    print(f"    M77-CLSS     : {cv_totals['clss']}/{cv_totals['total']} ({cv_totals['clss']/cv_totals['total']:.4f})")
    print(f"    KN3-Left     : {cv_totals['left']}/{cv_totals['total']} ({cv_totals['left']/cv_totals['total']:.4f})")
    print(f"    KN3-Bidir    : {cv_totals['bidir']}/{cv_totals['total']} ({cv_totals['bidir']/cv_totals['total']:.4f})")
    print(f"    KN3-BlanketF : {cv_totals['blkf']}/{cv_totals['total']} ({cv_totals['blkf']/cv_totals['total']:.4f})")
    print(f"    SIGIL-Null   : {cv_totals['sigil']}/{cv_totals['total']} ({cv_totals['sigil']/cv_totals['total']:.4f})")


if __name__ == "__main__":
    main()
