#!/usr/bin/env python3
"""Standard-library checker for diagonal-layer transfer-matrix bounds (He, arXiv 2607.28810 and its
dimension-d and monomer-dimer extensions).  Everything is rebuilt from the definitions in DERIVATION.md:

  layer       V = Z/m1 x ... x Z/m_{r}   (r = d-1 cross-section directions), N = |V|
  D           {0, e1, ..., e_r}           (d forward directions)
  A[u,v]      1 if v - u is in D
  T[U,W]      per A[U, V minus W]   if |U|+|W| = N, else 0                (dimer layer, He eq. 2.2)
  TMD[U,W]    sum over S subset of (V minus U) of per A[S,W]              (monomer-dimer layer)
  group G     all x -> t + phi(x), phi an automorphism of V with phi(D) = s + D for some s
  X, Y        compressed blocks of T on G-orbits of subsets:  (Phi_k y)(U) = sum over injections
              f : U -> V with f(u)-u in D of y(orbit of V minus f(U));  X = Phi_i (|U| = i),  Y = Phi_{N-i}.
All counts are exact Python integers; ratios are compared by cross multiplication; no floating point
is used for any decision.

Subcommands (run with python3 cwcheck.py ...):
  trace  DIMS L            tr(T^L) and tr(TMD^L) against brute-force matching counts of the quotient graph
  iter   DIMS P            exact iterated Collatz-Wielandt bound C_p, p = 0..P, every sector, ceil to 6 places
  cert   DIMS SECTOR FILE  exact CW ratio of one sector for the test vector in FILE (orbit_id mask x [listed])
  propc  DIMS              property C (row sums over column orbits are orbit-invariant) on the full matrices
  mdcert DIMS FILE         full uncompressed monomer-dimer matrix, exact CW ratio for the vector in FILE
DIMS is a comma list of the cross-section sizes, e.g. 5,5 (three dimensions) or 3,3,2 (four dimensions).
"""
import sys, itertools, time
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 80


class Layer:
    def __init__(self, dims):
        self.dims = tuple(dims)
        self.r = len(dims)
        N = 1
        for d in dims:
            N *= d
        self.N = N
        self.FULL = (1 << N) - 1
        self.coords = list(itertools.product(*[range(d) for d in dims]))
        self.index = {c: i for i, c in enumerate(self.coords)}
        offs = [tuple([0] * self.r)]
        for j in range(self.r):
            e = [0] * self.r
            e[j] = 1
            offs.append(tuple(e))
        self.D = offs
        self.nbbit = []
        for c in self.coords:
            self.nbbit.append([1 << self.add(c, o) for o in offs])
        self.build_group()
        self.orb_cache = {}

    def add(self, c, o):
        return self.index[tuple((c[j] + o[j]) % self.dims[j] for j in range(self.r))]

    def build_group(self):
        dims, r, N = self.dims, self.r, self.N
        perms = []
        Dset = set(self.D)
        for imgs in itertools.product(range(N), repeat=r):
            a = [self.coords[i] for i in imgs]
            ok = True
            for j in range(r):
                if any((dims[j] * a[j][t]) % dims[t] for t in range(r)):
                    ok = False
                    break
            if not ok:
                continue
            phi = []
            for c in self.coords:
                phi.append(self.index[tuple(sum(c[j] * a[j][t] for j in range(r)) % dims[t] for t in range(r))])
            if len(set(phi)) != N:
                continue
            img = set(phi[self.index[o]] for o in self.D)
            found = False
            for s in range(N):
                if set(self.add(self.coords[s], o) for o in self.D) == img:
                    found = True
                    break
            if not found:
                continue
            for t in range(N):
                tc = self.coords[t]
                perms.append([self.add(tc, self.coords[phi[v]]) for v in range(N)])
        self.perms = perms
        self.ng = len(perms)
        self.CH = 9
        nch = (N + self.CH - 1) // self.CH
        self.nch = nch
        self.tabs = []
        for p in perms:
            tl = []
            for c in range(nch):
                t = [0] * (1 << self.CH)
                for b in range(1, 1 << self.CH):
                    low = b & -b
                    j = low.bit_length() - 1
                    v = c * self.CH + j
                    t[b] = t[b ^ low] | ((1 << p[v]) if v < N else 0)
                tl.append(t)
            self.tabs.append(tl)

    def image_masks(self, mask):
        out = []
        ch = [(mask >> (self.CH * c)) & ((1 << self.CH) - 1) for c in range(self.nch)]
        for tl in self.tabs:
            r = 0
            for c in range(self.nch):
                r |= tl[c][ch[c]]
            out.append(r)
        return out

    def orbits(self, k):
        """(reps sorted ascending, dict mask -> orbit id) for all k-subsets"""
        if k in self.orb_cache:
            return self.orb_cache[k]
        N = self.N
        seen = {}
        reps = []
        for comb in itertools.combinations(range(N), k):
            m = 0
            for v in comb:
                m |= 1 << v
            if m in seen:
                continue
            orb = set(self.image_masks(m))
            rep = min(orb)
            reps.append(rep)
            for x in orb:
                seen[x] = rep
        reps.sort()
        idx = {rp: i for i, rp in enumerate(reps)}
        oid = {m: idx[rp] for m, rp in seen.items()}
        self.orb_cache[k] = (reps, oid)
        return reps, oid

    def phi_matrix(self, k):
        """rows: orbit reps of k-sets; entries: dict column orbit (of the (N-k)-sets) -> count"""
        reps, _ = self.orbits(k)
        _, oid2 = self.orbits(self.N - k)
        FULL = self.FULL
        rows = []
        for U in reps:
            vs = [v for v in range(self.N) if U >> v & 1]
            nbs = [self.nbbit[v] for v in vs]
            acc = {}

            def rec(i, used):
                if i == k:
                    o = oid2[FULL ^ used]
                    acc[o] = acc.get(o, 0) + 1
                    return
                for t in nbs[i]:
                    if not used & t:
                        rec(i + 1, used | t)
            rec(0, 0)
            ks = sorted(acc)
            rows.append(([c for c in ks], [acc[c] for c in ks]))
        return rows


def matvec(rows, x):
    out = []
    for cols, cnts in rows:
        s = 0
        for c, w in zip(cols, cnts):
            s += w * x[c]
        out.append(s)
    return out


def argmax_ratio(num, den):
    best = 0
    for u in range(1, len(num)):
        if num[u] * den[best] > num[best] * den[u]:
            best = u
    return best


def bound_from_ratio(num, den, scale):
    """ln(num/den)/scale as a Decimal"""
    return (Decimal(num).ln() - Decimal(den).ln()) / Decimal(scale)


def ceil6(b):
    return (b * 1000000).to_integral_value(rounding='ROUND_CEILING') / 1000000


def sector_blocks(L, i):
    X = L.phi_matrix(i)
    Y = X if L.N - i == i else L.phi_matrix(L.N - i)
    return X, Y


def cmd_iter(dims, P):
    L = Layer(dims)
    N = L.N
    t0 = time.time()
    print("layer %s |G|=%d N=%d" % (dims, L.ng, N), flush=True)
    best = [None] * (P + 1)
    for i in range(N // 2 + 1):
        X, Y = sector_blocks(L, i)
        a = len(X)
        v = [1] * a
        for p in range(P + 1):
            z = matvec(X, matvec(Y, v))
            u = argmax_ratio(z, v)
            b = bound_from_ratio(z[u], v[u], 2 * N)
            if best[p] is None or b > best[p][0]:
                best[p] = (b, i, z[u], v[u])
            v = z
        print("  sector %d: %d orbits (%.1fs)" % (i, a, time.time() - t0), flush=True)
    for p in range(P + 1):
        b, i, num, den = best[p]
        print("RESULT dims=%s p=%d bound=%.10f ceil6=%s sector=%d ratio=%d/%d" % (",".join(map(str, dims)), p, b, ceil6(b), i, num, den))
    return best


def read_cert(path):
    rows = []
    with open(path) as f:
        for line in f:
            if not line.strip() or line[0] == '#':
                continue
            t = line.split()
            rows.append((int(t[0]), int(t[1]), int(t[2]), int(t[3]) if len(t) > 3 else None))
    return rows


def cmd_cert(dims, i, path):
    L = Layer(dims)
    N = L.N
    reps, oid = L.orbits(i)
    cert = read_cert(path)
    x = [None] * len(reps)
    listed = [None] * len(reps)
    for (idn, mask, xv, tv) in cert:
        if mask not in oid or oid[mask] != idn or reps[idn] != mask or x[idn] is not None or xv <= 0:
            print("CERT INVALID line", idn, mask)
            return None
        x[idn] = xv
        listed[idn] = tv
    if any(v is None for v in x):
        print("CERT INVALID: orbits missing")
        return None
    X, Y = sector_blocks(L, i)
    z = matvec(X, matvec(Y, x))
    u = argmax_ratio(z, x)
    mism = sum(1 for r in range(len(z)) if listed[r] is not None and listed[r] != z[r])
    b = bound_from_ratio(z[u], x[u], 2 * N)
    print("RESULT cert dims=%s sector=%d orbits=%d listed_mismatches=%d u=%d ratio=%d/%d bound=%.10f ceil6=%s" % (
        ",".join(map(str, dims)), i, len(z), mism, u, z[u], x[u], b, ceil6(b)))
    return z[u], x[u], b


def md_matrix(L):
    N = L.N
    nbs = [[b.bit_length() - 1 for b in L.nbbit[v]] for v in range(N)]
    # cnt[S] : dict W -> number of injections S -> W with steps in D
    cnt = {}
    for S in range(1 << N):
        vs = [v for v in range(N) if S >> v & 1]
        d = {}

        def rec(i, used):
            if i == len(vs):
                d[used] = d.get(used, 0) + 1
                return
            for c in nbs[vs[i]]:
                if not used >> c & 1:
                    rec(i + 1, used | 1 << c)
        rec(0, 0)
        cnt[S] = d
    rows = []
    for U in range(1 << N):
        comp = L.FULL ^ U
        row = {}
        S = comp
        while True:
            for W, k in cnt[S].items():
                row[W] = row.get(W, 0) + k
            if S == 0:
                break
            S = (S - 1) & comp
        rows.append(row)
    return rows


def cmd_mdcert(dims, path):
    """Exact CW ratio on the FULL (uncompressed) monomer-dimer matrix.  The certificate lists one value per orbit
    of the subgroup H = (all translations) x| (identity, and the coordinate swap when the two sizes are equal);
    the file's orbits are rebuilt here, every state gets its orbit's value, and the check itself uses the
    whole matrix, so the choice of H only decides how the file is expanded, not the validity of the bound."""
    L = Layer(dims)
    N = L.N
    assert len(dims) == 2
    m, n = dims
    sw = [False, True] if m == n else [False]
    H = []
    for s_ in sw:
        for t in range(N):
            tx, ty = divmod(t, n)
            perm = []
            for x in range(m):
                for y in range(n):
                    a, b = (y, x) if s_ else (x, y)
                    perm.append(((a + tx) % m) * n + (b + ty) % n)
            H.append(perm)
    seen = {}
    reps = []
    for mk in range(1 << N):
        if mk in seen:
            continue
        orb = set(sum(1 << p[v] for v in range(N) if mk >> v & 1) for p in H)
        rp = min(orb)
        reps.append(rp)
        for o in orb:
            seen[o] = rp
    reps.sort()
    gid = {rp: j for j, rp in enumerate(reps)}
    cert = read_cert(path)
    xs = [None] * len(reps)
    for (idn, mask, xv, tv) in cert:
        if gid.get(mask) != idn or xs[idn] is not None or xv <= 0:
            print("CERT INVALID", idn, mask)
            return None
        xs[idn] = xv
    if any(v is None for v in xs):
        print("CERT INVALID: orbits missing")
        return None
    x = [xs[gid[seen[mk]]] for mk in range(1 << N)]
    rows = md_matrix(L)
    nums = [sum(k * x[W] for W, k in row.items()) for row in rows]
    u = argmax_ratio(nums, x)
    b = bound_from_ratio(nums[u], x[u], N)
    print("RESULT mdcert dims=%s states=%d orbits=%d u=%d ratio=%d/%d bound=%.10f ceil10=%s" % (
        ",".join(map(str, dims)), 1 << N, len(xs), u, nums[u], x[u], b,
        (b * 10 ** 10).to_integral_value(rounding='ROUND_CEILING') / 10 ** 10))
    return nums[u], x[u], b


# ---------------------------------------------------------------- brute-force trace check
def quotient_graph(dims_r, l):
    """vertices of Z^d / Lambda, Lambda = span(m_j (e_j - e_d), l e_d), via the triangular reduction"""
    r = len(dims_r)
    d = r + 1

    def red(x):
        x = list(x)
        for j in range(r):
            q = x[j] // dims_r[j]
            x[j] -= q * dims_r[j]
            x[d - 1] += q * dims_r[j]
        x[d - 1] %= l
        return tuple(x)
    verts = {}
    for x in itertools.product(*([range(m) for m in dims_r] + [range(l)])):
        verts[red(x)] = len(verts)
    edges = set()
    for x, a in verts.items():
        for j in range(d):
            y = list(x)
            y[j] += 1
            b = verts[red(y)]
            assert a != b
            edges.add((min(a, b), max(a, b)))
    return len(verts), sorted(edges)


def count_matchings(nv, E, perfect):
    inc = [[] for _ in range(nv)]
    for a, b in E:
        inc[a].append(b)
        inc[b].append(a)
    memo = {}
    sys.setrecursionlimit(10000)

    def rec(mask):
        if mask == (1 << nv) - 1:
            return 1
        if mask in memo:
            return memo[mask]
        v = 0
        while mask >> v & 1:
            v += 1
        t = 0 if perfect else rec(mask | 1 << v)
        for w in inc[v]:
            if not mask >> w & 1:
                t += rec(mask | 1 << v | 1 << w)
        memo[mask] = t
        return t
    return rec(0)


def full_T(L, md):
    N = L.N
    rows = []
    if md:
        return md_matrix(L)
    nbs = [[b.bit_length() - 1 for b in L.nbbit[v]] for v in range(N)]
    # T[U][W] = per A[U, V minus W]
    cnt = {}
    for S in range(1 << N):
        vs = [v for v in range(N) if S >> v & 1]
        d = {}

        def rec(i, used):
            if i == len(vs):
                d[used] = d.get(used, 0) + 1
                return
            for c in nbs[vs[i]]:
                if not used >> c & 1:
                    rec(i + 1, used | 1 << c)
        rec(0, 0)
        cnt[S] = d
    for U in range(1 << N):
        rows.append({L.FULL ^ img: k for img, k in cnt[U].items()})
    return rows


def trace_pow(rows, l):
    n = len(rows)
    tr = 0
    for s in range(n):
        vec = {s: 1}
        for _ in range(l):
            new = {}
            # vec is a row vector: new = vec * T
            for U, c in vec.items():
                for W, k in rows[U].items():
                    new[W] = new.get(W, 0) + c * k
            vec = new
        tr += vec.get(s, 0)
    return tr


def cmd_trace(dims, l):
    L = Layer(dims)
    nv, E = quotient_graph(list(dims), l)
    pm = count_matchings(nv, E, True)
    am = count_matchings(nv, E, False)
    tp = trace_pow(full_T(L, False), l)
    ta = trace_pow(full_T(L, True), l)
    ok = (pm == tp and am == ta)
    print("RESULT trace dims=%s l=%d vertices=%d perfect_matchings=%d tr(T^l)=%d all_matchings=%d tr(TMD^l)=%d %s" % (
        ",".join(map(str, dims)), l, nv, pm, tp, am, ta, "EQUAL" if ok else "MISMATCH"))
    return ok


def _orbit_table(L, k):
    """array indexed by mask -> orbit id (ids = index of the orbit's least mask among k-subsets); plus sorted reps"""
    from array import array
    N = L.N
    tab = array('i', [-1]) * (1 << N)
    reps = []
    for comb in itertools.combinations(range(N), k):
        m = 0
        for v in comb:
            m |= 1 << v
        if tab[m] != -1:
            continue
        orb = L.image_masks(m)
        j = len(reps)
        reps.append(min(orb))
        for x in orb:
            tab[x] = j
    order = sorted(range(len(reps)), key=lambda j: reps[j])
    newid = [0] * len(reps)
    for pos, j in enumerate(order):
        newid[j] = pos
    return tab, newid, [reps[j] for j in order]


_G = {}


def _row_sum(args):
    """sum over injections f: U -> V, f(u)-u in D, of vec[orbit id of complement of f(U)]"""
    lo, hi = args
    reps, nbs_all, tab, newid, vec, FULL = _G['reps'], _G['nb'], _G['tab'], _G['newid'], _G['vec'], _G['FULL']
    N = _G['N']
    out = []
    for r in range(lo, hi):
        U = reps[r]
        vs = [v for v in range(N) if U >> v & 1]
        nbs = [nbs_all[v] for v in vs]
        k = len(vs)
        tot = [0]

        def rec(i, used):
            if i == k:
                tot[0] += vec[newid[tab[FULL ^ used]]]
                return
            a, b, c = nbs[i]
            if not used & a:
                rec(i + 1, used | a)
            if not used & b:
                rec(i + 1, used | b)
            if not used & c:
                rec(i + 1, used | c)
        rec(0, 0)
        out.append(tot[0])
    return out


def apply_phi(L, k, vec, procs):
    """(Phi_k vec) on the orbit reps of k-subsets; vec is indexed by orbits of (N-k)-subsets (sorted by rep mask)"""
    import multiprocessing as mp
    reps, _ = L.orbits(k) if L.N <= 20 else (_REPS[k], None)
    tab, newid, _r = _TABS[L.N - k]
    _G.update(dict(reps=reps, nb=[b for b in [[x[0], x[1], x[2]] for x in L.nbbit]], tab=tab, newid=newid, vec=vec, FULL=L.FULL, N=L.N))
    nrows = len(reps)
    chunks = [(i, min(i + 64, nrows)) for i in range(0, nrows, 64)]
    if procs > 1:
        ctx = mp.get_context('fork')
        with ctx.Pool(procs) as pool:
            parts = pool.map(_row_sum, chunks)
    else:
        parts = [_row_sum(c) for c in chunks]
    res = []
    for pt in parts:
        res.extend(pt)
    return res


_REPS = {}
_TABS = {}


def cmd_certfull(dims, i, path, procs):
    """Exact CW ratio of sector i for the vector in path, with dense orbit tables (suited to N up to 25)."""
    L = Layer(dims)
    N = L.N
    t0 = time.time()
    for k in {i, N - i}:
        _TABS[k] = _orbit_table(L, k)
        _REPS[k] = _TABS[k][2]
    reps = _REPS[i]
    tab, newid, _r = _TABS[i]
    cert = read_cert(path)
    x = [None] * len(reps)
    listed = [None] * len(reps)
    for (idn, mask, xv, tv) in cert:
        if idn >= len(reps) or reps[idn] != mask or x[idn] is not None or xv <= 0:
            print("CERT INVALID line", idn, mask)
            return None
        x[idn] = xv
        listed[idn] = tv
    if any(v is None for v in x):
        print("CERT INVALID: orbits missing")
        return None
    print("orbit tables built, %d orbits in sector %d (%.0fs)" % (len(reps), i, time.time() - t0), flush=True)
    w = apply_phi(L, N - i, x, procs)
    print("second layer done (%.0fs)" % (time.time() - t0), flush=True)
    z = apply_phi(L, i, w, procs)
    u = argmax_ratio(z, x)
    mism = sum(1 for r in range(len(z)) if listed[r] is not None and listed[r] != z[r])
    b = bound_from_ratio(z[u], x[u], 2 * N)
    print("RESULT certfull dims=%s sector=%d orbits=%d listed_mismatches=%d u=%d ratio=%d/%d bound=%.10f ceil6=%s (%.0fs)" % (
        ",".join(map(str, dims)), i, len(z), mism, u, z[u], x[u], b, ceil6(b), time.time() - t0))
    return z[u], x[u], b


def cmd_propc(dims):
    """Check He's property C on the full matrix: for orbits O1, O2 of G on subsets, the sum over V in O2 of
    T[U,V] does not depend on the representative U of O1 (dimer layer), and also for the monomer-dimer layer."""
    L = Layer(dims)
    N = L.N
    orbit_of = {}
    for k in range(N + 1):
        reps, oid = L.orbits(k)
        for mk, o in oid.items():
            orbit_of[mk] = (k, o)
    ok = True
    for md in (False, True):
        rows = full_T(L, md)
        table = {}
        for U in range(1 << N):
            sums = {}
            for W, c in rows[U].items():
                key = orbit_of[W]
                sums[key] = sums.get(key, 0) + c
            key1 = orbit_of[U]
            if key1 in table:
                if table[key1] != sums:
                    ok = False
            else:
                table[key1] = sums
    print("RESULT propc dims=%s |G|=%d %s" % (",".join(map(str, dims)), L.ng, "HOLDS (dimer and monomer-dimer)" if ok else "FAILS"))
    return ok


if __name__ == '__main__':
    cmd = sys.argv[1]
    dims = [int(t) for t in sys.argv[2].split(',')]
    if cmd == 'trace':
        sys.exit(0 if cmd_trace(dims, int(sys.argv[3])) else 1)
    elif cmd == 'iter':
        cmd_iter(dims, int(sys.argv[3]))
    elif cmd == 'cert':
        sys.exit(0 if cmd_cert(dims, int(sys.argv[3]), sys.argv[4]) else 1)
    elif cmd == 'certfull':
        sys.exit(0 if cmd_certfull(dims, int(sys.argv[3]), sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 1) else 1)
    elif cmd == 'propc':
        sys.exit(0 if cmd_propc(dims) else 1)
    elif cmd == 'mdcert':
        sys.exit(0 if cmd_mdcert(dims, sys.argv[3]) else 1)
    else:
        sys.exit(2)
