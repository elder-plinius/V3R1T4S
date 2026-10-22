#!/usr/bin/env python3
"""polish lens (run 2026-10-16-0758): in-place deep polish of posted codes, one worker process, CPU-time cap per row.

usage: polish_rows.py WID ROWS_TSV OUTDIR --cap CPU_S --deadline EPOCH [--config NAME] [--seed S]
ROWS_TSV: tab separated, header 'd N seed tag' (seed = path of the start file, tag = class or 'star').

Pipeline (same code path for every row, including the starred sanity-control rows):
  X0 = start file, rows normalised. c0 = float64 max over ALL pairs (C, all pairs: the max is exact up to float64).
  S1 gentle continuation: C L-BFGS on the LogSumExp smooth max over ALL pairs, beta ladder G_BETAS, one call per beta,
     each stage starts from the best-so-far code; a stage is kept only if it lowers the true all-pairs max.
  S2 precise: penalty-threshold descent (bsprec.precise: minimise sum (G_ij - t)_+^2 with t = c - delta, accept if
     the true max drops, adapt delta), PREC_T CPU-s.
  S3 kicks (monotonic basin hopping): best + sigma * gaussian, chained LSE ladder K_BETAS from a low beta, then
     precise; accept if the true max drops. Sigmas cycle through SIGMAS. Repeat until the row's CPU cap.
Every stage end logs (cpu_s, best_c) so yield at any shorter cap can be read off the same run.
Output: OUTDIR/d<d>_N<N>.txt (best code, '%.25e', comma separated) when it is below c0 by > 1e-14 in float64;
OUTDIR/results_<WID>.jsonl one line per finished row; OUTDIR/progress_<WID>.json (checkpoint, rewritten per stage).
Acceptance is never trusted to this program: the checker of record (RUN/code/sc_check.py) re-checks every file.
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bsopt as B
import bsprec as P
import bslist as BL  # pair-list objectives for N >= LISTN (added 09:15Z; rows before that used all pairs)
LISTN = 400
import io, contextlib
sys.path.insert(0, "WORKSPACE/runs/2026-10-16-0758/code")
import sc_check  # checker of record, used read-only as a library (same main() as the command line)

RUN = "WORKSPACE/runs/2026-10-16-0758"

CONFIGS = {
    # P1: production candidate
    "P1": dict(G_BETAS=[1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=600, PREC_T=15.0,
               K_BETAS=[1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10], K_IT=500, K_PREC_T=8.0,
               SIGMAS=[1e-4, 3e-4, 1e-4, 1e-3, 3e-5]),
    # P2: production (chosen 08:40Z from the calibration traces): shorter penalty stages, early stop once the row
    # beats the table by EARLY (the ledger needs 1e-9), so CPU goes to more rows instead of deeper gains.
    "P2": dict(G_BETAS=[1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=600, PREC_T=4.0,
               K_BETAS=[1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10], K_IT=400, K_PREC_T=3.0,
               SIGMAS=[1e-4, 1e-3, 3e-4, 1e-4, 3e-5], EARLY=1e-8),
    # P3 (08:43Z): P2 with EARLY=3e-9 (3x the ledger bar), run with --cap 12: the CPU share is ~10% per worker.
    "P3": dict(G_BETAS=[1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=600, PREC_T=4.0,
               K_BETAS=[1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10], K_IT=400, K_PREC_T=3.0,
               SIGMAS=[1e-4, 1e-3, 3e-4, 1e-4, 3e-5], EARLY=3e-9),
    # P4 (pass 2, slow movers: rows that P3 moved by 1e-12..3e-9): longer stages, same early stop. Start file =
    # the P3 output (best so far), so pass 2 continues pass 1.
    "P4": dict(G_BETAS=[3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=1500, PREC_T=20.0,
               K_BETAS=[1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10], K_IT=1000, K_PREC_T=10.0,
               SIGMAS=[1e-4, 3e-5, 3e-4, 1e-4, 1e-3], EARLY=3e-9),
    # P5 (09:30Z): P3 with the penalty threshold descent FIRST (PREC0_T CPU-s from the posted code). Reason: in the
    # first 33 improved rows the penalty stage made the first gain on 13 of 17 Özgen rows, while the LSE ladder cost
    # 5-12 CPU-s there for nothing (and starved N ~ 300 rows before the penalty stage was reached).
    "P5": dict(G_BETAS=[1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=600, PREC_T=4.0,
               K_BETAS=[1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10], K_IT=400, K_PREC_T=3.0,
               SIGMAS=[1e-4, 1e-3, 3e-4, 1e-4, 3e-5], EARLY=3e-9, PREC_FIRST=20, PREC0_T=5.0,
               PREC_STOP=True),  # PREC_FIRST=20: penalty first only for d >= 20; PREC_STOP: penalty stops at EARLY
}


def table():
    T = {}
    with open(RUN + "/data/sc/index_parsed.tsv") as fh:
        next(fh)
        for l in fh:
            p = l.rstrip("\n").split("\t")
            T[(int(p[0]), int(p[1]))] = float(p[3])
    return T


def readcode(p):
    X = np.array([[float(t) for t in l.replace(",", " ").split()] for l in open(p) if l.strip()], dtype=np.float64)
    return X


def write_code(path, Y):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        for v in Y:
            fh.write(",".join("%.25e" % t for t in v) + "\n")
    os.replace(tmp, path)


def main():
    a = sys.argv
    wid, rows_tsv, outdir = a[1], a[2], a[3]
    cap = float(a[a.index("--cap") + 1])
    deadline = float(a[a.index("--deadline") + 1])
    cfgname = a[a.index("--config") + 1] if "--config" in a else "P1"
    seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 20261016
    C = CONFIGS[cfgname]
    os.makedirs(outdir, exist_ok=True)
    T = table()
    resf = os.path.join(outdir, "results_%s.jsonl" % wid)
    done = set()
    for p in os.listdir(outdir):
        if p.startswith("results_") and p.endswith(".jsonl"):
            for l in open(os.path.join(outdir, p)):
                try:
                    r = json.loads(l); done.add((r["d"], r["N"]))
                except Exception:
                    pass
    rows = []
    with open(rows_tsv) as fh:
        hdr = next(fh).rstrip("\n").split("\t")
        for l in fh:
            p = dict(zip(hdr, l.rstrip("\n").split("\t")))
            rows.append((int(p["d"]), int(p["N"]), p["seed"], p.get("tag", "")))
    res = open(resf, "a")
    for d, N, sp, tag in rows:
        if (d, N) in done:
            continue
        if time.time() > deadline - 30:
            break
        lockf = os.path.join(outdir, "lock_d%d_N%d" % (d, N))  # two workers may share one rows file
        try:
            fd = os.open(lockf, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, wid.encode()); os.close(fd)
        except FileExistsError:
            continue
        rng = np.random.default_rng(seed + 1000 * d + N)
        X0 = B.normalize(readcode(sp))
        assert X0.shape == (N, d), (X0.shape, d, N)
        O = B.CObj(N, d)
        use_list = N >= LISTN

        def lse(X, b, it, W=None):
            if use_list:
                return BL.lpolish(O, X, [b], maxiter=it, W=W if W else (2e-3 if b < 1e8 else 5e-4))
            return B.cc_polish(O, X, [b], maxiter=it)

        ct = T.get((d, N), float("nan"))
        cstop = (ct - C["EARLY"]) if (C.get("EARLY") is not None and C.get("PREC_STOP")) else None

        def prec(Y, tc):
            if use_list:
                return BL.lprecise(O, Y, time_cap=tc, c_stop=cstop)
            return P.precise(O, Y, time_cap=tc, c_stop=cstop)
        c0 = O.cmax(X0)
        ct = T.get((d, N), float("nan"))
        cpu0, w0 = time.process_time(), time.time()
        best_c, best_X = c0, X0.copy()
        trace = []

        def el():
            return time.process_time() - cpu0

        def out_of_time():
            return el() >= cap or time.time() > deadline - 20

        def stop_row():
            return out_of_time() or (C.get("EARLY") is not None and ct - best_c >= C["EARLY"])

        def note(stage):
            trace.append([round(el(), 2), stage, best_c])
            with open(os.path.join(outdir, "progress_%s.json" % wid), "w") as fh:
                json.dump(dict(d=d, N=N, stage=stage, cpu=round(el(), 1), best_c=best_c, c0=c0, ct=ct,
                               utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())), fh)

        # S0 (P5 only) penalty threshold descent straight from the start code
        if C.get("PREC_FIRST") and d >= C["PREC_FIRST"] and not stop_row():
            Z, cz, st = prec(best_X, min(C["PREC0_T"], max(1.0, cap - el())))
            if cz < best_c:
                best_c, best_X = cz, Z
            note("prec0")
        # S1 gentle continuation from the start code
        for b in C["G_BETAS"]:
            if stop_row():
                break
            Z, cz = lse(best_X, b, C["G_IT"])
            if cz < best_c:
                best_c, best_X = cz, Z
            note("g%.0e" % b)
        # S2 precise penalty descent
        if not stop_row():
            Z, cz, st = prec(best_X, min(C["PREC_T"], max(1.0, cap - el())))
            if cz < best_c:
                best_c, best_X = cz, Z
            note("prec")
        # S3 kicks
        nk = 0
        while not stop_row():
            sig = C["SIGMAS"][nk % len(C["SIGMAS"])]
            nk += 1
            Y = B.normalize(best_X + sig * rng.standard_normal(best_X.shape))
            for b in C["K_BETAS"]:
                if out_of_time():
                    break
                Y, cy = lse(Y, b, C["K_IT"], W=min(0.05, max(2e-3, 6 * sig * np.sqrt(d))) if b <= 1e6 else None)
            cy = O.cmax(Y)
            if not out_of_time():
                Y2, cy2, st = prec(Y, min(C["K_PREC_T"], max(1.0, cap - el())))
                if cy2 < cy:
                    Y, cy = Y2, cy2
            if cy < best_c:
                best_c, best_X = cy, Y
            note("k%d_%.0e" % (nk, sig))
        wrote = None
        if best_c < c0 - 1e-14:
            wrote = os.path.join(outdir, "d%d_N%d.txt" % (d, N))
            write_code(wrote, best_X)
        chk = None
        if wrote and ct - best_c > 3e-10:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                sc_check.main(["sc_check.py", wrote, str(d), str(N), "--table", RUN + "/data/sc/plain.csv",
                               "--index", RUN + "/data/sc/index_parsed.tsv", "--require-digits", "20"])
            chk = json.loads(buf.getvalue().strip().splitlines()[-1])
            with open(os.path.join(outdir, "checks.jsonl"), "a") as fh:
                fh.write(json.dumps(chk) + "\n")
        rec = dict(d=d, N=N, tag=tag, seed=sp, config=cfgname, cap=cap, c0=c0, c_table=ct, best_c=best_c,
                   gain_vs_table=ct - best_c, gain_vs_start=c0 - best_c, cpu=round(el(), 2),
                   wall=round(time.time() - w0, 2), kicks=nk, file=wrote, trace=trace, check=chk, pair_list=use_list,
                   utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        res.write(json.dumps(rec) + "\n"); res.flush()
        print("%s d%d N%d tag %s gain_tab %.3e gain_start %.3e cpu %.1f kicks %d" % (
            wid, d, N, tag, ct - best_c, c0 - best_c, el(), nk), flush=True)
    res.close()


if __name__ == "__main__":
    main()
