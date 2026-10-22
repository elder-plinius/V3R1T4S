"""CLASSIFIER lens system (run 2026-10-18-0202; started from the code of run 2026-10-18-0104's classifier lens):
MSA columns -> per-column discriminative classifiers (mixture) -> beam + MBR.

Run 2026-10-18-0202 additions: a joint log-linear model per (family, target) with copy features ('candidate equals
source s's segment', first-segment and base-letter matches, agreeing-source counts) over candidates = target labels +
family segments (own L-BFGS); a linear mixture of three members (absolute-label LR, copy-label LR, log-linear); a
family-pooled back-off log-linear model (target-agnostic ranked-source + copy features + target identity) weighted
kappa/(n_t+kappa); temperature 2 before beam/MBR; weights pruned at 0.01 and stored as CSR, one file per family;
training parallelised over (family, target) jobs in a 2-process spawn pool. Final options: config.json.

train --manifest M --model-dir D
    For each surprise family (only the manifest's training file), for every training cognate set and every attested
    language t: progressive multiple alignment of the OTHER attested reflexes (exactly as at test time), then the
    reflex of t is aligned to that profile; each profile column gets the label = t's segment(s) at that column
    ("-" = deletion; target insertions are glued to a neighbouring column as a multi-segment unit).
    One multinomial logistic regression per (family, target language) on sparse one-hot features of the column
    (source segment by language, its sound class and base letter, left/right context in each source, column majority,
    position). Seeds fixed; liblinear/lbfgs are deterministic.
predict --model-dir D --family F --jobs J
    Each row alone: MSA of its visible reflexes, column posteriors, beam over columns -> n-best strings, choice by
    minimum Bayes risk under item NED (unit-cost alignment, mismatches / alignment length).

Standard library + numpy + scipy + scikit-learn. Options: config.json next to this file, then env CLS_OPTS (JSON; for
development only, never set in frozen runs).
"""
import argparse
import json
import math
import os
import pickle
import sys
import unicodedata
from collections import Counter, defaultdict

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

HERE = os.path.dirname(os.path.abspath(__file__))
OPTS = {
    "C": 1.0,              # inverse L2 strength of the LR
    "ctx": True,           # left/right context features
    "beam": 32,            # n-best size
    "topk": 5,             # labels per column entering the beam
    "mbr": True,           # MBR choice among the n-best (else argmax)
    "temp": 1.0,           # temperature on column log-probs before beam/MBR
    "model": "lr",         # lr | hgb
    "pool_dev": False,     # unused placeholder
    "maxiter": 300,
    "copy": 0,             # relative labels @k = copy the k-th ranked source's segment
    "ens": None,           # list of members {"m": "lr"|"ll", "copy": k, "C": c, "w": weight}; linear mixture
    "Cu": 10.0,            # inverse L2 strength of the LL copy-feature weights
    "eqc": 0,              # LL copy features conjoined with sound class (dev: worse)
    "llv": "fam",          # LL candidates: target labels + all family segments ("fam") or target labels ("tgt")
    "eqr": 0,              # copy feature 'equals the k-th most similar source'
    "pool": 0,             # family-pooled back-off LL model
    "pool_cap": 6000,      # max columns for the pooled model (deterministic thinning)
    "pool_opts": {},       # option overrides while fitting the pooled model
    "pool_src": 0,         # source-specific segment features in the pooled model (dev: worse)
    "kappa": 20.0,         # back-off weight of the pooled model = kappa / (n_t + kappa), n_t = training reflexes of t
    "ls_m": 0,             # smoothing of language similarities (dev: no gain)
    "prune": 0.0,          # prune |w| < prune, store CSR float32
    "wmem": None,          # predict-time override of member weights (dev only)
    "lmw": 0.0,            # target trigram LM rescoring weight (dev: worse)
    "rank": 0,             # rank features: segments of the k sources most similar to the target
}
TRAIN_KEYS = ("C", "Cu", "ctx", "model", "maxiter", "pool_dev", "rank", "copy", "eqc", "llv", "ens", "eqr", "pool",
              "pool_cap", "pool_opts", "pool_src", "ls_m", "prune")
if os.path.isfile(os.path.join(HERE, "config.json")):
    OPTS.update(json.load(open(os.path.join(HERE, "config.json"))))
if os.environ.get("CLS_OPTS"):
    OPTS.update(json.loads(os.environ["CLS_OPTS"]))


# ---------------------------------------------------------------- data
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


# ---------------------------------------------------------------- sound classes (generic symbol table, no words)
VOW = set("aeiouəɛɔɨɯɜɑɪɤyɿʊæøœɒʅɐʌʉɵʏɶɞʯ")
CLS = {}
for chs, c in [("pbɓ", "P"), ("fvɸβʋ", "B"), ("mɱ", "M"), ("tdʈɖɗȶ", "T"), ("θð", "D"),
               ("szʃʒɕʑʂʐ", "S"), ("cʨʥɟ", "C"), ("kgɡqɢ", "K"), ("xɣχʁħʕ", "G"), ("nɲȵŋɴɳ", "N"),
               ("lɭɬɮʎ", "L"), ("rɾɹɽʀ", "R"), ("wɥ", "W"), ("jʝ", "J"), ("hɦʔ", "H")]:
    for ch in chs:
        CLS[ch] = c
PLACE = {"P": "lab", "B": "lab", "M": "lab", "W": "lab", "T": "cor", "D": "cor", "S": "cor", "C": "cor",
         "N": "cor", "L": "cor", "R": "cor", "J": "pal", "K": "dor", "G": "dor", "H": "lar"}
TONECH = set("⁰¹²³⁴⁵⁶⁷⁸⁹0123456789˥˦˧˨˩")
_bc = {}


def base_class(seg):
    r = _bc.get(seg)
    if r is not None:
        return r
    if seg in ("-", "#"):
        r = (seg, seg)
    elif all(ch in TONECH for ch in seg):
        r = ("TONE", "TONE")
    elif seg == "+":
        r = ("+", "+")
    else:
        b = None
        for ch in unicodedata.normalize("NFD", seg):
            if unicodedata.category(ch).startswith("L") and unicodedata.category(ch) != "Lm":
                b = ch
                break
        if b is None:
            b = seg[0]
        c = "V" if b in VOW else CLS.get(b, "?")
        r = (b, c)
    _bc[seg] = r
    return r


_sc = {}


def sim(a, b):
    k = (a, b)
    r = _sc.get(k)
    if r is not None:
        return r
    if a == b:
        r = 2.0
    else:
        ba, ca = base_class(a)
        bb, cb = base_class(b)
        if (ca == "TONE") != (cb == "TONE"):
            r = -3.0
        elif ca == "TONE":
            r = 1.0
        elif ba == bb:
            r = 1.5
        elif ca == cb:
            r = 1.0 if ca != "?" else 0.0
        elif (ca == "V") != (cb == "V"):
            r = -1.0 if (ca in ("W", "J") or cb in ("W", "J")) else -1.5
        elif PLACE.get(ca) and PLACE.get(ca) == PLACE.get(cb):
            r = 0.0
        else:
            r = -0.5
    _sc[k] = r
    return r


GAP = -1.0


def nw_pair(a, b):
    """global alignment score of two segment lists"""
    n, m = len(a), len(b)
    prev = [GAP * j for j in range(m + 1)]
    for i in range(1, n + 1):
        cur = [GAP * i] + [0.0] * m
        ai = a[i - 1]
        for j in range(1, m + 1):
            cur[j] = max(prev[j - 1] + sim(ai, b[j - 1]), prev[j] + GAP, cur[j - 1] + GAP)
        prev = cur
    return prev[m]


def align_seq_profile(seq, prof):
    """prof: list of columns, each a Counter of non-gap segments (with total count). Returns list of pairs
    (col_index or None, seq_index or None) in order."""
    n, m = len(seq), len(prof)
    colsc = []
    for col in prof:
        tot = sum(col.values())
        colsc.append([(s, c / tot) for s, c in col.items()])
    S = [[0.0] * (m + 1) for _ in range(n + 1)]
    B = [[0] * (m + 1) for _ in range(n + 1)]
    for j in range(1, m + 1):
        S[0][j] = GAP * j
        B[0][j] = 2
    for i in range(1, n + 1):
        S[i][0] = GAP * i
        B[i][0] = 1
        x = seq[i - 1]
        for j in range(1, m + 1):
            d = S[i - 1][j - 1] + sum(w * sim(x, s) for s, w in colsc[j - 1])
            u = S[i - 1][j] + GAP
            l = S[i][j - 1] + GAP
            if d >= u and d >= l:
                S[i][j], B[i][j] = d, 0
            elif u >= l:
                S[i][j], B[i][j] = u, 1
            else:
                S[i][j], B[i][j] = l, 2
    i, j, out = n, m, []
    while i > 0 or j > 0:
        b = B[i][j]
        if b == 0:
            out.append((j - 1, i - 1)); i -= 1; j -= 1
        elif b == 1:
            out.append((None, i - 1)); i -= 1
        else:
            out.append((j - 1, None)); j -= 1
    return out[::-1]


def msa(seqs, order_langs, pair_scores):
    """progressive center-star MSA. seqs: {lang: segs}. Returns (langs, rows) rows[l] = list with '-' gaps."""
    langs = list(order_langs)
    if len(langs) == 1:
        return langs, {langs[0]: list(seqs[langs[0]])}
    tot = {l: sum(pair_scores[(l, o)] for o in langs if o != l) for l in langs}
    center = max(langs, key=lambda l: (tot[l], -langs.index(l)))
    rest = sorted([l for l in langs if l != center], key=lambda l: (-pair_scores[(center, l)], langs.index(l)))
    rows = {center: list(seqs[center])}
    for l in rest:
        prof = []
        L = len(next(iter(rows.values())))
        for j in range(L):
            prof.append(Counter(r[j] for r in rows.values() if r[j] != "-"))
        al = align_seq_profile(seqs[l], prof)
        newrows = {k: [] for k in rows}
        newrows[l] = []
        for cj, si in al:
            for k in rows:
                newrows[k].append(rows[k][cj] if cj is not None else "-")
            newrows[l].append(seqs[l][si] if si is not None else "-")
        rows = newrows
    return langs, rows


def pairwise_all(seqs, langs):
    ps = {}
    for i, a in enumerate(langs):
        for b in langs[i + 1:]:
            sa, sb = seqs[a], seqs[b]
            v = nw_pair(sa, sb) / max(len(sa), len(sb), 1)
            ps[(a, b)] = v
            ps[(b, a)] = v
    return ps


def target_labels(rows, tseq):
    """align target sequence to the profile of rows; return a label per column"""
    L = len(next(iter(rows.values())))
    prof = [Counter(r[j] for r in rows.values() if r[j] != "-") for j in range(L)]
    al = align_seq_profile(tseq, prof)
    labs = [[] for _ in range(L)]
    pending = []
    last = None
    for cj, si in al:
        if cj is None:
            if last is None:
                pending.append(tseq[si])
            else:
                labs[last].append(tseq[si])
        else:
            if pending:
                labs[cj].extend(pending)
                pending = []
            if si is not None:
                labs[cj].append(tseq[si])
            last = cj
    if pending:  # only if L == 0
        return None
    return [" ".join(x) if x else "-" for x in labs]



# ---------------------------------------------------------------- fast progressive MSA with a family-level guide order
def _dp(M, n, m):
    """global alignment on score matrix M (n x m nested lists); returns path [(col or None, seq or None)]"""
    S = [[0.0] * (m + 1) for _ in range(n + 1)]
    B = [[0] * (m + 1) for _ in range(n + 1)]
    for j in range(1, m + 1):
        S[0][j] = GAP * j
        B[0][j] = 2
    for i in range(1, n + 1):
        S[i][0] = GAP * i
        B[i][0] = 1
        Mi = M[i - 1]
        Si, Sp, Bi = S[i], S[i - 1], B[i]
        for j in range(1, m + 1):
            d = Sp[j - 1] + Mi[j - 1]
            u = Sp[j] + GAP
            l = Si[j - 1] + GAP
            if d >= u and d >= l:
                Si[j] = d
            elif u >= l:
                Si[j], Bi[j] = u, 1
            else:
                Si[j], Bi[j] = l, 2
    i, j, out = n, m, []
    while i > 0 or j > 0:
        b = B[i][j]
        if b == 0:
            out.append((j - 1, i - 1)); i -= 1; j -= 1
        elif b == 1:
            out.append((None, i - 1)); i -= 1
        else:
            out.append((j - 1, None)); j -= 1
    return out[::-1]


class Aligner:
    def __init__(self, seqs, extra=()):
        import numpy as np
        inv = {}
        for q in list(seqs.values()) + list(extra):
            for x in q:
                if x not in inv:
                    inv[x] = len(inv)
        self.inv = inv
        syms = list(inv)
        self.Sim = np.array([[sim(a, b) for b in syms] for a in syms], dtype=float).reshape(len(syms), len(syms))
        self.np = np

    def profile_path(self, q, C):
        np = self.np
        qi = [self.inv[x] for x in q]
        W = C / C.sum(axis=1, keepdims=True)
        M = (self.Sim[qi] @ W.T).tolist()
        return _dp(M, len(qi), C.shape[0])

    def msa(self, seqs, order):
        np = self.np
        V = len(self.inv)
        first = order[0]
        rows = {first: list(seqs[first])}
        C = np.zeros((len(seqs[first]), V))
        for j, x in enumerate(seqs[first]):
            C[j, self.inv[x]] += 1
        for l in order[1:]:
            q = seqs[l]
            path = self.profile_path(q, C)
            newrows = {k: [] for k in rows}
            newrows[l] = []
            C2 = np.zeros((len(path), V))
            for jj, (cj, si) in enumerate(path):
                for k in rows:
                    newrows[k].append(rows[k][cj] if cj is not None else "-")
                if cj is not None:
                    C2[jj] = C[cj]
                if si is not None:
                    newrows[l].append(q[si])
                    C2[jj, self.inv[q[si]]] += 1
                else:
                    newrows[l].append("-")
            rows, C = newrows, C2
        self.C = C
        return rows


def guide_order(src, LS, langs):
    if len(src) == 1:
        return list(src)
    tot = {l: sum(LS.get((l, o), 0.0) for o in src if o != l) for l in src}
    center = max(src, key=lambda l: (tot[l], -langs.index(l)))
    rest = sorted([l for l in src if l != center], key=lambda l: (-LS.get((center, l), 0.0), langs.index(l)))
    return [center] + rest


def lang_similarity(langs, data):
    acc = defaultdict(list)
    for key in sorted(data):
        row = data[key]
        att = [l for l in langs if row[l]]
        for i, a in enumerate(att):
            for b in att[i + 1:]:
                v = nw_pair(row[a], row[b]) / max(len(row[a]), len(row[b]), 1)
                acc[(a, b)].append(v)
    LS = {}
    m = OPTS.get("ls_m", 0)
    if m:
        allv = [x for k in sorted(acc) for x in acc[k]]
        mu = sum(allv) / len(allv) if allv else 0.0
        for i, a in enumerate(langs):
            for b in langs[i + 1:]:
                v = acc.get((a, b), [])
                LS[(a, b)] = LS[(b, a)] = (sum(v) + m * mu) / (len(v) + m)
        return LS
    for (a, b), v in acc.items():
        LS[(a, b)] = LS[(b, a)] = sum(v) / len(v)
    return LS


def labels_from_path(path, tseq, L):
    labs = [[] for _ in range(L)]
    pending = []
    last = None
    for cj, si in path:
        if cj is None:
            if last is None:
                pending.append(tseq[si])
            else:
                labs[last].append(tseq[si])
        else:
            if pending:
                labs[cj].extend(pending)
                pending = []
            if si is not None:
                labs[cj].append(tseq[si])
            last = cj
    if pending:
        return None
    return [" ".join(x) if x else "-" for x in labs]


def source_msa(seqs, src, LS, langs, extra=()):
    al = Aligner(seqs, extra)
    order = guide_order(src, LS, langs)
    rows = al.msa(seqs, order)
    return al, rows


# ---------------------------------------------------------------- features
def rank_sources(src, tgt, LS):
    return sorted(src, key=lambda s: (-LS.get((tgt, s), -9.0), s))


def copy_label(lab, segs):
    for k, x in enumerate(segs):
        if lab == x:
            return "@%d" % k
    return lab


def resolve_cols(cols, rows, ranked):
    out = []
    for j, cand in enumerate(cols):
        acc = {}
        for lab, lp in cand:
            if lab.startswith("@"):
                lab = rows[ranked[int(lab[1:])]][j]
            if lab in acc:
                a = acc[lab]
                hi = max(a, lp)
                acc[lab] = hi + math.log(math.exp(a - hi) + math.exp(lp - hi))
            else:
                acc[lab] = lp
        out.append(sorted(acc.items(), key=lambda x: (-x[1], x[0])))
    return out


def column_features(langs_present, rows, L, tgt=None, LS=None):
    """list (per column) of feature-string lists"""
    feats = [[] for _ in range(L)]
    if OPTS.get("rank", 0) and tgt is not None:
        ranked = rank_sources(langs_present, tgt, LS)
        for k, s in enumerate(ranked[:OPTS["rank"]]):
            r = rows[s]
            for j in range(L):
                x = r[j]
                b, c = base_class(x)
                feats[j].append("r%d|%s" % (k, x))
                feats[j].append("r%db|%s" % (k, b))
                feats[j].append("r%dc|%s" % (k, c))
                if k == 0 and OPTS["ctx"]:
                    pl = next((r[i] for i in range(j - 1, -1, -1) if r[i] != "-"), "#")
                    nl = next((r[i] for i in range(j + 1, L) if r[i] != "-"), "#")
                    feats[j].append("r0l|%s|%s" % (base_class(pl)[1], x))
                    feats[j].append("r0r|%s|%s" % (x, base_class(nl)[1]))
        if len(ranked) > 1:
            for j in range(L):
                feats[j].append("r01|%s|%s" % (rows[ranked[0]][j], rows[ranked[1]][j]))
    # per-source non-gap neighbours
    for s in langs_present:
        r = rows[s]
        prevs = []
        p = "#"
        for j in range(L):
            prevs.append(p)
            if r[j] != "-":
                p = r[j]
        nexts = [None] * L
        nx = "#"
        for j in range(L - 1, -1, -1):
            nexts[j] = nx
            if r[j] != "-":
                nx = r[j]
        for j in range(L):
            x = r[j]
            b, c = base_class(x)
            f = feats[j]
            f.append("x|%s|%s" % (s, x))
            f.append("b|%s|%s" % (s, b))
            f.append("c|%s|%s" % (s, c))
            if OPTS["ctx"]:
                f.append("xl|%s|%s|%s" % (s, base_class(prevs[j])[1], x))
                f.append("xr|%s|%s|%s" % (s, x, base_class(nexts[j])[1]))
                if x != "-":
                    f.append("bl|%s|%s|%s" % (s, prevs[j] == "#", b))
                    f.append("br|%s|%s|%s" % (s, b, nexts[j] == "#"))
    for j in range(L):
        col = [rows[s][j] for s in langs_present]
        cnt = Counter(col)
        ng = [x for x in col if x != "-"]
        f = feats[j]
        if ng:
            mx = Counter(ng).most_common()
            top = sorted([x for x, c in mx if c == mx[0][1]])[0]
            f.append("maj|%s" % top)
            f.append("majb|%s" % base_class(top)[0])
            cc = Counter(base_class(x)[1] for x in ng).most_common()
            f.append("majc|%s" % sorted([x for x, c in cc if c == cc[0][1]])[0])
        gf = cnt.get("-", 0) / len(col)
        f.append("gap|%d" % int(gf * 4 + 0.5))
        f.append("pos0|%d" % min(j, 3))
        f.append("posE|%d" % min(L - 1 - j, 3))
        f.append("bias")
    return feats


def prep_row(seqs):
    """seqs: {lang: segs} of visible sources (ordered as in header). Returns rows, L"""
    langs = list(seqs)
    ps = pairwise_all(seqs, langs)
    _, rows = msa(seqs, langs, ps)
    L = len(next(iter(rows.values())))
    return langs, rows, L


# ---------------------------------------------------------------- train
def build_examples(langs, data, LS, only=None):
    ex = defaultdict(lambda: ([], [], [], []))  # t -> (feature lists, labels, column source segs, ranked segs)
    for key in sorted(data):
        row = data[key]
        att = [l for l in langs if row[l]]
        if len(att) < 2:
            continue
        for t in att:
            if only is not None and t != only:
                continue
            src = [l for l in att if l != t]
            seqs = {l: row[l] for l in src}
            al, rows = source_msa(seqs, src, LS, langs, extra=[row[t]])
            L = len(next(iter(rows.values())))
            labs = labels_from_path(al.profile_path(row[t], al.C), row[t], L)
            if labs is None:
                continue
            feats = column_features(src, rows, L, t, LS)
            X, Y, SG, RK = ex[t]
            X.extend(feats)
            Y.extend(labs)
            ranked = rank_sources(src, t, LS)
            SG.extend(tuple((l, rows[l][j]) for l in ranked) for j in range(L))
            RK.extend(tuple(rows[r][j] for r in ranked[:6]) for j in range(L))
    return ex


def fit_one(X, Y, C=None):
    from sklearn.feature_extraction import FeatureHasher  # noqa
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    from scipy.sparse import csr_matrix
    vocab = {}
    for fl in X:
        for f in fl:
            if f not in vocab:
                vocab[f] = len(vocab)
    ind, ptr = [], [0]
    for fl in X:
        ids = sorted(set(vocab[f] for f in fl))
        ind.extend(ids)
        ptr.append(len(ind))
    M = csr_matrix((np.ones(len(ind)), np.array(ind), np.array(ptr)), shape=(len(X), len(vocab)))
    classes = sorted(set(Y))
    if len(classes) == 1:
        return {"vocab": vocab, "classes": classes, "const": True}
    if OPTS["model"] == "lr":
        clf = LogisticRegression(C=OPTS["C"] if C is None else C, max_iter=OPTS["maxiter"], tol=1e-4)
        clf.fit(M, Y)
        return {"vocab": vocab, "classes": list(clf.classes_), "coef": clf.coef_.astype("float32"),
                "intercept": clf.intercept_.astype("float32"), "const": False}
    raise SystemExit("unknown model")



# ---------------------------------------------------------------- joint log-linear model with copy features
def copy_feats_col(sg, v, vb, vfirst):
    """copy-feature names firing for candidate label v (base letter vb, first segment vfirst) in a column whose present
    sources have segments sg = ((lang, seg), ...)"""
    out = []
    k = 0
    eqr = OPTS.get("eqr", 0)
    for idx, (l, x) in enumerate(sg):
        if x == v:
            if eqr:
                out.append("eqr|%d" % min(idx, 3))
            out.append("eq|" + l)
            if OPTS.get("eqc", 0):
                c = base_class(x)[1]
                out.append("eqc|%s|%s" % (l, c))
                out.append("eqc|%s" % c)
            k += 1
        elif x != "-" and v != "-":
            if vfirst == x:
                out.append("eq1|" + l)
            elif base_class(x)[0] == vb:
                out.append("beq|" + l)
    if k:
        out.append("cnt|%d" % min(k, 5))
        out.append("frac|%d" % int(4 * k / len(sg) + 0.5))
    return out


class LLData:
    """builds the sparse (column, candidate) copy-feature triplets for a list of columns over label list V"""
    def __init__(self, V, gvocab, grow):
        self.V = V
        self.vi = {v: i for i, v in enumerate(V)}
        self.gvocab = gvocab
        self.grow = grow
        self.vbase = [base_class(v.split()[0])[0] if v != "-" else "-" for v in V]
        self.vfirst = [v.split()[0] if v != "-" else "-" for v in V]
        # index: segment -> candidate indices related to it (equal, first segment equal, same base letter)
        self.rel = {}

    def related(self, x):
        r = self.rel.get(x)
        if r is None:
            if x == "-":
                r = [self.vi["-"]] if "-" in self.vi else []
            else:
                bx = base_class(x)[0]
                r = [i for i, v in enumerate(self.V) if v != "-" and (v == x or self.vfirst[i] == x or self.vbase[i] == bx)]
            self.rel[x] = r
        return r

    def triplets(self, SG):
        I, J, G = [], [], []
        gv = self.gvocab
        for i, sg in enumerate(SG):
            cand = set()
            for _, x in sg:
                cand.update(self.related(x))
            for j in sorted(cand):
                for g in copy_feats_col(sg, self.V[j], self.vbase[j], self.vfirst[j]):
                    gi = gv.get(g)
                    if gi is None:
                        if not self.grow:
                            continue
                        gi = gv[g] = len(gv)
                    I.append(i); J.append(j); G.append(gi)
        import numpy as np
        return np.array(I, dtype=np.int64), np.array(J, dtype=np.int64), np.array(G, dtype=np.int64)


def fit_ll(X, Y, SG):
    import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.optimize import minimize
    vocab = {}
    for fl in X:
        for f in fl:
            if f not in vocab:
                vocab[f] = len(vocab)
    ind, ptr = [], [0]
    for fl in X:
        ids = sorted(set(vocab[f] for f in fl))
        ind.extend(ids)
        ptr.append(len(ind))
    n, F = len(X), len(vocab)
    M = csr_matrix((np.ones(len(ind)), np.array(ind), np.array(ptr)), shape=(n, F))
    segs = set()
    for sg in SG:
        for _, x in sg:
            segs.add(x)
    V = sorted(set(Y) | segs | {"-"}) if OPTS.get("llv", "fam") == "fam" else sorted(set(Y) | {"-"})
    K = len(V)
    gvocab = {}
    D = LLData(V, gvocab, True)
    I, J, G = D.triplets(SG)
    ng = len(gvocab)
    y = np.array([D.vi[v] for v in Y], dtype=np.int64)
    C, Cu = OPTS["C"], OPTS.get("Cu", 10.0)
    MT = M.T.tocsr()
    nW = F * K

    def fg(theta):
        W = theta[:nW].reshape(F, K)
        b = theta[nW:nW + K]
        u = theta[nW + K:]
        Z = np.asarray(M @ W) + b
        if len(I):
            np.add.at(Z, (I, J), u[G])
        Z -= Z.max(axis=1, keepdims=True)
        E = np.exp(Z)
        S = E.sum(axis=1)
        loss = float(np.log(S).sum() - Z[np.arange(n), y].sum())
        P = E / S[:, None]
        P[np.arange(n), y] -= 1.0
        gW = np.asarray(MT @ P) + W / C
        gb = P.sum(axis=0)
        gu = (np.bincount(G, weights=P[I, J], minlength=ng) if len(I) else np.zeros(ng)) + u / Cu
        loss += float((W * W).sum() / (2 * C) + (u * u).sum() / (2 * Cu))
        return loss, np.concatenate([gW.ravel(), gb, gu])

    theta0 = np.zeros(nW + K + ng)
    r = minimize(fg, theta0, jac=True, method="L-BFGS-B", options={"maxiter": OPTS["maxiter"], "gtol": 1e-5})
    th = r.x
    return {"ll": True, "vocab": vocab, "V": V, "gvocab": gvocab, "W": th[:nW].reshape(F, K).astype("float32"),
            "b": th[nW:nW + K].astype("float32"), "u": th[nW + K:].astype("float32"), "const": False}


def column_posteriors_ll(mod, feats, SG, topk=None):
    import numpy as np
    V, voc = mod["V"], mod["vocab"]
    b, u = mod["b"], mod["u"]
    D = mod.get("_D")
    if D is None:
        D = mod["_D"] = LLData(V, mod["gvocab"], False)
    I, J, G = D.triplets(SG)
    out = []
    Zc = np.zeros((len(feats), len(V)), dtype="float64")
    if len(I):
        np.add.at(Zc, (I, J), u[G])
    for i, fl in enumerate(feats):
        ids = sorted(set(voc[f] for f in fl if f in voc))
        z = rowsum(mod, ids, len(V)) + b + Zc[i]
        labs = list(V)
        # unseen source segments: candidates scored by their copy features alone (+ median bias)
        extra = sorted({x for _, x in SG[i] if x not in D.vi})
        if extra:
            ze = []
            for x in extra:
                fs = copy_feats_col(SG[i], x, base_class(x)[0], x)
                ze.append(float(np.median(b)) + sum(float(u[mod["gvocab"][g]]) for g in fs if g in mod["gvocab"]))
            z = np.concatenate([z, np.array(ze)])
            labs = labs + extra
        if topk is None:
            z = z / OPTS["temp"]
        z = z - z.max()
        lps = z - math.log(np.exp(z).sum())
        order = np.argsort(-lps, kind="stable")[:topk or OPTS["topk"]]
        out.append([(labs[k], float(lps[k])) for k in order])
    return out

def compact(md, tau):
    """prune |weight| < tau and store the feature-by-label weight matrix as CSR float32 (model size; deterministic)"""
    import numpy as np
    from scipy.sparse import csr_matrix
    if md.get("const") or tau <= 0:
        return md
    if md.get("ll"):
        W = np.asarray(md.pop("W"), dtype="float32")
    else:
        W = np.asarray(md.pop("coef"), dtype="float32").T.copy()
    W[np.abs(W) < tau] = 0.0
    md["Wc"] = csr_matrix(W)
    return md


def rowsum(md, ids, K):
    import numpy as np
    if "Wc" in md:
        if not ids:
            return np.zeros(K, dtype="float32")
        return np.asarray(md["Wc"][ids].sum(axis=0)).ravel()
    if md.get("ll"):
        return md["W"][ids].sum(axis=0)
    return md["coef"][:, ids].sum(axis=1)


def fit_target(X, Y, SG, RK):
    """one model per ensemble member (OPTS['ens']) or the single model of OPTS['model']"""
    specs = OPTS.get("ens") or [{"m": OPTS["model"], "copy": OPTS.get("copy", 0), "w": 1.0}]
    out = []
    for sp in specs:
        if sp["m"] == "ll":
            md = fit_ll(X, Y, SG)
        else:
            k = sp.get("copy", 0)
            Yc = [copy_label(y, rk[:k]) for y, rk in zip(Y, RK)] if k else Y
            md = fit_one(X, Yc, sp.get("C"))
        md["copy"] = sp.get("copy", 0) if sp["m"] != "ll" else 0
        md["w"] = sp.get("w", 1.0)
        out.append(compact(md, OPTS.get("prune", 0.0)))
    return out


def _ls_job(args):
    fam, path, opts = args
    OPTS.update(opts)
    langs, data = load(path)
    return fam, langs, lang_similarity(langs, data)


def _dispatch(args):
    if args[2] == "__pool__":
        return _pool_job((args[0], args[1], args[3], args[4]))
    return _fit_job(args)


def _fit_job(args):
    fam, path, t, LS, opts = args
    OPTS.update(opts)
    langs, data = load(path)
    ex = build_examples(langs, data, LS, only=t)
    if t not in ex or not ex[t][0]:
        return fam, t, None, 0
    return fam, t, fit_target(*ex[t]), len(ex[t][1])


POOL_PREFIX = ("r0|", "r0b|", "r0c|", "r0l|", "r0r|", "r01|", "r1|", "r1b|", "r1c|", "maj|", "majb|", "majc|",
               "gap|", "pos0|", "posE|", "bias")


def pool_prefix():
    return POOL_PREFIX + (("x|", "b|", "c|") if OPTS.get("pool_src", 0) else ())


def _pool_job(args):
    """family-level pooled log-linear model over the columns of every target: target-agnostic features only (ranked-
    source features, column majority, position) plus copy features; back-off for targets with few training reflexes"""
    fam, path, LS, opts = args
    OPTS.update(opts)
    langs, data = load(path)
    ex = build_examples(langs, data, LS)
    X, Y, SG = [], [], []
    for t in langs:
        if t in ex:
            X.extend([f for f in fl if f.startswith(pool_prefix())] + ["T|" + t] for fl in ex[t][0])
            Y.extend(ex[t][1])
            SG.extend(ex[t][2])
    cap = OPTS.get("pool_cap", 6000)
    if len(Y) > cap:  # deterministic thinning for the largest families
        step = len(Y) / cap
        keep = sorted({int(i * step) for i in range(cap)})
        X = [X[i] for i in keep]; Y = [Y[i] for i in keep]; SG = [SG[i] for i in keep]
    saved = dict(OPTS)
    OPTS.update(OPTS.get("pool_opts", {}))
    md = fit_ll(X, Y, SG)
    OPTS.clear(); OPTS.update(saved)
    md["copy"] = 0
    md["pool"] = True
    md["w"] = 1.0
    return fam, "__pool__", compact(md, OPTS.get("prune", 0.0)), len(Y)


def train_all(paths, workers=2, log=print):
    """paths: {fam: training tsv}. Returns {fam: {"langs", "mods", "LS", "n"}}; fits run per (family, target) in a
    spawn pool of `workers` processes (deterministic: each fit depends only on its inputs)."""
    from multiprocessing import get_context
    model = {}
    with get_context("spawn").Pool(workers) as pool:
        for fam, langs, LS in pool.imap_unordered(_ls_job, [(f, q, dict(OPTS)) for f, q in sorted(paths.items())]):
            model[fam] = {"langs": langs, "mods": {}, "LS": LS, "n": {}}
        jobs = []
        for fam in sorted(paths):
            langs = model[fam]["langs"]
            cost = os.path.getsize(paths[fam]) * len(langs)
            for t in langs:
                jobs.append((cost, fam, t))
        jobs.sort(key=lambda x: (-x[0], x[1], x[2]))
        args = [(fam, paths[fam], t, model[fam]["LS"], dict(OPTS)) for _, fam, t in jobs]
        if OPTS.get("pool"):
            args = [(fam, paths[fam], "__pool__", model[fam]["LS"], dict(OPTS)) for fam in
                    sorted(paths, key=lambda f: (-os.path.getsize(paths[f]) * len(model[f]["langs"]), f))] + args
        for fam, t, mods, n in pool.imap_unordered(_dispatch, args):
            if t == "__pool__":
                model[fam]["pool"] = mods
            elif mods is not None:
                model[fam]["mods"][t] = mods
                model[fam]["n"][t] = n
    for fam in model:
        m = model[fam]
        langs, data = load(paths[fam])
        m["nref"] = {t: sum(1 for r in data.values() if r[t]) for t in langs}
        m["lm"] = {t: lm_train([data[k][t] for k in sorted(data) if data[k][t]]) for t in langs}
        m["mods"] = {t: m["mods"][t] for t in m["langs"] if t in m["mods"]}
        m["n"] = {t: m["n"][t] for t in m["langs"] if t in m["n"]}
        log("trained %s %s" % (fam, m["n"]))
    return {f: model[f] for f in sorted(model)}


def train(manifest, model_dir):
    man = json.load(open(manifest))
    model = train_all(man["surprise_train"], 2, log=lambda x: print(x, flush=True))
    with open(os.path.join(model_dir, "opts.json"), "w") as f:
        json.dump(OPTS, f, sort_keys=True)
    for fam, m in model.items():
        with open(os.path.join(model_dir, "model-%s.pkl" % fam), "wb") as f:
            pickle.dump(m, f, protocol=4)


# ---------------------------------------------------------------- decode
def ned_align(a, b):
    """unit-cost alignment; mismatches (incl. gaps) / alignment length"""
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 0.0
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    i, j, L = n, m, 0
    while i > 0 or j > 0:
        L += 1
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            i -= 1; j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    return D[n][m] / L


def column_posteriors(mod, feats, topk=None):
    import numpy as np
    out = []
    if mod["const"]:
        return [[(mod["classes"][0], 0.0)] for _ in feats]
    voc = mod["vocab"]
    b = mod["intercept"]
    K = len(b)
    for fl in feats:
        ids = sorted(set(voc[f] for f in fl if f in voc))
        if K == 1:  # binary
            z = float(rowsum(mod, ids, 1)[0] + b[0])
            lp1 = -math.log1p(math.exp(-z)) if z > -30 else z
            lp0 = -math.log1p(math.exp(z)) if z < 30 else -z
            lps = np.array([lp0, lp1])
        else:
            z = rowsum(mod, ids, K) + b
            z = z - z.max()
            lps = z - math.log(np.exp(z).sum())
        if topk is None:
            lps = lps / OPTS["temp"]
            lps = lps - math.log(np.exp(lps).sum())
        order = np.argsort(-lps, kind="stable")[:topk or OPTS["topk"]]
        out.append([(mod["classes"][k], float(lps[k])) for k in order])
    return out


def lm_train(seqs):
    """segment trigram counts of a target language's training reflexes (phonotactic LM for n-best rescoring)"""
    c = defaultdict(int)
    for q in seqs:
        h = ["<s>", "<s>"] + list(q) + ["</s>"]
        for i in range(2, len(h)):
            c[(h[i],)] += 1
            c[(h[i - 1], h[i])] += 1
            c[(h[i - 2], h[i - 1], h[i])] += 1
            c[(h[i - 1],) + ("*",)] += 1
            c[(h[i - 2], h[i - 1]) + ("*",)] += 1
        c[("*",)] += len(h) - 2
    return dict(c)


def lm_logp(lm, q):
    """interpolated trigram (weights c(h)/(c(h)+2)), add-one unigram floor"""
    V = sum(1 for k in lm if len(k) == 1 and k != ("*",)) + 1
    N = lm.get(("*",), 0)
    h = ["<s>", "<s>"] + list(q) + ["</s>"]
    lp = 0.0
    for i in range(2, len(h)):
        x, h1, h2 = h[i], h[i - 1], h[i - 2]
        p = (lm.get((x,), 0) + 1.0) / (N + V)
        c1 = lm.get((h1, "*"), 0)
        if c1:
            a = c1 / (c1 + 2.0)
            p = a * lm.get((h1, x), 0) / c1 + (1 - a) * p
        c2 = lm.get((h2, h1, "*"), 0)
        if c2:
            a = c2 / (c2 + 2.0)
            p = a * lm.get((h2, h1, x), 0) / c2 + (1 - a) * p
        lp += math.log(p)
    return lp


def decode(cols, lm=None):
    beam = [((), 0.0)]
    for cand in cols:
        nb = []
        for labs, lp in beam:
            for lab, l2 in cand:
                nb.append((labs + (lab,), lp + l2))
        nb.sort(key=lambda x: (-x[1], x[0]))
        beam = nb[:OPTS["beam"]]
    strs = {}
    for labs, lp in beam:
        segs = []
        for lab in labs:
            if lab != "-":
                segs.extend(lab.split())
        k = tuple(segs)
        strs[k] = strs.get(k, 0.0) + math.exp(lp)
    lmw = OPTS.get("lmw", 0.0)
    if lm is not None and lmw > 0:
        strs = {k: p * math.exp(lmw * lm_logp(lm, k)) for k, p in strs.items()}
    cands = [k for k in strs if k]
    if not cands:
        return None
    if not OPTS["mbr"]:
        return list(max(cands, key=lambda k: (strs[k], k)))
    tot = sum(strs.values())
    best, bestr = None, None
    for c in cands:
        r = sum(p * ned_align(c, h) for h, p in strs.items()) / tot
        if bestr is None or r < bestr - 1e-12 or (abs(r - bestr) <= 1e-12 and (strs[c], c) > (strs[best], best)):
            best, bestr = c, r
    return list(best)


def predict_row(m, row, langs):
    tgt = [l for l in langs if row[l] == ["?"]][0]
    src = [l for l in langs if l != tgt and row[l] and row[l] != ["?"]]
    seqs = {l: row[l] for l in src}
    _, rows = source_msa(seqs, src, m["LS"], langs)
    L = len(next(iter(rows.values())))
    wm = OPTS.get("wmem")
    mods = [(md, wm[i] if wm else md["w"]) for i, md in enumerate(m["mods"].get(tgt) or [])]
    pred = None
    if m.get("pool") is not None:
        kap = OPTS.get("kappa", 20.0)
        nt = m.get("nref", {}).get(tgt, 0)
        a = nt / (nt + kap)
        tot = sum(w for _, w in mods) or 1.0
        mods = [(md, w / tot * a) for md, w in mods] + [(m["pool"], 1 - a)]
    if mods:
        feats = column_features(src, rows, L, tgt, m["LS"])
        ranked = rank_sources(src, tgt, m["LS"])
        SG = [tuple((l, rows[l][j]) for l in ranked) for j in range(L)]
        mix = [defaultdict(float) for _ in range(L)]
        wsum = sum(w for _, w in mods)
        for md, w in mods:
            if md.get("pool"):
                saved = OPTS.get("eqr", 0)
                OPTS["eqr"] = OPTS.get("pool_opts", {}).get("eqr", saved)
                pf = [[f for f in fl if f.startswith(pool_prefix())] + ["T|" + tgt] for fl in feats]
                cols = column_posteriors_ll(md, pf, SG, topk=40)
                OPTS["eqr"] = saved
            elif md.get("ll"):
                cols = column_posteriors_ll(md, feats, SG, topk=40)
            else:
                cols = column_posteriors(md, feats, topk=40)
            if md["copy"]:
                cols = resolve_cols(cols, rows, ranked)
            for j, cand in enumerate(cols):
                for lab, lp in cand:
                    mix[j][lab] += w / wsum * math.exp(lp)
        cols = []
        for j in range(L):
            items = sorted(mix[j].items(), key=lambda x: (-x[1], x[0]))
            z = sum(p for _, p in items)
            lps = [(lab, math.log(max(p / z, 1e-300)) / OPTS["temp"]) for lab, p in items]
            zz = math.log(sum(math.exp(lp) for _, lp in lps))
            cols.append([(lab, lp - zz) for lab, lp in lps[:OPTS["topk"]]])
        pred = decode(cols, m.get("lm", {}).get(tgt))
    if not pred:
        # fallback: column majority
        pred = []
        for j in range(L):
            ng = [rows[s][j] for s in src if rows[s][j] != "-"]
            if len(ng) * 2 >= len(src):
                mc = Counter(ng).most_common()
                pred.append(sorted([x for x, c in mc if c == mc[0][1]])[0])
        if not pred:
            pred = list(seqs[src[0]])
    return tgt, pred


def predict(model_dir, fam, jobs):
    with open(os.path.join(model_dir, "opts.json")) as f:
        saved = json.load(f)
    for k in TRAIN_KEYS:
        OPTS[k] = saved.get(k)
    with open(os.path.join(model_dir, "model-%s.pkl" % fam), "rb") as f:
        m = pickle.load(f)
    for ln in open(jobs):
        inp, outp = ln.rstrip("\n").split("\t")
        langs, data = load(inp)
        with open(outp, "w", encoding="utf-8") as f:
            f.write("COGID\t" + "\t".join(langs) + "\n")
            for key, row in data.items():
                tgt, pred = predict_row(m, row, langs)
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
