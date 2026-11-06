"""Cube of the (m,k,n) cover with level 2 and level 3 (PREREG.md/v2 of run 0844, PREREG.md of run 1144, SOUNDNESS_L3.md).
Usage: cube3.py m k n d a b c1,c2,c3,c4|- [e,a2,b2|-] [solver] [proof_path]
Base CNF and level-1/2 constraints come from cube.build (v2 always on for m>=3). Level 3 (cube3.cells, add_l3) fixes a second vertex inside the largest cell."""
import sys, json, time, os
sys.path.insert(0, 'attempts/solver/code')
import cube
from checker import undominated
from pysat.card import CardEnc, EncType

def cells(n, d, a, b, c):
    blocks = [list(range(1, a+1)), list(range(a+1, d+1)), list(range(d+1, d+b+1)), list(range(d+b+1, n))]
    out = []
    for blk, ci in zip(blocks, c):
        for part in (blk[:ci], blk[ci:]):
            if part: out.append(part)
    out.sort(key=lambda p: p[0])
    return out

def pivot_cell(n, d, a, b, c):
    cs = cells(n, d, a, b, c)
    return max(cs, key=lambda p: (len(p), -p[0]))

def l3_params(n, d, a, b, c):
    C = pivot_cell(n, d, a, b, c); z = len(C)
    return [(e, a2, b2) for e in range((z)//2, z) for a2 in range(e+1) for b2 in range(z-1-e+1)]  # e >= ceil((z-1)/2) = z//2

def add_l3(cl, lit, nv, n, d, a, b, c, e, a2, b2):
    C = pivot_cell(n, d, a, b, c); z = len(C); s = C[0]
    assert z >= 3 and (z-1+1)//2 <= e <= z-1 and 0 <= a2 <= e and 0 <= b2 <= z-1-e
    for i, u in enumerate(C[1:], 1):
        cl.append([lit(0, s, u) if i <= e else -lit(0, s, u)])
        in_A = i <= e; j = i if in_A else i - e
        want = (j <= a2) if in_A else (j <= b2)
        cl.append([lit(1, s, u) if want else -lit(1, s, u)])
    for u in C:  # s has the maximum T_1 out-degree inside C, so no vertex of C exceeds e
        enc = CardEnc.atmost(lits=[lit(0, u, w) for w in C if w != u], bound=e, top_id=nv, encoding=EncType.seqcounter)
        nv = max(nv, enc.nv); cl.extend(enc.clauses)
    return nv

def build3(m, k, n, d, a, b, c, l3=None):
    nv, cl, lit = cube.build(m, k, n, d, a, b, c, True)
    if l3 is not None: nv = add_l3(cl, lit, nv, n, d, a, b, c, *l3)
    return nv, cl, lit

if __name__ == "__main__":
    m, k, n, d, a, b = map(int, sys.argv[1:7])
    c = None if sys.argv[7] == '-' else [int(x) for x in sys.argv[7].split(',')]
    l3 = None if len(sys.argv) < 9 or sys.argv[8] == '-' else tuple(int(x) for x in sys.argv[8].split(','))
    name = sys.argv[9] if len(sys.argv) > 9 else 'cadical153'
    proof = sys.argv[10] if len(sys.argv) > 10 else None
    from pysat.solvers import Solver
    nv, cl, lit = build3(m, k, n, d, a, b, c, l3)
    kw = dict(with_proof=True) if proof else {}
    s = Solver(name=name, bootstrap_with=cl, **kw)
    t0 = time.time(); r = s.solve(); dt = time.time() - t0
    out = dict(m=m, k=k, n=n, d=d, a=a, b=b, c=c, l3=l3, v2=True, solver=name, vars=nv, clauses=len(cl), result='SAT' if r else 'UNSAT', seconds=round(dt, 1))
    if proof and not r:
        import gzip
        pr = s.get_proof(); out['proof_lines'] = len(pr)
        with gzip.open(proof, 'wt') as f: f.write('\n'.join(pr) + '\n')
    if r:
        mats = cube.matrices(s.get_model(), m, n, lit)
        out['checker_undominated'] = undominated(mats, k)
        json.dump(mats, open(f'attempts/solver/witness_cube3_m{m}k{k}n{n}_{d}_{a}_{b}_{"x" if c is None else "-".join(map(str,c))}_{"x" if l3 is None else "-".join(map(str,l3))}.json', 'w'))
    print(json.dumps(out))
