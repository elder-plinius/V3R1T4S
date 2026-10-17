#!/usr/bin/env python3
"""Verify every row of result/claims.csv with python3 + mpmath only (no numpy, no screen).
For each claim: sha256 of result/d<d>_N<N>.txt, shape, >= 20 significant digits per coordinate, c* over all
N(N-1)/2 pairs in mpmath at 50 digits, gain = c_table - c* >= 1e-10, kissing exclusion.
usage (from the lens folder): python3 -I code/verify_all.py [PLAIN_CSV]
PLAIN_CSV defaults to ../../data/sc/plain.csv (snapshot); pass a freshly fetched /plain to re-compare."""
import csv, hashlib, os, re, sys
import mpmath
mpmath.mp.dps = 50
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
plain = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "data", "sc", "plain.csv")
T = {}
for row in csv.reader(open(plain)):
    if len(row) >= 3:
        try: T[(int(row[0]), int(row[1]))] = row[2].strip()
        except ValueError: pass
def sig(t):
    m = t.lower().split("e")[0].lstrip("+-").replace(".", "")
    s = m.lstrip("0"); return len(s) if s else len(m)
ok_all = True
for r in csv.DictReader(open(os.path.join(HERE, "result", "claims.csv"))):
    d, N = int(r["d"]), int(r["N"])
    path = os.path.join(HERE, "result", "d%d_N%d.txt" % (d, N))
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    toks = [NUM.findall(l) for l in open(path)]
    toks = [t for t in toks if t]
    shape = len(toks) == N and all(len(t) == d for t in toks)
    digits = min(sig(x) for t in toks for x in t)
    U = []
    for t in toks:
        v = [mpmath.mpf(x) for x in t]
        s = 1 / mpmath.sqrt(mpmath.fsum([x * x for x in v]))
        U.append([x * s for x in v])
    c = max(mpmath.fdot(U[i], U[j]) for i in range(N) for j in range(i + 1, N))
    ct = T.get((d, N))
    gain = mpmath.mpf(ct) - c if ct is not None else None
    kiss = 9 <= d <= 23 and c <= mpmath.mpf("0.5")
    ok = (sha == r["sha256"] and shape and digits >= 20 and gain is not None and gain >= mpmath.mpf("1e-10") and not kiss
          and mpmath.nstr(c, 25) == r["c_star"])
    ok_all &= ok
    print("d=%d N=%d sha_ok=%s shape=%s min_digits=%d c*=%s c_table=%s gain=%s kissing=%s -> %s" % (
        d, N, sha == r["sha256"], shape, digits, mpmath.nstr(c, 25), ct, mpmath.nstr(gain, 12) if gain is not None else None,
        kiss, "OK" if ok else "FAIL"))
print("ALL_OK" if ok_all else "SOME_FAIL")
