#!/usr/bin/env python3
"""repolish lens: near-miss continuation (H4/H5). For each (d, N, start file): active-set sequential LP trust-region
polish (code/slp_polish.py, HiGHS, CPU cap), then the penalty threshold descent (bsprec.precise, delta0 1e-10) and
a second SLP round, all from the given start state. Writes OUTDIR/d<d>_N<N>.txt ('%.25e') when the float max drops,
OUTDIR/results_<WID>.jsonl in the same format as repolish_rows.py (so finalize.py picks it up), and a log.
usage: nm_slp.py WID OUTDIR CAP DEADLINE d,N,startfile [d,N,startfile ...]"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bsopt as B
import bsprec as P
import slp_polish as S
RUN = "WORKSPACE/runs/2026-10-16-0758"


def table():
    T = {}
    with open(RUN + "/data/sc/index_parsed.tsv") as fh:
        next(fh)
        for l in fh:
            p = l.rstrip("\n").split("\t")
            T[(int(p[0]), int(p[1]))] = float(p[3])
    return T


def main():
    wid, outdir, cap, DL = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    os.makedirs(outdir, exist_ok=True)
    T = table()
    res = open(os.path.join(outdir, "results_%s.jsonl" % wid), "a")
    for spec in sys.argv[5:]:
        if time.time() > DL - 30:
            break
        ds, Ns, sp = spec.split(",", 2)
        d, N = int(ds), int(Ns)
        X0 = B.normalize(np.array([[float(t) for t in l.replace(",", " ").split()] for l in open(sp) if l.strip()]))
        O = B.CObj(N, d)
        c0 = O.cmax(X0)
        ct = T[(d, N)]
        cpu0 = time.process_time()
        trace = []
        best_X, best_c = X0, c0

        def log(m):
            with open(os.path.join(outdir, "log_%s.txt" % wid), "a") as fh:
                fh.write("d%d N%d %s\n" % (d, N, m))
        for rnd in range(3):
            left = cap - (time.process_time() - cpu0)
            if left < 2 or time.time() > DL - 30:
                break
            Y, info = S.polish(best_X, time_cap=min(left, 0.4 * cap), r0=1e-6, W=2e-3, eps_cap=1e-3, log=log)
            cy = O.cmax(Y)
            log("round %d slp %s cmax_C %.17g" % (rnd, json.dumps(info), cy))
            if cy < best_c:
                best_X, best_c = Y, cy
            trace.append([round(time.process_time() - cpu0, 2), "slp%d" % rnd, best_c])
            left = cap - (time.process_time() - cpu0)
            if left < 2 or time.time() > DL - 30:
                break
            Z, cz, st = P.precise(O, best_X, time_cap=min(left, 0.2 * cap), delta0=1e-10)
            if cz < best_c:
                best_X, best_c = Z, cz
            trace.append([round(time.process_time() - cpu0, 2), "prec%d" % rnd, best_c])
            log("round %d prec steps %d best %.17g gain_tab %.3e" % (rnd, st, best_c, ct - best_c))
            with open(os.path.join(outdir, "progress_%s.json" % wid), "w") as fh:
                json.dump(dict(d=d, N=N, round=rnd, best_c=best_c, gain=ct - best_c,
                               utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())), fh)
        wrote = None
        if best_c < c0 - 1e-16:
            wrote = os.path.join(outdir, "d%d_N%d.txt" % (d, N))
            with open(wrote + ".tmp", "w") as fh:
                for v in best_X:
                    fh.write(",".join("%.25e" % t for t in v) + "\n")
            os.replace(wrote + ".tmp", wrote)
        rec = dict(d=d, N=N, tag="nearmiss", seed=sp, config="SLP+penalty", cap=cap, early=0, floor=None, c0=c0,
                   c_table=ct, out_c=best_c, best_c=best_c, gain_vs_table=ct - best_c,
                   deep_gain_vs_table=ct - best_c, gain_vs_start=c0 - best_c,
                   cpu=round(time.process_time() - cpu0, 2), kicks=0, file=wrote, deep=None, trace=trace,
                   utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        res.write(json.dumps(rec) + "\n"); res.flush()
        print("%s d%d N%d gain_tab %.3e gain_start %.3e cpu %.1f" % (wid, d, N, ct - best_c, c0 - best_c,
                                                                    rec["cpu"]), flush=True)


if __name__ == "__main__":
    main()
