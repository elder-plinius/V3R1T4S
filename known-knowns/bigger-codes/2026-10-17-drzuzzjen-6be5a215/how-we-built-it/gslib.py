#!/usr/bin/env python3
"""Graham-Sloane class codes for d = 6 and an exhaustive maximality test, in numba.

Words are int64 bitmasks over n <= 62 coordinates (bit i = coordinate i).  For an S2 set a_0..a_{n-1} in Z_m, the
class C_g = {x : |x| = w, sum_{i in x} a_i = g mod m} has minimum distance >= 6 (a 1-swap changes the sum by
a_j - a_i != 0, a 2-swap by a_j1 + a_j2 - a_i1 - a_i2 != 0 by the S2 property).

free_words(g): every weight-w word x NOT in C_g such that no word of C_g is within distance 4 of x, i.e. no 1-swap or
2-swap of x lands in class g.  Such words can be added to C_g (subject to compatibility among themselves).
"""
import numpy as np
import numba as nb
from math import comb


@nb.njit(cache=True)
def _binom_table(N):
    T = np.zeros((N + 1, N + 1), dtype=np.int64)
    for a in range(N + 1):
        T[a, 0] = 1
        for b in range(1, a + 1):
            T[a, b] = T[a - 1, b - 1] + T[a - 1, b]
    return T


@nb.njit(cache=True)
def _unrank_colex(r, w, B):
    # combination c_1<..<c_w with sum C(c_i, i) = r  (colex == increasing integer order of bitmasks)
    x = 0
    for i in range(w, 0, -1):
        c = i - 1
        while B[c + 1, i] <= r:
            c += 1
        x |= (1 << c)
        r -= B[c, i]
    return x


@nb.njit(cache=True)
def _next_comb(x):
    u = x & -x
    v = x + u
    return v + (((v ^ x) // u) >> 2)


@nb.njit(cache=True)
def _wsum(x, a, m):
    s = 0
    while x:
        low = x & -x
        i = 0
        t = low
        while t > 1:
            t >>= 1
            i += 1
        s += a[i]
        x ^= low
    return s % m


@nb.njit(cache=True)
def _bitidx(low):
    i = 0
    while low > 1:
        low >>= 1
        i += 1
    return i


@nb.njit(parallel=True, cache=True)
def class_counts(n, w, a, m, nchunks):
    B = _binom_table(64)
    total = B[n, w]
    counts = np.zeros((nchunks, m), dtype=np.int64)
    step = (total + nchunks - 1) // nchunks
    for ch in nb.prange(nchunks):
        r0 = ch * step
        r1 = min(total, r0 + step)
        if r0 >= r1:
            continue
        x = _unrank_colex(r0, w, B)
        for r in range(r0, r1):
            s = 0
            y = x
            while y:
                low = y & -y
                s += a[_bitidx(low)]
                y ^= low
            counts[ch, s % m] += 1
            if r + 1 < r1:
                x = _next_comb(x)
    out = np.zeros(m, dtype=np.int64)
    for ch in range(nchunks):
        out += counts[ch]
    return out


@nb.njit(parallel=True, cache=True)
def class_words(n, w, a, m, g, nchunks, cap):
    B = _binom_table(64)
    total = B[n, w]
    step = (total + nchunks - 1) // nchunks
    buf = np.zeros((nchunks, cap), dtype=np.int64)
    cnt = np.zeros(nchunks, dtype=np.int64)
    for ch in nb.prange(nchunks):
        r0 = ch * step
        r1 = min(total, r0 + step)
        if r0 >= r1:
            continue
        x = _unrank_colex(r0, w, B)
        for r in range(r0, r1):
            s = 0
            y = x
            while y:
                low = y & -y
                s += a[_bitidx(low)]
                y ^= low
            if s % m == g:
                if cnt[ch] < cap:
                    buf[ch, cnt[ch]] = x
                cnt[ch] += 1
            if r + 1 < r1:
                x = _next_comb(x)
    return buf, cnt


def swap_tables(a, m):
    """one_i/one_j[delta]: the unique (i,j) with a_j - a_i = delta (Sidon) or -1.
    CSR pattern lists of 2-swaps: I mask = {i1,i2} (leave), J mask = {j1,j2} (enter), a_j1+a_j2-a_i1-a_i2 = delta."""
    n = len(a)
    one_i = -np.ones(m, dtype=np.int64)
    one_j = -np.ones(m, dtype=np.int64)
    for i in range(n):
        for j in range(n):
            if i != j:
                dl = (a[j] - a[i]) % m
                assert one_i[dl] == -1, "not Sidon"
                one_i[dl] = i
                one_j[dl] = j
    pats = [[] for _ in range(m)]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for (i1, i2) in pairs:
        for (j1, j2) in pairs:
            if len({i1, i2, j1, j2}) < 4:
                continue
            dl = (a[j1] + a[j2] - a[i1] - a[i2]) % m
            pats[dl].append(((1 << i1) | (1 << i2), (1 << j1) | (1 << j2)))
    ptr = np.zeros(m + 1, dtype=np.int64)
    for dl in range(m):
        ptr[dl + 1] = ptr[dl] + len(pats[dl])
    I = np.zeros(ptr[-1], dtype=np.int64)
    J = np.zeros(ptr[-1], dtype=np.int64)
    k = 0
    for dl in range(m):
        for (im, jm) in pats[dl]:
            I[k] = im
            J[k] = jm
            k += 1
    return one_i, one_j, ptr, I, J


@nb.njit(parallel=True, cache=True)
def free_words(n, w, a, m, g, one_i, one_j, ptr, I, J, nchunks, cap):
    """words x not in class g with no 1-/2-swap into class g."""
    B = _binom_table(64)
    total = B[n, w]
    step = (total + nchunks - 1) // nchunks
    buf = np.zeros((nchunks, cap), dtype=np.int64)
    cnt = np.zeros(nchunks, dtype=np.int64)
    for ch in nb.prange(nchunks):
        r0 = ch * step
        r1 = min(total, r0 + step)
        if r0 >= r1:
            continue
        x = _unrank_colex(r0, w, B)
        for r in range(r0, r1):
            s = 0
            y = x
            while y:
                low = y & -y
                s += a[_bitidx(low)]
                y ^= low
            s %= m
            if s != g:
                dl = (g - s) % m
                ok = True
                i = one_i[dl]
                if i >= 0:
                    if ((x >> i) & 1) == 1 and ((x >> one_j[dl]) & 1) == 0:
                        ok = False
                if ok:
                    for k in range(ptr[dl], ptr[dl + 1]):
                        if (x & I[k]) == I[k] and (x & J[k]) == 0:
                            ok = False
                            break
                if ok:
                    if cnt[ch] < cap:
                        buf[ch, cnt[ch]] = x
                    cnt[ch] += 1
            if r + 1 < r1:
                x = _next_comb(x)
    return buf, cnt


def gather(buf, cnt):
    out = []
    for ch in range(len(cnt)):
        c = int(cnt[ch])
        assert c <= buf.shape[1], "cap overflow"
        out.append(buf[ch, :c])
    return np.concatenate(out) if out else np.zeros(0, dtype=np.int64)


@nb.njit(parallel=True, cache=True)
def free_multi(n, w, a, m, G, one_i, one_j, ptr, I, J, nchunks, cap):
    """free words for several target classes G[0..K-1] in one pass: buf[ch, k, :], cnt[ch, k]."""
    B = _binom_table(64)
    total = B[n, w]
    step = (total + nchunks - 1) // nchunks
    K = G.shape[0]
    buf = np.zeros((nchunks, K, cap), dtype=np.int64)
    cnt = np.zeros((nchunks, K), dtype=np.int64)
    for ch in nb.prange(nchunks):
        r0 = ch * step
        r1 = min(total, r0 + step)
        if r0 >= r1:
            continue
        x = _unrank_colex(r0, w, B)
        for r in range(r0, r1):
            s = 0
            y = x
            while y:
                low = y & -y
                s += a[_bitidx(low)]
                y ^= low
            s %= m
            for kk in range(K):
                g = G[kk]
                if s == g:
                    continue
                dl = (g - s) % m
                ok = True
                i = one_i[dl]
                if i >= 0:
                    if ((x >> i) & 1) == 1 and ((x >> one_j[dl]) & 1) == 0:
                        ok = False
                if ok:
                    for k in range(ptr[dl], ptr[dl + 1]):
                        if (x & I[k]) == I[k] and (x & J[k]) == 0:
                            ok = False
                            break
                if ok:
                    c = cnt[ch, kk]
                    if c < cap:
                        buf[ch, kk, c] = x
                    cnt[ch, kk] += 1
            if r + 1 < r1:
                x = _next_comb(x)
    return buf, cnt
