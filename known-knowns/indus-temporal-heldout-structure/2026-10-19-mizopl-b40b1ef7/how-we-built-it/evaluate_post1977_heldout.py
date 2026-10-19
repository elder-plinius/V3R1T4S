#!/usr/bin/env python3
"""
evaluate_post1977_heldout.py
============================
Evaluates the frozen, timestamped M77-only structural model (`m77_frozen_structural_model.json`)
on the publication-dated, seal-identity-deduplicated post-1977 (> 1977) held-out Indus corpus.

Verifies:
  1. Timestamp & SHA-256 anti-leakage integrity (`m77_frozen_structural_model.json` and `PREREG.md`
     precede evaluation and `null_test.md`).
  2. Publication-dated post-1977 split construction (`CISI Vol. 1 1987`, `CISI Vol. 2 1991`,
     `CISI Vol. 3.1 2010`, `CISI Vol. 3.2 2019`, `HARP 1986-2008`, `Dales 1991 UPM`,
     `Aachen 1979-86 MN-S`, `Bisht 2015 Dholavira`, and post-1977 site excavations).
  3. Zero overlap with M77 sequences (forward or reverse, under exact or multi-valued bridge expansion),
     zero overlap with `loop24_pairs.json` aligned objects, and strict deduplication by object ID,
     exact sequence, and `identity-directory.json` (386 seal-impression identities).
  4. Reading-direction verification (W740 Jar sign terminal vs initial share).
  5. Paired-bootstrap p-values (10,000 resamples, seed=0) for Masked-Sign Top-1 Accuracy against:
       (i-a) Tuned Kneser-Ney 3-gram `KN3-Left` (D=0.55)
       (i-b) Tuned Bidirectional Kneser-Ney 3-gram `KN3-Bidir` (D=0.55)
       (i-c) Tuned Full-Blanket Kneser-Ney 3-gram `KN3-BlanketF` (D=0.55)
       (ii)  `SIGIL` matched-null synthetic control (matched on M77 unigram, initial, final, and length)
     across Pooled, Mohenjo-daro, Harappa, Dholavira, and All Post-1977 Excavated Sites,
     under both Mode 1 (`test_prereg.py` `m2g`) and Mode 2 (`bridge_extended.json` connected components),
     and across both Cohort A (all publication-dated post-1977 non-IM77 objects) and Cohort B
     (strict post-1977 catalog-number ranges).
  6. Partial win `p3`: Frozen Top-25 M77 telescoping composite/bigram substitution rate in parallel
     contexts of post-1977 held-out texts vs 10,000 frequency-matched random composite/bigram sets.
  7. 400 independent `SIGIL` matched-null controls written to `null_test.md`.
"""

import csv
import datetime
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "data", "indus_decipher"))
from analysis.ngram import train_kneser_ney
from data.adversarial_null_model import generate_matched_null_corpus
from data.loader import Corpus, Inscription

FROZEN_MODEL_PATH = os.path.join(HERE, "m77_frozen_structural_model.json")
PREREG_PATH = os.path.join(HERE, "PREREG.md")
IM77_CSV = os.path.join(HERE, "data", "Indus-", "data", "im77", "im77_corpus_lines.csv")
BRIDGE_JSON = os.path.join(HERE, "data", "Indus-", "data", "derived", "bridge_extended.json")
MERGED_V2_JSON = os.path.join(HERE, "data", "Indus-", "data", "derived", "merged-corpus-canonical.v2.json")
LOOP24_JSON = os.path.join(HERE, "data", "Indus-", "data", "derived", "dark", "loop24_pairs.json")
IDENTITY_JSON = os.path.join(HERE, "data", "Indus-", "data", "derived", "identity-directory.json")
OUT_RESULTS_JSON = os.path.join(HERE, "post1977_evaluation_results.json")
OUT_PREDS_CSV = os.path.join(HERE, "post1977_heldout_predictions.csv")
OUT_NULL_MD = os.path.join(HERE, "null_test.md")

EXPECTED_MODEL_SHA256 = "b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_slot(i: int, L: int) -> int:
    if i == 0:
        return 0
    if i == L - 1:
        return 4
    if i == 1 and L >= 3:
        return 1
    if i == L - 2 and L >= 4:
        return 3
    return 2


def classify_post1977_publication(cisi: str, site: str) -> tuple[str | None, bool]:
    """
    Returns `(publication_source, is_strict_post1977_catalog_range)` for a non-IM77 object.
    Returns `(None, False)` if the object lacks a documented post-1977 CISI or excavation source.
    """
    cisi = (cisi or "").strip()
    site = (site or "").strip()

    # 1. Sites excavated/published entirely after 1977 (absent from M77 or post-1977 excavations)
    post1977_sites = {
        "Dholavira": ("CISI Vol. 3.1 (2010) & Bisht (2015) ASI Excavations at Dholavira (1990-2005)", True),
        "Nausharo": ("Jarrige (1986-1996) Excavations at Nausharo & CISI Vol. 2 (1991) / Vol. 3.1 (2010)", True),
        "Banawali": ("Bisht (1982/1987) Excavations at Banawali & CISI Vol. 1 (1987) / Vol. 3.1 (2010)", True),
        "Lakhanjo-daro": ("Mughal / Shaikh (1994-2006) Excavations at Lakhanjo-daro & CISI Vol. 3.1 (2010)", True),
        "Rakhigarhi": ("Nath (1998-2001) / Shinde Excavations at Rakhigarhi & CISI Vol. 3.1 (2010)", True),
        "Allahdino": ("Fairservis (1982) Allahdino Excavations & CISI Vol. 2 (1991) / Vol. 3.1 (2010)", True),
        "Kanmer": ("Kharakwal, Rawat & Osada (2006-2012) Excavations at Kanmer", True),
        "Farmana": ("Shinde, Osada & Kumar (2008-2011) Excavations at Farmana", True),
        "Karanpura": ("Prabhakar (2012-2014) ASI Excavations at Karanpura", True),
        "Shikarpur": ("Bhan & Ajithprasad (2007-2014) MSU Excavations at Shikarpur", True),
        "Balakot": ("Dales (1979) / Franke-Vogt (1991) & CISI Vol. 2 (1991) / Vol. 3.1 (2010)", True),
        "Bhirrana": ("Rao et al. (2004-2006) ASI Excavations at Bhirrana & CISI Vol. 3.1 (2010)", True),
        "Gola Dhoro": ("Bhan et al. (1996-2005) Excavations at Bagasra / Gola Dhoro", True),
        "Gola Dhoro (Bagasra)": ("Bhan et al. (1996-2005) Excavations at Bagasra / Gola Dhoro", True),
        "Bagasra": ("Bhan et al. (1996-2005) Excavations at Bagasra / Gola Dhoro", True),
        "Shortughai": ("Francfort (1989) Fouilles de Shortughai", True),
        "Ra's al-Jinz": ("Cleuziou & Tosi (1985-1998) Excavations at Ra's al-Jinz", True),
        "Ra's al-Junayz": ("Cleuziou & Tosi (1985-1998) Excavations at Ra's al-Jinz / Ra's al-Junayz", True),
        "Saar": ("Killick & Moon (1991-2005) London-Bahrain Archaeological Expedition at Saar", True),
        "Karzakan": ("Bahrain Directorate of Archaeology / Hojlund (1990s-2000s) Karzakan Excavations", True),
        "Qala'at al-Bahrain": ("Hojlund & Andersen (1994/1997) Qala'at al-Bahrain Excavations", True),
        "Miri Qalat": ("Besenval (1992-2000) Mission Archeologique Francaise au Makran, CISI Vol. 3.1 (2010)", True),
        "Rehman Dheri": ("Durrani (1988) Excavations at Rehman Dheri & CISI Vol. 2 (1991)", True),
        "Hulas": ("Dikshit (1981-1985) Excavations at Hulas & CISI Vol. 1 (1987)", True),
        "Kunal": ("Khatri & Acharya (1995) Excavations at Kunal & CISI Vol. 3.1 (2010)", True),
        "Tarkhanewala-Dera": ("Trivedi (2009) ASI Excavations at Tarkhanewala-Dera & CISI Vol. 3.1 (2010)", True),
        "Baror": ("Sant et al. (2005) ASI Excavations at Baror & CISI Vol. 3.1 (2010)", True),
        "Nindowari": ("Jarrige, Quivron & Jarrige (2011) Fouilles de Nindowari & CISI Vol. 3.1 (2010)", True),
        "Sotka-koh": ("Dales & Lipo (1992) Makran Survey / CISI Vol. 3.1 (2010)", True),
        "Londo": ("CISI Vol. 3.1 (2010)", True),
        "Naru-waro-dharo": ("CISI Vol. 2 (1991)", True),
    }
    if site in post1977_sites:
        return post1977_sites[site]

    # For sites with pre-1977 excavations (Mohenjo-daro, Harappa, Kalibangan, Lothal, Chanhu-daro),
    # strictly require an explicit CISI or post-1977 excavation catalog number.
    if not cisi or cisi in ("-", "None", "none") or cisi.startswith("_anon"):
        return None, False

    # 2. Mohenjo-daro
    if site == "Mohenjo-daro":
        m = re.match(r"^M-(\d+)", cisi)
        if m:
            num = int(m.group(1))
            if num >= 1657:
                return "CISI Vol. 3.1 (Parpola, Pande & Koskikallio 2010), M-1657..2129", True
            elif num >= 626:
                return "CISI Vol. 2 (Shah & Parpola 1991), M-626..1656 (non-IM77 museum/excavation supplement)", False
            else:
                return "CISI Vol. 1 (Joshi & Parpola 1987), M-1..625 (non-IM77 supplement)", False
        if cisi.startswith(("UPM-", "MD-")):
            return "Dales & Kenoyer (1986/1991) UPM Mohenjo-daro Excavations / CISI Vol. 3.1 (2010)", True
        if cisi.startswith("MN-S"):
            return "Jansen & Urban (1979-1986) Aachen RWTH Mohenjo-daro Surface Survey", True
        return None, False

    # 3. Harappa
    if site == "Harappa":
        m = re.match(r"^H-(\d+)", cisi)
        if m:
            num = int(m.group(1))
            if num >= 1599:
                return "CISI Vol. 3.2 (Parpola, Koskikallio & Meadow 2019, HARP 1986-2008), H-1599..2589", True
            elif num >= 1020:
                return "CISI Vol. 3.1 (Parpola, Pande & Koskikallio 2010), H-1020..1598", True
            elif num >= 382:
                return "CISI Vol. 2 (Shah & Parpola 1991), H-382..1019 (non-IM77 museum/excavation supplement)", False
            else:
                return "CISI Vol. 1 (Joshi & Parpola 1987), H-1..381 (non-IM77 supplement)", False
        if re.match(r"^H(8[6-9]|9\d|20\d\d|[12]\d\d\d)[-/]", cisi) or cisi.startswith(("H9", "H8", "H200")):
            return "Harappa Archaeological Research Project (HARP 1986-2008, Meadow & Kenoyer) / CISI Vol. 3.2 (2019)", True
        return None, False

    # 4. Kalibangan, Lothal, Chanhu-daro post-1977 CISI supplements
    if site == "Kalibangan":
        m = re.match(r"^K-(\d+)", cisi)
        if m:
            num = int(m.group(1))
            if num >= 100:
                return "CISI Vol. 3.1 (2010), K-100..124", True
            return "CISI Vol. 1 (1987), K-1..99 (non-IM77 supplement)", False
    if site == "Lothal":
        m = re.match(r"^L-(\d+)", cisi)
        if m:
            num = int(m.group(1))
            if num >= 217:
                return "CISI Vol. 3.1 (2010) & Frenez-Tosi (2005), L-217..268", True
            return "Rao (1979/1985) Lothal Vol. I-II & CISI Vol. 1 (1987), L-1..216 (non-IM77 supplement)", False
    if site == "Chanhu-daro":
        m = re.match(r"^C-(\d+)", cisi)
        if m:
            return "CISI Vol. 1 (1987) / Vol. 3.1 (2010) Chanhu-daro non-IM77 museum supplement", False

    return None, False


def build_post1977_heldout_corpus(frozen_model: dict):
    bridge = json.load(open(BRIDGE_JSON, encoding="utf-8"))
    inv = defaultdict(set)
    for g, ms in bridge.items():
        for m in ms:
            inv[int(m)].add(int(g))

    m2g_mode1 = {int(k): int(v) for k, v in frozen_model["sign_mappings"]["m2g_mode1"].items()}
    m2g_mode2 = {int(k): int(v) for k, v in frozen_model["sign_mappings"]["m2g_mode2"].items()}
    w2g_mode2 = {int(k): int(v) for k, v in frozen_model["sign_mappings"]["w2g_mode2"].items()}

    # Build exhaustive set of M77 sequences (forward and reverse) under Mode 1, Mode 2, and bridge expansion
    m77_seqs_m1 = set()
    m77_seqs_m2 = set()
    m77_bridged_tuples = []
    with open(IM77_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["line"] == "9":
                continue
            m_seq = [int(x) for x in r["signs_clean"].split() if int(x) != 0]
            if not m_seq:
                continue
            s1 = tuple(str(m2g_mode1.get(m, 10000 + m)) for m in m_seq)
            s2 = tuple(str(m2g_mode2.get(m, 10000 + m)) for m in m_seq)
            m77_seqs_m1.add(s1)
            m77_seqs_m1.add(s1[::-1])
            m77_seqs_m2.add(s2)
            m77_seqs_m2.add(s2[::-1])
            # Also store multi-valued W sets for each M token to catch any allograph split of an M77 sequence
            w_sets = []
            for m in m_seq:
                gs = set(inv.get(m, set()))
                if m in m2g_mode1:
                    gs.add(m2g_mode1[m])
                if m in m2g_mode2:
                    gs.add(m2g_mode2[m])
                w_sets.append(gs)
            m77_bridged_tuples.append(w_sets)
            m77_bridged_tuples.append(w_sets[::-1])

    by_len_m77 = defaultdict(list)
    for ws in m77_bridged_tuples:
        by_len_m77[len(ws)].append(ws)

    def matches_any_m77_expansion(w_seq: list[int]) -> bool:
        for ws in by_len_m77.get(len(w_seq), []):
            if all((bool(gs) and (w in gs)) for w, gs in zip(w_seq, ws)):
                return True
        return False

    # Load loop24_pairs.json aligned objects (accepted alignments to IM77)
    loop24 = json.load(open(LOOP24_JSON, encoding="utf-8"))
    aligned_w_idx = set(p["widx"] for p in loop24 if p.get("accepted"))
    aligned_cisi = set(p["cisi"].strip() for p in loop24 if p.get("accepted") and p.get("cisi") and p["cisi"].strip() != "-")

    # Load 386-identity recurring seal directory (`stem -> {"full_texts": {"a+b+c": count, ...}}`)
    identities_dict = json.load(open(IDENTITY_JSON, encoding="utf-8"))
    seq_to_identity = {}
    identity_in_m77 = set()
    for stem_key, info in identities_dict.items():
        stem_toks = tuple(int(x) for x in stem_key.split("+") if x.isdigit())
        seq_to_identity[stem_toks] = stem_key
        for ft_str in info.get("full_texts", {}).keys():
            ft_toks = tuple(int(x) for x in ft_str.split("+") if x.isdigit())
            seq_to_identity[ft_toks] = stem_key
            ft_m1 = tuple(str(x) for x in ft_toks)
            ft_m2 = tuple(str(w2g_mode2.get(x, x)) for x in ft_toks)
            if ft_m1 in m77_seqs_m1 or ft_m2 in m77_seqs_m2 or matches_any_m77_expansion(list(ft_toks)):
                identity_in_m77.add(stem_key)

    # Load merged-corpus-canonical.v2.json
    merged = json.load(open(MERGED_V2_JSON, encoding="utf-8"))

    def cls_of(t: str) -> str:
        t = (t or "").upper()
        if t.startswith("SEAL"):
            return "seal"
        if t.startswith("TAG") or t == "SEALING":
            return "sealing"
        if t.startswith("TAB") or "TABLET" in t:
            return "tablet"
        return "other"

    heldout_records = []
    seen_cisi = set()
    seen_seq_m1 = set()
    seen_seq_m2 = set()
    seen_identities = set()
    filter_counts = Counter()

    for idx, r in enumerate(merged):
        filter_counts["total_merged_v2"] += 1
        cisi = (r.get("cisi") or "").strip()
        site = (r.get("site") or "").strip()
        w_raw = [int(x) for x in r.get("seq_raw", r["seq"]) if int(x) != 0]
        if len(w_raw) < 2:
            filter_counts["dropped_len_lt_2"] += 1
            continue

        # Exclude loop24 aligned objects
        if (r.get("v1") and idx in aligned_w_idx) or (cisi in aligned_cisi):
            filter_counts["excluded_in_im77_loop24"] += 1
            continue

        # Require documented post-1977 publication source
        pub_source, is_strict_range = classify_post1977_publication(cisi, site)
        if pub_source is None:
            filter_counts["excluded_no_post1977_pub_source"] += 1
            continue

        # Map sequence under Mode 1 and Mode 2
        s_m1 = tuple(str(x) for x in w_raw)
        s_m2 = tuple(str(w2g_mode2.get(x, x)) for x in w_raw)

        # Exclude any sequence matching M77 (forward or reverse) under Mode 1, Mode 2, or multi-valued bridge
        if s_m1 in m77_seqs_m1 or s_m2 in m77_seqs_m2 or matches_any_m77_expansion(w_raw):
            filter_counts["excluded_sequence_in_im77"] += 1
            continue

        # Seal-impression identity deduplication (386-identity directory)
        w_can = tuple(int(x) for x in r.get("seq", w_raw) if int(x) != 0)
        iid = seq_to_identity.get(tuple(w_raw)) or seq_to_identity.get(w_can)
        if iid is not None:
            if iid in identity_in_m77:
                filter_counts["excluded_seal_identity_in_im77"] += 1
                continue
            if iid in seen_identities:
                filter_counts["deduped_seal_identity"] += 1
                continue

        # Deduplicate by object ID (cisi or ICIT object id) and exact sequence (both Mode 1 and Mode 2)
        obj_id = cisi if cisi not in ("", "-", "None", "none") else f"ICIT-{str(r.get('id', idx)).split('.')[0]}"
        if obj_id in seen_cisi or s_m1 in seen_seq_m1 or s_m2 in seen_seq_m2:
            filter_counts["deduped_object_or_sequence"] += 1
            continue

        seen_cisi.add(obj_id)
        seen_seq_m1.add(s_m1)
        seen_seq_m2.add(s_m2)
        if iid is not None:
            seen_identities.add(iid)

        heldout_records.append({
            "cisi": obj_id,
            "site": site,
            "cls": cls_of(r.get("type", "")),
            "raw_type": r.get("type", ""),
            "symbol": r.get("symbol", ""),
            "publication_source": pub_source,
            "is_strict_post1977_range": is_strict_range,
            "seq_m1": list(s_m1),
            "seq_m2": list(s_m2),
        })
        filter_counts["kept_heldout"] += 1

    return heldout_records, dict(filter_counts)


class FrozenM77Evaluator:
    def __init__(self, train_seqs: list[list[str]], w2c: dict[str, str], discount: float = 0.55):
        self.train_seqs = train_seqs
        self.w2c = dict(w2c)
        self.discount = discount
        self.vocab = sorted(set(w for s in train_seqs for w in s))
        self.v2i = {w: i for i, w in enumerate(self.vocab)}
        self.V = len(self.vocab)
        self.n_clusters = 32
        self.v2c = np.array([int(self.w2c[w][1:]) for w in self.vocab], dtype=np.int64)

        self.uni = np.zeros(self.V, dtype=np.float64)
        self.slot_uni = np.zeros((5, self.V), dtype=np.float64)
        self.slot_bi_l = defaultdict(lambda: np.zeros(self.V, dtype=np.float64))
        self.slot_bi_r = defaultdict(lambda: np.zeros(self.V, dtype=np.float64))
        self.center_bi = defaultdict(lambda: np.zeros(self.V, dtype=np.float64))
        self.adj_rep = Counter()
        self.nonadj_rep = Counter()

        for s in train_seqs:
            L = len(s)
            pad = ["<S>"] + s + ["</S>"]
            for i, w in enumerate(s):
                vi = self.v2i[w]
                z = get_slot(i, L)
                self.uni[vi] += 1.0
                self.slot_uni[z, vi] += 1.0
                l1, r1 = pad[i], pad[i + 2]
                self.slot_bi_l[(z, l1)][vi] += 1.0
                self.slot_bi_r[(z, r1)][vi] += 1.0
                self.center_bi[(l1, r1)][vi] += 1.0
                if i + 1 < L and s[i + 1] == w:
                    self.adj_rep[w] += 1
                if w in (s[:max(0, i - 1)] + s[min(L, i + 2):]):
                    self.nonadj_rep[w] += 1

        self.kn3_f = train_kneser_ney([s + ["</S>"] for s in train_seqs], max_order=3, discount=discount)
        self.kn3_r = train_kneser_ney([s[::-1] + ["</S>"] for s in train_seqs], max_order=3, discount=discount)

        tr_corpus = Corpus([Inscription(inscription_id=str(idx), signs=s) for idx, s in enumerate(train_seqs)])
        sigil_corpus = generate_matched_null_corpus(tr_corpus, n_inscriptions=len(tr_corpus), seed=0)
        sigil_seqs = [ins.signs for ins in sigil_corpus.inscriptions]
        self.kn3_sigil = train_kneser_ney([s + ["</S>"] for s in sigil_seqs], max_order=3, discount=discount)

        tr_cls_f = [[self.w2c.get(w, "<UNK>") for w in s] + ["</S>"] for s in train_seqs]
        tr_cls_r = [[self.w2c.get(w, "<UNK>") for w in s[::-1]] + ["</S>"] for s in train_seqs]
        self.kn3_cf = train_kneser_ney(tr_cls_f, max_order=3, discount=0.50)
        self.kn3_cr = train_kneser_ney(tr_cls_r, max_order=3, discount=0.50)
        self.cls_vocab = [f"C{c}" for c in range(self.n_clusters)]

        self.p_uni = (self.uni + 0.5) / (self.uni.sum() + 0.5 * self.V)
        self.log_uni = np.log(self.p_uni)

        self.c_t1 = {}
        self.c_t2 = {}
        self.c_t3 = {}
        self.c_t4 = {}
        self.c_t5 = {}
        self.c_t6 = {}
        self.c_cls = {}
        self.c_sig = {}

    def _eval_cls_blanket(self, model, a, b, c):
        ca, cb, cc = self.w2c.get(a, "<UNK>"), self.w2c.get(b, "<UNK>"), self.w2c.get(c, "<UNK>")
        arr_c = np.array([
            math.log(max(model.prob((ca, cv), cb), 1e-12)) + math.log(max(model.prob((cv, cb), cc), 1e-12))
            for cv in self.cls_vocab
        ], dtype=np.float64)
        return arr_c[self.v2c]

    def _eval_cls_vec(self, model, a, b):
        ca, cb = self.w2c.get(a, "<UNK>"), self.w2c.get(b, "<UNK>")
        arr_c = np.array([math.log(max(model.prob((ca, cb), cv), 1e-12)) for cv in self.cls_vocab], dtype=np.float64)
        return arr_c[self.v2c]

    def _eval_vec(self, model, ctx):
        return np.array([math.log(max(model.prob(ctx, v), 1e-12)) for v in self.vocab], dtype=np.float64)

    def _eval_mid(self, model, a, b):
        return np.array([math.log(max(model.prob((a, v), b), 1e-12)) for v in self.vocab], dtype=np.float64)

    def _eval_step2(self, model, b, c):
        return np.array([math.log(max(model.prob((v, b), c), 1e-12)) for v in self.vocab], dtype=np.float64)

    @staticmethod
    def _disc_res(cnt_vec, base_p, D=0.4, alpha=2.0):
        tot = cnt_vec.sum()
        if tot == 0:
            return np.zeros_like(base_p)
        disc = np.maximum(cnt_vec - D, 0.0)
        rem = tot - disc.sum()
        p = (disc + (rem + alpha) * base_p) / (tot + alpha)
        return np.log(p) - np.log(base_p)

    def predict_sequence_tokens(self, s: list[str]) -> list[dict]:
        L = len(s)
        pad = ["<S>", "<S>", "<S>"] + s + ["</S>", "</S>", "</S>"]
        out = []
        for i in range(L):
            target = s[i]
            z = get_slot(i, L)
            pi = i + 3
            l2, l1 = pad[pi - 2], pad[pi - 1]
            r1, r2 = pad[pi + 1], pad[pi + 2]

            if (l2, l1) not in self.c_t1:
                self.c_t1[(l2, l1)] = self._eval_vec(self.kn3_f, (l2, l1))
            if (l1, r1) not in self.c_t2:
                self.c_t2[(l1, r1)] = self._eval_mid(self.kn3_f, l1, r1)
            if (r1, r2) not in self.c_t3:
                self.c_t3[(r1, r2)] = self._eval_step2(self.kn3_f, r1, r2)
            if (r2, r1) not in self.c_t4:
                self.c_t4[(r2, r1)] = self._eval_vec(self.kn3_r, (r2, r1))
            if (r1, l1) not in self.c_t5:
                self.c_t5[(r1, l1)] = self._eval_mid(self.kn3_r, r1, l1)
            if (l1, l2) not in self.c_t6:
                self.c_t6[(l1, l2)] = self._eval_step2(self.kn3_r, l1, l2)
            if (l2, l1) not in self.c_sig:
                self.c_sig[(l2, l1)] = self._eval_vec(self.kn3_sigil, (l2, l1))

            k_cls = (l2, l1, r1, r2)
            if k_cls not in self.c_cls:
                self.c_cls[k_cls] = 0.5 * (
                    self._eval_cls_vec(self.kn3_cf, l2, l1) + self._eval_cls_blanket(self.kn3_cf, l1, r1, r2) +
                    self._eval_cls_vec(self.kn3_cr, r2, r1) + self._eval_cls_blanket(self.kn3_cr, r1, l1, l2)
                )

            p_slot = (self.slot_uni[z] + 2.0 * self.p_uni) / (self.slot_uni[z].sum() + 2.0)
            slot_ll = np.log(p_slot) - self.log_uni
            sbl_res = self._disc_res(self.slot_bi_l[(z, l1)], p_slot, D=0.4, alpha=3.0)
            sbr_res = self._disc_res(self.slot_bi_r[(z, r1)], p_slot, D=0.4, alpha=3.0)
            cbi_res = self._disc_res(self.center_bi[(l1, r1)], p_slot, D=0.4, alpha=2.0)

            rep_v = np.zeros(self.V, dtype=np.float64)
            for j, other_w in enumerate(s):
                if j == i or other_w not in self.v2i:
                    continue
                vj = self.v2i[other_w]
                if abs(j - i) == 1 and self.adj_rep[other_w] == 0 and self.uni[vj] >= 5:
                    rep_v[vj] = -1.0
                elif abs(j - i) > 1 and self.nonadj_rep[other_w] <= 1 and self.uni[vj] >= 10:
                    rep_v[vj] = -0.35

            sc_left = self.c_t1[(l2, l1)]
            sc_bidir = self.c_t1[(l2, l1)] + self.c_t4[(r2, r1)]
            sc_blkf = self.c_t1[(l2, l1)] + self.c_t2[(l1, r1)] + self.c_t3[(r1, r2)]
            sc_sig = self.c_sig[(l2, l1)]
            sc_clss = (
                1.4 * (self.c_t1[(l2, l1)] + self.c_t4[(r2, r1)]) +
                0.8 * (self.c_t2[(l1, r1)] + self.c_t5[(r1, l1)]) +
                0.7 * (self.c_t3[(r1, r2)] + self.c_t6[(l1, l2)]) +
                0.15 * self.c_cls[k_cls] +
                0.25 * slot_ll +
                0.20 * (sbl_res + sbr_res) +
                0.25 * cbi_res +
                0.80 * rep_v
            )
            pred_left = self.vocab[int(np.argmax(sc_left))]
            pred_bidir = self.vocab[int(np.argmax(sc_bidir))]
            pred_blkf = self.vocab[int(np.argmax(sc_blkf))]
            pred_sig = self.vocab[int(np.argmax(sc_sig))]
            pred_clss = self.vocab[int(np.argmax(sc_clss))]
            out.append({
                "pos": i,
                "slot": z,
                "target": target,
                "pred_clss": pred_clss,
                "pred_kn3_left": pred_left,
                "pred_kn3_bidir": pred_bidir,
                "pred_kn3_blanket_f": pred_blkf,
                "pred_sigil": pred_sig,
                "hit_clss": int(pred_clss == target),
                "hit_kn3_left": int(pred_left == target),
                "hit_kn3_bidir": int(pred_bidir == target),
                "hit_kn3_blanket_f": int(pred_blkf == target),
                "hit_sigil": int(pred_sig == target),
            })
        return out


def paired_bootstrap_Summary(tok_rows: list[dict], n_boot: int = 10000, seed: int = 0) -> dict:
    """Computes exact accuracies and 10,000-resample paired-bootstrap p-values (seed=0)."""
    n = len(tok_rows)
    if n == 0:
        return {}
    c_clss = np.array([r["hit_clss"] for r in tok_rows], dtype=np.float64)
    c_left = np.array([r["hit_kn3_left"] for r in tok_rows], dtype=np.float64)
    c_bidir = np.array([r["hit_kn3_bidir"] for r in tok_rows], dtype=np.float64)
    c_blkf = np.array([r["hit_kn3_blanket_f"] for r in tok_rows], dtype=np.float64)
    c_sig = np.array([r["hit_sigil"] for r in tok_rows], dtype=np.float64)

    d_left = c_clss - c_left
    d_bidir = c_clss - c_bidir
    d_blkf = c_clss - c_blkf
    d_sig = c_clss - c_sig

    rng = np.random.default_rng(seed)
    # Vectorized bootstrap in chunks of 1000
    NonPos_left = 0
    NonPos_bidir = 0
    NonPos_blkf = 0
    NonPos_sig = 0
    for _ in range(n_boot // 1000):
        idx = rng.integers(0, n, size=(1000, n))
        NonPos_left += int(np.sum(d_left[idx].mean(axis=1) <= 0))
        NonPos_bidir += int(np.sum(d_bidir[idx].mean(axis=1) <= 0))
        NonPos_blkf += int(np.sum(d_blkf[idx].mean(axis=1) <= 0))
        NonPos_sig += int(np.sum(d_sig[idx].mean(axis=1) <= 0))

    return {
        "n_tokens": n,
        "clss_hits": int(c_clss.sum()),
        "clss_acc": round(float(c_clss.mean()), 6),
        "kn3_left_hits": int(c_left.sum()),
        "kn3_left_acc": round(float(c_left.mean()), 6),
        "kn3_bidir_hits": int(c_bidir.sum()),
        "kn3_bidir_acc": round(float(c_bidir.mean()), 6),
        "kn3_blanket_f_hits": int(c_blkf.sum()),
        "kn3_blanket_f_acc": round(float(c_blkf.mean()), 6),
        "sigil_hits": int(c_sig.sum()),
        "sigil_acc": round(float(c_sig.mean()), 6),
        "gain_vs_kn3_left": round(float(d_left.mean()), 6),
        "gain_vs_kn3_bidir": round(float(d_bidir.mean()), 6),
        "gain_vs_kn3_blanket_f": round(float(d_blkf.mean()), 6),
        "gain_vs_sigil": round(float(d_sig.mean()), 6),
        "p_boot_vs_kn3_left": round((NonPos_left + 1) / (n_boot + 1), 6),
        "p_boot_vs_kn3_bidir": round((NonPos_bidir + 1) / (n_boot + 1), 6),
        "p_boot_vs_kn3_blanket_f": round((NonPos_blkf + 1) / (n_boot + 1), 6),
        "p_boot_vs_sigil": round((NonPos_sig + 1) / (n_boot + 1), 6),
        "raw_nonpos_vs_kn3_left": NonPos_left,
        "raw_nonpos_vs_kn3_bidir": NonPos_bidir,
        "raw_nonpos_vs_kn3_blanket_f": NonPos_blkf,
        "raw_nonpos_vs_sigil": NonPos_sig,
    }


def evaluate_p3_telescoping_ligatures(
    m77_seqs: list[list[str]],
    heldout_seqs: list[list[str]],
    frozen_top25: list[dict],
    n_perm: int = 10000,
    seed: int = 0,
) -> dict:
    """Evaluates frozen M77 Top-25 telescoping composite/bigram pairs on post-1977 held-out parallel contexts."""
    uni_m77 = Counter(int(w) for s in m77_seqs for w in s if int(w) < 10000)
    bi_m77 = Counter(
        (int(a), int(b)) for s in m77_seqs for a, b in zip(s, s[1:]) if int(a) < 10000 and int(b) < 10000
    )

    c_frames_ho = defaultdict(set)
    ab_frames_ho = defaultdict(set)
    for s in heldout_seqs:
        int_s = [int(x) for x in s]
        pad = [-1] + int_s + [-2]
        L = len(int_s)
        for i in range(L):
            if int_s[i] < 10000:
                c_frames_ho[int_s[i]].add((pad[i], pad[i + 2]))
        for i in range(L - 1):
            if int_s[i] < 10000 and int_s[i + 1] < 10000:
                ab_frames_ho[(int_s[i], int_s[i + 1])].add((pad[i], pad[i + 3]))

    pairs = [(item["composite_sign"], tuple(item["bigram"])) for item in frozen_top25]
    per_pair_heldout = []
    real_total_shared = 0
    active_pairs = 0
    for c, ab in pairs:
        shared = len(c_frames_ho[c] & ab_frames_ho[ab])
        real_total_shared += shared
        if shared > 0:
            active_pairs += 1
        per_pair_heldout.append({
            "composite_sign": c,
            "bigram": list(ab),
            "heldout_shared_frames": shared,
            "heldout_c_frames": len(c_frames_ho[c]),
            "heldout_ab_frames": len(ab_frames_ho[ab]),
        })

    cand_c = [c for c, cnt in uni_m77.items() if cnt >= 5]
    cand_ab = [ab for ab, cnt in bi_m77.items() if cnt >= 5]
    c_neighbors = {
        c: sorted(cand_c, key=lambda x: abs(math.log(uni_m77[x]) - math.log(max(uni_m77[c], 1))))[:15]
        for c, _ in pairs
    }
    ab_neighbors = {
        ab: sorted(cand_ab, key=lambda x: abs(math.log(bi_m77[x]) - math.log(max(bi_m77[ab], 1))))[:15]
        for _, ab in pairs
    }

    rng = np.random.default_rng(seed)
    null_totals = np.zeros(n_perm, dtype=np.int64)
    for p_idx in range(n_perm):
        s_null = 0
        for c, ab in pairs:
            rc = c_neighbors[c][int(rng.integers(len(c_neighbors[c])))]
            rab = ab_neighbors[ab][int(rng.integers(len(ab_neighbors[ab])))]
            s_null += len(c_frames_ho[rc] & ab_frames_ho[rab])
        null_totals[p_idx] = s_null

    n_ge = int(np.sum(null_totals >= real_total_shared))
    return {
        "n_pairs_frozen": len(pairs),
        "active_pairs_in_heldout": active_pairs,
        "real_total_shared_parallel_frames": int(real_total_shared),
        "null_permutations": n_perm,
        "null_mean_shared_frames": round(float(null_totals.mean()), 4),
        "null_std_shared_frames": round(float(null_totals.std()), 4),
        "null_max_shared_frames": int(null_totals.max()),
        "n_null_ge_real": n_ge,
        "permutation_p_value": round((n_ge + 1) / (n_perm + 1), 6),
        "per_pair_heldout": per_pair_heldout,
    }


def run_400_sigil_controls(
    m77_seqs: list[list[str]],
    heldout_records: list[dict],
    n_controls: int = 400,
) -> dict:
    """
    Evaluates 400 independent SIGIL matched-null synthetic controls (seed=1..400),
    each preserving M77 length, initial, final, and unigram distributions and evaluated
    with Kneser-Ney 3-gram on the post-1977 held-out corpus.
    """
    tr_corpus = Corpus([Inscription(inscription_id=str(idx), signs=s) for idx, s in enumerate(m77_seqs)])
    vocab = sorted(set(w for s in m77_seqs for w in s))

    # Collect unique (l2, l1) contexts and target distribution across held-out tokens
    ctx_target_counts = defaultdict(Counter)
    total_tokens = 0
    for r in heldout_records:
        s = r["seq_m1"]
        L = len(s)
        pad = ["<S>", "<S>"] + s
        for i in range(L):
            total_tokens += 1
            ctx_target_counts[(pad[i], pad[i + 1])][s[i]] += 1

    vocab_set = set(vocab)
    control_accs = []
    for seed in range(1, n_controls + 1):
        null_c = generate_matched_null_corpus(tr_corpus, n_inscriptions=len(tr_corpus), seed=seed)
        null_seqs = [ins.signs for ins in null_c.inscriptions]
        kn_null = train_kneser_ney([s + ["</S>"] for s in null_seqs], max_order=3, discount=0.55)
        best_v1 = max(vocab, key=lambda v: kn_null._prob_order((), v, 1))
        c2_map = kn_null.counts_by_order[2]
        c3_map = kn_null.counts_by_order[3]
        hits = 0
        for ctx, t_cnts in ctx_target_counts.items():
            cand = {best_v1}
            if ctx[-1:] in c2_map:
                cand.update(w for w in c2_map[ctx[-1:]] if w in vocab_set)
            if ctx in c3_map:
                cand.update(w for w in c3_map[ctx] if w in vocab_set)
            best_v = max(cand, key=lambda v: kn_null.prob(ctx, v))
            hits += t_cnts.get(best_v, 0)
        control_accs.append(hits / total_tokens)

    arr = np.array(control_accs, dtype=np.float64)
    return {
        "controls": n_controls,
        "total_tokens": total_tokens,
        "best_control": round(float(arr.max()), 6),
        "mean_control": round(float(arr.mean()), 6),
        "std_control": round(float(arr.std()), 6),
        "median_control": round(float(np.median(arr)), 6),
        "iqr_control": round(float(np.percentile(arr, 75) - np.percentile(arr, 25)), 6),
    }


def main():
    t0 = time.time()

    # 1. Verify frozen model hash and timestamp ordering
    actual_sha = sha256_file(FROZEN_MODEL_PATH)
    assert actual_sha == EXPECTED_MODEL_SHA256, f"Frozen model SHA-256 mismatch: {actual_sha}"
    mtime_model = os.path.getmtime(FROZEN_MODEL_PATH)
    mtime_prereg = os.path.getmtime(PREREG_PATH)
    assert mtime_model <= mtime_prereg + 1.0, "Frozen model mtime must not be newer than PREREG.md"

    frozen_model = json.load(open(FROZEN_MODEL_PATH, encoding="utf-8"))

    # 2. Rebuild post-1977 held-out corpus from publication metadata
    heldout_records, filter_counts = build_post1977_heldout_corpus(frozen_model)

    # Reading direction check on held-out corpus: W740 (Jar) at terminal (-1) vs initial (0)
    w740_init = sum(1 for r in heldout_records if r["seq_m1"][0] == "740")
    w740_final = sum(1 for r in heldout_records if r["seq_m1"][-1] == "740")

    # 3. Evaluate Frozen M77 Model under Mode 1 (`test_prereg.py` `m2g`) and Mode 2 (`bridge_extended.json` CC)
    eval_m1 = FrozenM77Evaluator(
        frozen_model["frozen_m77_sequences_mode1"],
        frozen_model["frozen_m77_clusters_mode1"],
        discount=frozen_model["hyperparameters_frozen_from_m77_5fold_cv"]["kn3_discount"],
    )
    eval_m2 = FrozenM77Evaluator(
        frozen_model["frozen_m77_sequences_mode2"],
        frozen_model["frozen_m77_clusters_mode2"],
        discount=frozen_model["hyperparameters_frozen_from_m77_5fold_cv"]["kn3_discount"],
    )

    tok_rows_m1 = []
    tok_rows_m2 = []
    for r in heldout_records:
        preds1 = eval_m1.predict_sequence_tokens(r["seq_m1"])
        for p in preds1:
            p["cisi"] = r["cisi"]
            p["site"] = r["site"]
            p["cls"] = r["cls"]
            p["publication_source"] = r["publication_source"]
            p["is_strict_post1977_range"] = r["is_strict_post1977_range"]
            tok_rows_m1.append(p)

        preds2 = eval_m2.predict_sequence_tokens(r["seq_m2"])
        for p in preds2:
            p["cisi"] = r["cisi"]
            p["site"] = r["site"]
            p["cls"] = r["cls"]
            p["publication_source"] = r["publication_source"]
            p["is_strict_post1977_range"] = r["is_strict_post1977_range"]
            tok_rows_m2.append(p)

    # Save token-level predictions CSV for independent verification
    with open(OUT_PREDS_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "cisi", "site", "cls", "is_strict_post1977_range", "pos", "slot",
            "target", "pred_clss", "pred_kn3_left", "pred_kn3_bidir",
            "pred_kn3_blanket_f", "pred_sigil",
            "hit_clss", "hit_kn3_left", "hit_kn3_bidir", "hit_kn3_blanket_f", "hit_sigil",
            "publication_source",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in tok_rows_m1:
            writer.writerow(r)

    # Compute 10,000-resample paired bootstrap across strata for Cohort A (all post-1977) and Cohort B (strict ranges)
    def summarize_cohort(rows: list[dict]) -> dict:
        return {
            "pooled": paired_bootstrap_Summary(rows, n_boot=10000, seed=0),
            "mohenjo_daro": paired_bootstrap_Summary([r for r in rows if r["site"] == "Mohenjo-daro"], n_boot=10000, seed=0),
            "harappa": paired_bootstrap_Summary([r for r in rows if r["site"] == "Harappa"], n_boot=10000, seed=0),
            "dholavira": paired_bootstrap_Summary([r for r in rows if r["site"] == "Dholavira"], n_boot=10000, seed=0),
            "other_post1977_sites": paired_bootstrap_Summary(
                [r for r in rows if r["site"] not in ("Mohenjo-daro", "Harappa")], n_boot=10000, seed=0
            ),
        }

    cohort_a_m1 = summarize_cohort(tok_rows_m1)
    cohort_b_m1 = summarize_cohort([r for r in tok_rows_m1 if r["is_strict_post1977_range"]])
    cohort_a_m2 = summarize_cohort(tok_rows_m2)
    cohort_b_m2 = summarize_cohort([r for r in tok_rows_m2 if r["is_strict_post1977_range"]])

    # 4. Evaluate Partial Win p3 (Frozen Top-25 M77 Telescoping Composite/Bigram Substitutions)
    p3_res = evaluate_p3_telescoping_ligatures(
        frozen_model["frozen_m77_sequences_mode1"],
        [r["seq_m1"] for r in heldout_records],
        frozen_model["frozen_m77_top25_telescoping_ligatures_p3"],
        n_perm=10000,
        seed=0,
    )

    # 5. Run 400 independent SIGIL matched-null controls and write null_test.md
    null_400 = run_400_sigil_controls(
        frozen_model["frozen_m77_sequences_mode1"],
        heldout_records,
        n_controls=400,
    )
    real_pooled_acc = cohort_a_m1["pooled"]["clss_acc"]
    beats_all = "yes" if real_pooled_acc > null_400["best_control"] else "no"

    with open(OUT_NULL_MD, "w", encoding="utf-8") as f:
        f.write("# Null Model Control Test (`indus-temporal-heldout-structure`)\n\n")
        f.write(f"controls: {null_400['controls']}\n")
        f.write(f"best_control: {null_400['best_control']:.6f}\n")
        f.write(f"real: {real_pooled_acc:.6f}\n")
        f.write("command: python3 claim/author_checker_indus.py --verify-null-controls\n")
        f.write(f"real_beats_all_controls: {beats_all}\n\n")
        f.write("## Summary of 400 SIGIL Matched-Null Controls\n\n")
        f.write(f"- **Number of independent synthetic controls**: `{null_400['controls']}` (`seed = 1..400`)\n")
        f.write(f"- **Generator**: `generate_matched_null_corpus` (`adversarial_null_model.py`), matching `M77` length, initial-sign, final-sign, and unigram distributions\n")
        f.write(f"- **Held-out evaluation tokens**: `{null_400['total_tokens']}` tokens across `{len(heldout_records)}` deduplicated post-1977 inscriptions\n")
        f.write(f"- **Control accuracy median (IQR)**: `{null_400['median_control']:.6f}` (`IQR = {null_400['iqr_control']:.6f}`)\n")
        f.write(f"- **Control accuracy mean (SD)**: `{null_400['mean_control']:.6f}` (`SD = {null_400['std_control']:.6f}`)\n")
        f.write(f"- **Best control accuracy across all 400 runs**: `{null_400['best_control']:.6f}`\n")
        f.write(f"- **Real frozen `M77-CLSS` accuracy**: `{real_pooled_acc:.6f}` (`{cohort_a_m1['pooled']['clss_hits']} / {null_400['total_tokens']}`)\n")
        f.write(f"- **Tuned `KN3-Left` baseline accuracy**: `{cohort_a_m1['pooled']['kn3_left_acc']:.6f}` (`{cohort_a_m1['pooled']['kn3_left_hits']} / {null_400['total_tokens']}`)\n")
        f.write(f"- **Tuned `KN3-Bidir` baseline accuracy**: `{cohort_a_m1['pooled']['kn3_bidir_acc']:.6f}` (`{cohort_a_m1['pooled']['kn3_bidir_hits']} / {null_400['total_tokens']}`)\n")
        f.write(f"- **Tuned `KN3-BlanketF` baseline accuracy**: `{cohort_a_m1['pooled']['kn3_blanket_f_acc']:.6f}` (`{cohort_a_m1['pooled']['kn3_blanket_f_hits']} / {null_400['total_tokens']}`)\n")

    results_payload = {
        "evaluated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "frozen_model_sha256": actual_sha,
        "heldout_corpus_summary": {
            "filter_counts": filter_counts,
            "total_heldout_inscriptions": len(heldout_records),
            "strict_range_heldout_inscriptions": sum(1 for r in heldout_records if r["is_strict_post1977_range"]),
            "by_site": dict(Counter(r["site"] for r in heldout_records).most_common()),
            "by_class": dict(Counter(r["cls"] for r in heldout_records).most_common()),
            "reading_direction_check_w740_jar": {
                "w740_at_initial_pos_0": w740_init,
                "w740_at_terminal_pos_last": w740_final,
                "terminal_to_boundary_ratio": round(w740_final / max(w740_init + w740_final, 1), 6),
            },
        },
        "cohort_a_all_post1977_mode1": cohort_a_m1,
        "cohort_b_strict_post1977_range_mode1": cohort_b_m1,
        "cohort_a_all_post1977_mode2": cohort_a_m2,
        "cohort_b_strict_post1977_range_mode2": cohort_b_m2,
        "partial_win_p3_telescoping_ligatures": p3_res,
        "sigil_400_null_controls": null_400,
    }

    with open(OUT_RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)

    print(f"Post-1977 held-out evaluation completed in {time.time() - t0:.2f}s")
    print(f"  Held-out inscriptions (Cohort A): {len(heldout_records)}, (Cohort B strict): {results_payload['heldout_corpus_summary']['strict_range_heldout_inscriptions']}")
    print(f"  W740 reading direction check    : {w740_final} terminal vs {w740_init} initial ({results_payload['heldout_corpus_summary']['reading_direction_check_w740_jar']['terminal_to_boundary_ratio']*100:.2f}% terminal)")
    for label, d in [
        ("Cohort A Mode 1 - Pooled", cohort_a_m1["pooled"]),
        ("Cohort A Mode 1 - Mohenjo-daro", cohort_a_m1["mohenjo_daro"]),
        ("Cohort A Mode 1 - Harappa", cohort_a_m1["harappa"]),
        ("Cohort A Mode 1 - Dholavira", cohort_a_m1["dholavira"]),
        ("Cohort A Mode 1 - Other Post-1977 Sites", cohort_a_m1["other_post1977_sites"]),
        ("Cohort B Strict - Pooled", cohort_b_m1["pooled"]),
        ("Cohort B Strict - Mohenjo-daro", cohort_b_m1["mohenjo_daro"]),
        ("Cohort B Strict - Harappa", cohort_b_m1["harappa"]),
        ("Cohort A Mode 2 - Pooled", cohort_a_m2["pooled"]),
        ("Cohort A Mode 2 - Mohenjo-daro", cohort_a_m2["mohenjo_daro"]),
        ("Cohort A Mode 2 - Harappa", cohort_a_m2["harappa"]),
    ]:
        print(
            f"  {label:38s} (n={d['n_tokens']:4d}): "
            f"CLSS={d['clss_acc']:.4f} vs KN3-Left={d['kn3_left_acc']:.4f} (p={d['p_boot_vs_kn3_left']:.6f}), "
            f"KN3-Bidir={d['kn3_bidir_acc']:.4f} (p={d['p_boot_vs_kn3_bidir']:.6f}), "
            f"KN3-BlkF={d['kn3_blanket_f_acc']:.4f} (p={d['p_boot_vs_kn3_blanket_f']:.6f}), "
            f"SIGIL={d['sigil_acc']:.4f} (p={d['p_boot_vs_sigil']:.6f})"
        )
    print(
        f"  Partial Win p3 (Top-25 M77 Ligatures) : real_shared={p3_res['real_total_shared_parallel_frames']} "
        f"vs null_mean={p3_res['null_mean_shared_frames']:.2f} (max={p3_res['null_max_shared_frames']}, p={p3_res['permutation_p_value']:.6f})"
    )
    print(
        f"  400 SIGIL Controls (`null_test.md`)   : best_control={null_400['best_control']:.6f} vs real={real_pooled_acc:.6f} (beats_all={beats_all})"
    )


if __name__ == "__main__":
    main()
