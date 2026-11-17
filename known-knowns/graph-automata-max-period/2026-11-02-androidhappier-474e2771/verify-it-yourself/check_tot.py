"""Standalone checker for A357953 written from the OEIS definition (Python 3 standard library only).
A357953(n): maximum eventual cycle length of a totalistic CA on a connected graph with n nodes, over all graphs, all
rules and all start states. Each node is ON or OFF; all nodes update together; a node is ON next iff its number of ON
neighbours (the node itself not counted) lies in the rule set R, a subset of {0..n-1}. State s: bit v = node v ON.
Graphs are graph6 strings; vertex order as in graph6.
  check_tot.py outputs object/evidence      saved A/B outputs: counts, a(1..8), agreement on a(9) = 180
  check_tot.py witness G6 RULE START LEN    simulate one start; RULE like 0,2
  check_tot.py graph G6 LEN                 this graph over all 2^n rules and 2^n starts: max must be LEN
  check_tot.py small N                      a(1..N) over all labelled graphs, no nauty (N <= 6 is quick)"""
import itertools, os, re, sys

OEIS = [1, 2, 2, 6, 7, 18, 38, 96]                  # A357953(1..8), OEIS DATA
A001349 = [1, 1, 2, 6, 21, 112, 853, 11117, 261080]  # connected graphs on n nodes, n = 1..9
CLAIM = 180

def g6(s):
    n = ord(s[0]) - 63; bits = []
    for ch in s[1:]: bits += [((ord(ch) - 63) >> (5 - b)) & 1 for b in range(6)]
    nb = [0] * n; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: nb[i] |= 1 << j; nb[j] |= 1 << i
            k += 1
    return n, nb

def succ_table(n, nb, R):
    cnt = [[bin(s & nb[v]).count("1") for v in range(n)] for s in range(1 << n)]
    return [sum(1 << v for v in range(n) if (R >> cnt[s][v]) & 1) for s in range(1 << n)]

def cycle_from(nxt, x):
    seen = {}; t = 0
    while x not in seen: seen[x] = t; x = nxt(x); t += 1
    return seen[x], t - seen[x], x

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

def cmd_outputs(d):
    ok = True
    rd = lambda f: open(os.path.join(d, f)).read().splitlines()
    # a(1..8), both programs
    A = [re.match(r"n=(\d+) mode=neighbours graphs=(\d+) maxperiod=(\d+)", l).groups() for l in rd("A_n1_8.txt")]
    B = [re.match(r"order=(\d+) connected_graphs=(\d+) max_cycle=(\d+)", l).groups() for l in rd("B_n1_8.txt")]
    for k in range(8):
        a, b = [int(x) for x in A[k]], [int(x) for x in B[k]]
        g = a == b == [k + 1, A001349[k], OEIS[k]]; ok &= g
        print(f"n={k+1} A graphs={a[1]} max={a[2]}  B graphs={b[1]} max={b[2]}  A001349={A001349[k]} OEIS={OEIS[k]} {'ok' if g else 'MISMATCH'}")
    # n = 9 parts
    totA = totB = 0; mA = mB = 0; histsum = {}; lens = set(); wit = []
    for r in range(8):
        la, lb = rd(f"A_n9_part{r}.txt"), rd(f"B_n9_part{r}.txt")
        ma = re.match(r"n=9 mode=neighbours graphs=(\d+) maxperiod=(\d+) witness_graph6=(\S+) witness_rule_mask=(\d+) witness_state=(\d+)", la[0])
        mb = re.match(r"order=9 connected_graphs=(\d+) max_cycle=(\d+) witness (\S+) rule_mask (\d+) state (\d+)", lb[0])
        ga, pa, gb, pb = int(ma.group(1)), int(ma.group(2)), int(mb.group(1)), int(mb.group(2))
        g = ga == gb and pa == pb and ma.group(3) == mb.group(3) and la[-1] == "exit 0" and lb[-1] == "exit 0"
        h = {}
        for l in la[1:-1]:
            _, k, c = l.split(); h[int(k)] = int(c)
        g &= sum(h.values()) == ga and max(h) == pa
        ok &= g
        print(f"part {r}: A graphs={ga} max={pa} | B graphs={gb} max={pb} | witness {ma.group(3)} {'ok' if g else 'MISMATCH'}")
        totA += ga; totB += gb; mA = max(mA, pa); mB = max(mB, pb)
        for k, c in h.items(): histsum[k] = histsum.get(k, 0) + c
        lens |= set(int(x) for x in lb[1].split(":")[1].split())
        if pa == CLAIM: wit.append((ma.group(3), int(ma.group(4)), int(ma.group(5)), int(mb.group(4)), int(mb.group(5))))
    g = totA == totB == A001349[8] and mA == mB == CLAIM and max(lens) == CLAIM and histsum.get(CLAIM) == 1 and len(wit) == 1
    ok &= g
    print(f"n=9 total graphs A={totA} B={totB} (A001349(9)={A001349[8]}); max A={mA} B={mB}; graphs reaching {CLAIM}: {histsum.get(CLAIM)} {'ok' if g else 'MISMATCH'}")
    # merged files agree with the parts
    am, bm = rd("A_n9_merged.txt"), rd("B_n9_merged.txt")
    g = am[0].startswith(f"total_connected_graphs {totA} ") and f"({CLAIM}, " in am[1] and am[2] == "graphs_by_max_period_over_rules %r" % sorted(histsum.items())
    g &= bm[0].startswith(f"total_connected_graphs {totB} ") and f"({CLAIM}, " in bm[1] and bm[2] == "cycle_lengths_seen %r" % sorted(lens)
    ok &= g
    print("merged summaries consistent with parts:", "ok" if g else "MISMATCH")
    if wit:
        w = wit[0]; print(f"witness from saved outputs: {w[0]} A rule_mask={w[1]} state={w[2]}; B rule_mask={w[3]} state={w[4]}")
    print("A357953(1..9) from saved outputs:", [int(x[2]) for x in A] + [mA])
    return ok

def cmd_witness(g, rule, start, L):
    n, nb = g6(g); R = sum(1 << int(c) for c in rule.split(",") if c != "")
    nxt = lambda s: sum(1 << v for v in range(n) if (R >> bin(s & nb[v]).count("1")) & 1)
    pre, cyc, _ = cycle_from(nxt, int(start))
    print(f"witness {g} n={n} edges={sum(bin(x).count('1') for x in nb)//2} connected={connected(n, nb)} rule={{{rule}}} start={start} preperiod={pre} cycle_length={cyc} expected={L}")
    return cyc == int(L) and connected(n, nb)

def cmd_same_cycle(g, rule, a, b):
    n, nb = g6(g); R = sum(1 << int(c) for c in rule.split(",") if c != "")
    nxt = lambda s: sum(1 << v for v in range(n) if (R >> bin(s & nb[v]).count("1")) & 1)
    x, orbit = int(a), set()
    while x not in orbit: orbit.add(x); x = nxt(x)
    print(f"start {b} lies on the cycle through start {a}: {int(b) in orbit} (orbit size {len(orbit)})")
    return int(b) in orbit

def cmd_graph(g, L):
    n, nb = g6(g); best = (0, None)
    for R in range(1 << n):
        m = max_cycle(succ_table(n, nb, R))
        if m > best[0]: best = (m, R)
    rule = ",".join(str(k) for k in range(n) if best[1] >> k & 1)
    print(f"graph {g}: max over all {1<<n} rules and {1<<n} starts = {best[0]} (first at rule {{{rule}}}) expected={L}")
    return best[0] == int(L)

def cmd_small(N):
    ok = True
    for n in range(1, N + 1):
        pairs = [(i, j) for j in range(1, n) for i in range(j)]
        E = len(pairs); seen = bytearray(1 << E); classes = 0; conn = 0; best = 0
        perms = list(itertools.permutations(range(n)))
        pidx = {p: k for k, p in enumerate(pairs)}
        pmap = [[pidx[(min(p[i], p[j]), max(p[i], p[j]))] for (i, j) in pairs] for p in perms]
        for m in range(1 << E):            # every labelled graph; one representative per isomorphism class
            if seen[m]: continue
            classes += 1
            for pm in pmap:
                seen[sum(1 << pm[k] for k in range(E) if m >> k & 1)] = 1
            nb = [0] * n
            for k, (i, j) in enumerate(pairs):
                if m >> k & 1: nb[i] |= 1 << j; nb[j] |= 1 << i
            if not connected(n, nb): continue
            conn += 1
            for R in range(1 << n):
                best = max(best, max_cycle(succ_table(n, nb, R)))
        g = best == OEIS[n - 1] and conn == A001349[n - 1]; ok &= g
        print(f"n={n} labelled_graphs={1<<E} iso_classes={classes} connected={conn} (A001349={A001349[n-1]}) max_period={best} oeis={OEIS[n-1]} {'ok' if g else 'MISMATCH'}")
    return ok

if __name__ == "__main__":
    c, a = sys.argv[1], sys.argv[2:]
    r = {"outputs": lambda: cmd_outputs(*a), "witness": lambda: cmd_witness(*a), "samecycle": lambda: cmd_same_cycle(*a),
         "graph": lambda: cmd_graph(*a), "small": lambda: cmd_small(int(a[0]))}[c]()
    print("ok" if r else "FAIL"); sys.exit(0 if r else 1)
