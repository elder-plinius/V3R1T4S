"""Independent exhaustive covering-design check: every t-subset of {1..v} lies in some block."""
import json, sys, hashlib
from itertools import combinations
for p in sys.argv[1:]:
    raw = open(p, 'rb').read(); d = json.loads(raw)
    v, k, t, B = d['v'], d['k'], d['t'], d['blocks']
    ok = len(B) == d['b'] and all(len(b) == k and len(set(b)) == k and all(1 <= x <= v for x in b) for b in B)
    cov = set()
    for b in B:
        cov.update(combinations(sorted(b), t))
    need = sum(1 for _ in combinations(range(1, v + 1), t))
    print(f"C({v},{k},{t}) b={len(B)} blocks_ok={ok} covered={len(cov)}/{need} {'PASS' if ok and len(cov) == need else 'FAIL'} sha={hashlib.sha256(raw).hexdigest()[:16]}")
