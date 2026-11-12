"""Rebuild, WITHOUT any solver and without the saved files, every formula of the chain of one encoding (L1, L2, the 31
pieces and the glue of each of the K classes) from the encoder and the lists, and compare its sha256 with the one in
the manifest. So a reader who has only the generator, the lists and the manifest can check that the 34*K formulas
whose refutations are recorded are exactly the ones the construction prescribes. It also checks, on the rebuilt
formulas, how they compose (every clause is a clause of the base formula, an earlier lemma or case clause, or a
unit negating the formula's own target). What it cannot check is that each formula is unsatisfiable: that needs the
proofs (or a solver).
Pure Python, standard library only. Usage: python regen_formulas.py module n kind K M manifest.txt sets..."""
import hashlib, importlib, sys, time

mod, n, kind, K, M, manifest = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[7:] for l in open(p) if l.strip()]
_m = importlib.import_module(mod)
Enc = getattr(_m, 'Enc', None) or getattr(_m, 'Enc2')
t0 = time.time()
E = Enc(n, kind, K, M, sets)
N = n * n
g = min(len(S) for S in sets)
want = {}
for line in open(manifest):
    t = line.split()
    if len(t) > 4 and t[0] == mod:
        want[(t[1], t[2])] = (t[3], t[4].split('=')[1])


def dom(v, t):
    r1, c1, r2, c2 = v // n, v % n, t // n, t % n
    if v == t:
        return kind == 'dom'
    return r1 == r2 or c1 == c2 or r1 - c1 == r2 - c2 or r1 + c1 == r2 + c2


def digest(form):
    h = hashlib.sha256(('p cnf %d %d\n' % (E.nv, len(form))).encode())
    for cl in form:
        h.update((' '.join(map(str, cl)) + ' 0\n').encode())
    return h.hexdigest()


D = [v for v in range(N) if dom(v, 0)]
bad = n_ok = 0
all_class = set()
per_class = []
for c in range(K):
    if hasattr(E, 'class_vars'):
        V = list(E.class_vars(c))
    else:
        V = [E.X[v][c] for v in range(N)] + [E.CNT[c][i][m] for i in range(1, N + 1) for m in range(1, M + 1) if E.CNT[c][i][m]] + list(E.ZS[c]) + list(E.OCC[c])
    per_class.append(set(V)); all_class |= set(V)
# The base formula: the encoder's clauses whose variables all belong to some class (x variables and the auxiliary
# variables of a class). The clauses of the encoder's implied counting constraint are exactly the others: each of
# them mentions a variable of its own counter, which belongs to no class.
Fset = set(tuple(sorted(cl)) for cl in E.clauses if all(abs(l) in all_class for l in cl))
print('%s: encoder %d clauses, base formula %d clauses (sha256 of its DIMACS text %s)' % (
    mod, len(E.clauses), len(Fset), digest([cl for cl in E.clauses if all(abs(l) in all_class for l in cl)])))
for c in range(K):
    own = per_class[c]
    G = [cl for cl in E.clauses if all(abs(l) in own for l in cl)]
    lem = [[E.S[c][g]]] + [[E.S[c][size + 1]] + [E.ZS[c][j] for j, S in enumerate(sets) if len(S) <= size] for size in range(g, M)]
    L3 = lem[-1]; prem = lem[:-1]
    Q = [[-E.X[D[i]][c]] + [E.X[D[j]][c] for j in range(i)] + L3 for i in range(len(D))]
    files = [('L1', G + [[-l] for l in lem[0]], [], lem[0]), ('L2', G + [lem[0]] + [[-l] for l in lem[1]], [lem[0]], lem[1])]
    for i in range(len(D)):
        files.append(('piece-%02d' % i, G + prem + Q[:i] + [[-l] for l in Q[i]], prem + Q[:i], Q[i]))
    files.append(('glue', G + prem + Q + [[-l] for l in L3], prem + Q, L3))
    for name, form, earlier, target in files:
        key = ('c%02d' % c, name)
        allowed = set(tuple(sorted(cl)) for cl in earlier) | set((-l,) for l in target)
        composed = all(tuple(sorted(cl)) in Fset or tuple(sorted(cl)) in allowed for cl in form)
        rec = want.get(key)
        ok = rec is not None and rec[0] == 's_VERIFIED' and rec[1] == digest(form) and composed
        n_ok += ok; bad += not ok
        if not ok:
            print('MISMATCH %s %s %s: %s' % (mod, key[0], key[1], 'no line in the manifest' if rec is None else 'verdict %s, same sha256: %s, composition: %s' % (rec[0], rec[1] == digest(form), composed)))
extra = len(want) - (n_ok + bad)
print('%s: %d formulas rebuilt (%d per class, %d classes); %d equal to the manifest (sha256), recorded as VERIFIED and composed as described; %d not; %d manifest lines without a rebuilt formula; %.0fs' % (
    mod, n_ok + bad, len(D) + 3, K, n_ok, bad, extra, time.time() - t0))
print('REGEN %s: %s' % (mod, 'PASS' if bad == 0 and extra == 0 and n_ok == K * (len(D) + 3) else 'FAIL'))
sys.exit(0 if bad == 0 and extra == 0 else 1)
