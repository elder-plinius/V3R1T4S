#!/usr/bin/env python3
"""count_stable.py: exact count of the stable matchings of a stable marriage instance
(n men, n women, complete strict preference lists).

Definition (Gusfield & Irving 1989, Sec. 1.1; Knuth 1976): a matching M (a bijection men -> women)
is stable iff there is no blocking pair (m, w): m prefers w to M(m) and w prefers m to M(w).

Two independent counters:
  lattice : walk the lattice of stable matchings from the man-optimal matching M0 by eliminating
            exposed rotations (cycles of next_M), with a visited set.  Every matching visited is
            re-verified stable by the direct definition.  Theory: Gusfield & Irving, chapters 2-3.
  brute   : backtracking over all perfect matchings, assigning men in order and pruning a partial
            assignment as soon as two assigned pairs form a blocking pair (sound: the blocking
            property of two pairs depends only on them; complete: every stable matching passes every
            partial test).  No theory used.  Exponential; meant for n <= 9 or so.

Input:
  --oeis FILE --n N : the OEIS A357271 instance file; parses the paired ranking table for order N
                      ("a,b" in row i, column j = rank man i gives woman j, rank woman j gives man i),
                      and cross-checks it against the MiniZinc rankMen / rankWomen blocks for that N.
  --prefs FILE      : 2n lines: men's preference lists (women 1..n, best first), then women's lists.
  --ident N         : built-in test: identical lists for everyone (exactly 1 stable matching).
  --knuth4          : built-in test: Knuth's order-4 instance (10 stable matchings = A357269(4)).
  --random N SEED   : a random instance (for cross-checking the two counters).
Options: --brute (also run the brute-force counter), --expect K (exit 1 unless both counts == K).
"""
import argparse, random, re, sys, time

def parse_prefs(text):
    rows = [list(map(int, l.split())) for l in text.strip().splitlines() if l.strip() and not l.lstrip().startswith('#')]
    n = len(rows) // 2
    assert len(rows) == 2 * n, "need 2n lines"
    mpref = [[x - 1 for x in r] for r in rows[:n]]
    wpref = [[x - 1 for x in r] for r in rows[n:]]
    return n, mpref, wpref

def parse_oeis_pairs(text, n):
    """Paired ranking table 'order n example with K SM' -> (mpref, wpref, K)."""
    m = re.search(r'(?i)order\s+%d\s+example\s+with\s+(\d+)\s+SM\s*\n(.*?)\*/' % n, text, re.S)
    if not m:
        raise SystemExit("no 'order %d example' block in file" % n)
    claimed = int(m.group(1))
    rows = []
    for line in m.group(2).splitlines():
        pairs = re.findall(r'(\d+)\s*,\s*(\d+)', line)
        if pairs:
            rows.append([(int(a), int(b)) for a, b in pairs])
    assert len(rows) == n and all(len(r) == n for r in rows), "table is not n x n"
    rankMen = [[a for a, b in r] for r in rows]            # rankMen[i][j]: rank man i gives woman j
    rankWomen = [[rows[i][j][1] for i in range(n)] for j in range(n)]  # rankWomen[j][i]: rank woman j gives man i
    return rankMen, rankWomen, claimed

def parse_oeis_minizinc(text, n):
    """The 'n = N; rankWomen = [| ... |]; rankMen = [| ... |];' blocks for order n."""
    m = re.search(r'n\s*=\s*%d\s*;\s*rankWomen\s*=\s*\[\|(.*?)\|\]\s*;\s*rankMen\s*=\s*\[\|(.*?)\|\]\s*;' % n, text, re.S)
    if not m:
        return None, None
    def grid(s):
        return [[int(x) for x in re.findall(r'\d+', row)] for row in s.split('|') if re.search(r'\d', row)]
    return grid(m.group(2)), grid(m.group(1))   # rankMen, rankWomen

def ranks_to_prefs(rankMen, rankWomen):
    n = len(rankMen)
    for i in range(n):
        assert sorted(rankMen[i]) == list(range(1, n + 1)), "rankMen row %d is not a permutation" % (i + 1)
        assert sorted(rankWomen[i]) == list(range(1, n + 1)), "rankWomen row %d is not a permutation" % (i + 1)
    mpref = [sorted(range(n), key=lambda j: rankMen[i][j]) for i in range(n)]
    wpref = [sorted(range(n), key=lambda i: rankWomen[j][i]) for j in range(n)]
    return mpref, wpref

def rank_tables(n, mpref, wpref):
    mrank = [[0] * n for _ in range(n)]
    wrank = [[0] * n for _ in range(n)]
    for m in range(n):
        for pos, w in enumerate(mpref[m]):
            mrank[m][w] = pos
    for w in range(n):
        for pos, m in enumerate(wpref[w]):
            wrank[w][m] = pos
    return mrank, wrank

def is_stable(n, mrank, wrank, M):
    """Direct check of the definition. M[m] = w."""
    Mw = [0] * n
    for m in range(n):
        Mw[M[m]] = m
    for m in range(n):
        rm = mrank[m]
        for w in range(n):
            if rm[w] < rm[M[m]] and wrank[w][m] < wrank[w][Mw[w]]:
                return False
    return True

def gale_shapley(n, pref_p, rank_r):
    """Proposer-optimal stable matching. Returns match[p] = r."""
    nxt = [0] * n
    held = [-1] * n            # receiver -> proposer
    match = [-1] * n
    free = list(range(n))
    while free:
        p = free.pop()
        r = pref_p[p][nxt[p]]
        nxt[p] += 1
        h = held[r]
        if h == -1:
            held[r] = p; match[p] = r
        elif rank_r[r][p] < rank_r[r][h]:
            held[r] = p; match[p] = r; match[h] = -1; free.append(h)
        else:
            free.append(p)
    return match

def count_lattice(n, mpref, wpref, mrank, wrank, verify=True):
    M0 = gale_shapley(n, mpref, wrank)                 # man-optimal, M0[m] = w
    Mz_w = gale_shapley(n, wpref, mrank)               # woman-optimal, Mz_w[w] = m
    Mz = [0] * n
    for w in range(n):
        Mz[Mz_w[w]] = w
    assert is_stable(n, mrank, wrank, M0) and is_stable(n, mrank, wrank, Mz)
    seen = {tuple(M0)}
    stack = [M0]
    while stack:
        M = stack.pop()
        if verify:
            assert is_stable(n, mrank, wrank, M), "lattice walk produced an unstable matching"
        Mw = [0] * n
        for m in range(n):
            Mw[M[m]] = m
        # next_M: s_M(m) = first woman below M(m) on m's list (down to Mz(m)) who prefers m to her partner
        nxt = [-1] * n
        for m in range(n):
            lst = mpref[m]
            for w in lst[mrank[m][M[m]] + 1: mrank[m][Mz[m]] + 1]:
                if wrank[w][m] < wrank[w][Mw[w]]:
                    nxt[m] = Mw[w]
                    break
        # cycles of nxt = rotations exposed in M
        state = [0] * n
        for s in range(n):
            if state[s] or nxt[s] == -1:
                continue
            path = []
            u = s
            while u != -1 and state[u] == 0:
                state[u] = 1; path.append(u); u = nxt[u]
            if u != -1 and state[u] == 1:          # u is on the current path: cycle u -> ... -> u
                cyc = path[path.index(u):]
                M2 = list(M)
                for i, mi in enumerate(cyc):        # m_i moves to w_{i+1} = M(m_{i+1})
                    M2[mi] = M[cyc[(i + 1) % len(cyc)]]
                t = tuple(M2)
                if t not in seen:
                    seen.add(t); stack.append(M2)
            for v in path:
                state[v] = 2
    assert tuple(Mz) in seen, "woman-optimal matching not reached"
    return len(seen)

def count_brute(n, mrank, wrank):
    assign = [-1] * n
    taken = [False] * n
    cnt = 0
    def rec(m):
        nonlocal cnt
        if m == n:
            cnt += 1; return
        rm = mrank[m]
        for w in range(n):
            if taken[w]:
                continue
            ok = True
            rw = wrank[w]
            for m2 in range(m):
                w2 = assign[m2]
                if (rm[w2] < rm[w] and wrank[w2][m] < wrank[w2][m2]) or (mrank[m2][w] < mrank[m2][w2] and rw[m2] < rw[m]):
                    ok = False; break
            if ok:
                assign[m] = w; taken[w] = True
                rec(m + 1)
                assign[m] = -1; taken[w] = False
    rec(0)
    return cnt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--oeis'); ap.add_argument('--n', type=int)
    ap.add_argument('--prefs'); ap.add_argument('--ident', type=int); ap.add_argument('--knuth4', action='store_true')
    ap.add_argument('--random', nargs=2, type=int, metavar=('N', 'SEED'))
    ap.add_argument('--brute', action='store_true'); ap.add_argument('--expect', type=int)
    a = ap.parse_args()
    claimed = None
    if a.oeis:
        text = open(a.oeis, encoding='utf-8', errors='replace').read()
        rankMen, rankWomen, claimed = parse_oeis_pairs(text, a.n)
        mzMen, mzWomen = parse_oeis_minizinc(text, a.n)
        if mzMen is not None:
            print("minizinc_blocks_match_paired_table:", mzMen == rankMen and mzWomen == rankWomen)
        else:
            print("minizinc_blocks_match_paired_table: not found")
        mpref, wpref = ranks_to_prefs(rankMen, rankWomen); n = a.n
    elif a.prefs:
        n, mpref, wpref = parse_prefs(open(a.prefs).read())
    elif a.ident:
        n = a.ident; mpref = [list(range(n)) for _ in range(n)]; wpref = [list(range(n)) for _ in range(n)]
    elif a.knuth4:
        n = 4
        mpref = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
        wpref = [[3, 2, 1, 0], [2, 3, 0, 1], [1, 0, 3, 2], [0, 1, 2, 3]]
    elif a.random:
        n, seed = a.random; rng = random.Random(seed)
        mpref = [rng.sample(range(n), n) for _ in range(n)]; wpref = [rng.sample(range(n), n) for _ in range(n)]
    else:
        ap.error('no instance')
    for m in range(n):
        assert sorted(mpref[m]) == list(range(n)) and sorted(wpref[m]) == list(range(n)), "lists must be complete and strict"
    mrank, wrank = rank_tables(n, mpref, wpref)
    print("n:", n)
    if claimed is not None:
        print("claimed_in_file:", claimed)
    t0 = time.time(); L = count_lattice(n, mpref, wpref, mrank, wrank); t1 = time.time()
    print("lattice_count: %d  (%.2fs)" % (L, t1 - t0))
    B = None
    if a.brute:
        t0 = time.time(); B = count_brute(n, mrank, wrank); t1 = time.time()
        print("brute_count: %d  (%.2fs)" % (B, t1 - t0))
        print("counters_agree:", B == L)
    ok = True
    if a.expect is not None:
        ok = (L == a.expect) and (B is None or B == a.expect)
        print("expected:", a.expect, "PASS" if ok else "FAIL")
    if claimed is not None:
        print("matches_claimed_in_file:", L == claimed)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
