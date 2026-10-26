#!/usr/bin/env python3
"""Exhaustive box-level checks of the large gadgets used by the C7 construction (standard library only).

Usage: python3 check_box_axioms.py OBJECT_DIR

A "box" is a product of explicit word lists (factors) of dimension 10 and 5.  Every large set of the construction is a finite
union of boxes (Lemma 1 / Theorem 1 give the sets explicitly).  Two facts are used and nothing else:
  (a) a box is independent iff each factor is independent (a product of independent sets is independent);
  (b) two boxes are separated (no word of one confusable with a word of the other) if in at least one coordinate block the two
      factors are separated; N(A x B) = N(A) x N(B).
For a union of boxes this gives an exhaustive proof of independence (each factor is checked word by word; each pair of boxes is
checked factor by factor), without listing the 10^15 words.  If a pair of boxes were not separated in any factor, the check
reports failure (it does not try finer arguments).

Checks:
  A. I15 (main code of Gao(G10,G5), 49,495,055 words), hence J15 = T^3(I15), and the sets PH15, PV15, X15X = X10 x X5,
     X15het (eq. 156) and X15^{A,het}: independent.
  B. Dimension-15 private-pair property of G15 = Gao(G10, G5): R15 in I15, 2,504,616 private neighbours q, each outside I15
     and confusable with exactly one word of I15, which is its centre; the 2 x 2,504,616 endpoints are distinct.
  C. I30++ (main code of Gao(G15het, G15het), 2,455,726,444,728,097 words), hence J30++ = T^6(I30++): independent.
  D. Condition (33) at dimension 30: the codebook Xhat30 (auxiliary set of the sibling gadget over the ordered pair
     (G15AX, sigma G15Ah)) is independent, is confusable with no word of both transversals of G30L, and its class sizes
     relative to the transversals of G30L are those of the paper.  J30++ (used in the JH, JV positions) needs only
     independence, which is C together with the fact that T is an automorphism.
The transversals of G30L = Gao(G15AX, sigma G15Ah) are, by eq. (18): PH = (PH15A x V0) u (U0 x PH15A), PV = (PV15A x V0) u (U0 x PV15A),
U0, V0 the neutral parts of the auxiliary sets of G15AX and G15Ah and PH15A, PV15A the transversals of G15AX = G15Ah.
"""
import os, sys, json, time
from collections import Counter, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c7_lib as L

FAILS = []
T0 = time.time()


def check(c, msg):
    print(("  [ok]   " if c else "  [FAIL] ") + msg + "  [%.0fs]" % (time.time() - T0))
    sys.stdout.flush()
    if not c:
        FAILS.append(msg)


NBL = None
T5 = None
_LRU = OrderedDict()
LRU_MAX = 12


class Lst:
    def __init__(self, name, words, dim):
        self.name, self.words, self.dim = name, list(words), dim
        self._indep = None
        self._nflag = None
        self._cnt = None

    def __len__(self):
        return len(self.words)

    # ---- dimension 10: neighbourhood membership
    def N(self):
        s = _LRU.get(id(self))
        if s is None:
            s = L.SetN(NBL, self.words)
            _LRU[id(self)] = s
            if len(_LRU) > LRU_MAX:
                _LRU.popitem(last=False)
        else:
            _LRU.move_to_end(id(self))
        return s

    # ---- dimension 5
    def flag(self):
        if self._nflag is None:
            self._nflag = L.nflag(NBL, self.words)
        return self._nflag

    def count5(self):
        """c[x] = number of words of the list confusable with x"""
        if self._cnt is None:
            c = [0] * L.N5
            for w in self.words:
                for x in NBL[w]:
                    c[x] += 1
            self._cnt = c
        return self._cnt

    def independent(self):
        if self._indep is None:
            if self.dim == 5:
                c = self.count5()
                self._indep = len(set(self.words)) == len(self.words) and all(c[w] == 1 for w in self.words)
            else:
                self._indep = L.independent10(NBL, self.words)
        return self._indep


def separated(l1, l2):
    if l1.dim == 5:
        f = l2.flag()
        return not any(f[w] for w in l1.words)
    n = l2.N()
    return not any(n(a, b) for a, b in l1.words)


_sepc = {}


def sep(l1, l2):
    k = (id(l1), id(l2))
    if k not in _sepc:
        _sepc[k] = separated(l1, l2)
    return _sepc[k]


def boxes_independent(name, boxes):
    """boxes: list of tuples of Lst factors (same shape).  True iff every factor is independent and every two boxes are
    separated in at least one factor."""
    ok = all(f.independent() for bx in boxes for f in bx)
    # order the pair tests so that the same right-hand list is reused while its neighbourhood structure is cached
    bad = 0
    n = len(boxes)
    for j in range(n):
        for i in range(j):
            bi, bj = boxes[i], boxes[j]
            if not any(sep(fi, fj) for fi, fj in zip(bi, bj)):
                bad += 1
    check(ok and bad == 0, "%s: %d boxes, all factors independent, %d of %d box pairs not separated in any factor" % (name, n, bad, n * (n - 1) // 2))
    return ok and bad == 0


def tot(boxes):
    s = 0
    for bx in boxes:
        p = 1
        for f in bx:
            p *= len(f)
        s += p
    return s


def main(objdir):
    global NBL, T5
    I5, X5, pairs = L.load_base(os.path.join(objdir, "base_g5.json"))
    cin = json.load(open(os.path.join(objdir, "cert_input.json")))
    PVAL = cin["paper_values"]
    NBL = L.build_neighbours()
    T5 = [L.T5(n) for n in range(L.N5)]
    R5 = [r for r, q, s in pairs]
    Q5 = [q for r, q, s in pairs]
    PH5, PV5 = L.ph_pv(pairs)
    B5 = [w for w in I5 if w not in set(R5)]
    nPH, nPV = L.nflag(NBL, PH5), L.nflag(NBL, PV5)
    XH5 = [x for x in X5 if nPH[x]]
    XV5 = [x for x in X5 if nPV[x]]
    X05 = [x for x in X5 if not nPH[x] and not nPV[x]]
    mk5 = lambda nm, w: Lst(nm, w, 5)
    lB5, lR5, lQ5, lPH5, lPV5, lX0, lXH, lXV, lX5 = [mk5(n, w) for n, w in (("B5", B5), ("R5", R5), ("Q5", Q5), ("PH5", PH5), ("PV5", PV5), ("X5^0", X05), ("X5^H", XH5), ("X5^V", XV5), ("X5", X5))]
    nX0 = lX0.flag()

    # ----- 10-dimensional sets of G10 = Gao(G5,G5)
    def nPH10(a, b, o="std"):
        if o == "std":
            return bool((nPH[a] and nX0[b]) or (nX0[a] and nPV[b]))
        return bool((nPV[a] and nX0[b]) or (nX0[a] and nPV[b]))

    def nPV10(a, b, o="std"):
        if o == "std":
            return bool((nPV[a] and nX0[b]) or (nX0[a] and nPH[b]))
        return bool((nPH[a] and nX0[b]) or (nX0[a] and nPH[b]))
    X10 = [(x, y) for x in X5 for y in X5]
    X10_0 = [u for u in X10 if not nPH10(*u) and not nPV10(*u)]
    X10_H = [u for u in X10 if nPH10(*u) and not nPV10(*u)]
    X10_V = [u for u in X10 if nPV10(*u) and not nPH10(*u)]
    X05s, XH5s = set(X05), set(XH5)
    Lset = lambda x: R5 if x in X05s else (PH5 if x in XH5s else PV5)
    Kset = lambda y: R5 if y in X05s else (PV5 if y in XH5s else PH5)
    R10 = [(r, x) for r in R5 for x in X05] + [(y, r) for y in X05 for r in R5]
    Q10 = [(q, x) for q in Q5 for x in X05] + [(y, q) for y in X05 for q in Q5]
    I10 = [(a, b) for a in B5 for b in B5] + [(p, x) for x in X5 for p in Lset(x)] + [(y, q) for y in X5 for q in Kset(y)]
    R10s = set(R10)
    B10 = [w for w in I10 if w not in R10s]
    PH10 = [(p, x) for p in PH5 for x in X05] + [(x, p) for x in X05 for p in PV5]
    PV10 = [(p, x) for p in PV5 for x in X05] + [(x, p) for x in X05 for p in PH5]
    PH10A = [(p, x) for p in PV5 for x in X05] + [(x, p) for x in X05 for p in PV5]
    PV10A = [(p, x) for p in PH5 for x in X05] + [(x, p) for x in X05 for p in PH5]
    mk10 = lambda nm, w: Lst(nm, w, 10)
    lB10, lR10, lQ10, lPH10, lPV10, lPH10A, lPV10A, lX10_0, lX10_H, lX10_V = [mk10(n, w) for n, w in (
        ("B10", B10), ("R10", R10), ("Q10", Q10), ("PH10", PH10), ("PV10", PV10), ("PH10A", PH10A), ("PV10A", PV10A), ("X10^0", X10_0), ("X10^H", X10_H), ("X10^V", X10_V))]
    N_X10_0 = lX10_0.N()
    # J+ (exchanges of eq. 152)
    J = {(T5[a], T5[b]) for a, b in I10}
    ex = [(tuple(r), tuple(i)) for r, i in cin["exchanges"]]
    Jp = sorted((J - {r for r, i in ex}) | {i for r, i in ex})
    check(len(Jp) == 134753, "J+ rebuilt (134753 words)")

    # ----- 15-dimensional boxes
    I15 = [(lB10, lB5), (lR10, lX0), (lPH10, lXH), (lPV10, lXV), (lX10_0, lR5), (lX10_H, lPV5), (lX10_V, lPH5)]
    R15 = [(lR10, lX0), (lX10_0, lR5)]
    Q15 = [(lQ10, lX0), (lX10_0, lQ5)]
    PH15 = [(lPH10, lX0), (lX10_0, lPV5)]
    PV15 = [(lPV10, lX0), (lX10_0, lPH5)]
    PH15A = [(lPH10A, lX0), (lX10_0, lPV5)]
    PV15A = [(lPV10A, lX0), (lX10_0, lPH5)]
    check(tot(I15) == 49495055 and tot(R15) == 2504616 and tot(Q15) == 2504616, "|I15| = 49495055, |R15| = |Q15| = 2504616")

    # groups of X10 and J+ by the signatures that decide the class of a 15-dimensional word
    def usig(a, b):
        return (nPH10(a, b), nPV10(a, b), nPH10(a, b, "A"), nPV10(a, b, "A"), bool(N_X10_0(a, b)))

    def group_by(words, f):
        d = {}
        for w in words:
            d.setdefault(f(w), []).append(w)
        return d
    X10g = {k: mk10("X10" + str(k), v) for k, v in group_by(X10, lambda w: usig(*w)).items()}
    for k, g in X10g.items():
        g.sig = k
    Jg = {k: mk10("J+" + str(k), v) for k, v in group_by(Jp, lambda w: bool(N_X10_0(*w))).items()}
    for k, g in Jg.items():
        g.sig = (None, None, None, None, k)
    vcls = {"0": lX0, "H": lXH, "V": lXV}

    def cls15(sig, vc, o):
        ih, iv = (0, 1) if o == "std" else (2, 3)
        vX0, vPH, vPV = vc == "0", vc == "H", vc == "V"
        if vX0:
            n_ph, n_pv = sig[ih], sig[iv]
        else:
            assert sig[4] is not None
            n_ph = vPV and sig[4]
            n_pv = vPH and sig[4]
        assert not (n_ph and n_pv)
        return "H" if n_ph else ("V" if n_pv else "0")

    def aux(o, spec):
        out = {"0": [], "H": [], "V": []}
        for ugroups, vc in spec:
            for g in ugroups.values():
                out[cls15(g.sig, vc, o)].append((g, vcls[vc]))
        return out
    allX10 = X10g
    XXs = aux("A", [(X10g, "0"), (X10g, "H"), (X10g, "V")])             # X10 x X5 with the transversals of G15AX
    Xhet = aux("std", [(X10g, "0"), (Jg, "H"), (Jg, "V")])              # eq. (156) with the transversals of G15 (std)
    XA = aux("A", [(X10g, "0"), (Jg, "H"), (X10g, "V")])                # auxiliary set of G15Ah
    U0, U1 = XXs["0"], XXs["H"] + XXs["V"]
    V0 = XA["0"]
    check([tot(Xhet["0"]), tot(Xhet["H"]), tot(Xhet["V"])] == [35275258, 6703815, 7454670], "X15het classes (o,h,v) = %s" % str([tot(Xhet["0"]), tot(Xhet["H"]), tot(Xhet["V"])]))

    # ------------------------------------------------------------ A. independence at dimension 15
    print("-- A. independence of the 15-dimensional sets (box level, exhaustive)")
    boxes_independent("I15 (49,495,055 words; J15 = T^3(I15) is its image under an automorphism)", I15)
    boxes_independent("PH15", PH15)
    boxes_independent("PV15", PV15)
    boxes_independent("X15X = X10 x X5", XXs["0"] + XXs["H"] + XXs["V"])
    boxes_independent("X15het (eq. 156, auxiliary set of G15het)", Xhet["0"] + Xhet["H"] + Xhet["V"])
    boxes_independent("X15^{A,het} (auxiliary set of G15Ah)", XA["0"] + XA["H"] + XA["V"])

    # ------------------------------------------------------------ B. private pairs at dimension 15
    print("-- B. private-pair property of G15 = Gao(G10, G5), exhaustive over the 2,504,616 pairs")
    # every q-word w = (u, v): count the words of I15 confusable with w; need exactly 1, and the centre r is confusable with q
    # (r and q differ by a private pair of G5 in one block, equal elsewhere) and r lies in I15.
    # counts of a 10-dimensional list near u: sum over first-block neighbours.
    ptr = {}

    def cnt10(lst, u):
        b = ptr.get(id(lst))
        if b is None:
            b = {}
            for a1, a2 in lst.words:
                b.setdefault(a1, []).append(a2)
            ptr[id(lst)] = b
        u1, u2 = u
        nb2 = set(NBL[u2])
        c = 0
        for a1 in NBL[u1]:
            bk = b.get(a1)
            if bk:
                for a2 in bk:
                    if a2 in nb2:
                        c += 1
        return c
    cB = [bx[1].count5() for bx in I15]
    NA = [bx[0] for bx in I15]
    viol = 0
    tested = 0
    # r in I15: R15 boxes are literally boxes of I15
    check(all(any(r[0] is b[0] and r[1] is b[1] for b in I15) for r in R15), "the centres R15 are boxes of I15")
    for (A, B) in Q15:
        cache = {}
        for u in A.words:
            c_us = []
            for k, bx in enumerate(I15):
                if NA[k].N()(*u):
                    c_us.append((k, cnt10(NA[k], u)))
            for v in B.words:
                s = 0
                for k, cu in c_us:
                    s += cu * cB[k][v]
                tested += 1
                if s != 1:
                    viol += 1
    check(tested == 2504616 and viol == 0, "private-pair property at dimension 15: %d private neighbours q tested; each is confusable with exactly one word of I15 (the centre r, which is confusable with q since r, q differ by a private pair of G5 in one block); violations %d" % (tested, viol))
    # q-words are distinct and outside the centres: the two Q boxes are disjoint, and Q15 and I15 are disjoint (count 1 above plus r~q)
    disjoint = not (set(lQ10.words) & set(lX10_0.words)) or not (set(lX0.words) & set(lQ5.words))
    check(disjoint, "the two boxes of Q15 are disjoint (all 2504616 endpoints q distinct); the endpoints r are distinct because R15 sits in the independent set I15 as two disjoint boxes")

    # ------------------------------------------------------------ C. independence of I30++
    print("-- C. independence of I30++ (main code of Gao(G15het, G15het)) at box level")
    X15c = {"0": Xhet["0"], "H": Xhet["H"], "V": Xhet["V"]}
    B15 = [(lB10, lB5), (lPH10, lXH), (lPV10, lXV), (lX10_H, lPV5), (lX10_V, lPH5)]
    check(tot(B15) + tot(R15) == tot(I15), "I15 = B15 + R15")
    Sx = {"B": B15, "R": R15, "X0": X15c["0"], "XH": X15c["H"], "XV": X15c["V"], "PH": PH15, "PV": PV15}
    comps = [("B", "B"), ("R", "X0"), ("PH", "XH"), ("PV", "XV"), ("X0", "R"), ("XH", "PV"), ("XV", "PH")]
    boxes30 = []
    for a, b in comps:
        for ba in Sx[a]:
            for bb in Sx[b]:
                boxes30.append((ba[0], ba[1], bb[0], bb[1]))
    check(tot(boxes30) == PVAL["I30pp"], "I30++ as %d four-factor boxes, %d words in total (eq. 137)" % (len(boxes30), tot(boxes30)))
    boxes_independent("I30++ (2,455,726,444,728,097 words; J30++ = T^6(I30++) is its image under an automorphism)", boxes30)

    # ------------------------------------------------------------ D. condition (33) at dimension 30
    print("-- D. condition (33) for Xhat30 against the transversals of G30L, dimension 30")
    # J15 = T^3(I15) and the other codebook parts as 15-dimensional box lists
    def tr_list(l):
        if l.dim == 10:
            return Lst(l.name + "^T", [(T5[a], T5[b]) for a, b in l.words], 10)
        return Lst(l.name + "^T", [T5[w] for w in l.words], 5)
    J15 = [(tr_list(a), tr_list(b)) for a, b in I15]
    J0b = XA["0"] + XA["H"] + XA["V"]
    JVb = XXs["0"] + XXs["H"] + XXs["V"]
    VH, VV = XA["H"], XA["V"]            # classes of X^{A,het} in G15Ah orientation; the right gadget is sigma(G15Ah): H and V exchanged
    xhat_boxes = []
    for L15, R15c in ((J0b, V0), (J15, VV), (JVb, VH)):
        for la in L15:
            for rb in R15c:
                xhat_boxes.append((la[0], la[1], rb[0], rb[1]))
    check(tot(xhat_boxes) == 2444076335041121, "|Xhat30| = %d (paper: 2444076335041121)" % tot(xhat_boxes))
    boxes_independent("Xhat30 (auxiliary set of the sibling gadget), four-factor boxes", xhat_boxes)

    # flags of 15-dimensional words relative to PH15A, PV15A, U0, V0
    refs = [PH15A, PV15A, U0, V0]

    def hist(boxes, tr):
        ags, bgs = [], []
        for r in refs:
            for g, h in r:
                if g not in ags:
                    ags.append(g)
                if h not in bgs:
                    bgs.append(h)
        agi = {id(g): i for i, g in enumerate(ags)}
        bgi = {id(g): i for i, g in enumerate(bgs)}
        for g in ags:
            g.N()
        out = Counter()
        for A, B in boxes:
            hu = Counter()
            for a, b in A.words:
                if tr:
                    a, b = T5[a], T5[b]
                hu[tuple(g.N()(a, b) for g in ags)] += 1
            hv = Counter()
            for v in B.words:
                if tr:
                    v = T5[v]
                hv[tuple(bool(g.flag()[v]) for g in bgs)] += 1
            for ku, cu in hu.items():
                for kv, cv in hv.items():
                    key = tuple(any(ku[agi[id(g)]] and kv[bgi[id(h)]] for g, h in r) for r in refs)
                    out[key] += cu * cv
        return out
    hJ0, hJV = hist(J0b, False), hist(JVb, False)
    hJH = hist(J15, False)             # J15 lists are already transformed
    hR0, hRV, hRH = hist(V0, False), hist(VV, False), hist(VH, False)

    def combine(Lh, Rh):
        c = Counter()
        for (uPH, uPV, uU0, uV0), nu in Lh.items():
            for (vPH, vPV, vU0, vV0), nv in Rh.items():
                nph = (uPH and vV0) or (uU0 and vPH)
                npv = (uPV and vV0) or (uU0 and vPV)
                c[(bool(nph), bool(npv))] += nu * nv
        return c
    cls = Counter()
    for Lh, Rh in ((hJ0, hR0), (hJH, hRV), (hJV, hRH)):
        cls.update(combine(Lh, Rh))
    both = cls[(True, True)]
    check(both == 0, "Xhat30 meet N(P^H_30L) meet N(P^V_30L): %d words (condition (33) holds)" % both)
    o, h, v = cls[(False, False)], cls[(True, False)], cls[(False, True)]
    check([o, h, v] == [1435184942161465, 420235140891852, 588656251987804], "Xhat30 classes relative to G30L: (o,h,v) = (%d, %d, %d) = the paper's (j0 decomposition, eq. 132)" % (o, h, v))
    cls2 = Counter()
    cls2.update(combine(hist(JVb, False), hist(XA["0"] + XA["H"] + XA["V"], False)))
    check(cls2[(True, True)] == 0 and [cls2[(False, False)], cls2[(True, False)], cls2[(False, True)]] == [1446768903083453, 420235140891852, 576488425905496],
          "ordinary auxiliary set of G30L (X15X x X15^{A,het}): axiom X meet N(PH) meet N(PV) empty, classes (o,h,v) = (%d, %d, %d) = eq. (129)" % (cls2[(False, False)], cls2[(True, False)], cls2[(False, True)]))
    print("RESULT box-level axioms %s" % ("verified: I15, I30++ independent; dimension-15 private pairs; condition (33) for Xhat30 at dimension 30 (zero words in both neighbourhoods); J30++ independent as an automorphic image of I30++" if not FAILS else "FAILED") + " time=%.0fs" % (time.time() - T0))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
