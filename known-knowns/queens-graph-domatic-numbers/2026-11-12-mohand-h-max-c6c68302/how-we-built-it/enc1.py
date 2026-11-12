"""Encoding 1 of "the n x n queens graph has a (total) domatic K-partition", with the disclosed extras of PREREG.md.

Variables
  x(v,c)      square v is in class c                                   (v in 0..N-1, c in 0..K-1)
  cnt(c,i,m)  at least m of the squares 0..i-1 are in class c           (i in 1..N, m in 1..M)   [two-way definition]
  s(c,m)      = cnt(c,N,m): class c has at least m squares
  zs(c,j)     class c contains every square of the listed set S_j      [two-way definition]
  occ(c,L)    (dom only) class c has a square on the line L (row, column or diagonal)   [two-way definition]
Constraints
  each square in exactly one class; each class dominates (dom: closed neighbourhoods; tdom: open);
  symmetry breaking: class c+1 may contain square v only if class c contains a square before v;
  implied constraint: sum over c of min(|class c|, M) <= N, written on the bits s(c,1..M) with a sequential counter.
The generator is deterministic. It can also write the DIMACS file and a variable map.
"""
import itertools


class Enc:
    def __init__(self, n, kind, K, M, sets):
        self.n, self.N, self.kind, self.K, self.M = n, n * n, kind, K, M
        self.sets = [tuple(S) for S in sets]
        self.nv = 0
        self.clauses = []
        N = self.N
        self.X = [[self.new() for c in range(K)] for v in range(N)]
        self.nb = [[t for t in range(N) if self.dominates(v, t)] for v in range(N)]   # squares dominated by v
        self.dom_by = [[v for v in range(N) if self.dominates(v, t)] for t in range(N)]
        # exactly one class per square
        for v in range(N):
            self.add(self.X[v])
            for a, b in itertools.combinations(range(K), 2):
                self.add([-self.X[v][a], -self.X[v][b]])
        # every class dominates
        self.OCC = [[] for c in range(K)]
        if kind == 'dom':
            # line indicators, two-way definitions: occ(c, line) <-> some square of the line is in class c.
            # A square is dominated by class c iff its row, its column or one of its two diagonals is occupied
            # (closed neighbourhood = union of the four lines through the square).
            lines = []
            for r in range(n):
                lines.append([r * n + q for q in range(n)])
            for q in range(n):
                lines.append([r * n + q for r in range(n)])
            for d in range(-(n - 1), n):
                lines.append([r * n + (r - d) for r in range(n) if 0 <= r - d < n])
            for d in range(2 * n - 1):
                lines.append([r * n + (d - r) for r in range(n) if 0 <= d - r < n])
            self.lines = lines
            through = [[i for i, L in enumerate(lines) if t in L] for t in range(N)]
            for c in range(K):
                occ = []
                for L in lines:
                    o = self.new(); occ.append(o)
                    for v in L:
                        self.add([-self.X[v][c], o])
                    self.add([-o] + [self.X[v][c] for v in L])
                self.OCC[c] = occ
                for t in range(N):
                    assert len(through[t]) == 4
                    self.add([occ[i] for i in through[t]])
        else:
            for c in range(K):
                for t in range(N):
                    self.add([self.X[v][c] for v in self.dom_by[t]])
        # size counters, two-way definitions
        self.CNT = [[[0] * (M + 1) for i in range(N + 1)] for c in range(K)]
        for c in range(K):
            for i in range(1, N + 1):
                x = self.X[i - 1][c]
                for m in range(1, M + 1):
                    if m > i:
                        continue                       # constant false, never created
                    y = self.new()
                    self.CNT[c][i][m] = y
                    prev_m = self.CNT[c][i - 1][m] if m <= i - 1 else None          # None = false
                    prev_m1 = True if m == 1 else (self.CNT[c][i - 1][m - 1] if m - 1 <= i - 1 else None)
                    # y <- prev_m
                    if prev_m is not None:
                        self.add([-prev_m, y])
                    # y <- x and prev_m1
                    if prev_m1 is True:
                        self.add([-x, y])
                    elif prev_m1 is not None:
                        self.add([-x, -prev_m1, y])
                    # y -> prev_m or x ; y -> prev_m or prev_m1
                    self.add([-y, x] + ([prev_m] if prev_m is not None else []))
                    if prev_m1 is not True:
                        self.add([-y] + ([prev_m] if prev_m is not None else []) + ([prev_m1] if prev_m1 is not None else []))
        self.S = [[self.CNT[c][N][m] for m in range(M + 1)] for c in range(K)]       # S[c][m], m >= 1
        # symmetry breaking by first appearance
        for c in range(K - 1):
            for v in range(N):
                before = self.CNT[c][v][1] if v >= 1 else None
                self.add([-self.X[v][c + 1]] + ([before] if before is not None else []))
        # implied constraint: at most N of the K*M bits s(c,m) are true (sequential counter, one-way is enough)
        bits = [self.S[c][m] for c in range(K) for m in range(1, M + 1)]
        self.at_most(bits, N)
        # "class contains S_j" indicators, two-way
        self.ZS = [[0] * len(self.sets) for c in range(K)]
        for c in range(K):
            for j, S in enumerate(self.sets):
                z = self.new()
                self.ZS[c][j] = z
                for v in S:
                    self.add([-z, self.X[v][c]])
                self.add([z] + [-self.X[v][c] for v in S])

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, cl):
        self.clauses.append(list(cl))

    def dominates(self, v, t):
        n = self.n
        r1, c1, r2, c2 = v // n, v % n, t // n, t % n
        if v == t:
            return self.kind == 'dom'
        return r1 == r2 or c1 == c2 or r1 - c1 == r2 - c2 or r1 + c1 == r2 + c2

    def at_most(self, lits, bound):
        """Sinz sequential counter: at most `bound` of lits are true. r[i][j]: at least j+1 of the first i+1 lits."""
        L = len(lits)
        if bound >= L:
            return
        r = [[self.new() for j in range(bound)] for i in range(L - 1)]
        self.add([-lits[0], r[0][0]])
        for j in range(1, bound):
            self.add([-r[0][j]])
        for i in range(1, L - 1):
            self.add([-lits[i], r[i][0]])
            self.add([-r[i - 1][0], r[i][0]])
            for j in range(1, bound):
                self.add([-lits[i], -r[i - 1][j - 1], r[i][j]])
                self.add([-r[i - 1][j], r[i][j]])
            self.add([-lits[i], -r[i - 1][bound - 1]])
        self.add([-lits[L - 1], -r[L - 2][bound - 1]])

    def write_dimacs(self, path):
        with open(path, 'w', newline='\n') as f:
            f.write('p cnf %d %d\n' % (self.nv, len(self.clauses)))
            for cl in self.clauses:
                f.write(' '.join(map(str, cl)) + ' 0\n')

    def partition_assumptions(self, grid):
        """grid: list of N labels. Relabel by first appearance (symmetry breaking) and return the x literals."""
        order = {}
        for lab in grid:
            if lab not in order:
                order[lab] = len(order)
        assert len(order) == self.K, 'the grid has %d classes, the formula %d' % (len(order), self.K)
        return [self.X[v][order[grid[v]]] for v in range(self.N)]

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        return [next(c for c in range(self.K) if self.X[v][c] in pos) for v in range(self.N)]


def load_sets(*paths):
    out = []
    for p in paths:
        out += [tuple(sorted(map(int, l.split()))) for l in open(p) if l.strip()]
    return out


def load_grid(path):
    return [int(t) for l in open(path) if l.strip() for t in l.split()]
