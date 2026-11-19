#!/usr/bin/env python3
"""Baseline for a seeded result: the best length reachable from the published dictionary by ONE edit
(delete one value, insert one sum of two values, or replace one value by one sum), scored by acw_big (beam KB).
usage: trivial_edits.py CURVE BW DICTFILE KB OUTFILE"""
import itertools, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
c, bw, dfile, kb, outf = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
D = sorted(set(int(x) for x in open(dfile).read().split()))
VB = 1 << int(bw)
def valid(S):
    s = set(S)
    return all(x == 1 or any((x - a) in s for a in S if a < x) for x in S)
sums = sorted(set(a + b for a in D for b in D if a + b < VB) - set(D))
cands = [("base", D)]
for x in D[1:]:
    S = [y for y in D if y != x]
    if valid(S): cands.append(("del %d" % x, S))
for y in sums:
    cands.append(("ins %d" % y, sorted(D + [y])))
for x in D[1:]:
    for y in sums:
        S = sorted([z for z in D if z != x] + [y])
        if valid(S): cands.append(("rep %d->%d" % (x, y), S))
tmp = tempfile.mkdtemp()
def score(i):
    name, S = cands[i]
    f = os.path.join(tmp, "%d.txt" % i)
    open(f, "w").write(" ".join(map(str, S)))
    r = subprocess.run(["./acw_big", c, "1", bw, "1", "0.9", "0.15", f], env=dict(os.environ, KB=kb, EVAL="1"), capture_output=True, text=True)
    os.remove(f)
    return int(r.stdout.strip()) if r.stdout.strip() else 10**6
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(score, range(len(cands))))
hist = {}
for v in res: hist[v] = hist.get(v, 0) + 1
with open(outf, "w") as f:
    f.write("# one-edit neighbours of the dictionary in %s, scored with beam KB=%s\n# candidates: %d (1 base, deletions, insertions of a sum, replacements by a sum)\n" % (dfile, kb, len(cands)))
    f.write("# histogram length:count  " + " ".join("%d:%d" % (k, hist[k]) for k in sorted(hist)) + "\n")
    for (name, S), v in sorted(zip(cands, res), key=lambda t: t[1])[:40]:
        f.write("%d %s\n" % (v, name))
print(open(outf).read()[:1200])
