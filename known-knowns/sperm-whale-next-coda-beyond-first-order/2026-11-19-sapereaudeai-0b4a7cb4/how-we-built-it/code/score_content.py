"""FROZEN content scoring (run once, after PREREG.md): all 5 bank folds; R1, the frozen model ('full'), its cut
twin ('twin'), and the pre-registered diagnostics 'rep' (repetition-aware) and 'local' (stream-local bag);
per-position probabilities, folds, bin edges, REC bootstrap, leakage self-test.
Usage: python -I score_content.py <sperm-whale-dialogues.csv> <out_dir>"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "evaluator", "code"))
import leak  # noqa: E402
import seqlib  # noqa: E402
import seqpipe  # noqa: E402
import swlib  # noqa: E402

NAMES = ["R1", "twin", "rep", "local", "full"]
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
df, recs, fold_of = swlib.load_dialogues(sys.argv[1])
streams = swlib.streams_of(df)
with open(os.path.join(out_dir, "folds.csv"), "w", newline="\n") as f:
    f.write("REC,fold\n")
    for r in recs:
        f.write(f"{r},{fold_of[r]}\n")
P = {k: [] for k in NAMES}
Y, REC, POS, FOLD = [], [], [], []
summary = {"folds": {}, "edges": {}}
leakres = {}
t0 = time.time()
for k in range(5):
    tr = [g for g in range(5) if g != k]
    out = seqpipe.run_fold(streams, tr, [k], sets=("twin", "rep", "local", "full"))
    summary["edges"][k] = [repr(float(e)) for e in out["edges"]]
    for n in NAMES:
        p = out["probs"][n]
        assert np.all(p > 0) and np.allclose(p.sum(1), 1.0, atol=1e-12), n
        P[n].append(p)
    Y.append(out["y"])
    REC += [r for r, _ in out["where"]]
    POS += [t for _, t in out["where"]]
    FOLD += [k] * len(out["y"])
    fb = {n: float(seqpipe.bits(out["probs"][n], out["y"]).mean()) for n in NAMES}
    summary["folds"][k] = {"n": int(len(out["y"])), "r1_alpha": out["r1_alpha"], "lam": out["lam"], "bits": fb,
                           "theta": {n: [float(x) for x in th] for n, th in out["theta"].items()}}
    fns = {n: (lambda s, t, n=n, o=out: seqpipe.predict_one(o, n, s, t)) for n in NAMES}
    fns["positive_control_leaky"] = leak.leaky_control
    lr_ = leak.run(streams, out["where"], fns, seed=200 + k)
    dev = 0.0
    for i, (r, t) in enumerate(out["where"]):
        for n in NAMES:
            dev = max(dev, float(np.max(np.abs(seqpipe.predict_one(out, n, streams[r], t) - out["probs"][n][i]))))
    leakres[k] = {"tests": lr_, "single_vs_batch_max_abs": dev}
    print(f"fold {k}: n={len(out['y'])} bits {fb} alpha={out['r1_alpha']} lam={out['lam']} "
          f"leak={lr_} single-vs-batch={dev:.2e} ({time.time() - t0:.0f}s)", flush=True)

P = {n: np.concatenate(v) for n, v in P.items()}
Y = np.concatenate(Y)
REC = np.array(REC)
bits = {n: seqpipe.bits(P[n], Y) for n in NAMES}
for n in ["R1", "twin", "full"]:
    with open(os.path.join(out_dir, f"probs_{n}.csv"), "w", newline="\n") as f:
        f.write("REC,pos,fold,y_token," + ",".join(f"p{j}" for j in range(swlib.V)) + "\n")
        for i in range(len(Y)):
            f.write(f"{REC[i]},{POS[i]},{FOLD[i]},{Y[i]}," + ",".join(repr(float(x)) for x in P[n][i]) + "\n")
np.savez(os.path.join(out_dir, "probs_all.npz"), y=Y, rec=REC.astype(str), pos=np.array(POS), fold=np.array(FOLD),
         **{n: P[n] for n in NAMES})
pooled = {n: float(b.mean()) for n, b in bits.items()}
comp = {}
for a, b in [("R1", "full"), ("twin", "full"), ("rep", "full"), ("local", "full"), ("R1", "twin"), ("twin", "rep"),
             ("twin", "local")]:
    g, lo, hi, _ = swlib.rec_bootstrap(REC, bits[a] - bits[b], n_boot=10000, seed=20261119)
    comp[f"{b}_vs_{a}"] = [g, lo, hi]
pristine = np.isin(np.array(FOLD), [0, 1, 3])
for a, b in [("R1", "full"), ("twin", "full")]:
    g, lo, hi, _ = swlib.rec_bootstrap(REC[pristine], (bits[a] - bits[b])[pristine], n_boot=10000, seed=20261119)
    comp[f"{b}_vs_{a}_pristine_folds_013_diag"] = [g, lo, hi, int(pristine.sum())]
summary["pooled_bits"] = pooled
summary["comparisons"] = comp
g1, g2 = comp["full_vs_R1"], comp["full_vs_twin"]
summary["gates"] = {
    "criterion_cond1_gain_vs_R1_ge_0.10": bool(g1[0] >= 0.10),
    "criterion_cond2_gain_vs_twin_ge_0.05_and_ci_excl_0": bool(g2[0] >= 0.05 and g2[1] > 0),
    "criterion_met": bool(g1[0] >= 0.10 and g2[0] >= 0.05 and g2[1] > 0),
    "p1_gain_vs_R1_ge_0.05_and_ci_excl_0": bool(g1[0] >= 0.05 and g1[1] > 0),
    "p2_gain_vs_twin_ge_0.03_and_ci_excl_0": bool(g2[0] >= 0.03 and g2[1] > 0)}
summary["leakage"] = leakres
json.dump(summary, open(os.path.join(out_dir, "content_summary.json"), "w"), indent=1, default=str)
print("pooled bits", json.dumps(pooled))
print(json.dumps(comp, indent=1))
print("GATES:", summary["gates"])
