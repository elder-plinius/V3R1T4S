"""CORRESPONDENCE lens system (run 2026-10-18-0202; built on run 2026-10-18-0104 correspondence lens): multiple alignment + per-column correspondence experts + MBR.

train (per family, from the manifest's surprise_train file only):
  1. family PMI segment scores: align every pair of reflexes inside each training cognate set (Needleman-Wunsch),
     count aligned segment pairs, shrink segment PMI toward sound-class PMI, re-align (ITER rounds).
  2. pair reliability r(s,t): leave-one-out accuracy of the context-free s->t segment map on pairwise alignments.
  3. training columns built as at test time: for every training set and every attested target t, a progressive
     multiple alignment of the other reflexes (sources added in order of r(s,t)), then t aligned to that profile;
     each column gives, for every source s, a feature (segment of s in the column with its left/right context) and
     the label (t's segment(s) in that column, '-' if none; t segments in new columns are attached to a neighbour).
  4. per (s,t) count tables at back-off levels (seg+left+right, seg+right, seg, class) -> label.
predict (each row alone): MSA of the visible sources in the same order, per column a reliability-weighted product
  of the per-source back-off distributions, n-best strings by beam search, minimum-Bayes-risk choice under NED.
Standard library only; deterministic (no randomness, sorted iteration everywhere).
"""
import os as _os
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    _os.environ[_v] = "1"
import argparse
import json
import math
import os
import pickle
import unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = {
    "iter": 2, "gap": -1.0, "kappa": 3.0, "beta": 1.0, "copy_mix": 0.3,
    "gamma": 4.0, "wsum": 1.5, "temp": 1.0, "prior_w": 0.0,
    "beam": 12, "topk": 4, "nbest": 10, "mbr": 1, "ctx": "lr",
}


def params():
    p = dict(DEFAULTS)
    q = os.path.join(HERE, "params.json")
    if os.path.isfile(q):
        with open(q) as f:
            p.update(json.load(f))
    return p


# ---------------------------------------------------------------- sound classes (generic table, no word lists)
TONE_CH = set("⁰¹²³⁴⁵⁶⁷⁸⁹˥˦˧˨˩0123456789")
VOWEL_CLS = {}
for _c in "iɪyʏɨʉɿʅʯ":
    VOWEL_CLS[_c] = "I"
for _c in "eɛæøœɘɜəɵɞɚɝ":
    VOWEL_CLS[_c] = "E"
for _c in "aɑɐɒɶʌ":
    VOWEL_CLS[_c] = "A"
for _c in "oɔɤ":
    VOWEL_CLS[_c] = "O"
for _c in "uʊɯ":
    VOWEL_CLS[_c] = "U"
CONS_CLS = {}
for _s, _k in [("pbfvɸβɓʙ", "P"), ("tdθðʈɖɗ", "T"), ("szʃʒɕʑʂʐçʝ", "S"), ("cɟʨʥ", "C"), ("kgɡqɢxɣχʁɠ", "K"),
               ("hɦʔʕħ", "H"), ("mɱ", "M"), ("nɲŋɳȵɴ", "N"), ("lɬɭʎɮ", "L"), ("rɾɹʀɽ", "R"), ("wʋɥ", "W"),
               ("j", "J")]:
    for _c in _s:
        CONS_CLS[_c] = _k
SIB = set("szʃʒɕʑʂʐ")
_CLS_CACHE = {}


def sclass(seg):
    if seg in _CLS_CACHE:
        return _CLS_CACHE[seg]
    if seg == "-":
        c = "-"
    elif all(ch in TONE_CH for ch in seg):
        c = "Z"
    else:
        base = []
        for ch in unicodedata.normalize("NFD", seg):
            if unicodedata.combining(ch) or unicodedata.category(ch) in ("Lm", "Sk", "Mn", "No"):
                continue
            base.append(ch)
        if not base:
            c = "X"
        else:
            b = base[0]
            if b in VOWEL_CLS:
                c = VOWEL_CLS[b]
            elif b in CONS_CLS:
                c = CONS_CLS[b]
                if b in "td" and len(base) > 1 and base[1] in SIB:
                    c = "C"
            else:
                c = "X"
    _CLS_CACHE[seg] = c
    return c


def is_vowel_cls(c):
    return c in ("I", "E", "A", "O", "U")


def init_score(a, b):
    if a == b:
        return 3.0
    ca, cb = sclass(a), sclass(b)
    if ca == cb:
        return 1.5 if ca != "X" else 0.0
    if is_vowel_cls(ca) and is_vowel_cls(cb):
        return 0.5
    if {ca, cb} in ({"S", "C"}, {"T", "C"}, {"P", "W"}, {"J", "I"}, {"W", "U"}, {"K", "H"}, {"N", "M"},
                    {"L", "R"}, {"T", "S"}):
        return 0.0
    return -1.0


# ---------------------------------------------------------------- scoring object
TONE_CLASH = -10.0


class Scorer:
    """Segment similarity: shrunk segment PMI -> class PMI -> initial table."""

    def __init__(self, seg_pmi=None, cls_pmi=None):
        self.seg = seg_pmi
        self.cls = cls_pmi
        self.cache = {}

    def __call__(self, a, b):
        k = (a, b)
        v = self.cache.get(k)
        if v is not None:
            return v
        za, zb = sclass(a) == "Z", sclass(b) == "Z"
        if za != zb:
            v = TONE_CLASH
        elif za and TONE_FLOOR is not None and self.seg is not None:
            v = self.seg.get(k)
            if v is None:
                v = self.cls.get(("Z", "Z"), 0.0)
            v = max(v, TONE_FLOOR) + (1.0 if a == b else 0.0)
        elif self.seg is None:
            v = init_score(a, b)
        else:
            v = self.seg.get(k)
            if v is None:
                v = self.cls.get((sclass(a), sclass(b)))
                if v is None:
                    v = init_score(a, b) * 0.5 - 0.5
                elif a == b:
                    v = max(v, 1.0) + 1.0
        self.cache[k] = v
        return v


def nw(a, b, S, gap):
    n, m = len(a), len(b)
    D = [[0.0] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        D[i][0] = D[i - 1][0] + gap
        P[i][0] = 1
    for j in range(1, m + 1):
        D[0][j] = D[0][j - 1] + gap
        P[0][j] = 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        Di, Dp = D[i], D[i - 1]
        Pi = P[i]
        for j in range(1, m + 1):
            d = Dp[j - 1] + S(ai, b[j - 1])
            u = Dp[j] + gap
            l = Di[j - 1] + gap
            if d >= u and d >= l:
                Di[j] = d
                Pi[j] = 0
            elif u >= l:
                Di[j] = u
                Pi[j] = 1
            else:
                Di[j] = l
                Pi[j] = 2
    i, j, out = n, m, []
    while i > 0 or j > 0:
        p = P[i][j]
        if p == 0:
            out.append((a[i - 1], b[j - 1]))
            i -= 1
            j -= 1
        elif p == 1:
            out.append((a[i - 1], "-"))
            i -= 1
        else:
            out.append(("-", b[j - 1]))
            j -= 1
    out.reverse()
    return out, D[n][m]


def learn_pmi(data, langs, prm):
    S = Scorer()
    gap = prm["gap"]
    seg_pmi = cls_pmi = None
    pairs = []
    for key in sorted(data):
        row = data[key]
        att = [l for l in langs if row[l]]
        for i in range(len(att)):
            for j in range(i + 1, len(att)):
                pairs.append((row[att[i]], row[att[j]]))
    for _ in range(prm["iter"]):
        c = Counter()
        for a, b in pairs:
            al, _ = nw(a, b, S, gap)
            for x, y in al:
                if x != "-" and y != "-":
                    c[(x, y)] += 1
                    c[(y, x)] += 1
        tot = sum(c.values()) or 1
        marg = Counter()
        for (x, _y), v in c.items():
            marg[x] += v
        cc = Counter()
        for (x, y), v in c.items():
            cc[(sclass(x), sclass(y))] += v
        cm = Counter()
        for (x, _y), v in cc.items():
            cm[x] += v
        cls_pmi = {}
        allc = sorted(cm)
        for x in allc:
            for y in allc:
                v = cc.get((x, y), 0)
                cls_pmi[(x, y)] = math.log((v + 0.5) * tot / (cm[x] * cm[y] + 0.5 * tot / max(1, len(allc))))
        seg_pmi = {}
        kap = prm["kappa"]
        for (x, y), v in c.items():
            pm = math.log(v * tot / (marg[x] * marg[y]))
            base = cls_pmi[(sclass(x), sclass(y))]
            seg_pmi[(x, y)] = (v * pm + kap * base) / (v + kap)
        S = Scorer(seg_pmi, cls_pmi)
    return seg_pmi, cls_pmi


# ---------------------------------------------------------------- progressive multiple alignment
def align_to_profile(x, cols, nmem, S, gap):
    """cols: list of Counter(seg -> count over members, '-' included); returns list of (col index or None, seg) ops.
    op (j, seg): x segment aligned to column j; (j, None): column j gets a gap in x; (None, seg): new column."""
    n, m = len(x), len(cols)
    half = gap * 0.5
    csc = []
    for col in cols:
        items = [(s, c) for s, c in col.items() if s != "-"]
        ng = col.get("-", 0)
        csc.append((items, ng))
    D = [[0.0] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    gcol = [gap * (1.0 - csc[j][1] / nmem) for j in range(m)]
    for i in range(1, n + 1):
        D[i][0] = D[i - 1][0] + gap
        P[i][0] = 1
    for j in range(1, m + 1):
        D[0][j] = D[0][j - 1] + gcol[j - 1]
        P[0][j] = 2
    for i in range(1, n + 1):
        xi = x[i - 1]
        sc = []
        for items, ng in csc:
            s = ng * half
            for seg, c in items:
                s += c * S(xi, seg)
            sc.append(s / nmem)
        Di, Dp, Pi = D[i], D[i - 1], P[i]
        for j in range(1, m + 1):
            d = Dp[j - 1] + sc[j - 1]
            u = Dp[j] + gap
            l = Di[j - 1] + gcol[j - 1]
            if d >= u and d >= l:
                Di[j] = d
                Pi[j] = 0
            elif u >= l:
                Di[j] = u
                Pi[j] = 1
            else:
                Di[j] = l
                Pi[j] = 2
    i, j, ops = n, m, []
    while i > 0 or j > 0:
        p = P[i][j]
        if p == 0:
            ops.append((j - 1, x[i - 1]))
            i -= 1
            j -= 1
        elif p == 1:
            ops.append((None, x[i - 1]))
            i -= 1
        else:
            ops.append((j - 1, None))
            j -= 1
    ops.reverse()
    return ops


def msa(seqs, S, gap):
    """seqs: list of (lang, segments) in the order of addition. Returns (rows dict lang -> list over columns)."""
    lang0, s0 = seqs[0]
    rows = {lang0: list(s0)}
    cols = [Counter({seg: 1}) for seg in s0]
    nmem = 1
    for lang, x in seqs[1:]:
        ops = align_to_profile(x, cols, nmem, S, gap)
        new_rows = {l: [] for l in rows}
        new_rows[lang] = []
        new_cols = []
        for j, seg in ops:
            if j is None:
                for l in rows:
                    new_rows[l].append("-")
                new_rows[lang].append(seg)
                new_cols.append(Counter({"-": nmem, seg: 1}))
            else:
                for l in rows:
                    new_rows[l].append(rows[l][j])
                new_rows[lang].append(seg if seg is not None else "-")
                c = Counter(cols[j])
                c[seg if seg is not None else "-"] += 1
                new_cols.append(c)
        rows, cols = new_rows, new_cols
        nmem += 1
    return rows, cols


# ---------------------------------------------------------------- features
def ctx_of(rowseq, j):
    left = "#"
    for k in range(j - 1, -1, -1):
        if rowseq[k] != "-":
            left = rowseq[k]
            break
    right = "#"
    for k in range(j + 1, len(rowseq)):
        if rowseq[k] != "-":
            right = rowseq[k]
            break
    return left, right


FINE_V = True
VOICED = set("bdgɡɖɟɢzʒʑʐvβðɣʁɦɓɗ")


def ccls(seg):
    if seg == "#":
        return "#"
    c = sclass(seg)
    if FINE_V:
        return c
    return "V" if is_vowel_cls(c) else c


def laryngeal(seg):
    if "ʰ" in seg:
        return "h"
    c = sclass(seg)
    if c in ("M", "N", "L", "R", "W", "J") or is_vowel_cls(c):
        return "s"
    for ch in unicodedata.normalize("NFD", seg):
        if ch in VOICED:
            return "v"
    return "p"


def features(rowseq, j):
    seg = rowseq[j]
    left, right = ctx_of(rowseq, j)
    cl, cr = ccls(left), ccls(right)
    if TONE_INIT and sclass(seg) == "Z":
        first = "#"
        for x in rowseq:
            if x != "-":
                first = x
                break
        return (("3", seg, cl, cr), ("2", seg, "L" + laryngeal(first)), ("1", seg), ("0", sclass(seg)))
    return (("3", seg, cl, cr), ("2", seg, cr), ("1", seg), ("0", sclass(seg)))


TONE_INIT = True


def target_labels(rows, cols, tseq, S, gap, nmem):
    ops = align_to_profile(tseq, cols, nmem, S, gap)
    m = len(cols)
    lab = [[] for _ in range(m)]
    pending = []
    last = None
    for j, seg in ops:
        if j is None:
            if last is None:
                pending.append(seg)
            else:
                lab[last].append(seg)
        else:
            if seg is not None:
                lab[j].append(seg)
            last = j
            if pending:
                lab[j] = pending + lab[j]
                pending = []
    if pending and m:
        lab[0] = pending + lab[0]
    return [" ".join(l) if l else "-" for l in lab]


# ---------------------------------------------------------------- training
def pair_reliability(data, langs, S, gap):
    rel = {}
    for t in langs:
        for s in langs:
            if s == t:
                continue
            mp = defaultdict(Counter)
            inst = []
            for key in sorted(data):
                r = data[key]
                if r[s] and r[t]:
                    al, _ = nw(r[s], r[t], S, gap)
                    for x, y in al:
                        if x != "-":
                            mp[x][y] += 1
                            inst.append((x, y))
            if not inst:
                rel[(s, t)] = 0.05
                continue
            good = 0.0
            for x, y in inst:
                c = mp[x]
                own = c[y] - 1
                other = max([v for k, v in c.items() if k != y] or [0])
                if own > other:
                    good += 1
                elif own == other and own > 0:
                    good += 0.5
            n = len(inst)
            rel[(s, t)] = (good + 1.0) / (n + 2.0)
    return rel


def order_sources(srcs, t, rel, langs):
    return sorted(srcs, key=lambda s: (-rel.get((s, t), 0.0), langs.index(s)))


TONE_FLOOR = None


def set_feature_flags(prm):
    global FINE_V, TONE_INIT, TONE_FLOOR
    TONE_FLOOR = prm.get("tone_floor")
    FINE_V = bool(prm.get("fine_v", 1))
    TONE_INIT = bool(prm.get("tone_init", 1))


# Development families that are close relatives of a surprise family (BRIEF: allenbai ~ wangbai, mannburmish ~
# hillburmish; listsamplesize shares English/French/German with kesslersignificance). Language-name maps
# (surprise name -> dev name); "exact" uses only identical names, "syn" adds well-known synonyms.
DEV_MAP = {
    "exact": {
        "hillburmish": ("mannburmish", {"Lashi": "Lashi", "Maru": "Maru"}),
        "wangbai": ("allenbai", {"Zhoucheng": "Zhoucheng"}),
        "kesslersignificance": ("listsamplesize", {"English": "english", "French": "french", "German": "german"}),
    },
    "bai": {
        "wangbai": ("allenbai", {"Zhoucheng": "Zhoucheng"}),
    },
    "syn": {
        "hillburmish": ("mannburmish", {"Lashi": "Lashi", "Maru": "Maru", "Atsi": "Zaiwa", "Bola": "Bela",
                                        "AchangLongchuan": "Achang", "OldBurmese": "WrittenBurmese"}),
        "wangbai": ("allenbai", {"Zhoucheng": "Zhoucheng"}),
        "kesslersignificance": ("listsamplesize", {"English": "english", "French": "french", "German": "german"}),
    },
}


def load_dev_rows(dev_dir, fam, prm, langs):
    mode = prm.get("dev", "")
    if not mode or not dev_dir or fam not in DEV_MAP.get(mode, {}):
        return {}, []
    dfam, mp = DEV_MAP[mode][fam]
    inv = {d: s for s, d in mp.items() if s in langs}
    if prm.get("dev_all", 0):
        dl0, _ = load(os.path.join(dev_dir, dfam, "training-0.10.tsv"))
        for d in dl0:
            if d not in inv:
                inv[d] = "D:" + d
    L = list(langs) + sorted(v for v in inv.values() if v not in langs)
    rows = {}
    for fn in ("training-0.10.tsv", "test-0.10.tsv"):
        q = os.path.join(dev_dir, dfam, fn)
        if not os.path.isfile(q):
            continue
        dl, dd = load(q)
        for key in sorted(dd):
            base = key.split("-")[0]
            r = rows.setdefault("dev:" + base, {})
            for l in dl:
                v = dd[key][l]
                if l in inv and v and v != ["?"]:
                    if prm.get("dev_notone", 0):
                        v = [x for x in v if sclass(x) != "Z"]
                    if v:
                        r[inv[l]] = v
    out = {}
    for k in sorted(rows):
        if len(rows[k]) >= 2:
            out[k] = {l: rows[k].get(l, []) for l in L}
    return out, L[len(langs):]


def train_family(path, prm, fam=None, dev_dir=None):
    langs0, data = load(path)
    return train_family_data(langs0, data, prm, fam=fam, dev_dir=dev_dir)


def train_family_data(langs0, data, prm, fam=None, dev_dir=None):
    set_feature_flags(prm)
    extra, xl = load_dev_rows(dev_dir, fam, prm, langs0)
    for k in data:
        for l in xl:
            data[k][l] = []
    data.update(extra)
    langs = langs0 + xl
    gap = prm["gap"]
    go = prm.get("dev_glob_only", 0)
    core = {k: v for k, v in data.items() if not (go and k.startswith("dev:"))}
    seg_pmi, cls_pmi = learn_pmi(core, langs, prm)
    S = Scorer(seg_pmi, cls_pmi)
    rel = pair_reliability(core, langs, S, gap)
    tables = {}  # (s,t) -> {feature: Counter(label)}
    prior = {t: Counter() for t in langs}
    insts = defaultdict(list)
    for key in sorted(data):
        r = data[key]
        att = [l for l in langs if r[l]]
        if len(att) < 2:
            continue
        for t in att:
            srcs = order_sources([l for l in att if l != t], t, rel, langs)
            rows, cols = msa([(s, r[s]) for s in srcs], S, gap)
            labs = target_labels(rows, cols, r[t], S, gap, len(srcs))
            pooled = tables.setdefault(("*", t), {})
            glob = tables.setdefault(("*", "*"), {})
            if go and key.startswith("dev:"):
                for j, lab in enumerate(labs):
                    for s in srcs:
                        seg = rows[s][j]
                        glob.setdefault(("1", seg), Counter())[lab] += go
                        glob.setdefault(("0", sclass(seg)), Counter())["COPY" if lab == seg else "OTHER"] += go
                continue
            if len(srcs) >= 2:
                pt = tables.setdefault(("P", t), {})
                a0, a1 = srcs[0], srcs[1]
                for j, lab in enumerate(labs):
                    pt.setdefault((a0, a1, rows[a0][j], rows[a1][j]), Counter())[lab] += 1
            for j, lab in enumerate(labs):
                prior[t][lab] += 1
                insts[t].append((lab, [(s, features(rows[s], j), rows[s][j]) for s in srcs]))
                for s in srcs:
                    tb = tables.setdefault((s, t), {})
                    fs = features(rows[s], j)
                    for f in fs:
                        tb.setdefault(f, Counter())[lab] += 1
                    seg = rows[s][j]
                    cp = "COPY" if lab == seg else "OTHER"
                    tb.setdefault(("C", fs[3][1]), Counter())[cp] += 1
                    pooled.setdefault(("C", fs[3][1]), Counter())[cp] += 1
                    pooled.setdefault(("1", seg), Counter())[lab] += 1
                    glob.setdefault(("1", seg), Counter())[lab] += 1
                    glob.setdefault(("0", fs[3][1]), Counter())["COPY" if lab == seg else "OTHER"] += 1
    if xl:
        keep = set(langs0) | {"*", "P"}
        tables = {k: v for k, v in tables.items() if k[0] in keep and k[1] in keep}
        rel = {k: v for k, v in rel.items() if k[0] in keep and k[1] in keep}
        prior = {t: v for t, v in prior.items() if t in keep}
        insts = {t: [(lab, [x for x in fl if x[0] in keep]) for lab, fl in v] for t, v in insts.items() if t in keep}
        langs = langs0
    ident = {}
    for t in langs:
        for s2 in langs:
            if s2 == t:
                continue
            nb = ne = 0
            for key in sorted(core):
                r = core[key]
                if r[s2] and r[t]:
                    nb += 1
                    ne += r[s2] == r[t]
            if nb:
                ident[(s2, t)] = (ne + 0.5) / (nb + 1.0)
    model = {"langs": langs, "seg_pmi": seg_pmi, "cls_pmi": cls_pmi, "rel": rel, "ident": ident,
             "tables": {k: {f: dict(c) for f, c in v.items()} for k, v in tables.items()},
             "prior": {t: dict(c) for t, c in prior.items()}, "lm": train_lm(data, langs)}
    if prm.get("learn_w", 0):
        model["w"] = learn_weights(model, insts, prm)
    model["acc"] = expert_accuracy(model, insts, prm)
    return model


def expert_accuracy(model, insts, prm):
    """Leave-one-out accuracy and mean log-prob of each (s,t) expert on the training columns built as at test time."""
    langs = model["langs"]
    glob = model["tables"].get(("*", "*"), {})
    out = {}
    for t in langs:
        I = insts.get(t)
        if not I:
            continue
        prior_t = model["prior"].get(t, {})
        prior_tot = sum(prior_t.values())
        pooled = model["tables"].get(("*", t), {})
        good = defaultdict(float)
        lp = defaultdict(float)
        n = Counter()
        for lab, fl in I:
            feats_s = [(s, fs, model["tables"].get((s, t)), seg) for s, fs, seg in fl]
            cand = column_cands(feats_s, pooled)
            if lab not in cand:
                cand = sorted(set(cand) | {lab})
            for s, fs, tb, seg in feats_s:
                p = dist_for_source(tb, pooled, fs, cand, prior_t, prior_tot, prm, seg, excl=lab, glob=glob)
                best = max(p.values())
                if p[lab] >= best - 1e-12:
                    ties = sum(1 for v in p.values() if v >= best - 1e-12)
                    good[s] += 1.0 / ties
                lp[s] += math.log(p[lab])
                n[s] += 1
        for s in n:
            out[(s, t)] = ((good[s] + 1.0) / (n[s] + 2.0), lp[s] / n[s], n[s])
    return out


def column_cands(feats_s, pooled):
    cand = set(["-"])
    for s, fs, tb, seg in feats_s:
        if seg != "-":
            cand.add(seg)
        if tb:
            for f in fs[2:]:
                c = tb.get(f)
                if c:
                    cand.update(c.keys())
        c = pooled.get(("1", seg))
        if c:
            cand.update(c.keys())
    return sorted(cand)


def learn_weights(model, insts, prm):
    import numpy as np
    from scipy.optimize import minimize
    langs = model["langs"]
    out = {}
    for t in langs:
        I = insts.get(t)
        if not I:
            continue
        prior_t = model["prior"].get(t, {})
        prior_tot = sum(prior_t.values())
        pooled = model["tables"].get(("*", t), {})
        srcl = [l for l in langs if l != t]
        sidx = {l: i for i, l in enumerate(srcl)}
        rows = []
        for lab, fl in I:
            feats_s = [(s, fs, model["tables"].get((s, t)), seg) for s, fs, seg in fl]
            cand = column_cands(feats_s, pooled)
            if lab not in cand or len(cand) < 2:
                continue
            mat = {}
            for s, fs, tb, seg in feats_s:
                p = dist_for_source(tb, pooled, fs, cand, prior_t, prior_tot, prm, seg, excl=lab)
                mat[sidx[s]] = [math.log(p[l]) for l in cand]
            rows.append((cand.index(lab), len(cand), mat))
        if not rows:
            continue
        n, K = len(rows), len(srcl)
        C = max(r[1] for r in rows)
        X = np.zeros((n, K, C))
        M = np.full((n, C), -1e9)
        y = np.zeros(n, dtype=int)
        for i, (yi, nc, mat) in enumerate(rows):
            y[i] = yi
            M[i, :nc] = 0.0
            for k, v in mat.items():
                X[i, k, :nc] = v
        lam = prm.get("w_l2", 0.01)
        w0 = np.array([max(model["rel"].get((s, t), 0.05), 1e-3) ** prm["gamma"] for s in srcl])
        w0 = prm["wsum"] * w0 / w0.sum()
        Xy = X[np.arange(n), :, y]

        def f(w):
            sc = np.einsum("nkc,k->nc", X, w) + M
            mx = sc.max(axis=1, keepdims=True)
            e = np.exp(sc - mx)
            z = e.sum(axis=1, keepdims=True)
            pr = e / z
            ll = (sc[np.arange(n), y] - mx[:, 0] - np.log(z[:, 0])).sum()
            g = (Xy - np.einsum("nkc,nc->nk", X, pr)).sum(axis=0)
            return -ll / n + lam * (w * w).sum(), -g / n + 2 * lam * w

        r = minimize(f, w0, jac=True, method="L-BFGS-B", bounds=[(0.0, None)] * K,
                     options={"maxiter": 200})
        for k, s in enumerate(srcl):
            out[(s, t)] = float(r.x[k])
    return out


def train_lm(data, langs):
    lm = {}
    for t in langs:
        big = defaultdict(Counter)
        for key in sorted(data):
            w = data[key][t]
            if not w:
                continue
            seq = ["<s>"] + list(w) + ["</s>"]
            for a, b in zip(seq, seq[1:]):
                big[a][b] += 1
                big["*"][b] += 1
        lm[t] = {a: dict(c) for a, c in big.items()}
    return lm


def lm_logp(lm, prev, seg, beta=1.0):
    uni = lm.get("*", {})
    nu = sum(uni.values())
    pu = (uni.get(seg, 0) + 0.5) / (nu + 0.5 * (len(uni) + 1))
    c = lm.get(prev)
    if not c:
        return 0.0
    n = sum(c.values())
    u = len(c) * beta
    return math.log((c.get(seg, 0) + u * pu) / (n + u)) - math.log(pu)


# ---------------------------------------------------------------- prediction
def dist_for_source(tb, pooled, feats, cand, prior_t, prior_tot, prm, seg, excl=None, glob=None):
    beta = prm["beta"]
    nlab = len(cand)
    p = {l: (prior_t.get(l, 0) + 0.1) / (prior_tot + 0.1 * nlab) for l in cand}
    gmode = prm.get("glob", 0)

    def wb(p, c):
        if not c:
            return p
        n = sum(c.values())
        u = len(c)
        if excl is not None:
            ce = c.get(excl, 0)
            if ce > 0:
                n -= 1
                if ce == 1:
                    u -= 1
                if n <= 0:
                    return p
                u = u * beta
                return {l: (c.get(l, 0) - (1 if l == excl else 0) + u * p[l]) / (n + u) for l in cand}
        u = u * beta
        return {l: (c.get(l, 0) + u * p[l]) / (n + u) for l in cand}

    gord = prm.get("glob_order", 0)
    if gmode and glob and not gord:
        bsave = beta
        beta = prm["beta"] * prm.get("beta_glob", 1.0)
        p = wb(p, glob.get(("1", seg)))
        beta = bsave
    p = wb(p, tb.get(feats[3]) if tb else None)  # class level of this pair
    # copy-aware mix: how often does this class copy its segment for this pair (pooled over sources as prior)
    cc = (pooled or {}).get(("C", feats[3][1]), {})
    pc0 = (cc.get("COPY", 0) + 1.0) / (sum(cc.values()) + 2.0) if cc else prm["copy_mix"]
    if gmode >= 2 and glob:
        gc = glob.get(("0", feats[3][1]), {})
        g0 = (gc.get("COPY", 0) + 1.0) / (sum(gc.values()) + 2.0) if gc else prm["copy_mix"]
        nc = sum(cc.values()) if cc else 0
        pc0 = ((cc.get("COPY", 0) if cc else 0) + 2.0 * g0) / (nc + 2.0)
    c2 = (tb or {}).get(("C", feats[3][1]), {})
    n2 = sum(c2.values())
    ncopy = c2.get("COPY", 0)
    if excl is not None and n2 > 0:
        n2 -= 1
        if excl == seg:
            ncopy -= 1
    pc = (ncopy + 2.0 * pc0) / (n2 + 2.0)
    cu = prm.get("copy_unseen", 0.0)
    if cu and seg != "-" and not (tb and tb.get(feats[2])):
        pc = max(pc, cu)
    p = {l: (1 - pc) * v + (pc if l == seg else 0.0) + 1e-6 for l, v in p.items()}
    if gmode and glob and gord:
        bsave = beta
        beta = prm["beta"] * prm.get("beta_glob", 1.0)
        p = wb(p, glob.get(("1", seg)))
        beta = bsave
    if prm.get("pooled", 1):
        p = wb(p, (pooled or {}).get(("1", seg)))
    p = wb(p, tb.get(feats[2]) if tb else None)
    ctx = prm["ctx"]
    if ctx in ("r", "lr"):
        beta = prm["beta"] * prm.get("beta_ctx", 1.0)
        p = wb(p, tb.get(feats[1]) if tb else None)
        if ctx == "lr":
            p = wb(p, tb.get(feats[0]) if tb else None)
    return p


def predict_row(model, row, tgt, prm):
    set_feature_flags(prm)
    langs = model["langs"]
    S = model["_S"]
    gap = prm["gap"]
    rel = model["rel"]
    srcs = [l for l in langs if l != tgt and row[l] and row[l] != ["?"]]
    srcs = order_sources(srcs, tgt, rel, langs)
    rows, cols = msa([(s, row[s]) for s in srcs], S, gap)
    m = len(cols)
    prior_t = model["prior"].get(tgt, {})
    prior_tot = sum(prior_t.values())
    g = prm["gamma"]
    if prm.get("learn_w", 0) and "w" in model:
        ws = [model["w"].get((s, tgt), 0.0) for s in srcs]
        if sum(ws) <= 0:
            ws = [1.0 for _ in srcs]
    else:
        wm = prm.get("wmode", "rel")
        acc = model.get("acc", {})
        if wm == "acc":
            ws = [max(acc.get((s, tgt), (0.05, -5.0, 0))[0], 1e-3) ** g for s in srcs]
        elif wm == "lp":
            ws = [math.exp(g * acc.get((s, tgt), (0.05, -5.0, 0))[1]) for s in srcs]
        elif wm == "mix":
            ws = [(max(acc.get((s, tgt), (0.05, -5.0, 0))[0], 1e-3) * max(rel.get((s, tgt), 0.05), 1e-3)) ** (g / 2)
                  for s in srcs]
        else:
            ws = [max(rel.get((s, tgt), 0.05), 1e-3) ** g for s in srcs]
        z = sum(ws)
        ws = [prm["wsum"] * w / z for w in ws]
    hen = prm.get("hen", 0.0)
    if hen and len(srcs) > 2:
        hw = []
        for s in srcs:
            tot = 0.0
            for j in range(m):
                colsegs = [rows[x][j] for x in srcs]
                r = len(set(colsegs))
                tot += 1.0 / (r * colsegs.count(rows[s][j]))
            hw.append(tot / max(1, m))
        zh = sum(hw)
        hw = [len(srcs) * h / zh for h in hw]
        ws = [w * (h ** hen) for w, h in zip(ws, hw)]
        z = sum(ws)
        ws = [prm["wsum"] * w / z for w in ws]
    coldists = []
    rover = prm.get("rover", 0.0)
    src_best = [[] for _ in srcs]
    pooled = model["tables"].get(("*", tgt), {})
    glob = model["tables"].get(("*", "*"), {})
    ptab = model["tables"].get(("P", tgt), {})
    for j in range(m):
        feats_s = []
        cand = set(["-"])
        for s in srcs:
            fs = features(rows[s], j)
            tb = model["tables"].get((s, tgt))
            feats_s.append((s, fs, tb))
            seg = rows[s][j]
            if seg != "-":
                cand.add(seg)
            if tb:
                for f in fs[2:]:
                    c = tb.get(f)
                    if c:
                        cand.update(c.keys())
            c = pooled.get(("1", seg))
            if c:
                cand.update(c.keys())
        cand = sorted(cand)
        score = {l: 0.0 for l in cand}
        if prm["prior_w"]:
            for l in cand:
                score[l] += prm["prior_w"] * math.log((prior_t.get(l, 0) + 0.1) / (prior_tot + 0.1 * len(cand)))
        pat_w = prm.get("pat_w", 0.0)
        for si, ((s, fs, tb), w) in enumerate(zip(feats_s, ws)):
            p = dist_for_source(tb, pooled, fs, cand, prior_t, prior_tot, prm, rows[s][j], glob=glob)
            if pat_w and si == 0 and len(srcs) >= 2:
                c = ptab.get((srcs[0], srcs[1], rows[srcs[0]][j], rows[srcs[1]][j]))
                if c:
                    n = sum(c.values())
                    u = len(c) * prm["beta"] * prm.get("beta_pat", 1.0)
                    for l in cand:
                        score[l] += pat_w * (math.log((c.get(l, 0) + u * p[l]) / (n + u)) - math.log(p[l]))
            for l in cand:
                score[l] += w * math.log(p[l])
            if rover or prm.get("add_rover", 0):
                src_best[si].append(max(cand, key=lambda l: (p[l], l)))
        T = prm["temp"]
        mx = max(score.values())
        ex = {l: math.exp((v - mx) / T) for l, v in score.items()}
        zz = sum(ex.values())
        coldists.append(sorted(((v / zz, l) for l, v in ex.items()), key=lambda x: (-x[0], x[1])))
    # beam over columns
    lam = prm.get("lm_w", 0.0)
    lm = model["lm"].get(tgt, {}) if lam else None
    beam = [(0.0, (), "<s>")]
    for d in coldists:
        top = d[:prm["topk"]]
        nb = []
        for lp, hyp, last in beam:
            for pr, l in top:
                lq = lp + math.log(pr + 1e-12)
                nl = last
                if lam and l != "-":
                    for sg in l.split():
                        lq += lam * lm_logp(lm, nl, sg)
                        nl = sg
                nb.append((lq, hyp + (l,), nl))
        nb.sort(key=lambda x: (-x[0], x[1]))
        beam = nb[:prm["beam"]]
    if lam:
        beam = [(lp + lam * lm_logp(lm, last, "</s>"), hyp, last) for lp, hyp, last in beam]
    agg = {}
    for lp, hyp, _last in beam:
        segs = tuple(s for l in hyp if l != "-" for s in l.split())
        agg[segs] = agg.get(segs, 0.0) + math.exp(lp)
    cands = sorted(agg.items(), key=lambda x: (-x[1], x[0]))[:prm["nbest"]]
    cands = [(c, p) for c, p in cands if c] or [(tuple(row[srcs[0]]), 1.0)]
    if rover:
        zs = sum(p for _, p in cands)
        ev = {}
        for c, p in cands:
            ev[c] = ev.get(c, 0.0) + (1.0 - rover) * p / zs
        rg = prm.get("rover_gamma", prm["gamma"])
        rw = [max(rel.get((s, tgt), 0.05), 1e-3) ** rg for s in srcs]
        zr = sum(rw)
        for sb, w in zip(src_best, rw):
            ys = tuple(x for l in sb if l != "-" for x in l.split())
            if ys:
                ev[ys] = ev.get(ys, 0.0) + rover * w / zr
        cands = sorted(ev.items(), key=lambda x: (-x[1], x[0]))
    nbeam = len(cands)
    if prm.get("add_rover", 0):
        have = {c for c, _ in cands}
        zs = sum(p for _, p in cands)
        for sb in src_best:
            ys = tuple(x for l in sb if l != "-" for x in l.split())
            if ys and ys not in have:
                have.add(ys)
                cands.append((ys, zs * prm["add_rover"]))
    if prm.get("add_src", 0):
        have = {c for c, _ in cands}
        zs = sum(p for _, p in cands)
        for sname in srcs:
            c = tuple(row[sname])
            if c not in have:
                have.add(c)
                cands.append((c, zs * prm["add_src"]))
    if prm.get("return_cands"):
        return (cands, nbeam) if prm.get("return_cands") == 2 else cands
    rr = model.get("_rr")
    if prm.get("rerank", 0) and rr is not None and len(cands) > 1:
        F = rr_feats(model, row, tgt, cands, prm, nbeam=nbeam)
        sc = [sum(w * x for w, x in zip(rr, f)) for f in F]
        if prm.get("rr_mbr", 0):
            mx = max(sc)
            pr = [math.exp(v - mx) for v in sc]
            zz = sum(pr)
            risks = [sum(q * ned_al(list(c), list(d)) for (d, _), q in zip(cands, pr)) / zz for c, _ in cands]
            bi = min(range(len(cands)), key=lambda i: (risks[i], i))
            return list(cands[bi][0])
        bi = max(range(len(cands)), key=lambda i: (sc[i], -i))
        return list(cands[bi][0])
    if not prm["mbr"] or len(cands) == 1:
        return list(cands[0][0])
    zs = sum(p for _, p in cands)
    best, bestr = None, None
    for c, _ in cands:
        risk = sum(p * ned(c, d) for d, p in cands) / zs
        if bestr is None or risk < bestr - 1e-12:
            best, bestr = c, risk
    return list(best)


# ---------------------------------------------------------------- discriminative n-best reranker
RR_NAMES = ["lp", "top1", "risk", "srcned", "minned", "iscopy", "lm", "lendiff", "tonediff", "lenrel", "vowdiff",
            "copyrate", "srcned_id", "topned", "votes", "copytop", "lp_nsrc", "frombeam"]
RR_NSET = {1: 11, 2: 14, 3: 18}


def ned_al(a, b):
    """Alignment-based NED as the official scorer defines it: mismatched positions / alignment length."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    i, j, L, E = n, m, 0, 0
    while i > 0 or j > 0:
        L += 1
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            E += a[i - 1] != b[j - 1]
            i -= 1
            j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            E += 1
            i -= 1
        else:
            E += 1
            j -= 1
    return E / L if L else 0.0


def _lm_avg(lm, c):
    uni = lm.get("*", {})
    nu = sum(uni.values())
    if not nu:
        return 0.0
    tot = 0.0
    prev = "<s>"
    seq = list(c) + ["</s>"]
    for x in seq:
        pu = (uni.get(x, 0) + 0.5) / (nu + 0.5 * (len(uni) + 1))
        cc = lm.get(prev, {})
        n = sum(cc.values())
        u = max(1, len(cc))
        tot += math.log((cc.get(x, 0) + u * pu) / (n + u))
        prev = x
    return tot / len(seq)


def rr_feats(model, row, tgt, cands, prm, nbeam=None):
    if nbeam is None:
        nbeam = len(cands)
    langs = model["langs"]
    rel = model["rel"]
    srcs = [l for l in langs if l != tgt and row[l] and row[l] != ["?"]]
    ws = [max(rel.get((s, tgt), 0.05), 1e-3) ** prm["gamma"] for s in srcs]
    zw = sum(ws) or 1.0
    ws = [w / zw for w in ws]
    strs = [row[s] for s in srcs]
    mlen = sum(w * len(x) for w, x in zip(ws, strs))
    mton = sum(w * sum(1 for y in x if sclass(y) == "Z") for w, x in zip(ws, strs))
    mvow = sum(w * sum(1 for y in x if is_vowel_cls(sclass(y))) for w, x in zip(ws, strs))
    lm = model["lm"].get(tgt, {})
    ident = model.get("ident", {})
    idr = [ident.get((s, tgt), 0.0) for s in srcs]
    zi = sum(idr) or 1.0
    idw = [v / zi for v in idr]
    top = max(range(len(srcs)), key=lambda i: (ws[i], -i)) if srcs else None
    zs = sum(p for _, p in cands) or 1.0
    out = []
    for i, (c, p) in enumerate(cands):
        c = list(c)
        risk = sum(q * ned(c, list(d)) for d, q in cands) / zs
        nd = [ned(c, x) for x in strs]
        out.append([
            math.log(max(p / zs, 1e-9)),
            1.0 if i == 0 else 0.0,
            risk,
            sum(w * v for w, v in zip(ws, nd)),
            min(nd) if nd else 1.0,
            1.0 if any(c == x for x in strs) else 0.0,
            _lm_avg(lm, c),
            abs(len(c) - mlen),
            abs(sum(1 for y in c if sclass(y) == "Z") - mton),
            len(c) - mlen,
            abs(sum(1 for y in c if is_vowel_cls(sclass(y))) - mvow),
            max([v for v, x in zip(idr, strs) if c == x] or [0.0]),
            sum(w * v for w, v in zip(idw, nd)),
            nd[top] if top is not None else 1.0,
            sum(1 for x in strs if c == x) / max(1, len(strs)),
            1.0 if top is not None and c == strs[top] else 0.0,
            math.log(max(p / zs, 1e-9)) * math.log(1 + len(strs)),
            1.0 if i < nbeam else 0.0,
        ][:RR_NSET[prm.get("rr_feats", 2)]])
    return out


def rr_data_family(langs, data, prm, fam=None, dev_dir=None, folds=2):
    """Reranker training instances from K-fold models on the training sets of one family (rows built as at test time:
    one attested language masked, the other attested reflexes visible)."""
    keys = sorted(data)
    out = []
    p2 = dict(prm)
    p2["return_cands"] = 2
    for k in range(folds):
        tr = {key: data[key] for i, key in enumerate(keys) if i % folds != k}
        te = [key for i, key in enumerate(keys) if i % folds == k]
        m = train_family_data(list(langs), {kk: dict(v) for kk, v in tr.items()}, prm, fam=fam, dev_dir=dev_dir)
        m["_S"] = Scorer(m["seg_pmi"], m["cls_pmi"])
        for key in te:
            r = data[key]
            att = [l for l in langs if r[l]]
            if len(att) < prm.get("rr_minatt", 3):
                continue
            for t in att:
                row = dict(r)
                row[t] = ["?"]
                cands, nbeam = predict_row(m, row, t, p2)
                if len(cands) < 2:
                    continue
                F = rr_feats(m, row, t, cands, prm, nbeam=nbeam)
                L = [ned_al(r[t], list(c)) for c, _ in cands]
                out.append((fam, t, F, L))
    return out


DEV_FAMS = ["abrahammonpa", "allenbai", "backstromnorthernpakistan", "castrosui", "davletshinaztecan",
            "felekesemitic", "hantganbangime", "hattorijaponic", "listsamplesize", "mannburmish"]


def dev_full(dev_dir, dfam):
    """Full cognate sets of a development family: training-0.10 rows plus test-0.10 rows merged per set."""
    langs, tr = load(os.path.join(dev_dir, dfam, "training-0.10.tsv"))
    _, te = load(os.path.join(dev_dir, dfam, "test-0.10.tsv"))
    full = {k: dict(v) for k, v in tr.items()}
    for k in sorted(te):
        b = k.rsplit("-", 1)[0]
        r = full.setdefault("t" + b, {l: [] for l in langs})
        for l in langs:
            v = te[k][l]
            if v and v != ["?"]:
                r[l] = v
    return langs, {k: v for k, v in full.items() if sum(1 for l in langs if v[l]) >= 2}


def fit_reranker(insts, prm):
    import numpy as np
    from scipy.optimize import minimize
    # weights: each family equal, each language equal within its family, each item equal within its language
    cnt = Counter((f, t) for f, t, _, _ in insts)
    nl = Counter(f for f, t in cnt)
    nf = len(nl)
    d = len(insts[0][2][0])
    Fs, Ls, Ws = [], [], []
    for f, t, F, L in insts:
        Fs.append(np.array(F, dtype=float))
        Ls.append(np.array(L, dtype=float))
        Ws.append(1.0 / (cnt[(f, t)] * nl[f] * nf))
    w0 = np.zeros(d)
    w0[0] = 1.0
    lam = prm.get("rr_l2", 0.01)
    T = prm.get("rr_temp", 1.0)

    def obj(w):
        tot = 0.0
        g = np.zeros(d)
        for F, L, wt in zip(Fs, Ls, Ws):
            s = F.dot(w) / T
            s = s - s.max()
            e = np.exp(s)
            pr = e / e.sum()
            el = pr.dot(L)
            tot += wt * el
            g += wt * ((pr * (L - el))[:, None] * F).sum(axis=0) / T
        r = w - w0
        return tot + lam * r.dot(r), g + 2 * lam * r

    res = minimize(obj, w0, jac=True, method="L-BFGS-B", options={"maxiter": 300})
    return [float(x) for x in res.x], float(obj(w0)[0]), float(res.fun)


def ned(a, b):
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 1.0
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        ai = a[i - 1]
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ai != b[j - 1]))
        prev = cur
    return prev[m] / max(n, m)


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


def train(manifest, model_dir):
    prm = params()
    with open(manifest) as f:
        man = json.load(f)
    insts = []
    for fam in sorted(man["surprise_train"]):
        m = train_family(man["surprise_train"][fam], prm, fam=fam, dev_dir=man.get("dev_dir"))
        with open(os.path.join(model_dir, "%s.pkl" % fam), "wb") as f:
            pickle.dump(m, f, protocol=4)
        if prm.get("rerank", 0):
            langs, data = load(man["surprise_train"][fam])
            insts += rr_data_family(langs, data, prm, fam=fam, dev_dir=man.get("dev_dir"))
    if prm.get("rerank", 0) and prm.get("rr_dev", 0) and man.get("dev_dir"):
        for dfam in DEV_FAMS:
            langs, data = dev_full(man["dev_dir"], dfam)
            insts += rr_data_family(langs, data, prm, fam="dev:" + dfam, dev_dir=None)
    if prm.get("rerank", 0):
        w, f0, f1 = fit_reranker(insts, prm)
        with open(os.path.join(model_dir, "rerank.json"), "w") as f:
            json.dump({"w": w, "names": RR_NAMES, "n": len(insts), "obj0": f0, "obj": f1}, f, sort_keys=True)
    with open(os.path.join(model_dir, "params.json"), "w") as f:
        json.dump(prm, f, sort_keys=True)


def load_model(model_dir, fam):
    with open(os.path.join(model_dir, "%s.pkl" % fam), "rb") as f:
        m = pickle.load(f)
    m["_S"] = Scorer(m["seg_pmi"], m["cls_pmi"])
    q = os.path.join(model_dir, "rerank.json")
    if os.path.isfile(q):
        with open(q) as f:
            m["_rr"] = json.load(f)["w"]
    return m


def predict(model_dir, fam, jobs):
    prm = params()
    set_feature_flags(prm)
    m = load_model(model_dir, fam)
    for ln in open(jobs):
        inp, outp = ln.rstrip("\n").split("\t")
        langs, data = load(inp)
        with open(outp, "w", encoding="utf-8") as f:
            f.write("COGID\t" + "\t".join(langs) + "\n")
            for key, row in data.items():
                tgt = [l for l in langs if row[l] == ["?"]][0]
                pred = predict_row(m, row, tgt, prm)
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
        train(a.manifest, a.model_dir)
    else:
        predict(a.model_dir, a.family, a.jobs)
