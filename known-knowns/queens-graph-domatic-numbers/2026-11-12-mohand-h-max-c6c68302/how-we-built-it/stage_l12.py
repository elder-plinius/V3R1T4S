"""First two class lemmas as independent refutations, each checked by drat-trim (binary proofs, nothing in memory):
   L1: G0 + (not L1)            is unsatisfiable      (class 0 has at least g squares)
   L2: G0 + L1 + (not L2)       is unsatisfiable      (class 0 has at least g+1 squares or contains a listed g-set)
Environment variable CLS selects the class (default 0); G0 below is then that class's sub-formula.
Usage: python stage_l12.py module n kind K M outdir drat-trim-bin.exe sets..."""
import hashlib, importlib, json, os, subprocess, sys, tempfile, time

mod, n, kind, K, M, outdir, dt = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7]
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[8:] for l in open(p) if l.strip()]
os.makedirs(outdir, exist_ok=True)
tmpdir = os.path.join(outdir, 'tmp'); os.makedirs(tmpdir, exist_ok=True)
tempfile.tempdir = tmpdir
from pysat.solvers import Solver
from pysat import solvers as _ps

_m = importlib.import_module(mod)
Enc = getattr(_m, 'Enc', None) or getattr(_m, 'Enc2')
E = Enc(n, kind, K, M, sets)
N = n * n
g = min(len(S) for S in sets)
CLS = int(os.environ.get('CLS', '0'))            # the class whose lemmas are proved (default: class 0)
if hasattr(E, 'class_vars'):
    V0 = list(E.class_vars(CLS))
else:
    V0 = [E.X[v][CLS] for v in range(N)] + [E.CNT[CLS][i][m] for i in range(1, N + 1) for m in range(1, M + 1) if E.CNT[CLS][i][m]] + list(E.ZS[CLS]) + list(E.OCC[CLS])
own = set(V0)
G0 = [cl for cl in E.clauses if all(abs(l) in own for l in cl)]
lemmas = [[E.S[CLS][g]]] + [[E.S[CLS][size + 1]] + [E.ZS[CLS][j] for j, S in enumerate(sets) if len(S) <= size] for size in range(g, M)]

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

res = []
for li in (0, 1):
    form = G0 + lemmas[:li] + [[-l] for l in lemmas[li]]
    cnf = os.path.join(outdir, 'L%d.cnf' % (li + 1)); prf = os.path.join(outdir, 'L%d.bin' % (li + 1))
    with open(cnf, 'w', newline='\n') as f:
        f.write('p cnf %d %d\n' % (E.nv, len(form)))
        for cl in form:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    t = time.time()
    s = Solver(name='cadical153', bootstrap_with=form, with_proof=True)
    r = s.solve(); assert r is False, 'lemma L%d is false' % (li + 1)
    ts = time.time() - t
    _ps.pysolvers.flushpr(s.solver.prfp); s.solver.prfile.seek(0)
    with open(prf, 'wb') as out:
        for chunk in iter(lambda: s.solver.prfile.read(1 << 20), b''):
            out.write(chunk)
        out.write(b'a\x00')
    s.delete()
    t = time.time()
    rr = subprocess.run([dt, cnf, prf], capture_output=True, text=True, timeout=3 * 3600)
    lines = [l.strip() for l in rr.stdout.replace('\r', '\n').split('\n') if l.strip().startswith('s ')]
    status = lines[-1] if lines else 'no status line'
    rec = {'lemma': 'L%d' % (li + 1), 'literals': len(lemmas[li]), 'solve_s': round(ts, 1), 'proof_bytes': os.path.getsize(prf), 'drat_trim': status,
           'verify_s': round(time.time() - t, 1), 'cnf_sha256': sha(cnf), 'proof_sha256': sha(prf)}
    res.append(rec)
    print('%s class %d L%d (%d literals): solved in %.1fs, proof %d bytes, drat-trim: %s in %.1fs' % (mod, CLS, li + 1, len(lemmas[li]), ts, rec['proof_bytes'], status, rec['verify_s']), flush=True)
json.dump(res, open(os.path.join(outdir, 'l12.json'), 'w'), indent=1)
print('STAGE L12:', 'COMPLETE' if all(r['drat_trim'] == 's VERIFIED' for r in res) else 'INCOMPLETE', flush=True)
