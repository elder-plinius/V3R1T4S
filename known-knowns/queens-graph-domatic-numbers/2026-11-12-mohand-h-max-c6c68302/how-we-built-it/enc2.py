"""Independent SAT encoding (Enc2) of the (total) domatic K-partition problem
on the n x n queens graph.

Square index v = r*n + c.  Two distinct squares are adjacent iff they share a
row, a column or a diagonal.

Variables
---------
X[v][c]      square v belongs to class c (v in 0..n^2-1, c in 0..K-1).
Q[c][v]      "class c contains a square with index strictly smaller than v"
             (two-way definition, chain  Q[c][0] = false,
             Q[c][v] <-> Q[c][v-1] or X[v-1][c]).  Used only by the symmetry
             breaking.
R[c][i][m]   sequential-counter cell: "among squares 0..i-1, at least m are in
             class c" (i = 1..n^2, m = 1..M).  Full two-way definition
             R[i][m] <-> R[i-1][m] or (X[i-1] and R[i-1][m-1]), with
             R[0][m] = false and R[i][0] = true.  Cells with m > i are
             therefore forced false by the clauses.
S[c][m]      (m = 1..M, S[c][0] is None) is the *same variable* as
             R[c][n^2][m]: true iff class c has at least m squares.
ZS[c][j]     true iff class c contains every square of sets[j]
             (two-way: ZS -> each X, and (all X) -> ZS).  An empty tuple gives
             a ZS that is forced true.
T...         global auxiliary variables of the totalizer of constraint (c).
             They belong to no single class.

Constraints
-----------
* Exactly one class per square: one at-least-one clause and pairwise
  at-most-one clauses.
* Domination, stated directly: for every class c and every square v one clause
  "OR of X[u][c] for u in N(v)", where N(v) is the closed neighbourhood
  (v and its attackers) for kind "dom" and the open neighbourhood (attackers
  only, v excluded) for kind "tdom".  (For n = 1 and "tdom" this is the empty
  clause, i.e. UNSAT, which is correct.)
* (a) Auxiliary definitions: the sequential counter (size counting, two-way),
  the ZS definitions (two-way) and the Q chain (two-way).
* (b) Symmetry breaking, "classes ordered by smallest square" (value
  precedence): for c >= 1 and every square v:  X[v][c] -> Q[c-1][v], i.e. a
  square may be in class c only if class c-1 already has a strictly smaller
  square.  Together with Q[c][0] = false this forces min(class 0) < min(class 1)
  < ... < min(class K-1) (in particular square 0 is in class 0).  Sound: any
  partition into K non-empty classes can be relabelled by increasing minimal
  square.  (A valid dominating class is never empty, so every class is
  non-empty.)  Every clause of this kind mentions two classes, and the unit
  clause "not Q[c][0]" is written for every class, so the per-class pure
  clause sets stay isomorphic under class renaming.
* (c) Implied constraint by double counting: sum over classes of
  min(|class|, M) <= n^2.  Since S[c][1..M] are the unary (sorted) bits of
  min(|class c|, M), the sum is the number of true S bits.  Encoded with my own
  *totalizer* (binary tree of unary merges, leaves = the M bits of each class,
  merged pairwise), one-directional (A_i and B_j -> O_{i+j}) and saturated at
  n^2+1 outputs; finally the unit clause "not O_{n^2+1}".  Only the direction
  "true count forces output" is encoded, which is enough to forbid sums > n^2
  and keeps every genuine solution (set the outputs to their exact values).
  If K*M <= n^2 the constraint is trivially true and nothing is added.

Attributes: n, kind, K, M, sets, nv, clauses, X, Q, R, S, ZS.
Methods: class_vars(c), decode(model), partition_literals(labels),
write_dimacs(path).

class_vars(c) = [X[v][c] for v] + [Q[c][v] for v] + [R[c][i][m] for i, m in
row-major order, i=1..n^2, m=1..M] + [ZS[c][j] for j].  The S variables are
included through R.  Same order for every c.
"""


def queens_neighbours(n):
    """open neighbourhoods: list of sorted lists of attacked squares."""
    nb = []
    for v in range(n * n):
        r, c = divmod(v, n)
        lst = []
        for u in range(n * n):
            if u == v:
                continue
            r2, c2 = divmod(u, n)
            if r == r2 or c == c2 or r - c == r2 - c2 or r + c == r2 + c2:
                lst.append(u)
        nb.append(lst)
    return nb


class Enc2:
    def __init__(self, n, kind, K, M, sets):
        if kind not in ("dom", "tdom"):
            raise ValueError("kind must be 'dom' or 'tdom'")
        if n < 1 or K < 1 or M < 1:
            raise ValueError("n, K, M must be >= 1")
        self.n, self.kind, self.K, self.M = n, kind, K, M
        self.sets = [tuple(s) for s in sets]
        N = n * n
        self.N = N
        self.nv = 0
        self.clauses = []
        add = self.clauses.append

        def new():
            self.nv += 1
            return self.nv

        # ---- variables (allocated class by class inside each family)
        self.X = [[new() for _ in range(K)] for _ in range(N)]
        self.Q = [[new() for _ in range(N)] for _ in range(K)]
        self.R = []
        for c in range(K):
            rows = [None]  # row 0 unused (constant)
            for i in range(1, N + 1):
                rows.append([None] + [new() for _ in range(M)])
            self.R.append(rows)
        self.S = [[None] + [self.R[c][N][m] for m in range(1, M + 1)]
                  for c in range(K)]
        self.ZS = [[new() for _ in self.sets] for _ in range(K)]

        # ---- exactly one class per square
        for v in range(N):
            add(list(self.X[v]))
            for a in range(K):
                for b in range(a + 1, K):
                    add([-self.X[v][a], -self.X[v][b]])

        # ---- domination
        opn = queens_neighbours(n)
        for c in range(K):
            for v in range(N):
                nbh = opn[v] if kind == "tdom" else [v] + opn[v]
                add([self.X[u][c] for u in nbh])

        # ---- Q chain (two-way) and symmetry breaking
        for c in range(K):
            add([-self.Q[c][0]])
            for v in range(1, N):
                q, qp, x = self.Q[c][v], self.Q[c][v - 1], self.X[v - 1][c]
                add([-qp, q])
                add([-x, q])
                add([-q, qp, x])
        for c in range(1, K):
            for v in range(N):
                add([-self.X[v][c], self.Q[c - 1][v]])

        # ---- sequential counter, two-way
        for c in range(K):
            for i in range(1, N + 1):
                x = self.X[i - 1][c]
                for m in range(1, M + 1):
                    r = self.R[c][i][m]
                    # a = R[i-1][m] (False if i == 1), b = R[i-1][m-1]
                    a = self.R[c][i - 1][m] if i > 1 else None
                    if m == 1:
                        b = True
                    else:
                        b = self.R[c][i - 1][m - 1] if i > 1 else None  # None=False
                    # a -> r
                    if a is not None:
                        add([-a, r])
                    # x and b -> r
                    if b is True:
                        add([-x, r])
                    elif b is not None:
                        add([-x, -b, r])
                    # r -> a or x
                    add([-r, x] + ([a] if a is not None else []))
                    # r -> a or b
                    if b is not True:
                        cl = [-r]
                        if a is not None:
                            cl.append(a)
                        if b is not None:
                            cl.append(b)
                        add(cl)

        # ---- ZS definitions
        for j, s in enumerate(self.sets):
            sq = sorted(set(s))
            for v in sq:
                if not 0 <= v < N:
                    raise ValueError("square out of range in sets")
            for c in range(K):
                z = self.ZS[c][j]
                for v in sq:
                    add([-z, self.X[v][c]])
                add([z] + [-self.X[v][c] for v in sq])

        # ---- (c) implied double-counting constraint, own totalizer
        if K * M > N:
            cap = N + 1
            seqs = [[self.S[c][m] for m in range(1, M + 1)] for c in range(K)]
            while len(seqs) > 1:
                nxt = []
                for t in range(0, len(seqs) - 1, 2):
                    nxt.append(self._merge(seqs[t], seqs[t + 1], cap, new))
                if len(seqs) % 2:
                    nxt.append(seqs[-1])
                seqs = nxt
            top = seqs[0]
            if len(top) >= cap:
                add([-top[N]])

    def _merge(self, A, B, cap, new):
        out = [new() for _ in range(min(len(A) + len(B), cap))]
        for i in range(len(A) + 1):
            for j in range(len(B) + 1):
                if i + j == 0:
                    continue
                k = min(i + j, cap)
                cl = [out[k - 1]]
                if i:
                    cl.append(-A[i - 1])
                if j:
                    cl.append(-B[j - 1])
                self.clauses.append(cl)
        return out

    # ------------------------------------------------------------------
    def class_vars(self, c):
        N, M = self.N, self.M
        res = [self.X[v][c] for v in range(N)]
        res += [self.Q[c][v] for v in range(N)]
        for i in range(1, N + 1):
            for m in range(1, M + 1):
                res.append(self.R[c][i][m])
        res += [self.ZS[c][j] for j in range(len(self.sets))]
        return res

    def decode(self, model):
        pos = set(l for l in model if l > 0)
        labels = []
        for v in range(self.N):
            cs = [c for c in range(self.K) if self.X[v][c] in pos]
            if len(cs) != 1:
                raise ValueError("square %d is in %d classes" % (v, len(cs)))
            labels.append(cs[0])
        return labels

    def partition_literals(self, labels):
        """Relabel classes by increasing smallest square (the symmetry
        breaking order) and return the X literal of every square."""
        if len(labels) != self.N:
            raise ValueError("wrong number of labels")
        order = {}
        for lab in labels:
            if lab not in order:
                order[lab] = len(order)
        if len(order) != self.K:
            raise ValueError("labels do not use exactly K classes")
        return [self.X[v][order[labels[v]]] for v in range(self.N)]

    def write_dimacs(self, path):
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (self.nv, len(self.clauses)))
            for cl in self.clauses:
                f.write(" ".join(str(l) for l in cl) + " 0\n")
