"""FROZEN p3 scoring (run once, after PREREG.md) on DominicaCodas.csv: all 5 date folds, smoothed bigram
reference, frozen model ('full'), diagnostics ('one', 'rep', 'local'); per-position probabilities, Date bootstrap,
leakage self-test (every field of the predicted coda and all later codas of its stream altered).
Usage: python -I score_p3.py <DominicaCodas.csv> <out_dir>"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dompipe  # noqa: E402

NAMES = ["bigram", "one", "rep", "local", "full"]
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
df, streams, vocab, fold_of = dompipe.load(sys.argv[1])
V = len(vocab)
with open(os.path.join(out_dir, "p3_folds.csv"), "w", newline="\n") as f:
    f.write("DateRewritten,fold\n")
    for d in sorted(fold_of):
        f.write(f"{d},{fold_of[d]}\n")
with open(os.path.join(out_dir, "p3_vocab.csv"), "w", newline="\n") as f:
    f.write("token,CodaType\n")
    for i, v in enumerate(vocab):
        f.write(f"{i},{v}\n")


def perturbed(s, t, rng):
    c = {"fold": s["fold"], "date": s["date"], "n": s["n"], "a": {k: v.copy() for k, v in s["a"].items()}}
    n = s["n"] - t
    a = c["a"]
    a["tok"][t:] = (s["a"]["tok"][t:] + rng.integers(1, V, n)) % V
    a["IDN"][t:] = np.array([f"{x}#x{j}" for j, x in enumerate(s["a"]["IDN"][t:])], dtype=object)
    a["nClicks"][t:] = s["a"]["nClicks"][t:] + rng.integers(1, 5, n)
    a["Duration"][t:] = s["a"]["Duration"][t:] + rng.uniform(0.01, 1.0, n)
    for k in a:
        assert np.all(a[k][t:] != s["a"][k][t:]), k
    return c


P = {k: [] for k in NAMES}
Y, KEY, POS, FOLD, DATE = [], [], [], [], []
summary, leakres = {"folds": {}}, {}
t0 = time.time()
for k in range(5):
    tr = [g for g in range(5) if g != k]
    out = dompipe.run_fold_full(streams, tr, [k], V)
    for n in NAMES:
        p = out["probs"][n]
        assert np.all(p > 0) and np.allclose(p.sum(1), 1.0, atol=1e-12), n
        P[n].append(p)
    Y.append(out["y"])
    KEY += [f"{key[0]}|{key[1]}" for key, _ in out["where"]]
    DATE += [key[0] for key, _ in out["where"]]
    POS += [t for _, t in out["where"]]
    FOLD += [k] * len(out["y"])
    fb = {n: float(dompipe.bits(out["probs"][n], out["y"]).mean()) for n in NAMES}
    summary["folds"][k] = {"n": int(len(out["y"])), "ref_alpha": out["ref_alpha"], "lam": out["lam"], "bits": fb}
    rng = np.random.default_rng(300 + k)
    nchk, nchg, mx, leaky_flagged, dev = 0, 0, 0.0, 0, 0.0
    for i, (key, t) in enumerate(out["where"]):
        s = streams[key]
        sp = perturbed(s, t, rng)
        for n in NAMES:
            a_ = dompipe.predict_one(out, n, s, t, V)
            b_ = dompipe.predict_one(out, n, sp, t, V)
            nchk += 1
            nchg += int(not np.array_equal(a_, b_))
            mx = max(mx, float(np.max(np.abs(a_ - b_))))
            dev = max(dev, float(np.max(np.abs(a_ - out["probs"][n][i]))))
        leaky_flagged += int(s["a"]["tok"][t] != sp["a"]["tok"][t])   # positive control: a reader of row t sees a change
    leakres[k] = {"checked": nchk, "changed": nchg, "max_abs_diff": mx, "positive_control_flagged": leaky_flagged,
                  "positions": len(out["where"]), "single_vs_batch_max_abs": dev}
    print(f"fold {k}: n={len(out['y'])} bits {fb} alpha={out['ref_alpha']} lam={out['lam']} leak={leakres[k]} "
          f"({time.time() - t0:.0f}s)", flush=True)

P = {n: np.concatenate(v) for n, v in P.items()}
Y = np.concatenate(Y)
DATE = np.array(DATE)
bits = {n: dompipe.bits(P[n], Y) for n in NAMES}
for n in ["bigram", "full"]:
    with open(os.path.join(out_dir, f"p3_probs_{n}.csv"), "w", newline="\n") as f:
        f.write("stream,pos,fold,y_token," + ",".join(f"p{j}" for j in range(V)) + "\n")
        for i in range(len(Y)):
            f.write(f"{KEY[i]},{POS[i]},{FOLD[i]},{Y[i]}," + ",".join(repr(float(x)) for x in P[n][i]) + "\n")
comp = {}
for a, b in [("bigram", "full"), ("bigram", "one"), ("rep", "full"), ("local", "full")]:
    g, lo, hi, _ = dompipe.date_bootstrap(DATE, bits[a] - bits[b], n_boot=10000, seed=20261119)
    comp[f"{b}_vs_{a}"] = [g, lo, hi]
pristine = np.isin(np.array(FOLD), [1, 2, 4])
g, lo, hi, _ = dompipe.date_bootstrap(DATE[pristine], (bits["bigram"] - bits["full"])[pristine], n_boot=10000,
                                      seed=20261119)
comp["full_vs_bigram_pristine_folds_124_diag"] = [g, lo, hi, int(pristine.sum())]
g3 = comp["full_vs_bigram"]
summary["pooled_bits"] = {n: float(b.mean()) for n, b in bits.items()}
summary["n_scored"] = int(len(Y))
summary["comparisons"] = comp
summary["gate_p3"] = {"gain_ge_0.05": bool(g3[0] >= 0.05), "ci_excludes_0": bool(g3[1] > 0),
                      "met": bool(g3[0] >= 0.05 and g3[1] > 0)}
summary["leakage"] = leakres
json.dump(summary, open(os.path.join(out_dir, "p3_summary.json"), "w"), indent=1, default=str)
print("pooled bits", json.dumps(summary["pooled_bits"]))
print(json.dumps(comp, indent=1))
print("GATE p3:", summary["gate_p3"])
