"""Leakage self-test helpers: alter every field of the predicted coda AND of every later coda of its stream
(in a copy, stream order kept fixed), recompute the prediction at that position through the normal code path,
and require bit-identical output. Positive control: a deliberately leaky predictor that reads row t must fail."""
import numpy as np

import swlib


def perturbed_copy(stream, t, rng):
    s = stream.copy()
    n = s.n - t
    a = s.a
    x = rng.integers(1, 30, n)
    a["nClicks"][t:] = np.where(x == stream.a["nClicks"][t:], x % 29 + 1, x)
    a["Duration"][t:] = rng.uniform(0.0, 3.0, n)
    for c in swlib.ICI_COLS:
        a[c][t:] = rng.uniform(0.0, 0.5, n)
    a["Whale"][t:] = (stream.a["Whale"][t:] + rng.integers(1, 11, n) - 1) % 12 + 1
    a["Whale"][t:] = np.where(a["Whale"][t:] == stream.a["Whale"][t:], a["Whale"][t:] % 12 + 1, a["Whale"][t:])
    a["TsTo"][t:] = stream.a["TsTo"][t:] + rng.normal(0.0, 50.0, n)
    for k in swlib.FIELDS:      # make sure every field really changed
        assert np.all(a[k][t:] != stream.a[k][t:]) or k.startswith("ICI"), k
    return s


def run(streams, positions, predict_fns, seed=7):
    """positions: list of (rec, t). predict_fns: {name: f(stream, t) -> np.ndarray or float}.
    Returns {name: (n_checked, n_changed, max_abs_diff)}."""
    rng = np.random.default_rng(seed)
    res = {k: [0, 0, 0.0] for k in predict_fns}
    for r, t in positions:
        s = streams[r]
        sp = perturbed_copy(s, t, rng)
        for k, f in predict_fns.items():
            a = np.atleast_1d(np.asarray(f(s, t), dtype=float))
            b = np.atleast_1d(np.asarray(f(sp, t), dtype=float))
            d = float(np.max(np.abs(a - b)))
            res[k][0] += 1
            res[k][1] += int(not np.array_equal(a, b))
            res[k][2] = max(res[k][2], d)
    return {k: tuple(v) for k, v in res.items()}


def leaky_control(stream, t):
    """Deliberately leaky: reads the predicted coda's own click count. The test must flag it."""
    return np.array([float(stream.a["nClicks"][t])])
