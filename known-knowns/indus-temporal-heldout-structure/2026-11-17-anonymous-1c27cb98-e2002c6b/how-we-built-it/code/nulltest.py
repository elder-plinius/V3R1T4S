"""null_test.md numbers: paired bootstrap vs BOTH baselines, B=10000, seed 20261117.

For each of {pooled, Mohenjo-daro, Harappa}: the 10,000-resample distributions of
claim accuracy, KN accuracy, synth accuracy; best_control = max over resamples of
max(KN, synth); real = the claim accuracy on the full (non-resampled) set;
real_beats_all_controls = (real > best_control) AND (real > real_KN_full) AND (real > real_synth_full).
Output: output_nulltest.json  (+ console)
"""
import sys, os, json, math, collections, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P
import models as M

SEED = 20261117
B = 10000

def m77_class_of(otype):
    if otype in ("seal", "sealing"):
        return "Seal"
    if otype in ("miniature tablet", "copper tablet", "ivory/bone rod", "bronze implement"):
        return "Tablet"
    if otype == "pottery graffito":
        return "Pottery"
    return "Other"

def main():
    out = {"seed": SEED, "B": B, "ts": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    recs = P.m77_training()
    train = [(r["seq"], m77_class_of(r["otype"])) for r in recs if r["seq"]]
    tmpl = M.TemplateModel(3)
    tmpl.fit(train)
    priors = tmpl.class_priors()

    import random as _rnd
    objs = sorted(set(r["obj"] for r in recs))
    shuf = _rnd.Random(SEED)
    shuf.shuffle(objs)
    split = set(objs[:len(objs) // 10])
    kn_by_cls = {}
    for c in M.CLASSES:
        tr = [r["seq"] for r in recs if r["seq"] and m77_class_of(r["otype"]) == c and r["obj"] not in split]
        tu = [r["seq"] for r in recs if r["seq"] and m77_class_of(r["otype"]) == c and r["obj"] in split]
        kn_by_cls[c] = M.kn3_fit(tr, lambda_max=1.0, min_lambda=0.05, step=0.25, tune_stream=tu)
    poscls = collections.defaultdict(collections.Counter)
    cls_tot = collections.Counter()
    for seq, c in train:
        cls_tot[c] += 1
        for i, x in enumerate(seq):
            poscls[(c, i)][x] += 1
    poscls_tot = {k: sum(v.values()) for k, v in poscls.items()}

    def kn_pred(seq):
        best, bestv = None, -math.inf
        for c in M.CLASSES:
            lp = M.kn3_sequence_logprob(kn_by_cls[c], seq)
            v = math.log(priors[c]) + lp
            if v > bestv:
                bestv, best = v, c
        return best

    def synth_pred(seq):
        best, bestv = None, -math.inf
        for c in M.CLASSES:
            s = math.log((cls_tot[c] + 1.0) / (sum(cls_tot.values()) + 4.0))
            for i, x in enumerate(seq):
                cnt = poscls[(c, i)]
                tot = poscls_tot.get((c, i), 0)
                s += math.log((cnt.get(x, 0) + 1.0) / (tot + len(cnt) + 1.0))
            if s > bestv:
                bestv, best = s, c
        return best

    reps, kept, info = P.build_pool_v2()
    pool = reps

    def site_block(rs, name):
        n = len(rs)
        c = np.fromiter((1.0 if tmpl.predict(r["seq_m"]) == r["otype"] else 0.0 for r in rs), float, n)
        k = np.fromiter((1.0 if kn_pred(r["seq_m"]) == r["otype"] else 0.0 for r in rs), float, n)
        s = np.fromiter((1.0 if synth_pred(r["seq_m"]) == r["otype"] else 0.0 for r in rs), float, n)
        rng = np.random.default_rng(SEED)
        idx = rng.integers(0, n, size=(B, n))
        cr = c[idx].mean(axis=1)
        kr = k[idx].mean(axis=1)
        sr = s[idx].mean(axis=1)
        best_control = float(np.maximum(kr, sr).max())
        p = float((cr <= np.maximum(kr, sr)).mean())
        return {
            "n": n,
            "real": round(float(c.mean()), 4),
            "real_kn": round(float(k.mean()), 4),
            "real_synth": round(float(s.mean()), 4),
            "best_control": round(best_control, 4),
            "real_beats_all_controls": bool(c.mean() > best_control and c.mean() > k.mean() and c.mean() > s.mean()),
            "p": round(p, 5),
            "real_minus_best_control": round(float(c.mean()) - best_control, 4),
        }

    out["pooled"] = site_block(pool, "pooled")
    out["Mohenjo-daro"] = site_block([r for r in pool if r["site"] == "Mohenjo-daro"], "MD")
    out["Harappa"] = site_block([r for r in pool if r["site"] == "Harappa"], "Harappa")
    json.dump(out, open(os.path.join(HERE, "..", "output_nulltest.json"), "w"), indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
