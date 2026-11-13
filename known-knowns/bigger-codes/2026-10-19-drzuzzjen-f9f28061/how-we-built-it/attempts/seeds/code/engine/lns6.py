#!/usr/bin/env python3
"""Shared numba helpers for the low-blocker exact LNS engines (d = 6 subset ranks, owner array, exact MIS).

Packing view: two weight-w words are at distance < 6 iff they share a (w-2)-subset.  owner[rank(s)] = id of the
codeword containing the (w-2)-subset s (or -1).  blockers(x) = distinct owners over the C(w,2) subsets of x.
mis_exact() is the bitset branch-and-bound maximum independent set solver used by lb_lns.py.

(This module started as a random-removal-set LNS driver; that driver was too slow and is not part of this release.
Only the helpers below are imported by lb_lns.py, lb_lns_gen.py and the later engines.)
"""
import sys, os, time, json
import numpy as np
import numba as nb
from math import comb

KMAX = 512          # max candidates in an exact MIS (bitset width 8 x 64)
WMAX = KMAX // 64


@nb.njit(cache=True)
def binom_table(N):
    T = np.zeros((N + 1, N + 1), dtype=np.int64)
    for a in range(N + 1):
        T[a, 0] = 1
        for b in range(1, a + 1):
            T[a, b] = T[a - 1, b - 1] + T[a - 1, b]
    return T


@nb.njit(cache=True)
def sub_ranks(x, n, w, B, out, e, S0, S1, S2):
    """colex ranks of the C(w,2) (w-2)-subsets of x (subset = x minus positions p<q of its sorted support)."""
    k = 0
    for i in range(n):
        if (x >> i) & 1:
            e[k] = i
            k += 1
    S0[0] = 0
    S1[0] = 0
    S2[0] = 0
    for k in range(w):
        S0[k + 1] = S0[k] + B[e[k], k + 1]
        S1[k + 1] = S1[k] + B[e[k], k]
        if k >= 1:
            S2[k + 1] = S2[k] + B[e[k], k - 1]
        else:
            S2[k + 1] = S2[k]
    idx = 0
    for p in range(w):
        for q in range(p + 1, w):
            out[idx] = S0[p] + (S1[q] - S1[p + 1]) + (S2[w] - S2[q + 1])
            idx += 1
    return idx


@nb.njit(cache=True)
def is_free(x, n, w, B, owner, rk, e, S0, S1, S2):
    m = sub_ranks(x, n, w, B, rk, e, S0, S1, S2)
    for i in range(m):
        if owner[rk[i]] != -1:
            return False
    return True


@nb.njit(cache=True)
def blockers(x, n, w, B, owner, rk, e, S0, S1, S2, outb):
    m = sub_ranks(x, n, w, B, rk, e, S0, S1, S2)
    nb_ = 0
    for i in range(m):
        o = owner[rk[i]]
        if o != -1:
            dup = False
            for j in range(nb_):
                if outb[j] == o:
                    dup = True
                    break
            if not dup:
                outb[nb_] = o
                nb_ += 1
    return nb_


@nb.njit(cache=True)
def set_owner(x, val, n, w, B, owner, rk, e, S0, S1, S2):
    m = sub_ranks(x, n, w, B, rk, e, S0, S1, S2)
    for i in range(m):
        owner[rk[i]] = val


@nb.njit(cache=True)
def build_owner(words, M, n, w, B, owner):
    rk = np.zeros(w * w, dtype=np.int64)
    e = np.zeros(64, dtype=np.int64)
    S0 = np.zeros(65, dtype=np.int64)
    S1 = np.zeros(65, dtype=np.int64)
    S2 = np.zeros(65, dtype=np.int64)
    bad = 0
    for i in range(M):
        m = sub_ranks(words[i], n, w, B, rk, e, S0, S1, S2)
        for j in range(m):
            if owner[rk[j]] != -1:
                bad += 1
            owner[rk[j]] = i
    return bad


@nb.njit(cache=True)
def popc(x):
    # int64 popcount
    c = 0
    while x != 0:
        x &= x - 1
        c += 1
    return c


@nb.njit(cache=True)
def popcu(x):
    # uint64 popcount
    c = 0
    one = np.uint64(1)
    zero = np.uint64(0)
    while x != zero:
        x &= x - one
        c += 1
    return c


@nb.njit(cache=True)
def mis_exact(cand, K, w, node_cap):
    """maximum independent set in the conflict graph on cand[0:K] (conflict iff |x & y| >= w-2).
    Returns (size, chosen bitset as array of WMAX uint64, complete flag)."""
    W = (K + 63) // 64
    adj = np.zeros((K, WMAX), dtype=np.uint64)
    for i in range(K):
        for j in range(i + 1, K):
            if popc(cand[i] & cand[j]) >= w - 2:
                adj[i, j >> 6] |= np.uint64(1) << np.uint64(j & 63)
                adj[j, i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    # explicit DFS stack
    stP = np.zeros((K + 2, WMAX), dtype=np.uint64)
    stC = np.zeros((K + 2, WMAX), dtype=np.uint64)
    stS = np.zeros(K + 2, dtype=np.int64)
    for i in range(K):
        stP[0, i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    sp = 1
    best = 0
    bestC = np.zeros(WMAX, dtype=np.uint64)
    tmp = np.zeros(WMAX, dtype=np.uint64)
    cand2 = np.zeros(WMAX, dtype=np.uint64)
    nodes = 0
    complete = True
    while sp > 0:
        sp -= 1
        nodes += 1
        if nodes > node_cap:
            complete = False
            break
        P = stP[sp].copy()
        C = stC[sp].copy()
        size = stS[sp]
        # count P
        cntP = 0
        for k in range(W):
            cntP += popcu(P[k])
        if cntP == 0:
            if size > best:
                best = size
                bestC[:] = C
            continue
        if size + cntP <= best:
            continue
        # greedy clique cover bound of P
        for k in range(W):
            tmp[k] = P[k]
        cover = 0
        while True:
            v = -1
            for k in range(W):
                if tmp[k] != 0:
                    t = tmp[k]
                    b = 0
                    while (t & np.uint64(1)) == 0:
                        t >>= np.uint64(1)
                        b += 1
                    v = k * 64 + b
                    break
            if v < 0:
                break
            cover += 1
            tmp[v >> 6] &= ~(np.uint64(1) << np.uint64(v & 63))
            for k in range(W):
                cand2[k] = tmp[k] & adj[v, k]
            while True:
                u = -1
                for k in range(W):
                    if cand2[k] != 0:
                        t = cand2[k]
                        b = 0
                        while (t & np.uint64(1)) == 0:
                            t >>= np.uint64(1)
                            b += 1
                        u = k * 64 + b
                        break
                if u < 0:
                    break
                tmp[u >> 6] &= ~(np.uint64(1) << np.uint64(u & 63))
                for k in range(W):
                    cand2[k] &= adj[u, k]
                cand2[u >> 6] &= ~(np.uint64(1) << np.uint64(u & 63))
        if size + cover <= best:
            continue
        # branch on vertex of max degree inside P
        bv = -1
        bd = -1
        for k in range(W):
            t = P[k]
            while t != 0:
                low = t & (~t + np.uint64(1))
                b = 0
                tt = low
                while tt > np.uint64(1):
                    tt >>= np.uint64(1)
                    b += 1
                v = k * 64 + b
                dg = 0
                for kk in range(W):
                    dg += popcu(adj[v, kk] & P[kk])
                if dg > bd:
                    bd = dg
                    bv = v
                t ^= low
        if bd == 0:
            # P independent: take all
            if size + cntP > best:
                best = size + cntP
                for k in range(W):
                    bestC[k] = C[k] | P[k]
            continue
        # child 1: exclude bv
        stP[sp, :] = P
        stP[sp, bv >> 6] &= ~(np.uint64(1) << np.uint64(bv & 63))
        stC[sp, :] = C
        stS[sp] = size
        sp += 1
        # child 2: include bv (explored first)
        for k in range(W):
            stP[sp, k] = P[k] & ~adj[bv, k]
        stP[sp, bv >> 6] &= ~(np.uint64(1) << np.uint64(bv & 63))
        stC[sp, :] = C
        stC[sp, bv >> 6] |= np.uint64(1) << np.uint64(bv & 63)
        stS[sp] = size + 1
        sp += 1
    return best, bestC, complete
