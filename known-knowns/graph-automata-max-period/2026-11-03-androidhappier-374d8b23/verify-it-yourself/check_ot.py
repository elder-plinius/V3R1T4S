"""Standalone checker for A357951 written from the OEIS definition (Python 3 standard library only).
A357951(n): maximum eventual cycle length of an OUTER-TOTALISTIC cellular automaton on a connected graph with n nodes,
over all connected graphs, all outer-totalistic rules and all start states. Each node is ON or OFF; all nodes update
together; with c = number of ON neighbours of a node (the node itself is NOT counted), an OFF node turns ON iff c is in
B and an ON node stays ON iff c is in S, for a rule (B, S) with B, S subsets of {0..n-1} (2^(2n) rules).
This is not A357952 (one totalistic set, node counts itself), not A357953 (one totalistic set, neighbours only, i.e.
B = S) and not A384209 (the single Game-of-Life rule on all simple graphs). State s: bit v = node v ON; graph6 order.
Rule completeness: c(v) <= deg(v) <= D (maximum degree), so membership of counts above D is never consulted and the
4^(D+1) rules over {0..D} induce every successor map that the 4^n rules over {0..n-1} induce. 'graph ... all' skips
this reduction and walks all 2^(2n) rules.
  check_ot.py outputs object/evidence        saved A/B outputs: counts, a(1..7), graph-by-graph agreement at n = 8
  check_ot.py witness G6 B S START LEN       simulate one start; B, S like 0,2 and 1,3,4 ('-' for empty)
  check_ot.py graph G6 LEN [all]             this graph over all rules and 2^n starts: max must be LEN
  check_ot.py small N                        a(1..N) over all labelled graphs, no nauty (N <= 5 is quick)"""
import itertools, os, re, sys

OEIS = [2, 2, 4, 6, 16, 26, 66]                       # A357951(1..7), OEIS DATA
A001349 = [1, 1, 2, 6, 21, 112, 853, 11117]          # connected graphs on n nodes, n = 1..8
CLAIM, WITNESS, NEXT, NEXTG = 150, "GCQfBg", 124, "G?rfUw"

def g6(s):
    n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: bits += [((ord(ch) - 63) >> (5 - b)) & 1 for b in range(6)]
    nb = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: nb[i] |= 1 << j; nb[j] |= 1 << i
            k += 1
    return n, nb

def step(n, nb, B, S, s):
    t = 0
    for v in range(n):
        c = bin(s & nb[v]).count("1")
        if (c in S) if (s >> v) & 1 else (c in B): t |= 1 << v
    return t

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

def graph_max(n, nb, allrules=False):
    """Max eventual cycle over rules (B,S) and all starts. Rule bit k = c + W*own (W = n if allrules else D+1).
    Rules are visited in Gray-code order: flipping bit k XORs delta[k] into the successor table."""
    N = 1 << n; D = max(bin(x).count("1") for x in nb) if n > 1 else 0
    W = n if allrules else D + 1; K = 2 * W
    delta = [[0] * N for _ in range(K)]
    for s in range(N):
        for v in range(n):
            delta[bin(s & nb[v]).count("1") + W * ((s >> v) & 1)][s] |= 1 << v
    nxt = [0] * N; best = (max_cycle(nxt), 0)
    for g in range(1, 1 << K):
        k = (g & -g).bit_length() - 1; d = delta[k]
        nxt = [a ^ b for a, b in zip(nxt, d)]
        m = max_cycle(nxt)
        if m > best[0]: best = (m, g ^ (g >> 1))
    m, R = best
    return m, [c for c in range(W) if R >> c & 1], [c for c in range(W) if R >> (W + c) & 1], K

def connected(n, nb):
    seen, todo = 1, 1
    while todo:
        v = (todo & -todo).bit_length() - 1; todo &= todo - 1
        new = nb[v] & ~seen; seen |= new; todo |= new
    return seen == (1 << n) - 1

def pergraph(lines):
    d = {}
    for l in lines:
        p = l.split()
        if len(p) == 2 and not l.startswith(("n=", "hist")):
            if p[0] in d: raise SystemExit("duplicate graph " + p[0])
            d[p[0]] = int(p[1])
    return d

def hist_lines(lines):
    return {int(l.split()[1]): int(l.split()[2]) for l in lines if l.startswith("hist ")}

SUM = r"n=(\d+) graphs=(\d+) maxperiod=(\d+) witness_graph6=(\S+)"

def cmd_outputs(d):
    ok = True
    rd = lambda f: open(os.path.join(d, f)).read().splitlines()
    A = [re.match(SUM, l).groups() for l in rd("A_n1_7.txt")]
    B = [re.match(SUM, l).groups() for l in rd("B_n1_7.txt")]
    for k in range(7):
        a, b = [int(x) for x in A[k][:3]], [int(x) for x in B[k][:3]]
        g = a == b == [k + 1, A001349[k], OEIS[k]]; ok &= g
        print(f"n={k+1} A graphs={a[1]} max={a[2]}  B graphs={b[1]} max={b[2]}  A001349={A001349[k]} OEIS={OEIS[k]} {'ok' if g else 'MISMATCH'}")
    allA, allB = {}, {}
    for r in range(8):
        la, lb = rd(f"A8_part{r}.txt"), rd(f"B8_part{r}.txt")
        sa = [re.match(SUM, l) for l in la if l.startswith("n=")]
        sb = [re.match(SUM, l) for l in lb if l.startswith("n=")]
        pa, pb = pergraph(la), pergraph(lb)
        g = len(sa) == len(sb) == 1 and sa[0] and sb[0] and sa[0].group(1) == sb[0].group(1) == "8"
        if g:
            ga, ma, wa = int(sa[0].group(2)), int(sa[0].group(3)), sa[0].group(4)
            gb, mb, wb = int(sb[0].group(2)), int(sb[0].group(3)), sb[0].group(4)
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
    reach = [x for x in allA if allA[x] == top[-1]]
    nxt = [x for x in allA if allA[x] == top[0]]
    g = (len(allA) == len(allB) == A001349[7] and allA == allB and top == [NEXT, CLAIM] and reach == [WITNESS]
         and nxt == [NEXTG])
    ok &= g
    print(f"n=8 total graphs A={len(allA)} B={len(allB)} (A001349(8)={A001349[7]}); A and B per-graph maxima identical: "
          f"{allA == allB}; max={top[-1]}; graphs reaching it: {reach}; next best {top[0]} on {nxt} {'ok' if g else 'MISMATCH'}")
    s = open(os.path.join(d, "A357951_8.txt")).read()
    g = f"A357951(8) = {CLAIM}" in s and WITNESS in s and "11117" in s; ok &= g
    print("A357951_8.txt states the value, witness and count:", "ok" if g else "MISMATCH")
    c = open(os.path.join(d, "completeness.txt")).read()
    g = c.count(": 11117") == 3; ok &= g
    print("completeness.txt: geng count, labelg-distinct count and A001349(8) all 11117:", "ok" if g else "MISMATCH")
    print("A357951(1..8) from saved outputs:", [int(x[2]) for x in A] + [top[-1]])
    return ok

def sets(x): return set() if x in ("", "-") else {int(t) for t in x.split(",")}

def cmd_witness(g, Bs, Ss, start, L):
    n, nb = g6(g); B, S = sets(Bs), sets(Ss)
    pre, cyc = cycle_from(lambda s: step(n, nb, B, S, s), int(start))
    deg = [bin(x).count("1") for x in nb]
    print(f"witness {g} n={n} edges={sum(deg)//2} degrees={sorted(deg)} connected={connected(n, nb)} B={sorted(B)} S={sorted(S)} "
          f"(outer-totalistic, node not counted) start={start} transient={pre} cycle_length={cyc} expected={L}")
    return cyc == int(L) and connected(n, nb)

def cmd_graph(g, L, mode=""):
    n, nb = g6(g); m, B, S, K = graph_max(n, nb, mode == "all")
    print(f"graph {g}: max over {1 << K} rules ({'all counts 0..n-1' if mode == 'all' else 'counts 0..maxdeg, complete'}) "
          f"and {1 << n} starts = {m} (first at B={B} S={S}) expected={L}")
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
