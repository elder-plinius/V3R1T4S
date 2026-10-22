#!/usr/bin/env python3
"""repolish lens: survey of the 217 territory rows (no optimisation, read-only inputs).
For each row: seed file, c0 (float64 all-pairs), gap profile c0 - G_(k) for k = 2, 10, 100, M/10, M/2, M (M = Maxwell
count N(d-1) - d(d-1)/2 + 1), wave-1 polish history (best float gain vs the 08:02Z table, total CPU-s, row-runs),
table neighbours (N-1, N+1) and the pool code at the same d with the smallest N' > N (dominance).
usage: survey.py > out/survey.tsv"""
import csv, glob, json, os, sys
import numpy as np

RUN = "WORKSPACE/runs/2026-10-16-0758"
T = {}
for r in csv.DictReader(open(RUN + "/data/sc/index_parsed.tsv"), delimiter="\t"):
    T[(int(r["d"]), int(r["N"]))] = float(r["cos"])
pool = {}
pf = RUN + "/merge/pool/pool.tsv"
if os.path.exists(pf):
    for r in csv.DictReader(open(pf), delimiter="\t"):
        try:
            pool[(int(r["d"]), int(r["N"]))] = float(r.get("c_star") or r.get("cstar") or r.get("c"))
        except Exception:
            pass
hist = {}
for f in glob.glob(RUN + "/attempts/polish/out/*/results_*.jsonl"):
    if "/smoke/" in f:
        continue
    for l in open(f):
        r = json.loads(l)
        k = (r["d"], r["N"])
        h = hist.setdefault(k, [-1.0, 0.0, 0])
        h[0] = max(h[0], r["gain_vs_table"]); h[1] += r["cpu"]; h[2] += 1


def readcode(p):
    return np.array([[float(t) for t in l.replace(",", " ").split()] for l in open(p) if l.strip()])


rows = list(csv.DictReader(open(RUN + "/data/queues2/repolish.tsv"), delimiter="\t"))
print("\t".join("d N class seed c0 table gain0 M k1e-9 k1e-7 k1e-6 gap2 gap10 gap100 gapM10 gapM2 gapM "
                "w1_best_gain w1_cpu w1_runs tab_Nm1 tab_Np1 pool_next_N pool_next_c".split()))
for r in rows:
    d, N, cl = int(r["d"]), int(r["N"]), r["class"]
    sp = RUN + "/data/seeds/%s_d%d_N%d.txt" % ("ours" if cl == "ours" else "posted", d, N)
    if not os.path.exists(sp):
        print("%d\t%d\t%s\tMISSING" % (d, N, cl)); continue
    X = readcode(sp)
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    G = X @ X.T
    v = G[np.triu_indices(N, 1)]
    v = -np.sort(-v)
    c0 = v[0]
    M = N * (d - 1) - d * (d - 1) // 2 + 1
    def gap(k):
        k = max(1, min(int(k), len(v)))
        return c0 - v[k - 1]
    nxt = [(n2, pool[(d2, n2)]) for (d2, n2) in pool if d2 == d and n2 > N]
    nxt = min(nxt) if nxt else ("", "")
    h = hist.get((d, N), ["", "", ""])
    print("\t".join(str(x) for x in [d, N, cl, os.path.basename(sp), "%.15f" % c0, "%.12f" % T[(d, N)],
                                       "%.3e" % (T[(d, N)] - c0), M,
                                       int((v >= c0 - 1e-9).sum()), int((v >= c0 - 1e-7).sum()),
                                       int((v >= c0 - 1e-6).sum())] +
                    ["%.2e" % gap(k) for k in (2, 10, 100, M / 10, M / 2, M)] +
                    [("%.3e" % h[0]) if h[0] != "" else "", ("%.1f" % h[1]) if h[1] != "" else "", h[2],
                     "%.12f" % T[(d, N - 1)] if (d, N - 1) in T else "", "%.12f" % T[(d, N + 1)] if (d, N + 1) in T else "",
                     nxt[0], ("%.15f" % nxt[1]) if nxt[1] != "" else ""]))
    sys.stdout.flush()
