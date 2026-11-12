"""A test in which the derived bound is NEEDED, at a size between the small boards and the real one, with timings.
Formula: the base formula (no counting block) plus the unit clauses "every class has at least M squares". With
K*M > N this is unsatisfiable, but only by counting. Proof: the derivation of counting.py followed by the empty clause,
which then follows by unit propagation. So drat-trim, in its default backward mode, must check the derivation itself
(it is the core of the proof), not just skip it.
Controls: the same proof on the formula WITHOUT the unit clauses (satisfiable: must be rejected), and a derivation
cut after half of the levels (the bound of the last level is then missing: must be rejected).
(A first version used "the proof without its diag units" as a control; that was a wrong control, kept in
probe-core.first-run.txt: those units follow by unit propagation from the other clauses, so leaving them out does
not make the proof wrong and the checker rightly accepts it.)
Usage: python probe_core.py module n K M drat-trim-bin outdir"""
import importlib, os, subprocess, sys, time
import counting

mod_name, n, K, M, dt, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), os.path.abspath(sys.argv[5]), sys.argv[6]
mod = importlib.import_module(mod_name)
Enc = getattr(mod, 'Enc', None) or getattr(mod, 'Enc2')
os.makedirs(outdir, exist_ok=True)
E = counting.build(Enc, n, 'dom', K, M, [])
assert K * M > E.N
base = counting.base_clauses(E)
units = [[E.S[c][M]] for c in range(K)]
tag = os.path.join(outdir, 'core-%s-n%d-K%d-M%d' % (mod_name, n, K, M))


def write_cnf(path, clauses):
    with open(path, 'w', newline='\n') as f:
        f.write('p cnf %d %d\n' % (E.nv, len(clauses)))
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')


def drat(cnf, prf, *opts):
    t = time.time()
    r = subprocess.run([dt, cnf, prf] + list(opts), capture_output=True, text=True)
    o = [l.strip() for l in r.stdout.replace('\r', '\n').split('\n') if l.strip()]
    st = [l for l in o if l.startswith('s ')]
    core = [l for l in o if 'lemmas in core' in l]
    return (st[-1] if st else 'no status line'), time.time() - t, (core[-1] if core else '')


write_cnf(tag + '.cnf', base + units)
write_cnf(tag + '-sat.cnf', base)
for name, levels in (('proof', E.N), ('proof-half', E.N // 2)):
    with open(tag + '-' + name + '.bin', 'wb') as f:
        sink = counting.BinSink(f)
        C = counting.Counting(E, sink)
        for i in range(1, levels + 1):
            C.level(i)
        sink.close()
        f.write(b'a\x00')
    if levels == E.N:
        cells, adds, dels, size = C.cells, sink.n_add, sink.n_del, os.path.getsize(tag + '-proof.bin')
b, tb, core = drat(tag + '.cnf', tag + '-proof.bin')
f_, tf, _ = drat(tag + '.cnf', tag + '-proof.bin', '-f')
print('%s n=%d K=%d M=%d: %d cells, %d added, %d deletion lines, %d bytes' % (mod_name, n, K, M, cells, adds, dels, size))
print('  bound needed: backward %s in %.1fs (%s); forward %s in %.1fs' % (b, tb, core, f_, tf), flush=True)
c1, t1, _ = drat(tag + '-sat.cnf', tag + '-proof.bin')
c2, t2, _ = drat(tag + '.cnf', tag + '-proof-half.bin')
print('  controls: same proof on the satisfiable formula: %s; derivation cut after half of the levels: %s' % (c1, c2), flush=True)
ok = b == 's VERIFIED' and f_ == 's VERIFIED' and c1 != 's VERIFIED' and c2 != 's VERIFIED'
print('PROBE_CORE %s n=%d: %s' % (mod_name, n, 'PASS' if ok else 'FAIL'))
