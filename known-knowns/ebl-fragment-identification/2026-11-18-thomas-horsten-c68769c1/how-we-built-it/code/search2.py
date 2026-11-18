#!/usr/bin/env python3
"""Core search for ebl-fragment-identification (frozen PREREG design)."""
import sys, os, json, time, argparse, math, re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import normalise_signs, ngrams
from sw import Aligner

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
IDX_N, RARE_MAX, MIN_HITS, TOPK = 4, 10, 2, 20
MATCH, MISMATCH, GAP, XMATCH, MIN_BLOCK = 3, -1, -2, 1, 6
SEED_BASE = 20261117

def load_corpus():
    d = json.load(open(f"{DATA}/corpus_all_signs.json"))
    chaps = []
    for x in d:
        s = x.get("signs"); s = s[0] if isinstance(s, list) else (s or "")
        cid = "/%s/%s/%s/%s/%s" % (x["textId"]["genre"], int(float(x["textId"]["category"])),
                                   int(float(x["textId"]["index"])), x["stage"], x["name"])
        chaps.append({"cid": cid,
                      "textid": (x["textId"]["genre"], int(float(x["textId"]["category"])),
                                 int(float(x["textId"]["index"]))),
                      "name": x.get("name",""),
                      "signs": s, "toks": normalise_signs(s),
                      "manuscripts": [m.get("museumNumber", {}) for m in (x.get("manuscripts") or [])]})
    return chaps

def load_population():
    d = json.load(open(f"{DATA}/fragments_all_signs.json"))
    pop = []
    for x in d:
        s = x.get("signs"); s = s[0] if isinstance(s, list) else (s or "")
        toks = normalise_signs(s)
        ne = [l for l in toks if l]
        ntok = sum(len(l) for l in toks)
        if len(ne) >= 3 and max((len(l) for l in ne), default=0) >= 15 and ntok <= 800:
            pop.append({"fid": x["_id"], "signs": s, "toks": toks, "ntok": ntok})
    return pop

def build_index(chaps):
    df = defaultdict(int)
    for c in chaps:
        seen = set()
        for line in c["toks"]:
            for g in ngrams(line, IDX_N):
                seen.add(g)
        for g in seen:
            df[g] += 1
    return df

def frag_rare_grams(toks, df):
    gs = set()
    for line in toks:
        for g in ngrams(line, IDX_N):
            if df.get(g, 0) <= RARE_MAX:
                gs.add(g)
    return gs

def chap_rare_gram_sets(chaps, df):
    out = []
    for c in chaps:
        s = set()
        for line in c["toks"]:
            for g in ngrams(line, IDX_N):
                if df.get(g, 0) <= RARE_MAX:
                    s.add(g)
        out.append(s)
    return out

def real_search(pop, chaps, align, chap_enc, df, chap_grams, workers=24):
    def _one(fi):
        f = pop[fi]
        gs = frag_rare_grams(f["toks"], df)
        cand = []
        if gs:
            for ci in range(len(chaps)):
                h = len(gs & chap_grams[ci])
                if h >= MIN_HITS:
                    cand.append((h, ci))
            cand.sort(key=lambda x: (-x[0], x[1]))
            cand = cand[:TOPK]
        Aa, Al = align.enc(f["toks"])
        best = None
        for h, ci in cand:
            r = align.align(Aa, Al, chap_enc[ci][0], chap_enc[ci][1], band=0, min_block=MIN_BLOCK)
            if r and (r["aligned"] >= 15 or r["consec_lines_a"] >= 3) and r["mismatch_frac"] <= 0.10:
                if best is None or r["score"] > best["score"]:
                    r = dict(r); r["chapter"] = ci; r["hitcount"] = h; best = r
        return {"fid": f["fid"], "ntok": f["ntok"], "n_prefilter": len(cand),
                "prefilter_hits": cand[0][0] if cand else 0, "best": best}
    res = [None] * len(pop)
    with ThreadPoolExecutor(workers) as ex:
        for fi, r in zip(range(len(pop)), ex.map(_one, range(len(pop)))):
            res[fi] = r
    return res

def pick_S(res, cap=40):
    passing = [r for r in res if r["best"]]
    passing.sort(key=lambda r: (-r["best"]["hitcount"], -r["prefilter_hits"], r["fid"]))
    return passing[:cap]

def null_seed(fragment, align_f, align, shuffled_pool):
    """One control: align the fragment to the (shuffled) corpus pool (full band)."""
    Bb, Bl = shuffled_pool
    Aa, Al = align_f.enc(fragment["toks"])
    r = align.align(Aa, Al, Bb, Bl, band=0, min_block=MIN_BLOCK)
    return r["score"] if r else 0

def build_shuffled_pool(chaps, align_f, align, seed):
    pool_lines = [l for c in chaps for l in c["toks"]]
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(pool_lines))
    if not hasattr(align, "line_enc"):
        align.line_enc = [align_f.enc([l])[0] for l in pool_lines]
    lens = [len(align.line_enc[i]) for i in order]
    Bb = np.concatenate([align.line_enc[i] for i in order])
    Bl = np.repeat(np.arange(len(order)), lens)
    return Bb, Bl

def run_nulls(S, pop, chaps, align, align_f, K, seed_base=SEED_BASE, workers=24):
    pop_by_fid = {f["fid"]: f for f in pop}
    S_idx = [pop_by_fid[s["fid"]] for s in S]
    align_f.intern([f["toks"] for f in S_idx])
    def _one_seed(k):
        sp = build_shuffled_pool(chaps, align_f, align, seed_base + k)
        return [null_seed(f, align_f, align, sp) for f in S_idx]
    cols = [None] * K
    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(_one_seed, k) for k in range(K)]
        for k, fu in enumerate(futs):
            cols[k] = fu.result()
            if (k + 1) % 50 == 0:
                print(f"  null {k+1}/{K} seeds", file=sys.stderr)
    per_frag = {S[i]["fid"]: [cols[k][i] for k in range(K)] for i in range(len(S))}
    return per_frag

def tfidf_top10(fid, signs, chaps, n_values=(1, 2, 3)):
    def preprocess(signs):
        lines = [l.strip() for l in signs.split("\n")]
        lines = [l for l in lines if not re.fullmatch(r"[X\s]*", l)]
        return (" ".join(lines)).split()
    def ngrams_seq(seq, n):
        return {tuple(seq[i:i+n]) for i in range(max(0, len(seq) - n + 1))}
    def grams_doc(signs):
        toks = preprocess(signs)
        g = set()
        for n in n_values:
            g |= ngrams_seq(toks, n)
        g = {g2 for g2 in g if "X" not in g2}
        return g
    fg = grams_doc(signs)
    doc_grams = [grams_doc(c["signs"]) for c in chaps]
    df = {g: sum(1 for dg in doc_grams if g in dg) for g in fg}
    N = len(chaps) + 1
    idf = {g: math.log(N / (df[g] + 1)) + 1 for g in fg}
    scores = []
    for ci, dg in enumerate(doc_grams):
        sc = sum(idf[g] for g in (fg & dg))
        scores.append((sc, ci))
    scores.sort(key=lambda x: (-x[0], x[1]))
    top10 = [(chaps[ci]["cid"], sc) for sc, ci in scores[:10]]
    return top10, fg

def formula_count(block_seq, chaps, align, align_f, min_len=10):
    block_doc = [tuple(block_seq)]
    align_f.intern([block_doc])
    Aa, Al = align_f.enc(block_doc)
    textids = set(); cids = []
    for ci, c in enumerate(chaps):
        Bb, Bl = align_f.enc(c["toks"])
        r = align.align(Aa, Al, Bb, Bl, band=0, min_block=MIN_BLOCK)
        hit = False
        if r and (r["aligned"] >= 15 or r["consec_lines_b"] >= 3) and r["mismatch_frac"] <= 0.10:
            hit = True
        elif len(block_seq) >= min_len:
            flat = " ".join(" ".join(l) for l in c["toks"])
            bs = " ".join(block_seq)
            if bs in flat:
                hit = True
        if hit:
            textids.add(c["textid"]); cids.append(c["cid"])
    return len(textids), sorted(cids)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["search", "nulls", "all"], default="all")
    ap.add_argument("--k", type=int, default=400)
    ap.add_argument("--s", default=None)
    ap.add_argument("--out", default="output")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()
    chaps = load_corpus()
    pop = load_population()
    print(f"corpus chapters={len(chaps)} population P={len(pop)} ({time.time()-t0:.1f}s)", file=sys.stderr)
    align = Aligner()
    align.intern([c["toks"] for c in chaps] + [f["toks"] for f in pop])  # single consistent vocab
    align_f = align
    chap_enc = [align.enc(c["toks"]) for c in chaps]
    df = build_index(chaps)
    chap_grams = chap_rare_gram_sets(chaps, df)
    if args.mode in ("search", "all"):
        t0 = time.time()
        res = real_search(pop, chaps, align, chap_enc, df, chap_grams, workers=24)
        passing = [r for r in res if r["best"]]
        json.dump({"population": len(pop), "n_passing_b": len(passing),
                   "passing": passing}, open(f"{args.out}/search.json", "w"), indent=1)
        S = pick_S(res)
        json.dump(S, open(f"{args.out}/S.json", "w"), indent=1)
        print(f"real search: {len(pop)} frags, {len(passing)} pass (b) bar; S={len(S)} "
              f"in {time.time()-t0:.1f}s (24 threads)", file=sys.stderr)
    if args.mode in ("nulls", "all"):
        S = json.load(open(args.s or f"{args.out}/S.json"))
        t0 = time.time()
        per_frag = run_nulls(S, pop, chaps, align, align_f, K=args.k, workers=24)
        out = {}
        for fid, scores in per_frag.items():
            out[fid] = {"n_controls": len(scores), "control_max": max(scores),
                        "control_p99": sorted(scores)[int(0.99 * len(scores))] if scores else 0,
                        "scores": sorted(scores)}
        json.dump(out, open(f"{args.out}/null{args.k}.json", "w"), indent=1)
        print(f"nulls {args.k} x {len(S)} frags in {time.time()-t0:.1f}s", file=sys.stderr)
