"""SMUGGLER lens core: pairwise segment-in-context rewrite transducers + system combination (ROVER / MBR).

Imported technique: system combination from speech recognition (ROVER, Fiscus 1997: voting over a word transition
network built by aligning several recognisers' outputs) and machine translation (minimum-Bayes-risk decoding and
confusion-network combination, Kumar and Byrne 2004; Rosti et al. 2007). Here every visible sister reflex is one
"recogniser": a per-ordered-language-pair transducer turns it into an n-best list of guesses for the masked reflex;
the guesses are pooled with source reliability weights (cross-fitted NED of the pair transducer on training pairs),
and the output is the candidate (pool strings plus confusion-network consensus strings) with the lowest expected
alignment NED against the weighted pool.

Standard library only. Deterministic: no set iteration reaches the output; every tie is broken on explicit keys.
"""
import math
import pickle
from collections import Counter, defaultdict

TONES = set("⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉")
VOW = set("aeiouyæøœɶɑɒɐəɘɵɤɯɨʉɪʏʊɛɜɞʌɔɿʅɚɝɷᴀᴇ")
_CLS = {}
_BASE = {}


def scls(s):
    r = _CLS.get(s)
    if r is None:
        if s in ("#", "<s>"):
            r = s
        elif any(c in TONES for c in s):
            r = "T"
        elif any(c in VOW for c in s):
            r = "V"
        else:
            r = "C"
        _CLS[s] = r
    return r


def sbase(s):
    r = _BASE.get(s)
    if r is None:
        r = next((c for c in s if c.isalpha() or c in TONES), s[:1])
        _BASE[s] = r
    return r


def init_cost(x, y):
    """Class-aware substitution cost for the first alignment pass (gap cost is 1)."""
    if x == y:
        return 0.0
    cx, cy = scls(x), scls(y)
    if (cx == "T") != (cy == "T"):
        return 3.0
    if sbase(x) == sbase(y):
        return 0.3
    if cx == cy:
        return 0.7 if cx != "T" else 0.5
    return 1.3


def align(a, b, cost, gap=1.0):
    """Min-cost global alignment; returns list of (x or None, y or None). Ties: diagonal, then up, then left."""
    n, m = len(a), len(b)
    D = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        D[i][0] = i * gap
    for j in range(1, m + 1):
        D[0][j] = j * gap
    for i in range(1, n + 1):
        ai = a[i - 1]
        Di, Dp = D[i], D[i - 1]
        for j in range(1, m + 1):
            d = Dp[j - 1] + cost(ai, b[j - 1])
            u = Dp[j] + gap
            l = Di[j - 1] + gap
            Di[j] = d if (d <= u and d <= l) else (u if u <= l else l)
    i, j, out = n, m, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and abs(D[i][j] - (D[i - 1][j - 1] + cost(a[i - 1], b[j - 1]))) < 1e-9:
            out.append((a[i - 1], b[j - 1])); i -= 1; j -= 1
        elif i > 0 and abs(D[i][j] - (D[i - 1][j] + gap)) < 1e-9:
            out.append((a[i - 1], None)); i -= 1
        else:
            out.append((None, b[j - 1])); j -= 1
    out.reverse()
    return out


def sned(a, b):
    """Scorer-style NED: Needleman-Wunsch (match +1, mismatch -1, gap -1), mismatched columns / alignment length.
    Among max-score alignments the shortest one is taken."""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 1.0
    # cell: (score, -length, matches)
    prev = [(-j, -j, 0) for j in range(m + 1)]
    for i in range(1, n + 1):
        ai = a[i - 1]
        cur = [(-i, -i, 0)] + [None] * m
        for j in range(1, m + 1):
            p = prev[j - 1]
            if ai == b[j - 1]:
                d = (p[0] + 1, p[1] - 1, p[2] + 1)
            else:
                d = (p[0] - 1, p[1] - 1, p[2])
            q = prev[j]
            u = (q[0] - 1, q[1] - 1, q[2])
            q = cur[j - 1]
            l = (q[0] - 1, q[1] - 1, q[2])
            best = d
            if u[:2] > best[:2]:
                best = u
            if l[:2] > best[:2]:
                best = l
            cur[j] = best
        prev = cur
    s, negl, mt = prev[m]
    L = -negl
    return (L - mt) / L


# ---------------------------------------------------------------- data
def load(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    h = lines[0].split("\t")
    langs = h[1:]
    data = {}
    for ln in lines[1:]:
        r = ln.split("\t") + [""] * len(h)
        data[r[0]] = {l: tuple(r[i + 1].split()) for i, l in enumerate(langs)}
    return langs, data


# ---------------------------------------------------------------- transducer
def chunks_from_alignment(al, n):
    """al: list of (src seg or None, tgt seg or None). Return n+1 chunks: chunk 0 = insertions before the first
    source segment, chunk i = target material aligned to source segment i plus insertions after it."""
    ch = [[] for _ in range(n + 1)]
    pos = 0
    for a, b in al:
        if a is not None:
            pos += 1
            if b is not None:
                ch[pos].append(b)
        else:
            ch[pos].append(b)
    return [tuple(c) for c in ch]


def ctx_keys(x, i, cfg):
    """Context keys for position i (0 = word start slot, 1..n = source segments), general to specific."""
    n = len(x)
    if i == 0:
        return [("B",), ("B", x[0] if n else "#")]
    s = x[i - 1]
    L = x[i - 2] if i >= 2 else "#"
    R = x[i] if i < n else "#"
    keys = [("1", s), ("C", scls(L), s, scls(R))]
    if cfg.get("ctx_lr", 1):
        keys.append(("L", L, s))
        keys.append(("R", s, R))
    if scls(s) == "T" and cfg.get("tone_init", 1):
        keys.append(("I", x[0], s))
    keys.append(("3", L, s, R))
    return keys


def aux_align(x, u):
    """Aligned segment of an auxiliary source u for every position of x (0 = word start: first segment of u)."""
    aux = ["-"] * (len(x) + 1)
    aux[0] = u[0] if u else "#"
    i = 0
    for a, b in align(x, u, init_cost):
        if a is not None:
            i += 1
            aux[i] = b if b is not None else "-"
    return aux


def keys_with_aux(x, i, cfg, aux):
    k = ctx_keys(x, i, cfg)
    if aux is None:
        return k
    if i == 0:
        return k + [("XB", aux[0])]
    s = x[i - 1]
    L = x[i - 2] if i >= 2 else "#"
    R = x[i] if i < len(x) else "#"
    return k + [("X1", s, aux[i]), ("XC", scls(L), s, scls(R), aux[i])]


def copy_chunk(x, i):
    return () if i == 0 else (x[i - 1],)


def events(x, ch, cfg, aux=None):
    return [(keys_with_aux(x, i, cfg, aux), ch[i]) for i in range(len(x) + 1)]


def build_table(event_lists):
    tab = defaultdict(Counter)
    for evs in event_lists:
        for keys, c in evs:
            for k in keys:
                tab[k][c] += 1
    out = {}
    for k, c in tab.items():
        out[k] = (sum(c.values()), len(c), dict(c))
    return out


def pos_dist(tab, keys, cp, beta, prune=1e-4):
    P = {cp: 1.0}
    for k in keys:
        e = tab.get(k)
        if e is None:
            continue
        N, T, c = e
        lam = beta * T
        z = N + lam
        newP = {o: lam * p / z for o, p in P.items()}
        for o, v in c.items():
            newP[o] = newP.get(o, 0.0) + v / z
        P = newP
    if prune:
        P = {o: p for o, p in P.items() if p >= prune}
    return P


def up_keys(x, i):
    if i == 0:
        return [("B",)]
    s = x[i - 1]
    L = x[i - 2] if i >= 2 else "#"
    R = x[i] if i < len(x) else "#"
    return [("1", s), ("C", scls(L), s, scls(R))]


def dists(tab, x, cfg, aux=None):
    beta = cfg["beta"]
    up = cfg.get("_up")
    if not up:
        return [pos_dist(tab, keys_with_aux(x, i, cfg, aux), copy_chunk(x, i), beta) for i in range(len(x) + 1)]
    bu = cfg.get("beta_up", beta)
    out = []
    for i in range(len(x) + 1):
        uk = up_keys(x, i)
        P = {copy_chunk(x, i): 1.0}
        for ut in up:
            P = mix_stage(ut, uk, P, bu)
        P = mix_stage(tab, keys_with_aux(x, i, cfg, aux), P, beta)
        out.append({o: p for o, p in P.items() if p >= 1e-4})
    return out


def mix_stage(tab, keys, P, beta):
    for k in keys:
        e = tab.get(k)
        if e is None:
            continue
        N, T, c = e
        lam = beta * T
        z = N + lam
        newP = {o: lam * p / z for o, p in P.items()}
        for o, v in c.items():
            newP[o] = newP.get(o, 0.0) + v / z
        P = newP
    return P


def nbest(tab, x, cfg, K=None, B=None, D=None):
    K = K or cfg["K"]
    B = B or cfg["beam"]
    kpos = cfg.get("kpos", 4)
    beams = [((), 0.0)]
    for Di in (D if D is not None else dists(tab, x, cfg)):
        items = sorted(Di.items(), key=lambda kv: (-kv[1], kv[0]))[:kpos]
        new = []
        for h, lp in beams:
            for o, p in items:
                new.append((h + o, lp + math.log(p)))
        new.sort(key=lambda z: (-z[1], z[0]))
        beams = new[:B]
    agg = {}
    for h, lp in beams:
        agg[h] = agg.get(h, 0.0) + math.exp(lp)
    out = sorted(agg.items(), key=lambda kv: (-kv[1], kv[0]))
    out = [(h, p) for h, p in out if h][:K]
    z = sum(p for _, p in out)
    return [(h, p / z) for h, p in out] if z > 0 else []


def forced_logp(D, h, floor):
    """Viterbi log-probability that the transducer (position distributions D over chunks) emits string h.
    Chunks of length 0..3; a chunk the distribution does not list costs log(floor)."""
    m = len(h)
    NEG = -1e18
    lf = math.log(floor)
    prev = [NEG] * (m + 1)
    D0 = D[0]
    for j in range(min(m, 3) + 1):
        p = D0.get(h[:j])
        prev[j] = math.log(p) if p else lf * max(1, j)
    for Di in D[1:]:
        cur = [NEG] * (m + 1)
        for j in range(m + 1):
            best = NEG
            for l in range(0, min(j, 3) + 1):
                b = prev[j - l]
                if b <= NEG / 2:
                    continue
                p = Di.get(h[j - l:j])
                v = b + (math.log(p) if p else lf * max(1, l))
                if v > best:
                    best = v
            cur[j] = best
        prev = cur
    return prev[m]


# ---------------------------------------------------------------- alignment learning (hard EM, H9)
def learn_cost(pairs_al, cfg):
    """From alignments of an unordered language pair, build a PMI-like substitution cost (gap cost stays 1)."""
    c = Counter()
    cx, cy = Counter(), Counter()
    for al in pairs_al:
        for a, b in al:
            c[(a, b)] += 1
            cx[a] += 1
            cy[b] += 1
    N = sum(c.values())
    kap = cfg.get("em_kappa", 1.0)
    cache = {}

    def cost(x, y):
        r = cache.get((x, y))
        if r is None:
            ic = init_cost(x, y)
            if ic >= 3.0:
                r = ic
            else:
                prior = math.exp(-2.0 * ic)
                pxy = (c.get((x, y), 0) + kap * prior) / (N + kap)
                px = (cx.get(x, 0) + kap) / (N + kap)
                py = (cy.get(y, 0) + kap) / (N + kap)
                pmi = math.log(pxy / (px * py))
                # map PMI to a cost in [0, 2.5]; strong correspondences are cheap
                r = min(2.5, max(0.0, 1.0 - 0.25 * pmi))
            cache[(x, y)] = r
        return r
    return cost


def train_family(path, cfg):
    langs, data = load(path)
    return train_from_data(langs, data, cfg)


def train_from_data(langs, data, cfg):
    keys = list(data)
    K = cfg.get("folds", 5)
    fold = {k: i % K for i, k in enumerate(keys)}
    pairs = {}
    rel = {}
    tune = cfg.get("tune", 0) or cfg.get("rr_cf", 0)
    cfnb = {}  # (row, src, tgt) -> cross-fitted n-best (only when tuning)
    hier = cfg.get("hier", 0)
    ALS = {}
    up_fam, up_tgt = None, {}
    if hier:
        # pre-pass: pooled (any source -> target t) and family-wide correspondence counts for the backoff hierarchy
        fam_ev, tgt_ev = [], defaultdict(list)
        for ia, s in enumerate(langs):
            for t in langs[ia + 1:]:
                rows = [k for k in keys if data[k][s] and data[k][t]]
                for k in rows:
                    al = align(data[k][s], data[k][t], init_cost)
                    ALS[(s, t, k)] = al
                    for (src, tgt, a) in ((s, t, al), (t, s, [(y, x) for x, y in al])):
                        x = data[k][src]
                        ch = chunks_from_alignment(a, len(x))
                        ev = [(up_keys(x, i), ch[i]) for i in range(len(x) + 1)]
                        fam_ev.append(ev)
                        tgt_ev[tgt].append(ev)
        up_fam = build_table(fam_ev)
        up_tgt = {t: build_table(tgt_ev[t]) for t in langs}
        del fam_ev, tgt_ev
    for ia, s in enumerate(langs):
        for t in langs[ia + 1:]:
            rows = [k for k in keys if data[k][s] and data[k][t]]
            if not rows:
                continue
            al = {k: ALS.get((s, t, k)) or align(data[k][s], data[k][t], init_cost) for k in rows}
            for _ in range(cfg.get("em_iters", 0)):
                cost = learn_cost(list(al.values()), cfg)
                al = {k: align(data[k][s], data[k][t], cost) for k in rows}
            for (src, tgt, flip) in ((s, t, False), (t, s, True)):
                cfg_t = dict(cfg, _up=(up_fam, up_tgt[tgt])) if hier else cfg
                evs = {}
                for k in rows:
                    a = [(y, x) for x, y in al[k]] if flip else al[k]
                    x = data[k][src]
                    evs[k] = events(x, chunks_from_alignment(a, len(x)), cfg)
                tab = build_table(evs.values())
                pairs[(src, tgt)] = tab
                # cross-fitted reliability
                tot, nn = 0.0, 0
                if len(rows) >= 2:
                    for f in range(K):
                        held = [k for k in rows if fold[k] == f]
                        if not held:
                            continue
                        ftab = build_table([evs[k] for k in rows if fold[k] != f])
                        for k in held:
                            if tune:
                                nb = nbest(ftab, data[k][src], cfg_t)
                                cfnb[(k, src, tgt)] = nb
                            else:
                                nb = nbest(ftab, data[k][src], cfg_t, K=1, B=cfg.get("cf_beam", 4))
                            h = nb[0][0] if nb else data[k][src]
                            tot += sned(h, data[k][tgt]); nn += 1
                rel[(src, tgt)] = (tot / nn if nn else 1.0, len(rows))
    model = {"langs": langs, "pairs": pairs, "rel": rel}
    if hier:
        model["up_fam"] = up_fam
        model["up_tgt"] = up_tgt
    if cfg.get("aux", 0):
        train_aux(model, data, keys, fold, cfg)
    if cfg.get("tune", 0):
        tune_alpha(model, data, keys, cfnb, cfg)
    if cfg.get("rr_cf", 0):
        train_reranker(model, data, keys, cfnb, cfg)
    if cfg.get("rr_inner", 0):
        model["lms"] = {t: lm_build([data[k][t] for k in keys if data[k][t]]) for t in langs}
    return model


def train_reranker(model, data, keys, cfnb, cfg):
    langs = model["langs"]
    lms = {t: lm_build([data[k][t] for k in keys if data[k][t]]) for t in langs}
    model["lms"] = lms
    lists = []
    cap = cfg.get("rr_maxlists", 3000)
    jobs = []
    for t in langs:
        for k in keys:
            if data[k][t]:
                jobs.append((k, t))
    if len(jobs) > cap:
        step = len(jobs) / cap
        jobs = [jobs[int(i * step)] for i in range(cap)]
    for k, t in jobs:
        gold = data[k][t]
        nbs = [(s, cfnb[(k, s, t)]) for s in langs if s != t and cfnb.get((k, s, t))]
        if not nbs:
            continue
        cands, F = cand_features(nbs, t, model, cfg, lms[t], loo=gold)
        lists.append((F, [sned(c, gold) for c in cands]))
    model["rr"] = fit_reranker(lists, cfg) if lists else None
    model["rr_nlists"] = len(lists)


def aux_choice(model, s, t, cfg):
    """Auxiliary source for pair (s, t): the most reliable source for t other than s (by cross-fitted NED)."""
    order = model.setdefault("_order", {})
    if t not in order:
        cand = [(r, u) for (u, tt), (r, n) in model["rel"].items() if tt == t and n >= cfg.get("aux_min", 10)]
        order[t] = [u for _, u in sorted(cand)]
    for u in order[t]:
        if u != s:
            return u
    return None


def train_aux(model, data, keys, fold, cfg):
    """Multi-source transducers (multi-source NMT import): pair (s, t) also conditions on the aligned segment of an
    auxiliary source u (the best source for t other than s)."""
    langs = model["langs"]
    K = cfg.get("folds", 5)
    pairs2, rel2 = {}, {}
    for (s, t) in sorted(model["pairs"]):
        u = aux_choice(model, s, t, cfg)
        if u is None or u == t:
            continue
        rows = [k for k in keys if data[k][s] and data[k][t] and data[k][u]]
        if len(rows) < cfg.get("aux_min", 10):
            continue
        evs = {}
        for k in rows:
            x = data[k][s]
            al = align(x, data[k][t], init_cost)
            evs[k] = events(x, chunks_from_alignment(al, len(x)), cfg, aux_align(x, data[k][u]))
        pairs2[(s, t)] = (u, build_table(evs.values()))
        tot, nn = 0.0, 0
        for f in range(K):
            held = [k for k in rows if fold[k] == f]
            if not held:
                continue
            ftab = build_table([evs[k] for k in rows if fold[k] != f])
            for k in held:
                x = data[k][s]
                D = dists(ftab, x, cfg, aux_align(x, data[k][u]))
                nb = nbest(ftab, x, cfg, K=1, B=cfg.get("cf_beam", 4), D=D)
                h = nb[0][0] if nb else x
                tot += sned(h, data[k][t]); nn += 1
        rel2[(s, t)] = (tot / nn if nn else 1.0, len(rows))
    model["pairs2"] = pairs2
    model["rel2"] = rel2
    model.pop("_order", None)


def tune_alpha(model, data, keys, cfnb, cfg):
    """Fit the source-weight sharpness alpha (and the posterior temperature gamma) on cross-fitted training
    predictions (MT-style combination-weight tuning on held-out data): per target language, mean NED of a cheap MBR
    combination at each grid point; the family choice minimises the mean over target languages (the scorer's
    language weighting)."""
    langs = model["langs"]
    agrid = cfg.get("alpha_grid", [0, 2, 4, 6, 8, 12, 16, 24, 32])
    ggrid = cfg.get("gamma_grid", [cfg.get("gamma", 1.0)])
    grid = [(a, g) for g in ggrid for a in agrid]
    res = {}
    for t in langs:
        acc = [0.0] * len(grid)
        n = 0
        for k in keys:
            gold = data[k][t]
            if not gold:
                continue
            nbs = [(s, cfnb[(k, s, t)]) for s in langs if s != t and (k, s, t) in cfnb and cfnb[(k, s, t)]]
            if not nbs:
                continue
            cache = {}
            for gi, (a, g) in enumerate(grid):
                c = dict(cfg, alpha=a, gamma=g, M=cfg.get("tune_M", 5), pool_max=cfg.get("tune_pool", 20), rover=0)
                pred = combine_nbests(nbs, t, model, c, cache)
                key = (pred, gold)
                if key not in cache:
                    cache[key] = sned(pred, gold)
                acc[gi] += cache[key]
            n += 1
        if n:
            res[t] = [x / n for x in acc]
    fam_curve = [sum(res[t][gi] for t in res) / len(res) for gi in range(len(grid))] if res else [0] * len(grid)
    gi = min(range(len(grid)), key=lambda i: (fam_curve[i], i))
    model["alpha_fam"] = grid[gi][0]
    model["gamma_fam"] = grid[gi][1]
    model["alpha_tgt"] = {t: grid[min(range(len(grid)), key=lambda i: (res[t][i], i))][0] for t in res}
    model["tune_curve"] = {"grid": grid, "fam": fam_curve, "tgt": res}


# ---------------------------------------------------------------- combination
def rover(pivot, items):
    """Confusion network on the pivot: returns per-slot vote dicts (slots: 2j = insertion before pivot j, 2j+1 =
    pivot segment j)."""
    m = len(pivot)
    votes = [defaultdict(float) for _ in range(2 * m + 1)]
    for h, w in items:
        al = align(pivot, h, init_cost)
        ins = defaultdict(list)
        sub = [()] * m
        j = 0
        for a, b in al:
            if a is None:
                ins[j].append(b)
            else:
                sub[j] = (b,) if b is not None else ()
                j += 1
        for j in range(m + 1):
            votes[2 * j][tuple(ins.get(j, ()))] += w
        for j in range(m):
            votes[2 * j + 1][sub[j]] += w
    return votes


def cn_paths(votes, nalt=3):
    best, margins = [], []
    for si, v in enumerate(votes):
        it = sorted(v.items(), key=lambda kv: (-kv[1], kv[0]))
        best.append(it[0][0])
        if len(it) > 1:
            margins.append((it[0][1] - it[1][1], si, it[1][0]))
    out = [tuple(s for o in best for s in o)]
    margins.sort()
    for _, si, alt in margins[:nalt]:
        b2 = list(best)
        b2[si] = alt
        out.append(tuple(s for o in b2 for s in o))
    return out


def get_gamma(model, cfg):
    if cfg.get("gamma_mode") == "fam" and "gamma_fam" in model:
        return model["gamma_fam"]
    return cfg.get("gamma", 1.0)


def get_alpha(model, tgt, cfg):
    am = cfg.get("alpha_mode", "fixed")
    if am == "fam" and "alpha_fam" in model:
        return model["alpha_fam"]
    if am == "tgt" and "alpha_tgt" in model:
        return model["alpha_tgt"].get(tgt, model["alpha_fam"])
    return cfg["alpha"]


def src_weight(r, n, alpha, n0, cfg):
    """Source reliability weight. exp: exp(-alpha*NED) (scale-dependent); inv: NED^-k (scale-free)."""
    wm = cfg.get("wmode", "exp")
    if wm == "inv":
        w = (max(r, cfg.get("rfloor", 0.02))) ** (-cfg.get("kinv", 2.0))
    else:
        w = math.exp(-alpha * r)
    return w * (n / (n + n0))


def combine_nbests(nbs, tgt, model, cfg, cache=None, rels=None):
    """nbs: list of (source language, n-best list). Returns the chosen string (tuple of segments)."""
    langs = model["langs"]
    alpha, gamma = cfg["alpha"], cfg.get("gamma", 1.0)
    n0 = cfg.get("n0", 5.0)
    pool = defaultdict(float)
    contrib = []
    for s, nb in nbs:
        r, n = rels[s] if rels else model["rel"][(s, tgt)]
        w = src_weight(r, n, alpha, n0, cfg)
        ps = [p ** gamma for _, p in nb]
        z = sum(ps)
        for (h, _), p in zip(nb, ps):
            pool[h] += w * p / z
        contrib.append((w, s, nb))
    items = sorted(pool.items(), key=lambda kv: (-kv[1], kv[0]))
    if cfg.get("mode") == "top1":
        return items[0][0]
    if cfg.get("mode") == "best_source":
        w, s, nb = max(contrib, key=lambda z: (z[0], -langs.index(z[1])))
        return nb[0][0]
    items = items[:cfg.get("pool_max", 40)]
    W = sum(w for _, w in items)
    items = [(h, w / W) for h, w in items]
    cands = [h for h, _ in items[:cfg.get("M", 10)]]
    if cfg.get("rover", 1):
        votes = rover(items[0][0], items)
        for c in cn_paths(votes, cfg.get("nalt", 3)):
            if c and c not in cands:
                cands.append(c)
    if cache is None:
        cache = {}
    best, bl = None, None
    for c in cands:
        loss = 0.0
        for h, w in items:
            key = (c, h)
            d = cache.get(key)
            if d is None:
                d = cache[key] = sned(c, h)
            loss += w * d
        if bl is None or loss < bl - 1e-12:
            best, bl = c, loss
    return best


def mbr_pick(cands, items, cache=None):
    if cache is None:
        cache = {}
    best, bl = None, None
    for c in cands:
        loss = 0.0
        for h, w in items:
            key = (c, h)
            d = cache.get(key)
            if d is None:
                d = cache[key] = sned(c, h)
            loss += w * d
        if bl is None or loss < bl - 1e-12:
            best, bl = c, loss
    return best


def combine(row, tgt, model, cfg):
    langs = model["langs"]
    srcs = [l for l in langs if l != tgt and row[l] and row[l] != ("?",)]
    cfg = dict(cfg, alpha=get_alpha(model, tgt, cfg), gamma=get_gamma(model, cfg))
    if cfg.get("hier", 0) and "up_fam" in model:
        cfg["_up"] = (model["up_fam"], model["up_tgt"][tgt])
    nbs, Ds, rels = [], [], {}
    p2 = model.get("pairs2", {}) if cfg.get("aux", 0) else {}
    for s in srcs:
        tab = model["pairs"].get((s, tgt))
        if tab is None:
            continue
        rels[s] = model["rel"][(s, tgt)]
        D = None
        if (s, tgt) in p2:
            u, tab2 = p2[(s, tgt)]
            if row[u] and row[u] != ("?",):
                D = dists(tab2, row[s], cfg, aux_align(row[s], row[u]))
                tab = tab2
                rels[s] = model["rel2"][(s, tgt)]
        if D is None:
            D = dists(tab, row[s], cfg)
        nb = nbest(tab, row[s], cfg, D=D)
        if nb:
            nbs.append((s, nb))
            Ds.append((s, D))
    if not nbs:
        return row[srcs[0]] if srcs else ("a",)
    if cfg.get("rerank", 0) and model.get("rr"):
        cands, F = cand_features(nbs, tgt, model, cfg, model["lms"][tgt])
        return rerank_pick(cands, F, model["rr"])
    if not cfg.get("poe", 0):
        return combine_nbests(nbs, tgt, model, cfg, rels=rels)
    # product-of-experts rescoring (log-linear multi-source combination) of pool + consensus candidates
    alpha, gamma, n0 = cfg["alpha"], cfg.get("gamma", 1.0), cfg.get("n0", 5.0)
    pool = defaultdict(float)
    ws = {}
    for s, nb in nbs:
        r, n = model["rel"][(s, tgt)]
        w = math.exp(-alpha * r) * (n / (n + n0))
        ws[s] = w
        ps = [p ** gamma for _, p in nb]
        z = sum(ps)
        for (h, _), p in zip(nb, ps):
            pool[h] += w * p / z
    items = sorted(pool.items(), key=lambda kv: (-kv[1], kv[0]))[:cfg.get("pool_max", 40)]
    W = sum(w for _, w in items)
    items = [(h, w / W) for h, w in items]
    cands = [h for h, _ in items]
    if cfg.get("rover", 1):
        for c in cn_paths(rover(items[0][0], items), cfg.get("nalt", 3)):
            if c and c not in cands:
                cands.append(c)
    pa = cfg.get("poe_alpha", alpha)
    pw = {s: math.exp(-pa * model["rel"][(s, tgt)][0]) * (model["rel"][(s, tgt)][1] / (model["rel"][(s, tgt)][1] + n0))
          for s, _ in Ds}
    Z = sum(pw.values())
    floor, cap = cfg.get("poe_floor", 1e-4), cfg.get("poe_cap", -30.0)
    sc = []
    for c in cands:
        v = 0.0
        for s, D in Ds:
            v += pw[s] / Z * max(forced_logp(D, c, floor), cap)
        sc.append(v)
    T = cfg.get("poe_T", 0.3)
    mx = max(sc)
    post = [math.exp((v - mx) / T) for v in sc]
    zp = sum(post)
    post = [p / zp for p in post]
    lam = cfg.get("poe_mix", 1.0)
    pd = dict(items)
    mixed = [(c, lam * p + (1 - lam) * pd.get(c, 0.0)) for c, p in zip(cands, post)]
    if cfg.get("poe_argmax", 0):
        return mixed[max(range(len(mixed)), key=lambda i: (mixed[i][1], -i))][0]
    mixed = [(c, p) for c, p in mixed if p > 1e-6]
    return mbr_pick(cands, mixed)


def predict_file(model, inp, outp, cfg):
    langs, data = load(inp)
    with open(outp, "w", encoding="utf-8") as f:
        f.write("COGID\t" + "\t".join(langs) + "\n")
        for key, row in data.items():
            tgt = [l for l in langs if row[l] == ("?",)][0]
            pred = combine(row, tgt, model, cfg)
            f.write(key + "".join("\t" + (" ".join(pred) if l == tgt else "") for l in langs) + "\n")


def save(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f, protocol=4)


def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)


# ---------------------------------------------------------------- discriminative n-best reranking (MT/ASR import)
FEAT_ALPHAS = (0.0, 5.0, 20.0)
NFEAT = 15


def lm_build(words):
    big, uni = Counter(), Counter()
    inv = set()
    for w in words:
        seq = ("<s>",) + tuple(w) + ("</s>",)
        for a, b in zip(seq, seq[1:]):
            big[(a, b)] += 1
            uni[a] += 1
        inv.update(w)
    return {"big": dict(big), "uni": dict(uni), "V": len(inv) + 2, "N": sum(uni.values())}


def lm_score(lm, w, loo=None):
    """Average log-prob per transition of a segment bigram LM (add-k mix with unigram); loo = word whose counts are
    left out (exact leave-one-out for training rows)."""
    sub_b, sub_u = Counter(), Counter()
    if loo:
        seq = ("<s>",) + tuple(loo) + ("</s>",)
        for a, b in zip(seq, seq[1:]):
            sub_b[(a, b)] += 1
            sub_u[a] += 1
    big, uni, V, N = lm["big"], lm["uni"], lm["V"], lm["N"] - sum(sub_u.values())
    seq = ("<s>",) + tuple(w) + ("</s>",)
    tot = 0.0
    for a, b in zip(seq, seq[1:]):
        pu = (uni.get(b, 0) - sub_u.get(b, 0) + 1.0) / (N + V)
        ca = uni.get(a, 0) - sub_u.get(a, 0)
        cab = big.get((a, b), 0) - sub_b.get((a, b), 0)
        tot += math.log((cab + 2.0 * pu) / (ca + 2.0))
    return tot / (len(seq) - 1)


def cand_features(nbs, tgt, model, cfg, lm, loo=None):
    n0 = cfg.get("n0", 5.0)
    rel = model["rel"]
    pools = []
    for a in FEAT_ALPHAS:
        pool = defaultdict(float)
        for s, nb in nbs:
            r, n = rel[(s, tgt)]
            w = math.exp(-a * r) * (n / (n + n0))
            for h, p in nb:
                pool[h] += w * p
        z = sum(pool.values())
        pools.append({h: v / z for h, v in pool.items()})
    p5 = pools[1]
    items = sorted(p5.items(), key=lambda kv: (-kv[1], kv[0]))
    ref = items[:cfg.get("rr_ref", 25)]
    zr = sum(w for _, w in ref)
    ref = [(h, w / zr) for h, w in ref]
    cands = [h for h, _ in items[:cfg.get("rr_cands", 20)]]
    cons = set()
    if cfg.get("rover", 1):
        for c in cn_paths(rover(items[0][0], ref), cfg.get("nalt", 3)):
            if c and c not in cands:
                cands.append(c)
            cons.add(c)
    ws = {}
    for s, nb in nbs:
        r, n = rel[(s, tgt)]
        ws[s] = math.exp(-5.0 * r) * (n / (n + n0))
    W = sum(ws.values())
    top1 = defaultdict(float)
    inlist = defaultdict(float)
    maxp = defaultdict(float)
    for s, nb in nbs:
        top1[nb[0][0]] += ws[s] / W
        for h, p in nb:
            inlist[h] += ws[s] / W
            if p > maxp[h]:
                maxp[h] = p
    elen = sum(w * len(h) for h, w in ref)
    pinv = defaultdict(float)
    for s, nb in nbs:
        r, n = rel[(s, tgt)]
        w = max(r, 0.02) ** -2.0 * (n / (n + n0))
        for h, p in nb:
            pinv[h] += w * p
    zi = sum(pinv.values())
    pinv = {h: v / zi for h, v in pinv.items()}
    refi = sorted(pinv.items(), key=lambda kv: (-kv[1], kv[0]))[:cfg.get("rr_ref", 25)]
    zr = sum(w for _, w in refi)
    refi = [(h, w / zr) for h, w in refi]
    cache = {}
    F = []
    for c in cands:
        en = 0.0
        for h, w in ref:
            d = cache.get((c, h))
            if d is None:
                d = cache[(c, h)] = sned(c, h)
            en += w * d
        F.append([math.log(pools[0].get(c, 0.0) + 1e-4), math.log(pools[1].get(c, 0.0) + 1e-4),
                  math.log(pools[2].get(c, 0.0) + 1e-4), en, top1.get(c, 0.0), 1.0 if c in cons else 0.0,
                  1.0 if c == items[0][0] else 0.0, abs(len(c) - elen), lm_score(lm, c, loo) if lm else 0.0,
                  math.log(maxp.get(c, 0.0) + 1e-4), inlist.get(c, 0.0), float(len(c)), math.log(len(nbs)),
                  math.log(pinv.get(c, 0.0) + 1e-4), sum(w * cache.get((c, h)) if (c, h) in cache else
                                                           w * sned(c, h) for h, w in refi)])
    return cands, F


def fit_reranker(lists, cfg, weights=None):
    """lists: [(F (C x NFEAT), d (C))]. Listwise softmax, minimise (weighted) expected NED + L2; Adam;
    deterministic."""
    import numpy as np
    C = max(len(d) for _, d in lists)
    N = len(lists)
    om = np.ones(N) if weights is None else np.asarray(weights, dtype=float)
    om = om / om.mean()
    X = np.zeros((N, C, NFEAT))
    D = np.ones((N, C))
    M = np.zeros((N, C))
    for i, (F, d) in enumerate(lists):
        X[i, :len(d)] = F
        D[i, :len(d)] = d
        M[i, :len(d)] = 1
    flat = X[M > 0]
    mu, sd = flat.mean(0), flat.std(0) + 1e-6
    Xn = (X - mu) / sd * M[..., None]
    th = np.zeros(NFEAT)
    th[3] = -cfg.get("rr_init", 3.0)  # start near MBR (low expected NED preferred)
    lam = cfg.get("rr_l2", 1e-3)
    m1, m2 = np.zeros(NFEAT), np.zeros(NFEAT)
    lr, b1, b2 = cfg.get("rr_lr", 0.05), 0.9, 0.999
    for it in range(1, cfg.get("rr_iters", 300) + 1):
        s = Xn @ th
        s = np.where(M > 0, s, -1e9)
        s = s - s.max(1, keepdims=True)
        p = np.exp(s) * M
        p = p / p.sum(1, keepdims=True)
        E = (p * D).sum(1, keepdims=True)
        gs = p * (D - E) * om[:, None]
        g = np.einsum("nc,ncf->f", gs, Xn) / N + 2 * lam * th
        m1 = b1 * m1 + (1 - b1) * g
        m2 = b2 * m2 + (1 - b2) * g * g
        th = th - lr * (m1 / (1 - b1 ** it)) / (np.sqrt(m2 / (1 - b2 ** it)) + 1e-8)
    s = Xn @ th
    s = np.where(M > 0, s, -1e9)
    pick = s.argmax(1)
    final = float((D[np.arange(N), pick] * om).mean())
    return {"theta": th.tolist(), "mu": mu.tolist(), "sd": sd.tolist(), "train_ned": final}


def rerank_pick(cands, F, rr):
    th, mu, sd = rr["theta"], rr["mu"], rr["sd"]
    best, bs = None, None
    for c, f in zip(cands, F):
        v = sum(t * (x - m) / s for t, x, m, s in zip(th, f, mu, sd))
        if bs is None or v > bs + 1e-12:
            best, bs = c, v
    return best


def inner_lists(path, cfg):
    """Mimic the organisers' split inside the training file: the 15% most complete cognate sets become an inner test
    set (as complete as real test rows), transducers are trained on the rest, and every inner-test row yields one
    reranking list (candidates, features, NED to the inner gold). Returns (lists, weights) with every target language
    of the family weighing the same."""
    langs, data = load(path)
    keys = list(data)
    order = sorted(keys, key=lambda k: sum(1 for l in langs if data[k][l]), reverse=True)
    cut = int(len(keys) * cfg.get("inner_ratio", 0.15) + 0.5)
    te = set(order[:cut])
    tr_path_data = {k: data[k] for k in keys if k not in te}
    m = train_from_data(langs, tr_path_data, dict(cfg, rr_cf=0, tune=0, rr_inner=0))
    lms = {t: lm_build([v[t] for v in tr_path_data.values() if v[t]]) for t in langs}
    m["lms"] = lms
    per_t = defaultdict(list)
    for k in order[:cut]:
        row = data[k]
        for t in langs:
            gold = row[t]
            if not gold:
                continue
            nbs = []
            for s in langs:
                if s == t or not row[s] or (s, t) not in m["pairs"]:
                    continue
                nb = nbest(m["pairs"][(s, t)], row[s], cfg)
                if nb:
                    nbs.append((s, nb))
            if not nbs:
                continue
            cands, F = cand_features(nbs, t, m, cfg, lms[t])
            per_t[t].append((F, [sned(c, gold) for c in cands]))
    lists, wts = [], []
    nt = len(per_t)
    for t in langs:
        for L in per_t.get(t, []):
            lists.append(L)
            wts.append(1.0 / (nt * len(per_t[t])))
    return lists, wts
