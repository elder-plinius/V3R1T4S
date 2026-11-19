"""Standalone checker for A384209 (Python 3 standard library only), written from the OEIS definition:
"Maximum period for Game of Life on a simple graph with n vertices. A live vertex lives on to the next generation
only if it has 2 or 3 living neighbors. A dead vertex comes alive if it has exactly 3 living neighbors."
a(n) = max over all simple graphs on n vertices (disconnected included) and all 2^n start states of the length of
the eventual cycle. State s: bit v = vertex v live; vertex order as in graph6.
Modes:
  witness <graph6> <state> <expected>   simulate from one start; the cycle length must equal <expected>
  graph <graph6> <expected>             this graph over all 2^n starts: the maximum cycle length must equal <expected>
  small <nmax>                          exhaustive over ALL labelled graphs on n <= nmax vertices (no nauty), vs OEIS
  outputs <dir>                         saved program outputs: graph counts, a(1..11), agreement of A and B at n = 11
"""
import sys, itertools, re, glob, os
OEIS = [1, 1, 1, 1, 2, 4, 8, 14, 27]           # A384209(1..9) as published
A000088 = [1, 2, 4, 11, 34, 156, 1044, 12346, 274668, 12005168, 1018997864]
A001349 = [1, 1, 2, 6, 21, 112, 853, 11117, 261080, 11716571, 1006700565]
CLAIM = 71
def decode_g6(s):
    n = ord(s[0]) - 63
    bits = [((ord(c) - 63) >> (5 - b)) & 1 for c in s[1:] for b in range(6)]
    adj = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: adj[i] |= 1 << j; adj[j] |= 1 << i
            k += 1
    return n, adj
def successor(n, adj, s):
    t = 0
    for v in range(n):
        c = bin(s & adj[v]).count("1")
        if c == 3 or (c == 2 and (s >> v) & 1): t |= 1 << v
    return t
def cycle_len(n, adj, s):
    seen = {}; i = 0
    while s not in seen:
        seen[s] = i; s = successor(n, adj, s); i += 1
    return i - seen[s], seen[s]
def max_period(n, adj):
    nxt = [successor(n, adj, s) for s in range(1 << n)]
    best = 0; state = [0] * (1 << n)
    for s in range(1 << n):
        if state[s]: continue
        path = {}; x = s
        while not state[x] and x not in path:
            path[x] = len(path); x = nxt[x]
        if x in path: best = max(best, len(path) - path[x])
        for y in path: state[y] = 1
    return best
def field(t, key):
    m = re.search(r"\b%s=(\d+)" % key, t); return int(m.group(1)) if m else None
def outputs(d):
    ok = True
    def rep(msg, good):
        nonlocal ok; ok &= bool(good); print(msg, "ok" if good else "MISMATCH")
    # Program A, n = 1..9 and n = 10 (all graphs)
    for n, line in enumerate(open(os.path.join(d, "A_n1_9.txt")).read().splitlines(), 1):
        g, p = field(line, "graphs"), field(line, "maxperiod")
        rep(f"A n={n} graphs={g} maxperiod={p}", g == A000088[n-1] and p == OEIS[n-1])
    t = [l for l in open(os.path.join(d, "A10_r0of1.txt")) if l.startswith("n=10")][0]
    g, p = field(t, "graphs"), field(t, "maxperiod")
    rep(f"A n=10 graphs={g} maxperiod={p} (reproduced, not claimed)", g == A000088[9] and p == 46)
    # Program A, n = 11, 64 residue classes of geng -q 11
    files = sorted(glob.glob(os.path.join(d, "A11_r*of64.txt")))
    tot = con = best = 0; hall = {}; hcon = {}; highA = set(); summaries = 0
    for f in files:
        for l in open(f):
            p = l.split()
            if not p: continue
            if l.startswith("n=11"):
                summaries += 1; tot += field(l, "graphs"); con += field(l, "connected"); best = max(best, field(l, "maxperiod"))
            elif p[0] == "hist_all": hall[int(p[1])] = hall.get(int(p[1]), 0) + int(p[2])
            elif p[0] == "hist_conn": hcon[int(p[1])] = hcon.get(int(p[1]), 0) + int(p[2])
            elif p[0] == "high" and p[3] == "1": highA.add((p[1], int(p[2])))
    rep(f"A n=11 residue files={len(files)} summaries={summaries}", len(files) == 64 and summaries == 64)
    rep(f"A n=11 graphs={tot} (A000088(11)={A000088[10]}) connected={con} (A001349(11)={A001349[10]})",
        tot == A000088[10] and con == A001349[10] and sum(hall.values()) == tot and sum(hcon.values()) == con)
    rep(f"A n=11 maxperiod={best}, graphs reaching it={hall.get(best)}", best == CLAIM and hall.get(best) == 2)
    rep(f"A n=11 disconnected graphs: max per-graph period {max(k for k in hall if hall[k] != hcon.get(k, 0))}",
        max(k for k in hall if hall[k] != hcon.get(k, 0)) <= 46)
    # Program B, connected graphs per order, n = 11 merged from 64 residue classes
    P = {}
    for k in range(1, 12):
        t = open(os.path.join(d, f"B_order{k}.txt")).read()
        g = field(t, "connected_graphs"); P[k] = set(map(int, re.search(r"periods:(.*)", t).group(1).split()))
        rep(f"B order={k} connected_graphs={g} max_cycle={field(t, 'max_cycle')}", g == A001349[k-1] and field(t, "max_cycle") == max(P[k]))
    parts = sorted(glob.glob(os.path.join(d, "B11_parts", "B_order11_r*of64.txt")))
    ptot = 0; pper = set(); phist = {}
    for f in parts:
        for l in open(f):
            p = l.split()
            if not p: continue
            if l.startswith("order="): ptot += field(l, "connected_graphs")
            elif p[0] == "periods:": pper |= set(map(int, p[1:]))
            elif p[0] == "hist": phist[int(p[1])] = phist.get(int(p[1]), 0) + int(p[2])
    B = open(os.path.join(d, "B_order11.txt")).read()
    hB = {int(a): int(b) for a, b in re.findall(r"^hist (\d+) (\d+)$", B, re.M)}
    highB = {(g, int(v)) for g, v in re.findall(r"^high (\S+) (\d+)$", B, re.M)}
    rep(f"B order=11 parts={len(parts)} re-merged: graphs={ptot}, same periods and histogram as B_order11.txt",
        len(parts) == 64 and ptot == A001349[10] and pper == P[11] and phist == hB)
    # combine: lcm over partitions into connected components (a disjoint union evolves componentwise)
    from math import lcm
    reach = {0: {1}}
    memo = {}
    def R(n, m):
        if n == 0: return {1}
        if (n, m) in memo: return memo[(n, m)]
        out = set()
        for k in range(1, min(n, m) + 1):
            for q in R(n - k, k):
                for p in P[k]: out.add(lcm(p, q))
        memo[(n, m)] = out; return out
    vals = [max(R(n, n)) for n in range(1, 12)]
    rep(f"B combine (recomputed here) a(1..11)={vals}", vals == OEIS + [46, CLAIM])
    c = open(os.path.join(d, "combine_n1_11.txt")).read()
    rep("B combine saved output matches", [int(x) for x in re.findall(r"a\(n\)=(\d+)", c)] == vals)
    # A versus B at n = 11
    rep(f"A connected histogram == B histogram ({sum(hB.values())} graphs)", hcon == hB)
    rep(f"A and B: same connected graphs with max >= 40 ({len(highA)} / {len(highB)})", highA == highB)
    rep(f"A max {best} == B connected max {max(P[11])} == B combine a(11) {vals[-1]}", best == max(P[11]) == vals[-1] == CLAIM)
    return ok
def main():
    m = sys.argv[1]
    if m == "witness":
        g, st, exp = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        n, adj = decode_g6(g); L, pre = cycle_len(n, adj, st)
        print(f"witness {g} n={n} edges={sum(bin(a).count('1') for a in adj)//2} start={st} preperiod={pre} cycle_length={L} expected={exp}")
        return L == exp
    if m == "graph":
        g, exp = sys.argv[2], int(sys.argv[3])
        n, adj = decode_g6(g); p = max_period(n, adj)
        print(f"graph {g} n={n} all {1 << n} starts: max cycle_length={p} expected={exp}")
        return p == exp
    if m == "small":
        ok = True
        for n in range(1, int(sys.argv[2]) + 1):
            pairs = list(itertools.combinations(range(n), 2)); best = 0
            for mask in range(1 << len(pairs)):
                adj = [0] * n
                for b, (i, j) in enumerate(pairs):
                    if mask >> b & 1: adj[i] |= 1 << j; adj[j] |= 1 << i
                best = max(best, max_period(n, adj))
            print(f"n={n} labelled_graphs={1 << len(pairs)} max_period={best} oeis={OEIS[n-1]}")
            ok &= best == OEIS[n - 1]
        return ok
    if m == "outputs":
        return outputs(sys.argv[2])
    raise SystemExit("unknown mode")
if __name__ == "__main__":
    r = main(); print("ok" if r else "FAIL"); sys.exit(0 if r else 1)
