#!/usr/bin/env python3
"""Fresh rebuild (2026-10-17 reverify): A5 < PSL(2,19) acting on PG(1,19); min union of A5-orbits on 6-sets
covering all 3-sets. Written from scratch; does not import or read the run's code."""
import itertools, sys, json, random
from math import comb
P = 19; INF = 19            # points 0..18 = GF(19), 19 = infinity
pts = list(range(20))
def inv(a): return pow(a, P-2, P)
def apply(m, x):
    a,b,c,d = m
    if x == INF:
        return INF if c == 0 else a*inv(c) % P
    num = (a*x+b) % P; den = (c*x+d) % P
    return INF if den == 0 else num*inv(den) % P
def perm(m): return tuple(apply(m,x) for x in pts)
def compose(p,q): return tuple(p[q[x]] for x in pts)   # p after q
ident = tuple(pts)
def order(p):
    k, r = 1, p
    while r != ident: r = compose(p, r); k += 1
    return k
def closure(gens):
    G = {ident}; frontier = [ident]
    while frontier:
        nf = []
        for g in frontier:
            for h in gens:
                x = compose(h, g)
                if x not in G: G.add(x); nf.append(x)
        frontier = nf
        if len(G) > 400: return None
    return G
# all PSL(2,19) elements: det a square
squares = {x*x % P for x in range(1,P)}
psl = set()
for a,b,c,d in itertools.product(range(P), repeat=4):
    det = (a*d-b*c) % P
    if det in squares: psl.add(perm((a,b,c,d)))
print("|PSL(2,19)| =", len(psl))
inv_ = [g for g in psl if order(g)==2]; o3 = [g for g in psl if order(g)==3]
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
while True:
    x = random.choice(inv_); y = random.choice(o3)
    if order(compose(x,y)) == 5:
        G = closure([x,y])
        if G is not None and len(G) == 60: break
G = sorted(G)
print("found subgroup of order", len(G), "element orders", sorted({order(g) for g in G}))
# A5 check: order 60 with 24 elements of order 5, 20 of order 3, 15 of order 2 (A5 signature)
from collections import Counter
print("order counts", sorted(Counter(order(g) for g in G).items()))
# orbits on points
print("point orbit sizes", sorted(len({g[p] for g in G}) for p in [0]))
def orbits(k):
    seen = set(); orbs = []
    for s in itertools.combinations(pts, k):
        if s in seen: continue
        o = {tuple(sorted(g[x] for x in s)) for g in G}
        seen |= o; orbs.append(sorted(o))
    return orbs
B = orbits(6); T = orbits(3)
tidx = {t:i for i,o in enumerate(T) for t in o}
print("6-set orbits", len(B), "triple orbits", len(T))
cover = []
for o in B:
    s = o[0]; cover.append(sorted({tidx[t] for t in itertools.combinations(s,3)}))
from ortools.sat.python import cp_model
m = cp_model.CpModel(); xv = [m.NewBoolVar(f"x{i}") for i in range(len(B))]
for j in range(len(T)):
    m.AddBoolOr([xv[i] for i in range(len(B)) if j in cover[i]])
m.Minimize(sum(len(B[i])*xv[i] for i in range(len(B))))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 600; sv.parameters.num_workers = 4
st = sv.Solve(m)
print("CP-SAT status", sv.StatusName(st), "objective", sv.ObjectiveValue(), "bound", sv.BestObjectiveBound())
chosen = [i for i in range(len(B)) if sv.Value(xv[i])]
blocks = sorted({b for i in chosen for b in B[i]})
print("chosen orbit sizes", sorted(len(B[i]) for i in chosen), "blocks", len(blocks))
with open("rebuilt_C20_6_3.txt","w") as f:
    for b in blocks: f.write(" ".join(str(x+1) for x in b)+"\n")
json.dump({"G":G,"orbits6":B,"orbits3":T,"chosen":chosen}, open("rebuild_state.json","w"))
