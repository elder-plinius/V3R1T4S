"""Broker lens system (run 2026-10-18-0202): pairwise correspondence transducers on a language graph, with
broker-path composition for sparse pairs, combined across sources as a weighted product of experts.

train (per family, all ordered language pairs s->t that are co-attested in training-P):
  - a pair transducer: the source word (with a BOS slot) emits one target "piece" (0..3 target segments) per source
    segment; alignment by Viterbi segmentation, re-estimated (hard EM) from a sound-class prior;
  - context levels: trigram (left, seg, right) -> piece, class-context, unigram seg -> piece, Witten-Bell smoothed;
  - the base (backoff) distribution of s->t mixes: compositions s->b->t through broker languages b (weighted by the
    reliability of both edges), a target-pooled map (all sources -> t), and a sound-class prior.
predict: each visible source proposes its k-best strings; every candidate is scored by the weighted sum of
  log-probabilities under every source's transducer (forced Viterbi) plus a target bigram phonotactic model; the best
  candidate (optionally an MBR choice) is written. Standard library only; deterministic.
"""
import argparse
import json
import math
import os
import pickle
import sys
import unicodedata
from collections import Counter, defaultdict

BOS, EOS = "<s>", "</s>"
POOL_HOOK = None  # analysis only
MAXP = 3

# ------------------------------------------------------------------ configuration (overridable by env for dev runs)
CFG = {
    "iters": 2,          # hard-EM realignment iterations
    "beta": 1.0,         # Witten-Bell type multiplier
    "r_prior": 1.0,      # base mixture weight of the sound-class prior
    "r_pool": 0.0,       # base mixture weight of the target-pooled map
    "r_comp": 0.0,       # base mixture weight scale of broker compositions
    "r_comp_pred": 3.0,  # if >= 0: composition weight used at prediction only (training keeps r_comp)
    "nbrok": 3,          # brokers per pair
    "kbest": 4,          # candidates per source
    "beam": 8,
    "topp": 5,           # pieces per position in the beam
    "maxsrc": 8,         # sources used in the product of experts
    "wkappa": 5.0,       # source weight n/(n+kappa) (+ broker term)
    "wfloor": 0.2,       # source weight floor for unseen pairs (composition only)
    "wlm": 0.0,          # target LM weight
    "alpha": 6.0,        # source weight exp(-alpha * (cvned - best cvned in row))
    "mbr": 0.0,          # MBR temperature (0 = argmax)
    "usectx": 1,
    "npseudo": 1,        # broker pseudo-sources per row (string-level friends of friends)
    "pgamma": 0.5,       # weight discount of a pseudo-source
    "pmargin": 0.3,      # use a broker only if its compounded cvned < best visible cvned + margin
    "mbrn": 10,
    "hybrid": 0,         # greedy hill-climbing rounds over single edits taken from the candidate pool
    "hybn": 6,
    "wch": 0.4,          # noisy-channel weight: + wch * log P_{t->s}(source | candidate)
    "ptemp": 4.0,        # sharpness of the sound-class prior
    "ctxcv": 1.0,        # blend of contextual cross-fitted NED into the edge reliability
    "cgate": 0.0,        # composition weight * g/(g + n_st) (0 = no gate)
    "ens": 0,            # mixture over ENS_VARIANTS configurations (predict time)
    "enst": 1.0,         # temperature of each variant's PoE posterior
    "ensmbr": 1,         # MBR under NED over the mixture (else argmax)
    "wrev": 0.0,         # weight of right-to-left (reversed-string) transducers in each source's expert
    "pfew": 0,           # extra pseudo-sources for rows with <= 2 visible sources
    "kuni": 0.0,         # extra additive prior strength at the unigram level
    "kctx": 0.0,         # extra additive prior strength at the context levels
    "ctx5": 0,           # add a 5-segment source context level (l2, l, x, r, r2)
    "selfsel": 0,        # per-family option choice by cross-fitting on training-P
    "selcap": 600,       # held-out rows per fold for selfsel
    "selmargin": 0.0,    # bias toward the default option
    "rerank": 0,         # use the cross-fitted reranker (theta) at depth 0
    "cvk": 2,            # folds for the reranker's training rows
    "cvcap": 1500,       # held-out rows per fold and family
}


def env_overrides():
    """Development only: BRK_<KEY> environment overrides, active only when BRK_DEV=1."""
    if os.environ.get("BRK_DEV") != "1":
        return
    for k in list(CFG):
        v = os.environ.get("BRK_" + k.upper())
        if v is not None:
            CFG[k] = type(CFG[k])(float(v)) if not isinstance(CFG[k], int) else int(float(v))


env_overrides()


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


# ------------------------------------------------------------------ sound classes (generic symbol table, no words)
TONE = set("0123456789¹²³⁴⁵⁶⁷⁸⁹⁰₀₁₂₃₄₅₆₇₈₉˥˦˧˨˩⁻")
VOW = set("aeiouyæøœɶɑɒɐəɘɵɜɞɛɔɤɯɨʉɪʏʊɚɝɿʅʯ")
CLS = {}
for chars, c in (("pbɸβfvɓ", "P"), ("tdθðɗʈɖ", "T"), ("szʃʒɕʑʂʐʨʥȿɀ", "S"), ("kgxɣqɢχʁcɟçʝ", "K"),
                 ("m", "M"), ("nŋɲɳɴȵ", "N"), ("rlɾɽɭʎɹɻʀɬɮ", "R"), ("wʋɥɰ", "W"), ("j", "J"), ("hɦʔħʕ", "H")):
    for ch in chars:
        CLS[ch] = c


def strip(seg):
    out = []
    for ch in unicodedata.normalize("NFD", seg):
        if unicodedata.combining(ch):
            continue
        if ch in "ːˑʰʱʷʲˠˤⁿˀ̚˞ʼ":
            continue
        out.append(ch)
    return "".join(out) or seg


def cls(seg):
    if seg in (BOS, EOS):
        return seg
    if seg and all(ch in TONE for ch in seg):
        return "0"
    b = strip(seg)
    if not b:
        return "?"
    if b[0] in VOW:
        return "V"
    c = CLS.get(b[0], "?")
    if c in "TK" and len(b) > 1 and b[1] in "szʃʒɕʑʂʐ":
        return "S"
    return c


def sub_cost(x, y):
    if x == y:
        return 0.0
    cx, cy = cls(x), cls(y)
    if (cx == "0") != (cy == "0"):
        return 3.0
    if cx == "0":
        return 0.3
    if strip(x) == strip(y):
        return 0.15
    if cx == cy:
        return 0.4
    if cx == "V" or cy == "V":
        return 1.0
    return 0.85


# ------------------------------------------------------------------ pair model
class Prior:
    """Sound-class prior over pieces for a target inventory."""

    def __init__(self, inv):
        self.inv = list(inv)
        self.u = 1.0 / max(1, len(self.inv))
        self.cache = {}

    def single(self, x):
        d = self.cache.get(x)
        if d is None:
            cand = set(self.inv)
            if x not in (BOS, EOS):
                cand.add(x)
            sc = {y: math.exp(-CFG["ptemp"] * sub_cost(x, y)) for y in sorted(cand)}
            z = sum(sc.values())
            d = {y: v / z for y, v in sc.items()}
            self.cache[x] = d
        return d

    def p(self, x, o):
        if x == BOS:
            if not o:
                return 0.95
            return 0.05 * (self.u ** len(o)) * (0.1 ** (len(o) - 1))
        if not o:
            return 0.08
        s = self.single(x)
        if len(o) == 1:
            return 0.87 * s.get(o[0], 1e-6)
        best = max(s.get(o[i], 1e-6) for i in range(len(o)))
        return 0.05 * (0.1 ** (len(o) - 2)) * best * (self.u ** (len(o) - 1))

    def top(self, x, k=3):
        if x == BOS:
            return [()]
        s = self.single(x)
        return [()] + [(y,) for y, _ in sorted(s.items(), key=lambda z: (-z[1], z[0]))[:k]]


def viterbi(src, tgt, cost):
    """src: tuple with BOS at 0; tgt: tuple. cost(j, piece) -> float. Returns (total, pieces)."""
    n, m = len(src), len(tgt)
    INF = float("inf")
    prev = [INF] * (m + 1)
    prev[0] = 0.0
    back = []
    for j in range(n):
        cur = [INF] * (m + 1)
        bk = [0] * (m + 1)
        for k in range(m + 1):
            best, bl = INF, 0
            for l in range(0, min(MAXP, k) + 1):
                pv = prev[k - l]
                if pv == INF:
                    continue
                c = pv + cost(j, tgt[k - l:k])
                if c < best:
                    best, bl = c, l
            cur[k] = best
            bk[k] = bl
        back.append(bk)
        prev = cur
    if prev[m] == INF:
        return INF, None
    pieces = []
    k = m
    for j in range(n - 1, -1, -1):
        l = back[j][k]
        pieces.append(tgt[k - l:k])
        k -= l
    return prev[m], pieces[::-1]


def prior_cost_fn(src, prior):
    def cost(j, o):
        return -math.log(prior.p(src[j], o))
    return cost


class Dist:
    """counts h -> Counter(piece); stores (counter, total, types)."""

    def __init__(self):
        self.c = defaultdict(Counter)

    def add(self, h, o, w=1.0):
        self.c[h][o] += w

    def freeze(self):
        out = {}
        for h, cnt in self.c.items():
            out[h] = (dict(cnt), sum(cnt.values()), len(cnt))
        return out


def train_family(langs, data, final=True):
    words = {l: [tuple(r[l]) for r in data.values() if r[l]] for l in langs}
    inv = {l: sorted({s for w in words[l] for s in w}) for l in langs}
    priors = {l: Prior(inv[l]) for l in langs}
    pairs = {}
    for s in langs:
        for t in langs:
            if s == t:
                continue
            ps = [((BOS,) + tuple(r[s]), tuple(r[t])) for r in data.values()
                  if r[s] and r[t] and len(r[t]) <= MAXP * (len(r[s]) + 1)]
            if ps:
                pairs[(s, t)] = ps
    beta = CFG["beta"]
    # ---- hard EM on context-free maps
    align = {}
    for (s, t), ps in pairs.items():
        pr = priors[t]
        al = []
        for a, b in ps:
            _, pcs = viterbi(a, b, prior_cost_fn(a, pr))
            al.append(pcs)
        align[(s, t)] = al
    for _ in range(CFG["iters"]):
        for (s, t), ps in pairs.items():
            pr = priors[t]
            cnt = defaultdict(Counter)
            for (a, b), pcs in zip(ps, align[(s, t)]):
                for x, o in zip(a, pcs):
                    cnt[x][o] += 1
            tot = {x: sum(c.values()) for x, c in cnt.items()}
            typ = {x: len(c) for x, c in cnt.items()}

            def mk(a, cnt=cnt, tot=tot, typ=typ, pr=pr):
                def cost(j, o):
                    x = a[j]
                    p0 = pr.p(x, o)
                    if x in cnt:
                        lam = tot[x] / (tot[x] + beta * typ[x])
                        p = lam * cnt[x].get(o, 0) / tot[x] + (1 - lam) * p0
                    else:
                        p = p0
                    return -math.log(p)
                return cost
            align[(s, t)] = [viterbi(a, b, mk(a))[1] for a, b in ps]
    # ---- final counts per pair
    models = {}
    uni_mle = {}
    pool = defaultdict(lambda: defaultdict(Counter))
    for (s, t), ps in pairs.items():
        tri, cc, uni, c5 = Dist(), Dist(), Dist(), Dist()
        for (a, b), pcs in zip(ps, align[(s, t)]):
            ext = a + (EOS, EOS)
            for j in range(len(a)):
                x, o = a[j], pcs[j]
                l = a[j - 1] if j > 0 else BOS
                l2 = a[j - 2] if j > 1 else BOS
                r = ext[j + 1]
                r2 = ext[j + 2]
                uni.add(x, o)
                cc.add((cls(l), x, cls(r)), o)
                tri.add((l, x, r), o)
                if CFG["ctx5"]:
                    c5.add((l2, l, x, r, r2), o)
                pool[t][x][o] += 1
        models[(s, t)] = {"tri": tri.freeze(), "cls": cc.freeze(), "uni": uni.freeze(), "c5": c5.freeze(),
                          "n": len(ps)}
        u = {}
        for x, (cnt, tot, _) in models[(s, t)]["uni"].items():
            u[x] = {o: v / tot for o, v in cnt.items()}
        uni_mle[(s, t)] = u
    # ---- edge reliability: 2-fold cross-fitted NED of the context-free argmax map (proxy for pair quality)
    for (s, t), ps in pairs.items():
        al = align[(s, t)]
        n = len(ps)
        errs = []
        for fold in (0, 1):
            cnt = defaultdict(Counter)
            for i, ((a, b), pcs) in enumerate(zip(ps, al)):
                if i % 2 != fold:
                    for x, o in zip(a, pcs):
                        cnt[x][o] += 1
            amax = {x: max(sorted(c.items()), key=lambda z: z[1])[0] for x, c in cnt.items()}
            for i, (a, b) in enumerate(ps):
                if i % 2 == fold:
                    out = []
                    for x in a:
                        if x in amax:
                            out.extend(amax[x])
                        elif x != BOS:
                            out.append(x)
                    errs.append(ned(out, b))
        e = sum(errs) / len(errs) if n >= 2 else 0.7
        models[(s, t)]["cvned"] = (n * e + 2 * 0.6) / (n + 2)
    poolp = {}
    for t, d in pool.items():
        poolp[t] = {x: {o: v / sum(c.values()) for o, v in c.items()} for x, c in d.items()}
    # ---- broker compositions s->b->t (context-free), for every ordered pair (also never co-attested ones)
    comp = {}
    for s in langs:
        for t in langs:
            if s == t:
                continue
            cands = []
            for b in langs:
                if b in (s, t) or (s, b) not in uni_mle or (b, t) not in uni_mle:
                    continue
                nsb, nbt = models[(s, b)]["n"], models[(b, t)]["n"]
                r = nsb * nbt / (nsb + nbt)
                cands.append((r, b))
            cands.sort(key=lambda z: (-z[0], z[1]))
            cands = cands[:CFG["nbrok"]]
            if not cands:
                continue
            mix = defaultdict(lambda: defaultdict(float))
            wsum = defaultdict(float)
            for r, b in cands:
                sb, bt = uni_mle[(s, b)], uni_mle[(b, t)]
                for x, dy in sb.items():
                    out = defaultdict(float)
                    for y, py in sorted(dy.items(), key=lambda z: -z[1])[:6]:
                        if x == BOS:
                            if y == ():
                                out[()] += py
                            continue
                        partial = {(): py}
                        for yi in y:
                            dd = bt.get(yi)
                            if dd is None:
                                dd = {(yi,): 1.0}
                            nxt = defaultdict(float)
                            for pre, pp in partial.items():
                                for o, po in sorted(dd.items(), key=lambda z: -z[1])[:4]:
                                    q = pre + o
                                    if len(q) <= MAXP:
                                        nxt[q] += pp * po
                            partial = nxt
                        for q, pq in partial.items():
                            out[q] += pq
                    z = sum(out.values())
                    if z <= 0:
                        continue
                    for q, pq in out.items():
                        mix[x][q] += r * pq / z
                    wsum[x] += r
            r0, b0 = cands[0]
            e1, e2 = models[(s, b0)]["cvned"], models[(b0, t)]["cvned"]
            comp[(s, t)] = ({x: dict(d) for x, d in mix.items()}, dict(wsum), 1 - (1 - e1) * (1 - e2))
    # ---- target bigram LM
    lm = {}
    for t in langs:
        bg = defaultdict(Counter)
        for w in words[t]:
            seq = (BOS,) + w + (EOS,)
            for i in range(1, len(seq)):
                bg[seq[i - 1]][seq[i]] += 1
        lm[t] = ({h: (dict(c), sum(c.values())) for h, c in bg.items()}, len(inv[t]) + 1)
    M = {"langs": langs, "inv": inv, "models": models, "pool": poolp, "comp": comp, "lm": lm,
         "cfg": dict(CFG)}
    if final and CFG["ctxcv"] > 0:
        # edge reliability from the full contextual transducer: 2-fold cross-fitted NED of its 1-best
        keys = sorted(data)
        errs = defaultdict(list)
        for fold in (0, 1):
            part = {k: data[k] for i, k in enumerate(keys) if i % 2 != fold}
            held = [k for i, k in enumerate(keys) if i % 2 == fold]
            Mf = train_family(langs, part, final=False)
            pf = {l: Prior(Mf["inv"][l]) for l in langs}
            for (s, t) in pairs:
                hs = [k for k in held if data[k][s] and data[k][t]]
                if not hs:
                    continue
                scr = PairScorer(Mf, s, t, pf)
                for k in hs:
                    kb = scr.kbest(data[k][s])
                    pred = kb[0][1] if kb else tuple(data[k][s])
                    errs[(s, t)].append(ned(pred, data[k][t]))
        for (s, t), m in models.items():
            e = errs.get((s, t))
            if e:
                n = len(e)
                ec = (n * (sum(e) / n) + 2 * 0.6) / (n + 2)
                m["cvned_cf"] = m["cvned"]
                m["cvned"] = (1 - CFG["ctxcv"]) * m["cvned"] + CFG["ctxcv"] * ec
    return M


SELF_OPTIONS = [{}, {"r_comp": 3.0}, {"alpha": 3.0}, {"alpha": 10.0}]


def self_select(langs, data):
    """Per-family choice among SELF_OPTIONS by 2-fold cross-fitting on this family's training-P sets
    (held-out sets simulated as rows: each attested language masked in turn, the others visible)."""
    keys = sorted(data, key=lambda k: (-sum(1 for l in langs if data[k][l]), k))
    base = dict(CFG)
    loss = [defaultdict(list) for _ in SELF_OPTIONS]
    for fold in (0, 1):
        part = {k: data[k] for i, k in enumerate(keys) if i % 2 != fold}
        held = [k for i, k in enumerate(keys) if i % 2 == fold]
        Mf = train_family(langs, part, final=False)
        pf = {l: Prior(Mf["inv"][l]) for l in langs}
        rows = []
        for k in held:
            att = [l for l in langs if data[k][l]]
            if len(att) >= 2:
                rows.extend((k, t) for t in att)
        rows = rows[:CFG["selcap"]]
        for oi, opt in enumerate(SELF_OPTIONS):
            CFG.clear()
            CFG.update(base)
            CFG.update(opt)
            for k, t in rows:
                row = {l: (["?"] if l == t else list(data[k][l])) for l in langs}
                pred = predict_row(Mf, pf, {}, row, langs)
                loss[oi][t].append(ned(data[k][t], pred))
    CFG.clear()
    CFG.update(base)
    vals = []
    for oi in range(len(SELF_OPTIONS)):
        d = loss[oi]
        vals.append(sum(sum(v) / len(v) for v in d.values()) / max(1, len(d)) if d else 9.0)
    best = min(range(len(vals)), key=lambda i: (vals[i] - (CFG["selmargin"] if i == 0 else 0.0), i))
    return SELF_OPTIONS[best], vals


def train(manifest, model_dir):
    man = json.load(open(manifest))
    models, allex = {}, {}
    for fam in man["families"]:
        langs, data = load(man["surprise_train"][fam])
        models[fam] = train_family(langs, data)
        if CFG["wrev"] > 0:
            rdata = {k: {l: list(reversed(v)) for l, v in r.items()} for k, r in data.items()}
            models[fam]["rev"] = train_family(langs, rdata)
        if CFG["selfsel"]:
            opt, vals = self_select(langs, data)
            models[fam]["cfg"].update(opt)
            print("selfsel", fam, opt, " ".join("%.4f" % v for v in vals), flush=True)
        if CFG["rerank"]:
            allex[fam] = crossfit_examples(langs, data, CFG["cvk"], CFG["cvcap"], fam)
        print("trained", fam, len(allex.get(fam, [])), flush=True)
    theta = None
    if CFG["rerank"]:
        theta, L0, L1 = fit_theta(allex)
        print("theta", " ".join("%.4f" % x for x in theta), "loss %.5f -> %.5f" % (L0, L1), flush=True)
    for fam, m in models.items():
        m["theta"] = theta
        with open(os.path.join(model_dir, fam + ".pkl"), "wb") as f:
            pickle.dump(m, f, protocol=4)


# ------------------------------------------------------------------ prediction
class PairScorer:
    def __init__(self, M, s, t, priors):
        self.s, self.t = s, t
        self.pm = M["models"].get((s, t))
        self.n = self.pm["n"] if self.pm else 0
        self.pool = M["pool"].get(t, {})
        self.comp = M["comp"].get((s, t))
        self.prior = priors[t]
        if self.pm is not None:
            self.cvned = self.pm["cvned"] if CFG["ctxcv"] > 0 else self.pm.get("cvned_cf", self.pm["cvned"])
            if self.comp is not None and self.n < 5:
                self.cvned = min(self.cvned, self.comp[2] + 0.05)
        else:
            self.cvned = self.comp[2] + 0.05 if self.comp is not None else 0.9
        self.cache = {}
        self.basecache = {}

    def base(self, x, o):
        key = (x, o)
        v = self.basecache.get(key)
        if v is not None:
            return v
        num = CFG["r_prior"] * self.prior.p(x, o)
        den = CFG["r_prior"]
        if x in self.pool:
            num += CFG["r_pool"] * self.pool[x].get(o, 0.0)
            den += CFG["r_pool"]
        if self.comp is not None:
            mix, wsum = self.comp[0], self.comp[1]
            if x in mix:
                w = wsum[x]
                rc = CFG["r_comp"] * w / (w + 5.0) * 3.0
                if CFG["cgate"] > 0:
                    rc *= CFG["cgate"] / (CFG["cgate"] + self.n)
                num += rc * mix[x].get(o, 0.0) / w
                den += rc
        v = num / den
        self.basecache[key] = v
        return v

    def prob(self, l, x, r, o, l2=BOS, r2=EOS):
        p = self.base(x, o)
        pm = self.pm
        if pm is None:
            return p
        beta = CFG["beta"]
        hs = (("uni", x), ("cls", (cls(l), x, cls(r))), ("tri", (l, x, r)), ("c5", (l2, l, x, r, r2))) \
            if CFG["usectx"] else (("uni", x),)
        for lev, h in hs:
            e = pm[lev].get(h) if lev in pm else None
            if e is None:
                continue
            cnt, tot, typ = e
            lam = tot / (tot + beta * typ + (CFG["kuni"] if lev == "uni" else CFG["kctx"]))
            p = lam * cnt.get(o, 0.0) / tot + (1 - lam) * p
        return p

    def options(self, l, x, r, l2=BOS, r2=EOS):
        opts = set(self.prior.top(x))
        if x in self.pool:
            opts.update(self.pool[x])
        if self.comp is not None and x in self.comp[0]:
            opts.update(self.comp[0][x])
        pm = self.pm
        if pm is not None:
            for lev, h in (("uni", x), ("cls", (cls(l), x, cls(r))), ("tri", (l, x, r)), ("c5", (l2, l, x, r, r2))):
                e = pm[lev].get(h) if lev in pm else None
                if e is not None:
                    opts.update(e[0])
        sc = [(self.prob(l, x, r, o, l2, r2), o) for o in opts]
        sc.sort(key=lambda z: (-z[0], z[1]))
        return sc[:CFG["topp"]]

    def kbest(self, src):
        a = (BOS,) + tuple(src)
        ext = a + (EOS, EOS)
        beam = {(): 0.0}
        for j in range(len(a)):
            l = a[j - 1] if j > 0 else BOS
            l2 = a[j - 2] if j > 1 else BOS
            opts = self.options(l, a[j], ext[j + 1], l2, ext[j + 2])
            nb = {}
            for out, lp in beam.items():
                for p, o in opts:
                    q = out + o
                    v = lp + math.log(p)
                    if v > nb.get(q, -1e300):
                        nb[q] = v
            beam = dict(sorted(nb.items(), key=lambda z: (-z[1], z[0]))[:CFG["beam"]])
        res = [(v, q) for q, v in beam.items() if q]
        res.sort(key=lambda z: (-z[0], z[1]))
        return res[:CFG["kbest"]]

    def forced(self, src, cand):
        a = (BOS,) + tuple(src)
        ext = a + (EOS, EOS)
        ctx = [(a[j - 1] if j > 0 else BOS, a[j], ext[j + 1], a[j - 2] if j > 1 else BOS, ext[j + 2])
               for j in range(len(a))]

        def cost(j, o):
            key = (ctx[j], o)
            v = self.cache.get(key)
            if v is None:
                c = ctx[j]
                v = -math.log(max(self.prob(c[0], c[1], c[2], o, c[3], c[4]), 1e-12))
                self.cache[key] = v
            return v
        c, _ = viterbi(a, tuple(cand), cost)
        return -c


def lm_logp(lm, cand):
    bg, V = lm
    seq = (BOS,) + tuple(cand) + (EOS,)
    lp = 0.0
    for i in range(1, len(seq)):
        e = bg.get(seq[i - 1])
        if e is None:
            lp += math.log(1.0 / V)
        else:
            cnt, tot = e
            lp += math.log((cnt.get(seq[i], 0) + 0.5) / (tot + 0.5 * V))
    return lp


def ned(a, b):
    n, m = len(a), len(b)
    if not n or not m:
        return 1.0
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[m] / max(n, m)


def src_weight(n):
    return max(CFG["wfloor"], n / (n + CFG["wkappa"]))


def lev_align(a, b):
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    i, j, out = n, m, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            out.append((i - 1, b[j - 1])); i -= 1; j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            out.append((i - 1, None)); i -= 1
        else:
            out.append((-(i) - 1, b[j - 1])); j -= 1   # insertion before top position i (encoded negative)
    return out[::-1]


def edit_set(top, q):
    ed = set()
    for pos, y in lev_align(top, q):
        if pos >= 0:
            if y is None:
                ed.add(("d", pos, ""))
            elif y != top[pos]:
                ed.add(("s", pos, y))
        else:
            ed.add(("i", -pos - 1, y))
    return ed


def apply_edit(top, e):
    kind, pos, y = e
    t = list(top)
    if kind == "s":
        t[pos] = y
    elif kind == "d":
        del t[pos]
    else:
        t.insert(pos, y)
    return tuple(t)


def get_scorer(M, priors, scorers, s, t, tag=""):
    key = (tag, s, t)
    if key not in scorers:
        scorers[key] = PairScorer(M, s, t, priors)
    return scorers[key]


NFEAT = 9


def row_pool(M, priors, scorers, row, langs, depth=0):
    """Candidate pool of one row: returns (candidates sorted by PoE score, PoE scores, feature rows) or None."""
    tgt = [l for l in langs if row[l] == ["?"]][0]
    srcs = [l for l in langs if l != tgt and row[l] and row[l] != ["?"]]
    strs = [tuple(row[s]) for s in srcs]
    sc = [get_scorer(M, priors, scorers, s, tgt) for s in srcs]
    disc = [1.0] * len(srcs)
    cvs = [x.cvned for x in sc]
    # friends of friends: impute reflexes of broker languages absent from the row, use them as discounted sources
    if depth == 0 and CFG["npseudo"] > 0 and srcs:
        brok = []
        for b in langs:
            if b == tgt or b in srcs:
                continue
            bt = get_scorer(M, priors, scorers, b, tgt)
            if bt.pm is None:
                continue
            e_sb = min(get_scorer(M, priors, scorers, s, b).cvned for s in srcs)
            e = 1 - (1 - e_sb) * (1 - bt.cvned)
            brok.append((e, langs.index(b), b))
        brok.sort()
        npse = CFG["npseudo"] + (CFG["pfew"] if len(srcs) <= 2 else 0)
        for e, _, b in brok[:npse]:
            if e >= min(cvs) + CFG["pmargin"]:
                continue
            row2 = {l: (row[l] if l in srcs else []) for l in langs}
            row2[b] = ["?"]
            imp = predict_row(M, priors, scorers, row2, langs, depth=1)
            srcs.append(b)
            strs.append(tuple(imp))
            sc.append(get_scorer(M, priors, scorers, b, tgt))
            disc.append(CFG["pgamma"])
            cvs.append(e)
    if not srcs:
        return None
    order = sorted(range(len(srcs)), key=lambda i: (cvs[i], -sc[i].n, langs.index(srcs[i])))[:CFG["maxsrc"]]
    bestc = cvs[order[0]]
    wts = {i: disc[i] * src_weight(sc[i].n) * math.exp(-CFG["alpha"] * (cvs[i] - bestc)) for i in order}
    cands = {}
    top1 = {}
    MR = M.get("rev") if CFG["wrev"] > 0 else None
    if MR is not None:
        scr = [get_scorer(MR, priors, scorers, srcs[i], tgt, "R") for i in range(len(srcs))]
    for i in order:
        kb = sc[i].kbest(strs[i])
        if kb:
            top1[i] = kb[0][1]
        for v, q in kb:
            cands.setdefault(q, 0)
        if MR is not None:
            for v, q in scr[i].kbest(strs[i][::-1]):
                cands.setdefault(q[::-1], 0)
    if not cands:
        return [strs[order[0]]], [0.0], [[0.0] * NFEAT]
    cl = sorted(cands)
    per = {q: [sc[i].forced(strs[i], q) for i in order] for q in cl}
    if CFG["wch"] > 0:
        ch = [get_scorer(M, priors, scorers, tgt, srcs[i]) for i in order]
        for q in cl:
            per[q] = [lp + CFG["wch"] * c.forced(q, strs[i]) for lp, c, i in zip(per[q], ch, order)]
    if MR is not None:
        wr = CFG["wrev"]
        chr_ = [get_scorer(MR, priors, scorers, tgt, srcs[i], "R") for i in order] if CFG["wch"] > 0 else None
        for q in cl:
            qr = q[::-1]
            vals = []
            for k, (lp, i) in enumerate(zip(per[q], order)):
                v = scr[i].forced(strs[i][::-1], qr)
                if chr_ is not None:
                    v += CFG["wch"] * chr_[k].forced(qr, strs[i][::-1])
                vals.append((1 - wr) * lp + wr * v)
            per[q] = vals
    poe = {q: sum(wts[i] * lp for i, lp in zip(order, per[q])) for q in cl}
    if CFG["wlm"]:
        for q in cl:
            poe[q] += CFG["wlm"] * lm_logp(M["lm"][tgt], q)
    ranked = sorted(cl, key=lambda q: (-poe[q], q))
    if depth > 0:
        return ranked, [poe[q] for q in ranked], None
    # features (row-local only)
    mx = poe[ranked[0]]
    nsrc = len(order)
    uni = {q: sum(per[q]) / nsrc for q in cl}
    mu = max(uni.values())
    b0 = {q: per[q][0] for q in cl}
    mb0 = max(b0.values())
    b1 = {q: (per[q][1] if nsrc > 1 else per[q][0]) for q in cl}
    mb1 = max(b1.values())
    wsum = sum(wts.values())
    vote = {q: sum(wts[i] for i in order if top1.get(i) == q) / wsum for q in cl}
    top = ranked[:10]
    ws = [math.exp(poe[q] - mx) for q in top]
    z = sum(ws)
    risk = {q: sum(w * ned(q, q2) for w, q2 in zip(ws, top)) / z for q in cl}
    lmv = {q: lm_logp(M["lm"][tgt], q) / (len(q) + 1) for q in cl}
    mlm = max(lmv.values())
    lens = sorted((len(strs[i]), wts[i]) for i in order)
    half, acc, medlen = wsum / 2, 0.0, lens[-1][0]
    for ln_, w in lens:
        acc += w
        if acc >= half:
            medlen = ln_
            break
    feats = []
    for q in ranked:
        feats.append([poe[q] - mx, uni[q] - mu, b0[q] - mb0, b1[q] - mb1, vote[q], -risk[q], lmv[q] - mlm,
                      -abs(len(q) - medlen), 1.0 if q in top1.values() else 0.0])
    return ranked, [poe[q] for q in ranked], feats


ENS_VARIANTS = [{}, {"r_comp": 3.0}, {"ctxcv": 0.0}]


def predict_row_ens(M, priors, row, langs):
    """Mixture of the PoE posteriors of several predict-time configurations, then MBR under NED."""
    base = dict(CFG)
    mix = defaultdict(float)
    for var in ENS_VARIANTS:
        CFG.clear()
        CFG.update(base)
        CFG.update(var)
        CFG["ens"] = 0
        res = row_pool(M, priors, {}, row, langs, 0)
        if res is None:
            continue
        ranked, poe, _ = res
        mx = poe[0]
        ws = [math.exp((v - mx) / CFG["enst"]) for v in poe]
        z = sum(ws)
        for q, w in zip(ranked, ws):
            mix[q] += w / z / len(ENS_VARIANTS)
    CFG.clear()
    CFG.update(base)
    if not mix:
        return ["a"]
    top = sorted(mix.items(), key=lambda z: (-z[1], z[0]))[:CFG["mbrn"]]
    if not CFG["ensmbr"]:
        return list(top[0][0])
    best, bq = 1e9, None
    zt = sum(w for _, w in top)
    for q, _ in top:
        r = sum(w * ned(q, q2) for q2, w in top) / zt
        if r < best - 1e-12:
            best, bq = r, q
    return list(bq)


def predict_row(M, priors, scorers, row, langs, depth=0):
    if depth == 0 and CFG["ens"]:
        return predict_row_ens(M, priors, row, langs)
    res = row_pool(M, priors, scorers, row, langs, depth)
    if res is None:
        return ["a"]
    ranked, poe, feats = res
    if POOL_HOOK is not None and depth == 0:
        POOL_HOOK.append(list(zip(poe, ranked)))
    theta = M.get("theta") if CFG["rerank"] else None
    if depth == 0 and theta is not None and feats is not None:
        sc = [sum(t * f for t, f in zip(theta, fv)) for fv in feats]
        bi = max(range(len(ranked)), key=lambda i: (sc[i], -i))
        return list(ranked[bi])
    if depth == 0 and CFG["mbr"] > 0 and len(ranked) > 1:
        top = ranked[:CFG["mbrn"]]
        mx = poe[0]
        ws = [math.exp((v - mx) / CFG["mbr"]) for v in poe[:CFG["mbrn"]]]
        z = sum(ws)
        best, bq = 1e9, None
        for q in top:
            r = sum(w * ned(q, q2) for w, q2 in zip(ws, top)) / z
            if r < best - 1e-12:
                best, bq = r, q
        return list(bq)
    return list(ranked[0])


# ------------------------------------------------------------------ reranker (trained on cross-fitted training rows)
def crossfit_examples(langs, data, K, cap, seed_name):
    """K-fold over training cognate sets: pair models on K-1 folds, candidate pools + features for held-out rows."""
    keys = sorted(data, key=lambda k: (-sum(1 for l in langs if data[k][l]), k))
    exs = []
    for f in range(K):
        part = {k: data[k] for i, k in enumerate(keys) if i % K != f}
        held = [k for i, k in enumerate(keys) if i % K == f]
        Mf = train_family(langs, part, final=False)
        priors = {l: Prior(Mf["inv"][l]) for l in langs}
        rows = []
        for k in held:
            att = [l for l in langs if data[k][l]]
            if len(att) < 2:
                continue
            for t in att:
                rows.append((k, t))
        rows = rows[:cap]
        for k, t in rows:
            row = {l: (["?"] if l == t else list(data[k][l])) for l in langs}
            res = row_pool(Mf, priors, {}, row, langs)
            if res is None or res[2] is None:
                continue
            ranked, _, feats = res
            gold = tuple(data[k][t])
            exs.append((t, feats, [ned(gold, q) for q in ranked]))
    return exs


def fit_theta(allex, iters=300, l2=0.01):
    import numpy as np
    exs, W = [], []
    for fam, ex in sorted(allex.items()):
        bylang = Counter(t for t, _, _ in ex)
        nl = len(bylang)
        for t, feats, neds in ex:
            exs.append((feats, neds))
            W.append(1.0 / (nl * bylang[t] * len(allex)))
    N = len(exs)
    C = max(len(n) for _, n in exs)
    X = np.zeros((N, C, NFEAT))
    Y = np.zeros((N, C))
    mask = np.zeros((N, C), dtype=bool)
    for i, (f, n) in enumerate(exs):
        X[i, :len(n)] = np.array(f)
        Y[i, :len(n)] = n
        mask[i, :len(n)] = True
    W = np.array(W)
    th0 = np.zeros(NFEAT)
    th0[0] = 1.0

    def loss_grad(th):
        sc = X @ th
        sc = np.where(mask, sc, -1e30)
        sc = sc - sc.max(axis=1, keepdims=True)
        p = np.exp(sc) * mask
        p /= p.sum(axis=1, keepdims=True)
        el = (p * Y).sum(axis=1)
        L = float(W @ el) + l2 * float(np.sum((th - th0) ** 2))
        g = np.einsum("n,nc,ncf->f", W, p * (Y - el[:, None]), X) + 2 * l2 * (th - th0)
        return L, g
    theta = th0.copy()
    m = np.zeros(NFEAT)
    v = np.zeros(NFEAT)
    lr = 0.05
    L0, _ = loss_grad(theta)
    for it in range(1, iters + 1):
        L, g = loss_grad(theta)
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        theta = theta - lr * (m / (1 - 0.9 ** it)) / (np.sqrt(v / (1 - 0.999 ** it)) + 1e-8)
    L1, _ = loss_grad(theta)
    return [float(x) for x in theta], L0, L1


def predict(model_dir, fam, jobs):
    with open(os.path.join(model_dir, fam + ".pkl"), "rb") as f:
        M = pickle.load(f)
    CFG.update(M["cfg"])
    env_overrides()
    if CFG["r_comp_pred"] >= 0:
        CFG["r_comp"] = CFG["r_comp_pred"]
    priors = {l: Prior(M["inv"][l]) for l in M["langs"]}
    for ln in open(jobs):
        inp, outp = ln.rstrip("\n").split("\t")
        langs, data = load(inp)
        with open(outp, "w", encoding="utf-8") as f:
            f.write("COGID\t" + "\t".join(langs) + "\n")
            for key, row in data.items():
                scorers = {}  # fresh per row: nothing carried between rows
                tgt = [l for l in langs if row[l] == ["?"]][0]
                pred = predict_row(M, priors, scorers, row, langs)
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
