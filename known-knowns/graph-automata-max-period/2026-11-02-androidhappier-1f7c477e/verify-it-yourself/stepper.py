"""Independent witness stepper (pure Python, no shared code with lifeA/lifeB).
Usage: stepper.py <graph6> <start_state_int>. Bit v of the state = vertex v alive.
Decodes graph6 per the nauty format spec (N(n) then upper triangle column by column, 6 bits per char),
runs Conway's Life rule (live: survive iff 2 or 3 live nbrs; dead: born iff exactly 3), and prints the
pre-period and the minimal cycle length reached from the start state."""
import sys
def g6(s):
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        x = ord(ch) - 63
        bits += [(x >> (5 - b)) & 1 for b in range(6)]
    E = set(); k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: E.add((i, j))
            k += 1
    nb = [[u for u in range(n) if (min(u, v), max(u, v)) in E] for v in range(n)]
    return n, nb
def step(n, nb, st):
    alive = [(st >> v) & 1 for v in range(n)]
    out = 0
    for v in range(n):
        c = sum(alive[u] for u in nb[v])
        if c == 3 or (alive[v] and c == 2): out |= 1 << v
    return out
if __name__ == "__main__":
    s, st = sys.argv[1], int(sys.argv[2])
    n, nb = g6(s)
    seen = {}; t = 0; x = st
    while x not in seen:
        seen[x] = t; x = step(n, nb, x); t += 1
    print(f"graph6={s} n={n} edges={sum(len(a) for a in nb)//2} start={st} preperiod={seen[x]} cycle_length={t - seen[x]}")
