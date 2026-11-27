#!/usr/bin/env python3
"""A089980 hard squares T(w,m) mod primes: cell-by-cell broken-profile DP, numpy.

State factorisation (key trick): when the break sits after row k of the current
column, the frontier is (A, B) with
    A = occupancy of current column rows r_0..r_k   (a Fibonacci string, no two adjacent 1s)
    B = occupancy of previous column rows r_{k+1}.. (a Fibonacci string)
and NO constraint between A and B (the two cells across the break are diagonal).
So the state space is a product V(k+1) x V(w-k-1), stored as a dense 2-D array.

Ordering: Fibonacci strings of length n are ordered recursively by their LEADING
bit: [0 + V(n-1)] followed by [1 + 0 + V(n-2)]. Then the strings with leading
0 are the first V(n-1) entries and those with leading 1 are the next V(n-2)
entries, whose tails coincide with the first V(n-2) entries of V(n-1).
B's leading bit = next row to process; A's leading bit = most recently processed row.
Processing cell r_k (new bit x, left neighbour b = leading bit of B, up neighbour =
leading bit of A'):
    new[:nA', :]      = old[:, :N1] (+ old[:, N1:] on first N2 cols)      x = 0
    new[nA':, :]      = old[:nA0, :N1]                                    x = 1 (b=0, up=0)
All operations are contiguous slices. At column end A holds the whole column with
its last row leading; the next column is processed in the opposite direction so
this is exactly the required B ordering (boustrophedon, no permutation).

Arithmetic: uint64, primes p < 2^31, each cell at most adds two entries, so a value
at most doubles per cell; after a reduction values are < 2^31, so 32 unreduced
cells keep values < 2^63 < 2^64. We reduce every RED=32 cells (no overflow).
A trailing axis holds P primes at once.

CLI:
  hs_mod.py residues W L P [--first-prime-index i]   -> prints m, residues for each prime
  hs_mod.py exact W L [--stacked]                     -> exact T(W,m), m=0..L via CRT
  hs_mod.py validate BFILE W [W ...] [--stacked]      -> compare vs b-file, w+m<=78
  (exact/validate default: one prime per sweep; --stacked = v1 all-primes-at-once)
  hs_mod.py bench W L P                               -> time one sweep
"""
import sys, time, math, resource
import numpy as np

RED = 32


def V(n):
    # number of Fibonacci strings of length n; V(-1)=1, V(0)=1, V(1)=2
    a, b = 1, 1  # V(-1), V(0)
    if n == -1:
        return 1
    for _ in range(n):
        a, b = b, a + b
    return b


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primes_below_2_31(count, start=0):
    out, n, idx = [], (1 << 31) - 1, 0
    while len(out) < count:
        if is_prime(n):
            if idx >= start:
                out.append(n)
            idx += 1
        n -= 2 if n % 2 else 1
    return out


def residues(w, L, primes):
    """Return array R of shape (L+1, P): R[m, j] = T(w, m) mod primes[j]."""
    P = len(primes)
    pr = np.array(primes, dtype=np.uint64)
    R = np.zeros((L + 1, P), dtype=np.uint64)
    R[0] = 1 % pr
    if w == 0:
        R[:] = 1 % pr
        return R
    maxst = max(V(k) * V(w - k) for k in range(w + 1))
    buf0 = np.zeros(maxst * P, dtype=np.uint64)
    buf1 = np.zeros(maxst * P, dtype=np.uint64)
    # column 0: previous column empty -> B = all-zero string (index 0)
    cur = buf0[: V(w) * P].reshape(1, V(w), P)
    cur[:] = 0
    cur[0, 0, :] = 1
    since = 0
    for m in range(1, L + 1):
        for k in range(w):
            nAp = V(k)          # A' strings, length k
            nA0 = V(k - 1)      # A' with leading bit 0
            nB = V(w - k)       # B' strings length w-k
            N1 = V(w - k - 1)
            N2 = V(w - k - 2)
            assert cur.shape[0] == nAp and cur.shape[1] == nB
            nA = nAp + nA0
            # choose the other buffer
            other = buf1 if np.shares_memory(cur, buf0) else buf0
            new = other[: nA * N1 * P].reshape(nA, N1, P)
            new[:nAp] = cur[:, :N1]
            new[:nAp, :N2] += cur[:, N1:]
            new[nAp:] = cur[:nA0, :N1]
            cur = new
            since += 1
            if since >= RED:
                np.remainder(cur, pr, out=cur)
                since = 0
        # end of column: cur shape (V(w), 1, P) -> becomes B for next column
        np.remainder(cur, pr, out=cur)
        since = 0
        cur = cur.reshape(1, V(w), P)
        R[m] = cur.sum(axis=(0, 1), dtype=np.uint64) % pr  # V(w)*2^31 < 2^64 for w<=60
    return R


def crt(res, primes):
    """Garner/CRT: res list of residues -> integer in [0, prod)."""
    x, M = 0, 1
    for r, p in zip(res, primes):
        t = ((int(r) - x) * pow(M, -1, p)) % p
        x += M * t
        M *= p
    return x, M


def nprimes_for(w, L, extra=1):
    # rigorous bound T(w,m) <= V(w)^m ; primes > 2^30.99
    bits = L * math.log2(V(w)) + 1
    return int(math.ceil(bits / 30.99)) + extra


def exact(w, L, stacked=False):
    """Exact T(w,m), m=0..L. Default: one prime per DP sweep (peak memory = one prime).
    stacked=True restores the v1 behaviour (all primes on a trailing axis, one sweep)."""
    n = nprimes_for(w, L)
    primes = primes_below_2_31(n)
    if stacked:
        R = residues(w, L, primes)
    else:
        R = np.zeros((L + 1, n), dtype=np.uint64)
        for j, p in enumerate(primes):
            R[:, j] = residues(w, L, [p])[:, 0]
    out = []
    for m in range(L + 1):
        x, M = crt(R[m, :-1], primes[:-1])
        assert x % primes[-1] == int(R[m, -1]), "check prime disagrees"
        out.append(x)
    return out


def parse_bfile(path):
    seq = []
    for line in open(path, encoding="utf-8"):
        p = line.split()
        if len(p) == 2 and p[0].lstrip("-").isdigit():
            seq.append(int(p[1]))
    vals, k, d = {}, 0, 0
    while k + d + 1 <= len(seq):
        for i in range(d + 1):
            vals[(i, d - i)] = seq[k + i]
        k += d + 1
        d += 1
    return vals, d - 1


def main():
    a = sys.argv[1:]
    stacked = "--stacked" in a
    a = [x for x in a if x != "--stacked"]
    fpi = 0
    if "--first-prime-index" in a:
        i = a.index("--first-prime-index")
        fpi = int(a[i + 1])
        del a[i:i + 2]
    if a[0] == "residues":
        w, L, P = int(a[1]), int(a[2]), int(a[3])
        primes = primes_below_2_31(P, start=fpi)
        R = residues(w, L, primes)
        print("primes", *primes)
        for m in range(L + 1):
            print(m, *[int(x) for x in R[m]])
    elif a[0] == "exact":
        w, L = int(a[1]), int(a[2])
        for m, x in enumerate(exact(w, L, stacked)):
            print(w, m, x)
    elif a[0] == "validate":
        vals, dmax = parse_bfile(a[1])
        tot = bad = 0
        for w in map(int, a[2:]):
            t0 = time.time()
            L = dmax - w
            ex = exact(w, L, stacked)
            mism = 0
            for m in range(L + 1):
                tot += 1
                if vals[(w, m)] != ex[m] or vals[(m, w)] != ex[m]:
                    mism += 1
            bad += mism
            print(f"w={w} cells={L+1} m=0..{L} primes={nprimes_for(w, L)} mismatches={mism} "
                  f"time={time.time()-t0:.2f}s "
                  f"peak_rss_MiB={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20:.0f}", flush=True)
        print(f"TOTAL cells={tot} mismatches={bad} (dmax={dmax}) mode={'stacked' if stacked else 'per-prime'}")
    elif a[0] == "bench":
        w, L, P = int(a[1]), int(a[2]), int(a[3])
        primes = primes_below_2_31(P)
        t0 = time.time()
        R = residues(w, L, primes)
        dt = time.time() - t0
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20  # macOS bytes -> MiB
        maxst = max(V(k) * V(w - k) for k in range(w + 1))
        print(f"BENCH w={w} L={L} P={P} sec={dt:.3f} sec_per_prime={dt/P:.3f} "
              f"sec_per_prime_col={dt/P/L:.5f} maxstates={maxst} rss_MiB={rss:.0f} "
              f"chk={int(R[L,0])}", flush=True)


if __name__ == "__main__":
    main()
