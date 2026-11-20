"""Third class lemma as a chain of INDEPENDENT pieces, each checked by drat-trim as soon as it is produced.
Piece i:  formula_i = G0 + L1 + L2 + Q_0 .. Q_(i-1) + (negation of Q_i as unit clauses);  a fresh solver refutes it;
          its binary DRAT stream is copied to disk (never held in memory) and checked by drat-trim-bin.exe.
Glue:     G0 + L1 + L2 + Q_0 .. Q_30 + (negation of L3 as units) is refuted by unit propagation alone
          (proof = the empty clause), also checked by drat-trim.
So for the class:  G + L1 + L2  implies  L3, by 32 drat-trim checks (G = the clauses of F that mention only
variables of that class; environment variable CLS selects the class, default 0).  (L1 and L2 from G0: checked in run 2026-11-11-2012.)
Resumable: state.json keeps the pieces already VERIFIED; a piece that is not VERIFIED stops the run.
Usage: python stage_a4.py module n kind K M outdir capSeconds drat-trim-bin.exe sets..."""
import hashlib, importlib, json, os, subprocess, sys, tempfile, time

mod, n, kind, K, M, outdir, cap, dt = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], float(sys.argv[7]), sys.argv[8]
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[9:] for l in open(p) if l.strip()]
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
L3 = lemmas[-1]; premises = lemmas[:-1]

def dom(v, t):
    r1, c1, r2, c2 = v // n, v % n, t // n, t % n
    if v == t:
        return kind == 'dom'
    return r1 == r2 or c1 == c2 or r1 - c1 == r2 - c2 or r1 + c1 == r2 + c2
D = [v for v in range(N) if dom(v, 0)]
Q = [[-E.X[D[i]][CLS]] + [E.X[D[j]][CLS] for j in range(i)] + L3 for i in range(len(D))]

def write_cnf(path, clauses):
    with open(path, 'w', newline='\n') as f:
        f.write('p cnf %d %d\n' % (E.nv, len(clauses)))
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def drat(cnf, proof, timeout):
    t = time.time()
    r = subprocess.run([dt, cnf, proof], capture_output=True, text=True, timeout=timeout)
    lines = [l.strip() for l in r.stdout.replace('\r', '\n').split('\n') if l.strip().startswith('s ')]
    return (lines[-1] if lines else 'no status line (exit %d)' % r.returncode), time.time() - t

state_path = os.path.join(outdir, 'state.json')
state = json.load(open(state_path)) if os.path.exists(state_path) else {'verified': 0, 'pieces': [], 'glue': None}
print('%s class %d: sub-formula %d clauses, %d pieces, %d already verified' % (mod, CLS, len(G0), len(D), state['verified']), flush=True)
t0 = time.time()
base = G0 + premises
for i in range(state['verified'], len(D)):
    if time.time() - t0 > cap:
        print('cap reached before piece %d; resume later' % i, flush=True); sys.exit(0)
    cnf = os.path.join(outdir, 'piece-%02d.cnf' % i); prf = os.path.join(outdir, 'piece-%02d.bin' % i)
    form = base + Q[:i] + [[-l] for l in Q[i]]
    write_cnf(cnf, form)
    t = time.time()
    s = Solver(name='cadical153', bootstrap_with=form, with_proof=True)
    r = s.solve()
    assert r is False, 'piece %d is satisfiable: the lemma is false or the list is incomplete' % i
    ts = time.time() - t
    raw = s.solver
    _ps.pysolvers.flushpr(raw.prfp)
    raw.prfile.seek(0)
    with open(prf, 'wb') as out:
        for chunk in iter(lambda: raw.prfile.read(1 << 20), b''):
            out.write(chunk)
        out.write(b'a\x00')                       # explicit empty clause (harmless if already there)
    s.delete()
    size = os.path.getsize(prf)
    status, tv = drat(cnf, prf, 6 * 3600)
    rec = {'piece': i, 'square': D[i], 'solve_s': round(ts, 1), 'proof_bytes': size, 'drat_trim': status, 'verify_s': round(tv, 1),
           'cnf_sha256': sha(cnf), 'proof_sha256': sha(prf)}
    print('piece %2d (square %3d): solved in %6.1fs, proof %10d bytes, drat-trim: %s in %7.1fs, total %.0fs' % (i, D[i], ts, size, status, tv, time.time() - t0), flush=True)
    if status != 's VERIFIED':
        state['pieces'].append(rec); json.dump(state, open(state_path, 'w'), indent=1)
        print('STOP: piece %d not verified' % i, flush=True); sys.exit(3)
    state['pieces'].append(rec); state['verified'] = i + 1
    json.dump(state, open(state_path + '.part', 'w'), indent=1); os.replace(state_path + '.part', state_path)
# glue
cnf = os.path.join(outdir, 'glue.cnf'); prf = os.path.join(outdir, 'glue.bin')
write_cnf(cnf, base + Q + [[-l] for l in L3])
open(prf, 'wb').write(b'a\x00')
status, tv = drat(cnf, prf, 3600)
state['glue'] = {'drat_trim': status, 'verify_s': round(tv, 1), 'cnf_sha256': sha(cnf), 'proof_sha256': sha(prf)}
json.dump(state, open(state_path, 'w'), indent=1)
print('glue (all Q_i give L3 by unit propagation): drat-trim: %s in %.1fs' % (status, tv), flush=True)
ok = status == 's VERIFIED' and state['verified'] == len(D)
print('STAGE A4 class %d:' % CLS, 'COMPLETE, all %d pieces and the glue step VERIFIED' % len(D) if ok else 'INCOMPLETE', flush=True)
