#!/usr/bin/env python3
"""ANALOGIST lens system (run 2026-10-18-0104): memory-based column prediction over multiple alignments.

train  (per family, from the manifest's training file only):
  1. segment similarity: a fixed sound-class prior refined by iterated PMI over pairwise alignments of the reflexes
     inside each training cognate set (Jaeger-style iterated alignment);
  2. for every training set c and every attested target language t: progressive multiple alignment of the other
     reflexes of c (exactly the procedure used at prediction time on a test row's visible reflexes), then the target
     reflex aligned to that profile; every MSA column becomes one instance: features = segment / left / right
     neighbour of every source language (missing language = unknown), label = the target chunk aligned to it;
  3. per target language: gain-ratio feature weights (IB1-IG, TiMBL) and the instance matrix.
predict: MSA of the row's visible reflexes, per column a weighted-overlap kNN vote over the target's training
  columns (analogy: an aligned column of the row is solved by the training columns it most resembles), n-best by a
  beam over columns, final string by minimum Bayes risk under normalised edit distance (optional, config).
Deterministic, standard library + numpy. Hyperparameters in config.json next to this file.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import argparse
import json
import math
import pickle
import sys
import unicodedata
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = {
    "gap": -1.5, "endgap": -0.75, "pmi_iters": 2, "w_init": 0.5, "pmi_a": 1.0,
    "ctx": 1, "posfeat": 1, "lam": 0.0, "k": 1, "beta": 2.0, "weighting": "gr",
    "nbest": 0, "mbr": 0, "mbr_temp": 1.0, "pool_pmi": 0,
    "wcur": 1.0, "wctx": 1.0, "wpos": 1.0, "guide": "pair",
    "mix": 0.0, "psv_a": 1.0, "psv_ctx": 1, "psv_rpow": 1.0, "psv_eps": 0.01, "psv_comb": "lin", "psv_temp": 1.0,
    "psv_rel": "gr", "psv_logit0": 1.0, "learn_w": 0, "lw_iters": 150, "lw_reg": 0.01,
    "pool_fb": 1, "pool_w": 0.5, "knn_fb": 0, "a_id": 0.0, "copy_fb": 0, "copy_w": 0.5,
    "pmi_maxpairs": 0, "gorder_every": 1, "lw_maxinst": 0, "lw_maxK": 1000,
    "a_pool": 0.0, "psv_D": 0.0, "lm": 0.0, "lm_order": 3, "lm_ratio": 0, "src_cand": 0.0, "tune": 0, "tune_grid": [], "tune_max_rows": 1500, "jk": 0, "jk_min": 2, "jk_pow": 1.0, "jk_mode": "pair", "copy_cand": 0.0, "cand_ev": 0, "aid_learn": 0, "aid_grid": [0.0, 0.5, 1.0, 2.0, 4.0, 8.0],
    "nb": 0, "nb_min": 2, "nb_frac": 1.0, "nb_w": 0.5, "nb_pow": 1.0,
}


def load_cfg(path=None):
    cfg = dict(DEFAULTS)
    p = path or os.path.join(HERE, "config.json")
    if os.path.exists(p):
        with open(p) as f:
            cfg.update(json.load(f))
    return cfg


# ---------------------------------------------------------------- io
def load(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    h = lines[0].split("\t")
    langs = h[1:]
    data = {}
    for ln in lines[1:]:
        r = ln.split("\t") + [""] * len(h)
        data[r[0]] = {l: r[i + 1].split() for i, l in enumerate(langs)}
    return langs, data


# ---------------------------------------------------------------- sound classes and similarity
TONE_CH = set("0123456789⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉˥˦˧˨˩")
VOW = set("aeiouyɑɐɒæɛɜəɘɤɨɪɯɵøœɔʊʉʌʏɞɶɚɝɿʅ")


def base(seg):
    for ch in unicodedata.normalize("NFD", seg):
        if unicodedata.category(ch) in ("Ll", "Lu", "Lo"):
            return ch
    return seg[:1]


def sclass(seg):
    if seg and all(ch in TONE_CH for ch in seg):
        return "T"
    b = base(seg)
    if b in VOW:
        return "V"
    if b.isalpha():
        return "C"
    return "X"


def init_sim(x, y):
    if x == y:
        return 3.0
    cx, cy = sclass(x), sclass(y)
    if cx in "TX" or cy in "TX":
        return 1.0 if cx == cy else -4.0
    if base(x) == base(y):
        return 2.0
    if cx == cy:
        return 0.5 if cx == "V" else 0.0
    return -1.5


class Sim:
    def __init__(self, pmi, w_init):
        self.pmi = pmi
        self.w = w_init
        self.memo = {}

    def __call__(self, x, y):
        k = (x, y)
        v = self.memo.get(k)
        if v is None:
            p = self.pmi.get(k)
            if p is None:
                p = self.default(x, y)
            v = self.w * init_sim(x, y) + p
            self.memo[k] = v
        return v

    def default(self, x, y):
        d = self.pmi.get("__unseen__")
        if d is None:
            return 0.0
        cx = d["cnt"].get(x, 0)
        cy = d["cnt"].get(y, 0)
        e = cx * cy / max(d["N"], 1.0)
        return math.log(d["a"] / (e + d["a"]))


# ---------------------------------------------------------------- alignment of a sequence to a profile
def align_profile(seq, cols, sim, gap, endgap):
    """seq: list of segments; cols: list of lists of segments (non-gap entries of each profile column).
    Returns (score, path) with path ops: ("d", i, j), ("i", i, None) seq seg vs gap, ("c", None, j) column vs gap."""
    n, m = len(seq), len(cols)
    ccols = []
    for col in cols:
        c = Counter(col)
        ccols.append((sorted(c.items()), float(len(col))))
    sc = [[sum(k * sim(x, y) for y, k in cc) / tot for cc, tot in ccols] for x in seq]
    NEG = -1e18
    D = [[NEG] * (m + 1) for _ in range(n + 1)]
    B = [[0] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(1, n + 1):
        D[i][0] = D[i - 1][0] + endgap
        B[i][0] = 1
    for j in range(1, m + 1):
        D[0][j] = D[0][j - 1] + endgap
        B[0][j] = 2
    for i in range(1, n + 1):
        Di, Dp, Bi, sci = D[i], D[i - 1], B[i], sc[i - 1]
        gi = endgap if i == n else gap
        for j in range(1, m + 1):
            gj = endgap if j == m else gap
            best = Dp[j - 1] + sci[j - 1]
            b = 0
            v = Dp[j] + gj        # seq seg i vs gap (vertical move); in last column it is an end gap
            if v > best:
                best, b = v, 1
            v = Di[j - 1] + gi    # column j vs gap (horizontal move); in last row it is an end gap
            if v > best:
                best, b = v, 2
            Di[j] = best
            Bi[j] = b
    path = []
    i, j = n, m
    while i > 0 or j > 0:
        b = B[i][j]
        if b == 0:
            path.append(("d", i - 1, j - 1)); i -= 1; j -= 1
        elif b == 1:
            path.append(("i", i - 1, None)); i -= 1
        else:
            path.append(("c", None, j - 1)); j -= 1
    path.reverse()
    return D[n][m], path


def pair_score(a, b, sim, gap, endgap):
    s, _ = align_profile(a, [[y] for y in b], sim, gap, endgap)
    return s


def msa(order, seqs, sim, gap, endgap):
    """Progressive alignment in the given order. Returns rows: dict lang -> list (segment or None)."""
    first = order[0]
    rows = {first: list(seqs[first])}
    L = len(seqs[first])
    for l in order[1:]:
        cols = [[rows[k][j] for k in rows if rows[k][j] is not None] for j in range(L)]
        _, path = align_profile(seqs[l], cols, sim, gap, endgap)
        new = {k: [] for k in rows}
        mine = []
        for op, i, j in path:
            if op == "d":
                for k in rows:
                    new[k].append(rows[k][j])
                mine.append(seqs[l][i])
            elif op == "i":
                for k in rows:
                    new[k].append(None)
                mine.append(seqs[l][i])
            else:
                for k in rows:
                    new[k].append(rows[k][j])
                mine.append(None)
        new[l] = mine
        rows = new
        L = len(mine)
    return rows


def guide_order(langs_present, pmat, lang_index):
    """langs_present: list of languages; pmat: dict (a,b)->normalised pair score. Most central first."""
    cen = {}
    for a in langs_present:
        cen[a] = sum(pmat[(a, b)] if (a, b) in pmat else pmat[(b, a)] for b in langs_present if b != a)
    return sorted(langs_present, key=lambda a: (-cen[a], lang_index[a]))


def norm_pair(a, b, sim, gap, endgap):
    s = pair_score(a, b, sim, gap, endgap)
    sa = sum(sim(x, x) for x in a)
    sb = sum(sim(y, y) for y in b)
    return s / max(1e-9, 0.5 * (sa + sb))


# ---------------------------------------------------------------- PMI learning
def pair_list(n, maxpairs):
    """All index pairs if few, else a deterministic spread subset (offsets 1, 2, ... cyclically)."""
    allp = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if maxpairs <= 0 or len(allp) <= maxpairs:
        return allp
    out = []
    seen = set()
    off = 1
    while len(out) < maxpairs and off < n:
        for i in range(n):
            j = (i + off) % n
            p = (min(i, j), max(i, j))
            if p not in seen and p[0] != p[1]:
                seen.add(p)
                out.append(p)
                if len(out) >= maxpairs:
                    break
        off += 1
    return sorted(out)


def learn_pmi(sets, cfg):
    """sets: list of dict lang->seq (attested only)."""
    pmi = {}
    for it in range(cfg["pmi_iters"]):
        sim = Sim(pmi, cfg["w_init"])
        cnt = Counter()
        single = Counter()
        for s in sets:
            ls = sorted(s)
            for x_i, y_i in pair_list(len(ls), cfg["pmi_maxpairs"]):
                if True:
                    a, b = s[ls[x_i]], s[ls[y_i]]
                    _, path = align_profile(a, [[y] for y in b], sim, cfg["gap"], cfg["endgap"])
                    for op, i, j in path:
                        if op == "d":
                            cnt[(a[i], b[j])] += 1
                            cnt[(b[j], a[i])] += 1
                            single[a[i]] += 1
                            single[b[j]] += 1
        N = sum(single.values()) / 2.0
        a_ = cfg["pmi_a"]
        new = {}
        for (x, y), c in cnt.items():
            e = single[x] * single[y] / max(2.0 * N, 1.0)
            new[(x, y)] = math.log((c + a_) / (e + a_))
        new["__unseen__"] = {"cnt": dict(single), "N": 2.0 * N, "a": a_}
        pmi = new
    return pmi


# ---------------------------------------------------------------- instances
def column_features(rows, L, lang_index, nl, vocab, ctx, posfeat, add=False):
    """Return list of feature vectors (lists of ints, -1 missing) for each column of an MSA."""
    nf = nl * (1 + 2 * ctx) + (2 if posfeat else 0)
    out = []
    enc = {}

    def code(v):
        c = vocab.get(v)
        if c is None:
            if add:
                c = len(vocab)
                vocab[v] = c
            else:
                c = -2
        return c

    # per language: positions of non-gap entries
    nong = {l: [j for j in range(L) if r[j] is not None] for l, r in rows.items()}
    for j in range(L):
        f = [-1] * nf
        for l, r in rows.items():
            li = lang_index[l]
            base_ = li * (1 + 2 * ctx)
            f[base_] = code(r[j] if r[j] is not None else "-")
            if ctx:
                idx = nong[l]
                left = [r[q] for q in idx if q < j]
                right = [r[q] for q in idx if q > j]
                for c in range(ctx):
                    f[base_ + 1 + 2 * c] = code(left[-1 - c] if len(left) > c else "#")
                    f[base_ + 2 + 2 * c] = code(right[c] if len(right) > c else "#")
        if posfeat:
            f[nf - 2] = code("P%d" % min(j, 4))
            f[nf - 1] = code("Q%d" % min(L - 1 - j, 4))
        out.append(f)
    return out


def target_labels(tseq, rows, L, sim, gap, endgap):
    cols = [[rows[k][j] for k in rows if rows[k][j] is not None] for j in range(L)]
    _, path = align_profile(tseq, cols, sim, gap, endgap)
    labels = [[] for _ in range(L)]
    prefix = []
    last = -1
    for op, i, j in path:
        if op == "d":
            labels[j].append(tseq[i]); last = j
        elif op == "i":
            if last < 0:
                prefix.append(tseq[i])
            else:
                labels[last].append(tseq[i])
        else:
            last = j
    if prefix:
        labels[0] = prefix + labels[0]
    return [" ".join(x) for x in labels]


def gain_ratio(X, y, nlab):
    n, m = X.shape
    w = np.zeros(m)
    for f in range(m):
        col = X[:, f]
        mask = col >= 0
        if mask.sum() < 2:
            continue
        v = col[mask]
        yy = y[mask]
        tot = len(v)
        cy = Counter(yy.tolist())
        H = -sum(c / tot * math.log(c / tot) for c in cy.values())
        joint = defaultdict(Counter)
        for a, b in zip(v.tolist(), yy.tolist()):
            joint[a][b] += 1
        Hc = 0.0
        SI = 0.0
        for a, cb in joint.items():
            na = sum(cb.values())
            pa = na / tot
            SI -= pa * math.log(pa)
            Hc += pa * -sum(c / na * math.log(c / na) for c in cb.values())
        ig = H - Hc
        w[f] = ig / SI if SI > 1e-12 else 0.0
    return w


def info_gain(X, y, nlab):
    n, m = X.shape
    w = np.zeros(m)
    for f in range(m):
        col = X[:, f]
        mask = col >= 0
        if mask.sum() < 2:
            continue
        v = col[mask]
        yy = y[mask]
        tot = len(v)
        cy = Counter(yy.tolist())
        H = -sum(c / tot * math.log(c / tot) for c in cy.values())
        joint = defaultdict(Counter)
        for a, b in zip(v.tolist(), yy.tolist()):
            joint[a][b] += 1
        Hc = sum(sum(cb.values()) / tot * -sum(c / sum(cb.values()) * math.log(c / sum(cb.values()))
                                               for c in cb.values()) for cb in joint.values())
        w[f] = H - Hc
    return w


def train_family(path, cfg):
    langs, data = load(path)
    lang_index = {l: i for i, l in enumerate(langs)}
    nl = len(langs)
    sets = []
    for key in sorted(data):
        s = {l: data[key][l] for l in langs if data[key][l]}
        if s:
            sets.append(s)
    pmi = learn_pmi(sets, cfg)
    sim = Sim(pmi, cfg["w_init"])
    gap, endgap = cfg["gap"], cfg["endgap"]
    vocab = {"-": 0, "#": 1}
    inst = defaultdict(lambda: ([], []))
    rng = defaultdict(list)
    pms = []
    for si, s in enumerate(sets):
        ls = sorted(s, key=lambda l: lang_index[l])
        pmat = {}
        if cfg["guide"] != "global" or si % cfg["gorder_every"] == 0:
            for x_i in range(len(ls)):
                for y_i in range(x_i + 1, len(ls)):
                    pmat[(ls[x_i], ls[y_i])] = norm_pair(s[ls[x_i]], s[ls[y_i]], sim, gap, endgap)
        pms.append(pmat)
    # global guide: languages ranked by mean normalised pair score with the others (most central first)
    tot, num = Counter(), Counter()
    for pmat in pms:
        for (a, b), v in pmat.items():
            tot[a] += v; tot[b] += v; num[a] += 1; num[b] += 1
    grank = {l: (-(tot[l] / num[l]) if num[l] else 0.0, lang_index[l]) for l in langs}
    gorder = sorted(langs, key=lambda l: grank[l])
    for s, pmat in zip(sets, pms):
        ls = sorted(s, key=lambda l: lang_index[l])
        if len(ls) < 2:
            continue
        for t in ls:
            src = [l for l in ls if l != t]
            if cfg["guide"] == "global":
                order = [l for l in gorder if l in src]
            else:
                order = guide_order(src, pmat, lang_index)
            rows = msa(order, s, sim, gap, endgap)
            L = len(rows[order[0]])
            feats = column_features(rows, L, lang_index, nl, vocab, cfg["ctx"], cfg["posfeat"], add=True)
            labs = target_labels(s[t], rows, L, sim, gap, endgap)
            a0 = len(inst[t][0])
            inst[t][0].extend(feats)
            inst[t][1].extend(labs)
            rng[t].append((len(ls), a0, len(inst[t][0]), tuple(s[t]), {l: s[l] for l in src}))
    model = {"langs": langs, "vocab": vocab, "pmi": pmi, "targets": {}, "gorder": gorder}
    # whole-set exact-match index for set-level analogy: (lang, reflex) -> set ids; attested-language bitmask per set
    nb_index = defaultdict(list)
    masks = []
    for si, s in enumerate(sets):
        mk = 0
        for l, seq in s.items():
            nb_index[(l, " ".join(seq))].append(si)
            mk |= 1 << lang_index[l]
        masks.append(mk)
    model["lm"] = {t: train_lm([s[t] for s in sets if t in s]) for t in langs}
    model["nb_index"] = dict(nb_index)
    model["nb_masks"] = masks
    model["nb_sets"] = [{l: " ".join(v) for l, v in s.items()} for s in sets]
    for t in langs:
        if t not in inst or not inst[t][0]:
            continue
        X = np.array(inst[t][0], dtype=np.int32)
        labs = inst[t][1]
        segs = {v for v in vocab if v != "#" and not (len(v) == 2 and v[0] in "PQ" and v[1].isdigit())}
        labset = sorted(set(labs) | {("" if v == "-" else v) for v in segs})
        lid = {lb: i for i, lb in enumerate(labset)}
        idlab = {vocab[v]: lid["" if v == "-" else v] for v in segs}
        y = np.array([lid[lb] for lb in labs], dtype=np.int32)
        w = gain_ratio(X, y, len(labset)) if cfg["weighting"] == "gr" else info_gain(X, y, len(labset))
        tabs = source_tables(X, y, langs, lang_index, t, cfg["ctx"])
        ent = {"X": X, "y": y, "labels": labset, "w": w, "tabs": tabs, "idlab": idlab,
               "pool": pooled_table(X, y, langs, lang_index, t, cfg["ctx"])}
        if cfg["aid_learn"]:
            ent["aid"] = learn_aid(X, y, tabs, ent["pool"], langs, lang_index, t, cfg, idlab)
        if cfg["learn_w"]:
            ent["lw"], ent["mw"] = learn_pool_weights(X, y, tabs, langs, lang_index, t, cfg, idlab,
                                                      ent.get("aid"), ent["pool"])
        model["targets"][t] = ent
    if cfg["tune"] and cfg["tune_grid"]:
        model["tuned"], model["tune_log"] = tune_family(model, rng, cfg)
    return model


def set_delta(Xt, a0, a1, langs, lang_index, t, ctx):
    """Counts contributed by training columns a0..a1-1 (one training set) to each source's back-off tables."""
    per = 1 + 2 * ctx
    X, y = Xt["X"], Xt["y"]
    out = {}
    for l in langs:
        if l == t:
            continue
        c0 = lang_index[l] * per
        d = defaultdict(Counter)
        for q in range(a0, a1):
            cur = int(X[q, c0])
            if cur < 0:
                continue
            lab = int(y[q])
            d[(1, cur)][lab] += 1
            if ctx:
                Lv, Rv = int(X[q, c0 + 1]), int(X[q, c0 + 2])
                d[(2, (cur, Lv))][lab] += 1
                d[(3, (cur, Rv))][lab] += 1
                d[(4, (cur, Lv, Rv))][lab] += 1
        if d:
            out[l] = d
    return out


def tune_family(fm, rng, cfg):
    """Per-family choice of prediction settings by leave-one-set-out decoding of training rows: each chosen training
    set (most complete first, like the organisers' test split) is removed from the target's tables, its row is decoded
    under every setting of tune_grid, and the setting with the lowest language-mean NED (unit-cost ED / max length)
    is kept."""
    langs = fm["langs"]
    lang_index = {l: i for i, l in enumerate(langs)}
    inv = {v: k for k, v in fm["vocab"].items()}
    per = 1 + 2 * cfg["ctx"]
    items = []
    for t, lst in rng.items():
        if t not in fm["targets"]:
            continue
        for (nls, a0, a1, gold, srcs) in lst:
            items.append((-nls, t, a0, a1, gold, srcs))
    items.sort(key=lambda z: (z[0], lang_index[z[1]], z[2]))
    if cfg["tune_max_rows"] and len(items) > cfg["tune_max_rows"]:
        items = items[: cfg["tune_max_rows"]]
    scores = [defaultdict(list) for _ in cfg["tune_grid"]]
    for (_, t, a0, a1, gold, srcs) in items:
        Xt = fm["targets"][t]
        feats = [[int(v) for v in Xt["X"][q]] for q in range(a0, a1)]
        mrows = {}
        for l in srcs:
            c0 = lang_index[l] * per
            mrows[l] = [None if inv.get(f[c0]) in (None, "-") else inv[f[c0]] for f in feats]
        deltas = set_delta(Xt, a0, a1, langs, lang_index, t, cfg["ctx"])
        src = [l for l in langs if l in srcs]
        pre = (src, srcs, feats, mrows)
        for gi, ov in enumerate(cfg["tune_grid"]):
            c = dict(cfg)
            c.update(ov)
            c["_lm_minus"] = gold
            pred = predict_row(fm, None, t, None, c, pre=pre, deltas=deltas, excl=(a0, a1))
            scores[gi][t].append(edit_ned(pred, list(gold)))
    res = []
    for gi, sc in enumerate(scores):
        if not sc:
            continue
        res.append(sum(sum(v) / len(v) for v in sc.values()) / len(sc))
    if not res:
        return {}, []
    best = min(range(len(res)), key=lambda i: (res[i] - 1e-12 * 0, i))
    return dict(cfg["tune_grid"][best]), res


def pool_prior(pool, cur, minus_lab=None, minus_n=0):
    """Language-agnostic prior for target t given a source segment code: normalised pooled unigram counts
    (optionally with minus_n counts of minus_lab removed, for leave-one-out)."""
    if pool is None:
        return None
    c = pool[0].get(cur)
    if not c:
        return None
    if minus_n and minus_lab is not None:
        c = dict(c)
        c[minus_lab] = c.get(minus_lab, 0) - minus_n
        c = {k: v for k, v in c.items() if v > 0}
        if not c:
            return None
    n = float(sum(c.values()))
    return {k: v / n for k, v in c.items()}


def train_lm(words):
    """Segment trigram counts of one language's training reflexes (Witten-Bell interpolation at query time)."""
    c1, c2, c3 = Counter(), defaultdict(Counter), defaultdict(Counter)
    for w in words:
        seq = ["<s>", "<s>"] + list(w) + ["</s>"]
        for i in range(2, len(seq)):
            c1[seq[i]] += 1
            c2[seq[i - 1]][seq[i]] += 1
            c3[(seq[i - 2], seq[i - 1])][seq[i]] += 1
    return {"c1": dict(c1), "c2": {k: dict(v) for k, v in c2.items()}, "c3": {k: dict(v) for k, v in c3.items()},
            "N1": sum(c1.values()), "V": len(c1) + 1}


def lm_minus(lm, word):
    """Copy of the LM counts with one word's n-grams removed (leave-one-out)."""
    seq = ["<s>", "<s>"] + list(word) + ["</s>"]
    c1 = dict(lm["c1"]); c2 = dict(lm["c2"]); c3 = dict(lm["c3"])
    for i in range(2, len(seq)):
        w, h1, h2 = seq[i], seq[i - 1], seq[i - 2]
        c1[w] = c1.get(w, 0) - 1
        if c1[w] <= 0:
            del c1[w]
        d = dict(c2.get(h1, {})); d[w] = d.get(w, 0) - 1
        c2[h1] = {k: v for k, v in d.items() if v > 0}
        d = dict(c3.get((h2, h1), {})); d[w] = d.get(w, 0) - 1
        c3[(h2, h1)] = {k: v for k, v in d.items() if v > 0}
    return {"c1": c1, "c2": c2, "c3": c3, "N1": sum(c1.values()), "V": lm["V"]}


def lm_logp(lm, h2, h1, w, order=3):
    c1 = lm["c1"]
    p = (c1.get(w, 0) + 1.0) / (lm["N1"] + lm["V"])
    if order >= 2:
        d = lm["c2"].get(h1)
        if d:
            n = sum(d.values()); T = len(d)
            p = (d.get(w, 0) + T * p) / (n + T)
    if order >= 3:
        d = lm["c3"].get((h2, h1))
        if d:
            n = sum(d.values()); T = len(d)
            p = (d.get(w, 0) + T * p) / (n + T)
    return math.log(p)


def backoff_dist(T, cur, Lv, Rv, a, use_ctx, minus=None, ident=None, a_id=0.0, prior=None, a_pr=0.0, D=0.0):
    """Interpolated label distribution of one source; minus = label to leave out (one count) for LOO;
    ident = label id of the identity (copy) correspondence, mixed in with pseudo-count a_id;
    prior = label distribution (pooled over sources) mixed in with pseudo-count a_pr."""
    pri = {}
    if ident is not None and a_id > 0:
        pri[ident] = a_id
    if prior and a_pr > 0:
        for k, v in prior.items():
            pri[k] = pri.get(k, 0.0) + a_pr * v

    def prior_only():
        if not pri:
            return None
        z = sum(pri.values())
        return {k: v / z for k, v in pri.items()}

    if T is None:
        return prior_only()
    T1, T2L, T2R, T3 = T[:4]

    def get(tab, key, lev=0):
        c = tab.get(key)
        if c is None:
            return None
        if minus is None:
            return c
        if isinstance(minus, dict):
            dd = minus.get((lev, key))
            if not dd:
                return c
            c = dict(c)
            for k, v in dd.items():
                c[k] = c.get(k, 0) - v
            return {k: v for k, v in c.items() if v > 0}
        c = dict(c)
        c[minus] -= 1
        return {k: v for k, v in c.items() if v > 0}

    c1 = get(T1, cur, 1)
    if not c1:
        return prior_only()
    n1 = sum(c1.values())
    if pri:
        c1 = dict(c1)
        for k, v in pri.items():
            c1[k] = c1.get(k, 0) + v
            n1 += v
    P = {k: v / n1 for k, v in c1.items()}
    if use_ctx:
        ip = _interp_ad if D > 0 else _interp
        aa = D if D > 0 else a
        PL = ip(get(T2L, (cur, Lv), 2), P, aa)
        PR = ip(get(T2R, (cur, Rv), 3), P, aa)
        P2 = {k: 0.5 * (PL.get(k, 0.0) + PR.get(k, 0.0)) for k in set(PL) | set(PR)}
        P = ip(get(T3, (cur, Lv, Rv), 4), P2, aa)
    return P


def _interp_ad(cnt, prior, D):
    """Absolute discounting (Ney, Essen and Kneser 1994): every seen count loses D, the freed mass goes to the prior."""
    if not cnt:
        return prior
    n = float(sum(cnt.values()))
    u = sum(1 for v in cnt.values() if v > 0)
    lam = min(1.0, D * u / n)
    out = {k: lam * v for k, v in prior.items()}
    for k, v in cnt.items():
        out[k] = out.get(k, 0.0) + max(v - D, 0.0) / n
    z = sum(out.values())
    return {k: v / z for k, v in out.items()}


def learn_aid(X, y, tabs, pool, langs, lang_index, t, cfg, idlab):
    """Per-source identity pseudo-count chosen from a grid by leave-one-out log-likelihood of the training columns."""
    per = 1 + 2 * cfg["ctx"]
    use_ctx = bool(cfg["ctx"] and cfg["psv_ctx"])
    eps = cfg["psv_eps"]
    out = {}
    src_cols = [lang_index[l] * per for l in langs if l != t]
    for l in langs:
        if l == t or l not in tabs:
            continue
        c0 = lang_index[l] * per
        idx = np.nonzero(X[:, c0] >= 0)[0].tolist()
        best = None
        for g in cfg["aid_grid"]:
            ll = 0.0
            for q in idx:
                cur = int(X[q, c0]); lab = int(y[q])
                Lv, Rv = (int(X[q, c0 + 1]), int(X[q, c0 + 2])) if cfg["ctx"] else (None, None)
                pr = None
                if cfg["a_pool"] > 0:
                    mn = sum(1 for cc in src_cols if int(X[q, cc]) == cur)
                    pr = pool_prior(pool, cur, lab, mn)
                P = backoff_dist(tabs[l], cur, Lv, Rv, cfg["psv_a"], use_ctx, minus=lab, ident=idlab.get(cur),
                                 a_id=g, prior=pr, a_pr=cfg["a_pool"], D=cfg["psv_D"])
                ll += math.log((P.get(lab, 0.0) if P else 0.0) + eps)
            if best is None or ll > best[0] + 1e-9:
                best = (ll, g)
        out[l] = best[1] if best else cfg["a_id"]
    return out


def jk_dist(X, y, cols, vals, cfg, exclude=None):
    """Joint-match expert (whole-column analogy): training columns of this target vote their label with a weight
    growing with the number of visible sources whose aligned segment equals the row's (only columns matching at
    least jk_min sources vote)."""
    if len(cols) < cfg["jk_min"]:
        return None
    m = (X[:, cols] == np.asarray(vals)[None, :]).sum(axis=1).astype(np.float64)
    if exclude is not None:
        m[exclude] = 0.0
    if cfg["jk_mode"] == "pair":
        w = np.where(m >= cfg["jk_min"], m * (m - 1) / 2.0, 0.0)
    else:
        w = np.where(m >= cfg["jk_min"], (m / len(cols)) ** cfg["jk_pow"], 0.0)
    tot = w.sum()
    if tot <= 0:
        return None
    nz = np.nonzero(w)[0]
    out = defaultdict(float)
    for q in nz.tolist():
        out[int(y[q])] += w[q] / tot
    return dict(out)


def learn_pool_weights(X, y, tabs, langs, lang_index, t, cfg, idlab=None, aid=None, pool=None):
    """Log-linear pooling weights of the sources for target t, fit on leave-one-out expert distributions of the
    training columns (stacking). Returns dict lang -> weight >= 0."""
    per = 1 + 2 * cfg["ctx"]
    src = [l for l in langs if l != t and l in tabs]
    if not src:
        return {}
    S = len(src)
    use_ctx = bool(cfg["ctx"] and cfg["psv_ctx"])
    eps = cfg["psv_eps"]
    rows = []
    nq = X.shape[0]
    step = max(1, int(math.ceil(nq / cfg["lw_maxinst"]))) if cfg["lw_maxinst"] > 0 else 1
    for q in range(0, nq, step):
        lab = int(y[q])
        dists = {}
        for si, l in enumerate(src):
            c0 = lang_index[l] * per
            cur = int(X[q, c0])
            if cur < 0:
                continue
            Lv, Rv = (int(X[q, c0 + 1]), int(X[q, c0 + 2])) if cfg["ctx"] else (None, None)
            pr = None
            if cfg["a_pool"] > 0:
                mn = sum(1 for l2 in src if int(X[q, lang_index[l2] * per]) == cur)
                pr = pool_prior(pool, cur, lab, mn)
            P = backoff_dist(tabs[l], cur, Lv, Rv, cfg["psv_a"], use_ctx, minus=lab,
                             ident=(idlab or {}).get(cur), a_id=(aid or {}).get(l, cfg["a_id"]),
                             prior=pr, a_pr=cfg["a_pool"], D=cfg["psv_D"])
            if P:
                dists[si] = P
        if cfg["jk"] and dists:
            cols = [lang_index[l] * per for l in src if X[q, lang_index[l] * per] >= 0]
            Pj = jk_dist(X, y, cols, [int(X[q, c]) for c in cols], cfg, exclude=q)
            if Pj:
                dists[S] = Pj
        if not dists:
            continue
        tot = Counter()
        for P in dists.values():
            for k, v in P.items():
                tot[k] += v
        if lab not in tot:
            continue
        cands = sorted(sorted(tot, key=lambda k: (-tot[k], k))[: cfg["lw_maxK"]])
        if lab not in cands:
            cands = sorted(cands[:-1] + [lab]) if len(cands) >= cfg["lw_maxK"] else sorted(cands + [lab])
        rows.append((cands.index(lab), cands, dists))
    names = list(src) + (["__jk__"] if cfg["jk"] else [])
    S = len(names)
    if not rows:
        return {l: 1.0 for l in names}, {l: 1.0 / S for l in names}
    # linear-pool (mixture) weights by EM on the probability each present expert gives the true label
    PY = np.zeros((len(rows), S))
    MM = np.zeros((len(rows), S))
    for qi, (yy, cands, dists) in enumerate(rows):
        for si, P in dists.items():
            MM[qi, si] = 1.0
            PY[qi, si] = P.get(cands[yy], 0.0)
    pi = np.ones(S) / S
    for it in range(100):
        num = PY * pi[None, :] * MM
        den = num.sum(axis=1, keepdims=True) + 1e-300
        g = num / den
        pi = (g.sum(axis=0) + 1e-3) / (MM.sum(axis=0) + 1e-3 * S)
        pi = pi / pi.sum()
    mw = {l: float(pi[si]) for si, l in enumerate(names)}
    K = max(len(c) for _, c, _ in rows)
    n = len(rows)
    LP = np.zeros((n, K, S))
    M = np.zeros((n, S))
    valid = np.zeros((n, K), dtype=bool)
    yi = np.zeros(n, dtype=np.int64)
    for qi, (yy, cands, dists) in enumerate(rows):
        yi[qi] = yy
        valid[qi, :len(cands)] = True
        for si, P in dists.items():
            M[qi, si] = 1.0
            LP[qi, :len(cands), si] = np.log(np.array([P.get(c, 0.0) for c in cands]) + eps)
    # normalise each expert's contribution by the number of present experts (as at prediction: mean of logs)
    cnt = M.sum(axis=1, keepdims=True)
    LPn = LP / cnt[:, :, None]
    r = np.ones(S) * cfg["psv_temp"]
    m_, v_ = np.zeros(S), np.zeros(S)
    lr, b1, b2 = 0.05, 0.9, 0.999
    reg = cfg["lw_reg"]
    for it in range(1, cfg["lw_iters"] + 1):
        sc = LPn @ r
        sc = np.where(valid, sc, -1e30)
        sc -= sc.max(axis=1, keepdims=True)
        p = np.exp(sc)
        p /= p.sum(axis=1, keepdims=True)
        # gradient of mean log p(y)
        ely = LPn[np.arange(n), yi, :]
        ep = np.einsum("nk,nks->ns", p, LPn)
        g = (ely - ep).mean(axis=0) - reg * (r - cfg["psv_temp"])
        m_ = b1 * m_ + (1 - b1) * g
        v_ = b2 * v_ + (1 - b2) * g * g
        r = r + lr * (m_ / (1 - b1 ** it)) / (np.sqrt(v_ / (1 - b2 ** it)) + 1e-8)
        r = np.maximum(r, 0.0)
    return {l: float(r[si]) for si, l in enumerate(names)}, mw


def source_tables(X, y, langs, lang_index, t, ctx):
    """Per source language: label counts given (cur), (cur,L), (cur,R), (cur,L,R) of that language's MSA row."""
    per = 1 + 2 * ctx
    tabs = {}
    for l in langs:
        if l == t:
            continue
        c0 = lang_index[l] * per
        idx = np.nonzero(X[:, c0] >= 0)[0]
        if len(idx) == 0:
            continue
        T1, T2L, T2R, T3 = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
        for q in idx.tolist():
            cur = int(X[q, c0])
            lab = int(y[q])
            T1[cur][lab] += 1
            if ctx:
                Lv, Rv = int(X[q, c0 + 1]), int(X[q, c0 + 2])
                T2L[(cur, Lv)][lab] += 1
                T2R[(cur, Rv)][lab] += 1
                T3[(cur, Lv, Rv)][lab] += 1
        tabs[l] = ({k: dict(v) for k, v in T1.items()}, {k: dict(v) for k, v in T2L.items()},
                   {k: dict(v) for k, v in T2R.items()}, {k: dict(v) for k, v in T3.items()})
        # leave-one-out reliability: mean probability the source's own backoff model gives the true label
        tot, num = {}, 0
        for a_ in LOO_AS:
            tot[a_] = 0.0
        for q in idx.tolist():
            cur = int(X[q, c0])
            lab = int(y[q])
            c1 = dict(T1[cur]); c1[lab] -= 1
            if sum(c1.values()) <= 0:
                continue
            num += 1
            for a_ in LOO_AS:
                n1 = sum(c1.values())
                P = {k: v / n1 for k, v in c1.items() if v > 0}
                if ctx:
                    Lv, Rv = int(X[q, c0 + 1]), int(X[q, c0 + 2])
                    cl = dict(T2L[(cur, Lv)]); cl[lab] -= 1
                    cr = dict(T2R[(cur, Rv)]); cr[lab] -= 1
                    c3 = dict(T3[(cur, Lv, Rv)]); c3[lab] -= 1
                    PL = _interp({k: v for k, v in cl.items() if v > 0}, P, a_)
                    PR = _interp({k: v for k, v in cr.items() if v > 0}, P, a_)
                    P2 = {k: 0.5 * (PL.get(k, 0.0) + PR.get(k, 0.0)) for k in set(PL) | set(PR)}
                    P = _interp({k: v for k, v in c3.items() if v > 0}, P2, a_)
                tot[a_] += P.get(lab, 0.0)
        tabs[l] = tabs[l] + ({a_: (tot[a_] / num if num else 0.0) for a_ in LOO_AS}, num)
    return tabs


LOO_AS = (0.5, 1.0, 2.0)


def pooled_table(X, y, langs, lang_index, t, ctx):
    """Language-agnostic table for target t: counts of the target chunk given any source's (cur, L, R)."""
    per = 1 + 2 * ctx
    T1, T2L, T2R, T3 = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
    for l in langs:
        if l == t:
            continue
        c0 = lang_index[l] * per
        idx = np.nonzero(X[:, c0] >= 0)[0]
        for q in idx.tolist():
            cur = int(X[q, c0])
            lab = int(y[q])
            T1[cur][lab] += 1
            if ctx:
                Lv, Rv = int(X[q, c0 + 1]), int(X[q, c0 + 2])
                T2L[(cur, Lv)][lab] += 1
                T2R[(cur, Rv)][lab] += 1
                T3[(cur, Lv, Rv)][lab] += 1
    return ({k: dict(v) for k, v in T1.items()}, {k: dict(v) for k, v in T2L.items()},
            {k: dict(v) for k, v in T2R.items()}, {k: dict(v) for k, v in T3.items()})


# ---------------------------------------------------------------- prediction
def feat_mult(m, cfg):
    per = 1 + 2 * cfg["ctx"]
    mult = np.ones(m)
    npos = 2 if cfg["posfeat"] else 0
    for q in range(m - npos):
        mult[q] = cfg["wcur"] if q % per == 0 else cfg["wctx"]
    for q in range(m - npos, m):
        mult[q] = cfg["wpos"]
    return mult


def knn_dist(Xt, f, cfg):
    X, y, w, labels = Xt["X"], Xt["y"], Xt["w"], Xt["labels"]
    w = w * feat_mult(X.shape[1], cfg)
    f = np.asarray(f, dtype=np.int32)
    fm = f != -1
    eq = (X == f[None, :])
    present = (X >= 0) & fm[None, :]
    sims = eq.astype(np.float64) @ w
    if cfg["lam"]:
        sims -= cfg["lam"] * ((present & ~eq).astype(np.float64) @ w)
    # k nearest distinct similarity levels
    lv = np.unique(sims)[::-1][: cfg["k"]]
    sel = sims >= lv[-1] - 1e-12
    wt = np.exp(cfg["beta"] * (sims[sel] - lv[0]))
    votes = np.bincount(y[sel], weights=wt, minlength=len(labels))
    tot = votes.sum()
    dist = votes / tot
    return dist


def _interp(cnt, prior, a):
    if not cnt:
        return prior
    n = sum(cnt.values())
    out = {k: a * v / (n + a) for k, v in prior.items()}
    for k, v in cnt.items():
        out[k] = out.get(k, 0.0) + v / (n + a)
    return out


def psv_dist(Xt, f, langs, lang_index, t, cfg, deltas=None, excl=None):
    """Per-source backoff vote: every visible source predicts the target chunk from its own segment and context."""
    per = 1 + 2 * cfg["ctx"]
    nlab = len(Xt["labels"])
    a = cfg["psv_a"]
    use_ctx = bool(cfg["ctx"] and cfg["psv_ctx"])
    acc = np.zeros(nlab)
    logacc = np.zeros(nlab)
    wsum = 0.0
    nsrc = 0
    lw = Xt.get("lw") if cfg["psv_rel"] == "learn" else (Xt.get("mw") if cfg["psv_rel"] == "mix" else None)
    lw_mean = (sum(lw.values()) / len(lw)) if lw else 1.0
    for l in langs:
        if l == t:
            continue
        c0 = lang_index[l] * per
        cur = f[c0]
        if cur < 0:
            continue
        Lv, Rv = (f[c0 + 1], f[c0 + 2]) if cfg["ctx"] else (None, None)
        pooled = False
        ident = Xt["idlab"].get(cur) if "idlab" in Xt else None
        pr = pool_prior(Xt["pool"], cur) if cfg["a_pool"] > 0 else None
        P = backoff_dist(Xt["tabs"][l], cur, Lv, Rv, a, use_ctx, ident=ident,
                         minus=(deltas.get(l) if deltas else None),
                         a_id=Xt.get("aid", {}).get(l, cfg["a_id"]), prior=pr, a_pr=cfg["a_pool"],
                         D=cfg["psv_D"]) \
            if l in Xt["tabs"] else None
        if not P and cfg["pool_fb"] and "pool" in Xt:
            P = backoff_dist(Xt["pool"], cur, Lv, Rv, a, use_ctx, ident=ident, a_id=cfg["a_id"])
            pooled = True
        if not P and cfg["copy_fb"] and ident is not None:
            P = {ident: 1.0}
            pooled = True
        if not P:
            continue
        if pooled:
            r = (cfg["pool_w"] if cfg["pool_fb"] else cfg["copy_w"]) * (lw_mean if lw is not None else 1.0)
        elif lw is not None:
            r = lw.get(l, lw_mean)
        elif cfg["psv_rel"] == "gr":
            r = Xt["w"][c0] ** cfg["psv_rpow"] if cfg["psv_rpow"] else 1.0
        else:
            rel = Xt["tabs"][l][4].get(a, Xt["tabs"][l][4][1.0])
            if cfg["psv_rel"] == "loo_logit":
                rel = min(max(rel, 1e-3), 1 - 1e-3)
                r = max(0.0, math.log(rel / (1 - rel)) + cfg["psv_logit0"]) ** cfg["psv_rpow"]
            else:
                r = rel ** cfg["psv_rpow"]
        vec = np.zeros(nlab)
        for k, v in P.items():
            vec[k] = v
        acc += r * vec
        logacc += r * np.log(vec + cfg["psv_eps"])
        wsum += r
        nsrc += 1
    if nsrc and cfg["jk"] and lw is not None and "__jk__" in lw:
        cols = [lang_index[l] * per for l in langs if l != t and f[lang_index[l] * per] >= 0]
        Pj = jk_dist(Xt["X"], Xt["y"], cols, [f[c] for c in cols], cfg,
                     exclude=(slice(excl[0], excl[1]) if excl else None))
        if Pj:
            vec = np.zeros(nlab)
            for k, v in Pj.items():
                vec[k] = v
            r = lw["__jk__"]
            acc += r * vec
            logacc += r * np.log(vec + cfg["psv_eps"])
            wsum += r
            nsrc += 1
    if nsrc == 0:
        return None
    if lw is not None and cfg["psv_rel"] == "mix":
        return acc / acc.sum() if acc.sum() > 0 else None
    if lw is not None:
        z = logacc / nsrc
        z = np.exp(z - z.max())
        return z / z.sum()
    if wsum <= 0:
        return None
    if cfg["psv_comb"] == "log":
        z = logacc / wsum
        z = np.exp(cfg["psv_temp"] * (z - z.max()))
        return z / z.sum()
    return acc / acc.sum()


def edit_ned(a, b):
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 0.0
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        ai = a[i - 1]
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ai != b[j - 1]))
        prev = cur
    return prev[m] / max(n, m)


def row_features(fm, row, tgt, sim, cfg):
    """MSA of the row's visible reflexes and the column feature vectors (None if no usable model)."""
    langs = fm["langs"]
    lang_index = {l: i for i, l in enumerate(langs)}
    gap, endgap = cfg["gap"], cfg["endgap"]
    src = [l for l in langs if l != tgt and row.get(l) and row[l] != ["?"]]
    s = {l: row[l] for l in src}
    if not src or tgt not in fm["targets"]:
        return src, s, None, None
    if cfg["guide"] == "global":
        order = [l for l in fm["gorder"] if l in s]
    else:
        pmat = {}
        for x_i in range(len(src)):
            for y_i in range(x_i + 1, len(src)):
                pmat[(src[x_i], src[y_i])] = norm_pair(s[src[x_i]], s[src[y_i]], sim, gap, endgap)
        order = guide_order(src, pmat, lang_index)
    rows = msa(order, s, sim, gap, endgap)
    L = len(rows[order[0]])
    feats = column_features(rows, L, lang_index, len(langs), fm["vocab"], cfg["ctx"], cfg["posfeat"], add=False)
    return src, s, feats, rows


def predict_row(fm, row, tgt, sim, cfg, pre=None, deltas=None, excl=None):
    src, s, feats, mrows = pre if pre is not None else row_features(fm, row, tgt, sim, cfg)
    if not src:
        return ["a"]
    if feats is None:
        return list(s[src[0]])
    langs = fm["langs"]
    lang_index = {l: i for i, l in enumerate(langs)}
    Xt = fm["targets"][tgt]
    labels = Xt["labels"]
    per = 1 + 2 * cfg["ctx"]
    lw = Xt.get("lw") or {}
    cols = []
    for j, f in enumerate(feats):
        mu = cfg["mix"]
        d = knn_dist(Xt, f, cfg) if mu < 1 else None
        if mu > 0:
            d2 = psv_dist(Xt, f, langs, lang_index, tgt, cfg, deltas, excl)
            if d2 is not None:
                d = d2 if d is None else (1 - mu) * d + mu * d2
            elif d is None and cfg["knn_fb"]:
                d = knn_dist(Xt, f, cfg)
        if d is not None:
            top = np.argsort(-d, kind="stable")[: max(cfg["nbest"], 1) if cfg["mbr"] else 1]
            cols.append([(labels[q], float(d[q])) for q in top if d[q] > 0])
        else:
            # copy fallback: the segment of the most reliable visible source in this column
            best = None
            for l in src:
                c0 = lang_index[l] * per
                v = f[c0]
                if v == -1:
                    continue
                key = (-lw.get(l, 0.0), -Xt["w"][c0], lang_index[l])
                if best is None or key < best[0]:
                    best = (key, l)
            seg = mrows[best[1]][j]
            cols.append([("" if seg is None else seg, 1.0)])
    if cfg["nbest"] and cfg["mbr"]:
        lam = cfg["lm"]
        lm = fm["lm"].get(tgt) if lam else None
        if lm is not None and cfg.get("_lm_minus") is not None:
            lm = lm_minus(lm, cfg["_lm_minus"])
        order = cfg["lm_order"]
        beam = [((), 0.0, "<s>", "<s>")]
        for col in cols:
            nb = []
            for seqlab, sc, h2, h1 in beam:
                for lab, pr in col[: cfg["nbest"]]:
                    v = sc + math.log(pr)
                    g2, g1 = h2, h1
                    if lm is not None and lab:
                        for seg in lab.split():
                            v += lam * lm_logp(lm, g2, g1, seg, order)
                            if cfg["lm_ratio"]:
                                v -= lam * lm_logp(lm, g2, g1, seg, 1)
                            g2, g1 = g1, seg
                    nb.append((seqlab + (lab,), v, g2, g1))
            nb.sort(key=lambda x: (-x[1], x[0]))
            beam = nb[: cfg["nbest"]]
        fin = []
        for seqlab, sc, h2, h1 in beam:
            if lm is not None:
                sc += lam * lm_logp(lm, h2, h1, "</s>", order)
                if cfg["lm_ratio"]:
                    sc -= lam * lm_logp(lm, h2, h1, "</s>", 1)
            fin.append((seqlab, sc))
        mx = max(v for _, v in fin)
        cand = {}
        for seqlab, sc in fin:
            st = tuple(" ".join(seqlab).split())
            cand[st] = cand.get(st, 0.0) + math.exp((sc - mx) / cfg["mbr_temp"])
        cand = {k: v for k, v in cand.items() if k}
        if (cfg["src_cand"] > 0 or cfg["copy_cand"] > 0) and cand:
            Z0 = sum(cand.values())
            cand = {k: v / Z0 for k, v in cand.items()}
            extra = extra_candidates(Xt, feats, mrows, src, s, langs, lang_index, tgt, cfg)
            if cfg["cand_ev"]:
                # extra candidates enter the evidence space (weights added)
                for st, wgt in extra:
                    cand[st] = cand.get(st, 0.0) + wgt
            else:
                # hypothesis space only: candidates may be chosen, but do not change the evidence
                keys = sorted(cand, key=lambda k: (-cand[k], k))
                hyp = list(keys) + sorted({st for st, _ in extra if st and st not in cand})
                Z = sum(cand.values())
                best, bestr = None, None
                for k in hyp:
                    r = sum(cand[k2] / Z * edit_ned(k, k2) for k2 in keys)
                    if bestr is None or r < bestr - 1e-12:
                        best, bestr = k, r
                return list(best)
        if cfg["nb"] and "nb_index" in fm and cand:
            Z0 = sum(cand.values())
            cand = {k: v / Z0 for k, v in cand.items()}
            for st, wgt in neighbour_candidates(fm, s, tgt, lang_index, cfg):
                cand[st] = cand.get(st, 0.0) + wgt
        if cand:
            keys = sorted(cand, key=lambda k: (-cand[k], k))
            Z = sum(cand.values())
            best, bestr = None, None
            for k in keys:
                r = sum(cand[k2] / Z * edit_ned(k, k2) for k2 in keys)
                if bestr is None or r < bestr - 1e-12:
                    best, bestr = k, r
            return list(best)
    out = []
    for col in cols:
        if col and col[0][0]:
            out.extend(col[0][0].split())
    if not out:
        out = list(s[src[0]])
    return out


def extra_candidates(Xt, feats, mrows, src, s, langs, lang_index, tgt, cfg):
    """Single-expert strings (each visible source decoded alone through its own back-off model) and verbatim copies
    of each visible source, weighted by the source's learned pooling weight (normalised over present sources)."""
    per = 1 + 2 * cfg["ctx"]
    lw = Xt.get("lw") or {}
    present = [l for l in src if l in Xt["tabs"]]
    tw = sum(lw.get(l, 0.0) for l in src) or 1.0
    use_ctx = bool(cfg["ctx"] and cfg["psv_ctx"])
    out = defaultdict(float)
    labels = Xt["labels"]
    for l in src:
        wl = lw.get(l, 0.0) / tw
        if cfg["copy_cand"] > 0:
            out[tuple(s[l])] += cfg["copy_cand"] * wl
        if cfg["src_cand"] > 0 and l in present:
            c0 = lang_index[l] * per
            segs = []
            for j, f in enumerate(feats):
                cur = f[c0]
                if cur < 0:
                    continue
                Lv, Rv = (f[c0 + 1], f[c0 + 2]) if cfg["ctx"] else (None, None)
                P = backoff_dist(Xt["tabs"][l], cur, Lv, Rv, cfg["psv_a"], use_ctx, ident=Xt["idlab"].get(cur),
                                 a_id=Xt.get("aid", {}).get(l, cfg["a_id"]), D=cfg["psv_D"])
                if not P:
                    seg = mrows[l][j]
                    if seg:
                        segs.append(seg)
                    continue
                k = max(P, key=lambda q: (P[q], -q))
                if labels[k]:
                    segs.extend(labels[k].split())
            if segs:
                out[tuple(segs)] += cfg["src_cand"] * wl
    return sorted(out.items())


def neighbour_candidates(fm, s, tgt, lang_index, cfg):
    """Set-level analogy: training sets whose reflexes equal the row's visible reflexes in many shared languages
    propose their target reflex. Returns list of (tuple(segments), weight)."""
    hits = Counter()
    rmask = 0
    for l, seq in s.items():
        rmask |= 1 << lang_index[l]
        for si in fm["nb_index"].get((l, " ".join(seq)), ()):
            hits[si] += 1
    tb = 1 << lang_index[tgt]
    out = defaultdict(float)
    for si, m in sorted(hits.items()):
        if m < cfg["nb_min"]:
            continue
        mk = fm["nb_masks"][si]
        if not mk & tb:
            continue
        shared = bin(mk & rmask).count("1")
        frac = m / shared
        if frac < cfg["nb_frac"]:
            continue
        out[tuple(fm["nb_sets"][si][tgt].split())] += cfg["nb_w"] * frac ** cfg["nb_pow"]
    return sorted(out.items())


def train(manifest, model_dir, cfg):
    man = json.load(open(manifest))
    with open(os.path.join(model_dir, "cfg.json"), "w") as f:
        json.dump(cfg, f, indent=1, sort_keys=True)
    for fam in man["families"]:
        fm = train_family(man["surprise_train"][fam], cfg)
        with open(os.path.join(model_dir, "model-%s.pkl" % fam), "wb") as f:
            pickle.dump(fm, f, protocol=4)
        print("trained", fam, len(fm["targets"]), flush=True)


def predict(model_dir, fam, jobs):
    with open(os.path.join(model_dir, "cfg.json")) as f:
        cfg = json.load(f)
    with open(os.path.join(model_dir, "model-%s.pkl" % fam), "rb") as f:
        fm = pickle.load(f)
    if fm.get("tuned"):
        cfg = dict(cfg)
        cfg.update(fm["tuned"])
    for ln in open(jobs):
        if not ln.strip():
            continue
        inp, outp = ln.rstrip("\n").split("\t")
        langs, data = load(inp)
        with open(outp, "w", encoding="utf-8") as f:
            f.write("COGID\t" + "\t".join(langs) + "\n")
            for key, row in data.items():
                tgt = [l for l in langs if row[l] == ["?"]][0]
                sim = Sim(fm["pmi"], cfg["w_init"])  # fresh per row: no state carried between rows
                pred = predict_row(fm, row, tgt, sim, cfg)
                f.write(key + "".join("\t" + (" ".join(pred) if l == tgt else "") for l in langs) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--manifest")
    ap.add_argument("--model-dir")
    ap.add_argument("--family")
    ap.add_argument("--jobs")
    a = ap.parse_args()
    if a.cmd == "train":
        train(a.manifest, a.model_dir, load_cfg())
    else:
        predict(a.model_dir, a.family, a.jobs)
