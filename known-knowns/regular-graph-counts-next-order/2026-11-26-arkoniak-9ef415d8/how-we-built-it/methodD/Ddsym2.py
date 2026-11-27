#!/usr/bin/env python3
"""Ddsym with the short part by Svdp.S_all: all (side, n, shift) values a type needs come from one vertex DP per side
(memory ~ residual-count states, was Dd._S's memo over node partitions: MemoryError at d=6, 25 fixed points)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dd, Ddsym, Svdp
SALL = Svdp.S_all  # 2026-11-21: runDd --cvdp sets this to Svdpc.S_all (C port)


def F_D(lam):
    lam = tuple(lam); N = sum(lam); d = Dd.DEG; P = Dd.PMOD
    if (d * N) % 2:
        return 0
    f = lam.count(1); m = lam.count(2)
    longs = [x for x in lam if x >= 3]
    Q = Ddsym.long_Q(longs, f, m) if longs else {tuple([0] * (2 * d)): 1}
    need = {0: set(), 1: set()}
    orig = Dd._S

    def rec_S(side, n, shift):
        need[side].add(tuple(shift)); return 1
    try:
        Dd._S = rec_S
        for inj, c in Q.items():
            if c:
                Dd.short_extract(f, m, inj)
        tab = {0: SALL(d, 0, f, need[0], P), 1: SALL(d, 1, m, need[1], P)}
        Dd._S = lambda side, n, shift: tab[side][tuple(shift)]
        total = 0
        for inj, c in Q.items():
            if c:
                s = Dd.short_extract(f, m, inj)
                if s:
                    total = (total + c * Dd._m(s)) % P
    finally:
        Dd._S = orig
    assert total < P // 2, (lam, 'residue too large: F >= PMOD/2?')
    return total
