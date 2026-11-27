"""Box reproduction for small k: regenerate the M-X CNF with the run's encoder, solve it with CaDiCaL 3.0.1
writing a DRAT proof, check the proof with drat-trim, and compare both sha256s with the PC send-back list."""
import hashlib, json, os, resource, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "hept"))
from py.sat_compat import build_joint_cnf, board_for_k

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def timed(cmd, log):
    t0 = time.time()
    with open(log, "w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    return round(time.time() - t0, 2), ru.ru_maxrss

ref = dict((p, h) for h, p in (l.split() for l in open(os.path.join(HERE, "SHA256SUMS-files.txt"))))
for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    d = os.path.join(HERE, "small", "k%d" % k); os.makedirs(d, exist_ok=True)
    cnf, meta = build_joint_cnf("M", "X", k, board=board_for_k(k)); cp = os.path.join(d, "problem.cnf"); cnf.write(cp); del cnf
    pp = os.path.join(d, "proof.drat")
    cs, crss = timed([os.path.join(HERE, "hept/bin/cadical"), cp, pp], os.path.join(d, "cadical.log"))
    ds, drss = timed([os.path.join(HERE, "hept/bin/drat-trim"), cp, pp, "-t", "20000"], os.path.join(d, "drat.log"))
    clog = open(os.path.join(d, "cadical.log")).read(); dlog = open(os.path.join(d, "drat.log")).read()
    run = "run_unrestricted" if k <= 8 else "run_k9_20"
    c_sha, p_sha = sha(cp), sha(pp)
    r = {"k": k, "board": "%dx%d" % (meta["nrows"], meta["ncols"]),
         "cadical": "UNSATISFIABLE" if "s UNSATISFIABLE" in clog else ("SATISFIABLE" if "s SATISFIABLE" in clog else "OTHER"),
         "drat_trim": "VERIFIED" if "s VERIFIED" in dlog else "NOT VERIFIED",
         "cnf_bytes": os.path.getsize(cp), "cnf_sha256": c_sha, "cnf_match": c_sha == ref.get("work/%s/M-X/k%d/prove/problem.cnf" % (run, k)),
         "proof_bytes": os.path.getsize(pp), "proof_sha256": p_sha, "proof_match": p_sha == ref.get("work/%s/M-X/k%d/prove/proof.drat" % (run, k)),
         "cadical_s": cs, "drat_trim_s": ds, "max_child_rss_kB_so_far": max(crss, drss)}
    print(json.dumps(r), flush=True)
    os.remove(cp); os.remove(pp)
