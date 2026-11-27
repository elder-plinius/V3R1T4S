"""Regenerate M-X joint CNFs with the run's own encoder and compare sha256 to the PC send-back."""
import hashlib, sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hept"))
from py.sat_compat import build_joint_cnf, board_for_k
ref = {}
for line in open(sys.argv[1]):
    h, p = line.split()
    ref[p] = h
kmin, kmax = int(sys.argv[2]), int(sys.argv[3])
out = []
for k in range(kmin, kmax + 1):
    t0 = time.time()
    cnf, meta = build_joint_cnf("M", "X", k, board=board_for_k(k))
    path = "cnf_tmp_k%d.cnf" % k
    cnf.write(path)
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    sz = os.path.getsize(path)
    run = "run_unrestricted" if k <= 8 else "run_k9_20"
    key = "work/%s/M-X/k%d/prove/problem.cnf" % (run, k)
    r = {"k": k, "board": "%dx%d" % (meta["nrows"], meta["ncols"]), "nP": len(meta["P"]), "nQ": len(meta["Q"]),
         "nvars": cnf.nvars, "nclauses": len(cnf.clauses), "bytes": sz, "sha256": h, "ref": ref.get(key), "match": h == ref.get(key),
         "sec": round(time.time() - t0, 1)}
    print(json.dumps(r), flush=True)
    if k > 8 or "--keep" not in sys.argv:
        os.remove(path)
