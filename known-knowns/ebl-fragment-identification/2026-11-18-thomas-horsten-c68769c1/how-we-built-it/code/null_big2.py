#!/usr/bin/env python3
"""Fast big null (vectorised) for a given (a)-passer list: K line-order-shuffle
controls of the corpus pool, per fragment, seed grid 20261117+k. Saves per-fragment
score arrays (npz) + summary (max, Gumbel fit, p)."""
import json, os, sys, math, time, statistics
import numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search2 import load_corpus, load_population, Aligner, SEED_BASE

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, "output")

def main():
    K = int(sys.argv[1]); fidarg = sys.argv[2]; workers = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    fids = json.load(open(fidarg))
    chaps = load_corpus()
    pool = [l for c in chaps for l in c["toks"]]
    align_f = Aligner()
    align_f.intern([pool])
    line_enc = np.concatenate([align_f.enc([l])[0] for l in pool]).astype(np.int32)
    line_len = np.fromiter((len(l) for l in pool), np.int32, len(pool))
    cum = np.concatenate([[0], np.cumsum(line_len)])[1:]
    pop = load_population()
    popby = {f["fid"]: f for f in pop}
    missing = [f for f in fids if f not in popby]
    fids = [f for f in fids if f in popby]
    align = Aligner()
    align.intern([popby[f]["toks"] for f in fids] + [pool])
    fenc = {f: align.enc(popby[f]["toks"]) for f in fids}
    print(f"pool lines={len(pool)} tokens={line_enc.size} frags={len(fids)} K={K}", file=sys.stderr)

    def one_seed(k):
        rng = np.random.default_rng(SEED_BASE + k)
        order = rng.permutation(len(pool))
        Bb = line_enc[order]
        Bl = np.repeat(order, line_len[order])
        out = []
        for f in fids:
            Aa, Al = fenc[f]
            r = align.align(Aa, Al, Bb, Bl, band=0, min_block=6)
            out.append(r["score"] if r else 0)
        return out
    t0 = time.time()
    cols = [None] * K
    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(one_seed, k) for k in range(K)]
        for k, fu in enumerate(futs):
            cols[k] = fu.result()
            if (k + 1) % 5000 == 0:
                print(f"  {k+1}/{K} ({time.time()-t0:.0f}s)", file=sys.stderr)
    arr = np.array(cols, dtype=np.int32)  # (K, nfrag)
    np.savez(f"{OUT}/null_{K}_{os.path.basename(fidarg)}.npz", arr=arr, fids=np.array(fids))
    out = {}
    for i, f in enumerate(fids):
        s = arr[:, i].tolist()
        m = statistics.fmean(s); sd = statistics.pstdev(s)
        beta = sd / math.sqrt(6); gmu = m - beta * 0.5772156649
        out[f] = {"n_controls": K, "control_max": int(max(s)),
                  "control_p999": sorted(s)[int(0.999 * K)],
                  "gmu": gmu, "gbeta": beta}
    json.dump(out, open(f"{OUT}/null_{K}_{os.path.basename(fidarg)}.json", "w"), indent=1)
    for f in fids:
        print(f"{f}: K={K} max={out[f]['control_max']} p999={out[f]['control_p999']} gmu={out[f]['gmu']:.1f} gbeta={out[f]['gbeta']:.1f}")
    print(f"total {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
