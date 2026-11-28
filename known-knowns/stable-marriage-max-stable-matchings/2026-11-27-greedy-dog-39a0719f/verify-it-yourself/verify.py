#!/usr/bin/env python3
import csv, hashlib, os, sys

def load_prefs(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.split("#", 1)[0].strip()
            if s:
                rows.append([int(x) for x in s.split()])
    n = len(rows) // 2
    assert len(rows) == 2 * n and n == 10
    for row in rows:
        assert len(row) == n and set(row) == set(range(1, n + 1))
    mp = [[w - 1 for w in r] for r in rows[:n]]
    wp = [[m - 1 for m in r] for r in rows[n:]]
    mr = [[0] * n for _ in range(n)]
    wr = [[0] * n for _ in range(n)]
    for i in range(n):
        for r, v in enumerate(mp[i]): mr[i][v] = r
        for r, v in enumerate(wp[i]): wr[i][v] = r
    return n, mp, mr, wr

def is_stable(n, mp, mr, wr, match):
    if len(set(match)) != n: return False
    inv = [0] * n
    for m, w in enumerate(match): inv[w] = m
    for m in range(n):
        for r in range(mr[m][match[m]]):
            w = mp[m][r]
            if wr[w][m] < wr[w][inv[w]]: return False
    return True

def count_stable(n, mp, mr, wr):
    compat = [[[0] * n for _ in range(n)] for _ in range(n)]
    for m in range(n):
        for w in range(n):
            for m2 in range(n):
                if m2 == m: continue
                mask = 0
                for w2 in range(n):
                    if w2 == w: continue
                    if mr[m][w2] < mr[m][w] and wr[w2][m] < wr[w2][m2]: continue
                    if mr[m2][w] < mr[m2][w2] and wr[w][m2] < wr[w][m]: continue
                    mask |= 1 << w2
                compat[m][w][m2] = mask
    full = (1 << n) - 1
    match = [-1] * n
    cnt = 0
    def dfs(u, dom):
        nonlocal cnt
        if u == 0:
            assert is_stable(n, mp, mr, wr, match)
            cnt += 1
            return
        bm, bc, t = -1, n + 1, u
        while t:
            b = t & -t; m = b.bit_length() - 1; t ^= b
            c = dom[m].bit_count()
            if c == 0: return
            if c < bc:
                bc, bm = c, m
                if c == 1: break
        rem, cand = u ^ (1 << bm), dom[bm]
        while cand:
            b = cand & -cand; w = b.bit_length() - 1; cand ^= b
            match[bm] = w
            ndom, ok, r = list(dom), True, rem
            while r:
                rb = r & -r; m2 = rb.bit_length() - 1; r ^= rb
                nd = dom[m2] & compat[bm][w][m2]
                if nd == 0: ok = False; break
                ndom[m2] = nd
            if ok: dfs(rem, ndom)
    dfs(full, [full] * n)
    return cnt

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(root, "object", "object.prefs")
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    rows = list(csv.DictReader(open(os.path.join(root, "INDEX.csv"), encoding="utf-8")))
    assert len(rows) == 1 and rows[0]["sha256"] == sha and int(rows[0]["value"]) == 1008
    n, mp, mr, wr = load_prefs(p)
    cnt = count_stable(n, mp, mr, wr)
    print(f"n={n} stable_matchings={cnt} sha256={sha[:8]}")
    assert cnt == 1008
    print("PASS")

if __name__ == "__main__":
    main()
