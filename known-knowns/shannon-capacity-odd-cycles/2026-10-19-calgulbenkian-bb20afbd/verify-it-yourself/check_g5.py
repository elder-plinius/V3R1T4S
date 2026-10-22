#!/usr/bin/env python3
"""Exhaustive check of every axiom of Definition 2 (Gao gadget) for the 367-word base gadget G5 in C_7^(box 5),
written from the definition in arXiv:2608.30273.  Standard library only.

Usage: python3 check_g5.py OBJECT_DIR      (reads OBJECT_DIR/base_g5.json)
Definition 2: a Gao gadget in G consists of an independent set I, t pairwise endpoint-disjoint private pairs (r_i, q_i)
(r_i in I, q_i not in I, N(q_i) meets I only in r_i), two independent sets P^H, P^V forming complementary transversals of
the pairs (one endpoint of each pair in each), and an independent auxiliary set X with X meet N(P^H) meet N(P^V) empty.
Profile (a, t, s, o, h, v) = (|I|, t, |X|, |X^0|, |X^H|, |X^V|), X^H = X meet N(P^H), X^V = X meet N(P^V), X^0 the rest.
"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c7_lib as L

FAILS = []


def check(c, msg):
    print(("  [ok]   " if c else "  [FAIL] ") + msg)
    if not c:
        FAILS.append(msg)


def main(objdir):
    I, X, pairs = L.load_base(os.path.join(objdir, "base_g5.json"))
    nbl = L.build_neighbours()
    check(all(0 <= w < L.N5 for w in I + X), "all words are valid codes of C_7^5")
    check(len(set(I)) == len(I) == 367, "I has 367 distinct words")
    check(len(set(X)) == len(X) == 367, "X has 367 distinct words")
    # (a) independence of I and of X: exhaustive over all pairs
    def indep(S):
        return not any(L.confusable(u, v) for u, v in itertools.combinations(S, 2))
    check(indep(I), "I is independent (all %d pairs)" % (367 * 366 // 2))
    check(indep(X), "X is independent (all %d pairs)" % (367 * 366 // 2))
    # (b) private pairs
    Iset = set(I)
    R = [r for r, q, s in pairs]
    Q = [q for r, q, s in pairs]
    check(len(pairs) == 8, "t = 8 private pairs")
    ok = True
    for r, q, s in pairs:
        ok &= r in Iset and q not in Iset
        nb = [w for w in I if L.confusable(q, w)]
        ok &= nb == [r]
    check(ok, "each pair (r, q): r in I, q not in I, and the only word of I confusable with q is r (exhaustive over I)")
    ends = R + Q
    check(len(set(ends)) == 16, "the 16 endpoints are pairwise distinct (endpoint-disjoint pairs)")
    # (c) transversals
    PH, PV = L.ph_pv(pairs)
    check(all((h == r and v == q) or (h == q and v == r) for (r, q, s), h, v in zip(pairs, PH, PV)),
          "P^H and P^V contain exactly one endpoint of each pair, and complementary ones")
    check(indep(PH) and indep(PV), "P^H and P^V are independent (all pairs)")
    # (d) auxiliary condition
    nPH = L.nflag(nbl, PH)
    nPV = L.nflag(nbl, PV)
    check(not any(nPH[x] and nPV[x] for x in X), "X meet N(P^H) meet N(P^V) is empty")
    XH = [x for x in X if nPH[x]]
    XV = [x for x in X if nPV[x]]
    X0 = [x for x in X if not nPH[x] and not nPV[x]]
    a, t, s, o, h, v = len(I), len(pairs), len(X), len(X0), len(XH), len(XV)
    print("  profile (a,t,s,o,h,v) = %s" % str((a, t, s, o, h, v)))
    check((a, t, s, o, h, v) == (367, 8, 367, 322, 26, 19), "profile equals (367, 8, 367, 322, 26, 19) of eq. (47)")
    check(o + h + v == s, "X = X^0 + X^H + X^V")
    print("RESULT G5 Definition 2 axioms all verified exhaustively; profile (367, 8, 367, 322, 26, 19)" if not FAILS else "FAIL")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
