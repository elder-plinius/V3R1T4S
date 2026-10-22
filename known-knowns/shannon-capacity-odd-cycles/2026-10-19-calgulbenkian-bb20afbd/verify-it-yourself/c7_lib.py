"""Shared helpers for the C7 base-gadget and certificate checks (standard library only).
Vertices of C_7^(box 5) are base-7 codes 0..16806; coordinate k of n is (n // 7**k) % 7.
Two vertices are confusable (equal or adjacent) iff in every coordinate the difference mod 7 is 0, 1 or 6."""
import json
from array import array

N5 = 16807
POW = [7 ** k for k in range(5)]


def dec(n):
    return tuple((n // POW[k]) % 7 for k in range(5))


def enc(w):
    return sum(c * POW[k] for k, c in enumerate(w))


def confusable(u, v):
    """u, v are base-7 codes."""
    for k in range(5):
        if ((u // POW[k]) - (v // POW[k])) % 7 not in (0, 1, 6):
            return False
    return True


def build_neighbours():
    """NBL[n] = array of the 243 closed neighbours of n."""
    nbl = []
    for n in range(N5):
        cur = [0]
        for k in range(5):
            d = (n // POW[k]) % 7
            opts = [((d + e) % 7) * POW[k] for e in (-1, 0, 1)]
            cur = [c + o for c in cur for o in opts]
        nbl.append(array('H', cur))
    return nbl


def nflag(nbl, S):
    """bytearray flag of the closed neighbourhood N(S) of a set S of codes."""
    f = bytearray(N5)
    for s in S:
        for x in nbl[s]:
            f[x] = 1
    return f


def T5(n):
    """Tandon's automorphism T(w0..w4) = (2-w1, w3, w0, 2-w2, w4) mod 7 (eq. 50)."""
    w = dec(n)
    return enc(((2 - w[1]) % 7, w[3], w[0], (2 - w[2]) % 7, w[4]))


def load_base(path):
    d = json.load(open(path))
    pairs = [(r, q, bool(s)) for r, q, s in d["pairs"]]
    return d["I"], d["X"], pairs


def ph_pv(pairs):
    PH = [r if s else q for r, q, s in pairs]
    PV = [q if s else r for r, q, s in pairs]
    return PH, PV


class SetN:
    """Closed neighbourhood membership for an explicit set of pairs: u=(a,b) in N(S) iff exists (s1,s2) in S with
    s1~a and s2~b.  Implemented as: for each a, the union over s1~a of the neighbourhood masks of the s2's."""

    def __init__(self, nbl, words):
        self.nbl = nbl
        nbm = self._nbm = {}

        def nbmask(b):
            m = nbm.get(b)
            if m is None:
                m = 0
                for x in nbl[b]:
                    m |= 1 << x
                nbm[b] = m
            return m
        by_first = {}
        for a, b in words:
            by_first[a] = by_first.get(a, 0) | nbmask(b)
        dil = [0] * N5
        for a in range(N5):
            m = 0
            for a2 in nbl[a]:
                v = by_first.get(a2)
                if v:
                    m |= v
            dil[a] = m
        self.dil = dil

    def __call__(self, a, b):
        return (self.dil[a] >> b) & 1 == 1


def independent10(nbl, words):
    """Exhaustive: no two distinct words of the list are confusable in every one of 10 coordinates."""
    words = list(words)
    if len(set(words)) != len(words):
        return False
    nbm = {}

    def nbmask(b):
        m = nbm.get(b)
        if m is None:
            m = 0
            for x in nbl[b]:
                m |= 1 << x
            nbm[b] = m
        return m
    by_first = {}
    for a, b in words:
        by_first[a] = by_first.get(a, 0) | (1 << b)
    for a, b in words:
        nb = nbmask(b)
        for a2 in nbl[a]:
            v = by_first.get(a2)
            if v:
                m = v & nb
                if a2 == a:
                    m &= ~(1 << b)
                if m:
                    return False
    return True
