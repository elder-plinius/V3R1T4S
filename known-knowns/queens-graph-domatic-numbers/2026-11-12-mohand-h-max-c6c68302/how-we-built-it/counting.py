"""Derivation, as DRAT proof steps, of the counting bound "at most N of the K*M size bits are true" from a formula that
has, for N squares and K classes:
  x(v,c)        square v is in class c, with the pairwise clauses "at most one class per square";
  bit(c,i,m)    "class c has at least m of the squares 0..i-1" (i = 1..N, m = 1..M), with its two-way definition
                bit(c,i,m) <-> bit(c,i-1,m) or (x(i-1,c) and bit(c,i-1,m-1)).
Nothing else of the formula is used. The encoder object E gives the variable numbers (E.X, and E.CNT or E.R).

Bits are numbered k = c*M + m (k = 1..K*M). "Level i" means the bits bit(c,i,m). New variables, defined in the proof:
  W(i,k,t)   at least t of the first k bits are true at level i      (t = 1..min(k, i+1))
  Pre(i,c)   square i-1 is in one of the classes 0..c
Clause families at level i (old = level i-1; a clause with a constant-true literal is skipped, constant-false
literals are dropped; every clause below except the definitions must follow by unit propagation, which the proof
checker verifies):
  monob   bit(c,i,m) -> bit(c,i,m-1)
  def     the four clauses of W(i,k,t) <-> W(i,k-1,t) or (bit_k and W(i,k-1,t-1))           [definition]
  monot   W(i,k,t) -> W(i,k,t-1)
  pre     Pre(i,c) <-> Pre(i,c-1) or x(i-1,c)                                                  [definition]
  excl    Pre(i,c-1) -> not x(i-1,c)
  I1      not Pre(i,c) and W(i,k,t) -> W(i-1,k,t)          (bit k in class c: nothing has changed up to class c)
  I3      x(i-1,c) and W(i,k,t) -> W(i-1,k-1,t-1)          (bit k in class c: inside that block the bits shift by one)
  Jg      Pre(i,c-1) and W(i,k,t) -> W(i-1,k,t-1)          (bit k in class c: the square went to an earlier class)
  I2      W(i,k,t) -> W(i-1,k,t-1)
  diag    not W(i,k,i+1)                                    (no prefix has more than i true bits at level i)
After level i the clauses of level i-1 and the working clauses of level i are deleted. What remains after level N:
the definitions of W(N,.,.), monot, monob and the units "not W(N,k,N+1)", i.e. a counter over the bits
s(c,m) = bit(c,N,m) saying that at most N of them are true."""

T, F = True, False


def neg(a):
    return F if a is T else T if a is F else -a


def clause(*lits):
    out = []
    for l in lits:
        if l is T:
            return None
        if l is not F:
            out.append(l)
    return out


class ListSink:
    def __init__(self):
        self.steps = []

    def add(self, cl, tag):
        self.steps.append(('a', cl, tag))

    def delete(self, cl):
        self.steps.append(('d', cl, ''))


class BinSink:
    """binary DRAT: 'a' or 'd', each literal as the number 2*var + sign in 7-bit groups, then 0"""

    def __init__(self, f):
        self.f = f; self.n_add = 0; self.n_del = 0; self.buf = bytearray()

    def _w(self, lead, cl):
        b = self.buf; b.append(lead)
        for l in cl:
            u = 2 * abs(l) + (l < 0)
            while u > 127:
                b.append((u & 127) | 128); u >>= 7
            b.append(u)
        b.append(0)
        if len(b) > (1 << 20):
            self.f.write(b); self.buf = bytearray()

    def add(self, cl, tag):
        self._w(0x61, cl); self.n_add += 1

    def delete(self, cl):
        self._w(0x64, cl); self.n_del += 1

    def close(self):
        self.f.write(self.buf); self.buf = bytearray()


def base_clauses(E):
    """The encoder's clauses without its implied counting block (same variable numbers)."""
    b0, b1 = E._blk
    return E.clauses[:b0] + E.clauses[b1:]


def build(Enc, *args):
    """Build an encoder while recording which clauses form its implied counting block."""
    if hasattr(Enc, 'at_most'):                       # encoding 1: the block is what at_most adds
        orig = Enc.at_most

        def wrapped(self, lits, bound):
            a = len(self.clauses); orig(self, lits, bound); self._blk = (a, len(self.clauses))
        Enc.at_most = wrapped
        try:
            E = Enc(*args)
        finally:
            Enc.at_most = orig
    else:                                             # encoding 2: the block starts at the first merge, ends the list
        orig = Enc._merge

        def wrapped(self, A, B, cap, new):
            if not hasattr(self, '_blk0'):
                self._blk0 = len(self.clauses)
            return orig(self, A, B, cap, new)
        Enc._merge = wrapped
        try:
            E = Enc(*args)
        finally:
            Enc._merge = orig
        E._blk = (E._blk0, len(E.clauses)) if hasattr(E, '_blk0') else (len(E.clauses), len(E.clauses))
    if not hasattr(E, '_blk'):
        E._blk = (len(E.clauses), len(E.clauses))
    return E


class Counting:
    def __init__(self, E, sink):
        self.E, self.K, self.M, self.N = E, E.K, E.M, E.N
        self.nv = E.nv
        self.sink = sink
        self.lev = {0: {}}
        self.prev_keep = []
        self.cells = 0

    def new(self):
        self.nv += 1
        return self.nv

    def bit(self, c, i, m):
        if m == 0:
            return T
        if i == 0:
            return F
        if hasattr(self.E, 'CNT'):
            return self.E.CNT[c][i][m] or F
        return self.E.R[c][i][m]

    def w(self, i, k, t):
        if t == 0:
            return T
        if i == 0 or k == 0 or t > k or t > i + 1:
            return F
        return self.lev[i][(k, t)]

    def emit(self, store, tag, *lits):
        cl = clause(*lits)
        if cl is not None:
            self.sink.add(cl, tag); store.append(cl)

    def level(self, i):
        E, K, M = self.E, self.K, self.M
        p = i - 1
        y = [E.X[i - 1][c] for c in range(K)]
        keep, drop = [], []
        emit = self.emit
        for c in range(K):
            for m in range(2, M + 1):
                emit(keep, 'monob', neg(self.bit(c, i, m)), self.bit(c, i, m - 1))
        pre = [y[0]]
        for c in range(1, K):
            P = self.new()
            emit(drop, 'pre', -P, pre[c - 1], y[c])
            emit(drop, 'pre', P, -pre[c - 1])
            emit(drop, 'pre', P, -y[c])
            pre.append(P)
        for c in range(1, K):
            emit(drop, 'excl', -pre[c - 1], -y[c])
        cur = self.lev[i] = {}
        for k in range(1, K * M + 1):
            c, m = (k - 1) // M, (k - 1) % M + 1
            n = self.bit(c, i, m)
            for t in range(1, min(k, i + 1) + 1):
                a, b = self.w(i, k - 1, t), self.w(i, k - 1, t - 1)
                wv = self.new()
                emit(keep, 'def', -wv, a, n)
                emit(keep, 'def', -wv, a, b)
                emit(keep, 'def', wv, neg(a))
                emit(keep, 'def', wv, neg(n), neg(b))
                cur[(k, t)] = wv
                self.cells += 1
                if t >= 2:
                    emit(keep, 'monot', -wv, self.w(i, k, t - 1))
                emit(drop, 'I1', pre[c], -wv, self.w(p, k, t))
                if t >= 2:
                    emit(drop, 'I3', -y[c], -wv, self.w(p, k - 1, t - 1))
                    if c >= 1:
                        emit(drop, 'Jg', -pre[c - 1], -wv, self.w(p, k, t - 1))
                    emit(drop, 'I2', -wv, self.w(p, k, t - 1))
                if t == i + 1:
                    emit(keep, 'diag', -wv)
        kept = set(tuple(cl) for cl in keep)
        for cl in self.prev_keep + drop:
            if tuple(cl) not in kept:
                self.sink.delete(cl)
        self.prev_keep = keep
        del self.lev[p]

    def run(self):
        for i in range(1, self.N + 1):
            self.level(i)
        return self.prev_keep                 # the clauses that remain: the derived counter over the bits s(c,m)
