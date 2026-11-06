"""Standalone checker for A384209 (Python 3 standard library only), written from the OEIS definition:
"Maximum period for Game of Life on a simple graph with n vertices. A live vertex lives on to the next generation
only if it has 2 or 3 living neighbors. A dead vertex comes alive if it has exactly 3 living neighbors."
Modes:
  witness <graph6> <state> <expected>   simulate and check the minimal cycle length
  small <nmax>                          exhaustive over ALL labelled graphs on n <= nmax vertices (no nauty), compare with OEIS
  outputs <dir>                         check saved program outputs: graph counts, maxima, agreement of A and B
"""
import sys, itertools, re, glob, os
OEIS = [1, 1, 1, 1, 2, 4, 8, 14, 27]           # A384209(1..9) as published
A000088 = [1, 2, 4, 11, 34, 156, 1044, 12346, 274668, 12005168]
A001349 = [1, 1, 2, 6, 21, 112, 853, 11117, 261080, 11716571]
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
    seen = {}
    i = 0
    while s not in seen:
        seen[s] = i; s = successor(n, adj, s); i += 1
    return i - seen[s]
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
def main():
    m = sys.argv[1]
    if m == "witness":
        g, st, exp = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        n, adj = decode_g6(g); L = cycle_len(n, adj, st)
        print(f"witness {g} n={n} start={st} cycle_length={L} expected={exp}")
        return L == exp
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
        d = sys.argv[2]; ok = True
        a = open(os.path.join(d, "A_n1_9.txt")).read().splitlines()
        for n, line in enumerate(a, 1):
            g = int(re.search(r"graphs=(\d+)", line).group(1)); p = int(re.search(r"maxperiod=(\d+)", line).group(1))
            good = g == A000088[n-1] and p == OEIS[n-1]; ok &= good
            print(f"A n={n} graphs={g} maxperiod={p} {'ok' if good else 'MISMATCH'}")
        t = open(os.path.join(d, "A_n10_merged.txt")).read()
        g = int(re.search(r"total_graphs (\d+)", t).group(1)); p = int(re.search(r"max_period \((\d+)", t).group(1))
        good = g == A000088[9] and p == 46; ok &= good
        print(f"A n=10 graphs={g} maxperiod={p} {'ok' if good else 'MISMATCH'}")
        for k in range(1, 11):
            t = open(os.path.join(d, f"B_order{k}.txt")).read()
            g = int(re.search(r"connected_graphs=(\d+)", t).group(1))
            good = g == A001349[k-1]; ok &= good
            print(f"B order={k} connected_graphs={g} {'ok' if good else 'MISMATCH'}")
        c = open(os.path.join(d, "combine_n1_10.txt")).read()
        vals = [int(x) for x in re.findall(r"a\(n\)=(\d+)", c)]
        good = vals == OEIS + [46]; ok &= good
        print(f"B combine a(1..10)={vals} {'ok' if good else 'MISMATCH'}")
        return ok
    raise SystemExit("unknown mode")
if __name__ == "__main__":
    r = main(); print("ok" if r else "FAIL"); sys.exit(0 if r else 1)
