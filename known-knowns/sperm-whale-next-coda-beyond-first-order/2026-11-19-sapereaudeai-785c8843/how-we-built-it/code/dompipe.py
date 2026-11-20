"""p3 on DominicaCodas.csv, exactly as the bank's p3 says: tokens = CodaType; Date rewritten with every '-'
replaced by '/'; streams = rows sharing rewritten Date and Unit, ordered by codaNUM2018; folds = distinct
rewritten Date strings sorted as text, i-th in fold i mod 5; scored = every coda with >= 2 earlier codas in
its stream; reference = smoothed bigram over CodaType, additive alpha in {0.01,0.03,0.1,0.3,1} by inner CV on
the training folds. Model: log-linear tilt over the CodaType vocabulary from earlier codas only."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import log_softmax

ALPHAS = (0.01, 0.03, 0.1, 0.3, 1.0)
LAMS = (1e-4, 1e-3, 1e-2, 1e-1)
ONE = ["bigram", "uni", "same1"]                       # previous coda only
REP = ["rep_run", "rep_rate"]
HIGH = ["cache", "skip", "same2", "same_whale_last", "echo2_if_switch"]
ALL = ONE + REP + HIGH
SETS = {"one": ONE, "rep": ONE + REP, "local": ONE + REP + ["cache"], "full": ALL}
FIELDS = ["tok", "IDN", "nClicks", "Duration"]


def load(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["DateR"] = df["Date"].astype(str).str.replace("-", "/", regex=False)
    vocab = sorted(df["CodaType"].astype(str).unique())
    df["tok"] = df["CodaType"].astype(str).map({v: i for i, v in enumerate(vocab)})
    dates = sorted(df["DateR"].unique())
    fold_of = {d: i % 5 for i, d in enumerate(dates)}
    df["fold"] = df["DateR"].map(fold_of).astype(int)
    df = df.sort_values(["DateR", "Unit", "codaNUM2018"], kind="mergesort").reset_index(drop=True)
    streams = {}
    for (d, u), sub in df.groupby(["DateR", "Unit"], sort=True):
        streams[(d, u)] = {"fold": int(sub["fold"].iloc[0]), "date": d, "n": len(sub),
                           "a": {k: sub[k].to_numpy().copy() for k in FIELDS}}
    return df, streams, vocab, fold_of


def hist(s, t):
    return {k: v[:t].copy() for k, v in s["a"].items()}


class Tables:
    def __init__(self, seqs, V):
        uni, bg, sk = np.zeros(V), np.zeros((V, V)), np.zeros((V, V))
        for x in seqs:
            np.add.at(uni, x, 1)
            if len(x) >= 2:
                np.add.at(bg, (x[:-1], x[1:]), 1)
            if len(x) >= 3:
                np.add.at(sk, (x[:-2], x[2:]), 1)
        self.log_uni = np.log((uni + 0.5) / (uni.sum() + 0.5 * V))
        self.p_uni = np.exp(self.log_uni)
        self.log_bg = np.log((bg + 0.3) / (bg.sum(1, keepdims=True) + 0.3 * V))
        self.log_sk = np.log((sk + 0.3) / (sk.sum(1, keepdims=True) + 0.3 * V))


def feats(h, tb, V):
    tok, idn = h["tok"], h["IDN"]
    t = len(tok)
    F = np.zeros((V, len(ALL)))
    col = {k: i for i, k in enumerate(ALL)}
    x1 = tok[t - 1]
    e1 = (np.arange(V) == x1).astype(float)
    F[:, col["bigram"]] = tb.log_bg[x1]
    F[:, col["uni"]] = tb.log_uni
    F[:, col["same1"]] = e1
    r = 1
    while r < t and tok[t - 1 - r] == x1:
        r += 1
    F[:, col["rep_run"]] = e1 * np.log(r)
    nrep = float((tok[1:t] == tok[:t - 1]).sum())
    F[:, col["rep_rate"]] = e1 * np.log((nrep + 1.0) / (t - 1 - nrep + 1.0))
    cnt = np.bincount(tok, minlength=V).astype(float)
    F[:, col["cache"]] = np.log((cnt + tb.p_uni) / (t + 1.0))
    x2 = tok[t - 2]
    F[:, col["skip"]] = tb.log_sk[x2]
    F[:, col["same2"]] = (np.arange(V) == x2)
    # whale-aware (IDN 0 = unidentified in the file): last token of the whale that made coda t-1, before t-1
    if idn[t - 1] != 0:
        k = np.nonzero(idn[:t - 1] == idn[t - 1])[0]
        if len(k):
            F[:, col["same_whale_last"]] = (np.arange(V) == tok[k[-1]])
    if idn[t - 1] != 0 and idn[t - 2] != 0 and idn[t - 1] != idn[t - 2]:
        F[:, col["echo2_if_switch"]] = (np.arange(V) == x2)
    return F


def bigram_P(seqs, V, alpha):
    C = np.zeros((V, V))
    for x in seqs:
        if len(x) >= 2:
            np.add.at(C, (x[:-1], x[1:]), 1)
    return (C + alpha) / (C.sum(1, keepdims=True) + alpha * V)


def ref_fit(streams, train_folds, V):
    losses = []
    for a in ALPHAS:
        tot = 0.0
        for f in train_folds:
            P = bigram_P([s["a"]["tok"] for s in streams.values() if s["fold"] in train_folds and s["fold"] != f], V, a)
            for s in streams.values():
                if s["fold"] == f and s["n"] >= 3:
                    x = s["a"]["tok"]
                    tot -= np.log2(P[x[1:-1], x[2:]]).sum()
        losses.append(tot)
    a = ALPHAS[int(np.argmin(losses))]
    return bigram_P([s["a"]["tok"] for s in streams.values() if s["fold"] in train_folds], V, a), a, losses


def nll_grad(th, Fs, ys, lam):
    lp = log_softmax(Fs @ th, axis=1)
    n = len(ys)
    p = np.exp(lp)
    g = -(Fs[np.arange(n), ys] - (p[:, :, None] * Fs).sum(1)).mean(0) + 2 * lam * th
    return -lp[np.arange(n), ys].mean() + lam * th @ th, g


def fit(Fs, ys, lam):
    th0 = np.zeros(Fs.shape[2])
    th0[0] = 1.0
    return minimize(nll_grad, th0, args=(Fs, ys, lam), jac=True, method="L-BFGS-B", options={"maxiter": 500}).x


def predict(th, Fs):
    return np.exp(log_softmax(Fs @ th, axis=1))


def rows(streams, folds, tables_for, V):
    Fs, ys, where = [], [], []
    for key, s in streams.items():
        if s["fold"] not in folds:
            continue
        tb = tables_for(s["fold"])
        for t in range(2, s["n"]):
            Fs.append(feats(hist(s, t), tb, V))
            ys.append(s["a"]["tok"][t])
            where.append((key, t))
    return np.array(Fs), np.array(ys, dtype=int), where


def run_fold(streams, train_folds, test_folds, V, sets=("one", "rep", "local", "full")):
    train_folds, test_folds = list(train_folds), list(test_folds)
    P, alpha, rl = ref_fit(streams, train_folds, V)
    tb_all = Tables([s["a"]["tok"] for s in streams.values() if s["fold"] in train_folds], V)
    tb_cf = {g: Tables([s["a"]["tok"] for s in streams.values() if s["fold"] in train_folds and s["fold"] != g], V)
             for g in train_folds}
    Ftr, ytr, wtr = rows(streams, train_folds, lambda f: tb_cf[f], V)
    Fte, yte, wte = rows(streams, test_folds, lambda f: tb_all, V)
    gtr = np.array([streams[k]["fold"] for k, _ in wtr])
    out = {"ref_alpha": alpha, "ref_losses": rl, "where": wte, "y": yte, "probs": {}, "theta": {}, "lam": {}}
    out["probs"]["bigram"] = np.array([P[streams[k]["a"]["tok"][t - 1]] for k, t in wte])
    for name in sets:
        idx = [ALL.index(c) for c in SETS[name]]
        A, B = Ftr[:, :, idx], Fte[:, :, idx]
        ll = []
        for lam in LAMS:
            tot = 0.0
            for g in train_folds:
                th = fit(A[gtr != g], ytr[gtr != g], lam)
                p = predict(th, A[gtr == g])
                tot -= np.log2(p[np.arange((gtr == g).sum()), ytr[gtr == g]]).sum()
            ll.append(tot)
        lam = LAMS[int(np.argmin(ll))]
        th = fit(A, ytr, lam)
        out["probs"][name], out["theta"][name], out["lam"][name] = predict(th, B), th, lam
    return out


def bits(p, y):
    return -np.log2(p[np.arange(len(y)), y])


def date_bootstrap(groups, diff, n_boot=10000, seed=20261119):
    groups = np.asarray(groups)
    diff = np.asarray(diff, dtype=float)
    u, inv = np.unique(groups, return_inverse=True)
    sums, cnts = np.bincount(inv, weights=diff), np.bincount(inv).astype(float)
    rng = np.random.default_rng(seed)
    st = np.empty(n_boot)
    for i in range(n_boot):
        j = rng.integers(0, len(u), len(u))
        st[i] = sums[j].sum() / cnts[j].sum()
    lo, hi = np.percentile(st, [2.5, 97.5])
    return float(diff.mean()), float(lo), float(hi), st


def run_fold_full(streams, train_folds, test_folds, V, sets=("one", "rep", "local", "full")):
    """run_fold plus what the leakage self-test needs."""
    out = run_fold(streams, train_folds, test_folds, V, sets)
    out["tb_all"] = Tables([s["a"]["tok"] for s in streams.values() if s["fold"] in list(train_folds)], V)
    out["P_ref"] = ref_fit(streams, list(train_folds), V)[0]
    return out


def predict_one(out, name, s, t, V):
    h = hist(s, t)
    if name == "bigram":
        return out["P_ref"][h["tok"][t - 1]].copy()
    idx = [ALL.index(c) for c in SETS[name]]
    return predict(out["theta"][name], feats(h, out["tb_all"], V)[None, :, idx])[0]
