"""Broker lens system, run 2026-10-18-0839 SECONDARY (from run 2026-10-18-0202's broker code): forced broker-path
composition mixture (lam in 0.5..1) with the per-family combination chosen on nested band-validation folds (see
"band-fold learning" below), on top of pairwise correspondence transducers on a language graph, with
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
UNIV = {}  # universal segment substitution table learned from the development families (set in train / predict)
MAXP = 3

# ------------------------------------------------------------------ configuration (overridable by env for dev runs)
CFG = {
    "iters": 2,          # hard-EM realignment iterations
    "beta": 1.0,         # Witten-Bell type multiplier
    "r_prior": 1.0,      # base mixture weight of the sound-class prior
    "r_pool": 0.0,       # base mixture weight of the target-pooled map
    "r_comp": 0.0,       # base mixture weight scale of broker compositions
    "r_comp_pred": -1.0, # if >= 0: composition weight used at prediction only (training keeps r_comp)
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
    "umu": 0.0,          # weight of the universal (development-family) substitution table in the prior
    "upairs": 40,
    "usets": 60,
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
    # ---- band-fold learning (run 2026-10-18-0839): inner band = most complete 15% of the training sets
    "band": 1,           # 1: learn the combination on the inner band inside train() and use it at prediction
    "bratio": 0.15,      # band share (organisers' split rule)
    "brc": 3.0,          # composition weight of the composed experts
    "bsel": 3,           # 1 pooled params for all families; 2 per family if better by bmargin; 3 per family always
    "bmargin": 0.005,    # band-loss margin a family's own params must beat the pooled params by
    "bgrid": 4,          # grid id (see BAND_GRIDS)
    "bcomp": 1,          # include composed experts / candidates in the cache (needed if the grid has lam > 0)
    "bfloor": -60.0,     # floor of a forced log-probability (no segmentation)
    "bdef": 0,           # 1: the default combination is always a candidate (index 0, wins ties)
    "bnb": 4,            # number of nested inner bands (band b = most complete share of what is left below band b-1)
    "abp": 0,            # row-local aberrance: partners per source (0 = off)
    "abeta": 0.0,        # source weight * exp(-abeta * aberrance) (aberrance = mean excess NED toward partners)
    "abpos": 1,          # 1: use max(0, aberrance)
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

    def __init__(self, inv, use_univ=True):
        self.use_univ = use_univ
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
            ux = UNIV.get(x) if (self.use_univ and UNIV and CFG["umu"] > 0) else None
            if ux is not None:
                ud = {y: ux.get(y, 0.0) for y in sorted(cand)}
                zu = sum(ud.values())
                if zu > 0:
                    mu = CFG["umu"]
                    d = {y: (1 - mu) * d[y] + mu * ud[y] / zu for y in d}
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


def learn_univ(dev_dir, dev_fams):
    """Universal x -> y substitution probabilities from prior-cost alignments of development-family pairs
    (single-segment pieces only; at most 60 sets per ordered pair, 40 pairs per family; deterministic)."""
    cnt = defaultdict(Counter)
    for fam in dev_fams:
        path = os.path.join(dev_dir, fam, "training-0.10.tsv")
        if not os.path.isfile(path):
            continue
        langs, data = load(path)
        inv = {l: sorted({x for r in data.values() for x in r[l]}) for l in langs}
        keys = sorted(data)
        prs = [(s, t) for s in langs for t in langs if s != t][:CFG["upairs"]]
        for s, t in prs:
            pr = Prior(inv[t], use_univ=False)
            k = 0
            for key in keys:
                r = data[key]
                if not (r[s] and r[t]) or len(r[t]) > MAXP * (len(r[s]) + 1):
                    continue
                a = (BOS,) + tuple(r[s])
                _, pcs = viterbi(a, tuple(r[t]), prior_cost_fn(a, pr))
                for x, o in zip(a[1:], pcs[1:]):
                    if len(o) == 1:
                        cnt[x][o[0]] += 1
                k += 1
                if k >= CFG["usets"]:
                    break
    return {x: {y: v / sum(c.values()) for y, v in c.items()} for x, c in cnt.items() if sum(c.values()) >= 5}


def train(manifest, model_dir):
    global UNIV
    man = json.load(open(manifest))
    models, allex = {}, {}
    if CFG["umu"] > 0:
        UNIV = learn_univ(man["dev_dir"], man["dev_families"])
        print("univ", len(UNIV), flush=True)
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
    if CFG["band"]:
        per_fam, nlangs = {}, {}
        for fam in man["families"]:
            langs, data = load(man["surprise_train"][fam])
            per_fam[fam] = band_learn_family(langs, data)
            nlangs[fam] = len(langs)
            print("band rows", fam, [len(b) for b in per_fam[fam]], flush=True)
        choice, pooled = band_select(per_fam, nlangs)
        for fam, m in models.items():
            m["bparams"] = choice.get(fam, pooled)
    for fam, m in models.items():
        m["theta"] = theta
        m["univ"] = UNIV
        with open(os.path.join(model_dir, fam + ".pkl"), "wb") as f:
            pickle.dump(m, f, protocol=4)


# ------------------------------------------------------------------ prediction
class PairScorer:
    def __init__(self, M, s, t, priors, rcomp=None):
        self.s, self.t = s, t
        self.rcomp = CFG["r_comp"] if rcomp is None else rcomp
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
                rc = self.rcomp * w / (w + 5.0) * 3.0
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


def oned(gold, pred):
    """Item NED exactly as the official compare_words computes it: lingpy nw_align (match 1, mismatch -1, gap -1,
    the same tie order), mismatched alignment positions / alignment length; gold is the first sequence."""
    A, Bq = list(gold), list(pred)
    if not Bq:
        Bq = (2 * len(A)) * ["Ø"]
    M, N = len(A), len(Bq)
    mat = [[0] * (M + 1) for _ in range(N + 1)]
    tb = [[0] * (M + 1) for _ in range(N + 1)]
    for i in range(1, M + 1):
        mat[0][i] = mat[0][i - 1] - 1
        tb[0][i] = 2
    for i in range(1, N + 1):
        mat[i][0] = mat[i - 1][0] - 1
        tb[i][0] = 3
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            gA = mat[i - 1][j] - 1
            gB = mat[i][j - 1] - 1
            mt = mat[i - 1][j - 1] + (1 if A[j - 1] == Bq[i - 1] else -1)
            if gA >= mt and gA >= gB:
                mat[i][j], tb[i][j] = gA, 3
            elif mt >= gB:
                mat[i][j], tb[i][j] = mt, 1
            else:
                mat[i][j], tb[i][j] = gB, 2
    i, j, L, bad = N, M, 0, 0
    while i > 0 or j > 0:
        L += 1
        if tb[i][j] == 3:
            bad += 1
            i -= 1
        elif tb[i][j] == 1:
            bad += A[j - 1] != Bq[i - 1]
            i -= 1
            j -= 1
        else:
            bad += 1
            j -= 1
    return bad / L if L else 0.0


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


def get_scorer(M, priors, scorers, s, t, tag="", rcomp=None):
    key = (tag, s, t)
    if key not in scorers:
        scorers[key] = PairScorer(M, s, t, priors, rcomp)
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
    if depth == 0 and M.get("bparams") is not None and CFG["band"]:
        c = row_cache(M, priors, scorers, row, langs)
        if c is None:
            return ["a"]
        return combine(c, M["bparams"])
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


# ------------------------------------------------------------------ band-fold learning (run 2026-10-18-0839)
BAND_GRIDS = {
    0: {"alpha": [2.0, 3.0, 4.5, 6.0, 8.0, 11.0], "wch": [0.0, 0.2, 0.4, 0.7], "lam": [0.0, 0.15, 0.3, 0.5, 0.75, 1.0],
        "pg": [0.25, 0.5, 1.0]},
    1: {"alpha": [6.0], "wch": [0.4], "lam": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 1.0], "pg": [0.5]},
    2: {"alpha": [2.0, 3.0, 4.5, 6.0, 8.0], "wch": [0.2, 0.4, 0.7, 1.0], "lam": [0.0], "pg": [0.25, 0.5, 1.0]},
    3: {"alpha": [2.0, 3.0, 4.5, 6.0, 8.0], "wch": [0.2, 0.4, 0.7, 1.0], "lam": [0.0, 0.15, 0.3, 0.5, 0.75, 1.0],
        "pg": [0.25, 0.5, 1.0]},
    4: {"alpha": [2.0, 3.0, 4.5, 6.0, 8.0], "wch": [0.2, 0.4, 0.7, 1.0], "lam": [0.5, 0.75, 1.0],
        "pg": [0.25, 0.5, 1.0]},
}
DEFAULT_BP = {"alpha": 6.0, "lam": 0.0, "pg": 0.5, "wch": 0.4}


def band_split(data, langs, ratio):
    """The organisers' split rule (split_training_test_data): the most complete share of sets is the band."""
    split_off = int(len(data) * ratio + 0.5)
    keys = [k for k, v in sorted(data.items(), key=lambda x: sum(1 if " ".join(b) not in ("", "?") else 0
                                                                    for a, b in x[1].items()), reverse=True)]
    band = keys[:split_off]
    rest = {k: data[k] for k in keys[split_off:]}
    return rest, band


def row_cache(M, priors, scorers, row, langs):
    """Per-row score cache: candidate pool (union of the k-best of the direct and the composed experts) and, per
    candidate and source, forward and channel log-probabilities under the direct and the composed pair models."""
    tgt = [l for l in langs if row[l] == ["?"]][0]
    srcs = [l for l in langs if l != tgt and row[l] and row[l] != ["?"]]
    strs = [tuple(row[s]) for s in srcs]
    sc = [get_scorer(M, priors, scorers, s, tgt) for s in srcs]
    pse = [0] * len(srcs)
    cvs = [x.cvned for x in sc]
    if CFG["npseudo"] > 0 and srcs:
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
            pse.append(1)
            cvs.append(e)
    if not srcs:
        return None
    order = sorted(range(len(srcs)), key=lambda i: (cvs[i], -sc[i].n, langs.index(srcs[i])))[:CFG["maxsrc"]]
    usec = CFG["bcomp"] > 0
    scd = [sc[i] for i in order]
    hd = [get_scorer(M, priors, scorers, tgt, srcs[i]) for i in order]
    if usec:
        scc = [get_scorer(M, priors, scorers, srcs[i], tgt, "C", CFG["brc"]) for i in order]
        hc = [get_scorer(M, priors, scorers, tgt, srcs[i], "C", CFG["brc"]) for i in order]
    cands = set()
    dset = set()
    top1d, top1c = [], []
    for k, i in enumerate(order):
        kb = scd[k].kbest(strs[i])
        top1d.append(kb[0][1] if kb else None)
        cands.update(q for _, q in kb)
        dset.update(q for _, q in kb)
        if usec:
            kb = scc[k].kbest(strs[i])
            top1c.append(kb[0][1] if kb else None)
            cands.update(q for _, q in kb)
    cl = sorted(cands)
    if not cl:
        return {"fallback": strs[order[0]]}
    fl = CFG["bfloor"]
    # row-local aberrance (truth discovery): how badly each visible source predicts the other visible sources of
    # this row, in excess of the edge's expected (cross-fitted) error; computed from this row only
    ab = [0.0] * len(order)
    if CFG["abp"] > 0:
        real = [k for k in range(len(order)) if not pse[order[k]]]
        if len(real) >= 3:
            exc = {}
            for k in real:
                i = order[k]
                for k2 in real[:CFG["abp"] + 1]:
                    if k2 == k:
                        continue
                    j = order[k2]
                    e = get_scorer(M, priors, scorers, srcs[i], srcs[j])
                    kb = e.kbest(strs[i])
                    pred = kb[0][1] if kb else strs[i]
                    exc[(k, k2)] = ned(pred, strs[j]) - e.cvned
            for k in real:
                v = [x for (a, b), x in exc.items() if a == k]
                ab[k] = sum(v) / len(v) if v else 0.0

    def fs(scr, a, b):
        return max(fl, scr.forced(a, b))
    S = len(order)
    FD = [[fs(scd[k], strs[order[k]], q) for k in range(S)] for q in cl]
    HD = [[fs(hd[k], q, strs[order[k]]) for k in range(S)] for q in cl]
    if usec:
        FC = [[fs(scc[k], strs[order[k]], q) for k in range(S)] for q in cl]
        HC = [[fs(hc[k], q, strs[order[k]]) for k in range(S)] for q in cl]
    else:
        FC, HC = FD, HD
    return {"cl": cl, "FD": FD, "HD": HD, "FC": FC, "HC": HC, "n": [sc[i].n for i in order],
            "cv": [cvs[i] for i in order], "pse": [pse[i] for i in order], "top1d": top1d, "top1c": top1c,
            "lens": [len(strs[i]) for i in order], "ab": ab, "ind": [1 if q in dset else 0 for q in cl]}


def src_weights(c, p):
    bestc = c["cv"][0]
    ab = c.get("ab") or [0.0] * len(c["n"])
    be = p.get("abeta", CFG["abeta"])
    return [(p["pg"] if ps else 1.0) * src_weight(n) * math.exp(-p["alpha"] * (cv - bestc))
            * math.exp(-be * (max(0.0, a) if CFG["abpos"] else a))
            for n, cv, ps, a in zip(c["n"], c["cv"], c["pse"], ab)]


def combine(c, p):
    """Best candidate of a row cache under combination parameters p (pure Python, deterministic)."""
    if "fallback" in c:
        return list(c["fallback"])
    w = src_weights(c, p)
    lam, wch = p["lam"], p["wch"]
    best, bq = None, None
    ind = c.get("ind")
    for qi, q in enumerate(c["cl"]):
        if lam == 0 and ind is not None and not ind[qi]:
            continue
        fd, hd, fc, hc = c["FD"][qi], c["HD"][qi], c["FC"][qi], c["HC"][qi]
        v = 0.0
        for k in range(len(w)):
            v += w[k] * ((1 - lam) * (fd[k] + wch * hd[k]) + lam * (fc[k] + wch * hc[k]))
        if best is None or v > best:
            best, bq = v, q
    return list(bq)


def param_list(grid):
    keys = sorted(grid)
    out = [{}]
    for k in keys:
        out = [dict(d, **{k: v}) for d in out for v in grid[k]]
    return out


def band_rows(langs, data, band):
    rows = []
    for k in band:
        att = [l for l in langs if data[k][l]]
        if len(att) < 2:
            continue
        for t in att:
            rows.append((k, t, {l: (["?"] if l == t else list(data[k][l])) for l in langs}, tuple(data[k][t])))
    return rows


def band_learn_family(langs, data):
    """Nested inner bands of this family's training sets (like val is cut from training-P): band 1 = the most
    complete share of the sets, band 2 = the most complete share of the rest, ...; for each band, pair models trained
    on what lies below it, and a row cache + official-style NED per candidate for every band row."""
    bands = []
    cur = data
    for b in range(CFG["bnb"]):
        rest, band = band_split(cur, langs, CFG["bratio"])
        if not band or len(rest) < 10:
            break
        Mf = train_family(langs, rest, final=True)
        pf = {l: Prior(Mf["inv"][l]) for l in langs}
        out = []
        for k, t, row, gold in band_rows(langs, cur, band):
            c = row_cache(Mf, pf, {}, row, langs)
            if c is None:
                continue
            if "fallback" in c:
                c["g"] = None
                c["gf"] = oned(gold, c["fallback"])
            else:
                c["g"] = [oned(gold, q) for q in c["cl"]]
            c["t"] = t
            out.append(c)
        bands.append(out)
        cur = rest
    return bands


def band_eval(caches, plist, nlangs):
    """Family score per parameter setting on one band (numpy, used only for the choice): official weighting (sum over
    target languages of the language-mean item NED of the argmax, divided by the number of languages)."""
    import numpy as np
    sums, cnt = {}, {}
    P = len(plist)
    lam = np.array([p["lam"] for p in plist])
    wch = np.array([p["wch"] for p in plist])
    for c in caches:
        t = c["t"]
        cnt[t] = cnt.get(t, 0) + 1
        if c["g"] is None:
            sums[t] = sums.get(t, 0) + c["gf"]
            continue
        Wm = np.array([src_weights(c, p) for p in plist])
        FD, HD, FC, HC = (np.array(c[k]) for k in ("FD", "HD", "FC", "HC"))
        es = lambda A: np.einsum("ps,cs->pc", Wm, A)  # no BLAS: bit-reproducible
        v = (1 - lam)[:, None] * (es(FD) + wch[:, None] * es(HD)) + lam[:, None] * (es(FC) + wch[:, None] * es(HC))
        outside = np.array(c["ind"]) == 0
        if outside.any():
            v[np.ix_(lam == 0, outside)] = -np.inf
        g = np.array(c["g"])
        sums[t] = sums.get(t, 0) + g[np.argmax(v, axis=1)]
    tot = np.zeros(P)
    for t in sorted(sums):
        tot += sums[t] / cnt[t]
    return [float(x) for x in tot / nlangs]


def band_select(per_fam, nlangs):
    """per_fam: fam -> list of band caches. Family loss = mean over its bands; pooled = mean over families."""
    grid = BAND_GRIDS[CFG["bgrid"]]
    plist = param_list(grid)
    if CFG["bdef"]:
        if DEFAULT_BP in plist:
            plist.remove(DEFAULT_BP)
        plist = [dict(DEFAULT_BP)] + plist          # ties go to the default (index 0)
    di = 0
    L = {}
    for fam, bands in sorted(per_fam.items()):
        ev = [band_eval(c, plist, nlangs[fam]) for c in bands if c]
        if ev:
            L[fam] = [sum(e[i] for e in ev) / len(ev) for i in range(len(plist))]
    fams = sorted(L)
    pooled = [sum(L[f][i] for f in fams) / len(fams) for i in range(len(plist))]
    bi = min(range(len(plist)), key=lambda i: (round(pooled[i], 9), i))
    choice, info = {}, {}
    for f in fams:
        fi = min(range(len(plist)), key=lambda i: (round(L[f][i], 9), i))
        use = bi
        if CFG["bsel"] == 3 or (CFG["bsel"] == 2 and L[f][fi] < L[f][bi] - CFG["bmargin"]):
            use = fi
        choice[f] = dict(plist[use])
        info[f] = (L[f][di], L[f][bi], L[f][fi])
    print("band pooled: default %.4f best %.4f %s" % (pooled[di], pooled[bi], plist[bi]), flush=True)
    for f in fams:
        d, b, o = info[f]
        print("band %-20s default %.4f pooled %.4f own %.4f -> %s" % (f, d, b, o, choice[f]), flush=True)
    return choice, plist[bi]


def predict(model_dir, fam, jobs):
    with open(os.path.join(model_dir, fam + ".pkl"), "rb") as f:
        M = pickle.load(f)
    CFG.update(M["cfg"])
    env_overrides()
    if CFG["r_comp_pred"] >= 0:
        CFG["r_comp"] = CFG["r_comp_pred"]
    global UNIV
    UNIV = M.get("univ") or {}
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
