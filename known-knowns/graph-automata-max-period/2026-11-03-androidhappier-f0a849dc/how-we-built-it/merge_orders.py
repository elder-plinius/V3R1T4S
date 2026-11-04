#!/usr/bin/env python3
"""Merge lifeB2 residue-class outputs for one order into B_order<N>.txt (sum counts, union periods, sum histograms,
concatenate high lines, keep one witness per length)."""
import sys, glob, re
d, N = sys.argv[1], int(sys.argv[2])
files = sorted(glob.glob(f"{d}/B_order{N}_r*of*.txt"))
mods = {re.search(r'of(\d+)', f).group(1) for f in files}; assert len(mods) == 1
mod = int(mods.pop()); assert len(files) == mod, (len(files), mod)
tot = 0; per = set(); hist = {}; high = []; wit = {}
for f in files:
    for l in open(f):
        p = l.split()
        if l.startswith('order='): assert int(p[0].split('=')[1]) == N; tot += int(p[1].split('=')[1])
        elif l.startswith('periods:'): per |= set(map(int, p[1:]))
        elif p[0] == 'hist': hist[int(p[1])] = hist.get(int(p[1]), 0) + int(p[2])
        elif p[0] == 'high': high.append(l.rstrip('\n'))
        elif p[0] == 'witness': wit.setdefault(int(p[1]), (p[2], p[3]))
print(f"order={N} connected_graphs={tot} max_cycle={max(per)}")
print("periods: " + " ".join(map(str, sorted(per))))
for L in sorted(wit): print("witness", L, *wit[L])
for k in sorted(hist): print("hist", k, hist[k])
for h in sorted(high): print(h)
