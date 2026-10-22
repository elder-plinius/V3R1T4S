#!/usr/bin/env python3
"""Explicit-set test of Lemma 1 (Gao's product), Theorem 1 (heterogeneous refinement), sigma, the map Phi and the BPZ rule S3b
and terminal code K4a, in the configuration of the claimed object, at small scale.  Standard library only.

Usage: python3 set_level_test.py OBJECT_DIR

The configuration mirrors the object: a left gadget L with heterogeneous codebooks (J0, JH, JV) is combined, by Theorem 1, with
three different right gadgets R0, R1, R2 (R1 itself a Theorem-1 output, as R30 is in the object); the three results are
oriented as P0, sigma(P1), sigma(P2), converted by Phi to seven-family representations of real vertex sets, combined by the rule
S3b of object/rules.json, and every output family is checked to be independent, every separated pair of output families is
checked to be separated, and sizes are compared with the cardinality formulas.  K4a is checked on four copies of the base
representation.  Two such configurations are run: (A) a one-dimensional left gadget, (B) a two-dimensional left gadget
built the way the object builds G30L with its codebook taken from the sibling gadget over the same ordered pair of inputs.
Every vertex set is an explicit set of words of C_7^n with n at most 9 (configuration A: n = 2, 3, 2 and 7 for the combined families).  The statement tested for each gadget is Definition 2 of
the paper, verified by brute force on the vertex sets (not by the formulas); the formulas of eqs (21), (38), (39) are then
compared with the sizes of the sets.
"""
import os, sys, json, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FAILS = []


def check(c, msg):
    print(("  [ok]   " if c else "  [FAIL] ") + msg)
    sys.stdout.flush()
    if not c:
        FAILS.append(msg)


def conf(u, v):
    return all((a - b) % 7 in (0, 1, 6) for a, b in zip(u, v))


def space(n):
    return list(itertools.product(range(7), repeat=n))


def closed_nbhd(S, n, SP):
    S = list(S)
    return {w for w in SP if any(conf(w, s) for s in S)}


def independent(S):
    S = list(S)
    if len(set(S)) != len(S):
        return False
    return not conflicts(S, S, same=True)


def conflicts(A, B, same=False):
    """True if some a in A is confusable with some b in B (a != b when same)."""
    n = len(next(iter(A))) if A else 0
    k = min(5, n)
    buckets = {}
    for b in B:
        buckets.setdefault(tuple(b[:k]), []).append(b)
    offs = list(itertools.product((-1, 0, 1), repeat=k))
    for a in A:
        for o in offs:
            key = tuple((a[i] + o[i]) % 7 for i in range(k))
            for b in buckets.get(key, ()):
                if conf(a, b) and not (same and a == b):
                    return True
    return False


class Gad:
    def __init__(self, n, I, pairs, PH, PV, X):
        self.n, self.I, self.pairs, self.PH, self.PV, self.X = n, set(I), list(pairs), set(PH), set(PV), set(X)
        self.SP = space(n)
        self.nPH = closed_nbhd(self.PH, n, self.SP)
        self.nPV = closed_nbhd(self.PV, n, self.SP)
        self.XH = {x for x in self.X if x in self.nPH}
        self.XV = {x for x in self.X if x in self.nPV}
        self.X0 = self.X - self.XH - self.XV
        self.R = {r for r, q in self.pairs}
        self.B = self.I - self.R

    def verify(self, name):
        """Definition 2, by brute force on the sets."""
        ok = independent(self.I) and independent(self.X) and independent(self.PH) and independent(self.PV)
        for r, q in self.pairs:
            ok &= r in self.I and q not in self.I and [w for w in self.I if conf(q, w)] == [r]
        ends = [e for p in self.pairs for e in p]
        ok &= len(set(ends)) == len(ends)
        for r, q in self.pairs:
            ok &= (r in self.PH and q in self.PV) or (q in self.PH and r in self.PV)
        ok &= len(self.PH) == len(self.PV) == len(self.pairs)
        ok &= not (self.XH & self.XV) and not any(x in self.nPH and x in self.nPV for x in self.X)
        check(ok, "%s: Definition 2 holds on the explicit sets (dim %d, profile %s)" % (name, self.n, str(self.profile())))
        return ok

    def profile(self):
        return (len(self.I), len(self.pairs), len(self.X), len(self.X0), len(self.XH), len(self.XV))


def sigma(G):
    return Gad(G.n, G.I, G.pairs, G.PV, G.PH, G.X)


def gao_sets(G1, G2, J=None):
    """Lemma 1 (J None) or Theorem 1 (J = (J0, JH, JV), independent subsets of the left graph)."""
    L1 = lambda x: G1.R if x in G2.X0 else (G1.PH if x in G2.XH else G1.PV)
    K2 = lambda y: G2.R if y in G1.X0 else (G2.PV if y in G1.XH else G2.PH)
    I = {a + b for a in G1.B for b in G2.B} | {p + x for x in G2.X for p in L1(x)} | {y + q for y in G1.X for q in K2(y)}
    pairs = [(r + x, q + x) for (r, q) in G1.pairs for x in G2.X0] + [(y + r, y + q) for y in G1.X0 for (r, q) in G2.pairs]
    PH = {p + x for p in G1.PH for x in G2.X0} | {x + p for x in G1.X0 for p in G2.PV}
    PV = {p + x for p in G1.PV for x in G2.X0} | {x + p for x in G1.X0 for p in G2.PH}
    if J is None:
        X = {x + y for x in G1.X for y in G2.X}
    else:
        J0, JH, JV = J
        X = {u + x for u in J0 for x in G2.X0} | {u + x for u in JH for x in G2.XH} | {u + x for u in JV for x in G2.XV}
    return Gad(G1.n + G2.n, I, pairs, PH, PV, X)


def formula_gao(p1, p2):
    a1, t1, s1, o1, h1, v1 = p1
    a2, t2, s2, o2, h2, v2 = p2
    return ((a1 - t1) * (a2 - t2) + t1 * s2 + s1 * t2, t1 * o2 + o1 * t2, s1 * s2, o1 * o2 + (h1 + v1) * (h2 + v2), h1 * o2 + o1 * v2, v1 * o2 + o1 * h2)


def formula_het(GL, GR, J):
    """eqs (38), (39) with the counts taken from the explicit sets J = (J0, JH, JV)."""
    J0, JH, JV = J
    aL, tL, sL, oL, hL, vL = GL.profile()
    aR, tR, sR, oR, hR, vR = GR.profile()
    nX0 = closed_nbhd(GL.X0, GL.n, GL.SP)
    j0 = len(J0)
    o0 = len([u for u in J0 if u not in GL.nPH and u not in GL.nPV])
    h0 = len([u for u in J0 if u in GL.nPH])
    v0 = len([u for u in J0 if u in GL.nPV])
    jH, jV = len(JH), len(JV)
    qH = len([u for u in JH if u not in nX0])
    qV = len([u for u in JV if u not in nX0])
    return ((aL - tL) * (aR - tR) + tL * sR + sL * tR, tL * oR + oL * tR, j0 * oR + jH * hR + jV * vR,
            o0 * oR + qH * hR + qV * vR, h0 * oR + (jV - qV) * vR, v0 * oR + (jH - qH) * hR)


def theorem1(name, GL, GR, J):
    J0, JH, JV = J
    check(independent(J0) and independent(JH) and independent(JV), "%s: J0, JH, JV independent in the left graph" % name)
    check(not any(u in GL.nPH and u in GL.nPV for u in J0), "%s: J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)" % name)
    base = gao_sets(GL, GR)
    out = gao_sets(GL, GR, J)
    check(out.I == base.I and out.pairs == base.pairs and out.PH == base.PH and out.PV == base.PV,
          "%s: code, pairs and transversals are those of the ordinary product" % name)
    check(out.profile() == formula_het(GL, GR, J), "%s: profile of the explicit sets equals eqs (38),(39): %s" % (name, str(out.profile())))
    out.verify(name + " (Theorem 1 output)")
    return out


def lemma1(name, G1, G2):
    out = gao_sets(G1, G2)
    check(out.profile() == formula_gao(G1.profile(), G2.profile()), "%s: profile of the explicit sets equals eq. (21): %s" % (name, str(out.profile())))
    out.verify(name + " (Lemma 1 output)")
    return out


def rot(G, c):
    """image of a 1-dimensional gadget under x -> x + c (an automorphism of C_7)"""
    f = lambda w: tuple((x + c) % 7 for x in w)
    return Gad(G.n, {f(w) for w in G.I}, [(f(r), f(q)) for r, q in G.pairs], {f(w) for w in G.PH}, {f(w) for w in G.PV}, {f(w) for w in G.X})


def flip(G):
    """image under x -> -x (reflection of C_7)"""
    f = lambda w: tuple((-x) % 7 for x in w)
    return Gad(G.n, {f(w) for w in G.I}, [(f(r), f(q)) for r, q in G.pairs], {f(w) for w in G.PH}, {f(w) for w in G.PV}, {f(w) for w in G.X})


def phi_families(G):
    """Table 2: F_B = B, F_N = X^0, F_A = X^V, F_D = X^H, F_O = R, F_H = P^H, F_V = P^V"""
    return {"B": G.B, "N": G.X0, "A": G.XV, "D": G.XH, "O": G.R, "H": G.PH, "V": G.PV}


def apply_rule_sets(rules, name, fams, sep):
    tab = rules["tables"][name]["words"]
    out = {}
    for l in "BNADOHV":
        S = set()
        for w in tab[l]:
            parts = [fams[i][c] for i, c in enumerate(w)]
            if any(not p for p in parts):
                continue
            for combo in itertools.product(*parts):
                S.add(tuple(x for piece in combo for x in piece))
        out[l] = S
    return out


def main(objdir):
    rules = json.load(open(os.path.join(objdir, "rules.json")))
    sep = {(a, b) for a, b in rules["sep"]}
    # base one-dimensional gadget: I = {0,2,4}, pair (0,6), P^H = {0}, P^V = {6}, X = {1,3,5}; profile (3,1,3,1,1,1) of Example 1
    g = Gad(1, {(0,), (2,), (4,)}, [((0,), (6,))], {(0,)}, {(6,)}, {(1,), (3,), (5,)})
    check(g.verify("g"), "base gadget g")
    check(g.profile() == (3, 1, 3, 1, 1, 1), "g has the profile (3,1,3,1,1,1) of the paper's Example 1")
    g2, g3, gm = rot(g, 1), rot(g, 3), flip(g)
    for nm, x in (("g+1", g2), ("g+3", g3), ("-g", gm)):
        x.verify(nm)

    def run_branches(tag, L, J, R0, R1, R2):
        P0 = theorem1(tag + " P0 = HetGao(L,R0)", L, R0, J)
        H1 = theorem1(tag + " HetGao(L,R1)", L, R1, J)
        P1 = sigma(H1)
        H2 = theorem1(tag + " HetGao(L,R2)", L, R2, J)
        P2 = sigma(H2)
        for nm, P in (("P1 = sigma(HetGao(L,R1))", P1), ("P2 = sigma(HetGao(L,R2))", P2)):
            P.verify(tag + " " + nm)
        fams = [phi_families(P) for P in (P0, P1, P2)]
        dims = [P0.n, P1.n, P2.n]
        # Definition 5 for each input representation
        for i, f in enumerate(fams):
            ok = all(independent(f[l]) for l in f if f[l]) and all(not conflicts(f[a], f[b]) for (a, b) in sep if f[a] and f[b])
            check(ok, "%s: Phi(P%d) is a seven-family representation (7 independent sets, all separated pairs separated), dim %d" % (tag, i, dims[i]))
        out = apply_rule_sets(rules, "S3b", fams, sep)
        n = sum(dims)
        formula = {l: 0 for l in "BNADOHV"}
        for l in "BNADOHV":
            for w in rules["tables"]["S3b"]["words"][l]:
                p = 1
                for i, c in enumerate(w):
                    p *= len(fams[i][c])
                formula[l] += p
        check(all(len(out[l]) == formula[l] for l in out), "%s: S3b output sizes equal the polynomial map %s (dim %d)" % (tag, str([len(out[l]) for l in "BNADOHV"]), n))
        okf = all(independent(out[l]) for l in out if out[l])
        check(okf, "%s: every S3b output family is an independent set in C_7^%d" % (tag, n))
        oks = all(not conflicts(out[a], out[b]) for (a, b) in sep if out[a] and out[b])
        check(oks, "%s: every separated pair of S3b output families is separated (no word of one confusable with a word of the other)" % tag)
        return out

    print("-- Lemma 1 on gadgets of dimensions 1 and 2")
    G2d = lemma1("Gao(g,g+1)", g, g2)
    G2e = lemma1("Gao(-g,g+3)", gm, g3)
    print("-- configuration A: one-dimensional left gadget L = g, heterogeneous codebooks (J0, JH, JV)")
    J0 = {(1,), (3,)}
    JH = {(0,), (2,), (5,)}
    JV = {(1,), (3,), (5,)}
    # right gadgets: a base gadget, a Theorem-1 output (dimension 2, oriented), a reversed base gadget
    Jr = ({(1,), (5,)}, {(0,), (2,)}, {(1,), (3,), (5,)})
    R1 = sigma(theorem1("inner HetGao(g+1,g+3) (right gadget R1)", g2, g3, ({(2,), (4,)}, {(1,), (3,), (5,)}, {(0,), (4,)})))
    outA = run_branches("A:", g, (J0, JH, JV), g3, R1, sigma(gm))
    print("-- configuration B: two-dimensional left gadget L = Gao(g, sigma(g+1)) with J0 from the sibling gadget over the same ordered pair")
    Lb = lemma1("L = Gao(g, sigma(g+1))", g, sigma(g2))
    sib = theorem1("sibling Gh = HetGao(g, sigma(g+1))", g, sigma(g2), ({(1,), (3,), (5,)}, {(0,), (2,), (4,)}, {(1,), (3,), (5,)}))
    check(sib.I == Lb.I and sib.PH == Lb.PH and sib.PV == Lb.PV, "sibling and L have the same code, pairs and transversals, so the sibling's auxiliary set is admissible as J0 for L")
    Jmain = {tuple((-x) % 7 for x in w) for w in Lb.I}
    check(independent(Jmain), "JH = JV = image of the main code of L under x -> -x (independent)")
    outB = run_branches("B:", Lb, (sib.X, Jmain, Jmain), g3, sigma(g2), sigma(gm))
    print("-- terminal code K4a on four copies of the base representation (real sets)")
    f = phi_families(g)
    code = rules["codes"]["K4a"]["words"]
    words = set()
    for w in code:
        parts = [f[c] for c in w]
        if any(not p for p in parts):
            continue
        for combo in itertools.product(*parts):
            words.add(tuple(x for piece in combo for x in piece))
    formula = 0
    for w in code:
        p = 1
        for c in w: p *= len(f[c])
        formula += p
    check(len(words) == formula, "K4a on 4 copies of Phi(g): %d words in C_7^4 = formula" % len(words))
    check(independent(words), "K4a output is an independent set in C_7^4 (exhaustive)")
    print("RESULT set-level test %s" % ("passed: Lemma 1, Theorem 1, sigma, Phi, S3b, K4a on explicit sets" if not FAILS else "FAILED"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
