"""Null controls exactly as PREREG.md 'Null design' (N4, N2, N3). Each control runs the same frozen pipeline
end to end (all 5 folds, all inner CV) on resimulated data and appends 'i,gain[,extra]' to the output file.
Usage: python -I nulls.py {N4|N2|N3} <csv> <first> <last_exclusive> <out.csv>"""
import os
import sys
import time

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
for p in [here, os.path.join(here, "..", "..", "turn-taking", "code"), os.path.join(here, "..", "..", "sequence-model", "code"),
          os.path.join(here, "..", "..", "dominica", "code")]:
    sys.path.insert(0, p)
import swlib  # noqa: E402

kind, path, i0, i1, out_path = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
done = set()
if os.path.exists(out_path):
    done = {int(l.split(",")[0]) for l in open(out_path) if l.strip()}
fout = open(out_path, "a", newline="\n")


def fast_grad_factory():
    """Same objective and gradient as seqlib.nll_and_grad / dompipe.nll_grad, with the expectation term computed by
    einsum instead of a broadcast-and-sum (6-7x faster). Checked against the frozen per-position probabilities of
    the real data (verification mode below); used for the null controls only."""
    from scipy.special import log_softmax

    def g(theta, Fs, ys, lam):
        lp = log_softmax(Fs @ theta, axis=1)
        n = len(ys)
        p = np.exp(lp)
        Ey = np.einsum("nv,nvk->nk", p, Fs)
        grad = -(Fs[np.arange(n), ys] - Ey).mean(0) + 2 * lam * theta
        return -lp[np.arange(n), ys].mean() + lam * theta @ theta, grad
    return g


def pooled(bits_ref, bits_mod):
    return float((np.concatenate(bits_ref) - np.concatenate(bits_mod)).mean())


if kind == "N4":
    import p4lib
    df, recs, fold_of = swlib.load_dialogues(path)
    base = swlib.streams_of(df)
    N = np.zeros((2, 2))
    for s in base.values():
        if s.n >= 3:
            y = swlib.same_seq(s.a["Whale"])
            np.add.at(N, (y[1:-1], y[2:]), 1)
    p_same = N[:, 1] / N.sum(1)          # MLE P(same | prev same/switch)
    for i in range(i0, i1):
        if i in done:
            continue
        t0 = time.time()
        rng = np.random.default_rng(1000 + i)
        st = {}
        for r, s in base.items():
            c = s.copy()
            w = c.a["Whale"]
            K = max(len(np.unique(s.a["Whale"])), 2)
            for t in range(2, c.n):
                prev_same = int(w[t - 1] == w[t - 2])
                if rng.random() < p_same[prev_same]:
                    w[t] = w[t - 1]
                else:
                    choices = [k for k in range(1, K + 1) if k != w[t - 1]]
                    w[t] = choices[rng.integers(0, len(choices))]
            st[r] = c
        br, bm = [], []
        for k in range(5):
            fit = p4lib.fit_fold(st, [g for g in range(5) if g != k], [k], p4lib.FEATURE_SETS["full"])
            br.append(p4lib._bits(fit["y"], fit["p_ref"]))
            bm.append(p4lib._bits(fit["y"], fit["p"]))
        fout.write(f"{i},{pooled(br, bm)!r}\n")
        fout.flush()
        print(i, round(pooled(br, bm), 5), f"{time.time() - t0:.1f}s", flush=True)

elif kind == "N2":
    import types

    from scipy.special import ndtr

    import seqlib
    import seqpipe
    df, recs, fold_of = swlib.load_dialogues(path)
    base = swlib.streams_of(df)
    # Speed shim: scipy.stats.norm.cdf(x) with loc 0, scale 1 evaluates scipy.special.ndtr(x). Swap it in for the
    # null runs only, after checking bit-identical feature matrices on every position of the real data (fold 0's
    # edges and tables). The frozen seqlib.py file is not modified.
    e0 = swlib.bin_edges(np.concatenate([s.a["Duration"] for s in base.values() if s.fold != 0]))
    tk0 = swlib.stream_tokens(base, e0)
    tb0 = seqlib.Tables([tk0[r] for r, s in base.items() if s.fold != 0])
    pos = [(r, t) for r, s in base.items() for t in range(2, s.n)]
    ref = [seqlib.feats(swlib.History.of(base[r], t, e0), tb0) for r, t in pos]
    real_norm = seqlib.norm
    seqlib.norm = types.SimpleNamespace(cdf=ndtr)
    new = [seqlib.feats(swlib.History.of(base[r], t, e0), tb0) for r, t in pos]
    assert all(np.array_equal(a, b) for a, b in zip(ref, new)), "ndtr shim is not bit-identical"
    print(f"ndtr shim verified bit-identical on {len(pos)} positions x {ref[0].size} feature values", flush=True)
    del ref, new
    # Second speed shim: vectorised feats (fastfeats.py), checked bit-identical against the frozen feats on every
    # real scored position under fold 0's edges and tables before use.
    import fastfeats
    seqlib.norm = real_norm
    ref = [seqlib.feats(swlib.History.of(base[r], t, e0), tb0) for r, t in pos]
    new = [fastfeats.feats(swlib.History.of(base[r], t, e0), tb0) for r, t in pos]
    assert all(np.array_equal(a, b) for a, b in zip(ref, new)), "fastfeats is not bit-identical"
    print(f"fastfeats verified bit-identical on {len(pos)} positions", flush=True)
    del ref, new
    seqlib.feats = fastfeats.feats
    seqlib.nll_and_grad = fast_grad_factory()
    if len(sys.argv) > 6:      # verification against the frozen run: python -I nulls.py N2 csv 0 0 out probs_all.npz
        z = np.load(sys.argv[6], allow_pickle=False)
        o = seqpipe.run_fold(base, [1, 2, 3, 4], [0], sets=("twin", "full"))
        m = z["fold"] == 0
        for nme in ["R1", "twin", "full"]:
            d = float(np.max(np.abs(o["probs"][nme] - z[nme][m])))
            print(f"fast-grad check fold 0 {nme}: max abs prob diff vs frozen = {d:.3e}, identical = "
                  f"{np.array_equal(o['probs'][nme], z[nme][m])}", flush=True)
    gedges = swlib.bin_edges(df["Duration"].to_numpy())
    gtok = {r: swlib.tokens_from(s.a["nClicks"], s.a["Duration"], gedges) for r, s in base.items()}
    # all real within-stream transitions u -> v, indexed by the source's global token
    src = {}
    allcodas = [(r, t) for r, s in base.items() for t in range(s.n)]
    for r, s in base.items():
        for t in range(1, s.n):
            src.setdefault(int(gtok[r][t - 1]), []).append((r, t))
    copy_fields = ["nClicks", "Duration"] + swlib.ICI_COLS
    for i in range(i0, i1):
        if i in done:
            continue
        t0 = time.time()
        rng = np.random.default_rng(1000 + i)
        st = {}
        for r, s in base.items():
            c = s.copy()
            cur = int(gtok[r][0])
            for t in range(1, c.n):
                lst = src.get(cur)
                rr, tt = lst[rng.integers(0, len(lst))] if lst else allcodas[rng.integers(0, len(allcodas))]
                for f in copy_fields:
                    c.a[f][t] = base[rr].a[f][tt]
                cur = int(gtok[rr][tt])
            st[r] = c
        b1, bt, bf = [], [], []
        for k in range(5):
            o = seqpipe.run_fold(st, [g for g in range(5) if g != k], [k], sets=("twin", "full"))
            b1.append(seqpipe.bits(o["probs"]["R1"], o["y"]))
            bt.append(seqpipe.bits(o["probs"]["twin"], o["y"]))
            bf.append(seqpipe.bits(o["probs"]["full"], o["y"]))
        g_tw, g_r1 = pooled(bt, bf), pooled(b1, bf)
        fout.write(f"{i},{g_tw!r},{g_r1!r}\n")
        fout.flush()
        print(i, round(g_tw, 5), round(g_r1, 5), f"{time.time() - t0:.1f}s", flush=True)

elif kind == "N3":
    import dompipe
    df, base, vocab, fold_of = dompipe.load(path)
    V = len(vocab)
    dompipe.nll_grad = fast_grad_factory()
    if len(sys.argv) > 6:      # verification: python -I nulls.py N3 csv 0 0 out p3_probs_full.csv
        import pandas as pd
        o = dompipe.run_fold(base, [1, 2, 3, 4], [0], V, sets=("full",))
        fr = pd.read_csv(sys.argv[6])
        fr = fr[fr["fold"] == 0]
        cols = [c for c in fr.columns if c.startswith("p") and c[1:].isdigit()]
        d = float(np.max(np.abs(o["probs"]["full"] - fr[cols].to_numpy())))
        print(f"fast-grad check p3 fold 0 full: max abs prob diff vs frozen CSV = {d:.3e}", flush=True)
    T = np.zeros((V, V))
    for s in base.values():
        x = s["a"]["tok"]
        np.add.at(T, (x[:-1], x[1:]), 1)
    uni = np.bincount(np.concatenate([s["a"]["tok"] for s in base.values()]), minlength=V).astype(float)
    rows = np.where(T.sum(1, keepdims=True) > 0, T / np.maximum(T.sum(1, keepdims=True), 1), uni / uni.sum())
    cdf = np.cumsum(rows, 1)
    for i in range(i0, i1):
        if i in done:
            continue
        t0 = time.time()
        rng = np.random.default_rng(1000 + i)
        st = {}
        for key, s in base.items():
            c = {"fold": s["fold"], "date": s["date"], "n": s["n"], "a": {k: v.copy() for k, v in s["a"].items()}}
            x = c["a"]["tok"]
            for t in range(1, c["n"]):
                x[t] = min(int(np.searchsorted(cdf[x[t - 1]], rng.random(), side="right")), V - 1)
            st[key] = c
        br, bm = [], []
        for k in range(5):
            o = dompipe.run_fold(st, [g for g in range(5) if g != k], [k], V, sets=("full",))
            br.append(dompipe.bits(o["probs"]["bigram"], o["y"]))
            bm.append(dompipe.bits(o["probs"]["full"], o["y"]))
        fout.write(f"{i},{pooled(br, bm)!r}\n")
        fout.flush()
        print(i, round(pooled(br, bm), 5), f"{time.time() - t0:.1f}s", flush=True)
