"""Satisfiable side, on the formula WITHOUT the encoder's counting block (the object of this run): for each given
(K, partition file) the K-class formula must be satisfiable with the partition fixed, the model must decode to the same
partition up to the names of the classes, and the decoded grid is written out and handed to the independent checker
check.py (written on 2026-11-05 from the definition; it knows nothing about the encoders).
Usage: python crosscheck_base.py module n kind M outdir check.py sets5.txt sets6.txt K1 grid1 [K2 grid2 ...]"""
import importlib, os, subprocess, sys, time
from pysat.solvers import Solver
import counting

mod = importlib.import_module(sys.argv[1])
n, kind, M, outdir, checker = int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6]
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[7:9] for l in open(p) if l.strip()]
pairs = sys.argv[9:]
os.makedirs(outdir, exist_ok=True)
Enc = getattr(mod, 'Enc', None) or getattr(mod, 'Enc2')
ok_all = True
for i in range(0, len(pairs), 2):
    K, path = int(pairs[i]), pairs[i + 1]
    grid = [int(t) for l in open(path) if l.strip() for t in l.split()]
    assert len(grid) == n * n and len(set(grid)) == K
    t = time.time()
    E = counting.build(Enc, n, kind, K, M, sets)
    base = counting.base_clauses(E)
    order = {}
    for x in grid:
        order.setdefault(x, len(order))
    lits = [E.X[v][order[grid[v]]] for v in range(n * n)]
    with Solver(name='cadical153', bootstrap_with=base) as s:
        r = s.solve(assumptions=lits)
        model = s.get_model() if r else None
    line = '%s K=%d %s: %d variables, %d clauses (counting block of %d clauses cut out) -> %s in %.1fs' % (
        sys.argv[1], K, os.path.basename(path), E.nv, len(base), E._blk[1] - E._blk[0], 'SAT' if r else 'UNSAT', time.time() - t)
    if r:
        pos = set(l for l in model if l > 0)
        lab = [next(c for c in range(K) if E.X[v][c] in pos) for v in range(n * n)]
        same = len(set(zip(grid, lab))) == K
        out = os.path.join(outdir, '%s-decoded-K%d.txt' % (sys.argv[1], K))
        open(out, 'w', newline='\n').write('\n'.join(' '.join(str(lab[a * n + b]) for b in range(n)) for a in range(n)) + '\n')
        chk = subprocess.run([sys.executable, '-I', checker, out, kind], capture_output=True, text=True)
        verdict = [l.strip() for l in chk.stdout.split('\n') if l.strip()]
        line += ' | same partition: %s | class sizes %s | check.py: %s' % (same, sorted(lab.count(c) for c in range(K)), ' / '.join(verdict[-2:]))
        ok_all &= same and bool(verdict) and verdict[-1] == 'PASS'
    else:
        ok_all = False
    print(line, flush=True)
print('CROSSCHECK BASE %s: %s' % (sys.argv[1], 'PASS' if ok_all else 'FAIL'))
sys.exit(0 if ok_all else 1)
