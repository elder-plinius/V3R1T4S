#!/usr/bin/env python3
"""
Independent Zero-Shared-Code Brute-Force Proper Bond-Animal Enumerator on Z^k:
Directly grows fixed connected bond subsets on Z^k up to translation, computes
exact subspace perimeter t and vertex count v from the definition in Mertens & Moore
(arXiv:1805.02701, Section 2), and checks Theorem 7 ([binom(d, e-3)] D_e(q)).
"""

from collections import Counter


def enumerate_proper_animals_ztv(k: int, e: int):
    """Return Counter of (t_subspace, v_vertices) -> G_{e, t, v}^{(k)} from definition."""
    origin = tuple([0] * k)

    def canon(bonds):
        pts = set()
        for u, ax in bonds:
            pts.add(u)
            w = list(u)
            w[ax] += 1
            pts.add(tuple(w))
        mins = [min(p[c] for p in pts) for c in range(k)]
        return tuple(sorted((tuple(u[c] - mins[c] for c in range(k)), ax) for u, ax in bonds))

    cur = {canon([(origin, ax)]) for ax in range(k)}
    for _ in range(1, e):
        nxt = set()
        for anim in cur:
            bset = set(anim)
            pts = set()
            for u, ax in anim:
                pts.add(u)
                w = list(u)
                w[ax] += 1
                pts.add(tuple(w))
            for p in pts:
                for ax in range(k):
                    b_pos = (p, ax)
                    if b_pos not in bset:
                        nxt.add(canon(list(anim) + [b_pos]))
                    pm = list(p)
                    pm[ax] -= 1
                    b_neg = (tuple(pm), ax)
                    if b_neg not in bset:
                        nxt.add(canon(list(anim) + [b_neg]))
        cur = nxt

    counts = Counter()
    for anim in cur:
        if len({ax for _, ax in anim}) < k:
            continue
        bset = set(anim)
        pts = set()
        for u, ax in anim:
            pts.add(u)
            w = list(u)
            w[ax] += 1
            pts.add(tuple(w))
        # Definition of perimeter t: grid edges in Z^k incident to pts but NOT in bset
        perim_edges = set()
        for p in pts:
            for ax in range(k):
                b_pos = (p, ax)
                if b_pos not in bset:
                    perim_edges.add(b_pos)
                pm = list(p)
                pm[ax] -= 1
                b_neg = (tuple(pm), ax)
                if b_neg not in bset:
                    perim_edges.add(b_neg)
        counts[(len(perim_edges), len(pts))] += 1
    return counts


def eval_theorem7(e: int):
    g0 = (1 << (e - 7)) * (e - 3) * (
        8 * e**8 - 76 * e**7 + 254 * e**6 - 345 * e**5 + 446 * e**4
        - 2240 * e**3 + 16024 * e**2 - 76155 * e + 126212
    ) * (e + 1) ** (e - 8) // 3 if e >= 7 else 0
    # Use exact rational arithmetic so e = 4, 5, 6 work without negative shift issues
    from fractions import Fraction
    f2 = Fraction(1 << e)
    ep1 = Fraction(e + 1) ** (e - 8)
    ep0 = Fraction(e) ** (e - 7)
    vals = {
        (e + 1, 0): int(f2 * ep1 * Fraction(e - 3, 384) * (
            8 * e**8 - 76 * e**7 + 254 * e**6 - 345 * e**5 + 446 * e**4
            - 2240 * e**3 + 16024 * e**2 - 76155 * e + 126212
        )),
        (e + 1, 1): int(f2 * ep1 * Fraction((e - 3) * (e - 4), 96) * (
            12 * e**6 - 56 * e**5 - 49 * e**4 + 771 * e**3 - 245 * e**2 - 7243 * e + 15930
        )),
        (e + 1, 2): int(f2 * ep1 * Fraction((e - 3) * (e - 4), 32) * (
            8 * e**5 - 2 * e**4 - 325 * e**3 + 376 * e**2 + 5541 * e - 16990
        )),
        (e + 1, 3): int(f2 * ep1 * Fraction((e - 3) * (e - 4) * (e - 5), 24) * (
            4 * e**3 + 51 * e**2 + 120 * e - 2195
        )),
        (e, 0): int(f2 * ep0 * Fraction((e - 3) * (e - 4), 32) * (
            2 * e**3 - 9 * e**2 + 5 * e + 50
        )),
        (e, 1): int(f2 * ep0 * Fraction((e - 3) * (e - 4) * (e - 5), 16) * (2 * e + 9)),
    }
    return {kv: val for kv, val in vals.items() if val != 0}


def main():
    for e in [4, 5, 6]:
        k = e - 3
        bf_tv = enumerate_proper_animals_ztv(k, e)
        # Convert (t, v) to (v, s_chords = 2*k*v - 2*e - t)
        bf_vs = {(v, 2 * k * v - 2 * e - t): cnt for (t, v), cnt in bf_tv.items()}
        th7 = eval_theorem7(e)
        assert bf_vs == th7, f"Mismatch at e={e}: {bf_vs} != {th7}"
        print(f"Brute force (k={k}, e={e}) G_{{e,t,v}}^({k}) = {dict(sorted(bf_tv.items()))} -> MATCHES Theorem 7: {dict(sorted(th7.items()))}")


if __name__ == "__main__":
    main()
