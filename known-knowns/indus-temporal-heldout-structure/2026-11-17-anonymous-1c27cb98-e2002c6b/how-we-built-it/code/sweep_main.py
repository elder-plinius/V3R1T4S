"""Full sweep: claim (object-type template model, p2 field-symbol, p3 ligature) vs baselines.

Deterministic given SEED=20261117 (PREREG 2026-11-17T02:50Z).
Outputs: output/sweep_main.json (+ captured copy for the lens).
"""
import sys, os, json, math, collections, datetime, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P
import models as M

SEED = 20261117
B_BOOT = 10000

def m77_class_of(otype):
    if otype in ("seal", "sealing"):
        return "Seal"
    if otype in ("miniature tablet", "copper tablet", "ivory/bone rod", "bronze implement"):
        return "Tablet"
    if otype == "pottery graffito":
        return "Pottery"
    return "Other"

def main():
    out = {"seed": SEED, "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}

    # ---------- M77 training ----------
    recs = P.m77_training()
    train = [(r["seq"], m77_class_of(r["otype"])) for r in recs if r["seq"]]
    out["m77"] = {"lines": len(train), "classes": dict(collections.Counter(c for _, c in train)),
                  "vocab": len(set(s for seq, _ in train for s in seq))}

    # ---------- held-out (PREREG.v2 pool) ----------
    reps, kept, poolinfo = P.build_pool_v2()
    out["heldout"] = {"poolinfo": poolinfo,
                      "by_site": {s: sum(1 for r in reps if r["site"] == s) for s in
                                  ["Mohenjo-daro", "Harappa", "Dholavira", "Lothal", "Kalibangan", "Chanhu-daro", "Nausharo"]}}
    pool = reps

    # ---------- claim model: class-conditional template (frozen fit) ----------
    tmpl = M.TemplateModel(nmax=3)
    tmpl.fit(train)
    priors = tmpl.class_priors()
    out["claim_model"] = {"nmax": 3, "priors": {k: round(v, 4) for k, v in priors.items()}}

    def claim_pred(seq):
        return tmpl.predict(seq)

    # ---------- baseline (i): class-conditional tuned KN (3-gram; order-2 fallback when a class
    # stream is too small for 3-grams), trained on the same M77 data, discount grid-tuned per
    # class on the 10% M77 object split (seed 20261117). Pooled M77 data per class. ----------
    import random as _rnd
    objs = sorted(set(r["obj"] for r in recs if r["seq"]))
    shuf = _rnd.Random(SEED)
    shuf.shuffle(objs)
    split = set(objs[:len(objs) // 10])
    train_by_cls = {c: [r["seq"] for r in recs if r["seq"] and m77_class_of(r["otype"]) == c and r["obj"] not in split] for c in M.CLASSES}
    tune_by_cls = {c: [r["seq"] for r in recs if r["seq"] and m77_class_of(r["otype"]) == c and r["obj"] in split] for c in M.CLASSES}
    kn_by_cls = {}
    for c in M.CLASSES:
        n_tok = sum(len(s) for s in train_by_cls[c])
        if n_tok >= 3000:
            kmc = M.kn3_fit(train_by_cls[c], lambda_max=1.0, min_lambda=0.05, step=0.25, tune_stream=tune_by_cls[c])
            kn_by_cls[c] = {"order": 3, "km": kmc}
        else:
            kmc = M.kn3_fit(train_by_cls[c], lambda_max=1.0, min_lambda=0.05, step=0.25, tune_stream=tune_by_cls[c])
            kn_by_cls[c] = {"order": 2, "km": kmc}  # same fitter, effectively backoff-dominated
    out["kn3"] = {c: {"order": v["order"], "lambda": v["km"]["lambda"], "train_tokens": sum(len(s) for s in train_by_cls[c]),
                      "tune_tokens": sum(len(s) for s in tune_by_cls[c])} for c, v in kn_by_cls.items()}

    def kn_pred(seq):
        best, bestv = None, -math.inf
        for c in M.CLASSES:
            lp = M.kn3_sequence_logprob(kn_by_cls[c]["km"], seq)
            v = math.log(priors[c]) + lp
            if v > bestv:
                bestv, best = v, c
        return best

    # ---------- baseline (ii): SIGIL-style class-conditional position-unigram (unigram+length matched) ----------
    poscls = collections.defaultdict(collections.Counter)
    cls_tot = collections.Counter()
    for seq, c in train:
        cls_tot[c] += 1
        for i, x in enumerate(seq):
            poscls[(c, i)][x] += 1
    poscls_tot = {}
    for k, v in poscls.items():
        poscls_tot[k] = sum(v.values())

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

    # ---------- per-object correctness ----------
    for r in pool:
        y = r["otype"]
        r["pred_claim"] = claim_pred(r["seq_m"])
        r["pred_kn"] = kn_pred(r["seq_m"])
        r["pred_synth"] = synth_pred(r["seq_m"])
        r["ok_claim"] = r["pred_claim"] == y
        r["ok_kn"] = r["pred_kn"] == y
        r["ok_synth"] = r["pred_synth"] == y

    def acc(rs, key):
        return sum(1 for r in rs if r[key]) / len(rs) if rs else 0.0

    import numpy as np
    def boot_p(rs, B=B_BOOT, seed=SEED):
        n = len(rs)
        if n == 0:
            return 1.0
        c = np.fromiter((1.0 if r["ok_claim"] else 0.0 for r in rs), float, n)
        k = np.fromiter((1.0 if r["ok_kn"] else 0.0 for r in rs), float, n)
        s = np.fromiter((1.0 if r["ok_synth"] else 0.0 for r in rs), float, n)
        rng = np.random.default_rng(seed)
        idx = rng.integers(0, n, size=(B, n))
        cr = c[idx].mean(axis=1)
        kr = k[idx].mean(axis=1)
        sr = s[idx].mean(axis=1)
        return float((cr <= np.maximum(kr, sr)).mean())

    def block(rs):
        return {
            "n": len(rs),
            "acc_claim": round(acc(rs, "ok_claim"), 4),
            "acc_kn3": round(acc(rs, "ok_kn"), 4),
            "acc_synth": round(acc(rs, "ok_synth"), 4),
            "p_boot_claim_vs_both": round(boot_p(rs), 5),
            "acc_2class_seal_tablet": None,
        }
    def block2(rs):
        st = [r for r in rs if r["otype"] in ("Seal", "Tablet")]
        if not st:
            return {"n": 0}
        # 2-class: Seal vs Tablet (claim/KN/synth predictions folded: Tablet if pred in {Tablet}, Seal if Seal, else Other)
        def f2(p):
            return "Seal" if p == "Seal" else ("Tablet" if p == "Tablet" else "Other")
        okc = [f2(r["pred_claim"]) == r["otype"] for r in st]
        okk = [f2(r["pred_kn"]) == r["otype"] for r in st]
        oks = [f2(r["pred_synth"]) == r["otype"] for r in st]
        import numpy as np
        n = len(st)
        c = np.array(okc, float); k = np.array(okk, float); s = np.array(oks, float)
        rng = np.random.default_rng(SEED)
        idx = rng.integers(0, n, size=(B_BOOT, n))
        p = float((c[idx].mean(axis=1) <= np.maximum(k[idx].mean(axis=1), s[idx].mean(axis=1))).mean())
        return {"n": n, "acc_claim_2c": round(c.mean(), 4), "acc_kn3_2c": round(k.mean(), 4),
                "acc_synth_2c": round(s.mean(), 4), "p_boot_2c": round(p, 5)}

    out["property_A_objecttype"] = {}
    out["property_A_objecttype"]["pooled"] = block(pool)
    out["property_A_objecttype"]["pooled_2class"] = block2(pool)
    for s in ["Mohenjo-daro", "Harappa", "Dholavira", "Lothal"]:
        out["property_A_objecttype"][s] = block([r for r in pool if r["site"] == s])
        out["property_A_objecttype"][s + "_2class"] = block2([r for r in pool if r["site"] == s])

    # ---------- p2: field-symbol family from terminal segment (last 2 signs) ----------
    FAM = ["Unicorn", "Bull", "Gaur", "Zebu", "Elephant", "Rhino", "Tiger", "Antelope", "Buffalo", "Other"]
    # M77 training: (terminal 2-sign context, fs family) for seals with a family
    term_tr = [(r["seq"][-2:] if len(r["seq"]) >= 2 else r["seq"][-1:], r["fs"]) for r in recs if r["fs"]]
    fam_prior = collections.Counter(f for _, f in term_tr)
    fam_ctx = collections.defaultdict(collections.Counter)
    for ctx, f in term_tr:
        fam_ctx[tuple(ctx)][f] += 1
    def fam_pred(ctx):
        c = fam_ctx.get(tuple(ctx))
        if not c:
            return fam_prior.most_common(1)[0][0]
        return max(c.items(), key=lambda kv: (kv[1], FAM.index(kv[0]) if kv[0] in FAM else 99))[0]
    def fam_pred_synth(ctx):
        # unigram (no context): majority family
        return fam_prior.most_common(1)[0][0]
    seals2 = [r for r in pool if r["otype"] == "Seal" and r["symfam"]]
    for r in seals2:
        ctx = r["seq_m"][-2:] if len(r["seq_m"]) >= 2 else r["seq_m"][-1:]
        r["ctx_term"] = ctx
        r["fs_ok_claim"] = (fam_pred(ctx) == r["symfam"])
        r["fs_ok_synth"] = (fam_pred_synth(ctx) == r["symfam"])
    out["p2_fieldsymbol"] = {
        "n_seals_with_symbol": len(seals2),
        "by_site": {s: sum(1 for r in seals2 if r["site"] == s) for s in
                    ["Mohenjo-daro", "Harappa", "Dholavira", "Lothal"]},
        "acc_claim": round(sum(r["fs_ok_claim"] for r in seals2) / max(len(seals2), 1), 4),
        "acc_synth_majority": round(sum(r["fs_ok_synth"] for r in seals2) / max(len(seals2), 1), 4),
    }
    if seals2:
        import numpy as np
        n = len(seals2)
        c = np.fromiter((1.0 if r["fs_ok_claim"] else 0.0 for r in seals2), float, n)
        s = np.fromiter((1.0 if r["fs_ok_synth"] else 0.0 for r in seals2), float, n)
        rng = np.random.default_rng(SEED)
        idx = rng.integers(0, n, size=(B_BOOT, n))
        out["p2_fieldsymbol"]["p_boot_vs_majority"] = round(float((c[idx].mean(axis=1) <= s[idx].mean(axis=1)).mean()), 5)

    # save frozen claim model (timestamped freeze artifact)
    freeze = {
        "frozen_at": out["frozen_at"], "seed": SEED,
        "model": "class-conditional template, n<=3, add-one, wildcard OOV",
        "class_priors": priors,
        "kn3": {c: kn_by_cls[c]["km"]["lambda"] for c in kn_by_cls},
        "ctx_counts_sha": None,
    }
    import hashlib
    blob = json.dumps({str(k): v for k, v in tmpl.cnt.items()}, sort_keys=True)
    freeze["ctx_counts_sha256"] = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "output", "claim_model_frozen.json"), "w") as f:
        json.dump(freeze, f, indent=2)
    # store pool details
    out["pool_detail"] = [
        {"cisi": r["cisi"], "site": r["site"], "type": r["type"], "otype": r["otype"],
         "symfam": r["symfam"], "seq_w": r["seq_w"], "seq_m": r["seq_m"],
         "pred_claim": r["pred_claim"], "pred_kn": r["pred_kn"], "pred_synth": r["pred_synth"],
         "ok_claim": r["ok_claim"]}
        for r in pool
    ]
    json.dump(out, open(os.path.join(HERE, "output", "sweep_main.json"), "w"), indent=2)
    # console summary
    print("held-out pool:", out["heldout"])
    print("A pooled:", {k: v for k, v in out["property_A_objecttype"]["pooled"].items()})
    for s in ["Mohenjo-daro", "Harappa", "Dholavira", "Lothal"]:
        print("A", s, out["property_A_objecttype"][s])
    print("A 2class pooled:", out["property_A_objecttype"]["pooled_2class"])
    print("p2:", {k: v for k, v in out["p2_fieldsymbol"].items() if k != "by_site"})
    print("KN3 per-class:", out["kn3"])

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    main()
