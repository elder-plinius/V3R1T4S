"""Standalone checker for A357952 written from the OEIS definition (Python 3 standard library only).
A357952(n): maximum eventual cycle length of a totalistic cellular automaton on a connected graph with n nodes,
COUNTING THE UPDATED NODE ITSELF, over all connected graphs, all rules and all start states. Each node is ON or OFF;
all nodes update together; a node is ON next iff the number of ON nodes in its closed neighbourhood (its neighbours
plus itself) lies in the rule set R, a subset of {0..n} (2^(n+1) rules). This is not A357953, where the node itself
is not counted. State s: bit v = node v ON. Graphs are graph6 strings; vertex order as in graph6.
  check_self.py outputs object/evidence      saved A/B outputs: counts, a(1..8), graph-by-graph agreement at n = 9
  check_self.py witness G6 RULE START LEN    simulate one start; RULE like 1,3,5
  check_self.py graph G6 LEN                 this graph over all 2^(n+1) rules and 2^n starts: max must be LEN
  check_self.py small N                      a(1..N) over all labelled graphs, no nauty (N <= 6 is quick)"""
import itertools, os, re, sys

OEIS = [2, 2, 4, 6, 8, 18, 42, 112]                 # A357952(1..8), OEIS DATA
A001349 = [1, 1, 2, 6, 21, 112, 853, 11117, 261080]  # connected graphs on n nodes, n = 1..9
CLAIM, WITNESS, NEXT = 200, "H?o|]|~", 198

def g6(s):
    n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: bits += [((ord(ch) - 63) >> (5 - b)) & 1 for b in range(6)]
    nb = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: nb[i] |= 1 << j; nb[j] |= 1 << i
            k += 1
    return n, nb

def closed_counts(n, nb):
    """cnt[s][v] = number of ON nodes among v's neighbours and v itself in state s."""
    return [[bin(s & (nb[v] | 1 << v)).count("1") for v in range(n)] for s in range(1 << n)]

def succ_table(n, cnt, R):
    return [sum(1 << v for v in range(n) if (R >> c[v]) & 1) for c in cnt]

def cycle_from(nxt, x):
    seen = {}; t = 0
    while x not in seen: seen[x] = t; x = nxt(x); t += 1
    return seen[x], t - seen[x]

def max_cycle(table):
    N = len(table); mark = [0] * N; pos = [0] * N; best = 0
    for s in range(N):
        if mark[s]: continue
        x, p = s, 0
        while not mark[x]: mark[x] = s + 1; pos[x] = p; p += 1; x = table[x]
        if mark[x] == s + 1: best = max(best, p - pos[x])
    return best

def graph_max(n, nb):
    cnt = closed_counts(n, nb); best = (0, None)
    for R in range(1 << (n + 1)):
        m = max_cycle(succ_table(n, cnt, R))
        if m > best[0]: best = (m, R)
    return best

def connected(n, nb):
    seen, todo = 1, 1
    while todo:
        v = (todo & -todo).bit_length() - 1; todo &= todo - 1
        new = nb[v] & ~seen; seen |= new; todo |= new
    return seen == (1 << n) - 1

def pergraph(lines):
    d = {}
    for l in lines:
        if l.startswith("G "):
            _, g, m = l.split()
            if g in d: raise SystemExit("duplicate graph " + g)
            d[g] = int(m)
    return d

def hist_lines(lines):
    return {int(l.split()[1]): int(l.split()[2]) for l in lines if l.startswith("hist ")}

def cmd_outputs(d):
    ok = True
    rd = lambda f: open(os.path.join(d, f)).read().splitlines()
    A = [re.match(r"n=(\d+) mode=self graphs=(\d+) maxperiod=(\d+)", l).groups() for l in rd("A_n1_8.txt")]
    B = [re.match(r"summary order=(\d+) graphs=(\d+) max_cycle=(\d+)", l).groups() for l in rd("B_n1_8.txt")]
    for k in range(8):
        a, b = [int(x) for x in A[k]], [int(x) for x in B[k]]
        g = a == b == [k + 1, A001349[k], OEIS[k]]; ok &= g
        print(f"n={k+1} A graphs={a[1]} max={a[2]}  B graphs={b[1]} max={b[2]}  A001349={A001349[k]} OEIS={OEIS[k]} {'ok' if g else 'MISMATCH'}")
    allA, allB = {}, {}
    for r in range(8):
        la, lb = rd(f"A9_part{r}.txt"), rd(f"B9_part{r}.txt")
        sa = [re.match(r"n=9 mode=self graphs=(\d+) maxperiod=(\d+) witness_graph6=(\S+)", l) for l in la if l.startswith("n=")]
        sb = [re.match(r"summary order=9 graphs=(\d+) max_cycle=(\d+) witness=(\S+)", l) for l in lb if l.startswith("summary")]
        pa, pb = pergraph(la), pergraph(lb)
        g = len(sa) == len(sb) == 1 and sa[0] and sb[0]
        if g:
            ga, ma, wa = int(sa[0].group(1)), int(sa[0].group(2)), sa[0].group(3)
            gb, mb, wb = int(sb[0].group(1)), int(sb[0].group(2)), sb[0].group(3)
            hA, hB = hist_lines(la), hist_lines(lb)
            recount = {}
            for m in pa.values(): recount[m] = recount.get(m, 0) + 1
            g = (pa == pb and ga == gb == len(pa) and ma == mb == max(pa.values()) and wa == wb
                 and pa[wa] == ma and hA == hB == recount)
            print(f"part {r}: A graphs={ga} max={ma} | B graphs={gb} max={mb} | per-graph lines identical={pa == pb} "
                  f"| histograms consistent={hA == hB == recount} | witness {wa} {'ok' if g else 'MISMATCH'}")
        else:
            print(f"part {r}: summary line missing MISMATCH")
        ok &= bool(g)
        if set(pa) & set(allA): print("graph repeated across parts MISMATCH"); ok = False
        allA.update(pa); allB.update(pb)
    top = sorted(set(allA.values()))[-2:]
    reach = [x for x in allA if allA[x] == CLAIM]
    nxt = [x for x in allA if allA[x] == top[0]]
    g = (len(allA) == len(allB) == A001349[8] and allA == allB and top == [NEXT, CLAIM] and reach == [WITNESS])
    ok &= g
    print(f"n=9 total graphs A={len(allA)} B={len(allB)} (A001349(9)={A001349[8]}); A and B per-graph maxima identical: "
          f"{allA == allB}; max={top[-1]}; graphs reaching it: {reach}; next best {top[0]} on {nxt} {'ok' if g else 'MISMATCH'}")
    s = open(os.path.join(d, "A357952_9.txt")).read()
    g = f"A357952(9) = {CLAIM}" in s and WITNESS in s and "261080" in s; ok &= g
    print("A357952_9.txt states the value, witness and count:", "ok" if g else "MISMATCH")
    print("A357952(1..9) from saved outputs:", [int(x[2]) for x in A] + [top[-1]])
    return ok

def cmd_witness(g, rule, start, L):
    n, nb = g6(g); R = sum(1 << int(c) for c in rule.split(",") if c != "")
    cl = [nb[v] | 1 << v for v in range(n)]
    nxt = lambda s: sum(1 << v for v in range(n) if (R >> bin(s & cl[v]).count("1")) & 1)
    pre, cyc = cycle_from(nxt, int(start))
    deg = [bin(x).count("1") for x in nb]
    print(f"witness {g} n={n} edges={sum(deg)//2} degrees={deg} connected={connected(n, nb)} rule={{{rule}}} (self-counting) "
          f"start={start} preperiod={pre} cycle_length={cyc} expected={L}")
    return cyc == int(L) and connected(n, nb)

def cmd_graph(g, L):
    n, nb = g6(g); m, R = graph_max(n, nb)
    rule = ",".join(str(k) for k in range(n + 1) if R >> k & 1)
    print(f"graph {g}: max over all {1 << (n+1)} self-counting rules and {1 << n} starts = {m} (first at rule {{{rule}}}) expected={L}")
    return m == int(L)

def cmd_small(N):
    ok = True
    for n in range(1, N + 1):
        pairs = [(i, j) for j in range(1, n) for i in range(j)]
        E = len(pairs); seen = bytearray(1 << E); classes = conn = best = 0
        pidx = {p: k for k, p in enumerate(pairs)}
        pmap = [[pidx[(min(p[i], p[j]), max(p[i], p[j]))] for (i, j) in pairs] for p in itertools.permutations(range(n))]
        for m in range(1 << E):            # every labelled graph; one representative per isomorphism class
            if seen[m]: continue
            classes += 1
            for pm in pmap: seen[sum(1 << pm[k] for k in range(E) if m >> k & 1)] = 1
            nb = [0] * n
            for k, (i, j) in enumerate(pairs):
                if m >> k & 1: nb[i] |= 1 << j; nb[j] |= 1 << i
            if not connected(n, nb): continue
            conn += 1; best = max(best, graph_max(n, nb)[0])
        g = best == OEIS[n - 1] and conn == A001349[n - 1]; ok &= g
        print(f"n={n} labelled_graphs={1<<E} iso_classes={classes} connected={conn} (A001349={A001349[n-1]}) max_period={best} oeis={OEIS[n-1]} {'ok' if g else 'MISMATCH'}")
    return ok

if __name__ == "__main__":
    c, a = sys.argv[1], sys.argv[2:]
    r = {"outputs": lambda: cmd_outputs(*a), "witness": lambda: cmd_witness(*a),
         "graph": lambda: cmd_graph(*a), "small": lambda: cmd_small(int(a[0]))}[c]()
    print("ok" if r else "FAIL"); sys.exit(0 if r else 1)
