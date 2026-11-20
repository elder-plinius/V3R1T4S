"""Sample subgroups of a structured group acting on mixed-alphabet Hamming space; write osg element files.

usage: python mkgroups.py alph family lo hi samples seed outdir [maxk]
maxk: keep at most this many subgroups, spread evenly over the order-sorted list.
alph: e.g. "3x15" or "2x5,3x9" (blocks in coordinate order).
family: coordinate part and symbol part joined by '/', e.g. "cyc/glob", "pgl11+1/mono", "cyc5|agl9/glob".
  coordinate part: '|' separates blocks (one entry per alphabet block, or one entry for a single block).
    each entry: <kind>[+e] where +e appends e fixed coordinates. kinds:
      cyc (Z_k), agl (AGL(1,Z_k)), sym (S_k), pgl<p> (PGL(2,p) on p+1, p prime), pgf<q> (PGamL(2,q), q=4,8,9,16),
      aglm (AGL(m,p) on p^m points), aglf (AGamL(1,F_q) on q points), m11, m12 (Mathieu, on 11/12 points),
      grid<a>x<b> (S_a x S_b on a*b points), pg32 (GL(4,2) on PG(3,2)), pairs6 (S6 on 15 pairs), triv
  symbol part: glob (same S_q at every coordinate of a block), scal (global GF(q)* only, q prime or 4),
    mono (global S_q plus a GF(q)* scalar at one coordinate per block), aff (global S_q plus a translation at one
    coordinate per block), none.
Subgroups are closures of 1-3 random elements (random words in the generators raised to random powers), kept when
lo <= order <= hi, deduplicated by an invariant. A sample, not a classification.
"""
import collections, itertools, os, random, sys


def parse_alph(s):
    qs = []
    for blk in s.split(','):
        a, c = blk.split('x'); qs += [int(a)] * int(c)
    return qs


def blocks_of(s):
    out, start = [], 0
    for blk in s.split(','):
        a, c = map(int, blk.split('x')); out.append((a, start, int(c))); start += int(c)
    return out


# ---------- finite fields (small) ----------
IRRED = {4: (2, [1, 1]), 8: (2, [1, 1, 0]), 9: (3, [1, 0]), 16: (2, [1, 1, 0, 0])}  # x^m = -(c0 + c1 x + ...)


class GF:
    def __init__(self, q):
        self.q = q
        if q in IRRED:
            p, low = IRRED[q]; m = len(low)
        else:
            p, low, m = q, None, 1
        self.p, self.m = p, m
        els = list(itertools.product(range(p), repeat=m))  # little-endian coefficient tuples
        self.idx = {e: i for i, e in enumerate(els)}; self.els = els
        def mul(a, b):
            prod = [0] * (2 * m - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    prod[i + j] = (prod[i + j] + x * y) % p
            for k in range(2 * m - 2, m - 1, -1):
                c = prod[k]
                if c:
                    prod[k] = 0
                    for t in range(m):
                        prod[k - m + t] = (prod[k - m + t] - c * low[t]) % p
            return tuple(prod[:m])
        self.mul = [[self.idx[mul(a, b)] for b in els] for a in els]
        self.add = [[self.idx[tuple((x + y) % p for x, y in zip(a, b))] for b in els] for a in els]
        self.inv = [None] + [next(b for b in range(q) if self.mul[a][b] == 1) for a in range(1, q)]
        self.prim = next(g for g in range(2, q) if len({self._pow(g, k) for k in range(1, q)}) == q - 1) if q > 2 else 1
        self.frob = [self._pow(a, p) for a in range(q)]

    def _pow(self, a, k):
        r = 1
        for _ in range(k):
            r = self.mul[r][a]
        return r


def pgamma_gens(q):
    F = GF(q); inf = q
    def mob(f):
        return tuple(f(x) for x in range(q + 1))
    t = mob(lambda x: inf if x == inf else F.add[x][1])
    m = mob(lambda x: inf if x == inf else F.mul[F.prim][x])
    r = mob(lambda x: 0 if x == inf else (inf if x == 0 else F.inv[x]))
    gens = [t, m, r]
    if F.m > 1:
        gens.append(mob(lambda x: inf if x == inf else F.frob[x]))
    return gens


def aglf_gens(q):
    F = GF(q)
    gens = [tuple(F.add[x][1] for x in range(q)), tuple(F.mul[F.prim][x] for x in range(q))]
    if F.m > 1:
        gens.append(tuple(F.frob[x] for x in range(q)))
    return gens


def aglm_gens(k):
    p, m = next((p, m) for p in (2, 3, 5, 7, 11, 13) for m in range(1, 5) if p ** m == k)
    vecs = list(itertools.product(range(p), repeat=m)); ix = {v: i for i, v in enumerate(vecs)}
    gens = []
    for i in range(m):
        gens.append(tuple(ix[tuple((v[j] + (j == i)) % p for j in range(m))] for v in vecs))
    for i in range(m):
        for j in range(m):
            if i != j:
                gens.append(tuple(ix[tuple((v[t] + (v[j] if t == i else 0)) % p for t in range(m))] for v in vecs))
    if p > 2:
        g = next(a for a in range(2, p) if len({pow(a, e, p) for e in range(1, p)}) == p - 1)
        gens.append(tuple(ix[((v[0] * g) % p,) + v[1:]] for v in vecs))
    return gens


M12_GENS1 = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [(3, 7, 11, 8), (4, 10, 5, 6)], [(1, 12), (2, 11), (3, 6), (4, 8), (5, 9), (7, 10)]]


def cycles_to_perm(cycles, k):
    p = list(range(k))
    for c in cycles:
        for a, b in zip(c, c[1:] + c[:1]):
            p[a - 1] = b - 1
    return tuple(p)


def coord_kind_gens(kind):
    """return (k, generator list) for a coordinate group kind"""
    if kind.startswith('cyc'):
        k = int(kind[3:]); return k, [tuple((i + 1) % k for i in range(k))]
    if kind.startswith('agl') and kind[3:].isdigit():
        import math
        k = int(kind[3:])
        return k, [tuple((i + 1) % k for i in range(k))] + [tuple((a * i) % k for i in range(k)) for a in range(2, k) if math.gcd(a, k) == 1]
    if kind.startswith('sym'):
        k = int(kind[3:]); return k, [tuple([1, 0] + list(range(2, k))), tuple((i + 1) % k for i in range(k))]
    if kind.startswith('pgl'):
        p = int(kind[3:]); return p + 1, pgamma_gens(p)
    if kind.startswith('pgf'):
        q = int(kind[3:]); return q + 1, pgamma_gens(q)
    if kind.startswith('aglm'):
        k = int(kind[4:]); return k, aglm_gens(k)
    if kind.startswith('aglf'):
        q = int(kind[4:]); return q, aglf_gens(q)
    if kind == 'm12':
        g = [cycles_to_perm([tuple(M12_GENS1[0])], 12), cycles_to_perm(M12_GENS1[1], 12), cycles_to_perm(M12_GENS1[2], 12)]
        return 12, g
    if kind == 'm11':
        return 11, [cycles_to_perm([tuple(M12_GENS1[0])], 11), cycles_to_perm(M12_GENS1[1], 11)]
    if kind.startswith('grid'):
        a, b = map(int, kind[4:].split('x')); pts = [(i, j) for i in range(a) for j in range(b)]; ix = {p: t for t, p in enumerate(pts)}
        gens = []
        for s in ([1, 0] + list(range(2, a)), list(range(1, a)) + [0]):
            gens.append(tuple(ix[(s[i], j)] for i, j in pts))
        for s in ([1, 0] + list(range(2, b)), list(range(1, b)) + [0]):
            gens.append(tuple(ix[(i, s[j])] for i, j in pts))
        return a * b, gens
    if kind == 'pg32':
        pts = list(range(1, 16))
        def mat_perm(M):
            out = []
            for v in pts:
                w = 0
                for t in range(4):
                    if v >> t & 1:
                        w ^= M[t]
                out.append(w - 1)
            return tuple(out)
        return 15, [mat_perm([0b0010, 0b0100, 0b1000, 0b0011]), mat_perm([0b0001, 0b0011, 0b0100, 0b1000])]
    if kind == 'pairs6':
        pts = list(itertools.combinations(range(6), 2)); ix = {p: i for i, p in enumerate(pts)}
        return 15, [tuple(ix[tuple(sorted((s[a], s[b])))] for a, b in pts) for s in [(1, 0, 2, 3, 4, 5), (1, 2, 3, 4, 5, 0)]]
    if kind.startswith('triv'):
        k = int(kind[4:]); return k, []
    raise SystemExit(f'unknown coordinate kind {kind}')


def scalar_perms(q):
    if q == 4:
        F = GF(4); return [tuple(F.mul[F.prim][x] for x in range(4)), tuple(F.frob)]
    if q in (2, 3, 5, 7):
        g = 1 if q == 2 else next(a for a in range(2, q) if len({pow(a, e, q) for e in range(1, q)}) == q - 1)
        return [tuple((g * x) % q for x in range(q))] if q > 2 else []
    return []


def sym_gens_full(q):
    return [tuple([1, 0] + list(range(2, q))), tuple(list(range(1, q)) + [0])] if q > 1 else []


def build_gens(alph, family):
    qs = parse_alph(alph); n = len(qs); Q = max(qs); blocks = blocks_of(alph)
    cpart, spart = family.split('/')
    centries = cpart.split('|')
    if len(centries) == 1 and len(blocks) > 1:
        raise SystemExit('give one coordinate entry per alphabet block')
    idc = tuple(range(n)); ids = tuple(tuple(range(Q)) for _ in range(n))
    gens = []
    for (q, start, cnt), ent in zip(blocks, centries):
        kind, _, fx = ent.partition('+')
        k, cg = coord_kind_gens(kind)
        if k + (int(fx) if fx else 0) != cnt:
            raise SystemExit(f'{ent}: {k} + {fx or 0} points != block length {cnt}')
        for g in cg:
            p = list(idc)
            for i in range(k):
                p[start + i] = start + g[i]
            gens.append((tuple(p), ids))
    def at(i, perm):  # symbol perm at coordinate i only
        s = list(ids); s[i] = tuple(list(perm) + list(range(len(perm), Q))); return (idc, tuple(s))
    def glob(start, cnt, perm):
        s = list(ids)
        for i in range(start, start + cnt):
            s[i] = tuple(list(perm) + list(range(len(perm), Q)))
        return (idc, tuple(s))
    for q, start, cnt in blocks:
        if spart in ('glob', 'mono', 'aff'):
            gens += [glob(start, cnt, s) for s in sym_gens_full(q)]
        if spart == 'scal':
            gens += [glob(start, cnt, s) for s in scalar_perms(q)]
        if spart == 'mono':
            gens += [at(start, s) for s in scalar_perms(q)[:1]]
        if spart == 'aff':
            gens.append(at(start, tuple(list(range(1, q)) + [0])))
    return n, Q, idc, ids, gens


def compose(g, h):  # g after h
    pg, sg = g; ph, sh = h
    return (tuple(pg[ph[i]] for i in range(len(ph))), tuple(tuple(sg[ph[i]][x] for x in sh[i]) for i in range(len(ph))))


def main():
    alph, family, lo, hi, samples, seed, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    rnd = random.Random(seed)
    n, Q, idc, ids, gens = build_gens(alph, family)
    os.makedirs(out, exist_ok=True)
    e = (idc, ids)
    if not gens:
        items = []
    else:
        items = sample(rnd, gens, e, lo, hi, samples)
    maxk = int(sys.argv[8]) if len(sys.argv) > 8 else 0
    if maxk and len(items) > maxk:
        items = [items[round(i * (len(items) - 1) / (maxk - 1))] for i in range(maxk)] if maxk > 1 else items[:1]
    with open(os.path.join(out, 'manifest.tsv'), 'w') as mf:
        for k, S in enumerate(items):
            with open(os.path.join(out, f'g{k}.txt'), 'w') as f:
                for p, s in sorted(S):
                    f.write(' '.join(map(str, p)) + ' ' + ' '.join(' '.join(map(str, t)) for t in s) + '\n')
            mf.write(f'{k}\t{len(S)}\t{family}\t{orbit_sig(S, n)}\n')
    print(f'{alph} {family}: {len(items)} subgroups (orders {lo}..{hi})')


def orbit_sig(S, n):
    seen, res = set(), []
    for p in range(n):
        if p in seen:
            continue
        o = {g[0][p] for g in S}; seen |= o; res.append(len(o))
    return '.'.join(map(str, sorted(res)))


def closure(gs, e, cap):
    S = {e}; fr = [e]
    while fr:
        nf = []
        for x in fr:
            for g in gs:
                y = compose(g, x)
                if y not in S:
                    S.add(y); nf.append(y)
                    if len(S) > cap:
                        return None
        fr = nf
    return S


def cyc(perm):
    seen, res = set(), []
    for p in range(len(perm)):
        if p in seen:
            continue
        c = 0; x = p
        while x not in seen:
            seen.add(x); x = perm[x]; c += 1
        res.append(c)
    return tuple(sorted(res))


def invariant(S, n):
    fix = collections.Counter()
    for p, s in S:
        fix[(cyc(p), tuple(cyc(t) for t in s))] += 1
    return (len(S), orbit_sig(S, n), tuple(sorted(fix.items())))


def sample(rnd, gens, e, lo, hi, samples):
    n = len(e[0])
    def rand_elem():
        g = e
        for _ in range(rnd.randint(3, 30)):
            g = compose(rnd.choice(gens), g)
        h = e
        for _ in range(rnd.randint(1, 12)):
            h = compose(g, h)
        return h
    found = {}
    for _ in range(samples):
        gs = [rand_elem() for _ in range(rnd.choice([1, 2, 2, 2, 3]))]
        S = closure(gs, e, hi)
        if S is None or len(S) < lo:
            continue
        key = invariant(S, n)
        if key not in found:
            found[key] = S
    return sorted(found.values(), key=lambda S: -len(S))


if __name__ == '__main__':
    main()
