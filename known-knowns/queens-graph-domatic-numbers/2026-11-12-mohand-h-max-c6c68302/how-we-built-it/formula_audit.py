"""What exactly is in the base formula? This program imports NO encoder. From the definition of the problem and the
variable map (names of variable numbers) it builds, family by family, every clause the base formula is supposed to
contain, and compares the result with the DIMACS file as multisets: no clause may be missing, none may be extra.
Families (v, t squares; c classes; N = n*n squares; the graph is the queens graph, closed neighbourhoods):
  ALO   every square is in at least one class                     [bare constraint]
  AMO   no square is in two classes                               [bare constraint]
  DOM   every class dominates every square                        [bare constraint; encoding 1 states it through OCC]
  OCC   (encoding 1) OCC[c][l] <-> some square of line l is in class c            [two-way definition]
  CNT   CNT[c][i][m] <-> at least m of the squares 0..i-1 are in class c          [two-way definition]
  Q     (encoding 2) Q[c][v] <-> class c has a square with index < v              [two-way definition]
  ZS    ZS[c][j] <-> class c contains every square of the listed set j            [two-way definition]
  SB    class c+1 may contain square v only if class c contains a square before v [symmetry breaking]
Nothing else is allowed. In particular the implied counting constraint of the encoders must be absent.
Usage: python formula_audit.py varmap.json Fbase.cnf"""
import collections, hashlib, json, sys

m = json.load(open(sys.argv[1]))
n, K, M, X, ZS, CNT, sets = m['n'], m['K'], m['M'], m['X'], m['ZS'], m['CNT'], m['sets']
N = n * n
assert m['kind'] == 'dom'


def nbh(t):
    r, c = divmod(t, n)
    return [u for u in range(N) if u == t or u // n == r or u % n == c or abs(u // n - r) == abs(u % n - c)]


fam = collections.OrderedDict()


def add(name, lits):
    fam.setdefault(name, []).append(tuple(sorted(lits)))


for v in range(N):
    add('ALO', X[v])
    for a in range(K):
        for b in range(a + 1, K):
            add('AMO', [-X[v][a], -X[v][b]])
if 'OCC' in m:                                    # encoding 1
    OCC, lines = m['OCC'], m['lines']
    # the lines must be exactly the rows, columns and diagonals, and the 4 lines through t must cover exactly N[t]
    expect = [[r * n + q for q in range(n)] for r in range(n)] + [[r * n + q for r in range(n)] for q in range(n)]
    expect += [[r * n + (r - d) for r in range(n) if 0 <= r - d < n] for d in range(-(n - 1), n)]
    expect += [[r * n + (d - r) for r in range(n) if 0 <= d - r < n] for d in range(2 * n - 1)]
    assert sorted(map(sorted, lines)) == sorted(map(sorted, expect)), 'the lines are not the rows, columns and diagonals'
    through = [[l for l, L in enumerate(lines) if t in L] for t in range(N)]
    for t in range(N):
        assert sorted(set(u for l in through[t] for u in lines[l])) == nbh(t), 'lines through a square do not give its neighbourhood'
    for c in range(K):
        for l, L in enumerate(lines):
            for v in L:
                add('OCC', [-X[v][c], OCC[c][l]])
            add('OCC', [-OCC[c][l]] + [X[v][c] for v in L])
        for t in range(N):
            add('DOM', [OCC[c][l] for l in through[t]])
    for c in range(K - 1):
        for v in range(N):
            add('SB', [-X[v][c + 1]] + ([CNT[c][v][1]] if v >= 1 else []))
else:                                             # encoding 2
    Q = m['Q']
    for c in range(K):
        for t in range(N):
            add('DOM', [X[u][c] for u in nbh(t)])
        add('Q', [-Q[c][0]])
        for v in range(1, N):
            add('Q', [-Q[c][v - 1], Q[c][v]]); add('Q', [-X[v - 1][c], Q[c][v]]); add('Q', [-Q[c][v], Q[c][v - 1], X[v - 1][c]])
    for c in range(1, K):
        for v in range(N):
            add('SB', [-X[v][c], Q[c - 1][v]])
for c in range(K):                                # counters: y = CNT[c][i][m], a = CNT[c][i-1][m], b = CNT[c][i-1][m-1], x = X[i-1][c]
    for i in range(1, N + 1):
        x = X[i - 1][c]
        for mm in range(1, M + 1):
            y = CNT[c][i][mm]
            if not y:
                continue                           # no variable: the count cannot reach mm yet (encoding 1 only)
            a = CNT[c][i - 1][mm]                  # 0 = constant false
            b = True if mm == 1 else CNT[c][i - 1][mm - 1]
            if a:
                add('CNT', [-a, y])
            if b is True:
                add('CNT', [-x, y])
            elif b:
                add('CNT', [-x, -b, y])
            add('CNT', [-y, x] + ([a] if a else []))
            if b is not True:
                add('CNT', [-y] + ([a] if a else []) + ([b] if b else []))
    for j, S in enumerate(sets):
        for v in S:
            add('ZS', [-ZS[c][j], X[v][c]])
        add('ZS', [ZS[c][j]] + [-X[v][c] for v in S])
expected = collections.Counter(cl for cls in fam.values() for cl in cls)
got = collections.Counter()
nv = None
for line in open(sys.argv[2]):
    t = line.split()
    if t and t[0] == 'p':
        nv, nc = int(t[2]), int(t[3])
    elif t and t[0] != 'c':
        assert t[-1] == '0'
        got[tuple(sorted(int(x) for x in t[:-1]))] += 1
used = set(abs(l) for cl in got for l in cl)
print('%s: n=%d, K=%d, M=%d, %d listed sets; file: %d variables in the header, %d used, %d clauses, sha256 %s' % (
    m['module'], n, K, M, len(sets), nv, len(used), sum(got.values()), hashlib.sha256(open(sys.argv[2], 'rb').read()).hexdigest()))
for name, cls in fam.items():
    print('  %-4s %7d clauses' % (name, len(cls)))
missing = expected - got; extra = got - expected
print('  expected %d clauses in all; missing from the file: %d; in the file but not expected: %d' % (sum(expected.values()), sum(missing.values()), sum(extra.values())))
ok = not missing and not extra and nv == m['nv']
print('FORMULA AUDIT %s: %s' % (m['module'], 'PASS, the file is exactly these families and nothing else' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
