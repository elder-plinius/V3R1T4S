"""Compare our encoder (ours/, the certificate's cube.py/cube3.py, unchanged) with an independent second encoder (enc2/enc2.py,
written from the paper by a fresh agent that never saw ours). Usage: python -I compare.py [phase ...]   (phases: A B C; default all)
Both use the same arc variables: 1..m*C(n,2), t outer, then i<j lexicographic, true = i beats j in T_t.
A  small cells, every level-1 cube: same SAT/UNSAT per cube; each cell's answer (any cube SAT) equals enc2's plain Def 2.1 CNF with
   no cube; and on many full arc assignments (each side's models, their 1-3 arc flips, random ones) both CNFs with the arcs as unit
   clauses give the same answer as a direct check (checker.py: S_k, and the cube's constraints read off the matrices).
B  seeded samples of the real cells: 30 level-1 cubes of (2,5,13) and 20 quick level-1 leaves of (3,6,12); both must be UNSAT.
C  the two upper-bound witnesses (2,5,14) and (3,6,13): as units both CNFs are SAT; every single-arc flip gives the same answer on
   both CNFs and the direct check.
Each line: phase, case, ours, enc2, (expected), agree. Last line: AGREE or DISAGREE (or INCOMPLETE if a solve timed out)."""
import sys, os, json, random, itertools, time, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, 'ours'), os.path.join(HERE, 'enc2')]
import cube3, checker, enc2  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

def narcs(m, n): return m * n * (n - 1) // 2

def cnf(side, m, k, n, cube):
    if side == 'enc2' and cube is None: return enc2.base_cnf(m, k, n)
    if side == 'enc2': return enc2.cube_cnf(m, k, n, *cube)
    nv, cl, _ = cube3.build3(m, k, n, *cube, None, None); return nv, cl

def solve(nv, cl, units=(), model=False):
    with Solver(name='cadical195', bootstrap_with=cl) as s:
        r = s.solve(assumptions=list(units))
        return r, ([l for l in s.get_model()[:nv]] if r and model else None)

def mats_of(arcs, m, n):  # arcs: dict var -> bool
    A = [[[0] * n for _ in range(n)] for _ in range(m)]; v = 0
    for t in range(m):
        for i in range(n):
            for j in range(i + 1, n):
                v += 1
                if arcs[v]: A[t][i][j] = 1
                else: A[t][j][i] = 1
    return A

def cube_ok(A, m, n, d, a, b):  # the cube's constraints, read directly off the matrices
    if any(sum(row) > d for T in A for row in T): return False
    if A[0][0][1:] != [1 if 1 <= u <= d else 0 for u in range(1, n)]: return False
    if A[1][0][1:] != [1 if 1 <= u <= a or d + 1 <= u <= d + b else 0 for u in range(1, n)]: return False
    return not (m >= 3 and sum(A[2][0]) > a + b)

def truth(A, m, k, n, cube):
    return checker.undominated(A, k) == 0 and (cube is None or cube_ok(A, m, n, *cube))

def l1_cubes(n): return [(d, a, b) for d in range(n // 2, n) for a in range(d + 1) for b in range(n - d) if a + b <= d]

def _job(q, side, m, k, n, cube):
    t0 = time.time(); nv, cl = cnf(side, m, k, n, cube); r, mod = solve(nv, cl, model=True)
    q.put((r, mod[:narcs(m, n)] if mod else None, nv, len(cl), round(time.time() - t0, 1)))

def run(side, m, k, n, cube, timeout):
    """Solve in a child process (killed after timeout). Returns (SAT|UNSAT|TIMEOUT, arc model or None, vars, clauses, seconds)."""
    q = mp.Queue(); p = mp.Process(target=_job, args=(q, side, m, k, n, cube)); p.start(); p.join(timeout)
    if p.is_alive(): p.terminate(); p.join(); return 'TIMEOUT', None, 0, 0, timeout
    r, mod, nv, ncl, s = q.get()
    return ('SAT' if r else 'UNSAT'), mod, nv, ncl, s

BAD = []; TO = []
def out(*f, ok=True):
    print('\t'.join(map(str, f)) + ('' if ok else '\tDISAGREE'), flush=True)
    if not ok: BAD.append(f)

def extensional(tag, m, k, n, cube, assigns):
    """assigns: list of arc tuples (+v/-v). Both CNFs with the arcs as assumptions vs the direct check."""
    built = {s: cnf(s, m, k, n, cube) for s in ('ours', 'enc2')} if cube is not None else {'enc2': cnf('enc2', m, k, n, None)}
    sv = {s: Solver(name='cadical195', bootstrap_with=cl) for s, (nv, cl) in built.items()}
    nt = ns = nbad = 0
    for arcs in assigns:
        A = mats_of({abs(l): l > 0 for l in arcs}, m, n); want = truth(A, m, k, n, cube)
        got = {s: sv[s].solve(assumptions=list(arcs)) for s in sv}
        nt += 1; ns += want
        if any(g != want for g in got.values()): nbad += 1; out('ext', tag, got, 'expected', want, ok=False)
    for s in sv.values(): s.delete()
    out('ext', tag, f'{nt} assignments ({ns} satisfying) agree on {"+".join(sorted(sv))} and the direct check' if not nbad else f'{nt} assignments, {nbad} disagree')

def variants(model, rng, nflip=20):
    vs = [tuple(model)]
    for _ in range(nflip):
        f = set(rng.sample(range(len(model)), rng.randint(1, 3)))
        vs.append(tuple(-l if i in f else l for i, l in enumerate(model)))
    return vs

def random_assign(m, n, cube, rng):
    """Random arcs, except the cube's fixed rows of vertex 0 in T_1, T_2 (so the cube's other constraints are what is tested)."""
    d, a, b = cube; arcs = []; v = 0
    for t in range(m):
        for i in range(n):
            for j in range(i + 1, n):
                v += 1
                if i == 0 and t == 0: x = j <= d
                elif i == 0 and t == 1: x = j <= a or d + 1 <= j <= d + b
                else: x = rng.random() < 0.5
                arcs.append(v if x else -v)
    return tuple(arcs)

def phase_A(rng):
    cells = [(1, 1, 3), (1, 2, 6), (1, 2, 7), (2, 2, 4), (2, 2, 5), (2, 3, 6), (2, 3, 7), (2, 3, 8), (2, 4, 9), (2, 4, 10),
             (3, 2, 4), (3, 3, 6), (3, 3, 7)]
    for m, k, n in cells:
        anyours = False
        for cube in (l1_cubes(n) if m >= 2 else []):  # the normal form needs two tournaments; one-tournament cells test enc2 alone
            r = {s: run(s, m, k, n, cube, 600) for s in ('ours', 'enc2')}
            res = {s: r[s][0] for s in r}
            if 'TIMEOUT' in res.values(): TO.append((m, k, n, cube)); out('A', (m, k, n), cube, res, 'timeout'); continue
            out('A', (m, k, n), cube, res['ours'], res['enc2'], ok=res['ours'] == res['enc2'])
            anyours |= res['ours'] == 'SAT'
            assigns = [random_assign(m, n, cube, rng) for _ in range(20)]
            for s in r:
                if r[s][1]: assigns += variants(r[s][1], rng)
            extensional(f'{(m, k, n)} {cube}', m, k, n, cube, assigns)
        base = run('enc2', m, k, n, None, 1200)
        if base[0] == 'TIMEOUT': TO.append((m, k, n)); out('A', (m, k, n), 'cell', 'timeout'); continue
        if m == 1:
            known = 'SAT' if n >= {1: 3, 2: 7}[k] else 'UNSAT'  # classical: least n is 3 for S_1, 7 for S_2 (one tournament)
            out('A', (m, k, n), 'cell: known', known, 'enc2 plain (no cube)', base[0], ok=base[0] == known)
        else:
            out('A', (m, k, n), 'cell: some cube SAT (ours, normal form)', 'SAT' if anyours else 'UNSAT', 'enc2 plain (no cube)', base[0],
                ok=(base[0] == 'SAT') == anyours)
        if base[1]: extensional(f'{(m, k, n)} plain', m, k, n, None, variants(base[1], rng, 40))

def phase_B(rng):
    hard = {'6_0_0', '6_1_0', '6_0_2'}
    rows = [l.split('\t') for l in open(os.path.join(HERE, 'l1_m2k5n13.tsv')).read().splitlines()]
    pick5 = random.Random(20261103).sample([r[0] for r in rows if r[0].split('/')[1] not in hard], 30)
    rows = [l.split('\t') for l in open(os.path.join(HERE, 'l1_m3k6n12.tsv')).read().splitlines()]
    pick6 = random.Random(20261103).sample([r[0] for r in rows if float(r[1]) < 20], 20)
    for job in pick5 + pick6:
        cell, cid = job.split('/'); m, k, n = {'m2k5n13': (2, 5, 13), 'm3k6n12': (3, 6, 12)}[cell]
        cube = tuple(map(int, cid.split('_')))
        r = {s: run(s, m, k, n, cube, 900) for s in ('ours', 'enc2')}
        res = {s: r[s][0] for s in r}
        if 'TIMEOUT' in res.values(): TO.append(job)
        out('B', job, f'ours {res["ours"]} ({r["ours"][4]} s, {r["ours"][2]} vars)', f'enc2 {res["enc2"]} ({r["enc2"][4]} s, {r["enc2"][2]} vars)',
            ok=all(v in ('UNSAT', 'TIMEOUT') for v in res.values()))
        extensional(job, m, k, n, cube, [random_assign(m, n, cube, rng) for _ in range(10)])

def phase_C(rng):
    for f, (m, k, n, cube) in {'witness_cube_m2k5n14_d10a0b0.json': (2, 5, 14, (10, 0, 0)),
                               'witness_cube_m3k6n13_d11a7b0.json': (3, 6, 13, (11, 7, 0))}.items():
        A = json.load(open(os.path.join(HERE, f))); v = 0; arcs = []
        for t in range(m):
            for i in range(n):
                for j in range(i + 1, n): v += 1; arcs.append(v if A[t][i][j] else -v)
        assert truth(A, m, k, n, cube), f'{f}: witness fails the direct check'
        flips = [tuple(-l if i == x else l for i, l in enumerate(arcs)) for x in range(len(arcs))]
        extensional(f'{f} and its {len(flips)} single-arc flips', m, k, n, cube, [tuple(arcs)] + flips)

if __name__ == '__main__':
    rng = random.Random(20261103); t0 = time.time()
    for ph in (sys.argv[1:] or ['A', 'B', 'C']): globals()['phase_' + ph](rng)
    print(f'# {round(time.time() - t0)} s')
    print('DISAGREE' if BAD else 'INCOMPLETE' if TO else 'AGREE')
