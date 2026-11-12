#!/usr/bin/env python3
"""Build and check an explicit addition chain from a wide dictionary (model of acw.c).

usage: build_wide.py CURVE "s1 s2 ..." [out.txt] [KB]

The DP here is only a constructor; the claim rests on check_chain() from build_chain.py
(every element is a sum of two earlier ones, the last is E = N - 2, x * x^E == 1 mod N).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_chain import HEX, NAME, CTYPE, KRUN, JB, INF, Chain, check_chain, ladders

def top_table(c, S, W):
    ctype = CTYPE[c]; K = KRUN[c]
    Sset = set(S)
    kmax = 32 if ctype == 2 else 40
    small = [1] + [k for k in range(2, kmax + 1) if (1 << k) - 1 in Sset]
    tcost = [INF] * (W + 1); trec = [None] * (W + 1)
    if ctype == 1:
        def leaf(k, cost, path, visited):
            w = K - k
            if cost < tcost[w]:
                tcost[w] = cost; trec[w] = ("run", path, k)
        ladders(K - W, K, small, leaf)
    else:
        def leaf(k, cost, path, visited):
            coins = [m for m in visited if m <= 32]
            mc = [0] + [INF] * 64; pick = [0] * 65
            for o in range(1, 65):
                for m in coins:
                    if m <= o and mc[o - m] + 1 < mc[o]:
                        mc[o] = mc[o - m] + 1; pick[o] = m
            for w in range(W + 1):
                o = 64 - w
                cc = cost + 96 - w + mc[o]
                if cc < tcost[w]:
                    lst = []
                    while o:
                        lst.append(pick[o]); o -= pick[o]
                    tcost[w] = cc; trec[w] = ("p256", path, lst)
        ladders(32, 32, small, leaf)
    return tcost, trec

def build(c, S, KB=4000, W=None):
    E = int(HEX[c], 16); L = E.bit_length()
    S = sorted(set(S)); Sset = set(S)
    assert S[0] == 1
    ctype = CTYPE[c]; K = KRUN[c]
    Jb = JB[c] if ctype != 1 else L - K
    BW = max(S).bit_length()
    if W is None: W = min(40, BW + 2)
    ch = Chain()
    for x in S[1:]:
        pair = next(((a, x - a) for a in S if a < x and (x - a) in Sset), None)
        assert pair, "dictionary is not an addition chain at %d" % x
        ch.add(*pair)
    if ctype == 0:
        jend = L - 1; tcost = trec = None
    else:
        tcost, trec = top_table(c, S, W); jend = Jb + W
    pairs = {}
    for i, a in enumerate(S):
        for b in S[i:]:
            pairs.setdefault(a + b, (a, b))
    plist = list(pairs)
    # levels: dict delta -> (cost, parent) ; parent = (prev delta, adds tuple)
    lev = [{0: (0, None)}]
    res = (INF, None)
    for j in range(jend + 1):
        cur = lev[j]
        if len(cur) > KB:
            def key(d):
                c0 = cur[d][0]
                if d == 0: fr = 0
                else:
                    x = d ^ ((E >> j) & ((1 << 64) - 1)); ln = d.bit_length()
                    fr = (x & -x).bit_length() - 1 if x else 64
                    fr = min(fr, ln)
                return 8 * (c0 - j) - fr
            keep = sorted(cur, key=key)[:KB]
            cur = {d: cur[d] for d in keep}; lev[j] = cur
        b = (E >> j) & 1
        hi = E >> j
        nx = {}
        for d, (cst, _) in cur.items():
            if d >= hi: continue
            if ctype == 0:
                if hi - d in Sset:
                    if cst < res[0]: res = (cst, (j, d, hi - d))
                    continue
            elif d == 0 and j >= Jb and cst + tcost[j - Jb] < res[0]:
                res = (cst + tcost[j - Jb], (j, 0, j - Jb))
            if j == jend: continue
            if (d & 1) == b:
                if cst + 1 < nx.get(d >> 1, (INF,))[0]: nx[d >> 1] = (cst + 1, (d, ()))
            for a in S:
                if ((d + a) & 1) == b:
                    d2 = (d + a) >> 1
                    if cst + 2 < nx.get(d2, (INF,))[0]: nx[d2] = (cst + 2, (d, (a,)))
            for p in plist:
                if ((d + p) & 1) == b:
                    d2 = (d + p) >> 1
                    if cst + 3 < nx.get(d2, (INF,))[0]: nx[d2] = (cst + 3, (d, pairs[p]))
        lev.append(nx)
    assert res[1], "no path"
    g0, (j, d, tinfo) = res
    # walk down from (j, d) to (0, 0): at each level the stored parent tells the adds made at level j-1
    ops = []
    while j > 0:
        pd, adds = lev[j][d][1]
        ops.append(("d", 1))
        for a in adds: ops.append(("a", a))
        d = pd; j -= 1
    assert d == 0
    g0j, (jt, dt, tinfo) = res
    R = lambda k: (1 << k) - 1
    def run_ladder(path, kend):
        for (k, m) in path:
            v = R(k)
            for _ in range(m): v = ch.add(v, v)
            ch.add(v, R(m))
        return R(kend)
    if ctype == 0:
        v = tinfo
    else:
        rec = trec[tinfo]
        if rec[0] == "run":
            v = run_ladder(rec[1], rec[2])
        else:
            v = run_ladder(rec[1], 32)
            for _ in range(32): v = ch.add(v, v)
            for m in rec[2]:
                for _ in range(m): v = ch.add(v, v)
                v = ch.add(v, R(m))
    assert v == (E >> jt) - dt, "top value mismatch"
    for (op, x) in ops:
        v = ch.add(v, v) if op == "d" else ch.add(v, x)
    assert v == E
    return E, ch.steps, (len(S) - 1) + g0

if __name__ == "__main__":
    c = int(sys.argv[1]); S = [int(t) for t in sys.argv[2].split()]
    KB = int(sys.argv[4]) if len(sys.argv) > 4 else 4000
    E, steps, predicted = build(c, S, KB)
    n = check_chain(steps, E, E + 2)
    dbl = sum(1 for (i, j) in steps if i == j)
    print("%s: chain length %d (doublings %d, additions %d); DP predicted %d; checks PASS" % (NAME[c], n, dbl, n - dbl, predicted))
    if len(sys.argv) > 3 and sys.argv[3] != "-":
        with open(sys.argv[3], "w") as f:
            f.write("# %s inversion exponent N-2 = 0x%x\n# addition chain, length %d; line t: i j means a[t] = a[i] + a[j], a[0] = 1\n" % (NAME[c], E, n))
            for (i, j) in steps: f.write("%d %d\n" % (i, j))
