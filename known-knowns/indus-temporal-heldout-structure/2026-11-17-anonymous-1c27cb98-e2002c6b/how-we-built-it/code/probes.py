"""H5/H7/H8 probes for the structure lens: prefix truncation (where the class signal lives),
wildcard-excluded scoring (gap-code check), and M77<->held-out nearest-sequence overlap
(re-identification check). Deterministic; outputs output_probes.json.
"""
import sys, os, json, math, collections, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P
import models as M

SEED = 20261117

def m77_class_of(otype):
    if otype in ("seal", "sealing"):
        return "Seal"
    if otype in ("miniature tablet", "copper tablet", "ivory/bone rod", "bronze implement"):
        return "Tablet"
    if otype == "pottery graffito":
        return "Pottery"
    return "Other"

def main():
    out = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    recs = P.m77_training()
    train = [(r["seq"], m77_class_of(r["otype"])) for r in recs if r["seq"]]
    tmpl = M.TemplateModel(3)
    tmpl.fit(train)
    reps, kept, info = P.build_pool_v2()
    pool = reps

    # H5: prefix truncation
    out["H5_prefix_truncation"] = {}
    for K in [1, 2, 3, 4, None]:
        def predK(seq):
            s2 = seq[:K] if K else seq
            if not s2:
                s2 = (seq[0],)
            best, bestv = None, -math.inf
            priors = tmpl.class_priors()
            for c in M.CLASSES:
                v = math.log(priors[c]) + tmpl.score_seq(s2, c)
                if v > bestv:
                    bestv, best = v, c
            return best
        acc = float(np.mean([predK(r["seq_m"]) == r["otype"] for r in pool]))
        out["H5_prefix_truncation"][f"first_{K}" if K else "full"] = round(acc, 4)

    # H7: wildcard-excluded scoring (gap code): score only in-vocab positions
    VOC = set(x for seq, _ in train for x in seq)
    def pred_nooov(seq):
        priors = tmpl.class_priors()
        best, bestv = None, -math.inf
        for c in M.CLASSES:
            s = math.log(priors[c])
            prev1, prev2 = -1, -1
            for x in seq:
                if x in VOC:
                    s += math.log(tmpl._p(c, x, prev1, prev2))
                    prev2, prev1 = prev1, x
            if s > bestv:
                bestv, best = s, c
        return best
    oov_frac = float(np.mean([1.0 - sum(x in VOC for x in r["seq_m"]) / max(len(r["seq_m"]), 1) for r in pool]))
    out["H7_gap_code"] = {
        "acc_wildcard_excluded_pooled": round(float(np.mean([pred_nooov(r["seq_m"]) == r["otype"] for r in pool])), 4),
        "mean_OOV_fraction_heldout": round(oov_frac, 4),
    }

    # H8: re-identification check: how many held-out objects have a 1-edit (or exact) neighbor in the
    # M77 sequence set (beyond the already-dropped exact/identity leaks)? Use a Bloom-like exact +
    # 1-substitution scan over the distinct M77 sequences (bounded: only sequences of similar length).
    m77seqs = [s for s in set(r["seq"] for r in recs if r["seq"])]
    by_len = collections.defaultdict(list)
    for s in m77seqs:
        by_len[len(s)].append(s)
    n_exact = n_1edit = 0
    for r in pool:
        s = r["seq_m"]
        L = len(s)
        cand = set(by_len.get(L, [])) | set(by_len.get(L + 1, [])) | set(by_len.get(L - 1, []))
        exact = s in set(by_len.get(L, []))
        if exact:
            n_exact += 1
            continue
        one = False
        for t in by_len.get(L, []):
            d = sum(1 for a, b in zip(s, t) if a != b)
            if d == 1:
                one = True
                break
        if one:
            n_1edit += 1
    out["H8_reidentification"] = {
        "pool_n": len(pool),
        "exact_M77_seq_match": n_exact,
        "one_edit_M77_seq_match": n_1edit,
        "note": "exact matches should be 0 (dropped at pool build); 1-edit neighbors are recorded, not excluded",
    }

    json.dump(out, open(os.path.join(HERE, "..", "output_probes.json"), "w"), indent=2)
    print(json.dumps(out, indent=2)[:1500])

if __name__ == "__main__":
    main()
