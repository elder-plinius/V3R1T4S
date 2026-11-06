import sys, os, subprocess, time, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encode_schutte as E
from check_schutte import check
CAD = os.environ.get("CADICAL", "cadical")
def solve(m, k, n, sb, cap=600, extra=()):
    F = E.build(m, k, n, sb)
    for c in extra: F.add(list(c))
    p = os.path.join(tempfile.gettempdir(), f"g2_{m}{k}{n}.cnf")
    with open(p, "w") as f:
        f.write(f"p cnf {F.nv} {len(F.clauses)}\n")
        for c in F.clauses: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time(); r = subprocess.run([CAD, "-q", "-t", str(cap), p], capture_output=True, text=True); os.remove(p)
    res = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "UNKNOWN"); chk = ""
    if res == "SAT":
        T = E.decode([int(x) for l in r.stdout.splitlines() if l.startswith("v") for x in l.split()[1:]], m, n)
        ok, bad, cnt = check(m, k, n, T); chk = "checker PASS" if ok else "checker FAIL"
        chk += f", 0 beats all in T0: {all(T[0][0][u] for u in range(1, n))}"
    return res, round(time.time() - t0, 1), chk
for args in [(2, 4, 9), (2, 4, 10), (3, 5, 8), (3, 5, 9), (3, 6, 13)]:
    print(args, "global2", solve(*args, "global2"), flush=True)
# SAT side of the nested block: force d = n-1 (0 -> n-1 in T_0) where such solutions exist
# (m=3,k=5,n=9 has f(2,4)=10 > 8 so no; use (4,5,8)? f(3,4)=7 <= 7 so yes; and (3,6,13): f(2,5) > 12, so expect UNSAT)
for (m, k, n) in [(4, 5, 8), (3, 4, 7), (3, 6, 13)]:
    var_0_last = None
    # e(0, 0, n-1) variable index: tournament 0, pair (0, n-1) is the (n-1)-th variable (1-based)
    var_0_last = n - 1
    print((m, k, n), "global2 + force 0 beats all in T0", solve(m, k, n, "global2", extra=[[var_0_last]]), flush=True)
print((3, 6, 11), "global2", solve(3, 6, 11, "global2"), flush=True)
