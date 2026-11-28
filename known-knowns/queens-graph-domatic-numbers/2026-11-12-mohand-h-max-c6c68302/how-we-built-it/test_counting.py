"""Tests of counting.py on small boards, for one encoding module.
 A. Oracle test on satisfiable instances: every derived clause that is not a definition must follow by unit
    propagation from the base formula (the encoder's clauses WITHOUT its counting block) and the earlier steps:
    the solver's propagate() with the negated clause as assumptions must report a conflict. Deletions are ignored.
 C. drat-trim on unsatisfiable instances: formula = base; proof = the derivation (with its deletions) followed by the
    solver's refutation of "base + derived counter". Forward mode (-f) checks every line of the proof; the default
    backward mode is run too. Negative control: the same proof without one clause family must be rejected in
    forward mode.
Usage: python test_counting.py module drat-trim-bin outdir"""
import importlib, os, subprocess, sys, time
from pysat.solvers import Solver
from pysat import solvers as _ps
import counting

mod_name, dt, outdir = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
mod = importlib.import_module(mod_name)
Enc = getattr(mod, 'Enc', None) or getattr(mod, 'Enc2')
os.makedirs(outdir, exist_ok=True)
import tempfile
tempfile.tempdir = os.path.join(outdir, 'tmp'); os.makedirs(tempfile.tempdir, exist_ok=True)
LOG, FAILS = [], []


def log(s=''):
    print(s, flush=True); LOG.append(s)


def oracle(n, K, M):
    E = counting.build(Enc, n, 'dom', K, M, [])
    base = counting.base_clauses(E)
    sink = counting.ListSink()
    C = counting.Counting(E, sink)
    kept = C.run()
    tally, bad = {}, []
    with Solver(name='glucose4', bootstrap_with=base) as s:
        for kind, cl, tag in sink.steps:
            if kind == 'd':
                continue
            if tag not in ('def', 'pre'):
                st, _ = s.propagate(assumptions=[-l for l in cl])
                if st:
                    bad.append((tag, cl))
                    if len(bad) >= 5:
                        break
            tally[tag] = tally.get(tag, 0) + 1
            s.add_clause(cl)
        sat = s.solve() if not bad else None
        top = C.lev[C.N].get((K * M, C.N))           # "at least N of the bits are true": allowed by a correct bound
        tight = s.solve(assumptions=[top]) if (sat and top) else None
    ok = not bad
    log('A n=%d K=%d M=%d: block %d clauses removed, %d cells, steps %s -> %s%s%s' % (
        n, K, M, E._blk[1] - E._blk[0], C.cells, ' '.join('%s=%d' % kv for kv in sorted(tally.items())),
        'all follow by unit propagation' if ok else 'FAILS %s' % bad[:3], '' if sat is None else ' (formula still %s)' % ('SAT' if sat else 'UNSAT'),
        '' if tight is None else '; a model with exactly N true bits %s' % ('exists' if tight else 'does not exist')))
    if not ok:
        FAILS.append('oracle n=%d K=%d M=%d' % (n, K, M))


class Skip:
    """sink wrapper that leaves out one clause family (negative control)"""

    def __init__(self, inner, tag):
        self.inner, self.tag = inner, tag

    def add(self, cl, tag):
        if tag != self.tag:
            self.inner.add(cl, tag)

    def delete(self, cl):
        self.inner.delete(cl)


def drat(cnf, proof, *opts):
    r = subprocess.run([dt, cnf, proof] + list(opts), capture_output=True, text=True)
    lines = [l.strip() for l in r.stdout.replace('\r', '\n').split('\n') if l.strip()]
    st = [l for l in lines if l.startswith('s ')]
    return (st[-1] if st else 'no status line (exit %d)' % r.returncode), lines


def full(n, K, M, skip=None, false_bound=False):
    E = counting.build(Enc, n, 'dom', K, M, [])
    base = counting.base_clauses(E)
    tagname = '%s-n%d-K%d-M%d%s%s' % (mod_name, n, K, M, '-without-' + skip if skip else '', '-false-bound' if false_bound else '')
    cnf = os.path.join(outdir, tagname + '.cnf'); prf = os.path.join(outdir, tagname + '.bin')
    with open(cnf, 'w', newline='\n') as f:
        f.write('p cnf %d %d\n' % (E.nv, len(base)))
        for cl in base:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    with open(prf, 'wb') as f:
        sink = counting.BinSink(f)
        C = counting.Counting(E, Skip(sink, skip) if skip else sink)
        kept = C.run()
        if false_bound:                       # a bound that is one too strong: "fewer than N true bits at level N"
            sink.add([-C.lev[C.N][(C.K * C.M, C.N)]], 'false')
        sink.close()
        s = Solver(name='cadical153', bootstrap_with=base + kept, with_proof=True)
        r = s.solve()
        assert r is False, 'the instance should be unsatisfiable'
        _ps.pysolvers.flushpr(s.solver.prfp); s.solver.prfile.seek(0)
        for chunk in iter(lambda: s.solver.prfile.read(1 << 20), b''):
            f.write(chunk)
        f.write(b'a\x00')
        s.delete()
    t = time.time(); fwd, lf = drat(cnf, prf, '-f'); tf = time.time() - t
    t = time.time(); bwd, lb = drat(cnf, prf); tb = time.time() - t
    log('C n=%d K=%d M=%d%s%s: %d added, %d deleted, proof %d bytes; drat-trim forward: %s (%.1fs), backward: %s (%.1fs)' % (
        n, K, M, ' WITHOUT family %s' % skip if skip else '', ' WITH A FALSE BOUND ADDED' if false_bound else '',
        sink.n_add, sink.n_del, os.path.getsize(prf), fwd, tf, bwd, tb))
    with open(os.path.join(outdir, tagname + '.drat-trim.txt'), 'w', newline='\n') as f:
        f.write('forward:\n' + '\n'.join(lf) + '\nbackward:\n' + '\n'.join(lb) + '\n')
    return fwd, bwd


t0 = time.time()
for n, K, M in ((3, 3, 4), (3, 5, 2), (3, 4, 3), (4, 5, 4), (4, 8, 3), (4, 3, 6), (5, 5, 6), (6, 8, 6)):
    oracle(n, K, M)
for n, K, M in ((3, 6, 3), (3, 6, 2), (4, 9, 2), (4, 9, 4)):
    fwd, bwd = full(n, K, M)
    if fwd != 's VERIFIED' or bwd != 's VERIFIED':
        FAILS.append('drat-trim n=%d K=%d M=%d' % (n, K, M))
# Negative control, forward mode: a bound that is one too strong must be rejected.
# (Two earlier control designs were wrong and are kept in *.first-run.txt and *.second-run.txt: leaving out a clause
# family (I3, Jg, monot, and on the 3x3 board excl) does not make the proof wrong, because the checker falls back on
# its RAT rule, which unfolds the definition of W. The run without excl is still shown below, for information only.)
for n, K, M in ((4, 9, 4), (3, 6, 3)):
    full(n, K, M, skip='excl')
    fwd, bwd = full(n, K, M, false_bound=True)
    if fwd == 's VERIFIED':
        FAILS.append('negative control false bound accepted in forward mode (n=%d)' % n)
log('total %.1fs; failures: %s' % (time.time() - t0, FAILS if FAILS else 'none'))
log('TEST_COUNTING %s: %s' % (mod_name, 'PASS' if not FAILS else 'FAIL'))
open(os.path.join(outdir, 'test_counting-%s.txt' % mod_name), 'w', newline='\n').write('\n'.join(LOG) + '\n')
sys.exit(0 if not FAILS else 1)
