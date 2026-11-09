"""Fetch ZTF light curves listed in how-we-built-it/data/lc_manifest.csv from the public SNAD ZTF API (one GET each,
1.2 s apart, honest User-Agent; stops at the first HTTP error) into DIR as <set>_NNNN.json, and report how many are
byte-identical to the scored files. Default: the 82 variable stars; with --all: all 524 stars (about 15 minutes).
Usage: python3 -I verify-it-yourself/fetch_lightcurves.py DIR [--all]"""
import csv, hashlib, os, sys, time, urllib.request, urllib.error
d = sys.argv[1]; os.makedirs(d, exist_ok=True)
same = 0; n = 0
for r in csv.DictReader(open("how-we-built-it/data/lc_manifest.csv")):
    if r["set"] != "var" and "--all" not in sys.argv:
        continue
    req = urllib.request.Request(r["url"], headers={"User-Agent": "V3R1T4S-verify (research; honest client)"})
    try:
        body = urllib.request.urlopen(req, timeout=120).read()
    except urllib.error.HTTPError as e:
        print("HTTP %d for draw %s: stopping (no retries)" % (e.code, r["draw"])); sys.exit(1)
    open(os.path.join(d, "%s_%04d.json" % (r["set"], int(r["draw"]))), "wb").write(body)
    n += 1; same += hashlib.sha256(body).hexdigest() == r["sha256"]
    time.sleep(1.2)
print("fetched %d light curves; %d byte-identical to the scored files" % (n, same))
