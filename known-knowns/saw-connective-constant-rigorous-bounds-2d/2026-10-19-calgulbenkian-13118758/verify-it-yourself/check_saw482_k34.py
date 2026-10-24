"""Standard-library checker for the (4.8^2) lattice SAW upper bound with finite-pocket pruning.

Usage: python3 -I check_saw482_k34.py VECTOR_FILE K [--workers N] [--raw3] [--limit STATES]

VECTOR_FILE is the reassembled object/vector.xz (format: object/AUTOMATON.md), or with --raw3 a plain
file of 3-byte records (exponent, mantissa low byte, mantissa high byte) used only for testing.
The state set is REBUILT by breadth-first search from the two seed states, from the definition in
AUTOMATON.md (lattice, canonical form, loop-length pruning, chord shortcuts, finite-pocket pruning).
Every transition is rebuilt, every pruned move is re-tested and shown to fail a pocket test,
every chosen target is checked against the ordered subset-inclusion invariant (THEOREM.md), and the exact
maximum of (P x)_i / x_i is computed by integer cross-multiplication.  Last line: PASS or FAIL.
"""
import sys, time, lzma, resource
import multiprocessing as mp
from fractions import Fraction
from array import array
from collections import deque

K = int(sys.argv[2])
ARGS = sys.argv[3:]
def argval(name, default):
    return type(default)(ARGS[ARGS.index(name) + 1]) if name in ARGS else default
WORKERS = argval('--workers', 3)
LIMIT = argval('--limit', 0)
RAW3 = '--raw3' in ARGS
TARGET = Fraction(182926, 100000) - Fraction(2, 1000000)   # 1.82926 - 2e-6

# ---------------------------------------------------------------- lattice
OFF = {'E': ((-1, 1), (-1, -1), (1, 0)), 'N': ((1, -1), (-1, -1), (0, 1)),
       'W': ((1, 1), (1, -1), (-1, 0)), 'S': ((1, 1), (-1, 1), (0, -1))}
TYPE = {(1, 0): 'E', (2, 0): 'W', (0, 1): 'N', (0, 2): 'S'}
class NbrTable(dict):
    def __missing__(self, p):
        t = TYPE[(p[0] % 3, p[1] % 3)]
        r = tuple((p[0] + a, p[1] + b) for a, b in OFF[t])
        self[p] = r
        return r
NB = NbrTable()
def is_vertex(p): return (p[0] % 3, p[1] % 3) in TYPE
def g(s, x, y):
    sx = -x if s & 1 else x
    sy = -y if s & 2 else y
    return (sy, sx) if s & 4 else (sx, sy)

DT = {}
for rep in TYPE:
    d = {rep: 0}; frontier = [rep]
    for depth in range(1, K + 6):
        nxt = []
        for p in frontier:
            for q in NB[p]:
                if q not in d: d[q] = depth; nxt.append(q)
        frontier = nxt
    DT[rep] = d
def dist(p, q):
    rx = p[0] % 3; ry = p[1] % 3
    return DT[(rx, ry)].get((q[0] - p[0] + rx, q[1] - p[1] + ry), 9999)

# symmetries that send the (translated) head to (-1, 0); canonical heads are always (-1, 0)
HEADSYM = {}
for r in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    HEADSYM[r] = tuple(s for s in range(8) if g(s, *r) == (-1, 0))

def canon(walk):
    """walk: list of points oldest first.  Returns the key of its canonical form: bytes of neighbour indices stepping back from the head."""
    L = len(walk); ax, ay = walk[-1]
    rx = ax % 3; ry = ay % 3
    tx = ax - (-1 if rx == 2 else rx); ty = ay - (-1 if ry == 2 else ry)
    ss = HEADSYM[(ax - tx, ay - ty)]
    s = ss[0]
    if len(ss) > 1:
        s1 = ss[1]
        for i in range(L - 2, -1, -1):
            x = walk[i][0] - tx; y = walk[i][1] - ty
            a = g(s, x, y); b = g(s1, x, y)
            if a != b:
                if b < a: s = s1
                break
    pts = [g(s, p[0] - tx, p[1] - ty) for p in walk]
    return bytes([NB[pts[i]].index(pts[i - 1]) for i in range(L - 1, 0, -1)])

def decode(key):
    p = (-1, 0); pts = [p]
    for d in key:
        p = NB[p][d]; pts.append(p)
    pts.reverse()
    return pts

def inv_ok(ex, ids, key):
    """ordered subset-inclusion: key decodes to a sequence D with D[t] = sigma(ex[ids[t]]) for one sigma = (symmetry, translation by 3Z^2)."""
    D = decode(key)
    if len(D) != len(ids): return False
    if not (0 <= ids[0] and ids[-1] == len(ex) - 1 and all(ids[t] < ids[t + 1] for t in range(len(ids) - 1))): return False
    h = ex[ids[-1]]; dh = D[-1]
    for s in range(8):
        gh = g(s, *h)
        tx = dh[0] - gh[0]; ty = dh[1] - gh[1]
        if tx % 3 or ty % 3: continue
        for t in range(len(ids)):
            q = g(s, *ex[ids[t]])
            if q[0] + tx != D[t][0] or q[1] + ty != D[t][1]: break
        else:
            return True
    return False

# ---------------------------------------------------------------- finite-pocket test
STATS = {'ray_ok': 0, 'bfs': 0, 'bfs_cap': 0}
def escapes(s, B):
    """True iff s lies in an infinite component of G minus the vertex set B (s not in B).
    The search counter `count` caps the TOTAL number of vertices discovered (not the queue length) at 4096."""
    xs = [p[0] for p in B]; ys = [p[1] for p in B]
    mnx = min(xs); mxx = max(xs); mny = min(ys); mxy = max(ys)
    # quick proof of infinity: a path of strictly monotone coordinate that leaves the bounding box of B
    for f, bound in ((0, mxx), (1, mxy)):
        for sign in (1, -1):
            lim = bound if sign == 1 else (mnx if f == 0 else mny)
            seen = set(); stack = [s]
            while stack:
                p = stack.pop()
                v = p[f] * sign
                if v > lim * sign:
                    STATS['ray_ok'] += 1
                    return True
                for q in NB[p]:
                    if q[f] * sign > v and q not in B and q not in seen:
                        seen.add(q); stack.append(q)
    # full search (rarely reached): breadth-first search of the component, as in the definition
    STATS['bfs'] += 1
    lox = min(mnx, s[0]) - 2; hix = max(mxx, s[0]) + 2; loy = min(mny, s[1]) - 2; hiy = max(mxy, s[1]) + 2
    seen = set(B); seen.add(s); queue = deque([s]); count = 1
    while queue:
        p = queue.popleft()
        if p[0] < lox or p[0] > hix or p[1] < loy or p[1] > hiy: return True
        for q in NB[p]:
            if q not in seen:
                seen.add(q)
                count += 1
                if count > 4096: STATS['bfs_cap'] += 1; return True
                queue.append(q)
    return False

# ---------------------------------------------------------------- expansion of one state
def prune_start(ex, A):
    wL = len(ex); start = 0
    while start < wL - 2:
        if (wL - 1 - start) + dist(ex[start], A) <= K: break
        start += 1
    return start

def chords(w, ids, depth, min_a, out):
    wL = len(w)
    idx = {p: i for i, p in enumerate(w)}
    for a in range(min_a, wL - 3):
        bs = sorted(b for b in (idx.get(q) for q in NB[w[a]]) if b is not None and a + 2 <= b <= wL - 2)
        for b in bs:
            sx = w[:a + 1] + w[b:]; sids = ids[:a + 1] + ids[b:]
            st = prune_start(sx, sx[-1])
            out.append((canon(sx[st:]), sids[st:], sx))
            if depth < 3 and (len(sx) - 1) + dist(sx[0], sx[-1]) > K:
                chords(sx, sids, depth + 1, a, out)

def expand(key):
    """-> (noncanonical, bad_invariant, pruned1, pruned2, moves); moves = list of (ins_keys, second_keys)."""
    pts = decode(key)
    noncanon = 1 if canon(pts) != key else 0
    L = len(pts); head = pts[-1]; vset = set(pts)
    bad = 0; p1 = 0; p2 = 0; moves = []
    for A in NB[head]:
        if A in vset: continue
        ex = pts + [A]
        if not escapes(A, vset): p1 += 1; continue
        if not escapes(ex[0], set(ex[1:])): p2 += 1; continue
        ids = list(range(L + 1))
        st = prune_start(ex, A)
        ins = [canon(ex[st:])]
        if not inv_ok(ex, ids[st:], ins[0]): bad += 1
        sec = []
        if (L) + dist(ex[0], A) > K:          # (newL - 1) + dist, newL = L + 1
            out = []
            chords(ex, ids, 1, 0, out)
            for ck, cids, sx in out:
                ins.append(ck)
                # cids index into ex (ids were carried through the shortcuts)
                if not inv_ok(ex, cids, ck): bad += 1
            newL = L + 1
            for start in range(0, newL - 2):
                if (newL - 1 - start) + dist(ex[start], A) <= K: break
                k2 = canon(ex[start:])
                if not inv_ok(ex, ids[start:], k2): bad += 1
                sec.append(k2)
        moves.append((ins, sec))
    return (noncanon, bad, p1, p2, moves)

def work(keys):
    before = dict(STATS)
    r = [expand(k) for k in keys]
    return r, {k: STATS[k] - before[k] for k in STATS}

# ---------------------------------------------------------------- checks
fails = []
def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg, flush=True)
    if not ok: fails.append(msg)

def lattice_checks():
    ok = True
    for x in range(-9, 10):
        for y in range(-9, 10):
            if not is_vertex((x, y)): continue
            for q in NB[(x, y)]:
                ok &= is_vertex(q) and (x, y) in NB[q]
            for s in range(8):
                gp = g(s, x, y)
                ok &= is_vertex(gp) and sorted(g(s, *q) for q in NB[(x, y)]) == sorted(NB[gp])
            ok &= sorted((a + 3, b - 6) for a, b in NB[(x, y)]) == sorted(NB[(x + 3, y - 6)])
    check(ok, 'lattice: adjacency symmetric and 3-regular; the 8 symmetries about the origin and translations by 3Z^2 are automorphisms (window +-9)')
    ok = True
    for rep in TYPE:
        for f in (0, 1):
            ok &= any(q[f] > rep[f] for q in NB[rep]) and any(q[f] < rep[f] for q in NB[rep])
    # same for every vertex type shifted: neighbour offsets depend only on type
    check(ok, 'every vertex has a neighbour with strictly larger and one with strictly smaller x, and the same for y (monotone rays)')
    ok = True
    for x in range(-9, 10):
        for y in range(-9, 10):
            if is_vertex((x, y)):
                ok &= any(q[0] > x for q in NB[(x, y)]) and any(q[0] < x for q in NB[(x, y)])
                ok &= any(q[1] > y for q in NB[(x, y)]) and any(q[1] < y for q in NB[(x, y)])
    check(ok, 'monotone-ray property verified at every vertex of the window +-9')

def load_vec(path):
    raw = open(path, 'rb').read()
    if RAW3:
        N = len(raw) // 3
        E = raw[0::3]; Ml = raw[1::3]; Mh = raw[2::3]
        return [(Ml[i] | (Mh[i] << 8)) << E[i] for i in range(N)]
    data = lzma.decompress(raw)
    N = int.from_bytes(data[0:8], 'big'); assert data[8] == 1   # format version
    E = data[9:9 + N]; Mh = data[9 + N:9 + 2 * N]; Ml = data[9 + 2 * N:9 + 3 * N]
    assert len(data) == 9 + 3 * N
    return [((Mh[i] << 8) | Ml[i]) << E[i] for i in range(N)]

def main():
    t0 = time.time()
    lattice_checks()
    X = load_vec(sys.argv[1])
    check(min(X) > 0, 'all %d test-vector entries are positive integers (min %d, max %d)' % (len(X), min(X), max(X)))
    # seeds and edge classes
    seed_sq = canon([(1, 0), (0, 1)]); seed_oct = canon([(1, 0), (2, 0)])
    edge_keys = set()
    for x in range(-12, 13):
        for y in range(-12, 13):
            if is_vertex((x, y)):
                for q in NB[(x, y)]: edge_keys.add(canon([(x, y), q]))
    check(edge_keys == {seed_sq, seed_oct}, 'all directed edges in window +-12 reduce to the two seed states (%d classes)' % len(edge_keys))
    heads = set(canon([(x, y)]) for x in range(-12, 13) for y in range(-12, 13) if is_vertex((x, y)))
    check(len(heads) == 1, 'all vertices in the window are equivalent under the symmetry group: %d class' % len(heads))
    # ---- breadth-first rebuild of the state set
    index = {seed_sq: 0, seed_oct: 1}; keys = [seed_sq, seed_oct]
    mstart = array('I', [0])            # first move id of each processed state
    first = array('i')                  # per move: index of the plain candidate when it is the only one, else -1 - n into multi
    multi = []                          # per multi-candidate move: (first-pass indices tuple, second-pass resolved tuple, unresolved key tuple)
    tot = [0, 0, 0, 0]                  # noncanonical, bad invariant, pruned by test 1, pruned by test 2
    agg = {'ray_ok': 0, 'bfs': 0, 'bfs_cap': 0}
    ctx = mp.get_context('fork')
    pool = ctx.Pool(WORKERS)
    CH = 400
    pending = deque(); disp = 0; done = 0
    last = time.time()
    limit = LIMIT
    while True:
        while len(pending) < 4 * WORKERS and disp < len(keys) and (not limit or disp < limit):
            end = min(len(keys), disp + (CH if disp > 5000 else 20))
            if limit: end = min(end, limit)
            pending.append((disp, end, pool.apply_async(work, (keys[disp:end],)))); disp = end
        if not pending: break
        d0, d1, res = pending.popleft()
        data, st = res.get()
        for state_res in data:
            nc, bad, p1, p2, moves = state_res
            tot[0] += nc; tot[1] += bad; tot[2] += p1; tot[3] += p2
            for ins, sec in moves:
                idxs = []
                for k in ins:
                    j = index.get(k)
                    if j is None:
                        j = len(keys); index[k] = j; keys.append(k)
                    if j not in idxs and len(idxs) < 64: idxs.append(j)
                if len(idxs) == 1 and not sec:
                    first.append(idxs[0])
                else:
                    first.append(-1 - len(multi)); multi.append((tuple(idxs), tuple(sec)))
            mstart.append(len(first))
        done = d1
        for k2, v in st.items(): agg[k2] += v
        if time.time() - last > 120:
            last = time.time()
            print('   ... %d states processed of %d found, %.0fs' % (done, len(keys), last - t0), flush=True)
    pool.close(); pool.join()
    N = len(keys)
    print('states found %d, moves kept %d, pruned by test 1 %d, by test 2 %d, multi-candidate moves %d, %.0fs' % (N, len(first), tot[2], tot[3], len(multi), time.time() - t0), flush=True)
    print('pocket tests: monotone-ray proofs %d, full searches %d, full searches that hit the 4096 cap %d' % (agg['ray_ok'], agg['bfs'], agg['bfs_cap']))
    check(len(X) >= N if limit else len(X) == N, 'vector length %d against the rebuilt state count %d' % (len(X), N))
    check(agg['bfs_cap'] == 0, 'no full pocket search hit the 4096 cap, so every pocket decision is exact (cap hits: %d)' % agg['bfs_cap'])
    check(tot[0] == 0, 'every rebuilt state is in canonical form (non-canonical: %d)' % tot[0])
    check(tot[1] == 0, 'ordered subset-inclusion invariant holds for every candidate target examined (failures: %d)' % tot[1])
    # ---- resolve second-pass candidates, compute the exact ratio
    bn, bd, bi = 0, 1, -1
    nsec = 0; nsec_better = 0
    for i in range(len(mstart) - 1):
        Vi = X[i]; total = 0
        for m in range(mstart[i], mstart[i + 1]):
            f = first[m]
            if f >= 0:
                total += X[f]
            else:
                idxs, sec = multi[-1 - f]
                best = min(X[j] for j in idxs)
                for k in sec:
                    j = index.get(k)
                    if j is not None:
                        nsec += 1
                        if X[j] < best: best = X[j]; nsec_better += 1
                total += best
        if total * bd > bn * Vi: bn, bd, bi = total, Vi, i
    r = Fraction(bn, bd)
    print('second-pass candidates present in the state set (all enter the minimum): %d; of these, strictly lowering the running minimum: %d' % (nsec, nsec_better))
    print('exact max (P x)_i / x_i = %d / %d = %s = %.12f  (state index %d)' % (bn, bd, r, float(r), bi))
    check(r < TARGET, 'bound %s < 1.82926 - 2e-6 (exact rational comparison)' % r)
    sc = 2**30 if sys.platform == 'darwin' else 2**20
    print('elapsed %.0f s, peak resident memory: main process %.1f GB, largest worker %.1f GB' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / sc, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / sc))
    if limit:
        print('PARTIAL RUN (--limit): ratio over the first %d states only; never prints PASS' % (len(mstart) - 1))
        return 2
    check(K == 34 and N == 16873086, 'loop length K = 34 and 16,873,086 states, as claimed (K = %d, N = %d)' % (K, N))
    check(r == Fraction(169287, 92732), 'bound equals the claimed 169287/92732 exactly (got %s)' % r)
    print('PASS' if not fails else 'FAIL (%d)' % len(fails))
    return 0 if not fails else 1
if __name__ == '__main__':
    sys.exit(main())
