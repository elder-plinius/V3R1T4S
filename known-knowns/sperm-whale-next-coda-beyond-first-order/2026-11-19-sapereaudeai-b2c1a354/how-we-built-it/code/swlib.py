"""Shared evaluator for the sperm-whale dialogues target (bank id sperm-whale-next-coda-beyond-first-order).

Everything here follows the bank's success criterion literally:
  streams  = codas grouped by REC, ordered by TsTo, ties kept in file order (stable mergesort)
  folds    = distinct REC strings sorted as text, i-th REC in fold i mod 5
  token    = (min(nClicks,10), duration bin); 5 equal-frequency Duration bins cut on the training folds only
  scored   = every coda with at least 2 earlier codas in its stream
  R1       = bigram over tokens, additive smoothing alpha in {0.01,0.03,0.1,0.3,1} by inner CV on the training folds

Leakage discipline: every predictor gets a Stream object and a position t and may read only rows [:t]
(History.of(stream, t) slices the arrays before any feature code sees them). The leakage self-test
(leakage_test.py) alters every field of rows t.. of the stream and checks predictions are bit-identical.
"""
import numpy as np
import pandas as pd

ALPHAS = (0.01, 0.03, 0.1, 0.3, 1.0)
NC = 10          # click classes 1..10 (min(nClicks,10))
NB = 5           # duration bins
V = NC * NB      # 50 tokens; token id = (c-1)*NB + b
ICI_COLS = [f"ICI{i}" for i in range(1, 29)]
FIELDS = ["nClicks", "Duration"] + ICI_COLS + ["Whale", "TsTo"]


def load_dialogues(path):
    df = pd.read_csv(path)
    df["_file_order"] = np.arange(len(df))
    df = df.sort_values(["REC", "TsTo", "_file_order"], kind="mergesort").reset_index(drop=True)
    recs = sorted(df["REC"].unique())
    fold_of = {r: i % 5 for i, r in enumerate(recs)}
    df["fold"] = df["REC"].map(fold_of).astype(int)
    df["pos"] = df.groupby("REC", sort=False).cumcount()
    return df, recs, fold_of


class Stream:
    """Arrays of one REC in stream order. Fields are float/int numpy arrays."""

    def __init__(self, rec, sub):
        self.rec = rec
        self.n = len(sub)
        self.fold = int(sub["fold"].iloc[0])
        self.a = {k: sub[k].to_numpy().copy() for k in FIELDS}
        self.row = sub.index.to_numpy()

    def copy(self):
        s = Stream.__new__(Stream)
        s.rec, s.n, s.fold, s.row = self.rec, self.n, self.fold, self.row.copy()
        s.a = {k: v.copy() for k, v in self.a.items()}
        return s


def streams_of(df):
    return {rec: Stream(rec, sub) for rec, sub in df.groupby("REC", sort=True)}


class History:
    """Read-only view of rows [:t] of a stream. Feature code receives only this."""

    def __init__(self, stream, t, edges):
        self.t = t
        self.rec = stream.rec
        self.a = {k: v[:t].copy() for k, v in stream.a.items()}
        self.edges = edges
        self.tok = tokens_from(self.a["nClicks"], self.a["Duration"], edges)

    @staticmethod
    def of(stream, t, edges):
        return History(stream, t, edges)


def bin_edges(durations):
    """5 equal-frequency bins: the 20/40/60/80% quantiles (numpy default linear interpolation)."""
    return np.quantile(np.asarray(durations, dtype=float), [0.2, 0.4, 0.6, 0.8])


def dur_bin(d, edges):
    """bin b in 0..4 with edges[b-1] <= d < edges[b]."""
    return np.searchsorted(edges, np.asarray(d, dtype=float), side="right")


def tokens_from(nclicks, durations, edges):
    c = np.minimum(np.asarray(nclicks, dtype=int), NC)
    c = np.maximum(c, 1)
    return (c - 1) * NB + dur_bin(durations, edges)


def stream_tokens(streams, edges):
    return {r: tokens_from(s.a["nClicks"], s.a["Duration"], edges) for r, s in streams.items()}


def scored_positions(stream):
    return list(range(2, stream.n))


# ---------------------------------------------------------------- R1 (bigram over tokens)

def bigram_counts(tok_seqs):
    C = np.zeros((V, V))
    for x in tok_seqs:
        if len(x) >= 2:
            np.add.at(C, (x[:-1], x[1:]), 1)
    return C


def bigram_probs(C, alpha):
    return (C + alpha) / (C.sum(axis=1, keepdims=True) + alpha * V)


def r1_select_alpha(streams, tok, train_folds):
    """Inner CV on the training folds: leave one training fold out; total held-out log-loss on its scored
    positions; ties broken toward the smaller alpha (first in ALPHAS)."""
    losses = []
    for a in ALPHAS:
        tot = 0.0
        for f in train_folds:
            inner_train = [tok[r] for r, s in streams.items() if s.fold in train_folds and s.fold != f]
            P = bigram_probs(bigram_counts(inner_train), a)
            for r, s in streams.items():
                if s.fold == f and s.n >= 3:
                    x = tok[r]
                    tot -= np.log2(P[x[1:-1], x[2:]]).sum()
        losses.append(tot)
    return ALPHAS[int(np.argmin(losses))], losses


def r1_fit(streams, tok, train_folds):
    alpha, losses = r1_select_alpha(streams, tok, train_folds)
    P = bigram_probs(bigram_counts([tok[r] for r, s in streams.items() if s.fold in train_folds]), alpha)
    return P, alpha, losses


# ---------------------------------------------------------------- p4 reference (first-order same/switch chain)

def same_seq(whale):
    """y[t] = 1 if whale[t] == whale[t-1] (defined for t >= 1)."""
    w = np.asarray(whale)
    y = np.full(len(w), -1)
    y[1:] = (w[1:] == w[:-1]).astype(int)
    return y


def switch_counts(streams, folds):
    N = np.zeros((2, 2))
    for s in streams.values():
        if s.fold in folds and s.n >= 3:
            y = same_seq(s.a["Whale"])
            np.add.at(N, (y[1:-1], y[2:]), 1)
    return N


def switch_probs(N, alpha):
    return (N + alpha) / (N.sum(axis=1, keepdims=True) + 2 * alpha)


def switch_ref_fit(streams, train_folds):
    losses = []
    for a in ALPHAS:
        tot = 0.0
        for f in train_folds:
            P = switch_probs(switch_counts(streams, [g for g in train_folds if g != f]), a)
            for s in streams.values():
                if s.fold == f and s.n >= 3:
                    y = same_seq(s.a["Whale"])
                    tot -= np.log2(P[y[1:-1], y[2:]]).sum()
        losses.append(tot)
    alpha = ALPHAS[int(np.argmin(losses))]
    return switch_probs(switch_counts(streams, train_folds), alpha), alpha, losses


# ---------------------------------------------------------------- bootstrap

def rec_bootstrap(rec_ids, diff, n_boot=10000, seed=20261119):
    """Paired bootstrap over REC groups. diff = per-position loss difference (bits; reference minus model,
    so positive = model better). Resample the RECs that own >= 1 scored position, with replacement, same
    count; statistic = sum(diff)/count over the resample (pooled per-coda gain). Percentile 95% interval."""
    rec_ids = np.asarray(rec_ids)
    diff = np.asarray(diff, dtype=float)
    uniq, inv = np.unique(rec_ids, return_inverse=True)
    sums = np.bincount(inv, weights=diff)
    cnts = np.bincount(inv).astype(float)
    rng = np.random.default_rng(seed)
    G = len(uniq)
    stats = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, G, G)
        stats[i] = sums[idx].sum() / cnts[idx].sum()
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return float(diff.mean()), float(lo), float(hi), stats
