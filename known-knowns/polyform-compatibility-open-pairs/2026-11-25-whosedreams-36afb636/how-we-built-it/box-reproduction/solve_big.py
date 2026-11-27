"""Like solve_small.py, but the CNF is written by a separate short-lived Python process so its memory is
released before CaDiCaL and drat-trim run (keeps the packaging machine's peak RAM low for k = 13..20)."""
import hashlib, json, os, resource, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
GEN = ("import sys,os; sys.path.insert(0, %r); from py.sat_compat import build_joint_cnf, board_for_k; "
       "k=int(sys.argv[1]); c,m=build_joint_cnf('M','X',k,board=board_for_k(k)); c.write(sys.argv[2]); "
       "print('%%dx%%d' %% (m['nrows'], m['ncols']))") % os.path.join(HERE, "hept")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
def timed(cmd, log):
    t0 = time.time()
    with open(log, "w") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
        _, st, ru = os.wait4(p.pid, 0)
    return round(time.time() - t0, 2), ru.ru_maxrss
ref = dict((p, h) for h, p in (l.split() for l in open(os.path.join(HERE, "SHA256SUMS-files.txt"))))
for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    d = os.path.join(HERE, "small", "k%d" % k); os.makedirs(d, exist_ok=True)
    cp, pp = os.path.join(d, "problem.cnf"), os.path.join(d, "proof.drat")
    gs, grss = timed([sys.executable, "-c", GEN, str(k), cp], os.path.join(d, "gen.log"))
    board = open(os.path.join(d, "gen.log")).read().strip()
    cs, crss = timed([os.path.join(HERE, "hept/bin/cadical"), cp, pp], os.path.join(d, "cadical.log"))
    ds, drss = timed([os.path.join(HERE, "hept/bin/drat-trim"), cp, pp, "-t", "20000"], os.path.join(d, "drat.log"))
    clog = open(os.path.join(d, "cadical.log")).read(); dlog = open(os.path.join(d, "drat.log")).read()
    run = "run_unrestricted" if k <= 8 else "run_k9_20"
    c_sha, p_sha = sha(cp), sha(pp)
    print(json.dumps({"k": k, "board": board,
        "cadical": "UNSATISFIABLE" if "s UNSATISFIABLE" in clog else ("SATISFIABLE" if "s SATISFIABLE" in clog else "OTHER"),
        "drat_trim": "VERIFIED" if "s VERIFIED" in dlog else "NOT VERIFIED",
        "cnf_bytes": os.path.getsize(cp), "cnf_sha256": c_sha, "cnf_match": c_sha == ref.get("work/%s/M-X/k%d/prove/problem.cnf" % (run, k)),
        "proof_bytes": os.path.getsize(pp), "proof_sha256": p_sha, "proof_match": p_sha == ref.get("work/%s/M-X/k%d/prove/proof.drat" % (run, k)),
        "gen_s": gs, "cadical_s": cs, "drat_trim_s": ds, "gen_maxrss_kB": grss, "cadical_maxrss_kB": crss, "drat_trim_maxrss_kB": drss}), flush=True)
    os.remove(cp); os.remove(pp)
