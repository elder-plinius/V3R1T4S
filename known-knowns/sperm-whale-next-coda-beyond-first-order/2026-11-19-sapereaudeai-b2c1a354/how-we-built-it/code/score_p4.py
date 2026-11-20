"""FROZEN p4 scoring (run once, after PREREG.md): all 5 bank folds, reference + frozen LR model + the
pre-registered 'pattern' diagnostic, per-position probabilities, REC bootstrap, leakage self-test.
Usage: python -I score_p4.py <sperm-whale-dialogues.csv> <out_dir>"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "evaluator", "code"))
import leak  # noqa: E402
import p4lib  # noqa: E402
import swlib  # noqa: E402

out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
df, recs, fold_of = swlib.load_dialogues(sys.argv[1])
streams = swlib.streams_of(df)
rows, summary, leakres = [], {"folds": {}}, {}
t0 = time.time()
for k in range(5):
    tr = [g for g in range(5) if g != k]
    fit = p4lib.fit_fold(streams, tr, [k], p4lib.FEATURE_SETS["full"])
    pat = p4lib.fit_fold(streams, tr, [k], p4lib.FEATURE_SETS["pattern"])
    assert fit["where"] == pat["where"]
    b_ref = p4lib._bits(fit["y"], fit["p_ref"])
    b_mod = p4lib._bits(fit["y"], fit["p"])
    b_pat = p4lib._bits(fit["y"], pat["p"])
    summary["folds"][k] = {"n": int(len(b_ref)), "ref_alpha": fit["ref_alpha"], "C": fit["C"], "C_pattern": pat["C"],
                           "ref_bits": float(b_ref.mean()), "model_bits": float(b_mod.mean()),
                           "pattern_bits": float(b_pat.mean()), "gain": float((b_ref - b_mod).mean()),
                           "P_ref_same_given_prev_switch_same": [float(fit["P_ref"][0, 1]), float(fit["P_ref"][1, 1])]}
    for i, (r, t) in enumerate(fit["where"]):
        rows.append((r, t, k, int(fit["y"][i]), repr(float(fit["p_ref"][i])), repr(float(fit["p"][i])),
                     repr(float(pat["p"][i]))))
    # leakage self-test on every held-out scored position of this fold
    single = lambda s, t, F=fit: np.array(p4lib.predict_one(F, s, t))  # noqa: E731
    lr_ = leak.run(streams, fit["where"], {"model_and_ref": single, "positive_control_leaky": leak.leaky_control},
                   seed=100 + k)
    # consistency of the single-position path with the batch predictions
    dev = max(abs(p4lib.predict_one(fit, streams[r], t)[0] - fit["p"][i]) for i, (r, t) in enumerate(fit["where"]))
    leakres[k] = {"tests": lr_, "single_vs_batch_max_abs": float(dev)}
    print(f"fold {k}: n={len(b_ref)} ref {b_ref.mean():.4f} model {b_mod.mean():.4f} pattern {b_pat.mean():.4f} "
          f"C={fit['C']} alpha={fit['ref_alpha']} leak={lr_} single-vs-batch={dev:.2e} ({time.time() - t0:.0f}s)")

with open(os.path.join(out_dir, "p4_per_position.csv"), "w", newline="\n") as f:
    f.write("REC,pos,fold,y_same,p_same_ref,p_same_model,p_same_pattern\n")
    for r in rows:
        f.write(",".join(str(x) for x in r) + "\n")
rec = np.array([r[0] for r in rows])
y = np.array([r[3] for r in rows])
pr, pm, pp = (np.array([float(r[i]) for r in rows]) for i in (4, 5, 6))
b_ref, b_mod, b_pat = p4lib._bits(y, pr), p4lib._bits(y, pm), p4lib._bits(y, pp)
g, lo, hi, _ = swlib.rec_bootstrap(rec, b_ref - b_mod, n_boot=10000, seed=20261119)
gp, lop, hip, _ = swlib.rec_bootstrap(rec, b_ref - b_pat, n_boot=10000, seed=20261119)
nlab = {r: len(np.unique(streams[r].a["Whale"])) for r in streams}
multi = np.array([nlab[r] >= 2 for r in rec])
gm, lom, him, _ = swlib.rec_bootstrap(rec[multi], (b_ref - b_mod)[multi], n_boot=10000, seed=20261119)
pristine = np.isin([fold_of[r] for r in rec], [0, 1, 3])
gq, loq, hiq, _ = swlib.rec_bootstrap(rec[pristine], (b_ref - b_mod)[pristine], n_boot=10000, seed=20261119)
summary["pooled"] = {"n": int(len(y)), "same_rate": float(y.mean()), "ref_bits": float(b_ref.mean()),
                     "model_bits": float(b_mod.mean()), "pattern_bits": float(b_pat.mean()),
                     "gain_model": [g, lo, hi], "gain_pattern_diag": [gp, lop, hip],
                     "gain_model_multi_label_recs_diag": [gm, lom, him, int(multi.sum())],
                     "gain_model_single_label_recs_diag_mean": float((b_ref - b_mod)[~multi].mean()),
                     "n_single_label_positions": int((~multi).sum()),
                     "gain_model_pristine_folds_013_diag": [gq, loq, hiq, int(pristine.sum())]}
summary["gate_p4"] = {"gain_ge_0.05": bool(g >= 0.05), "ci_excludes_0": bool(lo > 0), "met": bool(g >= 0.05 and lo > 0)}
summary["leakage"] = leakres
json.dump(summary, open(os.path.join(out_dir, "p4_summary.json"), "w"), indent=1, default=str)
print(json.dumps(summary["pooled"], indent=1))
print("GATE p4:", summary["gate_p4"])
