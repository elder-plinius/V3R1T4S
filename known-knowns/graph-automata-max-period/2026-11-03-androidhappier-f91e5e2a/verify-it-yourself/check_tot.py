"""Standalone checker for A357953 written from the OEIS definition (Python 3 standard library only).
A357953(n): maximum eventual cycle length of a totalistic CA on a connected graph with n nodes, over all graphs, all
rules and all start states. Each node is ON or OFF; all nodes update together; a node is ON next iff its number of ON
neighbours (the node itself not counted) lies in the rule set R, a subset of {0..n-1}. State s: bit v = node v ON.
Graphs are graph6 strings; vertex order as in graph6.
  check_tot.py outputs object/evidence      saved A/B outputs: counts, a(1..8), class-by-class agreement on a(10) = 624
  check_tot.py witness G6 RULE START LEN    simulate one start; RULE like 0,2
  check_tot.py graph G6 LEN [all]           this graph over its rules and all 2^n starts: max must be LEN
                                            (default rules over {0..maxdeg}; 'all' = all 2^n rules, no pruning)
  check_tot.py small N                      a(1..N) over all labelled graphs, no nauty (N <= 6 is quick)"""
import itertools, os, re, sys

OEIS = [1, 2, 2, 6, 7, 18, 38, 96]                                       # A357953(1..8), OEIS DATA
A001349 = [1, 1, 2, 6, 21, 112, 853, 11117, 261080, 11716571]            # connected graphs on n nodes, n = 1..10
CLAIM = 624
CLASSES = 32

def g6(s):
    n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: bits += [((ord(ch) - 63) >> (5 - b)) & 1 for b in range(6)]
    nb = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: nb[i] |= 1 << j; nb[j] |= 1 << i
            k += 1
    return n, nb

def counts(n, nb):
    return [[bin(s & nb[v]).count("1") for v in range(n)] for s in range(1 << n)]

def succ_table(n, cnt, R):
    bit = [1 << v for v in range(n)]
    return [sum(bit[v] for v in range(n) if (R >> c[v]) & 1) for c in cnt]

def cycle_from(nxt, x):
    seen = {}; t = 0
    while x not in seen: seen[x] = t; x = nxt(x); t += 1
    return seen[x], t - seen[x]

def max_cycle(table):
    """Longest cycle of a functional graph on range(len(table)), visiting every state."""
    N = len(table); mark = [0] * N; pos = [0] * N; best = 0
    for s in range(N):
        if mark[s]: continue
        x, p = s, 0
        while not mark[x]: mark[x] = s + 1; pos[x] = p; p += 1; x = table[x]
        if mark[x] == s + 1: best = max(best, p - pos[x])
    return best

def connected(n, nb):
    seen, todo = 1, 1
    while todo:
        v = (todo & -todo).bit_length() - 1; todo &= todo - 1
        new = nb[v] & ~seen; seen |= new; todo |= new
    return seen == (1 << n) - 1

HEAD = re.compile(r"^n=(\d+) mode=neighbours graphs=(\d+) maxperiod=(\d+) witness_graph6=(\S+) witness_rule_mask=(\d+) witness_state=(\d+)", re.M)

def load(path):
    t = open(path).read()
    h = HEAD.search(t)
    fnv = re.search(r"^fnv ([0-9a-f]+)$", t, re.M)
    hist = {int(a): int(b) for a, b in re.findall(r"^hist (\d+) (\d+)$", t, re.M)}
    high = sorted((g, int(v)) for v, g in re.findall(r"^high (\d+) (\S+)$", t, re.M))
    return h, fnv, hist, high

def cmd_outputs(d):
    ok = True
    rd = lambda f: open(os.path.join(d, f)).read().splitlines()
    A = [HEAD.match(l).groups() for l in rd("A_n1_9.txt")]
    B = [HEAD.match(l).groups() for l in rd("B_n1_9.txt")]
    for k in range(8):
        a, b = [int(x) for x in A[k][:3]], [int(x) for x in B[k][:3]]
        g = a == b == [k + 1, A001349[k], OEIS[k]]; ok &= g
        print(f"n={k+1} A graphs={a[1]} max={a[2]}  B graphs={b[1]} max={b[2]}  A001349={A001349[k]} OEIS={OEIS[k]} {'ok' if g else 'MISMATCH'}")
    a9, b9 = [int(x) for x in A[8][:3]], [int(x) for x in B[8][:3]]
    g = a9 == b9 == [9, A001349[8], 180]; ok &= g
    print(f"n=9 A graphs={a9[1]} max={a9[2]}  B graphs={b9[1]} max={b9[2]} (earlier separate cell, not claimed here) {'ok' if g else 'MISMATCH'}")
    totA = totB = 0; mA = mB = 0; hsum = {}; nhigh = 0; wit = []
    for r in range(CLASSES):
        ha, fa, Ha, Xa = load(os.path.join(d, f"A10_r{r}of32.txt"))
        hb, fb, Hb, Xb = load(os.path.join(d, f"B10_r{r}of32.txt"))
        g = bool(ha and hb and fa and fb)
        if g:
            ga, pa, gb, pb = int(ha.group(2)), int(ha.group(3)), int(hb.group(2)), int(hb.group(3))
            g = (ha.group(1) == hb.group(1) == "10" and ga == gb and pa == pb and Ha == Hb and Xa == Xb and fa.group(1) == fb.group(1)
                 and sum(Ha.values()) == ga and max(Ha) == pa and all(v >= 150 for _, v in Xa)
                 and len(Xa) == sum(c for k, c in Ha.items() if k >= 150))
        ok &= g
        if not g:
            print(f"class {r}/32: incomplete or A/B MISMATCH"); continue
        print(f"class {r:2d}/32: graphs {ga} max {pa} high {len(Xa)} fnv {fa.group(1)} | A = B ok")
        totA += ga; totB += gb; mA = max(mA, pa); mB = max(mB, pb); nhigh += len(Xa)
        for k, c in Ha.items(): hsum[k] = hsum.get(k, 0) + c
        if pa == CLAIM: wit.append((r, ha.group(4), int(ha.group(5)), int(ha.group(6)), hb.group(4), int(hb.group(5)), int(hb.group(6))))
    g = totA == totB == A001349[9] and mA == mB == CLAIM and hsum.get(CLAIM) == 1 and len(wit) == 1
    ok &= g
    print(f"n=10 total graphs A={totA} B={totB} (A001349(10)={A001349[9]}); max A={mA} B={mB}; graphs reaching {CLAIM}: {hsum.get(CLAIM)}; graphs with max >= 150: {nhigh} {'ok' if g else 'MISMATCH'}")
    top = sorted(hsum)[-4:]
    print("top per-graph maxima (value:count):", " ".join(f"{k}:{hsum[k]}" for k in top))
    if wit:
        w = wit[0]; print(f"witness from saved outputs: class {w[0]} A {w[1]} rule_mask={w[2]} state={w[3]}; B {w[4]} rule_mask={w[5]} state={w[6]}")
        g = w[1] == w[4] == "I?AAD@oIg"; ok &= g
    cmp = rd("compare_AB.txt")
    g = cmp[-1] == f"VERDICT AGREE M = {CLAIM}" and sum(l.endswith(" SAME") for l in cmp) == CLASSES; ok &= g
    print("saved compare_AB.txt:", cmp[-1], "ok" if g else "MISMATCH")
    return ok

def parse_rule(rule):
    return sum(1 << int(c) for c in rule.split(",") if c != "")

def cmd_witness(g, rule, start, L):
    n, nb = g6(g); R = parse_rule(rule)
    nxt = lambda s: sum(1 << v for v in range(n) if (R >> bin(s & nb[v]).count("1")) & 1)
    pre, cyc = cycle_from(nxt, int(start))
    print(f"witness {g} n={n} edges={sum(bin(x).count('1') for x in nb)//2} connected={connected(n, nb)} rule={{{rule}}} start={start} preperiod={pre} cycle_length={cyc} expected={L}")
    return cyc == int(L) and connected(n, nb)

def cmd_graph(g, L, mode="maxdeg"):
    n, nb = g6(g); cnt = counts(n, nb)
    maxdeg = max(bin(x).count("1") for x in nb)
    nr = 1 << n if mode == "all" else 1 << (maxdeg + 1)
    best = (0, None)
    for R in range(nr):
        m = max_cycle(succ_table(n, cnt, R))
        if m > best[0]: best = (m, R)
    rule = ",".join(str(k) for k in range(n) if best[1] >> k & 1)
    print(f"graph {g}: max over {nr} rules ({'all subsets of {0..n-1}' if mode == 'all' else 'all subsets of {0..maxdeg}'}) and {1<<n} starts = {best[0]} (first at rule {{{rule}}}) expected={L}")
    return best[0] == int(L)

def cmd_small(N):
    ok = True
    for n in range(1, N + 1):
        pairs = [(i, j) for j in range(1, n) for i in range(j)]
        E = len(pairs); seen = bytearray(1 << E); classes = 0; conn = 0; best = 0
        pidx = {p: k for k, p in enumerate(pairs)}
        pmap = [[pidx[(min(p[i], p[j]), max(p[i], p[j]))] for (i, j) in pairs] for p in itertools.permutations(range(n))]
        for m in range(1 << E):            # every labelled graph; one representative per isomorphism class
            if seen[m]: continue
            classes += 1
            for pm in pmap:
                seen[sum(1 << pm[k] for k in range(E) if m >> k & 1)] = 1
            nb = [0] * n
            for k, (i, j) in enumerate(pairs):
                if m >> k & 1: nb[i] |= 1 << j; nb[j] |= 1 << i
            if not connected(n, nb): continue
            conn += 1; cnt = counts(n, nb)
            for R in range(1 << n):
                best = max(best, max_cycle(succ_table(n, cnt, R)))
        g = best == OEIS[n - 1] and conn == A001349[n - 1]; ok &= g
        print(f"n={n} labelled_graphs={1<<E} iso_classes={classes} connected={conn} (A001349={A001349[n-1]}) max_period={best} oeis={OEIS[n-1]} {'ok' if g else 'MISMATCH'}")
    return ok

if __name__ == "__main__":
    c, a = sys.argv[1], sys.argv[2:]
    r = {"outputs": lambda: cmd_outputs(*a), "witness": lambda: cmd_witness(*a),
         "graph": lambda: cmd_graph(*a), "small": lambda: cmd_small(int(a[0]))}[c]()
    print("ok" if r else "FAIL"); sys.exit(0 if r else 1)
