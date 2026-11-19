#!/usr/bin/env python3
"""Build an explicit addition chain from a dictionary S found by acsa, then check it.

usage: build_chain.py CURVE "s1 s2 ..." [out.txt]

The builder (a small DP with traceback) is only a constructor. The claim rests on
check_chain(): every element is the sum of two earlier elements, the last one is the
target exponent, and x * x^E == 1 mod N on random x, all in exact integer arithmetic.
"""
import sys, random

HEX = [
    "1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3eb",
    "ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc63254f",
    "fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f",
    "ffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52971",
]
NAME = ["Curve25519 scalar", "P-256 scalar", "secp256k1 scalar", "P-384 scalar"]
CTYPE = [0, 2, 1, 1]
KRUN = [0, 0, 127, 192]
JB = [125, 128, None, None]
INF = 10 ** 9
B = 11


def check_chain(steps, E, N=None):
    """steps: list of (i, j); element t+1 = a[i] + a[j], a[0] = 1. Returns length."""
    a = [1]
    for (i, j) in steps:
        assert 0 <= i < len(a) and 0 <= j < len(a), "index out of range"
        a.append(a[i] + a[j])
    assert a[-1] == E, "chain does not end at the target"
    if N is not None:
        rng = random.Random(20261110)
        for _ in range(100):
            x = rng.randrange(2, N - 1)
            p = [x]
            for (i, j) in steps:
                p.append(p[i] * p[j] % N)
            assert p[-1] * x % N == 1, "modular inverse check failed"
    return len(steps)


class Chain:
    def __init__(self):
        self.vals = [1]
        self.idx = {1: 0}
        self.steps = []

    def add(self, x, y):
        v = x + y
        if v in self.idx:
            return v
        self.steps.append((self.idx[x], self.idx[y]))
        self.idx[v] = len(self.vals)
        self.vals.append(v)
        return v


def ladders(target_lo, target_hi, small, leaf):
    """Enumerate run ladders k1, k1+m, ... (m in visited or small); call leaf(k, cost, path, visited)."""
    best = {}
    maxavail = max(small)

    def clog2(o, k):
        s = 0
        while k < o:
            k <<= 1
            s += 1
        return s

    def rec(k, cost, path, cnt):
        if target_lo <= k <= target_hi:
            if cost <= best.get(k, INF):
                best[k] = cost
                leaf(k, cost, list(path), set(cnt))
        if k == target_hi:
            return
        kk = max(k, maxavail)
        ok = False
        for o in range(max(target_lo, k + 1), target_hi + 1):
            if cost + (o - k) + max(1, clog2(o, kk)) <= best.get(o, INF):
                ok = True
                break
        if not ok:
            return
        for m in sorted(cnt, reverse=True):
            k2 = k + m
            if k2 > target_hi:
                continue
            new = k2 not in cnt
            cnt.add(k2)
            path.append((k, m))
            rec(k2, cost + m + 1, path, cnt)
            path.pop()
            if new:
                cnt.discard(k2)

    for k1 in sorted(small, reverse=True):
        rec(k1, 0, [], set(small))


FULLMODEL = False


def clean_dp(E, S, Sset, Jb, W, top, tcost):
    # main-line DP over clean levels
    low = lambda j, w: (E >> j) & ((1 << w) - 1)
    g = [INF] * (top + 60)
    how = [None] * (top + 60)
    for j in range(top, -1, -1):
        best, h = INF, None
        if j >= Jb and tcost[j - Jb] < best:
            best, h = tcost[j - Jb], ("top", j - Jb)
        if not (E >> j) & 1 and g[j + 1] + 1 < best:
            best, h = g[j + 1] + 1, ("z",)
        for b in S:
            ln = b.bit_length()
            if low(j, ln) == b and j + ln <= top and g[j + ln] + ln + 1 < best:
                best, h = g[j + ln] + ln + 1, ("win", ln, b)
            for s in range(0, ln):
                if low(j, s) != b & ((1 << s) - 1):
                    break
                ds, js = b >> s, j + s
                if js > top:
                    break
                for w in range(1, B + 2):
                    a = low(js, w) - ds
                    if a > 0 and a in Sset and g[js + w] + w + s + 2 < best:
                        best, h = g[js + w] + w + s + 2, ("two", s, w, a, b)
        g[j], how[j] = best, h
    # trace back from level 0 to the top, then replay forward
    ops, j = [], 0
    while True:
        h = how[j]
        assert h, "no path"
        if h[0] == "top":
            wtop = h[1]
            break
        if h[0] == "z":
            ops.append(("d", 1)); j += 1
        elif h[0] == "win":
            ops.append(("a", h[2])); ops.append(("d", h[1])); j += h[1]
        else:
            _, s, w, a, b = h
            ops.append(("a", b)); ops.append(("d", s)); ops.append(("a", a)); ops.append(("d", w)); j += s + w
    return ops, wtop, g[0]


def general_dp(E, S, Jb, W, tcost):
    """States (j, delta): value = (E >> j) - delta, delta >= 0. Moves: double, add a in S."""
    top = Jb + W
    cap = 4 << B
    Sd = sorted(S, reverse=True)
    lev = {}
    prev = {}
    for j in range(top, -1, -1):
        cur = {}
        if j + 1 in lev:
            bit = (E >> j) & 1
            for d, (cst, _) in lev[j + 1].items():
                d2 = 2 * d + bit
                if d2 < cap and cst + 1 < cur.get(d2, (INF,))[0]:
                    cur[d2] = (cst + 1, ("d", d))
        if j >= Jb and tcost[j - Jb] < cur.get(0, (INF,))[0]:
            cur[0] = (tcost[j - Jb], ("top", j - Jb))
        for d in sorted(cur, reverse=True):
            cst = cur[d][0]
            for a in Sd:
                d2 = d - a
                if d2 < 0:
                    continue
                if cst + 1 < cur.get(d2, (INF,))[0]:
                    cur[d2] = (cst + 1, ("a", a, d))
        # deltas reached by an add are smaller, and sorted() above was taken before inserts:
        # iterate to a fixed point
        changed = True
        while changed:
            changed = False
            for d in sorted(cur, reverse=True):
                cst = cur[d][0]
                for a in Sd:
                    d2 = d - a
                    if d2 >= 0 and cst + 1 < cur.get(d2, (INF,))[0]:
                        cur[d2] = (cst + 1, ("a", a, d))
                        changed = True
        lev[j] = cur
    ops, j, d = [], 0, 0
    g0 = lev[0][0][0]
    while True:
        h = lev[j][d][1]
        if h[0] == "top":
            assert d == 0
            return ops, h[1], g0
        if h[0] == "d":
            ops.append(("d", 1)); d = h[1]; j += 1
        else:
            ops.append(("a", h[1])); d = h[2]


def build(c, S):
    global B
    B = max(11, max(S).bit_length())
    E = int(HEX[c], 16)
    L = E.bit_length()
    S = sorted(set(S))
    Sset = set(S)
    assert S[0] == 1 and all(x < (1 << B) for x in S)
    ctype = CTYPE[c]
    K = KRUN[c]
    Jb = JB[c] if ctype != 1 else L - K
    W = B + 2
    top = Jb + W
    ch = Chain()
    # dictionary
    for x in S[1:]:
        pair = next(((a, x - a) for a in S if a < x and (x - a) in Sset and (x - a) < x), None)
        assert pair, "dictionary is not an addition chain at %d" % x
        ch.add(*pair)
    # top options: tcost[w], trecipe[w]
    tcost = [INF] * (W + 1)
    trec = [None] * (W + 1)
    if ctype == 0:
        for w in range(W + 1):
            q = (L - 1) - (Jb + w)
            p = max([pp for pp in range(1, B) if (1 << pp) in Sset and pp <= q], default=0)
            tcost[w] = q - p
            trec[w] = ("pow", p, q)
    else:
        small = [1] + [k for k in range(2, B + 1) if (1 << k) - 1 in Sset]
        if ctype == 1:
            def leaf(k, cost, path, visited):
                w = K - k
                if cost < tcost[w]:
                    tcost[w] = cost
                    trec[w] = ("run", path, k)
            ladders(K - W, K, small, leaf)
        else:
            def leaf(k, cost, path, visited):
                coins = [m for m in visited if m <= 32]
                mc = [0] + [INF] * 64
                pick = [0] * 65
                for o in range(1, 65):
                    for m in coins:
                        if m <= o and mc[o - m] + 1 < mc[o]:
                            mc[o] = mc[o - m] + 1
                            pick[o] = m
                for w in range(W + 1):
                    o = 64 - w
                    cc = cost + 96 - w + mc[o]
                    if cc < tcost[w]:
                        lst = []
                        while o:
                            lst.append(pick[o])
                            o -= pick[o]
                        tcost[w] = cc
                        trec[w] = ("p256", path, lst)
            ladders(32, 32, small, leaf)
    if FULLMODEL:
        ops, wtop, g0 = general_dp(E, S, Jb, W, tcost)
    else:
        ops, wtop, g0 = clean_dp(E, S, Sset, Jb, W, top, tcost)
    ops.reverse()
    R = lambda k: (1 << k) - 1
    rec = trec[wtop]

    def run_ladder(path, kend):
        for (k, m) in path:
            v = R(k)
            for _ in range(m):
                v = ch.add(v, v)
            ch.add(v, R(m))
        return R(kend)

    if rec[0] == "pow":
        v = 1 << rec[1]
        for _ in range(rec[2] - rec[1]):
            v = ch.add(v, v)
    elif rec[0] == "run":
        v = run_ladder(rec[1], rec[2])
    else:
        v = run_ladder(rec[1], 32)
        for _ in range(32):
            v = ch.add(v, v)
        for m in rec[2]:
            for _ in range(m):
                v = ch.add(v, v)
            v = ch.add(v, R(m))
    assert v == E >> (Jb + wtop), "top value mismatch"
    for (op, x) in ops:
        if op == "d":
            for _ in range(x):
                v = ch.add(v, v)
        else:
            v = ch.add(v, x)
    assert v == E
    return E, ch.steps, (len(S) - 1) + g0


if __name__ == "__main__":
    if "--full" in sys.argv:
        sys.argv.remove("--full")
        FULLMODEL = True
    c = int(sys.argv[1])
    S = [int(t) for t in sys.argv[2].split()]
    E, steps, predicted = build(c, S)
    N = E + 2
    n = check_chain(steps, E, N)
    dbl = sum(1 for (i, j) in steps if i == j)
    print("%s: chain length %d (doublings %d, additions %d); DP predicted %d; checks PASS" % (NAME[c], n, dbl, n - dbl, predicted))
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w") as f:
            f.write("# %s inversion exponent N-2 = 0x%x\n# addition chain, length %d; line t: i j means a[t] = a[i] + a[j], a[0] = 1\n" % (NAME[c], E, n))
            for (i, j) in steps:
                f.write("%d %d\n" % (i, j))
