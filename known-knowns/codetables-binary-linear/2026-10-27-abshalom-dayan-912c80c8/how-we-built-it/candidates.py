"""Cells (n,k) over GF(9), 28 <= n <= 36, where a Construction X code from nested one-point Hermitian codes
C(D,aP) in C(D,bP) (27 affine points; plain, n = 27 + l) or C(D,aP)|0 in E_b (extended, n = 28 + l) could beat the
live lower bound: upper bound U = min(d(P_a), d(base_b) + l) > lb(n,k), with exact d(P_m) from
constructor/out/plain_d*.txt and d(E_b) = d(P_b) + 1 (measured for b = 15..21; used here only as an upper bound
assumption, d(E_b) <= d(P_b) + 1 holds since puncturing the 28th coordinate gives P_b). Also lists the X lower bound
L = min(d(P_a), d(base_b) + l - r + 1) with an MDS tail. Usage: candidates.py RANGE.json PLAIN_D_FILES..."""
import sys, json, re
rng = json.load(open(sys.argv[1]))
dP = {}
for f in sys.argv[2:]:
    for line in open(f):
        m = re.match(r'^P_(\d+)(?:\.code)?\s.*?d=(\d+)', line)
        if m: dP[int(m.group(1))] = int(m.group(2))
poles = sorted(3 * i + 4 * j for j in range(3) for i in range(10) if 3 * i + 4 * j <= 26)
K = {m: sum(1 for p in poles if p <= m) for m in range(27)}
out = []
for a in range(27):
    for b in range(a + 1, 27):
        if a not in dP or b not in dP or K[b] == K[a] or b not in poles or a not in poles: continue
        r = K[b] - K[a]
        for ext in (0, 1):
            db = dP[b] + ext
            for l in range(max(1, r), 10):
                n = 27 + ext + l
                if n > 36: continue
                k = K[b]; c = rng.get(f"{n},{k}")
                if not c: continue
                U = min(dP[a], db + l); L = min(dP[a], db + l - r + 1)
                if U > c[0]:
                    out.append(dict(a=a, b=b, ext=ext, l=l, n=n, k=k, r=r, lb=c[0], ub=c[1], U=U, L=L))
print(len(out), "candidate codes;", len({(o['n'], o['k']) for o in out}), "cells")
for o in sorted(out, key=lambda o: (o['n'], o['k'])): print(json.dumps(o))
