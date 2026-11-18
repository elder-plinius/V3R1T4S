"""Andy's independent check of the whale candidate, written from the bank's criterion only (did NOT read the author's code).
Tokens: (min(nClicks,10), Duration quintile bin cut on training folds only) -> 50 tokens. Streams: codas of one REC ordered by TsTo (file order for ties).
Folds: sorted distinct REC strings, i-th in fold i mod 5. Scored: every coda with >= 2 earlier codas. R1: bigram with additive smoothing alpha chosen by inner CV.
Models compared (all pooled-CE in bits per scored coda): R1; order-k Dirichlet-backoff n-grams (k=2,3) with (alpha) chosen by inner CV over training RECs; a repetition-aware first-order model."""
import csv, math, collections, sys, itertools
import numpy as np
rows = list(csv.DictReader(open(sys.argv[1])))
for i, r in enumerate(rows): r['_i'] = i
recs = sorted({r['REC'] for r in rows}); fold_of = {rec: n % 5 for n, rec in enumerate(recs)}
by = collections.defaultdict(list)
for r in rows: by[r['REC']].append(r)
for rec in by: by[rec].sort(key=lambda r: (float(r['TsTo']), r['_i']))
V = 50
def cuts(train_recs):
    d = np.array([float(r['Duration']) for rec in train_recs for r in by[rec]]); return np.quantile(d, [0.2, 0.4, 0.6, 0.8])
def seqs(recs_, c):
    out = {}
    for rec in recs_:
        out[rec] = [ (min(int(r['nClicks']), 10) - 1) * 5 + int(np.searchsorted(c, float(r['Duration']), side='right')) for r in by[rec] ]
    return out
LOG2 = math.log(2)
def dirichlet_ngram(train, k, alpha):
    """hierarchical Dirichlet backoff: P_j(x|ctx_j) = (c(ctx_j,x) + alpha*P_{j-1}(x|ctx_{j-1})) / (c(ctx_j) + alpha), P_0 uniform-smoothed unigram"""
    cnt = [collections.defaultdict(collections.Counter) for _ in range(k + 1)]
    for s in train.values():
        for t in range(len(s)):
            for j in range(0, k + 1):
                if t - j < 0: break
                cnt[j][tuple(s[t - j:t])][s[t]] += 1
    uni = np.array([cnt[0][()][x] for x in range(V)], float); p0 = (uni + 1) / (uni.sum() + V)
    def prob(ctx):
        p = p0
        for j in range(1, k + 1):
            if len(ctx) < j: break
            c = cnt[j].get(tuple(ctx[len(ctx) - j:]))
            if not c: break
            tot = sum(c.values()); arr = np.zeros(V)
            for x, n in c.items(): arr[x] = n
            p = (arr + alpha * p) / (tot + alpha)
        return p
    return prob
def rep_first_order(train, alpha):
    """repetition-aware first order: context = (last token, capped run length of that token 1,2,3+) backing off to last token"""
    def rl(ctx):
        r = 1
        while r < len(ctx) and ctx[-1 - r] == ctx[-1] and r < 3: r += 1
        return r
    cnt1 = collections.defaultdict(collections.Counter); cnt2 = collections.defaultdict(collections.Counter)
    for s in train.values():
        for t in range(1, len(s)):
            cnt1[s[t - 1]][s[t]] += 1; cnt2[(s[t - 1], rl(s[:t]))][s[t]] += 1
    uni = collections.Counter(); [uni.update(s) for s in train.values()]; p0 = np.array([uni[x] for x in range(V)], float) + 1; p0 /= p0.sum()
    def prob(ctx):
        c1 = cnt1.get(ctx[-1], {}); a1 = np.zeros(V)
        for x, n in c1.items(): a1[x] = n
        p1 = (a1 + alpha * p0) / (a1.sum() + alpha)
        c2 = cnt2.get((ctx[-1], rl(ctx)), {}); a2 = np.zeros(V)
        for x, n in c2.items(): a2[x] = n
        return (a2 + alpha * p1) / (a2.sum() + alpha)
    return prob
def r1(train, alpha):
    cnt = collections.defaultdict(np.zeros.__class__ if False else (lambda: np.zeros(V)))
    cnt = {}
    for s in train.values():
        for t in range(1, len(s)):
            cnt.setdefault(s[t - 1], np.zeros(V))[s[t]] += 1
    def prob(ctx):
        a = cnt.get(ctx[-1], np.zeros(V)); return (a + alpha) / (a.sum() + alpha * V)
    return prob
def score(prob, seq_by_rec, recs_):
    tot = 0.0; n = 0
    for rec in recs_:
        s = seq_by_rec[rec]
        for t in range(2, len(s)):
            tot += -math.log(max(prob(s[:t])[s[t]], 1e-300)) / LOG2; n += 1
    return tot, n
def inner_select(train_recs, c, make, grid):
    """pooled inner CV over training RECs (5 inner folds by the same modulo rule); returns best hyperparameter"""
    inner = {rec: n % 5 for n, rec in enumerate(sorted(train_recs))}; best = None
    sq = seqs(train_recs, c)
    for hp in grid:
        tot = 0.0; n = 0
        for f in range(5):
            tr = {rec: sq[rec] for rec in train_recs if inner[rec] != f}; te = [rec for rec in train_recs if inner[rec] == f]
            t, m = score(make(tr, hp), sq, te); tot += t; n += m
        if best is None or tot / n < best[0]: best = (tot / n, hp)
    return best[1]
res = collections.defaultdict(lambda: [0.0, 0]); chosen = collections.defaultdict(list)
for f in range(5):
    train_recs = [r for r in recs if fold_of[r] != f]; test_recs = [r for r in recs if fold_of[r] == f]; c = cuts(train_recs)
    sq_all = seqs(recs, c); sq_tr = {r: sq_all[r] for r in train_recs}
    specs = {'R1 bigram': (r1, [0.01, 0.03, 0.1, 0.3, 1.0]),
             'order-2 Dirichlet': (lambda tr, a: dirichlet_ngram(tr, 2, a), [0.3, 1, 3, 10, 30]),
             'order-3 Dirichlet': (lambda tr, a: dirichlet_ngram(tr, 3, a), [0.3, 1, 3, 10, 30]),
             'repetition-aware first order': (rep_first_order, [0.3, 1, 3, 10, 30])}
    for name, (mk, grid) in specs.items():
        hp = inner_select(train_recs, c, mk, grid); chosen[name].append(hp)
        t, n = score(mk(sq_tr, hp), sq_all, test_recs); res[name][0] += t; res[name][1] += n
print('positions scored:', res['R1 bigram'][1], '(the author reports 3418)')
base = res['R1 bigram'][0] / res['R1 bigram'][1]
for name, (t, n) in res.items(): print(f'{name:32s} {t/n:.4f} bits/coda   vs R1: {base - t/n:+.4f}   chosen hyperparameters per fold: {chosen[name]}')
