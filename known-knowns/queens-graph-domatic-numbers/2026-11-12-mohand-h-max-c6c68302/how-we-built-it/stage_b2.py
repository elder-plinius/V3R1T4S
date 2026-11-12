"""Final refutation with the counting bound derived INSIDE the proof.
  base     the encoder's clauses without its implied counting block (same variable numbers)      -> Fbase.cnf
  lemmas   the class lemma clauses, three per class (each proved separately from clauses of base)
  formula  base + lemmas                                                                           -> Fbase-lemmas.cnf
  proof    D, written by counting.py (definitions of new variables, then the bound in unit-propagation steps, with
           deletions), followed by the solver's refutation of  base + lemmas + the clauses that D leaves in place
  check    drat-trim (binary build) on (Fbase-lemmas.cnf, proof) must print s VERIFIED.
The solver gets the derived counter as part of its input; in the checked proof those clauses are not premises, they
are lines of D. Nothing is held in memory: D is streamed to disk and the solver's proof stream is appended to it.
Usage: python stage_b2.py module n kind K M outdir drat-trim-bin.exe sets..."""
import hashlib, importlib, json, os, subprocess, sys, tempfile, time

mod_name, n, kind, K, M, outdir, dt = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], os.path.abspath(sys.argv[7])
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[8:] for l in open(p) if l.strip()]
os.makedirs(outdir, exist_ok=True)
tempfile.tempdir = os.path.join(outdir, 'tmp'); os.makedirs(tempfile.tempdir, exist_ok=True)
from pysat.solvers import Solver
from pysat import solvers as _ps
import counting

mod = importlib.import_module(mod_name)
Enc = getattr(mod, 'Enc', None) or getattr(mod, 'Enc2')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def write_cnf(path, nv, clauses):
    with open(path, 'w', newline='\n') as f:
        f.write('p cnf %d %d\n' % (nv, len(clauses)))
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')


t0 = time.time()
E = counting.build(Enc, n, kind, K, M, sets)
base = counting.base_clauses(E)
g = min(len(S) for S in sets)
lem = []
for c in range(K):
    lem.append([E.S[c][g]])
    for size in range(g, M):
        lem.append([E.S[c][size + 1]] + [E.ZS[c][j] for j, S in enumerate(sets) if len(S) <= size])
fb = os.path.join(outdir, 'Fbase.cnf'); fl = os.path.join(outdir, 'Fbase-lemmas.cnf'); prf = os.path.join(outdir, 'proofB2.bin')
write_cnf(fb, E.nv, base)
write_cnf(fl, E.nv, base + lem)
print('%s: encoder %d clauses, counting block %d clauses removed, base %d clauses, %d lemma clauses' % (
    mod_name, len(E.clauses), E._blk[1] - E._blk[0], len(base), len(lem)), flush=True)
with open(prf, 'wb') as f:
    sink = counting.BinSink(f)
    C = counting.Counting(E, sink)
    kept = C.run()
    sink.close()
    d_bytes = f.tell()
    print('derivation: %d cells, %d new variables, %d clauses added, %d deleted, %d bytes, %d clauses left in place, %.0fs' % (
        C.cells, C.nv - E.nv, sink.n_add, sink.n_del, d_bytes, len(kept), time.time() - t0), flush=True)
    t = time.time()
    s = Solver(name='cadical153', bootstrap_with=base + lem + kept, with_proof=True)
    r = s.solve()
    ts = time.time() - t
    print('solver on base + lemmas + derived counter: %s in %.1fs' % ('SAT' if r else 'UNSAT', ts), flush=True)
    if r:
        sys.exit(2)
    _ps.pysolvers.flushpr(s.solver.prfp); s.solver.prfile.seek(0)
    for chunk in iter(lambda: s.solver.prfile.read(1 << 20), b''):
        f.write(chunk)
    f.write(b'a\x00')
    s.delete()
size = os.path.getsize(prf)
t = time.time()
rr = subprocess.run([dt, fl, prf], capture_output=True, text=True)
tv = time.time() - t
out = [l.strip() for l in rr.stdout.replace('\r', '\n').split('\n') if l.strip()]
open(os.path.join(outdir, 'drat-trim-stageB2.log'), 'w', newline='\n').write('\n'.join(out) + '\n')
status = ([l for l in out if l.startswith('s ')] or ['no status line (exit %d)' % rr.returncode])[-1]
rec = {'module': mod_name, 'base_clauses': len(base), 'block_removed': E._blk[1] - E._blk[0], 'lemmas': len(lem), 'cells': C.cells,
       'new_variables': C.nv - E.nv, 'derivation_added': sink.n_add, 'derivation_deleted': sink.n_del, 'derivation_bytes': d_bytes,
       'proof_bytes': size, 'solve_s': round(ts, 1), 'drat_trim': status, 'verify_s': round(tv, 1),
       'Fbase_sha256': sha(fb), 'Fbase_lemmas_sha256': sha(fl), 'proof_sha256': sha(prf)}
json.dump(rec, open(os.path.join(outdir, 'stageB2.json'), 'w'), indent=1)
print('proof %d bytes; drat-trim: %s in %.1fs' % (size, status, tv), flush=True)
print('STAGE B2 %s: %s' % (mod_name, 'COMPLETE, the refutation with the counting bound derived in the proof is VERIFIED' if status == 's VERIFIED' else 'NOT verified'), flush=True)
sys.exit(0 if status == 's VERIFIED' else 3)
