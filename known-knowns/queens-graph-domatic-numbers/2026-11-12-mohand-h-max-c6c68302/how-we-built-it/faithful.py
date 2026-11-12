"""Does the formula of an encoding module (enc1 or enc2) say "a domatic K-partition of the n x n queens graph exists"?
Three tests; everything about the graph and about partitions is written here from the definition, and only the
attributes X (and OCC for enc1) of the encoder are used to read its variables.

 T1 small boards, exhaustive. For n = 3 and n = 4 a direct count (dynamic programme over subsets of squares) gives the
    number of partitions into exactly K dominating classes. The formula's models, projected on the x variables, are
    enumerated: every model must decode to a domatic partition, no partition may appear twice, and the number must
    equal the direct count. M is chosen so that the implied counting constraint is present and sometimes tight.
 T2 n = 11, K = 19, the real lists of small sets. The known 19-partition is perturbed (squares moved to other classes);
    the formula with the partition fixed must be satisfiable exactly when the perturbed partition is still domatic.
 T3 n = 11, K = 20, M = 7: the formula of the claim. Its domination clauses are removed (enc2: exactly the clauses
    "class c has a square in the closed neighbourhood of v", rebuilt here; enc1: the clauses made only of positive
    line indicators of one class). What is left must be satisfiable for EVERY partition of the board into 20
    non-empty classes: random ones, ones with all classes of at most 7 squares (the counting constraint is then
    tight), extreme ones, and the 19-partition with one square split off. Sensitivity controls: with the counting
    bound lowered by one the tight partitions must become unsatisfiable, and a square left without class must be
    unsatisfiable.
Usage: python faithful.py module sets5.txt sets6.txt grid19.txt out.txt"""
import importlib, random, sys, time
from pysat.solvers import Solver

mod_name, p5, p6, pgrid, out_path = sys.argv[1:6]
BASE = len(sys.argv) > 6 and sys.argv[6] == 'base'      # test the formula WITHOUT the encoder's counting block
mod = importlib.import_module(mod_name)
EncClass = getattr(mod, 'Enc', None) or getattr(mod, 'Enc2')
if BASE:
    import counting                                      # ../../counting-in-proof/code, only to cut the block out

    def Enc(*args):
        E = counting.build(EncClass, *args)
        E.clauses = counting.base_clauses(E)
        return E
else:
    Enc = EncClass
LOG, FAILS = [], []
T0 = time.time()


def log(s=''):
    print(s, flush=True); LOG.append(s)


def check(cond, msg):
    if not cond:
        FAILS.append(msg); log('  FAIL: ' + msg)
    return cond


def nbh(n):
    """closed neighbourhoods, from coordinates"""
    N = n * n
    return [[u for u in range(N) if u == t or u // n == t // n or u % n == t % n or abs(u // n - t // n) == abs(u % n - t % n)]
            for t in range(N)]


def is_domatic(nb, lab, K):
    """every closed neighbourhood meets all K classes"""
    return len(set(lab)) == K and all(len(set(lab[u] for u in nb[t])) == K for t in range(len(lab)))


def canon(lab):
    order = {}
    for x in lab:
        order.setdefault(x, len(order))
    return tuple(order[x] for x in lab)


def fix(E, lab):
    """the x literals of a partition, classes renamed by order of first appearance"""
    return [E.X[v][c] for v, c in enumerate(canon(lab))]


# ------------------------------------------------------------------ T1
def direct_counts(n):
    N = n * n
    nbm = [sum(1 << u for u in nb) for nb in nbh(n)]
    dom = bytearray(1 << N)
    for D in range(1, 1 << N):
        dom[D] = all(D & m for m in nbm)
    B = 40                                    # one coefficient per number of classes, 40 bits each
    f = [0] * (1 << N); f[0] = 1
    for mask in range(1, 1 << N):
        low = mask & -mask; rest = mask ^ low; s = rest; acc = 0
        while True:                           # the class of the lowest square of mask is D
            D = s | low
            if dom[D]:
                acc += f[mask ^ D]
            if s == 0:
                break
            s = (s - 1) & rest
        f[mask] = acc << B
    return [(f[-1] >> (B * k)) & ((1 << B) - 1) for k in range(N + 1)]


def small_sets(n):
    nb = nbh(n); N = n * n
    out = [(v,) for v in range(N) if len(nb[v]) == N]
    out += [(a, b) for a in range(N) for b in range(a + 1, N) if len(set(nb[a]) | set(nb[b])) == N]
    return out


def projected_models(E, nb, K, cap):
    seen = set()
    with Solver(name='glucose4', bootstrap_with=E.clauses) as s:
        while s.solve():
            pos = set(l for l in s.get_model() if l > 0)
            lab = []
            for v in range(E.N):
                cs = [c for c in range(K) if E.X[v][c] in pos]
                if len(cs) != 1:
                    return 'a square is in %d classes' % len(cs)
                lab.append(cs[0])
            if not is_domatic(nb, lab, K):
                return 'a model is not a domatic partition'
            key = canon(lab)
            if key in seen:
                return 'the same partition appears twice'
            seen.add(key)
            if len(seen) > cap:
                return 'more than %d models' % cap
            s.add_clause([-E.X[v][lab[v]] for v in range(E.N)])
    return len(seen)


log('== T1 small boards, exhaustive (%s)' % mod_name)
CAP = 35000
for n, plan in ((3, [(K, M) for K in range(1, 10) for M in (1, 3, 5)]),
                (4, [(2, 9)] + [(K, M) for K in range(3, 12) for M in (2, 4)])):
    t = time.time(); cnt = direct_counts(n); nb = nbh(n); N = n * n; sets = small_sets(n)
    log('  n=%d: direct counts by number of classes K=1..: %s (%.1fs)' % (n, cnt[1:max(k for k in range(N + 1) if cnt[k]) + 2], time.time() - t))
    done = 0; skipped = set()
    for K, M in plan:
        if cnt[K] > CAP:
            if K not in skipped:
                log('  n=%d K=%d: %d partitions, more than the cap, skipped' % (n, K, cnt[K]))
            skipped.add(K); continue
        E = Enc(n, 'dom', K, M, sets)
        r = projected_models(E, nb, K, CAP)
        active = K * M > N
        check(r == cnt[K], 'n=%d K=%d M=%d: direct count %d, formula %s' % (n, K, M, cnt[K], r))
        done += 1
        if cnt[K] or K <= 9:
            log('  n=%d K=%d M=%d (counting constraint %s): direct %d, formula %s' % (
                n, K, M, 'cut out' if BASE else 'present' if active else 'absent', cnt[K], r))
    log('  n=%d: %d formulas compared, %.1fs' % (n, done, time.time() - t))

# ------------------------------------------------------------------ T2
n, N = 11, 121
nb = nbh(n)
sets = [tuple(sorted(map(int, l.split()))) for p in (p5, p6) for l in open(p) if l.strip()]
grid = [int(x) for l in open(pgrid) if l.strip() for x in l.split()]
assert len(grid) == N and len(set(grid)) == 19 and is_domatic(nb, grid, 19)
log('== T2 n=11 K=19: perturbations of the known 19-partition')
rnd = random.Random(20261111)
E = Enc(n, 'dom', 19, 7, sets)
agree = {True: 0, False: 0}
with Solver(name='cadical153', bootstrap_with=E.clauses) as s:
    cases = []
    for v in range(N):                                    # single moves that keep the partition domatic, if any
        for d in rnd.sample(sorted(set(grid) - {grid[v]}), 2):
            g = list(grid); g[v] = d
            if is_domatic(nb, g, 19):
                cases.append(g)
    safe = len(cases)
    while len(cases) < safe + 300:
        g = list(grid)
        for _ in range(rnd.randint(1, 3)):
            g[rnd.randrange(N)] = rnd.choice(sorted(set(grid)))
        if len(set(g)) == 19 and g != grid:
            cases.append(g)
    images = []
    for tr in (0, 1):                                     # the 8 symmetries of the board
        for fr in (0, 1):
            for fc in (0, 1):
                g = [0] * N
                for v in range(N):
                    r, c = divmod(v, n)
                    if tr:
                        r, c = c, r
                    g[(n - 1 - r if fr else r) * n + (n - 1 - c if fc else c)] = grid[v]
                images.append(g)
    cases += images
    for g in cases:
        want = is_domatic(nb, g, 19)
        got = s.solve(assumptions=fix(E, g))
        if check(got == want, 'perturbation: definition says %s, formula says %s' % (want, got)):
            agree[want] += 1
log('  %d cases (%d single moves that keep it domatic, 300 random, the 8 symmetric images): agreement on %d domatic and %d non-domatic' % (len(cases), safe, agree[True], agree[False]))
check(agree[True] >= 8 and agree[False] >= 1, 'T2 did not see both outcomes')

log('== T2b n=11 K=18: every merge of two classes of the 19-partition, then single moves')
E = Enc(n, 'dom', 18, 7, sets)
labs = sorted(set(grid))
agree = {True: 0, False: 0}
profiles = set()
with Solver(name='cadical153', bootstrap_with=E.clauses) as s:
    cases = []
    for i in range(19):
        for j in range(i + 1, 19):
            g = [labs[i] if x == labs[j] else x for x in grid]
            cases.append(g)
            merged = [v for v in range(N) if g[v] == labs[i]]
            for k in range(3):
                h = list(g)
                v = rnd.choice(merged) if k < 2 else rnd.randrange(N)
                h[v] = rnd.choice([x for x in labs if x != labs[j] and x != g[v]])
                if len(set(h)) == 18:
                    cases.append(h)
    for g in cases:
        want = is_domatic(nb, g, 18)
        got = s.solve(assumptions=fix(E, g))
        if check(got == want, 'merge or move: definition says %s, formula says %s' % (want, got)):
            agree[want] += 1
        if want:
            profiles.add(tuple(sorted(g.count(x) for x in set(g))))
log('  %d cases: agreement on %d domatic (with %d different size profiles) and %d non-domatic' % (len(cases), agree[True], len(profiles), agree[False]))
check(agree[True] >= 171 and agree[False] >= 1, 'T2b did not see both outcomes')

# ------------------------------------------------------------------ T3
log('== T3 n=11 K=20 M=7: the formula of the claim without its domination clauses accepts every partition')
K = 20
E = Enc(n, 'dom', K, 7, sets)
if hasattr(E, 'OCC') and any(E.OCC):
    occ = [set(o) for o in E.OCC]
    is_dom_clause = lambda cl: any(all(l > 0 and l in o for l in cl) for o in occ)
    how = 'clauses made only of positive line indicators of one class'
else:
    expected = set(tuple(sorted(E.X[u][c] for u in nb[t])) for c in range(K) for t in range(N))
    is_dom_clause = lambda cl: tuple(sorted(cl)) in expected
    how = 'clauses "class c meets the closed neighbourhood of v", rebuilt from the definition'
import hashlib
_h = hashlib.sha256(('p cnf %d %d\n' % (E.nv, len(E.clauses))).encode())
for cl in E.clauses:
    _h.update((' '.join(map(str, cl)) + ' 0\n').encode())
log('  the formula tested here, written as a DIMACS file, has sha256 %s (lists read in the order %s, %s)' % (
    _h.hexdigest(), p5.replace('\\', '/').split('/')[-1], p6.replace('\\', '/').split('/')[-1]))
rest = [cl for cl in E.clauses if not is_dom_clause(cl)]
removed = len(E.clauses) - len(rest)
log('  %d clauses, %d domination clauses removed (%s)' % (len(E.clauses), removed, how))
check(removed == K * N, 'expected %d domination clauses, found %d' % (K * N, removed))


def by_sizes(sizes):
    sq = list(range(N)); rnd.shuffle(sq)
    g = [0] * N; i = 0
    for c, sz in enumerate(sizes):
        for v in sq[i:i + sz]:
            g[v] = c
        i += sz
    assert i == N
    return g


tight_sizes = [[7] + [6] * 19, [7] * 16 + [3, 2, 2, 2], [7] * 15 + [4, 3, 3, 3, 3], [7] * 12 + [5] * 5 + [4] * 3]
slack_sizes = [[102] + [1] * 19, [50, 52, 2] + [1] * 17, [8] * 14 + [2, 2, 2, 1, 1, 1], [8] + [6] * 17 + [5, 6]]
assert all(sum(x) == N and len(x) == K for x in tight_sizes + slack_sizes)
parts = []
for sz in tight_sizes:
    parts += [('tight', by_sizes(sz)) for _ in range(25)]
for sz in slack_sizes:
    parts += [('slack', by_sizes(sz)) for _ in range(25)]
while sum(1 for k, _ in parts if k == 'random') < 100:
    g = [rnd.randrange(K) for _ in range(N)]
    if len(set(g)) == K:
        parts.append(('random', g))
for _ in range(40):
    v = rnd.randrange(N)
    if grid.count(grid[v]) >= 2:
        g = list(grid); g[v] = max(grid) + 1
        parts.append(('split', g))
tally = {}
with Solver(name='cadical153', bootstrap_with=rest) as s:
    for kind, g in parts:
        ok = s.solve(assumptions=fix(E, g))
        check(ok, 'T3: a %s partition is excluded by the non-domination clauses' % kind)
        tally[kind] = tally.get(kind, 0) + (1 if ok else 0)
    lits = fix(E, parts[0][1])
    hole = [l for l in lits if l not in E.X[5]] + [-x for x in E.X[5]]
    check(s.solve(assumptions=hole) is False, 'control: a square without class should be unsatisfiable')
log('  accepted: %s out of %d partitions; control (a square without class): rejected' % (', '.join('%s %d' % kv for kv in sorted(tally.items())), len(parts)))

# sensitivity: the counting bound lowered by one (only when the formula still has its counting block)
if BASE:
    log('  (formula without counting block: no sensitivity control to run)')
else:
    if hasattr(Enc, 'at_most'):
        orig = Enc.at_most
        Enc.at_most = lambda self, lits, bound: orig(self, lits, bound - 1)
        E2 = Enc(n, 'dom', K, 7, sets)
        Enc.at_most = orig
        occ2 = [set(o) for o in E2.OCC]
        mut = [cl for cl in E2.clauses if not any(all(l > 0 and l in o for l in cl) for o in occ2)]
    else:
        E2 = E
        last = E.clauses[-1]
        assert len(last) == 1 and last[0] < 0
        mut = [cl for cl in rest[:-1]] + [[last[0] + 1]]       # the totalizer output just below the forbidden one
        assert rest[-1] == last
    with Solver(name='cadical153', bootstrap_with=mut) as s:
        t_unsat = sum(1 for kind, g in parts if kind == 'tight' and s.solve(assumptions=fix(E2, g)) is False)
        s_sat = sum(1 for kind, g in parts if kind == 'slack' and s.solve(assumptions=fix(E2, g)) is True)
    nt = sum(1 for k, _ in parts if k == 'tight'); ns = sum(1 for k, _ in parts if k == 'slack')
    log('  sensitivity (bound lowered by one): %d of %d tight partitions rejected, %d of %d slack partitions still accepted' % (t_unsat, nt, s_sat, ns))
    check(t_unsat == nt and s_sat == ns, 'the sensitivity control did not behave as expected')

log('total time %.1fs; failures: %d' % (time.time() - T0, len(FAILS)))
log('FAITHFUL %s%s: %s' % (mod_name, ' (base formula, counting block cut out)' if BASE else '', 'PASS' if not FAILS else 'FAIL'))
open(out_path, 'w', newline='\n').write('\n'.join(LOG) + '\n')
sys.exit(0 if not FAILS else 1)
