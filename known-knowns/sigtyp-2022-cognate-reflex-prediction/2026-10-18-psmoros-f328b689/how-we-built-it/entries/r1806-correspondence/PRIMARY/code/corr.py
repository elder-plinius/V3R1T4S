"""Correspondence-lens core: multiple alignment of visible reflexes + per-column classifiers per target language.

Alignment: lingpy SCA progressive alignment (Multiple.prog_align) of the reflexes of one cognate set.
Training labels: for a training set with reflexes of languages S+{t}, the set is aligned once (all reflexes); the
target t's row is removed, columns where only t had a segment are dropped and their segments merged into the label of
the neighbouring kept column (previous one; the first kept column for word-initial insertions), and each kept column's
label is the target's segment string there ('' = deletion).  Test time: the visible sources are aligned, each column
is classified, labels are concatenated.
"""
import math
import os
from collections import Counter, defaultdict

GAP = "-"
_CLS = {}


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


def sca(tok):
    c = _CLS.get(tok)
    if c is None:
        if tok == GAP:
            c = GAP
        elif tok == "#":
            c = "#"
        else:
            from lingpy.sequence.sound_classes import tokens2class
            try:
                c = tokens2class([tok], "sca")[0]
            except Exception:
                c = "0"
        _CLS[tok] = c
    return c


def _lev_align(a, b):
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    i, j, pairs = n, m, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            pairs.append((a[i - 1], b[j - 1])); i -= 1; j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            pairs.append((a[i - 1], GAP)); i -= 1
        else:
            pairs.append((GAP, b[j - 1])); j -= 1
    return pairs[::-1]


def msa(seqs):
    """seqs: list of token lists (non-empty). Returns list of aligned rows (same length), GAP for gaps."""
    seqs = [list(s) for s in seqs]
    if len(seqs) == 1:
        return [list(seqs[0])]
    try:
        from lingpy import Multiple
        m = Multiple([" ".join(s) for s in seqs])
        m.prog_align()
        mat = [list(r) for r in m.alm_matrix]
        ok = len(mat) == len(seqs) and all([x for x in r if x != GAP] == s for r, s in zip(mat, seqs))
        if ok and len({len(r) for r in mat}) == 1:
            return mat
    except Exception:
        pass
    # fallback: star alignment to the longest sequence (Levenshtein), deterministic
    c = max(range(len(seqs)), key=lambda i: (len(seqs[i]), -i))
    center = seqs[c]
    # columns indexed by center positions plus insertion slots; simple approach: align each to center, merge
    slots = [[] for _ in range(len(center) + 1)]  # insertions before center position i
    pairs_all = []
    for s in seqs:
        pairs = _lev_align(center, s)
        pairs_all.append(pairs)
        k, ins = 0, defaultdict(int)
        for a, b in pairs:
            if a == GAP:
                ins[k] += 1
            else:
                k += 1
        for kk, v in ins.items():
            slots[kk] = [None] * max(len(slots[kk]), v)
    rows = []
    for s, pairs in zip(seqs, pairs_all):
        row, k, buf = [], 0, []
        for a, b in pairs:
            if a == GAP:
                buf.append(b)
            else:
                row += buf + [GAP] * (len(slots[k]) - len(buf))
                buf = []
                row.append(b)
                k += 1
        row += buf + [GAP] * (len(slots[k]) - len(buf))
        rows.append(row)
    return rows


def split_target(mat, langs, t):
    """mat: aligned rows for langs (list), t: target lang in langs. Returns (src_langs, src_rows, labels)."""
    ti = langs.index(t)
    src = [i for i in range(len(langs)) if i != ti]
    n = len(mat[0])
    keep = [j for j in range(n) if any(mat[i][j] != GAP for i in src)]
    tgt = mat[ti]
    labels = [[] for _ in keep]
    pos = {j: q for q, j in enumerate(keep)}
    pending = []  # target-only segments before the first kept column
    last = -1
    for j in range(n):
        if j in pos:
            q = pos[j]
            if pending:
                labels[q] = pending + labels[q]
                pending = []
            if tgt[j] != GAP:
                labels[q].append(tgt[j])
            last = q
        else:
            if tgt[j] != GAP:
                if last >= 0:
                    labels[last].append(tgt[j])
                else:
                    pending.append(tgt[j])
    if pending and labels:
        labels[-1] += pending
    src_rows = [[mat[i][j] for j in keep] for i in src]
    return [langs[i] for i in src], src_rows, [" ".join(x) for x in labels]


def _prev_tok(r, j):
    k = j - 1
    while k >= 0 and r[k] == GAP:
        k -= 1
    return r[k] if k >= 0 else "#"


def _next_tok(r, j):
    k = j + 1
    while k < len(r) and r[k] == GAP:
        k += 1
    return r[k] if k < len(r) else "#"


def col_features(langs, rows, j, opts):
    n = len(rows[0])
    f = {}
    f["pos=%d" % min(j, 3)] = 1.0
    f["rpos=%d" % min(n - 1 - j, 3)] = 1.0
    clsc = Counter()
    for L, r in zip(langs, rows):
        s = r[j]
        c = sca(s)
        clsc[c] += 1
        f["%s=%s" % (L, s)] = 1.0
        f["%s~%s" % (L, c)] = 1.0
        if opts.get("ctx", 1):
            p, q = _prev_tok(r, j), _next_tok(r, j)
            f["%s<%s" % (L, sca(p))] = 1.0
            f["%s>%s" % (L, sca(q))] = 1.0
            if opts.get("conj", 0):
                f["%s=%s>%s" % (L, s, sca(q))] = 1.0
                f["%s=%s<%s" % (L, s, sca(p))] = 1.0
        if opts.get("bag", 1):
            f["any=%s" % s] = f.get("any=%s" % s, 0.0) + 1.0 / len(rows)
    if clsc:
        f["maj=%s" % clsc.most_common(1)[0][0]] = 1.0
    return f


def row_examples(langs_present, mat, t, opts):
    sl, sr, lab = split_target(mat, langs_present, t)
    feats = [col_features(sl, sr, j, opts) for j in range(len(sr[0]))]
    return feats, lab


class ConstClf:
    def __init__(self, label):
        self.label = label

    def predict_labels(self, X):
        return [self.label] * len(X)


def train_family(rows_aligned, langs, opts, log=None):
    """rows_aligned: list of (langs_present, mat). Returns {target: model}."""
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression
    ex = defaultdict(lambda: ([], []))
    for lp, mat in rows_aligned:
        if len(lp) < 2:
            continue
        for t in lp:
            F, Y = row_examples(lp, mat, t, opts)
            ex[t][0].extend(F)
            ex[t][1].extend(Y)
    models = {}
    for t in langs:
        if t not in ex:
            continue
        F, Y = ex[t]
        cnt = Counter(Y)
        if len(cnt) < 2:
            models[t] = ("const", cnt.most_common(1)[0][0])
            continue
        dv = DictVectorizer(sparse=True)
        X = dv.fit_transform(F)
        clf = LogisticRegression(C=opts.get("C", 1.0), max_iter=opts.get("iters", 300), tol=1e-4)
        clf.fit(X, Y)
        models[t] = ("lr", dv, clf)
        if log:
            log("  %s: %d cols, %d classes, %d feats" % (t, len(Y), len(cnt), X.shape[1]))
    return models


def predict_rows(models, tasks, opts):
    """tasks: list of (key, target, src_langs, src_rows). Returns {key: token list}."""
    out = {}
    byt = defaultdict(list)
    for task in tasks:
        byt[task[1]].append(task)
    for t, ts in byt.items():
        m = models.get(t)
        F, idx = [], []
        for key, _, sl, sr in ts:
            for j in range(len(sr[0])):
                F.append(col_features(sl, sr, j, opts))
                idx.append(key)
        if m is None:
            labs = None
        elif m[0] == "const":
            labs = [m[1]] * len(F)
        else:
            dv, clf = m[1], m[2]
            X = dv.transform(F)
            labs = list(clf.predict(X))
        res = defaultdict(list)
        if labs is not None:
            for key, lab in zip(idx, labs):
                if lab:
                    res[key] += lab.split()
        for key, _, sl, sr in ts:
            pred = res.get(key, [])
            if not pred:  # fallback: copy the longest source
                r = max(sr, key=lambda r: sum(x != GAP for x in r))
                pred = [x for x in r if x != GAP]
            out[key] = pred
    return out


# ---------------------------------------------------------------------------------------------------------------
# Candidate ranker: log-linear model over candidate labels per column, with learned per-source reliability weights
# on copy, sound-class copy and leave-one-out smoothed correspondence log-probabilities (context-free, right context,
# left context), plus language-independent vote features.
# ---------------------------------------------------------------------------------------------------------------
import numpy as np


def lab_of(s):
    return "" if s == GAP else s


def colinfo(sl, sr, j):
    srcs = []
    for L, r in zip(sl, sr):
        s = r[j]
        srcs.append((L, s, sca(_prev_tok(r, j)), sca(_next_tok(r, j))))
    return (tuple(srcs), j, len(sr[0]))


def lab_cls(c):
    if c == "":
        return GAP
    return " ".join(sca(x) for x in c.split())


class Ranker:
    def __init__(self, t, langs, opts):
        self.NPER = 6 if opts.get("ctx2") else 5
        self.t = t
        self.L = [l for l in langs if l != t]
        self.li = {l: i for i, l in enumerate(self.L)}
        self.o = opts
        self.beta = opts.get("beta", 1.0)
        self.xc = int(opts.get("xc", 0))
        self.topu = int(opts.get("topu", 0))
        self.ng = 9 + (1 if self.xc else 0)
        self.ntyp = 3 if opts.get("typed") else 1
        self.PL = self.NPER * self.ntyp  # per-language block size
        self.d = self.PL * len(self.L) + self.ng
        self.w = np.zeros(self.d)
        self.w[self.PL * len(self.L) + 0] = 1.0  # vote share, a sane default when no data

    def _count(self, cols, ys):
        C1, C2, C3, C4 = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
        U = Counter()
        for (srcs, j, n), y in zip(cols, ys):
            U[y] += 1
            for (L, s, pc, nc) in srcs:
                C1[(L, s)][y] += 1
                C2[(L, s, nc)][y] += 1
                C3[(L, s, pc)][y] += 1
                if self.NPER > 5:
                    C4[(L, s, pc, nc)][y] += 1
        self.C1, self.C2, self.C3, self.C4, self.U = C1, C2, C3, C4, U
        self.T4 = {k: sum(v.values()) for k, v in C4.items()}
        self.T1 = {k: sum(v.values()) for k, v in C1.items()}
        self.T2 = {k: sum(v.values()) for k, v in C2.items()}
        self.T3 = {k: sum(v.values()) for k, v in C3.items()}
        self.UT = sum(U.values())
        self.V = len(U) + 1
        CX = defaultdict(Counter)
        for (srcs, j, n), y in zip(cols, ys):
            for (L, s, pc, nc) in srcs:
                CX[s][y] += 1
        self.CX = CX
        self.TX = {k: sum(v.values()) for k, v in CX.items()}
        self.topU = [c for c, _ in sorted(U.items(), key=lambda x: (-x[1], x[0]))[:self.topu + 1]]

    def cands(self, ci, loo=None):
        srcs = ci[0]
        S = set()
        kc = int(self.o.get("kc", 0))
        score = defaultdict(float)
        for (L, s, pc, nc) in srcs:
            S.add(lab_of(s))
            cc = self.C1.get((L, s))
            if cc:
                tot = self.T1[(L, s)] - (1 if loo is not None else 0)
                for c, v in cc.items():
                    v2 = v - (1 if c == loo else 0)
                    if v2 > 0:
                        if kc:
                            score[c] += v2 / tot
                        else:
                            S.add(c)
        if kc and score:
            for c, _ in sorted(score.items(), key=lambda x: (-x[1], x[0]))[:kc]:
                S.add(c)
            if self.xc >= 2:
                cx = self.CX.get(s)
                if cx:
                    nl = sum(1 for x in srcs if x[1] == s)
                    for c, v in cx.items():
                        if v - (nl if c == loo else 0) > 0:
                            S.add(c)
        if self.topu:
            for c in self.topU[:self.topu]:
                if self.U.get(c, 0) - (1 if c == loo else 0) > 0:
                    S.add(c)
        return sorted(S)

    def feats(self, ci, cands, loo=None):
        srcs, j, n = ci
        nL = len(self.L)
        F = np.zeros((len(cands), self.d))
        lo = loo is not None
        UT = self.UT - (1 if lo else 0)
        u = {}
        for k, c in enumerate(cands):
            uc = self.U.get(c, 0) - (1 if lo and c == loo else 0)
            u[c] = (uc + 0.5) / (UT + 0.5 * self.V)
        b = self.beta
        npres = max(len(srcs), 1)
        ccls = [lab_cls(c) for c in cands]
        vote = np.zeros(len(cands))
        cvote = np.zeros(len(cands))
        avg1 = np.zeros(len(cands))
        avg2 = np.zeros(len(cands))
        typ = 0
        if self.ntyp > 1:
            tc = Counter()
            for x in srcs:
                if x[1] != GAP:
                    c0 = sca(x[1])
                    tc[2 if c0.isdigit() else (1 if c0 in "AEIOUY" else 0)] += 1
            if tc:
                typ = sorted(tc.items(), key=lambda x: (-x[1], x[0]))[0][0]
        for (L, s, pc, nc) in srcs:
            i = self.li.get(L)
            if i is None:
                continue
            sp = lab_of(s)
            sc = sca(s) if s != GAP else GAP
            c1 = self.C1.get((L, s), {})
            t1 = self.T1.get((L, s), 0) - (1 if lo else 0)
            c2 = self.C2.get((L, s, nc), {})
            t2 = self.T2.get((L, s, nc), 0) - (1 if lo else 0)
            c3 = self.C3.get((L, s, pc), {})
            t3 = self.T3.get((L, s, pc), 0) - (1 if lo else 0)
            base = i * self.PL + typ * self.NPER
            for k, c in enumerate(cands):
                self_ = 1 if (lo and c == loo) else 0
                q = 0.5 * (1.0 if c == sp else 0.0) + 0.5 * u[c]
                p1 = (c1.get(c, 0) - self_ + b * q) / (t1 + b)
                p2 = (c2.get(c, 0) - self_ + b * p1) / (t2 + b)
                p3 = (c3.get(c, 0) - self_ + b * p1) / (t3 + b)
                cp = 1.0 if c == sp else 0.0
                cl = 1.0 if ccls[k] == sc else 0.0
                lp1 = math.log(p1)
                F[k, base] = cp
                F[k, base + 1] = cl
                F[k, base + 2] = lp1
                F[k, base + 3] = math.log(p2)
                F[k, base + 4] = math.log(p3)
                if self.NPER > 5:
                    c4 = self.C4.get((L, s, pc, nc), {})
                    t4 = self.T4.get((L, s, pc, nc), 0) - (1 if lo else 0)
                    p4 = (c4.get(c, 0) - self_ + b * 0.5 * (p2 + p3)) / (t4 + b)
                    F[k, base + 5] = math.log(p4)
                vote[k] += cp
                cvote[k] += cl
                avg1[k] += lp1
                avg2[k] += math.log(p2)
        g = self.PL * nL
        F[:, g + 0] = vote / npres
        F[:, g + 1] = cvote / npres
        F[:, g + 2] = avg1 / npres
        F[:, g + 3] = avg2 / npres
        if self.xc:
            nseg = Counter(x[1] for x in srcs)
            ax = np.zeros(len(cands))
            for (L, s, pc, nc) in srcs:
                cx = self.CX.get(s, {})
                tx = self.TX.get(s, 0) - (nseg[s] if lo else 0)
                sp = lab_of(s)
                for k, c in enumerate(cands):
                    q = 0.5 * (1.0 if c == sp else 0.0) + 0.5 * u[c]
                    ax[k] += math.log((cx.get(c, 0) - (nseg[s] if (lo and c == loo) else 0) + b * q) / (tx + b))
            F[:, g + 9] = ax / npres
        for k, c in enumerate(cands):
            F[k, g + 4] = math.log(u[c])
            F[k, g + 5] = 1.0 if c == "" else 0.0
            F[k, g + 6] = 1.0 if (c == "" and (j == 0 or j == n - 1)) else 0.0
            F[k, g + 7] = 1.0 if len(c.split()) > 1 else 0.0
            F[k, g + 8] = 1.0 if (vote[k] == npres) else 0.0
        return F

    def fit(self, cols, ys):
        from scipy.optimize import minimize
        self._count(cols, ys)
        Xs, gold, sizes = [], [], []
        miss = 0
        pairs = list(zip(cols, ys))
        cap = int(self.o.get("maxfit", 0))
        if cap and len(pairs) > cap:
            import random
            idx = sorted(random.Random(20261017).sample(range(len(pairs)), cap))
            pairs = [pairs[i] for i in idx]
        for ci, y in pairs:
            cands = self.cands(ci, loo=y)
            if y not in cands:
                miss += 1
                continue
            Xs.append(self.feats(ci, cands, loo=y))
            gold.append(cands.index(y))
            sizes.append(len(cands))
        self.cover = 1.0 - miss / max(len(pairs), 1)
        if not Xs:
            return self
        X = np.vstack(Xs)
        starts = np.concatenate([[0], np.cumsum(sizes)[:-1]]).astype(np.int64)
        gidx = starts + np.array(gold)
        lam = np.full(self.d, float(self.o.get("l2", 1.0)))
        lam[self.PL * len(self.L):] = float(self.o.get("l2g", self.o.get("l2", 1.0)))
        seg = np.repeat(np.arange(len(sizes)), sizes)

        def fun(w):
            s = X @ w
            m = np.maximum.reduceat(s, starts)
            e = np.exp(s - m[seg])
            Z = np.add.reduceat(e, starts)
            lse = m + np.log(Z)
            loss = np.sum(lse) - np.sum(s[gidx]) + 0.5 * np.dot(lam * w, w)
            p = e / Z[seg]
            grad = X.T @ p - X[gidx].sum(axis=0) + lam * w
            return loss, grad

        r = minimize(fun, self.w.copy(), jac=True, method="L-BFGS-B", options={"maxiter": self.o.get("iters", 300)})
        self.w = r.x
        return self

    def dist(self, ci):
        cands = self.cands(ci)
        s = self.feats(ci, cands) @ self.w
        s = s - s.max()
        p = np.exp(s)
        p /= p.sum()
        return cands, p


def train_family_rank(rows_aligned, langs, opts, log=None):
    ex = defaultdict(lambda: ([], []))
    for lp, mat in rows_aligned:
        if len(lp) < 2:
            continue
        for t in lp:
            sl, sr, lab = split_target(mat, lp, t)
            for j in range(len(sr[0])):
                ex[t][0].append(colinfo(sl, sr, j))
                ex[t][1].append(lab[j])
    models = {}
    for t in langs:
        r = Ranker(t, langs, opts)
        if t in ex:
            r.fit(ex[t][0], ex[t][1])
        else:
            r._count([], [])
        models[t] = r
        if log:
            log("  %s: %d cols cover %.3f" % (t, len(ex[t][1]) if t in ex else 0, getattr(r, "cover", 0)))
    return models


def predict_rows_rank(models, tasks, opts):
    out = {}
    for key, t, sl, sr in tasks:
        m = models[t]
        pred = []
        for j in range(len(sr[0])):
            cands, p = m.dist(colinfo(sl, sr, j))
            k = int(np.argmax(p))
            if cands[k]:
                pred += cands[k].split()
        if not pred:
            r = max(sr, key=lambda r: sum(x != GAP for x in r))
            pred = [x for x in r if x != GAP]
        out[key] = pred
    return out


# ---------------------------------------------------------------------------------------------------------------
# n-best over independent column distributions + minimum-Bayes-risk choice under (alignment-based) NED
# ---------------------------------------------------------------------------------------------------------------
def ned_al(a, b):
    """unit-cost alignment: mismatched positions / alignment length (as the scorer's NED, approximately)."""
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 0.0
    D = [[(0, 0)] * (m + 1) for _ in range(n + 1)]  # (cost, length)
    for i in range(1, n + 1):
        D[i][0] = (i, i)
    for j in range(1, m + 1):
        D[0][j] = (j, j)
    for i in range(1, n + 1):
        ai = a[i - 1]
        Di, Dp = D[i], D[i - 1]
        for j in range(1, m + 1):
            c1, l1 = Dp[j - 1]
            c1 += (ai != b[j - 1])
            c2, l2 = Dp[j]
            c3, l3 = Di[j - 1]
            best = min((c1, l1 + 1), (c2 + 1, l2 + 1), (c3 + 1, l3 + 1))
            Di[j] = best
    c, l = D[n][m]
    return c / l


def nbest(cols, N=32, K=6):
    """cols: list of (cands, probs). Returns {token tuple: prob} for the N best label sequences."""
    beams = [((), 0.0)]
    for cands, p in cols:
        order = np.argsort(-p, kind="stable")[:K]
        new = []
        for labs, lp in beams:
            for k in order:
                if p[k] <= 0:
                    continue
                new.append((labs + (cands[k],), lp + math.log(p[k])))
        new.sort(key=lambda x: (-x[1], x[0]))
        beams = new[:N]
    agg = {}
    for labs, lp in beams:
        s = tuple(" ".join(l for l in labs if l).split())
        agg[s] = agg.get(s, 0.0) + math.exp(lp)
    return agg


def mbr_choose(agg, topc=None):
    items = sorted(agg.items(), key=lambda x: (-x[1], x[0]))
    cands = [s for s, _ in items[:topc]] if topc else [s for s, _ in items]
    best, bestv = None, None
    for c in cands:
        if not c:
            continue
        v = sum(p * ned_al(c, d) for d, p in items)
        if bestv is None or v < bestv - 1e-12:
            best, bestv = c, v
    return list(best) if best else []


def predict_rows_rank_mbr(models, tasks, opts):
    out = {}
    N = opts.get("mbr", 32)
    for key, t, sl, sr in tasks:
        m = models[t]
        cols = [m.dist(colinfo(sl, sr, j)) for j in range(len(sr[0]))]
        agg = nbest(cols, N=N, K=opts.get("K", 6))
        pred = mbr_choose(agg, opts.get("topc"))
        if not pred:
            r = max(sr, key=lambda r: sum(x != GAP for x in r))
            pred = [x for x in r if x != GAP]
        out[key] = pred
    return out
