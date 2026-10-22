#!/usr/bin/env python3
"""repolish lens (run 2026-10-16-0758, wave 2): in-place re-polish of a code, one worker process, CPU-time cap per row.
Derived from attempts/polish/code/polish_rows.py (the wave-1 production pipeline); no web imports.

usage: repolish_rows.py WID ROWS_TSV OUTDIR --deadline EPOCH [--config NAME] [--seed S]
ROWS_TSV: tab separated, header 'd N seed tag early cap floor'
  seed  = path of the start file; tag = class ('ours', 'nmo', ..., 'star');
  early = stop the row once (table - best) >= early (1.5e-6 for 'ours': PREREG condition 6 needs 1e-6);
  cap   = CPU-s for the row; floor = lowest c we want to output (table cosine of (d, N-1) + 1e-11, so the output
          code does not make the table drop row (d, N-1); '' = none). The deepest code is always saved too.

Pipeline (same code path for every row, including the starred sanity-control rows):
  S0 precise penalty-threshold descent first (bsprec.precise / bslist.lprecise for N >= LISTN), delta0 = D0,
     at most PREC0_T CPU-s, stops at table - early;
  S1 LSE beta ladder G_BETAS (C L-BFGS), a stage is kept only if the true all-pairs max drops;
  S2 precise again; S3 kicks (sigma cycle) + K_BETAS ladder + precise until the cap.
Acceptance in the optimiser is the float64 all-pairs max; the checker of record re-checks every written file.
Outputs: OUTDIR/d<d>_N<N>.txt (the lowest-c accepted state with c > floor, if it is below c0),
OUTDIR/deep/d<d>_N<N>.txt (the deepest state, when it differs), results_<WID>.jsonl, progress_<WID>.json.
"""
import io, contextlib, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bsopt as B
import bsprec as P
import bslist as BL
sys.path.insert(0, "WORKSPACE/runs/2026-10-16-0758/code")
import sc_check  # checker of record, read-only library use

RUN = "WORKSPACE/runs/2026-10-16-0758"
LISTN = 400
CONFIGS = {
    # R1: penalty first (delta0 1e-6), ladder, penalty, kicks. For our own unfinished codes.
    "R1": dict(D0=1e-6, PREC0_T=0.45, G_BETAS=[1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=600,
               PREC_T=0.25, K_BETAS=[1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10], K_IT=400,
               K_PREC_T=0.1, SIGMAS=[1e-4, 1e-3, 3e-4, 1e-4, 3e-5]),
    # R2: wave-1 P4-like slow-mover continuation (penalty first, delta0 1e-8, longer stages).
    "R2": dict(D0=1e-8, PREC0_T=0.4, G_BETAS=[3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11], G_IT=1500,
               PREC_T=0.3, K_BETAS=[1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10], K_IT=1000,
               K_PREC_T=0.1, SIGMAS=[1e-5, 3e-5, 1e-4, 3e-6]),
    # R3 (11:52Z): penalty threshold descent only (delta0 1e-6, the whole cap). Reason: in pass 1 every gain on our
    # codes came from the first penalty stage; the LSE ladder and a kick added nothing on (32,196) for 16 CPU-s.
    "R3": dict(D0=1e-6, PREC0_T=1.0, G_BETAS=[], G_IT=0, PREC_T=0.0, K_BETAS=[], K_IT=0, K_PREC_T=0.0, SIGMAS=[],
               KICKS=False),
    # R4 (11:58Z): R3 in two chunks: CHUNK1 CPU-s of penalty descent; abort the row if the gain over the table is
    # still below ABORT_GAIN (in R1/R3 every row that cleared 1.5e-6 did so within 12.3 CPU-s; rows that crawl,
    # e.g. (30,156) 8.1e-9 and (32,207) 8.6e-9 after 21-22 CPU-s, burned the whole cap); else continue to the cap.
    "R4": dict(D0=1e-6, PREC0_T=1.0, G_BETAS=[], G_IT=0, PREC_T=0.0, K_BETAS=[], K_IT=0, K_PREC_T=0.0, SIGMAS=[],
               KICKS=False, CHUNK1=5.0, ABORT_GAIN=1.5e-7),
    # R5 (12:03Z): R4 with delta0 1e-7 and an 8 CPU-s first chunk. Reason: under R4, 7 rows with dense near-max
    # sets ((32,198)-(32,202), (26,175)-(26,178)) were aborted after a single failed penalty call at delta 1e-6
    # (one maxiter-3000 L-BFGS call costs ~5 CPU-s at N ~ 200, d ~ 30).
    "R5": dict(D0=1e-7, PREC0_T=1.0, G_BETAS=[], G_IT=0, PREC_T=0.0, K_BETAS=[], K_IT=0, K_PREC_T=0.0, SIGMAS=[],
               KICKS=False, CHUNK1=8.0, ABORT_GAIN=1e-7),
    # R6 (pass 2): penalty descent only, delta0 1e-7, whole cap, no abort; used to continue rows that moved by
    # >= ~5e-8 in pass 1 from their pass-1 output state.
    "R6": dict(D0=1e-7, PREC0_T=1.0, G_BETAS=[], G_IT=0, PREC_T=0.0, K_BETAS=[], K_IT=0, K_PREC_T=0.0, SIGMAS=[],
               KICKS=False),
    # R7 (near misses, H4): penalty descent only from the wave-1 rejected state, delta0 1e-10, whole cap.
    "R7": dict(D0=1e-10, PREC0_T=1.0, G_BETAS=[], G_IT=0, PREC_T=0.0, K_BETAS=[], K_IT=0, K_PREC_T=0.0, SIGMAS=[],
               KICKS=False),
    # R8 (13:06Z, stalled rows of ours at 3.6e-7 .. 7.3e-7): short penalty, then at most NKICKS small kicks
    # (sigma 1e-6 .. 3e-5, no LSE ladder) each followed by the penalty descent; keep a kick only if the max drops.
    "R8": dict(D0=1e-7, PREC0_T=0.15, G_BETAS=[], G_IT=0, PREC_T=0.0, K_BETAS=[], K_IT=0, K_PREC_T=0.15,
               SIGMAS=[3e-6, 1e-5, 3e-6, 3e-5, 1e-6, 1e-5], NKICKS=6),
}
# PREC0_T, PREC_T, K_PREC_T are fractions of the row cap.


def table():
    T = {}
    with open(RUN + "/data/sc/index_parsed.tsv") as fh:
        next(fh)
        for l in fh:
            p = l.rstrip("\n").split("\t")
            T[(int(p[0]), int(p[1]))] = float(p[3])
    return T


def readcode(p):
    return np.array([[float(t) for t in l.replace(",", " ").split()] for l in open(p) if l.strip()], dtype=np.float64)


def write_code(path, Y):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        for v in Y:
            fh.write(",".join("%.25e" % t for t in v) + "\n")
    os.replace(tmp, path)


def check(path, d, N):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sc_check.main(["sc_check.py", path, str(d), str(N), "--table", RUN + "/data/sc/plain.csv",
                       "--index", RUN + "/data/sc/index_parsed.tsv", "--require-digits", "20"])
    return json.loads(buf.getvalue().strip().splitlines()[-1])


def main():
    a = sys.argv
    wid, rows_tsv, outdir = a[1], a[2], a[3]
    deadline = float(a[a.index("--deadline") + 1])
    cfgname = a[a.index("--config") + 1] if "--config" in a else "R1"
    seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 20261016
    C = CONFIGS[cfgname]
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "deep"), exist_ok=True)
    T = table()
    resf = os.path.join(outdir, "results_%s.jsonl" % wid)
    rows = []
    with open(rows_tsv) as fh:
        hdr = next(fh).rstrip("\n").split("\t")
        for l in fh:
            p = dict(zip(hdr, l.rstrip("\n").split("\t")))
            rows.append((int(p["d"]), int(p["N"]), p["seed"], p.get("tag", ""), float(p["early"]), float(p["cap"]),
                         float(p["floor"]) if p.get("floor") else None))
    res = open(resf, "a")
    for d, N, sp, tag, early, cap, floor in rows:
        if time.time() > deadline - 30:
            break
        lockf = os.path.join(outdir, "lock_d%d_N%d" % (d, N))
        try:
            fd = os.open(lockf, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, wid.encode()); os.close(fd)
        except FileExistsError:
            continue
        rng = np.random.default_rng(seed + 1000 * d + N)
        X0 = B.normalize(readcode(sp))
        assert X0.shape == (N, d), (X0.shape, d, N)
        O = B.CObj(N, d)
        use_list = N >= LISTN
        ct = T.get((d, N), float("nan"))
        cstop = ct - early

        def lse(X, b, it, W=None):
            if use_list:
                return BL.lpolish(O, X, [b], maxiter=it, W=W if W else (2e-3 if b < 1e8 else 5e-4))
            return B.cc_polish(O, X, [b], maxiter=it)

        def prec(Y, tc, d0):
            if use_list:
                return BL.lprecise(O, Y, time_cap=tc, delta0=d0, c_stop=cstop)
            return P.precise(O, Y, time_cap=tc, delta0=d0, c_stop=cstop)

        c0 = O.cmax(X0)
        cpu0, w0 = time.process_time(), time.time()
        best_c, best_X = c0, X0.copy()        # deepest accepted state
        out_c, out_X = c0, X0.copy()          # lowest accepted state with c > floor
        trace = []

        def el():
            return time.process_time() - cpu0

        def out_of_time():
            return el() >= cap or time.time() > deadline - 20

        def stop_row():
            return out_of_time() or best_c <= cstop

        def accept(Z, cz):
            nonlocal best_c, best_X, out_c, out_X
            if cz < best_c:
                best_c, best_X = cz, Z
            if cz < out_c and (floor is None or cz > floor):
                out_c, out_X = cz, Z

        def note(stage):
            trace.append([round(el(), 2), stage, best_c])
            with open(os.path.join(outdir, "progress_%s.json" % wid), "w") as fh:
                json.dump(dict(d=d, N=N, stage=stage, cpu=round(el(), 1), best_c=best_c, c0=c0, ct=ct,
                               utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())), fh)

        aborted = False
        if not stop_row() and C.get("CHUNK1"):
            Z, cz, st = prec(best_X, min(C["CHUNK1"], cap), C["D0"])
            accept(Z, cz); note("prec0a")
            if ct - best_c < C["ABORT_GAIN"]:
                aborted = True; note("abort")
        if not stop_row() and not aborted:
            Z, cz, st = prec(best_X, max(1.0, C["PREC0_T"] * cap - el()), C["D0"] if not C.get("CHUNK1") else 1e-7)
            accept(Z, cz); note("prec0")
        for b in C["G_BETAS"]:
            if stop_row() or aborted:
                break
            Z, cz = lse(best_X, b, C["G_IT"])
            accept(Z, cz); note("g%.0e" % b)
        if not stop_row() and C["PREC_T"] > 0:
            Z, cz, st = prec(best_X, max(1.0, min(C["PREC_T"] * cap, cap - el())), C["D0"])
            accept(Z, cz); note("prec")
        nk = 0
        while C.get("KICKS", True) and not aborted and not stop_row() and nk < C.get("NKICKS", 10**9):
            sig = C["SIGMAS"][nk % len(C["SIGMAS"])]
            nk += 1
            Y = B.normalize(best_X + sig * rng.standard_normal(best_X.shape))
            for b in C["K_BETAS"]:
                if out_of_time():
                    break
                Y, cy = lse(Y, b, C["K_IT"], W=min(0.05, max(2e-3, 6 * sig * np.sqrt(d))) if b <= 1e6 else None)
            cy = O.cmax(Y)
            if not out_of_time():
                Y2, cy2, st = prec(Y, max(1.0, min(C["K_PREC_T"] * cap, cap - el())), C["D0"])
                if cy2 < cy:
                    Y, cy = Y2, cy2
            accept(Y, cy); note("k%d_%.0e" % (nk, sig))
        wrote, chk, deep, chkd = None, None, None, None
        if out_c < c0 - 1e-14:
            wrote = os.path.join(outdir, "d%d_N%d.txt" % (d, N))
            write_code(wrote, out_X)
            if ct - out_c > 3e-10:
                chk = check(wrote, d, N)
                with open(os.path.join(outdir, "checks.jsonl"), "a") as fh:
                    fh.write(json.dumps(chk) + "\n")
        if best_c < out_c - 1e-14:
            deep = os.path.join(outdir, "deep", "d%d_N%d.txt" % (d, N))
            write_code(deep, best_X)
        rec = dict(d=d, N=N, tag=tag, seed=sp, config=cfgname, cap=cap, early=early, floor=floor, c0=c0, c_table=ct,
                   out_c=out_c, best_c=best_c, gain_vs_table=ct - out_c, deep_gain_vs_table=ct - best_c,
                   gain_vs_start=c0 - out_c, cpu=round(el(), 2), wall=round(time.time() - w0, 2), kicks=nk,
                   file=wrote, deep=deep, trace=trace, check=chk, pair_list=use_list,
                   utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        res.write(json.dumps(rec) + "\n"); res.flush()
        print("%s d%d N%d tag %s gain_tab %.3e deep %.3e gain_start %.3e cpu %.1f kicks %d" % (
            wid, d, N, tag, ct - out_c, ct - best_c, c0 - out_c, el(), nk), flush=True)
    res.close()


if __name__ == "__main__":
    main()
