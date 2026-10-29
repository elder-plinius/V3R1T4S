import sys, os, subprocess, time, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encode_alt as A
from check_schutte import check
KIS = os.environ.get("KISSAT", "kissat")
def run(m, k, n, sb="max0", cap=600):
    nv, cls, a = A.encode(m, k, n, sb); p = os.path.join(tempfile.gettempdir(), f"alt_{m}{k}{n}_{sb}.cnf")
    with open(p, "w") as f:
        f.write(f"p cnf {nv} {len(cls)}\n")
        for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time(); r = subprocess.run([KIS, "-q", f"--time={cap}", p], capture_output=True, text=True); os.remove(p)
    res = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "UNKNOWN"); chk = ""
    if res == "SAT":
        val = set(int(x) for l in r.stdout.splitlines() if l.startswith("v") for x in l.split()[1:] if int(x) > 0)
        T = [[[1 if (i != j and a[t, i, j] in val) else 0 for j in range(n)] for i in range(n)] for t in range(m)]
        ok, bad, cnt = check(m, k, n, T); chk = "checker PASS" if ok else f"checker FAIL {bad if isinstance(bad, list) else ''}"[:80]
    return res, round(time.time() - t0, 1), chk
cases = [(1, 2, 7), (1, 2, 6), (2, 3, 6), (2, 3, 5), (2, 4, 10), (2, 4, 9), (3, 5, 9), (3, 5, 8), (2, 5, 14), (3, 6, 13), (2, 5, 12)]
for c in cases:
    print(c, "max0/kissat", run(*c), flush=True)
