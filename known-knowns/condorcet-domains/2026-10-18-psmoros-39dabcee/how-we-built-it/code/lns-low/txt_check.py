"""Independent re-derivation: read the text assignment (a b c iNj), and check that every order of the gzipped list
obeys every line (pure Python, sampled every K-th order if K > 1). Usage: python txt_check.py assign.txt orders.gz K"""
import sys, gzip
rules = []
for l in open(sys.argv[1]):
    a, b, c, r = l.split(); i, j = int(r[0]), int(r[2]); rules.append(((int(a), int(b), int(c))[i - 1], (int(a), int(b), int(c)), j - 1))
K = int(sys.argv[3]); bad = 0; m = 0
with gzip.open(sys.argv[2], 'rt') as f:
    for k, l in enumerate(f):
        if k % K: continue
        o = list(map(int, l.split())); pos = {v: q for q, v in enumerate(o)}; m += 1
        for s, t, p in rules:
            r = sum(pos[u] < pos[s] for u in t if u != s)
            if r == p: bad += 1; break
print('rules', len(rules), 'orders checked', m, 'orders violating some rule', bad)
