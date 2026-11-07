#!/usr/bin/env python3
"""Predicted ranks for the p1 band next to LITA's odd squares N = 13..31, compared with the saved tables.
Step 1 (one slice + one absorption) removes (N^2+3N)/2 terms (object-as-data closed form, proved on 13, 15, 17; unverified);
step 2 removes (N^2+2N-1)/2 (seen on 15 and 17); step 3 (N^2+N-2)/2 (seen on 15 and 17). Predictions only: a cell
counts only once its scheme is built and checked exactly.
Usage: predict_p1_band.py <run dir>   (reads data/fmm_sota_claimtime.json and data/lille_index.html, not shipped)"""
import sys, os, json, re, html
run = sys.argv[1]
fs = {tuple(e["format"]): e["rank"] for e in json.load(open(os.path.join(run, "data", "fmm_sota_claimtime.json")))["entries"]}
lille = open(os.path.join(run, "data", "lille_index.html"), encoding="utf-8", errors="replace").read()
def lil(c):
    i = lille.find('"%dx%dx%d.html"' % c)
    if i < 0:
        return None
    seg = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", lille[i:i + 700])))
    m = re.search(r"⟨\s*%d\s*×\s*%d\s*×\s*%d\s*:\s*(\d+)\s*⟩" % c, seg)
    return int(m.group(1)) if m else None
lita = {13: 1379, 15: 1977, 17: 2723, 19: 3633, 21: 4723, 23: 6009, 25: 7507, 27: 9233, 29: 11203, 31: 13433}
print("N | cell | predicted | fmm_sota | Lille index | margin")
for N, R in lita.items():
    r1 = R - (N * N + 3 * N) // 2; r2 = r1 - (N * N + 2 * N - 1) // 2; r3 = r2 - (N * N + N - 2) // 2
    for c, r in (((N - 1, N, N), r1), ((N - 1, N - 1, N), r2), ((N - 1, N - 1, N - 1), r3)):
        bar = min(x for x in (fs.get(c), lil(c)) if x is not None)
        print("%d | %s | %d | %s | %s | %d" % (N, "x".join(map(str, c)), r, fs.get(c), lil(c), bar - r))
