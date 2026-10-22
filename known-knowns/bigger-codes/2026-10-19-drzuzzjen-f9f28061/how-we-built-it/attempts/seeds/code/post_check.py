"""Post-job check (Stage F): pick PREFIX_best.npy if it exists else PREFIX_cur.npy, write it as a 0/1 text file
(character j = bit j, sorted), run BOTH workspace checkers SEQUENTIALLY on that text file, and record M, sha256,
the fraction of final words that are seed words, and (from PREFIX.log) the first engine time at which M >= 8698.
usage: post_check.py PREFIX SEED.npy OUT.json"""
import datetime, hashlib, json, os, re, subprocess, sys
import numpy as np
WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
TOOLS = os.path.join(WS, "tools")
n, d, w = 25, 6, 11
prefix, seedp, out = sys.argv[1], sys.argv[2], sys.argv[3]
utc = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
src = prefix + "_best.npy" if os.path.exists(prefix + "_best.npy") else prefix + "_cur.npy"
arr = sorted(int(x) for x in np.unique(np.load(src).astype(np.int64)))
txt = os.path.splitext(src)[0] + ".txt"
data = "".join("".join("1" if (x >> j) & 1 else "0" for j in range(n)) + "\n" for x in arr).encode("ascii")
open(txt, "wb").write(data)
seed = set(int(x) for x in np.load(seedp))
r = {"start": utc(), "source": src, "source_sha256": hashlib.sha256(open(src, "rb").read()).hexdigest(), "file": txt,
     "file_sha256": hashlib.sha256(data).hexdigest(), "M": len(arr), "seed_word_fraction": round(sum(x in seed for x in arr) / len(arr), 4),
     "seed_words_kept": sum(x in seed for x in arr), "checks": {}}
for chk in ("cwcheck_int.py", "cwcheck_set.py"):
    t0 = utc()
    p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(TOOLS, chk), txt, str(n), str(d), str(w)], capture_output=True, text=True)
    try: js = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: js = {"raw": p.stdout[-300:], "err": p.stderr[-300:]}
    r["checks"][chk] = {"rc": p.returncode, "start": t0, "end": utc(), "json": js}
r["both_valid"] = all(v["rc"] == 0 and v["json"].get("valid") is True for v in r["checks"].values())
rounds = []
if os.path.exists(prefix + ".log"):
    for ln in open(prefix + ".log", encoding="utf-8"):
        m = re.match(r"round (\d+): M=(\d+) gain=(-?\d+) applied=(\d+) best=(\d+) t=(\d+)s", ln)
        if m: rounds.append(tuple(int(g) for g in m.groups()))
r["rounds"] = len(rounds)
r["M_start_round0"] = rounds[0][1] if rounds else None
r["best_log"] = max((x[4] for x in rounds), default=None)
r["t_first_M_ge_8698_s"] = next((x[5] for x in rounds if x[1] >= 8698), None)
r["t_first_M_gt_8698_s"] = next((x[5] for x in rounds if x[1] > 8698), None)
r["applied_rounds_gt0"] = sum(1 for x in rounds if x[3] > 0)
r["last_t_s"] = rounds[-1][5] if rounds else None
r["end"] = utc()
json.dump(r, open(out, "w"), indent=1)
print(json.dumps({k: r[k] for k in ("source", "M", "file_sha256", "both_valid", "seed_word_fraction", "t_first_M_ge_8698_s", "rounds")}))
sys.exit(0 if r["both_valid"] else 1)
