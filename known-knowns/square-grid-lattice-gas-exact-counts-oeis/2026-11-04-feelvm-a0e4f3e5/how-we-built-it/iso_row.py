"""Lens 1 (extender): exact a(15) of OEIS A054759 via the row transfer matrix +
Z_n character (isotypic) decomposition + exact modular float64 matmul + CRT.

Model: Eulerian orientations of the n x n toroidal grid = square ice.
Row transfer matrix T over 2^n states (n vertical-edge bits between consecutive rows):
  T[s][s'] = # of valid h-row completions; ice rule h[j] = h[j-1] + s[j] - s'[j],
  h in {0,1}^n cyclic (h[-1] = h[n-1]).
  Flip-set form: D = {j: s[j] != s'[j]}; |D| odd -> 0; D empty -> 2;
  else 1 iff the s-values on D alternate cyclically.

Symmetry: T commutes with the cyclic bit-rotation P.  V = R^{2^n} splits into
isotypic components V_k = {v : P v = zeta^k v} (zeta a primitive n-th root,
taken mod p, requires p = 1 mod n); T preserves each V_k, hence
  Trace(T^n) = sum_k Trace((T|V_k)^n).
Basis of V_k: for each rotation orbit O (size d | n) with (n/d) | k,
  b_O = sum_{x in O} zeta^{k*pos(x)} e_x,  pos(x) = the j with rot^j(x) = canon(x);
P b_O = zeta^k b_O; supports disjoint; V_k is spanned by {b_O} because every
v in V_k has v(x) = f_O * zeta^{k pos(x)} on each orbit O.  Operator matrix in
this basis (pointwise extraction, valid over any field: evaluate T b_O at the
canonical state of O', whose pos = 0):
  T_k[O'][O] = (T b_O)(canon O') = sum_{x in O} T[canon(O')][x] * zeta^{k pos(x)}.
(NB: the sesquilinear pairing <b_O,b_O> = d that orthonormal-basis extractions
use has no conjugation over F_p; the bilinear self-pairing is
sum_x zeta^{2k pos(x)} = 0 in general, so the pointwise form is the one that
works mod p.  Verified against a complex projector computation at n = 3.)
Exactness: entries < p < 2^15; matmul partial sums < 2^15*2^15*dim < 2^53 ->
float64 exact; reduceat group sums < 225*2*p^2 < 2^40 exact.
CRT over ~12 primes of 15 bits -> exact integer Trace(T^15) = a(15).
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------- structure

def rot_scalar(x, i, n):
    if i == 0:
        return x
    return ((x << i) | (x >> (n - i))) & ((1 << n) - 1)


def build_structure(n):
    """canon (min over rotations), pos (j with rot^j(x)=canon), orbit index, sizes."""
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
    for i in range(len(uniq)):
        members = {rot_scalar(int(uniq[i]), j, n) for j in range(n)}
        assert len(members) == d[i], (i, len(members), d[i])
    return canon, pos, oidx, d, len(uniq)


# ------------------------------------------------------- transfer matrix (T)

def alt_masks(bits, n):
    """Nonempty flip sets D (masks) whose s-values alternate cyclically.
    Enumerated with p1 = min(D); DFS keeps the chain alternating and records at
    even depth (the cyclic closure last!=first is then automatic)."""
    masks = []

    def dfs(last, need, mask, depth):
        if depth >= 2 and depth % 2 == 0:
            masks.append(mask)
        for q in range(last + 1, n):
            if bits[q] == need:
                dfs(q, 1 - need, mask | (1 << q), depth + 1)

    for p1 in range(n):
        dfs(p1, 1 - bits[p1], 1 << p1, 1)
    return masks


def transfer_element(s, s_prime, n):
    """Reference scalar element (the n<=8-validated definition)."""
    flips = []
    for j in range(n):
        if ((s >> j) & 1) != ((s_prime >> j) & 1):
            flips.append((s >> j) & 1)
    k = len(flips)
    if k % 2:
        return 0
    if k == 0:
        return 2
    for i in range(k):
        if flips[i] == flips[(i + 1) % k]:
            return 0
    return 1


def build_T_coo(n):
    """Sparse T via orbit representatives + rotation translation."""
    canon, pos, oidx, d, Norb = build_structure(n)
    N = 1 << n
    full = N - 1
    rows_l, cols_l, vals_l = [], [], []
    for a in np.unique(canon):
        a = int(a)
        bits = [(a >> j) & 1 for j in range(n)]
        masks = alt_masks(bits, n)
        d_o = len({rot_scalar(a, j, n) for j in range(n)})
        if masks:
            marr = np.array(masks, dtype=np.int64)
            bases = a ^ marr
            for i in range(d_o):
                row = rot_scalar(a, i, n)
                if i == 0:
                    cols = bases.copy()
                else:
                    cols = ((bases << i) | (bases >> (n - i))) & full
                rows_l.append(np.full(len(cols), row, dtype=np.int64))
                cols_l.append(cols)
                vals_l.append(np.ones(len(cols), dtype=np.int64))
        for i in range(d_o):  # empty flip set: T[s][s] = 2
            row = rot_scalar(a, i, n)
            rows_l.append(np.array([row], dtype=np.int64))
            cols_l.append(np.array([row], dtype=np.int64))
            vals_l.append(np.array([2], dtype=np.int64))
    rows = np.concatenate(rows_l)
    cols = np.concatenate(cols_l)
    vals = np.concatenate(vals_l)
    assert len(rows) == len(np.unique(rows * N + cols))  # no duplicate entries
    # spot-check against the reference element on deterministic samples
    rng = np.random.default_rng(12345)
    for _ in range(300):
        i = int(rng.integers(len(rows)))
        assert transfer_element(int(rows[i]), int(cols[i]), n) == int(vals[i])
    probes = sorted({0, 1, N - 1, (N - 1) // 3} & set(range(N)))
    for s in probes:
        for sp in probes:
            want = transfer_element(s, sp, n)
            hit = (rows == s) & (cols == sp)
            assert hit.sum() == (1 if want else 0)
            if want:
                assert int(vals[hit][0]) == want
    return rows, cols, vals, (canon, pos, oidx, d, Norb)


def T_rowsum_inf(rows, vals, n):
    sums = np.bincount(rows, weights=vals, minlength=1 << n)
    return int(round(sums.max()))


# ------------------------------------------------- exact / direct modular

def exact_trace_int(n):
    """Exact integer Trace(T^n) via numpy int64 dense power (safe for n <= 7)."""
    N = 1 << n
    T = np.zeros((N, N), dtype=np.int64)
    for s in range(N):
        for sp in range(N):
            T[s, sp] = transfer_element(s, sp, n)
    P = np.eye(N, dtype=np.int64)
    for _ in range(n):
        P = P @ T
    return int(np.trace(P))


def direct_mod_trace(n, p, rows, cols, vals):
    """Trace(T^n) mod p via dense float64 modular matmul (no symmetry). n <= 14."""
    N = 1 << n
    Td = np.zeros((N, N), dtype=np.float64)
    Td[rows, cols] = vals
    assert Td.max() < 2 ** 15

    def mm(A, B):
        assert A.shape[0] * A.max() * B.max() < 2 ** 53
        C = A @ B
        C %= p
        return C

    result = None
    sq = Td
    e = n
    while True:
        if e & 1:
            result = sq if result is None else mm(result, sq)
        e >>= 1
        if e == 0:
            break
        sq = mm(sq, sq)
    return int(round(np.trace(result))) % p


# ------------------------------------------------------------- isotypic

def find_primitive_root(n, p):
    """Element of order exactly n in F_p^* (requires n | p-1)."""
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
    raise RuntimeError("no primitive root found")


def make_pre(struct, sp_arrays):
    """Precomputed scatter for the pointwise extraction: only T-rows at
    canonical states are needed.  E[O'][O] = sum_x T[canon(O')][x] * w[pos(x)]."""
    canon, pos, oidx, d, Norb = struct
    rows, cols, vals = sp_arrays
    is_canon = np.zeros(int(canon.max()) + 1, dtype=bool)
    is_canon[np.unique(canon)] = True
    sel = is_canon[rows]
    r2, c2, v2 = rows[sel], cols[sel], vals[sel]
    key = oidx[r2].astype(np.int64) * Norb + oidx[c2]   # E[O'][O]: O' = row orbit
    order = np.argsort(key, kind="stable")
    keys = key[order]
    gst = np.concatenate([[0], np.where(np.diff(keys) != 0)[0] + 1]).astype(np.int64)
    return (order, keys, gst, oidx[r2].copy(), oidx[c2].copy(),
            pos[c2][order].copy(), v2[order].astype(np.float64))


def isotypic_trace_mod(n, p, struct, sp_arrays, pre=None, zeta=None):
    """Trace(T^n) mod p via the Z_n isotypic decomposition."""
    canon, pos, oidx, d, Norb = struct
    if zeta is None:
        zeta = find_primitive_root(n, p)
    assert pow(zeta, n, p) == 1
    if pre is None:
        pre = make_pre(struct, sp_arrays)
    order, keys, gst, pc, vbase = pre[0], pre[1], pre[2], pre[5], pre[6]
    W = np.array([[pow(zeta, (k * m) % n, p) for m in range(n)] for k in range(n)],
                 dtype=np.float64)
    total = 0
    Ebuf = np.zeros(Norb * Norb, dtype=np.float64)
    for k in range(n):
        part = np.array([(k % (n // dd)) == 0 for dd in d])
        idx = np.where(part)[0]
        if len(idx) == 0:
            continue
        vr = vbase * W[k][pc]          # weight zeta^{k pos(x)} on the column state
        sums = np.add.reduceat(vr, gst)
        Ebuf[:] = 0
        Ebuf[keys[gst]] = sums
        assert Ebuf.max() < 2 ** 53
        E = Ebuf.reshape(Norb, Norb) % p
        Mk = E[np.ix_(idx, idx)].copy()
        assert Mk.max() < 2 ** 15
        tr = mod_trace_power(Mk, n, p)
        total = (total + tr) % p
    return int(total), zeta


def mm_mod(A, B, p):
    """Modular matmul, exact. Supports p < 2^31 via a 2-chunk (16-bit) split."""
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
    # elementwise int64 combination: (M01+M10) < 2^32, <<16 < 2^48; M11*(2^32%p) < 2^62
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
    c = lo + ((1 - lo) % n)  # smallest q >= lo with q = 1 (mod n)
    for q in range(c, hi + 1, n):
        if q in exclude:
            continue
        if all(q % t for t in range(2, int(q ** 0.5) + 1)):
            out.append(q)
            if len(out) >= count:
                return out
    raise RuntimeError("not enough primes")


def primes_1mod_largest(n, hi, count, exclude=()):
    """The `count` largest primes q = hi..2 with q = 1 (mod n), each ~log2(hi) bits."""
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


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["ladder", "n15", "prime"], required=True)
    ap.add_argument("--prime", type=int, default=None)
    ap.add_argument("--n", type=int, default=15)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t0 = time.time()
    if args.mode == "prime":
        n, p = args.n, args.prime
        assert (p - 1) % n == 0 and p > 2 and all(p % t for t in range(2, int(p ** 0.5) + 1))
        rows, cols, vals, struct = build_T_coo(n)
        tr, zeta = isotypic_trace_mod(n, p, struct, (rows, cols, vals))
        print("n=%d prime=%d zeta=%d -> Trace(T^n) mod p = %d" % (n, p, zeta, tr))
        print("claimed a(%d) mod p = %d" % (n, tr))
        return

    if args.mode == "ladder":
        _iso = Path(__file__).resolve().parents[1]
        bf = bfile_terms(str(_iso.parent.parent / "data" / "A054759_b054759.txt.raw"))
        res = {}
        for n in range(1, 15):
            rows, cols, vals, struct = build_T_coo(n)
            if n <= 7:
                ref, ref_kind = exact_trace_int(n), "exact_int"
            else:
                pn = primes_1mod(n, 17, 30000, 1)[0]
                ref, ref_kind = direct_mod_trace(n, pn, rows, cols, vals.astype(np.float64)), \
                    "direct_mod(p=%d)" % pn
            if n <= 7:
                assert ref == bf[n], (n, ref, bf[n])
            else:
                assert ref == bf[n] % pn, (n, ref, bf[n] % pn)
            pn2 = primes_1mod(n, 101, 30000, 1, exclude={pn if n > 7 else 0})[0]
            iso, zeta = isotypic_trace_mod(n, pn2, struct, (rows, cols, vals))
            ok = iso == bf[n] % pn2
            res[n] = {"bfile": bf[n], "ref": ref, "ref_kind": ref_kind,
                      "isotypic_mod": iso, "prime_iso": pn2, "zeta": zeta,
                      "isotypic_matches": bool(ok)}
            print("n=%2d ref(%s)=%d iso(p=%d,z=%d)=%d %s (%.1fs)" %
                  (n, ref_kind, ref, pn2, zeta, iso, "OK" if ok else "FAIL",
                   time.time() - t0), flush=True)
        with open(args.out or str(Path(__file__).resolve().parents[1] / "output" / "ladder.json"), "w") as f:
            json.dump(res, f, indent=1)
        print("ladder done in %.1f s" % (time.time() - t0))
        return

    if args.mode == "n15":
        rows, cols, vals, struct = build_T_coo(15)
        canon, pos, oidx, d, Norb = struct
        rinf = T_rowsum_inf(rows, vals, 15)
        bound = (1 << 15) * rinf ** 15  # rigorous: Trace <= N * ||T||_inf^15
        print("||T||_inf = %d ; rigorous bound a(15) <= 2^15*||T||^15 = 2^%.1f"
              % (rinf, math.log2(bound)), flush=True)
        need = math.log2(bound) + 20  # PREREG margin: modulus >= bound * 1e6
        npr = int(math.ceil(need / math.log2(32749))) + 1
        P1 = primes_1mod_largest(15, 32749, npr)
        print("primes (%d): %s" % (len(P1), P1), flush=True)
        pre = make_pre(struct, (rows, cols, vals))
        resis = []
        for i, p in enumerate(P1):
            tr, zeta = isotypic_trace_mod(15, p, struct, (rows, cols, vals), pre=pre)
            resis.append(tr)
            print("prime %2d/%d p=%d zeta=%d -> %d  (%.1f s)" %
                  (i + 1, len(P1), p, zeta, tr, time.time() - t0), flush=True)
        x, m = crt(resis, P1)
        print("CRT modulus 2^%.1f vs bound 2^%.1f -> %s" %
              (math.log2(m), math.log2(bound), "OK" if m > bound else "TOO SMALL"))
        out = {"primes": P1, "residues": resis, "a15": x, "modulus": m,
               "rowsum_inf": rinf, "bound": int(bound)}
        with open(args.out or str(Path(__file__).resolve().parents[1] / "output" / "run1_result.json"), "w") as f:
            json.dump(out, f, indent=1)
        print("a(15) candidate = %d" % x)
        print("digits: %d ; ln(a)/225 = %.6f (Lieb limit 0.431523)" %
              (len(str(x)), np.log(x) / 225.0), flush=True)


if __name__ == "__main__":
    main()
