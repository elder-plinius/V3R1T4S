#!/usr/bin/env python3
"""Aggregate data/sample/sample_units.txt: all 4 passes x 4096 chunks present, totals, all CAP, and per-unit
max tcap <= the user's chunk maxtcap. Also recounts how many masks the frozen hash rule selects in a few chunks
(pure Python, independent of lantx2) and compares with n. Usage: python3 code/scripts/check_sample_summary.py [UNITS]"""
import glob, os, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
uf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "data", "sample", "sample_units.txt")
user = {}
for f in glob.glob(os.path.join(root, "data", "user-chunk-sums", "chunk_*.sum")):
    t = open(f).read().split(); kv = dict(zip(t[0::2], t[1::2])); user[int(kv["chunk"])] = int(kv["maxtcap"])
units = {}
for l in open(uf):
    t = l.split(); kv = dict(zip(t[0::2], t[1::2])); units[(int(kv["pass"]), int(kv["chunk"]))] = kv
bad = 0
if sorted(units) != [(p, c) for p in range(4) for c in range(4096)]: print("FAIL: units are not 4 x 4096"); bad += 1
n = cap = over = 0
for (p, c), kv in units.items():
    n += int(kv["n"]); cap += int(kv["CAP"])
    if kv["UNCAP"] != "0" or kv["OOB"] != "0" or kv["n"] != kv["CAP"]: bad += 1; print("NONCAP unit", p, c)
    if int(kv["maxtcap"]) > user[c]: over += 1; bad += 1; print("OVER", p, c, kv["maxtcap"], user[c])
M = (1 << 64) - 1
def smix(z):
    z = (z + 0x9E3779B97F4A7C15) & M
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M
    return z ^ (z >> 31)
SEED = 0x5EED20261020
for c in (() if os.environ.get("QUICK") else (0, 4095)):   # QUICK=1 skips; recount selection with pure Python (2^24 hashes per chunk, ~1 min each)
    cnt = [0, 0, 0, 0]
    for m in range(c << 24, (c + 1) << 24):
        r = smix((m + SEED) & M) % 10000
        if r < 100: cnt[r // 25] += 1
    for p in range(4):
        if cnt[p] != int(units[(p, c)]["n"]): bad += 1; print("SELECTION COUNT MISMATCH", p, c, cnt[p], units[(p, c)]["n"])
    print("chunk %d python selection counts per pass %s (units: %s)" % (c, cnt, [units[(p, c)]["n"] for p in range(4)]))
print("sample masks %d (%.6f%% of 2^36) CAP %d; units over user chunk max: %d" % (n, 100.0 * n / (1 << 36), cap, over))
print("SAMPLE SUMMARY: PASS" if bad == 0 else "SAMPLE SUMMARY: FAIL"); sys.exit(1 if bad else 0)
