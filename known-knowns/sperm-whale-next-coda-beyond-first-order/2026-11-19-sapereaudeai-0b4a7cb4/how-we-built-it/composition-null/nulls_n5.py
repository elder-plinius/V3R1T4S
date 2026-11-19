"""Composition-preserving null controls N5 (dialogues) and N6 (Dominica), exactly as PREREG.N5.md declares.

A POST-HOC DIAGNOSTIC, not a gate. See PREREG.N5.md: no result here may tighten a bank threshold or retract a
gate the bank's wording grants. It answers one question - how much of the model's advantage survives when the
order inside each recording is destroyed but that recording's composition is kept.

Each control permutes the coda records within each stream (the whole record moves as a unit), leaving TsTo in
place for N5 so the stream order and timing grid are unchanged, then reruns the frozen pipeline end to end: all
5 folds, all inner cross-validation. Two statistics are appended per control, so the ordered residual is
measured as well as the headline gain.

Usage: python -I nulls_n5.py {N5|N6} <csv> <first> <last_exclusive> <out.csv>

The frozen files are not modified. The speed shims below are copied from nulls.py unchanged and each asserts
bit-identity against the frozen feature code before any control runs.
"""
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
assert kind in ("N5", "N6"), kind
_d = os.path.dirname(os.path.abspath(out_path))


class _Done:
    """Controls already finished by any worker of the same kind; re-read before every control so that several
    workers can share one range without repeating work."""

    def __contains__(self, i):
        for _f in os.listdir(_d):
            if _f.startswith(kind + "_") and _f.endswith(".csv"):
                for l in open(os.path.join(_d, _f)):
                    if l.strip() and int(l.split(",")[0]) == i:
                        return True
        return False


done = _Done()
fout = open(out_path, "a", newline="\n")


def fast_grad_factory():
    """Same objective and gradient as seqlib.nll_and_grad / dompipe.nll_grad, with the expectation term computed
    by einsum instead of a broadcast-and-sum. Copied from nulls.py."""
    from scipy.special import log_softmax

    def g(theta, Fs, ys, lam):
        lp = log_softmax(Fs @ theta, axis=1)
        n = len(ys)
        p = np.exp(lp)
        Ey = np.einsum("nv,nvk->nk", p, Fs)
        grad = -(Fs[np.arange(n), ys] - Ey).mean(0) + 2 * lam * theta
        return -lp[np.arange(n), ys].mean() + lam * theta @ theta, grad
    return g


_WARM = {}


def fast_fit(Fs, ys, lam):
    """Same penalised objective as seqlib.fit / dompipe.fit, same L-BFGS-B call, with a warm start from the
    solution for the same rows at the previous lambda of the grid. Copied from nulls.py."""
    import hashlib

    from scipy.optimize import minimize
    n, V, K = Fs.shape
    F2 = Fs.reshape(n * V, K)
    Fy = Fs[np.arange(n), ys]
    idx = np.arange(n)

    def obj(theta):
        z = (F2 @ theta).reshape(n, V)
        m = z.max(1, keepdims=True)
        e = np.exp(z - m)
        s = e.sum(1, keepdims=True)
        lp_y = z[idx, ys] - m[:, 0] - np.log(s[:, 0])
        Ey = np.matmul((e / s)[:, None, :], Fs)[:, 0, :]
        return -lp_y.mean() + lam * theta @ theta, -(Fy - Ey).mean(0) + 2 * lam * theta

    key = (n, K, hashlib.sha1(ys.tobytes()).hexdigest(), hashlib.sha1(Fy.tobytes()).hexdigest())
    th0 = _WARM.get(key)
    if th0 is None:
        th0 = np.zeros(K)
        th0[0] = 1.0
    x = minimize(obj, th0, jac=True, method="L-BFGS-B", options={"maxiter": 500}).x
    _WARM[key] = x
    return x


def pooled(bits_ref, bits_mod):
    return float((np.concatenate(bits_ref) - np.concatenate(bits_mod)).mean())


if kind == "N5":
    import types

    from scipy.special import ndtr

    import seqlib
    import seqpipe
    df, recs, fold_of = swlib.load_dialogues(path)
    base = swlib.streams_of(df)

    # --- shim 1: ndtr for norm.cdf, checked bit-identical on every real scored position
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

    # --- shim 2: vectorised feats, checked bit-identical on every real scored position
    import fastfeats
    seqlib.norm = real_norm
    ref = [seqlib.feats(swlib.History.of(base[r], t, e0), tb0) for r, t in pos]
    new = [fastfeats.feats(swlib.History.of(base[r], t, e0), tb0) for r, t in pos]
    assert all(np.array_equal(a, b) for a, b in zip(ref, new)), "fastfeats is not bit-identical"
    print(f"fastfeats verified bit-identical on {len(pos)} positions", flush=True)
    del ref, new
    seqlib.feats = fastfeats.feats
    seqlib.nll_and_grad = fast_grad_factory()
    seqlib.fit = fast_fit

    # PREREG.N5: the record moves as a unit; TsTo stays in its slot (permuting it would restore the order)
    PERM_FIELDS = ["nClicks", "Duration", "Whale"] + swlib.ICI_COLS
    assert "TsTo" not in PERM_FIELDS
    for i in range(i0, i1):
        if i in done:
            continue
        t0 = time.time()
        rng = np.random.default_rng(5000 + i)
        _WARM.clear()
        st = {}
        for r, s in base.items():
            c = s.copy()
            perm = rng.permutation(s.n)
            for f in PERM_FIELDS:
                c.a[f] = s.a[f][perm]
            st[r] = c
        bt, bl, bf = [], [], []
        for k in range(5):
            o = seqpipe.run_fold(st, [g for g in range(5) if g != k], [k], sets=("twin", "local", "full"))
            bt.append(seqpipe.bits(o["probs"]["twin"], o["y"]))
            bl.append(seqpipe.bits(o["probs"]["local"], o["y"]))
            bf.append(seqpipe.bits(o["probs"]["full"], o["y"]))
        g_tw, g_lo = pooled(bt, bf), pooled(bl, bf)
        fout.write(f"{i},{g_tw!r},{g_lo!r}\n")
        fout.flush()
        print(i, round(g_tw, 5), round(g_lo, 5), f"{time.time() - t0:.1f}s", flush=True)

elif kind == "N6":
    import dompipe
    df, base, vocab, fold_of = dompipe.load(path)
    V = len(vocab)
    dompipe.nll_grad = fast_grad_factory()
    dompipe.fit = fast_fit
    for i in range(i0, i1):
        if i in done:
            continue
        t0 = time.time()
        rng = np.random.default_rng(5000 + i)
        _WARM.clear()
        st = {}
        for key, s in base.items():
            c = {"fold": s["fold"], "date": s["date"], "n": s["n"], "a": {k: v.copy() for k, v in s["a"].items()}}
            perm = rng.permutation(c["n"])
            for f in list(c["a"]):
                c["a"][f] = s["a"][f][perm]
            st[key] = c
        br, bl, bf = [], [], []
        for k in range(5):
            o = dompipe.run_fold(st, [g for g in range(5) if g != k], [k], V, sets=("local", "full"))
            br.append(dompipe.bits(o["probs"]["bigram"], o["y"]))
            bl.append(dompipe.bits(o["probs"]["local"], o["y"]))
            bf.append(dompipe.bits(o["probs"]["full"], o["y"]))
        g_bg, g_lo = pooled(br, bf), pooled(bl, bf)
        fout.write(f"{i},{g_bg!r},{g_lo!r}\n")
        fout.flush()
        print(i, round(g_bg, 5), round(g_lo, 5), f"{time.time() - t0:.1f}s", flush=True)
