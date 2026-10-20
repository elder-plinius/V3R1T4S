#!/usr/bin/env python3
"""Standalone rebuild of a C(29,5,3) orbit cover under PSL(2,7) acting on 14+14+1 points.
PSL(2,7) (order 168) is generated on PG(1,7) by x->x+1, x->2x, x->-1/x. Its subgroups of order 12 (A4) are found
by random 2-generation (seed 1), split into conjugacy classes, and each class gives a transitive action on the 14
cosets. The G-set is the disjoint union of two such 14-point actions plus one fixed point (v=29). The 5-subsets and
3-subsets are split into orbits and the minimum-size union of 5-orbits covering every 3-orbit is searched with CP-SAT.
usage: rebuild_psl27.py CAP_SECONDS [OUTFILE]      (prints one line per A4-class pair; writes the best design)
       rebuild_psl27.py --orbits DESIGNFILE       (reports, for each pair, whether DESIGNFILE is a union of orbits)"""
import sys, itertools, random
from ortools.sat.python import cp_model

def mul(a, b): return tuple(a[b[i]] for i in range(len(b)))
def inv(a):
    r = [0] * len(a)
    for i, x in enumerate(a): r[x] = i
    return tuple(r)
def elements(gens):
    e = tuple(range(len(gens[0]))); seen = {e}; fr = [e]
    while fr:
        nf = []
        for a in fr:
            for g in gens:
                b = mul(g, a)
                if b not in seen: seen.add(b); nf.append(b)
        fr = nf
    return seen
def psl27():
    def f(fn): return tuple(fn(x) for x in range(8))
    p1 = lambda x: 7 if x == 7 else (x + 1) % 7
    p2 = lambda x: 7 if x == 7 else (2 * x) % 7
    def p3(x):
        if x == 7: return 0
        if x == 0: return 7
        return (-pow(x, 5, 7)) % 7
    return [f(p1), f(p2), f(p3)]
def a4_classes(gens):
    E = list(elements(gens)); random.seed(1); subs = set()
    for a in E: subs.add(frozenset(elements([a])))
    for _ in range(4000):
        a, b = random.choice(E), random.choice(E); subs.add(frozenset(elements([a, b])))
    classes = []; seen = set()
    for H in sorted(subs, key=len):
        if H in seen: continue
        conj = set()
        for g in E:
            gi = inv(g); conj.add(frozenset(mul(mul(g, h), gi) for h in H))
        seen |= conj; classes.append(H)
    return E, [H for H in classes if len(H) == 12]
def coset_action(gens, E, H):
    Hl = list(H); cos = {}; reps = []
    for g in E:
        if g in cos: continue
        c = frozenset(mul(g, h) for h in Hl); i = len(reps); reps.append(g)
        for x in c: cos[x] = i
    return [tuple(cos[mul(s, r)] for r in reps) for s in gens]
def gset(gens, acts):
    perms = [[] for _ in gens]; off = 0
    for pa in acts:
        for j, p in enumerate(pa): perms[j] += [x + off for x in p]
        off += len(pa[0])
    for j in range(len(gens)): perms[j].append(off)   # the fixed point
    return [tuple(p) for p in perms], off + 1
def orbits(v, k, perms):
    rep = {}; reps = []; sizes = []
    for S in itertools.combinations(range(v), k):
        S = frozenset(S)
        if S in rep: continue
        orb = {S}; st = [S]
        while st:
            y = st.pop()
            for p in perms:
                z = frozenset(p[i] for i in y)
                if z not in orb: orb.add(z); st.append(z)
        for z in orb: rep[z] = len(reps)
        reps.append(min(orb, key=sorted)); sizes.append(len(orb))
    return reps, sizes, rep
def pairs():
    gens = psl27(); E, cls = a4_classes(gens)
    acts = [coset_action(gens, E, H) for H in cls]
    for i, j in itertools.combinations_with_replacement(range(len(acts)), 2):
        perms, v = gset(gens, [acts[i], acts[j]])
        yield (i, j), perms, v
def solve(perms, v, cap):
    kreps, ksizes, krep = orbits(v, 5, perms); treps, tsizes, trep = orbits(v, 3, perms)
    md = cp_model.CpModel(); x = [md.NewBoolVar('') for _ in kreps]; byT = [[] for _ in treps]
    for i, R in enumerate(kreps):
        for j in {trep[frozenset(c)] for c in itertools.combinations(sorted(R), 3)}: byT[j].append(i)
    for l in byT: md.AddBoolOr([x[i] for i in l])
    md.Minimize(sum(ksizes[i] * x[i] for i in range(len(kreps))))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = cap; sv.parameters.num_workers = 1
    st = sv.Solve(md); blocks = []
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = {i for i in range(len(kreps)) if sv.Value(x[i])}
        blocks = sorted(sorted(p + 1 for p in S) for S, r in krep.items() if r in chosen)
    return sv.StatusName(st), len(kreps), len(treps), blocks, int(sv.BestObjectiveBound())
def main():
    if sys.argv[1] == '--orbits':
        D = {frozenset(int(t) - 1 for t in l.split()) for l in open(sys.argv[2]) if l.strip()}
        for ij, perms, v in pairs():
            closed = all(frozenset(p[i] for i in B) in D for B in D for p in perms)
            print('A4 classes', ij, 'v', v, 'design is a union of orbits:', closed)
        return
    cap = float(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'rebuilt_C29_5_3.txt'; best = None
    for ij, perms, v in pairs():
        st, nk, nt, blocks, bd = solve(perms, v, cap)
        print('A4 classes', ij, 'v', v, '5-orbits', nk, '3-orbits', nt, 'CP-SAT', st, 'blocks', len(blocks), 'bound', bd, flush=True)
        if blocks and (best is None or len(blocks) < len(best)): best = blocks
    with open(out, 'w') as f:
        for B in best: f.write(' '.join(map(str, B)) + '\n')
    print('wrote', out, 'blocks', len(best))
main()
