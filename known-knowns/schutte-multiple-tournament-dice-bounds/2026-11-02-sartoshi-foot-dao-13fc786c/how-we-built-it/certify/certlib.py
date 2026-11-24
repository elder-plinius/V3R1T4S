"""Certification library (D-023). Builds every CNF of the certificate: the leaf cubes with the unchanged v2 encoder
(encoder/cube.py, encoder/cube3.py, byte-identical to runs/2026-10-27-1144/attempts/solver/code), and the cover lemmas
(one per refined node) described in README.md. No solver here; see solve.py."""
import sys, os, math, itertools, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'encoder'))
import cube, cube3  # noqa: E402  (unchanged v2 encoder)
from pysat.card import CardEnc, EncType  # noqa: E402

ENCODER_SHA = {'cube.py': 'dd42ba4e16c06871589f810b66744c08df867e87c151b6dd99ce632eb0db9463',
               'cube3.py': 'bb8a12d2caa2480af47120513dc9653346717af015a1b69bf5ee9cb024d27e9a',
               'checker.py': '25a1e6f6814c4ff449f72e98684732c6ae3e3fd5ba456f590e725b2e4530ed06'}
CELLS = {'m3k6n12': (3, 6, 12), 'm2k5n13': (2, 5, 13)}

def check_encoder():
    for f, h in ENCODER_SHA.items():
        got = hashlib.sha256(open(os.path.join(HERE, 'encoder', f), 'rb').read()).hexdigest()
        assert got == h, f'encoder file {f} changed: {got}'

# ---------------------------------------------------------------- tree (from the ledgers of runs 0844 and 1144)
def l1_cubes(n):
    return [(d, a, b) for d in range((n - 1 + 1) // 2, n) for a in range(d + 1) for b in range(n - d) if a + b <= d]

def l2_children(n, d, a, b):  # v2: only sum(c) <= a+b (PREREG.v2 of run 0844; audit.py of run 1144)
    sizes = [a, d - a, b, n - 1 - d - b]
    return [c for c in itertools.product(*[range(s + 1) for s in sizes]) if sum(c) <= a + b]

def l3_children(n, d, a, b, c):
    return cube3.l3_params(n, d, a, b, list(c))

def cid1(d, a, b): return f'{d}_{a}_{b}'
def cid2(d, a, b, c): return f'{d}_{a}_{b}_' + '-'.join(map(str, c))
def cid3(d, a, b, c, l3): return cid2(d, a, b, c) + '_L3_' + '_'.join(map(str, l3))

def tree(ws):
    """Returns (leaves, covers) for both cells. A leaf is (cell, level, params); a cover is (cell, level, parent params).
    Leaf/refinement structure is read from the ledgers exactly as runs/2026-10-27-1144/attempts/already-settled/code/audit.py does."""
    R = lambda p: [l.rstrip('\n').split('\t') for l in open(p)] if os.path.exists(p) else []
    v = collections.defaultdict(set); secs = {}
    for r in R(f'{ws}/runs/2026-10-27-1144/attempts/solver/ledger_m3k6n12.tsv') + R(f'{ws}/runs/2026-10-27-1144/attempts/solver/ledger_m3k6n12_L2.tsv'):
        v['m3k6n12/' + r[0]].add(r[5])
        if r[5] == 'UNSAT': secs['m3k6n12/' + r[0]] = float(r[6])
    for r in R(f'{ws}/runs/2026-10-27-1144/attempts/solver/ledger_run1144.tsv'):
        v['m3k6n12/' + r[0]].add(r[7])
        if r[7] == 'UNSAT': secs['m3k6n12/' + r[0]] = float(r[9]) if r[9] != '-' else float(r[8])
    for r in R(f'{ws}/runs/2026-10-27-0844/attempts/solver/ledger_m2k5n13.tsv'):
        v['m2k5n13/' + r[0]].add(r[5])
        if r[5] == 'UNSAT': secs['m2k5n13/' + r[0]] = float(r[6])
    assert not any('SAT' in x for x in v.values())
    leaves, covers = [], []
    # (2,5,13): run 0844 cover, 196 level-1 cubes; 3 closed there by counting only (no solver UNSAT), kept as leaves (tier 'hard')
    covers.append(('m2k5n13', 1, ()))
    cs = l1_cubes(13); assert len(cs) == 196
    for p in cs: leaves.append(('m2k5n13', 1, p, secs.get('m2k5n13/' + cid1(*p))))
    # (3,6,12): run 0844/1144 cover
    covers.append(('m3k6n12', 1, ()))
    cs = l1_cubes(12); assert len(cs) == 147
    for d, a, b in cs:
        if 'UNSAT' in v['m3k6n12/' + cid1(d, a, b)]:
            leaves.append(('m3k6n12', 1, (d, a, b), secs['m3k6n12/' + cid1(d, a, b)])); continue
        covers.append(('m3k6n12', 2, (d, a, b)))
        for c in l2_children(12, d, a, b):
            k = 'm3k6n12/' + cid2(d, a, b, c)
            if 'UNSAT' in v[k]: leaves.append(('m3k6n12', 2, (d, a, b, c), secs[k])); continue
            covers.append(('m3k6n12', 3, (d, a, b, c)))
            for l3 in l3_children(12, d, a, b, c):
                k3 = 'm3k6n12/' + cid3(d, a, b, c, l3)
                assert 'UNSAT' in v[k3], k3
                leaves.append(('m3k6n12', 3, (d, a, b, c, l3), secs[k3]))
    return leaves, covers

def leaf_id(cell, level, p):
    return f'{cell}/' + {1: lambda: cid1(*p), 2: lambda: cid2(*p), 3: lambda: cid3(*p)}[level]()

def cover_id(cell, level, p):
    return f'{cell}/COVER{level}' + ('' if not p else '/' + (cid1(*p) if level == 2 else cid2(*p)))

# ---------------------------------------------------------------- leaf CNFs (unchanged encoder)
def leaf_cnf(cell, level, p):
    m, k, n = CELLS[cell]
    if level == 1: d, a, b = p; nv, cl, lit = cube3.build3(m, k, n, d, a, b, None, None)
    elif level == 2: d, a, b, c = p; nv, cl, lit = cube3.build3(m, k, n, d, a, b, list(c), None)
    else: d, a, b, c, l3 = p; nv, cl, lit = cube3.build3(m, k, n, d, a, b, list(c), tuple(l3))
    return nv, cl, lit

# ---------------------------------------------------------------- cover lemmas
class Cnf:
    def __init__(self, top): self.top = top; self.cl = []
    def new(self): self.top += 1; return self.top
    def add(self, c): self.cl.append(c)

TRUE, FALSE = 'T', 'F'

def counter(F, lits):
    """Exact unary counter: s[i][k] <-> (at least k of lits[:i] true), both directions, so the honest assignment
    (each s equal to its definition) satisfies every clause. Returns ge(k) giving a literal / TRUE / FALSE."""
    L = len(lits); s = [[None] * (L + 2) for _ in range(L + 1)]
    for i in range(L + 1):
        for kk in range(L + 2): s[i][kk] = TRUE if kk == 0 else (FALSE if kk > i else None)
    def clause(*xs):
        out = []
        for x in xs:
            neg = isinstance(x, tuple)
            y = x[1] if neg else x
            if y == TRUE: y = FALSE if neg else TRUE
            elif y == FALSE: y = TRUE if neg else FALSE
            elif neg: y = -y
            if y == TRUE: return
            if y == FALSE: continue
            out.append(y)
        assert out, 'empty clause in counter'
        F.add(out)
    N = lambda x: ('neg', x)
    for i in range(1, L + 1):
        x = lits[i - 1]
        for kk in range(1, i + 1):
            s[i][kk] = F.new()
            clause(N(s[i - 1][kk]), s[i][kk])                    # s[i-1][k] -> s[i][k]
            clause(N(s[i - 1][kk - 1]), N(x), s[i][kk])          # s[i-1][k-1] & x -> s[i][k]
            clause(N(s[i][kk]), s[i - 1][kk], s[i - 1][kk - 1])  # s[i][k] -> s[i-1][k] | s[i-1][k-1]
            clause(N(s[i][kk]), s[i - 1][kk], x)                 # s[i][k] -> s[i-1][k] | x
    def ge(kk):
        if kk <= 0: return TRUE
        if kk > L: return FALSE
        return s[L][kk]
    return ge

def le_cmp(F, ge_small, ge_big, L):
    """count(small) <= count(big): ge_small(k) -> ge_big(k) for k = 1..L."""
    for kk in range(1, L + 1):
        a, b = ge_small(kk), ge_big(kk)
        if a == FALSE or b == TRUE: continue
        if a == TRUE and b == FALSE: F.add([]); continue
        if a == TRUE: F.add([b]); continue
        if b == FALSE: F.add([-a]); continue
        F.add([-a, b])

def split_child(parent, child, nx):
    """child = parent + extra (exact prefix); returns (units, nonunits) of the extra clauses; units must be on X vars."""
    assert child[:len(parent)] == parent, 'child CNF does not extend the parent CNF'
    extra = child[len(parent):]
    units = [c[0] for c in extra if len(c) == 1]; non = [c for c in extra if len(c) != 1]
    assert all(abs(u) <= nx for u in units)
    return units, non

def regen_am(specs, top):
    """Regenerates the encoder's seqcounter at-most constraints for the given (lits, bound) specs in order."""
    out = []
    for lits, bound in specs:
        enc = CardEnc.atmost(lits=lits, bound=bound, top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv); out.extend(enc.clauses)
    return out, top

def cover_cnf(cell, level, p):
    """Cover lemma for one refined node. Returns (nvars, clauses, meta). UNSAT means: every assignment of the arc variables
    that satisfies the parent's non-Definition-2.2 clauses and the normal form NF(level) satisfies L_j and the cardinality
    meaning of R_j for some child j (README.md, 'Cover lemmas')."""
    m, k, n = CELLS[cell]
    nx = m * n * (n - 1) // 2
    ndef = math.comb(n, k) * m * (n - k)   # Definition 2.2 auxiliaries d(U,t,v), numbered nx+1..nx+ndef by cube.build
    meta = {'children': 0}
    if level == 1:
        kids = l1_cubes(n)
        # parent = Definition 2.2 clauses only; it is the common prefix of all child CNFs and is dropped from the lemma
        _, c0, lit = leaf_cnf(cell, 1, kids[0])
        par = [c for c in c0 if any(nx < abs(x) <= nx + ndef for x in c)]
        assert c0[:len(par)] == par
        F = Cnf(nx + ndef)
        rows = {(t, v): [lit(t, v, u) for u in range(n) if u != v] for t in range(m) for v in range(n)}
        GE = {r: counter(F, ls) for r, ls in rows.items()}
        b = lambda t, u: lit(t, 0, u)
        for u in range(1, n - 1):  # NF: T_1 row of vertex 0 is a prefix 1..d
            F.add([-b(0, u + 1), b(0, u)])
        for u in range(1, n - 1):  # NF: T_2 row of vertex 0 is a prefix inside A = T_1-out(0) and inside B
            F.add([-b(0, u), -b(0, u + 1), -b(1, u + 1), b(1, u)])
            F.add([b(0, u), b(0, u + 1), -b(1, u + 1), b(1, u)])
        for r in rows:  # NF: (T_1, vertex 0) has the maximum out-degree among all m*n rows
            if r != (0, 0): le_cmp(F, GE[r], GE[(0, 0)], n - 1)
        if m >= 3: le_cmp(F, GE[(2, 0)], GE[(1, 0)], n - 1)  # NF (v2): T_3 row of 0 no larger than T_2 row of 0
        for d, a, bb in kids:
            nv, ch, lit2 = leaf_cnf(cell, 1, (d, a, bb))
            units, non = split_child(par, ch, nx)
            specs = [(rows[(t, v)], d) for t in range(m) for v in range(n)]
            pre_units = units  # the encoder appends: AM_d clauses, then the units, then the v2 clauses
            r_clauses = non
            v2spec = []
            if m >= 3 and a + bb > 0: v2spec = [([lit(2, 0, u) for u in range(1, n)], a + bb)]
            regen, _ = regen_am(specs + v2spec, nx + ndef)
            assert r_clauses == regen, f'R_j mismatch for {(d, a, bb)}'
            cl = [-u for u in pre_units]
            for ls, bound in specs + v2spec:
                key = [r for r in rows if rows[r] == ls]
                gl = (GE[key[0]] if key else counter(F, ls))(bound + 1)
                if gl == TRUE: cl = None; break
                if gl != FALSE: cl.append(gl)
            if cl is not None: F.add(cl)
            meta['children'] += 1
        return F.top, F.cl, meta
    if level == 2:
        d, a, bb = p
        nvp, par_full, lit = leaf_cnf(cell, 1, (d, a, bb))
        par = [c for c in par_full if not any(nx < abs(x) <= nx + ndef for x in c)]  # parent minus Definition 2.2 clauses
        F = Cnf(max(nvp, max(abs(x) for c in par_full for x in c))); F.cl.extend(par)
        blocks = [list(range(1, a + 1)), list(range(a + 1, d + 1)), list(range(d + 1, d + bb + 1)), list(range(d + bb + 1, n))]
        for blk in blocks:  # NF: T_3 row of vertex 0 is a prefix inside each block
            for u, w in zip(blk, blk[1:]): F.add([-lit(2, 0, w), lit(2, 0, u)])
        for c in l2_children(n, d, a, bb):
            _, ch, _ = leaf_cnf(cell, 2, (d, a, bb, c))
            units, non = split_child(par_full, ch, nx)
            assert non == []
            F.add([-u for u in units]); meta['children'] += 1
        return F.top, F.cl, meta
    if level == 3:
        d, a, bb, c = p
        nvp, par_full, lit = leaf_cnf(cell, 2, (d, a, bb, c))
        par = [cc for cc in par_full if not any(nx < abs(x) <= nx + ndef for x in cc)]
        top0 = max(nvp, max(abs(x) for cc in par_full for x in cc))
        F = Cnf(top0); F.cl.extend(par)
        C = cube3.pivot_cell(n, d, a, bb, list(c)); z = len(C); s = C[0]
        rows = {u: [lit(0, u, w) for w in C if w != u] for u in C}
        GE = {u: counter(F, rows[u]) for u in C}
        o = C[1:]
        for u, w in zip(o, o[1:]):  # NF: pivot s's T_1 row inside C is a prefix C[1..e]
            F.add([-lit(0, s, w), lit(0, s, u)])
        for u, w in zip(o, o[1:]):  # NF: s's T_2 row is a prefix inside A' and inside B'
            F.add([-lit(0, s, u), -lit(0, s, w), -lit(1, s, w), lit(1, s, u)])
            F.add([lit(0, s, u), lit(0, s, w), -lit(1, s, w), lit(1, s, u)])
        for u in C:  # NF: s has the maximum T_1 out-degree inside C
            if u != s: le_cmp(F, GE[u], GE[s], z - 1)
        for l3 in l3_children(n, d, a, bb, c):
            nv3, ch, _ = leaf_cnf(cell, 3, (d, a, bb, c, l3))
            units, non = split_child(par_full, ch, nx)
            e = l3[0]
            regen, _ = regen_am([(rows[u], e) for u in C], nvp)
            assert non == regen, f'R_j mismatch {l3}'
            cl = [-x for x in units]
            for u in C:
                g = GE[u](e + 1)
                if g == TRUE: cl = None; break
                if g != FALSE: cl.append(g)
            if cl is not None: F.add(cl)
            meta['children'] += 1
        return F.top, F.cl, meta
    raise ValueError(level)

def write_dimacs(path, nv, cl):
    nv = max([nv] + [abs(x) for c in cl for x in c])
    h = hashlib.sha256()
    with open(path, 'w') as f:
        hdr = f'p cnf {nv} {len(cl)}\n'; f.write(hdr); h.update(hdr.encode())
        for c in cl:
            line = ' '.join(map(str, c)) + ' 0\n'; f.write(line); h.update(line.encode())
    return h.hexdigest(), nv, len(cl)
