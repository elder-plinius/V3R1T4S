#!/usr/bin/env python3
"""Re-optimise generalized combining split for (v,k,t) using ONLY designs on disk (INDEX.tsv kept) + trivial designs.
eff(v,k,t) = min over on-disk (v',k',t) with v'>=v, k'<=k (point deletion + padding), plus trivial t=0,t=1,k>=v.
Plan per v1: per-j terms A_j*B_j with free k1_j, optionally V1whole tail (k>=v1) / V2whole head (k>=v2).
Usage: splitopt.py V K T [top]  -> prints best plans (JSON lines)."""
import sys, json, math, functools
RUN = './runs/2026-10-18-0304'
IDX = {}
for line in open(RUN + '/data/ljcr_designs/INDEX.tsv'):
    p = line.split('\t')
    if len(p) >= 5 and p[4].strip() == 'kept':
        IDX[(int(p[0]), int(p[1]), int(p[2]))] = int(p[3])
BYT = {}
for (a, b, c), n in IDX.items():
    BYT.setdefault(c, []).append((a, b, n))

@functools.lru_cache(maxsize=None)
def eff(v, k, t):
    """(count, source) for a (v,k,t) covering buildable from disk; None if impossible."""
    if k < 0 or k > v or t > v:
        return None
    if t == 0:
        return (1, ('triv0',))
    if k < t:
        return None
    if k == v:
        return (1, ('whole',))
    best = (math.ceil(v / k), ('triv1',)) if t == 1 else None
    for (a, b, n) in BYT.get(t, []):
        if a >= v and b <= k and b >= t and (a - v) <= 0 or (a >= v and b <= k and a > v and False):
            pass
        if a >= v and t <= b <= k and b <= v:
            if best is None or n < best[0]:
                best = (n, ('file', a, b, t))
    return best

def plan(v, k, t, v1):
    v2 = v - v1
    # per-j best term
    terms = []
    for j in range(t + 1):
        bj = None
        if j > v1 or t - j > v2:
            terms.append((0, None)); continue  # no t-set with this intersection
        for k1 in range(0, min(k, v1) + 1):
            k2 = k - k1
            if k2 < 0 or k2 > v2:
                continue
            A = eff(v1, k1, j); B = eff(v2, k2, t - j)
            if A is None or B is None:
                continue
            c = A[0] * B[0]
            if bj is None or c < bj[0]:
                bj = (c, (k1, A, B))
        if bj is None:
            return None
        terms.append(bj)
    # options: V2whole head covers j<=a (needs k>=v2): eff(v1,k-v2,a); V1whole tail covers j>=a (k>=v1): eff(v2,k-v1,t-a)
    best = None
    heads = [(-1, 0, None)]  # head covers j<=h
    if k >= v2:
        for h in range(0, t + 1):
            E = eff(v1, k - v2, h) if h <= v1 else None
            if E: heads.append((h, E[0], ('V2whole', h, E)))
    tails = [(t + 1, 0, None)]
    if k >= v1:
        for a in range(0, t + 1):
            E = eff(v2, k - v1, t - a) if t - a <= v2 else None
            if E: tails.append((a, E[0], ('V1whole', a, E)))
    for (h, hc, hs) in heads:
        for (a, tc, ts) in tails:
            if a <= h:
                tot = hc + tc; mid = []
            else:
                tot = hc + tc + sum(terms[j][0] for j in range(h + 1, a)); mid = list(range(h + 1, a))
            if best is None or tot < best[0]:
                best = (tot, v1, hs, ts, [(j, terms[j][1]) for j in mid if terms[j][1] is not None])
    return best

if __name__ == '__main__':
    v, k, t = map(int, sys.argv[1:4]); top = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    res = []
    for v1 in range(1, v):
        p = plan(v, k, t, v1)
        if p: res.append(p)
    res.sort(key=lambda x: x[0])
    seen = set()
    for r in res[:top]:
        print(json.dumps({'v': v, 'k': k, 't': t, 'b_pred': r[0], 'v1': r[1], 'head': r[2], 'tail': r[3], 'terms': r[4]}))
