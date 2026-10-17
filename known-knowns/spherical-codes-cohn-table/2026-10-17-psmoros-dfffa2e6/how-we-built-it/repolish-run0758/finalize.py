#!/usr/bin/env python3
"""repolish lens: assemble result/ from worker outputs, run the checker of record, apply PREREG 1-6 + v2 exclusions.

  finalize.py build     for every row of the territory, take the lowest-float-c written file over
                        out/*/results_*.jsonl (tag != star) and out/extra_candidates.tsv (d N file method seed);
                        run RUN/code/sc_check.py (main(), in-process, same argv as the command line) on the exact
                        bytes; apply PREREG.md 1-6 (shape, >= 20 digits, in index and /plain, unstarred, gain >= 1e-9,
                        not taken / not held, no kissing territory, rows we hold need gain >= 1e-6) and PREREG.v2
                        exclusions 9 (dominated by a code we hold for the same d and a larger N: merge pool or our
                        own result, c_other <= c* + 1e-12) and 10 (poly rows). Writes result/d<d>_N<N>.txt,
                        result/rows.tsv, out/near_misses.tsv, out/deletes.tsv, out/rejected.tsv,
                        out/build_check.jsonl.
  finalize.py recheck   literal re-run of the checker of record over every file in result/rows.tsv ->
                        out/final_check.jsonl (+ sha256 and c* agreement with rows.tsv).
"""
import contextlib, csv, glob, hashlib, io, json, os, shutil, sys
import mpmath

RUN = "WORKSPACE/runs/2026-10-16-0758"
L = RUN + "/attempts/repolish"
sys.path.insert(0, RUN + "/code")
import sc_check

TAKEN = {(29, 114), (30, 74), (29, 72), (28, 70), (30, 117), (29, 145), (26, 232), (27, 68)}
mpmath.mp.dps = 50


def index():
    return {(int(r["d"]), int(r["N"])): r for r in csv.DictReader(open(RUN + "/data/sc/index_parsed.tsv"), delimiter="\t")}


def plain_rows():
    s, poly = set(), set()
    for l in open(RUN + "/data/sc/plain.csv"):
        p = l.strip().split(",")
        if len(p) >= 3 and p[0].strip().isdigit():
            s.add((int(p[0]), int(p[1])))
            if len(p) >= 4 and p[3].strip():
                poly.add((int(p[0]), int(p[1])))
    return s, poly


def held():
    h = set()
    f = "WORKSPACE/uploads/hold.txt"
    if os.path.exists(f):
        for l in open(f):
            p = l.split()
            if len(p) >= 2 and p[0].isdigit() and p[1].isdigit():
                h.add((int(p[0]), int(p[1])))
    return h


def territory():
    return {(int(r["d"]), int(r["N"])): r["class"] for r in
            csv.DictReader(open(RUN + "/data/queues2/repolish.tsv"), delimiter="\t")}


def pool():
    P = {}
    for r in csv.DictReader(open(RUN + "/merge/pool/pool.tsv"), delimiter="\t"):
        P[(int(r["d"]), int(r["N"]))] = mpmath.mpf(r["c_star"])
    return P


def method_of(r):
    best_stage, prev = None, r["c0"]
    for t, s, c in r["trace"]:
        if c < prev and c <= r["out_c"] + 1e-18:
            best_stage, prev = s, c
        elif c < prev:
            prev = c
    kind = ("LSE ladder" if best_stage and best_stage.startswith("g") else
            "penalty descent" if best_stage in ("prec", "prec0") else
            ("kick+LSE+penalty (basin hop)" if best_stage else "none"))
    if r["config"] == "R8" and best_stage and best_stage.startswith("k"):
        kind = "small kick + penalty descent (basin hop, no LSE)"
    if r["config"] == "SLP+penalty":
        kind = "active-set SLP" if best_stage and best_stage.startswith("slp") else "penalty descent"
        return "near-miss continuation, code/nm_slp.py (SLP trust region + penalty) cap %g CPU-s; last gain at stage %s (%s)" % (
            r["cap"], best_stage, kind)
    return "in-place re-polish, code/repolish_rows.py %s cap %g CPU-s; output state from stage %s (%s)" % (
        r["config"], r["cap"], best_stage, kind)


def run_check(f, d, N):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sc_check.main(["sc_check.py", f, str(d), str(N), "--table", RUN + "/data/sc/plain.csv",
                       "--index", RUN + "/data/sc/index_parsed.tsv", "--require-digits", "20"])
    j = json.loads(buf.getvalue().strip().splitlines()[-1])
    j["sha256"] = hashlib.sha256(open(f, "rb").read()).hexdigest()
    return j


def collect(Tm):
    cands = {}
    for f in glob.glob(L + "/out/*/results_*.jsonl"):
        for l in open(f):
            r = json.loads(l)
            if r.get("tag") == "star" or not r.get("file"):
                continue
            k = (r["d"], r["N"])
            if k not in Tm or r["c_table"] - r["out_c"] < 1e-10:
                continue
            seed = r["seed"].replace(RUN + "/", "")
            meth = method_of(r)
            if "/attempts/repolish/" in r["seed"]:
                meth = "continued from %s; %s" % (seed.split("attempts/repolish/")[1], meth)
                orig = "data/seeds/%s_d%d_N%d.txt" % ("ours" if Tm.get(k) == "ours" else "posted", k[0], k[1])
                if os.path.exists(RUN + "/" + orig):
                    seed = orig
            fp = r["file"] if os.path.isabs(r["file"]) else os.path.join(L, r["file"])
            c = dict(c=r["out_c"], file=fp, method=meth, seed=seed)
            if k not in cands or c["c"] < cands[k]["c"]:
                cands[k] = c
    ex = L + "/out/extra_candidates.tsv"
    if os.path.exists(ex):
        for r in csv.DictReader(open(ex), delimiter="\t"):
            k = (int(r["d"]), int(r["N"]))
            c = dict(c=float(r["c_float"]), file=r["file"], method=r["method"], seed=r["seed"])
            if k in Tm and (k not in cands or c["c"] < cands[k]["c"]):
                cands[k] = c
    return cands


def check_part(K, M):
    """checker of record on candidate files with index % M == K -> out/build_check_part<K>.jsonl"""
    cands = collect(territory())
    with open(L + "/out/build_check_part%d.jsonl" % K, "w") as fo:
        for i, k in enumerate(sorted(cands)):
            if i % M != K:
                continue
            j = run_check(cands[k]["file"], k[0], k[1])
            fo.write(json.dumps(j) + "\n"); fo.flush()


def build():
    I = index(); Pl, Poly = plain_rows(); H = held(); Tm = territory(); PO = pool()
    cands = collect(Tm)
    cached = {}
    for f in glob.glob(L + "/out/build_check_part*.jsonl"):
        for l in open(f):
            j = json.loads(l); cached[(j["d"], j["N"], j["sha256"])] = j
    os.makedirs(L + "/result", exist_ok=True)
    os.makedirs(L + "/out/rejected", exist_ok=True)
    for p in glob.glob(L + "/result/d*_N*.txt"):
        os.remove(p)
    checks, ok = {}, {}
    rej, near, below = [], [], []
    with open(L + "/out/build_check.jsonl", "w") as fo:
        for k in sorted(cands):
            d, N = k
            c = cands[k]
            if os.environ.get("FIN_TEST") and len(checks) >= 2:
                break
            sha = hashlib.sha256(open(c["file"], "rb").read()).hexdigest()
            j = cached.get((d, N, sha)) or run_check(c["file"], d, N)
            fo.write(json.dumps(j) + "\n"); fo.flush()
            checks[k] = j
            ir = I.get(k)
            why = []
            cs = mpmath.mpf(j["c_star"]) if "c_star" in j else None
            if not j.get("shape_ok"): why.append("shape")
            if not j.get("digits_ok"): why.append("digits")
            if ir is None or k not in Pl: why.append("not in index/plain")
            elif ir["star"] == "1": why.append("starred")
            if k in TAKEN or k in H: why.append("taken/held row")
            if k in Poly or (ir is not None and ir.get("poly") == "1"): why.append("poly row (v2 exclusion 10)")
            if cs is not None and 9 <= d <= 23 and cs <= mpmath.mpf("0.5"): why.append("kissing territory")
            gain = None
            if cs is not None and ir is not None:
                gain = mpmath.mpf(ir["cos"]) - cs
                ours = ("anonymous internet user" in ir["ref"]) or Tm.get(k) == "ours"
                bar = mpmath.mpf("1e-6") if ours else mpmath.mpf("1e-9")
                if gain < bar:
                    if mpmath.mpf("1e-10") <= gain < mpmath.mpf("1e-9"):
                        near.append((d, N, j["c_star"], ir["cos"], mpmath.nstr(gain, 6), Tm.get(k, "?"),
                                     j["sha256"], "1e-10 <= gain < 1e-9"))
                    elif ours and gain >= mpmath.mpf("1e-9"):
                        below.append((d, N, j["c_star"], ir["cos"], mpmath.nstr(gain, 6), "ours", j["sha256"],
                                      "row we hold: gain below the 1e-6 bar (PREREG condition 6)"))
                    why.append("gain %s < bar %s" % (mpmath.nstr(gain, 4), mpmath.nstr(bar, 2)))
            if why:
                rej.append((d, N, "; ".join(why)))
                shutil.copyfile(c["file"], L + "/out/rejected/d%d_N%d.txt" % k)
            else:
                ok[k] = (cs, gain, c, j)
    # v2 exclusion 9 / W2 rule 4: dominance by a code we hold for the same d and a larger N (pool + our results)
    final = {}
    for k in sorted(ok, key=lambda x: (x[0], -x[1])):
        d, N = k
        cs = ok[k][0]
        dom = None
        for (d2, N2), c2 in list(PO.items()) + [(kk, v[0]) for kk, v in final.items()]:
            if d2 == d and N2 > N and c2 <= cs + mpmath.mpf("1e-12"):
                dom = (d2, N2, c2); break
        if dom:
            rej.append((d, N, "dominated by our (%d,%d) c* %s (v2 exclusion 9)" % (dom[0], dom[1], mpmath.nstr(dom[2], 15))))
            shutil.copyfile(ok[k][2]["file"], L + "/out/rejected/d%d_N%d.txt" % k)
            continue
        final[k] = ok[k]
    rows, dels = [], []
    for k in sorted(final):
        d, N = k
        cs, gain, c, j = final[k]
        dst = L + "/result/d%d_N%d.txt" % k
        shutil.copyfile(c["file"], dst)
        sha = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        assert sha == j["sha256"]
        rows.append((d, N, j["c_star"], I[k]["cos"], mpmath.nstr(gain, 12), Tm.get(k, "?"), c["method"], c["seed"], sha))
        for (d2, N2), ir in I.items():
            if d2 == d and N2 < N and mpmath.mpf(ir["cos"]) > cs:
                rescued = (d2, N2) in final and final[(d2, N2)][0] < cs - mpmath.mpf("1e-12")
                dels.append((d, N2, ir["cos"], ir["ref"][:60], "%d,%d" % (d, N), j["c_star"],
                             "kept by our own (%d,%d) result" % (d2, N2) if rescued else "deleted"))
    with open(L + "/result/rows.tsv", "w") as fh:
        fh.write("d\tN\tc_star\ttable_0802Z\tgain\tholder_class\tmethod\tseed\tsha256\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    with open(L + "/out/near_misses.tsv", "w") as fh:
        fh.write("d\tN\tc_star\ttable_0802Z\tgain\tholder_class\tsha256\tnote\n")
        for r in near:
            fh.write("\t".join(str(x) for x in r) + "\n")
    with open(L + "/out/ours_below_bar.tsv", "w") as fh:
        fh.write("d\tN\tc_star\ttable_0802Z\tgain\tholder_class\tsha256\tnote\n")
        for r in below:
            fh.write("\t".join(str(x) for x in r) + "\n")
    with open(L + "/out/deletes.tsv", "w") as fh:
        fh.write("d\tN_below\ttable_0802Z\tref\tour_row\tour_c_star\tstatus\n")
        for r in dels:
            fh.write("\t".join(str(x) for x in r) + "\n")
    with open(L + "/out/rejected.tsv", "w") as fh:
        fh.write("d\tN\twhy\n")
        for r in rej:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print("candidates", len(cands), "rows", len(rows), "near", len(near), "rejected", len(rej),
          "deletes", sum(1 for r in dels if r[-1] == "deleted"))


def recheck(K=0, M=1):
    rows = list(csv.DictReader(open(L + "/result/rows.tsv"), delimiter="\t"))
    with open(L + "/out/final_check_part%d.jsonl" % K, "w") as out:
        for i, r in enumerate(rows):
            if i % M != K:
                continue
            f = L + "/result/d%s_N%s.txt" % (r["d"], r["N"])
            j = run_check(f, int(r["d"]), int(r["N"]))
            j["sha256_matches_rows_tsv"] = j["sha256"] == r["sha256"]
            j["c_star_matches_rows_tsv"] = j["c_star"] == r["c_star"]
            out.write(json.dumps(j) + "\n"); out.flush()
    print("rechecked", len(rows))


def merge():
    rows = list(csv.DictReader(open(L + "/result/rows.tsv"), delimiter="\t"))
    got = {}
    for f in sorted(glob.glob(L + "/out/final_check_part*.jsonl")):
        for l in open(f):
            j = json.loads(l); got[(j["d"], j["N"])] = j
    with open(L + "/out/final_check.jsonl", "w") as out:
        for r in rows:
            out.write(json.dumps(got[(int(r["d"]), int(r["N"]))]) + "\n")
    bad = [k for k, j in got.items() if not (j["sha256_matches_rows_tsv"] and j["c_star_matches_rows_tsv"]
                                              and j["shape_ok"] and j["digits_ok"])]
    print("final_check lines", len(rows), "mismatches", bad)


if __name__ == "__main__":
    a = sys.argv
    if a[1] == "build": build()
    elif a[1] == "check": check_part(int(a[2]), int(a[3]))
    elif a[1] == "recheck": recheck(int(a[2]), int(a[3]))
    elif a[1] == "merge": merge()
