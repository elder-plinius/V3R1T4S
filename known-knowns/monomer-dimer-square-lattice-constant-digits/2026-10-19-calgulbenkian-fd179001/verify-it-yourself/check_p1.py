#!/usr/bin/env python3
"""Standard-library-only checker for the p1 certificate of h2 (monomer-dimer entropy of the square lattice).

What it does (see PROOF.md for why this certifies an enclosure of h2):
 1. verifies the sha256 of every certificate part and of the concatenation (MANIFEST.txt);
 2. self-test: rebuilds the periodic-row transfer matrix P_m from its DEFINITION (matchings of the induced subgraph of the cycle)
    for m = 3..8 and compares it with the fast big-integer "lane" sweep used for large m;
 3. for each certified width m (22 and 24): enumerates the dihedral orbits of subsets of Z_m, rebuilds the full integer vector x from the
    orbit values in the parts, computes y = P_m x EXACTLY (integers), and takes the exact max and min of y_i/x_i over orbit representatives
    (y and x are invariant under rotations/reflections, so representatives suffice);  all x_i > 0 is checked;
 4. derives  upper = ln(max ratio at M)/M  and  lower = (ln(min ratio at m2+p) - ln(max ratio at m2))/p  with decimal arithmetic (60 digits,
    rounded outward by 1e-55) and prints the decimals certified.
Usage:  python3 check_p1.py            (run in the folder that holds MANIFEST.txt and the parts)
Memory: peak about 6.5 GB resident for m = 24 (measured).  Runtime is printed at the end.
"""
import sys, os, time, hashlib, functools, random
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
getcontext().prec = 70
W = 128                      # lane width in bits (all values stay below 2^110)
ENTRY_BYTES = 10             # certificate entries are 80-bit big-endian integers
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- definition of the transfer matrix (used only in the self-test) ----------
def cycle_matchings(mask, m):
    verts = [i for i in range(m) if (mask >> i) & 1]
    edges = [(i, (i + 1) % m) for i in range(m)]
    edges = [(a, b) for (a, b) in edges if (mask >> a) & 1 and (mask >> b) & 1]
    @functools.lru_cache(maxsize=None)
    def rec(vs):
        if not vs: return 1
        v = min(vs)
        total = rec(vs - {v})
        for (a, b) in edges:
            if a == v and b in vs: total += rec(vs - {v, b})
            elif b == v and a in vs: total += rec(vs - {v, a})
        return total
    return rec(frozenset(verts))
def dense_T(m):
    full = (1 << m) - 1
    return [[(cycle_matchings(full & ~(s | t), m) if (s & t) == 0 else 0) for t in range(1 << m)] for s in range(1 << m)]

# ---------- fast exact product with Python big integers as SIMD lanes ----------
def lane_mask(j, N):
    """big integer with all W bits set in every lane i < N whose bit j is 0"""
    cur = (1 << (W * (1 << j))) - 1
    curlen = 1 << (j + 1)
    while curlen < N:
        cur |= cur << (curlen * W); curlen *= 2
    return cur
def sweep(G0, G1, j, N):
    Mj = lane_mask(j, N); S = W * (1 << j)
    a0 = G0 & Mj; a1 = G1 & Mj
    b = ((G0 >> S) & Mj) + ((G1 >> S) & Mj)
    s = a0 + a1
    return b + a1 + (s << S), s
def apply_T(x, m):
    """y = P_m x, x a big integer holding 2^m lanes of W bits; exact."""
    N = 1 << m
    G0, G1 = x, 0
    for j in range(m): G0, G1 = sweep(G0, G1, j, N)
    y = G0 + G1
    G0 = x & lane_mask(0, N) & lane_mask(m - 1, N); G1 = 0       # wrap dimer on sites m-1,0: inner chain 1..m-2
    for j in range(1, m - 1): G0, G1 = sweep(G0, G1, j, N)
    return y + G0 + G1
def pack(vec):  return int.from_bytes(b"".join(v.to_bytes(W // 8, "little") for v in vec), "little")
def unpack(x, n):
    bs = x.to_bytes(n * (W // 8), "little"); return [int.from_bytes(bs[i * (W // 8):(i + 1) * (W // 8)], "little") for i in range(n)]

def selftest():
    rnd = random.Random(1)
    for m in range(3, 9):
        T = dense_T(m); N = 1 << m
        vec = [rnd.randrange(0, 1 << 60) for _ in range(N)]
        want = [sum(T[s][t] * vec[s] for s in range(N)) for t in range(N)]
        got = unpack(apply_T(pack(vec), m), N)
        assert got == want, "self-test failed at m=%d" % m
    print("self-test: lane sweep == dense matrix built from the definition for m = 3..8 (random 60-bit vectors)")

# ---------- dihedral orbits ----------
def orbit_reps(m):
    """list of (rep, images) with rep = minimum of the orbit, reps ascending"""
    N = 1 << m; mask = N - 1; seen = bytearray(N)
    revtab = [0] * (1 << 12)
    for v in range(1 << 12): revtab[v] = int(format(v, "012b")[::-1], 2)
    # simple, obviously correct reflection (bit i -> bit m-1-i) via the table on 12-bit chunks:
    def refl(s):
        r = 0
        for i in range(0, m, 12):
            w = min(12, m - i); c = (s >> i) & ((1 << w) - 1)
            rc = int(format(c, "0%db" % w)[::-1], 2) if w != 12 else revtab[c]
            r |= rc << (m - i - w)
        return r
    reps = []
    for s in range(N):
        if seen[s]: continue
        imgs = set(); t = s
        for _ in range(m):
            imgs.add(t); imgs.add(refl(t)); t = ((t << 1) | (t >> (m - 1))) & mask
        for t in imgs: seen[t] = 1
        reps.append((s, imgs))
    return reps

def load_parts():
    man = {}
    lines = open(os.path.join(HERE, "MANIFEST.txt")).read().split("\n")
    parts = []; whole = None; widths = []
    for ln in lines:
        f = ln.split()
        if not f: continue
        if f[0] == "part": parts.append((f[1], int(f[2]), f[3]))
        elif f[0] == "whole": whole = (int(f[1]), f[2])
        elif f[0] == "width": widths.append((int(f[1]), int(f[2])))   # width m, number of orbits
    data = b""
    for name, size, sha in parts:
        b = open(os.path.join(HERE, name), "rb").read()
        assert len(b) == size and size <= 900000 and hashlib.sha256(b).hexdigest() == sha, "bad part " + name
        data += b
    assert len(data) == whole[0] and hashlib.sha256(data).hexdigest() == whole[1], "bad whole-file hash"
    print("sha256 of %d parts and of the concatenation (%d bytes) verified" % (len(parts), len(data)))
    return data, widths

def dlog(fr):  return (Decimal(fr.numerator) / Decimal(fr.denominator)).ln()
def check_width(m, vec_bytes):
    t0 = time.time(); N = 1 << m
    reps = orbit_reps(m)
    assert len(vec_bytes) == ENTRY_BYTES * len(reps), "orbit count mismatch at m=%d: %d vs %d" % (m, len(vec_bytes) // ENTRY_BYTES, len(reps))
    buf = bytearray(N * (W // 8)); vals = []
    for k, (s, imgs) in enumerate(reps):
        v = int.from_bytes(vec_bytes[k * ENTRY_BYTES:(k + 1) * ENTRY_BYTES], "big")
        assert v > 0, "non-positive entry"
        vals.append(v); vb = v.to_bytes(W // 8, "little")
        for t in imgs: buf[t * (W // 8):(t + 1) * (W // 8)] = vb
    x = int.from_bytes(bytes(buf), "little"); del buf
    print("m=%d: %d orbits, vector expanded (%.0fs)" % (m, len(reps), time.time() - t0), flush=True)
    y = apply_T(x, m); del x
    yb = y.to_bytes(N * (W // 8), "little"); del y
    rmax = rmin = None
    for k, (s, imgs) in enumerate(reps):
        yi = int.from_bytes(yb[s * (W // 8):(s + 1) * (W // 8)], "little"); xi = vals[k]
        if rmax is None: rmax = rmin = (yi, xi); continue
        if yi * rmax[1] > rmax[0] * xi: rmax = (yi, xi)
        if yi * rmin[1] < rmin[0] * xi: rmin = (yi, xi)
    print("m=%d: exact Collatz-Wielandt  min y/x = %s...  max y/x = %s...  (%.0fs)" % (m, str(Decimal(rmin[0]) / Decimal(rmin[1]))[:30], str(Decimal(rmax[0]) / Decimal(rmax[1]))[:30], time.time() - t0), flush=True)
    return Fraction(*rmin), Fraction(*rmax)

def main():
    T0 = time.time()
    selftest()
    data, widths = load_parts()
    res = {}; off = 0
    for m, norb in widths:
        res[m] = check_width(m, data[off:off + norb * ENTRY_BYTES]); off += norb * ENTRY_BYTES
    assert off == len(data)
    eps = Decimal(10) ** -55
    M = 22; m2 = 22; p = 2
    upper = dlog(res[M][1]) / M + eps
    lower = (dlog(res[m2 + p][0]) - dlog(res[m2][1])) / p - eps
    print("\nTheorem U (M=%d even >= 4):  h2 <= ln(maxratio_%d)/%d      = %s" % (M, M, M, upper))
    print("Theorem L (2q=%d, p=%d, q>=2): h2 >= (ln(minratio_%d) - ln(maxratio_%d))/%d = %s" % (m2, p, m2 + p, m2, p, lower))
    q22 = Decimal(10) ** -22   # display: lower endpoint rounded down, upper rounded up
    print("ENCLOSURE  %s <= h2 <= %s   (width %.6E)" % (lower.quantize(q22, rounding=ROUND_FLOOR), upper.quantize(q22, rounding=ROUND_CEILING), upper - lower))
    lo_s, up_s = format(lower, ".40f"), format(upper, ".40f")
    d = 0
    while lo_s[d] == up_s[d]: d += 1
    print("common decimals of the two bounds: %d  -> h2 = %s...  certified" % (d - 2, lo_s[:d]))
    assert lower > Decimal("0.6627989728337") and upper < Decimal("0.6627989728338"), "13-decimal claim failed"
    print("CERTIFIED: 0.6627989728337 < h2 < 0.6627989728338  (13 decimals)")
    print("total runtime %.0f s" % (time.time() - T0))
main()
