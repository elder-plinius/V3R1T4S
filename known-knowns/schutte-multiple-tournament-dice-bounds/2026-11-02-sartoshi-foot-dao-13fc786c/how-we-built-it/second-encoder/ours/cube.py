"""One cube of the (m,k,n) cover (PREREG.md). Usage: cube.py m k n d a b [solver]
Cube: global max out-degree d; T_1 vertex 0 beats exactly 1..d; T_2 vertex 0 beats exactly 1..a and d+1..d+b; all out-degrees <= d."""
import sys, json, time, itertools
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
sys.path.insert(0, 'attempts/solver/code')
from checker import undominated

def build(m, k, n, d, a, b, c=None, v2=False):
    nv = 0; X = {}
    for t in range(m):
        for i in range(n):
            for j in range(i+1, n):
                nv += 1; X[t, i, j] = nv
    def lit(t, v, u):
        return X[t, v, u] if v < u else -X[t, u, v]
    cl = []
    for U in itertools.combinations(range(n), k):
        ds = []
        for t in range(m):
            for v in range(n):
                if v in U: continue
                nv += 1; ds.append(nv)
                for u in U: cl.append([-nv, lit(t, v, u)])
        cl.append(ds)
    top = nv
    for t in range(m):
        for v in range(n):
            enc = CardEnc.atmost(lits=[lit(t, v, u) for u in range(n) if u != v], bound=d, top_id=top, encoding=EncType.seqcounter)
            top = max(top, enc.nv); cl.extend(enc.clauses)
    nv = top
    for u in range(1, n):
        cl.append([lit(0, 0, u) if u <= d else -lit(0, 0, u)])
        beats2 = (1 <= u <= a) or (d+1 <= u <= d+b)
        cl.append([lit(1, 0, u) if beats2 else -lit(1, 0, u)])
    if v2 and m >= 3:  # PREREG.v2.md: out-degree of vertex 0 in T_3 <= a+b (T_2 and T_3 ordered so that T_2 has the larger one)
        row3 = [lit(2, 0, u) for u in range(1, n)]
        if a + b == 0: cl.extend([[-l] for l in row3])
        else:
            enc = CardEnc.atmost(lits=row3, bound=a+b, top_id=nv, encoding=EncType.seqcounter)
            nv = max(nv, enc.nv); cl.extend(enc.clauses)
    if c is not None and m >= 3:  # level 2: T_3 row of vertex 0 is a prefix of size c_i in each of the four blocks (PREREG.md)
        blocks = [list(range(1, a+1)), list(range(a+1, d+1)), list(range(d+1, d+b+1)), list(range(d+b+1, n))]
        for blk, ci in zip(blocks, c):
            for idx, u in enumerate(blk): cl.append([lit(2, 0, u) if idx < ci else -lit(2, 0, u)])
    return nv, cl, lit

def matrices(model, m, n, lit):
    s = set(l for l in model if l > 0)
    out = []
    for t in range(m):
        A = [[0]*n for _ in range(n)]
        for v in range(n):
            for u in range(n):
                if u != v:
                    l = lit(t, v, u); A[v][u] = 1 if (l in s if l > 0 else -l not in s) else 0
        out.append(A)
    return out

if __name__ == "__main__":
    m, k, n, d, a, b = map(int, sys.argv[1:7]); name = 'cadical153'
    c = [int(x) for x in sys.argv[7].split(',')] if len(sys.argv) > 7 else None
    import os
    led = f'attempts/solver/ledger_m{m}k{k}n{n}.tsv'  # skip guard: a level-1 cube already final in the ledger is not re-run (two drivers share the ledger)
    if c is None and os.path.exists(led) and any(l.split('\t')[0] == f'{d}_{a}_{b}' and l.split('\t')[5] in ('SAT', 'UNSAT') for l in open(led)):
        print(json.dumps(dict(m=m, k=k, n=n, d=d, a=a, b=b, result='SKIP', seconds=0))); sys.exit(0)
    v2 = os.path.exists('attempts/solver/CUBE_V2') and m >= 3
    led2 = f'attempts/solver/ledger_m{m}k{k}n{n}_L2.tsv'  # same guard for level-2 sub-cubes (two level-2 drivers share the ledger)
    if c is not None and os.path.exists(led2) and any(l.split('\t')[0] == f'{d}_{a}_{b}_' + '-'.join(map(str, c)) and l.split('\t')[5] in ('SAT', 'UNSAT') for l in open(led2)):
        print(json.dumps(dict(m=m, k=k, n=n, d=d, a=a, b=b, c=c, result='SKIP', seconds=0))); sys.exit(0)
    nv, cl, lit = build(m, k, n, d, a, b, c, v2)
    s = Solver(name=name, bootstrap_with=cl)
    t0 = time.time(); r = s.solve(); dt = time.time() - t0
    out = dict(m=m, k=k, n=n, d=d, a=a, b=b, c=c, v2=v2, solver=name, vars=nv, clauses=len(cl), result='SAT' if r else 'UNSAT', seconds=round(dt, 1))
    if r:
        mats = matrices(s.get_model(), m, n, lit)
        out['checker_undominated'] = undominated(mats, k)
        json.dump(mats, open(f'attempts/solver/witness_cube_m{m}k{k}n{n}_d{d}a{a}b{b}c{"-".join(map(str, c)) if c else "x"}.json', 'w'))
    print(json.dumps(out))
