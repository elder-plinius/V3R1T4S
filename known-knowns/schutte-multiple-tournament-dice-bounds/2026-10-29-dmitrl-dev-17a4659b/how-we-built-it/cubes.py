"""Run the maximum-out-degree cube split of encode_schutte.py (--sb maxdeg --D d, d = k..n-1) under a solver.
Each cube is sound by the docstring argument in encode_schutte.py; all cubes UNSAT => no S_k m-set of order n.
Usage: cubes.py m k n seconds solver(cadical|kissat) [D-list] ; appends JSON lines to out/cubes.jsonl (solver binaries from $CADICAL / $KISSAT, default: on PATH)"""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encode_schutte as E
from check_schutte import check
m, k, n, secs, solver = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
Ds = [int(x) for x in sys.argv[6].split(",")] if len(sys.argv) > 6 else list(range(k, n))
BIN = {"cadical": os.environ.get("CADICAL", "cadical"), "kissat": os.environ.get("KISSAT", "kissat")}[solver]
os.makedirs("out", exist_ok=True); os.makedirs("out/cnf", exist_ok=True)
for D in Ds:
    F = E.build(m, k, n, "maxdeg", D)
    path = f"out/cnf/m{m}k{k}n{n}_D{D}.cnf"
    with open(path, "w") as f:
        f.write(f"c schutte m={m} k={k} n={n} sb=maxdeg D={D}\np cnf {F.nv} {len(F.clauses)}\n")
        for c in F.clauses: f.write(" ".join(map(str, c)) + " 0\n")
    args = [BIN, "-q", "-t", str(secs), path] if solver == "cadical" else [BIN, "-q", f"--time={secs}", path]
    t0 = time.time(); r = subprocess.run(args, capture_output=True, text=True); dt = time.time() - t0
    res = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "UNKNOWN")
    rec = dict(m=m, k=k, n=n, D=D, solver=solver, cap=secs, result=res, sec=round(dt, 1), vars=F.nv, clauses=len(F.clauses),
               utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    if res == "SAT":
        model = [int(x) for l in r.stdout.splitlines() if l.startswith("v") for x in l.split()[1:]]
        T = E.decode(model, m, n); ok, bad, cnt = check(m, k, n, T)
        rec["checker"] = "PASS" if ok else f"FAIL {len(bad)}"
        out = f"out/SAT_m{m}k{k}n{n}_D{D}.json"
        json.dump({"m": m, "k": k, "n": n, "tournaments": [["".join(map(str, row)) for row in A] for A in T]}, open(out, "w"))
        rec["object"] = out
    if res != "UNKNOWN": os.remove(path)
    print(json.dumps(rec), flush=True)
    open("out/cubes.jsonl", "a").write(json.dumps(rec) + "\n")
    if res == "SAT": break
