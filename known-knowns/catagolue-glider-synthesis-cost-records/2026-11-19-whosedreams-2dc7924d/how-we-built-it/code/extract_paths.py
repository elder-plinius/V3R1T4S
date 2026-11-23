#!/usr/bin/env python3
"""Run Shinjuku dijkstra once; dump component-line paths for the input apgcodes of failed compose candidates."""
import sys, os, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data', 'Shinjuku'))
from shinjuku.search import dijkstra
cands = sys.argv[1:-1]; out = sys.argv[-1]
need = set()
for l in (x for f in cands for x in open(f)):
    s = l.split()
    if s and s[0] == 'IMPROVE': need.add(s[7])
paths = dijkstra()
res = {}
for a in need:
    if a not in paths: continue
    lines = []; cur = a
    while cur != "":
        p = paths[cur]; lines.append(p[2]); cur = p[1]
    res[a] = {"cost": paths[a][0], "lines": lines[::-1]}
json.dump(res, open(out, "w"))
print("need", len(need), "found", len(res))
