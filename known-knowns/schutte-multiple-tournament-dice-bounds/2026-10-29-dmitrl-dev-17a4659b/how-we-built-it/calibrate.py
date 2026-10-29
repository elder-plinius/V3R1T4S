"""Calibrate encode_schutte.py + CaDiCaL on the starred cells of Figure 7 (arXiv:2604.08790):
SAT at n = f(m,k), UNSAT at n = f(m,k) - 1. SAT models are decoded and re-checked by check_schutte.py."""
import subprocess, time, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encode_schutte as E
from check_schutte import check
CAD = os.environ.get("CADICAL", "cadical")
starred = {(1,1):3, (1,2):7, (2,2):4, (1,3):19, (2,3):6, (3,3):5, (2,4):10, (3,4):7, (4,4):6, (3,5):9, (4,5):8, (5,5):7, (5,6):9}
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 300
os.makedirs("out/calib", exist_ok=True)
rows = []
for (m, k), N in sorted(starred.items(), key=lambda x: (x[1], x[0])):
    for n, expect in ((N, "SAT"), (N - 1, "UNSAT")):
        F = E.build(m, k, n)
        path = f"out/calib/m{m}k{k}n{n}.cnf"
        with open(path, "w") as f:
            f.write(f"p cnf {F.nv} {len(F.clauses)}\n")
            for c in F.clauses: f.write(" ".join(map(str, c)) + " 0\n")
        t0 = time.time()
        r = subprocess.run([CAD, "-q", "-t", str(limit), path], capture_output=True, text=True)
        dt = time.time() - t0
        res = {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"UNKNOWN(rc={r.returncode})")
        verified = ""
        if res == "SAT":
            model = [int(x) for l in r.stdout.splitlines() if l.startswith("v") for x in l.split()[1:]]
            T = E.decode(model, m, n)
            ok, bad, cnt = check(m, k, n, T)
            verified = f"checker {'PASS' if ok else 'FAIL'} ({cnt} subsets)"
        rows.append(dict(m=m, k=k, n=n, expect=expect, result=res, sec=round(dt, 2), verified=verified, vars=F.nv, clauses=len(F.clauses)))
        print(f"m={m} k={k} n={n:2d} expect {expect:5s} got {res:6s} {dt:7.2f}s {verified}", flush=True)
        os.remove(path)
json.dump(rows, open("out/calib/calibration.json", "w"), indent=1)
