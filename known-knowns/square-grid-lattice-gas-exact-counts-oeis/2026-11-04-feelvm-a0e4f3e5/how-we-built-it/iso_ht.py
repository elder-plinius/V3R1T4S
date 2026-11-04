"""Lens 2 (contrarian / second run): a(15) of OEIS A054759 via the H-TRACKED
encoding — a different state space than lens 1, as the bank's two-run rule
requires ("a different state encoding").

State space: 2^(n+1) states (s, c):
  s  = n vertical-edge bits between consecutive rows (same as lens 1),
  c  = the DIRECTION of the row's wrap horizontal edge H(i, n-1), carried
       EXPLICITLY instead of being integrated into the transfer element.
Transition, processing row i from (s_i, c_i) to (s_{i+1}, c_{i+1}):
  the h-walk  h[j] = h[j-1] + s_i[j] - s_{i+1}[j],  h[-1] = c_i,
  must satisfy h[j] in {0,1} for all j AND close: h[n-1] = c_i.
  c_{i+1} is the FREE wrap-edge choice for the next row (unconstrained here).
T2[(s,c)][(s',c')] = [walk from init c consistent], independent of c'.
Each Eulerian orientation maps to exactly one closed walk (c_i = direction of
H(i, n-1)), so Trace(T2^n) = a(n).  The transfer element here is built by an
independent per-row walk DFS, NOT by lens 1's flip-set enumeration.

Symmetry: rotation acts on the s-part (c invariant); orbits (O_s, c);
isotypic pointwise extraction as in lens 1 (fixed after the F_p pairing bug):
  M_k[(O',c')][(O,c)] = sum_{x in O_s} T2[(canon(O'), c')][(x, c)] * zeta^{k pos(x)}.
Trace(T2^n) = sum_k Trace(M_k^n) mod p; CRT over a prime set DISJOINT from lens 1.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np

_ISO = Path(__file__).resolve().parents[1]
sys_path0 = None


def rot_scalar(x, i, n):
    if i == 0:
        return x
    return ((x << i) | (x >> (n - i))) & ((1 << n) - 1)


def build_structure(n):
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    rots = np.empty((N, n), dtype=np.int64)
    rots[:, 0] = xs
    for i in range(1, n):
        rots[:, i] = ((xs << i) | (xs >> (n - i))) & (N - 1)
    canon = rots.min(axis=1)
    pos = np.argmax(rots == canon[:, None], axis=1).astype(np.int64)
    uniq, oidx = np.unique(canon, return_inverse=True)
    oidx = oidx.astype(np.int64)
    d = np.bincount(oidx, minlength=len(uniq)).astype(np.int64)
    assert d.sum() == N
    return canon, pos, oidx, d, len(uniq)


def t2_row_valid_sps(s, c, n):
    """All s' such that the h-walk from init c is consistent (independent DFS)."""
    out = []

    def walk(j, h_prev, sp):
        if j == n:
            if h_prev == c:
                out.append(sp)
            return
        sj = (s >> j) & 1
        for spj in (0, 1):
            h = h_prev + sj - spj
            if 0 <= h <= 1:
                walk(j + 1, h, sp | (spj << j))

    walk(0, c, 0)
    return out


def build_T2_coo(n):
    """Sparse T2 over 2^(n+1) states, rows (s,c), columns (s',c'), c' free."""
    canon, pos, oidx, d, Norb = build_structure(n)
    N = 1 << n
    state16 = N * 2
    rows_l, cols_l, vals_l = [], [], []
    # reference element for spot checks
    def t2_elem(row16, col16):
        s, c = row16 & (N - 1), row16 >> n
        sp, cp = col16 & (N - 1), col16 >> n
        h = c
        for j in range(n):
            h = h + ((s >> j) & 1) - ((sp >> j) & 1)
            if h not in (0, 1):
                return 0
        return 1 if h == c else 0

    for s in range(N):
        for c in (0, 1):
            row16 = s + (c << n)
            sps = t2_row_valid_sps(s, c, n)
            if not sps:
                continue
            sp_arr = np.array(sps, dtype=np.int64)
            for cp in (0, 1):
                cols = sp_arr + (cp << n)
                rows_l.append(np.full(len(cols), row16, dtype=np.int64))
                cols_l.append(cols)
                vals_l.append(np.ones(len(cols), dtype=np.int64))
    rows = np.concatenate(rows_l)
    cols = np.concatenate(cols_l)
    vals = np.concatenate(vals_l)
    assert len(rows) == len(np.unique(rows * state16 + cols))
    rng = np.random.default_rng(777)
    for _ in range(300):
        i = int(rng.integers(len(rows)))
        assert t2_elem(int(rows[i]), int(cols[i])) == int(vals[i])
    # full-row check on a few probe rows, vectorized (mask once per probe)
    probe_ok = 0
    for row16 in (0, 1, N, state16 - 1, 5, (7 << n) + 1 if n >= 3 else 1):
        if row16 >= state16:
            continue
        m = (rows == row16)
        got = {}
        for c_, col16 in zip(vals[m], cols[m]):
            got[int(col16)] = int(c_)
        for col16 in range(state16):
            assert t2_elem(row16, col16) == got.get(col16, 0)
        probe_ok += 1
    assert probe_ok >= 4
    return rows, cols, vals, (canon, pos, oidx, d, Norb)


def find_primitive_root(n, p):
    assert (p - 1) % n == 0
    if n == 1:
        return 1
    qs = set()
    m = n
    q = 2
    while q * q <= m:
        if m % q == 0:
            qs.add(q)
            while m % q == 0:
                m //= q
        q += 1
    if m > 1:
        qs.add(m)
    for c in range(2, 200):
        z = pow(c, (p - 1) // n, p)
        if z == 1:
            continue
        if all(pow(z, n // q, p) != 1 for q in qs):
            return z
    raise RuntimeError("no primitive root")


def make_pre2(struct, sp_arrays, n):
    """Pointwise scatter precomputation for the 2^(n+1) space.
    Only T2-rows at canonical states (canon(s), c) are needed."""
    canon, pos, oidx, d, Norb = struct
    rows, cols, vals = sp_arrays
    N = 1 << n
    oidx16 = oidx[rows & (N - 1)] + (rows >> n) * Norb     # orbit id of T2 row
    ocol16 = oidx[cols & (N - 1)] + (cols >> n) * Norb     # orbit id of T2 col
    Norb2 = 2 * Norb
    is_canon = np.zeros(N, dtype=bool)
    is_canon[np.unique(canon)] = True
    sel = is_canon[rows & (N - 1)]
    key = oidx16[sel].astype(np.int64) * Norb2 + ocol16[sel]
    order = np.argsort(key, kind="stable")
    keys = key[order]
    gst = np.concatenate([[0], np.where(np.diff(keys) != 0)[0] + 1]).astype(np.int64)
    pc = pos[cols[sel] & (N - 1)][order].copy()            # pos of column s-part, sorted
    v2 = vals[sel][order].astype(np.float64)
    return keys, gst, pc, v2, Norb2


def mm_mod(A, B, p):
    if p < 2 ** 15:
        assert A.shape[0] * A.max() * B.max() < 2 ** 53
        C = A @ B
        C %= p
        return C
    Ai = np.floor(A).astype(np.int64)
    Bi = np.floor(B).astype(np.int64)
    A0, A1 = (Ai & 0xFFFF).astype(np.float64), (Ai >> 16).astype(np.float64)
    B0, B1 = (Bi & 0xFFFF).astype(np.float64), (Bi >> 16).astype(np.float64)
    assert max(A0.shape[0] * max(A0.max(), 1) * max(B0.max(), 1),
               A0.shape[0] * max(A0.max(), 1) * max(B1.max(), 1),
               A0.shape[0] * max(A1.max(), 1) * max(B0.max(), 1),
               A0.shape[0] * max(A1.max(), 1) * max(B1.max(), 1)) < 2 ** 53
    M00 = (A0 @ B0) % p
    M01 = (A0 @ B1) % p
    M10 = (A1 @ B0) % p
    M11 = (A1 @ B1) % p
    C = (M00.astype(np.int64)
         + ((M01.astype(np.int64) + M10.astype(np.int64)) << 16)
         + M11.astype(np.int64) * pow(2, 32, p))
    C %= p
    return C.astype(np.float64)


def mod_trace_power(M, e, p):
    result = None
    sq = M
    while True:
        if e & 1:
            result = sq if result is None else mm_mod(result, sq, p)
        e >>= 1
        if e == 0:
            break
        sq = mm_mod(sq, sq, p)
    return int(round(np.trace(result))) % p


def isotypic_trace_mod2(n, p, struct, sp_arrays, pre=None, zeta=None):
    canon, pos, oidx, d, Norb = struct
    if zeta is None:
        zeta = find_primitive_root(n, p)
    assert pow(zeta, n, p) == 1
    if pre is None:
        pre = make_pre2(struct, sp_arrays, n)
    keys, gst, pc, v2, Norb2 = pre
    W = np.array([[pow(zeta, (k * m) % n, p) for m in range(n)] for k in range(n)],
                 dtype=np.float64)
    total = 0
    Ebuf = np.zeros(Norb2 * Norb2, dtype=np.float64)
    for k in range(n):
        part = np.array([(k % (n // dd)) == 0 for dd in d])
        idx = np.concatenate([part.nonzero()[0], part.nonzero()[0] + Norb])  # (O, c=0) and (O, c=1)
        if len(idx) == 0:
            continue
        vr = v2 * W[k][pc]
        sums = np.add.reduceat(vr, gst)
        Ebuf[:] = 0
        Ebuf[keys[gst]] = sums
        assert Ebuf.max() < 2 ** 53
        E = Ebuf.reshape(Norb2, Norb2) % p
        Mk = E[np.ix_(idx, idx)].copy()
        assert Mk.max() < 2 ** 15
        tr = mod_trace_power(Mk, n, p)
        total = (total + tr) % p
    return int(total), zeta


def crt(residues, primes):
    x, m = 0, 1
    for r, q in zip(residues, primes):
        t = ((r - x) % q) * pow(m % q, -1, q) % q
        x += m * t
        m *= q
    assert x < m
    return x, m


def primes_1mod(n, lo, hi, count, exclude=()):
    out = []
    c = lo + ((1 - lo) % n)
    for q in range(c, hi + 1, n):
        if q in exclude:
            continue
        if all(q % t for t in range(2, int(q ** 0.5) + 1)):
            out.append(q)
            if len(out) >= count:
                return out
    raise RuntimeError("not enough primes")


def primes_1mod_largest(n, hi, count, exclude=()):
    out = []
    start = hi - ((hi - 1) % n)
    for q in range(start, 1, -n):
        if q in exclude:
            continue
        if all(q % t for t in range(2, int(q ** 0.5) + 1)):
            out.append(q)
            if len(out) >= count:
                return out
    raise RuntimeError("not enough primes")


def bfile_terms(path):
    bf = {}
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        a, b = line.split()
        bf[int(a)] = int(b)
    return bf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["ladder", "n15", "prime"], required=True)
    ap.add_argument("--prime", type=int, default=None)
    ap.add_argument("--n", type=int, default=15)
    ap.add_argument("--exclude-primes", default="")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t0 = time.time()
    if args.mode == "prime":
        n, p = args.n, args.prime
        assert (p - 1) % n == 0 and p > 2 and all(p % t for t in range(2, int(p ** 0.5) + 1))
        rows, cols, vals, struct = build_T2_coo(n)
        tr, zeta = isotypic_trace_mod2(n, p, struct, (rows, cols, vals))
        print("n=%d prime=%d zeta=%d -> Trace(T2^n) mod p = %d" % (n, p, zeta, tr))
        print("claimed a(%d) mod p = %d" % (n, tr))
        return

    if args.mode == "ladder":
        bf = bfile_terms(str(_ISO.parent.parent / "data" / "A054759_b054759.txt.raw"))
        res = {}
        for n in range(1, 15):
            rows, cols, vals, struct = build_T2_coo(n)
            pn2 = primes_1mod(n, 101, 30000, 1)[0]
            iso, zeta = isotypic_trace_mod2(n, pn2, struct, (rows, cols, vals))
            ok = iso == bf[n] % pn2
            res[n] = {"bfile": bf[n], "isotypic_mod": iso, "prime": pn2,
                      "zeta": zeta, "matches": bool(ok)}
            print("n=%2d a=%d iso(p=%d,z=%d)=%d %s (%.1fs)" %
                  (n, bf[n], pn2, zeta, iso, "OK" if ok else "FAIL",
                   time.time() - t0), flush=True)
        with open(args.out or str(_ISO / "output" / "ladder2.json"), "w") as f:
            json.dump(res, f, indent=1)
        print("ladder2 done in %.1f s" % (time.time() - t0))
        return

    if args.mode == "n15":
        excl = {int(x) for x in args.exclude_primes.split(",") if x}
        rows, cols, vals, struct = build_T2_coo(15)
        print("T2 built: nnz=%d (%.1f s)" % (len(rows), time.time() - t0), flush=True)
        pre = make_pre2(struct, (rows, cols, vals), 15)
        print("pre done (%.1f s)" % (time.time() - t0), flush=True)
        P2 = primes_1mod_largest(15, 32749, 14, exclude=excl)
        print("primes (%d): %s" % (len(P2), P2), flush=True)
        resis = []
        for i, p in enumerate(P2):
            tr, zeta = isotypic_trace_mod2(15, p, struct, (rows, cols, vals), pre=pre)
            resis.append(tr)
            print("prime %2d/12 p=%d zeta=%d -> %d  (%.1f s)" %
                  (i + 1, p, zeta, tr, time.time() - t0), flush=True)
        x, m = crt(resis, P2)
        out = {"primes": P2, "residues": resis, "a15": x, "modulus": m}
        with open(args.out or str(_ISO / "output" / "run2_result.json"), "w") as f:
            json.dump(out, f, indent=1)
        print("a(15) candidate (run-2) = %d" % x)
        print("digits: %d ; ln(a)/225 = %.6f" % (len(str(x)), np.log(x) / 225.0), flush=True)


if __name__ == "__main__":
    main()
