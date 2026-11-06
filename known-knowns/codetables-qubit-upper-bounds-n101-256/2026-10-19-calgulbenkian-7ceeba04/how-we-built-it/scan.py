#!/usr/bin/env python3
"""Resumable batch runner: scan.py CELLS.json OUTDIR [prec]
CELLS.json: list of {"n","k","d","shadow","tag"}.  For each cell not yet in OUTDIR/results.jsonl, run the
Phase-1 LP; on infeasibility write OUTDIR/certs/cert_n_k_d_{sh|ns}.json and verify it with check_cert.py
(separate process).  One JSON line per finished cell = checkpoint (each cell takes seconds to minutes).
A heartbeat thread appends `date -u` style timestamps to OUTDIR/heartbeat.txt every 30 s."""
import json, os, sys, time, threading, subprocess, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qlp

cells = json.load(open(sys.argv[1]))
out = sys.argv[2]
prec = int(sys.argv[3]) if len(sys.argv) > 3 else 1536
WINDOW = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "full" else None
os.makedirs(os.path.join(out, "certs"), exist_ok=True)
res_path = os.path.join(out, "results.jsonl")

def beat():
    while True:
        with open(os.path.join(out, "heartbeat.txt"), "a") as f:
            f.write(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")
        time.sleep(30)
threading.Thread(target=beat, daemon=True).start()

checker = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_cert.py")
Kcache = {}

def run_one(n, k, d, sh, tag):
    if n not in Kcache:
        Kcache.clear(); Kcache[n] = qlp.kraw_table(n)
    t0 = time.time()
    try:
        r = qlp.solve_phase1(n, k, d, sh, prec=prec, K=Kcache[n], max_iter=60000, window=WINDOW)
    except Exception as ex:
        r = {"status": "error", "error": repr(ex)[:300]}
    cert = r.pop("cert", None)
    rec = {"n": n, "k": k, "d": d, "shadow": sh, "tag": tag, "window": WINDOW, **r,
           "wall": round(time.time() - t0, 1),
           "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if cert:
        fn = os.path.join(out, "certs", "cert_%d_%d_%d_%s.json" % (n, k, d, "sh" if sh else "ns"))
        json.dump(cert, open(fn, "w"))
        p = subprocess.run([sys.executable, "-I", checker, fn], capture_output=True, text=True)
        rec["checker"] = p.stdout.strip()[:200]
        rec["verified"] = p.returncode == 0
        rec["cert"] = os.path.relpath(fn, out)
    with open(res_path, "a") as f:
        f.write(json.dumps(rec) + "\n")
    done[(n, k, d, sh)] = rec
    return rec

done = {}
if os.path.exists(res_path):
    for line in open(res_path):
        try:
            r = json.loads(line); done[(r["n"], r["k"], r["d"], r["shadow"])] = r
        except Exception:
            pass

def get(n, k, d, sh, tag):
    return done.get((n, k, d, sh)) or run_one(n, k, d, sh, tag)

for c in cells:
    n, k, d, sh = c["n"], c["k"], c["d"], c["shadow"]
    r = get(n, k, d, sh, c.get("tag", ""))
    if not c.get("descend") or r.get("status") != "infeasible" or not r.get("verified"):
        continue
    lo = c["lower"]            # a code with distance lo exists: LP must be feasible at lo
    feas, inf = lo, d          # invariant: feasible at feas (by existence), infeasible at inf
    if c.get("linear"):        # step down one at a time (cheap when the gain is small)
        while inf - 1 > lo:
            rm = get(n, k, inf - 1, sh, c.get("tag", "") + "-linear")
            if rm.get("status") == "infeasible" and rm.get("verified"):
                inf -= 1
            else:
                if rm.get("status") == "feasible":
                    feas = inf - 1
                break
    while inf - feas > 1 and not c.get("linear"):
        mid = (feas + inf) // 2
        rm = get(n, k, mid, sh, c.get("tag", "") + "-bisect")
        if rm.get("status") == "feasible":
            feas = mid
        elif rm.get("status") == "infeasible" and rm.get("verified"):
            inf = mid
        else:
            break
    if inf <= lo:
        with open(res_path, "a") as f:
            f.write(json.dumps({"n": n, "k": k, "d": inf, "shadow": sh, "tag": "BUG-certificate-at-or-below-lower-bound"}) + "\n")
    with open(os.path.join(out, "lpbound.jsonl"), "a") as f:
        f.write(json.dumps({"n": n, "k": k, "shadow": sh, "lp_max_feasible_d": feas if inf - feas == 1 else None,
                            "first_infeasible_d": inf, "start_d": d}) + "\n")
print("SCAN DONE", flush=True)
