"""One certification job, solver step. Usage: python -I solve.py <job_id> <workdir> [noproof]
Builds the job's CNF (certlib), writes <workdir>/f.cnf, solves it with CaDiCaL 1.9.5 (pysat 'cadical195', the solver of
run 1144's proof probe) with DRAT proof logging straight to <workdir>/proof.drat (binary DRAT; nothing held in memory),
and prints one JSON line. Job ids: <cell>/<cube id> (leaf) or <cell>/COVER<level>[/<parent id>] (cover lemma)."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certlib

def parse(job):
    cell, rest = job.split('/', 1)
    if rest.startswith('COVER'):
        lv = int(rest[5]); p = ()
        if '/' in rest:
            q = rest.split('/', 1)[1].split('_')
            p = tuple(map(int, q[:3])) if lv == 2 else (int(q[0]), int(q[1]), int(q[2]), tuple(map(int, q[3].split('-'))))
        return 'cover', cell, lv, p
    q = rest.split('_')
    d, a, b = map(int, q[:3])
    if len(q) == 3: return 'leaf', cell, 1, (d, a, b)
    c = tuple(map(int, q[3].split('-')))
    if len(q) == 4: return 'leaf', cell, 2, (d, a, b, c)
    assert q[4] == 'L3'
    return 'leaf', cell, 3, (d, a, b, c, tuple(map(int, q[5:8])))

def valid(kind, cell, lv, p):
    n = certlib.CELLS[cell][2]
    if kind == 'cover': return lv == 1 and p == () or lv == 2 and p in certlib.l1_cubes(n) or lv == 3 and p[:3] in certlib.l1_cubes(n) and p[3] in certlib.l2_children(n, *p[:3])
    if p[:3] not in certlib.l1_cubes(n): return False
    if lv >= 2 and p[3] not in certlib.l2_children(n, *p[:3]): return False
    if lv == 3 and p[4] not in certlib.l3_children(n, *p[:4]): return False
    return True

def build(job):
    kind, cell, lv, p = parse(job)
    assert valid(kind, cell, lv, p), f'not a node of the cover: {job}'
    if kind == 'leaf':
        nv, cl, _ = certlib.leaf_cnf(cell, lv, p)
        assert certlib.leaf_id(cell, lv, p) == job
        return nv, cl
    nv, cl, meta = certlib.cover_cnf(cell, lv, p)
    assert certlib.cover_id(cell, lv, p) == job
    return nv, cl

if __name__ == '__main__':
    certlib.check_encoder()
    job, wd = sys.argv[1], sys.argv[2]; noproof = len(sys.argv) > 3 and sys.argv[3] == 'noproof'
    os.makedirs(wd, exist_ok=True)
    t0 = time.time()
    if job.startswith('FILE:'):  # validation only: solve a given DIMACS file (negative controls)
        cl = [list(map(int, l.split()[:-1])) for l in open(job[5:]) if l.strip() and l[0] not in 'pc']; nv = 0
    else: nv, cl = build(job)
    sha, nv, ncl = certlib.write_dimacs(os.path.join(wd, 'f.cnf'), nv, cl)
    tb = time.time() - t0
    import pysat.solvers as ps
    proof = os.path.join(wd, 'proof.drat')
    if not noproof:  # make pysat's proof trace file a named file instead of an anonymous temporary (no other change)
        ps.tempfile.TemporaryFile = lambda *a, **k: open(proof, 'w+b')
    s = ps.Solver(name='cadical195', bootstrap_with=cl, **({} if noproof else dict(with_proof=True)))
    t1 = time.time(); r = s.solve(); ts = time.time() - t1
    if not noproof: ps.pysolvers.flushpr(s.solver.prfp)
    out = dict(job=job, result='SAT' if r else 'UNSAT', vars=nv, clauses=ncl, cnf_sha256=sha, build_s=round(tb, 2), solve_s=round(ts, 2))
    if r:
        model = s.get_model(); out['model_head'] = model[:20]
    s.delete()
    print(json.dumps(out), flush=True)
