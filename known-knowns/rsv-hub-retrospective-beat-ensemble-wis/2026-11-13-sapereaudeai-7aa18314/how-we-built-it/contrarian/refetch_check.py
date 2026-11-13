"""Live re-check (PREREG R10): one honest GET of the HopkinsIDD hub's recursive tree (GitHub API, main) and one GET of each
2024-25 hub-ensemble file from raw.githubusercontent.com at main; compare with the local copies used for scoring by
git blob SHA and by sha256. usage: python refetch_check.py <out dir>"""
import os, sys, json, hashlib, time, glob, datetime as dt, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOCAL = os.path.join(RUN, "data", "hopkins", "hub")
UA = "V3R1T4S-research-agent/1.0 (honest single request; open research notebook)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""


def blob_sha(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    log = []
    t0 = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    code, body = get("https://api.github.com/repos/HopkinsIDD/rsv-forecast-hub/git/trees/main?recursive=1")
    log.append("%s GET tree main -> HTTP %d, %d bytes" % (t0, code, len(body)))
    if code != 200:
        print("\n".join(log)); open(os.path.join(out, "refetch_check.txt"), "w").write("\n".join(log) + "\n"); sys.exit(1)
    open(os.path.join(out, "tree_main_recheck.json"), "wb").write(body)
    tree = {t["path"]: t for t in json.loads(body)["tree"] if t["type"] == "blob"}
    diffs = 0; n = 0
    for p, t in sorted(tree.items()):
        if not p.startswith("model-output/") or p.count("/") != 2:
            continue
        loc = os.path.join(LOCAL, p)
        if not os.path.exists(loc):
            log.append("NEW upstream file not in local copy: %s" % p); diffs += 1; continue
        n += 1
        if blob_sha(open(loc, "rb").read()) != t["sha"]:
            log.append("CHANGED upstream: %s" % p); diffs += 1
    for loc in glob.glob(os.path.join(LOCAL, "model-output", "*", "*")):
        p = os.path.relpath(loc, LOCAL).replace(os.sep, "/")
        if p not in tree:
            log.append("REMOVED upstream: %s" % p); diffs += 1
    log.append("model-output files compared by git blob SHA: %d, differences: %d" % (n, diffs))
    tp = "target-data/2026-06-05_rsvnet_hospitalization.csv"
    same_truth = tp in tree and blob_sha(open(os.path.join(LOCAL, tp), "rb").read()) == tree[tp]["sha"]
    other_truth = [p for p in tree if p.startswith("target-data/") and p.endswith(".csv") and "/archive/" not in p]
    log.append("truth file %s unchanged upstream: %s; target-data/*.csv at top level: %s" % (tp, same_truth, other_truth))
    # one direct GET of each 2024-25 hub-ensemble file, sha256 compared with the local copy
    for p in sorted(x for x in tree if x.startswith("model-output/hub-ensemble/") and x.split("/")[-1][:10] >= "2024-10-01"):
        time.sleep(1.5)
        c, b = get("https://raw.githubusercontent.com/HopkinsIDD/rsv-forecast-hub/main/" + p)
        lb = open(os.path.join(LOCAL, p), "rb").read()
        log.append("%s GET %s -> HTTP %d sha256 %s local %s %s" % (
            dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%SZ"), p, c, hashlib.sha256(b).hexdigest()[:16],
            hashlib.sha256(lb).hexdigest()[:16], "SAME" if b == lb else "DIFFERENT"))
    txt = "\n".join(log)
    open(os.path.join(out, "refetch_check.txt"), "w").write(txt + "\n")
    print(txt)
