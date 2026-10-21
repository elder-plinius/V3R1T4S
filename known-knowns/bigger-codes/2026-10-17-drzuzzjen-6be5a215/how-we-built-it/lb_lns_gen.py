#!/usr/bin/env python3
"""Low-blocker exact LNS for constant-weight codes, general even d.
Generalisation of lb_lns.py: two words conflict iff they share a t-subset, t = w - d/2 + 1 (r = d/2 - 1 removals).

Round:
 1. one parallel pass over ALL C(n,w) words computes, for every non-code word, its blockers (codewords sharing a
    (w-2)-subset), keeping words with <= KB blockers ("low-blocked" words);
 2. removal sets R are taken from the blocker hypergraph: singletons, the blocker pairs/triples of 2-/3-blocked words,
    and random connected clusters (|R| <= rmax) of the co-blocking graph;
 3. for each R the candidate set is every low-blocked word whose blockers lie inside R, plus R itself, and an EXACT
    maximum independent set is computed (bitset branch and bound from lns6.mis_exact);
 4. all improving moves (|MIS| > |R|) with disjoint R and mutually compatible insertions are applied at once; if there
    are none, a random batch of disjoint plateau moves (|MIS| = |R|, different words) is applied instead.
The code is re-validated (owner rebuild: no (w-2)-subset used twice) after every round and saved when it grows.
Candidates with more than KB blockers are not enumerated, so step 3 is exact over the enumerated candidate set only.

usage: lb_lns_gen.py SEED.npy N D W OUT_PREFIX [--rounds R] [--seconds S] [--rmax 8] [--kb 3] [--seed X] [--plateau-frac F]
"""
import sys, os, time, json, random
import numpy as np
import numba as nb
from math import comb
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lns6 import binom_table, popc, popcu, KMAX, WMAX
from gslib import _unrank_colex, _next_comb


@nb.njit(cache=True)
def sub_ranks_g(x, n, w, r, B, out, e, S, pos):
    """colex ranks of all C(w, r)-many (w-r)-subsets of x."""
    k = 0
    for i in range(n):
        if (x >> i) & 1:
            e[k] = i
            k += 1
    for c in range(r + 1):
        S[c, 0] = 0
        for k in range(w):
            j = k + 1 - c
            S[c, k + 1] = S[c, k] + (B[e[k], j] if j >= 0 else 0)
    for i in range(r):
        pos[i] = i
    idx = 0
    while True:
        rank = S[0, pos[0]]
        for c in range(1, r):
            rank += S[c, pos[c]] - S[c, pos[c - 1] + 1]
        rank += S[r, w] - S[r, pos[r - 1] + 1]
        out[idx] = rank
        idx += 1
        # next combination of positions
        i = r - 1
        while i >= 0 and pos[i] == w - r + i:
            i -= 1
        if i < 0:
            break
        pos[i] += 1
        for j in range(i + 1, r):
            pos[j] = pos[j - 1] + 1
    return idx


@nb.njit(cache=True)
def build_owner_g(words, M, n, w, r, B, owner):
    nsub = B[w, r]
    rk = np.zeros(nsub, dtype=np.int64)
    e = np.zeros(64, dtype=np.int64)
    S = np.zeros((r + 1, 65), dtype=np.int64)
    pos = np.zeros(r, dtype=np.int64)
    bad = 0
    for i in range(M):
        m = sub_ranks_g(words[i], n, w, r, B, rk, e, S, pos)
        for j in range(m):
            if owner[rk[j]] != -1:
                bad += 1
            owner[rk[j]] = i
    return bad


@nb.njit(cache=True)
def mis_exact_g(cand, K, tthr, node_cap):
    """maximum independent set in the conflict graph on cand[0:K] (conflict iff |x & y| >= tthr)."""
    W = (K + 63) // 64
    adj = np.zeros((K, WMAX), dtype=np.uint64)
    for i in range(K):
        for j in range(i + 1, K):
            if popc(cand[i] & cand[j]) >= tthr:
                adj[i, j >> 6] |= np.uint64(1) << np.uint64(j & 63)
                adj[j, i >> 6] |= np.uint64(1) << np.uint64(i & 63)
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
    one = np.uint64(1)
    while sp > 0:
        sp -= 1
        nodes += 1
        if nodes > node_cap:
            complete = False
            break
        P = stP[sp].copy()
        C = stC[sp].copy()
        size = stS[sp]
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
        for k in range(W):
            tmp[k] = P[k]
        cover = 0
        while True:
            v = -1
            for k in range(W):
                if tmp[k] != 0:
                    t = tmp[k]
                    b = 0
                    while (t & one) == 0:
                        t >>= one
                        b += 1
                    v = k * 64 + b
                    break
            if v < 0:
                break
            cover += 1
            tmp[v >> 6] &= ~(one << np.uint64(v & 63))
            for k in range(W):
                cand2[k] = tmp[k] & adj[v, k]
            while True:
                u = -1
                for k in range(W):
                    if cand2[k] != 0:
                        t = cand2[k]
                        b = 0
                        while (t & one) == 0:
                            t >>= one
                            b += 1
                        u = k * 64 + b
                        break
                if u < 0:
                    break
                tmp[u >> 6] &= ~(one << np.uint64(u & 63))
                for k in range(W):
                    cand2[k] &= adj[u, k]
                cand2[u >> 6] &= ~(one << np.uint64(u & 63))
        if size + cover <= best:
            continue
        bv = -1
        bd = -1
        for k in range(W):
            t = P[k]
            while t != 0:
                low = t & (~t + one)
                b = 0
                tt = low
                while tt > one:
                    tt >>= one
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
            if size + cntP > best:
                best = size + cntP
                for k in range(W):
                    bestC[k] = C[k] | P[k]
            continue
        stP[sp, :] = P
        stP[sp, bv >> 6] &= ~(one << np.uint64(bv & 63))
        stC[sp, :] = C
        stS[sp] = size
        sp += 1
        for k in range(W):
            stP[sp, k] = P[k] & ~adj[bv, k]
        stP[sp, bv >> 6] &= ~(one << np.uint64(bv & 63))
        stC[sp, :] = C
        stC[sp, bv >> 6] |= one << np.uint64(bv & 63)
        stS[sp] = size + 1
        sp += 1
    return best, bestC, complete


@nb.njit(parallel=True, cache=True)
def lowblock(n, w, r, owner, words, KB, nchunks, cap):
    B = binom_table(63)
    total = B[n, w]
    step = (total + nchunks - 1) // nchunks
    outw = np.zeros((nchunks, cap), dtype=np.int64)
    outb = -np.ones((nchunks, cap, KB), dtype=np.int64)
    outn = np.zeros((nchunks, cap), dtype=np.int8)
    cnt = np.zeros(nchunks, dtype=np.int64)
    for ch in nb.prange(nchunks):
        r0 = ch * step
        r1 = min(total, r0 + step)
        if r0 >= r1:
            continue
        rk = np.zeros(B[w, r], dtype=np.int64)
        e = np.zeros(64, dtype=np.int64)
        S = np.zeros((r + 1, 65), dtype=np.int64)
        pos = np.zeros(r, dtype=np.int64)
        bl = np.zeros(KB + 1, dtype=np.int64)
        x = _unrank_colex(r0, w, B)
        for rr in range(r0, r1):
            m = sub_ranks_g(x, n, w, r, B, rk, e, S, pos)
            nbk = 0
            iscode = False
            for i in range(m):
                o = owner[rk[i]]
                if o != -1:
                    dup = False
                    for j in range(nbk):
                        if bl[j] == o:
                            dup = True
                            break
                    if not dup:
                        if words[o] == x:
                            iscode = True
                            break
                        bl[nbk] = o
                        nbk += 1
                        if nbk > KB:
                            break
            if (not iscode) and nbk <= KB:
                c = cnt[ch]
                if c < cap:
                    outw[ch, c] = x
                    outn[ch, c] = nbk
                    for j in range(nbk):
                        outb[ch, c, j] = bl[j]
                cnt[ch] += 1
            if rr + 1 < r1:
                x = _next_comb(x)
    return outw, outb, outn, cnt


def analyse(words, n, d, w, KB, nchunks=256):
    B = binom_table(63)
    r = d // 2 - 1
    owner = -np.ones(comb(n, w - r), dtype=np.int32)
    bad = build_owner_g(words, len(words), n, w, r, B, owner)
    assert bad == 0, f"INVALID code: {bad} shared t-subsets"
    cap = max(20000, int(comb(n, w) // nchunks // 20))
    while True:
        ow, ob, on, cnt = lowblock(n, w, r, owner, words, KB, nchunks, cap)
        if cnt.max() <= cap:
            break
        cap = int(cnt.max()) + 1000
    W, BL, NB = [], [], []
    for ch in range(nchunks):
        c = int(cnt[ch])
        W.append(ow[ch, :c]); BL.append(ob[ch, :c]); NB.append(on[ch, :c])
    return np.concatenate(W), np.concatenate(BL), np.concatenate(NB).astype(np.int64)


def compatible(x, y, tthr):
    return bin(int(x) & int(y)).count("1") < tthr


def run_round(words, n, d, w, KB, rmax, rng, node_cap, ncluster, plateau_frac, log):
    tthr = w - d // 2 + 1
    t0 = time.time()
    lw, lb, ln = analyse(words, n, d, w, KB)
    t1 = time.time()
    # index: blocker-set (sorted tuple) -> list of words ; codeword -> list of low-blocked word indices
    byset = defaultdict(list)
    bycw = defaultdict(list)
    for i in range(len(lw)):
        k = int(ln[i])
        s = tuple(sorted(int(v) for v in lb[i, :k]))
        byset[s].append(int(lw[i]))
        for c in s:
            bycw[c].append(i)
    free0 = byset.get((), [])
    hist = np.bincount(ln, minlength=KB + 1)
    log(f"  analyse: {len(lw)} low-blocked words, by #blockers {hist.tolist()} ({t1-t0:.0f}s)")
    # co-blocking graph adjacency from 2-/3-blocked words
    adj = defaultdict(set)
    for s in byset:
        if len(s) >= 2:
            for a in s:
                for b in s:
                    if a != b:
                        adj[a].add(b)
    Rs = set()
    for s in byset:
        if len(s) >= 1:
            Rs.add(s)
    # random clusters
    keys = list(adj.keys())
    for _ in range(ncluster if keys else 0):
        c = rng.choice(keys)
        R = {c}
        target = rng.randint(3, rmax)
        frontier = list(adj[c])
        while len(R) < target and frontier:
            v = frontier.pop(rng.randrange(len(frontier)))
            if v not in R:
                R.add(v)
                frontier.extend(u for u in adj[v] if u not in R)
        Rs.add(tuple(sorted(R)))
    improving, plateau = [], []
    nsolved = 0
    for R in Rs:
        Rset = set(R)
        cand = set()
        for c in R:
            for i in bycw[c]:
                k = int(ln[i])
                if all(int(v) in Rset for v in lb[i, :k]):
                    cand.add(int(lw[i]))
        if not cand:
            continue
        K = len(cand) + len(R)
        if K > KMAX:
            continue
        cl = sorted(cand)
        rng.shuffle(cl)
        candl = np.array(cl + [int(words[c]) for c in R], dtype=np.int64)  # R last: prefer new words on ties
        best, bestC, complete = mis_exact_g(candl, len(candl), tthr, node_cap)
        nsolved += 1
        if best < len(R):
            continue
        chosen = [int(candl[i]) for i in range(len(candl)) if (int(bestC[i >> 6]) >> (i & 63)) & 1]
        if best > len(R):
            improving.append((R, chosen))
        elif set(chosen) != set(int(words[c]) for c in R):
            plateau.append((R, chosen))
    t2 = time.time()
    log(f"  moves: {len(Rs)} removal sets, {nsolved} MIS solved, improving={len(improving)} plateau={len(plateau)} "
        f"({t2-t1:.0f}s)")
    # free words first (R = ())
    applied = []
    used, ins = set(), []

    def try_apply(R, S):
        if any(c in used for c in R):
            return False
        for x in S:
            for y in ins:
                if not compatible(x, y, tthr):
                    return False
        used.update(R)
        ins.extend(S)
        applied.append((R, S))
        return True

    # greedy maximal independent set of free words
    for x in free0:
        try_apply((), [x])
    improving.sort(key=lambda t: -(len(t[1]) - len(t[0])))
    for R, S in improving:
        try_apply(R, S)
    gain = sum(len(S) - len(R) for R, S in applied)
    if gain == 0 and plateau:
        rng.shuffle(plateau)
        for R, S in plateau[: max(1, int(len(plateau) * plateau_frac))]:
            try_apply(R, S)
    if not applied:
        return words, 0, 0
    rm = set(c for R, S in applied for c in R)
    keep = np.array([int(words[i]) for i in range(len(words)) if i not in rm], dtype=np.int64)
    new = np.unique(np.concatenate([keep, np.array(ins, dtype=np.int64)]))
    assert len(new) == len(keep) + len(ins), "duplicate insertion"
    return new, len(new) - len(words), len(applied)


def main():
    seedfile, n, d, w, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
    rounds = arg("--rounds", 1000)
    seconds = arg("--seconds", 3600.0)
    rmax = arg("--rmax", 8)
    KB = arg("--kb", 3)
    rs = arg("--seed", 1)
    ncl = arg("--clusters", 3000)
    pf = arg("--plateau-frac", 0.3)
    node_cap = arg("--nodecap", 100000)
    rng = random.Random(rs)
    words = np.unique(np.load(seedfile).astype(np.int64))
    M0 = len(words)
    best = M0
    logf = open(outp + ".log", "a")

    def log(s):
        print(s, flush=True)
        logf.write(s + "\n"); logf.flush()

    log(f"start {seedfile} M={M0} n={n} d={d} w={w} rmax={rmax} KB={KB} seed={rs}")
    t0 = time.time()
    for r in range(rounds):
        if time.time() - t0 > seconds:
            break
        words, gain, napp = run_round(words, n, d, w, KB, rmax, rng, node_cap, ncl, pf, log)
        M = len(words)
        log(f"round {r}: M={M} gain={gain} applied={napp} best={max(best, M)} t={time.time()-t0:.0f}s")
        if M > best:
            best = M
            np.save(outp + f"_best.npy", words)
            with open(outp + "_best.json", "w") as f:
                json.dump({"M": M, "n": n, "w": w, "d": d, "round": r, "t": time.time() - t0, "seed": seedfile}, f)
        np.save(outp + "_cur.npy", words)
    log(f"done best={best}")


if __name__ == "__main__":
    main()
