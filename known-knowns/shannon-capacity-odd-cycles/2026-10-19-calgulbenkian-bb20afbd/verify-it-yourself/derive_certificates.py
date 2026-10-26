#!/usr/bin/env python3
"""Independent re-derivation of Tandon's finite certificates C1, C2, C3, C4 (arXiv:2608.30273, Table 4, Appendix B)
from their definitions and the 367-word base gadget G5.  Standard library only; does not use or import Tandon's code.

Usage: python3 derive_certificates.py OBJECT_DIR [--brute]      (--brute adds a word-by-word enumeration of C2)

Setting.  G5 = (I5, X5, private pairs, P^H, P^V) as in object/base_g5.json.  Words of C_7^10 are pairs of codes.
All objects below are explicit sets assembled with Gao's product lemma (Lemma 1) and Tandon's Theorem 1:
  G10  = Gao(G5, G5):   I10 = (B5 x B5) u {(p,x): x in X5, p in L(x)} u {(y,q): y in X5, q in K(y)},
        L(x) = R5, P5^H, P5^V for x in X5^0, X5^H, X5^V;  K(y) = R5, P5^V, P5^H for y in X5^0, X5^H, X5^V;
        pairs centres R10 = (R5 x X5^0) u (X5^0 x R5); transversals P10^H = (P5^H x X5^0) u (X5^0 x P5^V),
        P10^V = (P5^V x X5^0) u (X5^0 x P5^H); auxiliary set X10 = X5 x X5.
  J+   = (T x T)(I10) with the eight exchanges of eq. (152);  C1 = |J+ minus N(X10^0)|.
  G15  = Gao(G10, G5) with main code I15 (same Lemma 1 formulas);  J15 = (T x T x T)(I15);
        X15X = X10 x X5 (ordinary auxiliary set), X15 = (X10 x X5^0) u (J+ x X5^H) u (J+ x X5^V) (eq. 156);
        C2 = |J15 minus N(X15^{0,X})|, C3 = |X15 minus N(X15^{0,X})|, X15^{0,X} the neutral part of X15X.
  G30++ = Gao(G15het, G15het)[X15; X15] with main code I30++ (Lemma 1), J30++ = T^6(I30++),
        C4 = |J30++ minus N(X30^{0,L})|, X30^{0,L} the neutral part of the auxiliary set of G30L = Gao(G15AX, sigma(G15Ah)).
The neutral part of an auxiliary set is what is confusable with neither propagated transversal; it is computed here from the
transversals (not from a formula), word class by word class.  N(A x B) = N(A) x N(B) and N(union) = union of N are the only
facts used to count neighbourhood membership.  Counting for the large sets uses flag histograms over explicit factors:
a word of a product component A x B is in N(U) iff for some product component (A', B') of U its A-part is in N(A') and its
B-part is in N(B').  The 10-dimensional neighbourhoods are computed exhaustively from explicit word lists.
"""
import os, sys, json, itertools, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c7_lib as L

FAILS = []
t0 = time.time()


def check(c, msg):
    print(("  [ok]   " if c else "  [FAIL] ") + msg)
    sys.stdout.flush()
    if not c:
        FAILS.append(msg)


def main(objdir, brute):
    I5, X5, pairs = L.load_base(os.path.join(objdir, "base_g5.json"))
    cin = json.load(open(os.path.join(objdir, "cert_input.json")))
    PV_ = cin["paper_values"]
    nbl = L.build_neighbours()
    T5 = [L.T5(n) for n in range(L.N5)]
    check(sorted(T5) == list(range(L.N5)), "T is a bijection of the 16807 words")
    check(all(L.confusable(T5[n], T5[m]) for n in range(L.N5) for m in nbl[n]),
          "T maps confusable pairs to confusable pairs (all 16807 x 243 pairs); T is a bijection, so it is an automorphism of C_7^5")
    R5 = [r for r, q, s in pairs]
    PH5, PV5 = L.ph_pv(pairs)
    Iset = set(I5)
    B5 = [w for w in I5 if w not in set(R5)]
    nPH, nPV = L.nflag(nbl, PH5), L.nflag(nbl, PV5)
    XH5 = [x for x in X5 if nPH[x]]
    XV5 = [x for x in X5 if nPV[x]]
    X05 = [x for x in X5 if not nPH[x] and not nPV[x]]
    check(not (set(XH5) & set(XV5)) and len(XH5) + len(XV5) + len(X05) == 367, "X5 = X5^0 + X5^H + X5^V (%d, %d, %d)" % (len(X05), len(XH5), len(XV5)))
    nX0 = L.nflag(nbl, X05)
    nXH = L.nflag(nbl, XH5)
    nXV = L.nflag(nbl, XV5)

    # ---------------- 10-dimensional objects ----------------
    X10 = [(x, y) for x in X5 for y in X5]

    def nPH10(a, b, o="std"):          # u in N(P10^H);  std: (PH x X0) u (X0 x PV);  A: (PV x X0) u (X0 x PV)
        if o == "std":
            return (nPH[a] and nX0[b]) or (nX0[a] and nPV[b])
        return (nPV[a] and nX0[b]) or (nX0[a] and nPV[b])

    def nPV10(a, b, o="std"):          # std: (PV x X0) u (X0 x PH);  A: (PH x X0) u (X0 x PH)
        if o == "std":
            return (nPV[a] and nX0[b]) or (nX0[a] and nPH[b])
        return (nPH[a] and nX0[b]) or (nX0[a] and nPH[b])

    X10_0 = [u for u in X10 if not nPH10(*u) and not nPV10(*u)]
    X10_H = [u for u in X10 if nPH10(*u) and not nPV10(*u)]
    X10_V = [u for u in X10 if nPV10(*u) and not nPH10(*u)]
    check(len(X10_0) + len(X10_H) + len(X10_V) == len(X10), "X10 = X10^0 + X10^H + X10^V")
    check([len(X10), len(X10_0), len(X10_H), len(X10_V)] == PV_["table6a_sizes"]["X10"], "X10 sizes (s,o,h,v) = %s (Table 6(a))" % str([len(X10), len(X10_0), len(X10_H), len(X10_V)]))
    X10A_0 = [u for u in X10 if not nPH10(*u, o="A") and not nPV10(*u, o="A")]
    check(X10A_0 == X10_0, "neutral part of X10 is the same for the orientation A (G10A = Gao(sigma G5, G5)) as for G10")

    # main code I10 of G10 (Lemma 1) and the pair centres R10
    def Lset(x): return R5 if x in X05s else (PH5 if x in XH5s else PV5)
    def Kset(y): return R5 if y in X05s else (PV5 if y in XH5s else PH5)
    X05s, XH5s, XV5s = set(X05), set(XH5), set(XV5)
    R10 = [(r, x) for r in R5 for x in X05] + [(y, r) for y in X05 for r in R5]
    I10 = [(a, b) for a in B5 for b in B5] + [(p, x) for x in X5 for p in Lset(x)] + [(y, q) for y in X5 for q in Kset(y)]
    I10s = set(I10)
    check(len(I10) == len(I10s) == 134753 and set(R10) <= I10s, "|I10| = 134753 and the 5152 pair centres lie in I10")
    t_ = time.time()
    check(L.independent10(nbl, I10), "I10 is independent (exhaustive)  [%.0fs]" % (time.time() - t_))
    B10 = [w for w in I10 if w not in set(R10)]
    PH10 = [(p, x) for p in PH5 for x in X05] + [(x, p) for x in X05 for p in PV5]
    PV10 = [(p, x) for p in PV5 for x in X05] + [(x, p) for x in X05 for p in PH5]

    # J+ = (T x T)(I10) after the eight exchanges
    J = {(T5[a], T5[b]) for a, b in I10}
    check(len(J) == 134753 and L.independent10(nbl, list(J)), "(T x T)(I10) is an independent set of 134753 words (T is an automorphism)")
    N_X10_0 = L.SetN(nbl, X10_0)
    before = sum(1 for a, b in J if not N_X10_0(a, b))
    check(before == PV_["C1_before_exchanges"], "|(T x T)(I10) minus N(X10^0)| = %d before the exchanges (eq. 151: 27480)" % before)
    ex = [(tuple(r), tuple(i)) for r, i in cin["exchanges"]]
    for rem, ins in ex:
        assert rem in J and ins not in J
    Jp = (J - {r for r, i in ex}) | {i for r, i in ex}
    check(len(Jp) == 134753 and L.independent10(nbl, list(Jp)), "J+ (after eight exchanges) has 134753 words and is independent (exhaustive)")
    Jpl = sorted(Jp)
    C1 = sum(1 for a, b in Jpl if not N_X10_0(a, b))
    check(C1 == PV_["C1"], "C1 = |J+ minus N(X10^0)| = %d (Table 4: 27,488)" % C1)

    # ---------------- groups ----------------
    class G10:
        def __init__(self, name, words, nfun=None):
            self.name, self.words = name, words
            self.nfun = nfun
    def mkN(words): return L.SetN(nbl, words)

    # signature of a (untransformed) 10-dim word for class decisions
    def usig(a, b):
        return (nPH10(a, b), nPV10(a, b), nPH10(a, b, "A"), nPV10(a, b, "A"), N_X10_0(a, b))

    def group_by(words, keyf):
        d = {}
        for w in words:
            d.setdefault(keyf(w), []).append(w)
        return d

    # X10 groups by full signature; J+ groups by membership in N(X10^0) only (that is all that matters next to X5^H, X5^V)
    X10g = {k: G10("X10" + str(k), v) for k, v in group_by(X10, lambda w: usig(*w)).items()}
    Jg = {k: G10("J+" + str(k), v) for k, v in group_by(Jpl, lambda w: N_X10_0(*w)).items()}
    print("  X10 groups by signature: %s" % {k: len(g.words) for k, g in X10g.items()})
    print("  J+ groups by 'in N(X10^0)': %s" % {k: len(g.words) for k, g in Jg.items()})
    for g in list(X10g.values()) + list(Jg.values()):
        g.N = mkN(g.words)
    # 5-dim groups
    class G5:
        def __init__(self, name, words, cls=None):
            self.name, self.words, self.cls = name, words, cls
            self.nflag = L.nflag(nbl, words)
    g_X0, g_XH, g_XV = G5("X5^0", X05, "0"), G5("X5^H", XH5, "H"), G5("X5^V", XV5, "V")
    g_R, g_PH, g_PV, g_B = G5("R5", R5), G5("PH5", PH5), G5("PV5", PV5), G5("B5", B5)

    # class of a 15-dimensional word (u, v) with u in C7^10 given by its signature, v in X5 given by its class, w.r.t. the
    # transversals of Gao(G10, G5) (orientation std) or of Gao(G10A, G5) (orientation A)
    def get(sig, i):
        assert sig[i] is not None
        return sig[i]

    def cls15(sig, vclass, o):
        ih, iv = (0, 1) if o == "std" else (2, 3)
        # v in X5: v in N(X5^0) iff class 0; v in N(PH5) iff class H; v in N(PV5) iff class V
        vX0, vPH, vPV = vclass == "0", vclass == "H", vclass == "V"
        n_ph = (vX0 and get(sig, ih)) or (vPV and (sig[4] if sig[4] is not None else None))
        n_pv = (vX0 and get(sig, iv)) or (vPH and sig[4])
        assert not (n_ph and n_pv)
        return "H" if n_ph else ("V" if n_pv else "0")

    def aux_components(o, spec):
        """spec: list of (u groups dict, v group): all u groups of the dict paired with the v group.  Returns class -> list of
        (u group, v group) product components."""
        out = {"0": [], "H": [], "V": []}
        for ug, vg in spec:
            for g in ug.values():
                # J+ groups only carry the N(X10^0) flag, so sig has None entries: build a partial signature
                sig = g.sig if hasattr(g, "sig") else None
                out[cls15(sig, vg.cls, o)].append((g, vg))
        return out
    # attach signatures
    for k, g in X10g.items(): g.sig = k
    for k, g in Jg.items(): g.sig = (None, None, None, None, k)

    def size(comps): return sum(len(g.words) * len(h.words) for g, h in comps)

    # aux sets
    spec_X = [(X10g, g_X0), (X10g, g_XH), (X10g, g_XV)]                       # X10 x X5 (ordinary)
    spec_het = [(X10g, g_X0), (Jg, g_XH), (Jg, g_XV)]                        # eq. (156)
    spec_Ahet = [(X10g, g_X0), (Jg, g_XH), (X10g, g_XV)]                     # G15Ah: (X10, J+, X10)
    XX_std, XX_A = aux_components("std", spec_X), aux_components("A", spec_X)
    check({(id(g), id(h)) for g, h in XX_std["0"]} == {(id(g), id(h)) for g, h in XX_A["0"]}, "neutral part of the ordinary X10 x X5 is the same for transversals of G15X and of G15AX")
    U0, U1 = XX_A["0"], XX_A["H"] + XX_A["V"]
    check(size(U0) == PV_["table6a_sizes"]["X15X_neutral"], "|X15^{0,X}| = %d (Table 6: 35342398)" % size(U0))
    Xhet = aux_components("std", spec_het)
    check([size(Xhet["0"]) + size(Xhet["H"]) + size(Xhet["V"]), size(Xhet["0"]), size(Xhet["H"]), size(Xhet["V"])] == PV_["table6a_sizes"]["X15het"],
          "X15 (eq. 156) class sizes (s,o,h,v) = %s (Table 6(a): 49433743, 35275258, 6703815, 7454670)" % str([size(Xhet["0"]) + size(Xhet["H"]) + size(Xhet["V"]), size(Xhet["0"]), size(Xhet["H"]), size(Xhet["V"])]))
    XA = aux_components("A", spec_Ahet)
    V0, V1 = XA["0"], XA["H"] + XA["V"]
    check(size(V0) == PV_["table6a_sizes"]["X15Ahet_neutral"], "|neutral part of X15^{A,het}| = %d (Table 6: 35303606)" % size(V0))

    # ---------------- histogram counting ----------------
    def refs_args(refs):
        ag, bg = [], []
        for r in refs:
            for g, h in r:
                if g not in ag: ag.append(g)
                if h not in bg: bg.append(h)
        return ag, bg

    def hist(comps10_5, refs, tr):
        """comps10_5: list of (list of 10-dim words, list of 5-dim words).  Returns Counter of tuples (in N(ref) for ref in refs)
        over all words (u, v) of the union of the products, after applying T on every 5-block when tr."""
        ag, bg = refs_args(refs)
        total = Counter()
        for A, B in comps10_5:
            hu = Counter()
            for a, b in A:
                if tr: a, b = T5[a], T5[b]
                hu[tuple(g.N(a, b) for g in ag)] += 1
            hv = Counter()
            for v in B:
                if tr: v = T5[v]
                hv[tuple(bool(h.nflag[v]) for h in bg)] += 1
            for ku, cu in hu.items():
                for kv, cv in hv.items():
                    flags = tuple(any(ku[ag.index(g)] and kv[bg.index(h)] for g, h in r) for r in refs)
                    total[flags] += cu * cv
        return total

    X10_0l, X10_Hl, X10_Vl = X10_0, X10_H, X10_V
    # I15 = main code of Gao(G10, G5)
    I15 = [(B10, B5), (R10, X05), (PH10, XH5), (PV10, XV5), (X10_0l, R5), (X10_Hl, PV5), (X10_Vl, PH5)]
    check(sum(len(A) * len(B) for A, B in I15) == 49495055, "|I15| = (a10-t10)(a5-t5) + t10 s5 + s10 t5 = 49495055")
    h = hist(I15, [U0], True)
    C2 = sum(c for f, c in h.items() if not f[0])
    check(C2 == PV_["C2"], "C2 = |J15 minus N(X15^{0,X})| = %d (Table 4: 12,839,823)  [%.0fs]" % (C2, time.time() - t0))
    # C3
    h = hist([(X10, X05), (Jpl, XH5), (Jpl, XV5)], [U0], False)
    C3 = sum(c for f, c in h.items() if not f[0])
    check(C3 == PV_["C3"], "C3 = |X15 minus N(X15^{0,X})| = %d (Table 4: 14,045,805)" % C3)

    # ---------------- C4 ----------------
    def lists(comps):
        # a class given as components of groups -> components of explicit lists, one per group pair
        return [(g.words, h.words) for g, h in comps]
    X15c = {k: lists(v) for k, v in Xhet.items()}
    R15 = [(R10, X05), (X10_0l, R5)]
    PH15 = [(PH10, X05), (X10_0l, PV5)]
    PV15 = [(PV10, X05), (X10_0l, PH5)]
    B15 = [(B10, B5), (PH10, XH5), (PV10, XV5), (X10_Hl, PV5), (X10_Vl, PH5)]
    check(sum(len(A) * len(B) for A, B in B15) + sum(len(A) * len(B) for A, B in R15) == 49495055, "I15 = B15 + R15")
    check(sum(len(A) * len(B) for A, B in R15) == 2504616 and sum(len(A) * len(B) for A, B in PH15) == 2504616, "t15 = 2504616")
    refs = [U0, U1, V0, V1]
    sets = {"B15": B15, "R15": R15, "X0": X15c["0"], "XH": X15c["H"], "XV": X15c["V"], "PH15": PH15, "PV15": PV15}
    H = {k: hist(v, refs, True) for k, v in sets.items()}
    print("  flag histograms done  [%.0fs]" % (time.time() - t0))
    HL = {k: Counter() for k in H}
    HR = {k: Counter() for k in H}
    for k, hh in H.items():
        for f, c in hh.items():
            HL[k][(f[0], f[1])] += c
            HR[k][(f[2], f[3])] += c

    def outside(Sa, Sb):
        """number of pairs (u, v) in Sa x Sb with (u,v) not in N(X30^{0,L}) = N(U0) x N(V0) u N(U1) x N(V1)."""
        tot = 0
        for (u0, u1), cu in HL[Sa].items():
            for (v0, v1), cv in HR[Sb].items():
                if not ((u0 and v0) or (u1 and v1)):
                    tot += cu * cv
        return tot

    def card(S): return sum(HL[S].values())
    comps = [("B15xB15", "B15", "B15"), ("R15xX15^0", "R15", "X0"), ("P15^HxX15^H", "PH15", "XH"), ("P15^VxX15^V", "PV15", "XV"),
             ("X15^0xR15", "X0", "R15"), ("X15^HxP15^V", "XH", "PV15"), ("X15^VxP15^H", "XV", "PH15")]
    tot_size = tot_contrib = 0
    for name, a, b in comps:
        sz, ct = card(a) * card(b), outside(a, b)
        tot_size += sz; tot_contrib += ct
        check([sz, ct] == PV_["table5"][name], "component %-12s size %d contribution %d (Table 5)" % (name, sz, ct))
    check(tot_size == PV_["I30pp"], "|I30++| = %d (eq. 137)" % tot_size)
    u0n = sum(len(g.words) * len(h.words) for g, h in U0); u1n = sum(len(g.words) * len(h.words) for g, h in U1)
    v0n = sum(len(g.words) * len(h.words) for g, h in V0); v1n = sum(len(g.words) * len(h.words) for g, h in V1)
    check(u0n * v0n + u1n * v1n == PV_["X30_0L"], "|X30^{0,L}| = |U0||V0| + |U1||V1| = %d (Table 6: 1446768903083453)" % (u0n * v0n + u1n * v1n))
    C4 = tot_contrib
    check(C4 == PV_["C4"], "C4 = |J30++ minus N(X30^{0,L})| = %d (Table 4: 841,760,069,965,664)  [%.0fs]" % (C4, time.time() - t0))

    if brute:
        print("-- word-by-word enumeration of J15 (49495055 words) for C2")
        ag = [g for g, h in U0]
        bg_ = [h for g, h in U0]
        # precompute per-5-block flags; a word is in N(U0) iff some component (g,h) of U0 has u in N(g) and v in N(h)
        cnt = 0
        total = 0
        for A, B in I15:
            tv = [[bool(h.nflag[T5[v]]) for h in bg_] for v in B]
            for a, b in A:
                ua, ub = T5[a], T5[b]
                uf = [g.N(ua, ub) for g in ag]
                active = [i for i, f in enumerate(uf) if f]
                for flags in tv:
                    total += 1
                    for i in active:
                        if flags[i]:
                            break
                    else:
                        cnt += 1
        check(total == 49495055 and cnt == C2, "brute-force enumeration of all %d words of J15 gives C2 = %d (agrees with the histogram method)  [%.0fs]" % (total, cnt, time.time() - t0))
    print("%s C1=%d C2=%d C3=%d C4=%d time=%.0fs" % ("RESULT certificates re-derived:" if not FAILS else "FAIL", C1, C2, C3, C4, time.time() - t0))
    return 1 if FAILS else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(main(args[0], "--brute" in sys.argv))
