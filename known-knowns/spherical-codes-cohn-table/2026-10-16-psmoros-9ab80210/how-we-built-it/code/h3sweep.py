#!/usr/bin/env python3
"""brute-scale lens, H3 sweep: neighbour codes as starts.
For a candidate (d, N, k): k > 0 -> posted (d, N+k) code minus k points (T removal choices: random, max contact
degree, random cap); k < 0 -> posted (d, N+k) code (N+k < N) plus |k| points in its deepest holes.
Each start: LSE polish (same BF schedule as mbh.py); the best start gets the FINE LSE polish, and if it lands
within 1e-6 above the table (or below it) also the precise penalty polish. Compared with c_table (plain.csv).
usage: h3sweep.py WID CANDS_FILE STOP_EPOCH [--cap SECONDS] [--tries T]
CANDS_FILE: lines "d N k" (extra columns ignored).
"""
import csv, json, os, sys, time
import numpy as np
sys.path.insert(0, "WORKDIR/runs/2026-10-16-0024/attempts/brute-scale/code")
import bsopt as B
import bsprec as P
from mbh import load_posted, write_code, LENS

BF = [1e4, 1e5, 1e6]
FINE = [3e6, 1e7, 3e7, 1e8]
PLAIN = "WORKDIR/runs/2026-10-16-0024/data/sc/plain.csv"


def table():
    T = {}
    for row in csv.reader(open(PLAIN)):
        if len(row) >= 3:
            try:
                T[(int(row[0]), int(row[1]))] = float(row[2])
            except ValueError:
                pass
    return T


def starts(X1, N, k, rng, T):
    M, d = X1.shape
    G = X1 @ X1.T
    np.fill_diagonal(G, -3.0)
    cm = G.max()
    deg = (G > cm - 1e-6).sum(axis=1)
    for t in range(T):
        if k > 0:
            if t % 3 == 0:
                rem = rng.choice(M, k, replace=False)
            elif t % 3 == 1:
                p = (deg + 0.5) ** 2; p = p / p.sum()
                rem = rng.choice(M, k, replace=False, p=p)
            else:
                u = B.normalize(rng.normal(size=(1, d)))[0]
                rem = np.argsort(-(X1 @ u))[:k]
            yield np.delete(X1, rem, axis=0)
        else:
            H = B.deep_holes(X1, -k, rng)
            if len(H) < -k:
                H = np.vstack([H, B.normalize(rng.normal(size=(-k - len(H), d)))])
            yield np.vstack([X1, H])


def main():
    wid = sys.argv[1]
    cands = [l.split() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]
    stop_at = float(sys.argv[3])
    cap = float(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 120.0
    T = int(sys.argv[sys.argv.index("--tries") + 1]) if "--tries" in sys.argv else 9
    FIT = int(sys.argv[sys.argv.index("--fine-it") + 1]) if "--fine-it" in sys.argv else 3000
    rng = np.random.default_rng(int(wid.encode().hex(), 16) % 100000)
    Tab = table()
    res = open(os.path.join(LENS, "out", "w%s_results.jsonl" % wid), "a")
    done = set()
    for c in cands:
        if time.time() > stop_at - 30: break
        d, N, k = int(c[0]), int(c[1]), int(c[2])
        if (d, N, k) in done or (d, N) not in Tab: continue
        done.add((d, N, k))
        t0 = time.time()
        try:
            X1 = load_posted(d, N + k)
        except Exception as e:
            res.write(json.dumps({"worker": wid, "d": d, "N": N, "k": k, "error": repr(e)}) + "\n"); res.flush(); continue
        O = B.CObj(N, d)
        ct = Tab[(d, N)]
        best = (9.0, None); n = 0
        for Y in starts(X1, N, k, rng, T):
            if time.time() - t0 > cap or time.time() > stop_at - 20: break
            Z, s = B.cc_polish(O, Y, BF, maxiter=400)
            n += 1
            if s < best[0]: best = (s, Z)
        out = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "worker": wid, "d": d, "N": N, "k": k,
               "tag": "h3sweep", "method": "neighbour (N%+d) start + LSE polish" % k, "tries": n, "c_table": ct,
               "best_s": best[0]}
        if best[1] is not None:
            Zf, cf = B.cc_polish(O, best[1], FINE, maxiter=FIT)
            out["fine_c"] = cf
            if cf < ct + 1e-6:
                Zp, cp, st = P.precise(O, Zf, time_cap=40.0)
                out["precise_c"] = cp
                if cp < cf: Zf, cf = Zp, cp
            out["best_c"] = cf
            out["gain_vs_table"] = ct - cf
            if cf < ct - 1e-10:
                write_code(os.path.join(LENS, "out", "best", "d%d_N%d_h3_%s.txt" % (d, N, wid)), Zf)
                out["event"] = "new_best"
        out["elapsed"] = round(time.time() - t0, 1)
        res.write(json.dumps(out) + "\n"); res.flush()
    res.close()


if __name__ == "__main__":
    main()
